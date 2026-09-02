# AMD Instinct MI300X -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** OAM
**TDP:** 750W
**MSRP:** ~$15,000 | **Used (Mar 2026):** $16,000-$18,000

---

## 1. Card Overview

The AMD Instinct MI300X is among the most complex semiconductor packages ever manufactured, using AMD's "3.5D packaging" -- a combination of 3D die stacking (TSMC SoIC hybrid bonding) and 2.5D silicon interposer (CoWoS-S class). It is an OAM (OCP Accelerator Module) targeting AI training and HPC workloads, with 192GB HBM3 memory and 153 billion transistors across its chiplet complex.

| Attribute | Value |
|-----------|-------|
| GPU die | 8x XCD "Banff" (TSMC N5) + 4x IOD "Elk Range" (TSMC N6) |
| Die area | XCD ~80-115 mm2 each; IOD ~370 mm2 each |
| Transistors | 153 billion (across all 12 logic chiplets) |
| Memory | 192 GB HBM3 (8x 24GB 12-Hi stacks) |
| Memory bus | 8,192-bit |
| Interconnect | 7x AMD Infinity Fabric links (GPU-to-GPU) + PCIe Gen 5.0 x16 |
| TDP | 750 W (max board power 862 W) |
| Board weight | ~765 g estimated (OAM module with heatsink) |
| Packaging | 3.5D: CoWoS-S passive silicon interposer + SoIC hybrid bonding |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (Al fin stack) | 350 | 46% |
| Copper vapor chamber / baseplate | 180 | 24% |
| VRM (inductors + MOSFETs + caps) | 36 | 5% |
| GPU dies (8x XCD + 4x IOD) + interposer + package substrate | 62 | 8% |
| Memory (8x HBM3 stacks) | 48 | 6% |
| Connectors (2x OAM mezzanine) + stiffener + lid/IHS | 71 | 9% |
| Other (solder, TIM, underfill, OAM PCB, passives, misc) | 18 | 2% |
| **Total** | **~765** | **100%** |

Note: AMD does not publish detailed OAM module weights. All weights are estimates derived from OAM spec dimensions (102x165mm), material densities, and comparable datacenter accelerator teardowns. Overall module weight is plausible within the 600-900g range for 750W-class OAM modules with passive cooling.

---

## 3. Component Breakdown

### GPU Dies
- 8x XCD "Banff" chiplets: TSMC N5, ~80-115 mm2 each, 38 enabled CUs per XCD (2 disabled for yield), CDNA 3 architecture
- 4x IOD "Elk Range" dies: TSMC N6, ~370 mm2 each, houses HBM controllers + 64MB Infinity Cache per die (256MB total) + xGMI/PCIe/CXL interfaces
- XCDs are hybrid-bonded to IODs via TSMC SoIC (non-separable)
- Secondary market: XCDs ~$1,200 total ($150 each); IODs ~$300 total ($75 each)
- Raw scrap: ~$0.20 total (semiconductor-grade silicon at ~$5.50/kg)

### Memory
- 8x HBM3 24GB stacks, 12-Hi configuration (12 DRAM layers + 1 base logic die per stack)
- Dual-sourced: SK Hynix (primary/initial supplier) and Samsung (validated Q1 2024, confirmed by TechInsights physical teardown of some units)
- 5.3 TB/s aggregate bandwidth, 8,192-bit interface
- Secondary market: ~$1,600 total (~$200/stack for tested-good pulls)
- Raw scrap: ~$3.60 total (Si + Cu TSVs + solder microbumps + trace Au/Ag)
- HBM3 stacks are the most practically recoverable component (attached via conventional solder bumps, not hybrid bonds)

### Heatsink
- Copper vapor chamber / solid baseplate (~180g) + aluminum fin stack (~350g)
- Passive cooling for OAM form factor, dissipates 750W TDP via server chassis airflow
- Secondary market: ~$8 (generic copper/aluminum thermal assembly)
- Raw scrap: ~$2.87 (Cu 180g at $12.05/kg = $2.17; Al 350g at $2.00/kg = $0.70)
- Note: Aluminum scrap price of $2.00/kg may be ~40-65% high vs. actual scrap yard prices (~$1.21-$1.43/kg); impact is ~$0.20-$0.28.

### VRM / Power Delivery
- Estimated 12-phase for 750W delivery on OAM board (AMD does not publish phase count; 12 is plausible given 48V/54V input from OAM UBB baseboard, which reduces per-phase current vs. 12V architectures)
- Power delivered via OAM baseboard at 48V/54V nominal (OCP UBB spec supports up to 700W+ per module at 48V)
- DrMOS or discrete MOSFETs + chokes
- Secondary market: ~$18 total ($1.50/phase)
- Raw scrap: ~$0.36 (ferrite/Cu in inductors)

### PCB
- OAM spec PCB, 102x165mm, multi-layer FR-4 with Cu traces
- Hosts VRMs, capacitors, resistors, and support components
- Cu content ~8% by weight (~2.8g)
- Secondary market: ~$10 (functional donor board)
- Raw scrap: ~$2.80 (Cu recovery from PCB)

### Connectors
- 2x OAM mezzanine connectors (bottom-side, Molex Mirror Mezz Pro per OAM v1.5 spec): gold-plated pins for high-speed signaling, ~0.002-0.003g Au per connector (revised from 0.05-0.1g per first-principles calibration; see gold_content_analysis.md Section 2.5)
- Secondary market: ~$10 total ($5 each, if undamaged)
- Raw scrap: ~$1.20 total (Au/Cu in plating)

### Other
- Silicon interposer: CoWoS-S passive, TSMC 65nm, ~5,530 mm2 package footprint (76.8x72.0mm per TechInsights). Bare interposer silicon area is ~2,831 mm2 (~3.5x reticle at ~830 mm2/reticle), which is the CoWoS-S maximum. The remaining package footprint area is organic substrate margin and BGA ball field extending beyond the interposer.
  - Secondary market: ~$250 (limited reuse potential; manufacturing cost $500-$1,500)
  - Raw scrap: ~$0.05 (high-purity silicon)
- Package substrate: large organic BT/FR4 multi-layer, ~77x72mm, gold-plated BGA pads
  - Secondary market: ~$25
  - Raw scrap: ~$3.50 (est. ~0.003g Au in BGA ENIG pads + 2-3g Ag in plating/traces, Cu content ~15-20%; Au revised from 0.3-0.5g per first-principles calibration)
- Lid/IHS: nickel-plated copper, ~30g
  - Secondary market: ~$2
  - Raw scrap: ~$0.36
- Stiffener frame: nickel-plated steel, ~25g
  - Secondary market: ~$1
  - Raw scrap: ~$0.08
- TIM: indium-based solder or thermal compound, ~2g
  - Raw scrap: ~$0.80-$1.00 (indium at ~$0.40-$0.50/g after scrap discount)
  - Correction: Original claimed $0.15 using indium at $0.30/g. Market price in 2026 is $0.69-$0.97/g pure; scrap recovery at 30-40% discount gives ~$0.40-$0.50/g.
- Underfill epoxy: capillary underfill protecting solder joints, no recovery value
- BGA solder (SAC305): ~3g, scrap ~$0.12
- Silicon shims/spacers: ~12+ pieces used for structural support in 3D SoIC stacking (analogous to 3D V-Cache packaging). Omitted from original BOM. Negligible individual value.
- Misc SMD passives (~100): resistors, ferrite beads, ceramic. No meaningful scrap value.

### Total Die / Silicon Piece Count
- 12 logic dies (8 XCD + 4 IOD) + 104 HBM dies (8 stacks x 13 dies each: 12 DRAM + 1 base) = 116 functional dies
- Plus 1 interposer + ~12+ silicon shims/spacers = ~130+ total silicon pieces
- AMD publicly claims "over 100 pieces of silicon" -- the 116 functional dies alone exceed this before counting shims and interposer
- Note: Original report erroneously listed "8-Hi" (8 DRAM + 1 base = 9 per stack, 72 HBM total, 84 functional). Corrected to 12-Hi per SK Hynix and Samsung HBM3 specifications for 24GB stacks.

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.02-0.03 | $145/g | $2.90-$4.35 | First-principles build-up (see gold_content_analysis.md): OAM mezzanine connectors 2x (~0.005g total), BGA ENIG pads (~0.003g), PCB ENIG surface finish (~0.008g). Total ~0.016g, range 0.02-0.03g. Previous 0.40g estimate was ~14-20x too high due to confusing plating thickness with component mass and extrapolating from inapplicable consumer GPU benchmarks. 3.5D packaging (SoIC hybrid bonding, CoWoS-S interposer) does not add meaningful gold -- these use copper-based metallurgy throughout. |
| Silver (Ag) | 0.15 | $2.25/g | $0.34 | SAC305 BGA solder (~3g x 3% Ag = 0.09g) + MLCC terminations (~0.06g). **Revised from 5.0g:** original erroneously included "substrate traces" and "thermal interface layers" as silver sources -- neither contains meaningful silver. A 765g OAM module has ~3-5g of SAC305 solder total; 3% of ~4g midpoint = 0.12g Ag from solder, +25% for MLCC = ~0.15g. |
| Palladium (Pd) | 0.005 | $45.16/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.08g. |
| **Total** | | | **$3.47-$4.92** | |

Notes on precious metals:
- Gold revised from 0.40g to 0.02-0.03g following first-principles calibration (gold_content_analysis.md). OAM connectors, BGA pads, and PCB ENIG finish are the only meaningful gold sources. HBM3 microbumps use copper pillar + SnAg solder with negligible Au UBM wetting layer (~0.01 mg total for all 8 stacks). SoIC hybrid bonds are Cu-Cu direct bonds with zero gold.
- **Silver revised from 5.0g to 0.15g** (2026-03-29). The original 5.0g was ~33x too high. Silver in electronics comes almost entirely from SAC305 solder (3% Ag by weight). The MI300X OAM module has only ~3-5g of BGA solder total. Substrate traces use copper, not silver. Thermal interface layers (indium-based) do not contain silver. The corrected 0.15g is physically consistent with the solder mass of the module.
- Recovery rates for professional refining: Au ~65%, Ag ~70%, Pd ~70%. Net recoverable precious metals: ~$5-$6.

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $16,000-$18,000 | 107-120% |
| Component salvage (theoretical max) | $3,426 | 22.8% |
| Component salvage (realistic) | $50-$200 | 0.3-1.3% |
| Raw material scrap (gross) | ~$30-$31 | 0.20-0.21% |
| Recycler payout (net, what you'd receive) | $12-$19 | 0.08-0.13% |

Notes:
- Used MI300X cards trade above MSRP due to AI/HPC demand and supply constraints.
- Theoretical component salvage of $3,426 assumes perfect recovery. In practice, 3.5D packaging makes chiplet-level salvage nearly impossible -- XCDs are hybrid-bonded to IODs via SoIC and cannot be non-destructively separated. HBM3 stacks are the most practically recoverable component.
- Realistic salvage for a dead unit is $50-$200 sold as-is for parts/scrap.

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **HBM3 supplier attribution [MODERATE]:** Original listed SK Hynix as sole supplier. AMD dual-sourced HBM3: SK Hynix was primary/initial, Samsung was validated Q1 2024 and confirmed in some units by TechInsights physical teardown.
- **Die count and HBM3 stack height [HIGH]:** Original stated "84 individual silicon dies" based on 8-Hi HBM3 stacks (8 DRAM + 1 base = 9 per stack, 72 HBM total). Corrected: 24GB HBM3 stacks are 12-Hi (12 DRAM + 1 base = 13 per stack), giving 104 HBM dies and 116 functional dies total. Both SK Hynix and Samsung use 12-Hi for 24GB HBM3. AMD's "over 100 pieces of silicon" claim is consistent with 116 functional dies + interposer + shims.
- **Interposer area conflation [MODERATE]:** 5,530 mm2 (76.8x72.0mm) is confirmed as the package footprint (per TechInsights), not the bare interposer silicon area. Bare interposer is ~2,831 mm2 (3.5x reticle) -- roughly half the package footprint, not "slightly smaller" as previously stated.
- **Reticle multiplier [MINOR]:** Listed as 3.3x reticle. SemiAnalysis and most sources cite 3.5x for the MI300X specifically.
- **Missing silicon shims [MINOR]:** ~12+ silicon shims/spacers for 3D stacking structural support were omitted from the original BOM. SemiAnalysis specifically mentions "more than a dozen pieces of support silicon." Negligible scrap value but relevant to die count.
- **Missing components [MINOR]:** Serial EEPROM/SPD chip, discrete temperature sensors, and additional thermal pads/gaskets between IHS and heatsink were omitted. All have negligible value.

### Pricing Issues
- **Tin price [MODERATE]:** Claimed $25/kg; actual LME tin in March 2026 was ~$43/kg (nearly double). Impact on total is small (~$0.08 on 5g of solder).
- **Indium price [MODERATE]:** Claimed $0.30/g scrap; actual 2026 indium market is $0.69-$0.97/g pure, with scrap at ~$0.40-$0.50/g after discount. TIM scrap value corrected from $0.15 to ~$0.80-$1.00. Impact: ~$0.65-$0.85.
- **Silver spot price [MINOR]:** Claimed $2.45/g, which was accurate for mid-March but ~8% high for late March 2026 (~$2.27/g). Impact: ~$0.90 reduction in gross Ag value.
- **Aluminum scrap price [MINOR]:** Claimed $2.00/kg which is closer to primary aluminum pricing. Actual scrap yard prices are ~$1.21-$1.43/kg. Impact: ~$0.20-$0.28.
- **HBM3 secondary pricing [UNCERTAIN]:** $200/stack for tested-good pulls is plausible but unverifiable. The secondary market for individual HBM stacks is extremely thin.
- **All arithmetic verified correct.** Both the $51.62 raw scrap total and $3,426 component salvage total are accurately computed from their inputs. Rounding differences are within $0.01.

### Confidence Assessment
- Component accuracy: 80/100
- Pricing accuracy: 78/100
- Overall confidence in scrap estimate: 75/100

### Web Verification (2026-03-29)

Independent verification of key claims against public sources:

1. **8 XCD + 4 IOD chiplet layout -- CONFIRMED.** TechInsights floorplan analysis ([link](https://www.techinsights.com/blog/amd-instinct-mi300x-processor-floorplan-analysis)) confirms 8 XCD (TSMC N5) + 4 IOD (TSMC N6). Each pair of XCDs is 3D-stacked atop one IOD via SoIC hybrid bonding at 9um pitch. Die photos show the 4-quadrant layout with 2 HBM stacks flanking each IOD.

2. **HBM3 12-Hi stacks, dual-sourced -- CONFIRMED (with correction).** Both SK Hynix ([link](https://news.skhynix.com/sk-hynix-develops-industrys-first-12-layer-hbm3/)) and Samsung Icebolt ([link](https://semiconductor.samsung.com/dram/hbm/hbm3-icebolt/)) use **12-Hi** (not 8-Hi) for 24GB HBM3 stacks: 12 DRAM layers of 16Gb each + 1 base logic die = 13 dies per stack. TechInsights confirmed Samsung HBM3 in MI300X units ([link](https://www.techinsights.com/blog/techinsights-analysis-amds-mi300x-reveals-samsung-hbm3)). Samsung validated Q1 2024 per TrendForce ([link](https://www.trendforce.com/presscenter/news/20240313-12075.html)).

3. **Interposer: 5,530mm2 is package footprint, not bare interposer -- CONFIRMED.** TechInsights gives package dimensions as 76.8x72.0mm = 5,530mm2. The CoWoS-S passive silicon interposer itself is ~2,831mm2 (3.5x reticle, where one reticle is ~830mm2), which is the CoWoS-S maximum capacity. The difference is organic substrate margin and BGA ball field.

4. **OAM form factor, 750W TDP -- CONFIRMED.** AMD datasheet confirms 750W TDP, 862W max board power. OAM module uses Molex Mirror Mezz Pro mezzanine connectors (OAM v1.5 spec, [link](https://www.molex.com/en-us/blog/mirror-mezz-pro-connector-selected-for-open-compute-project)), not generic connectors. Power delivered via OAM UBB baseboard at 48V/54V nominal.

5. **Total silicon die count -- CORRECTED UPWARD.** With 12-Hi HBM3 stacks: 12 logic + 104 HBM (8x13) = 116 functional dies + 1 interposer + ~12+ shims = ~130+ total silicon pieces. AMD's "over 100 pieces of silicon" claim ([SemiAnalysis](https://semianalysis.com/2023/06/12/amd-mi300-taming-the-hype-ai-performance/)) is consistent. Previous report listed 84 functional dies based on incorrect 8-Hi assumption.

6. **SoIC hybrid bonding (XCD-to-IOD) -- CONFIRMED non-separable.** XCDs are hybrid-bonded to IODs via TSMC SoIC gen 1 at 9um pitch ([Hot Chips 2024](https://hc2024.hotchips.org/assets/program/conference/day1/23_HC2024.AMD.MI300X.ASmith(MI300X).v1.Final.20240817.pdf)). These are Cu-Cu direct bonds with oxide bonding -- physically inseparable without destroying both dies. Silicon shims are required for structural support due to die thinning for TSV exposure, analogous to 3D V-Cache packaging.

7. **VRM phase count -- UNVERIFIABLE.** AMD does not publish VRM phase count for the MI300X OAM module. The 12-phase estimate is plausible but unconfirmed. The OAM UBB delivers power at 48V/54V (OCP spec supports up to 700W+ per module at 48V, [link](https://www.opencompute.org/documents/ocp-accelerator-module-design-specification-v1p5-final-20220223-docx-1-pdf)), which reduces per-phase current demand vs. 12V by ~4x, making 12 phases reasonable for 750W.

---

## 7. Key Observations

1. **The MI300X has an exceptionally low scrap-to-MSRP ratio (~0.20%).** The overwhelming majority of value is in advanced packaging (hybrid bonding, CoWoS interposer) and IP/design, not raw materials. At ~$30-$31 gross scrap, the materials in a $15,000 module are worth less than a cheap restaurant meal. Recycler payout of $12-$19 is negligible.

2. **3.5D packaging makes chiplet-level salvage nearly impossible.** The XCDs are hybrid-bonded to IODs via SoIC -- these bonds cannot be non-destructively separated. This fundamentally distinguishes the MI300X from conventional flip-chip BGA packages where die removal is routine. The theoretical $3,426 component salvage figure is academic.

3. **HBM3 stacks are the only practically recoverable high-value component.** At ~$200/stack ($1,600 total), they sit on the interposer via conventional solder bumps and can theoretically be removed. But this requires specialized rework equipment and yields are uncertain.

4. **Silver, not gold, is the largest precious metal contributor.** After first-principles gold calibration, silver ($11.35 gross from 5.00g in SAC solder and substrate traces) exceeds gold ($2.90-$4.35 gross from 0.02-0.03g) as the dominant precious metal by value. Precious metals ($18-$19 total) account for ~60% of gross scrap value, with base metals (~$12) making up the rest. The previous claim that gold alone was worth more than all base metals combined was based on a ~14-20x overestimate of gold content.

5. **The interposer is a cost-value paradox.** Manufacturing cost of $500-$1,500 for the ~2,831 mm2 bare silicon interposer (within a 5,530 mm2 package footprint), but scrap value is ~$0.05 (raw silicon) and secondary reuse is essentially nil.

6. **Used MI300X units trade above MSRP** ($16,000-$18,000 vs. $15,000 MSRP), reflecting sustained AI/HPC demand. This makes any scrap or salvage scenario relevant only for confirmed-dead units.

---

## 8. Methodology & Sources

### GPU Specifications
- [AMD Instinct MI300X Product Page](https://www.amd.com/en/products/accelerators/instinct/mi300/mi300x.html) -- official product overview
- [AMD Instinct MI300X Data Sheet](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-data-sheet.pdf) -- detailed specs, 750W TDP, 192GB HBM3
- [AMD Instinct MI300X Platform Data Sheet](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-platform-data-sheet.pdf) -- OAM platform integration, power delivery
- [Hot Chips 2024 -- MI300X Presentation](https://hc2024.hotchips.org/assets/program/conference/day1/23_HC2024.AMD.MI300X.ASmith(MI300X).v1.Final.20240817.pdf) -- die architecture, 3.5D packaging details
- [TensorWave MI300X Deep Dive](https://tensorwave.com/blog/mi300x-2) -- detailed technical analysis
- [Chips and Cheese MI300X Testing](https://chipsandcheese.com/p/testing-amds-giant-mi300x) -- independent verification, performance and architecture
- Die sizes and architecture: TechInsights floorplan analysis, SemiAnalysis ("AMD MI300 -- Taming the Hype")
- BOM estimates: SemiAnalysis ($5,300 total), TrendForce, Epoch AI, Raymond James
- HBM3 pricing: TrendForce ($200-$225/stack new), Wevolver ($120/stack for 16GB HBM3), scaled to 24GB
- Physical verification: TechInsights MI300X floorplan, Samsung HBM3 teardown from MI300X, OCP Accelerator Module spec v1.5/v2.0
- Weight estimates: Derived from OAM dimensions (102x165mm), material densities, and comparable OAM/SXM module teardown data
- HBM3 supplier dual-sourcing: TrendForce (Samsung validated Q1 2024), TechInsights (Samsung HBM3 confirmed in physical analysis), AMD-Samsung deal reporting
- Recovery rates: 60-70% for precious metals through professional refining

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report
- **PCB scrap rates:** [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)
- Tin ~$43/kg (LME); Indium ~$0.69-$0.97/g pure (Trading Economics)

### Secondary Market
- GPUCost.org ($18,000 market price)
- eBay active listings (Mar 2026)

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Assumes every component is perfectly extracted and sold to the highest-value buyer globally.

| Component | Ceiling Value | Notes |
|-----------|--------------|-------|
| XCD dies (8x) | $1,200 | $150 each; Shenzhen gray-market only. SoIC hybrid bonds make extraction impossible without destroying both XCD and IOD. |
| IOD dies (4x) | $300 | $75 each; same SoIC constraint as XCDs -- these are non-separable |
| HBM3 stacks (8x) | **$0** | CoWoS-S interposer with capillary underfill + 40um-pitch microbumps. No commercial rework service exists. No secondary market for individual HBM stacks (zero listings found anywhere). Per hbm_secondary_market.md: "realistic standalone value: $0." |
| Interposer | $250 | CoWoS-S passive, ~2,831 mm2. Manufacturing cost $500-$1,500 but no reuse pathway |
| Heatsink (Cu/Al) | $8 | Generic thermal assembly; or ~$2.87 as raw Cu/Al scrap |
| VRM components | $18 | $1.50/phase; labor cost exceeds value in US |
| Connectors (2x OAM mezz) | $10 | $5 each if undamaged; extremely thin buyer pool |
| Package substrate | $25 | Organic BT/FR4, limited reuse |
| **Total** | **~$1,811** | Requires Shenzhen-only buyers and physically impossible die separation |

The $3,426 theoretical max in Section 5 includes $1,600 for HBM3 stacks and $1,500 for XCD/IOD dies. In practice: HBM3 stacks have $0 separable value (per hbm_secondary_market.md), and XCD-to-IOD SoIC hybrid bonds at 9um pitch are physically inseparable. The realistic ceiling with these corrections is ~$310 (interposer + VRM + connectors + heatsink + substrate), accessible only to Shenzhen-class operations.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator actually receives for a dead MI300X:

**Option A -- Sell dead card to ITAD broker:** At 10-25% of used working price ($16,000-$18,000), expect **$1,600-$4,500**. However, the MI300X's OAM form factor and AMD/ROCm ecosystem limit the broker pool. Fewer buyers than NVIDIA equivalents; expect the lower end of the range.

**Option B -- E-waste recycler by weight:** Module weighs ~765g (~1.69 lb). At $5-15/lb server PCB rate: $8-$25 base. PM assay credit at 60-70% recovery on ~$4.92 gross precious metals adds ~$3-$3.50. Total: **$11-$29**.

Component harvesting is not viable in the US. The 3.5D packaging (SoIC + CoWoS) makes every high-value component physically inseparable without TSMC-class equipment that does not exist in the repair ecosystem.

**Realistic range: $1,600-$4,500** (broker, Option A preferred) or **$11-$29** (recycler, last resort).
