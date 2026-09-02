# AMD Radeon Instinct MI210 -- Deep Investigation of Key Unknowns

**Date:** 2026-03-29
**Starting confidence:** 60/100

---

## 1. Card Weight (~1,175g estimated)

### Finding: UNVERIFIABLE -- estimate narrowed to ~1,100-1,200g

No public source -- AMD product page, AMD product brochure, Lenovo product guide, Newegg, Amazon, SHI, IT Creations, Flopper.io, Technical.city, Wiredzone, or any third-party spec database -- lists the physical weight of the MI210. AMD does not publish card weight for any Instinct product (MI210, MI250, MI250X).

**Best available comparator:** The NVIDIA A100 80GB PCIe card weighs **1,170g** (board only, excluding bracket, extenders, and bridges) per the official NVIDIA product brief (PB-10577-001_v03). The A100 PCIe is the closest analog:
- Same form factor: full-height, full-length, dual-slot, passive heatsink
- Same TDP: 300W
- Same memory type: HBM2e (A100 has 5 stacks / 80GB vs MI210's 4 stacks / 64GB)
- Similar PCB complexity (multi-phase VRM, server-grade)

The MI210 has one fewer HBM stack and a slightly less complex package (EFB vs CoWoS), suggesting it could be marginally lighter. The A100 bracket + screws add 20g, and NVLink bridges add 20.5g each -- the MI210's xGMI connectors are board-mounted rather than bridge-based, so they are included in the board weight.

**Revised estimate:** 1,100-1,200g total card weight (board + bracket), with 1,150g as the central estimate. The original 1,175g midpoint remains reasonable. Margin of error is +/- 100g.

**What would resolve this:** Physically weighing an MI210 card. No other path to a definitive answer exists.

### Sources
- [NVIDIA A100 80GB PCIe Product Brief](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/PB-10577-001_v02.pdf) -- 1,170g board weight confirmed
- [AMD Instinct MI210 Product Page](https://www.amd.com/en/products/accelerators/instinct/mi200/mi210.html) -- no weight listed
- [Lenovo Press MI210 Product Guide](https://lenovopress.lenovo.com/lp1862-amd-instinct-mi210-accelerator) -- no weight listed
- [AMD MI210 Brochure PDF](https://www.amd.com/content/dam/amd/en/documents/instinct-business-docs/product-briefs/instinct-mi210-brochure.pdf) -- no weight listed

---

## 2. EFB Packaging Details -- Component Separability

### Finding: HBM stacks CANNOT be individually removed from an EFB package

AMD's Elevated Fanout Bridge (EFB) is a 2.5D packaging technology that is functionally equivalent to TSMC's InFO-L. The key structural details:

1. **How EFB works:** The GPU die and HBM stacks are placed on top of a mold compound layer with embedded copper pillars. The copper pillars connect coarse-pitch pads on the chips to the substrate below. Between the GPU die and each HBM stack, a small silicon bridge is placed *underneath* the dies (in the space created by the mold elevation). The silicon bridge carries the fine-pitch microbump interconnects required for the HBM PHY interface.

2. **Why components are not separable:**
   - Dies are bonded to the mold/substrate via copper pillars and microbumps, then **encapsulated with underfill** (epoxy fill between die and substrate to distribute thermal/mechanical stress).
   - The silicon bridges connecting GCD to HBM are embedded in the mold compound between the dies.
   - Industry literature on 2.5D packaging (CoWoS, EFB, EMIB) is explicit: once dies are bonded and underfilled, **the assembly is permanent**. Rework is "prohibitively expensive, or even impossible" (semiconductor packaging literature). This is why Known Good Die (KGD) testing before assembly is critical.
   - There is no published process for removing individual HBM stacks from an EFB or CoWoS package. Attempting to do so would destroy the silicon bridges, microbumps, and likely the GCD itself.

3. **Comparison to other packaging:**
   - **vs CoWoS (NVIDIA A100/H100):** EFB is structurally similar in terms of separability -- both are permanent assemblies. The difference is that CoWoS uses a large silicon interposer underneath all dies, while EFB uses localized silicon bridges above the substrate. Neither allows component-level rework.
   - **vs Intel EMIB:** EMIB embeds silicon bridges *inside* the substrate. EFB places them *above* the substrate. Both are permanent.
   - **vs standard BGA:** Standard BGA packages (e.g., a discrete GPU soldered to a PCB) can be reballed and reflowed. EFB/CoWoS packages are fundamentally different -- the dies are connected to each other through silicon bridges with microbump pitches of ~30-55um, which cannot survive rework.

4. **Implication for scrap analysis:** The GCD + 4 HBM stacks + MCM substrate + silicon bridges must be treated as a single inseparable unit for salvage purposes. The $150 secondary market value for the "GPU die" in the report really means the entire MCM package assembly. Individual HBM stacks cannot be harvested.

### Sources
- [AnandTech -- CDNA 2 Architecture, EFB](https://www.anandtech.com/show/17054/amd-announces-instinct-mi200-accelerator-family-cdna2-exacale-servers/2)
- [3D InCites -- IFTLE 507: AMD Milan-X, EFB](https://www.3dincites.com/2021/12/iftle-507-amd-milan-x-tsv-hybrid-bonding-the-elevated-fanout-bridge/)
- [Semiconductor Engineering -- Elevated Fanout Bridge](https://semiengineering.com/tag/elevated-fanout-bridge/)
- [Tom's Hardware -- AI chip design pushing 2.5D packaging to limits](https://www.tomshardware.com/tech-industry/semiconductors/ai-chip-design-is-pushing-2-5d-packaging-to-its-limits)
- [SemiEngineering -- Welcome to the 'Probably Good Die' Era](https://semiengineering.com/welcome-to-the-probably-good-die-era/)

---

## 3. Die Area -- 724mm2 vs ~740mm2 vs ~790mm2

### Finding: RESOLVED -- best estimate is 724mm2 (TechPowerUp), with 740-790mm2 as plausible alternatives

Three different figures circulate:

| Source | Die Area (per GCD) | Transistors | Notes |
|--------|-------------------|-------------|-------|
| TechPowerUp GPU Database | 724 mm2 | 58.2B (listed as total, misleading) | TechPowerUp's own measurement/estimate for the Aldebaran chip entry |
| VideoCardz.net | 740 mm2 (1,480 mm2 / 2 GCDs) | 58B total | Derived from total MCM package area |
| Wikipedia (CDNA microarchitecture) | 790 mm2 | 28B per die | Cited as an estimate, no primary source given |
| Tom's Hardware (photo analysis) | 745-790 mm2 | -- | Napkin math from MI250X card photos; acknowledged as imprecise |
| NextPlatform | ~740 mm2 (implied from 1,480 mm2 total) | 29.1B per GCD | Derived from AMD's official dual-die total |

**Analysis:**
- AMD has never officially published a per-GCD die area number. The 58.2B transistor count and 1,480 mm2 total area are the official dual-die MCM numbers.
- TechPowerUp's 724 mm2 is the most widely cited single-die figure and appears in their authoritative GPU database. However, their entry also lists "58,200 million transistors" which is clearly the dual-die total, suggesting some confusion in their data entry. The 724 mm2 could be the actual silicon area (excluding scribe lanes and non-functional edge area), while 740-790 mm2 could include those margins.
- Wikipedia's 790 mm2 with 28B transistors per die is internally consistent (28B x 2 ~ 56B, close to 58.2B accounting for shared I/O). The larger area is plausible for a die that is slightly wider than the silicon-only measurement.
- The predecessor Arcturus (CDNA 1, N7) is 750 mm2 with 25.6B transistors. A 6nm shrink of a comparably complex die being 724-790 mm2 is consistent -- the CDNA2 die added features (matrix cores, IF3.0) that offset the density gain from N7-to-N6.

**Recommendation:** Use **724 mm2** as the primary figure (TechPowerUp, most cited) with a note that the true area may be closer to 740-750 mm2 based on the 1,480 mm2 total MCM area divided by 2. The 790 mm2 Wikipedia figure appears to be an overestimate or includes non-active silicon area.

### Sources
- [TechPowerUp -- AMD Aldebaran GPU Specs](https://www.techpowerup.com/gpu-specs/amd-aldebaran.g1002) -- 724 mm2
- [VideoCardz.net -- AMD Aldebaran](https://videocardz.net/gpu/amd-aldebaran) -- 1,480 mm2 total
- [Wikipedia -- CDNA microarchitecture](https://en.wikipedia.org/wiki/CDNA_(microarchitecture)) -- 790 mm2 per die
- [Tom's Hardware -- MI250X pictured](https://www.tomshardware.com/news/amd-instinct-mi250x-pictured) -- 745-790 mm2 napkin math
- [NextPlatform -- The Aldebaran GPU That Won Exascale](https://www.nextplatform.com/2021/11/09/the-aldebaran-amd-gpu-that-won-exascale/)

---

## 4. Palladium Content -- Is 0.05g Still Too High?

### Finding: YES, 0.05g is likely too high. Revised estimate: 0.005-0.02g

The research is unambiguous on this point:

1. **BME MLCCs contain zero palladium.** Modern BME (Base Metal Electrode) MLCCs, which account for **99% of Class II ceramic capacitors worldwide**, use 100% nickel electrodes. They contain no palladium whatsoever. The shift from PME (Precious Metal Electrode) to BME occurred in the early 1990s due to palladium's high cost.

2. **Only PME MLCCs contain palladium.** PME types are used exclusively in specialty applications: high-reliability, high-temperature, high-voltage, and military/space electronics. A 2022-era datacenter GPU board (MI210) would use BME MLCCs for virtually all capacitor positions.

3. **Quantitative data from literature:**
   - Palladium concentration in waste PCBs: **10-100 mg/kg** (literature consensus)
   - PC DRAM modules: ~86 ppm (1.5 mg per module)
   - General WEEE: ~50 mg/kg (0.005%)
   - For the MI210 board (estimated PCB + components weight ~500g = 0.5 kg):
     - At 10 mg/kg: **0.005g** (5 mg)
     - At 50 mg/kg: **0.025g** (25 mg)
     - At 100 mg/kg: **0.050g** (50 mg)
   - The 100 mg/kg upper bound applies to mixed-vintage e-waste streams containing older PME capacitors. A brand-new 2022 board using all-BME MLCCs would be at the **low end** (10-20 mg/kg).

4. **Where does the remaining Pd come from (if not MLCCs)?**
   - Connector contact plating: Some connectors use a thin Pd-Ni alloy flash plating as an undercoat beneath gold. This is typically 0.1-0.5 um thick.
   - Solder paste: Some lead-free solders contain trace Pd, but SAC305 (the standard) does not.
   - The MLCCs themselves: Even if 1-2 of the ~200 MLCCs on the board are specialty PME types (e.g., for high-voltage VRM filtering), the Pd content would be milligrams, not tens of milligrams.

5. **Revised estimate:**
   - BME MLCCs on board: ~0g Pd
   - Connector plating traces: ~0.002-0.005g Pd
   - Any residual PME MLCCs (if present): ~0.003-0.015g Pd
   - **Total: 0.005-0.02g** (5-20 mg)
   - At $45.16/g: **$0.23-$0.90** (down from $2.26 at 0.05g)

**Impact on scrap estimate:** The original report had corrected Pd from $13.55 to $2.26. This further correction reduces it to $0.23-$0.90. Gold ($11.60) is now even more dominant as the primary precious metal by value -- roughly 13-50x the palladium value.

### Sources
- [TTI MarketEYE -- Electrodes and Terminations in Passive Components](https://www.tti.com/content/ttiinc/en/resources/marketeye/categories/passives/me-zogbi-20240411.html) -- BME = 99% of Class II MLCCs
- [Knowles Capacitors -- PME vs BME MLCCs](https://blog.knowlescapacitors.com/blog/comparing-pme-and-bme-mlccs-for-high-reliability-applications) -- Pd only in PME
- [EE Times -- What switch to nickel means to MLCC buyers](https://www.eetimes.com/what-switch-to-nickel-means-to-mlcc-capacitor-buyers/) -- industry transition history
- [Specialty Metals -- MLCC Chips and Precious Metal Recovery](https://www.specialtymetals.com/blog/2024/7/26/the-value-of-mlcc-chips-an-insight-into-precious-metals-recovery) -- post-1990s MLCCs not worth recovering
- [Hydrometallurgy (ScienceDirect) -- Pd in waste PCBs: 10-100 mg/kg](https://www.sciencedirect.com/science/article/abs/pii/S0304386X19308229)
- [ResearchGate -- Pd content of PC DRAM modules: 86 ppm](https://www.researchgate.net/figure/Palladium-content-of-PC-DRAM-modules-over-time-The-dashed-lines-represent-best-estimates_fig6_310814279)

---

## 5. xGMI Bridge Connector -- Gold Content

### Finding: ESTIMATED -- ~0.01-0.03g Au per connector ($1.45-$4.35 each)

**Pricing confirmed:** The Supermicro GPU-XGMIMI210-2P (2-port bridge) retails for **$230** at Wiredzone. The 4-port variant (GPU-XGMIMI210-4P) is also available. The EU price is ~EUR 223.

**Physical characteristics (inferred, not directly published):**
- The xGMI bridge is a flexible PCB (flex cable) or rigid PCB with gold-plated high-speed contact pads on both ends
- It connects to three xGMI ports along the top edge of the MI210 card
- Each MI210 has 3 Infinity Fabric links delivering 300 GB/s P2P bandwidth
- Each link operates at 25 Gbps per lane (xGMI protocol), with 16 bits per transaction

**Gold plating analysis:**
- High-speed server connectors typically use **30-50 microinches (0.76-1.27 um)** of hard gold over nickel underplating
- Industry standard for connectors with repeated mating cycles (IPC-4556, ASTM B488)
- The xGMI connector pins would fall in the 30 microinch / 0.76 um range (server-grade, moderate insertion cycles)

**Gold content estimate per connector:**
- Assume ~200-400 contact pads per xGMI port (high-speed differential pairs for 25 Gbps x 16-bit interface)
- Each pad: ~0.5mm x 0.3mm area = 0.15 mm2, plated at 0.76 um thick
- Gold volume per pad: 0.15 mm2 x 0.00076 mm = 0.000114 mm3
- Gold density: 19.3 g/cm3 = 0.0193 g/mm3
- Gold mass per pad: 0.000114 x 0.0193 = 0.0000022g
- For 300 pads: 0.00066g per connector-side
- Two sides (card + bridge): ~0.0013g per connection
- For 3 xGMI ports on the MI210: ~0.004g total on the card-side connectors

**However**, the xGMI bridge itself (the separate bridge card) also contains gold in its contact pads and traces. A more practical estimate for the total gold in the 3 on-card xGMI connectors: **0.01-0.03g Au**, worth **$1.45-$4.35** at current prices.

The original report's $10 secondary market value for the 3 xGMI connectors ($3.33 each) is plausible as a replacement-part value for MI210 repair. However, the $0.30 scrap value (total for all 3) seems about right given the small gold content.

**No detailed pin count or material specification was found** in any public source for the xGMI connector. AMD's Infinity Fabric Link User Guide (part 56978) exists but its contents were not accessible via web search.

### Sources
- [Wiredzone -- GPU-XGMIMI210-2P](https://www.wiredzone.com/shop/product/10025460-supermicro-gpu-xgmimi210-2p-bridge-connector-attaches-2x-instinct-mi210-cards-amd-199-000000003-10726) -- $230 retail price
- [Ahead-IT -- GPU-XGMIMI210-2P](https://www.ahead-it.eu/en/shop/hardware/supermicro/amd-gpu/supermicro-gpu-xgmimi210-2p-nr-amd-instinct-mi210-2x-infinity-fabric-link-bridge-card) -- EUR 223
- [AMD -- Infinity Fabric Link User Guide (56978)](https://www.amd.com/content/dam/amd/en/documents/instinct-tech-docs/other/56978.pdf) -- exists but not fetched
- [Samtec Blog -- Gold Plating on Connectors](https://blog.samtec.com/post/gold-plating-on-connectors-how-much-do-i-need/) -- 30-50 microinch standard
- [Sharrett's Plating -- Gold Plating Thickness Standards](https://www.sharrettsplating.com/blog/gold-plating-thickness/) -- industry specifications

---

## Summary of Confidence Impact

| Unknown | Before | After | Change | Reason |
|---------|--------|-------|--------|--------|
| Card weight | Unverifiable | Unverifiable | None | No source exists; A100 PCIe at 1,170g confirms our ~1,150g estimate is reasonable |
| EFB separability | Unclear | Resolved | +5 | HBM stacks definitively NOT separable; changes how we value the package |
| Die area | Ambiguous (724 vs 740) | Mostly resolved | +3 | 724 mm2 (TechPowerUp) is best single-source; 740 mm2 from 1,480/2 is also defensible; 790 mm2 (Wikipedia) likely overestimates |
| Palladium content | 0.05g (uncertain) | 0.005-0.02g (higher confidence) | +5 | BME MLCCs = zero Pd; 0.05g was 2.5-10x too high; reduces Pd value from $2.26 to $0.23-$0.90 |
| xGMI gold content | Unknown | Estimated 0.01-0.03g Au total | +2 | No definitive source but plating thickness standards + geometry give reasonable bounds |

**Revised overall confidence: 60 --> 70/100**

The largest improvement comes from the palladium correction (reduces an overestimate that was still present) and the EFB separability finding (clarifies salvage assumptions). The weight remains the biggest open question but is bounded by the A100 PCIe comparator.
