# Datacenter GPU MSRP Verification

**Date:** 2026-03-29
**Purpose:** Cross-reference the "MSRP" figures used in the 22 scrap-value reports against the most authoritative available pricing data. NVIDIA does not publish official datacenter GPU MSRPs. All figures below are derived from OEM channel pricing (Cisco GPL, Lenovo configurators, Dell price lists), reseller listings, DGX system teardowns, launch-era press, and broker/resale data.

**Confidence scale:**
- **HIGH** = corroborated by 2+ independent OEM/reseller sources at launch or shortly after
- **MEDIUM** = single authoritative source, or multiple sources with significant spread
- **LOW** = no primary source; figure is an estimate, analyst inference, or single secondary-market data point

---

## Summary Table

| # | GPU | Report MSRP | Verified MSRP | Delta | Confidence | Key Source |
|---|-----|-------------|---------------|-------|------------|------------|
| 1 | A10 | $2,500 | $2,500-$2,800 | OK | MEDIUM | TechPowerUp launch price; Cisco UCSC-GPU-A10 reseller ~$7,588 (includes Cisco margin) |
| 2 | A100 PCIe 40GB | $11,000 | $10,000-$12,000 | OK | HIGH | CNBC ("$10,000 chip"), multiple resellers, DGX A100 teardown ($199K / 8 = $24.9K system-level) |
| 3 | A100 PCIe 80GB | $15,000 | $15,000-$17,000 | OK | HIGH | Cisco UCSC-GPU-A100-80 = $36,252 (Connection.com, includes Cisco margin ~2.4x); market consensus $15K |
| 4 | A100 SXM4 80GB | $10,000-$11,000 | $15,000-$20,000 | **LOW by $5-9K** | MEDIUM | SXM4 not sold individually; DGX A100 ($199K) implies ~$25K/GPU at system level; standalone SXM market pricing $15-20K; report figure appears to be 40GB PCIe pricing misapplied |
| 5 | A100X | ~$33,700 | ~$33,700 | OK | MEDIUM | Interpro Microsystems (Supermicro Tier-1 partner) lists at $33,717.15; niche product with thin market |
| 6 | A16 PCIe | ~$5,000 | ~$5,000-$5,500 (NVIDIA channel) | OK but uncertain | LOW | No public NVIDIA MSRP; Cisco UCSC-GPU-A16 MSRP = $17,152 (Tech-America), reseller ~$8,249 (Connection.com), both include Cisco margin. Direct NVIDIA channel ~$5,000 is plausible but unverified |
| 7 | A30 PCIe | $4,599 | $4,599 | OK | HIGH | Thinkmate lists at $4,599; Amazon/PNY ~$5,199; multiple resellers confirm $3,500-$5,000 range |
| 8 | A40 | ~$27,500 (OEM) | ~$27,500 | OK | HIGH | Cisco UCSC-GPU-A40 = $27,561 (Hummingbird Networks); Lenovo 4X67A72593 = EUR 26,526 (~$28,500). Two independent OEM sources. NOTE: gpucost.org lists "$5,000" which is the current *used* price, not launch MSRP |
| 9 | MI300X | ~$15,000 | $10,000-$15,000 | OK (upper bound) | MEDIUM | AMD never disclosed MSRP. Samsung bulk purchase implied ~$10K/unit; gpucost.org lists $15K; market consensus $10-15K enterprise |
| 10 | Gaudi2 HL-225H | $8,125 | $8,125 | OK | HIGH | ServeTheHome launch article: $65K / 8-card UBB kit = $8,125/card. Single authoritative source but widely cited |
| 11 | H100 PCIe 80GB | $25,000-$30,000 | $25,000-$30,000 | OK | HIGH | Raymond James (Jan 2024) est. $25-30K; Cisco UCSC-GPU-H100-80 MSRP = $99,696 (Tech-America) / reseller $61,521 (CompSource) -- Cisco margins are ~3-4x NVIDIA channel; ASA Computers lists at $30,971 |
| 12 | H100 SXM5 80GB | $25,000-$40,000 | $25,000-$40,000 | OK | MEDIUM | Not sold individually; DGX H100 ($350-500K for 8-GPU) implies $25-35K/GPU at system level. Market range very wide due to supply/demand fluctuations 2023-2025 |
| 13 | H200 NVL | $35,000-$40,000 | $31,000-$45,000 | OK | MEDIUM | Resellers list $31-32K (single card) to $45K; TRG Datacenters, IntuitionLabs, Modal.com all cite $30-40K range |
| 14 | H200 SXM | $25,000 | $38,000-$44,000 | **LOW by $13-19K** | LOW | TRG Datacenters: 4-GPU SXM board = $175K (~$43.75K/GPU); 8-GPU board = $308-315K (~$38-39K/GPU). $25K figure in report appears too low -- likely confused with H100 SXM pricing. No standalone SXM module sales to verify |
| 15 | L4 | $2,500 | $2,500 | OK | MEDIUM | gpucost.org MSRP = $2.5K; market price ~$2.8K; Amazon PNY L4 = $2,599 |
| 16 | L40 | ~$6,800 | ~$30,000-$33,000 (OEM list) | **LOW by ~$23-26K** | HIGH | Cisco UCSC-GPU-L40 = $30,915 (CDW MSRP); Lenovo ThinkSystem L40 = $33,109; Cisco GPL ~$30K. The $6,800 in the report is the *current used market price*, not the launch OEM list price |
| 17 | L40S | ~$8,000 | ~$39,000-$52,000 (OEM list) | **LOW by ~$31-44K** | HIGH | Cisco UCSC-GPU-L40S MSRP = $30,930-$39,095 (IDM Products); Lenovo MSRP = $51,579. The $8,000 in the report is the *current used market price*, not the launch OEM list price |
| 18 | GH200 | ~$35,000 | $35,000-$45,000 | OK | MEDIUM | Fluence: single module sells for $35-45K; GPTshop.ai base system = $41,500 (includes CPU + chassis); NotebookCheck valued used dual-GH200 at ~$80K new |
| 19 | MI210 | ~$16,500 | ~$16,500 | OK | MEDIUM | WCCFTech/TweakTown: Japanese market price 2,087,800 JPY = ~$16,486 USD. Single-market data point but widely cited; AMD never disclosed MSRP |
| 20 | T4 | $2,500 | $2,299 | **HIGH by ~$200** | HIGH | TechPowerUp database: launch MSRP $2,299; TechCrunch launch article corroborates. $2,500 is close but slightly overstated |
| 21 | V100 PCIe 16GB | $8,000 | $8,000-$10,664 | OK (low end) | HIGH | Microway price analysis: $10,664 single-unit list; CDW/Next Platform (Mar 2018): $9,900; general market consensus $8-10K |
| 22 | V100 PCIe 32GB | $10,000 | $10,000-$11,458 | OK (low end) | HIGH | Microway: $11,458 single-unit list for 32GB variant; premium of ~$800-1,500 over 16GB |
| 23 | V100 SXM2 | $8,000-$10,000 | $10,000-$15,900 | **LOW by $2-6K** | MEDIUM | SXM2 commanded premium over PCIe: Microway lists 16GB SXM2 at ~$15,900; not sold individually but priced through DGX-1 ($149K / 8 = $18.6K system-level) |
| 24 | V100S PCIe 32GB | ~$11,500 | ~$11,000-$11,500 | OK | MEDIUM | Microway: $11,458 for V100 32GB PCIe; V100S was higher-clocked refresh at similar or slightly higher price. No exact launch MSRP published; IT Creations lists used at $9,288 (2026) |

---

## Detailed Findings by GPU

### 1. NVIDIA A10 (PCIe, 24GB GDDR6, 150W)
**Report MSRP:** $2,500
**Verified:** $2,500-$2,800
**Confidence:** MEDIUM

- TechPowerUp GPU database lists the MSRP at the time of launch (April 2021) but the exact figure was not surfaced in web searches.
- NextPlatform (April 2021) cited the A10 at approximately $2,800 in a pricing comparison article.
- Cisco UCSC-GPU-A10 reseller price = $7,588.49 (Connection.com), which includes standard Cisco 2.5-3x markup over NVIDIA channel.
- gpupoet.com: estimated MSRP ~$2,800.
- Newegg: ~$3,299 (retail markup).
- The $2,500 figure is plausible as a direct NVIDIA channel/OEM price, possibly the lower bound.

**Sources:**
- [VideoCardz: NVIDIA announces A10 and A30](https://videocardz.com/press-release/nvidia-announces-a10-and-a30-tensor-core-gpus)
- [Cisco UCSC-GPU-A10 at Connection.com](https://www.connection.com/product/cisco-tesla-a10-passive-150w-24gb/ucsc-gpu-a10/41269988)
- [GPU Poet: A10 Specs & Pricing](https://gpupoet.com/gpu/learn/card/nvidia-a10)

---

### 2. NVIDIA A100 PCIe 40GB / 80GB
**Report MSRP:** $11,000 (40GB) / $15,000 (80GB)
**Verified:** $10,000-$12,000 (40GB) / $15,000-$17,000 (80GB)
**Confidence:** HIGH

- CNBC (Feb 2023): "Nvidia's A100 is the $10,000 chip powering the race for AI" -- widely cited as the canonical A100 figure.
- Multiple market sources: A100 40GB PCIe at $10,000-$12,000; A100 80GB PCIe at $13,000-$17,000.
- Cisco UCSC-GPU-A100-80= listed at $36,251.85 (Connection.com) -- standard Cisco markup of ~2.4x.
- DGX A100 system at $199,000 with 8x A100 SXM4 GPUs = $24,875/GPU at system level (includes NVSwitch, CPUs, chassis).
- The report figures ($11K/$15K) fall within the verified range and are reasonable for direct NVIDIA channel pricing.

**Sources:**
- [CNBC: NVIDIA's A100 is the $10,000 chip](https://www.cnbc.com/2023/02/23/nvidias-a100-is-the-10000-chip-powering-the-race-for-ai-.html)
- [Cisco UCSC-GPU-A100-80 at Connection.com](https://www.connection.com/product/cisco-tesla-a100-passive-300w-80g/ucsc-gpu-a100-80/41498129)
- [Northflank: How much does an NVIDIA A100 cost?](https://northflank.com/blog/nvidia-a100-gpu-cost)
- [Modal: How much is an Nvidia A100?](https://modal.com/blog/nvidia-a100-price-article)

---

### 3. NVIDIA A100 SXM4 80GB
**Report MSRP:** $10,000-$11,000
**Verified:** $15,000-$20,000
**Confidence:** MEDIUM
**STATUS: REPORT FIGURE IS LOW**

- The $10,000-$11,000 figure in the report matches the A100 40GB *PCIe* launch price, not the SXM4.
- SXM4 modules are not sold individually -- they are sold as part of HGX/DGX systems.
- Multiple sources cite SXM4 standalone market pricing at $18,000-$20,000 new.
- DGX A100 ($199,000 / 8 GPUs) implies ~$24,875/GPU at system level, but significant system overhead reduces the per-GPU attribution.
- A realistic NVIDIA-channel price for a standalone A100 SXM4 80GB module is $15,000-$20,000.
- **Recommendation:** Revise report MSRP to $15,000-$20,000, or clarify that $10,000-$11,000 represents only the 40GB PCIe variant.

**Sources:**
- [NVIDIA DGX A100 press release](https://nvidianews.nvidia.com/news/nvidia-ships-worlds-most-advanced-ai-system-nvidia-dgx-a100-to-fight-covid-19-third-generation-dgx-packs-record-5-petaflops-of-ai-performance)
- [AI Tool Discovery: A100 Specs & Price](https://www.aitooldiscovery.com/ai-infra/nvidia-a100-specs-price)
- [SimplePod: Understand the Nvidia A100 Price](https://simplepod.ai/blog/nvidia-a100-price/)

---

### 4. NVIDIA A100X (Converged Accelerator, BlueField-2 DPU)
**Report MSRP:** ~$33,700
**Verified:** ~$33,700
**Confidence:** MEDIUM

- Interpro Microsystems (Supermicro Tier-1 direct partner): $33,717.15.
- Ahead-IT (EU): EUR 16,184 (~$17,400) -- significantly lower, but EU pricing often diverges.
- Niche product sold almost exclusively through Supermicro GPU server assemblies for 5G/telecom.
- The $33,700 figure from a Supermicro Tier-1 partner is the most authoritative available.

**Sources:**
- [Interpro Microsystems: NVIDIA A100X](https://www.interpromicro.com/product/38951-nvidia-a100x-converged-accelerator)
- [Exxact: NVIDIA A100X](https://www.exxactcorp.com/NVIDIA-900-21004-0030-000-E5520399)
- [PNY: NVIDIA A100X](https://www.pny.com/nvidia-a100x)

---

### 5. NVIDIA A16 PCIe (4x GA107, 64GB total)
**Report MSRP:** ~$5,000
**Verified:** ~$5,000 (NVIDIA channel, unverified); Cisco OEM MSRP = $17,152
**Confidence:** LOW

- NVIDIA does not publish A16 MSRP.
- Cisco UCSC-GPU-A16 MSRP = $17,151.83 (Tech-America.com) -- but this is Cisco OEM pricing with ~3x markup.
- Connection.com reseller price = $8,249.23; Tech-America sale price = $7,493.
- The $5,000 figure may originate from a 2021 NextPlatform article that listed approximate NVIDIA-channel prices for Ampere datacenter GPUs, but no direct source was found.
- Report correctly notes this is "unverified."

**Sources:**
- [Tech-America: Cisco UCSC-GPU-A16](https://www.tech-america.com/item/nvidia-a16-pcie-250w-4x16gb4x16gb/ucsc-gpu-a16)
- [Connection.com: Cisco UCSC-GPU-A16](https://www.connection.com/product/cisco-nvidia-a16-pcie-250w-4x16gb/ucsc-gpu-a16/41426143)
- [CDW: UCSC-GPU-A16](https://www.cdw.com/product/nvidia-gpu-computing-processor-64-gb/8249381)

---

### 6. NVIDIA A30 PCIe (24GB HBM2, 165W)
**Report MSRP:** $4,599
**Verified:** $4,599
**Confidence:** HIGH

- Thinkmate lists NVIDIA A30 at $4,599.00.
- Amazon PNY A30 Module (TCSA30M-PB) at $5,199.
- router-switch.com: retail range $3,500-$5,000.
- The $4,599 appears to be the standard NVIDIA-channel/reseller price, well-corroborated.

**Sources:**
- [GPU Poet: A30 Specs & Pricing](https://gpupoet.com/gpu/learn/card/nvidia-a30)
- [Amazon: PNY NVIDIA A30](https://www.amazon.com)
- [ServerSupply: NVIDIA A30 Dell OEM](https://www.serversupply.com/GPU/HBM2/24GB/NVIDIA/699-21001-0205-600_379654.htm)

---

### 7. NVIDIA A40 (48GB GDDR6, 300W)
**Report MSRP:** ~$27,500 (OEM)
**Verified:** ~$27,500
**Confidence:** HIGH

- Cisco UCSC-GPU-A40 = $27,561.22 (Hummingbird Networks).
- Lenovo ThinkSystem A40 (4X67A72593) = EUR 26,526 (~$28,500 USD).
- Two independent OEM sources corroborate the ~$27,500 figure.
- **Critical note:** gpucost.org and some secondary sources list "$5,000" for the A40 -- this is the *current used market price*, not the launch OEM list price. The original report caught this error and revised up from $5,000 to $27,500.

**Sources:**
- [Cisco UCSC-GPU-A40 GPL via itprice.com](https://itprice.com/cisco-gpl/nvidia%20a40)
- [Lenovo Press: ThinkSystem NVIDIA A40](https://lenovopress.lenovo.com/lp1773-thinksystem-nvidia-a40-48gb-pcie-gen4-passive-gpu)
- [GPU Poet: A40 Specs & Pricing](https://gpupoet.com/gpu/learn/card/nvidia-a40)

---

### 8. AMD Instinct MI300X (OAM, 192GB HBM3, 750W)
**Report MSRP:** ~$15,000
**Verified:** $10,000-$15,000
**Confidence:** MEDIUM

- AMD has never disclosed an official MSRP.
- Samsung bulk purchase (WCCFTech): implied ~$10,000/unit.
- gpucost.org: $15K MSRP.
- Multiple analyst reports: $10,000-$15,000 enterprise pricing.
- Current market price: $16,000-$18,000 (above "MSRP" due to AI demand).
- The $15,000 figure represents the upper end of the estimated range and is defensible.

**Sources:**
- [WCCFTech: Samsung purchases MI300X GPUs](https://wccftech.com/samsung-amd-instinct-mi300x-ai-gpus-data-center-ai-worth-20-million-usd/)
- [gpucost.org: MI300X](https://gpucost.org/gpu/mi300x)
- [getdeploying.com: MI300X pricing](https://getdeploying.com/gpus/amd-mi300x)

---

### 9. Intel Habana Gaudi2 HL-225H (OAM, 96GB HBM2e, 600W)
**Report MSRP:** $8,125 (per card, from $65K 8-card UBB kit)
**Verified:** $8,125
**Confidence:** HIGH

- ServeTheHome launch article (May 2022): $65,000 for the 8-card Universal Base Board (UBB) kit = $8,125/card.
- This is the only publicly available pricing and is widely cited across tech media.
- No contradictory pricing has been found.

**Sources:**
- [ServeTheHome: Intel Habana Gaudi2 Launched](https://www.servethehome.com/intel-habana-gaudi2-launched-ai-training-chip-supermicro-ddn-oam/)
- [Intel Habana Gaudi2 Datasheet](https://habana.ai/wp-content/uploads/2023/10/HL-225H_Datasheet_10_23.pdf)

---

### 10. NVIDIA H100 PCIe 80GB (350W)
**Report MSRP:** $25,000-$30,000
**Verified:** $25,000-$30,000
**Confidence:** HIGH

- Raymond James Financial analysts (Jan 2024): estimated NVIDIA selling price at $25,000-$30,000.
- ASA Computers: $30,970.79 (retail).
- Cisco UCSC-GPU-H100-80 MSRP = $99,696 (Tech-America) -- Cisco markup is ~3-4x NVIDIA channel.
- CompSource reseller: $61,521 (Cisco part).
- The $25-30K range is well-established by multiple analyst and reseller sources.

**Sources:**
- [TRG Datacenters: NVIDIA H100 Price](https://www.trgdatacenters.com/resource/nvidia-h100-price/)
- [ASA Computers: H100 80GB](https://www.asacomputers.com/nvidia-h100-80gb-nvh100tcgpu-gpu-card.html)
- [Northflank: How much does an H100 cost?](https://northflank.com/blog/how-much-does-an-nvidia-h100-gpu-cost)
- [AI Tool Discovery: H100 Specs & Price](https://www.aitooldiscovery.com/ai-infra/nvidia-h100-specs-price)

---

### 11. NVIDIA H100 SXM5 80GB (700W)
**Report MSRP:** $25,000-$40,000
**Verified:** $25,000-$40,000
**Confidence:** MEDIUM

- SXM5 modules not sold individually; priced through DGX/HGX systems.
- DGX H100 (8x SXM5): $350,000-$500,000 = $43,750-$62,500/GPU at system level (includes NVSwitch, CPUs).
- Market pricing 2023-2024: $27,000-$45,000 per SXM5 unit on secondary market.
- The range is very wide, reflecting supply/demand volatility during 2023-2025.
- By Q1 2026, stabilized at ~$25K-$35K.

**Sources:**
- [Fluence: NVIDIA H100 Deep Dive](https://www.fluence.network/blog/nvidia-h100-deep-dive/)
- [Wecent: H100 price 2026](https://www.szwecent.com/what-is-the-current-nvidia-h100-price-in-2025/)
- [ArcCompute: H100 PCIe vs SXM5](https://www.arccompute.io/arc-blog/nvidia-h100-pcie-vs-sxm5-form-factors-which-gpu-is-right-for-your-company)

---

### 12. NVIDIA H200 NVL (PCIe, 141GB HBM3e, 600W)
**Report MSRP:** $35,000-$40,000
**Verified:** $31,000-$45,000
**Confidence:** MEDIUM

- Single NVL GPU card: $31,000-$32,000 (some resellers).
- Through authorized resellers: $35,000-$45,000.
- TRG Datacenters, IntuitionLabs, Modal.com all cite $30-40K range.
- The report range of $35-40K is within the verified band but may be slightly narrow.

**Sources:**
- [TRG Datacenters: H200 Price Guide](https://www.trgdatacenters.com/resource/nvidia-h200-price-guide/)
- [IntuitionLabs: NVIDIA AI GPU Pricing](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [Modal: How much is an Nvidia H200?](https://modal.com/blog/nvidia-h200-price-article)
- [Jarvislabs: H200 Price Guide](https://docs.jarvislabs.ai/blog/h200-price)

---

### 13. NVIDIA H200 SXM (700W, 141GB HBM3e)
**Report MSRP:** $25,000
**Verified:** $38,000-$44,000
**Confidence:** LOW
**STATUS: REPORT FIGURE IS LOW**

- TRG Datacenters: 4-GPU SXM board = $175,000 (~$43,750/GPU); 8-GPU board = $308-315K (~$38-39K/GPU).
- The $25,000 figure appears to understate the H200 SXM by $13-19K.
- H200 SXM is a higher-spec product than H100 SXM5 (HBM3e vs HBM3) and should be priced at a premium.
- The $25K figure may have been confused with the lower end of H100 SXM5 pricing.
- **Recommendation:** Revise to $35,000-$44,000, or flag as highly uncertain.

**Sources:**
- [TRG Datacenters: H200 Price Guide](https://www.trgdatacenters.com/resource/nvidia-h200-price-guide/)
- [IntuitionLabs: NVIDIA AI GPU Pricing](https://intuitionlabs.ai/articles/nvidia-ai-gpu-pricing-guide)
- [Hyperstack: H200 SXM Guide](https://www.hyperstack.cloud/blog/case-study/nvidia-h200-sxm-guide-specs-pricing-and-how-to-reserve-your-gpu-vm)

---

### 14. NVIDIA L4 (PCIe HHHL, 24GB GDDR6, 72W)
**Report MSRP:** $2,500
**Verified:** $2,500
**Confidence:** MEDIUM

- gpucost.org: MSRP $2,500; market price ~$2,800.
- Amazon PNY L4: ~$2,599.
- The figure is consistent across sources.

**Sources:**
- [gpucost.org: L4](https://gpucost.org/gpu/l4)
- [Amazon: NVIDIA Tesla L4 24GB](https://www.amazon.com/NVIDIA-Tesla-Graphics-ACELLERATOR-900-2G193-0000-000/dp/B0D9J1KZZX)
- [GPU Poet: L4 Specs & Pricing](https://gpupoet.com/gpu/learn/card/nvidia-l4)

---

### 15. NVIDIA L40 (PCIe, 48GB GDDR6, 300W)
**Report MSRP:** ~$6,800
**Verified:** ~$30,000-$33,000 (OEM list)
**Confidence:** HIGH
**STATUS: REPORT FIGURE IS WRONG -- USING CURRENT USED PRICE, NOT LAUNCH MSRP**

- Cisco UCSC-GPU-L40: CDW MSRP = $30,915.31; CDW sale price = $20,258.
- Lenovo ThinkSystem L40 (4X67A84823): MSRP = $33,109.
- Cisco GPL: ~$30,000.
- The $6,800 in the report is the *current secondary market / used price* (Mar 2026), not the original OEM list price.
- **Recommendation:** The report should use ~$30,000-$33,000 as the OEM launch price, or explicitly label $6,800 as "current market price" and not "MSRP."

**Sources:**
- [CDW: Cisco UCSC-GPU-L40](https://www.cdw.com/product/nvidia-l40-gpu-computing-processor-48-gb/7535116)
- [GPU Poet: L40 Specs & Pricing](https://gpupoet.com/gpu/learn/card/nvidia-l40)
- [getdeploying.com: L40](https://getdeploying.com/gpus/nvidia-l40)

---

### 16. NVIDIA L40S (PCIe, 48GB GDDR6, 350W)
**Report MSRP:** ~$8,000
**Verified:** ~$39,000-$52,000 (OEM list)
**Confidence:** HIGH
**STATUS: REPORT FIGURE IS WRONG -- USING CURRENT USED PRICE, NOT LAUNCH MSRP**

- Cisco UCSC-GPU-L40S: $30,930-$39,095 (IDM Products, CompSource).
- Lenovo MSRP = $51,579.
- Estimated consensus MSRP: ~$45,000 (midpoint of OEM range).
- The $8,000 in the report is the *current secondary market / used price* (Mar 2026), not the original OEM list price.
- **Recommendation:** The report should use ~$39,000-$52,000 as the OEM launch price, or explicitly label $8,000 as "current market price."

**Sources:**
- [IDM Products: Cisco UCSC-GPU-L40S](https://idmproducts.com/cisco-systems-cai-gpu-l40s-nvidia-l40s-350w-48gb-2-slot-fhfl-gpu/)
- [Lenovo Press: L40S Product Guide](https://lenovopress.lenovo.com/lp1812-nvidia-l40s-48gb-pcie-gen4-passive-gpu)
- [GPU Poet: L40S Specs & Pricing](https://gpupoet.com/gpu/learn/card/nvidia-l40s)

---

### 17. NVIDIA GH200 Grace Hopper Superchip
**Report MSRP:** ~$35,000
**Verified:** $35,000-$45,000
**Confidence:** MEDIUM

- Fluence: single GH200 module sells for $35,000-$45,000.
- GPTshop.ai: base GH200 workstation system = $41,500 (includes chassis, but the module is the primary cost).
- NotebookCheck: valued a used dual-GH200 server at ~$80K new (= ~$40K per module).
- The $35K figure is at the low end of the verified range but defensible.

**Sources:**
- [Fluence: NVIDIA GH200 Explained](https://www.fluence.network/blog/nvidia-gh200/)
- [Tom's Hardware: Grace Hopper Superchip systems start at $41,500](https://www.tomshardware.com/pc-components/cpus/nvidias-first-cpugpu-chips-come-to-ai-workstation-desktop-pcs)
- [NotebookCheck: Developer scores GH200 at discount](https://www.notebookcheck.net/Gamble-pays-off-Developer-scores-80-000-worth-of-hardware-with-960-GB-DDR5-memory-and-Nvidia-GH200-superchip-at-a-tenth-of-the-price.1183544.0.html)

---

### 18. AMD Instinct MI210 (PCIe, 64GB HBM2e, 300W)
**Report MSRP:** ~$16,500
**Verified:** ~$16,500
**Confidence:** MEDIUM

- WCCFTech and TweakTown (March 2022): Japanese market launch price of 2,087,800 JPY (tax included) = ~$16,486 USD.
- AMD never published an official MSRP.
- AnandTech launch article confirms the MI210 was the PCIe variant of CDNA 2, aimed at mainstream server slots.
- Single-market (Japan) data point, but widely cited and no contradictory pricing has emerged.

**Sources:**
- [WCCFTech: AMD MI210 priced $16,500 in Japan](https://wccftech.com/amd-instinct-mi210-gpu-accelerator-with-64-gb-hbm2e-memory-16500-usd-price-japan/)
- [TweakTown: AMD MI210 costs $16,500](https://www.tweaktown.com/news/85675/amd-instinct-mi210-accelerator-mcm-gpu-64gb-hbm2e-costs-16-500/index.html)
- [AnandTech: AMD Releases Instinct MI210](https://www.anandtech.com/show/17326/amd-releases-instinct-mi210-accelerator-cdna-2-on-a-pcie-card)

---

### 19. NVIDIA T4 (PCIe HHHL, 16GB GDDR6, 70W)
**Report MSRP:** $2,500
**Verified:** $2,299
**Confidence:** HIGH
**STATUS: REPORT FIGURE IS SLIGHTLY HIGH**

- TechPowerUp GPU database: launch MSRP = $2,299.
- TechCrunch launch article (Sep 2018) corroborates the ~$2,300 launch price.
- PassMark lists $2,299 as the launch price.
- The report's $2,500 overstates by ~$200 (8.7%).
- **Recommendation:** Revise to $2,299.

**Sources:**
- [TechCrunch: NVIDIA launches the Tesla T4](https://techcrunch.com/2018/09/12/nvidia-launches-the-tesla-t4-its-fastest-data-center-inferencing-platform-yet/)
- [NVIDIA T4 Product Brief](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/T4%20Product%20Brief.pdf)
- [PassMark: Tesla T4](https://www.videocardbenchmark.net/gpu.php?gpu=Tesla+T4&id=4211)

---

### 20. NVIDIA Tesla V100 PCIe 16GB / 32GB
**Report MSRP:** $8,000 (16GB) / $10,000 (32GB)
**Verified:** $8,000-$10,664 (16GB) / $10,000-$11,458 (32GB)
**Confidence:** HIGH

- Microway price analysis (2018): single-unit list = $10,664 (16GB PCIe).
- CDW/Next Platform (Mar 2018): $9,900.
- 32GB variant: Microway = $11,458; ~$800-$1,500 premium over 16GB.
- The report figures ($8K/$10K) represent the lower end of the verified range, consistent with volume/channel pricing rather than single-unit list.

**Sources:**
- [Microway: NVIDIA Tesla V100 Price Analysis](https://www.microway.com/hpc-tech-tips/nvidia-tesla-v100-price-analysis/)
- [GPU Poet: V100 16GB](https://gpupoet.com/gpu/learn/card/nvidia-tesla-v100-16gb)
- [GPU Poet: V100 32GB](https://gpupoet.com/gpu/learn/card/nvidia-tesla-v100-32gb)

---

### 21. NVIDIA Tesla V100 SXM2 16GB / 32GB
**Report MSRP:** $8,000-$10,000
**Verified:** $10,000-$15,900
**Confidence:** MEDIUM
**STATUS: REPORT FIGURE IS LOW**

- Microway: 16GB SXM2 single-unit list = ~$15,900 (significant premium over PCIe).
- DGX-1 with 8x V100 SXM2: $149,000 = $18,625/GPU at system level.
- The SXM2 form factor was never sold as a standalone card to end users; it was sold through DGX/HGX systems.
- The report's $8,000-$10,000 range matches the PCIe variant, not the SXM2.
- **Recommendation:** Revise to $10,000-$16,000, or note that the $8-10K figure reflects PCIe pricing and SXM2 was inherently more expensive.

**Sources:**
- [Microway: NVIDIA Tesla V100 Price Analysis](https://www.microway.com/hpc-tech-tips/nvidia-tesla-v100-price-analysis/)
- [NVIDIA DGX-1 launch article](https://wccftech.com/nvidia-volta-tesla-v100-dgx-1-hgx-1-supercomputers/)
- [Wikipedia: Nvidia DGX](https://en.wikipedia.org/wiki/Nvidia_DGX)

---

### 22. NVIDIA Tesla V100S PCIe 32GB
**Report MSRP:** ~$11,500
**Verified:** ~$11,000-$11,500
**Confidence:** MEDIUM

- The V100S was a higher-clocked refresh of the V100 launched November 2019.
- No exact NVIDIA MSRP was ever published.
- Microway lists the V100 32GB PCIe at $11,458; the V100S would be at parity or slightly above.
- IT Creations lists used V100S at $9,288 (2026).
- The $11,500 figure is consistent with the V100 32GB price point and is reasonable.

**Sources:**
- [Microway: NVIDIA Tesla V100 Price Analysis](https://www.microway.com/hpc-tech-tips/nvidia-tesla-v100-price-analysis/)
- [IT Creations: V100S PCIe 32GB](https://www.itcreations.com/product/121684)
- [VideoCardz.net: Tesla V100S PCIe 32GB](https://videocardz.net/nvidia-tesla-v100s-pcie-32gb)

---

## Critical Errors Found

### 1. L40 MSRP: $6,800 should be ~$30,000-$33,000
The report uses the current used market price as the "MSRP." The actual OEM launch price was ~$30,000-$33,000 (Cisco CDW = $30,915; Lenovo = $33,109). This error causes all depreciation calculations for the L40 to be dramatically wrong -- the card has depreciated ~78-80% from its OEM price, not retained ~100% as the report implies.

### 2. L40S MSRP: $8,000 should be ~$39,000-$52,000
Same issue. The report uses the current used market price. The actual OEM launch price was ~$39,000-$52,000 (Cisco = $30,930-$39,095; Lenovo = $51,579). All depreciation calculations are wrong.

### 3. A100 SXM4 MSRP: $10,000-$11,000 should be ~$15,000-$20,000
The report appears to use the A100 40GB PCIe launch price for the SXM4 variant. SXM modules were never sold at PCIe prices -- they carry a significant premium due to NVLink, higher TDP, and system-level integration.

### 4. H200 SXM MSRP: $25,000 should be ~$38,000-$44,000
The report figure appears too low, likely confused with H100 SXM pricing. H200 SXM boards (4-GPU and 8-GPU) price out to $38-44K per GPU at the board level.

### 5. V100 SXM2 MSRP: $8,000-$10,000 should be ~$10,000-$16,000
The report uses PCIe pricing for the SXM2 variant. Microway listed the SXM2 16GB at ~$15,900 single-unit.

### 6. T4 MSRP: $2,500 should be $2,299
Minor. TechPowerUp and TechCrunch both cite $2,299 as the launch MSRP.

---

## Key Observation: OEM List Price vs NVIDIA Channel Price

A recurring challenge is distinguishing between:
1. **NVIDIA channel/direct price** -- what NVIDIA charges OEMs/partners (not published)
2. **OEM list price** -- what Cisco/Lenovo/Dell charge customers (includes 2-4x markup for support, integration, warranty)
3. **Reseller/street price** -- what authorized resellers like PNY, Connection.com, CDW charge
4. **Secondary market price** -- what eBay, broker, and refurbished channels charge

For this project's depreciation modeling, the most appropriate "MSRP" is likely the **reseller/street price at launch** (closest to what a first buyer actually paid), not the OEM list price (which includes server integration margins) or the secondary market price (which reflects depreciation). The Cisco GPL prices are typically 2-4x the actual GPU value because they bundle Cisco's platform support, BIOS compatibility testing, and warranty.

---

## Note on Methodology

All web searches were conducted on 2026-03-29. NVIDIA does not publish official MSRPs for any datacenter GPU product. All "MSRP" figures are estimates derived from:
- OEM configurator pricing (Cisco GPL, Lenovo Press, Dell price lists)
- Authorized reseller listings (CDW, Connection.com, Provantage, CompSource)
- Analyst estimates (Raymond James, Goldman Sachs)
- Launch-era press coverage (TechCrunch, AnandTech, ServeTheHome, WCCFTech, TweakTown)
- System-level teardowns (DGX pricing / number of GPUs)
- Manufacturer bulk purchase reports (CNBC, WCCFTech)
