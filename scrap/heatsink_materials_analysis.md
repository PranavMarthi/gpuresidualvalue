# Heatsink Internal Construction Analysis -- 5 Unknown Datacenter GPUs

**Date:** 2026-03-29
**Purpose:** Determine heatsink internal construction (vapor chamber vs solid aluminum vs heatpipe) for 5 datacenter GPUs with unknown thermal solutions, to refine Cu/Al weight splits and scrap value estimates.

---

## Known Reference Points

| Card | GPU | TDP | Heatsink Type | Evidence |
|------|-----|-----|---------------|----------|
| A40 (GA102, 300W) | GA102-895 | 300W | Copper vapor chamber + Al fins | RTX A6000 Quasarzone/Tom's Hardware investigation (Oct 2023). Sealed copper plates, deionized water, sintered Cu wicking. |
| V100 PCIe (GV100, 250W) | GV100 | 250W | Copper vapor chamber + Al fins | xDevs Titan V teardown; GamersNexus Titan V VRM/teardown. Vapor chamber with copper heatfins confirmed. |
| H100 SXM5 (GH100, 700W) | GH100 | 700W | Solid/VC copper, Ni plated | Tom's Hardware teardown photos (May 2022). ~1.8 kg copper heatsink on SXM module. |

**Key pattern:** NVIDIA uses vapor chambers on datacenter GPUs at 250W+ TDP where the heatsink must spread heat from a concentrated die to a large fin area. Below ~150W, simpler designs are cost-effective.

---

## Card 1: NVIDIA A10 (GA102, 150W, single-slot)

### Investigation

**Search scope:** "NVIDIA A10 heatsink teardown," "A10 thermal solution," "A10 passive cooler construction," PG133 board design, ServeTheHome, eBay product photos, n3rdware cooling adapters, NVIDIA product brief PB-10415-001_v04.

**Findings:**
- No public teardown of the A10 passive heatsink exists. No review site (ServeTheHome, GamersNexus, Tom's Hardware) has removed the heatsink to photograph the internal construction.
- NVIDIA product brief says only "passive cooling" with no mention of vapor chamber or heat pipe technology.
- The A10 is a **single-slot** card at 150W. Single-slot passive heatsinks are severely volume-constrained -- there is physically very little room for a vapor chamber assembly between the GPU die and the fin tips.
- The A40 (same GA102 die, 300W) uses a vapor chamber, but it is **dual-slot** with twice the heatsink volume.
- The A10's board weight is 550g (NVIDIA spec). The heatsink is estimated at 310g total. A vapor chamber adds 40-60g of copper beyond what a flat copper base plate would require; at 150W with forced server airflow, a flat copper base plate is thermally sufficient.
- eBay product photos consistently show a simple extruded aluminum heatsink with a flat base -- no visible heat pipe ends or vapor chamber edges protruding from the fin stack.
- The A10 cooling adapter sold on eBay (for tower case use) references a heatsink that bolts directly to the PCB with four spring screws -- consistent with a simple baseplate design, not the more complex mounting of vapor chamber assemblies.

### Determination

**PROBABLE: Extruded aluminum fins with flat copper base plate (no vapor chamber)**

Confidence: 65/100

**Reasoning:** 150W in a single-slot passive form factor does not thermally justify a vapor chamber. Server airflow at 40-60 CFM through a single-slot fin stack can easily dissipate 150W with a flat copper base plate providing adequate heat spreading from the 628 mm2 die. NVIDIA uses vapor chambers on their 250W+ dual-slot cards (A40, V100 PCIe) where the die-to-fin thermal path is longer and the heat flux density demands phase-change spreading. The A10 is more likely to follow the simpler thermal design used on lower-TDP single-slot cards.

### Material Split (unchanged from current report)

| Material | Weight (g) | Scrap Value |
|----------|-----------|-------------|
| Aluminum fins | 250 | $0.19 |
| Copper base plate | 60 | $0.60 |
| **Total heatsink** | **310** | **$0.79** |

No change required. The current report already describes this as "copper base plate / vapor chamber" with a question mark; the determination is that it is more likely a flat copper base plate without vapor chamber internals.

---

## Card 2: NVIDIA A16 PCIe (4x GA107, 250W, dual-slot)

### Investigation

**Search scope:** "NVIDIA A16 heatsink teardown," "A16 thermal design," "A16 vapor chamber," ServeTheHome A16 launch coverage, NVIDIA product brief PB-10518-001_v02/v03, Lenovo ThinkSystem A16 Product Guide.

**Findings:**
- No public teardown of the A16 heatsink exists. ServeTheHome published quick-look photos of the exterior but did not remove the heatsink.
- NVIDIA product brief (PB-10518-001_v02) states only "passively cooled with a superior thermal design." No mention of vapor chamber, heat pipe, or internal construction.
- The A16 has a **unique thermal challenge**: four independent GA107 dies spread across the PCB, each producing ~62.5W. The heat sources are distributed, not concentrated on a single die.
- Board weight is 1,088g (NVIDIA spec, excl. bracket). Heatsink estimated at 680g.
- With four separate heat sources, a single large vapor chamber would need to be enormous to cover all four die sites. This is physically possible but expensive. More likely, NVIDIA uses either:
  (a) A large aluminum extrusion with four copper base pads (one per GPU), or
  (b) Individual vapor chambers per GPU site (unlikely at 62.5W each).
- At 62.5W per die, each GA107 is well within the range where a flat copper contact pad and forced airflow through aluminum fins is thermally adequate.
- The components.csv previously claimed "vapor-chamber base plates" but this was corrected during review to "internal construction unverified."

### Determination

**PROBABLE: Extruded aluminum heatsink with copper contact pads at each GPU site (no vapor chamber)**

Confidence: 55/100

**Reasoning:** The distributed heat source design (4x ~62.5W dies) makes a single vapor chamber impractical -- it would need to span ~200mm to cover all four GPU sites, and vapor chambers lose effectiveness at very long transport distances. Individual vapor chambers per GPU are possible but cost-prohibitive at 62.5W per die. The most likely design is a large aluminum extrusion (explaining the 680g weight) with small copper contact pads soldered or pressed into the base at each GPU location. The "superior thermal design" language in NVIDIA's product brief likely refers to optimized fin geometry and airflow channeling rather than vapor chamber technology.

### Material Split (revised)

| Material | Weight (g) | Scrap Value |
|----------|-----------|-------------|
| Aluminum extrusion (bulk) | 650 | $0.50 |
| Copper contact pads (4x ~7.5g) | 30 | $0.39 |
| **Total heatsink** | **680** | **$0.89** |

Previous estimate had heatsink as pure aluminum at 680g/$0.53. Adding 30g copper contact pads (relocated from the aluminum mass) changes scrap by +$0.36. Minor impact on total scrap value.

---

## Card 3: NVIDIA L40 (AD102, 300W, dual-slot)

### Investigation

**Search scope:** "NVIDIA L40 heatsink teardown," "L40 vapor chamber," "L40 thermal design," Comino RTX 6000 Ada teardown, water block compatibility (Comino, EKWB, Alphacool), Massed Compute thermal guidelines, NVIDIA product brief, ServeTheHome RTX 6000 Ada review.

**Findings:**
- No public teardown of the L40 passive heatsink exists.
- **Critical finding:** Water block manufacturers (Comino, EKWB, Alphacool) sell a single water block compatible with the RTX 6000 Ada, L40, and L40S. This confirms all three cards share the same or near-identical PCB layout (PG133 Ada family).
- The RTX 6000 Ada (active-cooled workstation variant, 300W) uses a **dual-slot blower cooler with vapor chamber** -- confirmed by Massed Compute FAQ and the Comino "Ultimate Teardown" blog post.
- The previous-generation Quadro RTX 6000 (Turing, 295W) used a vapor chamber (igor's LAB water cooling mod teardown). The Ada-generation RTX 6000 Ada continues this design.
- The RTX A6000 (Ampere, same GA102 as A40, 300W) used a vapor chamber -- confirmed by Quasarzone/Tom's Hardware investigation (Oct 2023).
- NVIDIA's consistent pattern: professional/datacenter GPUs at 300W use vapor chamber base + aluminum fin stack, whether active (workstation) or passive (datacenter). The passive variant simply omits the fan and optimizes fin spacing for high-velocity server airflow.
- The L40's passive heatsink at 300W faces the same thermal design challenge as the A40 (also 300W, also dual-slot, confirmed vapor chamber). The AD102 die area (608 mm2) is comparable to GA102 (628 mm2).

### Determination

**HIGHLY PROBABLE: Copper vapor chamber base + aluminum fin stack**

Confidence: 80/100

**Reasoning:** Three independent lines of evidence converge:
1. The L40 shares its PCB with the RTX 6000 Ada, which uses a vapor chamber in its active cooler.
2. NVIDIA's established pattern is to use vapor chambers on all 300W professional/datacenter GPUs (Quadro RTX 6000, RTX A6000, A40).
3. The thermal challenge (300W from a ~608 mm2 die through a passive dual-slot heatsink) is identical to the A40, which is confirmed to use a vapor chamber.

The passive L40 heatsink almost certainly uses the same vapor chamber base plate as the RTX 6000 Ada's active cooler, with a different fin stack optimized for server airflow rather than blower fan airflow.

### Material Split (revised from current report)

| Material | Weight (g) | Scrap Value |
|----------|-----------|-------------|
| Aluminum fins | 460 | $0.35 |
| Copper vapor chamber | 190 | $2.47 |
| **Total heatsink** | **650** | **$2.82** |

Previous estimate had the heatsink as pure aluminum at 650g/$0.94. Splitting into 460g Al + 190g Cu changes scrap from $0.94 to $2.82 (+$1.88). This is a material correction for the scrap valuation.

---

## Card 4: NVIDIA L40S (AD102, 350W, dual-slot)

### Investigation

**Search scope:** Same as L40 (shared PCB family). "NVIDIA L40S heatsink teardown," "L40S thermal design," water block compatibility, NVIDIA product brief PB-11470-001_v02, Lenovo Press LP1812.

**Findings:**
- No public teardown of the L40S passive heatsink exists.
- The L40S shares its PCB with the L40 and RTX 6000 Ada -- confirmed by Comino water block compatibility (single product SKU for all three cards).
- The L40S has a **higher TDP** (350W vs 300W for L40 and RTX 6000 Ada). If anything, the higher thermal load makes a vapor chamber *more* necessary, not less.
- Board weight is 1,052g (NVIDIA spec, excl. bracket) vs 1,051g for L40 -- essentially identical, suggesting the same or very similar heatsink assembly.
- The L40S report already estimates "primarily aluminum fins with copper vapor chamber base" at ~450g Al + ~100g Cu. This was a good initial estimate but the copper fraction may be understated relative to the L40 analysis.

### Determination

**HIGHLY PROBABLE: Copper vapor chamber base + aluminum fin stack**

Confidence: 85/100

**Reasoning:** Same evidence as L40 (shared PCB, shared water block compatibility with RTX 6000 Ada which uses vapor chamber), plus the higher 350W TDP makes the thermal case even stronger. The near-identical board weight (1,052g vs 1,051g) confirms the L40 and L40S use the same physical heatsink assembly. At 350W, a vapor chamber is essentially mandatory for adequate heat spreading from the AD102 die in a passive dual-slot form factor.

### Material Split (current report already has vapor chamber -- minor adjustment)

| Material | Weight (g) | Scrap Value |
|----------|-----------|-------------|
| Aluminum fins | 370 | $0.28 |
| Copper vapor chamber | 180 | $2.34 |
| **Total heatsink** | **550** | **$2.62** |

Current report estimates 450g Al + 100g Cu = $1.44. Revised to 370g Al + 180g Cu = $2.62 (+$1.18). The copper fraction is increased to be consistent with the L40 analysis and the known vapor chamber construction pattern. The total heatsink weight (550g) remains consistent with the current report.

---

## Card 5: NVIDIA Tesla T4 (TU104, 70W, HHHL, single-slot)

### Investigation

**Search scope:** "NVIDIA Tesla T4 heatsink teardown," "T4 thermal solution," "T4 heat pipe," n3rdware active cooler manual (disassembly steps), NVIDIA product brief PB-09256-001_v05, TechInsights DDT-1908-806 reference, eBay product photos, NVIDIA Developer Forums thermal integration thread, EEVBlog repair thread.

**Findings:**
- **Multiple product listing descriptions mention "copper heat pipes and aluminum fin arrays"** for the T4. This appears in marketing text from NetworkHardwares.com and similar resellers.
- **However, this is likely generic marketing copy**, not sourced from a teardown. No public teardown with photos showing heat pipes inside the T4 stock heatsink has been found.
- The n3rdware disassembly manual shows the stock heatsink removal (four spring screws) and describes the die contact area as having thermal paste -- but does not describe or show heat pipe construction.
- The T4 is a **HHHL (half-height, half-length)** card at only 70W. The heatsink dimensions are approximately 168 x 69 mm (the PCB footprint), severely constrained.
- Total board weight is 301g; heatsink is estimated at 130g. A 130g heatsink in HHHL form factor leaves very little room for heat pipes -- typical small heat pipes weigh 8-15g each and add significant height.
- eBay listing for "NVIDIA TESLA P4 heatsink copper core" exists, suggesting the P4 (predecessor, GP104, 75W, same HHHL form factor) may have a copper core/base insert.
- The T4's 70W TDP from a 545 mm2 die produces a heat flux density of only 0.128 W/mm2 -- very low. For comparison, the A40 at 300W/628mm2 has 0.478 W/mm2. At 0.128 W/mm2, a flat copper contact pad with aluminum fins is more than adequate.
- The TechInsights deep dive teardown (DDT-1908-806) exists but is behind a paywall. This is the only known professional teardown of the T4 PG183 board.

### Determination

**MOST PROBABLE: Extruded aluminum heatsink with copper core insert (no heat pipes, no vapor chamber)**

Confidence: 70/100

**Reasoning:** The T4 at 70W in HHHL form factor has the lowest thermal design challenge of any card in this study. The 130g heatsink weight is consistent with a simple extruded aluminum body with a small copper insert/slug at the die contact point (similar to the P4 "copper core" design referenced on eBay). Heat pipes are unlikely because: (a) the HHHL form factor severely constrains available height for pipe routing, (b) 70W does not require phase-change heat transport, and (c) the heatsink weight (130g) does not leave room for significant copper mass beyond a small contact insert. The "copper heat pipes" mentioned in some product descriptions is almost certainly generic marketing copy reused from higher-end product templates.

### Material Split (revised from current report)

| Material | Weight (g) | Scrap Value |
|----------|-----------|-------------|
| Aluminum extrusion (body) | 115 | $0.09 |
| Copper core insert | 15 | $0.19 |
| **Total heatsink** | **130** | **$0.28** |

Current report lists heatsink as pure aluminum (6063 alloy) at 130g/$0.10 with "no vapor chamber." The addition of a ~15g copper core insert (relocated from the aluminum mass) adds $0.18 in scrap value. Minor impact. The current report's assertion of "no vapor chamber" is confirmed as correct.

---

## Summary Table

| Card | TDP | Form Factor | Heatsink Type (Determination) | Confidence | Cu (g) | Al (g) | Heatsink Scrap |
|------|-----|-------------|-------------------------------|------------|--------|--------|---------------|
| **A10** | 150W | Single-slot FHFL | Al extrusion + Cu base plate (no VC) | 65% | 60 | 250 | $0.79 |
| **A16** | 250W | Dual-slot FHFL | Al extrusion + Cu contact pads (no VC) | 55% | 30 | 650 | $0.89 |
| **L40** | 300W | Dual-slot FHFL | Cu vapor chamber + Al fins | 80% | 190 | 460 | $2.82 |
| **L40S** | 350W | Dual-slot FHFL | Cu vapor chamber + Al fins | 85% | 180 | 370 | $2.62 |
| **T4** | 70W | Single-slot HHHL | Al extrusion + Cu core insert (no VC) | 70% | 15 | 115 | $0.28 |

### Pattern Observed

NVIDIA's vapor chamber usage in datacenter GPUs follows a clear TDP threshold:
- **Below 150W (T4, A10):** Simple aluminum extrusion with copper base/insert. Cost-effective; server airflow handles the thermal load.
- **250W with distributed heat (A16):** Aluminum extrusion with localized copper pads. Vapor chamber impractical across 4 die sites.
- **300W+ with single large die (L40, L40S, A40, V100 PCIe):** Copper vapor chamber base + aluminum fin stack. High heat flux from large die requires phase-change heat spreading.

---

## Impact on Scrap Valuations

| Card | Current Heatsink Scrap | Revised Heatsink Scrap | Delta |
|------|----------------------|----------------------|-------|
| A10 | $0.79 (Al $0.19 + Cu $0.60) | $0.79 (unchanged) | $0.00 |
| A16 | $0.53 (all Al) | $0.89 (Al + Cu pads) | +$0.36 |
| L40 | $0.94 (all Al) | $2.82 (Al + Cu VC) | +$1.88 |
| L40S | $1.44 (Al $0.50 + Cu $0.94) | $2.62 (revised split) | +$1.18 |
| T4 | $0.10 (all Al) | $0.28 (Al + Cu insert) | +$0.18 |

**Total scrap impact across all 5 cards: +$3.60**

The most significant correction is the L40, where the heatsink was previously modeled as pure aluminum. Adding a 190g copper vapor chamber increases heatsink scrap by $1.88 -- a meaningful correction for the scrap model.

---

## Sources

### Confirmed Vapor Chamber References
- [Tom's Hardware -- RTX 3080 / A6000 Vapor Chamber Cracks (Oct 2023)](https://www.tomshardware.com/news/some-rtx-3080-rtx-a6000-gpus-are-prone-to-vapor-chamber-cracks-report)
- [Overclocking.com -- RTX 3080 / A6000 Steam Chamber Oxidation](https://en.overclocking.com/rtx-3080-rtx-a6000-steam-chamber-oxidation/)
- [Massed Compute -- RTX A6000 Ada Vapor Chamber Cooling](https://massedcompute.com/faq-answers/?question=How+does+the+RTX+A6000+ADA+GPU's+vapor+chamber+cooling+system+work?)
- [LTT Forums -- RTX A6000 Disassembly Guide](https://linustechtips.com/topic/1339957-nvidia-rtx-a6000-disassembly-with-small-guide/)
- [igor's LAB -- Quadro RTX 6000 Water Cooled (vapor chamber visible)](https://www.igorslab.de/en/nvidia-quadro-rtx-6000-water-cooled-more-boost-and-performance-through-modification-even-without-manual-overclocking/)

### PCB Sharing Evidence (L40/L40S/RTX 6000 Ada)
- [Comino GPU Waterblock for RTX 6000 Ada / L40 / L40S](https://www.comino.com/products/gpu-waterblock-for-nvidia-rtxtm-6000-ada-l40-l40s)
- [Comino GPU WCB blog post -- RTX 6000 Ada / L40 / L40S shared PCB](https://www.comino.com/blog/comino-gpu-wcb-for-nvidia-rtx6000-ada-l40-and-l40s-cu-steel)
- [Comino "Ultimate Teardown" -- RTX 6000 Ada](https://www.comino.com/blog/ultimate-teardown-dissecting-cutting-edge-rtx-6000-ada-comino-rtx-6000-ada-waterblock-teaser)
- [EKWB -- L40S Water Block Compatibility](https://www.ekwb.com/configurator/step1_complist?gpu_gpus=5937)

### T4 Thermal Design
- [NVIDIA Developer Forums -- T4 Thermal Integration](https://forums.developer.nvidia.com/t/t4-thermal-integration/75470)
- [n3rdware -- Tesla T4/P4 Active Cooler Manual (disassembly steps)](https://n3rdware.com/knowledge-base/manuals/tesla-t4-p4-active-cooler)
- [TechInsights -- Deep Dive Teardown Tesla T4 PG183 (paywalled)](https://www.techinsights.com/products/ddt-1908-806)
- [NVIDIA T4 Product Brief PB-09256-001_v05](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-t4/t4-tensor-core-product-brief.pdf)

### A10 and A16 Product Briefs
- [NVIDIA A10 Product Brief PB-10415-001_v04](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a10/pdf/A10-Product-Brief.pdf)
- [NVIDIA A16 Datasheet](https://images.nvidia.com/content/Solutions/data-center/vgpu-a16-datasheet.pdf)
- [Lenovo Press -- ThinkSystem A10](https://lenovopress.lenovo.com/lp1816-thinksystem-nvidia-a10-24gb-pcie-gen4-passive-gpu)
- [Lenovo Press -- ThinkSystem A16](https://lenovopress.lenovo.com/lp1815-thinksystem-nvidia-a16-64gb-gen4-pcie-passive-gpu)

### L40 / L40S Product Briefs
- [NVIDIA L40 Product Brief](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/datasheets/L-40/product-brief-L40.pdf)
- [NVIDIA L40S Product Brief PB-11470-001_v02](https://www.pny.com/File%20Library/Company/Support/product-briefs/data-center-gpus/NVIDIA-L40S-Product-Brief.pdf)
- [Massed Compute -- L40/L40S Thermal Design Guidelines](https://massedcompute.com/faq-answers/?question=What+are+the+thermal+design+guidelines+for+NVIDIA+L40+and+L40S+GPUs)

### General Thermal Design
- [Radian -- Vapor Chamber Heatsink Technology](https://radianheatsinks.com/vapor-chamber-heatsink/)
- [ServeTheHome -- RTX 6000 Ada Review](https://www.servethehome.com/nvidia-rtx-6000-ada-graphics-card-review-pny/)
- [Akasa -- 600-1000W Vapor Chamber Module for RTX 5090/RTX PRO 6000](https://videocardz.com/newz/akasa-prepares-600-1000w-vapor-chamber-cooler-module-for-rtx-5090-and-rtx-pro-6000)
