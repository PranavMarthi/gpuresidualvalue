# NVIDIA A100X Converged Accelerator -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** PCIe (Dual-slot FHFL, Gen4 x16 physical / x8 electrical)
**TDP:** 300W (per NVIDIA converged accelerator datasheet; 350W is the AX800, not the A100X)
**MSRP:** ~$33,700 (enterprise) | **Used (Mar 2026):** $8,000-$15,000 (revised upward; see deep_investigation.md Q5)

---

## 1. Card Overview

The NVIDIA A100X is a converged accelerator combining the A100 Tensor Core GPU (GA100, Ampere) with the BlueField-2 DPU on a single PCB. An on-board PCIe Gen4 switch enables direct GPU-to-DPU communication. Dual 100GbE/InfiniBand QSFP56 ports are provided via the ConnectX-6 Dx integrated into the BlueField-2 SoC. Designed primarily for 5G vRAN and edge AI workloads, it is a low-volume, telecom-oriented product with thin secondary market liquidity.

| Attribute | Value |
|-----------|-------|
| GPU die | GA100 (TSMC N7) |
| Die area | 826 mm2 |
| Transistors | 54.2 billion |
| Memory | 80 GB HBM2e (5 x 16 GB, 8-Hi stacks) + 16 GB DDR4 (DPU) |
| Memory bus | 5120-bit (GPU) + 64-bit ECC (DPU) |
| Interconnect | NVLink bridge (3 pads, corrected from 1) + PCIe Gen4 x8 |
| TDP | 300 W (per NVIDIA datasheet) |
| Board weight | ~1,250 g estimated (see correction note below) |
| Packaging | CoWoS-S flip-chip BGA (GPU) + standard BGA (BlueField-2) |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (passive, copper base + aluminum fins) | 500 | 40.0% |
| PCB (14-layer FR-4) | 320 | 25.6% |
| VRM (MOSFETs + inductors + capacitors) | 140 | 11.2% |
| GPU die + package substrate (GA100 CoWoS BGA) | 28 | 2.2% |
| HBM2e stacks (5x) | ~0.5 | <0.1% |
| BlueField-2 DPU SoC | 12 | 1.0% |
| DDR4 SDRAM (8 chips; ECC integrated in 8-chip layout) | 12.0 | 1.0% |
| Connectors (QSFP56 x2, PCIe, NVLink x3, EPS-12V 8-pin) | 74 | 5.9% |
| Bracket + mounting hardware | 25 | 2.0% |
| Other (TIM, PCIe switch IC, clock ICs, passives, solder, eMMC) | ~138.5 | 11.1% |
| **Total** | **~1,250** | **100%** |

Note: The original summary estimated total card weight at ~1,135g. The standard A100 PCIe 80GB board-only weight is 1,170g (per NVIDIA product brief PB-10577-001_v02; the often-cited 1,240g is the 40GB variant). Since the A100X adds a DPU, DDR4, PCIe switch, and QSFP56 cages on top of the base A100 80GB, it should weigh somewhat more than 1,170g. The heatsink has been adjusted to 500g (from 480g) to account for dual-chip cooling, and the total is revised to ~1,250g.

---

## 3. Component Breakdown

### GPU Die
- GA100, 826 mm2, 54.2B transistors, TSMC N7
- Uses flip-chip copper pillar bumps (not gold wire bonds) on CoWoS-S interposer
- Secondary market: $0 (bare die extraction from CoWoS package is impractical)
- Raw scrap: $4.50 (gold in BGA pad plating, silicon scrap)

### Memory
- GPU: 5 x 16 GB HBM2e 8-Hi stacks (Samsung Flashbolt or SK Hynix), 80 GB total on CoWoS-S interposer
- DPU: 16 GB DDR4-3200 SDRAM, 64-bit + 8-bit ECC, soldered down (8 chips per NVIDIA BlueField-2 datasheet)
- Secondary market: $0 (all BGA-soldered, no practical extraction)
- Raw scrap: $2.20 (HBM micro-bump metals + DDR4 gold plating)

### Heatsink
- Passive copper base plate + aluminum fin array, bidirectional airflow
- Must cool both GA100 GPU and BlueField-2 DPU (~300W combined TDP)
- ~500g estimated (170g copper, 330g aluminum)
- Secondary market: $0 (no standard reuse)
- Raw scrap: $2.30 (Cu 170g at $5/lb scrap = $1.87; Al 330g at $1.30/kg = $0.43)

### VRM / Power Delivery
- ~16 phases DrMOS for GPU subsystem
- 16x MOSFETs (~40g), 16x inductors/chokes (~64g), ~120 MLCC + polymer capacitors (~36g)
- Secondary market: $0 (commodity components, not worth harvesting)
- Raw scrap: $1.45 (copper windings in inductors + trace metals in MLCCs)

### PCB
- 14-layer server-grade FR-4, ~320g
- Cu content ~96g (30% copper by weight, typical for dense multi-layer)
- ENEPIG gold finish ~0.010g Au (revised from 0.10g per first-principles calibration; see gold_content_analysis.md Section 2.2)
- Classified as Class 1-C (modern GPU/accelerator board) by European e-scrap refiners
- Secondary market: $0 (no standard reuse due to niche converged design)
- Raw scrap: $18.50 (bulk board rate; copper traces + ENEPIG gold)

### Connectors
- 2x QSFP56 cages (dual 100GbE ports, gold-plated contacts, ~0.001g Au each; revised from 0.02g per first-principles: 38 pins x 0.45mm^2 x 0.762um Au = ~0.25 mg per port)
- 1x PCIe edge connector (x16 physical, gold fingers ~0.011g Au; revised from 0.12g per IPC-4556: 164 pads x 2.74mm^2 x 0.762um x 19.32 g/cm^3 = ~6.6-11 mg)
- 3x NVLink bridge connector pads (corrected from 1; standard A100 PCIe has 3 pads for full 600 GB/s, ~0.005g Au each; revised from 0.03g per first-principles pad geometry)
- 1x EPS-12V 8-pin power connector (corrected from "standard PCIe 8-pin"; EPS can deliver ~300W vs. ~150W for PCIe 8-pin)
- Secondary market: $0
- Raw scrap: $3.30

### BlueField-2 DPU
- 7B transistor SoC: 8x Arm Cortex-A72 + ConnectX-6 Dx (on-die), BGA package
- ~0.002g Au in ENEPIG pad plating (revised from 0.15g; BGA ENIG pads contain ~0.05-0.10 um Au over nickel -- no wire bonds, BlueField-2 uses flip-chip BGA)
- Standalone BF2 DPUs sell used at $90-$260 on eBay (full card); as a soldered component on the A100X main PCB, extraction requires hot-air rework and risks destruction
- Secondary market: $90 (low-end, if successfully desoldered and tested)
- Raw scrap: $1.20

### Other
- TIM: 2x indium-based thermal interface (GPU die + DPU die), ~6g total ($3.30 at corrected ~$550/kg)
- 1x PCIe Gen4 switch IC (~5g, enables GPU-DPU direct link)
- 3x voltage regulator / PWM controller ICs (~4.5g)
- 4x crystal oscillators / clock generators (~2g)
- ~200 discrete SMD passives (resistors, diodes, ESD protection, ~20g)
- 8x tantalum capacitors (~6.4g, tantalum scrap ~$33-110/kg)
- eMMC flash storage for BlueField-2 (64 GB, per P-Series SKU MBF2H516B; the "16GB" in the datasheet is DDR4 capacity, not eMMC)
- Raw scrap: ~$1.00

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.04-0.06 | $144/g | $5.76-$8.64 | First-principles build-up (see gold_content_analysis.md): PCIe x16 fingers (~0.011g), NVLink 3 bridge pads (~0.015g), GA100 BGA ENIG pads (~0.003g), BlueField-2 BGA pads (~0.002g), QSFP56 2x connector plating (~0.002g), PCB ENIG surface finish (~0.010g). Total ~0.043g, range 0.04-0.06g. Previous 1.0-1.3g estimate was ~15-25x too high due to confusing plating thickness with component mass, assuming gold wire bonds on flip-chip packages, and conflating connector weight with gold content. |
| Silver (Ag) | 0.30 | $2.35/g | $0.71 | Trace in solder (SAC305 3% Ag) and substrate layers |
| Palladium (Pd) | 0.005 | $45/g | $0.23 | Trace from connector plating (gold-over-palladium, ~15 microinch) and tantalum cap terminations. Modern BME MLCCs use 100% nickel electrodes -- zero Pd. Corrected from 0.08g. |
| **Total** | | | **$6.70-$9.58** | |

Note: Gold revised from 1.0-1.3g down to 0.04-0.06g following first-principles calibration (gold_content_analysis.md). Every sub-component was recalculated from IPC plating specs and physical geometry: PCIe x16 fingers contain ~6-11 mg (not 120 mg), BGA ENIG pads contain ~2-3 mg (not 300-400 mg), HBM micro-bumps contain ~0.01 mg (not 150-250 mg -- a 10,000x overestimate), QSFP56 cages contain ~0.5 mg (not 40 mg). The GA100 uses copper pillar flip-chip, not gold wire bonds. This reduces gross precious metal value from $148-$191 to $10-$13 -- a ~$140-$180 reduction.

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $8,000-$15,000 | 24-45% |
| Component salvage (theoretical max) | $90-$260 | 0.3-0.8% |
| Component salvage (realistic) | $50-$100 | 0.1-0.3% |
| Raw material scrap (gross) | $16-$19 | <0.1% |
| Recycler payout (net, what you'd receive) | $6-$11 | <0.1% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **TDP [VERIFIED AT 300W]:** Originally 300W, then incorrectly "corrected" to 350W. The NVIDIA converged accelerator datasheet (which lists A100X, A30X, and AX800 side by side) gives A100X max power as 300W. The 350W figure belongs to the AX800 (BlueField-3 based). The A100 PCIe 80GB GPU alone is also 300W; the A100X's 300W total board power implies the BlueField-2 DPU subsystem runs within the same thermal envelope, consistent with ServeTheHome's note that the DPU draws 60-75W from a shared PCIe power budget of 300W. Reverted to 300W.
- **NVLink connector count [UNCERTAIN -> CORRECTED]:** Originally listed as 1 pad. Standard A100 PCIe cards have 3 NVLink bridge connector pads (required for full 600 GB/s). Corrected to 3.
- **DDR4 chip count [VERIFIED AT 8]:** Originally 8x 2GB, then incorrectly "corrected" to 9. The NVIDIA BlueField-2 datasheet explicitly states "8 units of SDRAM" for a 16GB single-channel DDR4 configuration with 64-bit + 8-bit ECC. The ECC bits are handled within the 8-chip layout (likely using x8 or x16 chips with internal ECC columns). Reverted to 8.
- **Power connector type [MISLEADING -> CORRECTED]:** Originally described as "standard 8-pin PCIe power." NVIDIA Ampere datacenter cards use EPS-12V 8-pin (up to ~300W), not standard PCIe 8-pin (~150W). Corrected.
- **Missing BlueField-2 eMMC flash [OMISSION -> RESOLVED]:** BlueField-2 includes eMMC flash for on-board OS/firmware. Not listed in original BOM. Added. Deep investigation (2026-03-29) narrowed capacity to **64 GB** based on P-Series SKU match (MBF2H516B-EENOT). The "16GB" in the datasheet refers to DDR4, not eMMC.
- **Card weight [UNDERESTIMATE, REVISED]:** Originally 1,135g. The standard A100 PCIe 80GB board-only weight is 1,170g (per PB-10577-001_v02); the 1,240g figure cited earlier is for the 40GB variant. The A100X with additional DPU, DDR4, PCIe switch, and QSFP56 cages should weigh somewhat more than 1,170g. Revised to ~1,250g.
- **Gold content [MASSIVE OVERESTIMATE -> CORRECTED]:** Originally 1.5g, then revised to 1.0-1.3g, now corrected to **0.04-0.06g** via first-principles calibration (gold_content_analysis.md). Every sub-component was recalculated from IPC plating standards and physical pad geometry. The 1.0-1.3g estimate was ~15-25x too high due to: confusing plating thickness with component mass (BGA pads: 0.30-0.40g claimed vs. ~0.003g actual), assuming gold where there is none (HBM micro-bumps: 0.15-0.25g claimed vs. ~0.00001g actual), and conflating connector weight with gold content (QSFP56: 0.04g claimed vs. ~0.001g actual).

### Pricing Issues
- **Indium price [WRONG]:** Summary listed $0.50/g. Current benchmarks are ~$0.55/g (Western) to $0.62/g (SMM China). Impact: +$0.03 on indium scrap -- immaterial.
- **Copper scrap price [INTERNAL INCONSISTENCY]:** Base metals table used $12.00/kg, but material prices table listed bare bright at $4.96/lb ($10.93/kg). Dollar impact ~$0.33, immaterial.
- **Tantalum price [INTERNAL INCONSISTENCY]:** Base metals calculation used $200/kg (pure metal reference), but material prices table listed $33-110/kg for capacitor scrap. Dollar impact ~$0.04, immaterial.

### Deep Investigation (2026-03-29)
Five key unknowns investigated: card weight, gold content, eMMC capacity, TDP sharing, secondary market. See `deep_investigation.md` for full analysis. Definitive answers found for eMMC (64 GB) and TDP sharing (confirmed within 300W envelope). Secondary market range revised upward to $8,000-$15,000. Card weight and gold content remain unresolvable without physical access.

### Confidence Assessment (updated 2026-03-29)
- Component accuracy: 62/100 (up from 60; eMMC resolved, TDP confirmed, QSFP gold refined)
- Pricing accuracy: 65/100 (down from 70; secondary market data is thinner than initially assumed)
- Overall confidence in scrap estimate: 62/100 (up from 60)

---

## 7. Key Observations

1. **Gold is the dominant precious metal by a wide margin.** After first-principles calibration and BME MLCC correction, gold at 0.04-0.06g contributes $5.76-$8.64 gross (~86-90% of PM total). Palladium, previously thought to be a meaningful contributor at $3.61 (0.08g from MLCC electrodes), was reduced to $0.23 (0.005g) after the MI210 investigation confirmed modern BME MLCCs contain zero Pd. The total raw scrap value of $13-$16 is split roughly 50/50 between precious metals ($6.70-$9.58) and base metals (~$6). At recycler payout of $5-$9, the A100X has negligible scrap value relative to its $33,700 MSRP.

2. **The converged design adds components but not scrap value.** The BlueField-2 DPU, DDR4, PCIe switch, and QSFP56 cages add ~100g and several line items to the BOM, but contribute less than $1 in additional precious metal value (mostly from extra BGA pads and QSFP56 connector plating). The DPU's $90+ secondary market value is the only meaningful uplift -- and only if it can be successfully desoldered, which is impractical for most actors.

3. **Niche product with thin secondary market.** The A100X was sold almost exclusively through Supermicro GPU server assemblies for telecom/5G workloads. Secondary market listings are sparse. The converged GPU+DPU form factor limits the buyer pool. It trades at a discount to the standard A100 PCIe despite higher MSRP.

---

## 8. Methodology & Sources

### GPU Specifications
- [NVIDIA Converged Accelerator Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcf21/converged-accelerator/pdf/datasheet.pdf) -- A100X specs, 300W max power, converged GPU+DPU architecture
- [NVIDIA BlueField-2 DPU Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/documents/datasheet-nvidia-bluefield-2-dpu.pdf) -- DPU subsystem details, ConnectX-6 Dx, DDR4 configuration
- [Q9 Technology product page](https://q9.group/product/nvidia-a100x-converged-accelerator/) -- product reference and availability
- [Exxact listing (900-21004-0030-000)](https://www.exxactcorp.com/NVIDIA-900-21004-0030-000-E5520399) -- pricing and configuration reference
- Board weight: NVIDIA A100 PCIe 80GB product brief (PB-10577-001_v02, 1,170g board-only; the 1,240g figure is the 40GB variant); A100X estimated at ~1,250g accounting for additional DPU subsystem
- Precious metal quantities: Estimated from BGA pad count, connector pin count, PCB ENEPIG coverage, and e-waste industry benchmarks. GA100 gold reduced from original after confirming copper pillar flip-chip packaging.
- Recovery rates: 30-50% refining cost deducted from gross metal value (industry standard for professional bulk recycling via Umicore, Boliden, etc.)

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report
- **PCB scrap rates:** [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)
- Tin $46.89/kg (SMM), Indium ~$0.55/g (corrected, Western benchmark)

### Secondary Market
- eBay sold/active listings (Mar 2026)
- Interpro Microsystems ($33,717 new)
- Project tier3 transaction data

---

## 9. Web Verification (2026-03-29)

Independent verification of six claims via web search against NVIDIA datasheets, product briefs, and ServeTheHome analysis.

### Q1: GA100 GPU + BlueField-2 DPU on the same PCB?
**Confirmed.** Multiple sources (NVIDIA datasheet, PNY, Exxact, ServeTheHome, NVIDIA deployment docs) confirm the A100X places the GA100 GPU and the BlueField-2 DPU on a single PCB. ServeTheHome photographed the board and identified both chips and the top-edge NVLink connectors. No public teardown exists showing individual component markings at close range, but the architecture is not in dispute.

### Q2: Actual TDP -- 300W vs 350W?
**300W is correct. The report's earlier "correction" to 350W was wrong.** The NVIDIA converged accelerator datasheet lists three products side by side: AX800 at 350W, A100X at 300W, A30X at 230W. The 350W figure belongs to the AX800 (BlueField-3 + A100 GPU, PCIe Gen5, 2x 200Gb/s). The A100X is BlueField-2 based and rated at 300W. ServeTheHome's analysis is consistent: the BlueField-2 DPU draws 60-75W "from a PCIe power budget of... 300W with the new NVIDIA A100 80GB PCIe," implying the GPU and DPU share a 300W envelope rather than exceeding it. Reverted to 300W.

### Q3: NVLink pads -- 1 vs 3?
**3 pads is correct.** ServeTheHome explicitly states: "NVIDIA has three sets of top connectors on standard A100 PCIe cards that are used for NVLink bridges." The A100 PCIe 80GB product brief confirms three bridges are required for full 600 GB/s. The original "1 pad" was wrong; the correction to 3 was valid.

### Q4: DDR4 chip count and eMMC flash?
**8 chips, not 9. eMMC is present.** The NVIDIA BlueField-2 datasheet states "8 units of SDRAM for a total of 16GB @ 3200MT/s single DDR4 channel, 64bit + 8bit ECC, solder-down memory." The earlier "correction" to 9 chips (assuming a separate ECC chip) was wrong; the 8-chip configuration handles ECC internally (likely using x8 or x16 dies with wider internal organization). The eMMC flash is confirmed present: the "x8" in "16GB x8 NAND flash" refers to the eMMC bus width, not capacity -- the 16GB is the DDR4 size. The P-Series SKU matching the A100X (MBF2H516B-EENOT) ships with **64GB eMMC**. Other BlueField-2 SKUs offer 128GB eMMC (effective 40GB in high-durability mode). The BlueField-2 also includes a 256Mbit Quad SPI NOR flash for firmware and EEPROM storage.

### Q5: PCIe switch connecting GPU and DPU?
**Confirmed.** The NVIDIA converged accelerator datasheet, multiple vendor pages, and ServeTheHome all confirm an integrated PCIe Gen4 switch on the A100X that provides a direct GPU-to-DPU data path without traversing the host PCIe bus. This is described as a core architectural feature, not optional.

### Q6: Card weight -- heavier than a standard A100 PCIe?
**Yes, but the reference weight was wrong.** The NVIDIA A100 PCIe 80GB product brief (PB-10577-001_v02) lists board-only weight as **1,170g** (excluding bracket, extenders, and bridges). The report previously cited 1,240g, which is the A100 PCIe **40GB** variant. The A100X should weigh more than 1,170g due to the added DPU, DDR4, PCIe switch, and QSFP56 cages. Revised estimate: ~1,250g (up from 1,135g original, down from the incorrect 1,300g).

### Verification Sources
- [NVIDIA Converged Accelerator Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcf21/converged-accelerator/pdf/datasheet.pdf) -- A100X/A30X/AX800 specs table with 300W/230W/350W max power
- [NVIDIA BlueField-2 DPU Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/documents/datasheet-nvidia-bluefield-2-dpu.pdf) -- DDR4 8-chip config, eMMC, SPI NOR
- [NVIDIA A100 80GB PCIe Product Brief (PB-10577-001_v02)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/PB-10577-001_v02.pdf) -- 1,170g board-only weight, 3x NVLink bridges
- [ServeTheHome: CPU-GPU-NIC PCIe Card Realized with NVIDIA BlueField-2 A100](https://www.servethehome.com/cpu-gpu-nic-pcie-card-realized-with-nvidia-bluefield-2-a100/) -- PCB photos, NVLink 3-pad confirmation, DPU 60-75W power draw
- [ServeTheHome: NVIDIA AX800 A100X A30X Specs](https://www.servethehome.com/nvidia-ax800-high-end-arm-server-on-a-pcie-card-ampere-ai-dpu/nvidia-ax800-a100x-a30x-specs/) -- side-by-side spec comparison
- [Exxact A100X listing](https://www.exxactcorp.com/NVIDIA-900-21004-0030-000-E5520399) -- product reference
- [Q9 Technology A100X page](https://q9.group/product/nvidia-a100x-converged-accelerator/) -- confirms 2x 100Gb/s networking, PCIe Gen4

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Absolute ceiling assuming perfect component recovery, 100% precious metal extraction, and a buyer for every part. The A100X is a converged GPU+DPU card with CoWoS packaging on the GPU side.

| Component | Basis | Value |
|-----------|-------|-------|
| GPU die (GA100) | $0 -- permanently bonded to CoWoS interposer | $0 |
| HBM2e stacks (5x 16GB) | $0 -- bonded via microbumps + underfill; no market (per hbm_secondary_market.md) | $0 |
| BlueField-2 DPU | Desoldered and tested, low-end eBay pricing | $90 |
| DDR4 SDRAM (8x 2GB) | BGA-soldered; $0 unless desoldered, then $2-3/chip | $16 |
| Heatsink (170g Cu + 330g Al) | Cu at $5.90/lb + Al scrap | $2.30 |
| VRM components (16x DrMOS, 16x inductors) | Harvested DrMOS at $1/ea, inductors at $0.30/ea | $21 |
| PCB (320g, 14-layer) | Server-grade e-scrap at $12/lb | $8.45 |
| Precious metals (0.05g Au, 0.30g Ag) | 100% extraction at spot ($144/g Au, $2.25/g Ag) | $7.88 |
| QSFP56 cages (2x) | Replacement connectors | $5 |
| PCIe switch IC | Niche component market | $10 |
| **Total theoretical max** | | **~$161** |

The BlueField-2 DPU ($90) is the single most valuable recoverable component, but successful desoldering requires professional BGA rework and risks destroying the chip. Without it, the card is worth ~$71 in parts -- essentially VRM copper, PCB scrap, and precious metals.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator would actually receive for a dead A100X.

| Channel | Basis | Payout |
|---------|-------|--------|
| ITAD/broker (whole dead card) | 10-20% of $8,000-$15,000 used working price; discount for niche converged form factor | $800-$2,250 |
| Certified e-waste recycler | 2.76 lb board at $10-15/lb + PM assay credit (0.05g Au at 65% recovery = $4.70 net) | $32-$46 |

**Realistic range: $800-$2,250** (selling the dead card whole to a broker).

The A100X is a niche telecom/5G product with a thin secondary market. Broker bids will trend toward the lower end of the 10-20% range due to limited buyer demand -- most repair shops want standard A100 PCIe or SXM4, not the converged GPU+DPU variant. The BlueField-2 DPU adds some value as a donor component, but only to buyers with the equipment and expertise to harvest it. E-waste recycling ($32-$46) benefits from the heavier board (1,250g vs. 550g for the A10) but remains a last resort. Component harvesting in the US is not viable at any scale for this card.
