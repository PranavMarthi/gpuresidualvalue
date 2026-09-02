# AMD Radeon Instinct MI210 -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe 4.0 x16
**TDP:** 300W
**MSRP:** ~$16,500 | **Used (Mar 2026):** $2,187-$4,640

---

## 1. Card Overview

The Radeon Instinct MI210 is AMD's single-die CDNA 2 datacenter accelerator, using one Aldebaran GCD on a PCIe form factor with passive cooling. It targets HPC and AI inference workloads and is the PCIe counterpart to the dual-die MI250/MI250X OAM modules.

| Attribute | Value |
|-----------|-------|
| GPU die | Aldebaran GCD (TSMC N6) |
| Die area | ~724 mm2 per GCD (TechPowerUp); VideoCardz: ~740 mm2 (1,480/2); Wikipedia: ~790 mm2 (likely overestimate) |
| Transistors | ~29.1 billion (single GCD) |
| Memory | 64 GB HBM2e (4 stacks x 16 GB) |
| Memory bus | 4096-bit |
| Interconnect | Infinity Fabric 3.0 (3x xGMI links, 300 GB/s P2P) |
| TDP | 300 W |
| Board weight | ~1,100-1,200 g (estimated; no official figure; NVIDIA A100 PCIe comparator = 1,170g board-only) |
| Packaging | 2.5D Elevated Fanout Bridge (EFB) MCM |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (passive aluminum extrusion) | 650 | 55.3% |
| PCB (10-12 layer FR4) | 150 | 12.8% |
| VRM (MOSFETs + inductors + caps) | 125 | 10.6% |
| GPU die + MCM package substrate | 55 | 4.7% |
| Memory (4x HBM2e stacks) | 10 | 0.9% |
| Connectors (PCIe + xGMI + power) | 39 | 3.3% |
| Bracket + mounting hardware | 20 | 1.7% |
| Other (solder, TIM, passives, misc) | 126 | 10.7% |
| **Total** | **~1,175** | **100%** |

---

## 3. Component Breakdown

### GPU Die
- Aldebaran (single GCD), ~724 mm2 (TechPowerUp; VideoCardz cites ~740 mm2 per GCD), ~29.1B transistors, TSMC N6
- Note: 58.2B is the dual-die MI250/MI250X total. The MI210 uses one GCD with 104 of 128 CUs enabled.
- Secondary market: $150 (reballing/rework for board-level repair; extremely niche)
- Raw scrap: $0.02

### Memory
- 4 x 16 GB HBM2e stacks (64 GB total, 8-Hi with TSVs, 4096-bit bus, 1.6 TB/s)
- Secondary market: $120 total ($30/stack; demand for MI200-series repair) -- NOTE: HBM stacks are not individually removable from the EFB package; this value applies only if the entire MCM assembly is functional
- Raw scrap: $0.04

### Heatsink
- Passive aluminum extrusion (likely 6061 alloy)
- 650g (55% of card)
- Secondary market: $5 (replacement part for MI210 cards)
- Raw scrap: $0.86 (650g / 453.6 g/lb x $0.60/lb; corrected from $0.39 -- original had g-to-lb units error)

### VRM / Power Delivery
- Estimated 10-14 phase design for 300W TDP
- DrMOS power stages, ferrite-core inductors, MLCCs + bulk caps
- Secondary market: $20 ($15 MOSFETs + $2 inductors + $3 caps)
- Raw scrap: $0.88 ($0.25 MOSFETs + $0.18 inductors + $0.45 caps)

### PCB
- ~10-12 layer FR4, 267 mm x 111 mm
- Cu content ~80g (heavy copper planes)
- Secondary market: $8 (e-waste recycler payout for high-grade server boards)
- Raw scrap: $1.80

### MCM Package Substrate
- 2.5D EFB (Elevated Fanout Bridge) with localized silicon bridges above the substrate (functionally equivalent to TSMC InFO-L)
- ABF substrate with high-density copper redistribution layers, ~45g
- **Inseparable assembly:** GCD, 4 HBM stacks, silicon bridges, and substrate are permanently bonded via copper pillars, microbumps, and underfill encapsulation. Individual components (e.g., HBM stacks) cannot be removed without destroying the package. This is consistent with all 2.5D packaging (CoWoS, EMIB, EFB). See deep_investigation.md Section 2.
- Secondary market: $30 (only as part of package swap; no standalone market)
- Raw scrap: $0.15

### Connectors
- PCIe 4.0 x16 edge connector: gold-plated, ~0.02-0.05g Au -- secondary $0.50 / scrap $0.35
- 3x xGMI Infinity Fabric connectors: gold-plated pins, ~8g each -- secondary $10 / scrap $0.30
- 1x 8-pin EPS12V power connector (per AnandTech; Lenovo guide says 2x): tin-plated -- secondary $0.25 / scrap $0.02
- Total secondary: $10.75 / Total scrap: $0.67

### Other
- TIM (indium-based): ~1-2g indium at $0.62/g = $0.62-$1.24 (corrected from $0.15; original used outdated $0.30/g price)
- Bracket and mounting hardware: $0.10 secondary / $0.01 scrap
- Resistors and discrete SMD (~150 components): negligible

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.08 | $144.96/g | $11.60 | Wire bonds, connector plating, substrate pads |
| Silver (Ag) | 0.45 | $2.25/g | $1.01 | SAC305 solder (~12-15g x 3% Ag = 0.36-0.45g) + MLCC terminations (~0.05g). **Revised from 1.5g:** a ~1,175g PCIe card has ~12-15g of SAC305 solder; 3% Ag = 0.36-0.45g. The original 1.5g implied ~50g of solder, which is physically inconsistent with the board mass. |
| Palladium (Pd) | 0.01 | $45.16/g | $0.45 | Trace only; modern BME MLCCs contain zero Pd; residual from connector plating and any rare PME caps (see deep_investigation.md Section 4) |
| **Total** | | | **$13.06** | |

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $2,187-$4,640 | 13-28% |
| Component salvage (theoretical max) | ~$344 | 2.1% |
| Component salvage (realistic) | ~$100-$170 | 0.6-1.0% |
| Raw material scrap (gross) | ~$17-$18 | 0.10-0.11% |
| Recycler payout (net, what you'd receive) | $7-$10 | 0.04-0.06% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **Transistor count misattribution (WRONG):** Original stated 58.2B transistors. This is the dual-die MI250/MI250X total. The MI210 single GCD contains ~29.1B transistors. Corrected.
- **MLCC palladium content overstated (WRONG, corrected twice):** Original claimed 0.2-0.4g Pd based on outdated 2% Pd-by-weight assumption. First correction to 0.05g. Deep investigation (2026-03-29) found that BME MLCCs -- which account for 99% of Class II capacitors worldwide -- contain **zero palladium** (100% nickel electrodes). Literature confirms waste PCB Pd concentration of 10-100 mg/kg, with modern all-BME boards at the low end (~10-20 mg/kg). For a ~500g board: 0.005-0.02g Pd. **Re-corrected to 0.01g midpoint** ($0.45, down from $2.26).
- **Power connector count (UNCERTAIN):** AnandTech identifies 1x 8-pin EPS12V; Lenovo product guide says 2x 8-pin. Majority of sources (Amazon, IT Creations, Tom's Hardware) say 1x. Retained as 1x with caveat.
- **Card weight (UNCERTAIN, narrowed):** No official figure from AMD, Lenovo, or any retailer. NVIDIA A100 PCIe 80GB board weight confirmed at **1,170g** (excluding bracket) per official product brief. MI210 has similar form factor, TDP, and cooling but one fewer HBM stack and simpler packaging (EFB vs CoWoS), suggesting slightly lighter. Revised estimate: 1,100-1,200g with 1,150g central estimate.
- **EFB package inseparability (RESOLVED):** Deep investigation confirmed that HBM stacks cannot be individually removed from the EFB assembly. Dies are bonded via copper pillars and microbumps, then underfilled. This is consistent with all 2.5D packaging technologies. The GPU die + HBM stacks + substrate must be valued as a single unit.
- **VRM phase count (UNCERTAIN):** 10-14 phases is a reasonable estimate for 300W but unconfirmed.

### Pricing Issues
- **Heatsink scrap units error (WRONG):** Original claimed $0.39 for 650g aluminum at $0.60/lb. Calculation divided by 1000 (g-to-kg) instead of 453.6 (g-to-lb). Correct value: $0.86. Factor of ~2.2x understatement.
- **Indium price outdated (WRONG):** Original used $0.30/g. March 2026 indium is $0.54-$0.97/g (SMM benchmark ~$0.62/g). Corrected to $0.62/g, roughly doubling the TIM scrap value from $0.15 to $0.62-$1.24.
- **Gold per-gram conversion (WRONG, minor):** $4,430/oz / 31.1035 = $142.43/g, not $141.02/g as originally stated. This report uses the corrected $4,509/oz ($144.96/g) for Mar 29.
- **Palladium scrap value inflated (WRONG, corrected twice):** Original claimed $13.55 for 0.3g Pd. First correction to 0.05g/$2.26. Deep investigation further reduced to 0.01g/$0.45. Total reduction from original: ~30x. This was the single largest error by dollar impact.

### Web Verification (2026-03-29)
Independent web search verification of key claims:

| Claim | Status | Sources |
|-------|--------|---------|
| Single Aldebaran GCD, ~29.1B transistors | CONFIRMED | AnandTech, WCCFTech, TechPowerUp, NextPlatform |
| TSMC N6 (6nm) process | CONFIRMED | AMD brochure, AnandTech, TechPowerUp, Chips and Cheese |
| 4x HBM2e stacks, 64 GB, 4096-bit, 1.6 TB/s | CONFIRMED | AMD product page, Lenovo product guide, Newegg listing |
| 3x xGMI IF connectors along top edge | CONFIRMED | AnandTech, IT Creations; Supermicro sells bridge connectors (GPU-XGMIMI210-2P). No bare-PCB teardown photos found online. |
| 2.5D EFB packaging | CONFIRMED | AnandTech, AMD press release, IEEE Xplore (10.1109/ECTC51909.2023.00218), Yole teardown report |
| PCIe 4.0 x16, dual-slot, passive cooling | CONFIRMED | All sources agree |
| 1x 8-pin power connector | LIKELY (1x EPS12V per AnandTech, Amazon, IT Creations, Tom's Hardware; Lenovo guide says 2x) |
| Card weight ~1,150g | UNVERIFIABLE (narrowed) | No official weight published anywhere. NVIDIA A100 PCIe 80GB = 1,170g (board only, official). MI210 likely ~1,100-1,200g. Central estimate revised to 1,150g. |
| Die area 724 mm2 | MOSTLY RESOLVED | TechPowerUp: 724 mm2 (most cited). VideoCardz: ~740 mm2 (1,480/2). Wikipedia: ~790 mm2 (likely overestimate or includes non-active area). AMD has never published an official per-GCD area. 724 mm2 adopted as primary; 740 mm2 is defensible. See deep_investigation.md Section 3. |

- **CSV fix applied:** components.csv line 2 still had "58.2B transistors" (the dual-die total). Corrected to "~29.1B transistors (single GCD)".
- **Power connector clarified:** AnandTech specifically identifies the connector as 8-pin EPS12V (not standard PCIe auxiliary). Updated in CSV and report.
- **No teardown found:** No public MI210 PCB teardown or bare-board photos were found. Physical claims (weight breakdown, VRM phase count, PCB layer count) remain estimates based on comparable cards.

### Confidence Assessment
- Component accuracy: 90/100 (core specs confirmed; transistor count corrected; Pd corrected twice; EFB separability resolved; die area clarified)
- Pricing accuracy: 65/100 (Pd further reduced to 0.01g; all prior pricing errors corrected; remaining uncertainty in gold quantity and weight estimate)
- Overall confidence in scrap estimate: 70/100 (corrected range of ~$17-$18 is moderately reliable; silver revised from 1.5g to 0.45g during audit; deep investigation resolved EFB, Pd, and die area unknowns)

---

## 7. Key Observations

1. **Working card value dominates by 120-270x:** A functional MI210 at $2,187-$4,640 is worth 120-270x its corrected raw scrap value (~$17-$18). Scrapping is only rational for confirmed-dead cards.
2. **Palladium was the phantom value driver:** The original analysis identified palladium in MLCCs as the largest precious metal contributor ($13.55). After two rounds of correction for modern BME electrode chemistry, palladium drops to ~$0.45 (0.01g), and gold ($11.60) is now the dominant precious metal by ~26x.
3. **The heatsink is 55% of the weight but under 5% of the scrap value:** 650g of aluminum yields $0.86 in scrap. The 0.08g of gold -- weighing 8,125x less -- is worth 13x more. This illustrates the extreme value density of precious metals versus base metals in e-waste.
4. **EFB packaging makes component-level salvage impossible:** The GCD, HBM stacks, silicon bridges, and substrate are permanently bonded. Unlike socketed or BGA components, 2.5D packaged dies cannot be individually removed and reused. The entire MCM assembly must be treated as a single unit for salvage or scrap valuation.

---

## 8. Methodology & Sources

### GPU Specifications
- [AMD Instinct MI210 Product Page](https://www.amd.com/en/products/accelerators/instinct/mi200/mi210.html) -- official specifications, TDP, memory configuration
- [AMD Instinct MI210 Product Brochure](https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/product-briefs/instinct-mi210-brochure.pdf) -- feature summary, performance data
- [Tom's Hardware -- MI210 Shipments](https://www.tomshardware.com/news/amd-starts-shipments-of-mi210-pcie-cards) -- launch details, PCIe form factor confirmation
- [WCCFTech -- MI210 Aldebaran](https://wccftech.com/amd-instinct-mi210-with-single-aldebaran-cdna-2-gpu-die-features-104-compute-units-64-gb-hbm2e-memory-40-faster-than-mi100/) -- single-die configuration, CU count, HBM2e details
- [Lenovo Press -- AMD Instinct MI210](https://lenovopress.lenovo.com/lp1862-amd-instinct-mi210-accelerator) -- OEM integration specs, form factor confirmation
- [IT Creations -- AMD Instinct MI210](https://www.itcreations.com/amd-gpu/amd-instinct-mi210-gpu) -- secondary market pricing reference

### Precious Metal Spot Prices (March 29, 2026)
- Gold: $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- Silver: ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- Palladium: $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price)

### Scrap Metal & Commodity Prices
- Copper: $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- Copper scrap (#1 bare bright): [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- Weekly scrap report: [ScrapMonster (Mar 20-26, 2026)](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785)
- DRAM spot: [TrendForce](https://www.trendforce.com/price/dram/dram_spot)
- PCB scrap: [iScrapApp](https://iscrapapp.com/metals/pc-boards/)

### Secondary Market
- eBay listings March 2026 (sold prices not independently confirmed)

### Methodology Notes
- Board weight: Estimated from comparable datacenter PCIe cards; NVIDIA A100 PCIe 80GB = 1,170g board-only (official, PB-10577-001_v03); no official MI210 weight published
- Precious metal quantities: Gold 0.08g from industry refiner data for modern BGA GPUs; silver 1.5g from SAC305 solder composition; palladium 0.01g (deep investigation: BME MLCCs = zero Pd; residual from connector plating only)
- EFB packaging: AnandTech, 3D InCites, SemiEngineering confirm inseparable 2.5D assembly; rework impossible after underfill
- Recovery rates: Gold ~50%, Silver ~90%, Palladium ~85%, Copper ~95% (industry standard for professional e-waste recycling)
- Component verification: AMD product page, AnandTech, WCCFTech, Tom's Hardware, Lenovo Press, TechPowerUp, Chips and Cheese, AMD CDNA2 whitepaper
- Price verification: Cross-referenced against Specialty Metals (MLCC Pd), Knowles Capacitors (PME vs BME), EE Times (nickel switch in MLCCs)

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Component-by-component ceiling, assuming a buyer exists for each part at stated prices:

| Component | Ceiling Value | Notes |
|-----------|------------:|-------|
| Aldebaran GCD | $150 | Shenzhen gray-market reballing; limited demand vs NVIDIA dies |
| HBM2e stacks (4x) | **$0** | EFB 2.5D package -- stacks bonded via copper pillars + microbumps + underfill; not separable |
| Heatsink (passive Al) | $5 | Replacement part; niche |
| VRM components | $20 | MOSFETs + inductors + caps; labor cost may exceed value |
| PCB (server-grade) | $8 | E-waste recycler premium for high-grade boards |
| Connectors (PCIe + 3x xGMI) | $11 | xGMI connectors have some repair demand |
| **Theoretical ceiling** | **~$194** | |

EFB packaging makes the GCD + HBM assembly permanently inseparable -- identical constraint to NVIDIA's CoWoS. The die has modest gray-market value ($150) because AMD datacenter GPUs face less sanctions-driven demand than NVIDIA equivalents.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

| Option | Expected Recovery | Notes |
|--------|------------------:|-------|
| **A. ITAD broker** | $220-$1,160 | 10-25% of $2,187-$4,640 working price; AMD datacenter cards have thinner broker market than NVIDIA |
| **B. E-waste recycler** | $8-$15 | ~1.2 kg card at $5-15/lb server PCB + 60-70% PM assay credit on ~$13 precious metals |

**Realistic range for a dead MI210: $220-$500 (ITAD broker).** The MI210's niche position (single-GCD CDNA 2, PCIe form factor) means broker demand is thinner than for A100/H100 cards, but still far better than the $8-$15 a recycler would pay. The xGMI connectors and PCIe form factor make it easier to resell as a "for parts" unit than SXM/OAM modules.
