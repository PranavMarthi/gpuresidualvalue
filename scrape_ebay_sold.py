#!/usr/bin/env python3
"""
Scrape eBay completed/sold listings for datacenter GPUs with thin data.

Produces rows in the same format as scraped_datacenter_supplement.csv:
    gpu_name, date, price_usd, condition, source, confidence, notes

Usage:
    python scrape_ebay_sold.py

Requires: requests, beautifulsoup4
    pip install requests beautifulsoup4
"""

import csv
import re
import sys
import time
from datetime import datetime, timedelta

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Install dependencies:  pip install requests beautifulsoup4")
    sys.exit(1)

# ── GPUs we need data for, with eBay search queries ──────────────────────────

TARGETS = [
    # (gpu_name in our model, eBay search query, MSRP for sanity check)
    ("H100 SXM5 64 GB",       "NVIDIA H100 SXM 64GB -server -system -DGX",           25000),
    ("H100 SXM5 80 GB",       "NVIDIA H100 SXM 80GB -server -system -DGX",           30000),
    ("H100 SXM5 94 GB",       "NVIDIA H100 SXM 94GB -server -system -DGX",           33000),
    ("H100 PCIe 80 GB",       "NVIDIA H100 PCIe 80GB -server -system -DGX",          25599),
    ("H200 SXM",              "NVIDIA H200 SXM -server -system -DGX",                35000),
    ("H200 NVL",              "NVIDIA H200 NVL -server -system -DGX",                32000),
    ("NVIDIA GH200",          "NVIDIA GH200 Grace Hopper -server -system",           35000),
    ("AMD Instinct MI300X",   "AMD Instinct MI300X -server -system",                 15000),
    ("Gaudi2 HL-225H",        "Intel Gaudi 2 HL-225H",                                8125),
    ("Radeon Instinct MI210", "AMD Instinct MI210 -server -system",                   7500),
    # V100 SXM2 and FHHL excluded from model — see data_prep.py LAUNCH_DATES comment
    ("A100X",                 "NVIDIA A100X BlueField",                               17500),
    ("L4",                    "NVIDIA L4 24GB Tensor -laptop",                         2500),
    ("L40",                   "NVIDIA L40 48GB -L40S",                                 7500),
    ("L40S",                  "NVIDIA L40S 48GB",                                      7500),
    ("GeForce RTX 4090 D",    "GeForce RTX 4090 D 24GB -4090D",                       1599),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

OUT_PATH = "data/ebay_sold_supplement.csv"


def search_ebay_sold(query: str, max_pages: int = 3) -> list[dict]:
    """Search eBay completed/sold listings and extract prices."""
    results = []
    for page in range(1, max_pages + 1):
        url = (
            "https://www.ebay.com/sch/i.html"
            f"?_nkw={requests.utils.quote(query)}"
            f"&_pgn={page}"
            "&LH_Complete=1"   # completed listings
            "&LH_Sold=1"      # actually sold (not just ended)
            "&_sop=13"        # sort by end date newest first
            "&rt=nc"
            "&LH_ItemCondition=3000|1000|1500|2000|2500"  # new + used + refurb
        )
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"  [!] Page {page} failed: {e}")
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select("li.s-item")

        if not items:
            break

        for item in items:
            try:
                # Title
                title_el = item.select_one(".s-item__title")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                if title.lower().startswith("shop on ebay"):
                    continue

                # Price
                price_el = item.select_one(".s-item__price")
                if not price_el:
                    continue
                price_text = price_el.get_text(strip=True)
                # Handle "US $1,234.56" or "$1,234.56" or price ranges
                price_match = re.search(r'\$[\d,]+\.?\d*', price_text)
                if not price_match:
                    continue
                price = float(price_match.group().replace("$", "").replace(",", ""))

                # Condition
                cond_el = item.select_one(".SECONDARY_INFO")
                condition = "USED"
                if cond_el:
                    cond_text = cond_el.get_text(strip=True).upper()
                    if "NEW" in cond_text or "BRAND NEW" in cond_text:
                        condition = "NEW"
                    elif "REFURBISHED" in cond_text or "RENEWED" in cond_text:
                        condition = "REFURBISHED"

                # Date (eBay sold date)
                date_el = item.select_one(".s-item__title--tag .POSITIVE")
                sold_date = datetime.now().strftime("%Y-%m-%d")  # fallback
                if date_el:
                    date_text = date_el.get_text(strip=True)
                    date_match = re.search(r'(\w+ \d+, \d{4})', date_text)
                    if date_match:
                        try:
                            sold_date = datetime.strptime(
                                date_match.group(1), "%b %d, %Y"
                            ).strftime("%Y-%m-%d")
                        except ValueError:
                            pass

                results.append({
                    "title": title,
                    "price": price,
                    "condition": condition,
                    "date": sold_date,
                })
            except Exception:
                continue

        time.sleep(1.5)  # rate limit

    return results


def filter_results(results: list[dict], msrp: float) -> list[dict]:
    """Remove obvious junk: accessories, multi-GPU systems, extreme prices."""
    filtered = []
    for r in results:
        title_lower = r["title"].lower()

        # Skip accessories, brackets, cables
        skip_words = ["bracket", "cable", "adapter", "heatsink", "fan",
                       "cooler", "backplate", "riser", "tray", "dummy",
                       "for parts", "not working", "defective", "broken"]
        if any(w in title_lower for w in skip_words):
            continue

        # Skip multi-GPU systems (DGX, HGX, servers)
        system_words = ["dgx", "hgx", "server", "system", "8x ", "4x ",
                         "supermicro", "dell poweredge", "lenovo thinksystem"]
        if any(w in title_lower for w in system_words):
            continue

        # Price sanity: between 5% and 300% of MSRP
        if r["price"] < msrp * 0.05 or r["price"] > msrp * 3.0:
            continue

        filtered.append(r)
    return filtered


def main():
    all_rows = []
    for gpu_name, query, msrp in TARGETS:
        print(f"\n{'='*60}")
        print(f"Searching: {gpu_name}")
        print(f"  Query: {query}")

        results = search_ebay_sold(query, max_pages=3)
        print(f"  Raw results: {len(results)}")

        filtered = filter_results(results, msrp)
        print(f"  After filtering: {len(filtered)}")

        for r in filtered:
            all_rows.append({
                "gpu_name": gpu_name,
                "date": r["date"],
                "price_usd": f"{r['price']:.2f}",
                "condition": r["condition"],
                "source": "eBay sold listing (scraped)",
                "confidence": "HIGH",
                "notes": r["title"][:100],
            })
            print(f"    {r['date']}  ${r['price']:>10,.2f}  {r['condition']:<5}  {r['title'][:60]}")

        time.sleep(2)  # be nice between GPU searches

    # Write output
    if all_rows:
        with open(OUT_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "gpu_name", "date", "price_usd", "condition",
                "source", "confidence", "notes"
            ])
            writer.writeheader()
            writer.writerows(all_rows)
        print(f"\n{'='*60}")
        print(f"Wrote {len(all_rows)} rows to {OUT_PATH}")
        print(f"To merge: append rows to data/scraped_datacenter_supplement.csv")
    else:
        print("\nNo results found.")


if __name__ == "__main__":
    main()
