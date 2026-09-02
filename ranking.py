"""
ranking.py
Final depreciation ranking across GPU models.
Metrics: TVR, % loss, half-life, AUC (trapezoidal).
Composite rank. Additional scenario analysis for demand-shock GPUs.
Reads curve_fit_results.csv produced by depreciation_curves.py.
"""

import sys
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from data_prep import load_data, MSRP_REFERENCE
from depreciation_curves import GPU_SEGMENTS, SEG_K_FALLBACK


# ── GPU segment lookup ────────────────────────────────────────────────────────
_SEG_LOOKUP = {gpu: seg for seg, gpus in GPU_SEGMENTS.items() for gpu in gpus}

def gpu_segment(name):
    """Return segment string for *name*, or 'UNKNOWN' if not catalogued."""
    return _SEG_LOOKUP.get(name, "UNKNOWN")


# ── Shock-scenario proxy decay parameters ─────────────────────────────────────
# Default k/floor used for shock GPUs whose segment is not in SEG_K_FALLBACK.
SHOCK_PROXY_K     = 0.020   # /month → half-life ~35 months
SHOCK_PROXY_FLOOR = 0.15    # 15% residual value at long horizon

# ── Ranking metrics ───────────────────────────────────────────────────────────

def pct_loss(tvr):
    """(1 - TVR) * 100. Higher = worse."""
    return (1 - tvr) * 100


def audc_from_curve(fits_row, t_max=60):
    """
    Area under depreciation curve using the *fitted curve* columns from
    curve_fit_results.csv (proj_t0 … proj_t60).

    This is the correct data source for AUDC because:
    1. The fitted curve integrates Keepa-extended history back to t=0, not just
       the 22-month retail window.
    2. It shares the same data pipeline as TVR and sigma_yr5.
    3. It always starts at t=0, so all GPUs share the same normalisation baseline.

    Skips NaN values (e.g. 'observed' GPUs may lack t=0..t48 back-extrapolation).
    Returns NaN if fewer than 2 non-NaN points are available.

    Normalised by dividing by t_max. Values can exceed 1.0 for GPUs that
    traded above MSRP (uncapped projections). Higher AUDC = better value retention.
    """
    times = [0, 12, 24, 36, 48, 60]
    cols  = ["proj_t0", "proj_t12", "proj_t24", "proj_t36", "proj_t48", "proj_t60"]
    t_pts, y_pts = [], []
    for t_pt, col in zip(times, cols):
        val = fits_row.get(col, np.nan)
        if val is not None and not (isinstance(val, float) and np.isnan(val)):
            t_pts.append(float(t_pt))
            # Cap at 1.0 for AUDC: back-extrapolated values above MSRP inflate
            # the area and make GPUs with scaling artifacts look like better
            # value holders. Depreciation is measured FROM MSRP, not above it.
            y_pts.append(min(float(val), 1.0))
    if len(t_pts) < 2:
        return np.nan
    t_arr = np.array(t_pts)
    y_arr = np.array(y_pts)
    # Normalise by actual integration range, not a fixed t_max.
    # Dividing by t_max=60 when the integration only spans [12, 60] (e.g. t=0
    # is NaN) under-normalises AUDC by 48/60=0.80, deflating it relative to
    # GPUs with complete curves. Using the actual range keeps AUDC on [0, 1]
    # regardless of which time points are present.
    actual_range = float(t_arr[-1] - t_arr[0])
    if actual_range <= 0:
        return np.nan
    _trapz = getattr(np, "trapezoid", np.trapz)  # NumPy 2.0+ renamed trapz
    return _trapz(y_arr, t_arr) / actual_range


# ── Build ranking table ───────────────────────────────────────────────────────

def build_ranking(fits_df, df):
    """
    fits_df: output of depreciation_curves.py (curve_fit_results.csv)
    df: full combined dataset from data_prep.load_data()
    """
    # MSRP from data — use msrp_canonical (median across all rows per GPU) so
    # abs_loss_usd is computed on the same reference price as price_ratio.
    # data_prep.py computes msrp_canonical = median(msrp) per GPU; using .first()
    # on the raw msrp column could return a stale or inconsistent value.
    msrp_col = "msrp_canonical" if "msrp_canonical" in df.columns else "msrp"
    msrp_map = (df[df["condition"] == "NEW"]
                  .groupby("gpu_name")[msrp_col]
                  .median()
                  .reset_index()
                  .rename(columns={msrp_col: "msrp_usd"}))

    ranking = fits_df.merge(msrp_map, on="gpu_name", how="left")
    # Fill missing MSRP from canonical reference (GPUs absent from retail CSV)
    ranking["msrp_usd"] = ranking["msrp_usd"].fillna(
        ranking["gpu_name"].map(MSRP_REFERENCE)
    )

    # Core metrics
    ranking["tvr"]      = ranking["proj_yr5_ratio"]
    ranking["pct_loss"] = pct_loss(ranking["tvr"])
    ranking["abs_loss_usd"] = (1 - ranking["tvr"]) * ranking["msrp_usd"]

    # AUDC — computed from fitted curve columns (proj_t0 … proj_t60).
    # These columns come from depreciation_curves.py which uses the Keepa-extended
    # data back to launch, giving all GPUs a common t=0 baseline.  Using raw retail
    # data here would give older GPUs (T4, V100) only their last 22 months of history,
    # making AUDC non-comparable across GPUs with different observation horizons.
    ranking["audc"] = ranking.apply(audc_from_curve, axis=1)

    # ── Composite rank (lower number = worse depreciator) ─────────────────────
    # Each metric ranked ascending (rank 1 = worst).
    # NOTE: pct_loss is excluded — it equals (1 - TVR) * 100, making it a
    # monotone transform of TVR. Including both would double-weight TVR in the
    # composite (OECD Handbook on Composite Indicators §4.3 collinearity rule).
    #
    # half_life_months NaN handling: NaN occurs for 'observed' method GPUs (real
    # t=60 data — most trustworthy) and power-law fits with floor ≥ 0.5 (slow
    # depreciators that never reach 50% MSRP). These are structurally different
    # NaN causes that must not be conflated via imputation. Use na_option='keep'
    # so NaN rows are excluded from the composite mean rather than penalised as
    # rank-last. pandas .mean(axis=1) already skips NaN by default.
    #
    # AUDC NaN: Previously blocked for appreciating observed-method GPUs, leaving
    # ~13 GPUs without AUDC. The back-extrapolation fix in depreciation_curves.py
    # (_curve_from_canonical_scaled) now caps intermediate values at 1.0 instead
    # of blocking entirely, so all observed GPUs get a valid AUDC.
    # rank 1 = worst depreciator: lowest TVR, highest dollar loss, lowest AUDC
    # half_life_months is EXCLUDED from composite: GPUs with NaN half_life
    # (observed method, slow depreciators) would get mean of 3 ranks while
    # others get mean of 4, making scores non-comparable.  half_life is kept
    # as a display column only.
    for col, asc in [("tvr", True), ("abs_loss_usd", False),
                     ("audc", True)]:
        if col in ranking.columns and ranking[col].notna().any():
            # audc NaN: use 'keep' to exclude from composite mean
            # rather than penalising with worst rank (which would punish observed/
            # appreciating GPUs unfairly — their NaN is structural, not data-poor)
            na_opt = "keep" if col == "audc" else "bottom"
            ranking[f"rank_{col}"] = ranking[col].rank(ascending=asc,
                                                        na_option=na_opt)

    rank_cols = [c for c in ranking.columns if c.startswith("rank_")]
    ranking["composite_score"] = ranking[rank_cols].mean(axis=1)
    # method='min' (competition ranking): tied GPUs share the lower rank number
    # and the next rank is skipped, preventing duplicate integer ranks from
    # default method='average' which produces non-integer 2.5, truncated to 2.
    ranking["overall_rank"]    = ranking["composite_score"].rank(ascending=True, method="min").astype(int)
    ranking = ranking.sort_values("overall_rank")

    # ── Confidence weight & reliability flag ──────────────────────────────────
    # confidence_weight: Tier 1 = 1.0, Tier 2 = 0.7, Tier 3 = 0.4.
    # NOT used to weight the composite score (that would be opaque) — provided
    # so downstream consumers can filter / sort by data reliability.
    tier_weight_map = {1: 1.0, 2: 0.7, 3: 0.4}
    if "fit_tier" in ranking.columns:
        ranking["confidence_weight"] = (
            ranking["fit_tier"]
            .apply(lambda t: tier_weight_map.get(int(t), 0.4) if pd.notna(t) else 0.4)
        )
    else:
        ranking["confidence_weight"] = 0.4

    # reliability: combined assessment of conf_flag (CI width) and fit_tier
    # (data richness).  HIGH requires both strong data AND tight CI.
    def _reliability(row):
        conf = str(row.get("conf_flag", "")).upper()
        tier = int(row["fit_tier"]) if pd.notna(row.get("fit_tier")) else 3
        if tier == 1 and conf == "HIGH":
            return "HIGH"
        if tier <= 2 and conf in ("HIGH", "MEDIUM"):
            return "MEDIUM"
        return "LOW"

    ranking["reliability"] = ranking.apply(_reliability, axis=1)

    return ranking


# ── Demand-shock section ──────────────────────────────────────────────────────

def shock_gpu_summary(df):
    """
    Two scenarios for demand-shock GPUs:
    (a) Shock persists, then decays at proxy rate from CURRENT level to t=60 from launch
    (b) Price normalises to MSRP today, then decays at proxy rate to t=60 from launch

    TVR is always projected to t=60 months from launch (consistent with main ranking).
    time_to_t60 = max(0, 60 - current_age_months) is used so the decay window is
    measured from NOW to the 5-year mark, not 60 additional months from now.
    """
    shock = df[(df["demand_shock"]) & (df["condition"] == "NEW")].copy()
    if shock.empty:
        return

    cutoff = shock["date"].max() - pd.Timedelta(days=90)
    recent = (shock[shock["date"] >= cutoff]
              .groupby("gpu_name")
              .agg(recent_ratio=("price_ratio", "median"),
                   msrp=("msrp_canonical" if "msrp_canonical" in shock.columns else "msrp", "median"),
                   recent_age=("age_months", "median"))
              .reset_index())

    print("=" * 60)
    print("DEMAND-SHOCK GPUs (scenario analysis — also included in main ranking)")
    print("TVR projected to t=60 months from launch")
    print("=" * 60)
    for _, row in recent.iterrows():
        gpu            = row["gpu_name"]
        ratio_a        = row["recent_ratio"]
        current_age    = float(row["recent_age"]) if not np.isnan(row["recent_age"]) else 0.0
        time_to_t60    = max(0.0, 60.0 - current_age)

        # Use segment-specific k/floor; fall back to SHOCK_PROXY constants
        seg = gpu_segment(gpu)
        proxy_k, proxy_floor = SEG_K_FALLBACK.get(seg, (SHOCK_PROXY_K, SHOCK_PROXY_FLOOR))

        # Scenario A: shock premium persists, then decays at proxy rate from CURRENT level to t=60.
        # Uses floor-model form (consistent with Scenario B) so TVR cannot fall
        # below proxy_floor even for long time_to_t60 windows.
        tvr_a = proxy_floor + max(0, ratio_a - proxy_floor) * np.exp(-proxy_k * time_to_t60)

        # Scenario B: price snaps to MSRP now, then decays at proxy rate to t=60
        tvr_b = proxy_floor + max(0, 1 - proxy_floor) * np.exp(-proxy_k * time_to_t60)

        print(f"  {gpu} [{seg}]:  current ratio {ratio_a:.2f}x MSRP  "
              f"(age ~{current_age:.0f} mo, {time_to_t60:.0f} mo to 5yr mark)")
        print(f"    Scenario A (shock persists → TVR at yr5): {tvr_a:.3f}  "
              f"({(1-tvr_a)*100:.1f}% loss)")
        print(f"    Scenario B (normalises to MSRP → TVR at yr5): {tvr_b:.3f}  "
              f"({(1-tvr_b)*100:.1f}% loss)")
    print()


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import os

    df = load_data(verbose=False)

    fits_path = "outputs/curve_fit_results.csv"
    if not os.path.exists(fits_path):
        print(f"{fits_path} not found — run depreciation_curves.py first.")
        sys.exit(1)

    fits_df = pd.read_csv(fits_path)
    ranking = build_ranking(fits_df, df)

    display_cols = ["overall_rank", "gpu_name", "reliability", "msrp_usd", "tvr",
                    "pct_loss", "abs_loss_usd", "half_life_months",
                    "audc", "conf_flag", "confidence_weight", "proj_ci_lo", "proj_ci_hi"]
    display_cols = [c for c in display_cols if c in ranking.columns]

    print("=" * 70)
    print("5-YEAR DEPRECIATION RANKING  (rank 1 = worst depreciator)")
    print("TVR = projected price / MSRP at year 5")
    print("conf_flag: LOW = wide uncertainty, treat projection with caution")
    print("=" * 70)
    print(ranking[display_cols].to_string(index=False))

    print()
    shock_gpu_summary(df)

    # ── Save FIRST (before display, so a display error can't block the file) ──
    os.makedirs("outputs", exist_ok=True)
    ranking.to_csv("outputs/depreciation_ranking.csv", index=False)
    print("Saved → outputs/depreciation_ranking.csv")

    # ── Top 5 worst ───────────────────────────────────────────────────────────
    worst = ranking.head(5)
    print("=" * 60)
    print("TOP 5 WORST DEPRECIATORS (5-year projection)")
    print("=" * 60)
    for _, row in worst.iterrows():
        print(f"  #{int(row['overall_rank'])}  {row['gpu_name']}")
        print(f"      TVR {row['tvr']:.3f}  |  "
              f"{row['pct_loss']:.1f}% loss  |  "
              f"half-life {row.get('half_life_months', np.nan):.1f} mo  |  "
              f"[{row.get('proj_ci_lo', np.nan):.3f}, {row.get('proj_ci_hi', np.nan):.3f}] CI  |  "
              f"{row.get('conf_flag', 'N/A')} confidence")
    print()
