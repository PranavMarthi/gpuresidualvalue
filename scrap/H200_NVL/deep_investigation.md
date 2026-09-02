# H200 Deep Investigation: Five Key Unknowns

**Date:** 2026-03-29
**Starting confidence (both variants):** 60/100

---

## 1. H200 NVL Card Weight

**Question:** Estimated ~1,500g, no official source. Has NVIDIA published a product brief with weight?

### Findings

**No official H200 NVL weight has been published.** NVIDIA does not list bare-card weight in the H200 NVL datasheet (PNY), the H200 NVL whitepaper (inhosted.ai), or the NVIDIA H200 datasheet (resources.nvidia.com).

**Best available data points:**

| Source | Value | What It Measures |
|--------|-------|-----------------|
| H100 NVL product brief (PB-11773-001_v01) | **1,214 g** | Board weight, excluding bracket, extenders, and bridges |
| H100 NVL product brief | **20.5 g per bridge** (x3 bridges) | NVLink bridges |
| Microless retailer listing (H200 NVL) | **1.45 kg shipping weight** | Includes minimal packaging |
| Exxact listing (H200 NVL) | ~1.45 kg | Shipping weight |

**Analysis:**

The H100 NVL bare board (no bracket, no bridges) weighs 1,214 g. The H200 NVL uses the same PCB form factor, same heatsink design, same power delivery, and same GH100 die. The only physical difference is the memory subsystem: H200 enables all 6 HBM stacks (vs 5 active on H100) and upgrades from HBM3 to HBM3e 8-Hi stacks. Since each bare HBM stack weighs under 1 g, the memory upgrade adds negligible mass.

The 1.45 kg shipping weight from retailers is consistent with: 1,214 g board + ~50 g bracket + ~20 g antistatic bag + ~170 g box/padding = ~1,454 g. Alternatively: 1,214 g board + ~50 g bracket = ~1,264 g bare card with bracket.

**Verdict:** The report's estimate of ~1,500 g appears **too high by ~200 g**. A more defensible estimate is **~1,260-1,300 g** (board + bracket), derived from the confirmed H100 NVL board weight of 1,214 g plus bracket (~50 g). The memory upgrade adds negligible weight. Confidence in this revised estimate: 75/100.

**Impact on scrap values:** Modest. Approximately 200 g reduction comes primarily from heatsink/structural components (Al, Cu), reducing raw scrap by ~$0.50-$1.00. Not material.

---

## 2. H200 SXM Module Weight

**Question:** Estimated ~1,020g. Does any datasheet (Megware, PNY, Lenovo) list physical specs?

### Findings

**No published weight for either the H200 SXM or H100 SXM bare module exists in any publicly accessible source.** Checked:

- NVIDIA H200 Datasheet (Megware-hosted): no weight
- PNY H200 NVL Datasheet: NVL form factor only, no SXM weight
- Lenovo Press LP1944 product guide: no weight
- NVIDIA H200 product page: no weight
- Tom's Hardware H100 SXM5 teardown photos: no weight given
- ServeTheHome H100 SXM5 hands-on: Patrick Kennedy held the module but was not allowed to photograph the bare die assembly; no weight disclosed
- The Register (Nov 2025): noted "Nvidia has very rarely given out the weight of its SXM GPU cards" and attempted to estimate weights for their price-per-ounce comparison, but specific SXM module weights were not confirmed by NVIDIA
- TechPowerUp, VideoCardz, 2CRSi: no weight data

The 1,020 g figure in the existing report was described as "an engineering estimate derived by subtracting an assumed heatsink weight from The Register/Omdia average." This derivation has no primary source backing.

**Cross-reference:** For the H200 NVL PCIe card, the bare board (a much larger form factor with heatsink, backplate, bracket, VRM) weighs 1,214 g. An SXM module is substantially smaller and lacks a full-size heatsink, backplate, and bracket. The SXM module consists of: PCB (~120 g), GPU package + interposer (~92 g), VRM components (~150 g), heat spreader (~80 g), connector + stiffener (~75 g), memory stacks (~17 g), and passives/solder/misc. This sums to ~534 g of identified components, with ~486 g attributed to "other" in the existing breakdown -- an implausibly large residual (50.6% of total).

**Verdict:** The 1,020 g estimate is **plausible but poorly substantiated**, and the weight breakdown has a suspiciously large "other" category. A bare SXM module likely weighs somewhere in the **600-1,000 g range**, but without a published spec or physical measurement, confidence is low. Confidence in current estimate: 40/100 (downgraded from 45/100).

**Impact on scrap values:** Low. The SXM module's scrap value is dominated by precious metals and silicon content, not bulk material weight. A 200-400 g weight error would shift raw scrap by ~$1-2.

---

## 3. H200 NVL Gold Content (0.40 g)

**Question:** Is 0.40 g realistic? The H100 PCIe (same form factor) was estimated at 0.04-0.07 g elsewhere. Why would H200 NVL have 6-10x more gold?

### Findings

This is the most significant finding of the investigation. **The 0.40 g gold estimate is almost certainly too high, likely by a factor of 3-5x.**

**Engineering calculation for gold sources on the H200 NVL PCIe card:**

**a) PCIe x16 edge connector (gold fingers):**
- 164 pins, each ~0.70 x 3.91 mm, both sides
- Gold plating: ~30 microinches (0.76 um) per IPC/Intel spec
- Total gold-plated area: 164 x 0.70 x 3.91 x 2 = ~896 mm^2
- Gold volume: 896 mm^2 x 0.00076 mm = 0.68 mm^3
- Gold mass: 0.68 mm^3 x 19.3 mg/mm^3 = **~0.013 g**

**b) NVLink bridge connector pads:**
- The H200 NVL uses a single wide bridge connector (vs 3 bridges on H100 NVL). Bridge weighs ~20.5 g total (from H100 NVL product brief).
- Contact pads are gold-plated copper. Estimated total gold-plated area on card-side connector: ~400-800 mm^2
- At 0.76 um plating: 400-800 mm^2 x 0.00076 mm x 19.3 = **~0.006-0.012 g**

**c) PCB pad finish (ENIG/ENEPIG):**
- PCB area: ~267 x 111 mm = ~29,637 mm^2
- Pad coverage: ~15-25% of board area (conservative for high-density datacenter board)
- Gold-plated area: ~4,400-7,400 mm^2
- ENIG gold thickness: 0.05-0.20 um (IPC-4552 spec; typical production: 0.05-0.10 um)
- At 0.08 um typical: 5,900 mm^2 x 0.00008 mm x 19.3 = **~0.009 g**

**d) CoWoS package substrate ENIG/ENEPIG pads:**
- Package substrate area: ~2,500 mm^2 (interposer area; actual pad coverage ~30-40%)
- Gold-plated area: ~750-1,000 mm^2
- At 0.08 um: 875 mm^2 x 0.00008 mm x 19.3 = **~0.001 g**

**e) Gold wire bonds: NONE**
- Confirmed: H200 uses CoWoS-S with copper pillar bumps (flip-chip). No gold wire bonds. The original CSV listed "gold bond wires" as a source -- this is factually incorrect for any Hopper-class GPU.

**f) Other IC packages on board (PMICs, retimers, clock ICs, EEPROM):**
- ~10 ICs with small BGA/QFN packages, ENIG pads
- Combined gold-plated area: ~200-400 mm^2
- Gold content: **~0.001 g**

**Total engineering estimate: ~0.03-0.04 g of gold**

This aligns with:
- Experienced e-waste recyclers reporting PCIe x16 gold finger content of ~0.02-0.05 g per card
- The typical "0.5-1 g per consumer GPU" figure (which includes all motherboard-level gold if the entire card is processed as scrap -- the gold is spread across the entire assembly, not concentrated in one component)
- The ENIG calculation standard: ~0.4 g of gold per square meter of PCB at 20% pad coverage and 0.05 um thickness

**Why was 0.40 g originally estimated?**
The original CSV listed "0.8 g Au across die wire bonds, edge connector fingers, pad plating." The report halved this to 0.40 g after confirming no gold wire bonds, but this was still far too generous. The 0.8 g figure appears to have been sourced from generic "average graphics card gold content" estimates (0.5-1 g) which are often inflated by recycler marketing, or from older GPU generations that used gold wire bonds extensively.

**Verdict:** Gold content should be revised from **0.40 g down to ~0.04 g** (mid-estimate of engineering calculation range 0.03-0.04 g). This is a **10x reduction**. At $145/g, gold value drops from $57.60 to ~$5.80.

**Impact on scrap values:** Significant. The raw material scrap total drops by ~$52, and gold falls from 54% of raw scrap value to ~8%. The total raw scrap value would decrease from ~$101 to ~$49.

---

## 4. H200 SXM Gold Content (0.02-0.05 g)

**Question:** Very low for a ~1,020 g module. Is this too conservative? Compare with H100 SXM5 at 0.30 g (where did this figure come from?).

### Findings

**The H200 SXM report's 0.02-0.05 g range is actually more defensible than the NVL's 0.40 g.**

**Engineering calculation for SXM module gold:**

**a) SXM5 connector:**
- The SXM5 connector uses **silver-plated copper** pins, not gold-plated. This is confirmed in the H200 SXM components.csv ("silver-plated copper pins, 3.81 um Ag").
- Gold content from connector: **~0 g**

**b) Package substrate (ABF) ENIG/ENEPIG pads:**
- The organic ABF substrate under the CoWoS-S package has ENIG surface finish
- BGA pad area: ~5,000 mm^2 substrate, ~30-40% pad coverage = ~1,500-2,000 mm^2
- At 0.05-0.10 um ENIG gold: ~1,750 mm^2 x 0.00008 mm x 19.3 = **~0.003 g**

**c) PCB/module board pads:**
- Module board is much smaller than a PCIe card; pad area perhaps 2,000-3,000 mm^2
- At 0.08 um ENIG: ~2,500 mm^2 x 0.00008 mm x 19.3 = **~0.004 g**

**d) Small IC packages:**
- Fewer support ICs than PCIe card (VRM controllers, etc.)
- Gold content: **<0.001 g**

**Total engineering estimate: ~0.007-0.01 g of gold**

This is actually *lower* than the report's 0.02-0.05 g range, suggesting the existing estimate may even be slightly generous.

**Comparison with the "H100 SXM5 at 0.30 g" claim:** This figure (from the question prompt) does not appear in either report. If it exists elsewhere, it would be highly implausible for the same reasons: an SXM module has no gold-plated edge connector, uses silver-plated SXM5 pins, and all die-level interconnects are copper pillar bumps. 0.30 g would require ~20,000 mm^2 of ENIG surface at 0.8 um thickness, which far exceeds plausible pad area at realistic gold thicknesses.

**Verdict:** The existing 0.02-0.05 g range is **reasonable and may even be slightly generous**. A tighter mid-estimate of **~0.01 g** is defensible. The H200 SXM has dramatically less gold than a PCIe card because it lacks gold-plated edge connectors entirely. No change required to the report, though the mid-estimate in the precious metals table could shift from 0.02 g to 0.01 g.

**Impact on scrap values:** Minimal. Even at 0.05 g, gold contributes only $7.25 to a module with $15 total raw scrap value.

---

## 5. HBM3e Stack Pricing ($650/stack for secondary market)

**Question:** Is $650/stack realistic for secondary/broker market? What is current HBM3e pricing data?

### Findings

**OEM/contract pricing (primary market):**
- Goldman Sachs (2026 report): HBM3e priced at **$15/GB in 2025**, expected to decline to **$10/GB in 2026** (28% YoY decline)
- At $15/GB: 24 GB stack = **$360/stack** (OEM contract price)
- At $10/GB: 24 GB stack = **$240/stack** (OEM contract price)
- TrendForce (Dec 2025): Samsung and SK Hynix raised HBM3e contract prices **~20% for 2026**, pushing against the Goldman Sachs decline forecast
- Epoch AI B200 cost model: Total HBM3e cost for B200 (8 x 24 GB stacks) = ~$2,900, implying **~$362/stack** at OEM level (using $14-17/GB range, centered at $15)

**Secondary/broker market:**
- **No established secondary market exists** for individual HBM3e stacks. HBM3e is sold exclusively through long-term direct contracts between SK Hynix/Samsung/Micron and hyperscaler/OEM customers.
- Qualification cycles stretch for quarters; capacity is "effectively pre-sold" per TrendForce
- No broker pricing, no spot market, and no publicly traded individual stacks found in any search

**Assessment of the $650/stack figure:**
- At $650/stack, the implied price is **$27/GB** -- roughly 1.8x the OEM contract price of $15/GB
- This markup is plausible for a hypothetical secondary market with small-volume/spot purchases, qualification risk, and limited supply
- However, the market essentially does not exist in practice. HBM3e stacks are not sold individually; they are integrated at the package level during CoWoS assembly. Recovering individual stacks from a dead GPU is theoretically possible but extremely difficult (requires removing underfill, reballing, and requalifying -- operations that few facilities can perform)
- The H200 SXM report uses a more conservative **$300-$420/stack** range, which is closer to OEM pricing and arguably more defensible

**Verdict:** The $650/stack figure used in the H200 NVL report is **on the high end but not unreasonable as a theoretical maximum** for a broker/spot transaction. However, the practical reality is that this market barely exists. The price should be revised to **$360-$500/stack** ($240-$360 at OEM level + 50-100% broker markup for small volumes with no qualification guarantee). Total secondary memory value would decline from $3,900 to **$2,160-$3,000**.

The H200 SXM report's range of $300-$420/stack is more conservative and arguably better calibrated.

**Impact on scrap values:** Moderate impact on secondary/component salvage value. Reduces theoretical component salvage from ~$8,865 to ~$7,425-$8,265. Does not affect raw material scrap values.

---

## Summary of Recommended Changes

| Item | Current Value | Revised Value | Confidence Change |
|------|--------------|---------------|-------------------|
| H200 NVL card weight | ~1,500 g | ~1,260-1,300 g | 45 -> 75/100 |
| H200 SXM module weight | ~1,020 g | ~1,020 g (unchanged, low confidence) | 45 -> 40/100 |
| H200 NVL gold content | 0.40 g ($57.60) | 0.04 g ($5.80) | 50 -> 80/100 |
| H200 SXM gold content | 0.02-0.05 g ($2.90-$7.25) | 0.01-0.04 g ($1.45-$5.80) | 60 -> 75/100 |
| HBM3e stack price (NVL) | $650/stack ($3,900 total) | $360-$500/stack ($2,160-$3,000) | 40 -> 60/100 |
| HBM3e stack price (SXM) | $300-$420/stack ($1,800-$2,520) | $300-$420/stack (unchanged) | 55 -> 60/100 |

### Revised Overall Confidence

- **H200 NVL:** 60/100 -> **70/100** (weight clarified via H100 NVL product brief; gold content corrected by engineering calculation; HBM pricing better sourced)
- **H200 SXM:** 60/100 -> **65/100** (gold content confirmed reasonable; HBM pricing validated; weight still unverified)

---

## Sources

### NVIDIA Product Documentation
- [NVIDIA H100 NVL Product Brief (PB-11773-001_v01)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/h100/PB-11773-001_v01.pdf) -- H100 NVL board weight 1,214 g, bridge weight 20.5 g
- [NVIDIA H100 PCIe Product Brief (PB-11133-001)](https://www.nvidia.com/content/dam/en-zz/Solutions/gtcs22/data-center/h100/PB-11133-001_v01.pdf) -- H100 PCIe specifications
- [PNY H200 NVL Datasheet](https://www.pny.com/file%20library/company/support/linecards/data-center-gpus/h200-nvl-datasheet.pdf)
- [NVIDIA H200 Datasheet (Megware)](https://www.megware.com/fileadmin/user_upload/LandingPage%20NVIDIA/NVIDIA_H200_Datasheet.pdf)
- [NVIDIA H200 NVL Whitepaper](https://www.inhosted.ai/doc/hopper-h200-nvl-whitepaper.pdf)

### Weight & Physical Data
- [The Register: GPUs aren't worth their weight in gold (Nov 2025)](https://www.theregister.com/2025/11/28/gold_gpu_weights/) -- GPU weight estimates and price-per-ounce analysis
- [Microless H200 NVL listing](https://global.microless.com/product/nvidia-h200-nvl-tensor-core-graphics-card-141gb-memory-4-8-tb-s-memory-bandwidth-7-nvdec-7-jpeg-decoders-up-to-3-341-tflops-pcie-dual-slot-air-cooled-form-factor-90skc000-m9gan0/) -- shipping weight 1.45 kg
- [Exxact H200 NVL listing](https://www.exxactcorp.com/PNY-NVH200NVLTCGPU-KIT-E7943727)
- [ServeTheHome: First Look at H100 SXM5](https://www.servethehome.com/checking-out-the-nvidia-h100-in-our-first-look-at-hopper/)
- [Tom's Hardware: H100 SXM5 Pictured](https://www.tomshardware.com/news/nvidia-hopper-h100-sxm5-pictured)

### Gold Content & Precious Metals
- [ENIG Gold Thickness Standards (IPC-4552)](https://www.protoexpress.com/kb/enig/) -- 0.05-0.23 um gold layer
- [PCB ENIG Cost Calculation](https://sqpcb.com/pcb-enig-cost-calculation-exact-gold-cost-total-expense/) -- gold weight per m^2 methodology
- [Sierra Circuits: Gold Fingers](https://www.protoexpress.com/kb/gold-fingers/) -- 30 microinch (0.76 um) minimum gold on edge connectors
- [Gold Refining Forum: GPU gold content](https://goldrefiningforum.com/threads/is-there-any-gold-in-video-games-card.25267/) -- recycler-reported yields
- [ms.codes: How Much Gold Is In A Graphics Card](https://ms.codes/blogs/computer-hardware/how-much-gold-is-in-a-graphics-card) -- 0.5-1 g general estimate
- [TechInsights: NVIDIA H100 Hopper CoWoS-S Flip Chip BGA](https://www.techinsights.com/blog/nvidia-h100-hopper-tsmc-cowos-s-flip-chip-ball-grid-array) -- confirms copper pillar flip-chip packaging
- [Infinity Turbine: Precious Metals in H100 GPU](https://infinityturbine.com/gold-recovery-from-nvidia-h100-gpu-co2-extraction-by-infinity-turbine.html) -- H100 precious metal overview (approximate)

### HBM3e Pricing
- [Goldman Sachs via @Jukanlosreve](https://x.com/Jukanlosreve/status/1988063459448418377) -- HBM3E $15/GB -> $10/GB forecast for 2026
- [TrendForce: Samsung, SK Hynix ~20% HBM3E Price Hike for 2026](https://www.trendforce.com/news/2025/12/24/news-samsung-sk-hynix-reportedly-plan-20-hbm3e-price-hike-for-2026-as-nvidia-h200-asic-demand-rises/)
- [Epoch AI: NVIDIA B200 Cost Breakdown](https://epoch.ai/data-insights/b200-cost-breakdown) -- HBM3e at $14-17/GB, ~$362/stack
- [Seeking Alpha: Samsung, SK Hynix HBM3E price increase](https://seekingalpha.com/news/4535511-samsung-sk-hynix-increase-hbm3e-prices-by-20-percent-for-2026-orders-report)
- [@zephyr_z9: HBM3E $15/GB in 2025](https://x.com/zephyr_z9/status/2006320382958272864)
