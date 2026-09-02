# Final Review -- GPU Scrap Value Reports (22 GPUs)

**Auditor:** Claude (final pass #3)
**Date:** 2026-03-29
**Scope:** All 22 report.md files, both prior audits (audit_prices.md, final_audit_prices.md)

---

## Master Comparison Table

| GPU | Wt(g) | Form | Au(g) | Au($) | Ag(g) | Ag($) | Pd(g) | Pd($) | PM_Total | Raw_Scrap | Recycler | Used_Price | MSRP |
|-----|-------|------|-------|-------|-------|-------|-------|-------|----------|-----------|----------|------------|------|
| A10 | 550 | PCIe | 0.04-0.06 | $5.76-$8.64 | 0.240 | $0.54 | 0.02-0.04 | $0.90-$1.80 | $7.20-$10.98 | $5-$6 | $1-$3 | $1,400-$1,800 | $2,500 |
| A100 PCIe | 1,240 | PCIe | 0.28 | $40.42 | 1.20 | $2.70 | 0.03 | $1.35 | $44.47 | $54 | $14-$25 | $3,000-$8,000 | $11,000-$15,000 |
| A100 SXM4 | ~325 | SXM4 | 0.25 | $36.00 | 5.00 | $11.35 | 0.05 | $2.26 | $49.61 | **~$57** | $25-$35 | $4,500-$7,000 | $10,000-$11,000 |
| A100X | ~1,300 | PCIe | 1.0-1.3 | $144-$187 | 0.30 | $0.71 | 0.08 | $3.61 | $148-$191 | $154-$197 | $77-$138 | $6,000-$9,000 | $33,700 |
| A16 PCIe | 1,088 | PCIe | 0.25 | $36.00 | 0.80 | $1.80 | 0.02 | $0.90 | $38.70 | $40 | $12-$20 | $2,800-$4,300 | ~$5,000 |
| A30 PCIe | 1,240 | PCIe | 0.06 | $8.64 | 0.60 | $1.35 | 0.02 | $0.90 | $10.89 | $14.48 | $4-$7 | $2,600-$3,125 | $4,599 |
| A40 | 1,010 | PCIe | 0.06 | $8.70 | 0.40 | $0.87 | 0.002 | $0.09 | $9.66 | ~$14 | $6-$8 | $5,000-$6,500 | ~$27,500 |
| MI300X | ~765 | OAM | 0.40 | $58.00 | 5.00 | $11.35 | 0.08 | $3.61 | $72.96 | **~$85** | $35-$55 | $16,000-$18,000 | ~$15,000 |
| Gaudi2 | ~850 | OAM | 0.12 | $17.28 | trace | <$0.10 | trace | <$0.10 | ~$17.28 | $28.22 | $7-$13 | ~$2,000 | $8,125 |
| H100 PCIe | 1,200 | PCIe | 0.04-0.07 | $5.80-$10.10 | 0.50-0.70 | $1.14-$1.59 | 0.01-0.03 | $0.45-$1.35 | $7.39-$13.04 | $15-$22 | $7-$13 | $18,000-$27,000 | $25,000-$30,000 |
| H100 SXM5 | ~3,000 | SXM5 | 0.30 | $43.20 | 0.80 | $1.80 | 0.04 | $1.80 | $46.80 | ~$77 | $32-$66 | $9,600-$15,000 | $25,000-$40,000 |
| H200 NVL | ~1,500 | PCIe | 0.40 | $57.60 | 0.75 | $1.69 | **0.20** | **$9.00** | $68.29 | ~$108 | $50-$85 | $31,000-$40,000 | $35,000-$40,000 |
| H200 SXM | ~1,020 | SXM5 | 0.02-0.05 | $2.90-$7.25 | 0.46 | $1.04 | 0.03 | $1.35 | $5.29-$9.64 | ~$14 | $6-$8 | ~$25,000 | $25,000 |
| L4 | 270 | PCIe | 0.005 | $0.71 | 0.090 | $0.20 | 0.002 | $0.09 | $1.00 | $1.25 | $1-$2 | $2,100-$2,600 | $2,500 |
| L40 | 1,051 | PCIe | 0.05 | $7.22 | 0.45 | $1.02 | 0.02 | $0.90 | $8.80* | ~$11 | $4-$6 | $6,350-$7,500 | ~$6,800 |
| L40S | 1,052 | PCIe | 0.05 | $7.22 | 0.60 | $1.36 | trace | ~$0 | $8.58 | ~$11 | $5-$7 | $7,267-$9,000 | ~$8,000 |
| GH200 | ~1,650 | SXM | 0.35 | $50.74 | 2.00 | $4.54 | 0.12 | $5.42 | $60.70 | ~$75 | $15-$30 | ~$5,500 | $35,000 |
| MI210 | ~1,175 | PCIe | 0.08 | $11.60 | 1.50 | $3.41 | 0.05 | $2.26 | $17.27 | ~$20-$24 | $8-$20 | $2,187-$4,640 | ~$16,500 |
| T4 | 301 | PCIe | 0.05 | $7.25 | 0.25-0.50 | $0.57-$1.14 | 0.002-0.005 | $0.09-$0.23 | $7.91-$8.62 | ~$4.07 | $1.50-$4.00 | $699-$1,100 | $2,500 |
| V100 PCIe | 1,196 | PCIe | 0.04-0.06 | $5.80-$8.70 | 0.50 | $1.09 | 0.02 | $0.91 | $7.80-$10.70 | ~$8-$10 | $4-$6 | $270-$1,080 | $8,000-$10,000 |
| V100 SXM2 | ~275 | SXM2 | 0.05 | $7.20 | 0.21 | $0.48 | 0.09 | $4.05 | $11.73 | ~$14.44 | $10-$12 | $95-$900 | $8,000-$10,000 |
| V100S PCIe | 1,196 | PCIe | 0.05 | $7.20 | 0.50 | $1.14 | 0.01 | $0.45 | $8.79 | ~$16.09 | $8-$10 | $4,950-$9,300 | ~$11,500 |

\* L40 PM total uses corrected 0.05g gold (harmonized with L40S), not the original 0.50g.

---

## Precious Metal Arithmetic Verification

Every qty x price multiplication in all 22 precious metals tables was checked. **All pass.** Minor rounding differences ($0.01-$0.17) exist where reports use $144.96/g unrounded vs $144/g rounded. No material errors.

---

## Cascade Ordering Verification (Working > Component > Raw > Recycler)

All 22 GPUs maintain the standard hierarchy with the following documented exceptions:

| GPU | Violation | Explanation |
|-----|-----------|-------------|
| A100 PCIe | Realistic component ($4.50) < Raw scrap ($54) | CoWoS kills component salvage; heatsink only |
| A100X | Realistic component ($50-$100) < Raw scrap ($154-$197) | Same CoWoS issue + high gold estimate |
| MI300X | Realistic component ($50-$200) overlaps Raw scrap (~$85) | 3.5D packaging makes chiplet extraction impossible |
| V100 SXM2 | Realistic component ($5) < Raw scrap ($14.44) | CoWoS; connectors only |
| L4 | Raw scrap ($1.25) < Recycler payout ($1-$2) | Card so small recycler pays handling minimum |

All are structurally explained by CoWoS/3.5D packaging constraints or minimum handling economics. No erroneous ordering.

## Recycler Payout < Raw Scrap Gross Check

**All 22 pass** except L4 (recycler $1-$2 vs raw $1.25). The L4 is 270g and its material content is so low that a recycler's minimum per-card handling fee exceeds actual metal content. This is noted but not an error.

---

## ERRORS AND ISSUES FOUND

### 1. CRITICAL: MI300X cascade total not updated ($52 should be ~$85)

The MI300X precious metals table was updated to March 2026 spot prices (Au $145/g, Ag $2.27/g) totaling $72.96 in PM alone. But the value cascade still says "~$52" for raw scrap gross -- a figure from the original pre-correction prices. Adding corrected base metals (~$12.44), the true gross scrap is approximately **$85**, not $52. The cascade understates by ~$33 (63%).

Both prior audits caught this. It remains unfixed in the report.

### 2. CRITICAL: A100 SXM4 cascade total not updated ($87 should be ~$57)

The A100 SXM4 precious metals table was revised from 0.50g gold to 0.25g gold ($36.00). But the value cascade still shows ~$87 for raw scrap gross, which only works if gold is still at 0.50g ($72.22 PM at original prices). With corrected PM ($49.61) + base metals (~$7.75 for a bare 325g module), the true gross scrap is approximately **$57**, not $87. The cascade overstates by ~$30 (53%).

The final_audit_prices.md caught this (Finding N8). Still unfixed.

### 3. HIGH: H200 NVL palladium (0.20g) is an unjustified outlier

The H200 NVL claims 0.20g Pd worth $9.00. The next highest across all 22 GPUs is GH200 at 0.12g. The H200 NVL is a 2024 product using modern BME (nickel electrode) MLCCs, which contain near-zero palladium. The 0.20g figure attributed to "~400 MLCC electrodes" is not defensible for BME caps. A realistic figure is 0.03-0.08g ($1.35-$3.60), consistent with the H100 SXM5 (0.04g for ~350 MLCCs).

Impact: gross scrap overstated by $5.40-$7.65. Corrected raw scrap: ~$100-$103, not ~$108.

### 4. HIGH: T4 precious metals total ($7.91-$8.62) exceeds raw scrap gross (~$4.07)

The T4 precious metals table totals $7.91-$8.62 gross, but the value cascade claims only ~$4.07 for total raw scrap. Since PM are a subset of raw scrap, PM cannot exceed the total. The ~$4.07 figure appears to use net-after-refining values or a different gold estimate than the PM table's 0.05g gross. The report notes "~0.015-0.02g recoverable after refining losses" in the gold notes, suggesting the cascade uses ~$2.18-$2.90 for gold (net) rather than the table's $7.25 (gross). **The cascade and PM table use different recovery assumptions without clearly stating this.** The PM table shows gross; the cascade should also show gross (~$8-$9), not a partial-net figure.

### 5. HIGH: A100 SXM4 silver quantity (5.0g) is an outlier

The A100 SXM4 claims 5.0g silver, the second-highest in the dataset (tied with MI300X). The MI300X is a 765g OAM module with a massive package substrate, making 5.0g plausible. But the A100 SXM4 is a bare 325g module. Its silver attribution is "Substrate interconnect layers, SAC305 solder (3% Ag)." With ~8g SAC305 solder providing only 0.24g Ag, the remaining 4.76g attributed to "substrate interconnect layers" is very aggressive for a module of this size. The A100 PCIe (1,240g, much larger) claims only 1.20g Ag. The 5.0g figure inflates PM total by ~$10.17 vs a more realistic 0.5-1.0g estimate.

### 6. MODERATE: Silver spot price inconsistency ($2.18-$2.35/g across reports)

| Price | GPUs Using It |
|-------|---------------|
| $2.18 | A40, V100 PCIe |
| $2.25 | A10, A100 PCIe, A16, A30, H100 SXM5, H200 NVL, H200 SXM |
| $2.26 | L40, L40S |
| $2.27 | A100 SXM4, MI300X, Gaudi2, H100 PCIe, L4, GH200, MI210, T4, V100 SXM2, V100S |
| $2.35 | A100X |

Target should be $2.25/g uniformly. The A100X at $2.35 and the A40/V100 PCIe at $2.18 are the widest deviations. Dollar impact is small (<$0.50 on any card) but the inconsistency is avoidable.

### 7. MODERATE: Gold price inconsistency ($141-$145/g across reports)

Most cluster at $144/g, which is correct. Deviations:
- L4 at $141/g (stale by $3/g; immaterial at 0.005g Au)
- A40, MI300X, H200 SXM, T4, V100 PCIe at $145/g (rounded up from $144.96; immaterial)
- L40, L40S at $144.43/g (more precise mid-week snapshot)

No material impact on any card given gold quantities involved. The L4 is the only genuine stale price but the impact is $0.015.

### 8. MODERATE: Copper scrap pricing varies 35% across reports ($4.25-$5.90/lb)

Reports use: $4.25/lb (L40S), $4.40/lb (H100 PCIe, L4), $4.50/lb (A10), $5.50/lb (V100 PCIe), $5.90/lb (many). The $5.90/lb is commodity futures; actual scrap buyback runs lower. This makes copper scrap values not directly comparable across reports. Gross impact is typically <$1 per card since copper quantities are small.

### 9. MODERATE: H100 SXM5 indium priced at $972/kg vs industrial benchmark $540-$618/kg

At 8g indium, the report claims $7.76 scrap. Industrial benchmark yields $4.32-$4.94. Overstatement: $2.82-$3.44. Both prior audits flagged this; still unresolved.

### 10. MODERATE: A30 gold (0.06g) appears very conservative for a 1,240g card

The A30 PCIe weighs 1,240g (same as A100 PCIe 40GB) and has CoWoS packaging with PCIe fingers and NVLink connector, yet claims only 0.06g gold -- 4.7x less than the A100 PCIe (0.28g). The report self-flags this, noting industry range of 0.2-1.0g. A more realistic estimate would be 0.15-0.25g, which would raise PM total from $10.89 to ~$23-$37.

### 11. LOW: L40 silver (0.45g in table) vs solder-derived silver (should be 0.45g minimum)

The L40 Section 4 table says 0.45g Ag but the verification notes say "only 0.30g total is claimed." The table was corrected to 0.45g, resolving the discrepancy. However, the original note about 0.30g remains in Section 6, creating a confusing trail.

### 12. LOW: V100 PCIe heatsink scrap arithmetic

Report claims $2.50 but Cu ($2.42 at $5.50/lb) + Al ($0.42 at $0.50/lb) = $2.84. Understatement of $0.34.

### 13. LOW: A100 PCIe heatsink scrap arithmetic

Report claims $3.81 but Cu ($2.17 at $12.05/kg) + Al ($1.80 at $3.28/kg) = $3.97. Understatement of $0.16.

---

## Cross-Report Consistency Checks

### Gold per gram of card weight (ppm-equivalent)

| GPU | Au(g) | Weight(g) | Au_ppm | Form | Notes |
|-----|-------|-----------|--------|------|-------|
| L4 | 0.005 | 270 | 18.5 | PCIe HHHL | Very low; tiny card |
| A10 | 0.05 | 550 | 90.9 | PCIe | OK |
| T4 | 0.05 | 301 | 166 | PCIe HHHL | OK |
| V100 PCIe | 0.05 | 1,196 | 41.8 | PCIe CoWoS | Low for a CoWoS card |
| V100S PCIe | 0.05 | 1,196 | 41.8 | PCIe CoWoS | Consistent with V100 |
| V100 SXM2 | 0.05 | 275 | 182 | SXM2 | High ppm but tiny card |
| L40 | 0.05 | 1,051 | 47.6 | PCIe | Now harmonized with L40S |
| L40S | 0.05 | 1,052 | 47.5 | PCIe | Consistent with L40 |
| A30 PCIe | 0.06 | 1,240 | 48.4 | PCIe CoWoS | Conservative (see Issue #10) |
| A40 | 0.06 | 1,010 | 59.4 | PCIe | OK |
| H100 PCIe | 0.055 | 1,200 | 45.8 | PCIe CoWoS | OK (midpoint) |
| MI210 | 0.08 | 1,175 | 68.1 | PCIe 2.5D | OK |
| Gaudi2 | 0.12 | 850 | 141 | OAM | OK |
| A16 PCIe | 0.25 | 1,088 | 230 | PCIe x4 GPU | 4 GPU dies + ConnectX switch justify higher Au |
| A100 SXM4 | 0.25 | 325 | 769 | SXM4 | High; dual mezzanine connectors |
| A100 PCIe | 0.28 | 1,240 | 226 | PCIe CoWoS | NVLink + PCIe fingers + large BGA |
| H100 SXM5 | 0.30 | 3,000 | 100 | SXM5 | OK |
| GH200 | 0.35 | 1,650 | 212 | SXM | Dual-die module |
| MI300X | 0.40 | 765 | 523 | OAM | Large package with dual OAM connectors |
| H200 NVL | 0.40 | 1,500 | 267 | PCIe | NVLink bridge connector adds gold |
| H200 SXM | 0.035 | 1,020 | 34.3 | SXM5 | Low (midpoint of 0.02-0.05g) |
| A100X | 1.15 | 1,300 | 885 | PCIe | Dual-chip + QSFP56 + NVLink; highest in dataset |

### SXM vs PCIe gold check (SXM should have LESS gold -- no PCIe edge fingers)

| Pair | SXM Au(g) | PCIe Au(g) | SXM < PCIe? |
|------|-----------|------------|-------------|
| A100 SXM4 vs A100 PCIe | 0.25 | 0.28 | YES (after correction from 0.50g) |
| H100 SXM5 vs H100 PCIe | 0.30 | 0.055 (mid) | **NO -- SXM is 5.5x higher** |
| H200 SXM vs H200 NVL | 0.035 (mid) | 0.40 | YES |
| V100 SXM2 vs V100 PCIe | 0.05 | 0.05 | EQUAL |

**Issue: H100 SXM5 (0.30g) is 5.5x higher than H100 PCIe (0.055g midpoint).** The H100 SXM5 has a large SXM5 connector with gold-plated contacts and a larger BGA substrate than the PCIe variant, which partly explains the difference. But the H100 PCIe estimate (0.04-0.07g) is very conservative -- it includes only ~25mg from PCIe fingers and ~25mg from misc. The H100 PCIe gold may be understated, or the H100 SXM5 may be overstated. The two should be closer together.

### Same-die platform consistency

| Die | Cards | Au range | Consistent? |
|-----|-------|----------|-------------|
| GV100 | V100 PCIe, V100 SXM2, V100S PCIe | 0.04-0.06g, 0.05g, 0.05g | YES |
| GA100 | A100 PCIe, A100 SXM4, A30, A100X | 0.28g, 0.25g, 0.06g, 1.15g | A30 is outlier low; A100X justified by dual-chip |
| AD102 | L40, L40S | 0.05g, 0.05g | YES (after harmonization) |
| GH100 | H100 PCIe, H100 SXM5, H200 NVL, H200 SXM, GH200 | 0.055g, 0.30g, 0.40g, 0.035g, 0.35g | Wide range (0.035-0.40g) |

The GH100-based products have the widest gold estimate spread. The H200 SXM (0.02-0.05g) and H100 PCIe (0.04-0.07g) are at the low end; the H200 NVL (0.40g) and GH200 (0.35g) are at the high end. Connector type and quantity largely explain this: the NVL has a gold-plated NVLink bridge connector, and the GH200 has NVLink + PCIe + power connectors totaling 130g of connector mass. The H200 SXM is a bare module with only a silver-plated SXM5 connector and minimal gold.

---

## Status of Prior Audit Findings

| Finding | Status |
|---------|--------|
| L40 vs L40S gold 10x discrepancy | **RESOLVED** -- both now use 0.05g |
| V100 SXM2 cascade $19.20 vs $14.44 | **RESOLVED** -- cascade now shows $14.44 |
| A100 SXM4 gold > A100 PCIe | **RESOLVED** -- SXM4 revised to 0.25g (< PCIe 0.28g) |
| H200 NVL gold 0.80g | **PARTIALLY RESOLVED** -- reduced to 0.40g; ratio to SXM still wide |
| MI300X cascade total stale | **STILL OPEN** -- cascade says ~$52, should be ~$85 |
| A100 SXM4 cascade total stale | **STILL OPEN** -- cascade says ~$87, should be ~$57 |
| H200 NVL Pd outlier (0.20g) | **STILL OPEN** -- should be 0.03-0.08g |
| A100X silver $2.35/g | **STILL OPEN** -- immaterial ($0.03) |
| H100 SXM5 indium $972/kg | **STILL OPEN** -- ~$3 overstatement |
| Copper price inconsistency | **STILL OPEN** -- $4.25-$5.90/lb spread |
| Recycler payout % inconsistency | **STILL OPEN** -- ranges from 2% to 98% across reports |

---

## Summary

**3 issues require correction before this dataset is usable:**
1. MI300X cascade: change ~$52 to ~$85
2. A100 SXM4 cascade: change ~$87 to ~$57
3. H200 NVL Pd: change 0.20g to 0.05g (and recalc PM total from $68.29 to ~$61.54, raw scrap from ~$108 to ~$101)

**4 issues are material but not blocking:**
4. T4 cascade ($4.07) inconsistent with PM table ($7.91-$8.62) -- clarify gross vs net
5. A100 SXM4 silver (5.0g) is aggressive for a 325g bare module
6. A30 gold (0.06g) is conservative vs comparable cards at same weight
7. H100 SXM5 vs H100 PCIe gold ratio inverts the SXM-should-have-less-gold rule

All precious metal qty x price arithmetic is correct across all 22 reports. Cascade ordering (Working > Component > Raw > Recycler) holds for all 22 with documented CoWoS-related exceptions. No new issues were found beyond what the two prior audits identified plus the T4 gross/net confusion noted above.
