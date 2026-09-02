# SXM/OAM Module Weight Investigation

**Date:** 2026-03-29
**Purpose:** Verify or correct unverified weight estimates used in scrap component models.

---

## Executive Summary

NVIDIA does not publish individual SXM bare module weights in any public datasheet, product brief, or service manual. AMD and Intel likewise omit bare OAM module weights from public documentation. The OCP OAM specification (v1.0 through v1.5) defines the PCB dimensions (102mm x 165mm) but does not specify a module mass limit or reference weight.

The single most useful data point discovered is the **NVIDIA HGX H100 PCF (Product Carbon Footprint) summary**, which states the complete HGX H100 baseboard weighs **24 kg**. This constrains the per-module weight when combined with known baseboard component weights.

PCIe card weights are well-documented in NVIDIA product briefs and provide useful anchor points for cross-checking SXM estimates.

---

## Known Reference Weights (Official NVIDIA Product Briefs)

These are NVIDIA-published board weights from official product briefs (bare board, excluding bracket/extenders):

| GPU | Form Factor | Board Weight (g) | Source |
|-----|-------------|-------------------|--------|
| Tesla V100 PCIe (16/32GB) | PCIe | 1,196 g | [NVIDIA PB-08744-001_v05](https://images.nvidia.com/content/tesla/pdf/Tesla-V100-PCIe-Product-Brief.pdf) |
| A100 40GB PCIe | PCIe | 1,240 g | [NVIDIA PB-10137-001_v03](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/A100-PCIE-Prduct-Brief.pdf) |
| A100 80GB PCIe | PCIe | 1,170 g | [NVIDIA PB-10577-001_v03](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/PB-10577-001_v02.pdf) |
| H100 80GB PCIe | PCIe | 1,200 g | [NVIDIA PB-11133-001_v02](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf) |
| H100 NVL 94GB PCIe | PCIe | 1,214 g | [NVIDIA H100 NVL Product Brief](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/h100/PB-11773-001_v01.pdf) |

Key observation: PCIe datacenter GPU boards are consistently in the 1,170--1,240 g range across three generations (Volta, Ampere, Hopper). This includes the passive heatsink, full-length PCB, and all components.

---

## HGX Baseboard Weight Constraint

The NVIDIA HGX H100 PCF Summary document states:
- **Product weight: 24 kg** (entire baseboard with 8x H100 SXM5 modules)
- Source: [NVIDIA HGX H100 PCF Summary](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-H100-PCF-Summary.pdf)

For comparison, the HGX B200 baseboard weighs **32 kg** (8x B200 SXM6, from the [NVIDIA HGX B200 PCF Summary](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf)).

### Deriving Per-Module Weight from HGX H100

The HGX H100 baseboard contains:
- 8x H100 SXM5 GPU modules (each with heatsink)
- 4x NVSwitch chips (3rd gen, mounted on the baseboard PCB)
- The baseboard PCB itself (large multi-layer, ~300mm x 416mm or larger)
- NVSwitch heatsinks
- Power delivery components on the baseboard
- Connectors (SXM5 sockets, PCIe edge connectors)

Estimating non-GPU baseboard mass:
- Baseboard PCB: ~2.0--3.0 kg (very large, dense multi-layer with heavy Cu planes for 5,600W delivery)
- 4x NVSwitch + heatsinks: ~0.5--1.0 kg (each NVSwitch die is small but requires a heatsink)
- Connectors, stiffeners, misc: ~0.5--1.0 kg

**Estimated non-GPU baseboard mass: ~3.0--5.0 kg**

Therefore: 8 GPU modules with heatsinks = 24 kg - (3.0 to 5.0 kg) = **19.0 to 21.0 kg**

**Per-module weight (with heatsink): ~2.4 to 2.6 kg**

This is significantly lower than the Omdia "over 3 kg" estimate and aligns better with the Tom's Hardware critique. Tom's Hardware noted that the H100 PCIe weighs 1.2 kg and a comparable OAM module with heatsink tops at ~2 kg, yielding a blended average of ~1.84 kg at 80/20 module/card mix -- not 3 kg.

---

## Module-by-Module Findings

### 1. H100 SXM5

**Current estimate:** ~3 kg total module with heatsink (Omdia); ~1,800 g heatsink derived by subtraction.

**Investigation findings:**
- NVIDIA does not publish individual SXM5 module weight. No teardown with a scale has been published.
- The Omdia estimate ("over 3 kg average weight of one H100 with heatsink") was published Sept 2023 via [Tom's Hardware](https://www.tomshardware.com/news/nvidia-sold-900-tons-of-h100-gpus-last-quarter) and [The Register](https://www.theregister.com/2023/09/19/900_tons_nvidia_servers/).
- Tom's Hardware immediately questioned this: the H100 PCIe weighs 1.2 kg (NVIDIA-confirmed), and a comparable OAM with heatsink is ~2 kg, making a blended average of ~1.84 kg at 80/20 module/card mix.
- The HGX H100 baseboard weighs 24 kg total. Back-calculating yields ~2.4--2.6 kg per SXM5 module with heatsink.
- The Comino teardown blog post exists but did not include mass measurements in available excerpts.
- ServeTheHome was allowed to hold a bare H100 package (not on SXM PCB) but was not allowed to photograph it, and no weight was reported.

**Revised estimate:** ~2.4--2.6 kg per module with heatsink. The 3 kg Omdia figure appears overstated.

**Heatsink revised estimate:** If the bare SXM5 board (PCB + GPU package + VRMs + passives + connector) weighs ~500--700 g (plausible given the SXM5 PCB is much smaller than a full-length PCIe card, but carries dense VRMs for 700W), then the heatsink is ~1.7--2.1 kg. Retaining ~1,800 g as a central estimate is reasonable, though it could be closer to 1,500--1,700 g if the bare board is heavier than estimated.

**Confidence:** 55/100 (improved from prior estimate, constrained by HGX total weight, but still no direct measurement)

| Source | Weight Claim | Assessment |
|--------|-------------|------------|
| Omdia (Sept 2023) | "over 3 kg" average with heatsink | Likely overstated -- may reflect a weighted average inflated by baseboard/tray components |
| Tom's Hardware analysis | ~1.84 kg blended average (80/20 module/card) | More plausible if "card" = PCIe at 1.2 kg and "module" = SXM at ~2 kg |
| HGX H100 PCF back-calculation | ~2.4--2.6 kg per module with heatsink | Best available indirect measurement |
| NVIDIA official | Not published | -- |

---

### 2. A100 SXM4

**Current estimate:** ~325 g bare module (no heatsink); component-sum estimate.

**Investigation findings:**
- NVIDIA does not publish bare SXM4 module weight. No teardown has weighed a bare A100 SXM4.
- The A100 PCIe 40GB board weighs 1,240 g and the 80GB weighs 1,170 g (NVIDIA product briefs). These include a full-length PCB + passive heatsink + bracket -- the SXM4 is a fundamentally different, smaller form factor.
- The SXM4 form factor is a bare module (no attached heatsink; cooling provided by server chassis). It carries the GA100 GPU package, VRM components, and an SXM4 connector.
- The A100 SXM4 has a smaller board than the H100 SXM5 and draws 400W vs 700W, so the VRM section is less massive.
- The 325 g component-sum estimate is plausible but unverified.

**Assessment:** 325 g as a bare module estimate remains reasonable. No contradicting data found. The module dimensions (similar to previous SXM generations) and the 400W power delivery requirements are consistent with a ~300--400 g bare board.

**Confidence:** 40/100 (unchanged -- no new data found to confirm or deny)

---

### 3. V100 SXM2

**Current estimate:** ~275 g bare module (no heatsink).

**Investigation findings:**
- NVIDIA does not publish bare SXM2 module weight.
- The V100 PCIe board weighs **1,196 g** (NVIDIA product brief PB-08744-001_v05). This includes a full-length PCB + passive heatsink.
- The SXM2 module dimensions are **140mm x 78mm** (from the V100 architecture whitepaper). This is a small bare module.
- The DGX-1 system (8x V100 SXM2) weighs 134 lbs / 61 kg total, but this includes dual Xeon CPUs, 512 GB RAM, SSDs, PSUs, chassis, etc. -- not useful for deriving individual module weight.
- The SXM2 form factor draws 300W and uses NVLink 2.0 (6 links). VRM complexity is lower than H100 SXM5.
- The DGX-1 service manual does not list individual GPU module weight.

**Assessment:** 275 g as a bare module estimate is plausible for a 140mm x 78mm bare board with VRM and one GPU package. No contradicting data found.

**Confidence:** 35/100 (unchanged -- no new data)

---

### 4. H200 SXM

**Current estimate:** **~640 g bare module** (revised from 1,020 g; see `H200_SXM/weight_engineering.md` and `H200_SXM/weight_investigation.md`).

**Investigation findings:**
- NVIDIA does not publish H200 SXM module weight. Exhaustive web research (40+ searches) confirms no published weight exists anywhere.
- The H200 uses the same GH100 die as H100, in the same SXM5 form factor, with upgraded memory (6x 24GB HBM3e stacks vs 5x 16GB HBM3).
- Since the H200 SXM fits the same SXM5 socket and uses the same baseboard (HGX H200 uses the same HGX form factor), its physical dimensions and heatsink design are likely very similar to H100 SXM5.
- The Lenovo service manuals for SR680a/SR685a reference "H100/H200 GPU and heat sink module" as a single FRU, suggesting identical or near-identical mechanical design.
- **DGX H100 and DGX H200 weigh identically: 287.6 lbs (130.45 kg).** This confirms the H200 module is physically interchangeable with the H100 module.
- **Dell XE9680 system weight by GPU config:** A100 SXM4 = 105 kg, H100/H200 SXM5 = ~108 kg, MI300X = ~114 kg. The ~3 kg delta for 8 modules (~375g/module with heatsink) is consistent with VRM scaling from 400W to 700W.
- **SXM5 PCB dimensions estimated at ~150x80mm** (Locuza photo analysis), giving ~12,000 mm^2 board area -- about 40% smaller than OAM (102x165mm = 16,830 mm^2).
- **No HGX H200 PCF document has been published.** Only HGX H100 (24 kg) and HGX B200 (32 kg) PCFs exist.
- Bottom-up engineering estimate yields 640 g (range 550--750 g), cross-checked 7 ways. See `H200_SXM/weight_engineering.md` for full calculation.

**Assessment:** The original 1,020 g was an artifact of subtracting an assumed heatsink from the overstated Omdia "3 kg" figure. The resulting 516 g "Other" category (50.6% of total) was a red flag -- solder, TIM, and passives on a 150x80mm board cannot weigh 516 g. The revised 640 g estimate is bottom-up, cross-validated, and self-consistent.

**Revised estimate:** ~640 g bare module (range 550--750 g). The previous 1,020 g has been retired.

**Confidence:** 55/100 (improved from 35; seven cross-checks converge, but still no direct measurement)

---

### 5. Gaudi2 HL-225H

**Current estimate:** ~850 g (engineering estimate, confidence 30-40/100).

**Investigation findings:**
- Intel/Habana does not publish the HL-225H card weight in the publicly accessible portions of the datasheet.
- The HL-225H datasheet PDF exists at [habana.ai](https://habana.ai/wp-content/uploads/2023/10/HL-225H_Datasheet_10_23.pdf) and [Intel CDN](https://cdrdv2-public.intel.com/784779/Gaudi2%20Mezzanine%20Card%20Datasheet%20.pdf). These may contain weight data in sections not indexed by search engines, but direct fetch was not possible in this investigation.
- The HL-225H complies with OCP OAM v1.1 specification: 102mm x 165mm PCB.
- Key specs: 600W TDP, 96GB HBM2E, 48MB SRAM, 24 tensor cores, 24x 100GbE RoCE v2 RDMA.
- No third-party teardown with weight measurements found.
- The OAM specification itself does not define a module weight limit.

**Assessment:** 850 g is a reasonable engineering estimate for an OAM v1.1 module at 600W TDP. However, it is completely unverified. The HL-225H has its own heatsink assembly as an OAM mezzanine card, so "850 g" likely includes whatever thermal solution is integrated.

**Confidence:** 30/100 (unchanged -- no new data found)

**Recommendation:** Download and review the full HL-225H datasheet PDF directly. The mechanical specifications section may list weight.

---

### 6. MI300X OAM

**Current estimate:** ~765 g (OAM module with heatsink).

**Investigation findings:**
- AMD does not publish MI300X OAM module weight in the public [MI300X data sheet](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-data-sheet.pdf).
- One third-party retailer (technologytraderz.com) lists the MI300X at "1.00 lb" (~454 g), but this may be a placeholder weight.
- A ServeTheHome discussion thread referenced a Supermicro listing (GPU-AMD-MI300X-OAM-0045H) showing "6 kg" for what was listed as 8 OAMs. Commenters debated whether this was per-unit or per-8-unit:
  - If 6 kg / 8 = **750 g per OAM module** -- very close to the current 765 g estimate.
  - One commenter estimated 6 kg was "in the ballpark" for a single OAM card plus heatsink and support frames, which would mean ~6 kg per module -- implausibly heavy.
- The MI300X is a 750W OAM module with a massive 153-billion-transistor chiplet package (8 compute dies + 4 I/O dies + 8 HBM3 stacks on a large organic substrate).
- An MI325X 8-GPU baseboard in its shipping box weighed ~39.5 kg (per ServeTheHome), but this includes foam, box, and the entire baseboard assembly.
- The OAM form factor is 102mm x 165mm PCB plus the accelerator package, VRM, heatsink, and stiffener.

**Assessment:** The 765 g estimate aligns well with the Supermicro listing interpreted as 6 kg / 8 modules. However, the listing is ambiguous. At 750W TDP, the MI300X will have a substantial thermal solution. 765 g for a bare OAM module with passive heatsink is plausible.

**Confidence:** 35/100 (marginally improved -- the 6 kg / 8 data point is weakly supportive but ambiguous)

---

## Summary Table

| Module | Current Estimate | Revised Estimate | Includes Heatsink? | Confidence | Best Available Source |
|--------|-----------------|------------------|---------------------|------------|---------------------|
| H100 SXM5 | ~3,000 g (with HS) | **~2,400--2,600 g (with HS)** | Yes | 55/100 | HGX H100 PCF back-calculation |
| H100 SXM5 heatsink | ~1,800 g | **~1,500--2,000 g** | (heatsink only) | 45/100 | Derived from revised total minus board |
| A100 SXM4 | ~325 g (bare) | ~325 g (bare) | No | 40/100 | Component-sum estimate (unchanged) |
| V100 SXM2 | ~275 g (bare) | ~275 g (bare) | No | 35/100 | Component-sum estimate (unchanged) |
| H200 SXM | ~1,020 g (bare) | **~640 g (bare, range 550--750 g)** | No (bare module, no baseboard heatsink) | 55/100 | Bottom-up engineering estimate + 7 cross-checks (see H200_SXM/weight_engineering.md, weight_investigation.md) |
| Gaudi2 HL-225H | ~850 g | ~850 g | Likely yes | 30/100 | Unverified estimate (unchanged) |
| MI300X OAM | ~765 g | ~765 g | Yes (passive) | 35/100 | Weakly supported by Supermicro 6kg/8 listing |

---

## Key Conclusions

1. **The Omdia "over 3 kg" H100 figure is almost certainly overstated.** The HGX H100 baseboard weighs 24 kg total (NVIDIA PCF data). Back-calculating yields ~2.4--2.6 kg per SXM5 module with heatsink. This is 15--20% less than the 3 kg Omdia estimate.

2. **No manufacturer publishes bare SXM/OAM module weight.** NVIDIA publishes PCIe card board weights in product briefs (V100: 1,196 g; A100: 1,170--1,240 g; H100: 1,200 g), but SXM module weights are absent from all public documentation.

3. **The H200 SXM weight estimate has been resolved.** The original 1,020 g was revised to **~640 g (range 550--750 g)** via bottom-up engineering estimate with seven cross-checks. The prior figure was an artifact of subtracting an uncertain heatsink from the overstated Omdia "3 kg" figure. The 516 g (51%) "Other" category was a residual padding error. Additional web research confirmed: DGX H100 and DGX H200 weigh identically (287.6 lbs); no HGX H200 PCF exists; Dell XE9680 shows A100-to-H100 delta of ~3 kg for 8 modules. See `H200_SXM/weight_engineering.md` and `H200_SXM/weight_investigation.md` for full analysis.

4. **The MI300X 765 g estimate has weak support** from a Supermicro listing that may show 6 kg for 8 OAM modules (= 750 g each), but the listing is ambiguous.

5. **Gaudi2 and V100/A100 bare module estimates remain completely unverified.** The Intel datasheet PDFs should be downloaded and reviewed directly for any mechanical specifications section.

---

## Recommended Actions

1. **H100 SXM5 components.csv:** Reduce heatsink weight from 1,800 g to ~1,700 g (or provide range of 1,500--2,000 g). Update the "SXM5 module with heatsink ~3 kg" note to "~2.4--2.6 kg per HGX H100 PCF back-calculation."

2. **H200 SXM components.csv: DONE.** Revised from 1,020 g to 640 g (bare module, no baseboard heatsink). Weight breakdown updated: heatspreader 200 g, VRM 190 g, PCB 95 g, GPU package 68 g, memory 17 g, connectors 50 g, misc 20 g. "Other" eliminated as a category.

3. **Download and review** the [HL-225H datasheet](https://habana.ai/wp-content/uploads/2023/10/HL-225H_Datasheet_10_23.pdf) and [MI300X data sheet](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-data-sheet.pdf) mechanical sections for any weight data not indexed by web search.

4. **Monitor eBay/secondary market** for individual SXM5 module listings that sometimes include shipping weight data, which can be used as an upper bound (packaging adds ~100--300 g).

---

## Sources

- [NVIDIA HGX H100 PCF Summary (24 kg baseboard weight)](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-H100-PCF-Summary.pdf)
- [NVIDIA HGX B200 PCF Summary (32 kg baseboard weight)](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf)
- [Tom's Hardware: Nvidia Sold 900 Tons of H100 GPUs (Omdia 3 kg critique)](https://www.tomshardware.com/news/nvidia-sold-900-tons-of-h100-gpus-last-quarter)
- [The Register: 900 tons of Nvidia H100 GPUs shipped](https://www.theregister.com/2023/09/19/900_tons_nvidia_servers/)
- [NVIDIA Tesla V100 PCIe Product Brief (1,196 g board)](https://images.nvidia.com/content/tesla/pdf/Tesla-V100-PCIe-Product-Brief.pdf)
- [NVIDIA A100 40GB PCIe Product Brief (1,240 g board)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/A100-PCIE-Prduct-Brief.pdf)
- [NVIDIA A100 80GB PCIe Product Brief (1,170 g board)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/PB-10577-001_v02.pdf)
- [NVIDIA H100 PCIe Product Brief (1,200 g board)](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf)
- [NVIDIA H100 NVL Product Brief (1,214 g board)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/h100/PB-11773-001_v01.pdf)
- [NVIDIA DGX H100/H200 Service Manual](https://docs.nvidia.com/dgx/dgxh100-service-manual/)
- [NVIDIA DGX-1 Datasheet (134 lbs system)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/dgx-1/dgx-1-rhel-datasheet-nvidia-us-808336-r3-web.pdf)
- [NVIDIA V100 Architecture Whitepaper (SXM2 dimensions)](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf)
- [Intel Gaudi2 HL-225H Datasheet](https://habana.ai/wp-content/uploads/2023/10/HL-225H_Datasheet_10_23.pdf)
- [AMD MI300X Data Sheet](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/data-sheets/amd-instinct-mi300x-data-sheet.pdf)
- [OCP OAM Specification v1.1 (102mm x 165mm)](https://www.opencompute.org/documents/ocp-accelerator-module-design-specification-v1p1-1-pdf)
- [Lenovo SR685a V3 H100/H200 GPU Install Guide](https://pubs.lenovo.com/sr685a-v3/install_an_h100_gpu)
- [ServeTheHome: AMD MI300X OAM Platform](https://www.servethehome.com/amd-instinct-mi300x-gpu-and-mi300a-apus-launched-for-ai-era/)
- [ServeTheHome: Checking Out the NVIDIA H100](https://www.servethehome.com/checking-out-the-nvidia-h100-in-our-first-look-at-hopper/)
- [Tom's Hardware: H100 SXM5 VRM Layout](https://www.tomshardware.com/news/nvidia-hopper-h100-sxm5-pictured)
- [Comino H100 Teardown Blog Post](https://www.comino.com/blog/how-we-destroyed-the-nvidia-h100-gpu-the-ultimate-comino-tear-down-comino-h100-waterblock-teaser)
