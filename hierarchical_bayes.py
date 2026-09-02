"""
hierarchical_bayes.py
PyMC-based hierarchical Bayesian depreciation model.

ALTERNATIVE fitting path that replaces or supplements the scipy-based
tier 1/2/3 system in depreciation_curves.py.

Model specification (per segment):
    mu_floor_seg   ~ HalfNormal(0.3)
    sigma_floor_seg ~ HalfNormal(0.15)
    mu_k_seg       ~ HalfNormal(0.03)
    sigma_k_seg    ~ HalfNormal(0.015)
    floor_i        ~ TruncatedNormal(mu_floor_seg, sigma_floor_seg, 0.001, 0.80)
    k_i            ~ TruncatedNormal(mu_k_seg, sigma_k_seg, 0.005, 0.25)
    sigma_obs      ~ HalfNormal(0.1)
    y_it           ~ Normal(floor_i + (1 - floor_i) * exp(-k_i * t_it), sigma_obs)

Produces the same output columns as curve_fit_results.csv.

Usage:
    python3 hierarchical_bayes.py
"""

import os
import sys
import warnings
import traceback

import numpy as np
import pandas as pd

# ── Imports from the existing pipeline ─────────────────────────────────────────

from depreciation_curves import (
    build_extended_monthly,
    exp_floor,
    CURVE_TIMES,
    GPU_SEGMENTS,
    gpu_segment,
    KEEPA_MONTHLY_PATH,
    TARGET_AGE,
)
from data_prep import load_data, load_datacenter_supplement

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="pymc")
warnings.filterwarnings("ignore", category=UserWarning, module="pytensor")
warnings.filterwarnings("ignore", category=RuntimeWarning)

# ── Constants ──────────────────────────────────────────────────────────────────

MCMC_DRAWS       = 2000
MCMC_TUNE        = 1000
MCMC_CHAINS      = 2
MCMC_CORES       = 1
TARGET_ACCEPT    = 0.9
RANDOM_SEED      = 42
MIN_OBS_PER_GPU  = 3    # GPUs with fewer obs still participate via shrinkage
OUTPUT_PATH      = "outputs/hierarchical_bayes_results.csv"
SCIPY_RESULTS    = "outputs/curve_fit_results.csv"


# ── Half-life helpers (mirrored from depreciation_curves.py) ───────────────────

def _half_life_exp(floor, k):
    """Months until exp_floor crosses price_ratio = 0.5."""
    if floor >= 0.5 or k <= 0:
        return np.nan
    return -np.log((0.5 - floor) / (1.0 - floor)) / k


def _half_life_from_curve(curve):
    """Months until the projected curve dict crosses price_ratio = 0.5."""
    cts = sorted(ct for ct in CURVE_TIMES if not np.isnan(curve.get(ct, np.nan)))
    for j in range(1, len(cts)):
        v_prev, v_cur = curve[cts[j - 1]], curve[cts[j]]
        if v_prev >= 0.5 and v_cur < 0.5:
            hl = float(cts[j - 1] + (cts[j] - cts[j - 1]) * (v_prev - 0.5) / (v_prev - v_cur))
            return hl if hl > 1.0 else float(np.nan)
    return float(np.nan)


def _hpd_interval(samples, credible_mass=0.95):
    """Highest Posterior Density interval."""
    sorted_s = np.sort(samples)
    n = len(sorted_s)
    interval_size = int(np.ceil(credible_mass * n))
    if interval_size >= n:
        return float(sorted_s[0]), float(sorted_s[-1])
    widths = sorted_s[interval_size:] - sorted_s[:n - interval_size]
    best = int(np.argmin(widths))
    return float(sorted_s[best]), float(sorted_s[best + interval_size])


# ── Data preparation ──────────────────────────────────────────────────────────

def prepare_segment_data(monthly, segment_name):
    """
    Extract (gpu_name, age_months, price_ratio) observations for all GPUs
    in a given segment.

    Returns:
        gpu_names: sorted list of GPU names in the segment
        gpu_idx:   integer array mapping each observation to a GPU index
        t_obs:     float array of age_months for each observation
        y_obs:     float array of price_ratio for each observation
        gpu_n_obs: dict mapping gpu_name -> number of observations
    """
    seg_gpus = set(GPU_SEGMENTS.get(segment_name, []))

    gpu_names = []
    gpu_idx_list = []
    t_list = []
    y_list = []
    gpu_n_obs = {}

    # Collect all GPUs that belong to this segment and appear in the monthly data
    for gpu in sorted(seg_gpus):
        grp = monthly[monthly["gpu_name"] == gpu].sort_values("age_months").dropna(
            subset=["age_months", "price_ratio"]
        )
        if len(grp) == 0:
            continue

        # Filter to plausible depreciation range
        grp = grp[(grp["price_ratio"] > 0.03) & (grp["price_ratio"] <= 1.5)]
        if len(grp) == 0:
            continue

        idx = len(gpu_names)
        gpu_names.append(gpu)
        n = len(grp)
        gpu_n_obs[gpu] = n

        gpu_idx_list.extend([idx] * n)
        t_list.extend(grp["age_months"].values)
        y_list.extend(grp["price_ratio"].values)

    if not gpu_names:
        return None, None, None, None, None

    return (
        gpu_names,
        np.array(gpu_idx_list, dtype=int),
        np.array(t_list, dtype=float),
        np.array(y_list, dtype=float),
        gpu_n_obs,
    )


# ── PyMC model construction and sampling ──────────────────────────────────────

def fit_segment_hierarchical(gpu_names, gpu_idx, t_obs, y_obs, gpu_n_obs,
                             segment_name):
    """
    Build and sample the hierarchical Bayesian depreciation model for one segment.

    Returns:
        trace: arviz InferenceData with posterior samples
        None if sampling fails
    """
    import pymc as pm

    n_gpus = len(gpu_names)
    print(f"\n  [{segment_name}] Building model: {n_gpus} GPUs, "
          f"{len(t_obs)} total observations")

    with pm.Model() as model:
        # ── Segment-level hyperpriors ──────────────────────────────────────
        mu_floor_seg = pm.HalfNormal("mu_floor_seg", sigma=0.3)
        sigma_floor_seg = pm.HalfNormal("sigma_floor_seg", sigma=0.15)
        mu_k_seg = pm.HalfNormal("mu_k_seg", sigma=0.03)
        sigma_k_seg = pm.HalfNormal("sigma_k_seg", sigma=0.015)

        # ── GPU-level parameters (partial pooling) ─────────────────────────
        floor_i = pm.TruncatedNormal(
            "floor_i", mu=mu_floor_seg, sigma=sigma_floor_seg,
            lower=0.001, upper=0.80, shape=n_gpus,
        )
        k_i = pm.TruncatedNormal(
            "k_i", mu=mu_k_seg, sigma=sigma_k_seg,
            lower=0.005, upper=0.25, shape=n_gpus,
        )

        # ── Observation noise ──────────────────────────────────────────────
        sigma_obs = pm.HalfNormal("sigma_obs", sigma=0.1)

        # ── Deterministic mean function ────────────────────────────────────
        floor_obs = floor_i[gpu_idx]
        k_obs = k_i[gpu_idx]
        import pytensor.tensor as pt
        mu = floor_obs + (1.0 - floor_obs) * pt.exp(-k_obs * t_obs)

        # ── Likelihood ─────────────────────────────────────────────────────
        pm.Normal("y_obs", mu=mu, sigma=sigma_obs, observed=y_obs)

    # ── Sample ─────────────────────────────────────────────────────────────
    print(f"  [{segment_name}] Sampling: {MCMC_DRAWS} draws, {MCMC_TUNE} tune, "
          f"{MCMC_CHAINS} chains ...")

    with model:
        trace = pm.sample(
            draws=MCMC_DRAWS,
            tune=MCMC_TUNE,
            chains=MCMC_CHAINS,
            cores=MCMC_CORES,
            target_accept=TARGET_ACCEPT,
            random_seed=RANDOM_SEED,
            progressbar=True,
            return_inferencedata=True,
        )

    # Print convergence diagnostics
    import arviz as az
    summary = az.summary(trace, var_names=["mu_floor_seg", "mu_k_seg",
                                            "sigma_floor_seg", "sigma_k_seg",
                                            "sigma_obs"])
    print(f"\n  [{segment_name}] Hyperparameter summary:")
    print(summary.to_string())

    # Check r_hat for floor_i and k_i
    floor_rhat = az.rhat(trace, var_names=["floor_i"])["floor_i"].values
    k_rhat = az.rhat(trace, var_names=["k_i"])["k_i"].values
    max_rhat = max(np.nanmax(floor_rhat), np.nanmax(k_rhat))
    print(f"  [{segment_name}] Max r_hat across GPU params: {max_rhat:.3f}")
    if max_rhat > 1.05:
        print(f"  [{segment_name}] WARNING: r_hat > 1.05 indicates "
              f"convergence issues for some GPUs")

    return trace


# ── Posterior predictive extraction ───────────────────────────────────────────

def extract_gpu_results(trace, gpu_names, gpu_n_obs, segment_name, monthly):
    """
    From the posterior trace, compute projections and summary statistics
    for each GPU in the segment.

    Returns a list of row dicts matching the curve_fit_results.csv schema.
    """
    # Stack chains: shape (n_draws * n_chains, n_gpus)
    floor_samples = trace.posterior["floor_i"].values.reshape(-1, len(gpu_names))
    k_samples = trace.posterior["k_i"].values.reshape(-1, len(gpu_names))
    n_posterior = floor_samples.shape[0]

    t_arr = np.array(CURVE_TIMES, dtype=float)
    target_idx = CURVE_TIMES.index(TARGET_AGE)
    rows = []

    for i, gpu in enumerate(gpu_names):
        # Posterior samples for this GPU
        fl_s = floor_samples[:, i]  # shape (n_posterior,)
        k_s = k_samples[:, i]      # shape (n_posterior,)

        # Posterior predictive at each CURVE_TIME
        # Shape: (n_posterior, len(CURVE_TIMES))
        proj = fl_s[:, None] + (1.0 - fl_s[:, None]) * np.exp(
            -k_s[:, None] * t_arr[None, :]
        )
        proj = np.clip(proj, 0.0, 3.0)

        # Anchor to current market price if available
        grp = monthly[monthly["gpu_name"] == gpu].sort_values("age_months").dropna(
            subset=["age_months", "price_ratio"]
        )
        current_ratio = np.nan
        if len(grp) >= 1:
            current_ratio = float(grp.tail(3)["price_ratio"].median())
            t_last = float(grp["age_months"].values[-1])
            # Canonical posterior value at the current age
            canon_now = fl_s + (1.0 - fl_s) * np.exp(-k_s * t_last)
            scale = np.where(canon_now > 0, current_ratio / canon_now, 1.0)
            scale = np.clip(scale, 0.5, 2.0)
            proj = proj * scale[:, None]
            proj = np.clip(proj, 0.0, 3.0)

        # Summary statistics at target (t=60)
        col = proj[:, target_idx]
        point = float(np.median(col))
        hpd_lo, hpd_hi = _hpd_interval(col)
        sigma_yr5 = float(np.std(col))
        p_below_10 = float(np.mean(col < 0.10))

        # Full curve (median at each time point, monotonicity enforced)
        curve_raw = {ct: float(np.median(proj[:, j]))
                     for j, ct in enumerate(CURVE_TIMES)}
        curve = {}
        prev = curve_raw[CURVE_TIMES[0]]
        for ct in CURVE_TIMES:
            v = min(curve_raw[ct], prev)
            curve[ct] = v
            prev = v
        # Ensure proj_t60 == point (the median at target)
        curve[CURVE_TIMES[target_idx]] = point
        for idx_back in range(target_idx, 0, -1):
            if curve[CURVE_TIMES[idx_back - 1]] < curve[CURVE_TIMES[idx_back]]:
                curve[CURVE_TIMES[idx_back - 1]] = curve[CURVE_TIMES[idx_back]]

        # Per-time-point CIs and sigma
        ci_lo_curve = {}
        ci_hi_curve = {}
        sigma_curve = {}
        for j, ct in enumerate(CURVE_TIMES):
            lo, hi = _hpd_interval(proj[:, j])
            ci_lo_curve[ct] = lo
            ci_hi_curve[ct] = hi
            sigma_curve[ct] = float(np.std(proj[:, j]))

        # Half-life from the median posterior params
        fl_median = float(np.median(fl_s))
        k_median = float(np.median(k_s))
        half_life = _half_life_exp(fl_median, k_median)
        # Fallback: interpolate from curve if analytic half-life is NaN
        if np.isnan(half_life):
            half_life = _half_life_from_curve(curve)

        # Metadata
        n_months = gpu_n_obs.get(gpu, 0)
        if len(grp) > 0:
            age_min = float(grp["age_months"].min())
            age_max = float(grp["age_months"].max())
            age_range = f"{age_min:.0f}-{age_max:.0f}"
        else:
            age_range = "n/a"

        appreciating = (current_ratio > 1.2) if not np.isnan(current_ratio) else False
        ci_width = hpd_hi - hpd_lo

        # Confidence flag (same logic as depreciation_curves.py)
        age_span = 0
        if "-" in str(age_range):
            parts = str(age_range).split("-")
            try:
                age_span = float(parts[-1]) - float(parts[0])
            except ValueError:
                age_span = 0
        sparse_data = (n_months < 12) or (age_span < 18)
        if appreciating:
            conf_flag = "LOW"
        elif sparse_data:
            conf_flag = "MEDIUM" if ci_width < 0.15 else "LOW"
        else:
            conf_flag = "HIGH" if ci_width < 0.15 else "MEDIUM" if ci_width < 0.35 else "LOW"

        rows.append({
            "gpu_name":         gpu,
            "segment":          segment_name,
            "fit_tier":         "bayes",
            "n_months":         n_months,
            "age_range_months": age_range,
            "current_ratio":    current_ratio,
            "appreciating":     appreciating,
            "is_shock":         False,
            "method":           "hierarchical_bayes",
            "best_model":       "exp_floor_hierarchical",
            "best_r2":          np.nan,
            "w_exp_floor":      np.nan,
            "w_power_floor":    np.nan,
            "proj_yr5_ratio":   point,
            "proj_ci_lo":       hpd_lo,
            "proj_ci_hi":       hpd_hi,
            "ci_width":         ci_width,
            "sigma_yr5":        sigma_yr5,
            "p_below_10pct":    p_below_10,
            **{f"proj_t{ct}": curve.get(ct, np.nan) for ct in CURVE_TIMES},
            **{f"ci_lo_t{ct}": ci_lo_curve.get(ct, np.nan) for ct in CURVE_TIMES},
            **{f"ci_hi_t{ct}": ci_hi_curve.get(ct, np.nan) for ct in CURVE_TIMES},
            **{f"sigma_t{ct}": sigma_curve.get(ct, np.nan) for ct in CURVE_TIMES},
            "conf_flag":        conf_flag,
            "half_life_months": half_life,
            "floor_posterior_median": fl_median,
            "k_posterior_median":     k_median,
            "floor_posterior_std":    float(np.std(fl_s)),
            "k_posterior_std":        float(np.std(k_s)),
        })

    return rows


# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_hierarchical_bayes(df=None, keepa_monthly=None, verbose=True):
    """
    Run the full hierarchical Bayes depreciation pipeline.

    Can be called standalone or from the main pipeline.

    Args:
        df: DataFrame from load_data(). If None, loads automatically.
        keepa_monthly: DataFrame of Keepa monthly data. If None, loads automatically.
        verbose: print progress info.

    Returns:
        DataFrame with same columns as curve_fit_results.csv, plus
        floor_posterior_median, k_posterior_median, floor_posterior_std,
        k_posterior_std.
    """
    import pymc as pm

    if verbose:
        print("=" * 70)
        print("HIERARCHICAL BAYESIAN DEPRECIATION MODEL")
        print(f"PyMC version: {pm.__version__}")
        print(f"MCMC: {MCMC_DRAWS} draws, {MCMC_TUNE} tune, "
              f"{MCMC_CHAINS} chains, target_accept={TARGET_ACCEPT}")
        print("=" * 70)

    # ── Load data if not provided ──────────────────────────────────────────
    if df is None:
        if verbose:
            print("\nLoading data ...")
        df = load_data(verbose=False)

    if keepa_monthly is None:
        if os.path.exists(KEEPA_MONTHLY_PATH):
            keepa_monthly = pd.read_csv(KEEPA_MONTHLY_PATH)
            if verbose:
                print(f"Loaded {len(keepa_monthly)} Keepa monthly observations")
        else:
            if verbose:
                print("No Keepa monthly data found; using retail data only")

    # Load optional datacenter supplement
    supp_monthly = load_datacenter_supplement(verbose=verbose)
    if supp_monthly is not None and keepa_monthly is not None:
        keepa_monthly = pd.concat([keepa_monthly, supp_monthly], ignore_index=True)
    elif supp_monthly is not None:
        keepa_monthly = supp_monthly

    # ── Build extended monthly data ────────────────────────────────────────
    if verbose:
        print("\nBuilding extended monthly data ...")
    monthly = build_extended_monthly(df, keepa_monthly)
    if verbose:
        n_gpus_total = monthly["gpu_name"].nunique()
        print(f"  {len(monthly)} monthly observations across {n_gpus_total} GPUs")

    # ── Fit each segment ───────────────────────────────────────────────────
    all_rows = []
    segments_to_fit = ["DATACENTER", "CONSUMER", "WORKSTATION"]

    for seg in segments_to_fit:
        if verbose:
            print(f"\n{'='*60}")
            print(f"SEGMENT: {seg}")
            print(f"{'='*60}")

        result = prepare_segment_data(monthly, seg)
        gpu_names, gpu_idx, t_obs, y_obs, gpu_n_obs = result

        if gpu_names is None or len(gpu_names) == 0:
            if verbose:
                print(f"  [{seg}] No GPUs with data in this segment, skipping")
            continue

        if verbose:
            sparse = sum(1 for g in gpu_names if gpu_n_obs.get(g, 0) < MIN_OBS_PER_GPU)
            print(f"  [{seg}] {len(gpu_names)} GPUs "
                  f"({sparse} with <{MIN_OBS_PER_GPU} obs, will shrink to segment mean)")

        try:
            trace = fit_segment_hierarchical(
                gpu_names, gpu_idx, t_obs, y_obs, gpu_n_obs, seg
            )
        except Exception as e:
            print(f"  [{seg}] MCMC sampling FAILED: {e}")
            traceback.print_exc()
            continue

        if trace is None:
            print(f"  [{seg}] MCMC returned no trace, skipping")
            continue

        # Extract per-GPU results from posterior
        seg_rows = extract_gpu_results(
            trace, gpu_names, gpu_n_obs, seg, monthly
        )
        all_rows.extend(seg_rows)

        if verbose:
            print(f"\n  [{seg}] Extracted results for {len(seg_rows)} GPUs")

    results = pd.DataFrame(all_rows)

    if verbose and len(results) > 0:
        print(f"\n{'='*70}")
        print(f"HIERARCHICAL BAYES COMPLETE: {len(results)} GPUs fitted")
        print(f"{'='*70}")

    return results


def print_comparison_table(bayes_results):
    """
    Print a comparison table: hierarchical Bayes TVR vs scipy TVR
    for datacenter GPUs.
    """
    if not os.path.exists(SCIPY_RESULTS):
        print(f"\nNo scipy results found at {SCIPY_RESULTS}, skipping comparison")
        return

    scipy_df = pd.read_csv(SCIPY_RESULTS)
    dc_bayes = bayes_results[bayes_results["segment"] == "DATACENTER"].copy()

    if len(dc_bayes) == 0:
        print("\nNo DATACENTER GPUs in hierarchical Bayes results")
        return

    # Merge on gpu_name
    merged = dc_bayes[["gpu_name", "proj_yr5_ratio", "proj_ci_lo", "proj_ci_hi",
                         "sigma_yr5", "half_life_months",
                         "floor_posterior_median", "k_posterior_median"]].merge(
        scipy_df[["gpu_name", "proj_yr5_ratio", "proj_ci_lo", "proj_ci_hi",
                   "sigma_yr5", "fit_tier"]].rename(columns={
            "proj_yr5_ratio": "scipy_tvr",
            "proj_ci_lo": "scipy_ci_lo",
            "proj_ci_hi": "scipy_ci_hi",
            "sigma_yr5": "scipy_sigma",
        }),
        on="gpu_name", how="left",
    )

    merged["tvr_diff"] = merged["proj_yr5_ratio"] - merged["scipy_tvr"]
    merged = merged.sort_values("proj_yr5_ratio")

    print("\n" + "=" * 110)
    print("COMPARISON: Hierarchical Bayes vs Scipy (DATACENTER GPUs)")
    print("=" * 110)
    print(f"{'GPU':<30s}  {'Bayes TVR':>9s}  {'Scipy TVR':>9s}  {'Diff':>7s}  "
          f"{'Bayes CI':>15s}  {'Scipy CI':>15s}  "
          f"{'Floor':>6s}  {'k':>6s}  {'Tier':>4s}")
    print("-" * 110)

    for _, row in merged.iterrows():
        scipy_tvr_str = f"{row['scipy_tvr']:.3f}" if pd.notna(row["scipy_tvr"]) else "n/a"
        scipy_ci_str = (f"[{row['scipy_ci_lo']:.3f}, {row['scipy_ci_hi']:.3f}]"
                        if pd.notna(row["scipy_ci_lo"]) else "n/a")
        diff_str = f"{row['tvr_diff']:+.3f}" if pd.notna(row["tvr_diff"]) else "n/a"
        tier_str = str(int(row["fit_tier"])) if pd.notna(row.get("fit_tier")) else "n/a"

        print(f"{row['gpu_name']:<30s}  "
              f"{row['proj_yr5_ratio']:9.3f}  "
              f"{scipy_tvr_str:>9s}  "
              f"{diff_str:>7s}  "
              f"[{row['proj_ci_lo']:.3f}, {row['proj_ci_hi']:.3f}]  "
              f"{scipy_ci_str:>15s}  "
              f"{row['floor_posterior_median']:6.3f}  "
              f"{row['k_posterior_median']:6.4f}  "
              f"{tier_str:>4s}")

    print("-" * 110)

    # Summary statistics
    valid = merged.dropna(subset=["tvr_diff"])
    if len(valid) > 0:
        print(f"\nMean absolute TVR difference: {valid['tvr_diff'].abs().mean():.4f}")
        print(f"Max absolute TVR difference:  {valid['tvr_diff'].abs().max():.4f}")
        print(f"Correlation (Bayes vs Scipy): "
              f"{valid['proj_yr5_ratio'].corr(valid['scipy_tvr']):.3f}")


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        os.makedirs("outputs", exist_ok=True)

        results = run_hierarchical_bayes(verbose=True)

        if len(results) > 0:
            results.to_csv(OUTPUT_PATH, index=False)
            print(f"\nSaved -> {OUTPUT_PATH}")
            print(f"Total GPUs: {len(results)}")

            # Print datacenter comparison
            print_comparison_table(results)
        else:
            print("\nNo results produced. Check errors above.")
            sys.exit(1)

    except ImportError as e:
        print(f"\nImport error: {e}")
        print("Ensure PyMC 5.12+ is installed: pip install pymc>=5.12")
        sys.exit(1)
    except Exception as e:
        print(f"\nHierarchical Bayes pipeline failed: {e}")
        traceback.print_exc()
        sys.exit(1)
