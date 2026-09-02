# Intel Gaudi2 HL-225H -- Scrap & Salvage Value Analysis

**Date:** 2026-03-29
**Form Factor:** OAM (OCP Accelerator Module v1.1)
**TDP:** 600W
**MSRP:** $8,125 (per card, from $65K 8-card UBB kit) | **Used (Mar 2026):** $1,999-$2,188

---

## 1. Card Overview

The Intel Gaudi2 HL-225H is a purpose-built AI training accelerator designed by Habana Labs (acquired by Intel). It uses the HL-2080 ASIC on TSMC 7nm with 24 integrated 100GbE RoCE v2 RDMA ports, targeting large-scale distributed training workloads in the OAM mezzanine form factor.

| Attribute | Value |
|-----------|-------|
| GPU die | HL-2080 (TSMC 7nm) |
| Die area | ~800 mm2 (Habana COO: "roughly the same die size" as A100 826 mm2) |
| Transistors | Not disclosed |
| Memory | 96 GB HBM2e (6 x 16 GB stacks, 8-Hi TSV) |
| Memory bus | 6 x 1024-bit = 6144-bit |
| Interconnect | 24x 100GbE RoCE v2 RDMA (on-die); PCIe Gen 4.0 x16 host |
| TDP | 600 W |
| Board weight | ~800-900 g estimated (no published weight) |
| Packaging | 2.5D with silicon interposer (TSMC advanced packaging; CoWoS confirmed for Gaudi1, assumed for Gaudi2) |

---

## 2. Weight Breakdown

| Component | Weight (g) | % of Total |
|-----------|-----------|-----------|
| Heatsink (aluminum or copper) | 350 | 41% |
| PCB (OAM, 102 x 165 mm) | 85 | 10% |
| VRM (DrMOS + inductors + caps) | 77 | 9% |
| GPU die + package substrate + interposer | 100 | 12% |
| Memory (6 x HBM2e stacks) | 27 | 3% |
| Connectors (2x mezzanine) + stiffeners | 137 | 16% |
| Other (solder, TIM, passives, hardware) | 74 | 9% |
| **Total** | **~850** | **100%** |

---

## 3. Component Breakdown

### GPU Die
- HL-2080, ~800 mm2 (Habana COO Eitan Medina at Intel Vision 2022: "roughly the same die size" as NVIDIA A100 at 826 mm2), TSMC 7nm
- 24 Tensor Processor Cores, 2x MME, 48 MB on-die SRAM, integrated media engine (HEVC/H.264/VP9/JPEG decode)
- Secondary market: $800 (functional ASIC for Habana/Intel ecosystem)
- Raw scrap: $6.34 (gold in ENEPIG pad plating ~0.04g Au at $144/g = $5.76; silicon negligible). Gaudi2 uses flip-chip 2.5D packaging, not wire bonds.

### Memory
- 6 x 16 GB HBM2e stacks (8-Hi TSV), 96 GB total, 2.45 TB/s aggregate bandwidth
- Samsung Flashbolt or SK Hynix (vendor not publicly confirmed)
- Secondary market: $900 total ($150/stack, HBM2e legacy market)
- Raw scrap: $4.20 (Au/Cu/Sn in TSVs and micro-bumps, ~$0.70/stack)

### Heatsink
- OAM module heatsink (aluminum fin-stack or vapor chamber)
- 350g (~41% of card)
- Secondary market: $8 (replacement heatsink for OAM systems)
- Raw scrap: $3.50 (Al at ~$0.45/lb or Cu at ~$2.70/lb depending on construction)

### VRM / Power Delivery
- Multi-phase buck converter for 600W TDP (12V and 48V input per OAM spec)
- DrMOS ICs, 12 ferrite-core inductors, MLCC capacitors, PWM controller
- Secondary market: $15 (functional VRM components) + $12 (inductors at ~$1 each)
- Raw scrap: $2.95 (copper in inductors ~1.2g Cu each, tin in solder)

### PCB
- Multi-layer FR-4, 102 mm x 165 mm (OAM v1.1)
- Cu content ~15g in traces
- Secondary market: none (no standalone resale for OAM PCB)
- Raw scrap: $4.38 (Cu traces + Au on mezzanine connector pads ~0.03g)

### Connectors
- 2x Molex Mirror Mezz (56Gbps, OAM v1.1; part 209311-1115; not "Pro" variant)
- Bottom-mount, high-speed differential pair connectors
- Secondary market: $10 (spare parts for OAM baseboard repair)
- Raw scrap: $1.76 (copper alloy + gold-plated contacts ~0.02g Au per connector)

### Other
- TIM (indium-based, ~0.5g In): $0.31 scrap (In at $0.62/g SMM industrial benchmark; corrected from $0.10 which used stale ~$0.20/g price)
- Tantalum capacitors (8x, 6.4g total): $0.35 scrap
- MLCC capacitors (120x, modern Ni-electrode): $0.90 scrap
- Misc ICs (EEPROM, temp sensors, BMC interface): $0.35 scrap
- Stiffeners, mounting hardware (stainless steel): $0.29 scrap
- Package substrate (ABF, Cu RDL): $1.20 scrap
- Solder + PCIe edge traces: $0.13 scrap

---

## 4. Precious Metals

| Metal | Est. Mass (g) | Price/g (Mar 2026) | Gross Value | Notes |
|-------|-------------|-------------------|-------------|-------|
| Gold (Au) | 0.12 | $144/g | $17.28 | ENEPIG pad finish (0.04g), PCB pads (0.03g), OAM connector plating (0.04g), PCIe fingers (0.005g). No wire bonds — Gaudi2 uses flip-chip CoWoS 2.5D packaging. |
| Silver (Ag) | trace | $2.27/g | <$0.10 | Minimal; modern Ni-electrode MLCCs |
| Palladium (Pd) | trace | $45/g | <$0.10 | Minimal in modern MLCCs |
| **Total** | | | **~$17.28** | |

---

## 5. Value Cascade

| Scenario | Value | % of MSRP |
|----------|-------|-----------|
| Working unit (used, Mar 2026) | $2,000 | 24.6% |
| Component salvage (theoretical max) | $1,745 | 21.5% |
| Component salvage (realistic) | $50-80 | 0.6-1.0% |
| Raw material scrap (gross) | $28.22 | 0.35% |
| Recycler payout (net, what you'd receive) | $11-$17 | 0.14-0.21% |

---

## 6. Verification Issues & Corrections

Issues identified during peer review (from verify_components.md and verify_prices.md):

### Component Issues
- **Connector naming (WRONG, corrected):** components.csv originally labelled the mezzanine connectors as "Molex Mirror Mezz Pro" but the correct name for OAM v1.1 is "Molex Mirror Mezz" (original, 56Gbps, part 209311-1115). The "Pro" variant (112Gbps) was introduced for OAM v1.5. Corrected in components.csv. Does not affect scrap value estimate. Severity: LOW.
- **Die size ~500mm2 (WRONG, corrected to ~800mm2):** Habana COO Eitan Medina stated at Intel Vision 2022 that Gaudi2 is "implemented in the same process node and roughly the same die size" as the NVIDIA A100 (826 mm2 on TSMC 7nm). The original ~500mm2 estimate was ~40% too low. Corrected to ~800mm2. Sources: [EE News Europe](https://www.eenewseurope.com/en/intel-takes-on-nvidia-graphcore-with-gaudi2-ai-chip/), [TechInsights](https://www.techinsights.com/blog/habana-gaudi2-triples-performance). VideoCardz leaked package photo also shows visually larger die than 500mm2 would imply. Does not affect scrap valuation. Confidence: 60/100 (COO statement, not measured). Severity: LOW.
- **Component weights (UNCERTAIN):** No published weight data for the HL-225H. All weights are engineering estimates based on OAM form factor dimensions and comparable modules. Confidence: 30-40/100. Severity: LOW.
- **HBM2e vendor (UNCERTAIN):** Samsung Flashbolt vs SK Hynix not publicly confirmed. Severity: NEGLIGIBLE.

### Pricing Issues
- **Gold price overstated (WRONG):** Document claimed $148/g ($4,565/oz) but multiple sources show $143-145/g ($4,427-$4,509/oz) for late March 2026. Corrected to $144/g. Impact: -$0.48 on total gold value. Severity: LOW.
- **Tantalum line item math error (WRONG):** components.csv states $1.50 scrap for 8 tantalum caps (6.4g = 0.014 lb) at $20-25/lb, but 0.014 lb x $25/lb = $0.35, not $1.50. The $1.50 figure would require ~$107/lb. Corrected to $0.35. Impact: -$1.15 on total scrap. Severity: MEDIUM.
- **Copper scrap price (UNCERTAIN):** The $5.90/lb figure used for copper appears to reference commodity futures rather than actual scrap buyback rates. Severity: LOW (small total Cu quantity).
- **Indium price understated [CORRECTED]:** Original used ~$0.20/g ($0.10 for 0.5g). SMM China 4N+ benchmark is $0.62/g ($618/kg) as of Mar 2026. Corrected to $0.31. Impact: +$0.21. See indium_price_analysis.md.

### Web Verification (2026-03-29)
Seven claims checked against public sources:

1. **Gaudi2 ASIC -- TSMC 7nm, die size:** CORRECTED. ~500mm2 was wrong. Habana COO stated "roughly the same die size" as A100 (826mm2). Updated to ~800mm2. No public teardown or die shot with measurements exists.
2. **6x 16GB HBM2e = 96GB:** CONFIRMED. Official datasheets, Intel white paper, VideoCardz package photo all consistent. 2.45 TB/s bandwidth confirmed.
3. **24x 100GbE integrated on-die:** CONFIRMED. Habana architecture docs and Intel white paper explicitly state "native integration on-chip of 24 x 100 Gbps RoCE V2 RDMA NICs." No separate NIC component.
4. **OAM v1.1, Molex Mirror Mezz (not Pro):** CONFIRMED. OAM v1.1 spec uses Molex Mirror Mezz 209311-1115 (56Gbps). Mirror Mezz Pro (112Gbps) is OAM v1.5. components.csv corrected.
5. **600W TDP:** CONFIRMED. Official HL-225H datasheet. Real-world stress tests show 530-560W at extreme load.
6. **CoWoS 2.5D packaging:** PARTIALLY CONFIRMED. Gaudi1 explicitly used TSMC CoWoS (WikiChip). Gaudi2 described as using "TSMC's advanced packaging technology" (Electronic Design) but no source explicitly names "CoWoS" for Gaudi2. Likely the same platform given TSMC fab continuity and HBM integration method. Qualified in report.
7. **Media processing engine -- integrated on-die:** CONFIRMED. Intel fact sheet: "integration of on-chip media processing engine." Supports HEVC, H.264, VP9, JPEG decode and pre-processing.

### Confidence Assessment
- Component accuracy: 80/100 (improved from 78; die size and connector corrected)
- Pricing accuracy: 68/100
- Overall confidence in scrap estimate: 74/100

---

## 7. Key Observations

1. **Scrap value is negligible relative to functional value.** At ~$28 corrected raw material scrap, the scrap value is 0.35% of MSRP and 1.4% of secondary market value (~$2,000). A functional card is worth ~71x its scrap value.
2. **2.5D packaging kills component salvage.** The ASIC and 6 HBM2e stacks are integrated on a shared silicon interposer (TSMC advanced packaging, likely CoWoS). Non-destructive separation is effectively impossible with standard e-waste processing, making the theoretical $1,745 component salvage unrealizable in practice.
3. **Gold dominates scrap value.** Despite containing only ~0.12g of gold, it accounts for ~61% of the total raw material scrap value at $144/g (March 2026). This is typical for modern electronics scrap.
4. **Ecosystem risk depresses secondary market.** Unlike NVIDIA GPUs with broad software support, the Gaudi2 depends on Intel's SynapseAI stack. Intel's strategic direction away from Gaudi accelerators further depresses the secondary market, with prices falling 73-76% from MSRP in under 2 years.
5. **Networking has zero separable value.** The 24x 100GbE RoCE v2 ports are fully integrated on-die -- there is no separate NIC chip or transceiver to salvage.

---

## 8. Methodology & Sources

### GPU Specifications
- [Habana Gaudi2 HL-225H Datasheet](https://habana.ai/wp-content/uploads/2023/10/HL-225H_Datasheet_10_23.pdf) -- official specs, 600W TDP, 96GB HBM2e, OAM v1.1 form factor
- [Intel Content -- HL-225H Datasheet](https://www.intel.com/content/www/us/en/content-details/784779/habana-gaudi-2-mezzanine-card-datasheet-hl-225h.html) -- Intel-hosted version with additional integration details
- [Habana Gaudi2 Product Page](https://habana.ai/products/gaudi2/) -- product overview, 24x 100GbE RoCE v2 RDMA
- [ServeTheHome Gaudi2 Launch](https://www.servethehome.com/intel-habana-gaudi2-launched-ai-training-chip-supermicro-ddn-oam/) -- launch details, MSRP ($65K / 8 cards = $8,125), Supermicro/DDN integration
- [Tom's Hardware Gaudi2 vs A100](https://www.tomshardware.com/news/intel-habana-gaudi2-outperforms-nvidia-a100) -- performance context, competitive positioning
- [EE News Europe -- Gaudi2 launch](https://www.eenewseurope.com/en/intel-takes-on-nvidia-graphcore-with-gaudi2-ai-chip/) -- COO Eitan Medina quote: "roughly the same die size" as A100
- [TechInsights -- Gaudi2 Triples Performance](https://www.techinsights.com/blog/habana-gaudi2-triples-performance) -- confirms die size comparison to A100
- [VideoCardz -- HL-2080 pictured](https://videocardz.com/newz/intel-habana-gaudi-hl-2080-ai-training-processor-pictured-features-6-stacks-of-high-bandwidth-memory) -- leaked package photo showing 6 HBM stacks
- [Habana -- Scaling with integrated RoCE](https://habana.ai/gaudi-integrated-roce/) -- confirms 24x 100GbE on-die integration
- [Habana Gaudi Architecture docs](https://docs.habana.ai/en/latest/Gaudi_Overview/Gaudi_Architecture.html) -- architecture reference
- [WikiChip -- Gaudi/CoWoS](https://en.wikichip.org/wiki/habana/microarchitectures/gaudi) -- confirms Gaudi1 used TSMC CoWoS
- [OAM v1.1 Design Spec](https://www.opencompute.org/documents/ocp-accelerator-module-design-specification-v1p1-1-pdf) -- confirms Molex Mirror Mezz 209311-1115
- [Molex Mirror Mezz Pro -- OAM v1.5](https://www.molex.com/en-us/blog/mirror-mezz-pro-connector-selected-for-open-compute-project) -- confirms Pro variant is v1.5 only
- Board weight: No published weight; estimated ~800-900g based on OAM v1.1 form factor dimensions and comparable OAM modules (NVIDIA A100/H100 OAM ~0.8-1.2 kg)
- Precious metal quantities: Conservative estimates based on industry teardown data for comparable datacenter accelerators and published gold content ranges for modern BGA/flip-chip packages. Total gold (0.12g) is internally consistent across component-level estimates.
- Recovery rates: Recycler payout estimated at 40-50% of gross precious metal value, based on industry norms for e-waste processing.

### Precious Metal Spot Prices (Mar 26--29, 2026)
- **Gold:** $4,509/oz ($144.96/g) -- [JM Bullion](https://www.jmbullion.com/charts/gold-price/) | [Fortune](https://fortune.com/article/current-price-of-gold-03-27-2026/)
- **Silver:** ~$70/oz ($2.25/g) -- [JM Bullion](https://www.jmbullion.com/charts/silver-prices/) | [Fortune](https://fortune.com/article/current-price-of-silver-3-26-2026/)
- **Palladium:** $1,405/oz ($45.16/g) -- [APMEX](https://www.apmex.com/palladium-price) | [JM Bullion](https://www.jmbullion.com/charts/palladium-price/)

### Scrap & Base Metal Prices
- **Copper:** $12,050/tonne -- [Trading Economics](https://tradingeconomics.com/commodity/copper)
- **Copper scrap (bare bright):** ~$5.90/lb -- [iScrapApp](https://iscrapapp.com/metals/bare-bright-copper/) | [Rockaway Recycling](https://rockawayrecycling.com/metal/1-bare-bright-wire/)
- **Scrap weekly report:** [ScrapMonster](https://www.scrapmonster.com/news/weekly-metal-price-report/scrap-metal-prices-weekly-market-report-march-20-26-2026-2026-3-27/98785) -- March 20--26 weekly market report; bulk e-scrap rate ~$7/lb
- **PCB scrap rates:** [boardsort.com](https://boardsort.com) | [iScrapApp](https://iscrapapp.com/metals/pc-boards/)

### Secondary Market
- eBay sold listings ($1,999-$2,188, Dec 2025-Feb 2026)
- Active listings trending $2,000-$2,700 in March 2026

---

## 10. Scrap Value Scenarios

### 10.1 Theoretical Maximum (Best Case)

Assumes every component is perfectly extracted and sold to the highest-value buyer globally.

| Component | Ceiling Value | Notes |
|-----------|--------------|-------|
| HL-2080 die | $800 | Functional ASIC for Habana/Intel ecosystem; Shenzhen gray-market only. Not subject to NVIDIA export controls, so gray-market demand is weaker than for H100/A100 dies. |
| HBM2e stacks (6x) | **$0** | 2.5D CoWoS-class interposer with capillary underfill + microbumps. No commercial rework service exists. No secondary market for individual HBM stacks (zero listings found on any marketplace or broker). Per hbm_secondary_market.md: "realistic standalone value: $0." |
| Heatsink (Al or Cu) | $8 | Replacement heatsink for OAM systems; or ~$3.50 as raw scrap |
| VRM components | $27 | $15 DrMOS + $12 inductors; labor cost exceeds value in US |
| Connectors (2x Mirror Mezz) | $10 | Spare parts for OAM baseboard repair; thin buyer pool |
| PCB | $0 | No standalone resale for OAM PCB |
| **Total** | **~$845** | Requires Shenzhen-class buyers and physically impossible HBM extraction |

The $1,745 theoretical max in Section 5 includes $900 for HBM2e stacks. These have $0 separable value -- the stacks sit on a shared silicon interposer bonded with capillary underfill and 40um-pitch microbumps. Even the Shenzhen repair shops that service NVIDIA GPUs have no documented capability for Gaudi2-specific rework, and the Habana ecosystem's small installed base makes donor-card demand negligible.

### 10.2 Realistic US Scrap Value (Grounded Estimate)

What a US datacenter operator actually receives for a dead Gaudi2:

**Option A -- Sell dead card to ITAD broker:** At 10-25% of used working price ($2,000), expect **$200-$500**. The Gaudi2's collapsing ecosystem (Intel strategic pivot away from Gaudi) severely limits the buyer pool. Expect the low end; some brokers may decline entirely.

**Option B -- E-waste recycler by weight:** Module weighs ~850g (~1.87 lb). At $5-15/lb server PCB rate: $9-$28 base. PM assay credit at 60-70% recovery on ~$17.28 gross precious metals (dominated by 0.12g Au) adds ~$10-$12. Total: **$19-$40**.

Component harvesting is not viable in the US. The 2.5D packaging makes HBM2e and die recovery impossible without TSMC-class equipment, and Intel/Habana-specific components have no repair demand outside the shrinking Gaudi user base.

**Realistic range: $200-$500** (broker) or **$19-$40** (recycler). The Gaudi2 is unusual in that Option B (recycler) may yield comparable or better value than Option A if no broker will take it.
