# HBM Secondary Market Reality Check

**Date:** 2026-03-29
**Question:** Are HBM stacks actually recoverable from a dead GPU, and if so, what are they worth?

---

## Executive Summary

**The HBM secondary market values used in the component reports ($100-$650/stack) are largely theoretical.** There is no established, visible secondary market for individual HBM stacks. The values are defensible as theoretical ceilings -- what a stack *would* be worth if it could be extracted, tested, and reused -- but the practical barriers to extraction are severe, and the buyer pool is essentially zero outside of a single niche use case: Shenzhen gray-market GPU repair shops.

---

## 1. Can You Buy an Individual HBM Stack?

### Answer: Effectively no.

**eBay / AliExpress / consumer marketplaces:** Zero listings found for HBM, HBM2, HBM2e, HBM3, or HBM3e memory stacks as standalone components. Not a single result across multiple search queries.

**Semiconductor brokers (Rochester Electronics, Quest Components, Smith & Associates, Microchip USA):**
- Rochester Electronics stocks 15 billion devices across 200,000+ part numbers, including extensive memory inventory. No evidence of HBM stacks in their catalog.
- Smith & Associates tracks HBM/DDR5/NAND market intelligence but appears to deal in HBM only at the system/module level, not individual stacks.
- Microchip USA (independent distributor) claims capability to source "specialty HBM memory" but this likely refers to complete modules or packaged parts, not bare KGD stacks.
- No broker was found publicly listing HBM stacks as a stocked or sourceable line item.

**Why there is no market:**
1. HBM stacks are sold exclusively B2B by three manufacturers (SK Hynix 62% share, Micron 21%, Samsung 17%) under pre-negotiated volume contracts. All supply is sold out through 2026.
2. HBM stacks are not standalone products -- they are designed to be permanently bonded to silicon interposers via microbumps at 40um pitch. They cannot be socketed or plugged in.
3. There is no standardized form factor or test interface for a "loose" HBM stack. Testing a removed stack requires the exact interposer/PHY it was designed for.
4. New HBM3e stacks cost ~$350-$420 each (2026 pricing, with ~20% YoY increase); HBM4 stacks are projected at ~$500+. These prices are for new, tested, guaranteed parts sold to NVIDIA/AMD in million-unit volumes.

---

## 2. Can HBM Stacks Be Desoldered from CoWoS Packages?

### Answer: Theoretically possible; practically destructive in almost all cases.

**The physical challenge:**
- HBM stacks are bonded to the silicon interposer via **microbumps at 40um pitch** (20-25um bump diameter, 15um spacing). Each stack has **over 1,000 I/O connections**.
- After bonding, the gap between the HBM stack and interposer is filled with **capillary underfill epoxy** -- a permanent encapsulant designed to survive thermal cycling and mechanical stress.
- The underfill + microbump combination is explicitly described in semiconductor packaging literature as a **permanent assembly**. Industry sources state rework is "prohibitively expensive, or even impossible."

**Underfill removal techniques (from BEST Inc., Semiconductor Equipment Corp., industry literature):**
1. **Thermal removal:** Heat substrate above underfill softening point (~200-240C), mechanically pry component. Risk: thermal damage to adjacent dies and interposer.
2. **Chemical softening:** Immerse in organic solvents to dissolve cured underfill. Risk: unknown chemical impact on other components; extremely slow for sub-25um gaps.
3. **Laser ablation:** Selectively ablate underfill, solder, and component material with tuned laser wavelengths. Risk: depth control at micron scale is extremely difficult; collateral damage to interposer traces.
4. **Precision cold milling:** High-speed mill removes component body to within thousandths of an inch from substrate. Risk: destroys the component being removed (this is a *removal* technique, not a *recovery* technique).
5. **"Reworkable" underfill adhesives:** Newer formulations decompose at 210-220C, enabling component removal with torque. However, CoWoS packages use **non-reworkable** capillary underfill for reliability reasons. These reworkable adhesives are not used in production CoWoS.

**The microbump problem:**
Even if underfill is successfully removed, the 40um-pitch microbumps present a separate challenge. At this scale:
- Solder volume is ~1,000x smaller than standard BGA balls
- Intermetallic compound (IMC) formation can bridge entire joints
- Thermal cycling during removal causes void formation unique to microbumps
- Realignment for rebonding requires sub-micron accuracy
- Standard BGA rework stations (even advanced infrared/laser models) are not designed for this pitch

**Conclusion:** Desoldering an HBM stack from a CoWoS interposer without destroying it is at the extreme edge of what is physically possible. Even if the stack survives removal, it cannot be retested without bonding it to another interposer -- which requires the same CoWoS-class equipment that makes the original package.

---

## 3. CoWoS Rework: Does Anyone Offer This Service?

### Answer: No commercial rework service exists for CoWoS component recovery.

**TSMC:** Does not offer CoWoS rework or component recovery services. TSMC's CoWoS lines are fully booked for new production (75,000-80,000 wafers/month scaling to 120,000-130,000 by end of 2026). There is zero economic incentive to use this capacity for rework.

**OSATs (ASE, Amkor, etc.):** OSATs are described by analysts as "not inclined to offer such services" for CoWoS due to the huge investment required and the risk that "a failure with multi-chiplet packaging renders several chiplets useless." Analysts are "skeptical about OSATs' penetration in CoW, as more front/backend process crossover raises execution risks." Even for *new assembly*, OSATs struggle with CoWoS yields. Rework is not on their roadmap.

**Shenzhen gray-market shops:** This is the only documented case of anything resembling CoWoS-level HBM rework (see Section 5 below). However, these shops do not offer component recovery as a standalone service -- they repair complete GPU cards.

**Academic/research labs:** The IEEE literature search found no published papers on successful CoWoS component recovery or HBM stack rework. The topic appears only as a "stretch goal" in research roadmaps. The CHIPS NAPMP initiative lists "rework of hybrid bonding" and "high-cost die/stack replacement" as future research objectives -- confirming these capabilities do not exist today.

---

## 4. What About EFB (AMD) and EMIB (Intel) Packages?

All 2.5D packaging technologies share the same fundamental limitation:

| Technology | Used By | Separability | Rework Status |
|---|---|---|---|
| CoWoS-S | NVIDIA A100, H100, H200 | NOT separable | No rework capability |
| CoWoS-L | NVIDIA B100/B200 | NOT separable | No rework capability |
| EFB (Elevated Fanout Bridge) | AMD MI200, MI210 | NOT separable | No rework capability |
| EMIB | Intel (various) | NOT separable | No rework capability |

The MI210 deep investigation (in this repo) confirmed: "There is no published process for removing individual HBM stacks from an EFB or CoWoS package. Attempting to do so would destroy the silicon bridges, microbumps, and likely the GCD itself."

---

## 5. The Shenzhen Exception: Gray-Market GPU Repair

### What is actually happening:

A dozen+ workshops in Shenzhen are repairing A100 and H100 GPUs at a rate of up to **500 units/month**, charging $1,400-$2,800 per card (10% of original value). Repair types include:

- **Common:** Fan replacement, thermal paste refresh, connector pin repair, passive component (cap/resistor/MOSFET) replacement, solder reflow
- **Advanced:** PCB-level fault diagnosis, power delivery subsystem repair, GPU package resolder
- **Claimed but unverified in detail:** "HBM replacement" and "solder-reflow work to HBM replacement"

### Critical analysis of "HBM replacement" claims:

The Tom's Hardware / Reuters reporting from mid-2025 describes repair work "ranging from solder-reflow work to HBM replacement." However, there are important caveats:

1. **"HBM replacement" likely means replacing the entire CoWoS package assembly** (GPU die + interposer + all HBM stacks as a unit), not surgically removing and replacing a single HBM stack. This is analogous to "engine replacement" in auto repair -- you swap the whole engine, not a single piston.

2. **Where do replacement CoWoS assemblies come from?** Likely from donor cards -- GPUs with board-level failures (dead VRMs, damaged connectors, cracked PCBs) whose CoWoS package is still functional. The package is removed from the donor board and reflowed onto the patient board. This is advanced BGA rework, not microbump-level die surgery.

3. **No shop has been documented performing individual HBM stack replacement** on a live CoWoS interposer. The microbump pitch (40um) and underfill make this essentially impossible with BGA rework stations, even advanced infrared/laser models.

4. **Testing infrastructure:** One shop has 256 servers for validation testing. This confirms they are testing complete cards, not individual HBM stacks.

### What repairs are NOT possible:
- Die cracking (especially under liquid cooling)
- Interposer delamination
- Individual HBM stack-level replacement within a bonded CoWoS package

---

## 6. Semiconductor Broker Inventory Check

| Broker | HBM Stock? | Notes |
|---|---|---|
| Rochester Electronics | No evidence | Stocks 15B+ devices, 200K+ part numbers; extensive memory portfolio but no HBM listings found |
| Quest Components | No evidence | Large distributor inventory; no HBM-specific listings |
| Smith & Associates | Tracks HBM market | $12.9B revenue since 2019; covers DDR5/HBM/NAND market intelligence but appears to deal in modules, not bare stacks |
| Microchip USA | Claims capability | Independent distributor; claims to source "specialty HBM memory" but likely refers to modules/cards, not bare KGD stacks |

**No semiconductor broker was found publicly listing individual HBM stacks for sale.**

---

## 7. Academic Literature on HBM/2.5D Rework

**IEEE Xplore search results:** Zero papers found specifically addressing HBM stack rework or recovery from 2.5D packages.

**Related findings:**
- **FormFactor (2024):** Published on Known Good Die test methodology for HBM -- the industry focus is entirely on *preventing* defective stacks from entering packages, not on recovering stacks from failed packages.
- **IEEE EPS Test Committee:** Published "Heterogeneous Integrated Product Testability" guidelines. Rework is explicitly excluded from the test flow: the assumption is that a failed CoWoS package is scrapped entirely.
- **CHIPS NAPMP roadmap:** Lists "rework of hybrid bonding" and "high-cost die/stack replacement" as **stretch goals** for future R&D. The fact that this is a *future research objective* confirms the capability does not exist in production today.
- **Semiconductor Engineering (SemiEngineering):** States that for 2.5D/3D integration, "(no rework)" is a design constraint, not a limitation to be overcome.
- **SemiEngineering, "Probably Good Die" era:** Acknowledges that as more chiplets are co-assembled, the cost of a failed package rises dramatically, but the solution is better pre-assembly testing -- not post-assembly rework.

---

## 8. What Happens When a CoWoS Package Fails?

Based on the research, the actual end-of-life flow for a failed GPU with HBM is:

1. **If the card is repairable at the board level** (VRM, connector, passive components): Repair and return to service. This is the Shenzhen model.
2. **If the CoWoS package itself has failed** (HBM degradation, die crack, interposer delamination): The card is scrapped as a unit. The CoWoS package cannot be economically repaired.
3. **Scrap recovery** from a dead card yields:
   - Copper from heatsink, PCB, inductors (~$5-25 depending on card)
   - Gold from connectors and pad plating (~$2-60 depending on card)
   - Indium from TIM (~$5-8)
   - The CoWoS package itself goes to e-waste precious metals recovery (hydrometallurgy/pyrometallurgy) for trace Au, Ag, Cu, Pd -- yielding perhaps $1-5 total

**The HBM stacks are never individually recovered.** They are destroyed along with the interposer and GPU die during precious metals extraction.

---

## 9. Implications for Report Valuations

### Current report values (theoretical secondary market per stack):

| GPU | HBM Gen | Stacks | Per-Stack Value | Total HBM Secondary | Confidence |
|---|---|---|---|---|---|
| V100 (16GB) | HBM2 4-Hi | 4 | $0 | $0 | HIGH (correct) |
| V100 (32GB) | HBM2 8-Hi | 4 | $0 | $0 | HIGH (correct) |
| A100 PCIe 40GB | HBM2 | 5 | $0 | $0 | HIGH (correct) |
| A100 SXM4 80GB | HBM2e | 5 | $60 | $300 | LOW |
| A30 | HBM2 | 3 | $0 | $0 | HIGH (correct) |
| H100 PCIe 80GB | HBM2e | 5 | $250 | $1,250 | VERY LOW |
| H100 PCIe 94GB | HBM3 | 6 | $350 | $2,100 | VERY LOW |
| H100 SXM5 80GB | HBM3 | 5+1 | $240 | $1,200 | VERY LOW |
| H200 NVL | HBM3e | 6 | Not stated | -- | -- |
| H200 SXM | HBM3e | 6 | Not stated | -- | -- |
| GH200 (GPU) | HBM3 | 6 | $100 | $600 | VERY LOW |
| MI210 | HBM2e | 4 | $30 | $120 | VERY LOW |
| MI300X | HBM3 | 8 | $200 | $1,600 | VERY LOW |
| Gaudi2 | HBM2e | 6 | Not stated | -- | -- |

### Recommended corrections:

**For all cards using HBM in a 2.5D package (CoWoS, EFB, EMIB):**

The "secondary_market_value_usd" for HBM stacks should be **$0.00** in the components.csv files, with a note explaining why.

**Rationale:**
1. Individual HBM stacks cannot be separated from the 2.5D package without destruction
2. No secondary market exists for individual HBM stacks (zero listings on any marketplace or broker)
3. No commercial rework service exists for CoWoS/EFB component recovery
4. No academic literature documents successful HBM stack recovery from a bonded package
5. The Shenzhen repair shops swap entire CoWoS assemblies, not individual stacks
6. Even TSMC and OSATs cannot perform this rework

**The only defensible secondary market value for HBM is as part of the complete CoWoS package assembly** -- which is already captured in the "GPU die" secondary market value line item (where those values represent the entire package, not just the bare die).

---

## 10. What *Would* an HBM Stack Be Worth If It Could Be Extracted?

For completeness, if the physical extraction problem were somehow solved:

| HBM Generation | New Price (2026) | Theoretical Pulled/Tested Value | Basis |
|---|---|---|---|
| HBM2 (4-Hi, 4GB) | EOL / unavailable | $10-20 | Obsolete; no new designs use it |
| HBM2 (8-Hi, 8GB) | EOL / unavailable | $20-40 | Obsolete; limited repair demand |
| HBM2e (8-Hi, 16GB) | ~$80-120 (est.) | $30-60 | Transitioning to EOL; repair-only demand |
| HBM3 (8-Hi, 16GB) | ~$350-420 | $150-250 | Current gen; strong demand |
| HBM3e (12-Hi, 24GB) | ~$420-500 | $200-350 | Current gen; sold out |
| HBM4 (12-Hi, 36GB) | ~$500+ | $300-400 | Next gen; 2026 ramp |

These values assume: (a) the stack is physically intact, (b) it can be electrically tested and confirmed functional, (c) a buyer exists who has the equipment to rebond it to an interposer. Conditions (a) and (b) are not achievable with current technology for stacks removed from bonded packages. Condition (c) limits the buyer pool to essentially TSMC, Samsung, and SK Hynix -- none of whom would buy used stacks.

---

## Sources

### Shenzhen GPU Repair
- [Tom's Hardware -- Underground China repair shops thrive servicing illicit Nvidia GPUs](https://www.tomshardware.com/pc-components/gpus/underground-china-repair-shops-thrive-servicing-illicit-nvidia-gpus-banned-by-export-restrictions-companies-resurrecting-banned-ai-accelerators-at-a-rate-of-up-to-500-per-month)
- [NotebookCheck -- Gray-market repairs for banned Nvidia H100 and A100 GPUs surge in China](https://www.notebookcheck.net/Gray-market-repairs-for-banned-Nvidia-H100-and-A100-GPUs-surge-in-China.1069609.0.html)
- [Techzine -- Illegal Nvidia chips repaired en masse in China](https://www.techzine.eu/news/infrastructure/133308/illegal-nvidia-chips-repaired-en-masse-in-china/)

### HBM Pricing & Market
- [TrendForce -- Samsung, SK hynix Plan ~20% HBM3E Price Hike for 2026](https://www.trendforce.com/news/2025/12/24/news-samsung-sk-hynix-reportedly-plan-20-hbm3e-price-hike-for-2026-as-nvidia-h200-asic-demand-rises/)
- [CNBC -- AI memory is sold out, causing an unprecedented surge in prices](https://www.cnbc.com/2026/01/10/micron-ai-memory-shortage-hbm-nvidia-samsung.html)
- [Introl -- The AI Memory Supercycle](https://introl.com/blog/ai-memory-supercycle-hbm-2026)
- [Epoch AI -- NVIDIA B200 cost breakdown](https://epoch.ai/data-insights/b200-cost-breakdown)

### CoWoS Packaging & Rework Challenges
- [TSMC -- CoWoS Technology](https://3dfabric.tsmc.com/english/dedicatedFoundry/technology/cowos.htm)
- [AnySilicon -- Understanding CoWoS Packaging Technology](https://anysilicon.com/cowos-package/)
- [TrendForce -- TSMC CoWoS-L/S Fully Booked, OSAT Partners Step Up](https://www.trendforce.com/news/2025/12/08/news-tsmcs-cowos-l-s-reportedly-fully-booked-osat-partners-step-up-with-ases-cowop-in-focus/)
- [PackNode -- The Compute Packaging Bottleneck](https://www.packnode.org/en/innovation/cowos-chip-packaging-crisis-2025)
- [Semiconductor Engineering -- Chiplet Design Considerations](https://semiengineering.com/chiplet-design-considerations/)

### Underfill Rework & Die Recovery
- [BEST Inc. -- Underfill Rework Services](https://www.solder.net/technical-info/underfill-rework/)
- [I-Connect007 -- Methods for Underfilled Component Rework](https://iconnect007.com/index.php/article/129680/knocking-down-the-bone-pile-methods-for-underfilled-component-rework/129683?skin=smt)
- [Semiconductor Equipment Corp. -- Reworking Underfilled Flip Chips](https://www.semicorp.com/articles/reworking-underfilled-flip-chips/)
- [Circuits Assembly -- Cold Underfill Component Removal](https://www.circuitsassembly.com/ca/features-itemid-fix/38014-cold-underfill-component-removal.html)

### Microbump & 2.5D Technology
- [IEEE Xplore -- Process integration of solder bumps and Cu pillar microbumps on 2.5D fine pitch TSV interposer](https://ieeexplore.ieee.org/document/6745756)
- [ResearchGate -- Micro Bump System for 2nd Generation Silicon Interposer with GPU and HBM](https://www.researchgate.net/publication/326954131_Micro_Bump_System_for_2nd_Generation_Silicon_Interposer_with_GPU_and_High_Bandwidth_Memory_HBM_Concurrent_Integration)
- [Semiconductor Engineering -- Scaling Bump Pitches in Advanced Packaging](https://semiengineering.com/scaling-bump-pitches-in-advanced-packaging/)
- [Semiconductor Digest -- Silicon interposers, CoWoS and microbumps](https://sst.semiconductor-digest.com/2013/10/silicon-interposers-cowos-and-microbumps/)

### HBM Failure Rates
- [Tom's Hardware -- Faulty Nvidia H100 GPUs and HBM3 memory caused half of failures during Llama 3 training](https://www.tomshardware.com/tech-industry/artificial-intelligence/faulty-nvidia-h100-gpus-and-hbm3-memory-caused-half-of-the-failures-during-llama-3-training-one-failure-every-three-hours-for-metas-16384-gpu-training-cluster)

### Known Good Die & Yield
- [FormFactor -- Known Good Die Test Enables Advanced Packaging for HBM](https://www.formfactor.com/blog/2024/known-good-die-test-enables-advanced-packaging-high-bandwidth-memory/)
- [Lucas8 -- HBM4 Yield Crisis: Why Nvidia's Rubin R100 Spec-Down is a Strategic Price Buffer](https://lucas8.com/hbm4-yield-crisis-nvidia-rubin-r100-dual-binning/)
- [Semiconductor Engineering -- Singulated Die Test Ensures Stacked Die Quality](https://semiengineering.com/singulated-die-test-ensures-stacked-die-quality-as-power-density-rises/)

### E-Waste & Semiconductor Recycling
- [TechTarget -- Chip recycling: Addressing e-waste in the AI hardware industry](https://www.techtarget.com/searchdatacenter/tip/Chip-recycling-Addressing-e-waste-in-the-AI-hardware-industry)
- [Microchip USA -- Recycling Semiconductors](https://www.microchipusa.com/industry-news/recycling-semiconductors-the-key-to-a-greener-tech-future)
- [Microchip USA -- Ultimate Guide to High Bandwidth Memory](https://www.microchipusa.com/electrical-components/ultimate-guide-to-high-bandwidth-memory)

### Semiconductor Brokers
- [Rochester Electronics](https://www.rocelec.com/)
- [Smith & Associates](https://smithweb.com/)
- [Quest Components](https://www.questcomp.com/)
