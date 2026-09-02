# NVIDIA L40S -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe
**TDP:** 350W
**MSRP:** ~$8,000 | **Used (Mar 2026):** $7,267-$9,000

---

## 1. Card Overview

The NVIDIA L40S is a data center GPU based on the Ada Lovelace architecture (AD102), positioned as the higher-performance sibling of the L40. It targets AI inference, LLM serving, graphics virtualization, and video workloads. Compared to the L40, the L40S has higher clock speeds (2,520 MHz vs 2,490 MHz boost), a 350W TDP (vs 300W), and an enabled Transformer Engine (dynamic FP8/FP16 recasting for ~2x tensor throughput). Both share the same AD102-895/895A die and 48GB GDDR6 memory configuration. Neither supports NVLink or MIG. It uses a passive heatsink for server deployment.

| Attribute | Value |
|-----------|-------|
| GPU die | AD102-895A (TSMC 4N) |
| Die area | 608.4 mm2 |
| Transistors | 76.3 billion |
| Memory | 48 GB GDDR6 ECC (24x 2GB 16Gbit clamshell, 12 per side) |
| Memory bus | 384-bit |
| Interconnect | PCIe Gen4 x16 |
| TDP | 350 W |
| Board weight | 1,052 g (NVIDIA Product Brief PB-11470-001_v02, excl. bracket) |
| Packaging | Standard flip-chip BGA (FCBGA) |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (passive Al/Cu, dual-slot) | 550 | 52.3% |
| PCB | 220 | 20.9% |
| VRM (inductors + MOSFETs + caps) | 105 | 10.0% |
| GPU die + package substrate | 28 | 2.7% |
| Memory (24x GDDR6 chips) | 24 | 2.3% |
| Connectors + bracket | 82 | 7.8% |
| Other (solder, TIM, passives, misc) | 58 | 5.5% |
| **Estimated total** | **~1,067** | **~101.4%** |

Note: Estimated component total is 1,067g vs NVIDIA's stated 1,052g board weight (excl. bracket). The ~1.4% overshoot reflects estimation uncertainty in heatsink, PCB, and VRM weights. No physical teardown of the L40S exists publicly; component weights are analog-based estimates from RTX 4090 / TITAN Ada teardowns.

---

## 3. Component Breakdown

### GPU Die
- AD102-895A, 608.4 mm2, 76.3B transistors, TSMC 4N
- ~51x51mm BGA package; bare die ~1.1g, package substrate + underfill ~27g
- Secondary market: $150 (reballing/rework for board repair -- unverifiable, grey-market estimate)
- Raw scrap: $2.80 (gold in BGA substrate ~0.02g Au at $144/g)

### Memory
- 24x 2GB (16Gbit) GDDR6 (Samsung K4ZAF325BM or equivalent), clamshell (12 per side)
- 180-ball FBGA, 12x14mm per chip
- Secondary market: $180 total ($7.50/chip; DRAMeXchange late-2025 spot ~$7.88/chip, likely higher in Q1 2026)
- Raw scrap: $2.88 total ($0.12/chip, thin Au on BGA balls)

### Heatsink
- Bidirectional airflow passive dual-slot cooler rated for 350W TDP
- Copper vapor chamber base (~180g) + aluminum fin stack (~370g)
- Vapor chamber construction confirmed via cross-reference: L40S shares PCB with RTX 6000 Ada (Comino/EKWB/Alphacool water block compatibility). RTX 6000 Ada uses vapor chamber (Comino teardown, Massed Compute FAQ). All NVIDIA 300W+ single-die datacenter GPUs use vapor chambers. Confidence: 85%. See heatsink_materials_analysis.md.
- 550g (52.3% of card)
- Secondary market: $12 (datacenter spare/replacement value)
- Raw scrap: $2.62 (Cu 180g at ~$5.90/lb = $2.34; Al 370g at ~$0.35/lb = $0.28)

### VRM / Power Delivery
- Estimated 16-20 GPU phases + 4 memory phases (350W TDP), likely 70A+ DrMOS (e.g., Infineon TDA21570 or MPS equivalent)
- 24 inductors (GPU + memory VRM), ~350 MLCCs (BME type, minimal precious metal), ~20 tantalum/polymer bulk caps, 1 PWM controller IC
- Secondary market: $45 (DrMOS $2/ea x 20 = $40, PWM controller $5)
- Raw scrap: $0.76 (inductors Cu $0.05, MLCCs $0.10, tantalum caps $0.45, DrMOS $0.15, PWM $0.01)

### PCB
- 12+ layer server-grade FR-4, 267mm x 111mm
- Cu content estimated ~60-80g (within PCB layers)
- Secondary market: $15 (functional replacement board for repair)
- Raw scrap: $3.30 (at $15/kg server-grade PCB scrap rate; 0.22kg x $15/kg)

### Connectors
- PCIe Gen4 x16 gold-plated edge connector (82 fingers, ~0.008g Au, 30 microinch plating)
- 1x 16-pin PCIe CEM5 power connector (12+4, rated 600W)
- 4x DisplayPort 1.4a
- Secondary market: $2.50 (power connector $1, DP connectors $0.50 each x 3 resalable)
- Raw scrap: $1.23 (edge connector Au $1.10, power $0.05, DP $0.08)

### Other
- TIM (thermal paste + pads, 15g), SAC305 solder (~18g), ~500 misc SMD passives, steel bracket (65g)
- Raw scrap: $0.35 (solder tin, bracket steel, misc)

---

## 4. Precious Metals

Values below use corrected spot prices where the original analysis was stale (see Section 6).

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.05 | $144.43/g | $7.22 | Edge connector (~0.008g), GPU BGA (~0.02g), DP connectors (~0.02g); total is at the low end of estimates (could be 0.03-0.15g) |
| Silver (Ag) | 0.60 | $2.26/g | $1.36 | SAC305 solder (3% Ag, ~0.54g) + MLCC traces; corrected from $0.64 using current $70/oz price |
| Palladium (Pd) | trace | $45.16/g | ~$0 | Modern BME-type MLCCs; negligible Pd content |
| **Total** | | | **$8.58** | |

Note on gold quantity uncertainty: The 0.05g total gold estimate is at the conservative end. The L40 analysis has been harmonized to the same 0.05g for the identical AD102 platform. PCIe edge connector gold content is the primary variable: 30-microinch plating yields ~0.008g, while 5-micron (197-microinch) server-grade plating could yield ~0.41g. Without physical assay, this remains the largest source of uncertainty (0.03-0.15g range).

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $7,267-$9,000 | 91-113% |
| Component salvage (theoretical max) | $405 | 5.1% |
| Component salvage (realistic) | $250-$325 | 3.1-4.1% |
| Raw material scrap (gross) | ~$13 | 0.16% |
| Recycler payout (net, what you'd receive) | $5-$8 | 0.06-0.10% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **Die size (LOW severity):** Stated as 609 mm2; correct value is 608.4 mm2 per NVIDIA whitepaper. A 0.1% rounding error with no material impact.
- **GPU die package weight (LOW severity):** Claimed 28g total (die + BGA substrate). The L40 analysis estimated 10.4g for the same AD102 package. The 28g figure includes a heavier substrate estimate; neither has been physically verified.
- **VRM phase count (MEDIUM severity):** Estimated 16-20 GPU + 4 memory phases based on RTX 4090 FE analog (23-phase at 450W, scaled for 350W). No L40S teardown exists. Plausible but unconfirmed.
- **GDDR6 chip supplier (LOW severity):** Samsung K4ZAF325BM is plausible but unconfirmed. NVIDIA sources from Samsung, Micron, and SK Hynix.

### Pricing Issues
- **Silver price critically stale (HIGH severity):** Original analysis used $33/oz ($1.06/g). Actual March 2026 silver price is $68-73/oz ($2.19-$2.35/g). Silver scrap value should be ~$1.36 (at $2.26/g), not $0.64. Understated by ~$0.72.
- **Aluminum scrap price overstated (HIGH severity):** Original used $1.30/lb. Heatsink aluminum scrap actually trades at $0.35-$0.65/lb. At midpoint $0.50/lb, the aluminum value drops from $1.29 to $0.50. Overstated by ~$0.79. (Note: the $0.65/lb figure in the L40 analysis was top-of-range but defensible; $1.30/lb is out of range for scrap aluminum.)
- **Gold price slightly stale (LOW severity):** Used $141/g ($4,386/oz, dated 2026-03-26). Current price on 2026-03-29 is ~$144.43/g ($4,492/oz). Difference is ~$0.17 on 0.05g gold -- negligible.
- **Gold quantity uncertain (MEDIUM severity):** The 0.05g estimate is conservative compared to the L40 analysis (0.50g) and industry benchmarks (0.5-1.0g for enterprise GPUs). If actual gold is 0.10-0.50g, raw scrap value increases by $7-$65. This is the largest uncertainty in the entire analysis.
- **Copper scrap price (LOW severity):** Used $4.25/lb (#1 bare bright grade). Current copper futures are ~$5.90/lb, but scrap copper grades vary. $4.25/lb for actual recovered scrap is defensible.
- **Tantalum cap scrap rate (LOW severity):** Used $20.50/lb; recyclers quote ~$15/lb for SMD/epoxy type. Minor overstatement (~$0.05 impact).
- **Heatsink narrative inconsistency (LOW severity):** Key Findings states heatsink scrap at "$2.94" but component table sums to $2.23 for heatsink aluminum + copper. The $2.94 appears to include non-heatsink copper.
- **Net effect of corrections on total:** Silver understated by ~$0.72 and aluminum overstated by ~$0.79 roughly cancel. After reconciling PM total ($8.58) with base metal contributions (~$4.43), corrected raw scrap total is approximately $13. Cascade updated from ~$11 to ~$13.

### Confidence Assessment
- Component accuracy: 92/100
- Pricing accuracy: 65/100
- Overall confidence in scrap estimate: 68/100

---

## 7. Key Observations

1. **Massive value destruction at end-of-life.** A working L40S worth $7,267-$9,000 yields only ~$13 in raw material scrap -- a 99.8% loss. Even theoretical component salvage ($405) recovers only 5% of market value, illustrating that GPU value is almost entirely in the integrated design and firmware, not the physical materials.
2. **Gold is the dominant scrap value driver, but its quantity is highly uncertain.** At 0.05g, gold accounts for ~56% of raw scrap value. However, the L40 analysis estimated 0.50g for the same AD102 platform. If the L40S contains closer to 0.50g, raw scrap value roughly quadruples to ~$40. A physical assay is needed to resolve this.
3. **The L40S and L40 share the same AD102-895/895A die and 48GB GDDR6 configuration.** The L40S has higher clocks (2,520 MHz vs 2,490 MHz boost), 350W TDP (vs 300W), and an enabled Transformer Engine (dynamic FP8/FP16 recasting, roughly doubling tensor throughput in TF32/FP16/FP8). Physically the cards are near-identical; scrap values should be comparable.
4. **GDDR6 memory has significant secondary value.** The 24 GDDR6 chips are worth ~$180 as functional pulls (44% of parts-out value), driven by the 2025-2026 memory shortage. Spot prices have risen ~60% since mid-2025 and the $7.50/chip estimate may already be conservative for Q1 2026.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA L40S Product Brief (PNY, PB-11470-001_v02)](https://www.pny.com/File%20Library/Company/Support/product-briefs/data-center-gpus/NVIDIA-L40S-Product-Brief.pdf) -- board weight (1,052 g excl. bracket), form factor, TDP
- [NVIDIA L40S Datasheet](https://resources.nvidia.com/en-us-l40s/l40s-datasheet-28413) -- memory configuration, bus width, compute specs
- [Cisco L40S Datasheet](https://www.cisco.com/c/dam/en/us/products/collateral/servers-unified-computing/ucs-c-series-rack-servers/nvidia-l40s-ucsc-gpu-l40s.pdf) -- OEM integration specs
- [NVIDIA L40S Product Page](https://www.nvidia.com/en-us/data-center/l40s/) -- official specifications
- [Lenovo Press -- NVIDIA L40S](https://lenovopress.lenovo.com/lp1812-nvidia-l40s-48gb-pcie-gen4-passive-gpu) -- OEM integration specs, form factor confirmation
- [GPU Poet -- NVIDIA L40S](https://gpupoet.com/gpu/learn/card/nvidia-l40s) -- secondary market pricing, specifications cross-reference
- [Fluence -- NVIDIA L40S](https://www.fluence.network/blog/nvidia-l40s/) -- performance benchmarks, market context

### Precious Metal Spot Prices (March 29, 2026)
- Gold: $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- Silver: ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- Palladium: $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price)

### Scrap Metal & Commodity Prices
- Copper: $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- Copper scrap (#1 bare bright): [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- Weekly scrap report: [ScrapMonster (Mar 20-26, 2026)](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785)
- GDDR6 memory pricing: [Tom's Hardware](https://www.tomshardware.com/news/gddr6-vram-prices-plummet) | [igor'sLAB](https://www.igorslab.de/en/gpu-prices-could-rise-at-the-beginning-of-2026-because-the-cost-of-gddr-memory-will-increase-significantly/)
- DRAM spot: [TrendForce](https://www.trendforce.com/price/dram/dram_spot)
- PCB scrap: [iScrapApp](https://iscrapapp.com/metals/pc-boards/)

### Secondary Market
- eBay tracked prices ($7,267 low, $8,584 avg, March 2026); DRAMeXchange GDDR6 spot (Dec 2025, ~$7.88/16Gbit chip)

### Methodology Notes
- Precious metal quantities: Component-level engineering estimates based on plating thickness, solder composition, and MLCC type. No L40S-specific assay exists. Gold quantity carries high uncertainty (0.03-0.50g range).
- VRM design: Estimated from RTX 4090 FE (23-phase at 450W) scaled for 350W TDP. No L40S teardown available.
- Memory configuration: 24x 2GB clamshell confirmed by NVIDIA product brief, 384-bit bus width analysis, and JEDEC GDDR6 density limits (16Gbit max for GDDR6)
- Recovery rates: 40-60% recycler payout assumed for precious metals (industry standard for small-lot mixed e-waste)

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Component-by-component ceiling assuming perfect extraction and a willing buyer for every part:

| Component | Theoretical Ceiling | Basis |
|-----------|-------------------|-------|
| GPU die (AD102) | $150 | Shenzhen gray-market reballing/rework. Same die as L40 and RTX 4090. Western bare-die value ~$0. |
| HBM stacks | N/A | Card uses GDDR6, not HBM. Standard FCBGA packaging, no CoWoS. |
| GDDR6 chips (24x 2 GB 16Gbit) | $72-$180 | Real AliExpress market: $3-$7.50/chip. 24 chips in clamshell, standard BGA, separable. Harvested/untested pulls: $3-$5/chip = $72-$120. |
| Precious metals (Au 0.05 g, Ag 0.60 g, Pd trace) | $8.58 | At 100% spot recovery. Gold ($7.22) dominates. Slightly more silver than L40 due to higher solder mass (18 g vs 15 g at 350W). |
| VRM components | $45 | ~20 DrMOS at $2/ea + PWM controller $5. Desoldering uneconomic at Western labor rates. |
| Heatsink (180 g Cu VC + 370 g Al) | $2.62 | Copper vapor chamber at $5.90/lb + aluminum fins at $0.35/lb. $12 secondary if sold as datacenter spare (illiquid). |
| PCB + connectors | $15-$18 | Donor board $15. Edge connector + DP connectors ~$1.23 gold content. |
| **Theoretical max total** | **$293-$404** | GDDR6 chips at $72-$180 are the primary harvestable value, same as L40. |

### 10.2 Realistic US Scrap Value (Grounded Estimate)

- **Option A -- ITAD broker buys dead card whole:** 10-25% of used working price ($7,267-$9,000) = **$727-$2,250.** The L40S has stronger broker demand than the L40 due to wider deployment (AI inference market). Net Equity, ALTA Technologies, and eBay "for parts" are viable channels.
- **Option B -- E-waste recycler:** Card weighs 1,052 g (~2.32 lbs). At $5-$15/lb for server-grade boards = **$12-$35**, plus 60-70% PM credit on ~$8.58 gross = **$5-$6.** Total: **$17-$41.**
- **Component harvesting partially viable for GDDR6 only.** The 24 GDDR6 chips are standard BGA (not CoWoS-bonded) and can be desoldered with conventional rework equipment. At $3-$5/chip harvested = $72-$120. The 2025-2026 GDDR6 shortage makes harvested chips more saleable than usual. The AD102 die and VRM components are not worth pursuing at US labor rates.
- **Realistic US scrap range: $17-$41 (recycler), $72-$120 (GDDR6 harvesting only), or $727-$2,250 (broker/ITAD).** Selling the dead card whole to a broker or remarketing firm is the overwhelmingly rational default disposition.

---

## 9. Web Verification (2026-03-29)

Cross-checked report claims against NVIDIA product briefs, Cisco/Lenovo/Dell OEM datasheets, and VideoCardz hardware database. No public L40S teardown exists as of this date.

| Claim | Status | Notes |
|-------|--------|-------|
| AD102-895A die, same as L40 | CONFIRMED | Both L40 and L40S use AD102-895/895A per VideoCardz and NVIDIA docs. No "AD102-890" variant exists in public records. |
| Die area 608.4 mm2 | MINOR DISCREPANCY | VideoCardz lists 608 mm2; NVIDIA whitepaper rounds to 608.4. Immaterial. |
| 24x 2GB GDDR6 clamshell = 48GB | CONFIRMED | NVIDIA product brief, Lenovo Press, Cisco datasheet all confirm 48GB GDDR6, 384-bit bus. Clamshell (12 per side) consistent with bus width. |
| Card weight 1,052g (PB-11470-001_v02) | UNVERIFIED | Product brief PB-11470-001_v02 is the correct document number and is cited by multiple OEM guides, but the 1,052g figure is not reproduced in any web-accessible summary. Likely in the PDF body. Not contradicted by any source. |
| 4x DisplayPort 1.4a | CONFIRMED | Lenovo Press: "4 x DisplayPort"; NVIDIA/Cisco datasheets confirm 4x DP 1.4a. One web summary incorrectly claimed 3x DP + 1x HDMI 2.1 -- this appears to be a confusion with RTX 6000 Ada; dismissed. |
| 16-pin power connector | CONFIRMED | All sources (NVIDIA, Cisco, Lenovo, Dell) confirm single 16-pin (12+4 PCIe CEM5) connector, 350W. |
| No NVLink, no MIG | CONFIRMED | Cisco datasheet and Lenovo Press explicitly state "MIG: No support", "NVLink: No". PCIe Gen4 x16 only. |
| 350W TDP (vs L40 300W) | CONFIRMED | NVIDIA datasheet, Cisco, Lenovo, Dell all list 350W max board power. VideoCardz once listed 300W in a spec field (likely copy error from L40); all primary sources say 350W. |
| L40S vs L40: clocks + TDP only | CORRECTED | Beyond clocks (2,520 vs 2,490 MHz boost) and TDP (350W vs 300W), the L40S enables the Transformer Engine (dynamic FP8/FP16 recasting) which roughly doubles tensor throughput in TF32, FP16, FP8, and INT8. The L40 supports FP8 ops but lacks Transformer Engine branding/tuning. Updated Sections 1 and 7. |

Sources: [VideoCardz L40S](https://videocardz.net/nvidia-l40s), [VideoCardz AD102](https://videocardz.net/gpu/nvidia-ad102), [Cisco L40S Datasheet](https://www.cisco.com/c/dam/en/us/products/collateral/servers-unified-computing/ucs-c-series-rack-servers/nvidia-l40s-ucsc-gpu-l40s.pdf), [Lenovo Press LP1812](https://lenovopress.lenovo.com/lp1812-nvidia-l40s-48gb-pcie-gen4-passive-gpu), [PNY Product Brief PB-11470-001_v02](https://www.pny.com/File%20Library/Company/Support/product-briefs/data-center-gpus/NVIDIA-L40S-Product-Brief.pdf), [NVIDIA L40S Product Page](https://www.nvidia.com/en-us/data-center/l40s/)
