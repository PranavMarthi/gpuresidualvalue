"""
generate_worst_case.py
Generate worst-case (mean − 5σ) depreciation curves and CSV for datacenter GPUs.
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.interpolate import PchipInterpolator, CubicSpline

OUTPUT_DIR = "outputs/worst_case"
CSV_PATH = "outputs/curve_fit_results.csv"
RANKING_PATH = "outputs/depreciation_ranking.csv"

TIME_POINTS = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120]
N_SIGMA = 5

from data_prep import LAUNCH_DATES


def sanitize_filename(name):
    return name.replace(" ", "_").replace("/", "-").replace("(", "").replace(")", "")


def get_gpu_age_now(gpu_name):
    from datetime import datetime
    TODAY = datetime(2026, 3, 16)
    launch_str = LAUNCH_DATES.get(gpu_name)
    if not launch_str:
        return 60
    return max(60, (TODAY - pd.to_datetime(launch_str)).days / 30.44)


def make_smooth_curve(anchor_t, anchor_v, max_month):
    valid = ~np.isnan(anchor_v)
    if valid.sum() < 2:
        return anchor_t, anchor_v

    ext_t = list(anchor_t[valid])
    ext_v = list(anchor_v[valid])

    if max_month > 60:
        v48 = anchor_v[4] if valid[4] else anchor_v[valid][-2]
        v60 = anchor_v[5] if valid[5] else anchor_v[valid][-1]
        floor_est = max(0.0, 2 * v60 - v48)
        if v60 > floor_est and v48 > v60:
            k_eff = -np.log((v60 - floor_est) / (v48 - floor_est)) / 12.0
            for t_extra in [72, 84, 96, 108, 120]:
                if t_extra <= max_month:
                    v_extra = floor_est + (v60 - floor_est) * np.exp(-k_eff * (t_extra - 60))
                    ext_t.append(t_extra)
                    ext_v.append(max(v_extra, 0.0))
        else:
            for t_extra in [72, 84, 96, 108, 120]:
                if t_extra <= max_month:
                    ext_t.append(t_extra)
                    ext_v.append(v60)

    ext_t = np.array(ext_t)
    ext_v = np.array(ext_v)

    n_pts = int(max_month * 200 / 60)
    t = np.linspace(float(ext_t[0]), float(ext_t[-1]), n_pts)
    if len(ext_t) >= 3:
        pchip = PchipInterpolator(ext_t, ext_v)
        v = pchip(t)
    else:
        v = np.interp(t, ext_t, ext_v)

    v = np.maximum(v, 0.0)
    return t, v


def compute_worst_case_csv(fits):
    """Compute worst-case table: mean - 5*sigma at each time point."""
    rows = []
    for _, r in fits.iterrows():
        gpu = r["gpu_name"]
        msrp = r.get("msrp_usd", np.nan)
        row = {"gpu_name": gpu, "segment": r["segment"], "msrp_usd": msrp,
               "fit_tier": r["fit_tier"]}

        for t in TIME_POINTS:
            mean_col = f"proj_t{t}"
            sigma_col = f"sigma_t{t}"
            mean_val = r[mean_col] if pd.notna(r.get(mean_col)) else np.nan
            sigma_val = r[sigma_col] if pd.notna(r.get(sigma_col)) else np.nan

            if pd.notna(mean_val) and pd.notna(sigma_val):
                wc_ratio = max(mean_val - N_SIGMA * sigma_val, 0.0)
            else:
                wc_ratio = np.nan

            row[f"mean_t{t}"] = mean_val
            row[f"sigma_t{t}"] = sigma_val
            row[f"worst_case_ratio_t{t}"] = wc_ratio
            if pd.notna(msrp) and pd.notna(wc_ratio):
                row[f"worst_case_usd_t{t}"] = round(wc_ratio * msrp, 2)
            else:
                row[f"worst_case_usd_t{t}"] = np.nan

        # Summary stats at 5yr (t=60)
        row["tvr_mean"] = r["proj_yr5_ratio"]
        row["sigma_yr5"] = r["sigma_yr5"]
        wc_5yr = max(r["proj_yr5_ratio"] - N_SIGMA * r["sigma_yr5"], 0.0)
        row["worst_case_5yr_ratio"] = wc_5yr
        if pd.notna(msrp):
            row["worst_case_5yr_usd"] = round(wc_5yr * msrp, 2)
        else:
            row["worst_case_5yr_usd"] = np.nan

        rows.append(row)

    return pd.DataFrame(rows)


def plot_worst_case(row, fits_row, output_dir):
    """Plot mean curve, ±1σ, and worst-case (−5σ) curve."""
    gpu = row["gpu_name"]
    msrp = row.get("msrp_usd", np.nan)

    # Build mean curve anchors
    anchor_t = np.array([0, 12, 24, 36, 48, 60])
    mean_cols = [f"proj_t{t}" for t in [0, 12, 24, 36, 48, 60]]
    anchor_mean = np.array([fits_row[c] if pd.notna(fits_row[c]) else np.nan for c in mean_cols])
    anchor_mean = np.minimum(anchor_mean, 1.0)

    t_curve, v_mean = make_smooth_curve(anchor_t, anchor_mean, 120)
    v_mean = np.minimum(v_mean, 1.0)

    # Build sigma band
    sigma_cols = [f"sigma_t{t}" for t in [0, 12, 24, 36, 48, 60]]
    sigma_anchors = np.array([fits_row[c] if c in fits_row and pd.notna(fits_row[c]) else np.nan
                               for c in sigma_cols])
    sigma_valid = ~np.isnan(sigma_anchors)
    sigma_band = None
    if sigma_valid.sum() >= 2:
        s_t = anchor_t[sigma_valid]
        s_v = sigma_anchors[sigma_valid]
        sigma_at_60 = s_v[-1]
        s_t_ext = np.append(s_t, [84, 120])
        s_v_ext = np.append(s_v, [sigma_at_60 * 1.1, sigma_at_60 * 1.2])
        if len(s_t_ext) >= 3:
            cs_sigma = CubicSpline(s_t_ext, s_v_ext, bc_type="natural")
            sigma_band = np.maximum(cs_sigma(t_curve), 0.0)
        else:
            sigma_band = np.interp(t_curve, s_t_ext, s_v_ext)

    if sigma_band is None:
        sigma_yr5 = fits_row.get("sigma_yr5", 0.03)
        sigma_band = sigma_yr5 * np.sqrt(np.clip(t_curve, 0, 120) / 60.0)
        sigma_band = np.maximum(sigma_band, 0.0)

    # Worst-case curve
    v_worst = np.maximum(v_mean - N_SIGMA * sigma_band, 0.0)

    # Data end month for solid/dotted split
    age_range = str(fits_row.get("age_range_months", ""))
    data_end_month = 0
    if "–" in age_range:
        try:
            data_end_month = float(age_range.split("–")[1])
        except (ValueError, IndexError):
            data_end_month = 60
    else:
        data_end_month = 60

    # Launch info
    launch_str = LAUNCH_DATES.get(gpu, "Unknown")
    launch_display = pd.to_datetime(launch_str).strftime("%b %Y") if launch_str != "Unknown" else "Unknown"

    # ── Plot ──
    fig, ax = plt.subplots(figsize=(11, 6.5))
    color_mean = "#1f77b4"
    color_worst = "#d62728"

    # Mean curve
    mask_data = t_curve <= data_end_month
    mask_spec = t_curve >= data_end_month
    if mask_data.sum() > 1:
        ax.plot(t_curve[mask_data], v_mean[mask_data], "-", color=color_mean,
                linewidth=2, zorder=4, label="Mean projection")
    if mask_spec.sum() > 1:
        ax.plot(t_curve[mask_spec], v_mean[mask_spec], ":", color=color_mean,
                linewidth=1.5, alpha=0.7, zorder=4)

    # ±1σ dashed
    ax.plot(t_curve, np.minimum(v_mean + sigma_band, 1.0), "--", color=color_mean,
            linewidth=0.7, alpha=0.35, zorder=3, label="±1σ")
    ax.plot(t_curve, np.maximum(v_mean - sigma_band, 0), "--", color=color_mean,
            linewidth=0.7, alpha=0.35, zorder=3)

    # Worst-case (−5σ) curve
    if mask_data.sum() > 1:
        ax.plot(t_curve[mask_data], v_worst[mask_data], "-", color=color_worst,
                linewidth=2.5, zorder=5, label=f"Worst case (−{N_SIGMA}σ)")
    if mask_spec.sum() > 1:
        ax.plot(t_curve[mask_spec], v_worst[mask_spec], ":", color=color_worst,
                linewidth=2, alpha=0.7, zorder=5)

    # Fill between mean and worst case
    ax.fill_between(t_curve, v_worst, v_mean, alpha=0.10, color=color_worst, zorder=2)

    # Reference lines
    ax.axhline(y=1.0, color="#cccccc", linestyle="--", linewidth=1, zorder=0)
    ax.axhline(y=0.10, color="black", linestyle=":", linewidth=1, alpha=0.5, zorder=0)
    ax.axvline(x=60, color="black", linestyle=":", linewidth=1, alpha=0.5, zorder=0)

    # Worst-case annotation at t=60
    idx_60 = np.argmin(np.abs(t_curve - 60))
    wc_at_60 = float(v_worst[idx_60])
    mean_at_60 = float(v_mean[idx_60])

    if wc_at_60 < 0.15:
        text_y = wc_at_60 + 0.08
    else:
        text_y = wc_at_60 - 0.10
    text_y = max(0.05, min(text_y, 0.90))

    wc_label = f"Worst case: {wc_at_60*100:.1f}%"
    if pd.notna(msrp):
        wc_label += f" (${wc_at_60 * msrp:,.0f})"
    ax.annotate(wc_label, xy=(60, wc_at_60),
                xytext=(42, text_y),
                fontsize=10, fontweight="bold", color=color_worst,
                arrowprops=dict(arrowstyle="->", color=color_worst, lw=1.2))

    # Title
    msrp_str = f"  |  MSRP ${msrp:,.0f}" if pd.notna(msrp) else ""
    ax.set_title(f"{gpu}  (launched {launch_display}){msrp_str}\nWorst-Case Analysis (−{N_SIGMA}σ)",
                 fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Years from Launch", fontsize=11)
    ax.set_ylabel("Price / MSRP", fontsize=11)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))
    ax.set_ylim(0, 1.05)
    ax.set_xlim(-1, 122)
    ax.set_xticks([0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120])
    ax.set_xticklabels(["Launch", "1yr", "2yr", "3yr", "4yr", "5yr",
                         "6yr", "7yr", "8yr", "9yr", "10yr"], fontsize=8)

    ax.legend(loc="upper right", fontsize=8, framealpha=0.8)
    ax.grid(True, alpha=0.2)

    # Bottom caption
    sigma_yr5 = fits_row.get("sigma_yr5", 0)
    caption = (f"Mean 5yr: {mean_at_60*100:.1f}%    |    "
               f"Worst case 5yr (−{N_SIGMA}σ): {wc_at_60*100:.1f}%    |    "
               f"σ at 5yr: ±{sigma_yr5*100:.1f}pp")
    if pd.notna(msrp):
        caption += f"    |    Worst case $: ${wc_at_60 * msrp:,.0f}"
    fig.text(0.5, 0.01, caption, ha="center", va="bottom",
             fontsize=9, color="#555555", style="italic")

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fname = sanitize_filename(gpu) + ".png"
    fig.savefig(os.path.join(output_dir, fname), dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fname


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fits = pd.read_csv(CSV_PATH)
    if os.path.exists(RANKING_PATH):
        ranking = pd.read_csv(RANKING_PATH)[["gpu_name", "msrp_usd"]]
        fits = fits.merge(ranking, on="gpu_name", how="left")

    # Filter to datacenter GPUs only
    dc = fits[fits["segment"] == "DATACENTER"].copy()
    print(f"Found {len(dc)} datacenter GPUs")

    # Compute worst-case CSV
    wc_df = compute_worst_case_csv(dc)
    csv_out = os.path.join(OUTPUT_DIR, "worst_case_datacenter.csv")
    wc_df.to_csv(csv_out, index=False)
    print(f"Saved worst-case CSV → {csv_out}")

    # Print summary table
    print(f"\n{'GPU':<35} {'MSRP':>10} {'Mean 5yr':>10} {'−5σ 5yr':>10} {'−5σ $ 5yr':>12}")
    print("─" * 82)
    for _, r in wc_df.sort_values("worst_case_5yr_ratio").iterrows():
        msrp_s = f"${r['msrp_usd']:,.0f}" if pd.notna(r['msrp_usd']) else "N/A"
        wc_usd = f"${r['worst_case_5yr_usd']:,.0f}" if pd.notna(r['worst_case_5yr_usd']) else "N/A"
        print(f"{r['gpu_name']:<35} {msrp_s:>10} {r['tvr_mean']*100:>9.1f}% "
              f"{r['worst_case_5yr_ratio']*100:>9.1f}% {wc_usd:>12}")

    # Generate worst-case charts
    print(f"\nGenerating {len(dc)} worst-case charts...")
    for _, wc_row in wc_df.iterrows():
        gpu = wc_row["gpu_name"]
        fits_row = dc[dc["gpu_name"] == gpu].iloc[0]
        fname = plot_worst_case(wc_row, fits_row, OUTPUT_DIR)
        print(f"  {gpu:40s} → {fname}")

    print(f"\nDone. {len(dc)} charts + CSV → {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
