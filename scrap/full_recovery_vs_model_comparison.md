# Full Recovery Path vs. Depreciation Model: Comprehensive Comparison

**Date:** 2026-03-29
**Scope:** All recovery paths from 22 scrap reports vs. depreciation model projections from `depreciation_ranking.csv`

---

## 1. Master Comparison Table

MSRP values below use the depreciation model's `msrp_usd` field (which is the figure the model uses for ratio calculations). Where the MSRP verification found discrepancies, those are noted in the "MSRP Notes" column. The "Used Ratio" is the midpoint of the scrap report's working used price divided by the model's MSRP.

| GPU | Model MSRP | Used Price (Mar 2026) | Used Ratio | Model current_ratio | Model Yr5 | Model Yr10 | Broker Dead ($) | Broker Dead % MSRP | ForParts eBay ($) | GDDR6 Harvest ($) | Recycler ($) | Raw Scrap ($) | MSRP Notes |
|-----|-----------|----------------------|------------|--------------------:|----------:|-----------:|----------------:|-------------------:|------------------:|-------------------:|-------------:|--------------:|------------|
| T4 | $2,299 | $699-$1,100 | 0.39 | 0.261 | 0.352 | 0.231 | $70-$275 | 3-12% | $50-$150 | N/A (no GDDR6) | $3.50-$5 | $8-$9 | Verified $2,299 |
| V100 PCIe 16GB | $9,900 | $270-$430 | 0.04 | 0.033 | 0.181 | 0.049 | $27-$108 | 0.3-1.1% | $99-$500 | N/A (HBM) | $6-$8 | $13-$15 | |
| V100 PCIe 32GB | $11,458 | $770-$1,080 | 0.08 | 0.095 | 0.224 | 0.068 | $77-$270 | 0.7-2.4% | $99-$500 | N/A (HBM) | $6-$8 | $13-$15 | |
| V100 SXM2 16GB | $9,900 | $95-$400 | 0.03 | 0.030 | 0.181 | 0.048 | $10-$100 | 0.1-1.0% | $99-$500 | N/A (HBM) | $7-$8 | $13.40 | |
| V100 SXM2 32GB | $11,458 | $500-$900 | 0.06 | 0.059 | 0.186 | 0.054 | $50-$225 | 0.4-2.0% | $99-$500 | N/A (HBM) | $7-$8 | $13.40 | |
| V100S PCIe | $11,458 | $4,950-$9,300 | 0.62 | 0.087 | 0.193 | 0.061 | $495-$2,325 | 4.3-20.3% | $99-$500 | N/A (HBM) | $8-$9.35 | $15.58 | **Anomaly: see below** |
| A10 | $2,800 | $1,400-$1,800 | 0.57 | 0.666 | 0.672 | 0.411 | $140-$360 | 5.0-12.9% | N/A | $72-$120 (24 GDDR6) | $4-$7 | $10-$12 | Model uses $2,800 |
| A16 PCIe | $4,500 | $2,800-$4,300 | 0.79 | 0.578 | 0.582 | 0.419 | $280-$1,075 | 6.2-23.9% | N/A | $480 max (32x$15) | $16-$24 | $40 | |
| A30 PCIe | $4,500 | $2,600-$3,125 | 0.64 | 0.567 | 0.571 | 0.370 | $260-$780 | 5.8-17.3% | N/A | N/A (CoWoS/HBM) | $6-$9 | $14.48 | Model uses $4,500 |
| A40 | $5,000 | $5,000-$6,500 | 1.15 | 0.960 | 0.638 | 0.223 | $500-$1,625 | 10.0-32.5% | N/A | $72-$120 (24 GDDR6) | $6-$8 | $14 | Model: $5,000; OEM: $27,500 |
| A100 PCIe 40GB | $11,000 | $3,000-$5,500 | 0.39 | 0.536 | 0.604 | 0.382 | $450-$1,375 | 4.1-12.5% | N/A | N/A (CoWoS) | $6-$10 | $22 | |
| A100 PCIe 80GB | $13,000 | $5,000-$8,000 | 0.50 | 1.211 | 0.622 | 0.212 | $750-$2,000 | 5.8-15.4% | N/A | N/A (CoWoS) | $5-$9 | $19 | Model: $13,000 |
| A100 SXM4 80GB | $15,000 | $4,500-$7,000 | 0.38 | 0.294 | 0.277 | 0.159 | $675-$1,750 | 4.5-11.7% | N/A | N/A (CoWoS) | $11-$15 | $24 | Report: $10K (low); verified $15-20K |
| A100X | $17,500 | $8,000-$15,000 | 0.66 | 0.657 | 0.524 | 0.309 | $800-$2,250 | 4.6-12.9% | N/A | N/A (CoWoS) | $6-$11 | $16-$19 | Model uses $17,500 |
| L4 | $2,500 | $2,350 | 0.94 | 1.000 | 0.758 | 0.500 | $210-$650 | 8.4-26.0% | N/A | $36-$60 (12 GDDR6) | $0.50-$0.75 | $1.25 | |
| L40 | $7,500 | $6,350-$7,500 | 0.92 | 0.867 | 0.681 | 0.413 | $635-$1,875 | 8.5-25.0% | N/A | $72-$120 (24 GDDR6) | $4.50-$6.50 | $11 | Model: $7,500; OEM: $30-33K |
| L40S | $7,500 | $7,267-$9,000 | 1.08 | 0.987 | 0.663 | 0.407 | $727-$2,250 | 9.7-30.0% | N/A | $72-$120 (24 GDDR6) | $5-$8 | $13 | Model: $7,500; OEM: $39-52K |
| H100 PCIe 80GB | $25,599 | $18,000-$23,000 | 0.80 | 1.117 | 0.807 | 0.515 | $1,800-$5,750 | 7.0-22.5% | N/A | N/A (CoWoS) | $7-$13 | $15-$22 | |
| H100 SXM5 80GB | $30,000 | $9,600-$15,000 | 0.41 | 0.667 | 0.486 | 0.329 | $960-$3,750 | 3.2-12.5% | N/A | N/A (CoWoS) | $15-$32 | $37 | |
| H200 NVL | $32,000 | $31,000-$40,000 | 1.11 | 0.920 | 0.394 | 0.115 | $3,100-$10,000 | 9.7-31.3% | N/A | N/A (CoWoS) | $20-$29 | $49 | Model: $32K |
| H200 SXM | $35,000 | $18,000-$25,000 | 0.61 | 0.857 | 0.479 | 0.275 | $1,800-$6,250 | 5.1-17.9% | N/A | N/A (CoWoS) | $6-$8 | $14 | Verified: $38-44K; report $25K too low |
| GH200 | $35,000 | $5,500 | 0.16 | 0.157 | 0.187 | 0.054 | $550-$1,375 | 1.6-3.9% | N/A | N/A (CoWoS) | $5-$10 | $24 | |
| MI300X | $15,000 | $16,000-$18,000 | 1.13 | 2.230 | 0.237 | 0.069 | $1,600-$4,500 | 10.7-30.0% | N/A | N/A (3.5D/CoWoS) | $12-$19 | $30-$31 | |
| MI210 | $7,500 | $2,187-$4,640 | 0.46 | 0.584 | 0.532 | 0.314 | $220-$1,160 | 2.9-15.5% | N/A | N/A (CoWoS) | $7-$10 | $17-$18 | Model: $7,500 |
| Gaudi2 | $8,125 | $2,000 | 0.25 | -- | 0.239 | 0.069 | $200-$500 | 2.5-6.2% | N/A | N/A (CoWoS) | $11-$17 | $28.22 | |

---

## 2. Analysis: Model current_ratio vs. Observed Used Prices

### 2.1 Methodology

The "Used Ratio" is calculated as: midpoint(working used price range) / model MSRP. The "Model current_ratio" is the model's own estimate of current price / MSRP based on fitted/extrapolated depreciation curves.

### 2.2 Divergence Table

| GPU | Used Ratio (scrap reports) | Model current_ratio | Delta | Direction |
|-----|---------------------------:|--------------------:|------:|-----------|
| T4 | 0.39 | 0.261 | +0.13 | Model underestimates |
| V100 PCIe 16GB | 0.04 | 0.033 | +0.01 | Close |
| V100 SXM2 16GB | 0.03 | 0.030 | 0.00 | Close |
| V100 SXM2 32GB | 0.06 | 0.059 | 0.00 | Close |
| V100 PCIe 32GB | 0.08 | 0.095 | -0.01 | Close |
| **V100S PCIe** | **0.62** | **0.087** | **+0.53** | **Model severely underestimates** |
| A10 | 0.57 | 0.666 | -0.10 | Model slightly overestimates |
| A16 PCIe | 0.79 | 0.578 | +0.21 | Model underestimates |
| A30 PCIe | 0.64 | 0.567 | +0.07 | Close |
| A40 | 1.15 | 0.960 | +0.19 | Model underestimates |
| A100 PCIe 40GB | 0.39 | 0.536 | -0.15 | Model overestimates |
| A100 PCIe 80GB | 0.50 | 1.211 | -0.71 | Model severely overestimates (appreciating flag) |
| A100 SXM4 80GB | 0.38 | 0.294 | +0.09 | Close |
| A100X | 0.66 | 0.657 | 0.00 | Close |
| L4 | 0.94 | 1.000 | -0.06 | Close |
| L40 | 0.92 | 0.867 | +0.05 | Close |
| L40S | 1.08 | 0.987 | +0.09 | Close |
| H100 PCIe 80GB | 0.80 | 1.117 | -0.32 | Model overestimates (appreciating flag) |
| H100 SXM5 80GB | 0.41 | 0.667 | -0.26 | Model overestimates |
| H200 NVL | 1.11 | 0.920 | +0.19 | Model underestimates |
| H200 SXM | 0.61 | 0.857 | -0.25 | Model overestimates |
| GH200 | 0.16 | 0.157 | 0.00 | Close |
| MI300X | 1.13 | 2.230 | -1.10 | Model severely overestimates (shock flag) |
| MI210 | 0.46 | 0.584 | -0.12 | Model slightly overestimates |
| Gaudi2 | 0.25 | -- | -- | No current_ratio in model |

### 2.3 Summary of Divergence

**Close matches (delta < 0.10):** V100 PCIe 16/32GB, V100 SXM2 16/32GB, A30, A100 SXM4, A100X, L4, L40, L40S, GH200 -- 12 of 25 GPUs (48%).

**Model underestimates (used price higher than model thinks):**
- **V100S PCIe (+0.53):** The most extreme divergence. The model shows the V100S at 8.7% of MSRP, but IT Creations verified listings show $4,950-$9,300, implying 43-81% of MSRP. The V100S is a scarce 32GB-only variant with a premium over the standard V100. The model appears to be treating it like a generic V100 variant despite its distinct pricing trajectory.
- **A16 PCIe (+0.21):** The model underestimates by ~21 pp. The A16's unique quad-GPU VDI role creates niche demand the model does not capture.
- **T4 (+0.13), A40 (+0.19), H200 NVL (+0.19):** Moderate underestimates.

**Model overestimates (model projects higher than observed):**
- **MI300X (-1.10):** The model shows 2.23x MSRP (the shock/appreciating flag is set). The scrap reports show $16-18K used vs. $15K MSRP = ~1.13x. The model is capturing peak 2024-2025 AI bubble pricing that has since corrected.
- **A100 PCIe 80GB (-0.71):** Also flagged as appreciating. Model's 1.21x vs. real ~0.50x. Similar AI bubble distortion.
- **H100 PCIe 80GB (-0.32), H100 SXM5 80GB (-0.26), H200 SXM (-0.25):** The model overstates current ratios for these H-series GPUs, likely due to lag in incorporating recent price declines as Blackwell supply ramps.

### 2.4 Interpretation

The model tracks used prices well for older GPUs with stable secondary markets (V100 series, A100 SXM4, GH200). It diverges most for:
1. GPUs with recent price volatility (MI300X, A100 PCIe 80GB) where the "appreciating" flag distorts the curve.
2. Scarce variants where the model uses a generic segment curve (V100S).
3. Recent-gen GPUs where AI bubble pricing is unwinding (H100, H200).

---

## 3. Broker/ITAD Floor -- When Does the Model Reach It?

The broker pays 10-25% of the **working used price**, not MSRP. As the working used price drops, the broker floor drops in absolute terms but may remain a fixed percentage of MSRP for a while. Let's express the broker floor as a % of MSRP and find when the model crosses it.

### 3.1 Broker Floor as % of MSRP

| GPU | Broker Range ($) | Broker Low % MSRP | Broker High % MSRP | Model Yr5 | Model Yr10 | Yr10 Above Broker Low? |
|-----|----------------:|------------------:|-------------------:|----------:|-----------:|:----------------------:|
| T4 | $70-$275 | 3.0% | 12.0% | 35.2% | 23.1% | YES (by 20 pp) |
| V100 PCIe 16GB | $27-$108 | 0.3% | 1.1% | 18.1% | 4.9% | YES (by 4.6 pp) |
| V100 SXM2 16GB | $10-$100 | 0.1% | 1.0% | 18.1% | 4.8% | YES (by 4.7 pp) |
| V100S PCIe | $495-$2,325 | 4.3% | 20.3% | 19.3% | 6.1% | YES (by 1.8 pp) |
| A10 | $140-$360 | 5.0% | 12.9% | 67.2% | 41.1% | YES (by 36 pp) |
| A16 PCIe | $280-$1,075 | 6.2% | 23.9% | 58.2% | 41.9% | YES (by 36 pp) |
| A30 PCIe | $260-$780 | 5.8% | 17.3% | 57.1% | 37.0% | YES (by 31 pp) |
| A40 | $500-$1,625 | 10.0% | 32.5% | 63.8% | 22.3% | YES (by 12 pp) |
| A100 PCIe 40GB | $450-$1,375 | 4.1% | 12.5% | 60.4% | 38.2% | YES (by 34 pp) |
| A100 SXM4 80GB | $675-$1,750 | 4.5% | 11.7% | 27.7% | 15.9% | YES (by 11 pp) |
| A100X | $800-$2,250 | 4.6% | 12.9% | 52.4% | 30.9% | YES (by 26 pp) |
| L4 | $210-$650 | 8.4% | 26.0% | 75.8% | 50.0% | YES (by 42 pp) |
| L40 | $635-$1,875 | 8.5% | 25.0% | 68.1% | 41.3% | YES (by 33 pp) |
| L40S | $727-$2,250 | 9.7% | 30.0% | 66.3% | 40.7% | YES (by 31 pp) |
| H100 PCIe 80GB | $1,800-$5,750 | 7.0% | 22.5% | 80.7% | 51.5% | YES (by 44 pp) |
| H100 SXM5 80GB | $960-$3,750 | 3.2% | 12.5% | 48.6% | 32.9% | YES (by 30 pp) |
| H200 NVL | $3,100-$10,000 | 9.7% | 31.3% | 39.4% | 11.5% | YES (by 1.8 pp) |
| H200 SXM | $1,800-$6,250 | 5.1% | 17.9% | 47.9% | 27.5% | YES (by 22 pp) |
| GH200 | $550-$1,375 | 1.6% | 3.9% | 18.7% | 5.4% | YES (by 3.8 pp) |
| MI300X | $1,600-$4,500 | 10.7% | 30.0% | 23.7% | 6.9% | NO -- Yr10 below broker high |
| MI210 | $220-$1,160 | 2.9% | 15.5% | 53.2% | 31.4% | YES (by 28 pp) |
| Gaudi2 | $200-$500 | 2.5% | 6.2% | 23.9% | 6.9% | YES (by 4.4 pp) |

### 3.2 Key Findings

**No GPU's model Yr10 projection falls below the broker floor low-end.** Every card's 10-year projected value remains above the minimum broker offer as a % of MSRP.

**Four GPUs are within 5 pp of the broker low-end at Yr10:**
- V100S PCIe: Yr10 6.1% vs. broker low 4.3% (gap: 1.8 pp)
- H200 NVL: Yr10 11.5% vs. broker low 9.7% (gap: 1.8 pp)
- GH200: Yr10 5.4% vs. broker low 1.6% (gap: 3.8 pp)
- V100 PCIe 16GB: Yr10 4.9% vs. broker low 0.3% (gap: 4.6 pp)

**However, the broker floor itself is dynamic.** As the working used price drops, so does the broker payout. By year 10, the used price will be lower, meaning the broker floor (10-25% of the then-lower used price) will also be lower. The model's Yr10 projection already IS the used price at year 10, so the relevant comparison is whether the Yr10 model projection is consistent with there being any functional demand (which determines whether a broker can sell it).

**The real question is: at what model ratio does a card transition from "sellable working" to "sell to broker/for parts"?** Based on the data:
- V100 SXM2 16GB at current_ratio = 0.030 ($300 on a $9,900 MSRP) -- still has working demand
- T4 at current_ratio = 0.261 ($600 on a $2,299 MSRP) -- still has working demand
- "For parts" replaces "working" when the working price drops below ~$100-$200

**Estimated transition ratios (working -> broker/for-parts):**
- High-MSRP cards (>$10K MSRP): ratio < 0.01-0.02 ($100-$200 working)
- Mid-MSRP cards ($2-10K MSRP): ratio < 0.04-0.10 ($100-$200 working)
- This transition does not happen within the model's 10-year window for any GPU except possibly V100 SXM2 16GB.

---

## 4. The "For Parts" Floor

### 4.1 Where It Exists

"For parts" eBay sales are a real, observable recovery path for older cards:

| GPU | Age (years) | Working Used | "For Parts" eBay | For-Parts as % Working | For-Parts as % MSRP |
|-----|------------|-------------|----------------:|----------------------:|--------------------:|
| T4 | 6.5 | $699-$1,100 | $50-$150 | 7-14% | 2.2-6.5% |
| V100 PCIe | 8-9 | $270-$1,080 | $99-$500 | 37-46% | 1.0-5.1% |
| V100 SXM2 | 8-9 | $95-$900 | $99-$500 | 56-104% | 1.0-5.1% |
| V100S PCIe | 6-7 | $4,950-$9,300 | $99-$500 | 2-5% | 0.9-4.4% |

**For the V100 SXM2 16GB, "for parts" prices ($99-$500) overlap with or exceed working unit prices ($95-$400).** This is a sign that the card has effectively reached the transition point where untested/for-parts and working units trade at nearly the same price, because the cost of testing and verifying exceeds the value premium.

### 4.2 Comparison to Model Terminal Values

| GPU | Model Yr10 (% MSRP) | Model Yr10 ($) | "For Parts" Midpoint ($) | For-Parts > Yr10? |
|-----|--------------------:|--------------:|-------------------------:|:-----------------:|
| T4 | 23.1% | $531 | $100 | NO -- model well above |
| V100 PCIe 16GB | 4.9% | $485 | $300 | NO -- close |
| V100 SXM2 16GB | 4.8% | $475 | $300 | NO -- close |
| V100S PCIe | 6.1% | $699 | $300 | NO -- model above |

The model's 10-year projections remain above "for parts" prices for all cards. However, for the V100 variants, the gap is small (model: $475-$699 vs. "for parts": $100-$500). By year 12-14, the model's extrapolation would likely converge with "for parts" pricing.

### 4.3 "For Parts" as a Price Floor

The "for parts" market provides a floor above recycler scrap that persists as long as:
1. Repair shops exist that can fix and resell the card
2. The card has a compatible installed base (driver support, system compatibility)
3. The absolute dollar value of the working card exceeds ~$100-$200 (repair economics threshold)

When condition 3 fails, "for parts" demand collapses to zero and the recycler floor ($3-$32) applies. The V100 SXM2 16GB is closest to this threshold now.

---

## 5. GDDR6 Harvesting Floor

### 5.1 Which Cards Have a GDDR6 Harvesting Floor?

Only non-CoWoS cards with standard BGA-packaged GDDR6 chips are candidates. CoWoS cards (A100, H100, H200, A30, MI300X, MI210, Gaudi2, GH200) have HBM that cannot be practically removed.

| GPU | GDDR6 Chips | Harvest Value ($) | As % of MSRP | Model Yr10 ($) | Model Yr10 % | Harvest > Recycler? |
|-----|------------:|------------------:|-------------:|--------------:|-------------:|:-------------------:|
| A10 | 24 | $72-$120 | 2.6-4.3% | $1,151 | 41.1% | YES (18-24x recycler) |
| A16 PCIe | 32 | $96-$480 | 2.1-10.7% | $1,886 | 41.9% | YES (4-20x recycler) |
| A40 | 24 | $72-$120 | 1.4-2.4% | $1,114 | 22.3% | YES (9-15x recycler) |
| L4 | 12 | $36-$60 | 1.4-2.4% | $1,250 | 50.0% | YES (48-80x recycler) |
| L40 | 24 | $72-$120 | 1.0-1.6% | $3,099 | 41.3% | YES (11-18x recycler) |
| L40S | 24 | $72-$120 | 1.0-1.6% | $3,050 | 40.7% | YES (9-15x recycler) |

**The A16 is the standout case.** With 32 GDDR6 chips (4 GPUs x 8 chips each), the A16's GDDR6 harvesting value of $96-$480 creates a hard floor that is 4-20x above the recycler payout ($16-$24). At $15/chip for intact Samsung K4ZAF325BM-HC14 chips, the theoretical ceiling is $480.

### 5.2 Does the Model Account for This?

**No.** The model's `exp_floor` parameter is a mathematical fitting artifact. For all GDDR6 cards, the model's Yr10 projection is far above the GDDR6 harvesting value, so the floor is not binding within the 10-year window. However, at extremely long time horizons (>15 years), the GDDR6 floor would become relevant:

- A16: Model would need to decline to $480 / $4,500 = 10.7% before GDDR6 harvesting becomes the floor. The model projects 41.9% at Yr10, so this would occur around year 15-18 under the model's extrapolation.
- A10: $120 / $2,800 = 4.3% floor. Model at 41.1% at Yr10. GDDR6 floor becomes binding around year 18-20.

**Recommendation:** The model should include a GDDR6 component floor for non-CoWoS cards, but it would only matter for projections beyond 15 years. Within the 10-year window, it is not a binding constraint.

### 5.3 GDDR6 Floor vs. Broker Floor

In all cases, the broker floor (10-25% of working used) exceeds the GDDR6 harvesting value. The GDDR6 harvesting path only becomes optimal when:
- The card is physically dead (no broker will take it)
- AND the failure is non-repairable (no "for parts" demand)
- AND someone has BGA rework equipment and labor available

This is a narrow scenario. In practice, broker > for-parts > GDDR6 harvest > recycler.

---

## 6. Optimal Recovery Path by Depreciation Stage

### 6.1 Lifecycle Map

| Stage | Model Ratio | Age (typical) | Optimal Path | Expected Recovery |
|-------|------------|--------------|--------------|-------------------|
| New/Appreciating | >1.0 | 0-1 yr | Sell working | 100-230% MSRP |
| Early depreciation | 0.50-1.0 | 1-3 yr | Sell working | 50-100% MSRP |
| Mid depreciation | 0.20-0.50 | 3-7 yr | Sell working (reduced) | 20-50% MSRP |
| Late depreciation | 0.05-0.20 | 7-10 yr | Sell working if possible; broker/for-parts as backup | 5-20% MSRP |
| Near-terminal | 0.02-0.05 | 10-15 yr | "For parts" eBay or broker | 1-5% MSRP |
| Terminal | <0.02 | 15+ yr | Recycler (only if all demand collapses) | 0.02-0.5% MSRP |
| Physical end-of-life | N/A | 15-20+ yr | E-waste recycler | $3-$92 per card |

### 6.2 Current Status of Each GPU

| GPU | Current Stage | Optimal Path Now | Next Transition (est.) |
|-----|--------------|------------------|----------------------|
| T4 | Mid depreciation (0.26) | Sell working | "For parts" in 3-5 yrs |
| V100 PCIe 16GB | Late depreciation (0.03) | "For parts" eBay now | Recycler in 3-5 yrs |
| V100 SXM2 16GB | Late depreciation (0.03) | "For parts" eBay now | Recycler in 2-4 yrs |
| V100S PCIe | Mid depreciation (0.62) | Sell working | Late depreciation in 3-5 yrs |
| A10 | Mid depreciation (0.57-0.67) | Sell working | Late in 5-8 yrs |
| A16 PCIe | Mid depreciation (0.58-0.79) | Sell working | Late in 5-8 yrs |
| A30 PCIe | Mid depreciation (0.57-0.64) | Sell working | Late in 5-8 yrs |
| A40 | Early/Mid depreciation (0.96-1.15) | Sell working | Mid in 3-5 yrs |
| A100 PCIe 40/80GB | Mid depreciation (0.39-0.54) | Sell working | Late in 5-7 yrs |
| A100 SXM4 80GB | Mid depreciation (0.29-0.38) | Sell working | Late in 5-7 yrs |
| L4 | New (0.94-1.00) | Sell working | Mid in 3-5 yrs |
| L40/L40S | Early depreciation (0.87-1.08) | Sell working | Mid in 3-5 yrs |
| H100 PCIe 80GB | Early depreciation (0.80-1.12) | Sell working | Mid in 2-4 yrs |
| H100 SXM5 80GB | Mid depreciation (0.41-0.67) | Sell working | Late in 5-7 yrs |
| H200 NVL | New (0.92-1.11) | Sell working | Mid in 2-4 yrs |
| H200 SXM | Mid depreciation (0.61-0.86) | Sell working | Late in 4-6 yrs |
| GH200 | Late depreciation (0.16) | Sell working (barely) | "For parts"/broker in 1-3 yrs |
| MI300X | Early depreciation (1.13-2.23) | Sell working | Mid in 2-4 yrs |
| MI210 | Mid depreciation (0.46-0.58) | Sell working | Late in 5-8 yrs |
| Gaudi2 | Near-terminal (0.25) | Sell working; broker backup | Recycler in 2-4 yrs |

### 6.3 Ecosystem-Collapse Risk

Two GPUs face near-term ecosystem collapse:
1. **Gaudi2 HL-225H:** Intel's strategic pivot away from Gaudi means the software ecosystem may die within 2-3 years. When this happens, working units will rapidly lose value and brokers may refuse the card entirely. The recycler floor ($11-$17) could become the only option sooner than the model projects.
2. **GH200:** Already trading at 16% of MSRP after less than 3 years. The Grace ARM CPU adds value via NVIDIA ecosystem support, but the module is too large/hot for most secondary applications. Broker demand will thin rapidly.

---

## 7. Model Confidence Intervals vs. Recovery Path Values

### 7.1 CI Lower Bounds at Key Time Points

The model provides `ci_lo_t60` (5-year CI lower bound) and `ci_lo_t120` (10-year CI lower bound). Let's compare these to recovery floor values.

| GPU | ci_lo Yr5 ($) | ci_lo Yr10 ($) | Broker Low ($) | For-Parts ($) | Recycler ($) | ci_lo Yr10 < Broker? | ci_lo Yr10 < Recycler? |
|-----|-------------:|--------------:|---------------:|--------------:|-------------:|:--------------------:|:---------------------:|
| T4 | $273 | $21 | $70 | $50 | $4 | YES | NO |
| V100 PCIe 16GB | $596 | $30 | $27 | $99 | $7 | YES | NO |
| V100 SXM2 16GB | $587 | $33 | $10 | $99 | $7 | NO | NO |
| V100 SXM2 32GB | $639 | $37 | $50 | $99 | $7 | YES | NO |
| V100S PCIe | $639 | $36 | $495 | $99 | $9 | YES | NO |
| A10 | $571 | $33 | $140 | -- | $6 | YES | NO |
| A16 PCIe | $982 | $318 | $280 | -- | $20 | NO | NO |
| A30 PCIe | $798 | $56 | $260 | -- | $8 | YES | NO |
| A40 | $900 | $51 | $500 | -- | $7 | YES | NO |
| A100 PCIe 40GB | $1,927 | $150 | $450 | -- | $8 | YES | NO |
| A100 PCIe 80GB | $2,400 | $102 | $750 | -- | $7 | YES | NO |
| A100 SXM4 80GB | $1,204 | $49 | $675 | -- | $13 | YES | NO |
| A100X | $2,570 | $128 | $800 | -- | $9 | YES | NO |
| L4 | $510 | $26 | $210 | -- | $1 | YES | NO |
| L40 | $1,425 | $53 | $635 | -- | $6 | YES | NO |
| L40S | $1,320 | $60 | $727 | -- | $7 | YES | NO |
| H100 PCIe 80GB | $5,796 | $257 | $1,800 | -- | $10 | YES | NO |
| H100 SXM5 80GB | $4,333 | $218 | $960 | -- | $24 | YES | NO |
| H200 NVL | $4,482 | $572 | $3,100 | -- | $25 | YES | NO |
| H200 SXM | $4,475 | $186 | $1,800 | -- | $7 | YES | NO |
| GH200 | $2,130 | $278 | $550 | -- | $8 | YES | NO |
| MI300X | $1,143 | $213 | $1,600 | -- | $16 | YES | NO |
| MI210 | $1,152 | $65 | $220 | -- | $9 | YES | NO |
| Gaudi2 | $667 | $99 | $200 | -- | $14 | YES | NO |

### 7.2 Findings

**CI lower bounds at Year 10 fall below the broker floor for 22 of 24 GPUs (92%).** Only V100 SXM2 16GB and A16 PCIe have Yr10 CI lower bounds that remain above the broker low-end.

**No CI lower bound falls below the recycler floor.** Even in the model's worst-case scenario (CI lower), the projected value never reaches the physical scrap floor. This makes sense -- the recycler floor ($1-$32) represents a catastrophic collapse scenario that falls outside the model's statistical framework.

**The CI lower bounds are not useful as practical floor values.** They represent a statistical lower envelope of the model's uncertainty about the *depreciation rate*, not about the economic floor. The broker/for-parts floor provides a more meaningful lower bound for practical planning.

### 7.3 Probability Analysis

The model provides `p_below_10pct` (probability of falling below 10% at Yr5), `p_below_10_8yr` (Yr8), and `p_below_10_10yr` (Yr10). Comparing against recovery path transitions:

| GPU | P(below 10%) at Yr5 | P(below 10%) at Yr10 | Broker enters picture at ~10% | Implication |
|-----|--------------------:|---------------------:|:----------------------------:|-------------|
| GH200 | 6.9% | 80.8% | YES | 81% chance of needing broker by Yr10 |
| V100 PCIe 16GB | 8.9% | 81.6% | YES | 82% chance |
| V100 SXM2 16GB | 8.8% | 82.4% | YES | 82% chance |
| V100 SXM2 32GB | 8.5% | 79.3% | YES | 79% chance |
| V100S PCIe | 8.8% | 71.5% | YES | 72% chance |
| Gaudi2 | 2.0% | 69.9% | YES | 70% chance |
| MI300X | 2.1% | 70.6% | YES | 71% chance |
| T4 | 0.9% | 11.4% | NO | Low probability |
| A10 | 0.03% | 7.6% | NO | Very low |
| H100 SXM5 80GB | 0.2% | 9.5% | NO | Low |
| H200 NVL | 0.1% | 42.0% | Approaching | Moderate |

The V100 series, GH200, Gaudi2, and MI300X all have >70% probability of falling below 10% of MSRP by year 10, which is the threshold at which broker/for-parts paths become the primary recovery mechanism. The model's probability framework correctly identifies these as high-risk for terminal value collapse.

---

## 8. GPUs Where the Scrap Research Suggests the Model May Be Wrong

### 8.1 Model Too Optimistic (projects above where cards actually trade)

| GPU | Issue | Model Says | Reality Says | Magnitude |
|-----|-------|-----------|-------------|-----------|
| **MI300X** | Shock/appreciating flag distorts projection | current_ratio = 2.23 | Used price = 1.07-1.20x MSRP | **~1.0x overstatement** |
| **A100 PCIe 80GB** | Appreciating flag; stale peak pricing | current_ratio = 1.21 | Used price = 0.38-0.62x MSRP | **~0.6-0.8x overstatement** |
| **H100 PCIe 80GB** | Current ratio inflated | current_ratio = 1.12 | Used price = 0.70-0.90x MSRP | **~0.2-0.4x overstatement** |
| **H100 SXM5 80GB** | Current ratio too high | current_ratio = 0.67 | Used price = 0.32-0.50x MSRP | **~0.2-0.3x overstatement** |
| **H200 SXM** | MSRP underestimated ($25K vs. verified $38-44K) | Yr10 = 0.275 at $25K MSRP | Real Yr10 would be much lower at correct $40K MSRP | **MSRP error propagates** |
| **A40** | MSRP in model ($5K) vs. OEM MSRP ($27.5K) | Yr10 = 22.3% of $5K | At correct $27.5K MSRP, Yr10 is 4.1% | **MSRP basis matters** |

The A40, L40, and L40S present a special case: the depreciation model uses market-adjusted MSRPs that are dramatically lower than OEM list prices (A40: $5K vs. $27.5K; L40: $7.5K vs. $30K; L40S: $7.5K vs. $39-52K). If the model's ratios are interpreted against OEM MSRPs, the Yr10 projections translate to much lower absolute dollar values.

### 8.2 Model Too Pessimistic (projects below real floor values)

| GPU | Issue | Model Says | Reality Says | Magnitude |
|-----|-------|-----------|-------------|-----------|
| **V100S PCIe** | Model shows 8.7% current ratio; actual is 43-81% | Yr10 = $699 | V100S scarcity sustains $1,000+ used prices | **Model underestimates by 5-10x** |
| **A16 PCIe** | Unique quad-GPU VDI niche not captured | Yr10 = $1,886 | GDDR6 harvest alone = $480 hard floor | Model OK, but floor higher than model assumes |
| **T4** | Large installed base sustains demand | Yr10 = $531 | Even as inference card, $200+ likely | Model probably OK |

The V100S PCIe is the most significant case. The model treats it like a generic V100 variant, but the V100S is a scarce 32GB-only, higher-clocked refresh with verified used prices of $4,950-$9,300 (43-81% of MSRP). The model projects 6.1% at Yr10, but the V100S's scarcity premium may sustain prices well above this.

### 8.3 GPUs Where the Model and Scrap Research Agree

| GPU | Assessment |
|-----|-----------|
| V100 PCIe 16/32GB | Model current_ratio matches reality closely. Yr10 projections (4.9-6.8%) are plausible given the "for parts" floor. |
| V100 SXM2 16/32GB | Close match. The "for parts" floor ($99-$500) provides a real safety net above the model's Yr10 projection. |
| A100 SXM4 80GB | Model (0.294) vs. reality (0.38) -- reasonable agreement. |
| L4 | Model (1.00) vs. reality (0.94) -- close. Model's Yr10 of 50% seems optimistic for a low-TDP inference card. |
| GH200 | Model (0.157) matches the scrap report's ~$5,500 working price closely. Yr10 at 5.4% ($1,890) is plausible. |

---

## 9. Summary Findings

### 9.1 The Recovery Path Hierarchy

At every stage of depreciation, the optimal recovery path follows this hierarchy:

```
1. Sell working (highest value, 20-120% MSRP)
    |
    v
2. Sell to broker/ITAD (10-25% of working price, ~3-30% MSRP)
    |
    v
3. Sell "for parts" on eBay (for old cards with repair demand, ~1-5% MSRP)
    |
    v
4. GDDR6 chip harvesting (non-CoWoS cards only, ~1-10% MSRP)
    |
    v
5. Recycler e-waste (absolute floor, 0.02-0.5% MSRP, $1-$32)
```

The model's projections live in tiers 1-2 for its entire 10-year window. The scrap research tiers 3-5 only become relevant beyond the model's time horizon.

### 9.2 How Well the Model Matches Reality

- **48% of GPUs** have current_ratio within 0.10 of observed used prices (good match)
- **24% of GPUs** have the model overstating current value (typically due to appreciating/shock flags or stale peak pricing)
- **28% of GPUs** have the model understating current value (V100S, A16, T4, A40, H200 NVL)

### 9.3 The Model's Blind Spots

1. **Scarcity premiums:** The V100S PCIe's pricing anomaly shows the model cannot capture supply-constrained niche products.
2. **Ecosystem collapse:** The Gaudi2's Intel pivot risk and the GH200's rapid decline are not captured by the smooth exponential decay.
3. **MSRP ambiguity:** The A40, L40, and L40S have model MSRPs that differ by 4-7x from OEM list prices, making ratio comparisons misleading.
4. **Stale peak pricing:** The MI300X and A100 80GB PCIe have appreciating flags based on 2024-2025 AI bubble pricing that has since corrected.

### 9.4 What the Scrap Research Adds

The scrap research provides three practical value anchors that the model lacks:

1. **Broker floor ($70-$10,000):** A real, transaction-based floor for dead-but-intact cards. The model's CI lower bounds often fall below this, suggesting the model's uncertainty bands are too wide on the downside.
2. **GDDR6 harvesting floor ($36-$480):** A component-level floor for non-CoWoS cards that is 4-80x above the recycler floor. The model has no mechanism to represent this.
3. **Recycler floor ($1-$32):** The absolute physical floor that only applies when ALL functional demand has collapsed. The model never reaches this level, which is correct for the 10-year window but misleading for longer horizons.

### 9.5 Actionable Conclusions

1. **For 5-year projections:** The model is generally reliable. The scrap research is irrelevant -- all recovery paths are dominated by "sell working."
2. **For 10-year projections:** The model is reasonable but should incorporate the broker floor as a sanity check. Four GPUs (V100 variants, GH200, Gaudi2) are approaching broker territory.
3. **For projections beyond 10 years:** The model needs structural changes (ecosystem collapse sigmoid, GDDR6 component floor, scrap floor parameter) to be meaningful. The exponential decay to `exp_floor` is not a realistic terminal value model.
4. **For MSRP-sensitive analysis:** The A40, L40, L40S, A100 SXM4, and H200 SXM should have their MSRPs corrected or flagged, as the model's ratios are misleading when compared against external reference prices.
