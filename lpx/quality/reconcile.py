"""Reconcile a rerun of Acceptance Test 001 against the artifacts stored at a reference commit.

* summary.json is compared field by field (recursive). Every difference must match an entry of ``EXPECTED`` — a named
  code or rule change with its explanation — or it is reported as UNEXPLAINED.
* windows.csv is compared window by window and column by column. Boundary changes must equal exactly the effect of
  the 2026-10-19 resync-break fix: no new coverage anywhere, and the coverage removed equals the reconnect gaps that the
  old windows spanned.

Output: results/acceptance_001/reconciliation.json.
Usage: ``uv run python -m lpx.quality.reconcile [<reference commit>]``  (default: the repository's root commit)
"""

from __future__ import annotations

import datetime as dt
import io
import json
import re
import subprocess
import sys

import numpy as np
import polars as pl

from lpx.data.acquire import ROOT
from lpx.provenance import provenance, require_clean

OUT = ROOT / "results" / "acceptance_001"
WKEY = ["source", "symbol", "day", "layer", "start_us", "end_us"]

# path regex -> explanation of an expected difference (anything else is UNEXPLAINED)
EXPECTED = [
    (r"^(run_at_utc|code_fingerprint)$", "new run"),
    (r"^(provenance|eligibility_rule)(\.|$)", "added 2026-10-19: run provenance / post-hoc eligibility rule"),
    (r"^tardis\.\d+\.(eligibility|normalized_inputs_sha256|raw_time_regressions)(\.|$)",
     "added 2026-10-19: eligibility label / input hashes / raw time-regression count"),
    (r"^hf_lobstream\.\d+\.normalized_inputs_sha256(\.|$)", "added 2026-10-19: input hashes"),
    (r"^rest_snapshot_checks\.\d+\.alignment(\.|$)", "added 2026-10-19: alignment uniqueness"),
    (r"^tardis\.\d+\.coverage_(book|joint)\.", "resync-break fix: windows no longer span vendor reconnect gaps"),
    (r"^tardis\.\d+\.trade_depth_linkage\.", "resync-break fix: linkage is measured on trades inside the (now narrower) book windows"),
    (r"^tardis\.\d+\.invalid_intervals\.trade_record_gaps", "order of runs now deterministic (maintain_order); compared as a set"),
    (r"^tardis\.\d+\.note_time_axis$", "state times now the running maximum of message times (engine.state_times): always monotone"),
]


def at_commit(commit: str, path: str) -> str:
    return subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def root_commit() -> str:
    return subprocess.run(["git", "rev-list", "--max-parents=0", "HEAD"], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.split()[0]


def flatten(x, prefix="") -> dict:
    out = {}
    if isinstance(x, dict):
        for k, v in x.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out.update(flatten(v, f"{prefix}.{i}"))
    else:
        out[prefix] = x
    return out


def explain(path: str) -> str | None:
    for pat, why in EXPECTED:
        if re.search(pat, path):
            return why
    return None


def resync_gaps(summary: dict) -> dict[tuple[str, str], list[tuple[int, int]]]:
    """(symbol, day) -> [(last pre-gap message time, resync snapshot time)] in microseconds."""
    out = {}
    for r in summary["tardis"]:
        g = []
        for x in r["resyncs"]:
            t_snap = int(dt.datetime.fromisoformat(x["snapshot_local_time"]).timestamp() * 1e6)
            g.append((t_snap - int(round(x["gap_last_diff_to_snapshot_ms"] * 1000)), t_snap))
        out[(r["symbol"], r["day"])] = g
    return out


def main(ref: str | None = None) -> dict:
    require_clean()
    ref = ref or root_commit()
    old = json.loads(at_commit(ref, "results/acceptance_001/summary.json"))
    new = json.loads((OUT / "summary.json").read_text())
    rows, unexplained = [], []

    # ---- summary.json, recursively
    fo, fn = flatten(old), flatten(new)
    # trade-record gap intervals: compare as sets per symbol-day
    for side in (fo, fn):
        for k in [k for k in side if re.search(r"invalid_intervals\.trade_record_gaps\.", k)]:
            side.pop(k)
    gap_sets_equal = all(
        sorted(map(tuple, a["invalid_intervals"]["trade_record_gaps"])) == sorted(map(tuple, b["invalid_intervals"]["trade_record_gaps"]))
        for a, b in zip(old["tardis"], new["tardis"]))
    rows.append({"quantity": "trade-record gap intervals (as sets, all symbol-days)", "old": "-", "new": "identical" if gap_sets_equal else "DIFFERENT",
                 "diff": None, "explanation": "identical" if gap_sets_equal else "UNEXPLAINED"})
    by_reason: dict[str, int] = {}
    for k in sorted(set(fo) | set(fn)):
        a, b = fo.get(k, "<absent>"), fn.get(k, "<absent>")
        same = a == b or (isinstance(a, float) and isinstance(b, float) and np.isclose(a, b, rtol=0, atol=1e-12))
        if same:
            continue
        why = explain(k)
        if why is None:
            unexplained.append({"path": k, "old": a, "new": b})
        else:
            by_reason[why] = by_reason.get(why, 0) + 1
    for why, n in by_reason.items():
        rows.append({"quantity": "summary.json fields changed", "old": "-", "new": n, "diff": None, "explanation": why})
    rows.append({"quantity": "summary.json fields changed without an identified cause", "old": 0, "new": len(unexplained), "diff": None,
                 "explanation": "none" if not unexplained else "UNEXPLAINED"})

    # ---- windows.csv
    Wo = pl.read_csv(io.StringIO(at_commit(ref, "results/acceptance_001/windows.csv")))
    Wn = pl.read_csv(OUT / "windows.csv")
    ko, kn = set(map(tuple, Wo.select(WKEY).rows())), set(map(tuple, Wn.select(WKEY).rows()))
    rows.append({"quantity": "windows identical in boundaries", "old": len(ko), "new": len(ko & kn), "diff": None, "explanation": "-"})
    rows.append({"quantity": "windows only in old / only in new", "old": len(ko - kn), "new": len(kn - ko), "diff": None,
                 "explanation": "resync-break fix (checked below)" if (ko - kn) else "identical"})
    gaps = resync_gaps(new)
    new_outside_old, removed_us, expected_us = 0, 0, 0
    for (src, sym, day, layer) in sorted({k[:4] for k in ko | kn}):
        o = Wo.filter((pl.col("source") == src) & (pl.col("symbol") == sym) & (pl.col("day") == day) & (pl.col("layer") == layer))
        n = Wn.filter((pl.col("source") == src) & (pl.col("symbol") == sym) & (pl.col("day") == day) & (pl.col("layer") == layer))
        oiv = list(o.select("start_us", "end_us").iter_rows())
        niv = list(n.select("start_us", "end_us").iter_rows())
        for a, b in niv:  # every new window must lie inside an old one
            if not any(x <= a and b <= y for x, y in oiv):
                new_outside_old += 1
        removed_us += sum(y - x for x, y in oiv) - sum(b - a for a, b in niv)
        if src == "tardis":
            for g0, g1 in gaps.get((sym, day), []):  # old coverage inside a reconnect gap (g0, g1) -> must be removed
                expected_us += sum(max(0, min(y, g1) - max(x, g0)) for x, y in oiv)
    rows.append({"quantity": "new windows not contained in an old window", "old": 0, "new": new_outside_old, "diff": None,
                 "explanation": "none" if new_outside_old == 0 else "UNEXPLAINED"})
    ok = abs(removed_us - expected_us) <= 0
    rows.append({"quantity": "coverage removed vs old coverage inside reconnect gaps (s, all layers)",
                 "old": round(expected_us / 1e6, 6), "new": round(removed_us / 1e6, 6), "diff": round((removed_us - expected_us) / 1e6, 6),
                 "explanation": "resync-break fix removes exactly the spanned reconnect gaps" if ok else "UNEXPLAINED"})
    # columns of windows whose boundaries did not change
    j = Wo.join(Wn, on=WKEY, how="inner", suffix="_new")
    snaps = {(r["symbol"], r["day"]): {int(dt.datetime.fromisoformat(x["local_time"]).timestamp() * 1e6) for x in r["snapshots"]}
             for r in new["tardis"]}
    for col in ("trades", "notional_quote", "median_touch_qty", "mid_first", "n_msgs", "duration_s"):
        changed = j.filter((pl.col(f"{col}_new").is_null() != pl.col(col).is_null())
                           | ((pl.col(f"{col}_new") - pl.col(col)).abs() > 1e-9 * pl.col(col).abs().clip(lower_bound=1.0)).fill_null(False))
        dd = (changed[f"{col}_new"] - changed[col]).abs().drop_nulls()
        mx = float(dd.max()) if dd.len() else (float("nan") if changed.height else 0.0)
        why = "identical"
        if changed.height:
            at_anchor = all(r["start_us"] in snaps.get((r["symbol"], r["day"]), set()) for r in changed.iter_rows(named=True))
            regress = {(r["symbol"], r["day"]): r.get("raw_time_regressions", 0) for r in new["tardis"]}
            within = all(abs(r[f"{col}_new"] - r[col]) <= regress.get((r["symbol"], r["day"]), 0) for r in changed.iter_rows(named=True))
            if col in ("mid_first", "median_touch_qty") and at_anchor:
                why = "window statistics now include anchor (snapshot) states: all changed windows start at a snapshot"
            elif col == "n_msgs" and within:
                why = ("state times are now the running maximum: a diff stamped earlier than the snapshot it follows is "
                       "counted in its window; every change is within the session's raw time-regression count")
            else:
                why = "UNEXPLAINED"
        rows.append({"quantity": f"unchanged windows: {col} (windows changed / max abs change)", "old": 0,
                     "new": f"{changed.height} / {mx:.6g}", "diff": None, "explanation": why})
    # event-mean spread is the old mean_spread_ticks under a corrected name; it may differ only where anchor states entered
    if "mean_spread_ticks" in Wo.columns:
        ch = j.filter((pl.col("event_mean_spread_ticks").is_null() != pl.col("mean_spread_ticks").is_null())
                      | ((pl.col("event_mean_spread_ticks") - pl.col("mean_spread_ticks")).abs() > 1e-9).fill_null(False))
        at_anchor = all(r["start_us"] in snaps.get((r["symbol"], r["day"]), set()) for r in ch.iter_rows(named=True))
        dd = (ch["event_mean_spread_ticks"] - ch["mean_spread_ticks"]).abs().drop_nulls()
        rows.append({"quantity": "unchanged windows: event-mean spread vs old mean_spread_ticks (windows changed / max abs change)",
                     "old": 0, "new": f"{ch.height} / {float(dd.max()) if dd.len() else 0.0:.3g}", "diff": None,
                     "explanation": ("identical" if ch.height == 0 else
                                     "anchor (snapshot) states now included: all changed windows start at a snapshot" if at_anchor
                                     else "UNEXPLAINED")})
    if "integrity_status" in Wn.columns:
        bad = Wn.filter((pl.col("source") == "tardis") & (pl.col("integrity_status") != "accepted")).height
        rows.append({"quantity": "Tardis windows from sessions failing integrity", "old": "-", "new": bad, "diff": None,
                     "explanation": "none" if bad == 0 else "UNEXPLAINED"})
    rows.append({"quantity": "unchanged windows: spread/RV columns", "old": "mean_spread_ticks, rv_1min_bps",
                 "new": "twa_spread_ticks, event_mean_spread_ticks, rv_1min_bp, n_valid_states", "diff": None,
                 "explanation": "estimators corrected 2026-10-19 (time weighting incl. anchor states; RV ddof=1, >=3 returns)"})
    unexplained += [{"path": r["quantity"]} for r in rows if r["explanation"] == "UNEXPLAINED"]
    res = {"reference_commit": ref, "reference_code_fingerprint": old.get("code_fingerprint"),
           "provenance": provenance(["configs/acceptance_001.toml"]), "new_run_provenance": new.get("provenance"),
           "rows": rows, "unexplained": unexplained}
    (OUT / "reconciliation.json").write_text(json.dumps(res, indent=1, default=str))
    return res


if __name__ == "__main__":
    r = main(sys.argv[1] if len(sys.argv) > 1 else None)
    for x in r["rows"]:
        print(f"{x['quantity']}: {x['old']} -> {x['new']}  [{x['explanation']}]")
    print("UNEXPLAINED:", r["unexplained"][:20])
