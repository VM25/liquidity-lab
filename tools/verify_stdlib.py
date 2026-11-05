#!/usr/bin/env python3
"""Independent verification of Acceptance Test 001 headline numbers using the Python standard library only.

Written separately from ``lpx`` (it imports nothing from it, and needs neither polars, pyarrow nor numpy) so that a
reviewer can recompute key results from the raw files with any Python >= 3.9:

1. Tardis trades vs the exchange's own trade archive (Binance Vision) for one symbol-day: exchange trades missing from
   the vendor file inside the exchange day, extra vendor trades, and price/quantity/side disagreements.
2. A plain-dict replay of the Tardis ``incremental_book_L2`` file (rows in file order; consecutive rows with equal
   ``(is_snapshot, timestamp, local_timestamp)`` form one message; a snapshot batch resets the book) compared with the
   vendor's own ``quotes`` file at identical (timestamp, local_timestamp): best bid/ask price and size agreement, and
   crossed/locked books observed at message boundaries.
3. Joint-layer valid hours from ``results/acceptance_001/windows.csv`` (all windows, and windows >= 600 s).

Limits: (2) compares the replay with the *same vendor's* derived quotes, so it checks replay logic, not the vendor
capture; (3) sums the windows the pipeline wrote, it does not regenerate them. Neither reproduces E001 — see
tools/verify_e001_stdlib.py for that.

Usage: python3 tools/verify_stdlib.py [--symbol SOLUSDT] [--day 2026-05-01] [--root .]
Compare the printed numbers with results/acceptance_001/summary.json and results/data_acceptance_report.md.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import gzip
import io
import zipfile
from decimal import Decimal
from pathlib import Path


def day_bounds(day: str) -> tuple[int, int]:
    d = dt.datetime.fromisoformat(day).replace(tzinfo=dt.timezone.utc)
    t0 = int(d.timestamp()) * 1_000_000
    return t0, t0 + 86_400_000_000 - 1


def trades_check(root: Path, sym: str, day: str) -> dict:
    t0, t1 = day_bounds(day)
    vendor = {}
    with gzip.open(root / f"data/raw/tardis/binance/trades/{day}/{sym}.csv.gz", "rt") as f:
        for r in csv.DictReader(f):
            ts = int(r["timestamp"])
            if t0 <= ts <= t1:
                vendor[int(r["id"])] = (Decimal(r["price"]), Decimal(r["amount"]), r["side"], ts)
    ref = {}
    with zipfile.ZipFile(root / f"data/raw/binance_vision/spot/daily/trades/{sym}/{sym}-trades-{day}.zip") as z:
        with z.open(z.namelist()[0]) as f:
            for row in csv.reader(io.TextIOWrapper(f)):
                tid, price, qty, _, time_us, buyer_maker = int(row[0]), Decimal(row[1]), Decimal(row[2]), row[3], int(row[4]), row[5]
                ref[tid] = (price, qty, "sell" if buyer_maker == "True" else "buy", time_us)
    missing = [t for t in ref if t not in vendor]
    extra = [t for t in vendor if t not in ref]
    mism = {"price": 0, "qty": 0, "side": 0, "time": 0}
    for t, (p, q, s, ts) in vendor.items():
        if t in ref:
            rp, rq, rs, rts = ref[t]
            mism["price"] += p != rp
            mism["qty"] += q != rq
            mism["side"] += s != rs
            mism["time"] += ts != rts
    return {"exchange_trades": len(ref), "vendor_trades_in_day": len(vendor), "missing_from_vendor": len(missing),
            "extra_in_vendor": len(extra), "field_mismatches": mism}


def book_check(root: Path, sym: str, day: str) -> dict:
    quotes = {}
    with gzip.open(root / f"data/raw/tardis/binance/quotes/{day}/{sym}.csv.gz", "rt") as f:
        for r in csv.DictReader(f):
            quotes[(r["timestamp"], r["local_timestamp"])] = (Decimal(r["bid_price"]), Decimal(r["bid_amount"]),
                                                             Decimal(r["ask_price"]), Decimal(r["ask_amount"]))
    bids: dict[Decimal, Decimal] = {}
    asks: dict[Decimal, Decimal] = {}
    stats = {"messages": 0, "snapshots": 0, "crossed_or_locked": 0, "quotes_compared": 0, "quotes_equal": 0}
    prev_key = None

    def close(key):
        if key is None:
            return
        stats["messages"] += 1
        if bids and asks:
            bb, ba = max(bids), min(asks)
            stats["crossed_or_locked"] += bb >= ba
            qk = (key[1], key[2])
            if qk in quotes:
                stats["quotes_compared"] += 1
                stats["quotes_equal"] += quotes[qk] == (bb, bids[bb], ba, asks[ba])

    with gzip.open(root / f"data/raw/tardis/binance/incremental_book_L2/{day}/{sym}.csv.gz", "rt") as f:
        for r in csv.DictReader(f):
            key = (r["is_snapshot"], r["timestamp"], r["local_timestamp"])
            if key != prev_key:
                close(prev_key)
                if r["is_snapshot"] == "true":
                    bids.clear()
                    asks.clear()
                    stats["snapshots"] += 1
                prev_key = key
            book = bids if r["side"] == "bid" else asks
            p, q = Decimal(r["price"]), Decimal(r["amount"])
            if q == 0:
                book.pop(p, None)
            else:
                book[p] = q
        close(prev_key)
    stats["vendor_quote_rows"] = len(quotes)
    return stats


def windows_check(root: Path) -> dict:
    out: dict[str, list[float]] = {}
    with open(root / "results/acceptance_001/windows.csv", newline="") as f:
        for r in csv.DictReader(f):
            if r["source"] == "tardis" and r["layer"] == "joint":
                h = out.setdefault(r["symbol"], [0.0, 0.0])
                d = float(r["duration_s"])
                h[0] += d / 3600
                h[1] += d / 3600 if d >= 600 else 0.0
    return {s: {"joint_hours": round(a, 6), "joint_hours_in_windows_ge_600s": round(b, 6)} for s, (a, b) in sorted(out.items())}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--symbol", default="SOLUSDT")
    ap.add_argument("--day", default="2026-05-01")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    a = ap.parse_args()
    root = Path(a.root)
    print("trades vs exchange archive:", trades_check(root, a.symbol, a.day))
    print("plain-dict book replay vs vendor quotes:", book_check(root, a.symbol, a.day))
    print("joint valid hours from windows.csv:", windows_check(root))


if __name__ == "__main__":
    main()
