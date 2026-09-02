"""
data_prep.py
Load, clean, validate, and annotate all three GPU price CSVs.
Implements: MSRP integrity check, launch-date time origin,
            successor-announcement tagging, ADF stationarity,
            demand-shock flagging, optional datacenter supplement loading.
Import load_data() from other scripts.
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller

# ── GPU launch dates (TechPowerUp reference) ─────────────────────────────────
LAUNCH_DATES = {
    "Quadro P5000":               "2016-08-01",
    # V100 SXM2: bare modules need $200 adapter — carrier-cost adjusted in pipeline
    # V100 FHHL: remapped to PCIe 16GB via GPU_NAME_ALIASES (same die, same market)
    "Tesla V100 SXM2 16 GB":      "2017-06-01",
    "Tesla V100 PCIe 16 GB":      "2017-06-01",
    "Tesla V100 SXM2 32 GB":      "2018-03-01",
    "Tesla V100 PCIe 32 GB":      "2018-03-01",
    "Quadro RTX 4000":            "2018-11-01",
    "Quadro RTX 5000":            "2018-11-01",
    "Quadro RTX 6000":            "2018-11-01",
    "T4":                         "2018-09-01",
    "Tesla V100S PCIe 32 GB":     "2019-11-01",   # SC19 Nov 2019, not 2020
    "A100 SXM4 40 GB":            "2020-05-01",
    "A40":                        "2020-10-01",
    "RTX A6000":                  "2020-10-01",
    "GeForce RTX 3080":           "2020-09-01",
    "GeForce RTX 3090":           "2020-09-01",
    "GeForce RTX 3060 Ti":        "2020-12-01",
    "GeForce RTX 3070":           "2020-10-01",
    "A100 PCIe 40 GB":            "2020-06-01",   # shipped Jun 2020 (not 2021)
    "A100 SXM4 80 GB":            "2021-11-01",
    "A100 PCIe 80 GB":            "2021-11-01",
    "A30 PCIe":                   "2021-04-01",
    "A16 PCIe":                   "2021-04-01",
    "A10":                        "2021-04-01",
    "RTX A2000":                  "2021-04-01",
    "RTX A4000":                  "2021-04-01",
    "RTX A5000":                  "2021-04-01",
    "RTX A4500":                  "2021-10-01",
    "GeForce RTX 3060":           "2021-02-01",
    "GeForce RTX 3070 Ti":        "2021-06-01",
    "GeForce RTX 3080 Ti":        "2021-06-01",
    "GeForce RTX 3090 Ti":        "2022-03-01",   # retail launch Mar 29, 2022 (not CES announce)
    "Radeon Instinct MI210":      "2021-11-01",
    "A100X":                      "2022-03-01",
    "L40":                        "2022-10-01",
    "GeForce RTX 4090":           "2022-10-01",
    "GeForce RTX 4080":           "2022-11-01",
    "RTX 6000 Ada Generation":    "2022-12-01",
    "Gaudi2 HL-225H":             "2022-12-01",
    "H100 SXM5 64 GB":            "2023-03-01",   # SXM5 shipped Q1 2023 (not GTC announce Sep 2022)
    "H100 SXM5 80 GB":            "2023-03-01",
    "H100 SXM5 94 GB":            "2023-03-01",
    "GeForce RTX 4070 Ti":        "2023-01-01",
    "RTX 4000 Ada Generation":    "2023-01-01",
    "L4":                         "2023-02-01",
    "H100 PCIe 80 GB":            "2023-03-01",
    "H100 PCIe 94 GB":            "2023-03-01",
    "GeForce RTX 4070":           "2023-04-01",
    "GeForce RTX 4060 Ti 8 GB":   "2023-05-01",
    "GeForce RTX 4060":           "2023-06-01",
    "GeForce RTX 4060 Ti 16 GB":  "2023-07-01",
    "L40S":                       "2023-08-01",
    "NVIDIA GH200":               "2023-11-01",
    "AMD Instinct MI300X":        "2023-12-01",
    "GeForce RTX 4090 D":         "2023-12-01",
    "GeForce RTX 4070 SUPER":     "2024-01-01",
    "GeForce RTX 4070 Ti SUPER":  "2024-01-01",
    "GeForce RTX 4080 SUPER":     "2024-01-01",
    "H200 SXM":                   "2024-03-01",
    "H200 NVL":                   "2024-03-01",
}

# ── GPU successor announcement dates (public record — NVIDIA GTC / CES / SIGGRAPH) ──
# Maps each GPU to the date its direct successor generation was publicly announced.
# Successor announcements cause a discrete 20-40% price step-down that is mechanistically
# different from continuous exponential decay. Including post-announcement observations
# in curve fitting inflates the k (decay rate) parameter, overstating structural
# depreciation speed. These dates let build_extended_monthly() tag post_successor months
# so fit_all_gpus() can use only pre-announcement data when estimating k.
SUCCESSOR_DATES = {
    # RTX 30-series → RTX 40-series announced GeForce Beyond September 20, 2022
    "GeForce RTX 3060":           "2022-09-01",
    "GeForce RTX 3060 Ti":        "2022-09-01",
    "GeForce RTX 3070":           "2022-09-01",
    "GeForce RTX 3070 Ti":        "2022-09-01",
    "GeForce RTX 3080":           "2022-09-01",
    "GeForce RTX 3080 Ti":        "2022-09-01",
    "GeForce RTX 3090":           "2022-09-01",
    "GeForce RTX 3090 Ti":        "2022-09-01",
    # RTX 40-series → RTX 50-series announced CES January 6, 2025
    "GeForce RTX 4060":           "2025-01-01",
    "GeForce RTX 4060 Ti 8 GB":   "2025-01-01",
    "GeForce RTX 4060 Ti 16 GB":  "2025-01-01",
    "GeForce RTX 4070":           "2025-01-01",
    "GeForce RTX 4070 SUPER":     "2025-01-01",
    "GeForce RTX 4070 Ti":        "2025-01-01",
    "GeForce RTX 4070 Ti SUPER":  "2025-01-01",
    "GeForce RTX 4080":           "2025-01-01",
    "GeForce RTX 4080 SUPER":     "2025-01-01",
    "GeForce RTX 4090":           "2025-01-01",
    "GeForce RTX 4090 D":         "2025-01-01",
    # Quadro RTX/Turing workstation → RTX A-series Ampere announced April 2021
    "Quadro P5000":               "2018-08-01",   # succeeded by Quadro RTX (SIGGRAPH Aug 2018)
    "Quadro RTX 4000":            "2021-04-01",
    "Quadro RTX 5000":            "2021-04-01",
    "Quadro RTX 6000":            "2021-04-01",
    # RTX A-series Ampere workstation → RTX Ada announced GTC September 20, 2022
    "RTX A2000":                  "2022-09-01",
    "RTX A4000":                  "2022-09-01",
    "RTX A4500":                  "2022-09-01",
    "RTX A5000":                  "2022-09-01",
    "RTX A6000":                  "2022-09-01",
    # V100 → A100 announced GTC May 14, 2020
    "Tesla V100 SXM2 16 GB":      "2020-05-01",
    "Tesla V100 PCIe 16 GB":      "2020-05-01",
    "Tesla V100 SXM2 32 GB":      "2020-05-01",
    "Tesla V100 PCIe 32 GB":      "2020-05-01",
    "Tesla V100S PCIe 32 GB":     "2020-05-01",   # NOTE: V100S launched Nov 2019, so all data is post-successor
    # T4 → L4 announced GTC March 20, 2023
    "T4":                         "2023-03-01",
    # A100 → H100 announced GTC Spring March 22, 2022
    "A100 SXM4 40 GB":            "2022-03-01",
    "A100 PCIe 40 GB":            "2022-03-01",
    "A100 SXM4 80 GB":            "2022-03-01",
    "A100 PCIe 80 GB":            "2022-03-01",
    # A100X omitted from SUCCESSOR_DATES — launch date equals H100 announcement
    # (both 2022-03-01), so all data is post-successor. No pre-announcement window.
    # A40 → L40 announced GTC September 20, 2022 (not SIGGRAPH Aug)
    "A40":                        "2022-09-01",
    # A10/A30 → L40S announced NVIDIA AI Conference September 2023
    "A10":                        "2023-09-01",
    "A30 PCIe":                   "2023-09-01",
    # L40 → L40S announced September 2023
    "L40":                        "2023-09-01",
    # MI210 → MI300X announced AMD Advancing AI December 2023
    "Radeon Instinct MI210":      "2023-12-01",
    # Gaudi2 → Gaudi3 announced Intel Vision April 9, 2024
    "Gaudi2 HL-225H":             "2024-04-01",
    # H100 → H200 announced SC23 November 2023
    "H100 SXM5 64 GB":            "2023-11-01",
    "H100 SXM5 80 GB":            "2023-11-01",
    "H100 SXM5 94 GB":            "2023-11-01",
    "H100 PCIe 80 GB":            "2023-11-01",
    "H100 PCIe 94 GB":            "2023-11-01",
}

# ── Shared thresholds — single definition used by data_prep AND depreciation_curves ──
DEMAND_SHOCK_RATIO  = 1.5   # GPU is "in shock" if recent NEW median > this × MSRP
SHOCK_WINDOW_DAYS   = 90    # look-back window (days) for demand-shock detection
SHOCK_MIN_SAMPLES   = 3     # minimum NEW observations in window to flag a shock

# ── Canonical launch MSRPs (public record) ────────────────────────────────────
# Single source of truth imported by keepa_prep.py (MSRP assignment for Keepa
# data) and ranking.py (fallback when a GPU has no NEW-condition rows in the
# retail CSV).  Values are NVIDIA/AMD official launch prices in USD.
MSRP_REFERENCE = {
    "GeForce RTX 3060":          329,
    "GeForce RTX 3060 Ti":       399,
    "GeForce RTX 3070":          499,
    "GeForce RTX 3070 Ti":       599,
    "GeForce RTX 3080":          699,
    "GeForce RTX 3080 Ti":      1199,
    "GeForce RTX 3090":         1499,
    "GeForce RTX 3090 Ti":      1999,
    "GeForce RTX 4060":          299,
    "GeForce RTX 4060 Ti 8 GB":  399,
    "GeForce RTX 4060 Ti 16 GB": 499,
    "GeForce RTX 4070":          599,
    "GeForce RTX 4070 SUPER":    599,
    "GeForce RTX 4070 Ti":       799,
    "GeForce RTX 4070 Ti SUPER": 799,
    "GeForce RTX 4080":         1199,
    "GeForce RTX 4080 SUPER":    999,
    "GeForce RTX 4090":         1599,
    "GeForce RTX 4090 D":       1599,
    "RTX A2000":                 450,
    "RTX A4000":                1000,
    "RTX A4500":                2249,
    "RTX A5000":                2249,
    "RTX A6000":                4650,
    "RTX 4000 Ada Generation":  1250,
    "RTX 6000 Ada Generation":  6800,
    "Quadro RTX 4000":           900,
    "Quadro RTX 5000":          2300,
    "Quadro RTX 6000":          6300,
    "Quadro P5000":             2499,
    "Tesla V100 PCIe 16 GB":    9900,   # Microway/CDW single-unit list ~$9,900; prior $8,999 unverifiable
    "Tesla V100 PCIe 32 GB":   11458,  # Microway single-unit list $11,458; prior $10,664 was 16GB price misapplied
    "T4":                       2299,
    "L4":                       2500,   # NVIDIA list price ~$2,500; prior $7,000 was OEM server bundle price
    # Datacenter GPUs — list prices from NVIDIA/OEM channels (approximate)
    "Tesla V100 SXM2 16 GB":    9900,   # Microway "no SXM premium"; carrier-adjusted +$200 in pipeline
    "Tesla V100 SXM2 32 GB":   11458,  # Microway $11,458; carrier-adjusted +$200 in pipeline
    "Tesla V100S PCIe 32 GB":  11458,  # Drop-in V100 32GB replacement at same price tier
    "A100 SXM4 40 GB":          11000,
    "A100 PCIe 40 GB":          11000,
    "A100 SXM4 80 GB":          15000,
    "A100 PCIe 80 GB":          13000,
    "A100X":                    17500,  # A100 80GB ($13K) + BlueField-2 DPU (~$3-4K); Ahead-IT EU €16,184 ex-VAT ≈ $17,500
    "A40":                       5000,  # standalone ~$5K; prior $27,500 was Cisco GPL OEM (same chip as A6000 at $4,650)
    "A30 PCIe":                 4500,
    "A16 PCIe":                 4500,   # quad-GPU VDI card (4x GA107, 64GB); eBay NEW $2,550-$3,499, USED $1,950-$2,999; prior $2,800 was single-GPU estimate
    "A10":                      2800,   # NextPlatform Apr 2021 estimate (~half the A30); prior $3,500 was likely T4 Dell channel confusion
    "L40":                       7500,  # standalone ~$7.5K; prior $31K was Cisco/Lenovo OEM (L40S successor at $7,500)
    "L40S":                     7500,
    "H100 SXM5 64 GB":         25000,
    "H100 SXM5 80 GB":         30000,
    "H100 SXM5 94 GB":         33000,
    "H100 PCIe 80 GB":         25599,
    "H100 PCIe 94 GB":         28000,
    "NVIDIA GH200":            35000,  # H100 GPU + Grace CPU + 480GB LPDDR5X; Wiredzone $35,430, Fluence $35-45K
    "H200 SXM":                35000,   # corrected from 27500; launch ~$35-40K per unit
    "H200 NVL":                32000,   # corrected from 35000; per-card ~$31-32K (NVL is dual-card)
    "AMD Instinct MI300X":     15000,
    "Radeon Instinct MI210":    7500,   # AMD never disclosed US MSRP; $15K was Japan OEM/Dell catalog. $7,500 from Amazon channel $7,850, half-MI250 cost, consistent with $4,380 NEW at 58% age 49mo
    "Gaudi2 HL-225H":          8125,   # Intel disclosed $65K/8-card UBB kit at Computex 2024; prior $15K was Gaudi 3 price
}

# ── GPU name aliases (remap before processing) ──────────────────────────────
# V100 FHHL is the same GV100 die + 16GB HBM2 as V100 PCIe 16GB.
# eBay sold prices are interchangeable ($293-$325 vs $259-$376).
# Merging avoids a phantom SKU with uncertain MSRP and only 7 data points.
GPU_NAME_ALIASES = {
    "Tesla V100 FHHL": "Tesla V100 PCIe 16 GB",
}

# ── SXM carrier cost adjustment ─────────────────────────────────────────────
# V100 SXM2 bare modules need a $200 PCIe adapter + heatsink to function.
# Only applied to V100 SXM2 where bare-module market dominates.
# A100 SXM4 and H100 SXM5 are NOT adjusted — they already have good direct
# data and their own curve fits. Carrier adjustment would distort those.
CARRIER_COST = {
    "Tesla V100 SXM2 16 GB":  200,
    "Tesla V100 SXM2 32 GB":  200,
}

FILES = {
    2024: "data/tier3_2024_retail.csv",
    2025: "data/tier3_2025_retail.csv",
    2026: "data/tier3_2026_retail.csv",
}

# ── Condition label normalisation ─────────────────────────────────────────────
CONDITION_MAP = {
    # Standard variants
    "NEW": "NEW", "new": "NEW", "New": "NEW",
    "USED": "USED", "used": "USED", "Used": "USED",
    "REFURBISHED": "REFURBISHED", "Refurbished": "REFURBISHED", "refurbished": "REFURBISHED",
    "renewed": "REFURBISHED", "Renewed": "REFURBISHED",
    # Amazon "renewed" listing format variations
    "Open Box": "REFURBISHED",   # physically like refurbished; remap to REFURBISHED
    # "For Parts" intentionally excluded — price data not comparable to working units
}


def load_data(verbose=True):
    frames = []
    for year, path in FILES.items():
        df = pd.read_csv(path, parse_dates=["date"],
                         encoding="latin-1", on_bad_lines="skip")
        df["source_year"] = year
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)

    # ── Apply GPU name aliases (FHHL → PCIe 16GB) ──────────────────────────
    if GPU_NAME_ALIASES:
        df["gpu_name"] = df["gpu_name"].replace(GPU_NAME_ALIASES)

    # ── Normalise condition labels (BEFORE dedup so "new"/"NEW" don't survive as distinct) ──
    unmapped = df[~df["condition"].isin(CONDITION_MAP)]["condition"].value_counts()
    df["condition"] = df["condition"].map(CONDITION_MAP)
    n_unmapped = df["condition"].isna().sum()
    df = df[df["condition"].notna()].copy()
    if verbose and n_unmapped > 0:
        print(f"⚠  Dropped {n_unmapped:,} rows with unmapped condition labels: "
              f"{dict(unmapped.head(10))}\n")

    # ── Deduplicate across overlapping CSVs ───────────────────────────────────
    # Include country so legitimate same-price listings from different markets survive.
    n_before = len(df)
    dedup_cols = ["gpu_name", "date", "condition", "price_usd"]
    if "country" in df.columns:
        dedup_cols.append("country")
    df = df.drop_duplicates(subset=dedup_cols)
    if verbose and len(df) < n_before:
        print(f"ℹ  Deduplicated {n_before - len(df):,} duplicate rows across CSVs\n")

    # ── Filter to US-only data ──────────────────────────────────────────────
    # The retail CSVs contain multi-country data (US, UK, SG, FR, FI, ES, etc.)
    # with prices in local currency mislabeled as USD.  Non-US datacenter GPU
    # prices are 2-5x US levels (e.g., France A100 at €42K labeled as $42K vs
    # actual US $8.8K).  This systematically inflates price_ratio for datacenter
    # GPUs.  Keepa data is already US-only (marketplace_id=1).  Filtering to
    # US reduces the dataset from ~580K to ~158K rows — still ample.
    if "country" in df.columns:
        n_before_country = len(df)
        df = df[df["country"] == "US"]
        if verbose:
            print(f"🇺🇸 Filtered to US-only: kept {len(df):,} of {n_before_country:,} rows "
                  f"({len(df)/n_before_country*100:.0f}%)\n")

    # ── Title-based junk filter (non-functional GPUs & misclassified accessories) ──
    # RTX 4090 (and others) attract junk listings: dead cards sold "as is",
    # heatsink-only kits, riser cables mis-tagged as GPU products, etc.
    # These contaminate price curves. Filter by title keywords BEFORE MSRP fill
    # so junk rows never reach downstream pipeline stages.
    if "title" in df.columns:
        JUNK_TITLE_KEYWORDS = [
            "no core", "as is", "for parts", "won't boot", "wont boot",
            "board only", "heatsink fan kit", r"\bdefective\b",
            r"\bbroken\b", "not working", "no display", "for repair",
        ]
        ACCESSORY_TITLE_KEYWORDS = [
            "riser cable", "gpu holder", "gpu support", "gpu brace",
            "backplate only", "dummy plug", "nvlink bridge", "nvlink hb bridge",
            r"\bbracket\b", "baffle plate", "cooler fan", "cooling fan",
        ]
        # Misclassified products: different GPU models or non-GPU products
        # that match a target GPU name as a substring in the scraper.
        MISCLASSIFIED_KEYWORDS = [
            r"\bt400\b",          # NVIDIA T400 workstation card tagged as T4
            r"\bt1000\b",         # NVIDIA T1000 tagged as T4 or similar
            r"i350-t4",           # Intel I350-T4 network adapter tagged as T4
            r"ï¸",                # Encoding-garbled titles (scraper artifact)
            "on-demand one month", # Cloud rental listings, not GPU sales
            r"\brent\b",          # Rental listings
            r"\biphone\b",        # iPhone chargers/cases matching A16 PCIe
            r"\bipad\b",          # iPad tablets matching A16 PCIe
            r"\bsamsung galaxy\b", # Samsung chargers matching A16 PCIe
            r"\bcharger\b",       # Phone chargers matching A16 PCIe
            r"\bintel arc\b",     # Intel Arc GPU tagged as NVIDIA
            r"\bv100\b.*\b12\s*gb\b",  # V100 was never 12GB — misclassified product
        ]
        # Server bundle / multi-GPU keywords: listings that contain a whole
        # server or multi-GPU tray but are tagged under a single GPU name,
        # inflating the price by 5-50x (e.g., DGX systems, server nodes).
        SERVER_BUNDLE_KEYWORDS = [
            r"\bdgx\b", "server node", "server system",
            r"\b[2-8]x\s+(?:nvidia\s+)?(tesla|v100|a100|h100|a40|l40|l4|gpu)\b",
            r"\b\d+\s*pcs\b",       # "4pcs" multi-GPU bundles
            r"\blot\s+of\s+\d+",    # "Lot of 8x" / "Lot of 10" multi-GPU lots
            r"\bcards?\s+lot\b",     # "Cards Lot Of 2" trailing lot pattern
            r"\bgpu modular\b",             # HGX/DGX modular units (not PCIe cards)
            r"\bcomputational accelerator\b", # HPE enterprise product language
            r"\bhgx\b",                      # HGX baseboard / multi-GPU tray
            r"\bgpu baseboard\b",            # Multi-GPU baseboard
            r"for poweredge\b",              # Dell server option SKU
            r"for proliant\b",               # HPE server option SKU
            r"for thinkagile\b",             # Lenovo HCI option SKU
            r"for thinksystem\b",            # Lenovo server option SKU
            r"\b(HPE|Cisco)\b.*\bGraphic Card\b",  # OEM catalog entries at enterprise markup
        ]
        # Gaming PCs, prebuilt desktops, workstations sold as individual GPUs
        PREBUILT_SYSTEM_KEYWORDS = [
            r"\byeyian\b",        # YEYIAN Gaming PCs
            r"\bibuypower\b",     # iBUYPOWER prebuilts
            r"\bcyberpower\b",    # CyberPowerPC prebuilts
            r"\bclx set\b",      # CLX SET gaming PCs
            r"\bskytech\b",      # Skytech Gaming PCs
            r"(?<!for )\bgaming pc\b(?! ?parts)",  # "gaming pc" but not "for gaming pc"
            r"\bgaming desktop\b(?! graphics)",     # not "gaming desktop graphics card"
            r"\bdesktop computer\b",
            # Recertified OEM workstations (HP/Dell/Lenovo + CPU + RAM = complete system)
            r"recertified.*(?:hp|dell|lenovo).*(?:xeon|intel i[3579]).*(?:ddr[45]|ssd|memory)",
            r"\bhp z[2468]\b",               # HP Z-series workstations
            r"\bprecision [357]820\b",       # Dell Precision tower workstations
            r"\bthinkstation\b",             # Lenovo ThinkStation workstations
        ]
        junk_pattern = "|".join(JUNK_TITLE_KEYWORDS + ACCESSORY_TITLE_KEYWORDS
                                + MISCLASSIFIED_KEYWORDS + SERVER_BUNDLE_KEYWORDS
                                + PREBUILT_SYSTEM_KEYWORDS)
        junk_mask = df["title"].str.contains(junk_pattern, case=False, na=False, regex=True)
        n_junk = junk_mask.sum()
        df = df[~junk_mask]
        if verbose and n_junk > 0:
            print(f"🗑  Dropped {n_junk:,} junk/accessory rows by title keyword filter\n")

    # ── Fill missing msrp from MSRP_REFERENCE BEFORE validity filter ────────
    # Some GPUs (AMD MI300X, MI210, Gaudi2) have empty msrp in the CSV.
    # Without this pre-fill, the msrp > 0 filter below would drop them before
    # the msrp_canonical fallback (which runs after the filter) could rescue them.
    msrp_fill = df["gpu_name"].map(MSRP_REFERENCE)
    df["msrp"] = df["msrp"].fillna(msrp_fill)

    # ── Basic type and validity filters ──────────────────────────────────────
    price_filter = (df["price_usd"] > 0) & (df["msrp"] > 0)
    if "fp32" in df.columns:
        price_filter = price_filter & (df["fp32"] > 0)
    df = df[price_filter]

    # ── Canonical MSRP per GPU ─────────────────────────────────────────────
    # MSRP_REFERENCE is the primary source: manually curated official NVIDIA/AMD
    # launch prices. The CSV's scraped msrp field is unreliable for datacenter
    # GPUs — resellers list T4 at $7,435 (3.2x the $2,299 launch MSRP), V100
    # SXM2 at $22,000 (2.4x the $8,999 launch MSRP). Using the curated launch
    # price ensures price_ratio is consistent across all data sources (retail,
    # keepa, supplement) and across all GPU segments.
    # Fallback: for GPUs not in MSRP_REFERENCE, use the CSV median.
    msrp_csv_median = df.groupby("gpu_name")["msrp"].median()
    df["msrp_canonical"] = df["gpu_name"].map(MSRP_REFERENCE)
    df["msrp_canonical"] = df["msrp_canonical"].fillna(
        df["gpu_name"].map(msrp_csv_median)
    ).fillna(df["msrp"])

    # ── MSRP integrity check ─────────────────────────────────────────────────
    msrp_check = (df.groupby("gpu_name")["msrp"]
                    .agg(msrp_min="min", msrp_max="max")
                    .assign(msrp_pct_range=lambda x:
                            (x.msrp_max - x.msrp_min) / x.msrp_min))
    flagged = msrp_check[msrp_check["msrp_pct_range"] > 0.05]
    if verbose and len(flagged):
        print(f"⚠  MSRP inconsistency (>5% range) in {len(flagged)} GPU models:")
        print(flagged[["msrp_min", "msrp_max", "msrp_pct_range"]].to_string())
        print()

    # ── SXM carrier cost adjustment ────────────────────────────────────────
    # Add adapter cost to USED SXM module prices to reflect "usable equivalent"
    carrier = df["gpu_name"].map(CARRIER_COST).fillna(0)
    used_mask = df["condition"].isin(["USED", "REFURBISHED"])
    adj_mask = (carrier > 0) & used_mask
    df["price_usd"] = df["price_usd"] + np.where(adj_mask, carrier, 0)
    n_carrier = adj_mask.sum()
    if verbose and n_carrier > 0:
        print(f"🔧 Carrier-adjusted {n_carrier:,} SXM USED rows "
              f"({df.loc[adj_mask, 'gpu_name'].nunique()} GPUs)\n")

    # ── price_ratio using canonical MSRP ──────────────────────────────────────
    # Using msrp_canonical (median per GPU) instead of per-row msrp eliminates
    # spurious price_ratio variation caused by MSRP scraping inconsistencies.
    df["price_ratio"] = df["price_usd"] / df["msrp_canonical"]

    # ── Launch-date time origin ───────────────────────────────────────────────
    launch = (pd.Series(LAUNCH_DATES)
                .rename_axis("gpu_name")
                .reset_index()
                .rename(columns={0: "launch_date"}))
    launch["launch_date"] = pd.to_datetime(launch["launch_date"])
    df = df.merge(launch, on="gpu_name", how="left")
    df["age_months"] = (df["date"] - df["launch_date"]).dt.days / 30.44
    df["left_censored"] = df["launch_date"].isna()  # no launch date on record

    # ── Successor announcement date ───────────────────────────────────────────
    # successor_announced: True if this observation falls after the GPU's next-gen
    # was announced. Used in depreciation_curves.py to isolate pre-announcement
    # data for k estimation, preventing announcement step-changes from inflating k.
    succ_map = pd.Series(SUCCESSOR_DATES).rename_axis("gpu_name").reset_index()
    succ_map.columns = ["gpu_name", "successor_date"]
    succ_map["successor_date"] = pd.to_datetime(succ_map["successor_date"])
    df = df.merge(succ_map, on="gpu_name", how="left")
    df["successor_announced"] = (
        df["successor_date"].notna() & (df["date"] >= df["successor_date"])
    )
    df["months_since_successor_announced"] = np.where(
        df["successor_announced"],
        (df["date"] - df["successor_date"]).dt.days / 30.44,
        np.nan,
    )

    # ── Demand-shock flag (before outlier filter so shock GPUs aren't stripped) ─
    # demand_shock is a GPU-level flag: True if the GPU is CURRENTLY in a demand
    # shock (median NEW price > 1.5x MSRP in the past 90 days). This flag is used
    # for reporting / ranking exclusion — it does NOT mean all historical rows
    # for the GPU are invalid. Pre-shock and post-shock observations are still
    # valid depreciation data; only the shock-period observations should be
    # excluded from curve fitting (handled in depreciation_curves.py by capping
    # price_ratio ≤ 1.5 in build_extended_monthly).
    cutoff = df["date"].max() - pd.Timedelta(days=SHOCK_WINDOW_DAYS)
    recent_new = (df[(df["date"] >= cutoff) & (df["condition"] == "NEW")]
                    .groupby("gpu_name")["price_ratio"]
                    .agg(median_ratio="median", n_obs="count"))
    shock_gpus = set(recent_new[
        (recent_new["median_ratio"] > DEMAND_SHOCK_RATIO) &
        (recent_new["n_obs"] >= SHOCK_MIN_SAMPLES)
    ].index)
    df["demand_shock"] = df["gpu_name"].isin(shock_gpus)
    if verbose and shock_gpus:
        print(f"⚡ Demand-shock GPUs (recent NEW > {DEMAND_SHOCK_RATIO}x MSRP): {sorted(shock_gpus)}\n")

    # ── Outlier filter: lower bound AND upper bound ────────────────────────
    # Lower: flat $50 for USED/REFURBISHED. Old datacenter GPUs (V100 at
    # $8,999 MSRP) legitimately trade at 1-7% of MSRP ($64-$639) as USED.
    # For NEW condition: max(5% of MSRP, $50). A "NEW" GPU at 1-3% of MSRP
    # is always a scraper artifact (Amazon price-per-unit error, auction
    # start bid, or placeholder). No legitimate NEW GPU sells at 1% of its
    # launch price. This catches ~100 scraper artifacts without blocking
    # any legitimate USED/REFURB data for deeply depreciated datacenter GPUs.
    # Upper: 3x MSRP. Catches multi-GPU server bundles (DGX at $200K-$500K
    # priced as single GPUs) while preserving legitimate demand-shock pricing
    # (individual cards rarely trade above 3x MSRP even in extreme scarcity).
    new_mask = df["condition"] == "NEW"
    outlier_floor_new = np.maximum(0.05 * df["msrp_canonical"], 50)
    # USED/REFURB floor: segment-dependent.
    # CONSUMER/WORKSTATION: max(10% of MSRP, $50). Catches scam/placeholder
    # listings like RTX 4090 USED at $75 ($1,599 × 10% = $160; real used $1,200+)
    # and RTX 3090 USED at $99 ($1,499 × 10% = $150). For low-MSRP cards
    # like RTX 3060 ($329), 10% = $33, so the $50 floor applies (real used $120+).
    # DATACENTER: flat $150. Old datacenter GPUs legitimately trade at 1-4% of
    # MSRP — V100 PCIe 16GB ($9,900 MSRP) sells for $259-$400 USED on eBay.
    # A 10% floor ($990) would kill all legitimate V100 USED data.
    dc_gpus = df["gpu_name"].str.contains(
        "V100|A100|H100|H200|A10|A16|A30|A40|L4|L40|T4|GH200|MI300|MI210|Gaudi|A100X",
        case=False, na=False)
    outlier_floor_used = np.where(
        dc_gpus,
        150,   # datacenter: flat $150 (filters bare SXM modules + stale ask-prices)
        np.maximum(0.10 * df["msrp_canonical"], 50)  # consumer/workstation: 10% MSRP
    )
    outlier_floor = np.where(new_mask, outlier_floor_new, outlier_floor_used)
    outlier_ceil = 3.0 * df["msrp_canonical"]

    n_before_outlier = len(df)
    df = df[(df["price_usd"] > outlier_floor) & (df["price_usd"] < outlier_ceil)]
    if verbose:
        print(f"🔍 Outlier filter: removed {n_before_outlier - len(df):,} rows "
              f"(NEW floor=5% MSRP, USED floor=10% MSRP consumer/$150 datacenter, ceil=3x MSRP)\n")

    return df


def stationarity_report(df, verbose=True):
    """ADF test on monthly median price_ratio per GPU. Returns dict of p-values."""
    results = {}
    for gpu, grp in df.groupby("gpu_name"):
        series = (grp.set_index("date")["price_ratio"]
                     .resample("M").median()
                     .dropna())
        if len(series) < 8:
            continue
        pval = adfuller(series, autolag="AIC", regression="ct")[1]
        results[gpu] = pval
        if verbose and pval > 0.05:
            print(f"  Non-stationary: {gpu}  (ADF p={pval:.3f})")
    return results


DATACENTER_SUPPLEMENT_PATH = "data/scraped_datacenter_supplement.csv"
EBAY_VERIFIED_PATH = "data/ebay_verified_supplement.csv"


def load_datacenter_supplement(path=DATACENTER_SUPPLEMENT_PATH, verbose=True):
    """
    Load optional datacenter secondary-market supplement data (e.g. eBay Terapeak
    sold listings, Vast.ai hardware buy prices) and return a DataFrame in the
    same monthly-median format as keepa_monthly.csv.

    Expected input CSV columns:
        gpu_name   — must match GPU names in LAUNCH_DATES / MSRP_REFERENCE
        date       — observation date (YYYY-MM-DD or MM/DD/YYYY)
        price_usd  — transaction or ask price in USD
        source_type — e.g. "ebay_sold", "vastai_bid", "servermonkey_ask"

    Returns None if the file does not exist (pipeline runs without supplement).
    Returns DataFrame with: gpu_name, month (Period M), price_ratio, age_months, source.
    """
    import os
    if not os.path.exists(path):
        return None

    try:
        raw = pd.read_csv(path, parse_dates=["date"], encoding="utf-8", on_bad_lines="skip")
    except Exception as e:
        if verbose:
            print(f"⚠  Could not load datacenter supplement ({path}): {e}")
        return None

    required = {"gpu_name", "date", "price_usd"}
    if not required.issubset(raw.columns):
        if verbose:
            print(f"⚠  datacenter_supplement.csv missing required columns "
                  f"(need: {required}, got: {set(raw.columns)})")
        return None

    raw = raw[(raw["price_usd"] > 0) & raw["date"].notna()].copy()
    if raw.empty:
        return None

    # ── Apply GPU name aliases ──────────────────────────────────────────────
    if GPU_NAME_ALIASES:
        raw["gpu_name"] = raw["gpu_name"].replace(GPU_NAME_ALIASES)

    # ── Exclude predictions / estimates from other models ────────────────────
    # Some rows are outputs of other pricing models (Oplexa age-based,
    # gpucost.org estimate, market consensus, etc.) rather than actual
    # transactions.  Feeding predictions as training data creates circular
    # dependency and inflates apparent data coverage.
    PREDICTION_KEYWORDS = ["estimate", "age-based", "consensus",
                           "implied", "forecast", "prediction",
                           "market range", "market price",
                           "active listing",   # eBay ask prices, not sold
                           "vastai_implied", "Vast.ai implied",
                           "cloud rental",
                           "NotebookCheck", "Hacker News", "Reddit"]
    src_col = "source_type" if "source_type" in raw.columns else "source"
    if src_col in raw.columns:
        pred_pattern = "|".join(PREDICTION_KEYWORDS)
        pred_mask = raw[src_col].astype(str).str.contains(
            pred_pattern, case=False, na=False)
        n_pred = pred_mask.sum()
        raw = raw[~pred_mask]
        if verbose and n_pred > 0:
            print(f"  Filtered {n_pred} prediction/estimate rows from supplement")
    # Drop LOW confidence rows (speculative, mislabeled, or model-derived)
    if "confidence" in raw.columns:
        low_mask = raw["confidence"].str.upper().str.strip() == "LOW"
        n_low = low_mask.sum()
        raw = raw[~low_mask]
        if verbose and n_low > 0:
            print(f"  Filtered {n_low} LOW-confidence rows from supplement")
    if raw.empty:
        return None

    # ── Filter dev boards and non-GPU components ──────────────────────────
    # Dev baseboards (P4261), engineering samples, and server chassis are
    # not comparable to production GPU modules.
    if "notes" in raw.columns:
        dev_pattern = r"baseboard|dev board|engineering sample|chassis|server system"
        dev_mask = raw["notes"].astype(str).str.contains(dev_pattern, case=False, na=False)
        n_dev = dev_mask.sum()
        raw = raw[~dev_mask]
        if verbose and n_dev > 0:
            print(f"  Filtered {n_dev} dev board/non-GPU rows from supplement")

    # Compute MSRP and price_ratio
    raw["msrp"] = raw["gpu_name"].map(MSRP_REFERENCE)
    raw = raw[raw["msrp"].notna()].copy()
    # SXM carrier cost adjustment for supplement data
    carrier = raw["gpu_name"].map(CARRIER_COST).fillna(0)
    if "condition" in raw.columns:
        supp_used = raw["condition"].str.upper().str.strip().isin(["USED", "REFURBISHED"])
    else:
        supp_used = pd.Series(True, index=raw.index)
    raw["price_usd"] = raw["price_usd"] + np.where((carrier > 0) & supp_used, carrier, 0)
    raw["price_ratio"] = raw["price_usd"] / raw["msrp"]
    # Lower floor for datacenter GPUs: V100 at $9,900 MSRP has eBay sold at
    # $80-$293, giving ratios 0.008-0.030. The old 0.03 floor killed this data.
    # Use 0.005 (~$50 minimum) for datacenter, 0.03 for consumer/workstation.
    dc_names = raw["gpu_name"].str.contains(
        "V100|A100|H100|H200|A10|A16|A30|A40|L4|L40|T4|GH200|MI300|MI210|Gaudi|A100X",
        case=False, na=False)
    ratio_floor = np.where(dc_names, 0.005, 0.03)
    raw = raw[(raw["price_ratio"] > ratio_floor) & (raw["price_ratio"] <= DEMAND_SHOCK_RATIO)]

    # Compute age_months from launch date
    launch = pd.Series(LAUNCH_DATES).rename_axis("gpu_name").reset_index()
    launch.columns = ["gpu_name", "launch_date"]
    launch["launch_date"] = pd.to_datetime(launch["launch_date"])
    raw = raw.merge(launch, on="gpu_name", how="left")
    raw = raw[raw["launch_date"].notna()].copy()
    raw["age_months"] = (raw["date"] - raw["launch_date"]).dt.days / 30.44
    raw = raw[raw["age_months"] >= 0]

    raw["month"] = raw["date"].dt.to_period("M")
    # Preserve actual condition from CSV (if present) for proper filtering downstream.
    # Previously all rows were stamped condition="NEW", which contaminated the
    # datacenter canonical fit by mixing used secondary-market prices with new prices.
    if "condition" in raw.columns:
        raw["condition"] = raw["condition"].str.upper().str.strip()
    else:
        raw["condition"] = "NEW"
    monthly = (raw.groupby(["gpu_name", "condition", "month"])
                  .agg(price_ratio=("price_ratio", "median"),
                       age_months=("age_months", "median"))
                  .reset_index())
    monthly["source"] = "supplement"

    if verbose:
        print(f"📦 Loaded datacenter supplement: {len(monthly)} GPU-months "
              f"across {monthly['gpu_name'].nunique()} GPUs from {path}")

    # ── Also load ebay_verified_supplement.csv (HIGH-confidence sold data) ──
    ebay_path = EBAY_VERIFIED_PATH
    if os.path.exists(ebay_path):
        try:
            ebay = pd.read_csv(ebay_path, parse_dates=["date"], encoding="utf-8", on_bad_lines="skip")
            ebay = ebay[(ebay["price_usd"] > 0) & ebay["date"].notna()].copy()
            # Keep only HIGH confidence eBay sold data
            if "confidence" in ebay.columns:
                ebay = ebay[ebay["confidence"].str.upper().str.strip() == "HIGH"]
            # Filter dev boards and non-GPU components (same as scraped supplement)
            if "notes" in ebay.columns:
                dev_pattern = r"baseboard|dev board|engineering sample|chassis|server system|not a gpu"
                dev_mask = ebay["notes"].astype(str).str.contains(dev_pattern, case=False, na=False)
                n_dev = dev_mask.sum()
                ebay = ebay[~dev_mask]
                if verbose and n_dev > 0:
                    print(f"  Filtered {n_dev} dev board/non-GPU rows from eBay supplement")
            # Apply aliases and carrier adjustment
            if GPU_NAME_ALIASES:
                ebay["gpu_name"] = ebay["gpu_name"].replace(GPU_NAME_ALIASES)
            ebay["msrp"] = ebay["gpu_name"].map(MSRP_REFERENCE)
            ebay = ebay[ebay["msrp"].notna()].copy()
            # SXM carrier cost adjustment
            ebay_carrier = ebay["gpu_name"].map(CARRIER_COST).fillna(0)
            if "condition" in ebay.columns:
                ebay_used = ebay["condition"].str.upper().str.strip().isin(["USED", "REFURBISHED"])
            else:
                ebay_used = pd.Series(True, index=ebay.index)
            ebay["price_usd"] = ebay["price_usd"] + np.where((ebay_carrier > 0) & ebay_used, ebay_carrier, 0)
            ebay["price_ratio"] = ebay["price_usd"] / ebay["msrp"]
            # Same DC-aware floor as scraped supplement: 0.005 for datacenter, 0.03 for others
            ebay_dc = ebay["gpu_name"].str.contains(
                "V100|A100|H100|H200|A10|A16|A30|A40|L4|L40|T4|GH200|MI300|MI210|Gaudi|A100X",
                case=False, na=False)
            ebay_floor = np.where(ebay_dc, 0.005, 0.03)
            ebay = ebay[(ebay["price_ratio"] > ebay_floor) & (ebay["price_ratio"] <= DEMAND_SHOCK_RATIO)]
            launch_map = pd.Series(LAUNCH_DATES).rename_axis("gpu_name").reset_index()
            launch_map.columns = ["gpu_name", "launch_date"]
            launch_map["launch_date"] = pd.to_datetime(launch_map["launch_date"])
            ebay = ebay.merge(launch_map, on="gpu_name", how="left")
            ebay = ebay[ebay["launch_date"].notna()].copy()
            ebay["age_months"] = (ebay["date"] - ebay["launch_date"]).dt.days / 30.44
            ebay = ebay[ebay["age_months"] >= 0]
            ebay["month"] = ebay["date"].dt.to_period("M")
            if "condition" in ebay.columns:
                ebay["condition"] = ebay["condition"].str.upper().str.strip()
            else:
                ebay["condition"] = "USED"
            ebay_monthly = (ebay.groupby(["gpu_name", "condition", "month"])
                               .agg(price_ratio=("price_ratio", "median"),
                                    age_months=("age_months", "median"))
                               .reset_index())
            ebay_monthly["source"] = "ebay_sold"
            monthly = pd.concat([monthly, ebay_monthly], ignore_index=True)
            if verbose:
                print(f"📦 Loaded eBay verified supplement: {len(ebay_monthly)} GPU-months "
                      f"across {ebay_monthly['gpu_name'].nunique()} GPUs from {ebay_path}")
        except Exception as e:
            if verbose:
                print(f"⚠  Could not load eBay verified supplement ({ebay_path}): {e}")

    return monthly


if __name__ == "__main__":
    df = load_data(verbose=True)
    print(f"Combined dataset: {len(df):,} rows | "
          f"{df['gpu_name'].nunique()} GPUs | "
          f"{df['date'].min().date()} → {df['date'].max().date()}")
    print(f"Condition counts:\n{df['condition'].value_counts().to_string()}\n")
    print("Stationarity check (non-stationary GPUs only):")
    stationarity_report(df, verbose=True)
