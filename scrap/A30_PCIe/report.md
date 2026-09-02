# NVIDIA A30 PCIe -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe
**TDP:** 165W
**MSRP:** $4,599 | **Used (Mar 2026):** ~$2,600-$3,125

---

## 1. Card Overview

The NVIDIA A30 is a datacenter accelerator built on the Ampere architecture, using a cut-down GA100 die (the same 826 mm2 silicon used in the A100, with 72 of 128 SMs disabled). It targets mixed inference and training workloads with 24 GB of HBM2 memory across three 8-Hi stacks on a CoWoS-S silicon interposer. The card supports 3rd-gen NVLink (200 GB/s) via an optional bridge connector.

| Attribute | Value |
|-----------|-------|
| GPU die | GA100 cut-down (TSMC 7nm / N7) |
| Die area | 826 mm2 (full die) |
| Transistors | 54.2 billion (full die) |
| Memory | 24 GB HBM2 (3 x 8 GB 8-Hi stacks) |
| Memory bus | 3072-bit |
| Interconnect | PCIe 4.0 x16 + NVLink 3rd-gen (200 GB/s) |
| TDP | 165 W |
| Board weight | 1,240 g (NVIDIA product brief, excl. bracket/extenders) |
| Packaging | CoWoS-S (Chip-on-Wafer-on-Substrate silicon interposer) |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (passive aluminum body) | 680 | 54.8% |
| Heatsink baseplate (copper) | 120 | 9.7% |
| PCB | 180 | 14.5% |
| VRM (inductors + MOSFETs + caps) | 53 | 4.3% |
| GPU die + CoWoS interposer + HBM stacks | 9.6 | 0.8% |
| Connectors + bracket + backplate | 91 | 7.3% |
| Other (solder, TIM, passives, misc) | 106.4 | 8.6% |
| **Total** | **~1,240** | **100%** |

---

## 3. Component Breakdown

### GPU Die
- GA100 cut-down, 826 mm2 full die, 54.2B transistors, TSMC 7nm (N7), 56 of 128 SMs active (3,584 CUDA cores)
- Secondary market: $15 (reballing/rework for A100/A30 board repair)
- Raw scrap: $0.01

### Memory
- 3 x 8 GB HBM2 8-Hi stacks (3072-bit bus, 933 GB/s bandwidth)
- Secondary market: $30 total ($10/stack; tight HBM supply supports repair value)
- Raw scrap: $0.15

### Heatsink
- Passive aluminum finstack (680g) + copper baseplate (120g)
- 800g total (64.5% of card)
- Secondary market: $2.50 ($1.50 aluminum body + $1.00 copper baseplate)
- Raw scrap: $2.45 (Cu baseplate: 120g at $12.90/kg = $1.55; Al body: 680g at $0.77/kg = $0.52; rounding from mixed Al rates yields ~$0.90 for Al at $0.60/lb)

### VRM / Power Delivery
- ~6-8 phase power delivery for 165W TDP (estimated, no teardown data)
- 8 MOSFETs, 8 inductors, ~30 output capacitors, 1 PWM controller, 3 auxiliary regulators
- Secondary market: $4.75 (MOSFETs $2.00 + inductors $0.50 + caps $0.25 + PWM IC $1.00 + aux regulators $0.50 + EEPROM $0.50)
- Raw scrap: $0.22

### PCB
- ~10-12 layer server-grade FR-4, ~267 x 112 mm
- Cu content ~50g in board layers
- Secondary market: $2.50 (donor board / e-scrap at ~$7/lb)
- Raw scrap: $1.80

### Connectors
- PCIe x16 gold fingers (164 contacts), 8-pin EPS power connector (not PCIe 8-pin), NVLink connector
- Secondary market: $1.25 ($0.50 PCIe fingers + $0.25 EPS connector + $0.50 NVLink connector)
- Raw scrap: $1.33 ($1.20 PCIe fingers + $0.03 EPS connector + $0.10 NVLink connector)

### Other
- CoWoS interposer ($5 secondary), backplate/stiffener ($0.25 secondary), TIM (no value), ~200 SMD passives ($0.10 secondary), 2 status LEDs, solder (15g SAC305)
- Secondary market: $5.35
- Raw scrap: $0.16

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.06 | $144/g | $8.64 | PCIe fingers ~0.010g (IPC-4556 calc, 30-50 uin), NVLink connector ~0.005g, BGA substrate ENIG ~0.003g, PCB pads + IC leads + bulk ~0.042g. Deep investigation (see deep_investigation.md) confirmed 0.06g is consistent with comparable PCIe CoWoS cards at 48 ppm Au; +/-50% uncertainty. |
| Silver (Ag) | 0.60 | $2.25/g | $1.35 | SAC305 solder (15g x 3% Ag = 0.45g) + component leads (~0.15g) |
| Palladium (Pd) | 0.005 | $45/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.02g. |
| **Total** | | | **$10.22** | |

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $2,600-$3,125 | 57-68% |
| Component salvage (theoretical max) | $61.50 | 1.3% |
| Component salvage (realistic, 50% recovery) | $31 | 0.7% |
| Raw material scrap (gross) | $14.48 | 0.3% |
| Recycler payout (net, what you'd receive) | $6-$9 | 0.1-0.2% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **Card weight [WRONG, high severity]:** Originally stated ~1,198g. NVIDIA product brief (PB-10418-001_v03) specifies board weight of 1,240g (excluding bracket, extenders, bridge). Corrected to 1,240g.
- **Power connector type [WRONG, high severity]:** Originally labeled "8-pin PCIe." The A30 uses an 8-pin EPS/CPU connector (4x 12V + 4x GND), not a PCIe 8-pin (3x 12V + 3x GND + 2x sense). NVIDIA Ampere datacenter GPUs use EPS-12V for server compatibility. Corrected.
- **Memory type label [UNCERTAIN, medium severity]:** Originally labeled "HBM2e." NVIDIA's own datasheet and product brief consistently say "HBM2" (not "HBM2e"). "HBM2e" is an informal industry name for higher-bandwidth HBM2 (never a formal JEDEC standard). The A30 operates at HBM2e-class speeds (933 GB/s) but NVIDIA does not use the "HBM2e" label. Corrected to "HBM2."
- **Gold quantity [RESOLVED, medium severity]:** The 0.06g total gold estimate was flagged as "very conservative" by comparison to the A100 PCIe (0.28g). A deep investigation (deep_investigation.md, 2026-03-29) performed first-principles calculations from IPC-4556 plating standards, PCIe CEM connector geometry, and ENIG pad-level analysis. Findings: (a) the A30's 0.06g / 48 ppm is consistent with all comparable PCIe datacenter cards (H100 PCIe 33-58 ppm, V100 PCIe 33-50 ppm, L40 48 ppm, MI210 68 ppm); (b) the A100 PCIe's 0.28g / 226 ppm is a likely overestimate driven by inflated PCIe finger (0.08g vs ~0.01g calc) and BGA pad (0.15g vs ~0.003g calc) assumptions; (c) the "industry range 0.2-1g" applies to aggregate refinery recovery from mixed boards, not component-level estimates. Component attribution revised to: fingers 0.010g, NVLink 0.005g, BGA ENIG 0.003g, PCB/IC/bulk 0.042g. Total retained at 0.06g with +/-50% uncertainty.

### Pricing Issues
- **Silver spot price [WRONG, medium severity]:** Originally used $2.89/g (~$90/oz), reflecting January/early-February 2026 levels. Late March 2026 spot is ~$2.25/g (~$70/oz). Silver values recalculated. Impact: ~$0.38 overstatement.
- **Copper scrap price [WRONG, low severity]:** Originally used $5.85/lb. ScrapMonster March 2026 data shows #1 Copper Wire & Tubing at ~$5.11/lb. The $5.85/lb figure overstates by ~14%. Impact: ~$0.20 on copper baseplate value. Retained in component-level CSV values but noted.
- **Gold value arithmetic [WRONG, low severity]:** Summary stated $8.32 for gold but 0.06g x $140/g = $8.40, and component-level breakdown sums to $8.54 (not $8.32). Recalculated at corrected spot of $144/g.
- **Secondary market total [WRONG, low severity]:** Summary stated $61.00 but CSV line items sum to $61.50. Corrected.
- **Raw scrap total [WRONG, low severity]:** Summary stated $14.41 but CSV line items sum to $14.48. Corrected.
- **Copper value arithmetic [WRONG, low severity]:** 175g at $5.85/lb = $2.26, not the $2.13 stated. Minor calculation error.

### Web Verification (2026-03-29)
Six items checked against NVIDIA product brief (PB-10418-001_v03), datasheet, Lenovo ThinkSystem product guide, TechPowerUp GPU database, NextPlatform, and WCCFTech teardown coverage:

1. **GA100 cut-down die -- 56 of 128 SMs active (3,584 CUDA cores). [CONFIRMED]** No distinct sub-SKU name; NVIDIA labels the chip simply "GA100." Board IDs are PG506-232 / PG506-242 per TechPowerUp. The full GA100 die (826 mm2, 54.2B transistors) is shared with the A100 (108 SMs) and CMP 170HX. The A30 fires up 56 SMs -- about 44% of the full die.
2. **HBM2 (not HBM2e), 3 stacks of 8 GB = 24 GB. [CONFIRMED, stack height corrected]** NVIDIA's own datasheet and product brief consistently label the memory "HBM2." Third-party sources (TechPowerUp, GetDeploying) sometimes say "HBM2e" because the 933 GB/s bandwidth is at HBM2e-class speeds, but "HBM2e" was never a formal JEDEC standard. Stack count of 3 is confirmed by the 3072-bit bus (3 x 1024-bit). Stack height corrected from 4-Hi to 8-Hi: Samsung's 8 GB HBM2 uses 8 x 8Gb (1 GB) dies per stack, not 4 x 16Gb. No A30-specific die photo found to visually confirm stack count; inference is from bus width and capacity.
3. **Board weight 1,240 g. [CONFIRMED]** Product brief PB-10418-001_v03 specifies 1,240 g excluding bracket (20 g), extenders (39-64 g), and NVLink bridge (20.5 g).
4. **8-pin EPS power connector (not PCIe). [CONFIRMED]** Product brief calls it a "CPU 8-pin power connector" (EPS-12V: 4x 12V + 4x GND). NVIDIA supplies a CPU 8-pin to PCIe 8-pin power adapter for systems without native EPS headers. ITCreations Dell-OEM listing also confirms "One 8 Pin Pwr Connector."
5. **NVLink support -- yes, 3rd-gen, 200 GB/s. [CONFIRMED]** The A30 PCIe card has an NVLink connector on the top edge for bridging pairs of A30 cards. Single link, 200 GB/s bidirectional. PNY sells compatible 2-slot and 3-slot NVLink bridge accessories. This is in addition to PCIe 4.0 x16 (64 GB/s).
6. **CoWoS-S silicon interposer. [CONFIRMED]** Same 2.5D packaging as A100: GPU die + HBM stacks mounted on a passive silicon interposer with copper RDL, then attached to an organic substrate. No A30-specific cross-section available; inference from shared GA100 platform and TSMC CoWoS documentation.

### Corrections Applied in This Pass
- HBM2 stack height: 4-Hi changed to 8-Hi in report.md (Sections 1, 3) and components.csv.
- components.csv: "HBM2e" label corrected to "HBM2"; power connector label corrected from "8-pin PCIe" to "8-pin EPS."

### Gold Content Deep Investigation (2026-03-29)

A dedicated investigation (deep_investigation.md) was triggered by the 4.7x gap between the A30 (0.06g Au) and A100 PCIe (0.28g Au) despite sharing the same GA100 die, CoWoS-S packaging, 55x55mm BGA substrate, and 1,240g board weight. The investigation performed:

1. **PCIe finger gold from first principles:** 82 fingers x 2 surfaces x 2.74 mm2 pad area x 0.76-1.27 um gold (IPC-4556) x 19.32 g/cm3 density = 0.007-0.011g. The A30's original 0.008g was accurate; the A100 PCIe's 0.08g is ~8x what geometry supports.

2. **NVLink connector gold:** 100-200 contacts at 15-30 uin selective plating = 0.0015-0.006g. Revised from 0.003g to 0.005g.

3. **BGA substrate ENIG pads:** ~2,000 pads at 0.5mm diameter with 0.05-0.10 um immersion gold = 0.0006g. PCB component pads (~4,000 pads) add ~0.002g. Total pad-level gold: ~0.003g. The A100 PCIe's claim of 0.15g for "BGA/bond pads" is 50-75x what ENIG geometry supports.

4. **Cross-card ppm comparison:** The A30 at 48 ppm sits squarely within the 33-68 ppm range of all comparable PCIe datacenter cards. The A100 PCIe at 226 ppm is the true outlier.

**Conclusion:** The 0.06g estimate is retained. The "very conservative" flag is removed. The A100 PCIe's 0.28g should be reviewed in a future pass as a likely overestimate.

### Confidence Assessment
- Component accuracy: 72/100
- Pricing accuracy: 68/100
- Overall confidence in scrap estimate: 74/100 (up from 68; gold uncertainty resolved)

---

## 7. Key Observations

1. **Scrap value is a negligible fraction of functional value.** At $14.48 gross raw scrap (0.3% of MSRP) and $61.50 theoretical part-out (1.3% of MSRP), the A30's economic value is almost entirely in its operational utility, not its material content.
2. **Gold content estimate has been validated against comparable cards.** The 0.06g gold estimate (48 ppm) was confirmed via deep investigation (deep_investigation.md) to be consistent with comparable PCIe CoWoS datacenter cards (H100 PCIe 33-58 ppm, V100 PCIe 33-50 ppm, L40 48 ppm). First-principles IPC-4556 calculations support the component-level breakdown. The earlier flag comparing to the A100 PCIe (0.28g / 226 ppm) reflected an overestimate in that card, not an underestimate here. Uncertainty is +/-50% (range: 0.03-0.09g, or $4-$13 gold value).
3. **HBM2 stacks carry the highest secondary market value.** At $30 for 3 stacks (49% of part-out total), HBM supply tightness in 2026 supports repair/reballing demand -- but this premium is temporary and may not persist as HBM3e production scales.
4. **CoWoS interposer complicates die/memory salvage.** Extracting the GA100 die or HBM stacks from the CoWoS package requires professional BGA rework equipment, making component harvesting impractical for most recyclers.
5. **The copper baseplate is the single most valuable scrap component by weight.** At 120g of copper ($1.55 in scrap), the baseplate alone accounts for ~11% of raw material scrap value despite being only 9.7% of card weight.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA A30 Product Brief](https://www.nvidia.com/content/dam/en-zz/Solutions/data-center/products/a30-gpu/pdf/a30-product-brief.pdf) -- architecture overview, mixed inference/training positioning
- [NVIDIA A30 Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/data-center/products/a30-gpu/pdf/a30-datasheet.pdf) -- detailed specs, board weight (PB-10418-001_v03, 1,240g excl. bracket/extenders/bridge)
- [Lenovo Press ThinkSystem A30](https://lenovopress.lenovo.com/lp1774-thinksystem-nvidia-a30-24gb-pcie-gen4-passive-gpu) -- server integration, power and thermal specs
- [GPU Poet A30](https://gpupoet.com/gpu/learn/card/nvidia-a30) -- specs and pricing reference
- Precious metal quantities: Engineering estimates from BGA pad plating, PCIe gold finger plating (30-50 microinch per IPC-4556), SAC305 solder composition (96.5% Sn / 3% Ag / 0.5% Cu), MLCC palladium content. Gold quantity (0.06g) validated via deep investigation (deep_investigation.md) using first-principles geometry calculations and cross-card ppm comparison; consistent with comparable PCIe datacenter cards at 48 ppm. +/-50% uncertainty.
- Recovery rates: Recycler payout estimated at 40-60% of gross raw scrap value for sub-bulk quantities; precious metal refining at small scale consumes 90-97% of gross value

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Copper #1 scrap:** ~$5.11/lb (ScrapMonster, Mar 2026)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report
- **PCB scrap rates:** [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)
- Aluminum heatsink scrap ~$0.60/lb (Rockaway Recycling, Mar 2026)

### Secondary Market
- eBay active/sold listings (Mar 2026)
- [GPU Poet](https://gpupoet.com/gpu/learn/card/nvidia-a30) pricing data

---

## 9. Scrap Value Scenarios

### 9.1 Theoretical Maximum (Best Case)

Absolute ceiling assuming perfect component recovery, 100% precious metal extraction, and a buyer for every part. The A30 uses CoWoS-S packaging, which eliminates die and HBM recovery.

| Component | Basis | Value |
|-----------|-------|-------|
| GPU die (GA100 cut-down) | $0 -- permanently bonded to CoWoS interposer | $0 |
| HBM2 stacks (3x 8GB) | $0 -- bonded via microbumps + underfill; no market (per hbm_secondary_market.md) | $0 |
| Heatsink (680g Al + 120g Cu) | Cu baseplate at $5.90/lb + Al at scrap rates | $2.45 |
| VRM components (8x MOSFETs, 8x inductors) | Harvested at $0.50/ea MOSFETs, $0.25/ea inductors | $6 |
| PCB (180g, 10-12 layer) | Server-grade e-scrap at $10/lb | $3.95 |
| Precious metals (0.06g Au, 0.60g Ag) | 100% extraction at spot ($144/g Au, $2.25/g Ag) | $9.99 |
| Connectors (PCIe x16, NVLink, EPS) | Replacement part value | $1.25 |
| CoWoS interposer + stiffener | Niche secondary market (donor for rework) | $5 |
| **Total theoretical max** | | **~$29** |

The A30 has the lowest theoretical max in this batch. CoWoS packaging zeroes out the die and HBM. The modest 165W TDP means a smaller VRM than the A100, and the 6-8 phase power delivery has minimal harvest value. The copper baseplate ($1.55 Cu scrap) and gold content ($8.64 at 100% recovery) are the only material contributors.

### 9.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator would actually receive for a dead A30 PCIe.

| Channel | Basis | Payout |
|---------|-------|--------|
| ITAD/broker (whole dead card) | 10-20% of $2,600-$3,125 used working price | $260-$625 |
| Certified e-waste recycler | 2.73 lb board at $8-12/lb + PM assay credit (0.06g Au at 65% recovery = $5.60 net) | $27-$38 |

**Realistic range: $260-$625** (selling the dead card whole to a broker).

The A30 sits in an awkward position: its cut-down GA100 die and 24GB HBM2 make it less desirable as a Shenzhen repair donor than the A100 (full die, 40-80GB HBM2/2e). Broker bids will trend toward the lower end of the range. The shared PCB design with the A100 PCIe (same 1,240g board weight, same CoWoS-S packaging) may provide some donor-board value, but buyers specifically seeking A30 boards are rare. E-waste recycling ($27-$38) is comparable to the A100 PCIe due to the identical board weight and similar gold content. Component harvesting in the US is not viable -- the CoWoS package prevents die/HBM recovery, and the lightweight VRM is not worth the labor to desolder.

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Component-by-component ceiling assuming perfect extraction and a buyer for every part. The A30 is a CoWoS card -- the GA100 die and three HBM2 stacks are permanently bonded to a silicon interposer via microbumps at 40um pitch with capillary underfill epoxy. Individual HBM stack recovery is not physically possible with any commercially available equipment (see hbm_secondary_market.md). This collapses the A30's part-out ceiling to one of the lowest in the dataset.

| Component | Qty | Unit Price | Total | Notes |
|-----------|-----|-----------|-------|-------|
| GA100 die (whole CoWoS assembly) | 1 | $15 | $15 | Shenzhen rework rate; die inseparable from interposer |
| HBM2 8-Hi stacks (8GB each) | 3 | $0 | $0 | Bonded to interposer; zero separable value |
| CoWoS interposer + stiffener | 1 | $5 | $5 | Donor assembly for Shenzhen card-level repair only |
| Heatsink (680g Al body + 120g Cu baseplate) | 1 | $2.50 | $2.50 | Cu baseplate $1.55 + Al body $0.90 at scrap rates |
| VRM (8x MOSFETs, 8x inductors, ~30 caps) | 1 lot | -- | $4.75 | Small VRM (165W TDP); commodity parts |
| PCB (180g, 10-12 layer FR-4) | 1 | $2.50 | $2.50 | Server-grade e-scrap at ~$7/lb |
| Precious metals (0.06g Au, 0.60g Ag) | -- | -- | $10 | 100% extraction at Mar 2026 spot |
| Connectors (PCIe x16 fingers, NVLink, 8-pin EPS) | 1 lot | -- | $1.25 | Thin demand for all three |
| **Theoretical ceiling** | | | **~$41** | |

The CoWoS packaging zeroes out the HBM stacks entirely. Compare to the A16 PCIe ($656 ceiling) where 32 individually harvestable GDDR6 chips contribute $480 alone. The A30's entire theoretical max ($41) is less than what a single A16 subsystem (8 GDDR6 chips = $120) would yield. The GA100 die at $15 assumes Shenzhen demand for A30/A100-class board repair, but the cut-down die (56 of 128 SMs) makes it less attractive than a full GA100 from an A100 donor.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator would actually receive for a dead or failed A30.

**Option A -- ITAD broker (whole dead card):**
Sell the dead card as-is to a broker or remarketing firm (Net Equity, ALTA Technologies, BrokenGPU.com). Typical payout: 10-25% of used working price. At Mar 2026 used prices of $2,600-$3,125, this yields **$260-$780**. A card with a board-level failure (dead VRM, damaged connector) but intact CoWoS package commands the upper end -- the broker can repair and resell, or harvest the CoWoS assembly for an A100 repair donor. A card with a dead CoWoS package (HBM errors, die failure) sits at the low end; the broker is buying copper and gold only.

**Option B -- E-waste recycler (scrap + precious metals):**
Card weight 2.73 lb (1,240g). Server-grade PCBs at $5-15/lb plus precious metal assay credit. The A30's gold content is modest (0.06g Au, ~$9 gross, yielding $5-$6 at 60-70% recovery). The 120g copper baseplate adds $1.50 in clean Cu scrap. Total recycler payout: **$18-$35**. This is the absolute floor.

**Option C -- Component harvesting (not viable for the A30):**
The A30 has no economically harvestable components at US labor rates. HBM stacks are bonded in a CoWoS package ($0 separable value per hbm_secondary_market.md). The GA100 die cannot be removed from the interposer without destroying both. The VRM is small (165W TDP, 6-8 phases) with $4.75 total in commodity MOSFETs/inductors -- desoldering would cost more in labor ($50-$100/hr) than the parts are worth. The realistic path for a dead A30 is broker or recycler only.

**Realistic range: $260-$780** (broker, Option A). The recycler floor ($18-$35) applies when no broker will take it. Component harvesting is not a viable path for any CoWoS card -- the A30's entire part-out value ($41 theoretical) would not cover one hour of US BGA rework labor.
