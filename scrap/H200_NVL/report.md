# NVIDIA H200 NVL -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe (dual-slot, NVLink-bridge capable)
**TDP:** 600W
**MSRP:** ~$35,000-$40,000 | **Used (Mar 2026):** $31,000-$40,000

---

## 1. Card Overview

The NVIDIA H200 NVL is a dual-slot PCIe Gen5 datacenter GPU accelerator using the same GH100 Hopper die as the H100 but upgraded to HBM3e memory (141 GB). The "NVL" designation indicates support for 2-way and 4-way NVLink bridging via an external bridge connector (900 GB/s bidirectional per pair). It targets LLM inference and training workloads requiring large memory capacity.

| Attribute | Value |
|-----------|-------|
| GPU die | GH100 (TSMC 4N custom) |
| Die area | 814 mm2 |
| Transistors | 80 billion |
| Memory | 141 GB HBM3e (6 x 24 GB 8-Hi stacks, SK Hynix) |
| Memory bus | 6144-bit |
| Interconnect | NVLink bridge (900 GB/s per pair; supports 2-way and 4-way) + PCIe Gen5 x16 |
| TDP | 600 W |
| Board weight | ~1,260 g bare card with bracket (derived from H100 NVL product brief: 1,214 g board + ~50 g bracket; shipping weight ~1.45 kg includes packaging) |
| Packaging | CoWoS-S (Chip-on-Wafer-on-Substrate) |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink / cold plate (Al fins + Cu vapor chamber) | 530 | 42.1% |
| PCB (~14-16 layer FR-4/Cu multilayer) | 280 | 22.2% |
| VRM (inductors + MOSFETs + caps) | 180 | 14.3% |
| GPU die + CoWoS package substrate | 75 | 6.0% |
| Memory (6 HBM3e stacks) | ~5 | 0.4% |
| Backplate (aluminum) | 100 | 7.9% |
| Bracket / shroud + connectors | 43 | 3.4% |
| Other (solder, TIM, passives, underfill, thermal pads, misc) | 47 | 3.7% |
| **Total** | **~1,260** | **100%** |

*Note: Total revised from ~1,500 g to ~1,260 g based on H100 NVL product brief (PB-11773-001_v01) which confirms board weight of 1,214 g excluding bracket. H200 NVL uses identical form factor; HBM3e upgrade adds negligible mass. Heatsink, backplate, and other categories reduced proportionally. See deep_investigation.md for full derivation.*

---

## 3. Component Breakdown

### GPU Die
- GH100, 814 mm2, 80B transistors, TSMC 4N (identical die to H100)
- Secondary market: $4,500 (known-good die resold for refurbishment/board repair)
- Raw scrap: $0.15

### Memory
- 6 x 24 GB HBM3e 8-Hi stacks (SK Hynix); 144 GB physical, 141 GB advertised
- Individual stack weight: under 1 g per bare stack (~5 mm x 7 mm footprint, ~720 um total height)
- Secondary market: $2,160-$3,000 total ($360-$500/stack). OEM contract pricing: $10-$15/GB per Goldman Sachs (2026), implying $240-$360/stack. Broker markup of 50-100% yields $360-$500. No established spot/broker market exists for individual HBM3e stacks. **Revised from $650/stack ($3,900 total).**
- Raw scrap: $10.80 total ($1.80/stack, Cu microbumps and trace Au)

### Heatsink
- Passive aluminum fins (~500 g) + copper vapor chamber base (~120 g Cu)
- 650 g total (~43% of card)
- Secondary market: $20
- Raw scrap: $5.50 (Al at $3.07/kg, Cu at $12.05/kg)

### VRM / Power Delivery
- Multi-phase (likely 16+ phases) for 600 W TDP; DrMOS ICs, ferrite-core inductors, MLCCs (~400)
- 180 g total
- Secondary market: $45 (component harvesting)
- Raw scrap: $12.00 (Cu windings, ferrite, trace Pd)

### PCB
- ~14-16 layer FR-4 with Ultra Low Loss CCL, ~267 mm x 111 mm
- ~280 g; Cu content ~120 g recoverable
- Secondary market: $15 (donor board)
- Raw scrap: $8.50 (Cu recovery at $12.05/kg + trace gold)

### Connectors
- NVLink bridge connector: Cu + Au plating, ~35 g. Secondary $150, raw scrap $3.00.
- PCIe Gen5 x16 edge connector: Au-plated Cu fingers, ~8 g. Raw scrap $2.00.
- Power connector: likely a single PCIe 16-pin (12VHPWR-style), rated for 600 W. The source CSV listed 2x 8-pin, but the NVIDIA H200 NVL whitepaper references a single 16-pin power connector. Secondary $2.00, raw scrap $0.50.
- Combined secondary: $152. Combined raw scrap: $5.50.

### Other
- TIM (indium-based, ~3 g): raw scrap $1.86 (In at $0.62/g industrial benchmark, corrected from source's $0.50/g)
- Tantalum capacitors (~20 units, ~6 g, ~2 g Ta): raw scrap $0.80 (Ta at $0.40/g, corrected from source's $0.60/g)
- 4 PMICs: secondary $8.00, raw scrap $0.10
- 2 PLL/clock ICs: secondary $5.00, raw scrap $0.05
- 2 NVLink retimer ICs: secondary $25.00, raw scrap $0.10
- 1 EEPROM/flash: secondary $2.00, raw scrap $0.01
- Ferrite beads, misc passives, thermal pads, conformal coating/underfill: raw scrap ~$0.06
- Backplate (Al, 120 g): secondary $2.00, raw scrap $0.37 (Al at $3.07/kg)
- Bracket/shroud (85 g mixed metal): secondary $1.00, raw scrap $0.25
- Raw scrap subtotal (other): ~$3.60

---

## 4. Precious Metals

All prices corrected to actual March 2026 spot rates. The source files used stale mid-2023 prices for gold, silver, and other metals.

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.04 | $144/g | $5.76 | Engineering calculation: PCIe x16 fingers ~0.013 g, NVLink bridge pads ~0.009 g, PCB ENIG pads ~0.009 g, CoWoS substrate pads ~0.001 g, support IC pads ~0.001 g. No wire bonds (Cu pillar bumps). **Revised from 0.40 g based on first-principles ENIG thickness calculation (see deep_investigation.md).** |
| Silver (Ag) | 0.52 | $2.25/g | $1.17 | SAC305 solder (~15g x 3% Ag = 0.45g) + MLCC terminations (~0.07g). **Revised from 0.75g:** a ~1,260g PCIe card has ~15g of SAC305 solder; 3% = 0.45g Ag from solder, +15% for MLCC = ~0.52g. |
| Palladium (Pd) | 0.005 | $45/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.05g (previously reduced from 0.20g). |
| **Total** | | | **$7.16** | |

Additional specialty metals: Copper (~200 g board + heatsink, ~$2.41 total), Tantalum (~2 g, $0.80), Indium (~3 g, $1.86).

---

## 5. Value Cascade

| Scenario | Value | % of MSRP ($37.5K mid) |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $31,000-$40,000 | 83-107% |
| Component salvage (theoretical max) | ~$7,785 | 20.8% |
| Component salvage (realistic, 15-25% yield) | $1,168-$1,946 | 3.1-5.2% |
| Raw material scrap (gross, corrected prices) | ~$49 | 0.1% |
| Recycler payout (net, what you'd receive) | ~$20-$29 | 0.05-0.08% |

*Note: Component salvage revised down from ~$8,865 primarily due to HBM3e stack repricing ($650 -> $430 mid-estimate, -$1,320 total). Raw scrap revised down from ~$101 primarily due to gold content correction (0.40 g -> 0.04 g, -$52).*

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **HBM stack weight [HIGH]:** CSV listed 12 g per stack. An 8-Hi HBM3e stack (~5 mm x 7 mm footprint, ~720 um tall, thin silicon dies at 30-50 um each) likely weighs well under 1 g as a bare stack. The 12 g figure overstates mass substantially and may have included surrounding substrate/packaging material in error.
- **Interposer area [LOW -- original CSV approximately correct]:** CSV stated ~2,500 mm2. This was originally corrected down to ~1,700 mm2 (2x-reticle), but that correction was wrong. SemiAnalysis and TSMC documentation indicate the H100/H200 CoWoS-S package uses a ~3.3x-reticle interposer (~2,831 mm2); the 2x-reticle ~1,700 mm2 interposer was an earlier generation (Broadcom/TSMC 2020 announcement). The IEEE CoWoS-S5 paper documents the 3x-reticle (~2,500 mm2) generation. The CSV's ~2,500 mm2 figure is in the correct range. Impact on scrap values is negligible either way.
- **Power connector [MODERATE]:** CSV listed 2x 8-pin. The NVIDIA H200 NVL whitepaper references a single PCIe 16-pin (12VHPWR) connector, which is rated for 600 W on its own. Report corrected to single 16-pin.
- **HBM3e pricing note contradiction [MODERATE]:** CSV note said "$100/GB at component level" but priced stacks at $650/24 GB = $27/GB. The $100/GB figure appears erroneous. Report uses the $650/stack figure, which is in the plausible range for secondary/broker market pricing.
- **MSRP [LOW-MODERATE]:** Summary stated ~$32,000 per GPU. Multiple sources indicate reseller pricing of $35,000-$45,000. Report uses the broader $35,000-$40,000 range. NVIDIA does not publish official datacenter GPU MSRPs.
- **NVL form factor [MINOR]:** Summary described NVL as exclusively a "pair." The H200 NVL is a single PCIe card that supports both 2-way and 4-way NVLink bridging.
- **PCB layer count [MINOR]:** CSV stated 16 layers. Teardown analysis of PCIe-variant datacenter GPUs suggests 14-16 layers. Report uses "14-16" range.

### Pricing Issues
- **ALL precious metal spot prices stale [CRITICAL]:** Source files used mid-2023 pricing levels. Gold was listed at $2,400/oz ($77/g) vs actual March 2026 of ~$4,500/oz ($144/g) -- an 88% understatement. Silver at $33/oz vs actual ~$70/oz (112% understatement). Copper at $9/kg vs actual $12/kg (33% understatement). All values in this report use corrected March 2026 prices.
- **Secondary market total arithmetic error [MODERATE]:** Summary claimed $8,525. The summary's own breakdown sums to ~$8,865 ($4,500 + $3,900 + $200 + $150 + $45 + $47 + $23). Discrepancy of ~$340. Report uses the corrected ~$8,865 figure.
- **Raw scrap total understated [HIGH]:** Source claimed $107 (arithmetic correct at stale prices). At actual March 2026 spot prices, the corrected raw scrap total is ~$166. The gold repricing alone accounts for ~$56 of the $59 difference.
- **Tantalum price [MINOR]:** Claimed $0.60/g; actual March 2026 ingot price is ~$0.40/g. Impact: -$0.40 per module.
- **Indium price [MINOR]:** Claimed $0.50/g; industrial benchmark is ~$0.55-0.62/g. Impact: +$0.36 per module.

### Web-Search Verification (2026-03-29)

Seven claims checked against public sources (NVIDIA whitepaper, PNY datasheet, SemiAnalysis, Tom's Hardware, AnandTech, IEEE):

| # | Claim | Verdict | Notes |
|---|-------|---------|-------|
| 1 | GH100 die (same silicon as H100) | **Confirmed** | Identical die; H200 is a memory-subsystem refresh, not a die respin. |
| 2 | 6x 24 GB HBM3e 8-Hi = 141 GB usable / 144 GB physical | **Confirmed** | H100 had 6 slots but only 5 active; H200 enables all 6. 3 GB reserved (yield/ECC). |
| 3 | NVL form factor: dual-slot PCIe, NVLink bridge | **Confirmed** | Single wide NVLink bridge per card (unlike H100 NVL which used 3 bridges). 2-way and 4-way supported. |
| 4 | TDP 600 W | **Confirmed** | NVL (PCIe) = 600 W; SXM = 700 W. PNY datasheet, Lenovo product guide, NVIDIA whitepaper all agree. |
| 5 | Single 16-pin 12VHPWR power connector | **Confirmed** | NVIDIA whitepaper specifies "PCIe 16-Pin Power Connector." Tom's Hardware repair article confirms 12VHPWR on H200. CSV had listed 2x 8-pin (already corrected in report). |
| 6 | Card weight ~1,500 g | **Revised to ~1,260 g** | H100 NVL product brief confirms 1,214 g board weight (excl. bracket/bridges). H200 NVL uses identical form factor; HBM3e upgrade adds <1 g. Microless shipping weight 1.45 kg includes packaging. Revised to ~1,260 g (board + bracket). |
| 7 | Interposer ~1,700 mm2 (2x-reticle) | **Incorrect -- reverted** | The report had corrected the CSV's ~2,500 mm2 down to ~1,700 mm2, but this was wrong. SemiAnalysis describes the H100 as using a ~3.3x-reticle interposer (~2,831 mm2). The IEEE CoWoS-S5 paper documents the 3x-reticle (~2,500 mm2) generation. The CSV's original ~2,500 mm2 was approximately correct. Correction reverted above. |

### Deep Investigation (2026-03-29)

Five key unknowns investigated via web research and first-principles engineering calculations. See `deep_investigation.md` for full analysis.

| # | Unknown | Resolution | Impact |
|---|---------|-----------|--------|
| 1 | Card weight (~1,500 g) | **Revised to ~1,260 g** via H100 NVL product brief (1,214 g board) | Low ($0.50-$1 scrap change) |
| 2 | Gold content (0.40 g) | **Revised to 0.04 g** via ENIG thickness calculation | High (-$52 raw scrap) |
| 3 | HBM3e stack price ($650) | **Revised to $360-$500** via Goldman Sachs/Epoch AI OEM data + broker markup | Moderate (-$900-$1,740 component salvage) |

### Confidence Assessment
- Component accuracy: 80/100 (weight derived from H100 NVL product brief; gold corrected by engineering calculation)
- Pricing accuracy: 55/100 (spot prices corrected; HBM3e pricing better sourced but secondary market is opaque)
- Overall confidence in scrap estimate: 70/100

---

## 7. Key Observations

1. **The H200 NVL holds its used value remarkably well** -- trading at $31,000-$40,000 used against a ~$35,000-$40,000 reseller price, reflecting sustained demand for HBM3e capacity before Blackwell supply ramps.
2. **Gold does NOT dominate raw scrap value** (corrected). First-principles ENIG/gold-finger thickness calculations show only ~0.04 g of gold ($5.76), not the 0.40 g ($57.60) previously estimated. Copper (~$2.89) and indium TIM (~$1.86) are comparable contributors. Total raw scrap is ~$49, not ~$101.
3. **The GPU die is the single largest secondary value driver** at $4,500, exceeding the combined HBM3e stack value ($2,160-$3,000 at revised pricing). But bare-die secondary markets are opaque and recovery rates are low.
4. **HBM3e secondary pricing is uncertain.** Goldman Sachs forecasts HBM3e declining from $15/GB to $10/GB in 2026, implying OEM stack costs of $240-$360. A broker markup of 50-100% yields $360-$500/stack, below the original $650 estimate. No established spot/broker market exists for individual HBM3e stacks.
5. **Card weight is ~1,260 g, not ~1,500 g.** The H100 NVL product brief confirms 1,214 g board weight; the H200 NVL uses an identical form factor with negligible mass delta from the memory upgrade.
6. **Practical scrap recovery is extremely low** -- at 15-25% of theoretical secondary value, a $35,000+ card yields $1,168-$1,946 in realistic salvage, and only ~$20-$29 as raw e-scrap to a recycler (40-60% of ~$49 gross).

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Component-by-component ceiling assuming perfect extraction and a willing buyer for every part:

| Component | Theoretical Ceiling | Basis |
|-----------|-------------------|-------|
| GPU die (GH100) | $500-$800 | Shenzhen gray-market donor card value; bare die with no provenance worth far less. Western value ~$0. |
| HBM3e stacks (6x 24 GB) | **$0** | CoWoS-bonded. Individual stacks cannot be separated without destruction. No secondary market exists. Zero listings on any marketplace or broker. |
| GDDR6 chips | N/A | Card uses HBM, not discrete GDDR6. |
| Precious metals (Au 0.04 g, Ag 0.52 g, Pd 0.005 g) | $7.16 | At 100% spot recovery (Mar 2026). Realistic refiner payout is 40-60% of this. |
| VRM components | $30-$60 | Shenzhen harvesting with skilled labor. Western value $0-$15 (labor exceeds recovery). |
| Heatsink / cooler (Al + Cu VC) | $20-$25 | Copper scrap at $5.90/lb + Al scrap. Straightforward mechanical separation. |
| PCB + connectors (incl. NVLink bridge) | $15-$167 | NVLink bridge connector alone $150 secondary (extremely illiquid). PCB donor $15. |
| **Theoretical max total** | **$572-$1,057** | Sum of above ceilings. Requires Shenzhen buyer for die and months to liquidate connectors. |

### 10.2 Realistic US Scrap Value (Grounded Estimate)

- **Option A -- ITAD broker buys dead card whole:** 10-25% of used working price ($31,000-$40,000) = **$3,100-$10,000.** This is the most likely outcome for a dead but intact H200 NVL. Brokers (Net Equity, ALTA Technologies) or Shenzhen-bound repair channels would be the buyers, pricing in the possibility of board-level repair.
- **Option B -- E-waste recycler:** Card weighs ~1,260 g (~2.78 lbs). At $5-$15/lb for server-grade boards = **$14-$42**, plus 60-70% precious metal credit on ~$7 gross PM = **$4-$5 PM credit.** Total: **$18-$47.**
- **Component harvesting is NOT viable in the US.** HBM3e stacks are CoWoS-bonded ($0 separable). The GH100 die requires $100K+ BGA rework stations. VRM desoldering at Western labor rates ($50-100/hr) costs more than the parts are worth.
- **Realistic US scrap range: $18-$47 (recycler) or $3,100-$10,000 (broker/ITAD).** The broker path is overwhelmingly superior and should be the default disposition for any dead H200 NVL.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA H200 Product Page](https://www.nvidia.com/en-us/data-center/h200/) -- official product overview, HBM3e memory upgrade
- [PNY H200 NVL Datasheet](https://www.pny.com/file%20library/company/support/linecards/data-center-gpus/h200-nvl-datasheet.pdf) -- detailed specs, 600W TDP, NVLink bridge support
- [Tom's Hardware H200 Announcement](https://www.tomshardware.com/news/nvidia-h200-gpu-announced) -- product launch context, HBM3e details
- [Lenovo Press NVIDIA H200 141GB](https://lenovopress.lenovo.com/lp1944-nvidia-h200-141gb-gpu) -- server integration, power and thermal specs
- [RunPod H200 Guide](https://www.runpod.io/articles/guides/nvidia-h200-gpu) -- deployment reference and performance context
- Board weight: Exxact retailer shipping weight (~1.45 kg); component-level estimate sums to ~1,500 g
- Precious metal quantities: First-principles engineering calculations using IPC-4552 ENIG thickness specs (0.05-0.20 um), Intel PCIe edge connector gold-finger spec (30 microinch / 0.76 um), measured pad areas, and gold density (19.3 g/cm3). Gold content revised to 0.04 g (from 0.40 g, originally 0.80 g) after detailed per-component ENIG area calculations. No independent assay of H200 NVL exists. See deep_investigation.md for full derivation.
- Recovery rates: 15-25% of theoretical secondary value per e-waste industry literature (WEEE compliance, Urban Mining Institute). 95-99% gold recovery via professional refining.

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report
- **PCB scrap rates:** [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)
- Aluminum $3.07/kg (LME); Indium ~$0.62/g (Shanghai Metals Market); Tantalum ~$0.40/g (Shanghai Metals Market, Metalary)

### HBM3e Pricing
- [Goldman Sachs via @Jukanlosreve](https://x.com/Jukanlosreve/status/1988063459448418377) -- HBM3E $15/GB -> $10/GB forecast for 2026
- [TrendForce: Samsung, SK Hynix ~20% HBM3E Price Hike](https://www.trendforce.com/news/2025/12/24/news-samsung-sk-hynix-reportedly-plan-20-hbm3e-price-hike-for-2026-as-nvidia-h200-asic-demand-rises/)
- [Epoch AI: NVIDIA B200 Cost Breakdown](https://epoch.ai/data-insights/b200-cost-breakdown) -- HBM3e at $14-17/GB, ~$362/stack at OEM level

### Gold Content Engineering References
- [ENIG Gold Thickness Standards (IPC-4552)](https://www.protoexpress.com/kb/enig/) -- 0.05-0.23 um gold layer
- [PCB ENIG Cost Calculation](https://sqpcb.com/pcb-enig-cost-calculation-exact-gold-cost-total-expense/) -- gold weight per m^2 methodology
- [Sierra Circuits: Gold Fingers](https://www.protoexpress.com/kb/gold-fingers/) -- 30 microinch (0.76 um) minimum on edge connectors
- [TechInsights: NVIDIA H100 CoWoS-S Flip Chip BGA](https://www.techinsights.com/blog/nvidia-h100-hopper-tsmc-cowos-s-flip-chip-ball-grid-array) -- confirms copper pillar flip-chip (no gold wire bonds)

### Secondary Market
- JarvisLabs, ThunderCompute, TRG Datacenters, IntuitionLabs for used card pricing
- No transparent public market exists for bare GH100 dies or HBM3e stacks

### Verification Sources (2026-03-29 web search)
- [NVIDIA H200 NVL Whitepaper](https://www.inhosted.ai/doc/hopper-h200-nvl-whitepaper.pdf) -- single 16-pin power connector, 600 W TDP, NVLink bridge details
- [Tom's Hardware: H200 12VHPWR repair](https://www.tomshardware.com/pc-components/gpus/busted-12vhpwr-connector-sidelines-usd30-000-h200-hopper-gpu-repair-technician-saves-the-data-center-day-by-fixing-power-port) -- confirms 12VHPWR connector on H200 NVL
- [SemiAnalysis: AI Capacity Constraints](https://semianalysis.com/2023/07/05/ai-capacity-constraints-cowos-and/) -- H100 as 7-die CoWoS-S package, interposer multiple reticles in size
- [AnandTech: TSMC 2x Reticle CoWoS](https://www.anandtech.com/show/15582/tsmc-broadcom-develop-1700-mm2-cowos-interposer-2x-larger-than-reticles) -- 1,700 mm2 is the 2x-reticle generation (pre-H100)
- [IEEE: CoWoS-S5 2,500 mm2](https://ieeexplore.ieee.org/document/9501649/) -- 3x-reticle interposer documentation
- [NVIDIA H100 NVL Product Brief](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/h100/PB-11773-001_v01.pdf) -- H100 NVL board weight 1,214 g (excluding bracket/bridges)
- [Spheron: H100 vs H200](https://www.spheron.network/blog/nvidia-h100-vs-h200/) -- confirms identical GH100 die in both products
- [AnandTech: H200 at SC23](https://www.anandtech.com/show/21136/nvidia-at-sc23-h200-accelerator-with-hbm3e-and-jupiter-supercomputer-for-2024) -- 6th HBM stack enabled, 141 GB / 144 GB physical
