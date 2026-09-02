"""
generate_family_curves.py
Generate pooled curves for GPU families and segments.
Same style as individual charts: single panel, raw cloud,
condition-colored scatter, fan CI, ±1σ, fitted curve.
X-axis is months from launch (families have mixed launch dates).
"""

import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from scipy.optimize import curve_fit

from data_prep import load_data, load_datacenter_supplement, LAUNCH_DATES
from depreciation_curves import GPU_SEGMENTS

OUTPUT_DIR = "outputs/curves"
KEEPA_PATH = "outputs/keepa_monthly.csv"

GPU_FAMILIES = {
    "Tesla V100 Family": [
        "Tesla V100 SXM2 16 GB", "Tesla V100 SXM2 32 GB",
        "Tesla V100 PCIe 16 GB", "Tesla V100 PCIe 32 GB",
        "Tesla V100S PCIe 32 GB",
        # FHHL merged into PCIe 16GB via GPU_NAME_ALIASES
    ],
    "A100 Family": [
        "A100 SXM4 40 GB", "A100 SXM4 80 GB",
        "A100 PCIe 40 GB", "A100 PCIe 80 GB", "A100X",
    ],
    "H100 Family": [
        "H100 SXM5 64 GB", "H100 SXM5 80 GB", "H100 SXM5 94 GB",
        "H100 PCIe 80 GB", "H100 PCIe 94 GB",
    ],
    "H200 Family": ["H200 SXM", "H200 NVL"],
    "RTX 30-series": [
        "GeForce RTX 3060", "GeForce RTX 3060 Ti", "GeForce RTX 3070",
        "GeForce RTX 3070 Ti", "GeForce RTX 3080", "GeForce RTX 3080 Ti",
        "GeForce RTX 3090", "GeForce RTX 3090 Ti",
    ],
    "RTX 40-series": [
        "GeForce RTX 4060", "GeForce RTX 4060 Ti 8 GB", "GeForce RTX 4060 Ti 16 GB",
        "GeForce RTX 4070", "GeForce RTX 4070 SUPER", "GeForce RTX 4070 Ti",
        "GeForce RTX 4070 Ti SUPER", "GeForce RTX 4080", "GeForce RTX 4080 SUPER",
        "GeForce RTX 4090", "GeForce RTX 4090 D",
    ],
    "Quadro RTX": ["Quadro RTX 4000", "Quadro RTX 5000", "Quadro RTX 6000"],
    "RTX A-series": ["RTX A2000", "RTX A4000", "RTX A4500", "RTX A5000", "RTX A6000"],
    "RTX Ada Generation": ["RTX 4000 Ada Generation", "RTX 6000 Ada Generation"],
}

SEGMENT_GROUPS = {
    "Datacenter GPUs": "DATACENTER",
    "Workstation GPUs": "WORKSTATION",
    "Consumer GPUs": "CONSUMER",
}

SEG_COLORS = {"DATACENTER": "#1f77b4", "WORKSTATION": "#ff7f0e", "CONSUMER": "#2ca02c"}
COND_COLORS = {"NEW": "#2196F3", "USED": "#FF9800", "REFURBISHED": "#9C27B0"}
COND_MARKERS = {"NEW": "o", "USED": "s", "REFURBISHED": "D"}
RAW_CLOUD_MAX = 1500


def sanitize(name):
    return name.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")


def exp_floor(t, floor, k):
    return floor + (1 - floor) * np.exp(-k * t)


def pool_observations(gpu_names, df, keepa, supp):
    """Pool monthly + raw observations from multiple GPUs."""
    monthly_pts = []
    raw_pts = []

    for gpu in gpu_names:
        gpu_data = df[df["gpu_name"] == gpu]
        for cond in ["NEW", "USED", "REFURBISHED"]:
            cd = gpu_data[gpu_data["condition"] == cond]
            if len(cd) == 0:
                continue
            # Monthly medians
            mm = (cd.groupby(pd.Grouper(key="date", freq="ME"))
                  .agg(price_ratio=("price_ratio", "median"),
                       age_months=("age_months", "median"))
                  .dropna().reset_index())
            for _, r in mm.iterrows():
                monthly_pts.append({"age": r["age_months"], "ratio": r["price_ratio"],
                                    "condition": cond})
            # Raw for cloud
            for _, r in cd[["age_months", "price_ratio", "condition"]].dropna().iterrows():
                if r["price_ratio"] <= 2.5:
                    raw_pts.append({"age": r["age_months"], "ratio": r["price_ratio"],
                                    "condition": r["condition"]})

        if keepa is not None:
            for _, r in keepa[keepa["gpu_name"] == gpu].iterrows():
                monthly_pts.append({"age": r["age_months"], "ratio": r["price_ratio"],
                                    "condition": "NEW"})

        if supp is not None:
            gs = supp[supp["gpu_name"] == gpu]
            if "condition" in gs.columns:
                for _, r in gs.iterrows():
                    c = r.get("condition", "NEW")
                    monthly_pts.append({"age": r["age_months"], "ratio": r["price_ratio"],
                                        "condition": c if pd.notna(c) else "NEW"})

    monthly = pd.DataFrame(monthly_pts) if monthly_pts else pd.DataFrame(columns=["age", "ratio", "condition"])
    raw = pd.DataFrame(raw_pts) if raw_pts else pd.DataFrame(columns=["age", "ratio", "condition"])

    if len(raw) > RAW_CLOUD_MAX:
        raw = raw.sample(RAW_CLOUD_MAX, random_state=42)

    return monthly, raw


def fit_and_plot(name, gpu_names, monthly, raw, output_dir, color):
    """Derive family curve from individual GPU results (curve_fit_results.csv).
    Averages per-GPU fitted curves rather than re-fitting from pooled raw data,
    ensuring family TVR is consistent with individual members."""

    fig, ax = plt.subplots(figsize=(11, 6.5))

    # Load individual GPU results and average their curves
    tvr = None
    sigma_yr5 = None
    p_below_10 = None
    has_fit = False

    try:
        cfr = pd.read_csv("outputs/curve_fit_results.csv")
        members = cfr[cfr["gpu_name"].isin(gpu_names)]
        if len(members) >= 1:
            # Average the per-GPU curve points (proj_t0...proj_t60)
            curve_cols = [f"proj_t{t}" for t in [0, 12, 24, 36, 48, 60]]
            sigma_cols = [f"sigma_t{t}" for t in [0, 12, 24, 36, 48, 60]]
            anchor_t = np.array([0, 12, 24, 36, 48, 60])

            avg_curve = members[curve_cols].mean().values
            # Sigma: use max of member sigmas (conservative — widest uncertainty)
            if all(c in members.columns for c in sigma_cols):
                avg_sigma = members[sigma_cols].max().values
            else:
                avg_sigma = np.full(6, 0.10)

            # Interpolate to smooth curve for plotting
            # Extend anchor points beyond t=60 so CubicSpline handles the
            # full range smoothly — no np.where boundary kink at t=60
            from scipy.interpolate import CubicSpline
            t_smooth = np.linspace(0, 120, 400)
            slope = (avg_curve[5] - avg_curve[4]) / 12.0
            v_84 = max(avg_curve[5] + slope * 24, 0.0)
            v_120 = max(avg_curve[5] + slope * 60, 0.0)
            c_t_ext = np.append(anchor_t, [84, 120])
            c_v_ext = np.append(avg_curve, [v_84, v_120])
            cs = CubicSpline(c_t_ext, c_v_ext, bc_type="natural")
            v_smooth = np.clip(cs(t_smooth), 0.0, 1.0)

            # Interpolate sigma with CubicSpline — smooth, no kinks at t=60
            # Extend sigma gently beyond t=60 (10% growth at 7yr, 20% at 10yr)
            sigma_at_60 = avg_sigma[5]
            s_t_ext = np.append(anchor_t, [84, 120])
            s_v_ext = np.append(avg_sigma, [sigma_at_60 * 1.1, sigma_at_60 * 1.2])
            cs_sigma = CubicSpline(s_t_ext, s_v_ext, bc_type="natural")
            v_sigma = np.maximum(cs_sigma(t_smooth), 0.0)

            # Stats from members
            tvr = float(members["proj_yr5_ratio"].mean())
            sigma_yr5 = float(members["sigma_yr5"].mean())
            p_below_10 = float(members["p_below_10pct"].mean())
            has_fit = True

            # Determine where data ends (max of member data ages)
            data_end = 0
            for _, m in members.iterrows():
                age_str = str(m.get("age_range_months", ""))
                if "–" in age_str:
                    try:
                        data_end = max(data_end, float(age_str.split("–")[1]))
                    except (ValueError, IndexError):
                        pass

            # ±1σ lines — single smooth pass, no split
            upper_band = np.minimum(v_smooth + v_sigma, 1.0)
            lower_band = np.maximum(v_smooth - v_sigma, 0)
            ax.plot(t_smooth, upper_band, "--", color=color,
                    linewidth=0.8, alpha=0.4, zorder=3, label="\u00B11 Std Dev")
            ax.plot(t_smooth, lower_band, "--", color=color,
                    linewidth=0.8, alpha=0.4, zorder=3)

            # Model curve — solid where data exists, dotted where predictive
            # Split at data_end (max observed age across family members)
            split = max(data_end, 1)
            mask_solid = t_smooth <= split + 2   # slight overlap for seamless join
            mask_dot = t_smooth >= split - 2
            if mask_solid.sum() > 1:
                ax.plot(t_smooth[mask_solid], v_smooth[mask_solid], "-", color=color,
                        linewidth=2.5, zorder=4, label="Model")
            if mask_dot.sum() > 1:
                ax.plot(t_smooth[mask_dot], v_smooth[mask_dot], ":", color=color,
                        linewidth=2, alpha=0.7, zorder=4, label="Predictive")

            # TVR annotation
            idx_60 = np.argmin(np.abs(t_smooth - 60))
            tvr_on_curve = float(v_smooth[idx_60])
            _text_y = tvr_on_curve + 0.08 if tvr_on_curve < 0.85 else tvr_on_curve - 0.12
            _text_y = max(0.05, min(_text_y, 0.95))
            ax.annotate(f"TVR: {tvr*100:.1f}%", xy=(60, tvr_on_curve),
                        xytext=(45, _text_y),
                        fontsize=11, fontweight="bold", color=color,
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.2))
    except Exception as e:
        print(f"  [!] Could not derive family curve for {name}: {e}")

    # Reference lines
    ax.axhline(y=1.0, color="#cccccc", linestyle="--", linewidth=1, zorder=0)
    ax.axhline(y=0.10, color="black", linestyle=":", linewidth=1, alpha=0.5, zorder=0)
    ax.axvline(x=60, color="black", linestyle=":", linewidth=1, alpha=0.5, zorder=0)

    # Title
    n_gpus = len(gpu_names)
    members_short = ", ".join(gpu_names[:3])
    if n_gpus > 3:
        members_short += f" + {n_gpus - 3} more"
    ax.set_title(f"{name}  ({n_gpus} GPUs)\n{members_short}",
                 fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("Years from Launch", fontsize=11)
    ax.set_ylabel("Price / MSRP", fontsize=11)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

    ax.set_ylim(0, 1.05)
    ax.set_xlim(-1, 122)
    ax.set_xticks([0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120])
    ax.set_xticklabels(["Launch", "1yr", "2yr", "3yr", "4yr", "5yr", "6yr", "7yr", "8yr", "9yr", "10yr"], fontsize=8)
    # Badge (disabled)
    # ax.text(0.02, 0.98, name, transform=ax.transAxes,
    #         fontsize=9, fontweight="bold", color="white",
    #         bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.8),
    #         va="top", ha="left")

    ax.legend(loc="upper right", fontsize=7, framealpha=0.8, ncol=2)
    ax.grid(True, alpha=0.2)

    # Caption
    if tvr is not None and sigma_yr5 is not None:
        tvr_pct = tvr * 100
        sigma_pct = sigma_yr5 * 100
        p10_pct = p_below_10 * 100 if p_below_10 is not None else 0
        caption = (f"5-Year Residual Value: {tvr_pct:.1f}%    |    "
                   f"P(below 10% at 5yr): {p10_pct:.5f}%    |    "
                   f"Std Dev: \u00B1{sigma_pct:.1f}pp")
        fig.text(0.5, 0.01, caption, ha="center", va="bottom",
                 fontsize=9, color="#555555", style="italic")

    fig.tight_layout(rect=[0, 0.04, 1, 1])

    fname = sanitize(name) + ".png"
    fig.savefig(os.path.join(output_dir, fname), dpi=150, bbox_inches="tight")
    plt.close(fig)
    return fname


def main():
    family_dir = os.path.join(OUTPUT_DIR, "families")
    segment_dir = os.path.join(OUTPUT_DIR, "segments")
    os.makedirs(family_dir, exist_ok=True)
    os.makedirs(segment_dir, exist_ok=True)

    print("Loading data...")
    df = load_data(verbose=False)
    keepa = pd.read_csv(KEEPA_PATH) if os.path.exists(KEEPA_PATH) else None
    supp = load_datacenter_supplement(verbose=False)

    # Family charts
    print(f"\n{len(GPU_FAMILIES)} family curves:")
    for name, members in GPU_FAMILIES.items():
        seg = next((s for s, gpus in GPU_SEGMENTS.items() if members[0] in gpus), "DATACENTER")
        color = SEG_COLORS.get(seg, "#7f7f7f")
        monthly, raw = pool_observations(members, df, keepa, supp)
        fname = fit_and_plot(name, members, monthly, raw, family_dir, color)
        print(f"  {name:25s} → families/{fname}  ({len(monthly)} monthly, {len(raw)} raw)")

    # Segment charts
    print(f"\n{len(SEGMENT_GROUPS)} segment curves:")
    for label, seg_key in SEGMENT_GROUPS.items():
        members = GPU_SEGMENTS.get(seg_key, [])
        color = SEG_COLORS.get(seg_key, "#7f7f7f")
        monthly, raw = pool_observations(members, df, keepa, supp)
        fname = fit_and_plot(label, members, monthly, raw, segment_dir, color)
        print(f"  {label:25s} → segments/{fname}  ({len(monthly)} monthly, {len(raw)} raw)")

    print("\nDone.")


if __name__ == "__main__":
    main()
