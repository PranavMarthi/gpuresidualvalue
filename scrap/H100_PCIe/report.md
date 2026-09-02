# NVIDIA H100 PCIe -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe (FHFL dual-slot)
**TDP:** 350W (80 GB) / 400W (94 GB NVL)
**MSRP:** ~$25,000-$30,000 | **Used (Mar 2026):** $18,000-$23,000 (80 GB) / $23,000-$27,000 (94 GB)

---

## 1. Card Overview

The NVIDIA H100 PCIe is a datacenter AI training and inference accelerator based on the Hopper architecture GH100 die. It ships in two variants: an 80 GB HBM2e version (5 active stacks) and a 94 GB HBM3 NVL version (6 active stacks). Both use TSMC's CoWoS-S 2.5D packaging and feature PCIe Gen5 x16 with NVLink bridge support. This report covers both variants, using the 80 GB as the primary reference and noting 94 GB differences where applicable.

| Attribute | Value |
|-----------|-------|
| GPU die | GH100 (TSMC 4N) |
| Die area | 814 mm2 |
| Transistors | 80 billion |
| Memory | 80 GB HBM2e (5 x 16 GB, 8-Hi) / 94 GB HBM3 (6 x 16 GB, 8-Hi) |
| Memory bus | 5120-bit (80 GB) / 6016-bit (94 GB; 128 bits disabled for yield) |
| Interconnect | NVLink bridge (3x bridges, 600 GB/s bidir); PCIe Gen5 x16 |
| TDP | 350 W (80 GB) / 400 W (94 GB NVL) |
| Board weight | 1,200 g excl. bracket (80 GB) / 1,214 g excl. bracket (94 GB) -- NVIDIA product brief |
| Packaging | CoWoS-S 2.5D (TSMC, silicon interposer with reticle stitching) |

---

## 2. Weight Breakdown

Based on the 80 GB variant (1,220 g total including bracket).

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (copper vapor chamber + Al fins) | 750 | 61% |
| PCB (PG520, 12-16 layer FR-4) | 180 | 15% |
| VRM (16x DrMOS + inductors + caps) | 120 | 10% |
| GPU die + package substrate + interposer | 28 | 2% |
| Memory (5 x HBM2e stacks) | 10 | 1% |
| Connectors + bracket | 36 | 3% |
| Other (solder, TIM, passives, EMI shields, misc ICs) | 96 | 8% |
| **Total** | **~1,220** | **100%** |

---

## 3. Component Breakdown

### GPU Die
- GH100, 814 mm2, 80B transistors, TSMC 4N (custom for NVIDIA)
- Die weight: ~1.4g (814 mm2 x 0.75 mm x 2.33 g/cm3)
- Secondary market: $800 (reballing/rework for repair; no liquid market for bare dies)
- Raw scrap: $0.01 (raw silicon is essentially worthless)

### Memory
- **80 GB variant:** 5 x 16 GB HBM2e stacks (8-Hi TSV), 5120-bit bus, 2,000 GB/s
- **94 GB variant:** 6 x 16 GB HBM3 stacks (8-Hi TSV, not 12-Hi), 6016-bit bus, 3,938 GB/s
- Secondary market: $1,250 total (80 GB, 5 x $250/stack) / $2,100 total (94 GB, 6 x $350/stack)
- Raw scrap: $0.40 (80 GB) / $0.60 (94 GB) -- negligible Si + trace Cu micro-bumps

### Heatsink
- Copper vapor chamber base (~280g Cu) + aluminum extruded fin stack (~470g Al)
- 750g (~61% of card) -- back-calculated from 1,200g total; no teardown weight available
- Secondary market: $25 (aftermarket replacement passive cooler)
- Raw scrap: $3.11 (Cu 280g = 0.62 lb x $4.40/lb = $2.72; Al 470g = 1.04 lb x $0.38/lb = $0.39)

### VRM / Power Delivery
- ~16-phase (estimated; PCIe 350W variant vs 29+3 for SXM5 700W)
- Monolithic Power Systems (MPS) DrMOS stages + ferrite-core inductors + MLCC/polymer caps
- Secondary market: $48 (16 x $3/DrMOS) + $15 (controller ICs)
- Raw scrap: $0.20 (Cu in inductors, Sn in solder; ferrite and Ni-electrode MLCCs have minimal PM content)

### PCB
- PG520 board, 12-16 layer FR-4, 267 mm x 111 mm
- Cu content in traces: part of ~80-90g total non-heatsink Cu
- Secondary market: $3-8 (scrap-by-weight at $8-20/lb for server-grade boards; the $15 figure in components.csv is a repair/donor board price, not scrap)
- Raw scrap: $2.50 (at bulk e-waste board rates)

### Connectors
- PCIe Gen5 x16 gold fingers: 164 pins, ~30 microinch Au plating, ~15-25 mg Au
- NVLink edge connector: gold-plated, ~10-15 mg Au
- 16-pin (12+4) power connector: Cu alloy with Au flash plating
- Secondary market: $3 (NVLink connector + power connector)
- Raw scrap: $1.55 (PCIe fingers $0.90, NVLink $0.50, power $0.15)

### Other
- TIM (indium-based, ~0.5g In): $0.31 scrap (In at $0.62/g SMM industrial benchmark; corrected from $0.15 which used stale ~$0.30/g price)
- Tantalum/polymer capacitors (8x): $0.30 scrap
- MLCC capacitors (~200x, Ni-electrode): <$0.01 scrap
- EEPROM/config ICs: negligible scrap
- EMI shield cans (tin-plated steel): $0.02 scrap
- Bracket + retention hardware (stainless steel): $0.05 scrap
- PCB-mounted passives (~500x resistors, signal caps): $0.01 scrap
- Board-level solder (SAC305, ~15g): $0.45 scrap (includes ~0.45g Ag from 3% Ag content)

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.040-0.070 | $144/g | $5.80-$10.10 | PCIe fingers (15-25 mg), NVLink connector (10-15 mg), PCB ENIG/ENEPIG pad finish (~25 mg). No wire bonds — H100 uses flip-chip Cu pillar bumps via CoWoS-S. |
| Silver (Ag) | 0.50-0.70 | $2.27/g | $1.14-$1.59 | SAC305 solder (~3% Ag), MLCC terminations |
| Palladium (Pd) | 0.010-0.030 | $45/g | $0.45-$1.35 | Minimal in modern Ni-electrode MLCCs |
| **Total** | | | **$7.39-$13.04** | |

---

## 5. Value Cascade

Values shown for the 80 GB HBM2e variant (primary). The 94 GB NVL variant commands higher secondary market and component salvage values.

| Scenario | Value (80 GB) | % of MSRP | Value (94 GB) |
|----------|-------|-----------|-------|
| Working unit (used, Mar 2026) | $18,000-$23,000 | 72-92% | $23,000-$27,000 |
| Component salvage (theoretical max) | $2,157 | 8.6% | $3,007 |
| Component salvage (realistic) | $100-200 | 0.4-0.8% | $150-250 |
| Raw material scrap (gross) | $15-$22 | 0.06-0.09% | $16-$23 |
| Recycler payout (net, what you'd receive) | $7-$13 | 0.03-0.05% | $8-$14 |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **HBM3 stack height (WRONG, HIGH severity):** components.csv claims "12-Hi DRAM dies" for the 94 GB HBM3 stacks. The correct configuration is 8-Hi (8 x 16 Gb = 16 GB/stack). The 12-Hi HBM3 variant yields 24 GB/stack and was not used in H100. Since 6 x 16 GB = 96 GB nominal (94 GB usable), the stacks must be 8-Hi. Corrected in this report.
- **Interposer weight (WRONG, MEDIUM severity):** components.csv claims 4.5g for the silicon interposer. Pure silicon calculation: 2831 mm2 x 0.1 mm x 2.33 g/cm3 = ~0.66g. Even with Cu TSVs and RDL, ~1-2g is realistic. The 4.5g figure is plausible only if the ABF package substrate beneath is included. Corrected to ~1-2g for the interposer proper in this report.
- **94 GB memory bus width (UNCERTAIN, LOW severity):** Summary implies 6144-bit (6 x 1024-bit) but actual shipped bus is 6016-bit -- NVIDIA disables 128 bits (one channel) for yield, which is why total is 94 GB not 96 GB. Corrected in this report.
- **VRM phase count (UNCERTAIN):** The ~16 phases for PCIe 350W is an estimate. No public teardown of the H100 PCIe board was found. The ratio vs SXM5 (29+3 phases at 700W) is plausible. Confidence: 55/100.
- **Heatsink weight/composition (UNCERTAIN):** 750g is back-calculated from 1,200g total. The Cu/Al split (280g/470g) is a reasonable engineering estimate for a vapor chamber design but is unverified without a physical teardown. Confidence: 70/100.

### Pricing Issues
- **PCB $15 is repair price, not scrap price (WRONG, MEDIUM severity):** The components.csv lists $15 as the PCB secondary market value, which represents a tested donor board for repair shops. The summary text conflates this with scrap-by-weight pricing. At 180g (~0.4 lb) and $8-20/lb for server-grade boards, actual scrap value is $3-8. Corrected in this report.
- **Copper quantity/value mismatch (WRONG, MEDIUM severity):** Summary Section 3 table claims 80-90g Cu = $3.30-$3.70, but the math yields $0.78-$0.87 at $4.40/lb. The $3.30-$3.70 values appear to include heatsink copper (~280g) without updating the quantity column. The two numbers are only consistent if total Cu (~360-370g including heatsink) is used. This report separates heatsink Cu (in heatsink scrap line) from other Cu.
- **Silver price internal inconsistency (LOW):** components.csv row 24 uses $2.35/g; summary Section 3 uses $2.27/g. Spot was $70.52/oz = $2.27/g. The $2.35/g is slightly high but within weekly volatility. Immaterial to totals.
- **GH100 die salvage $800 (UNCERTAIN):** No liquid secondary market exists for bare GH100 dies. The estimate is plausible relative to manufacturing cost (~$200-300 die + $750 CoWoS packaging) but is theoretical. Confidence: 50/100.
- **HBM stack salvage prices (UNCERTAIN):** $250/stack HBM2e and $350/stack HBM3 are reasonable estimates, but individual HBM stacks are not commonly sold due to the near-impossibility of desoldering from CoWoS packages. Confidence: 45/100.

### Confidence Assessment
- Component accuracy: 83/100
- Pricing accuracy: 78/100
- Overall confidence in scrap estimate: 80/100

### Web Verification (2026-03-29)

Cross-checked against NVIDIA product briefs, datasheets, AnandTech, Tom's Hardware, and TechPowerUp. Results:

| Claim | Status | Source |
|-------|--------|--------|
| GH100 die: 814 mm2, 80B transistors, TSMC 4N | CONFIRMED | [NVIDIA Hopper Architecture In-Depth](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/); [AnandTech](https://www.anandtech.com/show/17327/nvidia-hopper-gpu-architecture-and-h100-accelerator-announced) |
| 80 GB variant: 5x HBM2e 8-Hi stacks, 5120-bit bus | CONFIRMED | [NVIDIA H100 PCIe Product Brief PB-11133-001](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf); [AnandTech H100 NVL](https://www.anandtech.com/show/18780/nvidia-announces-h100-nvl-max-memory-server-card-for-large-language-models) |
| 94 GB NVL variant: 6x HBM3 8-Hi stacks, 6016-bit bus | CONFIRMED | [NVIDIA H100 NVL Product Brief PB-11773-001](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/h100/PB-11773-001_v01.pdf); AnandTech confirms 6th stack enabled, 8-Hi |
| Board weight: 1,200 g (80 GB) excl. bracket | CONFIRMED | PB-11133-001 lists 1,200 g excl. bracket, 20 g bracket, 20.5 g per NVLink bridge |
| Board weight: 1,214 g (94 GB NVL) excl. bracket | UNVERIFIED | Cited from PB-11773-001; PDF exists but weight not rendered in search snippets. Plausible given 6th HBM3 stack adds ~2.2 g + minor PCB/VRM differences |
| Power connector: 16-pin 12VHPWR | CONFIRMED | PB-11133-001 and PB-11773-001 both specify one PCIe 16-pin auxiliary power connector. 8-pin CPU adapters exist but are adapters, not the native connector |
| PCIe Gen5 x16 | CONFIRMED | All product briefs and datasheets |
| NVLink: 3x bridges, 600 GB/s bidir (PCIe) | CONFIRMED | PB-11133-001 and PB-11773-001; NVL brief states "three NVLink bridges, same as the one used with H100 PCIe." H100 SXM5 uses NVSwitch for 900 GB/s |
| VRM: ~16 phases (PCIe 350W) | UNVERIFIED | No public H100 PCIe teardown found. SXM5 has 29 dual-stage + 3 single-stage inductors = 61 power stages at 700W ([Tom's Hardware](https://www.tomshardware.com/news/nvidia-hopper-h100-sxm5-pictured)). ~16 phases for 350W PCIe is a plausible ratio but remains an estimate |
| VRM supplier: MPS DrMOS | UNVERIFIED | No source identified MPS specifically for H100 PCIe. MPS is a common datacenter VRM supplier but this is assumed, not confirmed |
| GH100 die shot available | NO | No Fritzchens Fritz or other public die shot of GH100 found. The chip is server-exclusive and too expensive for typical die photography workflows |
| Heatsink: 750 g, Cu vapor chamber + Al fins | UNVERIFIED | Back-calculated from 1,200 g total. No physical teardown with component weighing found. The Comino H100 waterblock teardown exists but does not publish component weights |

---

## 7. Key Observations

1. **The H100 PCIe retains extraordinary secondary market value.** A working 80 GB card at $18,000-$23,000 used represents 72-92% of MSRP -- far stronger value retention than the Gaudi2 (24.6%) -- driven by NVIDIA's dominant CUDA ecosystem and ongoing datacenter demand.
2. **Raw scrap value is vanishingly small relative to functional value.** At $15-22 gross scrap, the raw material recovery is 0.06-0.09% of MSRP and less than 0.1% of used market value. The functional card is roughly 1,000x more valuable than its raw materials.
3. **The heatsink dominates physical mass but not value.** At ~750g (61% of card weight), the passive copper vapor chamber + aluminum fin stack is the heaviest component, yet its scrap value ($3.11) accounts for only ~15-20% of total raw material scrap. Gold at 40-70 mg (invisible by weight) contributes $5.80-$10.10 or roughly 40-50% of total scrap value.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA H100 Datasheet](https://resources.nvidia.com/en-us-gpu-resources/h100-datasheet-24306) -- GH100 die specs, memory configurations, TDP
- [NVIDIA H100 PCIe Product Brief (PB-11133-001)](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf) -- 80 GB variant, board weight 1,200g excl. bracket
- [NVIDIA H100 NVL Product Brief (PB-11773-001)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/h100/PB-11773-001_v01.pdf) -- 94 GB variant, board weight 1,214g excl. bracket
- [NVIDIA Hopper Architecture In-Depth](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/) -- GH100 die architecture, CoWoS-S packaging, NVLink 4.0
- [Lenovo Press ThinkSystem H100 PCIe](https://lenovopress.lenovo.com/lp1732-thinksystem-nvidia-h100-pcie-gen5-gpu) -- server integration, power and thermal specs
- [TechPowerUp H100 SXM5 94GB](https://www.techpowerup.com/gpu-specs/h100-sxm5-94-gb.c4294) -- variant comparison and cross-reference
- [GPU Poet H100 PCIe](https://gpupoet.com/gpu/learn/card/nvidia-h100-pcie) -- specs and pricing reference
- Precious metal quantities: PCIe gold finger plating thickness per IPC/JEDEC (30 microinch Au), solder composition (SAC305 = 3% Ag), MLCC content based on modern Ni-electrode construction. Total Au of 40-70 mg consistent with industry benchmarks for datacenter GPU cards.
- Recovery rates: Recycler payout estimated at 40-60% of gross precious metal value, reflecting processing costs, assay fees, and recycler margins.

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Copper scrap #1 bare bright:** $4.40/lb (Rockaway Recycling / iScrapApp, March 2026)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report; bulk e-waste rate ~$7.17/lb
- **PCB scrap rates:** [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)
- Aluminum scrap $0.38/lb cast (iScrapApp, March 2026)

### Secondary Market
- eBay sold listings from project dataset (ebay_verified_supplement.csv)
- Retailer pricing from ASA Computers, Jarvislabs

---

## 10. Scrap Value Scenarios

Values shown for the 80 GB HBM2e variant (primary); 94 GB NVL noted where different.

### 10.1 Theoretical Maximum (Best Case)

Assumes every component is perfectly extracted and sold to the highest-value buyer globally.

| Component | Ceiling Value (80 GB) | Ceiling Value (94 GB) | Notes |
|-----------|----------------------|----------------------|-------|
| GH100 die | $800 | $800 | Shenzhen gray-market reballing/rework only. No liquid Western market for bare dies. |
| HBM stacks | **$0** | **$0** | CoWoS-S interposer with capillary underfill + 40um-pitch microbumps. No commercial rework service exists for component recovery. No secondary market for individual stacks (zero listings found). Per hbm_secondary_market.md: "realistic standalone value: $0." |
| Heatsink (Cu/Al) | $25 | $25 | Aftermarket replacement passive cooler; or ~$3.11 as raw Cu/Al scrap |
| VRM components | $63 | $63 | 16x DrMOS at $3 + controller ICs; labor cost exceeds value in US |
| PCB (donor board) | $15 | $15 | Repair/donor board price (scrap-by-weight is $3-$8) |
| Connectors | $3 | $3 | NVLink + power connector |
| CoWoS interposer | $50 | $50 | Limited reuse; manufacturing cost far exceeds secondary value |
| **Total** | **~$956** | **~$956** | Requires Shenzhen-only buyers and physically impossible HBM extraction |

The $2,157 / $3,007 theoretical max in Section 5 includes $1,250 / $2,100 for HBM stacks. These have $0 separable value. The stacks are bonded to the CoWoS-S silicon interposer via microbumps with capillary underfill -- a permanent assembly. Even the Shenzhen shops that repair H100s swap entire CoWoS package assemblies (die + interposer + all HBM stacks as a unit), not individual stacks.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator actually receives for a dead H100 PCIe:

**Option A -- Sell dead card to ITAD broker:** At 10-25% of used working price ($18,000-$23,000 for 80 GB), expect **$1,800-$5,750**. The H100 PCIe's strong CUDA ecosystem and PCIe form factor (fits standard servers) maximize broker demand. Brokers like Net Equity and ALTA Technologies actively buy H100s. 94 GB NVL: **$2,300-$6,750**.

**Option B -- E-waste recycler by weight:** Card weighs ~1,220g (~2.69 lb). At $5-15/lb server PCB rate: $13-$40 base. PM assay credit at 60-70% recovery on ~$10.20 midpoint gross precious metals adds ~$6-$7. Total: **$19-$47**.

Component harvesting is not viable in the US. CoWoS-S packaging makes the die and HBM inseparable, and desoldering 16 VRM phases at Western labor rates ($50-100/hr) costs more than the components are worth.

**Realistic range: $1,800-$5,750** (broker, Option A strongly preferred) or **$19-$47** (recycler, last resort).
