"""Fill the tables of results/e001/E001_report.md from the E001 discovery artifacts (numbers are machine-generated;
prose is written against them). Usage: ``uv run python -m lpx.research.e001_report``"""

from __future__ import annotations

import json

import polars as pl

from lpx.data.acquire import ROOT
from lpx.quality.report import fill, md

OUT = ROOT / "results" / "e001"
REPORT = OUT / "E001_report.md"
KEY = ["es", "mo_1s", "mo_5s", "mo_30s", "rs_1s", "rs_5s", "rs_30s"]


def ci(r: dict) -> str:
    return f"{r['mean_of_session_means']:+.3f} [{r['ci95_lo']:+.3f}, {r['ci95_hi']:+.3f}]"


def tables(out=OUT) -> dict[str, str]:
    res = json.loads((out / "e001_discovery.json").read_text())
    cells = pl.read_csv(out / "e001_discovery_cells.csv")
    per = pl.read_csv(out / "e001_discovery_per_session.csv")
    sens = pl.read_csv(out / "e001_discovery_sensitivity.csv")
    T = {}
    pv = res["provenance"]
    T["meta"] = (f"E001 discovery run {res['run_at_utc']} · git `{pv['git_commit'][:12]}`{' (DIRTY — not citable)' if pv['git_dirty'] else ''}"
                 f" · code fingerprint `{pv['code_fingerprint']}` · sessions: {len(res['sessions'])} ({', '.join(res['session_sets'])}) · "
                 f"windows.csv sha256 `{pv['inputs']['windows_csv_sha256'][:16]}` · acceptance run `{pv['inputs']['acceptance_git_commit'][:12]}`")
    prim = {r["metric"]: r for r in res["primary"]}
    T["primary"] = md(["metric (bp)", "mean of session means [95% session-bootstrap CI]", "event-weighted mean", "sessions > 0", "events"],
                      [[m, ci(prim[m]), f"{prim[m]['event_weighted_mean']:+.3f}", f"{prim[m]['sessions_positive']}/{prim[m]['sessions']}",
                        prim[m]["events"]] for m in KEY if m in prim])
    T["exclusions"] = md(["reason", "events"], [[k, v] for k, v in sorted(res["exclusions"]["primary"].items(), key=lambda kv: -kv[1])])
    rows = []
    for r in per.iter_rows(named=True):
        rows.append([r["day"], r["split"], "yes" if r["e001_eligible_posthoc"] else "no", r["events"],
                     *[f"{r[m]:+.3f} [{r[m + '_ci95_lo']:+.3f}, {r[m + '_ci95_hi']:+.3f}]" if r[m] is not None else "n/a"
                       for m in ("es", "mo_1s", "mo_30s", "rs_30s")]])
    T["per_session"] = md(["session", "split", "eligible (post hoc)", "events", "es", "mo 1 s", "mo 30 s", "rs 30 s"], rows)
    rows = []
    for cell in [c for c in cells["cell"].unique(maintain_order=True).to_list() if c != "all"]:
        sub = {r["metric"]: r for r in cells.filter(pl.col("cell") == cell).iter_rows(named=True)}
        rows.append([cell, sub["es"]["events"], ci(sub["es"]), ci(sub["mo_1s"]), ci(sub["mo_30s"]), ci(sub["rs_30s"])])
    T["cells"] = md(["cell", "events", "es", "mo 1 s", "mo 30 s", "rs 30 s"], rows)
    rows = [["pre-specified primary", "primary (cluster · exchange clock · baseline windows · all sessions)", prim["es"]["events"],
             *[ci(prim[m]) for m in ("es", "mo_1s", "mo_5s", "mo_30s", "rs_30s")]]]
    for spec in sens["spec"].unique(maintain_order=True).to_list():
        sub = {r["metric"]: r for r in sens.filter(pl.col("spec") == spec).iter_rows(named=True)}
        rows.append([sub["es"]["analysis"], spec, f"{sub['es']['events']:,} / {sub['mo_30s']['events']:,}" if spec == "available_case_per_horizon"
                     else sub["es"]["events"], *[ci(sub[m]) for m in ("es", "mo_1s", "mo_5s", "mo_30s", "rs_30s")]])
    T["sensitivity"] = md(["analysis", "specification", "events", "es", "mo 1 s", "mo 5 s", "mo 30 s", "rs 30 s"], rows)
    d = res["descriptive"]
    T["descriptive"] = (md(["metric (all events with a valid pre-state)", "events", "mean of session means (bp)"],
                           [[x["metric"], x["events"], f"{x['mean_of_session_means']:+.3f}"] for x in d["secondary_horizons"]])
                        + "\n\n" + md(["information clock", "pre-event state age p50 (ms)", "p90", "p99"],
                                       [[k, f"{v['0.5']:.0f}", f"{v['0.9']:.0f}", f"{v['0.99']:.0f}"]
                                        for k, v in d["pre_state_age_ms_quantiles"].items()]))
    T["proxy"] = md(["qty_ge_touch (proxy)", "events with a valid next state", "share whose touch price moved by the next state"],
                    [[str(r["qty_ge_touch"]), r["events"], f"{100 * r['share_touch_moved_next_state']:.1f}%"]
                     for r in res["proxy_validation_qty_ge_touch"]])
    if (out / "e001_exploratory.json").exists():
        T.update(exploratory_tables(out))
    return T


def exploratory_tables(out=OUT) -> dict[str, str]:
    """Tables of the exploratory addenda (configs/e001_exploratory_v1.toml); every row is exploratory."""
    T = {}
    xr = json.loads((out / "e001_exploratory.json").read_text())
    pv = xr["provenance"]
    T["x_meta"] = (f"Exploratory addenda run {xr['run_at_utc']} · git `{pv['git_commit'][:12]}`"
                   f"{' (DIRTY — not citable)' if pv['git_dirty'] else ''} · declared in `{xr['declared_in']}` · "
                   f"{xr['events_primary_set']:,} primary events · touch transition in {100 * xr['touch_transition_share']:.1f}%")
    P = pl.read_csv(out / "e001_exploratory_paired.csv")
    order = ["mo_0.1s", "d_0.1_1", "d_1_5", "d_5_30", "mo_30s", "c_batch", "drift_30", "half_rs_0.1s", "half_rs_1s", "half_rs_30s"]
    names = {"mo_0.1s": "mo(0.1 s)", "d_0.1_1": "mo(1) − mo(0.1)", "d_1_5": "mo(5) − mo(1)", "d_5_30": "mo(30) − mo(5)",
             "mo_30s": "mo(30 s)", "c_batch": "c: move within the trade's 100 ms batch", "drift_30": "drift: mo(30) − c",
             "half_rs_0.1s": "passive mark-to-mid rs/2 at 0.1 s", "half_rs_1s": "rs/2 at 1 s", "half_rs_30s": "rs/2 at 30 s"}
    subsets = P["subset"].unique(maintain_order=True).to_list()
    rows = []
    for m in order:
        row = [names[m]]
        for sub in subsets:
            x = P.filter((pl.col("subset") == sub) & (pl.col("metric") == m)).row(0, named=True)
            row.append(f"{x['mean_of_session_means']:+.3f} [{x['ci95_lo']:+.3f}, {x['ci95_hi']:+.3f}]")
        rows.append(row)
    ev = {sub: P.filter(pl.col("subset") == sub)["events"][0] for sub in subsets}
    T["x_paired"] = md(["paired quantity (bp of m0; same events)"] + [f"{sub} ({ev[sub]:,})" for sub in subsets], rows)
    Wt = pl.read_csv(out / "e001_exploratory_weighting.csv")
    rows = []
    for m in ["es", "mo_1s", "mo_30s", "rs_30s", "half_rs_30s"]:
        row = [m if m != "half_rs_30s" else "rs/2 at 30 s (passive mark-to-mid; per cluster / per unit of quantity / per unit of notional)"]
        for wt in ["event", "quantity", "notional"]:
            x = Wt.filter((pl.col("weight") == wt) & (pl.col("metric") == m)).row(0, named=True)
            row.append(f"{x['mean_of_session_means']:+.3f} [{x['ci95_lo']:+.3f}, {x['ci95_hi']:+.3f}]")
        rows.append(row)
    T["x_weighting"] = md(["metric (bp)", "cluster-weighted (= primary)", "quantity-weighted", "notional-weighted"], rows)
    D = pl.read_csv(out / "e001_exploratory_decision_time.csv")
    T["x_decision"] = md(["side hit (passive side)", "its queue vs the opposite touch, at the pre-event state", "clusters", "share of the side's clusters",
                          "mo 30 s", "rs/2 at 1 s", "rs/2 at 30 s [95% CI]"],
                         [[x["passive_side"], x["passive_queue"], x["events"], f"{100 * x['share_of_side_events']:.1f}%",
                           f"{x['mo_30s']:+.3f}", f"{x['half_rs_1s']:+.3f}",
                           f"{x['half_rs_30s']:+.3f} [{x['half_rs_30s_ci95_lo']:+.3f}, {x['half_rs_30s_ci95_hi']:+.3f}]"]
                          for x in D.iter_rows(named=True)])
    return T


def main() -> None:
    from lpx.provenance import require_clean

    require_clean()
    REPORT.write_text(fill(REPORT.read_text(), tables()))
    print(f"filled tables in {REPORT}")


if __name__ == "__main__":
    main()
