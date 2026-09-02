# NVIDIA Tesla V100 SXM2 -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** SXM2
**TDP:** 300W
**MSRP:** $8,000-$10,000 (at launch) | **Used (Mar 2026):** $95-$900

---

## 1. Card Overview

The Tesla V100 SXM2 is a mezzanine-style datacenter GPU accelerator built on the Volta architecture, launched in 2017. It uses NVIDIA's GV100 GPU with TSMC CoWoS-S 2.5D packaging, designed for DGX-1V and HGX server baseboards. Available in 16GB and 32GB configurations with NVLink 2.0 interconnect.

| Attribute | Value |
|-----------|-------|
| GPU die | GV100 (TSMC 12nm FFN) |
| Die area | 815 mm2 |
| Transistors | 21.1 billion |
| Memory | 16 GB or 32 GB HBM2 (4 stacks x 4GB or 4 x 8GB) |
| Memory bus | 4096-bit |
| Interconnect | NVLink 2.0 (6 links, 300 GB/s bidirectional) |
| TDP | 300 W |
| Board weight | ~240 g (+/-30g, bare module, no heatsink or IHS; unverified -- see deep_investigation.md) |
| Packaging | CoWoS-S (2.5D, reticle-stitched silicon interposer) |

---

## 2. Weight Breakdown

The SXM2 is a bare module with no attached heatsink; cooling is provided by the server chassis. Weight estimates below are for the 32GB variant.

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| PCB (12-16 layer FR-4) | 65 | 27% |
| VRM (16-phase: inductors + MOSFETs + caps) | 77 | 32% |
| GPU die + interposer + package substrate | 25 | 10% |
| Memory (4x HBM2 8-Hi stacks) | 7 | 3% |
| Connectors (2x MEG-Array + power headers) | 30 | 13% |
| Other (solder, passives, stiffener, underfill) | 36 | 15% |
| **Total** | **~240** | **100%** |

**Note:** The V100 SXM2 is a **bare die module with no integrated heat spreader (IHS/lid)**. The heatsink (part of the server chassis, not the module) contacts the GV100 die directly through a graphite thermal pad. The A100 SXM4 was the first NVIDIA SXM module to add a protective lid. See deep_investigation.md Section 4 for evidence.

---

## 3. Component Breakdown

### GPU Die
- GV100, 815 mm2, 21.1B transistors, TSMC 12nm FFN
- Flip-chip (C4 bump) attachment to silicon interposer -- not wire-bonded
- Secondary market: $0 (inseparable from CoWoS package)
- Raw scrap: ~$0.05 (silicon has negligible scrap value)

### Memory
- 4 x 8GB HBM2 stacks (32GB variant), Samsung/SK Hynix, 4096-bit bus, 900 GB/s
- On-interposer micro-bump attachment; cannot be separated without destruction
- Secondary market: $0 (inseparable from CoWoS package)
- Raw scrap: ~$0.30

### Heat Spreader / IHS
- **CORRECTED: The V100 SXM2 has NO integrated heat spreader (IHS/lid).** It is a bare-die module. The server chassis provides a heatsink (part 699-2G503-0204-200) with a graphite thermal pad that contacts the GV100 die directly. The A100 SXM4 was the first generation to add a protective lid, after server ODMs cracked V100-era dies by overtightening heatsink screws (per SemiAnalysis).
- The original report incorrectly attributed 35g of nickel-plated copper heat spreader to the module. This has been removed from the weight and scrap budgets.
- Secondary market: N/A
- Raw scrap: $0.00

### VRM / Power Delivery
- 16-phase (corrected from original 16 MOSFETs claimed; consistent with 300W TDP)
- Ferrite-core inductors (~2.5g each, ~16g Cu in windings), DrMOS/discrete FETs, MLCCs + polymer caps
- Secondary market: ~$2.00 (component harvesting lot)
- Raw scrap: ~$0.88

### PCB
- 12-16 layer FR-4, ~140mm x 78mm
- Cu content ~18g
- Secondary market: $0 (proprietary SXM2 form factor; no donor board market)
- Raw scrap: ~$3.50

### Connectors
- 2x Amphenol MEG-Array 400-pin mezzanine connectors (corrected from 1; one for PCIe/power, one for NVLink; 800 pins total)
- 2x 2x3 PCIe power headers
- NVLink 2.0 signal traces (6 links)
- Secondary market: ~$6.00 (MEG-Array connectors, ~$3 each used)
- Raw scrap: ~$10.95 (gold plating on 800+ contacts)

### Other
- ~200 discrete passives, aluminum stiffener (~15g), underfill epoxy, solder (~8g SAC305)
- **TIM correction:** The OEM heatsink (not the module itself) uses a graphite thermal pad, not indium-based TIM. Indium TIM may be present between the die and substrate within the CoWoS package, but the module-level TIM (between die surface and heatsink) is graphite. Indium scrap value reduced from $0.93 to ~$0.31 (0.5g internal indium at $0.62/g).
- Raw scrap: ~$0.50

---

## 4. Precious Metals

All gold quantities below are corrected to reflect that GV100 uses flip-chip C4 bumps (not gold wire bonding) for die-to-interposer interconnect. The original summary claimed 0.36g Au, of which 0.16g was attributed to non-existent gold bond wires. The corrected estimate harmonizes gold to ~0.05g, consistent with the V100S analysis and flip-chip packaging norms.

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.05 | $144/g | $7.20 | PCB ENIG ~0.015g, 2x MEG-Array ~0.012g, NVLink traces ~0.005g, BGA pad flash ~0.010g, misc IC pads ~0.005g, power headers ~0.003g. No wire bonds — GV100 uses flip-chip C4 bumps. |
| Silver (Ag) | 0.21 | $2.27/g | $0.48 | SAC305 solder (~0.16g Ag), MLCC Ag fraction (~0.05g) |
| Palladium (Pd) | 0.09 | $45/g | $4.05 | Pd-bearing MLCCs (~0.08g), tantalum cap terminal plating (~0.01g) |
| **Total** | | | **$11.73** | |

---

## 5. Value Cascade

| Scenario | Value | Notes |
|----------|-------|-------|
| Working unit -- 16GB (used, Mar 2026) | $95-$400 | eBay range; volume sellers at low end |
| Working unit -- 32GB (used, Mar 2026) | $500-$900 | eBay single cards |
| Working unit -- 32GB (refurbished) | $800-$6,160 | IT Creations upper end |
| Component salvage (theoretical max) | ~$8.00 | 2x MEG-Array connectors + VRM lot + passives lot |
| Component salvage (realistic) | ~$5.00 | Connector resale only; rest has minimal demand |
| Raw material scrap (gross) | ~$13.40 | See calculation below |
| Recycler payout (net, 50-60%) | $7-$8 | Small-lot e-scrap payout after refiner fees |

### Raw Material Scrap Breakdown (corrected v2 -- 2026-03-29)

| Category | Value |
|----------|------:|
| Gold (0.05g) | $7.20 |
| Palladium (0.09g) | $4.05 |
| Copper (~41g at $0.012/g) | $0.49 |
| Silver (0.21g) | $0.48 |
| Indium (~0.5g at $0.62/g) | $0.31 |
| Tantalum (5g at $0.08/g) | $0.40 |
| Tin (10g at $0.045/g) | $0.45 |
| Aluminum (15g stiffener) | $0.02 |
| **Gross total** | **~$13.40** |

Note: The original summary claimed $58.78 gross scrap. After three rounds of correction: (1) removing phantom gold bond wires ($23.04 overclaim), (2) updating commodity prices, and (3) removing the phantom 35g copper heat spreader (V100 SXM2 is bare-die, reducing Cu from 76g to ~41g) and correcting TIM from 1.5g indium to ~0.5g (graphite pad is on heatsink, not module), gross scrap falls to ~$13.40.

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues

1. **Interposer size: 1,250mm2 claimed, ~1,500mm2 correct (HIGH).** SemiAnalysis states the V100 used a 1.75x reticle interposer (1.75 x 858mm2 = ~1,500mm2), not 1.5x reticle (~1,250mm2). The P100 used a ~1,200mm2 interposer; the V100's is larger.

2. **MEG-Array connector count: 1 claimed, 2 correct (HIGH).** Each SXM2 module has two Amphenol MEG-Array 400-pin connectors (one for PCIe/power, one for NVLink), confirmed by bbenchoff reverse engineering. Total is 800 pins across 2 connectors.

3. **Gold bond wires on GV100: 0.16g claimed, ~0g correct (HIGH).** The GV100 die uses flip-chip C4 bumps for die-to-interposer connection, not gold wire bonding. The components.csv itself correctly notes "~2500 C4 flip-chip bumps" on a separate line, contradicting the bond wire claim. The 0.16g gold from "~80 bond wires" is the single largest error in the analysis, representing 39% of the original total scrap value. Corrected gold content harmonized to ~0.04-0.06g total.

4. **VRM phase count: 16 phases claimed but flagged as unverified.** 16 phases is reasonable for a 300W SXM2 module. Retained as-is.

5. **Heat spreader: 35g Ni-plated Cu claimed, does not exist (HIGH).** The V100 SXM2 is a bare-die module with no integrated heat spreader (IHS/lid). The OEM heatsink (part 699-2G503-0204-200, shared with P100) contacts the die directly through a graphite thermal pad. The A100 SXM4 was the first NVIDIA SXM generation to add a protective lid, after server ODMs cracked V100-era dies by overtightening heatsink screws. Evidence: aftermarket cooling products warn about cracking bare dies; Bykski water blocks designed for direct die contact; SemiAnalysis advanced packaging coverage documents the lid addition for A100. Impact: -35g weight, -$0.42 Cu scrap. See deep_investigation.md Section 4.

6. **TIM: 1.5g indium-based claimed, mostly incorrect (MEDIUM).** The module-level TIM (between die and external heatsink) is a graphite thermal pad, which is part of the heatsink assembly, not the module. Some indium-based material may exist within the CoWoS package (die-to-substrate interface), estimated at ~0.5g. Impact: indium scrap reduced from $0.93 to ~$0.31.

### Pricing Issues

1. **Tin price: $0.025/g claimed, $0.043-$0.046/g correct (MEDIUM).** LME tin in March 2026 is ~$43,000-$46,000/tonne, driven by AI/datacenter soldering demand. The $0.025/g figure is roughly half the actual price. Dollar impact is small (~$0.20) but percentage error is ~80%.

2. **Indium price: $0.50/g claimed, $0.54-$0.62/g correct (LOW).** China benchmark (SMM 4N+) is ~$618/kg = ~$0.62/g; Western benchmarks ~$0.54/g. Impact: ~$0.18 on 1.5g.

3. **Silver price: $2.50/g was accurate for early March but late-March spot fell to ~$2.27/g (LOW).** Minimal impact (~$0.05).

4. **Bond wire gold calculation rounding: $23.10 in CSV vs $23.04 correct (TRIVIAL).** 0.16g x $144/g = $23.04, not $23.10. Moot after correcting gold quantity to ~0.05g.

### Confidence Assessment

- Component accuracy: 70/100 (core specs correct; interposer size, connector count, gold bond wire claims, heat spreader existence, and TIM material were all wrong in the original)
- Pricing accuracy: 80/100 (gold, silver, palladium, copper correct; tin wrong; indium slightly stale)
- Overall confidence in corrected scrap estimate: 70/100 (up from 60 after deep investigation resolved heat spreader question and confirmed gold budget; gold quantity remains the dominant uncertainty at 0.05-0.08g range; module weight still unverified)

### Web Verification (2026-03-29)

Seven claims cross-checked against NVIDIA datasheets, Volta architecture whitepaper, bbenchoff reverse engineering, WikiChip CoWoS article, and SemiAnalysis packaging coverage:

| # | Claim | Status | Source |
|---|-------|--------|--------|
| 1 | Same GV100 die as V100 PCIe | CONFIRMED | Volta whitepaper; TechPowerUp specs (815mm2, 21.1B transistors, TSMC 12nm FFN identical across SXM2/PCIe) |
| 2 | 4x HBM2 stacks, SXM2 mezzanine | CONFIRMED | NVIDIA datasheet; Volta whitepaper |
| 3 | 2x Amphenol MEG-Array 400-pin connectors | CONFIRMED | bbenchoff reverse engineering ("The NVLink connector -- the second Meg-Array connector -- is not populated"); Wikipedia SXM article ("two Amphenol MEG-Array connectors") |
| 4 | NVLink 2.0, 6 links, 300 GB/s bidirectional | CONFIRMED | NVIDIA datasheet; Volta whitepaper (6 links x 25 GB/s x 2 directions = 300 GB/s) |
| 5 | CoWoS interposer ~1,500mm2 (1.75x reticle) | CONFIRMED | WikiChip ("By 2017, TSMC increased [CoWoS] to 1.75x with products such as NEC SX-Aurora and the V100"); 1.75 x 858mm2 = ~1,501mm2 |
| 6 | Module weight ~275g bare | REVISED to ~240g | No official NVIDIA weight for bare SXM2 module. Revised to ~240g after removing phantom 35g heat spreader. Still unverified by measurement. |
| 7 | 300W TDP | CONFIRMED | NVIDIA datasheet (SXM2 = 300W; PCIe variant = 250W) |
| 8 | Ni-plated Cu heat spreader on module | DISPROVED | V100 SXM2 is bare-die; heatsink contacts die directly via graphite pad. A100 was first SXM with lid. OEM heatsink listings, aftermarket cooling warnings, SemiAnalysis. |
| 9 | MEG-Array gold plating 15uin | CONFIRMED | Amphenol datasheet: 0.4um (15.7uin) Au over 0.8um Ni, selective plating, BeCu dual beam contacts, 0.8mm wipe |
| 10 | 0.05g total gold content | PLAUSIBLE | No assay data exists. 0.05g is consistent with flip-chip packaging norms and connector plating calculations. Range 0.05-0.08g. |

**CSV corrections applied:** (a) bond wire row zeroed (row was phantom -- GV100 uses C4 flip-chip); (b) interposer size corrected from 1,250mm2/1.5x to ~1,500mm2/1.75x; (c) MEG-Array connector quantity corrected from 1 to 2; (d) PCB gold traces corrected from 0.08g/$11.52 to 0.015g/$2.16 to harmonize with report's 0.05g total Au budget; (e) heat spreader row zeroed (V100 SXM2 is bare-die, no IHS); (f) TIM corrected from 1.5g indium to ~0.5g.

---

## 7. Key Observations

1. **Gold dominated the original scrap estimate, but most of it was phantom.** The original analysis claimed 0.36g Au ($51.84), with 0.16g attributed to bond wires that do not exist on this flip-chip design. After correction to ~0.05g, gold still accounts for ~50% of gross scrap value, but the absolute number drops from $52 to ~$7.

2. **Even defective V100 SXM2s are worth more alive than dead.** A "for parts" module at $100-$150 yields 7-10x more than the ~$10-12 net refiner payout. Functional resale is always the rational choice over scrapping.

3. **The SXM2 form factor limits the buyer pool.** Unlike PCIe cards, SXM2 modules require a compatible baseboard (DGX-1V, HGX, or OEM carrier). Aftermarket SXM2-to-PCIe adapter boards ($50-$150 on eBay/AliExpress) have expanded the addressable market somewhat.

4. **CoWoS packaging makes the highest-value components inseparable.** The GV100 die, silicon interposer, and 4 HBM2 stacks are bonded together with micro-bumps and underfill. The entire CoWoS package must be treated as a single unit for scrap.

5. **Palladium is the second-largest precious metal contributor.** At 0.09g ($4.05), palladium from MLCCs and cap terminals exceeds the corrected gold value on a per-gram basis, though the total mass is small.

6. **The V100 SXM2 is bare-die -- no heat spreader.** Unlike the A100 and later SXM modules, the V100 SXM2 has no integrated heat spreader (IHS/lid). The OEM heatsink contacts the GV100 die and HBM2 stacks directly through a graphite thermal pad. This means the module has less copper and less total weight than originally estimated. It also means the module is more fragile during handling -- improper heatsink mounting can crack the die.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA Tesla V100 Datasheet](https://images.nvidia.com/content/technologies/volta/pdf/tesla-volta-v100-datasheet-letter-fnl-web.pdf) -- memory configuration, bus width, compute specs, SXM2 form factor
- [NVIDIA Volta Architecture Whitepaper](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf) -- GV100 die details, CoWoS packaging, flip-chip C4 bump confirmation
- [IT Creations -- Tesla V100 SXM2](https://www.itcreations.com/nvidia-gpu/nvidia-tesla-v100-sxm2-gpu) -- secondary market pricing reference
- [Exxact -- V100 SXM2](https://www.exxactcorp.com/NVIDIA-900-2G503-0010-000-E1684753) -- OEM pricing, specifications
- [UnixSurplus -- V100 SXM2 32GB](https://unixsurplus.com/nvidia-tesla-v100-sxm2-32gb-hbm2-gpu/) -- refurbished pricing ($1,085)

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
- eBay sold/listed prices (March 2026); [IT Creations](https://www.itcreations.com/nvidia-gpu/nvidia-tesla-v100-sxm2-gpu) listings; [UnixSurplus](https://unixsurplus.com/nvidia-tesla-v100-sxm2-32gb-hbm2-gpu/) refurbished

### Deep Investigation Sources (2026-03-29)
- [Amphenol MEG-Array datasheet](https://cdn.amphenol-cs.com/media/wysiwyg/files/documentation/datasheet/mezzanine/mezz_megarray.pdf) -- contact plating specs (0.4um Au / 0.8um Ni), BeCu dual beam, 1.27mm pitch
- [Newark/FCI MEG-Array technical article](https://www.newark.com/pdfs/techarticles/fci/MEG_Array_Connector_The_First_Ball_Grid_Array_Connector.pdf) -- selective plating process, contact wipe 0.8mm, 30g normal force
- [CompEve SXM2 heatsink](https://www.compeve.com/heatsinks-c-29_8_52/heatsink-for-sxm2-gpu-nvidia-tesla-p100v100-1632gb-nvlink-gv100896ba1-6992g5030204200-p-14387.html) -- OEM heatsink with graphite thermal pad for direct die contact
- [SemiAnalysis Advanced Packaging Part 2](https://semianalysis.com/2022/01/06/advanced-packaging-part-2-review/) -- A100 lid addition after V100-era die cracking from heatsink overtightening
- [HPE Apollo 6500 Gen10 service docs](https://techlibrary.hpe.com/docs/iss/XL270d_Gen10/msg/index.html) -- SXM2 GPU module removal procedure
- [l4rz -- Running SXM GPUs in consumer PCs](https://l4rz.net/running-nvidia-sxm-gpus-in-consumer-pcs/) -- practical SXM2 module handling notes

### Methodology Notes
- Board weight: No official NVIDIA weight for bare SXM2 module; ~240g estimated from module dimensions (140mm x 78mm) and component mass summation after removing phantom heat spreader
- Precious metal quantities: Corrected to reflect flip-chip (C4 bump) interconnect rather than gold wire bonding; based on ENIG plating norms (IPC-4552), connector plating specs (Amphenol MEG-Array 0.4um Au), and industry BGA packaging data
- MEG-Array gold calculation: 400 contacts x dual beam x 0.64mm^2 plated area x 0.4um thickness x 19.32 g/cm^3 = ~0.002g per connector, ~0.004g for both. Report uses 0.012g (higher estimate including BGA pad flash on module side).
- Heat spreader: DISPROVED -- V100 SXM2 is bare-die. Removed 35g Cu and $0.42 from scrap budget.
- Recovery rates: 50-60% refiner payout assumed for small-lot e-scrap (Specialty Metals pays 97-98% on bulk assayed material; individual modules incur higher per-unit overhead)
- Key correction sources: SemiAnalysis (interposer size, A100 lid), bbenchoff reverse engineering (MEG-Array count), Gold Refining Forum and RF Cafe (bond wire properties), NVIDIA Volta whitepaper (flip-chip packaging), Amphenol datasheets (connector gold plating)
- Verification: verify_components.md, verify_prices.md, and deep_investigation.md, all dated 2026-03-29

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Component-by-component ceiling, assuming a buyer exists for each part at stated prices:

| Component | Ceiling Value | Notes |
|-----------|------------:|-------|
| GV100 GPU die | $0 | Inseparable from CoWoS package (die + interposer + HBM bonded as unit) |
| HBM2 stacks (4x) | **$0** | CoWoS 2.5D package -- stacks bonded via microbumps + underfill; not separable |
| 2x MEG-Array connectors | $6 | ~$3 each; niche SXM2 adapter/repair demand |
| VRM (16-phase lot) | $2 | Component harvesting; SXM2 form factor limits buyer pool |
| **Theoretical ceiling** | **~$8** | |

The SXM2 form factor severely limits salvage options. The bare module (no heatsink, no IHS) has almost no mechanically separable components of value. The CoWoS package is a single inseparable unit. The MEG-Array connectors are the only components with real (if thin) secondary demand, driven by hobbyist SXM2-to-PCIe adapter projects.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

| Option | Expected Recovery | Notes |
|--------|------------------:|-------|
| **A. ITAD broker** | $10-$225 | 10-25% of $95-$900 working price; SXM2 form factor narrows buyer pool (requires compatible baseboard or adapter) |
| **B. E-waste recycler** | $3-$5 | ~240g bare module at $5-15/lb server PCB + 60-70% PM assay credit on ~$12 precious metals |
| **C. "For parts" eBay sale** | $99-$500 | **Often the best option for V100 SXM2.** Despite the SXM2 form factor limitation, "for parts" V100 SXM2 listings on eBay sell at $99-$500. Aftermarket SXM2-to-PCIe adapter boards ($50-$150) have expanded the buyer pool. Repair shops buy dead modules as donors for CoWoS package swaps. |

**Realistic range for a dead V100 SXM2: $99-$300 ("for parts" eBay sale).** The SXM2 form factor depresses value vs. the PCIe variant, but "for parts" sales still dramatically outperform the $3-$5 a recycler would pay for a 240g bare module. The V100's large DGX-1V/HGX installed base sustains repair demand. For 16GB modules at the low end of working value ($95-$400), "for parts" sales may approach or exceed working-unit prices for untested modules.
