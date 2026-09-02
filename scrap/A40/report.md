# NVIDIA A40 -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe
**TDP:** 300W
**MSRP:** ~$27,500 OEM | **Used (Mar 2026):** $5,000-$6,500

---

## 1. Card Overview

The NVIDIA A40 is a dual-slot, full-height, full-length passively cooled datacenter GPU based on the full GA102 die (Ampere generation). It targets professional visualization, AI inference, and virtual desktop workloads, delivering 10,752 CUDA cores and 48GB GDDR6 ECC memory at 300W TDP.

| Attribute | Value |
|-----------|-------|
| GPU die | GA102-895 (Samsung 8nm LPP) |
| Die area | 628 mm2 |
| Transistors | 28.3 billion |
| Memory | 48 GB GDDR6 ECC (24x 2GB clamshell) |
| Memory bus | 384-bit |
| Interconnect | NVLink (112.5 GB/s bidirectional, 2-slot bridge) |
| TDP | 300 W |
| Board weight | 1,010 g incl. bracket (NVIDIA product brief PB-09976-001_v08) |
| Packaging | Standard flip-chip BGA |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (copper vapor chamber base + Al fin stack) | 690 | 68% |
| PCB (est. 8-10 layer FR-4) | 120 | 12% |
| VRM (inductors + MOSFETs + caps) | 65 | 6% |
| GPU die + package substrate | 28 | 3% |
| Memory (24x GDDR6 chips) | 29 | 3% |
| Connectors + bracket | 41 | 4% |
| Other (solder, TIM, passives, misc) | 37 | 4% |
| **Total** | **~1,010** | **--** |

Note: The NVIDIA product brief (PB-09976-001_v08) lists board weight as 990g excluding bracket and extenders. The bracket with screws adds 20g, giving 1,010g total. Long offset extender adds 48g; straight extender adds 32g (neither included in totals here). The heatsink is integrated into the passive card and is included in the 990g board weight. Component weights are estimates; individual items were adjusted so the column sums to ~1,010g. No public A40 teardown with per-component weighing exists.

---

## 3. Component Breakdown

### GPU Die
- GA102-895, 628 mm2, 28.3B transistors, Samsung 8nm LPP
- Full uncut die: 7 GPCs, 84 SMs, 10,752 CUDA cores
- Secondary market: ~$150 (reballing/rework for board repair)
- Raw scrap: ~$0.85 (trace gold from flip-chip BGA pads, ~0.005g Au)

### Memory
- 24x 2GB (16Gbit) GDDR6 chips, clamshell configuration (12 front + 12 back)
- Micron or Samsung (varies by production batch), 14.5 Gbps per pin
- 384-bit bus (12 channels x 32-bit, two chips per channel)
- Secondary market: ~$84 total (~$3.50/chip x 24)
- Raw scrap: ~$1.68 total (trace Au in BGA pads per chip)
- Correction: Original BOM listed 12x 4GB (32Gbit) chips, but 32Gbit GDDR6 was not commercially available in 2020-2021. Samsung's highest-density GDDR6 at the time was 16Gbit (K4ZAF325BM series). Clamshell layout confirmed by RTX 3090 and TITAN Ada precedents.

### Heatsink
- Passive dual-slot copper vapor chamber base with aluminum fin stack
- ~690g (68% of card weight); revised down from 750g to fit 990g board weight
- Aluminum fin stack ~490g, copper vapor chamber + any supplementary heatpipes ~200g
- Vapor chamber confirmed via RTX A6000 cross-reference: sealed copper plates with deionized water working fluid and sintered copper wicking (Tom's Hardware / Quasarzone investigation, Oct 2023). A40 and A6000 share the same GA102 die, 48GB GDDR6, 300W TDP, and near-identical reference PCB.
- Secondary market: ~$15 (replacement heatsink)
- Raw scrap: ~$3.18 (Al 490g at $0.55/lb = $0.59; Cu 200g at $5.90/lb = $2.60; totals rounded)
- Correction: Original claimed $4.28 scrap but itemized Al + Cu did not sum to that. Revised with corrected weights. Copper fraction increased slightly (200g vs 190g) after confirming vapor chamber construction.

### VRM / Power Delivery
- Estimated 14-18 total phases across multiple voltage rails (NVVDD, MSVDD, FBVDDQ), unconfirmed without teardown. The RTX 3090 FE (GA102, 350W) uses 10+6+4=20 phases (igor's LAB); the Quadro RTX 6000 (TU102, 295W) uses 12+3=15 phases. The A40 at 300W likely falls in between.
- Power stages (likely MPS MP86957 or similar Smart Power Stages), inductors, PWM controller ICs (likely MPS MP2888A or similar), input/output capacitors
- Secondary market: ~$3.85 (component harvesting for board repair)
- Raw scrap: ~$0.27 (copper from inductor windings, aluminum from caps)
- Note: Previous estimate of "12+2" used a simple GPU+memory split that omits the MSVDD (miscellaneous/SoC) voltage rail found on all Ampere GA102 designs.

### PCB
- Est. 8-10 layer FR-4, 267x112mm (NVIDIA product brief confirmed dimensions). The 12-layer backdrill requirement identified by igor's LAB applies specifically to GDDR6X cards (RTX 3080/3090) due to PAM4 signaling demands. The A40 uses standard GDDR6 (NRZ, 14.5 Gbps), which has significantly less stringent signal integrity requirements and does not mandate 12-layer boards.
- ~120g total (revised down from 180g; typical GPU PCBs of this size are 100-130g)
- Cu content ~24g (~20% by weight of 120g)
- Secondary market: ~$5 (donor board)
- Raw scrap: ~$0.31 (24g Cu at $5.90/lb)
- Correction: Original calculated PCB copper scrap as $1.04 using $13.05/lb, but $13.05 is the per-kg price mislabeled as per-lb. Weight also revised from 180g to 120g. Layer count revised from "12+" to "est. 8-10" after determining the 12-layer requirement is GDDR6X-specific.

### Connectors
- PCIe 4.0 x16 gold fingers: ~1-2 micron Au over Ni, est. 0.020-0.025g Au, scrap ~$3.40
- 8-pin EPS12V power: copper/tin, scrap ~$0.05
- 3x DisplayPort 1.4a: gold-plated pins, ~0.003g Au each, scrap ~$0.18
- NVLink bridge connector: gold-plated pins, scrap ~$0.08
- Secondary market: ~$2.25 total (replacement parts)

### Other
- I/O bracket: steel/nickel, 20g (NVIDIA spec), scrap ~$0.02
- Thermal pads: silicone/ceramic, no value
- Misc SMD passives (~100): resistors, ferrite beads, ESD diodes, scrap ~$0.01
- Solder (SAC305): ~12g lead-free (96.5% Sn, 3% Ag, 0.5% Cu), scrap ~$0.60
- VBIOS EEPROM (8 Mbit): present on PCB, negligible value
- Frame Lock / Stereo connector headers: present, negligible value

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.06 | $145/g | $8.70 | PCIe fingers (~0.023g), connectors (~0.012g), GPU BGA pads (~0.005g), PCB ENIG pads/vias (~0.020g) |
| Silver (Ag) | 0.40 | $2.18/g | $0.87 | SAC305 solder (3% Ag of 12g = 0.36g), plus trace in PCB |
| Palladium (Pd) | 0.002 | $45.50/g | $0.09 | Trace in MLCC capacitors (post-2020 BME, minimal Pd) |
| **Total** | | | **$9.66** | |

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $5,000-$6,500 | 18-24% |
| Component salvage (theoretical max) | ~$260 | 0.9% |
| Component salvage (realistic) | ~$50-$100 | 0.2-0.4% |
| Raw material scrap (gross) | ~$14 | 0.05% |
| Recycler payout (net, what you'd receive) | ~$6-$8 | 0.02-0.03% |

Notes on values:
- Component salvage theoretical max increased from ~$220 to ~$260 after correcting memory chip count from 12 to 24 (adds ~$42 in secondary value).
- Raw material scrap corrected from $17.78 to ~$14 after fixing copper $/lb vs $/kg unit error and heatsink scrap arithmetic.
- Recycler payout assumes 40-60% of gross scrap value after processing costs and refiner margins.

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **Memory chip count and density [CRITICAL]:** Claimed 12x 4GB (32Gbit) GDDR6 chips. Corrected to 24x 2GB (16Gbit) GDDR6 in clamshell configuration. 32Gbit GDDR6 was not commercially available when the A40 launched (2020-2021). Samsung's highest density was 16Gbit (K4ZAF325BM). This doubles chip count, total memory weight (~29g vs ~14g), and aggregate secondary value (~$84 vs ~$42).
- **MSRP [CRITICAL]:** Original listed "$5,000 (NVIDIA)" as the launch price. This is the current used market price, not the original list price. OEM channel pricing was ~$27,500 (Cisco UCSC-GPU-A40 at ~$27,561; Lenovo ~EUR 26,526). NVIDIA does not publish MSRP for datacenter GPUs.
- **Card weight double-count [MODERATE]:** Original claimed ~1,810g "with full heatsink assembly," implying the 990g board weight excluded the heatsink. Per NVIDIA PB-09976-001_v08, the 990g board weight already includes the integrated passive heatsink. Total card + bracket = 1,010g.
- **VRM phase count [MINOR]:** 12+2 phase is a reasonable estimate but unconfirmed. No public A40 VRM teardown exists.
- **Missing components [MINOR]:** VBIOS EEPROM (8 Mbit), Frame Lock/Stereo connector headers, temperature sensor ICs, and auxiliary voltage regulators (LDOs) were omitted from the original BOM. All have negligible scrap value.

### Pricing Issues
- **Copper scrap unit error [CRITICAL]:** Document states copper is $5.90/lb ($13.01/kg) but calculates scrap values using $13.05/lb -- confusing the per-kg price with per-lb. This roughly doubles all copper scrap contributions. Corrected copper total: ~$3.25 (at $5.90/lb) vs. claimed ~$7.19.
- **Heatsink scrap arithmetic [MODERATE]:** Claimed $4.28 but itemized Al ($0.67) + Cu ($2.60) = $3.27 only. The $1.01 gap is unexplained.
- **Tin spot price [MINOR]:** Claimed $19.80/kg; actual LME tin in March 2026 was ~$42-43/kg. Impact on total is small (~$0.28 difference on 12g of solder).
- **Raw material total [CRITICAL]:** Claimed $17.78 theoretical max. After correcting copper unit error and heatsink math: ~$14. Gold ($8.70) remains the dominant scrap material by value.

### Confidence Assessment
- Component accuracy: 76/100 (up from 72 -- heatsink type confirmed, PCB layers corrected, VRM better characterized)
- Pricing accuracy: 60/100 (unchanged -- corrections have negligible scrap value impact)
- Overall confidence in scrap estimate: 70/100 (up from 65)
- See `deep_investigation.md` for full research notes and sources.

---

## 7. Key Observations

1. **Working resale dominates all recovery paths.** A functioning A40 at $5,000+ makes teardown for parts or scrap economically irrational unless the card is confirmed dead. The scrap-to-MSRP ratio is ~0.05%.

2. **Gold is the single most valuable scrap material.** At ~0.06g worth ~$8.70 gross, gold (mostly in PCIe fingers) accounts for roughly 60% of the corrected raw material scrap value. Yet this is less than one-thousandth of a troy ounce.

3. **The heatsink is the heaviest component but contributes little scrap value.** At ~690g (68% of card weight), the passive aluminum/copper heatsink yields only ~$3.05 in scrap because aluminum trades at ~$0.55/lb.

4. **Copper is the most abundant valuable base metal** (~230g across heatsink, PCB, and inductors), but at $5.90/lb its total contribution is ~$3.00 -- less than half the gold value despite being ~3,800x heavier.

5. **The memory correction has meaningful impact on component salvage.** Correcting from 12 to 24 chips adds ~$42 in theoretical secondary value and nearly doubles the memory's weight contribution, though the absolute scrap value change is small (~$0.84).

6. **A recycler would realistically pay $6-$8** for a dead A40, factoring in processing costs, transport, and refiner margins (40-60% of ~$14 gross).

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA A40 Product Brief](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a40/NVIDIA%20A40%20Product%20Brief.pdf) -- architecture overview, board weight (PB-09976-001_v08, 990g board + 20g bracket)
- [NVIDIA A40 Datasheet](https://images.nvidia.com/content/Solutions/data-center/a40/nvidia-a40-datasheet.pdf) -- detailed specs, memory configuration, TDP
- [VideoCardz A40](https://videocardz.net/nvidia-a40) -- board layout, GA102-895 die reference
- [GPU Poet A40](https://gpupoet.com/gpu/learn/card/nvidia-a40) -- specs and pricing reference
- Component verification: NVIDIA GA102 Architecture Whitepaper V2.0/V2.1, Samsung/Micron GDDR6 datasheets (K4ZAF325BM 16Gbit series), ServeTheHome, Lenovo ThinkSystem Product Guide, Anandtech, RTX A6000 teardown references
- Recovery rates: 40-60% of theoretical gross for professional e-waste refining
- OEM pricing: Cisco UCSC-GPU-A40 (~$27,561), Lenovo (~EUR 26,526)

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report
- **PCB scrap rates:** [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)
- **GDDR6 pricing:** [Tom's Hardware](https://www.tomshardware.com/news/gddr6-vram-prices-plummet) | [igor'sLAB](https://www.igorslab.de/en/gpu-prices-could-rise-at-the-beginning-of-2026-because-the-cost-of-gddr-memory-will-increase-significantly/)
- Aluminum scrap $0.55/lb (Rockaway Recycling, Mar 2026); Tin ~$43/kg (LME via Trading Economics)

### Secondary Market
- eBay sold listings (Mar 2026)
- GetDeploying.com (~$5,050 avg from 38 listings)
- GPUnex

---

## 9. External Verification (2026-03-29)

Web searches conducted for "NVIDIA A40 teardown," "A40 PCB," GA102-895 specifications, and related queries. No public teardown with bare-PCB photos of the A40 specifically was found. The RTX A6000 (identical GA102 die, same 48GB/384-bit memory) has a disassembly guide on Linus Tech Tips that serves as the closest physical reference.

| Claim | Verdict | Source / Notes |
|-------|---------|----------------|
| 24x 2GB (16Gbit) GDDR6, clamshell (12+12) | **Confirmed** | GA102 has 12x 32-bit memory controllers. 48GB / 2GB = 24 chips, two per channel. Clamshell layout consistent with RTX A6000 disassembly and RTX 3090 precedent. 32Gbit GDDR6 was unavailable at launch. |
| GA102-895 die | **Confirmed** | NVIDIA product brief, VideoCardz (Device ID 0x2235), ServeTheHome, GPU Poet all agree. |
| Board weight 990g + 20g bracket = 1,010g | **Confirmed** | PB-09976-001_v08: board 990g excl. bracket/extenders; bracket w/ screws 20g; long offset extender 48g; straight extender 32g. |
| 3x DisplayPort 1.4a | **Confirmed** | Product brief, datasheet, Lenovo product guide, ServeTheHome all list 3x DP 1.4a. Disabled by default (display-off mode for vGPU). |
| NVLink: single 2-slot bridge, 112.5 GB/s bidir | **Confirmed** | Product brief: 3rd-gen NVLink, 2-slot span, 112.5 GB/s bidirectional, scales to 96GB across two cards. |
| Heatsink is copper vapor chamber | **Confirmed (cross-ref)** | RTX A6000 (same GA102, 48GB GDDR6, 300W) confirmed to use copper vapor chamber via Quasarzone/Tom's Hardware investigation (Oct 2023). A40 shares near-identical reference PCB. Vapor chamber is sealed copper with deionized water and sintered copper wicking. |
| Heatsink ~68% of weight (~690g) | **Plausible, consistent** | No teardown with per-component weighing exists. 990g board - ~310g non-heatsink components = ~680g, consistent with 690g estimate. |
| VRM phase count | **Revised: est. 14-18 total** | No public A40 VRM teardown. Previous "12+2" estimate omitted MSVDD rail. RTX 3090 FE (GA102, 350W) uses 20 phases across 3 rails (igor's LAB). Quadro RTX 6000 (TU102, 295W) uses 15 phases. A40 at 300W likely in between. |
| PCB layer count | **Revised: est. 8-10 layers** | Previous "12+" was based on RTX 3090 FE, but igor's LAB confirmed 12-layer backdrill is required specifically for GDDR6X (PAM4 signaling). A40 uses GDDR6 (NRZ), which has lower signal integrity requirements. |

### Weight breakdown revision
The previous weight table summed to ~1,130g (750+180+80+28+29+41+22), overshooting the 990g board + 20g bracket by 120g. Heatsink revised to 690g, PCB to 120g, VRM to 65g, and "Other" absorbs the remainder. These are still estimates; a physical teardown would be required for exact values.

### Deep investigation (2026-03-29)
Four specific unknowns were researched via web search and cross-referencing platform peers (RTX A6000, RTX 3090 FE, Quadro RTX 6000, RTX A4000). Results:
1. **Heatsink type:** Confirmed copper vapor chamber via RTX A6000 teardown cross-reference (Tom's Hardware/Quasarzone). Copper/aluminum weight split adjusted slightly (200g Cu / 490g Al).
2. **VRM phases:** Revised from "12+2" to "est. 14-18 total" across NVVDD, MSVDD, and FBVDDQ rails. Multi-rail architecture confirmed across all GA102 peers.
3. **PCB layers:** Revised from "12+" to "est. 8-10." The 12-layer backdrill requirement (igor's LAB) is specific to GDDR6X; the A40 uses GDDR6.
4. **Heatsink weight (690g):** Confirmed plausible by subtraction (990g board - ~310g components = ~680g).
Net scrap value impact of all changes: less than $0.25. Overall confidence raised from 65 to 70.

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Assumes every component is perfectly extracted and sold to the highest-value buyer globally.

| Component | Ceiling Value | Notes |
|-----------|--------------|-------|
| GA102 die | $150 | Shenzhen gray-market donor; no liquid Western market for bare dies |
| GDDR6 chips (24x) | $84 | $3.50/chip; AliExpress repair market exists but is thin |
| Heatsink (Cu/Al) | $15 | Replacement heatsink; or ~$3.18 as raw Cu/Al scrap |
| VRM components | $3.85 | Component harvesting; labor cost exceeds value in US |
| PCB (donor board) | $5 | Board-level repair shop |
| Connectors | $2.25 | PCIe fingers + DP + NVLink |
| **Total** | **~$260** | |

The A40 uses standard flip-chip BGA packaging (no CoWoS, no HBM), so the die is theoretically removable with professional BGA rework equipment. However, the GA102 die has near-zero value outside the Shenzhen gray market -- Western repair shops buy whole dead cards, not bare dies.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator actually receives for a dead A40:

**Option A -- Sell dead card to ITAD broker:** At 10-25% of used working price ($5,000-$6,500), expect **$500-$1,625**. The A40's standard BGA packaging and GDDR6 (not HBM) make it more repairable than CoWoS cards, pushing broker offers toward the higher end of the range.

**Option B -- E-waste recycler by weight:** Card weighs ~1,010g (~2.23 lb). At $5-15/lb server PCB rate: $11-$33 base. PM assay credit at 60-70% recovery on ~$9.66 gross precious metals adds ~$6-$7. Total: **$17-$40**.

Component harvesting (die removal, VRAM desoldering) is not viable in the US. Western labor rates ($50-100/hr) exceed the recoverable value of all harvestable parts combined.

**Realistic range: $500-$1,625** (broker, Option A preferred) or **$17-$40** (recycler, last resort).
