# Scrap Floor vs. Depreciation Model: Comparison Analysis

**Date:** 2026-03-29
**Scope:** 22 datacenter GPU scrap reports vs. depreciation model outputs from `depreciation_curves.py`

---

## 1. Executive Summary

The depreciation model uses an `exp_floor` parameter (asymptotic lower bound on price/MSRP ratio) that is fitted per GPU but has no connection to actual scrap or salvage values. This analysis compares the model's projected 10-year terminal values against real-world recycler scrap values researched in the scrap reports.

**Key finding:** The model's 10-year projected values (proj_t120) are consistently and dramatically higher than the recycler scrap floor -- typically 10-100x above the recycler payout as a percentage of MSRP. The model's `exp_floor` parameter, which ranges from 0.1% to 80% of MSRP, is a mathematical fitting artifact, not a scrap-value anchor. For the oldest GPUs in the dataset (V100 series, T4), the model projects 10-year values of 4-5% of MSRP, which is still far above the recycler scrap floor of 0.02-0.15% of MSRP, but getting closer to the broker/for-parts floor of 1-5% of MSRP.

---

## 2. Comparison Table

### Reading Notes
- **Recycler scrap** = Option B in the scrap reports (e-waste recycler pays by weight + precious metal assay credit). This is the absolute physical floor.
- **Broker/ITAD scrap** = Option A (broker buys dead card whole for resale/repair). This is the realistic floor for cards with any remaining secondary market.
- **Current ratio** = current_price / MSRP from the depreciation model (as of March 2026).
- **Proj Yr5** = model's projected price/MSRP at 60 months from launch.
- **Proj Yr10** = model's projected price/MSRP at 120 months from launch (proj_t120).
- **Recycler % MSRP** = midpoint of the recycler (Option B) range as a percentage of MSRP.
- **Broker % MSRP** = midpoint of the broker (Option A) range as a percentage of MSRP.

| GPU | MSRP | Current Ratio | Proj Yr5 | Proj Yr10 | Recycler Mid ($) | Recycler % MSRP | Broker Mid ($) | Broker % MSRP | Yr10 Above Recycler? | Gap (Yr10 - Recycler %) |
|-----|------|---------------|----------|-----------|-------------------|-----------------|----------------|---------------|---------------------|------------------------|
| T4 | $2,500 | 0.261 | 0.352 | 0.231 | $4 | 0.16% | $110 | 4.4% | YES | +23.0 pp |
| Tesla V100 PCIe (16GB) | $8,000 | 0.033 | 0.181 | 0.049 | $12 | 0.14% | $300 | 3.7% | YES | +4.7 pp |
| Tesla V100 PCIe (32GB) | $10,000 | 0.095 | 0.224 | 0.068 | $12 | 0.12% | $300 | 3.0% | YES | +6.7 pp |
| Tesla V100 SXM2 (16GB) | $8,000 | 0.030 | 0.181 | 0.048 | $4 | 0.05% | $200 | 2.5% | YES | +4.7 pp |
| Tesla V100 SXM2 (32GB) | $10,000 | 0.059 | 0.186 | 0.054 | $4 | 0.04% | $200 | 2.0% | YES | +5.3 pp |
| Tesla V100S PCIe | $11,500 | 0.087 | 0.193 | 0.061 | $12 | 0.10% | $600 | 5.2% | YES | +6.0 pp |
| A10 | $2,500 | 0.666 | 0.672 | 0.411 | $17 | 0.66% | $250 | 10.0% | YES | +40.4 pp |
| A16 PCIe | $5,000 | 0.578 | 0.582 | 0.419 | $49 | 0.97% | $678 | 13.6% | YES | +41.8 pp |
| A30 PCIe | $4,599 | 0.567 | 0.571 | 0.370 | $27 | 0.58% | $520 | 11.3% | YES | +36.4 pp |
| A40 | $27,500 | 0.960 | 0.638 | 0.223 | $29 | 0.10% | $1,063 | 3.9% | YES | +22.2 pp |
| A100 PCIe (40GB) | $11,000 | 0.536 | 0.604 | 0.382 | $40 | 0.36% | $913 | 8.3% | YES | +37.8 pp |
| A100 PCIe (80GB) | $15,000 | 1.212 | 0.622 | 0.212 | $37 | 0.24% | $1,375 | 9.2% | YES | +21.0 pp |
| A100 SXM4 (40/80GB) | $10,000 | 0.236 | 0.288 | 0.132 | $11 | 0.11% | $1,213 | 12.1% | YES | +13.1 pp |
| A100X | $33,700 | 0.657 | 0.524 | 0.309 | $39 | 0.12% | $1,525 | 4.5% | YES | +30.8 pp |
| L4 | $2,500 | 1.000 | 0.758 | 0.500 | $6 | 0.24% | $430 | 17.2% | YES | +49.8 pp |
| L40 | $6,800 | 0.867 | 0.681 | 0.413 | $29 | 0.43% | $1,255 | 18.5% | YES | +40.9 pp |
| L40S | $8,000 | 0.987 | 0.663 | 0.407 | $29 | 0.36% | $1,489 | 18.6% | YES | +40.3 pp |
| H100 PCIe (80GB) | $25,000 | 1.117 | 0.807 | 0.515 | $33 | 0.13% | $3,775 | 15.1% | YES | +51.4 pp |
| H100 SXM5 (80GB) | $30,000 | 0.667 | 0.486 | 0.329 | $92 | 0.31% | $2,355 | 7.9% | YES | +32.6 pp |
| H200 NVL | $37,500 | 0.920 | 0.394 | 0.115 | $33 | 0.09% | $6,550 | 17.5% | YES | +11.4 pp |
| H200 SXM | $25,000 | 0.857 | 0.479 | 0.275 | $16 | 0.06% | $4,025 | 16.1% | YES | +27.4 pp |
| NVIDIA GH200 | $35,000 | 0.157 | 0.187 | 0.054 | $28 | 0.08% | $963 | 2.7% | YES | +5.3 pp |
| AMD Instinct MI300X | $15,000 | 2.230 | 0.237 | 0.069 | $20 | 0.13% | $3,050 | 20.3% | YES | +6.7 pp |
| Radeon Instinct MI210 | $16,500 | 0.584 | 0.532 | 0.314 | $12 | 0.07% | $690 | 4.2% | YES | +31.3 pp |
| Gaudi2 HL-225H | $8,125 | -- | 0.239 | 0.069 | $30 | 0.37% | $350 | 4.3% | YES | +6.6 pp |

---

## 3. How the Depreciation Model Handles the Floor

### 3.1 The `exp_floor` Model

The primary depreciation model is:

```
P(t) = floor + (1 - floor) * exp(-k * t)
```

where:
- `floor` is an asymptotic lower bound on price/MSRP ratio
- `k` is the decay rate
- `t` is age in months

**Parameter bounds (from `MODELS` dict):**
- `floor`: [0.001, 0.80] -- the model allows the floor to be as low as 0.1% of MSRP
- `k`: [0.005, 0.25] -- decay rate bounded to plausible half-lives (2.8 to 138 months)

**Initial guess:** floor = 0.20, k = 0.02

### 3.2 Segment Fallback Floors

For GPUs that cannot be individually fitted (Tier 3 / canonical), the model uses hardcoded fallback values:

| Segment | Fallback k | Fallback floor | Rationale |
|---------|-----------|----------------|-----------|
| DATACENTER | 0.025 | 0.02 (2%) | "K80 at 0.4-0.7%, V100 at 3-4% and falling" |
| WORKSTATION | 0.018 | 0.03 (3%) | "Quadro M6000 at 1.9%, K6000 at 1-2% after 11-13yr" |
| CONSUMER | 0.020 | 0.05 (5%) | "GTX 980 Ti at 8% after 11yr; absolute $25-50 floor" |

### 3.3 Extrapolation Beyond Year 5

The `generate_curves.py` file contains a `make_smooth_curve()` function that extrapolates beyond the 60-month (5-year) model window to 120 months (10 years). It estimates a secondary floor from the t=48 and t=60 anchor points:

```python
floor_est = max(0.0, 2 * v60 - v48)
```

This is a linear extrapolation of the decay rate, not anchored to any physical scrap value. The extrapolated curve then decays exponentially toward this `floor_est` value.

### 3.4 Key Observation: The Model Floor Has Nothing to Do with Scrap Value

The `exp_floor` parameter in the depreciation model represents the asymptotic price ratio that the fitted curve converges toward. It is a mathematical fitting parameter driven by secondary market transaction data (eBay sold prices, Keepa data, datacenter supplement). It reflects the point at which price decline slows in the observed data window -- which is driven by residual functional demand, not by material recovery value.

The datacenter fallback floor of 2% of MSRP ($200 on a $10,000 GPU) is a reasonable representation of the "for parts" / broker market, but it is 10-100x higher than the actual recycler scrap value ($3-$92 depending on card weight and precious metal content).

---

## 4. Convergence Analysis

### 4.1 Do Depreciation Curves Reach the Scrap Floor?

**No, not within 10 years.** Every single GPU in the model has a proj_t120 (10-year projected value) that is dramatically higher than the recycler scrap floor:

- **Smallest gap:** V100 SXM2 16GB at proj_t120 = 4.8% of MSRP vs. recycler floor of 0.05% of MSRP (still 96x higher)
- **Largest gap:** L4 at proj_t120 = 50.0% of MSRP vs. recycler floor of 0.24% of MSRP (208x higher)

Even the most aggressively depreciating GPUs in the model (GH200, V100 PCIe 16GB, V100 SXM2 16GB) are projected to retain 4-5% of MSRP at 10 years, while their recycler scrap values are 0.04-0.16% of MSRP.

### 4.2 Would They Eventually Converge?

Using the `exp_floor` model formula P(t) = floor + (1-floor)*exp(-k*t), convergence to the recycler scrap floor would require t -> infinity, at which point P(t) -> floor. The question is whether the fitted `floor` parameter is below the recycler scrap value:

For the datacenter canonical (used for Tier 3 GPUs): `floor = 0.02` (2% of MSRP).
- On a $10,000 GPU: floor = $200. Recycler scrap = $4-$40. The model's mathematical floor is 5-50x above recycler scrap.
- On a $30,000 GPU: floor = $600. Recycler scrap = $16-$92. The model's floor is 7-38x above recycler scrap.

For individually fitted Tier 2 GPUs, the floor parameter is data-driven but the bound allows floor as low as 0.1% of MSRP, which would put it in the same neighborhood as recycler scrap. However, in practice the fitted floors tend to be much higher because the model is fitting to secondary market prices (which include functional demand), not scrap.

**Bottom line: The model never converges to the recycler scrap floor, even asymptotically, because the `exp_floor` parameter is set by functional secondary market dynamics, not material recovery value.**

### 4.3 The Two Distinct Floors

The scrap research reveals that there are actually two separate "floors" for end-of-life GPUs:

1. **Functional floor (broker/ITAD/for-parts):** 1-20% of MSRP. This is what the depreciation model's `exp_floor` parameter is capturing. It represents the price at which dead cards still have value for repair, donor boards, or resale into repair ecosystems. This floor depends on the installed base size, form factor, and ecosystem health.

2. **Physical floor (recycler/e-waste):** 0.02-1.0% of MSRP. This is the actual scrap floor -- what you get when no one wants the card for any functional purpose, and it is processed as e-waste by weight + precious metal assay. This floor depends on card weight, board composition, and precious metal content.

The depreciation model only captures floor #1. Floor #2 is never reached by any GPU that still has any functional demand whatsoever.

---

## 5. When Does a GPU Cross from Functional Floor to Scrap Floor?

Based on the scrap research, the transition from broker-viable to recycler-only happens when:

1. **The ecosystem collapses** -- No remaining repair demand, no driver support, no compatible systems available. The Gaudi2 is approaching this: Intel's strategic pivot means the Gaudi ecosystem may have no demand within 2-3 years.

2. **Working unit price drops below ~$50-100** -- Below this threshold, broker overhead exceeds recovery. The T4 is in this zone: at $699-$1,100 working, it is already borderline for ITAD brokers, and "for parts" eBay sales ($50-$150) are the highest-recovery path.

3. **The form factor becomes orphaned** -- SXM2 modules (V100) are becoming harder to broker as DGX-1V/HGX systems are retired. Adapter boards extend the functional floor, but not indefinitely.

From the data, the V100 series (launched 2017-2019) is the closest to the transition point at 7-9 years old:
- V100 SXM2 16GB: working price $95-$400, "for parts" $99-$300, recycler $3-$5
- V100 PCIe 16GB: working price $270-$430, "for parts" $99-$500, recycler $8-$15

The functional floor for these cards is perhaps 2-3 years from collapsing into the recycler floor, which would happen around year 10-12 from launch.

---

## 6. Implications for the Depreciation Model

### 6.1 The Model is Correct for Its Intended Purpose

The depreciation model projects secondary market resale value for GPUs that retain functional demand. Its `exp_floor` parameter correctly captures the price at which depreciation slows -- because there are real buyers (brokers, repair shops, budget labs) who will pay more than scrap for a working or repairable card.

### 6.2 But It Has No True Terminal Value

The model assumes the price curve asymptotically approaches the `floor` parameter and stays there forever. In reality:

- The functional floor eventually collapses when the ecosystem dies
- The price then falls rapidly from the functional floor to the physical scrap floor
- This collapse is a phase transition, not a smooth exponential decay

The model cannot capture this phase transition because it uses a monotonically decreasing curve that asymptotes smoothly.

### 6.3 The Gap Between Model and Reality

| GPU Age | Model Projects | Reality |
|---------|---------------|---------|
| 0-5 years | Accurate (fitted to data) | Functional demand drives pricing |
| 5-8 years | Reasonable extrapolation | Functional demand persists but thinning |
| 8-12 years | Overstates value | Ecosystem collapse begins for some GPUs |
| 12+ years | Significantly overstates | Most cards at or near recycler scrap floor |

---

## 7. Recommendations

### 7.1 Add a Scrap Floor Parameter to the Model

The model should incorporate a GPU-specific scrap floor derived from the physical teardown data:

```python
# Example: add scrap floor from recycler estimates
SCRAP_FLOOR_USD = {
    "T4": 4,
    "Tesla V100 PCIe 16 GB": 12,
    "A100 SXM4 80 GB": 11,
    "H100 SXM5 80 GB": 92,
    # ...
}
```

The scrap floor as a % of MSRP can then be used as an absolute lower bound:
```python
scrap_ratio = SCRAP_FLOOR_USD[gpu] / MSRP[gpu]
proj_t120 = max(model_projection, scrap_ratio)  # never below physical scrap
```

However, this would only matter at very long time horizons (15+ years) since the model currently projects values well above the scrap floor even at 10 years.

### 7.2 Model the Ecosystem Collapse Transition

A more impactful improvement would be to model the transition from functional floor to scrap floor as a step function or sigmoid:

```
P_final(t) = P_model(t) * survival_prob(t) + scrap_ratio * (1 - survival_prob(t))
```

where `survival_prob(t)` represents the probability that the GPU's secondary market ecosystem still exists at time t. This could be informed by:
- GPU generation age (older gens lose support faster)
- Installed base size (larger installed base sustains demand longer)
- Ecosystem health (NVIDIA CUDA cards survive longer than Intel Gaudi or AMD ROCm)
- Form factor (PCIe persists longer than SXM/OAM)

### 7.3 Use Broker Floor as a Practical Minimum for 5-10 Year Projections

For the 5-10 year window the model targets, the broker/ITAD floor (Option A from the scrap reports) is more relevant than the recycler floor. These values could serve as a reality check:

| GPU | Broker Floor % MSRP | Model Yr10 % MSRP | Status |
|-----|--------------------|--------------------|--------|
| T4 | 4.4% | 23.1% | Model well above broker floor |
| V100 PCIe 16GB | 3.7% | 4.9% | Approaching broker floor |
| V100 SXM2 32GB | 2.0% | 5.4% | Within striking distance |
| GH200 | 2.7% | 5.4% | Within striking distance |
| H100 PCIe 80GB | 15.1% | 51.5% | Model well above |
| L4 | 17.2% | 50.0% | Model well above |

For the V100 and GH200 (older or fast-depreciating GPUs), the model's 10-year projection is within 2-3 percentage points of the broker floor. This suggests the broker floor would be a useful sanity check for the model's extreme extrapolations.

### 7.4 Scrap Data as Confidence Bounds

The scrap research provides a hard lower bound on value that could be used to truncate the model's confidence intervals:
- The 90% CI lower bound (ci_lo_t120) should never go below the recycler scrap floor
- The model's `p_below_10pct` probability calculation could be augmented with a `p_below_scrap` probability

### 7.5 Weight-Based Scrap Heuristic

The scrap research reveals a surprisingly simple heuristic for the recycler floor:

```
Recycler scrap value = card_weight_lbs * $5-$15/lb + PM_credit * 0.65
```

For most datacenter GPUs, the precious metal credit is negligible ($2-$12), and the scrap value is dominated by the PCB weight at $5-15/lb. This means the recycler floor scales approximately with physical card mass, not with MSRP or compute capability. The model could incorporate a weight-based scrap estimate as a hardcoded minimum.

---

## 8. Summary Statistics

| Metric | Value |
|--------|-------|
| GPUs compared | 25 model variants across 22 scrap reports |
| GPUs where Yr10 model projection > recycler scrap | 25/25 (100%) |
| Average Yr10 model projection (% MSRP) | 23.4% |
| Average recycler scrap (% MSRP) | 0.24% |
| Average broker floor (% MSRP) | 9.1% |
| Ratio of model Yr10 to recycler scrap | ~97x (median) |
| Ratio of model Yr10 to broker floor | ~2.6x (median) |
| Closest to scrap convergence | V100 SXM2 16GB (model 4.8% vs recycler 0.05%) |
| Furthest from scrap convergence | H100 PCIe 80GB (model 51.5% vs recycler 0.13%) |

**The model's `exp_floor` parameter is not a scrap floor. It is a functional demand floor.** The recycler scrap floor is 1-2 orders of magnitude below the model's asymptote for every GPU analyzed. The scrap research provides a valuable anchor for understanding what happens after the model's relevance window ends -- when secondary market demand evaporates and the only remaining value is in the weight of copper and gold.
