"""Close-out dry run (docs/experiments/FINAL_EVALUATION.md, section 7). Discovery sessions only; refuses every test day.

    fits             check 1: the fit tool with `before` = s6..s15 equals e003_models.json and e004_lambda.csv
    e001 .. e004     run one experiment through the entry point's code path with walk-forward artifacts
    compare          check 2: the outputs reproduce every frozen discovery table; the analysis wiring equals the frozen JSONs
    inventory        every key of the frozen JSONs: compared by check 2, or excluded with its reason
    rehearsal        check 3: the whole test path on stand-ins s11..s15 in a scratch repository; outputs discarded unread
    faults           real-path fault injection on a stand-in session, in scratch repositories (separate from check 3)
    precheck         the pre-check on real stand-ins: injected failures, genuine input problems and refusals

Status: reruns of frozen discovery computations and synthetic failures; no test session is touched.
Usage: PYTHONPATH=. uv run python tools/closeout_dryrun.py <command>
"""

import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import numpy as np
import polars as pl

from lpx.data.acquire import ROOT
from lpx.research import closeout as C
from lpx.research import closeout_analysis as A

OUT = ROOT / "results" / "closeout_dryrun"
DEV = ROOT / "results" / "closeout_dev"
FITS = ROOT / "results" / "closeout_fits"


def days() -> tuple[dict, list[str]]:
    rc = C.load_rc()
    d = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    if set(d) & set(rc["splits"]["test"]):
        raise PermissionError("the dry run refuses test days")
    return rc, d


def dry_ctx(exp: str) -> C.Ctx:
    rc, d = days()
    sessions = {"E001": d, "E002": d, "E003": d[5:], "E004": d[5:]}
    out = OUT / exp.lower()
    out.mkdir(parents=True, exist_ok=True)
    return C.Ctx("dryrun", out, rc, sessions, lambda x: FITS / "walkforward" / x, lambda x: [y for y in d if y < x], ROOT / "results" / "e003")


def code_state() -> dict:
    ws = C.Workspace(ROOT)
    return {"git_commit": ws.git("rev-parse", "HEAD").strip(), "code_fingerprint": C.fingerprint(ROOT), "trees": C.trees(ws)}


def require_clean() -> None:
    """Evidence is produced from committed code only, with no override."""
    if os.environ.get("LPX_ALLOW_DIRTY"):
        raise SystemExit("refused: LPX_ALLOW_DIRTY must be unset")
    if C.Workspace(ROOT).git("status", "--porcelain", "--", *C.DIFF_SCOPE).strip():
        raise SystemExit("refused: uncommitted changes in the close-out's scope")


def run_one(exp: str) -> None:
    t0 = time.time()
    state = code_state()
    ctx = dry_ctx(exp)
    C.RUNNERS[exp](ctx)
    (ctx.out / "runtime.json").write_text(json.dumps({"seconds": round(time.time() - t0, 1), **state}))
    print(f"{exp} done in {time.time() - t0:.0f} s", flush=True)


def check_fits() -> dict:
    _, d = days()
    fm = json.loads((ROOT / "results" / "e003" / "e003_models.json").read_text())
    lam = pl.read_csv(ROOT / "results" / "e004" / "e004_lambda.csv", infer_schema_length=None)
    res = {}
    for x in d[5:]:
        art = json.loads((FITS / "walkforward" / x / "e003_fit.json").read_text())
        e3_same = {k: v for k, v in art.items() if k not in ("sessions", "before")} == fm[x]
        fits, _ = C.load_e004_fit(FITS / "walkforward" / x)
        rows = []
        for cell, fit in fits.items():
            for (tgt, ind), lv in fit.lam.items():
                g = fit.groups.get((tgt, ind))
                for gi, v in enumerate(lv):
                    rows.append((cell, tgt, ind, gi, "all" if g is None else ",".join(str(b) for b in np.flatnonzero(g == gi)), float(v), fit.train_rows[tgt]))
        fz = lam.filter(pl.col("day") == x).select("cell", "target", "indicator", "group", pl.col("buckets").cast(pl.String), "lambda", "train_rows").rows()
        res[x] = {"e003_models_equal": e3_same, "e004_lambda_rows": len(rows), "e004_lambda_equal": sorted(rows) == sorted(fz)}
    out = {"check": "fit tool vs frozen walk-forward fits", "sessions": res, "passed": all(r["e003_models_equal"] and r["e004_lambda_equal"] for r in res.values()),
           "provenance": code_state()}
    DEV.mkdir(parents=True, exist_ok=True)
    (DEV / "dryrun_check1_fits.json").write_text(json.dumps(out, indent=1))
    print("check 1 passed:", out["passed"])
    return out


def compare_csv(new: Path, frozen: Path, sha: str | None) -> dict:
    """Byte hash first; otherwise cell by cell (exact) over the frozen columns."""
    h = C.sha256_file(new)
    r = {"sha256": h, "byte_identical": h == (sha or C.sha256_file(frozen))}
    if not r["byte_identical"]:
        a, b = pl.read_csv(new, infer_schema_length=None), pl.read_csv(frozen, infer_schema_length=None)
        r["same_shape"] = a.shape == b.shape
        r["same_columns"] = a.columns == b.columns
        bad = [c for c in b.columns if c not in a.columns or not a[c].equals(b[c], null_equal=True)]
        r["differing_columns"] = bad[:20]
    return r


def compare() -> dict:
    res = {"check": "code path reproduces frozen discovery tables"}
    m2 = json.loads((ROOT / "results/e002/e002_meta.json").read_text())["outputs_sha256"]
    res["E002"] = {f: compare_csv(OUT / "e002" / f, ROOT / "results/e002" / f, m2[f]) for f in m2}
    m3 = json.loads((ROOT / "results/e003/e003_meta.json").read_text())["outputs_sha256"]
    res["E003"] = {f: compare_csv(OUT / "e003" / f, ROOT / "results/e003" / f, m3[f]) for f in m3 if f.endswith(".csv")}
    res["E003"]["e003_models.json"] = {"equal": json.loads((OUT / "e003/e003_models.json").read_text()) == json.loads((ROOT / "results/e003/e003_models.json").read_text())}
    m4 = json.loads((ROOT / "results/e004/e004_meta.json").read_text())["outputs_sha256"]
    res["E004"] = {f: compare_csv(OUT / "e004" / f, ROOT / "results/e004" / f, m4[f]) for f in m4}
    # E001: field by field, kept columns
    e1 = {}
    keep = ["analysis", "spec", "cell", "metric", "sessions", "events", "mean_of_session_means", "event_weighted_mean", "sessions_positive"]
    for new, old in (("e001_cells.csv", "e001_discovery_cells.csv"), ("e001_sensitivity.csv", "e001_discovery_sensitivity.csv")):
        a, b = pl.read_csv(OUT / "e001" / new, infer_schema_length=None), pl.read_csv(ROOT / "results/e001" / old, infer_schema_length=None)
        e1[new] = {"rows_equal": a.height == b.height, "columns_equal": all(a[c].equals(b[c], null_equal=True) for c in keep if c in b.columns),
                   "no_column_outside_the_allow_list": set(a.columns) <= set(A.ALLOW["e001_keys"])}
    a, b = pl.read_csv(OUT / "e001/e001_per_session.csv", infer_schema_length=None), pl.read_csv(ROOT / "results/e001/e001_discovery_per_session.csv", infer_schema_length=None)
    e1["e001_per_session.csv"] = {"columns_equal": all(a[c].equals(b[c], null_equal=True) for c in a.columns)}
    fj, nj = json.loads((ROOT / "results/e001/e001_discovery.json").read_text()), json.loads((OUT / "e001/e001_closeout.json").read_text())
    e1["json"] = {k: fj[k] == nj[k] or (k == "size_tercile_edges_base_qty" and list(fj[k]) == list(nj[k]))
                  for k in ("size_tercile_edges_base_qty", "exclusions", "descriptive", "proxy_validation_qty_ge_touch", "sensitivity_specs", "events_total", "events_primary")}
    res["E001"] = e1
    res["analysis_wiring"] = analysis_wiring()
    inv = json.loads((OUT / "e004/e004_invariants.json").read_text())
    res["E004_invariants"] = {"closeout": inv, "frozen": json.loads((ROOT / "results/e004/e004_meta.json").read_text())["invariants"]}
    bad = []
    for ex in ("E002", "E003", "E004"):
        bad += [f"{ex}/{f}" for f, r in res[ex].items() if not (r.get("byte_identical") or r.get("equal"))]
    res["passed_exact"] = {"tables_not_byte_identical": bad, "e001_all_equal": all(all(v.values()) for v in e1.values()),
                           "analysis_all_equal": res["analysis_wiring"]["mismatches"] == [],
                           "invariants_equal": res["E004_invariants"]["closeout"] == res["E004_invariants"]["frozen"]}
    state = code_state()
    runs = {ex: json.loads((OUT / ex / "runtime.json").read_text()) for ex in ("e001", "e002", "e003", "e004")}
    res["passed_exact"]["same_code_as_every_run"] = all(r["trees"] == state["trees"] and r["code_fingerprint"] == state["code_fingerprint"] for r in runs.values())
    res["runs"] = {ex: {"seconds": r["seconds"], "git_commit": r["git_commit"]} for ex, r in runs.items()}
    res["passed"] = not bad and all(res["passed_exact"][k] for k in ("e001_all_equal", "analysis_all_equal", "invariants_equal", "same_code_as_every_run"))
    res["provenance"] = state
    res["key_inventory"] = "comparison_key_inventory.json"
    DEV.mkdir(parents=True, exist_ok=True)
    (DEV / "dryrun_check2_reproduction.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps({**res["passed_exact"], "passed": res["passed"], "mismatches": res["analysis_wiring"]["mismatches"][:10]}, indent=1, default=str))
    if not res["passed"]:
        raise SystemExit("the dry run does not reproduce the frozen tables")
    return res


def walk(name: str, new, old, mism: list, seen: list | None = None) -> int:
    """Recursive exact comparison of the kept output against the frozen value. A key on either side only, or a length difference, is a
    mismatch. ``seen`` collects the type of each leaf compared."""
    n = 0
    if isinstance(new, dict) or isinstance(old, dict):
        if not (isinstance(new, dict) and isinstance(old, dict)):
            mism.append({"name": name, "problem": "a dict on one side only"})
            return n
        for k in sorted(set(new) | set(old), key=str):
            if k not in old:
                mism.append({"name": f"{name}.{k}", "problem": "absent from the frozen output"})
            elif k not in new:
                mism.append({"name": f"{name}.{k}", "problem": "absent from the close-out output"})
            else:
                n += walk(f"{name}.{k}", new[k], old[k], mism, seen)
    elif isinstance(new, list) and new and isinstance(new[0], dict):
        if not isinstance(old, list) or len(old) != len(new):
            mism.append({"name": name, "problem": "row count differs"})
            return n
        for i, (x, y) in enumerate(zip(new, old)):
            n += walk(f"{name}[{i}]", x, y, mism, seen)
    else:
        n = 1
        if seen is not None:
            seen.append("null" if new is None else "boolean" if isinstance(new, bool) else "number" if isinstance(new, (int, float)) else "string" if isinstance(new, str) else "list")
        if new != old:
            mism.append({"name": name, "closeout": new, "frozen": old})
    return n


def get(obj, path: str):
    for k in path.strip("/").split("/"):
        obj = obj[k]
    return obj


FROZEN = {"e001": "e001/e001_discovery.json", "e002": "e002/e002_h2.json", "e003": "e003/e003_analysis.json", "e004": "e004/e004_analysis.json"}
# Whole blocks, walked leaf by leaf through the allow-list: (frozen file, frozen path, path in the close-out analysis)
WALKS = [("e002", "/scenario_table", "E002/reported_only/scenario_table"), ("e002", "/paired_table", "E002/reported_only/paired_table"),
         ("e002", "/materiality", "E002/reported_only/model_pairs_table"), ("e002", "/descriptive_range_of_means", "E002/reported_only/descriptive_range_of_means"),
         ("e003", "/H1/reported", "E003/reported_only/H1_reported"), ("e003", "/H3/normalised", "E003/reported_only/H3/normalised"),
         ("e003", "/H3/other_schedules", "E003/reported_only/H3/other_schedules"), ("e003", "/P0_versus_E002", "E003/reported_only/P0_versus_E002"),
         ("e003", "/descriptive/scenarios", "E003/reported_only/descriptive/scenarios"), ("e003", "/descriptive/forecasts", "E003/reported_only/descriptive/forecasts"),
         *[("e004", f"/descriptive/{k}", f"E004/reported_only/descriptive/{k}") for k in ("policy_D1_E", "policy_D1_S", "p3_ua_vs_pl_forecasts_D1_S", "window_quality")]]
H4F_KEYS = [f"{c}:{t}" for c in ("D1_S", "D1_E", "D3", "D4", "D2", "D1_S1", "D1_S3") for t in ("y_k", "y_view")]
H4W_SHARES = ("wu_time_share_nostall", "wu_fill_share_nostall", "wp_time_share_install", "wp_fill_share_install")


def h4f_test_path(k: str) -> str:
    return f"E004/h4f_y_view/cells/{k.split(':')[0]}" if k.endswith("y_view") and k.split(":")[0] in ("D1_S", "D3") else f"E004/reported_only/h4f_other/{k}"


def named() -> list[tuple[str, str, str]]:
    """Single values compared one to one: (frozen file, frozen path, path in the close-out analysis)."""
    out = [("e003", "/H1/H1-F/mean", "E003/checks[H1-F]/components/r2_os/mean"), ("e003", "/H1/H1-T/mean", "E003/checks[H1-T]/components/D_bp/mean"),
           ("e003", "/H3/es_diff/mean", "E003/checks[H3]/components/es_diff/mean"), ("e003", "/H3/drawdown_diff/mean", "E003/checks[H3]/components/drawdown_diff/mean"),
           ("e003", "/H3/net_per_hour_diff/mean", "E003/checks[H3]/components/net_per_hour_diff/mean"), ("e003", "/H3/turnover_ratio_P4_over_P3F", "E003/checks[H3]/turnover_ratio_P4_over_P3F"),
           ("e003", "/H3/partly_mechanical", "E003/checks[H3]/partly_mechanical"), ("e003", "/H1/H1-T/gate_activity", "E003/checks[H1-T]/gate_activity"), ("e004", "/secondary/H4-0/difference_pp/mean", "E004/reported_only/H4_0/difference_pp/mean"),
           ("e004", "/secondary/H4-0/t_interval_95", "E004/reported_only/H4_0/difference_pp/t_interval_95_descriptive_not_used")]
    out += [("e003", f"/participation/policies/{p}/{f}", f"E003/policies_vip0_descriptive/policies/{p}/{g}") for p in ("P0", "P1", "P3_M1", "P3_M2", "P3_negM2", "P3F", "P4")
            for f, g in (("mean", "mean_net_per_hour"), ("turnover_per_hour", "turnover_per_hour"))]
    for c, frozen in (("r2_os", "/H1/H1-F"), ("D_bp", "/H1/H1-T")):
        cid = "H1-F" if c == "r2_os" else "H1-T"
        out += [("e003", f"{frozen}/{k}", f"E003/checks[{cid}]/components/{c}/{k}") for k in ("defined", "positive")]
    out += [("e003", f"/H3/{c}/{k}", f"E003/checks[H3]/components/{c}/{k}") for c in ("es_diff", "drawdown_diff", "net_per_hour_diff") for k in ("defined", "positive")]
    out += [("e004", "/secondary/H4-0/difference_pp/defined", "E004/reported_only/H4_0/difference_pp/defined")]
    out += [("e004", f"/secondary/H4-F/{c}:{t}/rho_A_minus_projection", f"{h4f_test_path(f'{c}:{t}')}/rho_A_minus_projection") for c in ("D1_S", "D3") for t in ("y_k", "y_view")]
    for b in ("P0", "P3_M2"):
        i, c = f"/primary/H4-W[{b}]", f"E004/checks[H4-W[{b}]]"
        out += [("e004", f"{i}/D_W_bp/{k}", f"{c}/components/D_W_bp/{k}") for k in ("defined", "positive")]
        out += [("e004", f"{i}/stall_only/D_W_bp/{k}", f"{c}/components/D_W_stall_bp/{k}") for k in ("defined", "positive")]
        out += [("e004", f"{i}/D_W_bp/mean", f"{c}/components/D_W_bp/mean"), ("e004", f"{i}/stall_only/D_W_bp/mean", f"{c}/components/D_W_stall_bp/mean"),
                ("e004", f"{i}/t_interval_95", f"{c}/components/D_W_bp/t_interval_95_descriptive_not_used"), ("e004", f"{i}/below_delta", f"{c}/sign_count_below_delta"),
                ("e004", f"{i}/gates/withdrawn_share_mean", f"{c}/gates/withdrawn_share_mean"), ("e004", f"{i}/gates/overlap_share_mean", f"{c}/gates/overlap_share_mean"),
                ("e004", f"{i}/gates/defined_sessions", f"{c}/gates/sessions_defined"), *[("e004", f"{i}/shares/{k}", f"{c}/withdrawn_and_shares/{k}") for k in H4W_SHARES]]
    for k in H4F_KEYS:
        for m in ("L", "A", "B", "C"):
            out += [("e004", f"/secondary/H4-F/{k}/{m}/{f}", f"{h4f_test_path(k)}/{m}/{g}") for f, g in (("mean", "mean"), ("defined", "defined"), ("positive", "positive"), ("t_interval_95", "t_interval_95_descriptive_not_used"))]
        out += [("e004", f"/secondary/H4-F/{k}/rho_A/value", f"{h4f_test_path(k)}/rho_A"), ("e004", f"/secondary/H4-F/{k}/rho_B/value", f"{h4f_test_path(k)}/rho_B")]
    return out


def at(a: dict, path: str):
    """A path into the close-out analysis, where checks[ID] selects a check row."""
    return A._at(a["experiments"], path) if not path.startswith("/") else get(a, path)


def analysis_wiring() -> dict:
    """On the dry-run tables, every walked block and every named value equals the frozen analysis JSONs, exactly.
    Discovery-rule labels and intervals are excluded by design; the labels here are five-session rules applied to more sessions."""
    rc, d = days()
    t = OUT / "all"
    if t.exists():
        shutil.rmtree(t)
    t.mkdir(parents=True)
    for ex in ("e001", "e002", "e003", "e004"):
        for p in (OUT / ex).iterdir():
            if p.name != "runtime.json":
                shutil.copy(p, t / p.name)
    statuses = {e: {"status": "complete", "outputs": {f: C.sha256_file(t / f) for f in A.EXPERIMENT_TABLES[e]}} for e in C.EXPERIMENTS}
    for f in A.INFRASTRUCTURE:
        (t / f).write_text("{}")
    sessions = {"E001": d, "E002": d, "E003": d[5:], "E004": d[5:]}
    tables = {p.name: C.sha256_file(p) for p in t.iterdir() if p.is_file()}
    (t / "closeout_meta.json").write_text(json.dumps({"statuses": statuses, "tables_sha256": tables}))
    a = A.analyse(t, SimpleNamespace(mode="dryrun", sessions=sessions))
    (t / "closeout_analysis.json").write_text(json.dumps(a, indent=0))
    mism: list = []
    seen: list = []
    fj = {k: A.jsonable(json.loads((ROOT / "results" / f).read_text())) for k, f in FROZEN.items()}
    compared = {"walked": 0, "named": 0, "e002_series": 0}
    for f, fp, tp in WALKS:
        compared["walked"] += walk(f"{f}{fp}", at(a, tp), A.keep(get(fj[f], fp)), mism, seen)
    for f, fp, tp in named():
        compared["named"] += walk(f"{f}{fp}", at(a, tp), get(fj[f], fp), mism, seen)
    d1 = {r["metric"]: r["mean_of_session_means"] for r in fj["e001"]["primary"]}
    e1 = a["experiments"]["E001"]
    for c in [*e1["checks"], e1["es"]]:
        m = c["id"].split()[1]
        compared["named"] += walk(f"e001/primary[{m}]/mean_of_session_means", c["components"][m]["mean"], d1[m], mism, seen)
    # the session series behind the E002 t-intervals: their means equal the frozen tables', on the frozen pairing (the same frozen means again)
    net2 = pl.read_csv(t / "e002_net_by_session.csv", infer_schema_length=None).sort(["policy", "fill_model", "latency", "fee_schedule", "day"])
    cfg2 = __import__("tomllib").loads((ROOT / "configs/e002_v1.toml").read_text())
    fee2, models2 = cfg2["fees"]["default"], cfg2["fill_models"]["primary"]
    mean = lambda x: float(x[~np.isnan(x)].mean())
    want = {(r["fill_model"], r["latency"]): r["mean_p1_minus_p0"] for r in fj["e002"]["paired_table"]}
    for k, x in A.e002_paired(net2, fee2, models2).items():
        compared["e002_series"] += walk(f"e002 paired series {k}", mean(x), want[k], mism)
    want = {(r["policy"], r["latency"], r["pair"]): r["mean"] for r in fj["e002"]["materiality"]}
    for k, x in A.e002_model_pairs(net2, fee2, models2).items():
        compared["e002_series"] += walk(f"e002 fill-model series {k}", mean(x), want[k], mism)
    for ex, block in (("E002", a["experiments"]["E002"]["reported_only"]), ("E003.H1", a["experiments"]["E003"]["reported_only"]["H1_reported"]),
                      ("E003.H3", a["experiments"]["E003"]["reported_only"]["H3"]), ("E003.desc", a["experiments"]["E003"]["reported_only"]["descriptive"]),
                      ("E004.desc", a["experiments"]["E004"]["reported_only"]["descriptive"])):
        A.assert_allowed({k: v for k, v in block.items() if not k.endswith("_descriptive_not_used")}, ex)
    types = {k: seen.count(k) for k in sorted(set(seen))}
    return {"values_compared": compared, "distinct_frozen_values_compared": compared["walked"] + compared["named"], "by_type": types,
            "note": "exact equality; the E002 series re-test frozen means already walked; discovery-rule labels and intervals excluded by design", "mismatches": mism}


# Every leaf key of the frozen JSONs: compared (walked, named, or by the E001 field and table checks), or excluded for a stated reason.
REASONS = {
    "discovery split, not computed on test (Appendix A)": ["/descriptive/scenarios_by_period/*", "/descriptive/forecasts_by_period/*"],
    "discovery-rule interval, not reported on five sessions (protocol section 4)": ["*/ci95", "*/ci95_lo", "*/ci95_hi", "*/ci97.5", "*/ci98.33", "*/ci99.29"],
    "discovery-rule label, flag or decision, not computed on test (sections 3, 4, 7)": ["*/label", "*/label_bonferroni", "*/bonferroni_label", "*/notes", "*/eligible", "*/robust_to_multiplicity",
                                                                                       "*/material", "/material_sensitivity", "/h2_supported_on_discovery", "/condition_*", "*/preferred_to_no_trade",
                                                                                       "/participation/abstention_rational", "/H1/skill_holds", "/multiplicity_note"],
    "rule parameter or projection: a pinned constant, not a computed outcome": ["*/margin_bp", "/min_defined_sessions", "/fee_schedule", "/H3/fee_schedule", "/H3/noninferiority_margin", "/participation/bonferroni_level",
                                                                                "/levels", "*/projection/*", "*/projection", "/secondary/H4-F/*/role", "/participation/fee_schedule", "/primary_spec/*", "/status/*", "/status"],
    "per-session value: the session tables are compared byte for byte": ["*/sessions/*", "*/per_session/*"],
    "status label of the discovery output; the test side writes its own": ["*/status"],
    "run provenance or identity of the discovery run": ["/provenance/*", "/evaluation_sessions", "/primary_scenario", "/experiment", "/symbol", "/session_sets", "/run_at_utc", "/sessions", "*/sessions",
                                                        "/secondary/H4-F/*/rho_*/sessions"],
    "a discovery statistic the test side does not report (P3F's LP tier 4 net per hour on its own; only H3's differences are reported)": ["/H3/P3F_net_per_hour/*"],
    "the seven-policy table reports means, turnover and fee terms, not counts or quote presence (section 3.4)": ["/participation/policies/*/defined", "/participation/policies/*/positive",
                                                                                                                  "/participation/policies/*/quote_presence_both"],
    "projections apply to D1-S and D3 only (section 3.5); the other cells have none on either side": [f"/secondary/H4-F/{c}:*/rho_A_minus_projection" for c in ("D1_E", "D4", "D2", "D1_S1", "D1_S3")],
    "discovery statistic with no test form": ["/primary/*/gates/withdrawn_share_min", "/primary/*/gates/overlap_share_max", "/primary/*/q_U_bp_mean", "/primary/*/q_P_bp_mean", "/primary/*/orders_U_min",
                                              "/primary/*/orders_P_min", "/primary/*/placebo_redraws", "/primary/*/episodes_excluded", "/secondary/H4-0/difference_pp/positive"],
    "compared by the E001 field and table checks of check 2": ["/size_tercile_edges_base_qty", "/exclusions/*", "/events_total", "/events_primary", "/proxy_validation_qty_ge_touch/*", "/sensitivity_specs/*",
                                                               "/descriptive/*", "/primary/*"],
}


def leaf_paths(o, prefix=""):
    """(path without list indices, key) for every scalar leaf; a list of scalars counts as one leaf."""
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, dict) or (isinstance(v, list) and v and isinstance(v[0], dict)):
                yield from leaf_paths(v, f"{prefix}/{k}")
            else:
                yield f"{prefix}/{k}"
    elif isinstance(o, list):
        for v in o:
            yield from leaf_paths(v, prefix)


def inventory() -> dict:
    """Every leaf of the four frozen JSONs is classified from the same lists the comparison uses: walked (an allow-listed key in a walked
    block), named, E001 checks, or excluded with a reason. A leaf with none of these fails."""
    from fnmatch import fnmatchcase

    allow = set(A.ALLOW["leaf_keys"])
    named_paths = {(f, fp) for f, fp, _ in named()}
    out = {"allow_list_leaf_keys": sorted(allow), "walked_blocks": [f"{f}{fp}" for f, fp, _ in WALKS], "named": sorted(f"{f}{fp}" for f, fp in named_paths), "reasons": REASONS, "files": {}, "unexplained": []}
    for f, rel in FROZEN.items():
        rows: dict = {}
        for path in leaf_paths(json.loads((ROOT / "results" / rel).read_text())):
            key = path.rsplit("/", 1)[1]
            walked = any(path.startswith(fp + "/") for g, fp, _ in WALKS if g == f) and key in allow
            if walked:
                how = "compared: walked"
            elif any(g == f and (path == fp or path.startswith(fp + "/")) for g, fp in named_paths) or (f == "e001" and path == "/primary/mean_of_session_means"):
                how = "compared: named"
            else:
                how = next((r for r, pats in REASONS.items() if any(fnmatchcase(path, p) for p in pats)), None)
                if f != "e001" and how == "compared by the E001 field and table checks of check 2":
                    how = None
                if any(path.startswith(fp + "/") for g, fp, _ in WALKS if g == f) and how is None:
                    how = "excluded by the allow-list inside a walked block: " + ("interval" if key.startswith(("ci", "t_interval")) else "label, flag or key not listed")
            if how is None:
                out["unexplained"].append(f"{f}{path}")
            r = rows.setdefault(path, {"count": 0, "how": how})
            r["count"] += 1
        out["files"][rel] = rows
    out["summary"] = {rel: {h: sum(r["count"] for r in rows.values() if r["how"] == h) for h in sorted({str(r["how"]) for r in rows.values()})} for rel, rows in out["files"].items()}
    out["passed"] = not out["unexplained"]
    out["provenance"] = code_state()
    DEV.mkdir(parents=True, exist_ok=True)
    (DEV / "comparison_key_inventory.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({"passed": out["passed"], "unexplained": out["unexplained"][:30], "n_unexplained": len(out["unexplained"])}))
    if not out["passed"]:
        raise SystemExit("a frozen key has no stated reason")
    return out


def precheck_scenarios() -> dict:
    """The real tool on a real stand-in: each scenario against its expected outcome. Failures are injected; no test day is touched."""
    sys.path.insert(0, str(ROOT))
    import tools.closeout_precheck as P

    rc, d = days()
    day = d[10]
    sym = rc["dataset"]["symbol"]
    real_hash = C.sha256_file
    out = {}

    def abort(exc):
        def fail(p):
            if "/data/" in str(p):
                raise exc("injected")
            return real_hash(p)
        return fail

    with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
        tmp = Path(tmp)
        def main_with(o, *patches):
            """Run the tool's main; returns (exit code, stderr)."""
            err = io.StringIO()
            with contextlib.ExitStack() as st:
                for pt in patches:
                    st.enter_context(pt)
                st.enter_context(mock.patch.object(sys, "argv", ["p", str(o), "--stand-ins"]))
                st.enter_context(contextlib.redirect_stderr(err))
                code = P.main()
            return code, err.getvalue()

        for i, exc in enumerate((OSError, MemoryError, ValueError, RuntimeError)):
            o = tmp / f"abort{i}.json"
            code, err = main_with(o, mock.patch.object(C, "sha256_file", abort(exc)))
            out[f"injected {exc.__name__} while hashing"] = {"expected": f"abort, exit 3, no record, {exc.__name__} named", "exit": code, "stderr": err.strip(), "record_written": o.exists(),
                                                             "passed": code == 3 and not o.exists() and f"aborted, no record written: {exc.__name__}" in err and "injected" not in err}
        real_paths = C.input_paths
        gone = tmp / "absent_dir" / "x.parquet"
        o = tmp / "root.json"
        code, err = main_with(o, mock.patch.object(C, "input_paths", lambda s, x: {**real_paths(s, x), "book": gone} if x == day else real_paths(s, x)))
        out["data directory absent"] = {"expected": "abort, exit 3, no record, NotADirectoryError", "exit": code, "stderr": err.strip(), "record_written": o.exists(),
                                        "passed": code == 3 and not o.exists() and "NotADirectoryError" in err}
        one = lambda w=None, rec=None, ep=600.0: P.session_record(sym, day, P.accepted_windows(sym, [day]) if w is None else w, C.acceptance_record(rc, [day])[day] if rec is None else rec, ep)
        rec = C.acceptance_record(rc, [day])[day]
        book = str(real_paths(sym, day)["book"].relative_to(ROOT))
        win = P.accepted_windows(sym, [day])
        cases = {"genuine: book hash differs": (lambda: one(rec={**rec, book: "0"}), "hash_mismatch:book"),
                 "genuine: no acceptance record for the session": (lambda: P.session_record(sym, day, win, None, 600.0), "acceptance_record_missing"),
                 "genuine: acceptance has no book hash": (lambda: one(rec={k: v for k, v in rec.items() if k != book}), "acceptance_hash_missing:book"),
                 "genuine: integrity status not accepted": (lambda: one(w=win.with_columns(pl.lit("rejected").alias("integrity_status"))), "integrity_not_accepted")}
        for name, (fn, want) in cases.items():
            r = fn()
            out[name] = {"expected": want, "reason": r["reason"], "undefined": r["undefined"], "passed": r["reason"] == want and r["undefined"] and not r["e001_valid"]}
        with mock.patch.object(C, "input_paths", lambda s, x: {**real_paths(s, x), "trades": real_paths(s, x)["trades"].with_name("absent.parquet")} if x == day else real_paths(s, x)), \
                mock.patch.object(C, "MISSING_RECHECK_DELAY_S", 0.0):
            r = one()
        out["genuine: file missing under a present directory, after its rechecks"] = {"expected": "input_missing:trades", "reason": r["reason"], "passed": r["reason"] == "input_missing:trades" and r["undefined"]}
        stub = tmp / "stub_volume"
        with mock.patch.object(C, "input_paths", lambda s, x: {**real_paths(s, x), "trades": real_paths(s, x)["trades"].with_name("absent.parquet")} if x == day else real_paths(s, x)), \
                mock.patch.object(C, "sentinel_inputs", lambda s: [stub / "first_discovery_states.parquet"]), mock.patch.object(C, "MISSING_RECHECK_DELAY_S", 0.0):
            try:
                one()
                got = "no abort"
            except FileNotFoundError as e:
                got = f"FileNotFoundError, class {C.classify(e)}"
        out["a missing file on a volume whose discovery inputs are gone too"] = {"expected": "abort (FileNotFoundError, environment), not input_missing", "got": got, "passed": got == "FileNotFoundError, class environment"}
        r = one(w=win.clear())
        out["no accepted windows"] = {"expected": "no_accepted_joint_windows", "e001_reason": r["e001_reason"], "episode_reason": r["episode_reason"], "undefined": r["undefined"],
                                      "passed": not r["undefined"] and r["e001_reason"] == r["episode_reason"] == "no_accepted_joint_windows"}
        r = one(ep=1e12)
        out["no qualifying episode"] = {"expected": "no_qualifying_episodes", "episode_reason": r["episode_reason"], "e001_valid": r["e001_valid"], "passed": not r["undefined"] and r["e001_valid"] and r["episode_reason"] == "no_qualifying_episodes"}
        fake = tmp / "fake_acceptance"
        fake.mkdir()
        (fake / "summary.json").write_text(json.dumps({"provenance": {"git_commit": "not-the-run-of-record", "git_dirty": False}, "tardis": []}))
        o = tmp / "not_of_record.json"
        code, err = main_with(o, mock.patch.object(C, "acceptance_dir", lambda: fake))
        out["acceptance summary not from the run of record"] = {"expected": "abort, exit 3, no record, RuntimeError raised in closeout.py", "exit": code, "stderr": err.strip(), "record_written": o.exists(),
                                                                "passed": code == 3 and not o.exists() and "RuntimeError at closeout.py" in err}
        o = ROOT / "results" / "closeout_freeze" / "standins_must_not_land_here.json"
        code, err = main_with(o)
        out["stand-ins aimed at results/closeout_freeze/"] = {"expected": "refused, exit 2, nothing written", "exit": code, "record_written": o.exists(), "passed": code == 2 and not o.exists()}
        o = tmp / "exists.json"
        o.write_text("first")
        code, err = main_with(o)
        out["output already exists"] = {"expected": "refused, exit 2, unchanged", "exit": code, "passed": code == 2 and o.read_text() == "first"}
        t = tmp / "test_days.json"
        with mock.patch.object(sys, "argv", ["p", str(t), "--test-days"]), mock.patch.object(C, "input_mismatch", side_effect=AssertionError("a test-day read was attempted")):
            code = P.main()
        out["test days refused in this repository before any read"] = {"expected": "refused, exit 2, no input read", "exit": code, "record_written": t.exists(), "passed": code == 2 and not t.exists()}
    audit = subprocess.run([sys.executable, "-c", READ_AUDIT.format(root=str(ROOT), out=str(DEV / "precheck_read_audit_status.json"), skip_clean=False)], capture_output=True, text=True, env={**os.environ, "PYTHONPATH": str(ROOT)})
    res_audit = json.loads(audit.stdout.strip().splitlines()[-1]) if audit.returncode == 0 else {"error": audit.stderr[-300:]}
    (DEV / "precheck_read_audit_status.json").unlink(missing_ok=True)
    rel = sorted(str(Path(x).relative_to(ROOT)) if str(x).startswith(str(ROOT)) else x for x in res_audit.get("opened", []))
    expected = {str(p.relative_to(ROOT)) for x in d[10:] for p in real_paths(sym, x).values()} | {"results/acceptance_001/summary.json", "results/acceptance_001/windows.csv"}
    out["read audit on all five stand-ins"] = {"expected": "Parquet readers disabled and not called; Python file opens of data and acceptance files are exactly the four inputs per session, summary.json and windows.csv (hashed)",
                                               "opened_data_and_acceptance_files": rel, "note": "the hook sees Python opens; polars also scans windows.csv natively", "passed": audit.returncode == 0 and set(rel) == expected}
    res = {"status": "real tool on discovery stand-in sessions, with injected failures; no test session touched", "stand_in": day, "scenarios": out, "passed": all(r["passed"] for r in out.values()), "provenance": code_state()}
    DEV.mkdir(parents=True, exist_ok=True)
    (DEV / "precheck_faults.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: v["passed"] for k, v in out.items()}, indent=1))
    if not res["passed"]:
        raise SystemExit("a pre-check scenario did not behave as specified")
    return res


READ_AUDIT = """
import json, sys
opened = []
sys.addaudithook(lambda e, a: opened.append(str(a[0])) if e == "open" and isinstance(a[0], str) else None)
from pathlib import Path
import pyarrow.parquet as pq, polars as pl
import os, pyarrow.parquet.core as pqc, pyarrow.dataset as pds
def forbidden(*a, **k):
    print("forbidden read: " + str(a[:1]), flush=True)
    os._exit(99)                    # no exception handler can hide it
for mod in (pq, pqc):
    for name in ("read_metadata", "read_table", "read_schema", "read_pandas", "ParquetFile", "ParquetDataset"):
        if hasattr(mod, name):
            setattr(mod, name, forbidden)
pds.dataset = forbidden
for name in ("read_parquet", "scan_parquet", "read_parquet_schema", "read_parquet_metadata"):
    if hasattr(pl, name):
        setattr(pl, name, forbidden)
sys.path.insert(0, {root!r})
import tools.closeout_precheck as P
from lpx.research import closeout as C
if {skip_clean!r}:
    P.refuse_dirty_scope = lambda ws: None
res = P.run(Path({out!r}), False, C.Workspace(Path({root!r})))
print(json.dumps({{"opened": sorted(set(x for x in opened if x.startswith(({root!r} + "/data/", {root!r} + "/results/acceptance_001/")))), "days": list(res["sessions"])}}))
"""


def scratch_repo(base: Path) -> C.Workspace:
    """A scratch git repository with a synthetic frozen protocol, freeze record and owner authorisation."""
    base.mkdir(parents=True, exist_ok=True)
    ws = C.Workspace(base)
    ws.git("init", "-q")
    ws.git("config", "user.email", "rehearsal@example.invalid")
    ws.git("config", "user.name", "rehearsal")
    for rel, text in ((C.PROTOCOL, "# synthetic protocol (FROZEN)\n"), ("docs/DECISIONS.md", "decisions\n"), ("configs/x.toml", "a = 1\n"), ("lpx/x.py", "x = 1\n")):
        (base / rel).parent.mkdir(parents=True, exist_ok=True)
        (base / rel).write_text(text)
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "baseline")
    baseline = ws.git("rev-parse", "HEAD").strip()
    rec = C.build_freeze_record(ws, baseline, [C.PROTOCOL, "configs/x.toml"])
    p = base / C.FREEZE_RECORD
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec))
    h = C.sha256_file(p)
    with open(base / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h) + "\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "synthetic freeze")
    ws.append({"event": "authorised", "n": 1, "freeze_record_sha256": h, "utc": "synthetic"})
    return ws


def standin_ctx(rc, d, status, sessions=None, injection=None):
    """Stand-ins s11..s15 with fits on s1..s10, through the same builder as test mode (only sessions, fits and paths differ)."""
    return C.session_context(ROOT, "rehearsal", d[10:], "rehearsal", d[:10], status, injection, sessions)


def standin_status() -> dict:
    p = DEV / "precheck_standins.json"
    if not p.exists():
        subprocess.run([sys.executable, str(ROOT / "tools/closeout_precheck.py"), str(p), "--stand-ins"], check=True, env={**os.environ, "PYTHONPATH": str(ROOT)})
    r = json.loads(p.read_text())
    if r["provenance"]["trees"] != code_state()["trees"]:
        raise SystemExit("the stand-in input status is from other code: remove it and rerun")
    return r["sessions"]


def schema_of(a: dict) -> dict:
    return {e: {"state": b["state"]["status"], "checks": [c["id"] for c in b.get("checks", [])], "labels_present": all("label" in c for c in b.get("checks", []))} for e, b in a["experiments"].items()}


def rehearsal() -> dict:
    rc, d = days()
    status = standin_status()
    t0 = time.time()
    with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
        ws = scratch_repo(Path(tmp) / "repo")
        r = C.run_attempt(ws, standin_ctx(rc, d, status), C.RUNNERS, A.analyse, env_check=C.verify_environment)
        a = json.loads((ws.promoted / "closeout_analysis.json").read_text())
        allow_ok(a)
        res = {"check": "whole test path on stand-ins s11..s15 (scratch repository; values discarded unread, schema only)",
               "stand_ins": d[10:], "outcome": r["outcome"], "statuses": {k: v["status"] for k, v in r["statuses"].items()},
               "tables": sorted(p.name for p in ws.promoted.iterdir()), "schema": schema_of(a),
               "ledger": [e["event"] for e in ws.events()], "report_written": (ws.promoted / "CLOSEOUT_report.md").stat().st_size > 0,
               "allow_list_ok": True, "seconds": round(time.time() - t0),
               "provenance": code_state()}
    res["passed"] = res["outcome"] == "completed" and set(res["statuses"].values()) == {"complete"} and res["ledger"] == ["authorised", "started", "completed"] and res["report_written"]
    (DEV / "dryrun_check3_rehearsal.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("passed", "outcome", "statuses", "ledger", "seconds")}, indent=1))
    if not res["passed"]:
        raise SystemExit("the rehearsal did not complete as expected")
    return res


def allow_ok(a: dict) -> bool:
    A.assert_allowed(a["experiments"]["E003"]["reported_only"]["H1_reported"])
    A.assert_allowed(a["experiments"]["E004"]["reported_only"]["descriptive"])
    return True


DIE = """
import json, sys
from pathlib import Path
sys.path.insert(0, {root!r}); sys.path.insert(0, {root!r} + "/tools")
import closeout_dryrun as T
from lpx.research import closeout as C, closeout_analysis as A
rc, d = T.days()
C.run_attempt(C.Workspace(Path({repo!r})), T.standin_ctx(rc, d, json.loads(Path({status!r}).read_text())["sessions"], {sessions!r}, {inj!r}), C.RUNNERS, A.analyse)
"""


def faults() -> dict:
    """Real code path on one stand-in session: each injected failure against its expected ledger, statuses and next-start result."""
    rc, d = days()
    status = standin_status()
    s = d[10]
    none = {"E001": [], "E002": [], "E003": [], "E004": []}
    e1 = {**none, "E001": [s]}
    e34 = {**none, "E003": [s], "E004": [s]}
    sw = "not_confirmable_software"
    cases = [
        ("software in baseline code, E001", ("E001", s, "baseline"), e1, {"outcome": "completed", "E001": sw, "ledger": ["authorised 1", "started 1", "completed 1"]}),
        ("software in a marked block, E003, blocks E004", ("E003", s, "software"), e34, {"outcome": "completed", "E003": sw, "E004": sw, "ledger": ["authorised 1", "started 1", "completed 1"]}),
        ("software, E004 after a real E003", ("E004", s, "software"), e34, {"outcome": "completed", "E003": "complete", "E004": sw, "ledger": ["authorised 1", "started 1", "completed 1"]}),
        ("environment failure, E001", ("E001", s, "environment"), e1, {"outcome": "failed", "class": "environment", "ledger": ["authorised 1", "started 1", "failed 1"]}),
        ("close-out failure, E003", ("E003", s, "closeout"), e34, {"outcome": "failed", "class": "closeout", "ledger": ["authorised 1", "started 1", "failed 1"]}),
        ("close-out failure in the metadata step", ("meta", None, "closeout"), e1, {"outcome": "failed", "class": "closeout", "ledger": ["authorised 1", "started 1", "failed 1"]}),
        ("analysis failure", ("analysis", None, "closeout"), e1, {"outcome": "failed", "class": "closeout", "ledger": ["authorised 1", "started 1", "failed 1"]}),
    ]
    out, ok = {}, True
    for name, inj, sessions, want in cases:
        with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
            ws = scratch_repo(Path(tmp) / "repo")
            r = C.run_attempt(ws, standin_ctx(rc, d, status, sessions, inj), C.RUNNERS, A.analyse)
            got = {"outcome": r["outcome"], "class": r.get("class"), **{k: v["status"] for k, v in r.get("statuses", {}).items()},
                   "ledger": [e["event"] + (f" {e['n']}" if "n" in e else "") for e in ws.events()]}
            passed = all(got.get(k) == v for k, v in want.items())
            rec = {"injected": list(inj), "expected": want, "got": got, "passed": passed, "promoted": ws.promoted.exists(), "sealed_dir": ws.attempt_dir(1).exists(), "staging_left": ws.staging.exists()}
            if ws.promoted.exists():
                a = json.loads((ws.promoted / "closeout_analysis.json").read_text())
                rec["labels"] = {e: sorted({c["label"] for c in b.get("checks", [])}) for e, b in a["experiments"].items()}
                rec["partial_tables_of_lost_experiments"] = [p.name for p in ws.promoted.iterdir() if p.name.startswith(tuple(x.lower() for x, v in r["statuses"].items() if v["status"] == sw))]
                passed = passed and not rec["partial_tables_of_lost_experiments"]
                rec["passed"] = passed
            out[name] = rec
            ok &= passed
            print(name, "->", "ok" if passed else f"UNEXPECTED {got}", flush=True)
    # real deaths on the real path: a subprocess dies, recovery runs, the next attempt is allowed or refused as specified
    for name, inj, sessions, want_rec in (("process death in E001", ("E001", s, "death"), e1, "attempt 1 failed"),
                                          ("process death before the analysis", ("analysis", None, "death"), e1, "attempt 1 failed"),
                                          ("process death after the analysis file", ("after_analysis", None, "death"), e1, "completed from the primary analysis")):
        with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
            ws = scratch_repo(Path(tmp) / "repo")
            code = DIE.format(root=str(ROOT), repo=str(ws.root), status=str(DEV / "precheck_standins.json"), sessions=sessions, inj=inj)
            p = subprocess.run([sys.executable, "-c", code], env={**os.environ, "PYTHONPATH": str(ROOT)}, capture_output=True, text=True)
            rec_out = C.recover(ws)
            passed = p.returncode == 137 and rec_out == want_rec
            out[name] = {"injected": list(inj), "exit": p.returncode, "recovery": rec_out, "ledger": [e["event"] for e in ws.events()], "passed": passed}
            ok &= passed
            print(name, "->", rec_out, flush=True)
    # three failures: fail closed on the real path
    with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
        ws = scratch_repo(Path(tmp) / "repo")
        h = [e for e in ws.events() if e["event"] == "authorised"][0]["freeze_record_sha256"]
        for n in (1, 2, 3):
            if n > 1:
                ws.append({"event": "authorised", "n": n, "freeze_record_sha256": h, "utc": "synthetic"})
            C.run_attempt(ws, standin_ctx(rc, d, status, e1, ("analysis", None, "environment")), C.RUNNERS, A.analyse)
        rep = (ws.promoted / "CLOSEOUT_report.md").read_text()
        passed = [e["event"] for e in ws.events()][-2:] == ["failed", "closed"] and "FAILED CLOSED" in rep and not (ws.promoted / "closeout_analysis.json").exists() and "**confirmed" not in rep
        try:
            C.check_guards(ws)
            next_start = "allowed"
        except C.Refused as e:
            next_start = f"refused: {e}"
        out["three failures: fail closed, E001 finished each time"] = {"ledger": [e["event"] for e in ws.events()], "report_has_no_confirmed_label": "**confirmed" not in rep, "next_start": next_start, "passed": passed and next_start != "allowed"}
        ok &= out["three failures: fail closed, E001 finished each time"]["passed"]
    # staged-file completeness and the classifier's table blocks, on the real path
    extra = {}
    with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
        ws = scratch_repo(Path(tmp) / "repo")

        def stray(tables, ctx):
            (tables / "stray.csv").write_text("x")
            return A.analyse(tables, ctx)
        r = C.run_attempt(ws, standin_ctx(rc, d, status, e1, None), C.RUNNERS, stray)
        extra["unexpected staged file"] = {"expected": "attempt failed in the analysis, before any table is read", "outcome": r["outcome"], "location": ws.events()[-1].get("location"),
                                           "passed": r["outcome"] == "failed" and "closeout_analysis.py" in str(ws.events()[-1].get("location")) and not ws.promoted.exists()}
    for name, exc, want in (("a table write raises ValueError, E001", ValueError, {"outcome": "completed", "E001": sw}), ("a table write raises OSError, E001", OSError, {"outcome": "failed", "class": "environment"})):
        with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
            ws = scratch_repo(Path(tmp) / "repo")
            with mock.patch.object(pl.DataFrame, "write_csv", side_effect=exc("injected")):
                r = C.run_attempt(ws, standin_ctx(rc, d, status, e1, None), C.RUNNERS, A.analyse)
            got = {"outcome": r["outcome"], "class": r.get("class"), **{k: v["status"] for k, v in r.get("statuses", {}).items()}}
            extra[name] = {"expected": want, "got": got, "passed": all(got.get(k) == v for k, v in want.items())}
    # after the freeze, a pinned input with other bytes or missing: an integrity failure of the attempt, never an undefined session.
    # No data file is touched: the stand-in record pins other bytes, or the input's path is pointed at a file that does not exist.
    s2 = d[11]
    real_paths = C.input_paths
    gone = lambda sym, day: {**real_paths(sym, day), **({"trades": Path("/private/tmp/closeout_dryrun_absent/trades.parquet")} if day == s2 else {})}
    for name, st, paths, finding in (("a pinned input with other bytes after the freeze", {**status, s2: {**status[s2], "sha256": {**status[s2]["sha256"], "trades": "0" * 64}}}, real_paths, "modified"),
                                     ("a pinned input missing after the freeze", status, gone, "missing")):
        with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp, mock.patch.object(C, "input_paths", paths):
            ws = scratch_repo(Path(tmp) / "repo")
            r = C.run_attempt(ws, standin_ctx(rc, d, st, e1, None), C.RUNNERS, A.analyse)
            e = ws.events()[-1]
            h = [x for x in ws.events() if x["event"] == "authorised"][0]["freeze_record_sha256"]
            ws.append({"event": "authorised", "n": 2, "freeze_record_sha256": h, "utc": "synthetic"})
            try:
                next_start = f"allowed: attempt {C.check_guards(ws)[0]} on the same freeze record"
            except C.Refused as x:
                next_start = f"refused: {x}"
            got = [(f["session"], f["input"], f["finding"]) for f in (e.get("integrity") or {}).get("findings", [])]
            extra[name] = {"expected": f"attempt 1 failed, class integrity, {s2} trades {finding}; nothing promoted; attempt 2 allowed on the same record", "outcome": r["outcome"],
                           "class": r.get("class"), "failed_event_integrity": e.get("integrity"), "ledger": [x["event"] + f" {x['n']}" for x in ws.events()],
                           "promoted": ws.promoted.exists(), "sealed_dir": ws.attempt_dir(1).exists(), "next_start": next_start,
                           "passed": r["outcome"] == "failed" and r.get("class") == "integrity" and e["event"] == "failed" and e.get("failure_class") == "integrity"
                           and got == [(s2, "trades", finding)]
                           and not ws.promoted.exists() and ws.attempt_dir(1).exists() and next_start.startswith("allowed: attempt 2")}
    # a pinned input changed under an experiment whose frozen code then raises: integrity, with no software no-retry record. The input is a
    # copy of the stand-in's file (the run reads the original); only the pins check looks at the copy, which changes at the injected failure.
    with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
        ws = scratch_repo(Path(tmp) / "repo")
        copy = Path(tmp) / "trades_copy.parquet"
        shutil.copyfile(real_paths(rc["dataset"]["symbol"], s2)["trades"], copy)
        moved = lambda sym, day: {**real_paths(sym, day), **({"trades": copy} if day == s2 else {})}
        real_inject = C.inject

        def changed_then_raise(kind):
            copy.write_bytes(b"changed under the experiment")
            real_inject(kind)
        with mock.patch.object(C, "input_paths", moved), mock.patch.object(C, "inject", changed_then_raise):
            r = C.run_attempt(ws, standin_ctx(rc, d, status, e1, ("E001", s, "software")), C.RUNNERS, A.analyse)
        e = ws.events()[-1]
        got = [(f["session"], f["input"], f["finding"]) for f in (e.get("integrity") or {}).get("findings", [])]
        extra["a pinned input changed under an experiment whose frozen code then raises"] = {
            "expected": f"attempt 1 failed, class integrity, {s2} trades modified; no software no-retry record", "outcome": r["outcome"], "class": r.get("class"),
            "failed_event_integrity": e.get("integrity"), "software_experiments": e.get("software_experiments"),
            "passed": r["outcome"] == "failed" and r.get("class") == "integrity" and got == [(s2, "trades", "modified")] and e.get("software_experiments") == []}
    with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
        ws = scratch_repo(Path(tmp) / "repo")
        h = [e for e in ws.events() if e["event"] == "authorised"][0]["freeze_record_sha256"]
        bad = {**status, s2: {**status[s2], "sha256": {**status[s2]["sha256"], "trades": "0" * 64}}}
        for n in (1, 2, 3):
            if n > 1:
                ws.append({"event": "authorised", "n": n, "freeze_record_sha256": h, "utc": "synthetic"})
            C.run_attempt(ws, standin_ctx(rc, d, bad, e1, None), C.RUNNERS, A.analyse)
        rep = (ws.promoted / "CLOSEOUT_report.md").read_text()
        classes = [e.get("failure_class") for e in ws.events() if e["event"] == "failed"]
        extra["three integrity failures: fail closed"] = {"ledger": [e["event"] for e in ws.events()], "failure_classes": classes,
                                                          "passed": [e["event"] for e in ws.events()][-2:] == ["failed", "closed"] and classes == ["integrity"] * 3
                                                          and "FAILED CLOSED" in rep and not (ws.promoted / "closeout_analysis.json").exists() and "**confirmed" not in rep}
    # a pinned data file changed after the freeze: an integrity failure recorded right after `started`, before anything is read
    with tempfile.TemporaryDirectory(dir="/private/tmp") as tmp:
        ws = scratch_repo(Path(tmp) / "repo")
        data = "results/acceptance_001/windows.csv"
        (ws.root / data).parent.mkdir(parents=True)
        (ws.root / data).write_text("windows\n")
        ws.git("add", "-A")
        ws.git("commit", "-q", "-m", "a data file")
        fr = ws.root / C.FREEZE_RECORD
        frec = json.loads(fr.read_text())
        frec["pinned_sha256"][data] = C.sha256_file(ws.root / data)
        fr.write_text(json.dumps(frec))
        h = C.sha256_file(fr)
        with open(ws.root / "docs/DECISIONS.md", "a") as f:
            f.write(C.FREEZE_APPROVAL.format(h=h) + "\n")
        ws.git("add", "-A")
        ws.git("commit", "-q", "-m", "freeze record with a data pin")
        ws.append({"event": "authorised", "n": 1, "freeze_record_sha256": h, "utc": "synthetic"})
        (ws.root / data).write_text("changed after the freeze\n")
        built = []
        r = C.run_attempt(ws, lambda out, progress: built.append(1), C.RUNNERS, A.analyse)
        e = ws.events()[-1]
        got = [(f["session"], f["input"], f["finding"]) for f in (e.get("integrity") or {}).get("findings", [])]
        extra["a pinned data file changed after the freeze"] = {
            "expected": "attempt 1 failed, class integrity, recorded right after started; no context built, nothing read", "outcome": r["outcome"],
            "class": r.get("class"), "failed_event_integrity": e.get("integrity"), "context_built": bool(built), "ledger": [x["event"] for x in ws.events()],
            "passed": r == {"attempt": 1, "outcome": "failed", "class": "integrity"} and not built and got == [(None, data, "modified")]
                      and [x["event"] for x in ws.events()][-2:] == ["started", "failed"]}
    for name, rec in extra.items():
        print(name, "->", "ok" if rec["passed"] else f"UNEXPECTED {rec}", flush=True)
        out[name] = rec
        ok &= rec["passed"]
    # the real repository, now
    try:
        C.check_guards(C.Workspace(ROOT))
        refusal = "NOT REFUSED"
    except C.Refused as e:
        refusal = str(e)
    res = {"status": "synthetic failures on a stand-in session (real runners, real analysis); no test session touched", "scenarios": out, "real_repository_test_mode": f"refused: {refusal}", "passed": ok and refusal != "NOT REFUSED",
           "provenance": code_state()}
    (DEV / "fault_injection_realpath.json").write_text(json.dumps(res, indent=1))
    print("all as expected:", res["passed"], flush=True)
    if not res["passed"]:
        raise SystemExit("a fault scenario did not behave as specified")
    return res


if __name__ == "__main__":
    cmd = sys.argv[1]
    require_clean()
    if cmd in ("e001", "e002", "e003", "e004"):
        run_one(cmd.upper())
    else:
        {"fits": check_fits, "compare": compare, "inventory": inventory, "rehearsal": rehearsal, "faults": faults, "precheck": precheck_scenarios}[cmd]()
