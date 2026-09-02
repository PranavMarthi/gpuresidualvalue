# NVIDIA GH200 Grace Hopper Superchip -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** SXM (MGX module)
**TDP:** 450-1000W (configurable; 900W typical)
**MSRP:** ~$35,000 | **Used (Mar 2026):** ~$5,500

---

## 1. Card Overview

The GH200 Grace Hopper Superchip is NVIDIA's heterogeneous compute module combining the Hopper-generation H100 GPU with a 72-core Grace ARM CPU, connected by a 900 GB/s NVLink-C2C coherent link. It targets HPC/AI workloads requiring unified CPU+GPU memory access.

| Attribute | Value |
|-----------|-------|
| GPU die | GH100 (TSMC 4N) |
| Die area | 814 mm2 |
| Transistors | 80 billion |
| CPU die | Grace CPU (TSMC 4N), 72 Neoverse V2 cores (84 physical, 12 disabled) |
| CPU die area | ~774 mm2 (Locuza estimate from die photo; unconfirmed by NVIDIA) |
| GPU Memory | 96 GB HBM3 (6 x 16 GB stacks) |
| CPU Memory | Up to 480 GB usable LPDDR5X (16 x 32 GB dual-channel packages; 512 GB physical, 32 GB reserved for RAS channel sparing) |
| Interconnect | NVLink-C2C (900 GB/s, PHY integrated into both dies) |
| TDP | 450-1000 W (configurable; 900 W typical) |
| Board weight | ~1,692 g (estimated; not officially disclosed) |
| Packaging | CoWoS-S (GPU+HBM complex), organic substrate module |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatspreaders (GPU + CPU, nickel-plated Cu) | 300 | 17.7% |
| Module substrate (organic, 12+ layer) | 450 | 26.6% |
| LPDDR5X packages (16x 32GB dual-ch, on-package) | 48 | 2.8% |
| HBM3 stacks (6x) | 45 | 2.7% |
| GPU die + interposer + underfill | 157 | 9.3% |
| Grace CPU die + underfill | 105 | 6.2% |
| VRM (inductors + MOSFETs + caps) | 261 | 15.4% |
| Connectors (NVLink + PCIe + power) | 130 | 7.7% |
| Module frame (aluminum) + mounting hardware | 125 | 7.4% |
| Other (solder, TIM, thermal pads, passives, misc ICs) | 71 | 4.2% |
| **Total** | **~1,692** | **100%** |

---

## 3. Component Breakdown

### GPU Die
- GH100, 814 mm2, 80B transistors, TSMC 4N
- Secondary market: $800 (reballing/rework for repair; extremely niche)
- Raw scrap: $0.08

### Grace CPU Die
- Grace CPU (no official die code; "GC100" is fictitious), ~774 mm2 (Locuza estimate), TSMC 4N, 72 enabled / 84 physical Neoverse V2 cores
- Secondary market: $200 (niche ARM server market limits demand)
- Raw scrap: $0.08

### GPU Memory (HBM3)
- 6 x 16 GB HBM3 stacks (96 GB total; 8-Hi with TSVs)
- Note: The 96 GB config uses HBM3, not HBM3e. HBM3e is the 144 GB config only.
- Secondary market: $600 total ($100/stack)
- Raw scrap: $1.80

### CPU Memory (LPDDR5X)
- 16 x 32 GB LPDDR5X dual-channel packages (512 GB physical; 480 GB usable), on-package PoP mounting
- Note: Corrected from 16 x 30 GB. The Grace CPU has 32 LPDDR5X channels (16 GB per channel). Each of the 16 physical packages (8 per side, per ServeTheHome) contains 2 channels = 32 GB. NVIDIA reserves 2 channels (32 GB) as spare channels for LPDDR5 RAS channel sparing, reducing usable capacity to 480 GB. The naive 480/16 = 30 GB calculation was incorrect.
- Die configuration (inferred): likely 8x 32Gb (4GB) LPDDR5X dies per package (Micron 8DP configuration).
- Secondary market: $180 (commodity DRAM, limited reuse due to PoP mounting)
- Raw scrap: $0.96 (based on 16 packages)

### Heatspreaders
- Two nickel-plated copper heatspreaders: GPU-side (180g) + CPU-side (120g) = 300g total
- Secondary market: $0
- Raw scrap: $3.89 (300g Cu at $5.90/lb)

### VRM / Power Delivery
- Module input: 12V DC (confirmed by part number 900-2G530-0060-000 "GH200 12V"). Not 48V -- rack-level PSU handles AC-to-12V conversion.
- GPU: ~12-phase (12 MOSFETs, 12 inductors). Reference: H100 SXM5 has 29 inductors with 2 power stages each for 700W GPU-only; GH200 GPU portion is lower power.
- CPU: ~8-phase (8 MOSFETs, 8 inductors)
- VRM controllers: NVIDIA OpenVReg (OVR) spec. DrMOS power stages (TI, AOS, or BPS).
- Capacitors: ~350 MLCCs + ~30 bulk polymer caps
- Secondary market: $0
- Raw scrap: $1.34 (copper in inductors + ferrite)

### Module Substrate
- 12+ layer HDI organic substrate (~250 mm x 200 mm est.), 450g
- Cu content ~8.1g (1.8% by weight)
- Secondary market: $0
- Raw scrap: $0.11 (8.1g Cu at $5.90/lb; corrected from erroneous $8.10)

### CoWoS-S Silicon Interposer
- Silicon interposer under GPU + HBM complex, ~35g
- Secondary market: $0
- Raw scrap: $0.63

### Connectors
- NVLink connector (external): gold-plated (selectively, ~50 uin), 45g, Au content ~0.005g -- secondary $15 / scrap $1.80
- PCIe Gen5 connector: gold-plated (selectively, ~50 uin), 35g, Au content ~0.005g -- secondary $10 / scrap $1.20
- Power connectors (2x): 50g total -- secondary $5 / scrap $0.45
- Total secondary: $30 / Total scrap: $3.45

### Other
- Indium-based TIM (GPU + CPU): ~6.7g indium total -- $4.02 at $0.60/g
- Thermal pads and gap fillers: no scrap value
- Misc ICs (clock, sensor, EEPROM): negligible
- Solder (SAC305, ~35g): $1.46 (tin at ~$19.50/lb)
- Module frame (85g aluminum): $0.19
- Retention hardware (40g steel): $0.04

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.035 | $144.96/g | $5.07 | NVLink connector plating ~0.005g, PCIe connector plating ~0.005g, 2x BGA ENIG (GPU+CPU) ~0.006g, PCB ENIG ~0.012g. No PCIe edge fingers (SXM/MGX form factor). No wire bonds -- both dies use flip-chip Cu pillar bumps. See gold_content_analysis.md for first-principles derivation. |
| Silver (Ag) | 1.20 | $2.25/g | $2.70 | SAC305 solder (~35g x 3% Ag = 1.05g) + MLCC terminations (~0.15g). **Revised from 2.0g:** original included "substrate traces" which use copper, not silver. The 35g of SAC305 solder yields 1.05g Ag; +15% for MLCC terminations = ~1.20g. |
| Palladium (Pd) | 0.005 | $45.16/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.12g. |
| **Total** | | | **$8.00** | |

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | ~$5,500 | 15.7% |
| Component salvage (theoretical max) | $1,810 | 5.2% |
| Component salvage (realistic, 30-50% yield) | $540-$905 | 1.5-2.6% |
| Raw material scrap (gross) | ~$24 | 0.07% |
| Recycler payout (net, what you'd receive) | ~$5-$10 | 0.01-0.03% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **HBM3e mislabeled (WRONG):** The 96 GB config uses HBM3, not HBM3e. HBM3e is only the 144 GB config. Corrected throughout this report.
- **LPDDR5X package count (WRONG, further corrected):** Original claimed 60 x 8 GB packages. ServeTheHome teardown confirms 16 packages (8 per side). Initially corrected to 16 x 30 GB, but this was also wrong. The Grace CPU has 32 LPDDR5X channels at 16 GB/channel = 512 GB physical. Each of the 16 packages contains 2 channels = 32 GB/package. 2 channels (32 GB) are reserved for RAS spare channel sparing, yielding 480 GB usable. Corrected to 16 x 32 GB.
- **NVLink-C2C "interconnect die" (WRONG):** Claimed as a separate silicon die with 8g weight and $50 secondary value. NVLink-C2C PHY is integrated into the Grace and GH100 dies -- there is no third die. Removed from BOM entirely.
- **Grace CPU die name "GC100" (WRONG):** This die code is fictitious. NVIDIA documentation refers to it simply as "Grace CPU." Corrected.
- **Grace CPU die size ~400 mm2 (WRONG):** NVIDIA has never officially disclosed this. The original report cited 350-400 mm2 with no source. Locuza's die photo analysis estimates ~774 mm2 (~6% smaller than GH100's 814 mm2), which is the only credible third-party estimate. Corrected to ~774 mm2. Die weight estimate raised from 55g to ~105g accordingly.
- **Module weight ~1,692g (UNCERTAIN):** No official disclosure found. Revised upward from ~1,650g after correcting Grace CPU die weight. Plausible given module complexity but unconfirmed.

- **TDP listed as fixed 900W (IMPRECISE):** The GH200 TDP is configurable from 450W to 1000W (ServeTheHome). 900W is a common default but not the only operating point. Corrected to show range.

### Pricing Issues
- **All precious metal prices stale (WRONG):** Gold, silver, palladium, and copper prices in the original CSV appear to be from mid-2024. Gold was listed at $2,400/oz (actual Mar 2026: $4,509/oz, +88%). Silver at $34/oz (actual: ~$70/oz, +106%). Palladium at $1,050/oz (actual: $1,405/oz, +34%). Copper at $4.50/lb (actual: $5.90/lb, +31%). All corrected in this report.
- **Substrate copper 100x calc error (WRONG):** Original claimed $8.10 for 8.1g Cu at $4.50/lb. Correct value: $0.08 (or $0.11 at current prices). Dividing grams by lb-price without unit conversion.
- **Gold per-gram conversion (WRONG):** $2,400/oz / 31.1035 = $77.16/g, not $75.3/g as originally stated.
- **Raw material total mismatch (WRONG):** Summary claimed ~$80 but CSV rows sum to $62.54. After March 2026 price corrections the total was ~$75; after gold calibration (0.35g -> 0.035g) and palladium correction (0.12g -> 0.005g) the gross scrap total is now ~$24.

### Deep Investigation Findings (2026-03-29)
- **12V power input CONFIRMED:** Part number 900-2G530-0060-000 explicitly listed as "GH200 12V". Module takes 12V DC, not 48V. Rack PSU handles conversion.
- **LPDDR5X per-package capacity CORRECTED:** 32 GB/package (2 channels x 16 GB), not 30 GB. The 480 GB usable figure comes from reserving 2 of 32 channels for RAS sparing.
- **Grace CPU die: 84 physical cores confirmed** (12 disabled for yield), consistent with ~774 mm2 estimate. Mesh is 6x7 grid.
- **Dual heatspreaders strongly supported** by Noctua cooler design (bonded to flat surfaces) and DLC cold plate evidence, though no teardown photo exists.
- **Module weight still unconfirmed.** Supermicro 1U system = 22 kg net, but module weight not isolatable from that figure.

### Confidence Assessment
- Component accuracy: 62/100 (5 original wrong items corrected, LPDDR5X further corrected, power input confirmed, cooling design better supported; weight still uncertain)
- Pricing accuracy: 35/100 (all precious metal prices corrected to Mar 2026 but still volatile; secondary market values speculative)
- Overall confidence in scrap estimate: 70/100 (up from 62; gold calibrated to 0.035g and palladium to 0.005g from first-principles analysis, LPDDR5X and power corrections improve component accuracy; scrap value revised to ~$24)

---

## 7. Key Observations

1. **Working value dwarfs scrap:** At ~$5,500 used, the GH200 trades at ~229x its corrected raw scrap value (~$24). Scrapping only makes sense for non-functional units.
2. **Dual-die complexity inflates theoretical salvage but not scrap:** The GH200 has ~$1,810 in theoretical parts-out value (GPU die + HBM + CPU die + LPDDR5X), but raw material scrap from two compute dies is still under $1 -- semiconductor value is almost entirely in the fabrication, not the silicon.
3. **Gold no longer dominates raw scrap after calibration.** Original gold estimate (0.35g, $50.74) was reduced ~10x to 0.035g ($5.07) based on first-principles analysis. Palladium also corrected (0.12g -> 0.005g; modern BME MLCCs contain zero Pd). Gold now accounts for ~21% of gross scrap (down from 68%). The largest scrap contributors are now indium TIM ($4.02), copper heatspreaders ($3.89), connectors ($3.45), and solder ($1.46). Precious metals combined ($9.84) are ~41% of gross scrap.
4. **Module has NO PCIe gold edge fingers.** As an SXM/MGX form factor, all connectors (NVLink, PCIe, power) use pin-and-socket or press-fit designs with selective gold plating, not the thick gold finger strips found on PCIe add-in cards. Gold sources: NVLink connector ~0.005g, PCIe connector ~0.005g, 2x BGA ENIG (GPU+CPU) ~0.006g, PCB ENIG ~0.012g. Total ~0.03-0.04g. See gold_content_analysis.md.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA GH200 Datasheet (AMAX)](https://www.amax.com/content/files/2023/12/NVIDIA_GH200_Grace_Hopper_Superchip_Datasheet.pdf) -- module specs, memory configuration, TDP
- [NVIDIA GH200 Datasheet (Boston)](https://download.boston.co.uk/downloads/0/5/8/0586c659-27bf-4c16-b8b0-0df7822468b2/grace-hopper-superchip-datasheet-2705455.pdf) -- specifications cross-reference
- [NVIDIA GH200 Product Page](https://www.nvidia.com/en-us/data-center/grace-hopper-superchip/) -- official specifications, architecture overview
- [ServeTheHome -- GH200 Introduction](https://www.servethehome.com/a-quick-introduction-to-the-nvidia-gh200-aka-grace-hopper-arm/) -- teardown data, LPDDR5X package count confirmation (16 packages)
- [Tom's Hardware -- GH200 HBM3e Reveal](https://www.tomshardware.com/news/nvidia-reveals-gh200-grace-hopper-gpu-with-141gb-of-hbm3e) -- HBM3 vs HBM3e configuration details
- [Spheron -- GH200 Guide](https://www.spheron.network/blog/nvidia-gh200-guide/) -- architecture details, NVLink-C2C specifications
- [Locuza (X/Twitter) -- Grace CPU die size estimate](https://x.com/Locuza_/status/1663217786812878848) -- ~774 mm2 from die photo analysis
- [Chips and Cheese -- Grace Hopper, Nvidia's Halfway APU](https://chipsandcheese.com/p/grace-hopper-nvidias-halfway-apu) -- architecture deep dive, NVLink-C2C details, 480-bit memory bus
- [Glenn Klockwood -- Grace CPU](https://www.glennklockwood.com/garden/processors/grace) -- 32 LPDDR5X channels, 512 GB physical vs 480 GB usable
- [Glenn Klockwood -- LPDDR5 RAS](https://glennklockwood.com/garden/LPDDR5-RAS) -- channel sparing architecture, inline ECC
- [NVIDIA Grace Hot Chips 34 Presentation](https://www.hc34.hotchips.org/assets/program/conference/day2/ADAS%20and%20Grace/HC2022.NVIDIA%20Grace.JonathonEvans.v5.pdf) -- 32-channel memory interface
- [Tom's Hardware -- H100 SXM5 VRM photos](https://www.tomshardware.com/news/nvidia-hopper-h100-sxm5-pictured) -- VRM reference design for Hopper
- [Tom's Hardware -- Noctua GH200 cooler](https://www.tomshardware.com/pc-components/air-cooling/noctua-creates-a-monstrous-cooler-for-nvidias-gh200-grace-hopper-superchip) -- cooling interface evidence
- [Wiredzone -- GH200 12V listing](https://www.wiredzone.com/shop/product/10029701-nvidia-900-2g530-0060-000-gh200-grace-hopper-superchip-12v-480gb-memory-supports-hbm3-or-hbm3e-gpu-nvgh480-12v-12767) -- 12V power input confirmation
- [The Next Platform -- Grace Memory](https://www.nextplatform.com/2023/05/29/nvidias-grace-hopper-hybrid-systems-bring-huge-memory-to-bear/) -- 32 channels, 512 GB physical
- [Supermicro ARS-111GL-NHR Datasheet](https://www.supermicro.com/en/products/system/datasheet/ars-111gl-nhr) -- system weight (22 kg net)

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
- Estimated from niche harvested-component markets; practical recovery yields 30-50%

### Methodology Notes
- Board weight: No official source; estimated at ~1,692g based on module complexity relative to ~1 kg H100 SXM5 (revised upward from ~1,650g after Grace CPU die size correction)
- Precious metal quantities: First-principles analysis from gold_content_analysis.md; 0.035g Au (revised from 0.35g) based on connector plating geometry, BGA ENIG pad area, and PCB ENIG surface finish calculations. No PCIe gold edge fingers on this form factor.
- Recovery rates: E-waste recyclers typically achieve 15-25% of theoretical secondary value
- Component verification: NVIDIA datasheets/whitepapers, AnandTech, ServeTheHome teardowns, Chips and Cheese, The Next Platform
- Price verification: Cross-referenced against multiple live spot price sources dated March 2026

---

## 9. Web Search Verification (2026-03-29)

Searched: "NVIDIA GH200 teardown", "Grace Hopper teardown", "GH200 PCB", "ServeTheHome GH200", "Grace CPU die size", "GH200 NVLink-C2C PHY", "GH200 HBM3 vs HBM3e", "GH200 module weight", "GH200 power delivery VRM".

| Claim | Verdict | Detail |
|-------|---------|--------|
| GH100 GPU die + Grace CPU (72 Neoverse V2) on one module | CONFIRMED | All sources consistent. |
| NVLink-C2C PHY integrated into both dies (no separate die) | CONFIRMED | NVIDIA NVLink-C2C page + Chips and Cheese + Spheron all confirm integrated SerDes. No bridge die. |
| LPDDR5X: 16 packages (8 per side) | CONFIRMED | ServeTheHome photos show 8 top + 8 bottom = 16 per CPU. |
| HBM3 (96 GB) vs HBM3e (144 GB) -- both variants exist | CONFIRMED | 96 GB = 6 x 16 GB HBM3; 144 GB (141 GB usable) = 6 x 24 GB HBM3e. AnandTech, Tom's Hardware, ServeTheHome all consistent. |
| Grace CPU die ~350-400 mm2 | WRONG | Locuza die photo analysis: ~774 mm2. No other credible estimate found. Report corrected. |
| Module weight ~1,650 g | NOT FOUND | No official or third-party source publishes module weight. NVIDIA datasheets omit it. Supermicro 1U system = 22 kg net but module not isolatable. Estimate retained as ~1,692 g. |
| TDP = 900 W fixed | IMPRECISE | Configurable 450-1000 W per ServeTheHome. 900 W is a common operating point, not a fixed spec. Corrected to show range. |
| Power delivery: combined CPU+GPU VRM on module | PLAUSIBLE | No GH200-specific VRM teardown found. GB200 successor uses multi-phase DrMOS (TI), RapidLock connectors, 48V-to-12V conversion. GH200 likely similar but at lower power. |
| Power input: 12V DC to module | CONFIRMED | Part number 900-2G530-0060-000 listed as "GH200 12V" by Wiredzone. Module does not do 48V conversion on-board. |
| LPDDR5X: 16 x 30 GB per package | WRONG | Grace has 32 LPDDR5X channels at 16 GB/channel = 512 GB physical. 16 packages x 2 channels = 32 GB/package. 2 channels reserved for RAS sparing = 480 GB usable. Corrected to 16 x 32 GB. |
| Grace CPU: 84 physical cores (12 disabled) | CONFIRMED | Die shot analysis shows 84 cores on die; 72 enabled. Layout: 2x8 + 5x12 core arrangement. Could fit 96 with one more row. |
| Dual heatspreaders on module | STRONGLY SUPPORTED | Noctua cooler "bonded to" flat surfaces (CPU, GPU), plus separate memory base plate. DLC cold plates designed for IHS contact. No bare-die evidence. No teardown photo of IHS itself. |
| LPDDR5X channel sparing (RAS) | CONFIRMED | Glenn Klockwood analysis + NVIDIA Grace Performance Tuning Guide confirm spare-channel architecture. "512 GB physical, 480 GB usable." |

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Component-by-component ceiling, assuming a buyer exists for each part at stated prices:

| Component | Ceiling Value | Notes |
|-----------|------------:|-------|
| GH100 GPU die | $800 | Shenzhen gray-market reballing/rework; sanctions-driven demand |
| Grace CPU die | $200 | Niche ARM server repair; far smaller buyer pool than GPU dies |
| HBM3 stacks (6x) | **$0** | CoWoS 2.5D package -- stacks bonded via microbumps + underfill; not separable |
| LPDDR5X (16x 32GB) | $180 | Commodity DRAM but PoP-mounted; limited reuse outside Grace modules |
| Connectors (NVLink + PCIe + power) | $30 | Illiquid; niche hobbyist/adapter market |
| **Theoretical ceiling** | **~$1,210** | |

The GH200 is unique: dual-die (CPU + GPU) architecture means two independently valuable compute dies, but the Grace CPU die has a much thinner repair market than datacenter GPU dies. The HBM3 stacks are permanently bonded in the CoWoS package and have $0 separable value (see hbm_secondary_market.md). LPDDR5X packages are on-substrate PoP, limiting reuse to Grace platform repair.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

| Option | Expected Recovery | Notes |
|--------|------------------:|-------|
| **A. ITAD broker** | $550-$1,375 | 10-25% of ~$5,500 working price; broker handles remarketing or parts-out |
| **B. E-waste recycler** | $20-$35 | ~1.7 kg module at $5-15/lb server PCB + 60-70% PM assay credit on ~$8 precious metals |

**Realistic range for a dead GH200: $550-$1,375 (ITAD broker).** The dual-die architecture and high working price make broker resale overwhelmingly superior to recycling. Even a dead module with one functional die complex is worth more to a Shenzhen repair operation than the $20-$35 a US recycler would pay. E-waste recycling is a last resort for physically destroyed modules only.
