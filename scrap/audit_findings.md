# Scrap Folder Audit — Consolidated Findings (22 Datacenter GPUs)

**Date:** 2026-03-29
**Scope:** All 22 GPU subdirectories in `scrap/`, auditing `components.csv` and `report.md` for math errors, internal consistency, factual accuracy, and cross-report issues.

---

## Systemic Issues (Affect Most or All GPUs)

- **CSV files were never updated after report revisions.** This is the single largest problem across the entire dataset. Every GPU that underwent precious metals corrections (gold, silver, palladium) in its report.md still carries the old, discredited values in components.csv. Affected GPUs: A100 PCIe, A100 SXM4, A100X, MI300X, H100 SXM5, H200 NVL, GH200, L40, A30, MI210, and others. In some cases the CSV overstates gold by 10-25x.

- **CSV column semantics (per-unit vs total) are inconsistent and undocumented.** The `secondary_market_value_usd` and `raw_material_scrap_value_usd` columns sometimes contain per-unit values (multiply by qty to get total) and sometimes contain pre-computed totals for the row. This varies *within the same file*. Affected: A40, L40S, H200 SXM, H200 NVL, Gaudi2, A16 PCIe, and others. Anyone consuming these CSVs programmatically will get wrong totals.

- **Every report skips Section 9.** All 22 reports jump from Section 8 to Section 10, or have sections out of order. This is a universal template artifact.

- **Palladium in modern BME MLCCs was corrected in some reports but not others.** The finding that modern Base Metal Electrode MLCCs contain zero palladium was applied to A100 SXM4, H100 SXM5, GH200, MI300X, and others, but NOT to V100 SXM2 (still 0.09g), H200 NVL CSV (still 0.20g), or A16 PCIe. This creates cross-report inconsistency.

- **Multiple contradictory "theoretical max" figures within single reports.** Most reports have a Section 5 cascade with one theoretical max (including HBM/die at full value) and a Section 10.1 "grounded" ceiling (zeroing CoWoS-bonded HBM). These coexist without reconciliation. In some cases (H200 SXM, A30), the "realistic" salvage estimate exceeds the "theoretical max ceiling."

- **Copper scrap pricing varies 35% across reports ($4.25-$5.90/lb)** without consistent justification. Silver spot price varies $2.18-$2.35/g (target: $2.25/g). Gold varies $141-$145/g. These make cross-GPU comparisons unreliable.

---

## Per-GPU Findings

### NVIDIA A10
- [MODERATE] CSV heatsink weight (280g) not updated to match report (250g)
- [MODERATE] CSV gold price still references $100/g (should be $144/g)
- [MODERATE] CSV Pd in decoupling caps (90mg) contradicts report (5mg); BME correction not applied to CSV
- [MODERATE] Solder recovery math error: $0.37 stated but 50% of $0.91 = $0.455
- [MODERATE] CSV raw scrap total (~$4.50) doesn't match report's $10-$12 range
- [LOW] Copper scrap price understated at $4.25/lb
- [LOW] Tin price elevated at $45.79/kg vs ~$30-35/kg market

### NVIDIA A100 PCIe (40/80 GB)
- [CRITICAL] CSV gold (0.28g/$40.42) never updated to match report revision (0.06g/$8.64) — 4.7x overstatement
- [CRITICAL] CSV raw scrap totals ($54/$51) not updated to match report (~$22/$19)
- [CRITICAL] CSV and report fundamentally out of sync on all precious metals
- [HIGH] CSV silver (1.20g) contradicts report (0.86g)
- [HIGH] CSV palladium (0.03g) contradicts report (0.005g) — 6x overstatement
- [LOW] GPU die weight in CSV (15g) conflates bare die (~1.5g) with full CoWoS package

### NVIDIA A100 SXM4 80 GB
- [CRITICAL] CSV gold (0.15g/$21.60) never updated to report's 0.02g/$2.88 — 7.5x
- [CRITICAL] CSV silver (5.0g/$11.35) never updated to report's 0.28g/$0.63 — 18x
- [CRITICAL] CSV palladium (0.05g/$2.26) never updated to report's 0.005g/$0.23 — 10x
- [HIGH] Three unreconciled revision layers in the report (original, first revision, final revision)
- [HIGH] Section 9 "Corrections Made" references intermediate figures, not final ones
- [MODERATE] Raw scrap ~$24 in cascade not reproducible from report's revised PM (~$3.74) + base metals (~$5)

### NVIDIA A100X
- [CRITICAL] CSV gold estimates stale by 15-25x (notes sum to ~1.3g, report says 0.04-0.06g)
- [CRITICAL] HBM2e weight in report table wrong by 42x (0.5g stated vs 21g actual)
- [CRITICAL] Raw scrap total inconsistent across three report sections ($16-19, $13-16, CSV $34.64)
- [HIGH] TIM scrap in CSV ($0.20) contradicts report ($3.30) — 16x undercount
- [HIGH] Gold range in report (0.04-0.06g) exceeds project calibration upper bound (0.040g)
- [HIGH] PCB copper note says "$1.06/g" — misleading (that's per gram of board, not copper)

### NVIDIA A16 PCIe
- [CRITICAL] Weight breakdown percentages sum to 118.3%, not 100%
- [HIGH] Duplicate Sections 9 and 10 with conflicting realistic ranges ($860 vs $1,075)
- [HIGH] Raw scrap total ($40) irreconcilable with CSV sum ($11.18) or CSV+PM ($48.72)
- [MODERATE] VRM raw scrap understated by ~$2.84 ($1.32 reported vs $4.16 from CSV)
- [MODERATE] Gold spot $141/g in CSV vs $144/g in report body

### NVIDIA A30 PCIe
- [HIGH] Duplicate contradictory Scrap Value Scenarios (Section 9: ~$29, Section 10: ~$41)
- [HIGH] Three different "theoretical max" figures ($29, $41, $61.50) in same report
- [HIGH] Recycler payout ranges don't overlap ($6-$9 in Section 5 vs $18-$35 in Section 10.2)
- [HIGH] Palladium CSV (0.02g) not updated to match report (0.005g)
- [MODERATE] Connector scrap subtotals in report stale ($1.33 vs CSV $2.19)
- [MODERATE] Silver: report says 0.60g, CSV only has 0.15g (solder Ag missing from CSV)

### NVIDIA A40
- [CRITICAL] Solder Ag calculation off by 10x ($0.08 stated in note vs $0.785 actual)
- [CRITICAL] Raw scrap total (~$14) unreproducible from CSV under any interpretation
- [CRITICAL] CSV value columns ambiguous (per-unit vs per-row) — memory appears per-unit ($3.50/chip) while everything else is per-group
- [CRITICAL] CSV total weight (1,038g) doesn't match report (1,010g)
- [HIGH] Silver spot $2.18/g in PM table vs $2.25/g in sources section
- [HIGH] DP connector gold content (0.009g=$1.31) vs scrap value ($0.18) — 7x gap
- [MODERATE] Heatsink scrap misquoted in Section 7 ($0.94 vs $3.18 in Section 3)
- [MODERATE] MSRP uses OEM price ($27,500) not NVIDIA reference (~$5,000)

### AMD Instinct MI300X
- [CRITICAL] CSV gold (0.40g/$56.80) never updated to report's 0.02-0.03g/$2.90-$4.35 — 13-20x
- [CRITICAL] CSV silver (5.0g/$8.58) never updated to report's 0.15g/$0.34 — 33x
- [CRITICAL] CSV palladium (0.08g/$2.53) never updated to report's 0.005g/$0.23 — 16x
- [CRITICAL] Three-way cascade disagreement (report $30-31, final_review $85, revised calc $15-20)
- [HIGH] Gold recovery factor inconsistently applied in CSV (Ag/Pd get 70%, Au gets 0% discount)
- [HIGH] Report Section 7 still references old silver figure ($11.35 from 5.0g)
- [HIGH] Recovery rate note impossible: "$5-6 net" from "$3.47-$4.92 gross" (net > gross)

### Intel Gaudi2 HL-225H
- [CRITICAL] Connector gold scrap ($1.80) is 3x less than gold content alone ($5.76 for 0.04g Au)
- [HIGH] CSV total weight (~800g) doesn't match report (850g) — 50g gap
- [HIGH] Indium TIM price stale in CSV ($0.10 vs report's corrected $0.31)
- [HIGH] CSV column semantics inconsistent (secondary per-unit, scrap pre-totaled)
- [MODERATE] Heatsink scrap ($3.50) implies $4.53/lb — doesn't match stated $0.45/lb aluminum rate (10x error)
- [MODERATE] PCB scrap value differs CSV ($4.50) vs report ($4.38)

### NVIDIA H100 PCIe (80/94 GB)
- [HIGH] Heatsink scrap in CSV ($6.30) is 2x the calculated value ($3.11)
- [HIGH] Copper cross-reference row math wrong ($5.20 for 120g, should be ~$1.16)
- [HIGH] Section 5 theoretical salvage ($2,157) contradicts Section 10.1 ($956) — HBM not reconciled
- [HIGH] final_review.md H100 SXM5 gold comparison is stale (uses pre-revision 0.30g)
- [MODERATE] PCB gold weight column (0.05g) contradicts notes (25mg=0.025g)
- [MODERATE] Solder scrap value ($0.45) appears to be silver mass entered as dollars

### NVIDIA H100 SXM5
- [CRITICAL] CSV gold (0.30g/$42.31) never updated to report's 0.025g/$3.62 — 12x
- [CRITICAL] CSV silver (0.80g/$1.75) never updated to report's 0.42g/$0.95 — 2x
- [HIGH] CSV palladium (0.04g/$1.81) not updated to report's 0.005g/$0.23 — 8x
- [HIGH] CSV indium price stale ($0.97/g vs $0.62/g industrial benchmark) — $2.80 overstatement
- [HIGH] VRM secondary $176 (CSV calculation) vs $165 (report) — $11 gap never explained
- [MODERATE] Raw scrap ~$37 appears stale vs reconstructed ~$46 from corrected values
- [MODERATE] Two contradictory theoretical max figures ($2,310 vs $1,107)

### NVIDIA H200 NVL
- [HIGH] CSV Pd (0.20g/$8.00) not updated to report's 0.005g/$0.23 — confirmed outlier
- [HIGH] Heatsink weight: three conflicting values (CSV 650g, Section 2 table 530g, Section 3 text 650g)
- [HIGH] CSV total weight (~1,587g) far exceeds report's ~1,260g
- [HIGH] "Realistic" component salvage ($1,168-$1,946) exceeds "theoretical max ceiling" ($572-$1,057)
- [HIGH] Component salvage total ($7,785) not reproducible from Section 3 values (~$7,555)
- [HIGH] Heatsink raw scrap overstated ($5.50 vs ~$3.10 calculated)
- [MODERATE] CSV silver data stale ($33/oz and 0.75g vs report's $70/oz and 0.52g)

### NVIDIA H200 SXM
- [CRITICAL] CSV schema ambiguity: VRM inductor scrap looks per-unit ($2.72 x 29 = $79) but is actually total
- [HIGH] Module total scrap ($12.04) doesn't reconcile with CSV sum ($13.71) either way
- [HIGH] Pd: three conflicting values (CSV capacitor line 0.03g, PM table 0.005g, BME MLCCs = zero)
- [HIGH] Value cascade "realistic" ($1,000) exceeds Section 10.1 "theoretical max" ($537-$867)
- [MODERATE] Indium TIM price stale in CSV ($0.97/g vs report's $0.62/g)
- [MODERATE] Section 10.1 theoretical max ($2,500) includes CoWoS-bonded HBM ($1,800-$2,520) that Section 10.1 zeros out

### NVIDIA L4
- [HIGH] CSV PCB scrap has grams entered as dollars ($1.65 should be ~$0.02)
- [HIGH] CSV heatsink scrap wrong ($0.07 should be $0.15)
- [HIGH] Gold price: calculations use $141/g but report's own sources cite $144.96/g
- [HIGH] Recycler payout contradicts: report $0.50-$0.75 vs final_review $1-$2
- [HIGH] CSV stale — known corrections never applied
- [MODERATE] Corrected raw scrap ($1.25) not reproducible from component sums ($1.08)

### NVIDIA L40
- [CRITICAL] Pd: CSV (0.02g/$0.45) contradicts report (0.005g/$0.23) — correction not applied to CSV
- [HIGH] Report Section 7 claims heatsink scrap "$0.94" — actual is $2.82 (3x error)
- [HIGH] Report Section 7 cites "$43 from raw material recovery" — no such figure exists anywhere
- [HIGH] Edge connector gold: Section 3 says 0.04g, CSV and PM table say 0.02g
- [MODERATE] Section 6 stale silver note still references old "0.30g" value
- [MODERATE] VRAM CSV notes imply 0.36g Au from VRAM alone, contradicting 0.05g total

### NVIDIA L40S
- [CRITICAL] Component salvage total doesn't reconcile ($405 vs CSV-derived $417 — $12 gap from omitted inductor resale)
- [CRITICAL] CSV per-unit vs total convention inconsistent within same file
- [HIGH] Raw scrap total (~$13) not derivable from CSV without knowing the convention
- [HIGH] Edge connector gold: CSV ($1.15) vs report ($1.10) — CSV math is correct ($0.008g x $144 = $1.15)
- [HIGH] Report VRM secondary omits inductor resale ($12 total, explaining the $405 vs $417 gap)
- [MODERATE] "Other" raw scrap ($0.35) contradicted by solder line alone ($1.22)
- [MODERATE] Potential double-count of silver between solder line ($1.22) and PM table ($1.36)

### NVIDIA GH200
- [CRITICAL] CSV gold (0.35g/$50.74) not updated to report's 0.035g/$5.07 — 10x
- [CRITICAL] CSV palladium (0.12g/$5.42) not updated to report's 0.005g/$0.23 — 24x
- [CRITICAL] CSV silver (2.0g/$4.54) not updated to report's 1.20g/$2.70
- [HIGH] Report scrap total (~$24) doesn't reconcile with corrected calc (~$27) — $3 gap
- [HIGH] Section 5 theoretical salvage ($1,810) includes $600 non-separable HBM
- [HIGH] Gold 0.035g still above project calibration upper bound (0.028g)
- [MODERATE] Interposer scrap ($0.63) is ~97x the copper content value ($0.0065)

### AMD Radeon Instinct MI210
- [CRITICAL] Silver mass in CSV (1.5g/$3.27) matches no stated quantity; report says 0.45g/$1.01
- [CRITICAL] Gold scrap value wrong in CSV ($11.27 vs $11.60 correct — 0.08g x $144.96)
- [CRITICAL] CSV total scrap (~$21.13) contradicts report's ~$17-18
- [HIGH] TIM scrap value inconsistent: CSV says $0.93 for 2g, but $0.93 = 1.5g x $0.62
- [HIGH] Value cascade $344 theoretical max contradicts Section 10.1 $194 ceiling
- [HIGH] CSV HBM2e secondary ($120) not zeroed despite EFB inseparability
- [MODERATE] PCIe edge connector scrap ($0.35) is 4-10x below stated recovery math

### NVIDIA T4
- [CRITICAL] Cascade raw scrap ($8-$9 gross) vs CSV sum ($4.25) — incompatible recovery assumptions
- [HIGH] Solder mass contradiction: CSV says 8g, PM table says 3-4g
- [HIGH] Final review uses stale T4 silver figures (0.25-0.50g vs report's corrected 0.12g)
- [HIGH] GDDR6 secondary value ambiguous ($3.50 per chip or per set?)
- [MODERATE] PM table total ($7.61) reports only low-end Pd without noting it's a range
- [MODERATE] Copper scrap pricing inconsistent within same report

### Tesla V100 PCIe (16/32 GB)
- [HIGH] Heatsink scrap understated: $2.50 claimed vs $2.84 calculated (Cu $2.42 + Al $0.42)
- [HIGH] Silver: CSV 0.50g contradicts report's corrected 0.31g
- [HIGH] Gold mass in PM table conflates gross content (0.15g) with recoverable (0.04-0.06g)
- [MODERATE] CSV scrap total (~$8.58) doesn't match cascade ($13-15)
- [MODERATE] Copper scrap at $5.50/lb vs $5.90/lb elsewhere

### Tesla V100 SXM2 (16/32 GB)
- [CRITICAL] Palladium at 0.09g is 18x the corrected A100 SXM4 value — BME correction never applied
- [HIGH] Tantalum cap Pd contribution (0.01g) based on Au/Pd plating, but modern POSCAPs use tin plating
- [MODERATE] CSV total scrap (~$21) vs report's ~$13.40 — structural double-counting in CSV
- [MODERATE] NVLink gold: CSV says 0.015g, gold budget says 0.005g — 3x discrepancy
- [LOW] SAC305 described as 2% Ag (should be 3%) — understates solder silver by ~38%

### Tesla V100S PCIe 32 GB
- [HIGH] $159 theoretical salvage contradicted by Section 10.1 ($59) — HBM included then excluded
- [HIGH] PCIe gold finger Au: V100S (0.017g) vs V100 PCIe (0.12g) — 7x for identical connectors
- [HIGH] Silver not harmonized across V100 family (V100S 0.28g vs V100 PCIe 0.31g for "identical" boards)
- [HIGH] Gold (0.05g) flagged as ~2x too high by project's own gold calibration
- [MODERATE] PCB scrap ($5.50) doesn't match engineering calc ($2.50-$2.92)
- [MODERATE] CSV scrap total (~$27.17) vs report ($15.58) — ambiguous per-unit/total convention

---

## Top Priority Fixes

1. **Update all 22 components.csv files** to match report.md corrected precious metals values
2. **Standardize CSV column semantics** — add a column or header note specifying per-unit vs total
3. **Reconcile Section 5 cascades with Section 10 grounded analyses** — pick one theoretical max definition
4. **Apply BME MLCC palladium correction** to V100 SXM2 (0.09g), H200 NVL CSV (0.20g), A16 PCIe, and any others still using PME assumptions
5. **Standardize metal spot prices** across all 22 reports: Au $145/g, Ag $2.25/g, Pd $45/g, Cu scrap $5.90/lb
6. **Fix Section 9/10 numbering** across all reports
