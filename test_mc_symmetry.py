"""
test_mc_symmetry.py
Empirical test: Is the MC posterior predictive distribution approximately
symmetric in log-space for the GPU depreciation model?

Approach:
  - Run the full pipeline (load_data, build_extended_monthly, fit_all_gpus)
  - Monkey-patch _mc_to_stats to intercept mc_out arrays for ~10 representative GPUs
  - For each intercepted GPU, at each of the 6 CURVE_TIMES (t=0,12,24,36,48,60):
      * Compute skewness in level-space and log-space
      * Compare lower/upper CI arm widths in log-space
  - Print a summary table and conclude whether log-space symmetry holds
"""

import os
import sys
import numpy as np
import pandas as pd
from scipy.stats import skew

# ── Setup ─────────────────────────────────────────────────────────────────────
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import depreciation_curves as dc
from data_prep import load_data, load_datacenter_supplement

# ── Representative GPUs: ~10 across all tiers and segments ────────────────────
# We want a spread: datacenter (old & new), workstation, consumer; tier 1/2/3.
TARGET_GPUS = {
    # Datacenter — old, well-observed (likely Tier 1)
    "T4",
    "Tesla V100 PCIe 32 GB",
    # Datacenter — newer, less data (likely Tier 2 or 3)
    "H100 SXM5 80 GB",
    "A100 SXM4 80 GB",
    # Workstation
    "RTX A6000",
    "Quadro RTX 6000",
    # Consumer — well-observed
    "GeForce RTX 3090",
    "GeForce RTX 3080",
    # Consumer — newer
    "GeForce RTX 4090",
    "GeForce RTX 4070",
}

# ── Monkey-patch _mc_to_stats to intercept mc_out arrays ─────────────────────
# We store the mc_out for each GPU that we care about, then delegate to the
# original function.
_original_mc_to_stats = dc._mc_to_stats
_captured_mc = {}  # gpu_name -> mc_out (2000 x 6)
_current_gpu = [None]  # mutable container for the current GPU being processed

def _patched_mc_to_stats(mc_out, target_idx):
    """Intercept mc_out for target GPUs, then call the original."""
    gpu = _current_gpu[0]
    if gpu is not None and gpu in TARGET_GPUS:
        _captured_mc[gpu] = mc_out.copy()
    return _original_mc_to_stats(mc_out, target_idx)

# We also need to know which GPU is being processed when _mc_to_stats is called.
# The cleanest way: patch fit_all_gpus' inner loop. But that's complex.
# Instead, we'll patch at the module level and also patch the per-GPU loop
# by wrapping the entire fit_all_gpus call and intercepting via the _mc_to_stats
# calls in order. But _mc_to_stats doesn't know the GPU name.
#
# Better approach: patch _mc_to_stats AND track GPU names by also patching
# the point where _mc_to_stats is called. Looking at the code, _mc_to_stats
# is called at 3 places (tier 1 line 1035, tier 2 line 1145, tier 3 line 1199).
# All are inside a `for gpu in all_gpus:` loop.
#
# Simplest: we'll monkey-patch the top of the GPU loop. We can do this by
# wrapping fit_all_gpus and inspecting calls. But actually the simplest approach
# is to patch `gpu_segment` which is called once per GPU at the start of the loop.

_original_gpu_segment = dc.gpu_segment

def _patched_gpu_segment(gpu_name):
    _current_gpu[0] = gpu_name
    return _original_gpu_segment(gpu_name)

# Apply patches
dc._mc_to_stats = _patched_mc_to_stats
dc.gpu_segment = _patched_gpu_segment

# ── Run the full pipeline ─────────────────────────────────────────────────────
print("=" * 70)
print("MC SYMMETRY TEST — Loading data and running full pipeline")
print("=" * 70)

df = load_data(verbose=False)

keepa_monthly = None
if os.path.exists(dc.KEEPA_MONTHLY_PATH):
    keepa_monthly = pd.read_csv(dc.KEEPA_MONTHLY_PATH)
    print(f"[keepa] Loaded {len(keepa_monthly)} monthly obs")

supp_monthly = load_datacenter_supplement(verbose=False)
if supp_monthly is not None and keepa_monthly is not None:
    keepa_monthly = pd.concat([keepa_monthly, supp_monthly], ignore_index=True)
elif supp_monthly is not None:
    keepa_monthly = supp_monthly

print("\nRunning fit_all_gpus (this takes a minute) ...\n")
results = dc.fit_all_gpus(df, keepa_monthly)

# ── Restore original functions ────────────────────────────────────────────────
dc._mc_to_stats = _original_mc_to_stats
dc.gpu_segment = _original_gpu_segment

# ── Analyze captured MC distributions ─────────────────────────────────────────
print("\n" + "=" * 70)
print("MC POSTERIOR PREDICTIVE SYMMETRY ANALYSIS")
print("=" * 70)

CURVE_TIMES = dc.CURVE_TIMES  # [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120]
EPS = 1e-10  # guard against log(0)

rows = []
for gpu in sorted(_captured_mc.keys()):
    mc_out = _captured_mc[gpu]  # shape (2000, 6)

    # Get tier and method from results
    gpu_row = results[results["gpu_name"] == gpu]
    if len(gpu_row) == 0:
        tier = "?"
        method = "?"
        segment = "?"
    else:
        tier = str(gpu_row.iloc[0]["fit_tier"])
        method = str(gpu_row.iloc[0]["method"])
        segment = str(gpu_row.iloc[0]["segment"])

    for i, t in enumerate(CURVE_TIMES):
        samples = mc_out[:, i]

        # Level-space statistics
        level_skew = float(skew(samples, nan_policy='omit'))

        # Log-space statistics (guard against log(0))
        log_samples = np.log(np.maximum(samples, EPS))
        log_skew = float(skew(log_samples, nan_policy='omit'))

        # CI arm comparison in log-space
        log_p2_5 = float(np.percentile(log_samples, 2.5))
        log_median = float(np.median(log_samples))
        log_p97_5 = float(np.percentile(log_samples, 97.5))

        lower_arm = log_median - log_p2_5    # distance from median to lower bound
        upper_arm = log_p97_5 - log_median    # distance from median to upper bound

        # Ratio: if symmetric, lower_arm / upper_arm ~ 1.0
        arm_ratio = lower_arm / upper_arm if upper_arm > 1e-12 else np.nan

        rows.append({
            "gpu_name": gpu,
            "segment": segment,
            "tier": tier,
            "method": method,
            "t": t,
            "median": float(np.median(samples)),
            "level_skew": level_skew,
            "log_skew": log_skew,
            "log_lower_arm": lower_arm,
            "log_upper_arm": upper_arm,
            "arm_ratio": arm_ratio,
        })

df_analysis = pd.DataFrame(rows)

# ── Print detailed table ──────────────────────────────────────────────────────
print(f"\nCaptured MC distributions for {len(_captured_mc)} GPUs:")
print(f"  {sorted(_captured_mc.keys())}\n")

pd.set_option("display.float_format", "{:.4f}".format)
pd.set_option("display.max_rows", 200)
pd.set_option("display.width", 200)

print("-" * 160)
print(f"{'GPU':<30s} {'Seg':<12s} {'T':>1s} {'Meth':<14s} {'t':>3s} "
      f"{'Median':>8s} {'Lev.Skew':>9s} {'Log.Skew':>9s} "
      f"{'LogLowArm':>10s} {'LogUpArm':>10s} {'ArmRatio':>9s}")
print("-" * 160)

for _, r in df_analysis.iterrows():
    print(f"{r['gpu_name']:<30s} {r['segment']:<12s} {r['tier']:>1s} {r['method']:<14s} {r['t']:>3.0f} "
          f"{r['median']:>8.4f} {r['level_skew']:>9.4f} {r['log_skew']:>9.4f} "
          f"{r['log_lower_arm']:>10.4f} {r['log_upper_arm']:>10.4f} {r['arm_ratio']:>9.4f}")

# ── Summary statistics ────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SUMMARY STATISTICS")
print("=" * 70)

# Overall
print(f"\nTotal GPU x time-point combinations: {len(df_analysis)}")
print(f"\nLevel-space skewness:")
print(f"  Mean absolute:   {df_analysis['level_skew'].abs().mean():.4f}")
print(f"  Median absolute: {df_analysis['level_skew'].abs().median():.4f}")
print(f"  Max absolute:    {df_analysis['level_skew'].abs().max():.4f}")
print(f"  Fraction |skew| < 0.5:  {(df_analysis['level_skew'].abs() < 0.5).mean():.1%}")
print(f"  Fraction |skew| < 1.0:  {(df_analysis['level_skew'].abs() < 1.0).mean():.1%}")

print(f"\nLog-space skewness:")
print(f"  Mean absolute:   {df_analysis['log_skew'].abs().mean():.4f}")
print(f"  Median absolute: {df_analysis['log_skew'].abs().median():.4f}")
print(f"  Max absolute:    {df_analysis['log_skew'].abs().max():.4f}")
print(f"  Fraction |skew| < 0.5:  {(df_analysis['log_skew'].abs() < 0.5).mean():.1%}")
print(f"  Fraction |skew| < 1.0:  {(df_analysis['log_skew'].abs() < 1.0).mean():.1%}")

print(f"\nLog-space CI arm ratio (1.0 = perfectly symmetric):")
valid_arms = df_analysis[df_analysis['arm_ratio'].notna() & np.isfinite(df_analysis['arm_ratio'])]
print(f"  Mean:   {valid_arms['arm_ratio'].mean():.4f}")
print(f"  Median: {valid_arms['arm_ratio'].median():.4f}")
print(f"  Std:    {valid_arms['arm_ratio'].std():.4f}")
print(f"  Fraction in [0.7, 1.4]:  {((valid_arms['arm_ratio'] >= 0.7) & (valid_arms['arm_ratio'] <= 1.4)).mean():.1%}")
print(f"  Fraction in [0.8, 1.25]: {((valid_arms['arm_ratio'] >= 0.8) & (valid_arms['arm_ratio'] <= 1.25)).mean():.1%}")

# By time point
print(f"\nLog-space skewness by time point:")
for t in CURVE_TIMES:
    sub = df_analysis[df_analysis["t"] == t]
    print(f"  t={t:>2d}:  mean |skew|={sub['log_skew'].abs().mean():.4f}  "
          f"median |skew|={sub['log_skew'].abs().median():.4f}  "
          f"max |skew|={sub['log_skew'].abs().max():.4f}  "
          f"frac<0.5={( sub['log_skew'].abs() < 0.5).mean():.0%}")

# By tier
print(f"\nLog-space skewness by fit tier:")
for tier in sorted(df_analysis["tier"].unique()):
    sub = df_analysis[df_analysis["tier"] == tier]
    print(f"  Tier {tier}:  mean |skew|={sub['log_skew'].abs().mean():.4f}  "
          f"median |skew|={sub['log_skew'].abs().median():.4f}  "
          f"frac<0.5={( sub['log_skew'].abs() < 0.5).mean():.0%}")

# ── Conclusion ────────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)

overall_frac = (df_analysis['log_skew'].abs() < 0.5).mean()
overall_frac_level = (df_analysis['level_skew'].abs() < 0.5).mean()
mean_arm_ratio = valid_arms['arm_ratio'].mean()
median_log_skew = df_analysis['log_skew'].abs().median()

print(f"\n  Log-space:   {overall_frac:.0%} of GPU x time-point combinations have |skewness| < 0.5")
print(f"  Level-space: {overall_frac_level:.0%} of GPU x time-point combinations have |skewness| < 0.5")
print(f"  Median log-space |skewness|: {median_log_skew:.4f}")
print(f"  Mean log-space CI arm ratio: {mean_arm_ratio:.4f} (1.0 = symmetric)")

if overall_frac >= 0.80 and median_log_skew < 0.5:
    print(f"\n  RESULT: YES -- the MC posterior predictive distribution IS approximately")
    print(f"  symmetric in log-space for most GPUs at most time points.")
    print(f"  Log-normal CIs are a reasonable approximation.")
elif overall_frac >= 0.60:
    print(f"\n  RESULT: PARTIALLY -- log-space symmetry holds for the majority of")
    print(f"  GPU x time-point combinations, but there are notable exceptions.")
    print(f"  Log-normal CIs are a reasonable but imperfect approximation.")
else:
    print(f"\n  RESULT: NO -- the MC posterior predictive distribution is NOT approximately")
    print(f"  symmetric in log-space for most GPUs. Log-normal CIs may be inappropriate.")

# Compare improvement: how much better is log-space vs level-space?
improvement = overall_frac - overall_frac_level
print(f"\n  Log-space improves symmetry by {improvement:+.0%} vs level-space"
      f" ({overall_frac:.0%} vs {overall_frac_level:.0%} with |skew| < 0.5).")

print()
