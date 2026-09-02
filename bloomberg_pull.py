"""
bloomberg_pull.py — One-time Bloomberg data export for GPU depreciation model.

Copy this file to the Windows PC running Bloomberg Terminal.
Open Bloomberg Terminal and log in, then run from Command Prompt:

    pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi
    pip install pandas
    python bloomberg_pull.py

If the first pip line fails, try:  pip install blpapi

Output:  Desktop/bloomberg_gpu_data/*.csv
"""

import sys
import os

try:
    import blpapi
except ImportError:
    print("blpapi not installed. Run:")
    print("  pip install --index-url=https://bcms.bloomberg.com/pip/simple/ blpapi")
    print("If that fails, try:  pip install blpapi")
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print("pandas not installed. Run:  pip install pandas")
    sys.exit(1)

from datetime import datetime


# ── Config ──────────────────────────────────────────────────────────────────

OUTPUT = os.path.join(os.path.expanduser("~"), "Desktop", "bloomberg_gpu_data")
os.makedirs(OUTPUT, exist_ok=True)

START = "20200101"
END   = datetime.today().strftime("%Y%m%d")


# ── Connection ──────────────────────────────────────────────────────────────

def connect():
    opts = blpapi.SessionOptions()
    opts.setServerHost("localhost")
    opts.setServerPort(8194)
    session = blpapi.Session(opts)
    if not session.start():
        print("ERROR: Cannot connect to Bloomberg.")
        print("Make sure Bloomberg Terminal is OPEN and LOGGED IN on this machine.")
        sys.exit(1)
    if not session.openService("//blp/refdata"):
        print("ERROR: Cannot open //blp/refdata service.")
        sys.exit(1)
    print("Connected to Bloomberg.\n")
    return session


# ── Generic historical pull ─────────────────────────────────────────────────

def pull(session, tickers, fields, start, end, period="DAILY"):
    """Pull historical data via HistoricalDataRequest. Returns DataFrame."""
    svc = session.getService("//blp/refdata")
    req = svc.createRequest("HistoricalDataRequest")

    for t in tickers:
        req.getElement("securities").appendValue(t)
    for f in fields:
        req.getElement("fields").appendValue(f)

    req.set("startDate", start)
    req.set("endDate", end)
    req.set("periodicitySelection", period)
    req.set("periodicityAdjustment", "ACTUAL")

    session.sendRequest(req)

    rows = []
    while True:
        ev = session.nextEvent(60000)

        if ev.eventType() == blpapi.Event.TIMEOUT:
            print("  Timeout waiting for Bloomberg response.")
            break

        for msg in ev:
            if not msg.hasElement("securityData"):
                continue

            sd = msg.getElement("securityData")
            ticker = sd.getElementAsString("security")

            # Security-level error (ticker not found / not entitled)
            if sd.hasElement("securityError"):
                try:
                    err = sd.getElement("securityError").getElementAsString("message")
                except Exception:
                    err = "unknown error"
                print(f"  SKIP {ticker}: {err}")
                continue

            # Field-level warnings
            if sd.hasElement("fieldExceptions"):
                fe = sd.getElement("fieldExceptions")
                for j in range(fe.numValues()):
                    try:
                        ex = fe.getValueAsElement(j)
                        fi = ex.getElementAsString("fieldId")
                        em = ex.getElement("errorInfo").getElementAsString("message")
                        print(f"  FIELD WARN {ticker}/{fi}: {em}")
                    except Exception:
                        pass

            # Extract data rows
            fd = sd.getElement("fieldData")
            for i in range(fd.numValues()):
                el = fd.getValueAsElement(i)
                rec = {"ticker": ticker}
                try:
                    rec["date"] = el.getElementAsString("date")
                except Exception:
                    continue
                for f in fields:
                    try:
                        rec[f] = el.getElementAsFloat(f) if el.hasElement(f) else None
                    except Exception:
                        rec[f] = None
                rows.append(rec)

        if ev.eventType() == blpapi.Event.RESPONSE:
            break

    df = pd.DataFrame(rows)
    if not df.empty and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(["ticker", "date"]).reset_index(drop=True)
    return df


def save(df, name):
    """Save DataFrame to CSV in OUTPUT directory."""
    path = os.path.join(OUTPUT, name)
    df.to_csv(path, index=False)
    return path


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    session = connect()

    # ── 0. Oracle capex (missing from original — 5th major hyperscaler) ────
    # Oracle's AI infrastructure spend (OCI GPU clusters) is a significant
    # demand signal for H100/H200 GPUs not captured by the original 5 tickers.
    print("[0/8] Adding Oracle to hyperscaler capex...")

    # ── 1. Hyperscaler quarterly capex ──────────────────────────────────────
    print("[1/6] Hyperscaler quarterly capex (MSFT, GOOGL, META, AMZN, NVDA)...")
    df = pull(session,
        tickers=["MSFT US Equity", "GOOGL US Equity", "META US Equity",
                 "AMZN US Equity", "NVDA US Equity", "ORCL US Equity"],
        fields=["CF_CAP_EXPENDITURE"],
        start=START, end=END, period="QUARTERLY")
    p = save(df, "capex_quarterly.csv")
    print(f"  {len(df)} rows -> {p}\n")

    # ── 2. NVDA total + TSMC quarterly revenue ──────────────────────────────
    print("[2/6] NVDA + TSMC quarterly revenue...")
    df = pull(session,
        tickers=["NVDA US Equity", "2330 TT Equity"],
        fields=["SALES_REV_TURN"],
        start=START, end=END, period="QUARTERLY")
    p = save(df, "nvda_tsmc_revenue_quarterly.csv")
    print(f"  {len(df)} rows -> {p}\n")

    # ── 3. NVDA datacenter segment (if available) ───────────────────────────
    # Segment fields are indexed — SEGMENT_REVENUES_1 may be Datacenter or
    # Compute & Networking depending on Bloomberg's ordering.
    # Pull both indexed segments; you'll identify them from the values.
    print("[3/6] NVDA segment revenue (indexed — verify which is Datacenter)...")
    df = pull(session,
        tickers=["NVDA US Equity"],
        fields=["SEGMENT_REVENUES_1", "SEGMENT_REVENUES_2",
                "SEGMENT_REVENUES_3", "SEGMENT_REVENUES_4"],
        start="20220101", end=END, period="QUARTERLY")
    p = save(df, "nvda_segments_quarterly.csv")
    if df.empty:
        print("  No segment data via BDH — use BDS on terminal instead.")
        print("  Terminal: BDS(\"NVDA US Equity\",\"IS_SEGMENT_REVENUE_DETAIL\")\n")
    else:
        print(f"  {len(df)} rows -> {p}")
        print("  NOTE: Verify which SEGMENT_REVENUES_N is Datacenter by comparing")
        print("  values against NVDA earnings releases.\n")

    # ── 4. BTC + ETH daily prices ───────────────────────────────────────────
    # ETH ticker varies by subscription — trying both
    print("[4/6] BTC + ETH daily prices...")
    df = pull(session,
        tickers=["XBT Curncy", "ETH Curncy", "XETH Curncy"],
        fields=["PX_LAST"],
        start=START, end=END, period="DAILY")

    # Deduplicate: keep whichever ETH ticker resolved with more data
    eth1 = df[df["ticker"] == "ETH Curncy"]
    eth2 = df[df["ticker"] == "XETH Curncy"]
    if len(eth1) > 0 and len(eth2) > 0:
        drop = "ETH Curncy" if len(eth2) > len(eth1) else "XETH Curncy"
        df = df[df["ticker"] != drop]
        kept = "XETH Curncy" if drop == "ETH Curncy" else "ETH Curncy"
        print(f"  Both ETH tickers resolved; keeping {kept} ({len(df[df['ticker']==kept])} rows)")
    elif len(eth2) > 0:
        print("  ETH Curncy not found, using XETH Curncy")
    elif len(eth1) > 0:
        print("  Using ETH Curncy")
    else:
        print("  WARNING: Neither ETH ticker resolved — check on terminal with DES <GO>")

    p = save(df, "crypto_daily.csv")
    print(f"  {len(df)} rows -> {p}\n")

    # ── 5. European wholesale electricity prices (monthly) ──────────────────
    # WHOLESALE day-ahead, NOT retail industrial tariffs.
    # For retail: use EIA (US free API) and Eurostat nrg_pc_204 (EU free).
    print("[5/6] Wholesale electricity prices (monthly)...")
    print("  NOTE: These are wholesale spot/day-ahead, not what a datacenter pays.")
    print("  Tickers may not all resolve — check warnings below.")
    power_tickers = [
        "EEXGBSLD Index",   # Germany EEX Baseload Day-Ahead
        "EPEXFRBA Index",   # France EPEX Spot
        "BNEGUKDA Index",   # UK N2EX Day-Ahead
        "ITPUNMKT Index",   # Italy PUN
        "OMIESDA Index",    # Spain OMIE
        "PJMWRTH Index",    # US PJM West Hub
        "JEPXDA Index",     # Japan JEPX
        "AESOPWR Index",    # Canada Alberta
    ]
    df = pull(session, tickers=power_tickers, fields=["PX_LAST"],
              start=START, end=END, period="MONTHLY")
    p = save(df, "electricity_wholesale_monthly.csv")
    resolved = df["ticker"].nunique() if not df.empty else 0
    print(f"  {resolved}/{len(power_tickers)} tickers resolved, {len(df)} rows -> {p}")
    if resolved < len(power_tickers):
        print("  If tickers failed: open ELEC <GO> on terminal, navigate to the country,")
        print("  note the actual ticker shown, and update the list above.\n")
    else:
        print()

    # ── 6. EU carbon price (drives European electricity costs) ──────────────
    print("[6/6] EU ETS carbon price (monthly)...")
    df = pull(session, tickers=["MO1 Comdty"], fields=["PX_LAST"],
              start=START, end=END, period="MONTHLY")
    p = save(df, "eu_carbon_monthly.csv")
    print(f"  {len(df)} rows -> {p}\n")

    # ── 7. Semiconductor equipment + AI indices ────────────────────────────
    # SOX (semiconductor index) and NVDA stock price as demand proxies.
    # NVDA stock tracks datacenter GPU demand better than any macro variable.
    print("[7/8] Semiconductor indices + NVDA price (monthly)...")
    df = pull(session,
        tickers=["SOX Index", "NVDA US Equity"],
        fields=["PX_LAST"],
        start=START, end=END, period="MONTHLY")
    p = save(df, "semiconductor_indices_monthly.csv")
    print(f"  {len(df)} rows -> {p}\n")

    # ── 8. Cloud GPU instance pricing (as a demand proxy) ──────────────────
    # No direct Bloomberg ticker for cloud GPU pricing, but NVDA's deferred
    # revenue (a proxy for enterprise GPU backlog) signals demand pressure.
    print("[8/8] NVDA deferred revenue + order backlog (quarterly)...")
    df = pull(session,
        tickers=["NVDA US Equity"],
        fields=["BS_DEFERRED_REVENUE", "TOTAL_BACKLOG"],
        start="20220101", end=END, period="QUARTERLY")
    p = save(df, "nvda_backlog_quarterly.csv")
    print(f"  {len(df)} rows -> {p}\n")

    session.stop()

    # ── Summary ─────────────────────────────────────────────────────────────
    print("=" * 60)
    print(f"DONE. All CSVs saved to:\n  {OUTPUT}")
    print("=" * 60)
    files = sorted(f for f in os.listdir(OUTPUT) if f.endswith(".csv"))
    for f in files:
        sz = os.path.getsize(os.path.join(OUTPUT, f))
        print(f"  {f:45s} {sz:>10,} bytes")

    print()
    print("Next steps:")
    print("  1. Copy the CSVs to gpu_modeling/data/external/ on your Mac")
    print("  2. For RETAIL electricity tariffs (what a DC actually pays):")
    print("     - US: api.eia.gov  field ELEC.PRICE.US-IND.M  (free, monthly)")
    print("     - EU: Eurostat nrg_pc_204  (free API, semi-annual)")
    print("  3. Verify NVDA segment indices by comparing values to earnings releases")
    print("  4. To build a demand-adjusted depreciation rate:")
    print("     - Compute trailing 4Q capex growth from capex_quarterly.csv")
    print("     - Compute NVDA datacenter revenue growth from nvda_segments_quarterly.csv")
    print("     - Use growth rate to scale the canonical k: fast growth → slower k")
    print("     - Feed adjusted k into depreciation_curves.py fit_constrained_floor()")


if __name__ == "__main__":
    main()
