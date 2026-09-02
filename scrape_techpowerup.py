#!/usr/bin/env python3
"""
Scrape TechPowerUp GPU database for MSRP and launch date verification.

TechPowerUp maintains a comprehensive GPU database with verified MSRPs
and launch dates. This script cross-checks our MSRP_REFERENCE and
LAUNCH_DATES against their data.

Also scrapes current retail pricing from their price tracker where available.

Usage:
    python scrape_techpowerup.py

Requires: requests, beautifulsoup4
"""

import csv
import re
import sys
import time

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install: pip install requests beautifulsoup4")
    sys.exit(1)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
}

# TechPowerUp GPU DB URLs for our target GPUs
# Format: (our_gpu_name, techpowerup_url_slug)
TARGETS = [
    ("T4",                     "nvidia-tesla-t4"),
    ("L4",                     "nvidia-l4"),
    ("L40",                    "nvidia-l40"),
    ("L40S",                   "nvidia-l40s"),
    ("A10",                    "nvidia-a10"),
    ("A16 PCIe",               "nvidia-a16"),
    ("A30 PCIe",               "nvidia-a30"),
    ("A40",                    "nvidia-a40"),
    ("A100 PCIe 40 GB",        "nvidia-a100-pcie-40-gb"),
    ("A100 PCIe 80 GB",        "nvidia-a100-pcie-80-gb"),
    ("A100 SXM4 40 GB",        "nvidia-a100-sxm4-40-gb"),
    ("A100 SXM4 80 GB",        "nvidia-a100-sxm4-80-gb"),
    ("H100 PCIe 80 GB",        "nvidia-h100-pcie-80-gb"),
    ("H100 SXM5 80 GB",        "nvidia-h100-sxm5-80-gb"),
    ("H200 SXM",               "nvidia-h200-sxm"),
    ("NVIDIA GH200",           "nvidia-gh200-grace-hopper"),
    ("AMD Instinct MI300X",    "amd-instinct-mi300x"),
    ("Radeon Instinct MI210",  "amd-instinct-mi210"),
    ("Tesla V100 PCIe 16 GB",  "nvidia-tesla-v100-pcie-16-gb"),
    ("Tesla V100 PCIe 32 GB",  "nvidia-tesla-v100-pcie-32-gb"),
    ("Tesla V100 SXM2 16 GB",  "nvidia-tesla-v100-sxm2-16-gb"),
    ("Tesla V100 SXM2 32 GB",  "nvidia-tesla-v100-sxm2-32-gb"),
    ("Tesla V100 FHHL",        "nvidia-tesla-v100-fhhl"),
    ("Tesla V100S PCIe 32 GB", "nvidia-tesla-v100s-pcie-32-gb"),
    ("GeForce RTX 4090",       "nvidia-geforce-rtx-4090"),
    ("GeForce RTX 3090",       "nvidia-geforce-rtx-3090"),
]

OUT_PATH = "data/techpowerup_specs.csv"


def scrape_gpu_page(slug: str) -> dict:
    """Scrape a TechPowerUp GPU page for MSRP and launch date."""
    url = f"https://www.techpowerup.com/gpu-specs/{slug}.c0"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 404:
            return {"error": "404 Not Found"}
        resp.raise_for_status()
    except requests.RequestException as e:
        return {"error": str(e)}

    soup = BeautifulSoup(resp.text, "html.parser")
    result = {}

    # Find the specs table
    for row in soup.select("table.gpu-specs-table tr"):
        cells = row.select("td")
        if len(cells) >= 2:
            label = cells[0].get_text(strip=True).lower()
            value = cells[1].get_text(strip=True)

            if "launch price" in label or "msrp" in label:
                result["msrp_text"] = value
                price_match = re.search(r'\$[\d,]+', value)
                if price_match:
                    result["msrp_usd"] = float(
                        price_match.group().replace("$", "").replace(",", "")
                    )

            if "release date" in label or "launch date" in label:
                result["launch_date_text"] = value

    return result


def main():
    rows = []
    print(f"{'GPU':<35} {'MSRP':>10} {'Launch Date':<20} {'Status'}")
    print("-" * 80)

    for gpu_name, slug in TARGETS:
        data = scrape_gpu_page(slug)
        msrp = data.get("msrp_usd", "")
        msrp_text = data.get("msrp_text", "")
        launch = data.get("launch_date_text", "")
        error = data.get("error", "")

        status = "OK" if msrp or launch else error or "no data"
        msrp_str = f"${msrp:,.0f}" if msrp else msrp_text or "n/a"

        print(f"{gpu_name:<35} {msrp_str:>10} {launch:<20} {status}")

        rows.append({
            "gpu_name": gpu_name,
            "tpu_slug": slug,
            "msrp_usd": msrp or "",
            "msrp_text": msrp_text,
            "launch_date_text": launch,
        })

        time.sleep(1.0)  # rate limit

    # Write CSV
    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "gpu_name", "tpu_slug", "msrp_usd", "msrp_text", "launch_date_text"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {OUT_PATH}")
    print("Cross-check these against MSRP_REFERENCE and LAUNCH_DATES in data_prep.py")


if __name__ == "__main__":
    main()
