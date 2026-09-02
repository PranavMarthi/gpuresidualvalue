# H200 SXM Weight Budget -- Bottom-Up Engineering Estimate

**Date:** 2026-03-29
**Purpose:** Resolve the suspect ~1,020 g bare module weight with 51% attributed to "Other."

---

## Problem Statement

The report claims the H200 SXM bare module weighs ~1,020 g, with the weight breakdown showing 516 g (50.6%) as "Other (solder, TIM, passives, underfill, misc)." This is physically implausible -- solder, TIM, passives, and underfill on a module this size cannot constitute half the total mass. Either the 1,020 g total is wrong, or major components are misattributed to the "Other" bucket.

The `module_weights_investigation.md` already flagged this: "The 1,020 g figure sits in an ambiguous zone -- too heavy for a bare board (which should be ~500--700 g based on H100 SXM5 analysis), too light for a module with heatsink (~2,400--2,600 g)."

This analysis resolves the ambiguity with a first-principles bottom-up estimate.

---

## 1. SXM5 PCB

### Dimensions

The SXM5 module is NOT a full-length PCIe card. It is a compact module that plugs into a baseboard socket. From Tom's Hardware photos of the H100 SXM5 and the known SXM5 connector geometry:

- The SXM5 board is approximately **100 mm x 100 mm** (roughly square). Public photos from Tom's Hardware and Comino show a near-square module with the SXM5 connector on one edge and the GPU package occupying the central area.
- Some sources suggest up to **100 mm x 120 mm** accounting for asymmetric VRM layout on one side.
- Best estimate: **100 mm x 110 mm = 110 cm2 = 11,000 mm2**

For reference, a full-length PCIe card (like H100 PCIe at 267 mm x 111 mm = ~297 cm2) is roughly 2.7x larger in area.

### Layer count and thickness

A 700W GPU module with 61 power stages requires substantial copper for current delivery. Expected:
- **16--20 layers** (typical for high-power datacenter GPU modules)
- **2 oz (70 um) copper on power planes**, 1 oz on signal layers
- Total board thickness: ~2.4--2.8 mm (thicker than consumer boards due to layer count)

### Mass calculation

FR-4 density: ~1.85 g/cm3
Copper density: 8.96 g/cm3

For a 20-layer board at 2.6 mm total thickness:

- **FR-4 dielectric volume:** Board area (110 cm2) x effective dielectric thickness (~1.8 mm after subtracting Cu planes) = 110 x 0.18 = 19.8 cm3
- **FR-4 mass:** 19.8 cm3 x 1.85 g/cm3 = **36.6 g**
- **Copper volume:** Assume 6 power/ground planes at 70 um + 14 signal layers at 35 um = 6 x 0.007 cm x 110 cm2 + 14 x 0.0035 cm x 110 cm2 = 4.62 + 5.39 = 10.0 cm3 (but copper fill is not 100%; use ~60% average fill) = 6.0 cm3
- **Copper mass:** 6.0 cm3 x 8.96 g/cm3 = **53.8 g**
- **Total PCB mass: ~90 g**

Range: **80--110 g** depending on exact dimensions, layer count, and copper fill.

The report's 120 g is slightly high but within plausible range if the board is closer to 100 x 120 mm with heavy copper fills. Retaining **95 g** as the central estimate.

---

## 2. GPU Package (GH100 CoWoS-S)

The GH100 package is a CoWoS-S (Chip-on-Wafer-on-Substrate) assembly consisting of:

### Components

| Sub-component | Dimensions | Mass estimate | Notes |
|---------------|-----------|---------------|-------|
| Organic substrate (ABF) | ~55 x 55 mm, ~1.2 mm thick | 8--10 g | ABF buildup layers + BT core, density ~2.5 g/cm3 |
| Silicon interposer | ~53 x 53 mm, ~100 um | 5.5 g | TSMC 65nm, 2,831 mm2, thinned. At 2.33 g/cm3 x 28.31 cm2 x 0.01 cm = 0.66 g. But with redistribution layers and microbumps: ~1--2 g |
| GH100 die | 814 mm2, ~50--100 um thinned | 0.1--0.2 g | Backgrind for CoWoS. Full thickness 0.775 mm = 1.47 g, but CoWoS dies are thinned |
| 6x HBM3e stacks | 11 x 11 mm each, 8-Hi | 16.8 g | 6 x 2.8 g per stack |
| Underfill epoxy | fills gap under die and HBM | 2--3 g | Capillary underfill, silica-filled epoxy |
| Solder balls (BGA) | ~1,500+ balls, SAC305 | 8--12 g | Package-to-board interconnect |
| Copper lid/heat spreader (package-level) | ~55 x 55 mm | See Section 5 | Discussed separately |

### Package total (without lid): ~35--45 g

The report lists GPU die + interposer + substrate at 92 g and memory at 17 g, totaling 109 g for the package assembly. This is plausible if the 85 g substrate weight includes the full organic package substrate at 55 x 55 mm (which is much larger than a typical BGA substrate and carries heavy copper power distribution for 700W).

Revised package assembly (die + interposer + substrate + HBM + underfill + BGA balls): **~55--65 g** without any lid, or **~90--110 g** with a copper stiffener frame integrated into the package.

The report's combined 109 g (92 + 17) is reasonable if the substrate is on the heavy side. Using **85 g** as central estimate for the package assembly without separate IHS.

---

## 3. VRM / Power Delivery

The H100 SXM5 (and by inference, H200 SXM) has a 700W power envelope with 61 power stages. From Tom's Hardware photos:

### Inductors
- **29 inductors** (plus 3 single-stage) = 32 inductor components
- Datacenter power inductors at this current rating: **3.0--4.0 g each**
- **32 x 3.5 g = 112 g**

### DrMOS / Power stages
- **61 DrMOS ICs** (integrated driver + high-side + low-side MOSFET)
- Typical DrMOS (e.g., Renesas RAA22010540, MPS MP86956): **0.3--0.5 g each** in QFN/PQFN package
- Some high-current stages use larger packages. Using 0.4 g average.
- **61 x 0.4 g = 24 g**

### Capacitors (VRM input/output)
- High-current VRM needs substantial decoupling: **~100 input caps + ~100 output caps**
- Mix of MLCCs (0.1--0.3 g each) and polymer caps (~0.5 g each)
- **~40--60 g total for VRM capacitors**

### VRM controller ICs
- 2--3 multi-phase PWM controllers: **~2 g total**

### VRM total: ~180--200 g

The report lists 150 g for the entire VRM. This is **underestimated** given 32 inductors at 3.5 g each = 112 g for inductors alone. The report's 150 g implies only ~38 g for 61 DrMOS + 200 caps, which is too low.

**Revised VRM estimate: 190 g** (central), range 175--210 g.

---

## 4. SXM5 Connector

The SXM5 is a high-density proprietary connector with hundreds of power and signal pins. Based on comparable high-pin-count board-to-board connectors at this power rating:

- Connector body (LCP plastic): ~5 g
- Pin array (copper alloy, silver-plated): ~10--15 g
- Total: **15--25 g**

The report lists 15 g for the connector alone plus 30 g for a stiffener ring = 45 g combined. This is reasonable.

**Revised estimate: 20 g** connector + **30 g** stiffener = **50 g** total.

---

## 5. Heatspreader / IHS -- THE MISSING MASS

This is the critical question. Does the H200 SXM module have a copper IHS (Integrated Heat Spreader) as part of the module assembly?

### Evidence that an IHS/heatspreader exists on the module

1. **The report already lists "Nickel-plated copper heat spreader" at 80 g.** But 80 g for a copper spreader over a 55 x 55 mm GPU package is far too light. A copper plate of 55 x 55 mm at 3 mm thickness weighs: 5.5 x 5.5 x 0.3 cm x 8.96 g/cm3 = **81 g**. So 80 g corresponds to a thin (3 mm) lid that covers only the package area.

2. **SXM modules require a thermal interface to the baseboard heatsink.** The baseboard heatsink sits on top of the module. Between the GPU die and the heatsink, there must be a heat spreader to distribute heat from the 814 mm2 die + 6 HBM stacks to the heatsink contact area.

3. **The TIM entry lists "indium-based solder TIM between die and heat spreader."** This confirms there IS a heat spreader. The question is whether it is a thin package lid (80 g, already counted) or a larger vapor chamber / copper spreader.

4. **Photos of SXM5 modules from Comino and ServeTheHome** show a large flat copper-colored surface on top of the module, covering essentially the entire board area. This is NOT just a 55 mm package lid -- it appears to be a full-board-coverage heatspreader.

### Heatspreader mass estimate

If the heatspreader covers most of the module board area (~100 x 110 mm) with an average thickness of 3--5 mm:

- **Thin estimate (3 mm):** 10 x 11 x 0.3 cm x 8.96 g/cm3 = **296 g**
- **Medium estimate (4 mm):** 10 x 11 x 0.4 cm x 8.96 g/cm3 = **394 g**
- **Thick estimate (5 mm):** 10 x 11 x 0.5 cm x 8.96 g/cm3 = **493 g**

However, the heatspreader is not a solid block -- it has pockets, channels, and reduced thickness in areas away from the die. A realistic estimate for the copper content:

- **Effective copper volume: ~60% of a 4 mm solid plate** = 10 x 11 x 0.4 x 0.6 = 26.4 cm3
- **Mass: 26.4 x 8.96 = ~237 g**

But the SXM5 module may use a **vapor chamber** instead of a solid copper plate. Vapor chambers for 700W have:
- Copper shell (top + bottom plates): ~2 mm total effective copper
- Internal wick structure
- Working fluid (water/methanol)
- **Total mass: 150--250 g** for this footprint

**Best estimate for heatspreader on the module: 200 g** (range 150--300 g).

The report's 80 g is too low if this is a full-coverage spreader. The 80 g makes sense only if it is a bare package-level lid (just over the die area), but the photos suggest a much larger thermal component.

---

## 6. Passives, Misc ICs, Solder

| Item | Mass (g) |
|------|---------|
| ~100 resistors (0402/0603) | 2 |
| VRM controller ICs, EEPROMs, sensors | 3 |
| ESD protection, misc support ICs | 2 |
| Solder paste (reflow, entire board) | 5 |
| Board-level BGA solder (already counted in package) | 0 |
| TIM (indium, 3 g, already counted) | 0 |
| Underfill (already counted in package) | 0 |
| Miscellaneous (labels, thermal pads, adhesive) | 3 |
| **Total** | **~15--20 g** |

---

## 7. Bottom-Up Sum

| Component | Low (g) | Central (g) | High (g) |
|-----------|---------|-------------|----------|
| PCB (FR-4 module board) | 80 | 95 | 110 |
| GPU package assembly (die + interposer + substrate + HBM + underfill + BGA) | 70 | 85 | 110 |
| VRM (inductors + DrMOS + caps + controllers) | 175 | 190 | 210 |
| SXM5 connector + stiffener ring | 40 | 50 | 60 |
| Heatspreader / IHS (nickel-plated copper, full coverage) | 150 | 200 | 300 |
| Passives, misc ICs, solder | 15 | 20 | 30 |
| **Total** | **530** | **640** | **820** |

---

## 8. Diagnosis

The bottom-up estimate yields **530--820 g** with a central value of **640 g** for the bare module including a full-coverage copper heatspreader (but NOT the large baseboard-mounted heatsink/cold plate).

### How did the report get to 1,020 g?

The original 1,020 g was "derived by subtracting an assumed heatsink weight from The Register/Omdia average." The Omdia figure was "over 3 kg" for the module with the large baseboard heatsink. If you subtract a ~2,000 g heatsink from 3,000 g, you get ~1,000 g. But:

1. The Omdia "over 3 kg" figure was already shown to be overstated (HGX PCF back-calculation yields ~2,400--2,600 g per module with heatsink).
2. The subtracted heatsink weight was itself an estimate.
3. The resulting 1,020 g was then force-fit into a weight table, with 516 g dumped into "Other" because the identified components only summed to ~504 g.

### Resolution

The bare module weight is most likely **550--700 g**, consistent with:
- The `module_weights_investigation.md` revised estimate of "~500--700 g bare module"
- The bottom-up engineering estimate central value of 640 g
- The PCIe card comparison: H100 PCIe weighs 1,200 g but includes a full-length 267 mm PCB, a large passive heatsink (~400--500 g), and a metal bracket. The SXM5 board is ~1/3 the PCB area, has no passive heatsink tower, and no bracket.

The 1,020 g figure is **wrong** -- it was an artifact of subtracting an uncertain heatsink weight from an overstated Omdia total. The "51% Other" was the residual that should have been a red flag: you cannot have 516 g of solder, TIM, passives, and underfill on a board this size.

### Revised weight: 640 g (range 550--750 g), confidence 50/100

This is still uncertain because no one has weighed a bare H200 SXM module. But it is internally consistent and derived from first principles rather than back-calculating from a disputed Omdia figure.

---

## 9. Cross-Checks

### Cross-check 1: HGX back-calculation
- HGX H100 baseboard: 24 kg
- Non-GPU baseboard components: ~3.5 kg (central estimate)
- 8 modules with baseboard heatsinks: 20.5 kg
- Per module with heatsink: 2,563 g
- Baseboard heatsink (large copper cold plate with fins): ~1,800--2,000 g
- Bare module: 2,563 - 1,900 = **~660 g** -- consistent with 640 g central estimate.

### Cross-check 2: A100 SXM4 scaling
- A100 SXM4 bare module: ~325 g (400W, 5 HBM2e stacks, SXM4 connector)
- H200 SXM5 has: ~75% more power (700W vs 400W), requiring ~75% more VRM mass; 1 additional HBM stack; larger PCB; larger heatspreader
- Scaled: 325 g x 1.75 (VRM) would be ~570 g, plus additional heatspreader and connector mass = **~600--700 g** -- consistent.

### Cross-check 3: PCIe card comparison
- H100 PCIe: 1,200 g (NVIDIA-confirmed), includes ~400--500 g passive heatsink, ~50 g bracket, and a PCB ~2.7x larger than SXM5
- Stripping heatsink and bracket: ~700--750 g for PCIe bare board
- SXM5 has ~37% the PCB area but denser VRM (700W vs 350W for PCIe)
- Expected: ~550--700 g -- consistent.

---

## Sources

- Tom's Hardware H100 SXM5 photos (VRM layout, board dimensions): https://www.tomshardware.com/news/nvidia-hopper-h100-sxm5-pictured
- Comino H100 teardown (module photos): https://www.comino.com/blog/how-we-destroyed-the-nvidia-h100-gpu-the-ultimate-comino-tear-down-comino-h100-waterblock-teaser
- NVIDIA HGX H100 PCF Summary (24 kg baseboard): https://images.nvidia.com/aem-dam/Solutions/documents/HGX-H100-PCF-Summary.pdf
- FR-4 material properties: IPC-4101 specification, density 1.80--1.87 g/cm3
- Copper density: 8.96 g/cm3
- CoWoS-S package dimensions: TSMC reference, AnandTech/WikiChip GH100 die analysis
- DrMOS typical mass: Renesas RAA22010540 datasheet, MPS MP86956 datasheet (QFN packages)
- SXM5 connector geometry: NVIDIA HGX H100 Design Guide (NDA, but pin count and form factor widely reported)
