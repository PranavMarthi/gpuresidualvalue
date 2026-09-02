"""
keepa_prep.py
Extract historical GPU price data from the Keepa/Amazon database and produce
a monthly price-ratio time series aligned with the retail CSV schema.

Output: outputs/keepa_monthly.csv
Columns: gpu_name, month (Period M), price_usd, msrp, price_ratio, age_months,
         n_products, source='keepa'

Strategy
--------
1. Load products.csv → filter to US marketplace, map titles → our GPU model names.
2. Load price_history.csv → filter to matched products, price_type in ['new', 'amazon'].
   Prefer 'amazon' (first-party NVIDIA/MSFT seller) over 'new' (third-party FBA/FBM).
   Falls back to 'new' when Amazon is not selling the product.
3. Clip price outliers: remove prices < 3% or > 500% of MSRP.
4. Aggregate to monthly median per GPU model.
5. Join MSRP from retail CSV (data_prep.load_data). For GPUs not in retail CSV,
   use MSRP_REFERENCE dict (launch MSRPs from public record).
6. Compute price_ratio and age_months using data_prep.LAUNCH_DATES.
7. Write to outputs/keepa_monthly.csv.

Run standalone: python3 keepa_prep.py
"""

import re
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from data_prep import load_data, LAUNCH_DATES, MSRP_REFERENCE

KEEPA_DIR = "keepa data"
OUT_PATH  = "outputs/keepa_monthly.csv"

# ── GPU title → our standard model name ──────────────────────────────────────
# Order matters: longer/more-specific patterns must come before shorter ones.
GPU_PATTERNS = [
    # RTX 40-series variants first
    ("GeForce RTX 4090 D",          r"RTX[\s\-]?4090\s*D\b"),
    ("GeForce RTX 4090",            r"RTX[\s\-]?4090(?!\s*D)"),
    ("GeForce RTX 4080 SUPER",      r"RTX[\s\-]?4080\s*SUPER"),
    ("GeForce RTX 4080",            r"RTX[\s\-]?4080(?!\s*SUPER)"),
    ("GeForce RTX 4070 Ti SUPER",   r"RTX[\s\-]?4070\s*Ti\s*SUPER"),
    ("GeForce RTX 4070 Ti",         r"RTX[\s\-]?4070\s*Ti(?!\s*SUPER)"),
    ("GeForce RTX 4070 SUPER",      r"RTX[\s\-]?4070\s*SUPER"),
    ("GeForce RTX 4070",            r"RTX[\s\-]?4070(?!\s*(Ti|SUPER))"),
    ("GeForce RTX 4060 Ti 16 GB",   r"RTX[\s\-]?4060\s*Ti.*16\s*[Gg][Bb]"),
    ("GeForce RTX 4060 Ti 8 GB",    r"RTX[\s\-]?4060\s*Ti(?!.*16\s*[Gg][Bb])"),
    ("GeForce RTX 4060",            r"RTX[\s\-]?4060(?!\s*Ti)"),
    # RTX 30-series
    ("GeForce RTX 3090 Ti",         r"RTX[\s\-]?3090\s*Ti"),
    ("GeForce RTX 3090",            r"RTX[\s\-]?3090(?!\s*Ti)"),
    ("GeForce RTX 3080 Ti",         r"RTX[\s\-]?3080\s*Ti"),
    ("GeForce RTX 3080",            r"RTX[\s\-]?3080(?!\s*Ti)"),
    ("GeForce RTX 3070 Ti",         r"RTX[\s\-]?3070\s*Ti"),
    ("GeForce RTX 3070",            r"RTX[\s\-]?3070(?!\s*Ti)"),
    ("GeForce RTX 3060 Ti",         r"RTX[\s\-]?3060\s*Ti"),
    ("GeForce RTX 3060",            r"RTX[\s\-]?3060(?!\s*Ti)"),
    # Professional / workstation
    ("RTX 6000 Ada Generation",     r"RTX\s*6000\s*Ada"),
    ("RTX 4000 Ada Generation",     r"RTX\s*4000\s*Ada"),
    ("RTX A6000",                   r"RTX\s*A6000"),
    ("RTX A5000",                   r"RTX\s*A5000"),
    ("RTX A4500",                   r"RTX\s*A4500"),
    ("RTX A4000",                   r"RTX\s*A4000"),
    ("RTX A2000",                   r"RTX\s*A2000"),
    ("Quadro RTX 6000",             r"Quadro\s*RTX\s*6000"),
    ("Quadro RTX 5000",             r"Quadro\s*RTX\s*5000"),
    ("Quadro RTX 4000",             r"Quadro\s*RTX\s*4000"),
    ("Quadro P5000",                r"Quadro\s*P5000"),
    # Datacenter (thin on Amazon but present)
    # V100S must come BEFORE V100 PCIe 32GB — "V100S" matches "V100.*32" too
    ("Tesla V100S PCIe 32 GB",      r"V100S.*PCIe?.*32|V100S.*32.*PCIe?"),
    ("Tesla V100 PCIe 32 GB",       r"V100.*PCIe?.*32|V100.*32.*PCIe?"),
    ("Tesla V100 PCIe 16 GB",       r"V100.*PCIe?.*16|V100.*16.*PCIe?"),
    ("T4",                          r"\bT4\b(?!.*Ti)"),
    ("L4",                          r"\bL4\b(?!.*Ti)"),
]

# Compile once
GPU_PATTERN_RE = [(name, re.compile(pat, re.IGNORECASE)) for name, pat in GPU_PATTERNS]


def map_title_to_gpu(title):
    if not isinstance(title, str):
        return None
    for name, pat in GPU_PATTERN_RE:
        if pat.search(title):
            return name
    return None


def load_keepa(verbose=True):
    """
    Load and process Keepa data into monthly GPU price series.
    Returns DataFrame with columns:
      gpu_name, month, price_usd, msrp, price_ratio, age_months, n_products
    """

    # ── 1. Products: US marketplace only, map titles ─────────────────────────
    if verbose:
        print("[keepa] Loading products...")
    prod = pd.read_csv(f"{KEEPA_DIR}/products.csv",
                       usecols=["product_id", "marketplace_id", "title"])
    us_prod = prod[prod["marketplace_id"] == 1].copy()
    us_prod["gpu_name"] = us_prod["title"].apply(map_title_to_gpu)

    # ── Filter out Amazon Renewed / Refurbished listings ──────────────────
    # These are refurbished products whose "new" price in Keepa reflects the
    # Renewed buy-box price, not the genuine new-condition price.
    renewed_mask = us_prod["title"].str.contains(
        r'\(Renewed\)|\(Refurbished\)|Certified\s+Refurbished'
        r'|Certified\s+\(Renewed\)|\bRENEWED\b|\bRefurbished\b',
        case=False, na=False, regex=True)
    n_renewed = renewed_mask.sum()
    us_prod = us_prod[~renewed_mask].copy()
    if verbose:
        print(f"[keepa] Excluded {n_renewed} Renewed/Refurbished products")

    matched = us_prod[us_prod["gpu_name"].notna()].copy()

    if verbose:
        counts = matched["gpu_name"].value_counts()
        print(f"[keepa] Matched {len(matched)} US products → {len(counts)} GPU models")
        for gpu, n in counts.items():
            print(f"         {gpu}: {n} products")

    matched_ids = set(matched["product_id"])

    # ── 2. Price history: new + amazon, matched products only ────────────────
    if verbose:
        print("[keepa] Loading price history (this may take ~30s)...")

    chunks = []
    for chunk in pd.read_csv(f"{KEEPA_DIR}/price_history.csv",
                             parse_dates=["timestamp"],
                             chunksize=500_000):
        c = chunk[(chunk["product_id"].isin(matched_ids)) &
                  (chunk["price_type"].isin(["new", "amazon"])) &
                  (chunk["value_usd"] > 0) &
                  (chunk["timestamp"] >= "2017-01-01")]
        if len(c):
            chunks.append(c)

    if not chunks:
        raise ValueError(
            "[keepa] No price history rows matched the filtered criteria. "
            "Check that price_history.csv contains matched product_ids with "
            "price_type in ['new', 'amazon'] from 2017-01-01 onward."
        )
    ph = pd.concat(chunks, ignore_index=True)
    ph = ph.merge(matched[["product_id", "gpu_name"]], on="product_id")

    if verbose:
        print(f"[keepa] {len(ph):,} price observations for matched GPUs")

    # ── 3. MSRP from retail CSV ───────────────────────────────────────────────
    try:
        df_retail = load_data(verbose=False)
        msrp_map = (df_retail[df_retail["condition"] == "NEW"]
                    .groupby("gpu_name")["msrp_canonical"]
                    .first()          # all rows per GPU share the same msrp_canonical
                    .to_dict())
    except Exception:
        msrp_map = {}

    def get_msrp(gpu_name):
        return msrp_map.get(gpu_name, MSRP_REFERENCE.get(gpu_name, np.nan))

    ph["msrp"] = ph["gpu_name"].apply(get_msrp)
    ph = ph[ph["msrp"].notna() & (ph["msrp"] > 0)]

    # ── 4. Clip price outliers (< 3% or > 500% of MSRP) ─────────────────────
    ph = ph[(ph["value_usd"] > 0.03 * ph["msrp"]) &
            (ph["value_usd"] < 5.00 * ph["msrp"])]

    # ── 5. Prefer 'amazon' over 'new' per product-timestamp where both exist ─
    # Rank 0 = amazon (first-party, more stable), 1 = new (third-party).
    # Sort by rank then drop duplicates keeps the amazon row when both exist.
    ph["rank"] = ph["price_type"].map({"amazon": 0, "new": 1})
    ph = (ph.sort_values(["rank", "product_id", "timestamp"])
            .drop_duplicates(subset=["product_id", "timestamp"])
            .drop(columns="rank"))

    # ── 6. Monthly median per GPU model ──────────────────────────────────────
    ph["month"] = ph["timestamp"].dt.to_period("M")
    monthly = (ph.groupby(["gpu_name", "month"])
                 .agg(price_usd    = ("value_usd", "median"),
                      msrp         = ("msrp", "first"),
                      n_products   = ("product_id", "nunique"))
                 .reset_index())

    # ── 7. price_ratio and age_months ────────────────────────────────────────
    monthly["price_ratio"] = monthly["price_usd"] / monthly["msrp"]

    launch = (pd.Series(LAUNCH_DATES)
                .rename_axis("gpu_name")
                .reset_index()
                .rename(columns={0: "launch_date"}))
    launch["launch_date"] = pd.to_datetime(launch["launch_date"])
    monthly = monthly.merge(launch, on="gpu_name", how="left")

    # Use mid-month date (15th) as the time anchor for age_months.
    # dt.to_timestamp() returns period-START (the 1st), which is ~15 days earlier
    # than the typical retail CSV observation date (median transaction ~day 10-20).
    # This ~15-day systematic offset would bias k slightly upward. Using the 15th
    # aligns Keepa age estimates with the retail data's median transaction date.
    month_as_date = monthly["month"].dt.to_timestamp() + pd.Timedelta(days=14)
    monthly["age_months"] = ((month_as_date - monthly["launch_date"])
                             .dt.days / 30.44)

    monthly = monthly[monthly["age_months"] >= 0].copy()
    monthly["source"] = "keepa"

    if verbose:
        print(f"\n[keepa] Final: {len(monthly)} monthly observations across "
              f"{monthly['gpu_name'].nunique()} GPU models")
        print(f"        Age range: {monthly['age_months'].min():.0f}–"
              f"{monthly['age_months'].max():.0f} months")
        print(f"        price_ratio range: {monthly['price_ratio'].min():.2f}–"
              f"{monthly['price_ratio'].max():.2f}")

    return monthly


if __name__ == "__main__":
    import os
    os.makedirs("outputs", exist_ok=True)
    monthly = load_keepa(verbose=True)

    print("\nSample (oldest observations per GPU):")
    sample = (monthly.sort_values("age_months")
                     .groupby("gpu_name")
                     .first()
                     .reset_index()
                     [["gpu_name", "month", "age_months", "price_ratio", "n_products"]]
                     .sort_values("age_months"))
    print(sample.to_string(index=False))

    monthly.to_csv(OUT_PATH, index=False)
    print(f"\nSaved → {OUT_PATH}")
