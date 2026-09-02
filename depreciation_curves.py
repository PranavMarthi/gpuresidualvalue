"""
depreciation_curves.py
Fit depreciation curves per GPU (NEW condition, non-shock, non-left-censored).
Models: exponential-with-floor, power-law-with-floor.
Ensemble: AICc-based Akaike weights.
Uncertainty: Monte Carlo from curve_fit covariance matrix (regularised).

Three-tier hierarchical fitting strategy:
  Tier 1 (INDIVIDUAL): GPU has ≥TIER1_MIN_MONTHS data starting before age
           TIER1_MAX_MIN_AGE. Full individual fit with both models + ensemble.
  Tier 2 (CONSTRAINED): Sparse GPUs / mid-lifecycle-only data.
           Fix k from segment canonical; fit floor only from observed window.
  Tier 3 (DEFAULT): Very sparse or all fits failed.
           Use segment canonical curve scaled to observed median level.

Outputs per GPU (in addition to existing cols):
  - sigma_yr5:     std dev of MC projections at t=60
  - p_below_10pct: P(price_ratio < 0.10 at t=60)
  - proj_t0/t12/t24/t36/t48/t60: full depreciation curve
  - fit_tier:      1 / 2 / 3
  - segment:       DATACENTER / WORKSTATION / CONSUMER / UNKNOWN
"""

import hashlib
import os
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, module="scipy")
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*overflow.*")
warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*invalid value.*")

from data_prep import load_data, DEMAND_SHOCK_RATIO, SUCCESSOR_DATES, load_datacenter_supplement, CARRIER_COST

KEEPA_MONTHLY_PATH = "outputs/keepa_monthly.csv"

MC_SAMPLES        = 10000
MIN_MONTHS_DATA   = 4          # absolute minimum observations to attempt any fit
HOLDOUT_MONTHS    = 6
VALIDATION_GPUS   = ["Tesla V100 PCIe 32 GB", "T4", "A10", "GeForce RTX 3090"]
TARGET_AGE        = 60         # months — 5-year projection target
OBS_WINDOW        = 12         # if data within ±12 mo of TARGET_AGE, use observed
CURVE_TIMES       = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120]

# Tier-1 thresholds
TIER1_MIN_MONTHS  = 18         # must have ≥ 18 monthly observations
TIER1_MAX_MIN_AGE = 30         # first observation must be before age 30

# Minimum uncertainty floor — backward scatter from a handful of stable-price
# data points underestimates 5-year forward uncertainty. A GPU trading stably
# at 50% MSRP for 12 months gets sigma=0.02 from std(), but the real forward
# uncertainty includes successor launches, demand shifts, and end-of-life.
# 0.10 = ±10 percentage points minimum, consistent with observed cross-GPU
# dispersion of ~15% within same-generation variants.
MIN_SIGMA_YR5 = 0.03

SEG_CANONICAL_MIN      = 12    # minimum pooled points for canonical segment fit
SEG_ANCHOR_MIN_MONTHS  = 18    # lowered from 24; T4 passes this but still fails dep>=6 after post_successor filter
APPRECIATING_THRESHOLD = 1.2   # current_ratio above this → GPU is appreciating (excluded from ranking)

# Fallback canonical k and floor used when the data-driven canonical is degenerate
# (R² < 0 or k hits upper bound — happens when training data is only mid-lifecycle,
# making the exp_floor model non-identifiable: can't separate k from floor).
# Values informed by GPU secondary market empirical norms (eBay sold data):
#   DATACENTER:  Fastest decay, lowest floor (K80 at 0.4-0.7%, V100 at 3-4% after 8-9yr)
#   WORKSTATION: High-MSRP cards depreciate heavily in % terms (Quadro M6000 at 1.9%,
#                K6000 at 1-2% after 11-13yr). Mid-tier ($800-900) closer to 10-15%.
#   CONSUMER:    Absolute $ floor of ~$25-50 means % floor depends on MSRP. GTX 980 Ti
#                at 8% after 11yr, GTX 1080 Ti at 20% after 9yr, still falling.
# All segments have a fallback to prevent silent GPU dropout when canonical fit fails.
SEG_K_FALLBACK = {
    "CONSUMER":    (0.020, 0.05),   # (k, floor) — GTX 980 Ti at 8% after 11yr; absolute $25-50 floor
    "UNKNOWN":     (0.020, 0.05),
    "DATACENTER":  (0.025, 0.02),   # K80 at 0.4-0.7%, V100 at 3-4% and falling
    "WORKSTATION": (0.018, 0.03),   # Quadro M6000 at 1.9%, K6000 at 1-2% after 11-13yr
}


# ── GPU segment assignments ────────────────────────────────────────────────────

GPU_SEGMENTS = {
    "DATACENTER": [
        "T4",
        "Tesla V100 SXM2 16 GB", "Tesla V100 SXM2 32 GB",
        "Tesla V100 PCIe 16 GB", "Tesla V100 PCIe 32 GB",
        "Tesla V100S PCIe 32 GB",
        "A100 SXM4 40 GB", "A100 SXM4 80 GB",
        "A100 PCIe 40 GB", "A100 PCIe 80 GB", "A100X",
        "A10", "A16 PCIe", "A30 PCIe", "A40",
        "L4", "L40", "L40S",
        "H100 SXM5 64 GB", "H100 SXM5 80 GB", "H100 SXM5 94 GB",
        "H100 PCIe 80 GB", "H100 PCIe 94 GB",
        "NVIDIA GH200", "H200 SXM", "H200 NVL",
        "AMD Instinct MI300X", "Radeon Instinct MI210", "Gaudi2 HL-225H",
    ],
    "WORKSTATION": [
        "Quadro P5000", "Quadro RTX 4000", "Quadro RTX 5000", "Quadro RTX 6000",
        "RTX A2000", "RTX A4000", "RTX A4500", "RTX A5000", "RTX A6000",
        "RTX 6000 Ada Generation", "RTX 4000 Ada Generation",
    ],
    "CONSUMER": [
        "GeForce RTX 3060", "GeForce RTX 3060 Ti",
        "GeForce RTX 3070", "GeForce RTX 3070 Ti",
        "GeForce RTX 3080", "GeForce RTX 3080 Ti",
        "GeForce RTX 3090", "GeForce RTX 3090 Ti",
        "GeForce RTX 4060", "GeForce RTX 4060 Ti 8 GB", "GeForce RTX 4060 Ti 16 GB",
        "GeForce RTX 4070", "GeForce RTX 4070 Ti",
        "GeForce RTX 4070 SUPER", "GeForce RTX 4070 Ti SUPER",
        "GeForce RTX 4080", "GeForce RTX 4080 SUPER",
        "GeForce RTX 4090", "GeForce RTX 4090 D",
    ],
}

_SEG_LOOKUP = {gpu: seg for seg, gpus in GPU_SEGMENTS.items() for gpu in gpus}

def gpu_segment(gpu_name):
    return _SEG_LOOKUP.get(gpu_name, "UNKNOWN")


# ── Model definitions ──────────────────────────────────────────────────────────

def exp_floor(t, floor, k):
    """P(t) = floor + (1-floor)*exp(-k*t)"""
    return floor + (1 - floor) * np.exp(-k * t)


def power_floor(t, floor, b):
    """P(t) = floor + (1-floor)*(t+1)^(-b)

    Reparameterised to enforce P(0) = 1.0 exactly (GPU launches at MSRP).
    The original form floor + a*(t+1)^(-b) left a free, allowing unphysical
    launch values (e.g. floor=0.95, a=5 → P(0)=5.95×MSRP). Replacing a with
    the identity a ≡ (1-floor) removes that degree of freedom and eliminates
    the t=0 constraint violation.
    """
    return floor + (1 - floor) * np.power(t + 1, -b)


# ── Half-life helpers ─────────────────────────────────────────────────────────

def _half_life_exp(floor, k):
    """Months until exp_floor curve crosses price_ratio = 0.5.

    P(t) = floor + (1-floor)*exp(-k*t) = 0.5
    → t = -ln((0.5 - floor) / (1 - floor)) / k

    The naive formula ln(2)/k ignores the floor and is only correct when
    floor = 0.  With a non-zero floor the half-life is always longer, and
    if floor >= 0.5 the curve never reaches 50% MSRP at all.
    """
    if floor >= 0.5 or k <= 0:
        return np.nan
    return -np.log((0.5 - floor) / (1.0 - floor)) / k


def _half_life_from_curve(curve):
    """Months until the projected curve dict crosses price_ratio = 0.5.

    Linearly interpolates between the two CURVE_TIMES entries that straddle
    0.5.  Returns NaN if the curve never crosses 0.5.
    """
    cts = sorted(ct for ct in CURVE_TIMES if not np.isnan(curve.get(ct, np.nan)))
    for j in range(1, len(cts)):
        v_prev, v_cur = curve[cts[j - 1]], curve[cts[j]]
        if v_prev >= 0.5 and v_cur < 0.5:
            hl = float(cts[j - 1] + (cts[j] - cts[j - 1]) * (v_prev - 0.5) / (v_prev - v_cur))
            # half_life at or near t=0 is a boundary artifact (proj_t0 ≈ 0.5),
            # not a real depreciation signal. Treat as NaN.
            return hl if hl > 1.0 else float(np.nan)
    return float(np.nan)


def _half_life_power(floor, b):
    """Months until power_floor curve crosses price_ratio = 0.5.

    With the reparameterised form P(t) = floor + (1-floor)*(t+1)^(-b):
        floor + (1-floor)*(t+1)^(-b) = 0.5
        → (t+1)^(-b) = (0.5 - floor) / (1 - floor)
        → t = ((0.5 - floor) / (1 - floor))^(-1/b) - 1

    Since a ≡ (1-floor) and P(0) = 1.0 > 0.5 whenever floor < 1.0, the curve
    always starts above 0.5 when floor < 0.5, so no guard for floor+a≤0.5 is needed.
    """
    if floor >= 0.5 or b <= 0:
        return np.nan
    ratio = (0.5 - floor) / (1.0 - floor)
    return ratio ** (-1.0 / b) - 1.0


# bounds stored as (lower_bounds_tuple, upper_bounds_tuple)
MODELS = {
    # k bounds tightened from [1e-4, 1.0] to [0.005, 0.25]:
    #   k=0.005 → half-life ≈ 138 months (~11 yrs, essentially flat)
    #   k=0.25  → half-life ≈ 2.8 months (very aggressive, fastest plausible GPU drop)
    #   The original upper bound of 1.0 allowed sub-1-month half-lives which is
    #   unphysical for any GPU market; the lower bound of 1e-4 allowed 579-yr half-lives.
    "exp_floor":   (exp_floor,   [0.20, 0.02],  ((0.001, 0.005), (0.80, 0.25))),
    # power_floor now has 2 params (floor, b) after reparameterisation.
    # b bounds [0.01, 3.0]: b=0.01 is nearly flat; b=3.0 is very steep.
    "power_floor": (power_floor, [0.20, 0.30],  ((0.001, 0.01),  (0.80, 3.0))),
}


# ── AICc ──────────────────────────────────────────────────────────────────────

def aicc(ss_res, n, k):
    """AICc for WLS with known heteroskedastic weights.

    sigma_i = max(y_i, 0.05) are treated as known observation weights
    (absolute_sigma=False in curve_fit: scipy infers the noise scale from
    residuals). Under this error model the negative log-likelihood is
    proportional to SS_res_w = Σ(residual_i/sigma_i)², and sigma² is NOT
    a separately estimated free parameter — so k_eff = k (curve params only),
    not k+1.

    The sigma_i terms (Σ log(2πσ_i²)) are constant across models sharing
    the same data and drop out of AIC differences, so they are omitted.

    Correct formula for this error model:
        AICc = SS_res_w + 2*k + 2*k*(k+1)/(n-k-1)
    """
    k_eff = k                         # sigma_i are known weights, not estimated
    if n - k_eff - 1 <= 0:
        return np.inf
    aic = ss_res + 2 * k_eff
    return aic + 2 * k_eff * (k_eff + 1) / (n - k_eff - 1)


# ── Fit one model to one GPU ───────────────────────────────────────────────────

def fit_model(t, y, name):
    fn, p0, bounds = MODELS[name]
    lo = list(bounds[0])
    hi = list(bounds[1])

    p0 = list(p0)
    p0[0] = float(np.clip(np.min(y) * 0.9, lo[0] + 1e-6, hi[0] - 1e-6))

    try:
        # Proportional (relative) error weighting: sigma_i = max(y_i, 0.05).
        # Price data is multiplicative — a 10% error on a $100 GPU is equivalent
        # to a 10% error on a $1000 GPU, but linear least squares would
        # weight the expensive GPU 100× more. sigma=y makes errors scale with
        # price level, producing approximately homoskedastic weighted residuals.
        # This makes fitting, R², and AICc all consistent in the same
        # proportional-error space, resolving the optimization–selection mismatch.
        # Floor of 0.05 prevents extreme leverage from very-low price_ratio
        # observations (data_prep filters price_ratio > 0.03, so observations near
        # that floor would otherwise receive ~1000× the weight of near-MSRP points).
        sigma = np.maximum(y, 0.05)
        # absolute_sigma=False: sigma values are proportional weights, not
        # calibrated measurement SDs. scipy infers the actual noise scale from
        # the residuals and scales pcov accordingly — giving correct parameter
        # uncertainty for downstream Monte Carlo propagation.
        popt, pcov = curve_fit(fn, t, y, p0=p0,
                               bounds=(lo, hi), maxfev=12000,
                               sigma=sigma, absolute_sigma=False)
        y_pred   = fn(t, *popt)
        resid_w  = (y - y_pred) / sigma
        ss_res_w = float(np.sum(resid_w ** 2))
        # Weighted SS_tot must use the weighted mean, not the unweighted mean.
        # Using np.mean(y) in a weighted context gives SS_tot that is not the
        # baseline for the weighted model, which can make R² exceed [0, 1].
        y_mean_w = float(np.average(y, weights=1.0 / sigma ** 2))
        ss_tot_w = float(np.sum(((y - y_mean_w) / sigma) ** 2))
        r2       = 1 - ss_res_w / ss_tot_w if ss_tot_w > 0 else 0
        n, k     = len(t), len(popt)
        # Serial-correlation correction: curve_fit assumes IID residuals,
        # but monthly GPU prices are autocorrelated (AR(1) ρ ≈ 0.3–0.7).
        # Inflate pcov by the Bartlett factor (1+ρ)/(1−ρ) to approximate
        # the effective-sample-size reduction. This widens MC CIs to better
        # reflect true predictive uncertainty.
        if n >= 4:
            rho = float(np.corrcoef(resid_w[:-1], resid_w[1:])[0, 1])
            if np.isfinite(rho):
                rho = float(np.clip(rho, -0.95, 0.95))  # prevent blow-up
                if rho > 0:
                    inflation = (1 + rho) / (1 - rho)
                    pcov = pcov * inflation
        # Detect if any parameter is pinned at its bound — indicates
        # non-identifiability, producing meaningless degenerate fits.
        tol = 1e-4
        bounds_hit = any(
            abs(popt[i] - lo[i]) < tol * (hi[i] - lo[i])
            or abs(popt[i] - hi[i]) < tol * (hi[i] - lo[i])
            for i in range(len(popt))
        )
        return {"params": popt, "cov": pcov,
                "r2": r2, "aicc": aicc(ss_res_w, n, k),
                "ss_res": ss_res_w, "n": n, "bounds_hit": bounds_hit}
    except (RuntimeError, ValueError, np.linalg.LinAlgError):
        return None


# ── Segment canonical fit ──────────────────────────────────────────────────────

def _synthetic_fit(k, floor, n):
    """
    Build a fake fit-result dict for a known (k, floor) prior.
    Covariance is inflated (50% relative uncertainty per param) to reflect
    that this is a prior, not a fitted value. Raised from 30% — the real
    cross-GPU k dispersion across datacenter GPUs is 50-60%.

    A weak negative floor–k cross-correlation (ρ ≈ -0.30) is included because
    in exp_floor a higher k requires a lower floor to reproduce the same observed
    data. Ignoring this (diagonal cov) would overstate MC uncertainty by treating
    floor and k as independent when they structurally are not.
    """
    params = np.array([floor, k])
    fl_std = 0.30 * floor
    k_std  = 0.30 * k
    corr   = -0.30   # conservative empirical floor–k correlation for exp_floor
    cov = np.array([[fl_std ** 2,              corr * fl_std * k_std],
                    [corr * fl_std * k_std,    k_std ** 2           ]])
    return {"params": params, "cov": cov, "r2": np.nan,
            "aicc": np.inf, "ss_res": np.nan, "n": n}


def fit_segment_canonical(monthly, segment_name):
    """
    Pool well-observed GPUs from segment (≥24 months, min_age < 30) and fit
    exp_floor to get a shared canonical decay rate k.

    Only observations with price_ratio ≤ 1.0 are used: we want to measure the
    DEPRECIATION rate, not demand-shock appreciation. Above-MSRP data distorts k
    toward zero (flat) when it is mixed with normal depreciation observations.

    Returns (fit_result_dict, list_of_anchor_gpus).
    """
    seg_gpus = set(GPU_SEGMENTS.get(segment_name, []))
    pooled_t, pooled_y, anchors = [], [], []

    for gpu, grp in monthly.groupby("gpu_name"):
        if gpu not in seg_gpus:
            continue
        grp = grp.sort_values("age_months").dropna()
        if len(grp) < SEG_ANCHOR_MIN_MONTHS or grp["age_months"].min() > TIER1_MAX_MIN_AGE:
            continue
        # Only depreciating observations (below MSRP) for canonical decay rate.
        # Also exclude post-successor observations to prevent discrete announcement
        # step-changes from inflating the segment canonical k.
        dep = grp[grp["price_ratio"] <= 1.0]
        if "post_successor" in grp.columns:
            dep = dep[~dep["post_successor"]]
        if len(dep) < 6:
            continue
        pooled_t.extend(dep["age_months"].values)
        pooled_y.extend(dep["price_ratio"].values)
        anchors.append(gpu)

    if len(pooled_t) < SEG_CANONICAL_MIN:
        # Try fallback
        fallback = SEG_K_FALLBACK.get(segment_name)
        if fallback is not None:
            k_fb, fl_fb = fallback
            result = _synthetic_fit(k_fb, fl_fb, len(pooled_t) or SEG_CANONICAL_MIN)
            return result, anchors
        return None, anchors

    t = np.array(pooled_t)
    # Filter extreme outliers (bad data) before canonical fit
    y_raw = np.array(pooled_y)
    mask  = (y_raw >= 0.05) & (y_raw <= 1.0)
    t, y  = t[mask], y_raw[mask]
    if len(t) < SEG_CANONICAL_MIN:
        fallback = SEG_K_FALLBACK.get(segment_name)
        if fallback is not None:
            k_fb, fl_fb = fallback
            return _synthetic_fit(k_fb, fl_fb, len(t)), anchors
        return None, anchors

    result = fit_model(t, y, "exp_floor")

    # Degenerate-fit detection: k pinned near upper bound (≥ 0.24), negative R²,
    # or floor hitting its lower bound (≤ 0.02 = boundary artifact).
    def _is_degenerate(res, strict=False):
        if res is None:
            return True
        k_fit = res["params"][1]
        fl_fit = res["params"][0]
        r2 = res["r2"]
        # Basic checks: k at boundary, negative R², floor at boundary
        if k_fit >= 0.24 or r2 < 0 or fl_fit <= 0.04:
            return True
        # Strict mode (for all-data retry): also require R² >= 0.20
        # to avoid accepting a poor fit just because floor/k are in-bounds
        if strict and r2 < 0.20:
            return True
        return False

    if _is_degenerate(result):
        # ── Retry with ALL data (including post-successor) ──────────────
        # The pre-successor-only fit failed because the plateau-then-cliff
        # pattern makes floor/k unidentifiable. Including post-successor
        # data gives a wider age range and anchors the floor better.
        # The announcement step-change slightly inflates k, but a data-
        # derived k with that bias is better than a handcrafted fallback.
        pooled_all_t, pooled_all_y = [], []
        for gpu, grp in monthly.groupby("gpu_name"):
            if gpu not in seg_gpus:
                continue
            grp = grp.sort_values("age_months").dropna()
            if len(grp) < SEG_ANCHOR_MIN_MONTHS or grp["age_months"].min() > TIER1_MAX_MIN_AGE:
                continue
            dep_all = grp[grp["price_ratio"] <= 1.0]  # no post_successor filter
            if len(dep_all) < 6:
                continue
            pooled_all_t.extend(dep_all["age_months"].values)
            pooled_all_y.extend(dep_all["price_ratio"].values)

        if len(pooled_all_t) >= SEG_CANONICAL_MIN:
            t_all = np.array(pooled_all_t)
            y_all_raw = np.array(pooled_all_y)
            mask_all = (y_all_raw >= 0.05) & (y_all_raw <= 1.0)
            t_all, y_all = t_all[mask_all], y_all_raw[mask_all]
            if len(t_all) >= SEG_CANONICAL_MIN:
                result_all = fit_model(t_all, y_all, "exp_floor")
                if not _is_degenerate(result_all, strict=True):
                    k_old = result["params"][1] if result else float("nan")
                    r2_old = result["r2"] if result else float("nan")
                    print(f"  [{segment_name}] canonical k={k_old:.4f} R²={r2_old:.3f} "
                          f"→ degenerate (floor≤0.02), retried with all data")
                    return result_all, anchors

        # ── Final fallback: handcrafted SEG_K_FALLBACK ──────────────────
        k_old = result["params"][1] if result else float("nan")
        r2_old = result["r2"] if result else float("nan")
        fallback = SEG_K_FALLBACK.get(segment_name)
        if fallback is not None:
            k_fb, fl_fb = fallback
            print(f"  [{segment_name}] canonical k={k_old:.4f} R²={r2_old:.3f} "
                  f"→ degenerate, using fallback k={k_fb}")
            return _synthetic_fit(k_fb, fl_fb, len(t)), anchors

    return result, anchors


# ── Segment empirical floor prior ─────────────────────────────────────────────

def _segment_floor_prior(monthly, segment_name):
    """
    Compute an empirical Bayes floor prior from GPUs in the segment that have
    data near t=60 (age max ≥ 60 months). Their long-run median price_ratio
    is a direct estimate of the floor parameter.

    The floor is the most cross-GPU-correlated parameter in the model: all
    datacenter GPUs converge to some fraction of MSRP reflecting enterprise
    residual / scrap value. Data-rich peers inform the prior for sparse GPUs.

    Returns (floor_mean, floor_std) or None if < 2 anchor GPUs available.
    """
    seg_gpus = set(GPU_SEGMENTS.get(segment_name, []))
    floor_estimates = []

    for gpu, grp in monthly.groupby("gpu_name"):
        if gpu not in seg_gpus:
            continue
        grp = grp.sort_values("age_months").dropna()
        if grp["age_months"].max() < 72:  # raised from 48→60→72 to exclude mid-lifecycle GPUs
            continue
        # Use the median of observations in the final 12-month window as the
        # floor estimate. 12-month window reduces noise from thin markets.
        recent = grp[grp["age_months"] >= grp["age_months"].max() - 12]
        if len(recent) < 2:
            continue
        floor_est = float(recent["price_ratio"].median())
        # Accept only plausible floor values — exclude GPUs still appreciating
        # (floor_est > 1.0) or with suspect near-zero values (< 0.05)
        if 0.05 <= floor_est <= 0.95:
            floor_estimates.append(floor_est)

    if len(floor_estimates) < 2:
        return None

    return (float(np.mean(floor_estimates)),
            max(float(np.std(floor_estimates, ddof=1)), 0.05))  # sample std, min 0.05


# ── Constrained floor fit (k fixed from segment) ──────────────────────────────

def fit_constrained_floor(t, y, k_fixed, floor_prior=None, n_data_months=None):
    """
    Fit exp_floor with k fixed at k_fixed. Floor is the only free parameter.
    Returns (floor_opt, floor_var) or (None, None).

    floor_prior: optional (mean, std) from _segment_floor_prior().
    When provided, adds a Bayesian regularisation term that shrinks the floor
    estimate toward the segment empirical mean. The strength of regularisation
    scales with the inverse of observed data — GPUs with no depreciation visible
    (e.g. H100 at age 17–35 months) are almost entirely driven by the prior;
    GPUs with 36+ months of post-MSRP data are almost entirely data-driven.

    This converts H100-class TVR estimates from "0.95 (segment bound)" to
    "~0.35 (inferred from segment peer distribution)" — a meaningful projection
    rather than an uninformative boundary hit.
    """
    from scipy.optimize import minimize as _minimize

    def model_fixed_k(t_arr, floor):
        return floor + (1 - floor) * np.exp(-k_fixed * t_arr)

    # ── Bayesian path (prior available) ───────────────────────────────────────
    if floor_prior is not None:
        prior_mean, prior_std = floor_prior
        prior_var = prior_std ** 2

        # Regularisation weight: 1 observation → full prior; scales down as data
        # accumulates. n_data_months proxy: segment default TIER1_MIN_MONTHS=18.
        n_eff = max(1, n_data_months or len(t))
        lambda_reg = max(0.0, 1.0 - n_eff / 36.0)   # 0 at 36+ months, 1 at 0 months

        def penalised_wls(params):
            fl = float(np.clip(params[0], 0.001, 0.80))
            pred   = model_fixed_k(t, fl)
            sigma  = np.maximum(y, 0.05)
            wls    = float(np.sum(((y - pred) / sigma) ** 2))
            penalty = lambda_reg * ((fl - prior_mean) ** 2) / prior_var
            return wls + penalty

        try:
            res = _minimize(penalised_wls, [prior_mean],
                            method="L-BFGS-B", bounds=[(0.01, 0.95)])
            if res.success:
                floor_opt = float(np.clip(res.x[0], 0.001, 0.80))
                # Posterior variance: blend likelihood and prior precisions.
                # Typical proportional residual variance ≈ mean(sigma)².
                sigma_bar  = float(np.mean(np.maximum(y, 0.05)))
                like_prec  = len(t) / max(sigma_bar ** 2, 1e-4)
                prior_prec = 1.0 / prior_var
                # Scale prior precision by lambda_reg to match the penalised objective:
                # when lambda_reg < 1, less prior info was actually used, so posterior
                # variance should be wider than the full-prior case.
                post_var   = 1.0 / (like_prec + lambda_reg * prior_prec)
                return floor_opt, post_var
        except (RuntimeError, ValueError, np.linalg.LinAlgError):
            pass  # fall through to original path

    # ── Original path (no prior or optimisation failed) ───────────────────────
    p0_floor = float(np.clip(np.min(y) * 0.9, 0.001, 0.80))
    try:
        # Proportional weighting (consistent with fit_model): price_ratio data is
        # multiplicative, so errors should scale with price level. Without sigma,
        # sparse low-ratio observations get the same weight as dense mid-ratio
        # observations, biasing the floor estimate upward.
        sigma = np.maximum(y, 0.05)
        popt, pcov = curve_fit(model_fixed_k, t, y,
                               p0=[p0_floor], bounds=([0.01], [0.95]),
                               sigma=sigma, absolute_sigma=False,
                               maxfev=5000)
        floor_var = float(pcov[0, 0])
        if not np.isfinite(floor_var):
            floor_var = None  # signal that covariance is unreliable
        # Bartlett serial-correlation correction (mirrors fit_model):
        # curve_fit assumes IID residuals, but monthly prices are AR(1).
        # Inflate floor_var by (1+ρ)/(1−ρ) so Tier 2 uncertainty is
        # consistent with the Bartlett-corrected k_var from the canonical.
        if floor_var is not None and len(t) >= 4:
            resid_w = (y - model_fixed_k(t, popt[0])) / sigma
            rho = float(np.corrcoef(resid_w[:-1], resid_w[1:])[0, 1])
            if np.isfinite(rho):
                rho = float(np.clip(rho, -0.95, 0.95))
                if rho > 0:
                    floor_var *= (1 + rho) / (1 - rho)
        return float(popt[0]), floor_var
    except (RuntimeError, ValueError, np.linalg.LinAlgError):
        return None, None


# ── MC helpers ─────────────────────────────────────────────────────────────────

def _mc_from_ensemble(fits, t_values, rng, mc_samples=MC_SAMPLES):
    """
    Monte Carlo from AICc-weighted ensemble over a list of t values.
    Returns (mc_array[mc_samples, len(t_values)], weight_dict) or (None, None).
    """
    valid = {k: v for k, v in fits.items() if v is not None}
    if not valid:
        return None, None

    # Drop models that explain < 20% of variance before computing Akaike weights.
    # If both models are poor fits (R² < 0.20), ensembling them averages two wrong
    # answers without reducing systematic error. Better to let the caller fall
    # through to Tier 2 (this returns None, None which triggers the fallback).
    valid = {k: v for k, v in valid.items()
             if not np.isnan(v.get("r2", np.nan)) and v.get("r2", 0) >= 0.20}
    if not valid:
        return None, None

    model_names = list(valid.keys())
    aicc_vals   = np.array([valid[m]["aicc"] for m in model_names])
    # Guard: if the minimum AICc is inf (e.g. n - k - 1 <= 0 for all models),
    # delta = inf - inf = nan and weights become all-nan. Fall back to ss_res
    # or return None if all models are degenerate.
    # When only some models have inf AICc, the finite ones naturally dominate
    # (delta = inf → weight ≈ 0), so no special handling is needed.
    if not np.isfinite(aicc_vals.min()):
        aicc_vals = np.array([valid[m].get("ss_res", np.inf) for m in model_names])
        if not np.isfinite(aicc_vals.min()):
            return None, None
    delta       = aicc_vals - aicc_vals.min()
    weights     = np.exp(-0.5 * delta)
    weights    /= weights.sum()

    # Pre-extract per-model data outside the MC loop for speed
    model_meta = []
    for mname, w in zip(model_names, weights):
        fn, _, (lo, hi) = MODELS[mname]
        model_meta.append((fn, valid[mname]["params"], valid[mname]["cov"],
                           list(lo), list(hi), float(w)))

    t_arr  = np.array(t_values, dtype=float)
    mc_out = np.zeros((mc_samples, len(t_arr)))

    for s in range(mc_samples):
        proj = np.zeros(len(t_arr))
        for fn, params, cov, lo, hi, w in model_meta:
            try:
                trace_abs = max(1e-10, 1e-6 * abs(np.trace(cov)))
                cov_reg = cov + np.eye(len(params)) * trace_abs
                if not np.all(np.isfinite(cov_reg)) or np.linalg.cond(cov_reg) > 1e10:
                    sp = params
                else:
                    sp = np.clip(rng.multivariate_normal(params, cov_reg), lo, hi)
            except (np.linalg.LinAlgError, ValueError, RuntimeError):
                sp = params
            proj += w * np.clip(fn(t_arr, *sp), 0.0, 3.0)
        mc_out[s] = proj

    return np.clip(mc_out, 0.0, 3.0), dict(zip(model_names, weights))


def _mc_from_constrained(floor_opt, floor_var, k_opt, k_var, t_values, rng,
                          mc_samples=MC_SAMPLES, k_floor_cov=None):
    """
    MC for tier-2 constrained fit. Samples [floor, k] jointly using a bivariate
    normal with cross-covariance derived from the segment canonical fit.

    floor and k are structurally negatively correlated in exp_floor (higher k
    requires lower floor to reproduce the same observed data). k_floor_cov carries
    this cross-covariance so we avoid the independent-sampling bias that inflated
    sigma_yr5 and p_below_10pct in the previous version.

    If k_floor_cov is None (e.g. canonical cov is unavailable), falls back to
    independent sampling — same behaviour as before.
    """
    t_arr  = np.array(t_values, dtype=float)
    mc_out = np.zeros((mc_samples, len(t_arr)))

    k_std  = float(np.sqrt(abs(k_var)))     if k_var    is not None else 0.0
    # When floor_var is None (unreliable covariance), use 30% relative uncertainty
    # instead of 0.0 — pinning floor at the point estimate with zero spread produces
    # artificially narrow CIs for the least reliable fits.
    fl_std = float(np.sqrt(abs(floor_var))) if floor_var is not None else 0.30 * max(floor_opt, 0.05)

    use_joint = (k_floor_cov is not None and (k_std > 0 or fl_std > 0))

    if use_joint:
        cov_2x2 = np.array([[fl_std ** 2, k_floor_cov],
                             [k_floor_cov, k_std ** 2]])
        # Regularise to guarantee PSD (numerical noise can make eigenvalues ≤ 0)
        cov_2x2 += np.eye(2) * max(1e-12, 1e-6 * np.trace(cov_2x2))
        try:
            samples = rng.multivariate_normal([floor_opt, k_opt], cov_2x2,
                                              size=mc_samples)
            fl_samples = np.clip(samples[:, 0], 0.001, 0.80)
            k_samples  = np.clip(samples[:, 1], 0.005, 0.25)
            for s in range(mc_samples):
                fl_s, k_s = fl_samples[s], k_samples[s]
                mc_out[s] = np.clip(fl_s + (1 - fl_s) * np.exp(-k_s * t_arr), 0.0, 3.0)
            return mc_out
        except (np.linalg.LinAlgError, ValueError, RuntimeError):
            pass  # fall through to independent sampling if MVN fails

    # Fallback: independent sampling (conservative — overstates uncertainty)
    for s in range(mc_samples):
        k_s  = float(np.clip(rng.normal(k_opt,    k_std),  0.005, 0.25)) if k_std  > 0 else k_opt
        fl_s = float(np.clip(rng.normal(floor_opt, fl_std), 0.001, 0.80)) if fl_std > 0 else floor_opt
        mc_out[s] = np.clip(fl_s + (1 - fl_s) * np.exp(-k_s * t_arr), 0.0, 3.0)

    return mc_out


def _hpd_interval(samples, credible_mass=0.95):
    """Highest Posterior Density interval — the shortest interval containing
    `credible_mass` fraction of the samples.  Unlike the equal-tailed interval
    (ETI), HPD is centered on the highest-density region, so the point estimate
    (mode/median) sits near the middle of the band rather than being pulled to
    one edge by distribution skewness.

    Algorithm: sort samples, slide a window of size ceil(credible_mass * n),
    pick the window with the smallest width (max − min).
    """
    sorted_s = np.sort(samples)
    n = len(sorted_s)
    interval_size = int(np.ceil(credible_mass * n))
    if interval_size >= n:
        return float(sorted_s[0]), float(sorted_s[-1])
    widths = sorted_s[interval_size:] - sorted_s[:n - interval_size]
    best = int(np.argmin(widths))
    return float(sorted_s[best]), float(sorted_s[best + interval_size])


def _mc_to_stats(mc_out, target_idx):
    """
    Summarise MC array (mc_samples × len(CURVE_TIMES)) at target column index.
    Returns dict with point, ci_lo, ci_hi, sigma_yr5, p_below_10, curve,
    plus per-time-point CIs (ci_lo_curve, ci_hi_curve, sigma_curve).

    CI uses the Highest Posterior Density (HPD) interval — the shortest interval
    containing 95% of MC samples.  For skewed posteriors (common with exp_floor
    due to floor/k parameter bound asymmetry), HPD keeps the point estimate
    near the centre of the band, unlike the equal-tailed interval (ETI) which
    pushes the median toward one edge.  This follows Bank of England fan chart
    methodology (mode-centred, density-based bands).

    sigma_yr5 is the sample std dev; it is NOT a CI half-width since the MC
    posterior predictive distribution can be asymmetric near parameter bounds.

    Curve values are marginal medians at each time point, then monotonicity is
    enforced: a GPU's price_ratio must be non-increasing across time. Without this
    guard, marginal medians from a bimodal MC posterior (some samples fast-decaying,
    some slow) can produce a non-monotone curve.
    """
    col        = mc_out[:, target_idx]
    curve_raw  = {ct: float(np.median(mc_out[:, i])) for i, ct in enumerate(CURVE_TIMES)}
    # Per-time-point HPD CI and sigma from the full MC array
    ci_lo_curve = {}
    ci_hi_curve = {}
    sigma_curve = {}
    for i, ct in enumerate(CURVE_TIMES):
        lo, hi = _hpd_interval(mc_out[:, i])
        ci_lo_curve[ct] = lo
        ci_hi_curve[ct] = hi
        sigma_curve[ct] = float(np.std(mc_out[:, i]))
    # Enforce monotonicity: prices cannot rise over time in the depreciation model
    curve = {}
    prev = curve_raw[CURVE_TIMES[0]]  # start from the actual t=0 value, not 1.0
    for ct in CURVE_TIMES:
        v = min(curve_raw[ct], prev)
        curve[ct] = v
        prev = v
    # Ensure proj_t{TARGET_AGE} == point (median MC at the target horizon).
    # The monotonicity clamp can lower curve[TARGET_AGE] below the median when
    # marginal medians are non-monotone (e.g. bimodal Tier-1 ensemble where
    # the median at t=48 exceeds that at t=60). proj_yr5_ratio and proj_t60
    # must agree in the output CSV.
    curve[CURVE_TIMES[target_idx]] = float(np.median(col))
    # Re-enforce monotonicity after the overwrite: walk backwards from
    # target_idx to clamp any earlier value that is now below the target.
    for i in range(target_idx, 0, -1):
        if curve[CURVE_TIMES[i - 1]] < curve[CURVE_TIMES[i]]:
            curve[CURVE_TIMES[i - 1]] = curve[CURVE_TIMES[i]]
    hpd_lo, hpd_hi = _hpd_interval(col)
    # P(<10%) at extended horizons (8yr, 10yr) from MC samples
    p_below_10_by_t = {}
    for i, ct in enumerate(CURVE_TIMES):
        p_below_10_by_t[ct] = float(np.mean(mc_out[:, i] < 0.10))
    return {
        "point":      float(np.median(col)),
        "ci_lo":      hpd_lo,
        "ci_hi":      hpd_hi,
        "sigma_yr5":  max(float(np.std(col)), MIN_SIGMA_YR5),
        "p_below_10": float(np.mean(col < 0.10)),
        "p_below_10_by_t": p_below_10_by_t,
        "curve":      curve,
        "ci_lo_curve": ci_lo_curve,
        "ci_hi_curve": ci_hi_curve,
        "sigma_curve": sigma_curve,
    }


def _normalize_curve_to_launch(stats):
    """
    Force proj_t0 = 1.0 (GPUs launch at MSRP) and re-derive intermediate
    curve points using exp_floor interpolation from (0, 1.0) to (60, TVR).
    This fixes the nonsensical back-extrapolation that produces proj_t0 of
    200-300% for GPUs with late-lifecycle-only data.
    """
    curve = stats["curve"]
    ci_lo_curve = stats["ci_lo_curve"]
    ci_hi_curve = stats["ci_hi_curve"]
    sigma_curve = stats["sigma_curve"]
    tvr = curve.get(60, curve[max(curve.keys())])

    # Set t=0 to launch value
    # Sigma starts at 10% of the yr5 sigma (not zero) so the band ramps
    # gently from launch instead of having a sharp 0→nonzero kink at t=12.
    curve[0] = 1.0
    s0 = stats["sigma_yr5"] * 0.10  # small seed sigma at launch
    ci_lo_curve[0] = max(1.0 - 2 * s0, 0.0)
    ci_hi_curve[0] = 1.0 + 2 * s0
    sigma_curve[0] = s0

    # Re-derive intermediate points from (0, 1.0) to (60, TVR)
    if tvr >= 0.95:
        # Near-MSRP or appreciating GPU: linear interpolation from 1.0 to TVR.
        # exp_floor produces near-flat or non-monotonic curves when TVR is close
        # to 1.0 (floor ≈ 0.475, k ≈ 0.001 → indistinguishable from linear).
        # Use linear for TVR ≥ 0.95 to avoid monotonicity violations.
        for t in [12, 24, 36, 48]:
            frac = t / 60.0
            curve[t] = 1.0 + frac * (tvr - 1.0)  # linear from 1.0 to TVR
    else:
        # Depreciating GPU: exp_floor interpolation from (0,1.0) to (60,TVR)
        floor = min(max(tvr * 0.5, 0.001), 0.80)
        exp_term = max((tvr - floor) / (1.0 - floor), 1e-10)
        k = max(-np.log(exp_term) / 60.0, 0.001)
        for t in [12, 24, 36, 48]:
            curve[t] = floor + (1.0 - floor) * np.exp(-k * t)

    # Scale CIs proportionally — narrower near launch, wider at t=60
    for t in [12, 24, 36, 48]:
        frac = t / 60.0
        ci_lo_curve[t] = max(curve[t] - frac * (tvr - stats["ci_lo"]), 0.0)
        ci_hi_curve[t] = curve[t] + frac * (stats["ci_hi"] - tvr)  # no hard cap — let CI follow the curve
        sigma_curve[t] = frac * stats["sigma_yr5"]

    # Enforce monotonicity on intermediate points (t=12..48) only.
    # t=0 is fixed at 1.0 and t=60 is the TVR — both are sacrosanct.
    # Clamp intermediates to stay between curve[0] and curve[60].
    lo_bound = min(curve[0], curve[60])
    hi_bound = max(curve[0], curve[60])
    for t in [12, 24, 36, 48]:
        curve[t] = max(lo_bound, min(hi_bound, curve[t]))

    stats["curve"] = curve
    stats["ci_lo_curve"] = ci_lo_curve
    stats["ci_hi_curve"] = ci_hi_curve
    stats["sigma_curve"] = sigma_curve
    return stats


# ── Ensemble projection (kept for validate_extrapolation) ──────────────────────

def ensemble_project(fits, t_project=TARGET_AGE, mc_samples=MC_SAMPLES):
    """AICc-weighted ensemble projection at a single t_project. Returns
    (point, ci_lo, ci_hi, weight_dict) or None."""
    rng = np.random.default_rng(42)
    mc_out, weights = _mc_from_ensemble(fits, [t_project], rng, mc_samples)
    if mc_out is None:
        return None
    col   = np.clip(mc_out[:, 0], 0.0, 3.0)
    hpd_lo, hpd_hi = _hpd_interval(col)
    return (float(np.median(col)), hpd_lo, hpd_hi, weights)


# ── Merge retail + Keepa monthly data ─────────────────────────────────────────

def build_extended_monthly(df, keepa_monthly=None):
    """
    Combine retail-CSV monthly medians (Jun 2024+) with Keepa historical
    monthly medians (pre-Jun 2024) into a single time series per GPU.
    Retail is the authoritative source for the overlap period.
    Returns DataFrame: gpu_name, month (Period M), price_ratio, age_months, source.
    """
    # ── Condition switch at 24 months ──────────────────────────────────────
    # Early lifecycle (age ≤ 24 mo): use NEW condition (launch-era pricing).
    # Late lifecycle (age > 24 mo): use REFURBISHED or USED (realistic resale
    # value). NEW-old-stock prices after 2 years reflect scarcity premiums,
    # not depreciation. Dropping them and using refurb/used gives a more
    # accurate picture of what an owner would actually receive on resale.
    CONDITION_SWITCH_AGE = 24  # months

    base = df[(~df["left_censored"]) &
              (df["age_months"] >= 0) &
              (df["price_ratio"] <= DEMAND_SHOCK_RATIO)].copy()

    # Early: NEW only (first 2 years)
    early = base[(base["condition"] == "NEW") &
                 (base["age_months"] <= CONDITION_SWITCH_AGE)]

    # Late: prefer REFURBISHED/USED; fall back to NEW for GPUs that
    # have NO refurb/used data after 24 months (6 current-gen datacenter GPUs).
    # Cap USED/REFURB at price_ratio <= 1.0 for old GPUs (age > 48mo).
    # A used GPU trading above MSRP after 4+ years is almost always
    # contamination (server bundles, mislabeled form factors like SXM4→PCIe).
    # Younger GPUs can legitimately trade above MSRP used (AI demand).
    # Age-dependent USED/REFURB price caps to filter server bundles and
    # mislabeled form factors (SXM4 sold as "PCIe", multi-GPU trays, etc.).
    # Real used GPUs depreciate; listings above these thresholds are contamination.
    USED_CAP_TIERS = [
        (48, 1.2),   # age 24-48mo: tightened from 1.5 to 1.2 — enterprise USED at 1.5x MSRP is OEM contamination
        (72, 0.75),  # age 48-72mo: cap at 75% MSRP (4-6yr old GPU above 75% is suspect)
        (999, 0.50), # age 72+mo: cap at 50% MSRP (6yr+ GPU above 50% is almost always contamination)
    ]
    late_refurb_parts = []
    prev_age = CONDITION_SWITCH_AGE
    for max_age, max_ratio in USED_CAP_TIERS:
        # USED-only: drop REFURBISHED to eliminate enterprise-channel OEM markup
        # contamination (server bundles, HPE/Dell modules at 2-3x bare-card MSRP).
        # REFURBISHED datacenter data is dominated by OEM-channel units, not
        # genuine refurbished bare cards. USED data is cleaner.
        part = base[(base["condition"] == "USED") &
                    (base["age_months"] > prev_age) &
                    (base["age_months"] <= max_age) &
                    (base["price_ratio"] <= max_ratio)]
        late_refurb_parts.append(part)
        prev_age = max_age
    late_refurb = pd.concat(late_refurb_parts, ignore_index=True)
    # Find GPUs with zero refurb/used after 24mo — allow NEW as fallback
    gpus_with_refurb = set(late_refurb["gpu_name"].unique())
    gpus_all = set(base[base["age_months"] > CONDITION_SWITCH_AGE]["gpu_name"].unique())
    gpus_need_fallback = gpus_all - gpus_with_refurb
    late_fallback_raw = base[(base["condition"] == "NEW") &
                             (base["age_months"] > CONDITION_SWITCH_AGE) &
                             (base["gpu_name"].isin(gpus_need_fallback))]
    # Require NEW fallback to have >= 3 distinct monthly periods per GPU.
    # A single stale Amazon listing repeated daily across months creates phantom
    # data that dominates the median (e.g., A100 PCIe 40GB at $8,829 NEW).
    if len(late_fallback_raw) > 0:
        fb_months = late_fallback_raw.groupby("gpu_name")["date"].apply(
            lambda x: x.dt.to_period("M").nunique())
        valid_fb_gpus = set(fb_months[fb_months >= 3].index)
        late_fallback = late_fallback_raw[late_fallback_raw["gpu_name"].isin(valid_fb_gpus)]
    else:
        late_fallback = late_fallback_raw
    late = pd.concat([late_refurb, late_fallback], ignore_index=True)

    sub = pd.concat([early, late], ignore_index=True)
    sub["month"] = sub["date"].dt.to_period("M")
    retail = (sub.groupby(["gpu_name", "month"])
                 .agg(price_ratio=("price_ratio", "median"),
                      age_months=("age_months", "median"))
                 .reset_index())
    retail["source"] = "retail"

    if keepa_monthly is None or len(keepa_monthly) == 0:
        retail["post_successor"] = False
        return retail

    k = keepa_monthly.copy()
    k["month"] = pd.PeriodIndex(k["month"], freq="M")
    # Keepa data is NEW condition (Amazon buy-box). Apply the same 24-month
    # cutoff: only use keepa data for the first 2 years of each GPU's life.
    # Supplement data may contain REFURBISHED/USED which is valid after 24 months.
    k = k[(k["price_ratio"] <= DEMAND_SHOCK_RATIO) &
          (k["age_months"] >= 0)]
    # Filter phantom Keepa listings: Amazon third-party "NEW" listings for
    # datacenter GPUs older than 72 months are inflated ask prices that rarely
    # transact (e.g., V100 16GB listed at $500-1000 on Amazon while eBay sold
    # price is $80-350). These poison the monthly median and inflate current_ratio.
    KEEPA_MAX_AGE = 72  # months — exclude Keepa NEW data for GPUs > 6yr old
    # Apply age cap only to Keepa-sourced rows, not supplement rows. Supplement
    # USED data at age 72+ is legitimate (eBay sold prices), not phantom listings.
    is_keepa = k["source"] == "keepa" if "source" in k.columns else pd.Series(True, index=k.index)
    k = k[~(is_keepa & (k["age_months"] > KEEPA_MAX_AGE))]
    if "condition" in k.columns:
        k["condition"] = k["condition"].fillna("NEW")
        # Same condition switch: NEW ≤ 24mo, REFURB/USED > 24mo
        # Allow NEW fallback for GPUs with no refurb/used (same 6 GPUs)
        k_new_early = k[(k["condition"] == "NEW") & (k["age_months"] <= CONDITION_SWITCH_AGE)]
        k_refurb_late = k[(k["condition"] == "USED") & (k["age_months"] > CONDITION_SWITCH_AGE)]
        k_gpus_with_refurb = set(k_refurb_late["gpu_name"].unique())
        k_new_fallback = k[(k["condition"] == "NEW") & (k["age_months"] > CONDITION_SWITCH_AGE) &
                           (~k["gpu_name"].isin(k_gpus_with_refurb)) &
                           (k["gpu_name"].isin(gpus_need_fallback))]
        k = pd.concat([k_new_early, k_refurb_late, k_new_fallback], ignore_index=True)
    else:
        # Pure keepa (no supplement) — all NEW. Allow beyond 24mo only for fallback GPUs.
        k_early = k[k["age_months"] <= CONDITION_SWITCH_AGE]
        k_late_fallback = k[(k["age_months"] > CONDITION_SWITCH_AGE) &
                            (k["gpu_name"].isin(gpus_need_fallback))]
        k = pd.concat([k_early, k_late_fallback], ignore_index=True)
    k = k[["gpu_name", "month", "price_ratio", "age_months", "source"]]

    combined = pd.concat([retail, k], ignore_index=True)
    # Retail is authoritative for any overlapping month: give it explicit priority
    # instead of relying on alphabetic ordering ('r' > 'k').
    # eBay sold data (actual transactions) > retail (Amazon ask prices) > supplement/keepa
    _priority = {"ebay_sold": 2, "retail": 1, "supplement": 0, "keepa": 0}
    combined["_src_priority"] = combined["source"].map(_priority).fillna(0)
    combined = (combined
                .sort_values("_src_priority", ascending=False)
                .drop_duplicates(subset=["gpu_name", "month"])
                .drop(columns="_src_priority")
                .sort_values(["gpu_name", "age_months"])
                .reset_index(drop=True))

    # ── Post-successor flag ───────────────────────────────────────────────────
    # Tag monthly observations that fall after the GPU's successor was announced.
    # Used in fit_all_gpus() to isolate pre-announcement data for k estimation.
    succ_dates = pd.Series({
        gpu: pd.to_datetime(date) for gpu, date in SUCCESSOR_DATES.items()
    }).rename_axis("gpu_name").reset_index()
    succ_dates.columns = ["gpu_name", "successor_date"]
    combined = combined.merge(succ_dates, on="gpu_name", how="left")
    combined["month_ts"] = combined["month"].dt.to_timestamp()
    combined["post_successor"] = (
        combined["successor_date"].notna() &
        (combined["month_ts"] >= combined["successor_date"])
    )
    combined = combined.drop(columns=["successor_date", "month_ts"])

    return combined


# ── Three-tier hierarchical fitting ───────────────────────────────────────────

def fit_all_gpus(df, keepa_monthly=None):
    """
    Produce depreciation projections for every GPU in the tier-3 datasets.

    Tier 1 (INDIVIDUAL): ≥TIER1_MIN_MONTHS obs starting before age TIER1_MAX_MIN_AGE
             → full AICc-weighted ensemble fit.
    Tier 2 (CONSTRAINED): data exists but sparse/mid-lifecycle only
             → fix segment canonical k, fit floor from observed window.
    Tier 3 (DEFAULT): < MIN_MONTHS_DATA or all fits failed
             → use segment canonical curve directly.

    For demand-shock GPUs: excluded from build_extended_monthly, so grp is empty.
      They receive tier-3 segment-default projections with is_shock=True.

    Returns DataFrame with columns for TVR, CI, sigma, P(below 10%), full curve.
    """
    monthly    = build_extended_monthly(df, keepa_monthly)
    # NOTE: rng is seeded per-GPU inside the loop from the GPU name hash so that
    # adding or removing any GPU does not perturb other GPUs' MC draws.
    target_idx = CURVE_TIMES.index(TARGET_AGE)

    # ── Fit segment canonical curves ──────────────────────────────────────────
    print("Fitting segment canonical curves …")
    canonical = {}
    for seg in GPU_SEGMENTS:
        result, anchors = fit_segment_canonical(monthly, seg)
        canonical[seg]  = result
        if result is not None:
            k_c  = result["params"][1]
            fl_c = result["params"][0]
            print(f"  [{seg}] canonical k={k_c:.4f}  floor={fl_c:.3f}  "
                  f"R²={result['r2']:.3f}  anchors={anchors}")
        else:
            print(f"  [{seg}] canonical fit FAILED (insufficient anchor data)")
    # Ensure UNKNOWN segment has a canonical fallback from SEG_K_FALLBACK
    if "UNKNOWN" not in canonical or canonical.get("UNKNOWN") is None:
        fb = SEG_K_FALLBACK.get("UNKNOWN", (0.020, 0.25))
        canonical["UNKNOWN"] = _synthetic_fit(fb[0], fb[1], SEG_CANONICAL_MIN)
        print(f"  [UNKNOWN] using fallback canonical k={fb[0]}, floor={fb[1]}")
    print()

    # ── Empirical floor priors per segment ────────────────────────────────────
    # Collect the long-run floor distribution from data-rich GPUs (age ≥ 60 mo)
    # within each segment. Used to regularise Tier 2 floor estimates for GPUs
    # that haven't yet shown visible depreciation (e.g. H100 at ages 17–35 mo).
    # Without this prior, those GPUs return floor ≈ 0.95 (segment bound) because
    # the optimiser has nothing to contradict the initial plateau. With the prior,
    # the estimate converges to the segment-typical floor (~0.35 for DATACENTER).
    print("Computing empirical floor priors …")
    seg_floor_priors = {}
    for seg in GPU_SEGMENTS:
        prior = _segment_floor_prior(monthly, seg)
        seg_floor_priors[seg] = prior
        if prior is not None:
            print(f"  [{seg}] floor prior:  mean={prior[0]:.3f}  "
                  f"std={prior[1]:.3f}")
        else:
            print(f"  [{seg}] floor prior:  insufficient anchor data "
                  f"(< 2 GPUs with age ≥ 60 mo)")
    print()

    # ── Demand-shock GPU set ──────────────────────────────────────────────────
    shock_set = set(df.loc[df["demand_shock"], "gpu_name"].unique())

    # ── Process every GPU that appears in any data source ─────────────────────
    # Include GPUs from retail, Keepa, and supplement so that GPUs with zero
    # retail data (e.g., H200 NVL after US-only filtering) are still processed
    # via their supplement/Keepa data and get Tier 2/3 treatment.
    all_gpus = sorted(set(df["gpu_name"].unique()) | set(monthly["gpu_name"].unique()))
    rows = []

    for gpu in all_gpus:
        # Per-GPU RNG seeded from GPU name: adding/removing any GPU elsewhere in
        # the dataset cannot perturb this GPU's MC draws (order-independent).
        # hashlib.md5 produces a deterministic hash independent of PYTHONHASHSEED
        # (Python's built-in hash() is randomised per-process by default since 3.3,
        # so abs(hash(gpu)) changes every run — breaking reproducibility).
        rng = np.random.default_rng(
            int(hashlib.md5(gpu.encode()).hexdigest(), 16) % (2 ** 32)
        )

        seg     = gpu_segment(gpu)
        can_fit = canonical.get(seg)
        is_shock = gpu in shock_set

        # Monthly data for this GPU (demand-shock GPUs are excluded from monthly)
        grp = monthly[monthly["gpu_name"] == gpu].sort_values("age_months").dropna()
        t   = grp["age_months"].values
        y   = grp["price_ratio"].values
        n   = len(grp)

        # Current ratio and appreciating flag
        if n >= 1:
            current_ratio = float(grp.tail(3)["price_ratio"].median())
        elif is_shock:
            raw = df[(df["gpu_name"] == gpu) & (df["condition"] == "NEW")].sort_values("date")
            current_ratio = float(raw.tail(20)["price_ratio"].median()) if len(raw) else np.nan
        else:
            current_ratio = np.nan
        appreciating = (current_ratio > APPRECIATING_THRESHOLD) if not np.isnan(current_ratio) else False

        age_range  = f"{t.min():.0f}–{t.max():.0f}" if n > 0 else "n/a"
        min_age    = float(t.min()) if n > 0 else np.nan

        # ── Choose strategy ───────────────────────────────────────────────────
        method   = None   # sentinel; set by whichever tier fires first
        p_below_10_by_t = {}  # P(<10%) at each horizon; populated by MC paths
        near = grp[np.abs(grp["age_months"] - TARGET_AGE) <= OBS_WINDOW] if n > 0 else pd.DataFrame()

        # A. Tier 1: try individual fit FIRST (before observed fallback).
        # Previously the observed path fired first, which meant a GPU with
        # 36 months of rich data but 3 obs near t=60 would skip curve fitting
        # entirely. Now we attempt the model fit first and fall back to
        # observed only if the fit fails or doesn't qualify.
        if n >= TIER1_MIN_MONTHS and not np.isnan(min_age) and min_age < TIER1_MAX_MIN_AGE:
            # Successor-adjusted fitting: if the GPU has a successor announcement and
            # pre-announcement data alone meets Tier 1 thresholds, fit only on that
            # window to avoid inflating k from the discrete announcement step-change.
            has_post_succ = ("post_successor" in grp.columns and grp["post_successor"].any())
            if has_post_succ:
                grp_pre = grp[~grp["post_successor"]]
                t_pre   = grp_pre["age_months"].values
                y_pre   = grp_pre["price_ratio"].values
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
            mc_out, w = _mc_from_ensemble(fits, CURVE_TIMES, rng)
            if mc_out is not None:
                valid_f  = {k: v for k, v in fits.items() if v is not None}
                best_model_name = (max(valid_f, key=lambda k: valid_f[k]["r2"])
                                   if valid_f else "n/a")
                best_r2  = valid_f[best_model_name]["r2"] if valid_f else np.nan

                # Quality gate 1: if best model R² < 0.20, the fit explains less
                # than 20% of price_ratio variance — essentially no better than a
                # weak linear trend. This threshold (raised from the old R²≥0 gate
                # that only rejected models worse than the mean) ensures we fall
                # through to Tier 2 for GPUs where the functional form genuinely
                # doesn't fit the observed data window.
                # Quality gate 2: if the median MC projection at t=0 exceeds 1.5x
                # MSRP, the model is back-extrapolating in a physically unrealistic
                # direction (GPUs do not launch at >1.5x their MSRP). This happens
                # when mid-lifecycle data is fit to a power-law or exp model that
                # diverges at t=0 — reject and fall through to tier 2.
                # Quality gate 3: if ALL valid models have parameters pinned
                # at bounds, the data window is insufficient for parameter
                # identification (e.g. floor+k both at lower bound → identical
                # meaningless TVR=0.7434). Fall through to Tier 2, which fixes
                # k from segment canonical and only fits floor.
                all_bounds_hit = all(
                    v.get("bounds_hit", False) for v in valid_f.values()
                ) if valid_f else True
                if not np.isnan(best_r2) and best_r2 >= 0.20 and not all_bounds_hit:
                    stats  = _normalize_curve_to_launch(_mc_to_stats(mc_out, target_idx))
                    proj_t0_check = stats["curve"].get(0, np.nan)
                    if not np.isnan(proj_t0_check) and proj_t0_check > DEMAND_SHOCK_RATIO:
                        pass   # implausible t=0 → method stays None → tier 2/3
                    else:
                        point = stats["point"];  ci_lo = stats["ci_lo"];  ci_hi = stats["ci_hi"]
                        sigma = stats["sigma_yr5"];  p_bel = stats["p_below_10"]
                        p_below_10_by_t = stats["p_below_10_by_t"]
                        curve = stats["curve"]
                        ci_lo_curve = stats["ci_lo_curve"]
                        ci_hi_curve = stats["ci_hi_curve"]
                        sigma_curve = stats["sigma_curve"]
                        method   = "fitted"
                        fit_tier = 1
                        best_model = best_model_name
                        exp_f    = fits.get("exp_floor")
                        pow_f    = fits.get("power_floor")
                        if best_model_name == "power_floor" and pow_f:
                            half_life = _half_life_power(*pow_f["params"])
                        elif exp_f:
                            half_life = _half_life_exp(*exp_f["params"])
                        else:
                            half_life = np.nan
                # else: R² < 0.20 → method stays None → falls through to observed/tier 2/3
            # else: mc_out is None → method stays None → falls through to observed/tier 2/3

        # B. Observed fallback: DISABLED — all GPUs now go through constrained
        # (Tier 2) or segment_default (Tier 3) for consistent MC-based uncertainty.
        # The observed path produced single-scalar sigma without MC, giving visually
        # different (rougher) uncertainty bands than the MC-based methods.
        if method is None and False:  # disabled — force Tier 2/3 for all GPUs
            point    = float(near["price_ratio"].median())
            ci_lo    = float(near["price_ratio"].quantile(0.025))
            ci_hi    = float(near["price_ratio"].quantile(0.975))
            sigma    = max(float(near["price_ratio"].std()) if len(near) > 1 else 0.0, MIN_SIGMA_YR5)
            # Use Gaussian CDF instead of raw frequency — raw counts from 3-21
            # data points can't estimate tail probabilities (always returns 0.0).
            # Compute p_below_10 at all curve times using the canonical curve shape
            # and growing sigma (uncertainty increases with forecast horizon).
            from scipy.stats import norm
            curve    = _curve_from_canonical_scaled(can_fit, TARGET_AGE, point)
            # Observed path has no MC — per-time-point CIs are unavailable.
            # Set to NaN so the chart can detect and fall back gracefully.
            ci_lo_curve = {ct: np.nan for ct in CURVE_TIMES}
            ci_hi_curve = {ct: np.nan for ct in CURVE_TIMES}
            sigma_curve = {ct: np.nan for ct in CURVE_TIMES}
            # But we do have the t=60 CI from the raw data quantiles above
            ci_lo_curve[TARGET_AGE] = ci_lo
            ci_hi_curve[TARGET_AGE] = ci_hi
            sigma_curve[TARGET_AGE] = sigma
            # Normalize to launch: force proj_t0=1.0
            obs_stats = _normalize_curve_to_launch({
                "curve": curve, "ci_lo_curve": ci_lo_curve,
                "ci_hi_curve": ci_hi_curve, "sigma_curve": sigma_curve,
                "ci_lo": ci_lo, "ci_hi": ci_hi, "sigma_yr5": sigma,
            })
            curve = obs_stats["curve"]
            ci_lo_curve = obs_stats["ci_lo_curve"]
            ci_hi_curve = obs_stats["ci_hi_curve"]
            sigma_curve = obs_stats["sigma_curve"]
            # Compute p_below_10 at all curve times using Gaussian CDF.
            # Sigma grows with time: sigma(t) = sigma_yr5 * sqrt(t/60) for t>60
            # (random walk scaling), capped at MIN_SIGMA_YR5 for t<=60.
            p_bel = float(norm.cdf(0.10, loc=point, scale=sigma))
            p_below_10_by_t = {}
            for ct in CURVE_TIMES:
                cv = curve.get(ct, np.nan)
                if np.isnan(cv):
                    p_below_10_by_t[ct] = np.nan
                else:
                    # Sigma grows beyond year 5 (more uncertainty at longer horizons)
                    sigma_t = sigma * max(1.0, (ct / 60.0) ** 0.5) if ct > 0 else 0.0
                    sigma_t = max(sigma_t, MIN_SIGMA_YR5)
                    p_below_10_by_t[ct] = float(norm.cdf(0.10, loc=cv, scale=sigma_t))
            method   = "observed"
            fit_tier = 1
            best_model = "n/a";  best_r2 = np.nan;  w = {}
            # Estimate half_life by interpolating the observed curve
            _hl = np.nan
            _ct = sorted(ct for ct in CURVE_TIMES if not np.isnan(curve.get(ct, np.nan)))
            for _j in range(1, len(_ct)):
                v_prev, v_cur = curve[_ct[_j - 1]], curve[_ct[_j]]
                if v_prev >= 0.5 and v_cur < 0.5:
                    # linear interpolation between the two time-points
                    _hl = _ct[_j - 1] + (_ct[_j] - _ct[_j - 1]) * (v_prev - 0.5) / (v_prev - v_cur)
                    break
            half_life = float(_hl)

        # C. Tier 2: segment-constrained (fix k, fit floor with empirical prior)
        if method is None and n >= MIN_MONTHS_DATA and can_fit is not None:

            k_can      = float(can_fit["params"][1])
            k_var      = float(can_fit["cov"][1, 1]) if can_fit["cov"].shape[0] > 1 else 1e-6
            floor_prior = seg_floor_priors.get(seg)   # (mean, std) or None
            floor_opt, floor_var = fit_constrained_floor(
                t, y, k_can,
                floor_prior=floor_prior,
                n_data_months=n,
            )

            if floor_opt is not None:
                # Derive floor–k cross-covariance from the canonical segment fit.
                # floor and k are negatively correlated in exp_floor: a higher k
                # yields the same observed data with a lower floor. Using the
                # canonical correlation as a proxy avoids the independent-sampling
                # bias that inflated sigma_yr5 and p_below_10pct.
                k_floor_cov = 0.0
                if can_fit["cov"].shape[0] >= 2 and floor_var is not None:
                    can_fl_std = float(np.sqrt(abs(can_fit["cov"][0, 0])))
                    can_k_std  = float(np.sqrt(abs(can_fit["cov"][1, 1])))
                    if can_fl_std > 0 and can_k_std > 0:
                        corr = float(np.clip(
                            can_fit["cov"][0, 1] / (can_fl_std * can_k_std),
                            -0.99, 0.99))
                        k_floor_cov = corr * float(np.sqrt(abs(floor_var))) * float(np.sqrt(abs(k_var)))

                mc_out = _mc_from_constrained(floor_opt, floor_var,
                                               k_can, k_var, CURVE_TIMES, rng,
                                               k_floor_cov=k_floor_cov)

                # ── Forward projection from current market price ────────────
                # Standard conditional forecasting: anchor the projection at
                # the most recent observed price rather than re-simulating
                # from P(0)=1.0. This prevents the model from ignoring where
                # the GPU actually trades today. Consistent with Tier 3.
                # Cap at 1.0 so above-MSRP premiums are treated as temporary.
                if n > 0 and not np.isnan(current_ratio):
                    t_last = float(t[-1])
                    # Canonical curve value at the current age
                    canon_now = floor_opt + (1 - floor_opt) * np.exp(-k_can * t_last)
                    if canon_now > 0:
                        # Use the actual current_ratio — no cap at MSRP.
                        # If a GPU trades above MSRP, the forward projection
                        # starts from that elevated level and decays from there.
                        anchor = current_ratio
                        scale = anchor / canon_now
                        scale = float(np.clip(scale, 0.75, 2.5))
                        # Stochastic scaling: each MC draw gets its own scale
                        # sampled from Normal(scale, 0.20*scale), propagating
                        # observation noise from the current market price.
                        # Deterministic scaling compressed P(<10%) by shifting
                        # all samples uniformly; stochastic scaling widens tails.
                        scale_samples = rng.normal(scale, 0.10 * abs(scale), MC_SAMPLES)
                        scale_samples = np.clip(scale_samples, 0.75, 2.5)
                        mc_out = mc_out * scale_samples[:, np.newaxis]

                stats  = _normalize_curve_to_launch(_mc_to_stats(mc_out, target_idx))
                point  = stats["point"];  ci_lo = stats["ci_lo"];  ci_hi = stats["ci_hi"]
                sigma  = stats["sigma_yr5"];  p_bel = stats["p_below_10"]
                p_below_10_by_t = stats["p_below_10_by_t"]
                curve  = stats["curve"]
                ci_lo_curve = stats["ci_lo_curve"]
                ci_hi_curve = stats["ci_hi_curve"]
                sigma_curve = stats["sigma_curve"]
                method   = "constrained"
                fit_tier = 2
                best_model = "exp_floor(k_fixed)"
                best_r2  = np.nan
                half_life = _half_life_from_curve(curve)
                w = {"exp_floor_constrained": 1.0}
            # else: floor fit failed → method stays None → tier 3 fires

        # D. Tier 3: segment default (use canonical curve; scale to observed level)
        if method is None:

            if can_fit is not None:
                k_can   = float(can_fit["params"][1])
                fl_can  = float(can_fit["params"][0])
                k_var   = float(can_fit["cov"][1, 1]) if can_fit["cov"].shape[0] > 1 else 1e-6
                fl_var  = float(can_fit["cov"][0, 0])

                # Scale canonical to observed median if we have any data
                if n > 0 and not np.isnan(current_ratio):
                    # Find closest age in observed data
                    t_obs = float(t[-1])
                    canon_at_obs = fl_can + (1 - fl_can) * np.exp(-k_can * t_obs)
                    scale = current_ratio / canon_at_obs if canon_at_obs > 0 else 1.0
                    scale = float(np.clip(scale, 0.75, 2.5))
                else:
                    scale = 1.0

                # MC: sample canonical params, apply stochastic scale
                mc_out = np.zeros((MC_SAMPLES, len(CURVE_TIMES)))
                t_arr  = np.array(CURVE_TIMES, dtype=float)
                cov_can = can_fit["cov"]
                cov_reg = cov_can + np.eye(2) * max(1e-10, 1e-6 * np.trace(cov_can))
                # Stochastic scale: each MC draw gets its own scale factor
                scale_samples = rng.normal(scale, 0.10 * abs(scale), MC_SAMPLES)
                scale_samples = np.clip(scale_samples, 0.75, 2.5)
                for s in range(MC_SAMPLES):
                    try:
                        if np.linalg.cond(cov_reg) < 1e10:
                            fl_s, k_s = rng.multivariate_normal([fl_can, k_can], cov_reg)
                        else:
                            fl_s, k_s = fl_can, k_can
                    except (np.linalg.LinAlgError, ValueError, RuntimeError):
                        fl_s, k_s = fl_can, k_can
                    fl_s = float(np.clip(fl_s, 0.001, 0.80))
                    k_s  = float(np.clip(k_s,  0.005, 0.25))   # match updated MODELS bounds
                    mc_out[s] = np.clip(scale_samples[s] * (fl_s + (1 - fl_s) * np.exp(-k_s * t_arr)),
                                         0.0, 3.0)
                # No cap at t=0 — allow the curve to reflect above-MSRP
                # pricing when the market data shows it.

                stats  = _normalize_curve_to_launch(_mc_to_stats(mc_out, target_idx))
                point  = stats["point"];  ci_lo = stats["ci_lo"];  ci_hi = stats["ci_hi"]
                sigma  = stats["sigma_yr5"];  p_bel = stats["p_below_10"]
                p_below_10_by_t = stats["p_below_10_by_t"]
                curve  = stats["curve"]
                ci_lo_curve = stats["ci_lo_curve"]
                ci_hi_curve = stats["ci_hi_curve"]
                sigma_curve = stats["sigma_curve"]
                method   = "segment_default"
                fit_tier = 3
                best_model = f"canonical_{seg}"
                best_r2  = np.nan
                half_life = _half_life_from_curve(curve)
                w = {}
            else:
                # No canonical fit available — skip
                continue

        # Guard: if method is still None, all branches failed — skip this GPU
        if method is None:
            continue

        # ── Confidence flag ───────────────────────────────────────────────────
        ci_width = ci_hi - ci_lo
        # Minimum data requirements for HIGH/MEDIUM: sparse data with
        # artificially tight CIs (e.g., MI210 with 6 months) must not get HIGH.
        age_span = float(str(age_range).split("–")[-1]) - float(str(age_range).split("–")[0]) if "–" in str(age_range) else 0
        sparse_data = (n < 12) or (age_span < 18)
        if method == "observed":
            if sparse_data:
                conf_flag = "MEDIUM" if ci_width < 0.15 else "LOW"
            else:
                conf_flag = "HIGH" if ci_width < 0.15 else "MEDIUM" if ci_width < 0.30 else "LOW"
        elif appreciating or is_shock:
            conf_flag = "LOW"
        elif fit_tier == 3:
            # Tier 3 uses a pooled canonical, not an individual fit, so confidence
            # is capped at MEDIUM. A Tier 3 GPU with a very tight CI (well-anchored
            # by recent data) can be MEDIUM; otherwise LOW.
            conf_flag = "MEDIUM" if ci_width < 0.30 else "LOW"
        elif fit_tier == 2:
            conf_flag = "LOW" if ci_width >= 0.35 else "MEDIUM"
        else:
            conf_flag = "HIGH" if ci_width < 0.15 else "MEDIUM" if ci_width < 0.35 else "LOW"

        rows.append({
            "gpu_name":         gpu,
            "segment":          seg,
            "is_carrier_adjusted": gpu in CARRIER_COST,
            "fit_tier":         fit_tier,
            "n_months":         n if n > 0 else 0,
            "age_range_months": age_range,
            "current_ratio":    current_ratio,
            "appreciating":     appreciating,
            "is_shock":         is_shock,
            "method":           method,
            "best_model":       best_model,
            "best_r2":          best_r2,
            "w_exp_floor":      w.get("exp_floor", np.nan),
            "w_power_floor":    w.get("power_floor", np.nan),
            "proj_yr5_ratio":   point,
            "proj_ci_lo":       ci_lo,
            "proj_ci_hi":       ci_hi,
            "ci_width":         ci_width,
            "sigma_yr5":        sigma,
            "p_below_10pct":    p_bel,
            "p_below_10_8yr":  p_below_10_by_t.get(96, np.nan) if isinstance(p_below_10_by_t, dict) else np.nan,
            "p_below_10_10yr": p_below_10_by_t.get(120, np.nan) if isinstance(p_below_10_by_t, dict) else np.nan,
            **{f"proj_t{t}": curve.get(t, np.nan) for t in CURVE_TIMES},
            **{f"ci_lo_t{t}": ci_lo_curve.get(t, np.nan) for t in CURVE_TIMES},
            **{f"ci_hi_t{t}": ci_hi_curve.get(t, np.nan) for t in CURVE_TIMES},
            **{f"sigma_t{t}": sigma_curve.get(t, np.nan) for t in CURVE_TIMES},
            "conf_flag":        conf_flag,
            "half_life_months": half_life,
        })

    return pd.DataFrame(rows)


def _curve_from_canonical_scaled(can_fit, t_anchor, anchor_value):
    """
    Return full curve dict {t: ratio} using floor-preserving amplitude scaling
    of the segment canonical curve so that curve[t_anchor] == anchor_value.
    Used for 'observed' tier-1 GPUs.

    Formula: g(t) = fl_c + (anchor_value - fl_c) * exp(-k_c * (t - t_anchor))
    This keeps the long-run asymptote at fl_c (the segment canonical floor),
    unlike multiplicative scaling which shifts the floor to scale * fl_c. All
    values are capped at 1.0 since GPUs cannot launch above MSRP.

    If anchor_value > 1.0 (GPU is appreciating), early back-extrapolated values
    are clipped at 1.0.
    """
    curve = {ct: np.nan for ct in CURVE_TIMES}
    curve[t_anchor] = anchor_value
    if can_fit is None:
        return curve
    k_c  = float(can_fit["params"][1])
    fl_c = float(can_fit["params"][0])
    # Clamp effective floor to anchor_value when anchor < canonical floor.
    # Without this, the amplitude (anchor_value - fl_c) goes negative and
    # backward extrapolation produces an inverted (rising) curve.
    fl_eff = min(fl_c, anchor_value)
    for ct in CURVE_TIMES:
        if ct != t_anchor:
            val = fl_eff + (anchor_value - fl_eff) * np.exp(-k_c * (ct - t_anchor))
            curve[ct] = float(np.clip(val, 0.0, 3.0))
    return curve


# ── Out-of-sample validation ───────────────────────────────────────────────────

def validate_extrapolation(df, keepa_monthly=None):
    """
    Time-based holdout: fit on all-but-last-6-months, project forward,
    compare against actual held-out values.
    """
    ext     = build_extended_monthly(df, keepa_monthly)
    monthly = ext[ext["gpu_name"].isin(VALIDATION_GPUS)].copy()

    print("=" * 60)
    print("OUT-OF-SAMPLE VALIDATION (last-6-month holdout)")
    print("Fit on earlier data, project forward, compare to held-out months")
    print("=" * 60)

    for gpu, grp in monthly.groupby("gpu_name"):
        grp = grp.sort_values("age_months").dropna()
        if len(grp) < MIN_MONTHS_DATA + HOLDOUT_MONTHS:
            print(f"  {gpu}: not enough months for holdout ({len(grp)} total)")
            continue

        train = grp.iloc[:-HOLDOUT_MONTHS]
        test  = grp.iloc[-HOLDOUT_MONTHS:]

        t_tr      = train["age_months"].values
        y_tr      = train["price_ratio"].values
        t_project = test["age_months"].mean()

        fits = {name: fit_model(t_tr, y_tr, name) for name in MODELS}
        proj = ensemble_project(fits, t_project=t_project)

        if proj is None:
            print(f"  {gpu}: fit failed on training window")
            continue

        point, ci_lo, ci_hi, _ = proj
        actual    = test["price_ratio"].median()
        error_pct = (point - actual) / actual * 100 if actual > 0 else np.nan
        within_ci = ci_lo <= actual <= ci_hi

        print(f"  {gpu}  (train age: {t_tr.min():.0f}–{t_tr.max():.0f} mo  "
              f"| project to t={t_project:.0f} mo):")
        print(f"    Projected: {point:.3f}  [{ci_lo:.3f}, {ci_hi:.3f}]")
        print(f"    Actual (holdout median): {actual:.3f}")
        print(f"    Error: {error_pct:+.1f}%   Within CI: {'YES ✓' if within_ci else 'NO ✗'}")
        print()


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)

    df = load_data(verbose=False)

    keepa_monthly = None
    if os.path.exists(KEEPA_MONTHLY_PATH):
        keepa_monthly = pd.read_csv(KEEPA_MONTHLY_PATH)
        print(f"[keepa] Loaded {len(keepa_monthly)} monthly obs from {KEEPA_MONTHLY_PATH}\n")
    else:
        print("[keepa] keepa_monthly.csv not found — run keepa_prep.py first.\n")

    # Load optional datacenter supplement (eBay/Vast.ai data)
    supp_monthly = load_datacenter_supplement(verbose=True)
    if supp_monthly is not None and keepa_monthly is not None:
        keepa_monthly = pd.concat([keepa_monthly, supp_monthly], ignore_index=True)
    elif supp_monthly is not None:
        keepa_monthly = supp_monthly

    print("[1/2] Out-of-sample validation")
    try:
        validate_extrapolation(df, keepa_monthly)
    except Exception as e:
        print(f"  Validation failed ({e}), continuing to fitting step\n")

    print("[2/2] Three-tier hierarchical fitting — all GPUs")
    results = fit_all_gpus(df, keepa_monthly)

    # ── Display ────────────────────────────────────────────────────────────────
    deprec  = results[~results["appreciating"] & ~results["is_shock"]].sort_values("proj_yr5_ratio")
    appreci = results[results["appreciating"] | results["is_shock"]].sort_values("proj_yr5_ratio", ascending=False)

    print("=" * 90)
    print("DEPRECIATION RESULTS — all GPUs  (rank 1 = worst depreciator)")
    print("Tier 1=individual  2=segment-constrained  3=segment-default")
    print("=" * 90)
    display = ["gpu_name", "segment", "fit_tier", "n_months", "age_range_months",
               "current_ratio", "method", "best_r2",
               "proj_yr5_ratio", "proj_ci_lo", "proj_ci_hi",
               "sigma_yr5", "p_below_10pct",
               "half_life_months", "conf_flag"]
    display = [c for c in display if c in deprec.columns]
    print(deprec[display].to_string(index=False))

    print("\n" + "=" * 90)
    print("FULL DEPRECIATION CURVES  (price_ratio at t=0,12,24,36,48,60 months)")
    print("=" * 90)
    curve_cols = ["gpu_name", "segment", "fit_tier",
                  "proj_t0", "proj_t12", "proj_t24", "proj_t36", "proj_t48", "proj_t60",
                  "p_below_10pct", "sigma_yr5", "conf_flag"]
    curve_cols = [c for c in curve_cols if c in deprec.columns]
    pd.set_option("display.float_format", "{:.3f}".format)
    print(deprec[curve_cols].to_string(index=False))

    if len(appreci):
        print("\n" + "=" * 70)
        print(f"APPRECIATING / SHOCK GPUs (current ratio > {APPRECIATING_THRESHOLD}x MSRP)")
        print("=" * 70)
        print(appreci[["gpu_name", "segment", "fit_tier", "is_shock",
                        "current_ratio", "proj_yr5_ratio", "conf_flag"]]
              .to_string(index=False))

    results.to_csv("outputs/curve_fit_results.csv", index=False)
    print("\nSaved → outputs/curve_fit_results.csv")
    print(f"Total GPUs in output: {len(results)}")
