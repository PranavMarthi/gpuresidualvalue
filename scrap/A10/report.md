# NVIDIA A10 -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe
**TDP:** 150W
**MSRP:** $2,500 (launch) | **Used (Mar 2026):** $1,400-$1,800

---

## 1. Card Overview

The NVIDIA A10 is an Ampere-generation datacenter inference and virtual workstation GPU built on the GA102 die. It uses a single-slot passive heatsink, draws 150W, and is designed for PCIe Gen4 x16 server deployments.

| Attribute | Value |
|-----------|-------|
| GPU die | GA102-890 (Samsung 8nm / 8N custom) |
| Die area | 628.4 mm2 |
| Transistors | 28.3 billion |
| Memory | 24 GB GDDR6 (12 x 2 GB) |
| Memory bus | 384-bit |
| Interconnect | PCIe Gen4 x16 (no NVLink) |
| TDP | 150 W |
| Board weight | 550 g (NVIDIA product brief, excl. bracket) |
| Packaging | Standard flip-chip BGA on organic substrate |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (passive Al fin array) | 250 | 45.5% |
| Heatsink (Cu base plate / vapor chamber) | 60 | 10.9% |
| PCB | 95 | 17.3% |
| VRM (inductors + MOSFETs + caps) | 57 | 10.4% |
| GPU die + package substrate | 15 | 2.7% |
| Memory (12 x GDDR6 chips) | 14.4 | 2.6% |
| Connectors + bracket | 20 | 3.6% |
| Other (solder, TIM, passives, backplate, misc) | 38.6 | 7.0% |
| **Total** | **550** | **100%** |

*Note: Heatsink aluminum reduced from original 280g estimate to 250g to reconcile with NVIDIA's 550g board weight specification. The original analysis overestimated by ~31g (+5.6%).*

---

## 3. Component Breakdown

### GPU Die
- GA102-890, 628.4 mm2, 28.3B transistors, Samsung 8nm (8N custom)
- Secondary market: $25 (reballing/rework for repair)
- Raw scrap: $0.08

### Memory
- 12 x 2 GB GDDR6 16Gbit (Samsung K4ZAF325BM or Micron MT61K512M32KPA)
- 384-bit bus, 12.5 Gbps, 600 GB/s peak bandwidth
- Secondary market: $96 total ($8/chip -- elevated by 2025-2026 DRAM shortage; normalized ~$3-5/chip)
- Raw scrap: $0.24 (trace gold on BGA pads)

### Heatsink
- Passive single-slot: extruded aluminum fins (~250g) + flat copper base plate (~60g, no vapor chamber)
- Vapor chamber ruled out: 150W in single-slot form factor does not justify vapor chamber cost. Server airflow through single-slot fins with flat copper base plate is thermally adequate for 0.24 W/mm2 heat flux from GA102 die. No teardown confirms VC; eBay photos show simple extruded aluminum. Confidence: 65%. See heatsink_materials_analysis.md.
- 310g total (~56% of card)
- Secondary market: $8
- Raw scrap: $0.79 (Cu at ~$4.50/lb for 60g = $0.60; Al at $0.35/lb for 250g = $0.19)

### VRM / Power Delivery
- Estimated 8-10 phase, DrMOS integrated power stages
- 10x inductors (ferrite + Cu winding), 10x MOSFETs, ~40x bulk capacitors, 1x PWM controller IC
- Secondary market: $27 (MOSFETs $15, inductors $5, caps $4, PWM controller $3)
- Raw scrap: $0.91 (copper in inductors, trace metals in caps)

### PCB
- Estimated 10-12 layer FR-4, 267mm (10.5") FHFL
- Cu content ~20g
- Secondary market: $3 (donor board for reballing)
- Raw scrap: $1.08 (mid-grade PCB e-scrap at ~$7/lb)

### Connectors
- PCIe x16 Gen4 gold fingers (~30-50mg Au), 8-pin EPS-12V power connector, stainless steel bracket (12g)
- No display outputs (no DisplayPort, no HDMI -- headless datacenter GPU; display only via NVIDIA vGPU software)
- No NVLink connector
- Secondary market: $1.00
- Raw scrap: $0.47 (mostly gold on PCIe fingers)

### Other
- TIM (thermal paste + pads, ~2g), backplate/stiffener (~20g), ~200 resistors/passives (~4g), EEPROM/flash (1x), ~5x LDO regulators, ~8g SAC305 solder, ~300x decoupling MLCCs near GPU die
- Raw scrap: $0.52

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.040-0.060 | $144/g | $5.76-$8.64 | PCIe fingers (~35mg), GPU substrate pads (~10mg), IC leads (~5-10mg) |
| Silver (Ag) | 0.240 | $2.25/g | $0.54 | In SAC305 solder (3% Ag of ~8g solder) |
| Palladium (Pd) | 0.005 | $45/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.020-0.040g. |
| **Total** | | | **$6.53-$9.41** | |

*Note: Gold price corrected from $100/g used in original analysis to ~$144/g (March 2026 spot). Palladium quantity further corrected downward from 20-40mg to 5mg -- MI210 deep investigation confirmed modern BME MLCCs (standard since ~2000 for Class II capacitors) contain zero palladium; the only legitimate Pd sources are selective gold-over-palladium connector plating and trace amounts in tantalum capacitor terminations.*

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $1,400-$1,800 | 56-72% |
| Component salvage (theoretical max) | $162 | 6.5% |
| Component salvage (realistic) | $80-$120 | 3.2-4.8% |
| Raw material scrap (gross) | $10-$12 | 0.4-0.5% |
| Recycler payout (net, what you'd receive) | $4-$7 | 0.2-0.3% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **VRAM part number (WRONG):** Original cited K4Z80325BC, which is an 8Gbit (1GB) chip. Corrected to K4ZAF325BM (16Gbit / 2GB). The VRAM capacity and count were always correct; only the part number was wrong.
- **Power connector (CORRECTED BACK TO EPS):** A prior review incorrectly changed "8-pin EPS" to "8-pin PCIe." The original was correct. NVIDIA's Ampere datacenter GPUs (A10, RTX A6000) transitioned to EPS-12V 8-pin connectors, which provide additional 12V rails vs. PCIe 8-pin. Confirmed by PNY Pro Tip #23, Supermicro CBL-PWEX-0665 adapter cable documentation, and multiple third-party sources. NVIDIA's own product brief uses the term "PEX 8-pin" which caused the confusion, but the physical connector on the board is EPS-12V.
- **GPU die package weight (UNCERTAIN):** 15g estimate for die + substrate + solder balls is reasonable but unverified. Typical large GPU BGA packages range 10-20g.
- **Heatsink weight (UNCERTAIN):** Original 280g aluminum estimate caused a 31g overestimate vs. NVIDIA's 550g spec. Adjusted to 250g to reconcile.
- **Missing minor components:** Clock generator/PLL, temperature sensor(s), I2C/SMBus interface ICs, InfoROM chip, fuses, ESD protection diodes. None material to the valuation.

### Pricing Issues
- **Gold price (WRONG):** Original used ~$100/g in component calculations; actual March 2026 spot is ~$144/g (+42%). Corrected. Gross gold value revised upward from $4.00-$6.00 to $5.76-$8.64.
- **Palladium quantity in MLCCs (WRONG, corrected twice):** Original estimated 100-120mg total Pd. First correction to 20-40mg based on BME electrode transition. Second correction to 5mg: MI210 deep investigation confirmed modern BME MLCCs (standard since ~2000 for Class II capacitors) contain zero palladium. Only legitimate Pd sources are selective gold-over-palladium connector plating (~15 microinch) and trace tantalum cap terminations. Gross Pd value revised from $4.50-$5.40 to $0.23.
- **Copper scrap price (UNCERTAIN):** $4.25/lb is at the low end; $4.50-$5.00/lb more typical for clean copper scrap in March 2026.
- **Aluminum LME price (LOW):** Cited $3.07/kg vs. actual $3.28/kg (7% undercount). Impact minor (~$0.02 on total).
- **Used market price (LOW):** Original $1,200 low end appears outdated for March 2026. Revised to $1,400-$1,800 based on GPUPoet and eBay tracking.
- **Solder recovery math (LOW):** $0.37 net implies 41% recovery from $0.91 gross, slightly below the stated 40-60% midpoint.
- **Decoupling cap Pd recovery rate (LOW):** Implied 3.7% recovery is inconsistent with stated 40-60% general rate, though this reflects the impracticality of recovering Pd from tiny 0201/0402 caps.

### Confidence Assessment
- Component accuracy: 78/100
- Pricing accuracy: 68/100
- Overall confidence in scrap estimate: 70/100

---

## 7. Key Observations

1. **VRAM dominates component salvage value.** The 12 GDDR6 chips account for $96 of $162 (59%) of secondary market parts value. This is inflated by the 2025-2026 DRAM shortage; in a normalized market, VRAM value drops to $36-$60.
2. **Working card value dwarfs scrap by 130-170x.** A functional A10 at $1,400-$1,800 is worth roughly 130-170x its $10-$12 raw material scrap value. The rational economic action for any working card is resale, never recycling.
3. **Gold and palladium pricing errors in the original analysis roughly offset.** Gold was understated (~$100/g vs. $144/g) while palladium quantity was overstated (100-120mg vs. 5mg in modern BME caps). Raw scrap (gross) corrected to $10-$12 to reflect PM total ($6.53-$9.41) plus base metals (~$3).

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA A10 Product Brief (PB-10415-001_v04)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a10/pdf/A10-Product-Brief.pdf) — 550g board weight, 150W TDP, single-slot FHFL, PCIe Gen4 x16
- [NVIDIA A10 Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a10/pdf/a10-datasheet.pdf) — 24GB GDDR6, 384-bit bus, 600 GB/s
- [NVIDIA GA102 GPU — VideoCardz.net](https://videocardz.net/gpu/nvidia-ga102) — GA102 die: 628.4 mm2, 28.3B transistors, Samsung 8nm
- [NVIDIA A10 — VideoCardz.net](https://videocardz.net/nvidia-a10) — GA102-890 SKU, 9,216 CUDA cores, 150W

### Precious Metal Spot Prices (March 29, 2026)
- [Gold $4,509/oz ($144.96/g) — JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Bullion.com](https://www.bullion.com/spotprices/gold-price-gram) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- [Palladium $1,405/oz ($45.16/g) — APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)
- [Silver ~$70/oz ($2.25/g) — Gold.org](https://www.gold.org/goldhub/data/gold-prices)

### Scrap Metal Prices (March 2026)
- [Bare Bright Copper — iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) — ~$5.90/lb (March 25, 2026)
- [Bare Bright Copper Wire — Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/) — daily pricing
- [Weekly Scrap Metal Report — ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) — Cu +2.10% week of March 20-26

### GDDR6 Memory Pricing
- [GDDR6 spot prices — Tom's Hardware](https://www.tomshardware.com/news/gddr6-vram-prices-plummet) — 8Gb chips ~$3.94 (Dec 2025); 16Gbit ~$7-8 estimated
- [DRAM Price Trends — TrendForce](https://www.trendforce.com/price/dram/dram_spot) — contract/spot pricing database
- [GPU prices rising on GDDR costs — igor'sLAB](https://www.igorslab.de/en/gpu-prices-could-rise-at-the-beginning-of-2026-because-the-cost-of-gddr-memory-will-increase-significantly/) — 33-43% increase across densities

### Secondary Market
- [NVIDIA A10 eBay listings](https://www.ebay.com/sch/i.html?_nkw=nvidia+a10&_sop=12) — $1,390-$2,494 used/open-box (March 2026)
- [NVIDIA A10 — GPU Poet](https://gpupoet.com/gpu/learn/card/nvidia-a10) — pricing and benchmarks
- [Lenovo ThinkSystem A10 — Lenovo Press](https://lenovopress.lenovo.com/lp1816-thinksystem-nvidia-a10-24gb-pcie-gen4-passive-gpu) — OEM specs

### Precious Metal Quantities
- Geometric calculation for PCIe gold fingers per IPC-4556 plating standard (30-50 microinches hard gold over 100-200 microinches nickel)
- SAC305 solder composition: 96.5% Sn, 3.0% Ag, 0.5% Cu (industry standard Pb-free)
- MLCC palladium adjusted for modern BME (nickel electrode) shift — post-2020 datacenter GPUs use predominantly BME capacitors

### Recovery Rates
- 40-60% of gross precious metal value assumed for professional batch refining (BoardSort, ESG Edelmetall-Service published rates)
- Single-card processing yields $1-$3 recycler payout due to handling minimums

---

## 9. Component Verification (Deep Research)

Independent verification conducted 2026-03-29 via web searches of NVIDIA official documentation, OEM integration guides (Lenovo, Supermicro, Exxact), third-party spec databases (technical.city, VideoCardz, ServeTheHome), and secondary market listings.

### Errors Found and Corrected

1. **Display outputs (WRONG -- now fixed):** The report previously listed "4x DisplayPort 1.4 (virtual workstation capability)." This is incorrect. The NVIDIA A10 has **no physical display outputs** of any kind -- no DisplayPort, no HDMI, no DVI. It is a headless datacenter/compute GPU. Display capability is provided exclusively through NVIDIA vGPU software (RTX vWS, vPC). This distinguishes it from the RTX A4000 and RTX A5000, which do have 4x DisplayPort. The bracket is blank. Sources: ServeTheHome A10/A16 launch coverage; NVIDIA A10 Product Brief PB-10415-001_v04; Lenovo ThinkSystem A10 Product Guide.

2. **Power connector (WRONG correction reversed -- now fixed):** A prior review changed "8-pin EPS" to "8-pin PCIe," citing incompatible pinouts. This correction was itself wrong. The NVIDIA A10 uses an **EPS-12V 8-pin** connector, consistent with NVIDIA's Ampere-generation transition for datacenter and professional GPUs. PNY's Pro Tip #23 explicitly documents this change for the RTX A6000 (same generation), and Supermicro sells a dedicated CPU-8-pin-to-PCIe-8-pin adapter cable (CBL-PWEX-0665) specifically for the A10 and A5000. NVIDIA's own product brief uses the term "PEX 8-pin," which is ambiguous and contributed to the original misidentification. The physical connector on the A10 board accepts EPS-12V (all 8 pins carry 12V + ground, no sense pins, no 6+2 split).

### Confirmed Correct

3. **GDDR6 chip count and configuration:** 12x 2GB GDDR6 chips = 24GB total on a 384-bit bus (12x 32-bit channels) confirmed across all sources. Memory bandwidth 600 GB/s at 12.5 Gbps confirmed.

4. **GPU die:** GA102-890, Samsung 8nm (8N custom), 628.4 mm2, 28.3B transistors -- confirmed by VideoCardz and NVIDIA product brief.

5. **Form factor:** Single-slot, full-height full-length (FHFL), 267mm (10.5"), passive cooling, 150W TDP -- confirmed across all sources.

6. **Board weight:** 550g -- confirmed in NVIDIA Product Brief PB-10415-001_v04.

7. **Board design:** PG133 SKU 215 (NVPN 699-2G133-0215-C01), shared board lineage with RTX 3090/3080 Founders Edition but in a datacenter-specific configuration.

8. **No NVLink:** Confirmed. PCIe Gen4 x16 only.

### Remaining Uncertainties

9. **Heatsink construction (PARTIALLY RESOLVED):** No teardown of the A10 passive heatsink exists publicly. Determination: most likely extruded aluminum fins (~250g) + flat copper base plate (~60g) WITHOUT vapor chamber. Reasoning: 150W in single-slot form factor is below NVIDIA's vapor chamber threshold (250W+ for dual-slot cards). eBay product photos show simple extruded aluminum. The GA102 platform uses VCs on higher-TDP variants (A40 at 300W, RTX A6000 at 300W) but the A10 at 150W single-slot does not thermally require one. Confidence 65%. See heatsink_materials_analysis.md for full analysis.

10. **VRM phase count (UNVERIFIED):** The report estimates 8-10 phases. The GA102 PG133 reference board for consumer RTX 3090/3080 used "over 20 chokes," but the A10's 150W TDP (vs. 350W for RTX 3090) likely uses a reduced VRM configuration. 8-10 phases is a reasonable estimate for 150W but remains unconfirmed absent a teardown.

11. **GDDR6 vendor (UNVERIFIED):** Samsung K4ZAF325BM or Micron MT61K512M32KPA are plausible part numbers for 16Gbit GDDR6 chips, but the actual vendor likely varies by production batch. NVIDIA does not publish memory vendor details.

### Confidence Assessment (Updated)
- Component accuracy: 82/100 (up from 78 -- DisplayPort error fixed, EPS connector restored)
- Pricing accuracy: 68/100 (unchanged)
- Overall confidence in scrap estimate: 72/100 (up from 70)

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Absolute ceiling assuming perfect component recovery, 100% precious metal extraction, and a buyer for every part.

| Component | Basis | Value |
|-----------|-------|-------|
| GPU die (GA102-890) | Shenzhen rework shop, reballing candidate | $25 |
| GDDR6 chips (12x 2GB) | AliExpress individual sale at $8/chip (shortage pricing) | $96 |
| Heatsink (250g Al + 60g Cu) | Clean Cu scrap at $5.90/lb + Al scrap | $1.50 |
| VRM components (10x DrMOS, 10x inductors) | Harvested DrMOS at $1-2/ea, inductors at $0.50/ea | $27 |
| PCB (95g, 10-12 layer) | Server-grade e-scrap at $12/lb | $1.50 |
| Precious metals (0.05g Au, 0.24g Ag) | 100% extraction at spot ($144/g Au, $2.25/g Ag) | $7.74 |
| Connectors (PCIe x16 fingers, EPS 8-pin) | Replacement part value | $1.00 |
| **Total theoretical max** | | **~$160** |

This ceiling requires Shenzhen-grade BGA rework capability, individual chip testing, and willing buyers for every line item. The GDDR6 chips ($96) drive 60% of the total; without them, the card is worth ~$64 in parts.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator would actually receive for a dead A10.

| Channel | Basis | Payout |
|---------|-------|--------|
| ITAD/broker (whole dead card) | 10-20% of $1,400-$1,800 used working price | $140-$360 |
| Certified e-waste recycler | 1.21 lb board at $8-12/lb PCB scrap + PM assay credit (0.05g Au at 65% recovery = $4.70 net) | $14-$19 |

**Realistic range: $140-$360** (selling the dead card whole to an ITAD broker like ALTA Technologies or Net Equity).

The A10 is unusual among datacenter GPUs: its 12 individually-desoldered GDDR6 chips have real secondary market value ($3-5/chip harvested), which supports the broker bid. However, component harvesting at US labor rates is uneconomical -- only the whole-card sale channel is practical. E-waste recycling ($14-$19) should be treated as a floor, not a target. Minimum lot sizes typically apply (10+ cards), and shipping runs $5-$15 per card.
