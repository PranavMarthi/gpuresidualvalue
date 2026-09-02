# NVIDIA H200 SXM (141GB HBM3e) -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** SXM5
**TDP:** 700W
**MSRP:** $25,000 | **Used (Mar 2026):** $18,000-$25,000

---

## 1. Card Overview

The NVIDIA H200 SXM is a Hopper-generation datacenter accelerator with 141GB of HBM3e memory, designed for large-scale AI training and inference in liquid-cooled DGX/HGX chassis. It shares the GH100 die with the H100 but upgrades the memory subsystem from HBM3 to HBM3e.

| Attribute | Value |
|-----------|-------|
| GPU die | GH100 (TSMC 4N) |
| Die area | 814 mm2 |
| Transistors | 80 billion |
| Memory | 141 GB HBM3e (6 x ~24 GB, 8-Hi stacks) |
| Memory bus | 6144-bit |
| Interconnect | NVLink 4.0, 18 links, 900 GB/s bidirectional |
| TDP | 700 W |
| Board weight | ~640 g bare module (bottom-up engineering estimate, range 550--750 g; no published spec -- see weight_engineering.md) |
| Packaging | CoWoS-S, ~2,831 mm2 silicon interposer (TSMC 65nm) |

---

## 2. Weight Breakdown

*Revised 2026-03-29 via bottom-up engineering estimate (see `weight_engineering.md`). The prior 1,020 g estimate was an artifact of subtracting an uncertain heatsink weight from the overstated Omdia "3 kg" figure, which produced a 516 g (51%) "Other" residual -- physically implausible for solder, TIM, and passives on a module this size.*

| Component | Weight (g) | % of Total | Method |
|-----------|-----------|-----------|--------|
| Heatspreader / IHS (nickel-plated copper, full board coverage) | 200 | 31.3% | Estimated from ~100x110 mm footprint, ~4 mm effective Cu at 60% fill |
| VRM (32 inductors + 61 DrMOS + caps + controllers) | 190 | 29.7% | 32 inductors x 3.5 g + 61 DrMOS x 0.4 g + ~50 g caps + 2 g controllers |
| PCB (FR-4 module board, ~20 layers) | 95 | 14.8% | FR-4 + Cu planes, ~100x110 mm, density calc |
| GPU package assembly (die + interposer + substrate + underfill + BGA) | 68 | 10.6% | CoWoS-S 55x55 mm package without HBM |
| Memory (6 x HBM3e 8-Hi stacks) | 17 | 2.7% | 6 x 2.8 g |
| SXM5 connector + stiffener ring | 50 | 7.8% | Connector ~20 g + stiffener ~30 g |
| Passives, misc ICs, solder, TIM | 20 | 3.1% | ~100 resistors, support ICs, solder paste, 3 g indium TIM |
| **Total** | **~640** | **100%** | **Bottom-up sum (range 550--750 g)** |

Cross-checks: (1) HGX 24 kg back-calc yields ~660 g bare; (2) A100 SXM4 325 g scaled by 1.75x VRM yields ~600--700 g; (3) H100 PCIe 1,200 g minus heatsink/bracket, area-adjusted, yields ~550--700 g; (4) DGX H100 and DGX H200 weigh identically (287.6 lbs), confirming physical interchangeability; (5) Dell XE9680 A100-to-H100 delta (~375 g/module with heatsink) is consistent with VRM scaling. See `weight_investigation.md` for full web research and `weight_engineering.md` for bottom-up calculation.

---

## 3. Component Breakdown

### GPU Die
- GH100, 814 mm2, 80B transistors, TSMC 4N
- Secondary market: $500-$800 (reballing/rework candidate for repair)
- Raw scrap: $0.15 (silicon at ~$100/kg)

### Memory
- 6 x ~24 GB 8-Hi HBM3e stacks (SK Hynix or Micron), 11 mm x 11 mm footprint each
- Secondary market: $1,800-$2,520 total ($300-$420/stack, 2026 pricing with ~20% hike)
- Raw scrap: $0.18 (6 stacks x 2.8 g = 16.8 g at $11/kg bulk IC scrap rate)

### Heatspreader / IHS
- Nickel-plated copper heat spreader covering full module area (~100x110 mm)
- 200 g (31.3% of module) -- revised from 80 g; photos of SXM5 modules show a full-board-coverage copper surface, not just a 55 mm package lid
- Secondary market: negligible (proprietary form factor)
- Raw scrap: $2.60 (200 g Cu at $13/kg)

### VRM / Power Delivery
- 32 inductors (29 dual-stage + 3 single-stage) and 61 DrMOS power stages total
- 190 g total (29.7% of module): inductors 112 g, DrMOS 24 g, caps ~50 g, controllers ~2 g
- Secondary market: negligible (bulk e-waste)
- Raw scrap: $2.97 (copper in inductors $0.38 + ferrite $2.34 + MOSFETs $0.25)

### PCB
- ~20-layer FR-4 module board, ~100x110 mm (SXM5 module form factor, NOT a full-length PCIe card)
- 95 g (14.8% of module), Cu content ~54 g (heavy power planes for 700W delivery)
- Secondary market: negligible (proprietary SXM form factor)
- Raw scrap: $1.24 (95 g at bulk e-scrap board rate ~$13/kg)

### Connectors + Stiffener
- SXM5 proprietary high-pin-count connector (~20 g), silver-plated copper pins (3.81 um Ag)
- Stiffener ring / frame (~30 g, stainless steel or nickel alloy)
- 50 g combined (7.8% of module)
- Secondary market: negligible (no standalone market)
- Raw scrap: $0.37 (~0.1 g Ag = $0.23, plus copper content $0.05, stiffener $0.09)

### Passives, Misc ICs, Solder, TIM
- 20 g (3.1% of module): TIM (indium-based solder, ~3 g), ~100 resistors (~2 g), support ICs (~5 g), solder paste (~5 g), labels/adhesive (~3 g), underfill (~2 g)
- Note: solder balls (BGA) and stiffener ring are now accounted for in the GPU package assembly and connector lines respectively
- Raw scrap: $2.50 (indium $1.86 at $0.62/g SMM industrial benchmark -- corrected from $2.92 at retail $0.97/g; solder $0.48, stiffener $0.09, passives $0.05, micro-bumps $0.03)

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.01-0.04 | $145/g | $1.45-$5.80 | ENIG on substrate pads + module board pads. Engineering calculation: substrate ENIG ~0.003 g, module board ENIG ~0.004 g, support ICs <0.001 g. SXM5 connector is silver-plated, not gold. No PCIe gold fingers. Mid-estimate ~0.01 g. |
| Silver (Ag) | 0.46 | $2.25/g | $1.04 | 0.36 g in SAC305 BGA solder (3% Ag) + 0.1 g on SXM5 connector |
| Palladium (Pd) | 0.005 | $45/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.03g. |
| **Total** | | | **$2.72-$7.07** | Mid-estimate ~$2.72 using 0.01 g Au |

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $25,000 | 100% |
| Component salvage (theoretical max) | $2,500 | 10% |
| Component salvage (realistic) | $1,000 | 4% |
| Raw material scrap (gross, revised) | ~$14 | 0.06% |
| Recycler payout (net, what you'd receive) | $6-$8 | 0.03% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **HBM3e stack dimensions (WRONG):** Summary claimed 7.75 mm x 11.87 mm (JEDEC HBM2 footprint). Correct HBM3e dimensions are 11 mm x 11 mm per Micron product brief. Severity: medium (does not affect scrap value directly, but factually wrong).
- **Module weight (REVISED):** Original 1,020 g was derived by subtracting an assumed heatsink weight from the overstated Omdia "3 kg" figure. Bottom-up engineering estimate (see `weight_engineering.md`) yields **~640 g** (range 550--750 g), cross-checked three ways: HGX 24 kg back-calc (~660 g), A100 SXM4 scaling (~600--700 g), H100 PCIe area adjustment (~550--700 g). The prior 51% "Other" residual was the telltale sign of a bad top-down estimate. Confidence: 50/100 (improved from 45, but still no published spec).
- **GPU die weight (UNCERTAIN):** 1.47 g assumes full wafer thickness (0.775 mm). After backgrind for CoWoS, die may be thinned to 50-100 um, reducing weight to ~0.1-0.2 g. Interposer is at near-full thickness.
- **Missing minor components:** VRM controller ICs, EEPROMs, temperature sensors, ESD protection not itemized. Impact on scrap estimate: <$1.

### Pricing Issues
- **Substrate copper scrap $3.40 (WRONG -- unit error):** 3.4 g Cu at $13/kg = $0.04, not $3.40. Grams misread as dollars. Overstatement: $3.36.
- **HBM scrap rate $1.85 per line (WRONG -- inconsistent):** At the cited $11/kg IC rate, 6 stacks at 2.8 g each = 16.8 g = $0.18 total, not $1.85. Overstatement: $1.67.
- **Silver spot price (WRONG):** Claimed $80.28/oz ($2.58/g), actual late-March 2026 price ~$70/oz ($2.25/g). ~15% overstated. Impact: $0.15.
- **Palladium spot price (WRONG):** Claimed $1,621/oz ($52.12/g), actual ~$1,405/oz ($45/g). ~15% overstated. Impact: $0.21.
- **Indium price [CORRECTED]:** Original cited $972/kg from retail source (strategicmetalsinvest.com). Corrected to $618/kg ($0.62/g) per SMM China 4N+ industrial benchmark (Mar 2026). Indium TIM value reduced from $2.92 to $1.86 (-$1.06). See indium_price_analysis.md.
- **Gold quantity (UNCERTAIN):** 0.05 g is plausible upper bound. ENIG calculation alone yields ~0.005-0.01 g. Mid-estimate 0.02 g is more defensible. Impact: $4.15 at upper bound.
- **Solder silver value (internally inconsistent):** SAC305 solder line shows $0.48 total scrap but contains 0.36 g Ag worth $0.81 at $2.25/g. The $0.48 appears to be a bulk solder scrap rate, not a precious-metal-extracted rate.

### Deep Investigation (2026-03-29)

Cross-referenced with H200 NVL deep investigation (see `../H200_NVL/deep_investigation.md`). Key findings for SXM variant:

| # | Unknown | Resolution | Impact |
|---|---------|-----------|--------|
| 1 | Module weight (~1,020 g) | **Revised to ~640 g** via bottom-up engineering estimate (see `weight_engineering.md`). Three cross-checks converge on 550--750 g. Prior 1,020 g was artifact of Omdia back-calculation. Still no published spec. | Low for scrap values (changes Cu scrap by ~$1) |
| 2 | Gold content (0.02-0.05 g) | **Validated, tightened to 0.01-0.04 g** via ENIG calculation | Minimal (-$1.45 at mid-estimate) |
| 3 | HBM3e stack price ($300-420) | **Validated** -- consistent with Goldman Sachs $10-15/GB OEM data + markup | None (already well-calibrated) |

### Confidence Assessment
- Component accuracy: 75/100
- Pricing accuracy: 60/100 (HBM3e pricing validated via Goldman Sachs/Epoch AI data)
- Overall confidence in scrap estimate: 65/100

---

## 7. Key Observations

1. **The corrected functional-to-scrap ratio is approximately 1,800:1** ($25,000 working vs ~$14 scrap). Even a 1% chance of successful repair justifies attempting rework over material recovery. The original 1,000:1 ratio was understated because the scrap total was overstated.

2. **HBM3e stacks dominate component-level salvage value.** At $300-$420/stack (2026 pricing), the six stacks represent $1,800-$2,520 -- dwarfing all precious metal content by more than 100x. However, their raw scrap value is only $0.18 total ($0.03/stack).

3. **Gold content is extremely low** (~0.01-0.04 g, worth $1.45-$5.80). First-principles ENIG thickness calculations confirm: SXM modules have no gold-plated edge connectors (SXM5 uses silver-plated copper), no gold wire bonds (CoWoS-S uses Cu pillar bumps), and only thin ENIG on substrate/board pads. At 80 billion transistors and $25,000 MSRP, the gold content is worth less than a cup of coffee.

---

## 8. Web Verification (2026-03-29)

Independent web search performed against six claims. Results:

| # | Claim | Status | Source |
|---|-------|--------|--------|
| 1 | Same GH100 die as H100 SXM5 (814 mm2, 80B transistors, TSMC 4N) | **CONFIRMED** | NVIDIA product page; Tom's Hardware; AnandTech SC23 coverage; multiple vendor datasheets |
| 2 | 6x 24GB HBM3e 8-Hi stacks = 141 GB usable (144 GB physical), 4.8 TB/s, 6144-bit bus | **CONFIRMED** | NVIDIA H200 datasheet (Megware); Tom's Hardware H200 announcement; Micron HBM3E product brief; HWCooling.net |
| 3 | SXM5 form factor, 700W TDP | **CONFIRMED** | NVIDIA datasheet; Lenovo Press LP1944; 2CRSi spec page |
| 4 | VRM: 29 inductors, 61 power stages (same as H100 SXM5) | **INFERRED, NOT DIRECTLY CONFIRMED** | Tom's Hardware H100 SXM5 teardown confirms 29 dual-stage + 3 single-stage = 61 stages for H100. No public H200 teardown exists. Same SXM5 socket, same 700W TDP, drop-in compatible -- very likely identical VRM, but board-level differences near HBM area are possible (H200 uses 6 stacks vs H100's 5). Confidence: 70/100. |
| 5 | Module weight ~640 g bare (revised from ~1,020 g) | **REVISED via bottom-up estimate + web research** | No published NVIDIA spec anywhere (exhaustive search confirmed). Bottom-up engineering calc yields ~640 g (550--750 g range), cross-checked 7 ways: HGX PCF back-calc, A100 SXM4 scaling, H100 PCIe area adjustment, DGX H100/H200 identical weight (287.6 lbs), Dell XE9680 per-config deltas, Locuza PCB dimensions (~150x80mm), HGX B200 PCF (32 kg) validates methodology. Prior 1,020 g was artifact of Omdia back-calculation with 51% unexplained residual. Confidence: 55/100 (improved from 50; additional evidence, still no direct measurement). |
| 6 | NVLink 4.0, 18 links, 900 GB/s bidirectional | **CONFIRMED** | NVIDIA datasheet; Lenovo Press; RunPod spec guide; ArcCompute |

### Notes on verification
- **VRM (claim 4):** The report and components.csv attribute the 29-inductor/61-stage count to the Tom's Hardware H100 SXM5 photo analysis. This is the best available proxy. The H200 is a drop-in replacement with identical power envelope, but the extra HBM3e stack (6 vs 5) could in principle require minor PCB routing changes near the memory area. VRM notes in components.csv updated to say "inferred for H200."
- **Weight (claim 5):** NVIDIA does not publish bare module weight for any SXM-class GPU. Exhaustive web research (40+ searches, see `weight_investigation.md`) confirms no published weight exists anywhere. The original 1,020 g was revised to ~640 g via bottom-up engineering estimate with seven independent cross-checks (see `weight_engineering.md`). Additional evidence: DGX H100 and DGX H200 weigh identically (287.6 lbs each), and the Dell XE9680 shows A100-to-H100 system weight delta of ~3 kg (375g/module with heatsink). No HGX H200 PCF document has been published. Still no direct measurement available.
- **HBM3e supplier:** Micron confirmed as volume supplier for H200 (surprising the market, per TechPowerUp/Korea JoongAng Daily). SK Hynix also supplies. Report correctly lists "SK Hynix or Micron."

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Component-by-component ceiling assuming perfect extraction and a willing buyer for every part:

| Component | Theoretical Ceiling | Basis |
|-----------|-------------------|-------|
| GPU die (GH100) | $500-$800 | Shenzhen gray-market donor value only. Western value ~$0. Bare desoldered die with no provenance has no liquid market. |
| HBM3e stacks (6x ~24 GB) | **$0** | CoWoS-bonded at 40 um microbump pitch with capillary underfill. Non-destructive removal is not possible with any commercially available equipment. No individual HBM stacks have ever been listed on any marketplace or broker. |
| GDDR6 chips | N/A | SXM module uses HBM, not discrete GDDR6. |
| Precious metals (Au ~0.01 g, Ag 0.46 g, Pd 0.005 g) | $2.72 | At 100% spot recovery. SXM5 modules have very low gold -- no PCIe edge fingers, silver-plated (not gold) connector. |
| VRM components (61 DrMOS + 32 inductors) | $30-$60 | Shenzhen only. Desoldering 61 power stages at Western labor rates exceeds the component value. |
| Heatspreader / IHS (200 g Cu) | $2.60 | Copper scrap at $13/kg. Proprietary form factor, no secondary resale. |
| PCB + connector | $1.24 | SXM5 proprietary form factor. No standalone resale market for either PCB or connector. |
| **Theoretical max total** | **$537-$867** | Almost entirely dependent on finding a Shenzhen buyer for the die. |

### 10.2 Realistic US Scrap Value (Grounded Estimate)

- **Option A -- ITAD broker buys dead module whole:** 10-25% of used working price ($18,000-$25,000) = **$1,800-$6,250.** Dead SXM modules are harder to broker than PCIe cards (require HGX baseboard), so expect the lower end. Shenzhen repair channels (500 units/month capacity) are the most likely ultimate buyer.
- **Option B -- E-waste recycler:** Module weighs ~640 g (~1.41 lbs). At $5-$15/lb for server-grade boards = **$7-$21**, plus 60-70% PM credit on ~$2.72 gross = **$1.60-$1.90 PM credit.** Total: **$9-$23.**
- **Component harvesting is NOT viable in the US.** HBM3e is CoWoS-bonded ($0). VRM labor cost exceeds recovery. SXM5 connector and PCB are proprietary with no aftermarket demand.
- **Realistic US scrap range: $9-$23 (recycler) or $1,800-$6,250 (broker/ITAD).** The broker path is overwhelmingly superior. For SXM modules specifically, selling the entire HGX baseboard (8 modules) as a unit to a remarketing firm will yield a better per-module price than individual disposition.

---

## 9. Methodology & Sources

### GPU Specifications
- [NVIDIA H200 Product Page](https://www.nvidia.com/en-us/data-center/h200/) -- official product overview, HBM3e memory upgrade
- [NVIDIA H200 Datasheet (Megware)](https://www.megware.com/fileadmin/user_upload/LandingPage%20NVIDIA/NVIDIA_H200_Datasheet.pdf) -- detailed specs, 700W TDP, SXM5 form factor
- [Fluence H200 Deep Dive](https://www.fluence.network/blog/nvidia-h200-deep-dive/) -- technical analysis, GH100 die details, CoWoS-S packaging
- [Lenovo Press NVIDIA H200 141GB](https://lenovopress.lenovo.com/lp1944-nvidia-h200-141gb-gpu) -- server integration, power and thermal specs
- Board weight: **Revised** -- bottom-up engineering estimate ~640 g (see `weight_engineering.md` and `weight_investigation.md`), replacing the prior 1,020 g Omdia-derived figure. Cross-checked via HGX H100 PCF 24 kg back-calculation, A100 SXM4 scaling, H100 PCIe area adjustment, DGX H100/H200 identical system weights (287.6 lbs), and Dell XE9680 per-config weight deltas. Not an NVIDIA-published specification
- [DGX H200 Datasheet (287.6 lbs)](https://resources.nvidia.com/en-us-dgx-systems/dgx-h200-datasheet) -- identical weight to DGX H100, confirming H200 SXM is drop-in physical replacement
- [Dell XE9680 Service Manual -- System Weight](https://www.dell.com/support/manuals/en-us/poweredge-xe9680/xe9680_ism_pub/system-weight) -- A100 SXM4 at 105 kg vs H100/H200 SXM5 at 107-108 kg
- [Locuza SXM5 dimension estimate (~150x80mm)](https://x.com/Locuza_/status/1522260942049918981) -- photo-derived, cross-validated by die size calculation
- [HGX B200 PCF Summary (32 kg)](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf) -- validates PCF weight methodology
- Precious metal quantities: ENIG thickness calculation for gold; SAC305 alloy composition (3% Ag) for silver; MLCC literature for palladium
- Recovery rates: Professional hydrometallurgical processing recovers 40-60% of theoretical content; recycler payout estimated at 40-55% of gross scrap value after refining costs

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report
- **PCB scrap rates:** [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)

### Secondary Market
- eBay sold listings (Mar 2026)
- ALTA Technologies, Thunder Compute
