#!/usr/bin/env python3
"""
Extract historical cloud GPU pricing from the 633MB CSV already on disk.

This file (from_2015_to_2024_historical_data.csv) contains per-hour rental
prices from cloud providers. We can use these as a supplementary depreciation
signal: if cloud pricing for a GPU drops over time, the underlying hardware
is depreciating.

Maps cloud GPU names to our model's gpu_name and produces monthly median
per-hour prices.

Usage:
    python extract_cloud_pricing.py
"""

import csv
import os
import sys
from collections import defaultdict
from datetime import datetime

INPUT_PATH = "data/from_2015_to_2024_historical_data.csv"
OUT_PATH = "data/cloud_pricing_monthly.csv"

# Map cloud CSV gpu_name → our model gpu_name
CLOUD_GPU_MAP = {
    "NVIDIA A100 SXM4 40GB":    "A100 SXM4 40 GB",
    "NVIDIA A100 SXM4 80GB":    "A100 SXM4 80 GB",
    "NVIDIA H100 SXM5 80GB":    "H100 SXM5 80 GB",
    "NVIDIA L4":                 "L4",
    "NVIDIA Tesla T4":           "T4",
    "NVIDIA Tesla T4G":          "T4",  # Graviton variant, same GPU
    "NVIDIA Tesla V100 PCIe 16GB": "Tesla V100 PCIe 16 GB",
    "NVIDIA Tesla V100 PCIe 32GB": "Tesla V100 PCIe 32 GB",
    "NVIDIA A10G":               "A10",  # A10G is the cloud variant of A10
    "Intel Gaudi HL-205":        None,   # predecessor to Gaudi2, not in our model
}


def main():
    if not os.path.exists(INPUT_PATH):
        print(f"File not found: {INPUT_PATH}")
        sys.exit(1)

    print(f"Reading {INPUT_PATH} (this may take a minute for 633MB)...")

    # Collect: (gpu_name, month) → list of per-GPU hourly prices
    monthly_prices = defaultdict(list)
    total_rows = 0
    matched_rows = 0

    with open(INPUT_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            if total_rows % 500000 == 0:
                print(f"  Processed {total_rows:,} rows...")

            cloud_name = row.get("gpu_name", "")
            our_name = CLOUD_GPU_MAP.get(cloud_name)
            if our_name is None:
                continue

            try:
                date = row["date"][:7]  # YYYY-MM
                num_gpus = float(row.get("num_gpus", 1) or 1)
                price_gpu = float(row.get("price_gpu", 0) or 0)

                # price_gpu is per-GPU per-hour in some rows, per-total in others
                # Use it directly as the per-GPU hourly rate
                if price_gpu <= 0 or price_gpu > 100:  # sanity: >$100/hr/GPU is junk
                    continue

                monthly_prices[(our_name, date)].append(price_gpu)
                matched_rows += 1
            except (ValueError, KeyError):
                continue

    print(f"\nTotal rows: {total_rows:,}")
    print(f"Matched rows: {matched_rows:,}")
    print(f"Unique (gpu, month) cells: {len(monthly_prices):,}")

    # Compute monthly stats
    rows = []
    for (gpu_name, month), prices in sorted(monthly_prices.items()):
        prices.sort()
        n = len(prices)
        median = prices[n // 2]
        p25 = prices[max(0, int(n * 0.25))]
        p75 = prices[min(n - 1, int(n * 0.75))]
        rows.append({
            "gpu_name": gpu_name,
            "month": month,
            "n_offers": n,
            "median_dph": f"{median:.4f}",
            "p25_dph": f"{p25:.4f}",
            "p75_dph": f"{p75:.4f}",
        })

    # Write
    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "gpu_name", "month", "n_offers", "median_dph", "p25_dph", "p75_dph"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} monthly summaries to {OUT_PATH}")

    # Summary
    print(f"\nGPU coverage:")
    gpu_months = defaultdict(int)
    for (gpu, _), _ in monthly_prices.items():
        gpu_months[gpu] += 1
    for gpu in sorted(gpu_months.keys()):
        print(f"  {gpu:<30} {gpu_months[gpu]:>4} months of cloud pricing data")


if __name__ == "__main__":
    main()
