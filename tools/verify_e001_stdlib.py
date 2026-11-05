#!/usr/bin/env python3
"""Independent reproduction of the E001 primary metrics for one session, standard library only.

Imports nothing from ``lpx`` and needs neither polars, pyarrow nor numpy. From the raw files it:

1. replays the Tardis ``incremental_book_L2`` file with plain dicts (consecutive rows with equal
   ``(is_snapshot, timestamp, local_timestamp)`` form one message; a snapshot batch resets the book), stamping each state
   with the running maximum of message times (exchange time; receive time for snapshots);
2. derives the validity window *itself* for a single-window session (no reconnect, a complete trade record and exactly
   one accepted joint window — 8 of the 15 discovery sessions):
   valid while the book is uncrossed and both touches stay inside the price range of the snapshot's 900 best levels per
   side (the acceptance rule); the window runs from the first valid state to the last valid state of the first unbroken
   run — and prints it next to the window in ``results/acceptance_001/windows.csv`` for comparison;
3. builds timestamp-side clusters from the exchange trade archive, takes the last state strictly before T as the
   pre-event state and the last state at or before T + h as the outcome, keeps events with T and T + 30 s in the window,
   and computes the session means of es, mo(h) and rs(h) (bp of the pre-event mid);
4. prints them next to ``results/e001/e001_discovery_per_session.csv``.

It does not regenerate silence, trade-gap or proven-region cuts that split a session into several windows: it refuses
sessions whose acceptance record shows reconnects or missing trades, or more than one joint window (on those it would
silently compute the first unbroken run only). It shares the vendor capture with the pipeline: it checks the
computation, not the data source.

Usage: python3 tools/verify_e001_stdlib.py [--day 2026-05-01] [--symbol SOLUSDT] [--root .]
"""

from __future__ import annotations

import argparse
import csv
import gzip
import io
import json
import zipfile
from pathlib import Path

PROVEN = 900
HORIZONS = (1, 5, 30)


def replay(path: Path):
    """Yield (time_us, best_bid, best_ask, ok) after every message; ok = uncrossed and inside the proven region."""
    bids: dict[float, float] = {}
    asks: dict[float, float] = {}
    floor = ceil = None
    t_run = -1
    prev_key = None
    snaps = 0

    def close(key):
        nonlocal t_run, floor, ceil
        if key is None:
            return None
        is_snap, ts, lts = key
        t = int(lts) if is_snap == "true" else int(ts)
        t_run = max(t_run, t)
        if is_snap == "true":
            sb = sorted(bids, reverse=True)
            sa = sorted(asks)
            floor = sb[min(PROVEN, len(sb)) - 1]
            ceil = sa[min(PROVEN, len(sa)) - 1]
        if not bids or not asks:
            return (t_run, None, None, False)
        bb, ba = max(bids), min(asks)
        ok = bb < ba and floor is not None and bb >= floor and ba <= ceil
        return (t_run, bb, ba, ok)

    with gzip.open(path, "rt") as f:
        for r in csv.DictReader(f):
            key = (r["is_snapshot"], r["timestamp"], r["local_timestamp"])
            if key != prev_key:
                out = close(prev_key)
                if out is not None:
                    yield out
                if r["is_snapshot"] == "true" and (prev_key is None or prev_key[0] != "true"):
                    bids.clear()
                    asks.clear()
                    snaps += 1
                    if snaps > 1:
                        raise SystemExit("session has a reconnect; this checker handles single-anchor sessions only")
                prev_key = key
            book = bids if r["side"] == "bid" else asks
            p, q = float(r["price"]), float(r["amount"])
            if q <= 0:
                book.pop(p, None)
            else:
                book[p] = q
        out = close(prev_key)
        if out is not None:
            yield out


def clusters(path: Path) -> list[tuple[int, int, float, float]]:
    """(T, sign, qty, vwap) per (trade time, aggressor side)."""
    acc: dict[tuple[int, int], list[float]] = {}
    with zipfile.ZipFile(path) as z, z.open(z.namelist()[0]) as f:
        for row in csv.reader(io.TextIOWrapper(f)):
            t, side = int(row[4]), (-1 if row[5] == "True" else 1)
            q, p = float(row[2]), float(row[1])
            a = acc.setdefault((t, side), [0.0, 0.0])
            a[0] += q
            a[1] += p * q
    return [(t, s, a[0], a[1] / a[0]) for (t, s), a in sorted(acc.items())]


def last_at_or_before(times: list[int], x: int, strict: bool) -> int:
    lo, hi = 0, len(times)
    while lo < hi:  # first index with times[i] >= x (strict) or > x (non-strict)
        mid = (lo + hi) // 2
        if times[mid] < x or (not strict and times[mid] == x):
            lo = mid + 1
        else:
            hi = mid
    return lo - 1


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--symbol", default="SOLUSDT")
    ap.add_argument("--day", default="2026-05-01")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    a = ap.parse_args()
    root = Path(a.root)
    acc = json.loads((root / "results/acceptance_001/summary.json").read_text())
    rec = next(r for r in acc["tardis"] if r["symbol"] == a.symbol and r["day"] == a.day)
    if rec["resyncs"] or rec["trades"]["missing_vs_reference"]:
        raise SystemExit("session has reconnects or missing trades; choose a single-window, complete session")
    pipeline_w = [(int(r["start_us"]), int(r["end_us"])) for r in csv.DictReader(open(root / "results/acceptance_001/windows.csv"))
                  if r["source"] == "tardis" and r["symbol"] == a.symbol and r["day"] == a.day and r["layer"] == "joint"]
    if len(pipeline_w) != 1:
        raise SystemExit(f"session has {len(pipeline_w)} joint windows; this checker reproduces single-window sessions only")

    states = list(replay(root / f"data/raw/tardis/binance/incremental_book_L2/{a.day}/{a.symbol}.csv.gz"))
    times = [s[0] for s in states]
    first = next(i for i, s in enumerate(states) if s[3])
    last = first
    while last + 1 < len(states) and states[last + 1][3]:
        last += 1
    w0, w1 = times[first], times[last]
    print(f"independent window: [{w0}, {w1}]  ({(w1 - w0) / 3.6e9:.6f} h); pipeline joint windows: {pipeline_w}")
    tail_invalid = sum(1 for s in states[last + 1:] if not s[3])
    print(f"states: {len(states):,}; invalid states after the run: {tail_invalid}")

    sums = {k: 0.0 for k in ["es"] + [f"mo_{h}s" for h in HORIZONS] + [f"rs_{h}s" for h in HORIZONS]}
    n = 0
    for T, s, q, vwap in clusters(root / f"data/raw/binance_vision/spot/daily/trades/{a.symbol}/{a.symbol}-trades-{a.day}.zip"):
        if not (w0 <= T <= w1 and T + 30_000_000 <= w1):
            continue
        i0 = last_at_or_before(times, T, strict=True)
        if i0 < first or i0 > last:
            continue
        m0 = (states[i0][1] + states[i0][2]) / 2
        es = 2 * s * (vwap - m0) / m0 * 1e4
        mo = {}
        for h in HORIZONS:
            ih = last_at_or_before(times, T + h * 1_000_000, strict=False)
            mo[h] = s * ((states[ih][1] + states[ih][2]) / 2 - m0) / m0 * 1e4
        sums["es"] += es
        for h in HORIZONS:
            sums[f"mo_{h}s"] += mo[h]
            sums[f"rs_{h}s"] += es - 2 * mo[h]
        n += 1
    ours = {k: v / n for k, v in sums.items()}
    per = {r["day"]: r for r in csv.DictReader(open(root / "results/e001/e001_discovery_per_session.csv"))}.get(a.day)
    print(f"events: {n:,}" + (f" (pipeline: {per['events']})" if per else ""))
    for k, v in ours.items():
        pv = f"{float(per[k]):+.6f}" if per and k in per else "n/a"
        print(f"{k:>6}: independent {v:+.6f} bp   pipeline {pv} bp")


if __name__ == "__main__":
    main()
