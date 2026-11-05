"""Fill the evidence tables of results/data_acceptance_report.md from the acceptance artifacts.

The narrative is written by hand; every number in a table is machine-generated from results/acceptance_001/
(summary.json, windows.csv) and data/raw/manifest.jsonl, between ``<!-- BEGIN:name -->`` / ``<!-- END:name -->`` markers.

Usage: ``uv run python -m lpx.quality.report``
"""

from __future__ import annotations

import datetime as dt
import json
import re
from collections import defaultdict

import polars as pl

from lpx.data.acquire import ROOT, load_manifest

OUT = ROOT / "results" / "acceptance_001"
REPORT = ROOT / "results" / "data_acceptance_report.md"
SENS = OUT / "sensitivity.json"
RECON = OUT / "reconciliation.json"


def md(headers: list[str], rows: list[list]) -> str:
    def f(x):
        if isinstance(x, float):
            return f"{x:,.4f}" if abs(x) < 10 else f"{x:,.1f}"
        if isinstance(x, int):
            return f"{x:,}"
        return "" if x is None else str(x)
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(f(x) for x in r) + " |" for r in rows]
    return "\n".join(out)


def pct(x: float | None, d: int = 2) -> str:
    return "n/a" if x is None else f"{100 * x:.{d}f}%"


def tables(S: dict, W: pl.DataFrame) -> dict[str, str]:
    T: dict[str, str] = {}
    man = load_manifest()
    agg = defaultdict(lambda: [0, 0, 0, 0])
    for rec in man.values():
        a = agg[rec["source"]]
        a[0] += 1
        a[1] += rec["bytes"]
        a[2] += rec["checksum_verified"] is True
        a[3] += rec["checksum_verified"] is None
    T["manifest"] = md(["source", "files", "GB", "publisher checksum verified", "no publisher checksum (sha256 recorded)"],
                       [[k, v[0], f"{v[1] / 1e9:.2f}", v[2], v[3]] for k, v in sorted(agg.items())])

    rows = []
    for r in S["tardis"]:
        t, cj = r["trades"], r["coverage_joint"]
        ref_mid = None
        w = W.filter((pl.col("source") == "tardis") & (pl.col("symbol") == r["symbol"]) & (pl.col("day") == r["day"]) & (pl.col("layer") == "joint"))
        if w.height and w["mid_first"].drop_nulls().len():
            ref_mid = float(w["mid_first"].drop_nulls().median())
        rows.append([r["symbol"], r["day"], r["decision"]["status"],
                     "yes" if r["eligibility"]["e001_eligible"] else "no", len(r["resyncs"]),
                     pct(r["engine_vs_vendor_quotes"]["agreement_rate"], 3),
                     f"{t['missing_vs_reference']}/{t['reference_trades']:,}",
                     pct(r["trade_depth_linkage"]["linkage_rate_two_events"], 3),
                     pct(r["flags"]["bbo_valid_fraction"], 1), f"{cj['covered_hours']:.2f}",
                     f"{cj['usable_windows_ge_min']} / {cj['usable_hours_ge_min']:.1f}h",
                     f"{1e4 * 0.01 / ref_mid:.3g}" if ref_mid else "n/a", f"{r['day_price_range_bps']:.0f}"])
    T["tardis_days"] = md(["symbol", "day", "integrity", "E001-eligible (post hoc)", "resyncs", "engine = vendor BBO", "trades missing / exchange",
                           "trade→depth link", "BBO proven", "joint valid h", "windows ≥10 min / hours",
                           "tick (bp)", "day range (bp)"], rows)

    rows = []
    for r in S["hf_lobstream"]:
        c, b, t = r["sequence_census"], r["capture_blocks"], r["trades"]
        tr_ret = t["trades"] / (t["last_id"] - t["first_id"] + 1)
        rows.append([r["symbol"], r["period"], pct(c["update_ids_present_fraction"]), pct(c["time_retained_fraction"]),
                     c["sequence_breaks"], f"{b['median_block_min']:.2f}", r["flags"].get("snapshot", 0), pct(tr_ret),
                     t["internal_id_gaps"], f"{r['coverage_book']['covered_hours']:.2f}"])
    T["hf_months"] = md(["symbol", "month", "update ids present", "time retained", "sequence breaks", "median block (min)",
                         "REST snapshots", "trade ids present", "trade-id gaps", "anchored valid h"], rows)

    rows = [[x["symbol"], x["day"], x["reference_messages"], f"{x['runs_reproduced_unbroken']}/{x['reference_contiguous_runs']}",
             pct(x["match_rate"], 3), x["realignments_within_runs"],
             f"{x['reference_receive_lag_ms_quantiles']['0.5']:.0f} / {x['reference_receive_lag_ms_quantiles']['0.99']:.0f}"]
            for x in S["cross_capture"]]
    T["cross_capture"] = md(["symbol", "day", "HF messages", "id-contiguous runs reproduced unbroken", "aligned",
                             "re-alignments", "HF receive lag p50 / p99 (ms)"], rows)

    rows = []
    for x in S["rest_snapshot_checks"]:
        u = x["unrestricted"]
        day = next(t for t in S["tardis"] if t["symbol"] == x["symbol"] and t["day"] == x["day"])
        tm = dt.datetime.fromisoformat(x["hf_snapshot_local_time"]) + dt.timedelta(milliseconds=x["best_match_offset_ms"])
        anchor = max(a for a in (dt.datetime.fromisoformat(s["local_time"]) for s in day["snapshots"]) if a <= tm)
        al = x["alignment"]
        rows.append([x["symbol"], x["day"], x["hf_snapshot_local_time"][11:19], f"{x['best_match_offset_ms']:.0f}",
                     f"{al['candidates_at_minimum']}/{x['candidates_searched']}",
                     f"{al['minimum_offsets_ms'][0]:.0f} … {al['minimum_offsets_ms'][1]:.0f}",
                     f"{(tm - anchor).total_seconds() / 3600:.1f}",
                     "yes" if x["best_match_replay_flags_valid"] else "no (one side unproven)",
                     f"{sum(x['match'])}/{sum(x['levels'])}", sum(x["qty_diff"]) + sum(x["only_replay"]) + sum(x["only_snapshot"]),
                     "yes" if x["bbo_equal"] and x["touch_qty_equal"] else "no",
                     f"{sum(u['match'])}/{sum(u['levels'])}", str(u["only_snapshot"])])
    T["rest_checks"] = md(["symbol", "day", "HF snapshot (UTC)", "selected offset (ms)", "candidates at minimum / searched",
                           "offset range at minimum (ms)", "hours since replay anchor", "replay touch proven",
                           "proven-region levels equal", "proven-region mismatches", "touch price & size equal",
                           "all levels equal (unrestricted)", "snapshot-only levels by bp bucket [0,1,5,25,100,∞)"], rows)

    rows = []
    for r in S["tardis"]:
        rs = [x for x in r["resyncs"] if x.get("comparable")]
        if not rs:
            continue
        pv = [x for x in rs if x["pre_resync_flags_valid"]]
        rows.append([r["symbol"], r["day"], len(rs), sum(x["bbo_equal"] for x in rs),
                     f"{sum(x['gap_last_diff_to_snapshot_ms'] for x in rs) / len(rs):.0f}",
                     len(pv), sum(sum(x["only_replay"][:2]) for x in pv), sum(sum(x["only_replay"][2:]) for x in pv),
                     sum(sum(x["only_snapshot"][:2]) for x in pv), sum(sum(x["qty_diff"][:2]) for x in pv)])
    T["resyncs"] = md(["symbol", "day", "resyncs", "BBO equal", "mean capture gap (ms)", "pre-resync proven",
                       "replay-only <5bp", "replay-only ≥5bp", "snapshot-only <5bp", "size diffs <5bp"], rows)

    rows = []
    by = defaultdict(list)
    for r in S["tardis"]:
        by[r["symbol"]].append(r)
    for sym, rs in by.items():
        acc = [r for r in rs if r["decision"]["status"] == "accepted"]
        el = [r for r in acc if r["eligibility"]["e001_eligible"]]
        jh = sum(r["coverage_joint"]["covered_hours"] for r in acc)
        uh = sum(r["coverage_joint"]["usable_hours_ge_min"] for r in acc)
        un = sum(r["coverage_joint"]["usable_windows_ge_min"] for r in acc)
        rows.append([sym, f"{len(acc)}/{len(rs)}", f"{len(el)}/{len(rs)}", f"{jh:.3f}", f"{uh:.3f}", f"{jh - uh:.3f}", un,
                     pct(jh / (24 * len(rs)), 2), f"{min(r['coverage_joint']['covered_hours'] for r in rs):.2f}"])
    T["coverage"] = md(["symbol", "pass integrity", "E001-eligible (post hoc ≥20 h)", "joint valid h",
                        "h in windows ≥600 s", "h in shorter windows", "windows ≥600 s", "joint h / sampled h",
                        "worst session (h)"], rows)

    cw = W.filter((pl.col("source") == "tardis") & (pl.col("symbol") == "SOLUSDT") & (pl.col("layer") == "joint"))
    daily = cw.group_by("day").agg(pl.col("duration_s").sum().alias("s"), pl.col("trades").sum(), pl.col("notional_quote").sum(),
                                   (pl.col("twa_spread_ticks") * pl.col("duration_s")).sum().alias("sp"),
                                   ((pl.col("event_mean_spread_ticks") * pl.col("n_valid_states")).sum() / pl.col("n_valid_states").sum()).alias("esp"),
                                   pl.col("mid_first").drop_nulls().median().alias("mid"),
                                   pl.col("rv_1min_bp").drop_nulls().median().alias("rv")).sort("day")
    T["sol_market_state"] = md(["day", "valid h", "mid (USDT)", "tick (bp)", "trades", "notional (M USDT)",
                                "time-weighted spread (ticks)", "event-mean spread (ticks)", "median window RV (bp/√min)"],
                               [[d["day"], f"{d['s'] / 3600:.2f}", f"{d['mid']:.2f}", f"{1e4 * 0.01 / d['mid']:.2f}", d["trades"],
                                 f"{d['notional_quote'] / 1e6:.1f}", f"{d['sp'] / d['s']:.4f}", f"{d['esp']:.4f}",
                                 f"{d['rv']:.2f}" if d["rv"] is not None else "n/a"]
                                for d in daily.iter_rows(named=True)])
    if SENS.exists():
        V = pl.DataFrame(json.loads(SENS.read_text())["variants"])
        agg_v = (V.group_by(["symbol", "factor", "value", "baseline"]).agg(
            pl.col("joint_hours").sum(), pl.col("hours_in_windows_ge_min").sum(), pl.col("joint_windows").sum(),
            pl.col("bbo_proven_fraction").mean(), pl.col("silent_trades").sum()).sort(["symbol", "factor", "value"]))
        for factor in ("proven_levels", "silence_s"):
            sub = agg_v.filter(pl.col("factor") == factor)
            T[f"sens_{factor}"] = md(["symbol", factor, "baseline", "mean BBO-proven fraction", "joint h", "h in windows ≥600 s",
                                      "joint windows", "silent trades"],
                                     [[x["symbol"], ("full extent" if factor == "proven_levels" and x["value"] == 0 else f"{x['value']:g}"),
                                       "yes" if x["baseline"] else "",
                                       f"{x['bbo_proven_fraction']:.4f}", f"{x['joint_hours']:.3f}",
                                       f"{x['hours_in_windows_ge_min']:.3f}", x["joint_windows"], x["silent_trades"]]
                                      for x in sub.iter_rows(named=True)])
    if RECON.exists():
        R = json.loads(RECON.read_text())
        T["reconciliation"] = md(["quantity", "2026-10-14 run (b0a808014c0514ad)", "this run", "difference", "explanation"],
                                 [[x["quantity"], x["old"], x["new"], x["diff"], x["explanation"]] for x in R["rows"]])
    prov = S.get("provenance", {})
    T["run_meta"] = (f"Test `{S['test_id']}` · run {S['run_at_utc']} · git `{prov.get('git_commit', 'n/a')[:12]}`"
                     f"{' (DIRTY — not citable)' if prov.get('git_dirty') else ''} · code fingerprint `{S['code_fingerprint']}` · "
                     f"config `configs/acceptance_001.toml` · machine-readable coverage `results/acceptance_001/windows.csv`")
    return T


def fill(text: str, T: dict[str, str]) -> str:
    for k, v in T.items():
        pat = re.compile(rf"<!-- BEGIN:{k} -->\n.*?<!-- END:{k} -->", re.S)
        text, n = pat.subn(lambda m: f"<!-- BEGIN:{k} -->\n{v}\n<!-- END:{k} -->", text)
        if n == 0:
            raise KeyError(f"report has no marker for table '{k}'")
    return text


def main() -> None:
    from lpx.provenance import require_clean

    require_clean()
    S = json.loads((OUT / "summary.json").read_text())
    W = pl.read_csv(OUT / "windows.csv")
    REPORT.write_text(fill(REPORT.read_text(), tables(S, W)))
    print(f"filled tables in {REPORT}")


if __name__ == "__main__":
    main()
