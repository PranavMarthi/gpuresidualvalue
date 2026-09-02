# GPU Scrap Value Reports -- Final Review (Third-Pass Audit)

**Auditor:** Final-Pass Hardware Audit
**Date:** 2026-03-29
**Scope:** All 22 report.md files + both prior audits (audit_components.md, final_audit_components.md)

---

## 1. Die Consistency Table

| Die | Cards Using It | Die Size (mm2) | Transistors | Node | Consistent? |
|-----|---------------|---------------|-------------|------|-------------|
| GA102 | A10 (GA102-890), A40 (GA102-895) | 628.4 / 628 | 28.3B / 28.3B | Samsung 8nm "8N custom" / "8nm LPP" | YES -- 0.06% rounding on area; process label is same fab, different marketing names |
| GA100 | A100 PCIe, A100 SXM4, A100X, A30 (cut-down) | 826 / 826 / 826 / 826 | 54.2B all | TSMC 7nm (N7) all | YES |
| AD102 | L40 (AD102-895-A1), L40S (AD102-895A) | 608.4 / 608.4 | 76.3B / 76.3B | TSMC 4N / TSMC 4N | YES |
| AD104 | L4 | 295 | 35.8B | TSMC 4N | N/A (single card) |
| GH100 | H100 PCIe, H100 SXM5, H200 NVL, H200 SXM, GH200 | 814 all | 80B all | TSMC 4N all | YES |
| GV100 | V100 PCIe, V100 SXM2, V100S PCIe | 815 all | 21.1B all | TSMC 12nm FFN all | YES |
| TU104 | T4 (TU104-895-A1) | 545 | 13.6B | TSMC 12nm FFN | N/A (single card) |
| GA107 | A16 (GA107-890 x4) | ~200 | ~8.7B | Samsung 8nm (8N) | N/A (single card) |
| HL-2080 | Gaudi2 | ~500 (est.) | Not disclosed | TSMC 7nm | N/A (single card) |
| Aldebaran | MI210 | 724 | ~29.1B | TSMC N6 | N/A (single card) |
| XCD+IOD | MI300X (8 XCD + 4 IOD) | XCD ~80-115 / IOD ~370 | 153B total | TSMC N5 / N6 | N/A (single card) |

**All shared dies are consistent across cards.** No contradictions in die size, transistor count, or process node.

---

## 2. Memory Validation Table

| GPU | Mem Type | Units | Cap/Unit | Calc Total | Reported Total | VALID? |
|-----|----------|-------|----------|-----------|---------------|--------|
| A10 | GDDR6 | 12 chips | 2 GB | 24 GB | 24 GB | YES |
| A100 PCIe 40GB | HBM2 | 5 stacks | 8 GB | 40 GB | 40 GB | YES |
| A100 PCIe 80GB | HBM2e | 5 stacks | 16 GB | 80 GB | 80 GB | YES |
| A100 SXM4 80GB | HBM2e | 5 stacks | 16 GB | 80 GB | 80 GB | YES |
| A100X (GPU) | HBM2e | 5 stacks | 16 GB | 80 GB | 80 GB | YES |
| A100X (DPU) | DDR4 | 9 chips | ~1.78 GB | ~16 GB | 16 GB | YES |
| A16 | GDDR6 | 32 chips | 2 GB | 64 GB | 64 GB | YES |
| A30 | HBM2 | 3 stacks | 8 GB | 24 GB | 24 GB | YES |
| A40 | GDDR6 | 24 chips | 2 GB | 48 GB | 48 GB | YES |
| MI300X | HBM3 | 8 stacks | 24 GB | 192 GB | 192 GB | YES |
| Gaudi2 | HBM2e | 6 stacks | 16 GB | 96 GB | 96 GB | YES |
| H100 PCIe 80GB | HBM2e | 5 stacks | 16 GB | 80 GB | 80 GB | YES |
| H100 PCIe 94GB | HBM3 | 6 stacks | 16 GB | 96 GB nom (94 usable) | 94 GB | YES |
| H100 SXM5 80GB | HBM3 | 5 active of 6 | 16 GB | 80 GB | 80 GB | YES |
| H200 NVL | HBM3e | 6 stacks | 24 GB | 144 GB nom (141 usable) | 141 GB | YES |
| H200 SXM | HBM3e | 6 stacks | ~24 GB | ~141 GB | 141 GB | YES |
| L4 | GDDR6 | 12 chips | 2 GB | 24 GB | 24 GB | YES |
| L40 | GDDR6 | 24 chips | 2 GB | 48 GB | 48 GB | YES |
| L40S | GDDR6 | 24 chips | 2 GB | 48 GB | 48 GB | YES |
| GH200 (GPU) | HBM3 | 6 stacks | 16 GB | 96 GB | 96 GB | YES |
| GH200 (CPU) | LPDDR5X | 16 pkg | 30 GB | 480 GB | 480 GB | YES |
| MI210 | HBM2e | 4 stacks | 16 GB | 64 GB | 64 GB | YES |
| T4 | GDDR6 | 8 chips | 2 GB | 16 GB | 16 GB | YES |
| V100 PCIe 16GB | HBM2 | 4 stacks | 4 GB (4-Hi) | 16 GB | 16 GB | YES |
| V100 PCIe 32GB | HBM2 | 4 stacks | 8 GB (8-Hi) | 32 GB | 32 GB | YES |
| V100 SXM2 32GB | HBM2 | 4 stacks | 8 GB (8-Hi) | 32 GB | 32 GB | YES |
| V100S PCIe | HBM2 | 4 stacks | 8 GB (8-Hi) | 32 GB | 32 GB | YES |

**All 27 memory configurations validated. No arithmetic errors.**

---

## 3. Actual Errors Found

### 3.1 CRITICAL: Residual "wire bonds" / "bond wires" References on Flip-Chip Cards

Both prior audits flagged this. Four reports STILL contain problematic wire bond language in their precious metals tables or component breakdowns for cards that use flip-chip packaging:

| Report | Location | Exact Text | Problem |
|--------|----------|-----------|---------|
| H100 PCIe | Sec 4 gold notes | "PCB ENIG finish + wire bonds (~25 mg)" | H100 uses CoWoS-S flip-chip. "wire bonds" is wrong; should say "IC lead plating" or "pad finish" |
| MI210 | Sec 4 gold notes | "Wire bonds, connector plating, substrate pads" | MI210 uses 2.5D EFB flip-chip. "Wire bonds" is wrong for the GPU die interconnect |
| A100X | Sec 3 BlueField-2 | "~0.15g Au in bond wires and pad plating" | BF2 uses standard flip-chip BGA. "bond wires" overstates gold; should be "pad plating" only |
| A40 | Sec 3 GPU die / memory | "trace gold from bond wires/bumps" and "trace Au bond wires per chip" | A40 uses flip-chip BGA. GDDR6 chips use BGA pads, not wire bonds |
| V100S PCIe | Sec 4 gold notes | "IC bond wires ~0.005g" | CoWoS-S card; peripheral ICs *might* use wire bonds but this is speculative and should say "IC lead/pad plating" |
| V100 SXM2 | Sec 4 gold notes | "misc IC bond wires ~0.005g" | Same issue as V100S |
| A16 | Sec 3 GPU die | "trace gold on bond wires/pads" | GA107 uses flip-chip BGA, not wire bonds |

**Dollar impact:** The A100X BlueField-2 claim of 0.15g in bond wires is the most material (~$21.60 gross at $144/g). The others reference small amounts (<0.01g) but the terminology is factually wrong.

### 3.2 CRITICAL: L40 Gold Estimate is a 10x Outlier

The L40 report's 0.05g gold in its final precious metals table is now harmonized with the L40S. HOWEVER, in Section 7 Key Observations, the L40 report says: "The original analysis overestimated PCIe finger gold at 0.41g by assuming 5-micron server-grade plating." The correction to 0.05g was applied. **This is fixed in the final table but the prior audits flagged it as "STILL UNFIXED" -- it appears the final table IS correct at 0.05g.** The prior audit may have been looking at an older version. Current state: FIXED.

### 3.3 HIGH: H200 NVL vs H200 SXM Gold 10x+ Discrepancy

| Card | Gold (g) | Gross Gold Value |
|------|---------|-----------------|
| H200 NVL | 0.40 | $57.60 |
| H200 SXM | 0.02-0.05 | $2.90-$7.25 |

Both cards share the same GH100 die on CoWoS-S with 6 HBM3e stacks. The NVL adds PCIe gold fingers and an NVLink bridge connector, which could justify 0.05-0.10g more gold than the SXM. But a 10-20x gap is not defensible. Either:
- H200 NVL at 0.40g is overstated (likely by 2-4x)
- H200 SXM at 0.02g (mid-estimate) is understated (likely by 2-5x)
- A defensible harmonized range: NVL 0.10-0.20g, SXM 0.05-0.10g

### 3.4 HIGH: H100 PCIe vs H100 SXM5 Gold 5x+ Discrepancy

| Card | Gold (g) | Gross Gold Value |
|------|---------|-----------------|
| H100 PCIe | 0.04-0.07 | $5.80-$10.10 |
| H100 SXM5 | 0.30 | $43.20 |

Same GH100 die. The SXM5 has a high-pin-count mezzanine connector, but 0.30g total is very high for a module with no PCIe gold fingers. The V100 SXM2 (similar concept) estimates only 0.05g. Realistic range for H100 SXM5: 0.10-0.20g.

### 3.5 HIGH: H200 SXM "Other" Category is 51% of Weight

The H200 SXM weight breakdown has 516g (50.6%) in "Other" -- over half the module weight is unattributed. This was flagged in BOTH prior audits and remains unfixed. The physical characterization of this card is the weakest of all 22.

### 3.6 HIGH: A40 Weight Budget Anomalies

- Heatsink at 750g = 74% of card weight (expected 40-65% for passive PCIe)
- "Other" at 22g = 2% of total (lowest of any PCIe card; expected 5-15%)
- Component weights sum to ~1,130g but NVIDIA spec is 1,010g (board + bracket)

The weight breakdown sums to more than the stated total. The 750g heatsink is likely overstated, or other components are underestimated.

### 3.7 MODERATE: VRM Phase Count Anomalies

| GPU | TDP (W) | Claimed Phases | Expected Range | Issue |
|-----|---------|---------------|---------------|-------|
| MI300X | 750 | 12 | 16-32 | Low for TDP; may use 48V architecture but not documented |
| GH200 | 900 | 20 (12+8) | 24-40 | Low for TDP; may use higher-current stages but not documented |
| Gaudi2 | 600 | 12+ | 16-24 | Borderline low; OAM 48V input may reduce phase count |

All three are OAM/module form factors where 48V power delivery could justify lower phase counts, but none of the reports document this.

### 3.8 MODERATE: Power Connector vs TDP Mismatches

All prior connector errors (A10 EPS/PCIe swap, A30 PCIe/EPS swap, A100X type, H200 NVL 2x8pin->16pin) have been corrected. No new mismatches found. Current state for all 22 cards:

| TDP Range | Expected Connector | Cards | Correct? |
|-----------|-------------------|-------|----------|
| <75W (slot only) | None | T4 (70W), L4 (72W) | YES |
| 150W | 1x 8-pin PCIe | A10 | YES |
| 165W | 1x 8-pin EPS | A30 | YES |
| 250W | 1x 8-pin | A16, A100 PCIe 40GB, V100 PCIe, V100S | YES |
| 300W | 1x 8-pin / 1x 16-pin | A40, A100 PCIe 80GB, L40, MI210, V100 SXM2 | YES |
| 350W | 1x 16-pin / 1x 8-pin | A100X, H100 PCIe, L40S | YES |
| 400-700W | SXM/OAM mezzanine | A100 SXM4, H100 SXM5, H200 SXM, V100 SXM2 | YES |
| 600W PCIe | 1x 16-pin | H200 NVL | YES |
| 600-750W OAM | OAM mezzanine | MI300X, Gaudi2 | YES |
| 900W module | Module connectors | GH200 | YES |

**No connector errors remain.**

### 3.9 MODERATE: Display Output Audit

Pure compute cards that should have NO display outputs:

| Card | Display Outputs Listed | Correct? |
|------|----------------------|----------|
| V100 PCIe | None | YES |
| V100 SXM2 | None | YES |
| V100S PCIe | None | YES |
| A100 PCIe | None | YES |
| A100 SXM4 | None | YES |
| A100X | None (has QSFP56 for network) | YES |
| A30 | None | YES |
| H100 PCIe | None | YES |
| H100 SXM5 | None | YES |
| H200 NVL | None | YES |
| H200 SXM | None | YES |
| T4 | None | YES |
| L4 | None | YES |
| Gaudi2 | None | YES |
| MI210 | None | YES |
| MI300X | None | YES |
| GH200 | None | YES |

Cards that SHOULD have display outputs:

| Card | Display Outputs Listed | Correct? |
|------|----------------------|----------|
| A10 | None listed | **ERROR** -- The A10 has 4x DisplayPort 1.4 outputs (per NVIDIA datasheet). Not mentioned in report. |
| A16 | None listed | YES -- A16 is a pure vGPU card with NO physical display outputs |
| A40 | 3x DisplayPort 1.4a | YES |
| L40 | 4x DisplayPort 1.4a | YES |
| L40S | 4x DisplayPort 1.4a | YES |

**ERROR FOUND: A10 report omits 4x DisplayPort 1.4 outputs.** The NVIDIA A10 datasheet confirms 4x DisplayPort 1.4. The report lists no display connectors. This is a component omission. Dollar impact on scrap: minimal (4x DP connectors add ~$0.50 gold in plating), but it is factually wrong.

---

## 4. Summary of Unfixed Issues from Prior Audits

| Issue | Status |
|-------|--------|
| Gaudi2 gold attributed to "bond wires" (0.04g) | UNFIXED -- text in Sec 3 GPU Die still references it as pad plating but total gold (0.12g) still includes it |
| H100 PCIe "wire bonds" in gold notes | UNFIXED |
| H200 NVL says "No wire bonds" but H200 NVL gold at 0.40g is 10x SXM | UNFIXED (gold quantity issue) |
| MI210 "Wire bonds" in gold notes | UNFIXED |
| H200 SXM 51% unaccounted weight | UNFIXED |
| A40 heatsink 74% of weight / 2% "Other" | UNFIXED |
| MI300X 12-phase for 750W underdocumented | UNFIXED |
| GH200 20-phase for 900W underdocumented | UNFIXED |
| L40 gold was 10x outlier | FIXED -- table now reads 0.05g |
| L40/L40S package weight inconsistency (10.4g vs 28g) | UNFIXED |

---

## 5. New Error Found This Audit

### 5.1 A10 Missing Display Outputs

The A10 report makes no mention of DisplayPort connectors anywhere in its component breakdown (Sec 3 Connectors), precious metals table, or weight breakdown. The NVIDIA A10 datasheet and product brief confirm 4x DisplayPort 1.4 outputs. These should be listed under Connectors with their gold plating contribution (~0.003-0.005g Au per DP connector, ~$1.50-$2.50 total gross gold).

### 5.2 A40 Gold Notes Reference "GPU bond wires" and "Au bond wires per chip"

The A40 report Section 3 states:
- GPU die: "trace gold from bond wires/bumps, ~0.005g Au"
- Memory: "trace Au bond wires per chip"

The GA102 uses flip-chip BGA packaging. GDDR6 chips also use BGA ball connections, not wire bonds. This is factually incorrect terminology. The gold amounts themselves (0.005g for GPU, small amounts per memory chip) are plausible for pad plating, but the "bond wires" label is wrong.

---

## 6. Final Error Count

| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 2 | H200 NVL/SXM gold 10x discrepancy; A100X BF2 "0.15g bond wires" claim |
| HIGH | 4 | H100 PCIe/SXM5 gold 5x discrepancy; H200 SXM 51% unaccounted weight; A40 weight budget; L40/L40S package weight inconsistency |
| MODERATE | 6 | Wire bond language on 6 reports (H100 PCIe, MI210, A40, V100S, V100 SXM2, A16); MI300X/GH200/Gaudi2 VRM phase documentation |
| LOW | 1 | A10 missing DisplayPort outputs |

**Total unique errors: 13** across 22 reports (0.6 per report average). None are catastrophic to the scrap valuations -- the dollar impact is concentrated in the gold quantity discrepancies between PCIe and SXM variants of the same die, which affects 4 reports.
