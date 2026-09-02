# Bloomberg Data Sources for Model Optimisation

## Priority 1 — Electricity Prices by Country (TCO Analysis)

**What:** Industrial/commercial electricity rates ($/kWh) by country, monthly.
**Why:** Enables full TCO ranking. The dataset already has `country` on every row. Joining $/kWh per country lets us compute:
  `5yr_TCO = purchase_price + (TDP_watts / 1000 × 43,800 hrs × $/kWh) - resale_value`
  A GPU ranked 10th by depreciation alone could be ranked 1st by TCO if it draws 400W vs a competitor at 150W.

**Bloomberg fields:**
- ~~BFIX~~ (BFIX is Bloomberg's FX fixing benchmark, not a power price product — disregard)
- EIA US industrial electricity price (US only, very granular) — **free, no Bloomberg needed**
- Eurostat nrg_pc_204 semi-annual industrial rates for EU/UK — **free API**
- IEA World Energy Prices (annual, broad country coverage) — free annual PDF; industrial tier is paywalled

**Coverage needed:** US, DE, UK, JP, FR, CA, IT, ES (matches our 9 Keepa marketplaces).
**Frequency:** Monthly or quarterly is sufficient.

**Additional data needed (not Bloomberg):**
- GPU TDP (watts) per model — from TechPowerUp GPU database (free, can scrape or hardcode).

---

## Priority 2 — Cloud Capex Quarterly (Demand Shock Timing)

**Status:** Cloud GPU rental pricing has been partially addressed. `extract_cloud_pricing.py` processes a historical cloud pricing database (2015–2024) and produces `data/cloud_pricing_monthly.csv` with monthly median rental rates ($/hr) per GPU. `scrape_vastai.py` queries the Vast.ai public API for current GPU rental pricing and produces `data/vastai_pricing.csv`. These provide the cloud rental rate signal; what remains is the upstream hyperscaler capex data below.

**What:** Cloud infrastructure capital expenditure by hyperscaler, quarterly.
**Why:** The cloud compute pricing CSV already shows that DC pricing leads consumer GPU prices by 1–6 months. Cloud capex announcements are one step upstream — they signal when DC GPU purchasing is ramping, which drives DC cloud pricing, which then moves consumer prices.
  Specifically: large GPU procurement announcements (Microsoft/Azure, Google/GCP, Meta, Amazon/AWS) explain the H100/H200 scarcity at 12–13x MSRP.

**Bloomberg fields:**
- `MSFT US Equity CF_CAP_EXPENDITURE` — Microsoft quarterly capex
- `GOOGL US Equity CF_CAP_EXPENDITURE` — Alphabet
- `META US Equity CF_CAP_EXPENDITURE` — Meta
- `AMZN US Equity CF_CAP_EXPENDITURE` — Amazon
- `NVDA US Equity` — NVIDIA earnings/revenue by segment (data center vs gaming)

**Coverage needed:** Q1 2020 – present (covers AI capex surge period).

---

## Priority 3 — NVIDIA/AMD Product Announcement Dates

**What:** Exact dates of product announcement and product launch for each GPU model.
**Why:** GPU prices drop 20–40% when the successor generation is announced. This discrete
event is already accounted for in the pipeline: a `SUCCESSOR_DATES` dict in `data_prep.py`
maps each GPU to the date its successor was publicly announced (50 entries covering all
major consumer, workstation, and datacenter generations). The pipeline tags
`successor_announced` and `months_since_successor_announced` on every observation, and
`depreciation_curves.py` uses only pre-announcement data for k estimation when sufficient
pre-announcement history exists. Bloomberg data for this priority is therefore **not needed**
unless finer-grained intra-day announcement timing is desired.

**Note:** The `SUCCESSOR_DATES` dict already covers the relevant announcements. Example entries:
- RTX 40-series announced Sep 2022 → RTX 30-series prices drop
- RTX 50-series announced Jan 2025 → RTX 40-series prices drop

---

## Priority 4 — Bitcoin & Ethereum Price History

**What:** BTC and ETH daily close prices.
**Why:** Consumer GPU demand spikes (RTX 30-series at 1.5–2x MSRP in 2020–2022) are driven by crypto mining profitability. Adding crypto price as a covariate to the demand shock model allows decomposition of:
  - Crypto-driven premium (temporary, tied to BTC/ETH cycle)
  - Genuine scarcity premium (structural)

**Bloomberg fields:**
- `XBT Curncy` — Bitcoin USD
- `ETH Curncy` — Ethereum USD

**Coverage needed:** Jan 2020 – present.

**Note:** The Keepa DB already captures the *effect* of crypto cycles in historical price data (RTX 3060/3070 price spikes 2020–2022 are fully visible). Crypto prices would only add value if building a causal/predictive model for future demand shocks.

---

## Priority 5 — HBM / DRAM Spot Prices

**What:** High Bandwidth Memory (HBM2e/HBM3) and GDDR6 spot prices.
**Why:** A100/H100 use HBM which has a separate supply chain from GDDR. HBM price spikes affect GPU margins and can explain secondary market behaviour for datacenter cards. GDDR6 prices affect consumer GPU pricing.

**Bloomberg fields:**
- DRAMeXchange via Bloomberg commodity data
- `MEMRY Index` (if available) — memory chip pricing index

**Note:** HBM data is thin on Bloomberg; TrendForce or DRAMeXchange may be better sources.

---

## Not Worth Pulling

| Dataset | Reason to skip |
|---------|----------------|
| Semiconductor index (SOXX) | Too broad; NVIDIA-dominated anyway |
| NVIDIA stock price | Correlated with everything; no independent signal above what DC cloud pricing gives |
| Freight/shipping rates (BDIY) | Too many steps removed from GPU prices |
| Data center REIT index | Useful for capacity forecasting but too indirect for price modeling |

---

## Implementation Notes

When Bloomberg data arrives, the join key for electricity prices is `country` (already in the retail CSVs). For cloud capex, the join key is `date` (quarterly). For crypto prices, the join key is `date` (daily → downsample to monthly).

When external data is added, it should be loaded through the existing
pipeline infrastructure (e.g. `data_prep.py`'s `load_datacenter_supplement()`
for secondary-market data, or new loader functions as needed) rather than
creating a separate module.
