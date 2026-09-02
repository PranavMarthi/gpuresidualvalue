# NVIDIA A100 SXM4 80 GB -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** SXM4
**TDP:** 400W
**MSRP:** $10,000-$11,000 | **Used (Mar 2026):** $4,500-$7,000

---

## 1. Card Overview

The NVIDIA A100 SXM4 is an Ampere-generation datacenter GPU module designed for NVIDIA HGX baseboards, providing 80 GB of HBM2e memory and 600 GB/s NVLink 3.0 interconnect. It is a mezzanine-style module with no onboard heatsink or fan, relying on the baseboard cooling assembly and server chassis airflow.

| Attribute | Value |
|-----------|-------|
| GPU die | GA100 (TSMC N7) |
| Die area | 826 mm2 |
| Transistors | 54.2 billion |
| Memory | 80 GB HBM2e (5 x 16 GB, 8-Hi stacks) |
| Memory bus | 5120-bit |
| Interconnect | NVLink 3.0 (12 links, 600 GB/s bidirectional) |
| TDP | 400 W |
| Board weight | ~300-350 g estimated (bare module, no heatsink) |
| Packaging | CoWoS-S (flip-chip with copper pillar bumps on silicon interposer) |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Module PCB | 120 | 37.0% |
| BGA package substrate (55x55 mm, 12-layer) | 35 | 10.8% |
| GPU die (GA100, bare silicon) | ~1.5 | 0.5% |
| Silicon interposer (CoWoS-S, ~1,200 mm2) | ~1 | 0.3% |
| HBM2e stacks (5x, all-in) | ~0.5 | 0.2% |
| Vicor MCD + 2x MCM | 20 | 6.2% |
| DC-DC converters (3x) | 12 | 3.7% |
| Mezzanine connectors (2x) | 36 | 11.1% |
| Module stiffener/frame (aluminum) | 25 | 7.7% |
| Passive components (MLCCs, tantalum, inductors) | ~34 | 10.5% |
| Other (solder, TIM, underfill, misc) | ~40 | 12.3% |
| **Total** | **~325** | **100%** |

Note: Component weights for die, interposer, and HBM stacks have been corrected downward from the original components.csv (which listed 10g, 12g, and 3.5g respectively). Bare silicon components at these dimensions weigh well under 2g each. The total module weight of ~325g is an estimate; no public source provides a weighed bare SXM4 module.

---

## 3. Component Breakdown

### GPU Die
- GA100, 826 mm2, 54.2B transistors, TSMC N7 (7nm FinFET)
- Secondary market: $150 (reballing/rework candidate for repair; extremely niche)
- Raw scrap: $0.05 (silicon scrap at ~$5/kg)

### Memory
- 5 x 16 GB HBM2e 8-Hi stacks (Samsung Flashbolt or SK Hynix), 80 GB total
- 40 GB variant uses 5 x 8 GB HBM2 8-Hi stacks (eight 1 GB dies per stack, not 4-Hi as originally stated)
- Secondary market: $300 total ($60/stack, if tested good -- impractical to decouple from interposer)
- Raw scrap: $0.10 (silicon + trace metals in micro-bumps)

### Heatsink
- None onboard. SXM4 is a bare module; cooling provided by HGX baseboard heatsink/cold plate.

### VRM / Power Delivery
- 48V input via mezzanine connector
- 1x Vicor MCD (Modular Current Divider, 48V to intermediate bus)
- 2x Vicor MCM (Modular Current Multipliers; MCM4608 ChiP-set rated 600A continuous / 1,000A peak per Vicor press release)
- 3x auxiliary DC-DC converters (5V memory rail, 12V ancillary)
- Secondary market: $85 total (MCD $25, MCMs 2x$20, DC-DCs 3x$5)
- Raw scrap: $1.00

### PCB
- Multi-layer high-Tg FR-4 module PCB, ~120g
- Cu content ~15g in traces and planes
- Secondary market: $25 (donor board for component harvest)
- Raw scrap: $1.20

### Connectors
- 2x Amphenol MEG-Array mezzanine connectors (1.27 mm pitch): one for PCIe/power, one for NVLink
- Gold-plated contacts, ~0.002g gold per connector (~0.004g total) per first-principles calculation (50 uin selective gold on ~800 total pins with ~0.5 mm^2 contact area each)
- Secondary market: $30 total (2x$15, used in SXM adapter projects)
- Raw scrap: $0.58 (gold in contact plating ~$0.58; copper/nickel negligible)

### Other
- TIM: indium-based high-performance thermal interface, ~2g ($1.20 scrap at corrected $600/kg)
- BGA solder balls: SAC305 lead-free (96.5% Sn / 3% Ag / 0.5% Cu), ~8g
- Underfill/molding compound: epoxy resin, no recoverable value
- Module stiffener: aluminum frame, ~25g ($0.05 scrap)
- ~200 MLCC capacitors (BME/nickel, negligible precious metal), ~8 tantalum capacitors, ~6 inductors/ferrite beads
- Missing from original BOM but present: EEPROM (FRU ID), temperature sensors, status LEDs, MCU, resistor networks, ESD protection diodes (all negligible scrap value)
- Raw scrap: ~$2.50

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | ~0.02 | $144/g | $2.88 | 2x MEG-Array mezzanine connectors (~0.004g total), BGA ENIG pads (~0.003g), PCB ENIG surface finish (~0.008g). First-principles build-up per gold_content_analysis.md. SXM4 has NO PCIe gold fingers. No wire bonds -- CoWoS uses Cu pillar bumps. Range: 0.015-0.025g. |
| Silver (Ag) | ~0.28 | $2.25/g | $0.63 | SAC305 solder (~8g x 3% Ag = 0.24g) + MLCC terminations (~0.04g). **Revised from 0.8g:** original erroneously attributed 0.3g to "mezzanine connector plating" (which uses gold-over-palladium, not silver) and 0.26g to "substrate traces" (which use copper, not silver). A 325g SXM module has ~5-8g of SAC305 solder; 3% of 8g = 0.24g Ag from solder, +15% for MLCC = ~0.28g. |
| Palladium (Pd) | 0.005 | $45/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.05g. |
| **Total** | | | **$3.74** | |

Note: Gold revised from 0.25g to 0.02g based on first-principles engineering analysis (gold_content_analysis.md). The original 0.25g was ~12x too high, driven by overestimates of mezzanine connector plating (0.16g claimed vs. ~0.004g calculated) and BGA pad gold (0.05g claimed vs. ~0.003g calculated). SXM4 has no PCIe edge fingers -- the only gold sources are the 2x Amphenol MEG-Array mezzanine connectors (~0.004g total, ~800 pins at 50 uin selective gold plating on small contact areas), BGA ENIG on the 55x55mm CoWoS package substrate (~0.003g), and PCB ENIG surface finish (~0.008g). The original 0.15g "gold wire bonds" line item was already correctly removed (CoWoS-S uses copper pillar bumps).

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $4,500-$7,000 | 45-70% |
| Component salvage (theoretical max) | $630 | 6.3% |
| Component salvage (realistic) | $100-$200 | 1-2% |
| Raw material scrap (gross) | ~$24 | 0.2% |
| Recycler payout (net, what you'd receive) | $11-$15 | 0.1-0.15% |

*Note: Raw scrap revised downward from ~$57 following gold recalibration from 0.25g to 0.02g (see Section 4 notes). Non-precious-metal scrap (~$17) is unchanged; the reduction is entirely in gold value (-$33).*

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **40 GB HBM2 stack height [MATERIAL ERROR]:** Originally claimed 4-Hi (8 GB each). Corrected to 8-Hi (eight 1 GB dies per stack = 8 GB each). AnandTech confirms 8-Hi stacking for HBM2.
- **Gold wire bonds [MATERIAL ERROR]:** Originally claimed 0.15g gold in wire bonds. The A100 uses flip-chip copper pillar bumps via CoWoS-S, not gold wire bonds. Line item removed. Gold is present only in pad plating and connector surfaces.
- **GPU die weight [OVERESTIMATE]:** Originally 10g. Bare GA100 die (826 mm2, ~0.77 mm thick) weighs ~1.5g. The 10g figure conflated the die with the broader CoWoS assembly.
- **Silicon interposer weight [OVERESTIMATE]:** Originally 12g. A thinned CoWoS interposer (~1,200 mm2, ~0.1 mm thick) weighs well under 1g.
- **HBM stack weight [OVERESTIMATE]:** Originally 3.5g per stack. An 8-Hi stack on a ~92 mm2 footprint should weigh well under 1g (~0.1g estimated).
- **Vicor MCM current ratings [VERIFIED]:** 600A continuous / 1,000A peak is correct per Vicor's MCM4608 ChiP-set press release (Mar 2018). A newer MCM4609 ChiP-set raises this to 650A / 1,200A. The earlier "320A / 640A" correction was itself in error.

### Pricing Issues
- **Indium price [WRONG]:** Originally ~$250/kg. Corrected to ~$600/kg (SMM/Western benchmarks, Mar 2026). Indium surged due to Chinese export licensing (Feb 2025). Impact: +$0.37 net on TIM scrap -- immaterial to totals.
- **Tin price [WRONG]:** Originally ~$35/kg. Corrected to ~$43/kg (LME, Mar 2026). Impact: +$0.06 on solder ball scrap -- immaterial.
- **A100 SXM4 40 GB used price [WRONG]:** Originally $2,500-$3,000. Corrected to $3,500-$4,500 based on current eBay data (eBay listing at $4,050 with 179 units sold).
- **BGA gold pad recovery yield [UNCERTAIN]:** components.csv implies ~6.5% net yield ($2.80 on $43 gross). The summary uses 50% recovery on total gold. These are internally inconsistent. The 50% figure in the summary is more standard for refinery-grade recovery.

### Confidence Assessment
- Component accuracy: 70/100
- Pricing accuracy: 72/100
- Overall confidence in scrap estimate: 70/100

---

## 7. Key Observations

1. **Scrap value is negligible relative to working resale.** A working A100 SXM4 80 GB fetches $4,500-$7,000 used. Raw material scrap is ~$24 gross (~$11-15 net after refining), less than 0.25% of used resale. Even optimistic component harvesting tops out at ~$630, and realistic recovery is $100-$200.

2. **Gold is a minor contributor to scrap after recalibration.** At March 2026 gold prices ($144/g), the ~0.02g of gold in pad plating and connector surfaces accounts for $2.88 of the $6.96 gross precious metal value (41%). The original 0.25g estimate was ~12x too high -- the SXM4 has no PCIe edge fingers, and the MEG-Array mezzanine connectors contain far less gold than originally estimated (~0.004g total vs. 0.16g claimed). Non-precious-metal scrap (~$17) now dominates the raw material total.

3. **CoWoS packaging makes component harvesting impractical.** The 2.5D CoWoS-S integration (GA100 die + 5 HBM stacks on a silicon interposer) makes non-destructive die separation nearly impossible without TSMC-grade repackaging equipment. The practical salvage pathway is limited to Vicor power modules and connectors.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA A100 Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/nvidia-a100-datasheet-us-nvidia-1758950-r4-web.pdf) -- official specs, TDP, memory configuration
- [NVIDIA Ampere Architecture Whitepaper](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf) -- GA100 die details, CoWoS packaging, NVLink 3.0
- [Amazon listing (900-2G506-0210-320)](https://www.amazon.com/Module-HBM2e-Memory-900-2G506-0210-320-965-2G506-0031-200/dp/B0FM6SJX3F) -- confirms 400W TDP, SXM4 form factor
- [IT Creations A100 SXM](https://www.itcreations.com/nvidia-gpu/nvidia-a100-sxm-gpu) -- product reference and secondary market context
- Board weight: No NVIDIA-published weight for bare SXM4 module; estimated from component sum (~325g)
- Additional references: System Plus Consulting A100 teardown (SP20579), AnandTech A100 80GB analysis, l4rz SXM4 hobbyist teardown, Vicor power-on-package documentation

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)
- Precious metal quantities estimated from BGA pad count, connector pin count, substrate area, and industry benchmarks. No destructive assay performed.
- Recovery rates: 40-60% yield assumed for precious metals via professional refining; 50% midpoint used for summary calculations

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report
- **PCB scrap rates:** [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)
- Indium ~$600/kg (SMM/Western benchmarks, corrected for Chinese export licensing surge)

### Secondary Market
- eBay sold/active listings (Mar 2026)
- Project file data/scraped_datacenter_supplement.csv

---

## 9. Component Verification (Deep Research)

Independent web research conducted 2026-03-29 against teardown sources, Vicor press releases, NVIDIA whitepapers, AnandTech, Samsung HBM2 product data, and the System Plus Consulting SP20579 report sample.

### Confirmed

| Claim | Status | Source |
|-------|--------|--------|
| GA100 die: 826 mm2, 54.2B transistors, TSMC N7 | Confirmed | NVIDIA Ampere Architecture Whitepaper |
| BGA package substrate: 55x55 mm, 12-layer | Confirmed | System Plus Consulting SP20579 |
| CoWoS-S packaging (flip-chip, Cu pillar bumps, silicon interposer) | Confirmed | NVIDIA whitepaper; System Plus SP20579 |
| 80 GB variant: 5 active 8-Hi HBM2e stacks, 16 GB/stack (2 GB/die) | Confirmed | AnandTech; Samsung Flashbolt spec |
| 40 GB variant: 5 active 8-Hi HBM2 stacks, 8 GB/stack (1 GB/die) | Confirmed | Samsung 8GB HBM2 KGSD = eight 8Gb dies (8-Hi) |
| NVLink 3.0: 12 links, 600 GB/s bidirectional | Confirmed | NVIDIA A100 datasheet; NVLink Wikipedia |
| 2x Amphenol MEG-Array mezzanine connectors (PCIe+power / NVLink) | Confirmed | l4rz SXM teardown; SXM Wikipedia; Grokipedia |
| 48V input via Vicor MCD + 2x MCM power delivery | Confirmed | l4rz teardown photos; Vicor PoP press releases; SemiAnalysis |
| No onboard heatsink (bare mezzanine module) | Confirmed | All SXM4 product listings; l4rz teardown |
| TDP: 400W (SXM4 form factor) | Confirmed | NVIDIA A100 datasheet |
| Vicor designed out of H100 (replaced by MPS) | Confirmed | SemiAnalysis |

### Corrections Made

| Item | Previous (Erroneous) | Corrected | Source |
|------|----------------------|-----------|--------|
| Vicor MCM current ratings | Report said "320A / 640A" and flagged original 600A/1000A as exceeding spec | 600A continuous / 1,000A peak is correct per MCM4608 ChiP-set (newer MCM4609: 650A / 1,200A) | Vicor press release (Mar 2018); Vicor Hydra II (May 2020) |
| Section 7 gold/silver figures | Referenced "~0.5g gold" and "~5g silver" (stale from pre-revision) | Updated to match Section 4 revised estimates (0.25g Au, 0.8g Ag) | Internal consistency fix |

### Unverifiable (No Public Source)

| Claim | Notes |
|-------|-------|
| Bare SXM4 module weight ~325g | No NVIDIA-published weight; no teardown source provides a weighed bare module. Component-sum estimate is plausible given the A100 PCIe card weighs 1,240g with heatsink/bracket, and the SXM4 is a much smaller bare board. |
| Individual component weights (PCB 120g, stiffener 25g, connectors 18g each) | Reasonable engineering estimates but not independently verified |
| Gold content ~0.25g, Silver ~0.8g | Order-of-magnitude plausible for ENIG pad finish + connector plating on a module this size, but no destructive assay exists |

### No Missing Components Identified

The BOM covers all major subsystems: GPU die, HBM stacks, interposer, power delivery (MCD + MCMs + DC-DCs), connectors, passives (MLCCs, tantalum caps, inductors), TIM, solder, underfill, stiffener, and supporting ICs (EEPROM, temp sensors, MCU, ESD diodes). No significant omissions found.

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Absolute ceiling assuming perfect component recovery, 100% precious metal extraction, and a buyer for every part. Note: SXM4 is a bare module with no onboard heatsink, and CoWoS packaging prevents die/HBM extraction.

| Component | Basis | Value |
|-----------|-------|-------|
| GPU die (GA100) | $0 -- permanently bonded to CoWoS interposer (per hbm_secondary_market.md) | $0 |
| HBM2e stacks (5x 16GB) | $0 -- bonded via microbumps + underfill; no secondary market exists | $0 |
| Vicor MCD + 2x MCM modules | Shenzhen repair market, tested modules | $85 |
| DC-DC converters (3x) | Component harvest at $5/ea | $15 |
| MEG-Array connectors (2x) | Niche SXM adapter projects, $15/ea | $30 |
| PCB (120g module board) | Server-grade e-scrap at $12/lb | $3.15 |
| Precious metals (0.02g Au, 0.28g Ag) | 100% extraction at spot ($144/g Au, $2.25/g Ag) | $3.51 |
| TIM (indium, 2g) | Indium scrap at $600/kg | $1.20 |
| **Total theoretical max** | | **~$138** |

The Vicor power modules ($85) and MEG-Array connectors ($30) drive 83% of the theoretical max. These are the only components with identifiable buyers. The CoWoS-bonded GPU die and HBM stacks -- which would dominate value on a non-CoWoS card -- contribute $0. No heatsink scrap since the SXM4 is a bare module.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator would actually receive for a dead A100 SXM4 module.

| Channel | Basis | Payout |
|---------|-------|--------|
| ITAD/broker (whole dead module) | 15-25% of $4,500-$7,000 used working price | $675-$1,750 |
| Certified e-waste recycler | 0.72 lb module at $10-15/lb + PM assay credit (0.02g Au at 65% recovery = $1.87 net) | $9-$13 |

**Realistic range: $675-$1,750** (selling the dead module whole to a specialized broker).

SXM4 modules are the primary targets of Shenzhen gray-market repair shops (500 repairs/month documented). Dead modules serve as donors for CoWoS package transplants, Vicor module harvesting, and connector reuse. This demand supports broker bids well above raw scrap value. However, SXM4 modules must be sold with the HGX baseboard context in mind -- standalone modules are harder to liquidate than PCIe cards. Minimum lot sizes of 4-8 modules (one baseboard set) may apply. E-waste recycling ($9-$13) yields almost nothing due to the module's low weight (~325g) and minimal gold content (no PCIe edge fingers on SXM form factor).
