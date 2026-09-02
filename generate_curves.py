"""
generate_curves.py
Generate individual depreciation curve images for every GPU.
Shows: faint raw cloud, condition-colored monthly medians, fitted curve,
fan CI band, ±1σ lines, extrapolation to present for older GPUs.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.interpolate import PchipInterpolator, CubicSpline

from data_prep import load_data, load_datacenter_supplement, LAUNCH_DATES

OUTPUT_DIR = "outputs/curves"

# ── Display toggles ──
SHOW_RAW_CLOUD = False       # Faint background cloud of individual listings
SHOW_MONTHLY_SCATTER = False # Condition-colored monthly median dots
SHOW_MSRP_IN_TITLE = False   # Show "| MSRP $XX,XXX" in chart title
CSV_PATH = "outputs/curve_fit_results.csv"
KEEPA_PATH = "outputs/keepa_monthly.csv"

SEG_COLORS = {"DATACENTER": "#1f77b4", "WORKSTATION": "#ff7f0e", "CONSUMER": "#2ca02c"}
COND_COLORS = {"NEW": "#2196F3", "USED": "#FF9800", "REFURBISHED": "#9C27B0"}
COND_MARKERS = {"NEW": "o", "USED": "s", "REFURBISHED": "D"}
RAW_CLOUD_MAX = 1000  # max raw points per GPU for faint cloud


def sanitize_filename(name):
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


def get_gpu_age_now(gpu_name):
    from datetime import datetime
    TODAY = datetime(2026, 3, 16)
    launch_str = LAUNCH_DATES.get(gpu_name)
    if not launch_str:
        return 60
    return max(60, (TODAY - pd.to_datetime(launch_str)).days / 30.44)


def load_all_data():
    df = load_data(verbose=False)
    keepa = pd.read_csv(KEEPA_PATH) if os.path.exists(KEEPA_PATH) else None
    supp = load_datacenter_supplement(verbose=False)
    return df, keepa, supp


def get_raw_cloud(gpu_name, df):
    """Get raw individual listings for faint background cloud, randomly sampled."""
    gpu_data = df[df["gpu_name"] == gpu_name][["age_months", "price_ratio", "condition"]].dropna()
    gpu_data = gpu_data[gpu_data["price_ratio"] <= 2.5]
    if len(gpu_data) > RAW_CLOUD_MAX:
        gpu_data = gpu_data.sample(RAW_CLOUD_MAX, random_state=42)
    return gpu_data


def get_monthly_obs(gpu_name, df, keepa, supp):
    """Get monthly median observations by condition."""
    points = []
    gpu_data = df[df["gpu_name"] == gpu_name]
    for cond in ["NEW", "USED", "REFURBISHED"]:
        cd = gpu_data[gpu_data["condition"] == cond]
        if len(cd) == 0:
            continue
        monthly = (cd.groupby(pd.Grouper(key="date", freq="ME"))
                   .agg(price_ratio=("price_ratio", "median"),
                        age_months=("age_months", "median"))
                   .dropna().reset_index())
        for _, r in monthly.iterrows():
            points.append({"age": r["age_months"], "ratio": r["price_ratio"], "condition": cond})

    if keepa is not None:
        for _, r in keepa[keepa["gpu_name"] == gpu_name].iterrows():
            points.append({"age": r["age_months"], "ratio": r["price_ratio"], "condition": "NEW"})

    if supp is not None:
        gs = supp[supp["gpu_name"] == gpu_name]
        if "condition" in gs.columns:
            for _, r in gs.iterrows():
                c = r.get("condition", "NEW")
                points.append({"age": r["age_months"], "ratio": r["price_ratio"],
                                "condition": c if pd.notna(c) else "NEW"})

    return pd.DataFrame(points) if points else pd.DataFrame(columns=["age", "ratio", "condition"])


def make_smooth_curve(anchor_t, anchor_v, max_month):
    valid = ~np.isnan(anchor_v)
    if valid.sum() < 2:
        return anchor_t, anchor_v

    # Build extended anchor points including extrapolation targets,
    # then fit ONE smooth PCHIP through everything — no splice kink.
    ext_t = list(anchor_t[valid])
    ext_v = list(anchor_v[valid])

    if max_month > 60:
        v48 = anchor_v[4] if valid[4] else anchor_v[valid][-2]
        v60 = anchor_v[5] if valid[5] else anchor_v[valid][-1]
        floor_est = max(0.0, 2 * v60 - v48)
        if v60 > floor_est and v48 > v60:
            k_eff = -np.log((v60 - floor_est) / (v48 - floor_est)) / 12.0
            # Add extrapolation anchors at 72, 84, 96, 108, 120
            for t_extra in [72, 84, 96, 108, 120]:
                if t_extra <= max_month:
                    v_extra = floor_est + (v60 - floor_est) * np.exp(-k_eff * (t_extra - 60))
                    ext_t.append(t_extra)
                    ext_v.append(max(v_extra, 0.0))
        else:
            # Flat: extend at v60
            for t_extra in [72, 84, 96, 108, 120]:
                if t_extra <= max_month:
                    ext_t.append(t_extra)
                    ext_v.append(v60)

    ext_t = np.array(ext_t)
    ext_v = np.array(ext_v)

    # Single smooth PCHIP through all anchor points (original + extrapolated)
    n_pts = int(max_month * 200 / 60)  # ~3.3 pts/month throughout
    t = np.linspace(float(ext_t[0]), float(ext_t[-1]), n_pts)
    if len(ext_t) >= 3:
        pchip = PchipInterpolator(ext_t, ext_v)
        v = pchip(t)
    else:
        v = np.interp(t, ext_t, ext_v)

    v = np.maximum(v, 0.0)
    return t, v


def plot_gpu(row, monthly_obs, raw_cloud, output_dir, cap_at_msrp=False):
    gpu = row["gpu_name"]
    seg = row["segment"]
    tier = int(row["fit_tier"])
    method = row["method"]
    tvr = row["proj_yr5_ratio"]
    ci_lo = row["proj_ci_lo"]
    ci_hi = row["proj_ci_hi"]
    sigma_yr5 = row.get("sigma_yr5", np.nan)
    p_below_10 = row.get("p_below_10pct", np.nan)

    launch_str = LAUNCH_DATES.get(gpu, "Unknown")
    launch_display = pd.to_datetime(launch_str).strftime("%b %Y") if launch_str != "Unknown" else "Unknown"
    age_now = get_gpu_age_now(gpu)
    n_months = int(row["n_months"]) if pd.notna(row.get("n_months")) else 0

    # Determine where data ends — beyond this the curve is speculative
    data_end_month = 0
    if n_months > 0:
        age_range = str(row.get("age_range_months", ""))
        if "–" in age_range:
            try:
                data_end_month = float(age_range.split("–")[1])
            except (ValueError, IndexError):
                data_end_month = min(age_now, 60)
        else:
            data_end_month = min(age_now, 60)
    max_month = 120  # 10-year window

    anchor_t = np.array([0, 12, 24, 36, 48, 60])
    cols = ["proj_t0", "proj_t12", "proj_t24", "proj_t36", "proj_t48", "proj_t60"]
    anchor_v = np.array([row[c] if pd.notna(row[c]) else np.nan for c in cols])

    # Cap anchor values BEFORE interpolation so the spline shows
    # depreciation within 0-100%, not a flat line at the ceiling
    if cap_at_msrp:
        anchor_v = np.minimum(anchor_v, 1.0)
        tvr = min(tvr, 1.0)
        if pd.notna(ci_hi):
            ci_hi = min(ci_hi, 1.0)

    t_curve, v_curve = make_smooth_curve(anchor_t, anchor_v, 120)  # 10yr

    if cap_at_msrp:
        v_curve = np.minimum(v_curve, 1.0)  # safety clip on interpolated values

    # Build ±1σ band — use per-time-point MC sigma when available
    # Smooth with CubicSpline to avoid sharp kinks at anchor points and t=60
    sigma_band = None
    sigma_cols = [f"sigma_t{t}" for t in [0, 12, 24, 36, 48, 60]]
    sigma_anchors = np.array([row[c] if c in row and pd.notna(row[c]) else np.nan for c in sigma_cols])
    sigma_valid = ~np.isnan(sigma_anchors)
    if sigma_valid.sum() >= 2:
        # Build extended sigma anchors for smooth extrapolation beyond t=60
        s_t = anchor_t[sigma_valid]
        s_v = sigma_anchors[sigma_valid]
        sigma_at_60 = s_v[-1]
        # Extend to t=120 with gentle linear growth (sigma grows slowly beyond 5yr)
        s_t_ext = np.append(s_t, [84, 120])
        s_v_ext = np.append(s_v, [sigma_at_60 * 1.1, sigma_at_60 * 1.2])
        if len(s_t_ext) >= 3:
            cs_sigma = CubicSpline(s_t_ext, s_v_ext, bc_type="natural")
            sigma_band = np.maximum(cs_sigma(t_curve), 0.0)
        else:
            sigma_band = np.interp(t_curve, s_t_ext, s_v_ext)
    elif pd.notna(sigma_yr5) and sigma_yr5 > 0:
        # Fallback: smooth fan using sqrt scaling (not linear — avoids kink at t=60)
        sigma_band = sigma_yr5 * np.sqrt(np.clip(t_curve, 0, 120) / 60.0)
        sigma_band = np.maximum(sigma_band, 0.0)

    # CI band — use per-time-point MC percentiles when available
    ci_band = None
    ci_lo_cols = [f"ci_lo_t{t}" for t in [0, 12, 24, 36, 48, 60]]
    ci_hi_cols = [f"ci_hi_t{t}" for t in [0, 12, 24, 36, 48, 60]]
    ci_lo_anchors = np.array([row[c] if c in row and pd.notna(row[c]) else np.nan for c in ci_lo_cols])
    ci_hi_anchors = np.array([row[c] if c in row and pd.notna(row[c]) else np.nan for c in ci_hi_cols])
    ci_lo_valid = ~np.isnan(ci_lo_anchors)
    ci_hi_valid = ~np.isnan(ci_hi_anchors)
    if ci_lo_valid.sum() >= 2 and ci_hi_valid.sum() >= 2:
        # Smooth CI bands with CubicSpline — avoids kinks at anchor points
        lo_t = anchor_t[ci_lo_valid]
        lo_v = ci_lo_anchors[ci_lo_valid]
        hi_t = anchor_t[ci_hi_valid]
        hi_v = ci_hi_anchors[ci_hi_valid]
        # Extend to t=120 with gentle linear extrapolation
        lo_60 = lo_v[-1]
        hi_60 = hi_v[-1]
        lo_slope = (lo_v[-1] - lo_v[-2]) / max(lo_t[-1] - lo_t[-2], 1) if len(lo_v) >= 2 else 0
        hi_slope = (hi_v[-1] - hi_v[-2]) / max(hi_t[-1] - hi_t[-2], 1) if len(hi_v) >= 2 else 0
        lo_t_ext = np.append(lo_t, [84, 120])
        lo_v_ext = np.append(lo_v, [lo_60 + lo_slope * 24, lo_60 + lo_slope * 60])
        hi_t_ext = np.append(hi_t, [84, 120])
        hi_v_ext = np.append(hi_v, [hi_60 + hi_slope * 24, hi_60 + hi_slope * 60])
        if len(lo_t_ext) >= 3:
            cs_lo = CubicSpline(lo_t_ext, lo_v_ext, bc_type="natural")
            cs_hi = CubicSpline(hi_t_ext, hi_v_ext, bc_type="natural")
            ci_lower = cs_lo(t_curve)
            ci_upper = cs_hi(t_curve)
        else:
            ci_lower = np.interp(t_curve, lo_t_ext, lo_v_ext)
            ci_upper = np.interp(t_curve, hi_t_ext, hi_v_ext)
        ci_lower = np.maximum(ci_lower, 0)
        if cap_at_msrp:
            ci_upper = np.minimum(ci_upper, 1.0)
        ci_band = (ci_lower, ci_upper)
    elif pd.notna(ci_lo) and pd.notna(ci_hi):
        # Fallback: linear fan (for observed-method GPUs without per-time MC)
        ci_frac = np.where(t_curve <= 60,
                           np.interp(t_curve, [0, 60], [0, 1]),
                           1 + (t_curve - 60) / 60)
        ci_upper = v_curve + ci_frac * (ci_hi - tvr)
        ci_lower = v_curve + ci_frac * (ci_lo - tvr)
        ci_lower = np.maximum(ci_lower, 0)
        if cap_at_msrp:
            ci_upper = np.minimum(ci_upper, 1.0)
        ci_band = (ci_lower, ci_upper)

    color = SEG_COLORS.get(seg, "#7f7f7f")
    fig, ax = plt.subplots(figsize=(11, 6.5))

    # Debug: faint raw cloud
    if SHOW_RAW_CLOUD and len(raw_cloud) > 0:
        for cond in ["REFURBISHED", "USED", "NEW"]:
            cd = raw_cloud[raw_cloud["condition"] == cond]
            if len(cd) > 0:
                ax.scatter(cd["age_months"], cd["price_ratio"],
                           c=COND_COLORS.get(cond, "#ccc"), marker=".",
                           s=3, alpha=0.08, zorder=0)

    # Debug: monthly median scatter
    if SHOW_MONTHLY_SCATTER and len(monthly_obs) > 0:
        obs = monthly_obs[monthly_obs["ratio"] <= 2.5]
        for cond in ["REFURBISHED", "USED", "NEW"]:
            cd = obs[obs["condition"] == cond]
            if len(cd) > 0:
                ax.scatter(cd["age"], cd["ratio"],
                           c=COND_COLORS.get(cond, "#999"),
                           marker=COND_MARKERS.get(cond, "o"),
                           s=20, alpha=0.5, zorder=2, label=cond.title())

    # HPD CI band disabled — asymmetric bands were confusing on the charts.
    # The ±1σ lines below provide symmetric, model-centred uncertainty instead.
    # HPD data is still computed and available in the CSV (ci_lo_t*, ci_hi_t*).

    # ±1σ lines
    if sigma_band is not None:
        ax.plot(t_curve, np.minimum(v_curve + sigma_band, 1.0), "--", color=color, linewidth=0.8, alpha=0.4, zorder=3, label="±1 Std Dev")
        ax.plot(t_curve, np.maximum(v_curve - sigma_band, 0), "--", color=color, linewidth=0.8, alpha=0.4, zorder=3)

    # Model curve — solid where we have data, dotted where speculative
    mask_data = t_curve <= data_end_month
    mask_spec = t_curve >= data_end_month

    if mask_data.sum() > 1:
        ax.plot(t_curve[mask_data], v_curve[mask_data], "-",
                color=color, linewidth=2.5, zorder=4, label="Model")
    if mask_spec.sum() > 1:
        ax.plot(t_curve[mask_spec], v_curve[mask_spec], ":",
                color=color, linewidth=2, alpha=0.7, zorder=4, label="Predictive")

    # Reference lines
    ax.axhline(y=1.0, color="#cccccc", linestyle="--", linewidth=1, zorder=0)
    ax.axhline(y=0.10, color="black", linestyle=":", linewidth=1, alpha=0.5, zorder=0)  # 10% MSRP
    ax.axvline(x=60, color="black", linestyle=":", linewidth=1, alpha=0.5, zorder=0)    # 5yr mark

    # TVR annotation — find actual curve value at t=60 for arrow target
    idx_60 = np.argmin(np.abs(t_curve - 60))
    tvr_on_curve = float(v_curve[idx_60])
    # Place text above or below depending on where there's room
    if tvr_on_curve > 0.70:
        text_y = tvr_on_curve - 0.12
    elif tvr_on_curve < 0.20:
        text_y = tvr_on_curve + 0.10
    else:
        text_y = tvr_on_curve + 0.08
    # Clamp text position to visible area
    text_y = max(0.05, min(text_y, 0.95))
    ax.annotate(f"TVR: {tvr*100:.1f}%", xy=(60, tvr_on_curve),
                xytext=(45, text_y),
                fontsize=11, fontweight="bold", color=color,
                arrowprops=dict(arrowstyle="->", color=color, lw=1.2))

    # Title
    msrp = row.get("msrp_usd", np.nan)
    msrp_str = f"  |  MSRP ${msrp:,.0f}" if (SHOW_MSRP_IN_TITLE and pd.notna(msrp)) else ""
    title = f"{gpu}  (launched {launch_display}){msrp_str}"
    if SHOW_MONTHLY_SCATTER or SHOW_RAW_CLOUD:
        data_str = f"\n{n_months} months of data" if n_months > 0 else "\nno direct data"
        title += data_str
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Years from Launch", fontsize=11)
    ax.set_ylabel("Price / MSRP", fontsize=11)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

    # Axis limits — strict 0-105% and 0-120 months
    ax.set_ylim(0, 1.05)
    ax.set_xlim(-1, 122)
    ax.set_xticks([0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120])
    ax.set_xticklabels(["Launch", "1yr", "2yr", "3yr", "4yr", "5yr", "6yr", "7yr", "8yr", "9yr", "10yr"],
                        fontsize=8)

    # Segment badge (disabled)
    # ax.text(0.02, 0.98, seg, transform=ax.transAxes,
    #         fontsize=9, fontweight="bold", color="white",
    #         bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.8),
    #         va="top", ha="left")

    ax.legend(loc="upper right", fontsize=7, framealpha=0.8, ncol=2)
    ax.grid(True, alpha=0.2)

    # ── Bottom caption with key stats ──
    sigma_pct = sigma_yr5 * 100 if pd.notna(sigma_yr5) else 0
    sigma_usd = sigma_yr5 * msrp if pd.notna(sigma_yr5) and pd.notna(msrp) else 0
    tvr_pct = min(tvr, 1.0) * 100 if cap_at_msrp else tvr * 100
    p10_pct = p_below_10 * 100 if pd.notna(p_below_10) else 0
    residual_usd = tvr_pct / 100 * msrp if pd.notna(msrp) else 0

    if SHOW_MSRP_IN_TITLE:
        caption = (f"5-Year Residual Value: {tvr_pct:.1f}% (\${residual_usd:,.0f})    |    "
                   f"P(below 10% at 5yr): {p10_pct:.5f}%    |    "
                   f"Std Dev: \u00B1{sigma_pct:.1f}pp (\u00B1\${sigma_usd:,.0f})")
    else:
        caption = (f"5-Year Residual Value: {tvr_pct:.1f}%    |    "
                   f"P(below 10% at 5yr): {p10_pct:.5f}%    |    "
                   f"Std Dev: \u00B1{sigma_pct:.1f}pp")
    fig.text(0.5, 0.01, caption, ha="center", va="bottom",
             fontsize=9, color="#555555", style="italic")

    fig.tight_layout(rect=[0, 0.04, 1, 1])  # make room for caption

    fname = sanitize_filename(gpu) + ".png"
    fig.savefig(os.path.join(output_dir, fname), dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fname


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fits = pd.read_csv(CSV_PATH)
    ranking_path = "outputs/depreciation_ranking.csv"
    if os.path.exists(ranking_path):
        ranking = pd.read_csv(ranking_path)[["gpu_name", "msrp_usd"]]
        fits = fits.merge(ranking, on="gpu_name", how="left")

    print("Loading data...")
    df, keepa, supp = load_all_data()

    print(f"Generating {len(fits)} curves...")
    for _, row in fits.iterrows():
        gpu = row["gpu_name"]
        monthly = get_monthly_obs(gpu, df, keepa, supp)
        raw = get_raw_cloud(gpu, df)
        plot_gpu(row, monthly, raw, OUTPUT_DIR, cap_at_msrp=True)
        print(f"  {gpu:40s}  ({len(monthly)} monthly, {len(raw)} raw)")

    print(f"\nSaved {len(fits)} curves → {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
