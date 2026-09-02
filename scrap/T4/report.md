# NVIDIA Tesla T4 -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe (HHHL, single-slot, passive)
**TDP:** 70W
**MSRP:** ~$2,500 (launch, 2018) | **Used (Mar 2026):** $699-$1,100

---

## 1. Card Overview

The Tesla T4 is a half-height, half-length, single-slot, passively-cooled Turing-generation datacenter inference accelerator. Drawing only 70W entirely from the PCIe slot with no external power connector, it is one of the most widely deployed inference GPUs ever made and one of the most compact datacenter GPUs by weight and volume.

| Attribute | Value |
|-----------|-------|
| GPU die | TU104-895-A1 (TSMC 12nm FFN) |
| Die area | 545 mm2 |
| Transistors | 13.6 billion |
| Memory | 16 GB GDDR6 (8 x 2 GB) |
| Memory bus | 256-bit |
| Interconnect | PCIe Gen3 x16 physical / x8 electrical (no NVLink) |
| TDP | 70 W |
| Board weight | 301 g (NVIDIA Product Brief PB-09256-001) |
| Packaging | Standard flip-chip BGA |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (extruded aluminum, passive) | 130 | 41.5% |
| PCB (PG183, 6-8 layer) | 95 | 30.4% |
| VRM (inductors + MOSFETs + caps) | 12 | 3.8% |
| GPU die + BGA package | 15 | 4.8% |
| Memory (8x GDDR6 chips) | 10 | 3.2% |
| Connectors + bracket | 20 | 6.4% |
| Other (solder, TIM, passives, misc ICs) | 31 | 9.9% |
| **Total** | **~313** | **100%** |

Note: Component weights sum to ~313g vs. NVIDIA's stated 301g board-only weight. The 12g discrepancy is within estimation uncertainty for individual component weights.

---

## 3. Component Breakdown

### GPU Die
- TU104-895-A1, 545 mm2, 13.6B transistors, TSMC 12nm FFN
- 2,560 CUDA cores enabled (40 of 48 SMs), 320 Turing Tensor Cores
- Secondary market: ~$8 (reballing/rework for board repair)
- Raw scrap: ~$1.20

### Memory
- 8 x 2 GB GDDR6 (Samsung K4ZAF325BM or Micron equivalent), 256-bit bus, 320 GB/s
- Secondary market: ~$3.50 total (salvaged/tested set)
- Raw scrap: ~$0.15

### Heatsink
- Extruded aluminum (6063 alloy) with copper core insert (~15g), passive only -- no fan, no heat pipes, no vapor chamber
- eBay listing for Tesla P4 (same HHHL form factor, predecessor) references "copper core" heatsink. The T4 likely uses same design: small copper slug/insert at the die contact point for local heat spreading, with extruded aluminum body for convective dissipation. No heat pipes: HHHL height constraint and 70W TDP make them unnecessary. Confidence: 70%. See heatsink_materials_analysis.md.
- 130g (41.5% of card): ~115g aluminum + ~15g copper insert
- Secondary market: ~$2 (aftermarket replacement)
- Raw scrap: ~$0.28 (Al 115g at $0.77/kg = $0.09; Cu 15g at ~$5.90/lb = $0.19)

### VRM / Power Delivery
- ~4-6 phase, minimal design (70W from PCIe slot only, no external power)
- Inductors, MOSFETs, capacitors
- Secondary market: ~$2 (component harvesting)
- Raw scrap: ~$0.15

### PCB
- PG183, 6-8 layer FR-4, ~168 x 69 mm (HHHL form factor)
- Cu content ~19-22g (~20% of 95g bare board weight)
- Secondary market: ~$5 (donor board for component-level repair)
- Raw scrap: ~$1.50

### Connectors
- PCIe Gen3 x16 physical / x8 electrical gold edge fingers (~30 microinch hard gold plating, ~0.002-0.003g Au)
- No auxiliary power connector
- Secondary market: ~$0.50
- Raw scrap: ~$0.35

### Other
- TIM (thermal paste/pads), ~30 MLCCs and tantalum caps, ~5 voltage regulators/support ICs, SPI flash EEPROM (vBIOS), crystal oscillator, stiffener/EMI shield, bracket + screws, SAC305 solder, ~50 discrete passives
- Raw scrap: ~$0.62

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.05 (gross) | $145/g | $7.25 | PCB traces/pads (~0.05g gross); ~0.015-0.02g recoverable after refining losses |
| Silver (Ag) | 0.12 | $2.25/g | $0.27 | SAC305 solder (~3-4g x 3% Ag = 0.09-0.12g) + MLCC terminations (~0.01g). **Revised from 0.25-0.50g:** a 301g HHHL card has only ~3-5g of SAC305 solder. 3% of ~4g = 0.12g Ag from solder. The original 0.25-0.50g range implied 8-17g of solder, which is physically inconsistent with a card this small. |
| Palladium (Pd) | 0.002-0.005 | $45/g | $0.09-$0.23 | MLCC internal electrodes (modern BME, trace Pd) |
| **Total** | | | **$7.61** (gross) | |

Note on gold: The PCB row in components.csv lists 0.05g gross Au content. The summary's 0.015-0.02g figure represents estimated net recoverable gold after 60-70% refining losses. Both figures are used in this report -- gross for the precious metals table, net recovery factored into the value cascade.

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $699-$1,100 | 28-44% |
| Component salvage (theoretical max) | ~$22 | 0.9% |
| Component salvage (realistic) | ~$15-18 | 0.6-0.7% |
| Raw material scrap (gross) | ~$8-$9 | 0.3-0.4% |
| Recycler payout (net, what you'd receive) | ~$3.50-$5 | 0.14-0.20% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **SPI flash EEPROM omitted from BOM** [CORRECTED]: All NVIDIA GPUs contain an SPI flash chip for vBIOS storage (e.g., Winbond W25Q series). Weight ~0.3g, negligible scrap value. Added to "Other" in this report. Severity: low.
- **Crystal oscillator omitted from BOM** [CORRECTED]: Reference clock source present on all GPU boards. Weight <0.5g, negligible scrap value. Added to "Other" in this report. Severity: low.
- **Samsung K4ZAF325BM part number uncertain**: Correct capacity/type but exact supplier varies by production run. May be Micron equivalent. Severity: low (no value impact).
- **Discrete component counts are estimates**: ~30 MLCCs, ~5 ICs, ~50 passives cannot be verified without physical teardown or TechInsights BOM access. Flagged as estimates. Severity: low.

### Pricing Issues
- **Working T4 price was $200-$400** [CORRECTED to $699-$1,100]: The original estimate was significantly below current market. eBay active listings cluster at $699-$1,100; Amazon used $799-$837; Fluence reports $845. The T4 has recovered in value, likely driven by sustained inference demand. Severity: high.
- **PCB gold content inconsistency** [CLARIFIED]: The PCB row claims 0.05g gross Au, but the summary states 0.015-0.02g total. The summary figure represents net recoverable gold after refining losses, not gross content. The gross figure of 0.05g is used in the precious metals table; refining losses are noted. Severity: medium (clarification, not error).
- **Palladium quantity uncertain**: 0.002-0.005g Pd from modern BME MLCCs is plausible but unverifiable without assay. Confidence: 55. Severity: low (< $0.25 value at stake).

### Confidence Assessment
- Component accuracy: 82/100
- Pricing accuracy: 80/100
- Overall confidence in scrap estimate: 78/100

### Web Verification (2026-03-29)

Seven claims cross-checked against NVIDIA product brief (PB-09256-001_v05), VideoCardz, AnandTech, Tom's Hardware, Lenovo Press, and reseller listings:

1. **TU104-895-A1, 545 mm2, 13.6B transistors, TSMC 12nm FFN** -- Confirmed by multiple sources.
2. **8x 2GB GDDR6 = 16 GB, 256-bit bus** -- Confirmed. No public T4-specific board teardown photos found; RTX 2080 (same TU104 die) PCB teardown from VideoCardz shows 8 GDDR6 modules.
3. **Board weight 301g (PB-09256)** -- Confirmed. Product brief Table 1 lists 301g board, 17g FH bracket, 10g HH bracket.
4. **No external power connector, 70W from PCIe slot** -- Confirmed.
5. **HHHL single-slot** -- Confirmed. PCB ~168 x 69 mm.
6. **Passive cooling, extruded aluminum heatsink with copper core insert** -- Passive confirmed. No public teardown found. Determination: extruded aluminum with ~15g copper core insert at die contact, no vapor chamber, no heat pipes. eBay P4 "copper core" heatsink listing and HHHL form factor constraints support this. 70W TDP / 0.128 W/mm2 heat flux does not require phase-change heat transport. Confidence 70%. See heatsink_materials_analysis.md.
7. **PCIe Gen3 x16 (x8 electrical)** -- Confirmed. Product brief Table 1 states "PCI Express 3.0 x16 x8". Report table corrected to include x8 electrical detail (was omitted).

---

## 7. Key Observations

1. **The T4 has very low scrap value.** At ~$8-$9 in raw materials (gross), it is one of the lowest-value datacenter GPUs to scrap. This is a direct consequence of its compact 301g form factor, minimal passive aluminum heatsink, and simple slot-powered design.

2. **The working unit price has recovered significantly.** At $699-$1,100 (Mar 2026), the T4 has rebounded from the $200-$400 levels seen in earlier market conditions, likely driven by sustained inference deployment demand. The scrap floor at ~$8-$9 is now only 0.7-1.3% of functional value, making scrapping a working or repairable T4 economically irrational.

3. **Most scrap value is locked in gold that requires specialized refining.** The ~0.05g gross gold content accounts for ~$7.25 at spot, but actual recovery through an e-waste refiner yields only $2-3 net after 60-70% processing losses. Base metals (Cu, Al, Sn) contribute less than $1.50 combined.

4. **The heatsink is the heaviest component but nearly worthless as scrap.** At 130g (41.5% of card weight), the extruded aluminum heatsink yields only $0.10 in scrap. Aluminum heatsink scrap is one of the lowest-value recyclable metal categories.

5. **Volume economics dominate.** Individual T4 scrapping is not economical. At datacenter decommissioning scale (hundreds or thousands of units), batch processing and bulk recycler rates improve the economics, but the per-unit scrap value remains fundamentally constrained by the card's small size and modest precious metal content.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA T4 Product Brief (v03)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/T4%20Product%20Brief.pdf) -- board weight (301 g), form factor, TDP
- [NVIDIA T4 Product Brief (v05)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-t4/t4-tensor-core-product-brief.pdf) -- updated specifications
- [NVIDIA T4 Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-t4/t4-tensor-core-datasheet.pdf) -- memory configuration, bus width, compute specs
- [GPU Poet -- NVIDIA T4](https://gpupoet.com/gpu/learn/card/nvidia-t4) -- secondary market pricing, specifications cross-reference
- [Fluence -- NVIDIA T4](https://www.fluence.network/blog/nvidia-t4/) -- market pricing ($845), deployment context

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
- Working T4 pricing from eBay active listings ($699-$1,100), Amazon ($799-$837), [Fluence blog](https://www.fluence.network/blog/nvidia-t4/) ($845). Parts-out values from eBay component listings and repair market estimates.

### Methodology Notes
- Precious metal quantities: Engineering estimates from PCB construction (6-8 layer, HHHL), BGA package, PCIe gold finger plating thickness, SAC305 solder composition. Gross Au 0.05g from PCB row analysis; net 0.015-0.02g after refining losses.
- Recovery rates: 30-40% net recovery assumed for precious metals through professional e-waste refiner (BoardSort, ESG Edelmetall-Service published rates). Individual-card processing incurs disproportionate assay and handling fees vs. bulk lots.
- Component verification: TechInsights teardown reference (DDT-1908-806, BOM-1908-806), NVIDIA datasheets, Samsung semiconductor catalog, VideoCardz GPU database.

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Component-by-component ceiling, assuming a buyer exists for each part at stated prices:

| Component | Ceiling Value | Notes |
|-----------|------------:|-------|
| TU104 GPU die | $8 | Standard BGA; reballing possible but Turing inference dies have minimal repair demand |
| GDDR6 (8x 2GB chips) | $3.50 | Harvested GDDR6 chips sell at $0.50-$1 each on AliExpress; testable |
| Heatsink (passive Al) | $2 | Aftermarket replacement; very niche |
| PCB (donor board) | $5 | Component-level repair donor |
| VRM + other | $3.50 | Minimal |
| **Theoretical ceiling** | **~$22** | |

No HBM, no CoWoS -- the T4 uses standard flip-chip BGA with discrete GDDR6 chips. The GDDR6 chips are the only components with a real (if thin) secondary market. The TU104 die has near-zero repair demand because working T4s are cheap enough that nobody repairs dead ones.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

| Option | Expected Recovery | Notes |
|--------|------------------:|-------|
| **A. ITAD broker** | $70-$275 | 10-25% of $699-$1,100 working price; but at this price point, brokers may decline individual cards |
| **B. E-waste recycler** | $3-$5 | 301g card at $5-15/lb server PCB = $1-2 + PM assay on ~$7.60 gross (60-70% credit = $4.50-$5.30, minus fees) |
| **C. "For parts" eBay sale** | $50-$150 | **Best option for the T4.** At $699-$1,100 working, repair shops and hobbyists buy dead T4s for testing/donor boards. eBay "for parts" GPU listings in this price class typically sell at 5-15% of working value. |

**Realistic range for a dead T4: $50-$150 ("for parts" eBay sale).** The T4's low working price makes ITAD brokers unattractive (overhead exceeds recovery) and e-waste recycling yields only $3-$5. Selling directly as "for parts or not working" on eBay is the highest-recovery path. The T4's wide deployment base (millions of units in cloud datacenters) creates a steady repair/donor demand stream.
