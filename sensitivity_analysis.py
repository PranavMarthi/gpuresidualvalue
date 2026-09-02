"""
sensitivity_analysis.py
Varies key pipeline thresholds one-at-a-time and measures how much
the depreciation rankings change. Produces a stability report.

Does NOT modify any pipeline files.  Monkey-patches module constants
before each run, then restores defaults.

Usage:  python sensitivity_analysis.py
"""

import os
import sys
import time
import numpy as np
import pandas as pd

# Pipeline imports
import depreciation_curves as dc
from data_prep import load_data, load_datacenter_supplement
from ranking import build_ranking

# ── Thresholds to vary (name, module attr, default, test values) ─────────────
SCENARIOS = [
    # (label,           module,  attr,                     default, values)
    ("TIER1_MIN_MONTHS", dc,     "TIER1_MIN_MONTHS",       18,     [12, 15, 18, 21, 24]),
    ("OBS_WINDOW",       dc,     "OBS_WINDOW",             12,     [6, 9, 12, 15, 18]),
    ("APPRECIATING_THR", dc,     "APPRECIATING_THRESHOLD",  1.2,   [1.05, 1.1, 1.2, 1.5, 2.0]),
    ("TIER1_MAX_MIN_AGE",dc,     "TIER1_MAX_MIN_AGE",      30,     [18, 24, 30, 36, 42]),
]


def run_pipeline(df, keepa_monthly):
    """Run the curve fitting + ranking pipeline and return the ranking DataFrame."""
    results = dc.fit_all_gpus(df, keepa_monthly)
    ranking = build_ranking(results, df)
    return ranking


def rank_vector(ranking):
    """Extract GPU → overall_rank as a Series keyed by gpu_name."""
    return ranking.set_index("gpu_name")["overall_rank"]


def compare_rankings(base_ranks, test_ranks):
    """Compare two rank vectors. Returns summary stats."""
    common = base_ranks.index.intersection(test_ranks.index)
    if len(common) == 0:
        return {"max_shift": np.nan, "mean_shift": np.nan, "n_changed": 0,
                "n_common": 0, "rank_corr": np.nan}

    b = base_ranks.loc[common]
    t = test_ranks.loc[common]
    shifts = (t - b).abs()

    return {
        "max_shift":  int(shifts.max()),
        "mean_shift": float(shifts.mean()),
        "n_changed":  int((shifts > 0).sum()),
        "n_common":   len(common),
        "rank_corr":  float(b.corr(t, method="spearman")),
    }


def per_gpu_shifts(base_ranks, test_ranks):
    """Return a Series of rank shifts per GPU (test - base)."""
    common = base_ranks.index.intersection(test_ranks.index)
    return (test_ranks.loc[common] - base_ranks.loc[common]).sort_values()


def main():
    os.makedirs("outputs", exist_ok=True)

    # ── Load data once ───────────────────────────────────────────────────────
    print("Loading data …")
    df = load_data(verbose=False)

    keepa_monthly = None
    if os.path.exists(dc.KEEPA_MONTHLY_PATH):
        keepa_monthly = pd.read_csv(dc.KEEPA_MONTHLY_PATH)

    supp_monthly = load_datacenter_supplement(verbose=False)
    if supp_monthly is not None and keepa_monthly is not None:
        keepa_monthly = pd.concat([keepa_monthly, supp_monthly], ignore_index=True)
    elif supp_monthly is not None:
        keepa_monthly = supp_monthly

    # ── Baseline run (all defaults) ──────────────────────────────────────────
    print("\n[baseline] Running with default thresholds …")
    t0 = time.time()
    base_ranking = run_pipeline(df, keepa_monthly)
    base_time = time.time() - t0
    base_ranks = rank_vector(base_ranking)
    print(f"  Done in {base_time:.1f}s — {len(base_ranks)} GPUs ranked\n")

    # ── Vary each threshold ──────────────────────────────────────────────────
    all_results = []      # summary rows
    all_shifts  = {}      # {(param, value): Series of per-GPU shifts}

    for label, module, attr, default, values in SCENARIOS:
        print(f"{'='*70}")
        print(f"Varying {label}  (default={default})  values={values}")
        print(f"{'='*70}")

        for val in values:
            tag = f"{label}={val}"

            # Monkey-patch — always restore default even if post-processing fails
            setattr(module, attr, val)

            t0 = time.time()
            try:
                ranking = run_pipeline(df, keepa_monthly)

                elapsed = time.time() - t0

                ranks = rank_vector(ranking)
                stats = compare_rankings(base_ranks, ranks)
                stats["param"]   = label
                stats["value"]   = val
                stats["is_default"] = (val == default)
                stats["elapsed"] = round(elapsed, 1)
                stats["n_gpus"]  = len(ranks)
                all_results.append(stats)

                shifts = per_gpu_shifts(base_ranks, ranks)
                all_shifts[(label, val)] = shifts

                is_def = " (DEFAULT)" if val == default else ""
                print(f"  [{tag}]{is_def}  "
                      f"max_shift={stats['max_shift']:+d}  "
                      f"mean_shift={stats['mean_shift']:.1f}  "
                      f"changed={stats['n_changed']}/{stats['n_common']}  "
                      f"ρ={stats['rank_corr']:.4f}  "
                      f"({elapsed:.1f}s)")
            except Exception as e:
                print(f"  [{tag}] FAILED: {e}")
                continue
            finally:
                setattr(module, attr, default)

        print()

    # ── Summary table ────────────────────────────────────────────────────────
    summary = pd.DataFrame(all_results)
    summary = summary[["param", "value", "is_default", "max_shift", "mean_shift",
                        "n_changed", "n_common", "rank_corr", "n_gpus", "elapsed"]]

    print("\n" + "=" * 80)
    print("SENSITIVITY ANALYSIS SUMMARY")
    print("=" * 80)
    print(summary.to_string(index=False))

    # ── Most sensitive GPUs ──────────────────────────────────────────────────
    # Aggregate absolute shifts across all non-default runs
    gpu_sensitivity = pd.Series(dtype=float)
    for (param, val), shifts in all_shifts.items():
        # Skip default runs (shift = 0 by definition)
        scenario = next((s for s in SCENARIOS if s[0] == param), None)
        if scenario and val == scenario[3]:
            continue
        gpu_sensitivity = gpu_sensitivity.add(shifts.abs(), fill_value=0)

    if len(gpu_sensitivity) > 0:
        gpu_sensitivity = gpu_sensitivity.sort_values(ascending=False)
        print("\n" + "=" * 80)
        print("MOST SENSITIVE GPUs  (total absolute rank shift across all scenarios)")
        print("=" * 80)
        for gpu, total_shift in gpu_sensitivity.head(15).items():
            base_r = base_ranks.get(gpu, "?")
            print(f"  {gpu:40s}  base_rank={base_r:>3}  "
                  f"total_abs_shift={total_shift:.0f}")

    # ── Per-threshold biggest movers ─────────────────────────────────────────
    print("\n" + "=" * 80)
    print("BIGGEST MOVERS PER THRESHOLD CHANGE")
    print("=" * 80)
    for (param, val), shifts in all_shifts.items():
        scenario = next((s for s in SCENARIOS if s[0] == param), None)
        if scenario and val == scenario[3]:
            continue
        if shifts.abs().max() == 0:
            continue
        worst = shifts.abs().nlargest(3)
        movers = ", ".join(f"{g} ({shifts[g]:+.0f})" for g in worst.index)
        print(f"  {param}={val:<6}  {movers}")

    # ── Save ─────────────────────────────────────────────────────────────────
    out_path = "outputs/sensitivity_analysis.csv"
    summary.to_csv(out_path, index=False)
    print(f"\nSaved → {out_path}")

    # Interpretation guide
    print("\n" + "=" * 80)
    print("HOW TO READ THIS")
    print("=" * 80)
    print("""
  max_shift:   Largest rank position change for any single GPU vs baseline
  mean_shift:  Average rank change across all GPUs
  n_changed:   Number of GPUs whose rank moved at all
  rank_corr:   Spearman correlation with baseline ranking (1.0 = identical order)

  If rank_corr stays above ~0.95 across all threshold variations,
  the ranking is robust. Below 0.90 signals material sensitivity.

  GPUs in the "MOST SENSITIVE" list are the ones whose rank position
  depends most heavily on threshold choices — their placement should
  be interpreted with caution.
""")


if __name__ == "__main__":
    main()
