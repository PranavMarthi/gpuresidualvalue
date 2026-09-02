# Tesla V100S PCIe 32GB -- Power Connector Deep Investigation

**Date:** 2026-03-29
**Status:** RESOLVED -- 1x CPU 8-pin EPS12V (single connector)
**Confidence:** 85/100

---

## 1. The Question

Does the NVIDIA Tesla V100S PCIe 32GB have one or two 8-pin power connectors?

This matters for scrap value because each 8-pin connector contains copper pins, gold-plated contacts, and a nylon housing. Two connectors would mean roughly 2x the mass of connector materials (~10g vs ~5g), and approximately $0.03 more copper. The scrap impact is negligible in dollar terms, but the answer reveals whether secondary spec databases can be trusted for datacenter GPUs -- an important systemic question for this project.

---

## 2. Source-by-Source Evidence

### Sources claiming 1x 8-pin (single connector)

| # | Source | Type | Exact Claim | Reliability |
|---|--------|------|-------------|-------------|
| 1 | **NVIDIA Product Brief PB-08744-001_v05 (Mar 2018)** | Primary / Engineering | "The board provides a CPU 8-pin power connector on the East edge of the board." Singular. Includes pinout diagram for dongle NVPN: 030-0571-000. Figure 4 shows single connector. | **Authoritative** -- NVIDIA's own engineering document |
| 2 | **NVIDIA Product Brief PB-08744-001_v03 (Oct 2017)** | Primary / Engineering | Same language as v05. "CPU 8-pin power connector" (singular). | **Authoritative** |
| 3 | **IT Creations -- Dell V100S listing (900-2G500-0140-030-DELL)** | Major enterprise reseller | Title explicitly states: "Passive Cooling Heatsink 250W Max Power ( 1 ) One 8 Pin Pwr Connector - DUAL Slot" | **High** -- IT Creations physically inspects and tests every unit. They handle thousands of datacenter GPUs. |
| 4 | **IT Creations -- V100 16GB listing** | Major enterprise reseller | "250 watts of power coming in through a single 8-pin power connector" | **High** |
| 5 | **NVIDIA A100 PCIe 80GB product brief (PB-10577-001)** | Primary / Engineering | A100 PCIe (300W!) uses "(1) one 8-pin power connector" -- same form factor, same CPU 8-pin type, higher TDP, still single connector. | **Authoritative** -- establishes NVIDIA pattern continues to next generation |
| 6 | **Tesla P100 PCIe product brief (PB-08248-001)** | Primary / Engineering | Single CPU 8-pin. Same 030-0571-000 dongle. Same NVIDIA Form Factor 3.0. | **Authoritative** -- establishes pattern across Kepler/Pascal/Volta/Ampere generations |
| 7 | **Supermicro CBL-PWEX-0782** | Server OEM accessory | Single 8-pin cable for V100/K80/M60/M40/P100/P40. Not a Y-splitter. | **High** |
| 8 | **All third-party 030-0571-000 adapter cables** | Aftermarket | Every single adapter (COMeap, MODDIY, GinTai, Suyitai, BargainHardware) is "1x CPU 8-pin male to 2x PCIe 8-pin female." The GPU-side has ONE male connector. | **High** -- physical product design confirms single receptacle on GPU |
| 9 | **NVIDIA Developer Forums thread (177834)** | Community + NVIDIA staff | Users discuss powering V100 PCIe from a single EPS12V CPU 8-pin connector. No mention of needing two GPU-side connectors. | **Medium-High** |
| 10 | **RealTechTalk Tesla GPU desktop guide** | Community / Technical | Describes V100 as using a single EPS12V connector. Warns extensively about EPS vs PCIe pinout differences. Never mentions dual connectors. | **Medium** |
| 11 | **WhatPSU.com -- V100S PCIe 32GB** | Calculator / Database | Minimum 450W PSU, recommends 550-600W with CPU. These figures are consistent with a single 8-pin connector (PCIe slot 75W + 8-pin ~235W = 310W budget for a 250W card). | **Low-Medium** -- calculator, but math checks out |

### Sources claiming 2x 8-pin (dual connectors)

| # | Source | Type | Exact Claim | Reliability |
|---|--------|------|-------------|-------------|
| 1 | **Tom's Hardware (Nov 26, 2019)** | Hardware news site | "the power requirements (a pair of 8-pin PCIe power connectors) remain the same" -- in context of V100S being identical to V100 | **Medium** -- reputable outlet, but this is a news article (not a review/teardown), written on announcement day without hands-on testing |
| 2 | **technical.city -- V100S PCIe 32GB** | Spec aggregator | "Two 8-pin power connectors are required" | **Low** -- known to be unreliable for Tesla-class cards; auto-scraped data |
| 3 | **technical.city -- V100 PCIe 32GB** | Spec aggregator | "Two 8-pin power connectors are required" | **Low** -- same database, same unreliability |
| 4 | **CpuTronic -- V100S PCIe 32GB** | Spec aggregator | Lists 2x 8-pin | **Low** -- auto-scraped |
| 5 | **AxiomGaming GPU Database** | Spec aggregator | "2x 8-pin" | **Low** -- auto-scraped |
| 6 | **Express Computer Systems (expresscomputersystems.com)** | Reseller | "draws power from 2x 8-pin power connectors" | **Low-Medium** -- uses boilerplate spec text, likely sourced from same aggregator databases |

### Sources claiming 1x 8-pin + 1x 6-pin (mixed)

| # | Source | Type | Exact Claim | Reliability |
|---|--------|------|-------------|-------------|
| 1 | **VideoCardz.net -- V100S PCIe 32GB** | Spec aggregator | "draws power via 1x 8-pin, 1x 6-pin" | **Low** -- clearly wrong; no Tesla card uses a 6-pin connector. This is a consumer GPU spec template error. |

---

## 3. Analysis

### The NVIDIA product brief is unambiguous

The product brief PB-08744-001 (both v03 and v05) uses the singular form "a CPU 8-pin power connector" and includes:
- Figure 4: Board diagram showing ONE connector location on the East edge
- Figure 5: Pinout diagram for the 030-0571-000 dongle, which converts ONE CPU 8-pin to TWO PCIe 8-pin cables (for PSU compatibility)
- Section explicitly titled "CPU 8-Pin to PCIe 8-Pin Dongle" -- not "dongles" (plural)

There is no V100S-specific product brief. NVIDIA never published a separate PB document for the V100S, because the V100S is physically identical to the V100 PCIe 32GB. Tom's Hardware, ServeTheHome, and every other outlet confirmed this: "The Tesla V100S is physically identical to the Tesla V100."

### The dongle design proves single connector

The NVIDIA 030-0571-000 dongle is a 1-to-2 adapter: 1x CPU 8-pin male (plugs into GPU) to 2x PCIe 8-pin female (connects to PSU). Every single aftermarket clone of this cable has the same 1:2 design. If the GPU had two connectors, the dongle would need to be a 2:4 or 2:2 design, and aftermarket cables would reflect that. None do.

### The A100 PCIe confirms the pattern

The A100 PCIe 80GB draws 300W -- 50W more than the V100S -- and still uses a single CPU 8-pin connector. IT Creations explicitly lists it as "(1) One 8 Pin Pwr Connector." If NVIDIA can deliver 300W through a single CPU 8-pin + PCIe slot, there is zero engineering reason to use two connectors for a 250W card in the same form factor family.

### EPS12V power budget supports single connector

An EPS12V 8-pin connector is rated for 235W continuous (ATX spec, conservative) or up to 336W theoretical maximum (4 pairs x 7A x 12V). The PCIe x16 slot provides 75W. So:
- Single CPU 8-pin (conservative): 235W + 75W = **310W budget** for a 250W card -- 60W headroom
- Single CPU 8-pin (max): 336W + 75W = **411W budget** -- massive headroom

There is no power delivery reason to add a second connector. Even the A100 at 300W fits within the conservative budget.

### Tom's Hardware error analysis

The Tom's Hardware article was published on November 26, 2019 -- the day NVIDIA announced the V100S. The article is a news piece, not a hands-on review. The author (Zhiye Liu) did not have a physical unit. The phrase "a pair of 8-pin PCIe power connectors" appears to be:

1. Possibly sourced from the same spec aggregator databases (technical.city, etc.) that all list 2x 8-pin
2. A misinterpretation of the 030-0571-000 dongle -- seeing "dual 8-pin" in the dongle description and assuming it means two connectors on the GPU, when it actually means two PCIe 8-pin cables on the PSU side
3. A confusion between the EPS 8-pin physical connector and standard PCIe 8-pin connectors

The article also calls them "PCIe power connectors" -- but the V100's connector is explicitly a CPU/EPS 8-pin, not PCIe 8-pin. This nomenclature error further suggests the author was not working from NVIDIA's product brief.

### The spec aggregator echo chamber

technical.city, CpuTronic, AxiomGaming, and similar databases all appear to share the same underlying data source. They all list "2x 8-pin" for the V100S AND for the V100 PCIe 32GB AND for the V100 PCIe 16GB. But we know from NVIDIA's own documentation and IT Creations' physical inspection that the V100 PCIe 16GB has a single connector ("250 watts of power coming in through a single 8-pin power connector"). If the aggregators are wrong about the V100 16GB (which they demonstrably are), their V100S data is equally unreliable.

VideoCardz.net listing "1x 8-pin + 1x 6-pin" is clearly nonsensical for a Tesla card and confirms these databases are populating fields from consumer GPU templates rather than actual Tesla specifications.

---

## 4. Conclusion

**The NVIDIA Tesla V100S PCIe 32GB has ONE (1) CPU 8-pin EPS12V power connector.**

This is the same single connector used by every NVIDIA Tesla PCIe card from the K80 through the A100:
- Tesla K80: 1x CPU 8-pin (300W)
- Tesla M40: 1x CPU 8-pin (250W)
- Tesla P40: 1x CPU 8-pin (250W)
- Tesla P100 PCIe: 1x CPU 8-pin (250W)
- Tesla V100 PCIe 16GB: 1x CPU 8-pin (250W)
- Tesla V100 PCIe 32GB: 1x CPU 8-pin (250W)
- **Tesla V100S PCIe 32GB: 1x CPU 8-pin (250W)**
- A100 PCIe 40GB: 1x CPU 8-pin (250W)
- A100 PCIe 80GB: 1x CPU 8-pin (300W)

The "2x 8-pin" claim originates from spec aggregator databases that are unreliable for datacenter GPUs. Tom's Hardware propagated this error in a day-of-announcement news article without hands-on verification. The claim then echoed across secondary sources.

### Evidence hierarchy

1. NVIDIA product brief (primary engineering document): **1x CPU 8-pin** -- AUTHORITATIVE
2. IT Creations product listing (physical inspection by enterprise reseller): **1x 8-pin** -- HIGH
3. 030-0571-000 dongle design (physical product): **single GPU-side connector** -- HIGH
4. NVIDIA A100 PCIe precedent (300W, single connector): **consistent pattern** -- HIGH
5. EPS12V power budget math (310W+ budget vs 250W TDP): **supports single** -- HIGH
6. Tom's Hardware article (news article, no hands-on): "pair of 8-pin" -- MEDIUM, contradicted by all primary sources
7. Spec aggregator databases (auto-scraped, unreliable for Tesla): "2x 8-pin" -- LOW

---

## 5. Impact on Scrap Analysis

### Connector mass correction

The existing report and components.csv list the power connector as ambiguous ("1 per product brief, unresolved"). This should be updated to:

- **1x CPU 8-pin EPS12V connector** (on-board, soldered)
- Connector mass: ~5g (nylon housing + 8 tin-plated copper pins)
- Scrap value: ~$0.03 (copper pins, negligible)

The difference between 1x and 2x connectors is approximately:
- Mass: 5g difference
- Copper: ~2g difference (~$0.024)
- **Total scrap impact: < $0.03**

### Why this investigation mattered anyway

The dollar impact is trivial, but the investigation resolved a systemic reliability question: **spec aggregator databases cannot be trusted for Tesla-class datacenter GPU specifications.** Their power connector data is wrong not just for the V100S, but demonstrably for the V100 16GB, V100 32GB, and likely other Tesla models. For future cards in this project, always prefer:

1. NVIDIA product briefs (PB-xxxxx documents)
2. Enterprise reseller listings that describe physical inspection (IT Creations, ServerSupply)
3. Server OEM installation guides (Dell, HPE, Supermicro)

Never rely on technical.city, CpuTronic, AxiomGaming, or similar aggregators for Tesla connector specifications.

---

## 6. Sources

### Primary / Authoritative

- [NVIDIA Tesla V100 PCIe Product Brief PB-08744-001_v05 (Mar 2018)](https://images.nvidia.com/content/tesla/pdf/Tesla-V100-PCIe-Product-Brief.pdf) -- "a CPU 8-pin power connector"; Figure 4 and Figure 5 dongle pinout
- [NVIDIA Tesla V100 PCIe Product Brief PB-08744-001_v03 (Oct 2017)](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/Tesla-V100-PCIe-Product-Brief.pdf) -- same singular connector language
- [NVIDIA Tesla P100 PCIe Product Brief PB-08248-001_v01](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/tesla-product-literature/NV-tesla-p100-pcie-PB-08248-001-v01.pdf) -- predecessor, same single CPU 8-pin pattern
- [NVIDIA A100 40GB PCIe Product Brief PB-10137-001_v03](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/A100-PCIE-Prduct-Brief.pdf) -- successor, same single CPU 8-pin at 250W
- [NVIDIA A100 80GB PCIe Product Brief PB-10577-001_v03](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/a100/pdf/PB-10577-001_v02.pdf) -- 300W, still single CPU 8-pin
- [NVIDIA Volta Architecture Whitepaper WP-08608-001](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf) -- GV100 die details
- [NVIDIA Tesla V100 Datasheet](https://images.nvidia.com/content/technologies/volta/pdf/tesla-volta-v100-datasheet-letter-fnl-web.pdf) -- V100/V100S specifications

### Enterprise Reseller (Physical Inspection)

- [IT Creations -- Tesla V100S Dell (900-2G500-0140-030-DELL)](https://www.itcreations.com/product/122536) -- "(1) One 8 Pin Pwr Connector"
- [IT Creations -- Tesla V100S Used](https://www.itcreations.com/product/121684) -- V100S listing
- [IT Creations -- Tesla V100 16GB](https://www.itcreations.com/nvidia-gpu/nvidia-tesla-v100-16gb-gpu) -- "single 8-pin power connector"
- [IT Creations -- A100 PCIe 80GB](https://www.itcreations.com/product/132309) -- "(1) One 8 Pin Pwr Connector"

### Adapter Cable Evidence

- [COMeap 030-0571-000 Adapter (Amazon)](https://www.amazon.com/COMeap-2-Pack-Graphics-030-0571-000-Adapter/dp/B07M9X68DS) -- "CPU 8 Pin Male to Dual PCIe 8 Pin Female" (1 GPU-side, 2 PSU-side)
- [MODDIY Tesla GPU Power Cable](https://www.moddiy.com/products/5996/NVIDIA-Tesla-K80-M40-M60-P40-P10-P100-GPU-8-Pin-PCIE-Power-Cable.html) -- same 1:2 design
- [Supermicro CBL-PWEX-0782 (Exxact)](https://www.exxactcorp.com/Supermicro-CBL-PWEX-0782-E129086) -- single 8-pin, 55cm
- [BargainHardware 030-0571-000](https://www.bargainhardware.co.uk/nvidia-k80-m60-m40-p40-p100-2x-pcie-8-pin-to-8-pin-cpu-eps-power-cable-2) -- "2x PCIe 8-Pin to 8-Pin CPU EPS"

### Server OEM / Installation

- [Dell PowerEdge R7425 + Tesla V100 Discussion](https://www.dell.com/community/en/conversations/poweredge-hardware-general/r7425-nvidia-tesla-v100/660716eadf4617396d7deffa)
- [Dell PowerEdge R730 Tesla V100 Installation](https://www.dell.com/community/en/conversations/poweredge-hardware-general/installing-a-tesla-v100-gpu-card-in-r730-dell-server/64f9ba1d6f12761f23e05929)
- [HPE ProLiant DL380 Gen10 Maintenance Guide](https://dwn.alza.cz/manual/62490) -- Tesla V100 module integration
- [RealTechTalk -- Tesla GPU Desktop Cable Solutions](https://realtechtalk.com/Nvidia_Tesla_GPUs_K40K80M40P40P100V100_at_homedesktop_hacking_cooling_powering_cable_solutions_Tutorial_AIO_Solutions-2465-articles) -- detailed EPS12V warnings

### Secondary Sources (Used but Lower Reliability)

- [Tom's Hardware -- Tesla V100S Announcement (Nov 2019)](https://www.tomshardware.com/news/nvidia-tesla-v100s-graphics-card-data-center) -- "a pair of 8-pin PCIe power connectors" (CONTRADICTED by primary sources)
- [ServeTheHome -- V100S Performance at Same Power](https://www.servethehome.com/nvidia-tesla-v100s-boasts-big-performance-gains-at-same-power/) -- does not specify connector count
- [PNY Tesla V100S Product Page](https://www.pny.com/en-eu/tesla-v100s-32gb) -- does not specify connector count
- [B&H Photo -- V100S Listing](https://www.bhphotovideo.com/c/product/1544279-REG/nvidia_900_2g500_0040_000_tesla_v100s_32gb_pcie.html) -- product page

### Spec Aggregators (Unreliable for Tesla Cards)

- [technical.city -- V100S PCIe 32GB](https://technical.city/en/video/Tesla-V100S-PCIe-32-GB) -- claims "2x 8-pin" (WRONG)
- [technical.city -- V100 PCIe 32GB](https://technical.city/en/video/Tesla-V100-PCIe-32-GB) -- claims "2x 8-pin" (WRONG)
- [AxiomGaming GPU Database -- V100S](https://gpus.axiomgaming.net/gpu/tesla-v100s-pcie-32-gb) -- claims "2x 8-pin" (WRONG)
- [VideoCardz.net -- V100S PCIe 32GB](https://videocardz.net/nvidia-tesla-v100s-pcie-32gb) -- claims "1x 8-pin + 1x 6-pin" (WRONG -- nonsensical)

### EPS12V Specification

- [SSI EPS12V Power Supply Design Guide](https://www.smps.us/EPS12V_Spec2_92.pdf) -- 8-pin rated 235W continuous / 336W max
- [Exxact -- PCIe 8-pin vs EPS-12V 8-pin](https://support.exxactcorp.com/hc/en-us/articles/20180443940119-PCIe-8-pin-vs-EPS-12V-8-pin-power-connections) -- pinout differences
- [NVIDIA Developer Forums Thread 177834](https://forums.developer.nvidia.com/t/nvidia-tesla-v100-power-connector/177834) -- community discussion on V100 power connector type

---

## 7. Remaining Uncertainty (15%)

The 15% residual uncertainty exists because:

1. **No V100S-specific product brief exists.** The product brief PB-08744-001 covers "Tesla V100 PCIe" generically. It was last updated March 2018, 20 months before the V100S launched (November 2019). While Tom's Hardware and NVIDIA confirm the V100S is "physically identical," we cannot be 100% certain NVIDIA did not make a minor board revision that added a second connector.

2. **No teardown photos found.** Despite extensive searching, no public teardown or close-up photo of a V100S PCIe board showing the power connector area was found. A photograph would be dispositive.

3. **IT Creations is the only enterprise reseller with explicit connector count.** Other resellers (Express Computer Systems, ServerSupply, Newegg) either do not specify or use aggregator data.

To reach 100% confidence, one would need to physically inspect a V100S PCIe card or locate a V100S-specific NVIDIA engineering document. The weight of evidence strongly favors 1x CPU 8-pin, but destructive certainty requires a physical card.
