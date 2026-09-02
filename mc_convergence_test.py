#!/usr/bin/env python3
"""
MC Convergence Test: Is 2000 MC samples enough for stable CI estimation?

For 5 representative GPUs (one per fitting pathway), this script:
  1. Re-runs MC at 2000 vs 10000 samples and compares percentile estimates at t=60.
  2. Runs 2000 samples 10 times with different seeds and measures the coefficient
     of variation (CV) of the 2.5th and 97.5th percentiles across runs.
  3. Reports whether 2000-sample CIs are stable enough for practical use.
"""

import os
import sys
import hashlib
import numpy as np
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from depreciation_curves import (
    load_data, build_extended_monthly, fit_all_gpus,
    fit_model, fit_segment_canonical, fit_constrained_floor,
    _mc_from_ensemble, _mc_from_constrained, _mc_to_stats, _synthetic_fit,
    _segment_floor_prior,
    MODELS, CURVE_TIMES, TARGET_AGE, MC_SAMPLES, KEEPA_MONTHLY_PATH,
    GPU_SEGMENTS, gpu_segment, exp_floor, SEG_K_FALLBACK,
    TIER1_MIN_MONTHS, TIER1_MAX_MIN_AGE, MIN_MONTHS_DATA,
)
from data_prep import load_data as dp_load_data, load_datacenter_supplement

# ── Load data (same pipeline as depreciation_curves main) ────────────────────
print("Loading data ...")
df = dp_load_data(verbose=False)

keepa_monthly = None
if os.path.exists(KEEPA_MONTHLY_PATH):
    keepa_monthly = pd.read_csv(KEEPA_MONTHLY_PATH)
    print(f"  Loaded {len(keepa_monthly)} Keepa monthly obs")

supp_monthly = load_datacenter_supplement(verbose=False)
if supp_monthly is not None and keepa_monthly is not None:
    keepa_monthly = pd.concat([keepa_monthly, supp_monthly], ignore_index=True)
elif supp_monthly is not None:
    keepa_monthly = supp_monthly

monthly = build_extended_monthly(df, keepa_monthly)
print(f"  Extended monthly: {len(monthly)} rows\n")

# ── Load existing results to identify representative GPUs ─────────────────────
results = pd.read_csv("outputs/curve_fit_results.csv")

# Select 5 representative GPUs (one per pathway)
# 1) Tier 1 fitted: GeForce RTX 3090 (CONSUMER, long history, individual fit)
# 2) Tier 1 observed: A10 (DATACENTER, observed method)
# 3) Tier 2 constrained: H100 SXM5 80 GB (DATACENTER, constrained)
# 4) Tier 3 segment_default: Tesla V100 FHHL (DATACENTER, segment default)
# 5) Demand-shock: GeForce RTX 4090 (CONSUMER, is_shock=True)

# Find actual GPUs for each pathway from results
tier1_fitted = results[(results["fit_tier"] == 1) & (results["method"] == "fitted")]
tier1_observed = results[(results["fit_tier"] == 1) & (results["method"] == "observed")]
tier2_constrained = results[(results["fit_tier"] == 2) & (results["method"] == "constrained")]
tier3_default = results[(results["fit_tier"] == 3) & (results["method"] == "segment_default")]
shock_gpus = results[results["is_shock"] == True]

# Pick one from each
test_gpus = {}
if len(tier1_fitted) > 0:
    # Prefer GeForce RTX 3090 if available; otherwise first
    if "GeForce RTX 3090" in tier1_fitted["gpu_name"].values:
        test_gpus["Tier1_fitted"] = "GeForce RTX 3090"
    else:
        test_gpus["Tier1_fitted"] = tier1_fitted.iloc[0]["gpu_name"]

if len(tier1_observed) > 0:
    if "T4" in tier1_observed["gpu_name"].values:
        test_gpus["Tier1_observed"] = "T4"
    elif "A10" in tier1_observed["gpu_name"].values:
        test_gpus["Tier1_observed"] = "A10"
    else:
        test_gpus["Tier1_observed"] = tier1_observed.iloc[0]["gpu_name"]

if len(tier2_constrained) > 0:
    if "H100 SXM5 80 GB" in tier2_constrained["gpu_name"].values:
        test_gpus["Tier2_constrained"] = "H100 SXM5 80 GB"
    else:
        test_gpus["Tier2_constrained"] = tier2_constrained.iloc[0]["gpu_name"]

if len(tier3_default) > 0:
    if "Tesla V100 FHHL" in tier3_default["gpu_name"].values:
        test_gpus["Tier3_segment_default"] = "Tesla V100 FHHL"
    else:
        test_gpus["Tier3_segment_default"] = tier3_default.iloc[0]["gpu_name"]

if len(shock_gpus) > 0:
    if "GeForce RTX 4090" in shock_gpus["gpu_name"].values:
        test_gpus["Demand_shock"] = "GeForce RTX 4090"
    elif "AMD Instinct MI300X" in shock_gpus["gpu_name"].values:
        test_gpus["Demand_shock"] = "AMD Instinct MI300X"
    else:
        test_gpus["Demand_shock"] = shock_gpus.iloc[0]["gpu_name"]

print("=" * 80)
print("SELECTED TEST GPUs")
print("=" * 80)
for label, gpu in test_gpus.items():
    row = results[results["gpu_name"] == gpu].iloc[0]
    print(f"  {label:25s} -> {gpu:30s}  (tier={row['fit_tier']}, method={row['method']}, "
          f"segment={row['segment']}, shock={row['is_shock']})")
print()

# ── Pre-compute segment canonicals and floor priors ──────────────────────────
print("Fitting segment canonical curves ...")
canonical = {}
for seg in GPU_SEGMENTS:
    result, anchors = fit_segment_canonical(monthly, seg)
    canonical[seg] = result
    if result is not None:
        print(f"  [{seg}] k={result['params'][1]:.4f}  floor={result['params'][0]:.3f}")
if "UNKNOWN" not in canonical or canonical.get("UNKNOWN") is None:
    fb = SEG_K_FALLBACK.get("UNKNOWN", (0.020, 0.25))
    canonical["UNKNOWN"] = _synthetic_fit(fb[0], fb[1], 12)

print("\nComputing empirical floor priors ...")
seg_floor_priors = {}
for seg in GPU_SEGMENTS:
    prior = _segment_floor_prior(monthly, seg)
    seg_floor_priors[seg] = prior
    if prior is not None:
        print(f"  [{seg}] floor prior:  mean={prior[0]:.3f}  std={prior[1]:.3f}")
print()

# ── Demand-shock set ─────────────────────────────────────────────────────────
shock_set = set(df.loc[df["demand_shock"], "gpu_name"].unique())

target_idx = CURVE_TIMES.index(TARGET_AGE)


# ── Helper: run MC for a specific GPU at a given sample count with a given rng ─
def run_mc_for_gpu(gpu_name, mc_samples, rng):
    """
    Reproduce the exact MC pipeline from fit_all_gpus for one GPU,
    but with a custom mc_samples count and rng.
    Returns the raw mc_out array (mc_samples x len(CURVE_TIMES)) and the method used.
    """
    seg = gpu_segment(gpu_name)
    can_fit = canonical.get(seg)
    is_shock = gpu_name in shock_set

    grp = monthly[monthly["gpu_name"] == gpu_name].sort_values("age_months").dropna()
    t = grp["age_months"].values
    y = grp["price_ratio"].values
    n = len(grp)

    if n >= 1:
        current_ratio = float(grp.tail(3)["price_ratio"].median())
    elif is_shock:
        raw = df[(df["gpu_name"] == gpu_name) & (df["condition"] == "NEW")].sort_values("date")
        current_ratio = float(raw.tail(20)["price_ratio"].median()) if len(raw) else np.nan
    else:
        current_ratio = np.nan

    min_age = float(t.min()) if n > 0 else np.nan

    method = None

    # A. Tier 1: individual fit
    if n >= TIER1_MIN_MONTHS and not np.isnan(min_age) and min_age < TIER1_MAX_MIN_AGE:
        has_post_succ = ("post_successor" in grp.columns and grp["post_successor"].any())
        if has_post_succ:
            grp_pre = grp[~grp["post_successor"]]
            t_pre = grp_pre["age_months"].values
            y_pre = grp_pre["price_ratio"].values
            use_pre = (len(grp_pre) >= TIER1_MIN_MONTHS and
                       len(t_pre) > 0 and
                       not np.isnan(t_pre.min()) and
                       t_pre.min() < TIER1_MAX_MIN_AGE)
        else:
            use_pre = False

        if use_pre:
            fits = {name: fit_model(t_pre, y_pre, name) for name in MODELS}
        else:
            fits = {name: fit_model(t, y, name) for name in MODELS}

        mc_out, w = _mc_from_ensemble(fits, CURVE_TIMES, rng, mc_samples=mc_samples)
        if mc_out is not None:
            valid_f = {k: v for k, v in fits.items() if v is not None}
            best_r2 = max((v["r2"] for v in valid_f.values()), default=np.nan)
            all_bounds_hit = all(v.get("bounds_hit", False) for v in valid_f.values()) if valid_f else True
            if not np.isnan(best_r2) and best_r2 >= 0.20 and not all_bounds_hit:
                stats = _mc_to_stats(mc_out, target_idx)
                proj_t0_check = stats["curve"].get(0, np.nan)
                from depreciation_curves import DEMAND_SHOCK_RATIO
                if np.isnan(proj_t0_check) or proj_t0_check <= DEMAND_SHOCK_RATIO:
                    method = "fitted"
                    return mc_out, method

    # B. Observed fallback (skip — we need MC output, observed has none)
    # For observed GPUs, we use Tier 2 constrained to get MC output

    # C. Tier 2: constrained
    if method is None and n >= MIN_MONTHS_DATA and can_fit is not None:
        k_can = float(can_fit["params"][1])
        k_var = float(can_fit["cov"][1, 1]) if can_fit["cov"].shape[0] > 1 else 1e-6
        floor_prior = seg_floor_priors.get(seg)

        floor_opt, floor_var = fit_constrained_floor(
            t, y, k_can,
            floor_prior=floor_prior,
            n_data_months=n,
        )

        if floor_opt is not None:
            k_floor_cov = 0.0
            if can_fit["cov"].shape[0] >= 2 and floor_var is not None:
                can_fl_std = float(np.sqrt(abs(can_fit["cov"][0, 0])))
                can_k_std = float(np.sqrt(abs(can_fit["cov"][1, 1])))
                if can_fl_std > 0 and can_k_std > 0:
                    corr = float(np.clip(
                        can_fit["cov"][0, 1] / (can_fl_std * can_k_std),
                        -0.99, 0.99))
                    k_floor_cov = corr * float(np.sqrt(abs(floor_var))) * float(np.sqrt(abs(k_var)))

            mc_out = _mc_from_constrained(floor_opt, floor_var,
                                          k_can, k_var, CURVE_TIMES, rng,
                                          mc_samples=mc_samples,
                                          k_floor_cov=k_floor_cov)

            # Forward projection from current market price
            if n > 0 and not np.isnan(current_ratio):
                t_last = float(t[-1])
                canon_now = floor_opt + (1 - floor_opt) * np.exp(-k_can * t_last)
                if canon_now > 0:
                    anchor = current_ratio
                    scale = anchor / canon_now
                    scale = float(np.clip(scale, 0.5, 2.0))
                    mc_out = mc_out * scale

            method = "constrained"
            return mc_out, method

    # D. Tier 3: segment default
    if method is None and can_fit is not None:
        k_can = float(can_fit["params"][1])
        fl_can = float(can_fit["params"][0])
        k_var = float(can_fit["cov"][1, 1]) if can_fit["cov"].shape[0] > 1 else 1e-6
        fl_var = float(can_fit["cov"][0, 0])

        if n > 0 and not np.isnan(current_ratio):
            t_obs = float(t[-1])
            canon_at_obs = fl_can + (1 - fl_can) * np.exp(-k_can * t_obs)
            scale = current_ratio / canon_at_obs if canon_at_obs > 0 else 1.0
            scale = float(np.clip(scale, 0.5, 2.0))
        else:
            scale = 1.0

        mc_out = np.zeros((mc_samples, len(CURVE_TIMES)))
        t_arr = np.array(CURVE_TIMES, dtype=float)
        cov_can = can_fit["cov"]
        cov_reg = cov_can + np.eye(2) * max(1e-10, 1e-6 * np.trace(cov_can))
        for s in range(mc_samples):
            try:
                if np.linalg.cond(cov_reg) < 1e10:
                    fl_s, k_s = rng.multivariate_normal([fl_can, k_can], cov_reg)
                else:
                    fl_s, k_s = fl_can, k_can
            except (np.linalg.LinAlgError, ValueError, RuntimeError):
                fl_s, k_s = fl_can, k_can
            fl_s = float(np.clip(fl_s, 0.001, 0.80))
            k_s = float(np.clip(k_s, 0.005, 0.25))
            mc_out[s] = np.clip(scale * (fl_s + (1 - fl_s) * np.exp(-k_s * t_arr)),
                                0.0, 3.0)

        method = "segment_default"
        return mc_out, method

    return None, None


def make_rng(gpu_name, seed_offset=0):
    """Create a deterministic RNG from gpu name, optionally offset."""
    base_seed = int(hashlib.md5(gpu_name.encode()).hexdigest(), 16) % (2 ** 32)
    return np.random.default_rng(base_seed + seed_offset)


# ══════════════════════════════════════════════════════════════════════════════
# TEST 1: 2000 vs 10000 samples — point estimates comparison
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 80)
print("TEST 1: 2000 vs 10000 MC samples — point estimate comparison at t=60")
print("=" * 80)

comparison_rows = []
for label, gpu in test_gpus.items():
    rng_2k = make_rng(gpu, seed_offset=0)
    mc_2k, method_2k = run_mc_for_gpu(gpu, 2000, rng_2k)

    rng_10k = make_rng(gpu, seed_offset=0)
    mc_10k, method_10k = run_mc_for_gpu(gpu, 10000, rng_10k)

    if mc_2k is None or mc_10k is None:
        print(f"  {label} ({gpu}): MC returned None (method={method_2k}/{method_10k})")
        continue

    col_2k = mc_2k[:, target_idx]
    col_10k = mc_10k[:, target_idx]

    stats_2k = {
        "median": float(np.median(col_2k)),
        "p2.5": float(np.percentile(col_2k, 2.5)),
        "p97.5": float(np.percentile(col_2k, 97.5)),
        "std": float(np.std(col_2k)),
    }
    stats_10k = {
        "median": float(np.median(col_10k)),
        "p2.5": float(np.percentile(col_10k, 2.5)),
        "p97.5": float(np.percentile(col_10k, 97.5)),
        "std": float(np.std(col_10k)),
    }

    comparison_rows.append({
        "label": label,
        "gpu": gpu,
        "method": method_2k,
        **{f"2k_{k}": v for k, v in stats_2k.items()},
        **{f"10k_{k}": v for k, v in stats_10k.items()},
    })

print()
print(f"{'GPU':<30s} {'Method':<18s} | {'Metric':>8s} | {'N=2000':>8s} {'N=10000':>8s} {'Diff':>8s} {'Rel%':>6s}")
print("-" * 110)

for row in comparison_rows:
    gpu_str = row["gpu"][:29]
    method_str = row["method"][:17]
    for metric in ["median", "p2.5", "p97.5", "std"]:
        v2k = row[f"2k_{metric}"]
        v10k = row[f"10k_{metric}"]
        diff = v2k - v10k
        rel = abs(diff / v10k * 100) if v10k != 0 else 0.0
        print(f"{gpu_str:<30s} {method_str:<18s} | {metric:>8s} | {v2k:>8.4f} {v10k:>8.4f} {diff:>+8.4f} {rel:>5.1f}%")
        gpu_str = ""  # only print GPU name on first line
        method_str = ""
    print()


# ══════════════════════════════════════════════════════════════════════════════
# TEST 2: Run-to-run stability of 2000 samples (10 different seeds)
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 80)
print("TEST 2: Run-to-run stability — 2000 samples x 10 seeds")
print("  Measures coefficient of variation (CV) of percentiles across seeds")
print("=" * 80)
print()

N_SEEDS = 10

stability_rows = []
for label, gpu in test_gpus.items():
    medians = []
    p25s = []
    p975s = []
    stds = []

    for seed_i in range(N_SEEDS):
        rng = make_rng(gpu, seed_offset=seed_i * 9999)
        mc_out, method = run_mc_for_gpu(gpu, 2000, rng)
        if mc_out is None:
            continue
        col = mc_out[:, target_idx]
        medians.append(float(np.median(col)))
        p25s.append(float(np.percentile(col, 2.5)))
        p975s.append(float(np.percentile(col, 97.5)))
        stds.append(float(np.std(col)))

    if len(medians) < 2:
        print(f"  {label} ({gpu}): insufficient runs")
        continue

    medians = np.array(medians)
    p25s = np.array(p25s)
    p975s = np.array(p975s)
    stds_arr = np.array(stds)

    def cv(arr):
        return float(np.std(arr) / np.mean(arr) * 100) if np.mean(arr) != 0 else 0.0

    def spread(arr):
        return float(np.max(arr) - np.min(arr))

    stability_rows.append({
        "label": label,
        "gpu": gpu,
        "method": method,
        "median_mean": float(np.mean(medians)),
        "median_cv": cv(medians),
        "median_spread": spread(medians),
        "p2.5_mean": float(np.mean(p25s)),
        "p2.5_cv": cv(p25s),
        "p2.5_spread": spread(p25s),
        "p97.5_mean": float(np.mean(p975s)),
        "p97.5_cv": cv(p975s),
        "p97.5_spread": spread(p975s),
        "std_mean": float(np.mean(stds_arr)),
        "std_cv": cv(stds_arr),
        "std_spread": spread(stds_arr),
    })

print(f"{'GPU':<30s} {'Method':<18s} | {'Metric':>8s} | {'Mean':>8s} {'CV%':>6s} {'Min':>8s} {'Max':>8s} {'Spread':>8s}")
print("-" * 115)

for row in stability_rows:
    gpu_str = row["gpu"][:29]
    method_str = row["method"][:17]
    for metric_key, metric_label in [("median", "median"), ("p2.5", "p2.5"), ("p97.5", "p97.5"), ("std", "std")]:
        mean_val = row[f"{metric_key}_mean"]
        cv_val = row[f"{metric_key}_cv"]
        spread_val = row[f"{metric_key}_spread"]
        print(f"{gpu_str:<30s} {method_str:<18s} | {metric_label:>8s} | {mean_val:>8.4f} {cv_val:>5.1f}% {mean_val - spread_val/2:>8.4f} "
              f"{mean_val + spread_val/2:>8.4f} {spread_val:>8.4f}")
        gpu_str = ""
        method_str = ""
    print()


# ══════════════════════════════════════════════════════════════════════════════
# TEST 3: Summary assessment
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 80)
print("SUMMARY ASSESSMENT")
print("=" * 80)
print()

# Compute aggregate metrics
all_median_cvs = [r["median_cv"] for r in stability_rows]
all_p25_cvs = [r["p2.5_cv"] for r in stability_rows]
all_p975_cvs = [r["p97.5_cv"] for r in stability_rows]
all_std_cvs = [r["std_cv"] for r in stability_rows]

print("Run-to-run coefficient of variation (CV) across 10 seeds at N=2000:")
print(f"  Median at t=60:    CV range = {min(all_median_cvs):.1f}% - {max(all_median_cvs):.1f}%  (mean: {np.mean(all_median_cvs):.1f}%)")
print(f"  2.5th percentile:  CV range = {min(all_p25_cvs):.1f}% - {max(all_p25_cvs):.1f}%  (mean: {np.mean(all_p25_cvs):.1f}%)")
print(f"  97.5th percentile: CV range = {min(all_p975_cvs):.1f}% - {max(all_p975_cvs):.1f}%  (mean: {np.mean(all_p975_cvs):.1f}%)")
print(f"  Std at t=60:       CV range = {min(all_std_cvs):.1f}% - {max(all_std_cvs):.1f}%  (mean: {np.mean(all_std_cvs):.1f}%)")
print()

# Compute max absolute difference between 2k and 10k
if comparison_rows:
    max_median_diff = max(abs(r["2k_median"] - r["10k_median"]) for r in comparison_rows)
    max_p25_diff = max(abs(r["2k_p2.5"] - r["10k_p2.5"]) for r in comparison_rows)
    max_p975_diff = max(abs(r["2k_p97.5"] - r["10k_p97.5"]) for r in comparison_rows)
    max_median_relpct = max(abs(r["2k_median"] - r["10k_median"]) / max(abs(r["10k_median"]), 1e-6) * 100 for r in comparison_rows)
    max_p25_relpct = max(abs(r["2k_p2.5"] - r["10k_p2.5"]) / max(abs(r["10k_p2.5"]), 1e-6) * 100 for r in comparison_rows)
    max_p975_relpct = max(abs(r["2k_p97.5"] - r["10k_p97.5"]) / max(abs(r["10k_p97.5"]), 1e-6) * 100 for r in comparison_rows)

    print("Maximum absolute difference: N=2000 vs N=10000 (same seed):")
    print(f"  Median at t=60:    max |diff| = {max_median_diff:.4f}  ({max_median_relpct:.1f}% relative)")
    print(f"  2.5th percentile:  max |diff| = {max_p25_diff:.4f}  ({max_p25_relpct:.1f}% relative)")
    print(f"  97.5th percentile: max |diff| = {max_p975_diff:.4f}  ({max_p975_relpct:.1f}% relative)")
    print()

# Thresholds for "stable enough"
CV_THRESHOLD = 5.0  # CV < 5% is acceptable for CI endpoints
DIFF_THRESHOLD = 0.01  # absolute difference < 0.01 in price_ratio

worst_cv = max(max(all_p25_cvs), max(all_p975_cvs))
worst_abs_diff = max(max_p25_diff, max_p975_diff) if comparison_rows else 0

print("Verdict:")
if worst_cv < CV_THRESHOLD and worst_abs_diff < DIFF_THRESHOLD:
    print(f"  PASS: 2000 MC samples is sufficient for stable CI estimation.")
    print(f"  - Worst-case CI endpoint CV: {worst_cv:.1f}% (threshold: <{CV_THRESHOLD}%)")
    print(f"  - Worst-case 2k-vs-10k difference: {worst_abs_diff:.4f} (threshold: <{DIFF_THRESHOLD})")
elif worst_cv < CV_THRESHOLD:
    print(f"  MARGINAL: CIs are stable run-to-run (worst CV: {worst_cv:.1f}%),")
    print(f"  but 2k-vs-10k difference is noticeable ({worst_abs_diff:.4f}). Consider 5000 samples.")
elif worst_abs_diff < DIFF_THRESHOLD:
    print(f"  MARGINAL: 2k agrees well with 10k (worst diff: {worst_abs_diff:.4f}),")
    print(f"  but run-to-run variability is higher than ideal (worst CV: {worst_cv:.1f}%).")
    print(f"  Consider 5000 samples for tail percentiles.")
else:
    print(f"  FAIL: 2000 MC samples may be insufficient.")
    print(f"  - Worst-case CI endpoint CV: {worst_cv:.1f}% (threshold: <{CV_THRESHOLD}%)")
    print(f"  - Worst-case 2k-vs-10k difference: {worst_abs_diff:.4f} (threshold: <{DIFF_THRESHOLD})")
    print(f"  Recommend increasing to 5000-10000 samples.")

print()
print("Note: CV measures relative scatter of percentile estimates across 10 independent")
print("MC runs with different seeds. CV < 5% means the 95% CI endpoints are stable to")
print("within ~5% of their value, which is well within the model's inherent uncertainty.")
