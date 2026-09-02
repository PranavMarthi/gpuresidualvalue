# NVIDIA H100 SXM5 -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** SXM5
**TDP:** 700W
**MSRP:** $25,000-$40,000 | **Used (Mar 2026):** $9,600-$15,000

---

## 1. Card Overview

The NVIDIA H100 SXM5 is a mezzanine-form-factor GPU accelerator module that plugs into an HGX baseboard via a high-density SXM5 connector. It uses the GH100 die on TSMC 4N and is NVIDIA's flagship Hopper-generation datacenter accelerator. Cooling is provided externally by the server chassis; the module itself carries a copper heatsink/heatspreader assembly.

| Attribute | Value |
|-----------|-------|
| GPU die | GH100 (TSMC 4N custom) |
| Die area | 814 mm2 |
| Transistors | 80 billion |
| Memory | 80 GB HBM3 (5 of 6 stacks active, each 16 GB) |
| Memory bus | 5120-bit (80 GB); 6016-bit (94 GB, all 6 stacks active) |
| Interconnect | 4th-gen NVLink, 900 GB/s, 18 links |
| TDP | 700 W |
| Board weight | ~3.0 kg with heatsink (Omdia estimate); ~1.0-1.2 kg board only |
| Packaging | CoWoS-S (Chip-on-Wafer-on-Substrate) |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (Cu/Ni, vapor chamber or solid) | 1,800 | 60.0% |
| PCB (PG520, FR-4/Cu multilayer) | 280 | 9.3% |
| VRM (inductors + MOSFETs + caps) | 170 | 5.7% |
| GPU die + CoWoS package substrate | 87 | 2.9% |
| Memory (6 HBM3 stacks) | 7 | 0.2% |
| Connectors + stiffener frame | 60 | 2.0% |
| Other (solder, TIM, passives, underfill, misc) | 596 | 19.9% |
| **Total** | **~3,000** | **100%** |

---

## 3. Component Breakdown

### GPU Die
- GH100, 814 mm2, 80B transistors, TSMC 4N
- Die weight: ~0.19 g (thinned to ~100 um on CoWoS interposer) or ~1.47 g (unthinned at ~775 um). See Section 6 for the contradiction in source data.
- Secondary market: $800 (reballing/rework for refurbishment)
- Raw scrap: $0.004

### Memory
- 6 x 16 GB HBM3 8-Hi stacks (5 active on 80 GB SKU, all 6 active on 94 GB SKU)
- Note: the 94 GB variant uses HBM3, not HBM3e. HBM3e is the H200/Blackwell generation.
- Secondary market: $1,200 total ($240/stack for 5 active stacks on 80 GB SKU; $15/GB at 2025 HBM3 contract pricing)
- Raw scrap: $0.50 total ($0.10/stack, Cu microbumps and trace Au)

### Heatsink
- Copper vapor chamber or solid Cu, Ni plated
- 1,800 g (~60% of module)
- Secondary market: $15 (generic Cu heatsink scrap)
- Raw scrap: $21.69 (Cu at $12.05/kg)
- Note: the 1,800 g weight is derived by subtracting estimated board weight (~1.0-1.2 kg) from the Omdia module weight estimate (~3 kg). No independent teardown measurement has been published.

### VRM / Power Delivery
- 29+3 inductors (32 total: 29 dual-phase + 3 single-phase) + 61 power stages (MPS Monolithic Power Systems), ~350 MLCCs and bulk caps
- Inductors ~112 g, MOSFETs ~21 g, capacitors ~53 g
- Secondary market: $165 (component harvesting for board-level repair)
- Raw scrap: $3.10 (ferrite, Cu windings, trace Pd in MLCCs)

### PCB
- PG520, FR-4 multilayer (~12-16 layers)
- ~280 g; Cu content ~15-20% by weight (~45 g Cu)
- Secondary market: $25 (donor board for VRM components)
- Raw scrap: $6.50 (server-grade PCB at ~$17-44/kg to specialty recyclers)

### Connectors
- SXM5 mezzanine connector: high-density power + signal, delivers 700 W, PCIe Gen5, NVLink. Cu alloy body, Au-plated contacts (~1.27 um / 50 uin per MEG-Array spec, selectively plated). ~25 g. Gold content ~0.005-0.010g (see gold_content_analysis.md Section 2.5).
- Secondary market: $30 (replacement connector)
- Raw scrap: $0.80

### Other
- Indium TIM (~8 g): raw scrap $4.96 (In at $0.62/g, SMM industrial benchmark; corrected from $0.97/g retail/investor price)
- BGA solder SAC305 (~12 g): raw scrap $0.56
- Organic BGA substrate (~85 g): secondary $15, raw scrap $1.50
- CoWoS-S silicon interposer (~2,500 mm2): secondary $50, raw scrap $0.002
- Underfill epoxy, stiffener frame, misc passives: combined secondary ~$10, raw scrap ~$0.17
- Raw scrap subtotal (other): ~$10.01

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.025 | $144.96/g | $3.62 | SXM5 connector plating ~0.005-0.010g, BGA ENIG ~0.003g, PCB ENIG ~0.010-0.015g. No PCIe gold fingers (SXM form factor). No wire bonds -- H100 uses flip-chip Cu pillar bumps via CoWoS-S. See gold_content_analysis.md for first-principles derivation. |
| Silver (Ag) | 0.42 | $2.25/g | $0.95 | SAC305 solder (~12g x 3% Ag = 0.36g) + MLCC terminations (~0.06g). **Revised from 0.80g:** the board-only mass is ~1,000-1,200g with ~12g of SAC305 solder; 3% of 12g = 0.36g Ag from solder, +15% for MLCC = ~0.42g. The original 0.80g implied ~27g of solder, which is inconsistent with a board of this size. |
| Palladium (Pd) | 0.005 | $45/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.04g. |
| **Total** | | | **$4.80** | |

Additional specialty metals: Indium (~8 g, $4.96 at $0.62/g SMM), Tin (~11.6 g, $0.55), Copper (~95 g board + ~1,800 g heatsink, $22.83 total).

**Gold revision note (2026-03-29):** Original estimate was 0.30g, reduced to 0.025g (~0.02-0.03g range) based on first-principles analysis. SXM modules have NO PCIe gold fingers. Gold sources: SXM5 connector plating ~0.005-0.010g, BGA ENIG pads ~0.003g, PCB ENIG surface finish ~0.010-0.015g. The original 0.30g dramatically overestimated connector gold content (~10x). See gold_content_analysis.md Part 2 (sections 2.2, 2.3, 2.5) and Part 4 row 16.

---

## 5. Value Cascade

| Scenario | Value | % of MSRP ($25K) |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $9,600-$15,000 | 38-60% |
| Component salvage (theoretical max) | $2,310 | 9.2% |
| Component salvage (realistic, 50-70% yield) | $1,155-$1,617 | 4.6-6.5% |
| Raw material scrap (gross) | ~$37 | 0.15% |
| Recycler payout (net, what you'd receive) | $15-$32 | 0.06-0.13% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **94 GB variant memory type [HIGH]:** Summary claimed HBM3e with 12-Hi stacks. All public sources confirm it is HBM3, not HBM3e. HBM3e is used in the H200 and Blackwell-generation GPUs. The internal stack configuration for the 94 GB SKU is undisclosed by NVIDIA.
- **Die weight contradiction [MODERATE]:** Summary states die is "thinned to ~0.1 mm on CoWoS" but gives weight of 1.47 g, which corresponds to unthinned ~0.775 mm thickness. At 0.1 mm, the die would weigh ~0.19 g. The weight and thickness claims are mutually exclusive.
- **64 GB variant [MODERATE]:** Described as a "salvage bin" product, but only PCI ID registry entries exist. No evidence it ever shipped commercially.
- **94 GB bus width [LOW-MODERATE]:** Summary states 5120-bit for all variants. With all 6 HBM3 stacks active, the 94 GB variant likely uses a 6016-bit (or 6144-bit) bus, not 5120-bit.
- **Heatsink weight [MODERATE]:** The 1,800 g copper heatsink figure is derived from the Omdia ~3 kg module estimate minus board weight. No independent teardown has confirmed this. NVIDIA does not publish SXM module weights.
- **VRM internal rounding [MINOR]:** CSV line items sum to ~$176 for VRM secondary value (32 x $2.50 + 61 x $1.00 + 350 x $0.10), but summary uses ~$165. The ~$11 difference flows through to the component salvage total.

### Pricing Issues
- **Palladium $/oz vs $/g inconsistency [MINOR]:** Document cites $1,363/oz (tradingeconomics) but uses $45.22/g. At $1,363/oz the correct per-gram price is $43.82. The $45.22/g corresponds to ~$1,406/oz (Mar 29 live spot). Impact: $0.06 on total, negligible.
- **Indium pricing source [CORRECTED]:** The original $972/kg figure (strategicmetalsinvest.com) was a retail/investor price, not an industrial benchmark. Corrected to $618/kg ($0.62/g) per SMM China 4N+ benchmark (Mar 2026). Impact: indium TIM value reduced from $7.76 to $4.96 (-$2.80). See indium_price_analysis.md.
- **No independent assay [MODERATE]:** No assay of H100 SXM5 precious metal content has been published. The document correctly notes +/-50% uncertainty on metal quantities.

### Confidence Assessment
- Component accuracy: 80/100 (for the standard 80 GB module)
- Pricing accuracy: 80/100
- Overall confidence in scrap estimate: 75/100

### Web Verification (2026-03-29)

Claims cross-checked against public sources:

| # | Claim | Status | Detail |
|---|-------|--------|--------|
| 1 | VRM: 29+3 inductors, 61 power stages (MPS) | CONFIRMED | Tom's Hardware teardown photos (May 2022): 29 inductors with 2 power stages each + 3 with 1 = 32 inductors, 61 stages total. Report body corrected from "32 inductors" to "29+3 inductors (32 total)" to match source and CSV. |
| 2 | Module weight ~3 kg with heatsink (Omdia) | QUALIFIED | Omdia (via Tom's Hardware, Sept 2023) estimated "average weight of one H100 with heatsink is over 3 kg." However, Tom's Hardware noted the H100 PCIe weighs 1.2 kg and a comparable OAM module ~2 kg, yielding a blended average of ~1.84 kg at 80/20 module/card mix. The 3 kg figure may overstate the SXM module weight. NVIDIA does not publish SXM module weight. No independent teardown weight measurement exists. |
| 3 | Heatsink ~1.8 kg copper | UNVERIFIED (derived) | No independent measurement. Derived from ~3 kg (Omdia) minus ~1.0-1.2 kg board. If the module is lighter than 3 kg, the heatsink estimate is proportionally overstated. |
| 4 | 80 GB = 5 of 6 HBM3 stacks active (16 GB each) | CONFIRMED | Tom's Hardware, NVIDIA Hopper whitepaper, and multiple sources confirm 6 physical stacks with 5 active on the 80 GB SKU. |
| 5 | 94 GB variant uses HBM3 (not HBM3e), 8-Hi stacks | CONFIRMED | NVIDIA product page, ServerSupply specs, WCCFTech, and retailer listings all specify HBM3 for the H100 NVL 94 GB. HBM3e is H200/Blackwell generation. Stack height (8-Hi vs 12-Hi) for the 94 GB SKU is not publicly disclosed by NVIDIA; 8-Hi is inferred from the 16 GB/stack capacity matching standard HBM3 8-Hi. |
| 6 | 94 GB bus width: 6016-bit | CONFIRMED | ServerSupply, Dell, and Supermicro product listings for H100 NVL 94 GB all specify 6016-bit memory interface at 3,938 GB/s. TechPowerUp lists 5120-bit for "H100 SXM5 94 GB" but this appears incorrect; hardware spec sheets consistently show 6016-bit when all 6 stacks are active. |
| 7 | NVLink 4th gen, 18 links, 900 GB/s | CONFIRMED | NVIDIA datasheet and Hopper architecture whitepaper: 18 links at 25 GB/s unidirectional each = 900 GB/s bidirectional total. |
| 8 | SXM5 connector: high-density power + signal | CONFIRMED (partial) | SXM5 socket delivers 700 W power + PCIe Gen5 + NVLink signals. Full pinout is under NDA. Wikipedia SXM socket article confirms SXM5 is the Hopper-generation socket. |

---

## 7. Key Observations

1. **Massive value destruction at end-of-life.** A module costing $25,000-$40,000 new has a raw scrap value of only ~$37. Even component-level secondary recovery yields ~$2,310 -- less than 10% of new price.
2. **Copper dominates raw scrap value, not gold.** After first-principles gold calibration (0.30g -> 0.025g), gold contributes only ~$3.62 per module (~10% of PM value). The copper heatsink (~$22) is now the single largest scrap value contributor, accounting for ~59% of gross raw material value.
3. **SXM modules are gold-poor by design.** Unlike PCIe cards, SXM modules have NO PCIe gold edge fingers. Gold sources are limited to the mezzanine connector plating (~0.005-0.010g), BGA ENIG pads (~0.003g), and PCB ENIG surface finish (~0.010-0.015g). Total: ~0.02-0.03g.
4. **HBM3 stacks carry the most secondary market value** (~$1,200 for 5 active stacks on 80 GB), but extraction from a CoWoS package is extremely difficult without damaging the stacks due to underfill epoxy.
5. **The heatsink is the easiest high-value scrap component** -- mechanically separable, nearly pure Cu at ~1.8 kg, worth ~$22 as clean Cu scrap.
6. **The CoWoS packaging creates a recovery challenge.** The GPU die, HBM stacks, and interposer are bonded together with underfill epoxy, making non-destructive separation impractical without specialized equipment.

---

## 8. Methodology & Sources

### GPU Specifications
- [Tom's Hardware H100 SXM5 VRM Teardown](https://www.tomshardware.com/news/nvidia-hopper-h100-sxm5-pictured) -- physical teardown, VRM layout (29+3 phases), heatsink construction
- [NVIDIA H100 Datasheet](https://resources.nvidia.com/en-us-gpu-resources/h100-datasheet-24306) -- GH100 die specs, memory configurations, 700W TDP
- [NVIDIA Hopper Architecture In-Depth](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/) -- GH100 die architecture, CoWoS-S packaging, NVLink 4.0
- [IT Creations H100 SXM5](https://www.itcreations.com/nvidia-gpu/nvidia-h100-sxm5-gpu) -- product reference and secondary market context
- Board weight: Omdia via [Tom's Hardware](https://www.tomshardware.com/news/nvidia-sold-900-tons-of-h100-gpus-last-quarter) / [The Register](https://www.theregister.com/2023/09/19/900_tons_nvidia_servers/) (Sept 2023), estimating "average weight of one H100 with heatsink is over 3 kg." Tom's Hardware notes this may overstate the SXM module since H100 PCIe weighs 1.2 kg and a comparable OAM module ~2 kg. NVIDIA does not publish SXM module weight.
- Precious metal quantities: Engineering estimates based on ENEPIG finish, SAC305 solder, MLCC electrode composition, and general GPU recycling literature. No independent assay exists; +/-50% uncertainty.
- Recovery rates: 50-70% yield assumed for component salvage; 95-99% for gold via professional refining.

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)
- Tin $46.60/kg (LME); Indium $618/kg ($0.62/g) per Shanghai Metals Market (SMM) 4N+ benchmark, Mar 2026. Original $972/kg from strategicmetalsinvest.com was retail/investor pricing, not industrial spot. See indium_price_analysis.md.

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report
- **PCB scrap rates:** $17-44/kg -- [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)

### Secondary Market
- eBay sold/listed (Mar 2026)
- ALTA Technologies, JarvisLabs

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Assumes every component is perfectly extracted and sold to the highest-value buyer globally.

| Component | Ceiling Value | Notes |
|-----------|--------------|-------|
| GH100 die | $800 | Shenzhen gray-market reballing/rework only. No liquid Western market. Value exists specifically because US export controls create artificial scarcity in China. |
| HBM3 stacks (6x) | **$0** | CoWoS-S interposer with capillary underfill + 40um-pitch microbumps. Non-destructive removal is at the extreme edge of what is physically possible. No secondary market for individual HBM stacks (zero listings found on eBay, AliExpress, Taobao, or any broker). Per hbm_secondary_market.md: "realistic standalone value: $0." |
| Heatsink (~1.8 kg Cu) | $22 | Clean bare-bright Cu scrap at ~$5.90/lb. Mechanically separable with no special equipment -- the single easiest high-value recovery. |
| VRM (61 stages + 32 inductors) | $165 | Component harvesting; requires hours of skilled BGA rework labor. At US rates ($50-100/hr), labor exceeds recovery. |
| SXM5 connector | $30 | Replacement connector for niche adapter projects; extremely thin demand, may sit unsold for months |
| PCB (donor board) | $25 | Repair shop donor; or ~$6.50 as server-grade board scrap |
| CoWoS interposer | $50 | Limited reuse; manufacturing cost $500-$1,500 but no viable secondary application |
| Organic BGA substrate | $15 | Board-level repair |
| **Total** | **~$1,107** | Requires Shenzhen-only buyers and physically impossible HBM extraction |

The $2,310 theoretical max in Section 5 includes $1,200 for HBM3 stacks. These have $0 separable value. The Shenzhen repair shops documented in Reuters/Tom's Hardware reporting swap entire CoWoS package assemblies (die + interposer + all HBM stacks as a unit), not individual stacks. "HBM replacement" in the reporting means package-level swap, not stack-level surgery.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator actually receives for a dead H100 SXM5:

**Option A -- Sell dead card to ITAD broker:** At 10-25% of used working price ($9,600-$15,000), expect **$960-$3,750**. The H100 SXM5 has the deepest broker market of any datacenter GPU (Net Equity, ALTA Technologies actively buy). SXM form factor limits buyer pool to those with HGX baseboards, but demand from the Shenzhen repair ecosystem (500 repairs/month) provides a floor.

**Option B -- E-waste recycler by weight:** Module weighs ~3.0 kg (~6.61 lb). At $5-15/lb server PCB rate: $33-$99 base. PM assay credit at 60-70% recovery on ~$4.80 gross precious metals adds ~$3-$3.50. Copper heatsink separable for ~$22 additional. Total: **$58-$125**.

Component harvesting is not viable in the US. CoWoS-S packaging makes the die and HBM inseparable, and desoldering 61 VRM power stages and 32 inductors at Western labor rates costs more than $165 in labor alone.

**Realistic range: $960-$3,750** (broker, Option A strongly preferred) or **$58-$125** (recycler). The SXM5's heavy copper heatsink (~1.8 kg) makes it unusually valuable at the recycler compared to lighter OAM/PCIe cards.
