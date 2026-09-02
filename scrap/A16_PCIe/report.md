# NVIDIA A16 PCIe -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe
**TDP:** 250W
**MSRP:** ~$5,000 (unverified) | **Used (Mar 2026):** $2,800-$4,300

---

## 1. Card Overview

The NVIDIA A16 is a multi-GPU datacenter card carrying four independent GA107-890 dies on a single PCB, designed for high-density VDI (virtual desktop infrastructure) workloads rather than AI/ML training. Each GA107 provides 1,280 CUDA cores and 16 GB of GDDR6 on a 128-bit bus (64 GB total across the card). An NVIDIA/Mellanox ConnectX-6 PCIe switch aggregates the four GPUs behind a single PCIe Gen4 x16 upstream link.

| Attribute | Value |
|-----------|-------|
| GPU die | GA107-890 x4 (Samsung 8nm / 8N) |
| Die area | ~200 mm2 per die |
| Transistors | ~8.7 billion per die |
| Memory | 64 GB GDDR6 (32 x 2 GB chips, 8 per GPU) |
| Memory bus | 128-bit per GPU |
| Interconnect | PCIe Gen4 x16 (via ConnectX-6 switch) |
| TDP | 250 W |
| Board weight | 1,088 g (NVIDIA product brief, excl. bracket) |
| Packaging | Standard flip-chip BGA (x4 GPU sites) |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (passive aluminum extrusion) | 680 | 62.5% |
| PCB | 220 | 20.2% |
| VRM (inductors + MOSFETs + caps) | 220 | 20.2% |
| GPU die + package substrate (x4) | 44 | 4.0% |
| Memory (32 GDDR6 chips) | 26 | 2.4% |
| Connectors + bracket | 34 | 3.1% |
| Other (solder, TIM, passives, misc) | 64 | 5.9% |
| **Total** | **~1,088** | **100%** |

---

## 3. Component Breakdown

### GPU Die
- 4x GA107-890, ~200 mm2 each, ~8.7B transistors, Samsung 8nm (8N)
- Secondary market: $100 total ($25/die, reballing/rework for RTX 3050-class boards)
- Raw scrap: $1.40 (trace gold on BGA pads, ~$0.35/die)

### Memory
- 32 x 2 GB Samsung GDDR6 (K4ZAF325BM or equivalent, FBGA-180, 14x12 mm)
- Secondary market: $480 total ($15/chip, AliExpress floor price; $20-25 on eBay)
- Raw scrap: $2.56 (trace Au on BGA pads)

### Heatsink
- Passive aluminum extrusion (~650g) with copper contact pads at each GPU site (~30g total, 4x ~7.5g)
- Vapor chamber unlikely: four distributed GA107 dies at ~62.5W each make single VC impractical (would need to span ~200mm). Individual VCs per GPU site cost-prohibitive at 62.5W. Most likely design is aluminum extrusion with localized copper pads. Confidence: 55%. See heatsink_materials_analysis.md.
- 680g (62.5% of card)
- Secondary market: $8
- Raw scrap: $0.89 (Al 650g at $0.77/kg = $0.50; Cu 30g at ~$5.90/lb = $0.39)

### VRM / Power Delivery
- ~6+2 phases per GPU (estimated, no teardown data), 24 core + 8 memory stages
- Inductors (32), MOSFETs (32), capacitors (~232)
- Secondary market: $23.20 (component harvesting)
- Raw scrap: $1.32

### PCB
- Multi-layer FR-4, ~267 x 112 mm
- Cu content ~77g (PCB layers) + ~32g (inductors) = ~120g total board copper
- Secondary market: $5 (donor board)
- Raw scrap: $1.76

### Connectors
- PCIe x16 gold fingers (164 contacts), 8-pin EPS power connector, ConnectX-6 PCIe switch
- Secondary market: $10.75 ($0.50 PCIe fingers + $0.25 EPS connector + $10 switch IC)
- Raw scrap: $0.35

### Other
- TIM (thermal paste/pads), misc passives (~300), CEC1712 security chip (some SKUs), 4x PWM controller ICs, mounting bracket
- Secondary market: $9 ($8 voltage controllers + $1 CEC chip)
- Raw scrap: $0.02

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.25 | $144/g | $36.00 | PCIe fingers ~0.04g, 4x GPU BGA ~0.04g, 32x GDDR6 pads ~0.01g, PCB vias/traces ~0.16g |
| Silver (Ag) | 0.58 | $2.25/g | $1.31 | SAC305 solder (~17g x 3% Ag = 0.51g) + MLCC terminations (~0.07g). **Revised from 0.80g:** original included "traces" which use copper, not silver. A 1,088g PCIe card with 4 GPU BGA sites and 32 GDDR6 chips has ~15-20g of SAC305 solder; 3% of ~17g = 0.51g Ag, +15% for MLCC = ~0.58g. |
| Palladium (Pd) | 0.005 | $45/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.02g. |
| **Total** | | | **$37.54** | |

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $2,800-$4,300 | 56-86% |
| Component salvage (theoretical max) | $636 | 12.7% |
| Component salvage (realistic, 50% recovery) | $318 | 6.4% |
| Raw material scrap (gross) | $40 | 0.8% |
| Recycler payout (net, what you'd receive) | $16-$24 | 0.3-0.5% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **PCIe switch identity [WRONG, high severity]:** Originally described as "PLX/Mellanox switch." Corrected to NVIDIA/Mellanox ConnectX-6 PCIe switch. PLX is a Broadcom product line and is unrelated to the A16's on-board switch. Confirmed via Dell firmware (MT94X) and HPE firmware listings.
- **Vapor chamber claim [UNCERTAIN, medium severity]:** Heatsink originally described as having "vapor-chamber base plates." No public teardown or NVIDIA documentation confirms this. NVIDIA product brief says only "passively cooled with a superior thermal design." Corrected to "passive aluminum extrusion (internal construction unverified)."
- **GDDR6 part number [UNCERTAIN, low severity]:** Samsung K4ZAF325BM-HC14 is a plausible candidate (correct density, speed grade, package) but NVIDIA does not disclose DRAM vendor per board SKU. Actual chips may be Samsung, Micron, or SK Hynix depending on production batch. Reported as "K4ZAF325BM or equivalent."
- **VRM layout [UNCERTAIN, low severity]:** 6+2 phase count per GPU is a reasonable estimate for ~62.5W per GPU subsystem but no teardown data exists. Confidence ~40%.

### Pricing Issues
- **China-sourced eBay pricing [WRONG, high severity]:** Originally claimed $600-$1,500. Current March 2026 listings start at ~$2,800. The $600-$1,500 range reflects stale 2024-2025 pricing. Corrected to $2,800+.
- **Enterprise refurbished pricing [UNCERTAIN, medium severity]:** Originally claimed $800-$2,000. Current refurbished listings start at $3,599. Range appears to understate current market by $1,000-$2,000. Removed from working unit range.
- **Gold spot price [CORRECT, minor]:** $141/g was at the low end of March 2026 range ($142-$145/g). Updated to $144/g for current spot.
- **MSRP [UNCERTAIN, low severity]:** ~$5,000 figure is unverifiable from public sources. NVIDIA does not publicly list datacenter GPU MSRPs.
- **Tin price [UNCERTAIN, low severity]:** $32/kg is ~25% below LME ($42-43/kg) but plausible as a solder scrap recovery price.

### Web Verification (2026-03-29)

Six claims were checked against public sources. Findings:

1. **4x GA107 dies -- CONFIRMED.** ServeTheHome quick-look photos show the double-width card and a diagram of the four GPU sites. No bare-PCB teardown with exposed dies was found publicly; the heatsink was not removed in any published review. Die count (4x GA107-890) is confirmed by NVIDIA product brief (PB-10518-001), datasheet, VideoCardz, and Lenovo Press.

2. **32x GDDR6 chips (8 per GPU) -- CONFIRMED (spec-level).** NVIDIA datasheet lists 4x 16 GB GDDR6 on 128-bit bus per GPU. At 2 GB/chip this requires 8 chips per GPU (32 total). No published photo shows the memory chips directly (heatsink not removed in any public source).

3. **PCIe switch is ConnectX-6 -- CONFIRMED.** Dell firmware listing (driver ID MT94X) is titled "Nvidia Ampere A16 GPU ConnectX-6 PCIe Switch Firmware." HPE lists the same package as "NVIDIA-A16-PCIe-switch-CX-6-firmware." This is a Mellanox/NVIDIA ConnectX-6 silicon used in a PCIe switching role (not as a NIC). The earlier "PLX/Mellanox" label in components.csv was wrong; corrected in this pass. PLX is a Broadcom product line unrelated to the A16.

4. **Power connector is 8-pin EPS (CPU-style) -- CONFIRMED.** NVIDIA product brief (Table 7) specifies "CPU 8-pin power connector on the east edge of the board." ServeTheHome photos show the "data center 8-pin power connector" at the rear. This is an EPS-12V 8-pin, not a standard PCIe 8-pin -- the keying differs and EPS supports up to 300W vs 150W for PCIe 8-pin. Report and CSV are correct.

5. **Board weight 1,088g -- CONFIRMED.** NVIDIA product brief (PB-10518-001_v02/v03) states "Board: 1088 Grams (excluding bracket and extenders)." Bracket adds 20g, long offset extender 64g, straight extender 39g. The report correctly cites the product brief and notes "excl. bracket."

6. **Heatsink construction -- PARTIALLY RESOLVED.** No public teardown removes the heatsink. NVIDIA product brief says only "passively cooled with a superior thermal design." Determination: most likely aluminum extrusion with copper contact pads at each GPU site (~30g Cu total). Vapor chamber impractical for four distributed GA107 dies at ~62.5W each -- would need to span ~200mm across all four sites. Confidence 55%. See heatsink_materials_analysis.md.

**CSV corrections applied:** (a) heatsink note updated to remove vapor-chamber claim; (b) switch chip renamed from "PLX/Mellanox" to "ConnectX-6" with Dell/HPE firmware citation.

### Confidence Assessment
- Component accuracy: 75/100
- Pricing accuracy: 72/100
- Overall confidence in scrap estimate: 73/100

---

## 7. Key Observations

1. **GDDR6 chips dominate part-out value.** The 32 memory chips represent ~75% of the $636 theoretical part-out value. Samsung K4ZAF325BM-class GDDR6 chips are actively sought for GPU VRAM upgrades and ASIC miner repairs at $15-25 each.
2. **16x gap between part-out and raw scrap.** Secondary market component resale (~$636) is roughly 16x the raw material scrap value (~$40), making component harvesting the only economically sensible salvage path.
3. **Heatsink dominates weight, not value.** The aluminum heatsink is 62.5% of card mass but contributes less than $1 in scrap and only $8 in secondary market value.
4. **Multi-GPU design complicates repair economics.** A single-GPU failure renders the card partially functional but potentially unsuitable for enterprise VDI use, pushing it toward part-out.
5. **VDI niche faces steeper depreciation** than AI/ML accelerators. As enterprises shift to cloud-hosted virtual desktops, physical A16 hardware faces limited demand -- though March 2026 pricing ($2,800-$4,300) remains surprisingly strong.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA A16 Product Brief](https://images.nvidia.com/content/Solutions/data-center/vgpu-a16-product-brief.pdf) -- 4x GA107 architecture, VDI workload targeting, 250W TDP
- [NVIDIA A16 Datasheet](https://images.nvidia.com/content/Solutions/data-center/vgpu-a16-datasheet.pdf) -- detailed specs, memory configuration, board weight (PB-10518-001_v02, 1,088g excl. bracket)
- [VideoCardz A16](https://videocardz.net/nvidia-a16) -- board layout and configuration reference
- [VideoCardz GA107 GPU](https://videocardz.net/gpu/nvidia-ga107) -- die details, Samsung 8nm (8N) process
- [Lenovo Press ThinkSystem A16](https://lenovopress.lenovo.com/lp1815-thinksystem-nvidia-a16-64gb-gen4-pcie-passive-gpu) -- server integration, thermal and power specs
- Precious metal quantities: Engineering estimates from BGA pad plating thickness, PCIe gold finger plating (30 microinch), PCB via plating, solder alloy composition; cross-referenced against e-waste refining community data (Gold Refining Forum, CJD E-Cycling)
- Recovery rates: Recycler payout estimated at 40-60% of gross raw scrap value for sub-bulk quantities; component salvage assumes professional BGA rework capability

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
- Aluminum heatsink scrap $0.77/kg (ScrapMonster, Mar 2026)

### Secondary Market
- eBay sold/active listings (Mar 2026)
- AliExpress, ServerSupply (Mar 2026)

---

## 9. Scrap Value Scenarios

### 9.1 Theoretical Maximum (Best Case)

Absolute ceiling assuming perfect component recovery, 100% precious metal extraction, and a buyer for every part. The A16's four-GPU, 32-chip GDDR6 design gives it an unusually high part-out ceiling for a non-HBM card.

| Component | Basis | Value |
|-----------|-------|-------|
| GPU dies (4x GA107-890) | Shenzhen rework for RTX 3050-class boards, $25/die | $100 |
| GDDR6 chips (32x 2GB) | AliExpress at $15/chip (shortage pricing) | $480 |
| Heatsink (650g Al + 30g Cu) | Al scrap + Cu contact pads at scrap rates | $1.00 |
| VRM components (32x DrMOS, 32x inductors) | Harvested DrMOS at $0.50-1/ea, inductors at $0.25/ea | $23 |
| PCB (220g, multi-layer) | Server-grade e-scrap at $10/lb | $4.85 |
| Precious metals (0.25g Au, 0.58g Ag) | 100% extraction at spot ($144/g Au, $2.25/g Ag) | $37.31 |
| ConnectX-6 PCIe switch IC | Niche replacement component | $10 |
| **Total theoretical max** | | **~$656** |

The 32 GDDR6 chips ($480) drive 73% of the theoretical max. This is the highest part-out-to-scrap ratio of any card in this batch because GDDR6 chips, unlike HBM stacks, can be individually desoldered and have a real AliExpress/repair market. The 4x GA107 dies ($100) also have meaningful value as donor silicon for RTX 3050/A2000-class board repairs.

### 9.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator would actually receive for a dead A16.

| Channel | Basis | Payout |
|---------|-------|--------|
| ITAD/broker (whole dead card) | 10-20% of $2,800-$4,300 used working price | $280-$860 |
| Certified e-waste recycler | 2.40 lb board at $8-12/lb + PM assay credit (0.25g Au at 65% recovery = $23.40 net) | $42-$52 |

**Realistic range: $280-$860** (selling the dead card whole to a broker or repair shop).

The A16 has a dual advantage in the dead-card market: (1) its 32 GDDR6 chips are individually harvestable and have real demand from GPU repair technicians, and (2) the four independent GA107 dies mean a single-GPU failure can still leave the other three functional for part-out. However, the A16's VDI niche limits the broker pool compared to mainstream AI accelerators. Component harvesting is still not practical at US labor rates -- desoldering 32 GDDR6 chips takes 4-6 hours of skilled BGA rework time ($200-$600 in labor), which consumes most of the component value. E-waste recycling ($42-$52) is relatively strong here due to the card's 0.25g gold content (highest in this batch, from PCIe fingers + 4x BGA substrates + dense PCB).

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Component-by-component ceiling assuming perfect extraction, a buyer for every part, and top-of-range pricing. The A16 is unique in this dataset because it carries 32 GDDR6 chips -- the highest discrete VRAM count of any card analyzed -- and all 32 are individually desoldered using standard BGA rework (no CoWoS, no microbumps, no underfill epoxy).

| Component | Qty | Unit Price | Total | Notes |
|-----------|-----|-----------|-------|-------|
| GA107-890 dies | 4 | $25 | $100 | Shenzhen rework rate for RTX 3050-class boards |
| GDDR6 2GB chips (Samsung K4ZAF325BM or equiv.) | 32 | $15 | $480 | AliExpress floor; eBay repair market $20-25/chip |
| ConnectX-6 PCIe switch IC | 1 | $10 | $10 | Niche replacement for A16 boards |
| Heatsink (Al extrusion + Cu pads) | 1 | $1 | $1 | 650g Al + 30g Cu at scrap rates |
| VRM (DrMOS stages, inductors, caps) | 1 lot | -- | $23 | Harvested at $0.50-1/stage |
| PCB (donor board) | 1 | $5 | $5 | Server-grade e-scrap |
| Precious metals (0.25g Au, 0.58g Ag) | -- | -- | $37 | 100% extraction at Mar 2026 spot |
| **Theoretical ceiling** | | | **~$656** | |

The 32 GDDR6 chips ($480) represent 73% of the ceiling. This is the best part-out profile of any card in the batch because GDDR6 chips, unlike HBM stacks, have a real, liquid AliExpress/repair market (see component_salvage_market.md, Section 3). No CoWoS or 2.5D packaging is involved -- every chip is standard flip-chip BGA on FR-4.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator would actually receive for a dead or partially failed A16.

**Option A -- ITAD broker (whole dead card):**
Broker or remarketing firm (Net Equity, ALTA Technologies, BrokenGPU.com) buys the dead card as-is. Typical payout is 10-25% of used working price. At Mar 2026 used prices of $2,800-$4,300, this yields **$280-$1,075**. The A16's four independent GPUs mean a single-die failure still leaves three functional subsystems, which pushes broker offers toward the higher end. VDI niche limits the buyer pool versus AI accelerators but used pricing remains surprisingly strong.

**Option B -- E-waste recycler (scrap + precious metals):**
Card weight 2.40 lb. Server-grade PCBs at $8-12/lb plus precious metal assay credit (0.25g Au at 60-70% recovery = $22-$25 net, plus Ag credit). Total payout: **$42-$55**. This is the floor -- what you get from a certified recycler with no effort.

**Option C -- GDDR6 harvesting (the A16-specific opportunity):**
The A16 is the only card in this dataset where component harvesting has a defensible economic case even at US labor rates. The 32 GDDR6 chips at $15/chip AliExpress floor = $480 in gross component value. At 50% recovery (yield loss, unsold inventory, testing cost) that is $240. Desoldering 32 chips takes 4-6 hours of BGA rework ($200-$300 at US shop rates). Net after labor: **$0-$80 profit**, marginal but not negative. A Shenzhen shop with cheaper labor clears $150-$250 net. No other card in the batch has this profile because no other card has 32 individually harvestable VRAM chips on standard BGA.

**Realistic range: $280-$1,075** (broker, Option A). Component harvesting is break-even at best in the US; recycler payout ($42-$55) is the true floor.
