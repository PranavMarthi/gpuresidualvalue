# NVIDIA A100X Deep Investigation -- Five Key Unknowns

**Date:** 2026-03-29
**Starting confidence:** 60/100

---

## 1. Card Weight (~1,250g estimate)

### Finding: UNCHANGED -- no official source found; estimate remains ~1,250g

**What we searched:**
- NVIDIA converged accelerator datasheet (PDF) -- lists form factor (FHFL dual-slot, PCIe Gen4 x16), TDP (300W), and passive cooling, but **does not list weight or physical dimensions** for the A100X, A30X, or AX800.
- NVIDIA A100 80GB PCIe product brief (PB-10577-001_v02/v03) -- confirms the base A100 PCIe 80GB board-only weight at **1,170g** (excludes bracket, extenders, NVLink bridges).
- NVIDIA A100 40GB PCIe product brief + Newegg listing -- confirms the A100 PCIe 40GB board weight at **1,240g** (per Newegg listing for PNY A100 40GB: "Board Weight: 1240 Grams").
- Wiredzone, Q9 Technology, PNY, Exxact, Interpro product pages for the A100X -- none list a weight.
- ServeTheHome PCB photos of the A100X -- no weight mentioned.
- BlueField-2 standalone DPU (MBF2H516B) specifications from NVIDIA Docs -- physical dimensions (167.65mm x 11.15mm PCB) are listed, but **weight is not listed** in publicly available docs. Weight may be in the restricted "Electrical and Thermal Specifications" document behind NVIDIA NVOnline login.

**Analysis:**
The 80GB A100 PCIe weighs 1,170g. The 40GB variant weighs 1,240g (different PCB/heatsink design). The A100X adds on top of the 80GB base:
- BlueField-2 DPU SoC (~12g)
- 8x DDR4 SDRAM (~12g)
- PCIe Gen4 switch IC (~5g)
- 2x QSFP56 cages (~36g)
- eMMC flash (~1g)
- Supporting passives, traces, power delivery for DPU subsystem (~15-25g)
- Potentially heavier heatsink to cover dual-chip thermal load

Estimated delta: +80-90g over base A100 80GB -> ~1,250-1,260g. The ~1,250g estimate in report.md is well-grounded but unverifiable without a physical unit on a scale.

**Confidence on weight:** 55/100 (reasonable engineering estimate, no authoritative source)

**Sources:**
- [NVIDIA A100 80GB PCIe Product Brief (PB-10577-001_v02)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/PB-10577-001_v02.pdf) -- 1,170g board-only
- [PNY NVIDIA A100 40GB on Newegg](https://www.newegg.com/p/1FT-0004-006M7) -- 1,240g board weight
- [NVIDIA Converged Accelerator Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcf21/converged-accelerator/pdf/datasheet.pdf) -- no weight listed
- [NVIDIA BlueField-2 DPU Specifications](https://docs.nvidia.com/networking/display/bluefield2dpuenug/specifications) -- PCB dimensions, no weight

---

## 2. Gold Content (1.0-1.3g estimate)

### Finding: PLAUSIBLE -- independent calculation supports the range; QSFP56 gold revised downward

**What we searched:**
- Gold refining forum assay results for BGA chips: mixed BGA lots yield ~11.4g Au/kg (5.2g from 456.9g of 286 mixed BGA chips). Intel BGAs yield ~7g/kg; generic BGAs yield ~1g/kg.
- QSFP56 connector gold: 38-pin connectors with 30-50 microinch gold plating. Calculated from first principles below.
- NVLink bridge connector gold: no specific assay data found for NVLink pads. Only generic connector/PCB gold recovery data.
- CoWoS-packaged GPU gold: no published assays for modern CoWoS flip-chip packages. Confirmed that GA100 uses copper pillar bumps, not gold wire bonds -- this was already corrected in report.md.

**QSFP56 gold calculation (first principles):**

Each QSFP56 cage has a host-side connector with 38 gold-plated contact pads. Per Molex QSFP+ datasheet: 15-30 microinch (0.38-0.76 um) Au over Ni underplate.

- Pad area estimate: each pad ~0.6mm x 3.5mm = 2.1 mm^2 (both sides = 4.2 mm^2 if dual-sided, but host pads are typically single-sided)
- Total area per cage: 38 x 2.1 mm^2 = ~80 mm^2
- At 30 microinch (0.76 um): Volume = 80 mm^2 x 0.00076 mm = 0.061 mm^3
- Mass = 0.061 mm^3 x 19.32 g/cm^3 = 0.061e-3 cm^3 x 19.32 = **0.0012g = 1.2 mg per cage**
- At 50 microinch (1.27 um): ~2.0 mg per cage

Two QSFP56 cages on the A100X: **~2.4-4.0 mg total gold**, or ~0.002-0.004g.

This is an order of magnitude lower than the 0.02g per cage in report.md. However, the report's 0.02g likely includes the cage housing's flash gold plating on the stainless steel cage walls (larger area than just the 38 electrical pads), plus the PCB-side through-hole solder pins. Even so, **the 0.02g/cage estimate may be ~5-10x too high**. A more realistic figure is 0.005-0.010g per QSFP56 cage assembly (pins + housing plating combined).

**Revised QSFP56 gold: 0.01-0.02g total for both cages (down from 0.04g)**

**NVLink bridge pads:**
- Each NVLink pad has 2 rows of gold-plated edge-connector fingers. Based on the A100 product brief showing 3 bridges needed for 600 GB/s, each bridge pad has ~60-80 contact fingers.
- At similar plating thickness (30 microinch) and ~1mm x 4mm finger area: ~0.03-0.04g per pad is plausible.
- 3 pads x ~0.03g = ~0.09g -- consistent with report.md's 0.09g estimate.

**Overall gold budget check:**

| Component | Report estimate | Investigation finding |
|-----------|----------------|----------------------|
| PCIe gold fingers | 0.12g | Plausible (x16 edge connector, well-documented) |
| GA100 BGA substrate pads | 0.30-0.40g | Cannot verify; CoWoS BGA has thousands of pads, copper pillar bumps, some gold in ENEPIG layer. Range plausible. |
| HBM micro-bumps | 0.15-0.25g | Cannot verify; 5 HBM stacks with Cu-Sn micro-bumps + thin Au diffusion layer. Low end more likely. |
| BlueField-2 BGA pads | 0.15g | Plausible for large BGA (7B transistor SoC) with ENEPIG finish |
| ENEPIG PCB finish | 0.10g | Plausible for 14-layer server-grade PCB |
| QSFP56 cages (2x) | 0.04g -> **0.01-0.02g** | Revised down from first-principles calculation |
| NVLink pads (3x) | 0.09g | Plausible from edge-connector finger count |
| Misc | 0.05g | Catchall, reasonable |
| **Total** | **1.0-1.3g** | **0.97-1.28g** (with QSFP revision) |

The QSFP correction is small ($2-3 at current spot) and doesn't materially change the 1.0-1.3g range. The largest uncertainties remain the GA100 CoWoS substrate gold and HBM micro-bump gold, neither of which can be resolved without destructive assay.

**Confidence on gold content:** 45/100 (no published assay for any CoWoS-packaged GPU; bottom-up estimate is methodologically sound but unverified)

**Sources:**
- [Gold Refining Forum -- BGA assay results](https://goldrefiningforum.com/threads/my-results-of-specific-types-of-ic-chips-flatpacks-and-bga.22951/) -- 11.4g Au/kg for mixed BGAs
- [Molex QSFP+ Interconnect Solution Datasheet](https://www.tti.com/content/dam/ttiinc/manufacturers/molex/doc/Molex-Quad-Small-Form-Factor-Pluggable-Plus-Interconnect-Solution-Datasheet-Specifications.pdf) -- 15/30 microinch Au plating spec
- [Advanced Plating Technologies -- Gold Plating Thickness](https://advancedplatingtech.com/gold-plating/gold-plating-thickness-connectors/) -- industry plating standards
- [Samtec -- Gold Plating on Connectors](https://blog.samtec.com/post/gold-plating-on-connectors-how-much-do-i-need/) -- 10 microinch standard option
- [QSFP MSA Specification (INF-8438i)](https://www.gigalight.com/downloads/standards/QSFP-MSA.pdf) -- 38-pin pinout

---

## 3. BlueField-2 eMMC Capacity

### Finding: RESOLVED -- standard BlueField-2 ships with 64GB eMMC; 16GB is DDR4, not flash

**What we searched:**
- NVIDIA BlueField-2 DPU Datasheet -- states: "eMMC - x8 NAND flash (memory size might vary on different DPUs)" for Arm boot, OS, and disk. The "16GB" figure in the datasheet refers to DDR4 SDRAM, not eMMC.
- BlueField-2 DPU Ethernet User Guide -- confirms eMMC is present for boot, with note that "eMMC 128GB memory is effectively 40GB with high durability."
- BlueField-2 SKU tables:
  - MBF2H516B-EENOT (P-Series, dual 100GbE): **16GB DDR4 + 64GB eMMC**
  - MBF2M355A-VESOT (E-Series, dual 200GbE): **32GB DDR4 + 64GB eMMC**
  - Some E-Series (MBF2M516C-EECOT): **16GB DDR + 128GB eMMC** (effective 40GB in high-durability mode)

**For the A100X specifically:**
The A100X uses the BlueField-2 P-Series SoC with 16GB DDR4 and dual 100GbE. The most common P-Series eMMC configuration is **64GB**. No A100X-specific documentation contradicts this. The report.md currently says "64-128 GB" which is technically correct across the BlueField-2 family, but the A100X almost certainly uses the **64GB eMMC** variant (matching the P-Series MBF2H516B-EENOT SKU).

The report.md also mentions "16GB x8 NAND flash" in the Web Verification section (Q4). This "16GB" was an error in our earlier transcription -- the BlueField-2 datasheet says "16GB x8" refers to the eMMC bus width (x8 NAND), not the capacity. The 16GB figure is the DDR4 capacity.

**Action:** Update report.md to specify 64GB eMMC (narrowed from "64-128 GB").

**Confidence on eMMC capacity:** 80/100 (strong match to P-Series SKU; only remaining doubt is whether NVIDIA used a custom eMMC size for the converged accelerator variant)

**Sources:**
- [NVIDIA BlueField-2 DPU Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/documents/datasheet-nvidia-bluefield-2-dpu.pdf) -- eMMC and DDR4 specs by SKU
- [NVIDIA BlueField-2 Ethernet DPU Specifications](https://docs.nvidia.com/networking/display/bluefield2dpuenug/specifications) -- 64GB eMMC for P-Series
- [BlueField-2 Datasheet on PDF4PRO](https://pdf4pro.com/view/nvidia-bluefield-2-datasheet-751a7d.html) -- eMMC 128GB = 40GB effective
- [Wiredzone MBF2H516B-EENOT listing](https://www.wiredzone.com/shop/product/10022862-nvidia-mellanox-bf2500-mbf2h516b-eenot-network-adapter-2-port-with-16gb-on-board-fhhl-9267) -- 16GB DDR4 + 64GB eMMC

---

## 4. TDP -- Is BlueField-2's 60-75W Within or On Top of 300W?

### Finding: CONFIRMED WITHIN -- the 300W is the total board power envelope, shared between GPU and DPU

**What we searched:**
- NVIDIA Converged Accelerator Datasheet -- lists "Max Power" as 300W for the A100X (A30X: 230W, AX800: 350W). This is a board-level spec, not per-chip.
- ServeTheHome analysis -- explicitly states: "Having a DPU that takes 60-75W from a PCIe power budget of... 300W with the new NVIDIA A100 80GB PCIe is a fairly huge percentage." This clearly describes a shared envelope, with the DPU consuming a portion of the 300W total.
- BlueField-2 DPU standalone power specs -- the standalone BlueField-2 P-Series card draws 75W from PCIe slot + up to 75W from supplementary 6-pin ATX connector (150W max for the full DPU card). But on the A100X, the DPU subsystem shares power delivery with the GPU.
- The A100 PCIe 80GB standalone card has a TDP of 300W. The A100X also has a TDP of 300W. If the DPU power were additive, the A100X would be 360-375W, which would exceed the EPS-12V 8-pin connector's ~300W delivery capacity and require a different power connector. The identical 300W rating confirms the GPU must be power-limited when the DPU is active.

**Implication for GPU performance:**
The GPU subsystem on the A100X can only draw ~225-240W (300W minus 60-75W for DPU), which is 75-80% of a standalone A100 PCIe 80GB's thermal budget. This explains why the A100X was positioned for inference/5G workloads rather than training -- the GPU runs at reduced clocks under full DPU load.

**Operating modes matter:**
- Standard mode: DPU and GPU operate separately but share the 300W envelope.
- BlueField-X mode: GPU is exposed to DPU directly (no host visibility). Power budget still shared.

The report.md already states this correctly. No changes needed.

**Confidence on TDP:** 90/100 (converging evidence from datasheet, ServeTheHome, and power connector physics)

**Sources:**
- [NVIDIA Converged Accelerator Datasheet](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcf21/converged-accelerator/pdf/datasheet.pdf) -- 300W max power
- [ServeTheHome: CPU-GPU-NIC PCIe Card Realized with NVIDIA BlueField-2 A100](https://www.servethehome.com/cpu-gpu-nic-pcie-card-realized-with-nvidia-bluefield-2-a100/) -- "60-75W from a PCIe power budget of... 300W"
- [NVIDIA BlueField-2 DPU Specifications](https://docs.nvidia.com/networking/display/bf2endpucontroller/specifications) -- standalone DPU power requirements
- [PNY A100X page](https://www.pny.com/nvidia-a100x) -- 300W power supply wattage

---

## 5. Secondary Market Pricing (Mar 2026)

### Finding: UPDATED -- market is thinner than expected; asking prices higher than report range

**What we searched:**
- eBay active listings for "A100X" / "900-21004-0030-000":
  - Pre-owned unit from Denmark: **$20,900** (or Best Offer) -- seller epokaas (100%, 70 feedback)
  - Brand new unit from China: **$31,350** (or Best Offer) -- seller memorypartner_ltd (100%, 100.9K feedback)
  - AX800 (BlueField-3 variant) listed at **$9,900**
- No eBay **sold** listings found in search results. The sold-item data is behind eBay's login wall and not indexed by search engines.
- ALTA Technologies and Fusion Worldwide list the A100X but require quote requests (no public pricing).
- Wiredzone shows the A100X as "no longer available" and notes it was "exclusively available as part of a Supermicro GPU server assembly."

**Market analysis:**
The report.md states "$6,000-$9,000" for used (Mar 2026). The eBay asking prices ($20,900 pre-owned, $31,350 new) are significantly higher, but eBay asking prices for niche datacenter hardware are typically 2-4x actual transaction prices. The $20,900 "Best Offer" listing may accept $8,000-$12,000 in negotiation.

For comparison, standard A100 PCIe 80GB used market (Mar 2026): $4,000-$9,000 (multiple sources confirm). The A100X should trade at a modest premium due to the integrated BlueField-2, but at a discount for the reduced GPU performance (shared 300W envelope) and limited buyer pool.

However, the China repair/reuse market may value the A100X higher because the BlueField-2 DPU integration means the card is export-controlled more aggressively, making surviving units more scarce. The $20,900 asking price from Denmark and $31,350 from China suggest at least some market participants value it well above a standard A100.

**Revised estimate:** The $6,000-$9,000 range in report.md may be low. A more defensible range given the eBay evidence is **$8,000-$15,000** for a working unit, with significant variance depending on whether the buyer needs the converged GPU+DPU functionality.

**Action:** Update report.md secondary market range to $8,000-$15,000 (widened upward).

**Confidence on secondary market:** 30/100 (no sold-listing data, only asking prices; extremely thin market makes any point estimate unreliable)

**Sources:**
- [eBay A100X listings](https://www.ebay.com/shop/nvidia-a100x?_nkw=nvidia+a100x) -- active listings
- [eBay A100X 80GB listing (204516284753)](https://www.ebay.com/itm/204516284753)
- [eBay A100X 80GB listing (157361332040)](https://www.ebay.com/itm/157361332040) -- $20,900 pre-owned
- [ALTA Technologies A100X](https://altatechnologies.com/products/nvidia-900-21004-0030-000) -- quote-based
- [Wiredzone A100X](https://www.wiredzone.com/shop/product/10025508-nvidia-900-21004-0030-000-graphics-processing-unit-gpu-a100x-converged-accelerator-80gb-hbm2e-memory-fhfl-10761) -- discontinued
- [NVIDIA A100 80GB pricing analysis](https://www.aitooldiscovery.com/ai-infra/nvidia-a100-specs-price) -- standard A100 used at $5,500-$7,500
- [DirectMacro A100 price guide](https://directmacro.com/blog/post/nvidia-a100-in-2025) -- used market $4,000-$9,000

---

## Summary of Changes to report.md

| Item | Old Value | New Value | Impact |
|------|-----------|-----------|--------|
| Card weight | ~1,250g estimated | ~1,250g estimated (unchanged) | None |
| Gold content | 1.0-1.3g | 1.0-1.3g (unchanged; QSFP56 revision immaterial) | None |
| QSFP56 gold (detail) | 0.02g Au per cage (0.04g total) | 0.005-0.01g per cage (0.01-0.02g total) | -$2.90 to -$5.80 gross |
| BlueField-2 eMMC | 64-128 GB | **64 GB** (P-Series SKU match) | Clarification only |
| TDP shared/separate | "DPU draws 60-75W from shared PCIe power budget of 300W" | Confirmed: shared, not additive | None (already correct) |
| Used market price | $6,000-$9,000 | **$8,000-$15,000** | +$2,000-$6,000 working unit value |
| Overall confidence | 60/100 | **62/100** (TDP +5, eMMC +3, market -3, weight -1, gold -2) | Marginal improvement |

### Remaining unknowns that require physical access or privileged data:
1. **Card weight** -- needs a unit on a scale
2. **Gold content** -- needs destructive fire assay
3. **Exact eMMC SKU** -- needs board-level inspection (likely Micron or Samsung 64GB eMMC 5.1)
4. **Actual transaction prices** -- needs eBay sold data or broker quotes
