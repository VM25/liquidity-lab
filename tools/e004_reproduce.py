"""E004 reproduction (E004.md section 1 step 5 and section 7.1), before the run, with the E004 engine options off:

    E002   every frozen gross row of the 15 discovery sessions, bit for bit (tools/reproduce_e002_session.py's check);
    E003   on the evaluation sessions: the walk-forward M1/M2 equal results/e003/e003_models.json; REF forecasts equal the
           per-row recomputation from those coefficients and E003's aggregates; REF policy rows (P0, P3[M2] under the
           three fill models, regional) equal E003's frozen rows;
    D0     j(k) = k and NV = REF bitwise; P0 and P3[M2] through the view path equal REF (fills and every column).
No E004 outcome is computed (D0 is the reference itself).

Status: modeled historical replay / observed (reruns of frozen discovery computations; no new outcome).
    E003 full  (mode e003full) every frozen E003 row of one evaluation session (all 8 policies x 9 scenarios x fee rules)
           through the refactored run_session, every column, exactly.
Usage: PYTHONPATH=. uv run python tools/e004_reproduce.py [e002|e003|e003full|all]
       (writes results/e004_dev/reproduction_*.json; refuses a dirty tree)
"""

import importlib.util
import json
import sys
import time

import numpy as np
import polars as pl

from lpx.data.acquire import ROOT
from lpx.provenance import provenance, require_clean, sha256_file
from lpx.research import e003 as E3
from lpx.research import e003_features as F
from lpx.research import e004 as E4
from lpx.research import e004_degrade as DG
from lpx.research import e004_policy as PO
from lpx.research.e002 import to_states, to_trades

OUT = ROOT / "results" / "e004_dev"


STATUS = "modeled historical replay / observed (rerun of frozen discovery computations; no new outcome)"


def refuse_test(days: list[str]) -> None:
    import tomllib
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    if set(days) & set(rc["splits"]["test"]):
        raise PermissionError("test sessions are sealed")


def e002() -> dict:
    spec = importlib.util.spec_from_file_location("rep2", ROOT / "tools" / "reproduce_e002_session.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    days = json.loads((m.E.OUT / "e002_meta.json").read_text())["sessions"]
    refuse_test(days)
    res = []
    for d in days:
        r = {**m.main(d), "status": STATUS}
        res.append(r)
        print(d, "E002 reproduced" if r["reproduced"] else f"E002 MISMATCH {r['mismatched_columns']}", flush=True)
    out = {"sessions": len(res), "reproduced": all(r["reproduced"] for r in res), "per_session": res}
    return out


def e003() -> dict:
    e4, sc = E4.load_cfg()
    import tomllib
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    days = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    refuse_test(days)
    k0 = e4["scope"]["min_training_sessions"]
    fm, fg, ff, fcal = E4.e003_frozen()
    tick = sc["instrument"]["tick"]
    fc = sc["features"]
    thin, res = {}, []
    for d in days:
        st, tr, eps = E3.load_session(sc, d)
        thin[d] = E3.features(sc, st, tr, eps).filter(pl.col("eligible")).gather_every(fc["fit_thinning"])
    for i, d in enumerate(days[k0:], start=k0):
        t0 = time.time()
        models = E3.fit_models(sc, {x: thin[x] for x in days[:i]}, d, 5)
        tr_rows = pl.concat([thin[x] for x in days[:i]])
        rv_med = float(tr_rows.filter(pl.col("y_5s").is_not_nan() & pl.col("y_5s").is_not_null())["rv_60s"].median())
        rv_gate = sc["policies"]["p4_vol_gate_multiple"] * rv_med
        E4.check_models(d, models, rv_med, rv_gate, fm)
        st, tr, eps = E3.load_session(sc, d)
        ft = E3.features(sc, st, tr, eps)
        f_ref = E4.check_ref_forecasts(d, ft, models, fm, ff, fcal)
        A = DG.from_frames(d, st, tr, eps, tick)
        D0, _, _, part, _, _ = E4.cell_rows(e4, sc, A, "D0", "eval", 0, None)
        if not np.array_equal(part["view_row"], A.rows):
            raise AssertionError("D0: j(k) != k")
        if not np.array_equal(models["M2"].predict(E4.xframe(part)) * part["has"], f_ref):
            raise AssertionError("D0: NV != REF")
        states = to_states(st, tick)
        E3.attach(states, ft, models, rv_gate)
        sd = E3.SessionData(states, to_trades(tr, tick), eps, sc)
        h0 = E4.state_hash(sd.states, sd.trades)
        prim = sc["e004_primary"]
        ref, n = {}, 0
        for base in E4.BASES:
            for model, lat in [prim] + [tuple(x) for x in e4["analysis"]["descriptive_scenarios"]]:
                agg, fills = E3.simulate(sd, base, model, lat, None)
                E4.check_ref_policy(d, agg, fg)
                ref[(base, model)] = (agg, fills)
                n += 1
        v0 = [PO.episode_views(sd.states, s0, D0.idx[p0:p1], D0.d[p0:p1], f_ref[o0:o1], E4.md_us(sc), b)
              for (a, b), (s0, _), (p0, p1), (o0, o1) in zip(A.eps, A.ep_states, D0.ep_pos, E4._offsets(A))]
        for base in E4.BASES:
            agg, fills = E3.simulate(sd, base, *prim, None, views=v0)
            if not E4._agg_equal(agg, ref[(base, prim[0])][0]) or fills != ref[(base, prim[0])][1]:
                raise AssertionError(f"{d} {base}: D0 through the view path differs from REF")
        if E4.state_hash(sd.states, sd.trades) != h0:
            raise AssertionError("exchange stream mutated")
        res.append({"day": d, "status": STATUS, "models_equal": True, "ref_forecasts_equal": True, "ref_policy_rows_equal": n,
                    "d0_identity": True, "d0_view_policy_identity": len(E4.BASES), "seconds": round(time.time() - t0, 1)})
        print(d, "E003 REF reproduced; D0 identities hold", flush=True)
    return {"sessions": len(res), "reproduced": True, "per_session": res}


def e003full(day: str = "2025-08-01") -> dict:
    """Every frozen E003 gross row of one evaluation session through the refactored run_session (zero tolerance)."""
    import tomllib
    e4, sc = E4.load_cfg()
    e3cfg = tomllib.loads((ROOT / "configs" / "e003_v1.toml").read_text())
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    days = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    refuse_test(days)
    i = days.index(day)
    fm, fg, _, _ = E4.e003_frozen()
    fc = e3cfg["features"]
    thin = {}
    for d in days[:i]:
        st, tr, eps = E3.load_session(e3cfg, d)
        thin[d] = E3.features(e3cfg, st, tr, eps).filter(pl.col("eligible")).gather_every(fc["fit_thinning"])
    models = {h: E3.fit_models(e3cfg, thin, day, h) for h in fc["horizons_s"]}
    tr_rows = pl.concat([thin[x] for x in days[:i]])
    rv_med = float(tr_rows.filter(pl.col("y_5s").is_not_nan() & pl.col("y_5s").is_not_null())["rv_60s"].median())
    rv_gate = e3cfg["policies"]["p4_vol_gate_multiple"] * rv_med
    E4.check_models(day, models[5], rv_med, rv_gate, fm)
    st, tr, eps = E3.load_session(e3cfg, day)
    ft = E3.features(e3cfg, st, tr, eps)
    states = to_states(st, e3cfg["instrument"]["tick"])
    E3.attach(states, ft, models[fc["primary_horizon_s"]], rv_gate)
    rows = E3.run_session(states, to_trades(tr, e3cfg["instrument"]["tick"]), eps, e3cfg)
    for r in rows:
        _check_any_rule(day, r, fg)
    n_frozen = fg.filter(pl.col("day") == day).height
    if n_frozen != len(rows):
        raise AssertionError(f"{day}: {len(rows)} rows rerun, {n_frozen} frozen")
    print(day, f"E003 run_session reproduced ({len(rows)} rows, every column)", flush=True)
    return {"day": day, "status": STATUS, "rows": len(rows), "reproduced": True}


def _check_any_rule(day: str, agg: dict, gross: pl.DataFrame) -> None:
    e = gross.filter((pl.col("day") == day) & (pl.col("policy") == agg["policy"]) & (pl.col("fill_model") == agg["fill_model"])
                     & (pl.col("latency") == agg["latency"]) & (pl.col("fee_rule") == agg["fee_rule"]))
    if e.height != 1:
        raise AssertionError(f"{day} {agg['policy']} {agg['fee_rule']}: no unique E003 row")
    cols = set(e.columns) - {"day", "split"}
    # the frozen table is the union of all rows' columns: a fee-aware row (P3F, P4) has only its own rule's columns, and
    # the other rules' columns are empty in the frozen row; anything else is a mismatch
    extra, absent = set(agg) - cols, cols - set(agg)
    if extra or any(e[c][0] is not None for c in absent):
        raise AssertionError(f"{day} {agg['policy']}: columns differ: {sorted(extra | {c for c in absent if e[c][0] is not None})}")
    bad = [k for k, v in agg.items() if not E4._same(e[k][0], v)]
    if bad:
        raise AssertionError(f"{day} {agg['policy']} {agg['fill_model']} {agg['latency']} {agg['fee_rule']}: differs in {bad}")


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    require_clean()
    OUT.mkdir(parents=True, exist_ok=True)
    prov = {**provenance(["configs/e004_v1.toml", "configs/e003_v1.toml", "configs/e002_v1.toml"]),
            "tool_sha256": sha256_file(ROOT / "tools" / "e004_reproduce.py"),
            "e002_tool_sha256": sha256_file(ROOT / "tools" / "reproduce_e002_session.py")}
    for name, fn in (("e002", e002), ("e003", e003), ("e003full", e003full)):
        if what in (name, "all"):
            r = fn()
            (OUT / f"reproduction_{name}.json").write_text(json.dumps({**r, "provenance": prov}, indent=1, default=str))
            if not r["reproduced"]:
                raise SystemExit(f"{name} not reproduced")
