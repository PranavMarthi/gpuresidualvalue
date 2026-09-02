#!/usr/bin/env python3
"""
Query Vast.ai public API for current GPU rental pricing.

Vast.ai lists secondary-market GPU rentals. The on-demand price per hour
can be converted to an implied asset value using standard lease-rate
assumptions (useful as a cross-check for depreciation models).

Produces a CSV with current rental rates and implied GPU values.

Usage:
    python scrape_vastai.py

Requires: requests
    pip install requests
"""

import csv
import json
import sys
import time
from datetime import datetime

try:
    import requests
except ImportError:
    print("Install: pip install requests")
    sys.exit(1)

# ── Target GPUs to look up ───────────────────────────────────────────────────

# Maps our model gpu_name → Vast.ai gpu_name patterns
GPU_MAP = {
    "T4":                    ["Tesla T4", "T4"],
    "L4":                    ["L4"],
    "L40":                   ["L40"],
    "L40S":                  ["L40S"],
    "A10":                   ["A10"],
    "A16 PCIe":              ["A16"],
    "A30 PCIe":              ["A30"],
    "A40":                   ["A40"],
    "A100 SXM4 40 GB":       ["A100 SXM4 40GB", "A100-SXM4-40GB"],
    "A100 SXM4 80 GB":       ["A100 SXM4 80GB", "A100-SXM4-80GB"],
    "A100 PCIe 40 GB":       ["A100 PCIe 40GB", "A100-PCIE-40GB"],
    "A100 PCIe 80 GB":       ["A100 PCIe 80GB", "A100-PCIE-80GB"],
    "H100 SXM5 80 GB":       ["H100 SXM5 80GB", "H100-SXM5-80GB", "H100 SXM"],
    "H100 PCIe 80 GB":       ["H100 PCIe 80GB", "H100-PCIE-80GB", "H100 PCIe"],
    "H200 SXM":              ["H200"],
    "AMD Instinct MI300X":   ["MI300X"],
    "Radeon Instinct MI210": ["MI210"],
    "Tesla V100 PCIe 16 GB": ["V100 PCIe 16GB", "Tesla V100"],
    "Tesla V100 PCIe 32 GB": ["V100 PCIe 32GB"],
    "Tesla V100 SXM2 16 GB": ["V100 SXM2 16GB", "V100 SXM2"],
    "Tesla V100 SXM2 32 GB": ["V100 SXM2 32GB"],
    "GeForce RTX 3090":      ["RTX 3090"],
    "GeForce RTX 4090":      ["RTX 4090"],
}

VAST_API = "https://cloud.vast.ai/api/v0/bundles/"
OUT_PATH = "data/vastai_pricing.csv"


def query_vast_offers():
    """Pull current Vast.ai marketplace offers."""
    print("Querying Vast.ai API...")
    params = {
        "q": json.dumps({
            "verified": {"eq": True},
            "rentable": {"eq": True},
            "type": "on-demand",
            "order": [["dph_total", "asc"]],
            "limit": 2000,
        })
    }
    try:
        resp = requests.get(VAST_API, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        offers = data.get("offers", [])
        print(f"  Got {len(offers)} offers")
        return offers
    except Exception as e:
        print(f"  API error: {e}")
        return []


def match_gpu(gpu_name_vast: str):
    """Match a Vast.ai GPU name to our model's gpu_name."""
    for our_name, patterns in GPU_MAP.items():
        for pat in patterns:
            if pat.lower() in gpu_name_vast.lower():
                return our_name
    return None


def main():
    offers = query_vast_offers()
    if not offers:
        print("No offers returned. The Vast.ai API may require auth or have changed.")
        print("Try: curl 'https://cloud.vast.ai/api/v0/bundles/?q={\"verified\":{\"eq\":true},\"rentable\":{\"eq\":true},\"type\":\"on-demand\",\"limit\":10}'")
        return

    # Aggregate: for each GPU, collect all per-hour prices
    gpu_prices = {}
    for offer in offers:
        gpu_name_vast = offer.get("gpu_name", "")
        num_gpus = offer.get("num_gpus", 1)
        dph = offer.get("dph_total", 0)  # dollars per hour total
        if num_gpus < 1 or dph <= 0:
            continue

        per_gpu_dph = dph / num_gpus
        our_name = match_gpu(gpu_name_vast)
        if our_name:
            gpu_prices.setdefault(our_name, []).append({
                "dph": per_gpu_dph,
                "vast_name": gpu_name_vast,
                "num_gpus": num_gpus,
            })

    # Compute stats and implied values
    today = datetime.now().strftime("%Y-%m-%d")
    rows = []
    print(f"\n{'GPU':<35} {'Offers':>6} {'Med $/hr':>8} {'Implied $':>10}  {'Range $/hr'}")
    print("-" * 85)

    for our_name in sorted(gpu_prices.keys()):
        prices = gpu_prices[our_name]
        dphs = sorted([p["dph"] for p in prices])
        n = len(dphs)
        median_dph = dphs[n // 2]
        p10 = dphs[max(0, int(n * 0.1))]
        p90 = dphs[min(n - 1, int(n * 0.9))]

        # Implied asset value: assume 3-year payback at 50% utilization
        # Value ≈ median_hourly * 8760 hours/year * 3 years * 0.5 utilization
        implied_value = median_dph * 8760 * 3 * 0.5

        print(f"{our_name:<35} {n:>6} {median_dph:>8.3f} {implied_value:>10,.0f}  "
              f"[{p10:.3f} – {p90:.3f}]")

        rows.append({
            "gpu_name": our_name,
            "date": today,
            "n_offers": n,
            "median_dph": f"{median_dph:.4f}",
            "p10_dph": f"{p10:.4f}",
            "p90_dph": f"{p90:.4f}",
            "implied_value_3yr": f"{implied_value:.0f}",
        })

    # Write CSV
    if rows:
        with open(OUT_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "gpu_name", "date", "n_offers", "median_dph",
                "p10_dph", "p90_dph", "implied_value_3yr"
            ])
            writer.writeheader()
            writer.writerows(rows)
        print(f"\nWrote {len(rows)} GPU summaries to {OUT_PATH}")


if __name__ == "__main__":
    main()
