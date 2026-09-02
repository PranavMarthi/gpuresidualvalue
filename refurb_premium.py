"""
refurb_premium.py
Prove the refurbishment premium with:
  1. OLS F-test with GPU + time fixed effects  (confirmatory — ONE test)
  2. Cluster bootstrap CI                       (robustness)
  3. Per-GPU t-tests with B-H FDR correction   (exploratory decomposition)
  4. Power analysis — exclude under-powered cells before testing
"""

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.power import TTestIndPower

from data_prep import load_data

ALPHA = 0.05
POWER_TARGET = 0.80
MIN_MDE = 0.30       # exclude cells where we can only detect effects > 30%
FDR_Q = 0.10         # B-H FDR threshold for exploratory per-GPU tests (more lenient than ALPHA)
BOOT_B = 2000


# ── 1. CONFIRMATORY: OLS F-test ───────────────────────────────────────────────

def ols_confirmatory(df):
    """
    Primary test. condition coefficient on REFURBISHED (vs USED baseline)
    controlling for GPU model and month.
    Aggregates to monthly medians per (gpu, condition, month) first to avoid
    pseudo-replication and to make HC1 feasible on large datasets.
    Uses USED as the reference condition.
    """
    sub = df[df["condition"].isin(["USED", "REFURBISHED"])].copy()
    sub["year_month"] = sub["date"].dt.to_period("M").astype(str)

    has_country = "country" in df.columns

    # Aggregate to monthly medians — removes within-month pseudo-replication
    # and reduces 300k rows → ~2k, making HC1 feasible.
    groupby_keys = ["gpu_name", "condition", "year_month"]
    if has_country:
        groupby_keys.append("country")
    agg = (sub.groupby(groupby_keys)["price_usd"]
              .median()
              .reset_index())
    agg["log_price"] = np.log(agg["price_usd"])

    # Set USED as reference
    agg["condition"] = pd.Categorical(agg["condition"],
                                      categories=["USED", "REFURBISHED"])

    # Cluster-robust SE by GPU accounts for within-GPU temporal autocorrelation:
    # the same GPU appears across many months, creating correlated residuals that
    # HC1 (heteroskedasticity-only) does not correct. Clustering by gpu_name
    # gives valid inference when errors are correlated within GPU over time.
    formula = "log_price ~ C(gpu_name) + C(condition) + C(year_month)"
    if has_country:
        formula += " + C(country)"
    model = ols(formula,
                data=agg).fit(cov_type="cluster",
                              cov_kwds={"groups": agg["gpu_name"]})

    refurb_coef = model.params.get("C(condition)[T.REFURBISHED]", np.nan)
    refurb_pval = model.pvalues.get("C(condition)[T.REFURBISHED]", np.nan)
    refurb_ci   = model.conf_int().loc["C(condition)[T.REFURBISHED]"] \
                  if "C(condition)[T.REFURBISHED]" in model.params.index \
                  else (np.nan, np.nan)

    premium_pct = (np.exp(refurb_coef) - 1) * 100
    # Transform CI from log scale to % terms. exp() is convex so the %
    # CI is asymmetric around premium_pct — this is correct (not a bug).
    ci_lo_pct = (np.exp(refurb_ci[0]) - 1) * 100 if not np.isnan(refurb_ci[0]) else np.nan
    ci_hi_pct = (np.exp(refurb_ci[1]) - 1) * 100 if not np.isnan(refurb_ci[1]) else np.nan

    print("=" * 60)
    print("CONFIRMATORY TEST — OLS with GPU + Time Fixed Effects")
    print("=" * 60)
    print(f"  REFURBISHED coefficient (log scale): {refurb_coef:+.4f}")
    print(f"  Premium vs USED (% terms):           {premium_pct:+.2f}%")
    print(f"  95% CI (% terms):                    [{ci_lo_pct:+.2f}%, {ci_hi_pct:+.2f}%]")
    print(f"  95% CI (log scale):                  [{refurb_ci[0]:.4f}, {refurb_ci[1]:.4f}]")
    print(f"  p-value:                             {refurb_pval:.4f}")
    print(f"  Significant at {ALPHA}:              {'YES' if refurb_pval < ALPHA else 'NO'}")
    print(f"  Model R²:                            {model.rsquared:.4f}")
    print()
    return model, premium_pct, refurb_pval


# ── 2. CLUSTER BOOTSTRAP CI ───────────────────────────────────────────────────

def cluster_bootstrap(df, B=BOOT_B):
    """
    Resample GPU models with replacement (cluster bootstrap).
    Preserves within-GPU temporal autocorrelation.
    Returns 95% CI on (refurb_median - used_median) / used_median.

    Pre-aggregates to per-GPU medians to avoid O(n) row-filtering in each
    bootstrap iteration (raw data has 300k+ rows across 54 GPUs).
    """
    sub = df[df["condition"].isin(["USED", "REFURBISHED"])].copy()

    # Pre-aggregate: per-GPU median price by condition
    gpu_stats = (sub.groupby(["gpu_name", "condition"])["price_usd"]
                   .median()
                   .unstack("condition")
                   .dropna(subset=["USED", "REFURBISHED"]))
    used_arr   = gpu_stats["USED"].values
    refurb_arr = gpu_stats["REFURBISHED"].values
    n_gpus     = len(gpu_stats)

    premiums = []
    rng = np.random.default_rng(42)
    for _ in range(B):
        idx        = rng.integers(0, n_gpus, size=n_gpus)
        used_med   = np.median(used_arr[idx])
        refurb_med = np.median(refurb_arr[idx])
        if used_med > 0:
            premiums.append((refurb_med - used_med) / used_med * 100)

    ci_lo, ci_hi = np.percentile(premiums, [2.5, 97.5])
    print("=" * 60)
    print(f"CLUSTER BOOTSTRAP CI  (B={B}, GPU-level resampling)")
    print("=" * 60)
    print(f"  Mean premium:  {np.mean(premiums):+.2f}%")
    print(f"  95% CI:        [{ci_lo:+.2f}%, {ci_hi:+.2f}%]")
    print(f"  CI excludes 0: {'YES — premium is real' if ci_lo > 0 or ci_hi < 0 else 'NO — inconclusive'}")
    print()
    return np.array(premiums), (ci_lo, ci_hi)


# ── 3. POWER ANALYSIS + PER-GPU T-TESTS WITH B-H CORRECTION ──────────────────

def per_gpu_tests(df):
    """
    Exploratory decomposition. Per-GPU t-test REFURBISHED vs USED.
    Steps:
      a) Power analysis — skip cells where MDE > MIN_MDE
      b) Run t-tests on eligible GPUs
      c) Apply Benjamini-Hochberg FDR correction
    """
    sub = df[df["condition"].isin(["USED", "REFURBISHED"])].copy()
    power_analysis = TTestIndPower()

    results = []
    skipped = []

    for gpu, grp in sub.groupby("gpu_name"):
        used   = grp[grp["condition"] == "USED"]["price_usd"].values
        refurb = grp[grp["condition"] == "REFURBISHED"]["price_usd"].values

        if len(used) < 3 or len(refurb) < 3:
            skipped.append((gpu, len(used), len(refurb), "< 3 obs"))
            continue

        # Power analysis — minimum detectable effect size (Cohen's d)
        ratio = len(refurb) / len(used)
        mde = power_analysis.solve_power(
            effect_size=None, nobs1=len(used),
            alpha=ALPHA, power=POWER_TARGET, ratio=ratio
        )
        if mde > MIN_MDE:
            skipped.append((gpu, len(used), len(refurb),
                            f"low power (MDE={mde:.2f})"))
            continue

        t_stat, p_raw = stats.ttest_ind(refurb, used, equal_var=False)
        # Use means for premium_pct: the Welch t-test tests means, so reporting
        # a median-based premium alongside a mean-based p-value mixes estimands.
        # For right-skewed price distributions mean > median, but consistency
        # with the test statistic is more important than robustness here.
        premium_pct   = (np.mean(refurb) - np.mean(used)) / np.mean(used) * 100
        # Pooled sample std (ddof=1 in each group) — the standard Cohen's d denominator.
        # np.std() defaults to ddof=0 (population std), which underestimates variability
        # and inflates Cohen's d by ~10-15% for small samples.
        pooled_var = ((len(used) - 1) * np.var(used, ddof=1) +
                      (len(refurb) - 1) * np.var(refurb, ddof=1)) / (len(used) + len(refurb) - 2)
        pooled_std = np.sqrt(pooled_var)
        cohens_d      = (np.mean(refurb) - np.mean(used)) / pooled_std \
                        if pooled_std > 0 else np.nan

        results.append({
            "gpu_name":    gpu,
            "n_used":      len(used),
            "n_refurb":    len(refurb),
            "premium_pct": premium_pct,
            "cohens_d":    cohens_d,
            "p_raw":       p_raw,
        })

    if not results:
        print("No GPUs passed power threshold.")
        return pd.DataFrame(), pd.DataFrame()

    res_df = pd.DataFrame(results)

    # B-H FDR correction
    reject, p_corrected, _, _ = multipletests(
        res_df["p_raw"], alpha=FDR_Q, method="fdr_bh"
    )
    res_df["p_corrected"] = p_corrected
    res_df["significant_BH"] = reject

    res_df = res_df.sort_values("premium_pct", ascending=False)

    skip_df = pd.DataFrame(skipped,
                           columns=["gpu_name", "n_used", "n_refurb", "reason"])

    print("=" * 60)
    print("EXPLORATORY — Per-GPU t-tests (B-H FDR corrected, q=0.10)")
    print("=" * 60)
    print(res_df[["gpu_name", "n_used", "n_refurb", "premium_pct",
                  "cohens_d", "p_raw", "p_corrected", "significant_BH"]]
          .to_string(index=False))
    print(f"\nGPUs with significant premium (after B-H): "
          f"{res_df['significant_BH'].sum()} / {len(res_df)}")

    if len(skip_df):
        print(f"\nSkipped (low power or insufficient data): {len(skip_df)} GPUs")
        print(skip_df.to_string(index=False))
    print()

    return res_df, skip_df


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    df = load_data(verbose=False)

    print("\n[1/3] Confirmatory OLS test")
    model, premium_pct, p_val = ols_confirmatory(df)

    print("[2/3] Cluster bootstrap robustness check")
    premiums, ci = cluster_bootstrap(df, B=BOOT_B)

    print("[3/3] Per-GPU decomposition (exploratory)")
    results, skipped = per_gpu_tests(df)

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Refurbishment premium (OLS, controlling for GPU+time): {premium_pct:+.2f}%")
    print(f"  Primary test p-value: {p_val:.4f}")
    # Verdict driven by the designated confirmatory test (OLS) only.
    # The bootstrap estimates a different quantity (unconditional median premium)
    # and is reported as a robustness check, not a co-decision gate.
    verdict = "CONFIRMED" if p_val < ALPHA else "NOT CONFIRMED"
    print(f"  Verdict: {verdict}")
    print()
    print(f"  Robustness check — bootstrap (unconditional median, different estimand):")
    print(f"    Bootstrap 95% CI:  [{ci[0]:+.2f}%, {ci[1]:+.2f}%]")
    boot_note = "consistent" if ci[0] > 0 else "wider (expected: median estimand differs from OLS geometric mean)"
    print(f"    Bootstrap vs OLS:  {boot_note}")
