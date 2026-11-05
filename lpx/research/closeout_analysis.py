"""Close-out analysis (docs/experiments/FINAL_EVALUATION.md, sections 3-5 and 8, Appendix A).

Implements the confirmation rules on the staged tables. These are point-estimate checks on five sessions: never interval
decisions. Session-bootstrap intervals and discovery-rule labels are not reported: frozen functions that compute them are
called unchanged and their output passes through the allow-list in configs/closeout_v1.toml, so such keys are discarded in
memory. The frozen label functions (e003_analysis.participation, e004_analysis.h4w, h4f, h40) are not called.
"""

from __future__ import annotations

import itertools
import json
import math
import tomllib
from pathlib import Path

import numpy as np
import polars as pl

from lpx.data.acquire import ROOT
from lpx.research import e002_analysis as A2
from lpx.research import e003_analysis as A3
from lpx.research import e004_analysis as A4

ALLOW = tomllib.loads((ROOT / "configs" / "closeout_v1.toml").read_text())["allow_list"]
NEED = 4                         # at least 4 of the 5 sessions (E004 confirmation_min_sessions; protocol section 3.1)
CONFIRMED = "confirmed (point estimate)"
NOT_CONFIRMED = "not confirmed"
NOT_CONFIRMABLE = "not confirmable"
REPORTED = "reported only"
H4W_WORDING = "no material deterioration under the specified threshold"
H4W_NOTE = ("A confirmed label means a replicated point estimate below the one-sided 1 bp threshold. It is not equivalence, "
            "not proof of no effect, and says nothing about deterioration smaller than 1 bp.")
NOT_REFUTATION = ("Not confirmed means the test-session point estimate failed the frozen check. With five sessions this is not a "
                  "refutation of the discovery result and not evidence for the opposite claim.")
H4F_NOTE = "Secondary. Largely implied by the target choice (E004 §0, §9); reported against the projection, not as a discovery."
MEAN_A_SENTENCE = ("Discovery had the same sign without a flag, under 1% of L, and E004 §0 projects ρ_A ≈ 0 on y_view. A negative "
                   "mean of this size is not evidence that uncertainty-aware shrinkage does harm.")
DISCOVERY_MEAN_A = {"D1_S": -0.0055, "D3": -0.0066}
E001_METRICS = [f"{m}_{h}s" for m in ("mo", "rs") for h in (1, 5, 30)]
EXPERIMENT_TABLES = {"E001": ["e001_closeout.json", "e001_cells.csv", "e001_per_session.csv", "e001_sensitivity.csv"],
                     "E002": ["e002_gross_by_session.csv", "e002_net_by_session.csv"],
                     "E003": ["e003_gross_by_session.csv", "e003_net_by_session.csv", "e003_forecast_by_session.csv", "e003_calibration.csv", "e003_models.json", "e003_trades_without_receipt_time.json"],
                     "E004": ["e004_forecast_by_session.csv", "e004_calibration.csv", "e004_degradation_by_session.csv", "e004_lambda.csv", "e004_policy_gross_by_session.csv", "e004_policy_net_by_session.csv",
                              "e004_windows_by_session.csv", "e004_invariants.json"]}
SIDECARS = ("E001", "E002", "E003")          # E004's tables carry a status column
INFRASTRUCTURE = ("closeout_input_status.json", "closeout_relative_tick.json", *(f"closeout_status_{e}.json" for e in EXPERIMENT_TABLES))
NOT_STAGED_TABLES = ("closeout.log", "closeout_meta.json", ".DS_Store")
H4F_CELLS = ("D1_S", "D1_E", "D3", "D4", "D2", "D1_S1", "D1_S3")
H4F_MODELS = ("REF", "NV", "UA-lambda", "PL-lambda", "RF-lambda")


def t_int(x: np.ndarray) -> list:
    """Descriptive t-interval on the session values; never used by a rule."""
    return A4.t_interval(np.asarray(x, float), 95.0)


def keep(obj, allowed: set | None = None):
    """Allow-list at leaf level: containers pass through; a scalar or a list of scalars survives only if its key is listed."""
    allowed = set(ALLOW["leaf_keys"]) if allowed is None else allowed
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(v, dict) or (isinstance(v, list) and v and isinstance(v[0], dict)):
                out[k] = keep(v, allowed)
            elif k in allowed:
                out[k] = v
        return out
    if isinstance(obj, list):
        return [keep(v, allowed) for v in obj]
    return obj


def assert_allowed(obj, path: str = "") -> None:
    """Every written leaf key of an allow-listed block is on the list (protocol section 7)."""
    allowed = set(ALLOW["leaf_keys"])
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict) or (isinstance(v, list) and v and isinstance(v[0], dict)):
                assert_allowed(v, f"{path}.{k}")
            elif k not in allowed:
                raise AssertionError(f"key outside the allow-list: {path}.{k}")
    elif isinstance(obj, list):
        for v in obj:
            assert_allowed(v, path)


def jsonable(x):
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    if isinstance(x, (np.floating,)):
        return jsonable(float(x))
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    return x


def by_day(df: pl.DataFrame, col: str, days: list[str]) -> np.ndarray:
    """Session values aligned with ``days``; NaN where a session has no row or a null value (undefined, never imputed)."""
    if df["day"].n_unique() != df.height:
        raise ValueError(f"duplicate sessions for {col}")
    v = dict(zip(df["day"].to_list(), df[col].cast(pl.Float64).to_list()))
    return np.array([np.nan if v.get(d) is None else v[d] for d in days], float)


def check_row(cid: str, label: str, values: dict, days: list[str], status: str, discovery, basis: tuple | None = None, **extra) -> dict:
    """A check's standard row: session values, defined count, sign counts and a descriptive interval (protocol section 3.1).
    ``basis``: the components the label rests on, when others are shown only as qualifiers."""
    row = {"id": cid, "label": label, "status": status, "discovery": discovery, **extra}
    if values:
        k = min(int((~np.isnan(np.asarray(values[c], float))).sum()) for c in (basis or values))
        row["label_basis"] = f"point estimate, {k} of {len(days)} defined"
        row["components"] = {}
        for k, x in values.items():
            x = np.asarray(x, float)
            d = x[~np.isnan(x)]
            row["components"][k] = {"session_values": dict(zip(days, [None if np.isnan(v) else float(v) for v in x])),
                                    "defined": int(d.size), "mean": float(d.mean()) if d.size else None,
                                    "positive": int((d > 0).sum()), "negative": int((d < 0).sum()),
                                    "t_interval_95_descriptive_not_used": t_int(x)}
    return row


def definedness_ok(*xs: np.ndarray) -> bool:
    """Each component is defined in at least 4 of the 5 sessions (per component, protocol section 3.1)."""
    return all(int((~np.isnan(np.asarray(x, float))).sum()) >= NEED for x in xs)


def mean_of(x: np.ndarray) -> float:
    x = np.asarray(x, float)
    return float(np.nanmean(x)) if (~np.isnan(x)).any() else float("nan")


# ------------------------------------------------------------------------------------------------ E001
def e001_block(tables: Path, days: list[str], state: dict) -> dict:
    disc = json.loads((ROOT / "results" / "e001" / "e001_discovery.json").read_text())
    d_mean = {r["metric"]: r["mean_of_session_means"] for r in disc["primary"]}
    if state["status"] != "complete":
        c = [_lost("E001 " + m, state) for m in E001_METRICS]
        return {"state": state, "checks": c, "tally": _tally(c), "reported_only": _lost_items(state), "not_computed_on_test": NOT_COMPUTED["E001"]}
    ps = pl.read_csv(tables / "e001_per_session.csv", infer_schema_length=None) if (tables / "e001_per_session.csv").exists() else None
    for f in ("e001_cells.csv", "e001_sensitivity.csv"):
        if (tables / f).exists():
            extra = set(pl.read_csv(tables / f, n_rows=1).columns) - set(ALLOW["e001_keys"])
            if extra:
                raise AssertionError(f"{f} holds columns outside the allow-list: {sorted(extra)}")
    checks = []
    for m in E001_METRICS + ["es"]:
        x = by_day(ps, m, days) if ps is not None else np.full(len(days), np.nan)
        sign = 1.0 if d_mean[m] > 0 else -1.0
        ok_def = definedness_ok(x)
        count = int((sign * x > 0).sum())                # an undefined session counts as a failure
        if not ok_def:
            lab = NOT_CONFIRMABLE
        elif sign * mean_of(x) > 0 and count >= NEED:
            lab = CONFIRMED
        else:
            lab = NOT_CONFIRMED
        row = check_row(f"E001 {m}", lab if m != "es" else REPORTED, {m: x}, days, "observed", d_mean[m],
                        rule="mean of session means has the discovery sign, and that sign holds in at least 4 of 5 sessions",
                        sign_count=count, protocol_added=True)
        if m == "es":
            row.update(same_test_no_weight="sign rule holds" if lab == CONFIRMED else "sign rule fails" if lab == NOT_CONFIRMED else "not computable",
                       note="Close to mechanical for aggressive trades; no confirmatory weight.")
        checks.append(row)
    rep = {} if ps is not None else {"note": "no valid session"}
    for f in ("e001_cells.csv", "e001_sensitivity.csv"):
        if (tables / f).exists():
            rep[f] = pl.read_csv(tables / f, infer_schema_length=None).to_dicts()
    if (tables / "e001_closeout.json").exists():
        r = json.loads((tables / "e001_closeout.json").read_text())
        rep.update({k: r.get(k) for k in ("descriptive", "exclusions", "proxy_validation_qty_ge_touch", "sensitivity_specs")})
    disc_side = {"e001_cells.csv": _read_csv(ROOT / "results/e001/e001_discovery_cells.csv"),
                 "e001_sensitivity.csv": _read_csv(ROOT / "results/e001/e001_discovery_sensitivity.csv"),
                 "descriptive": disc.get("descriptive"), "exclusions": disc.get("exclusions"),
                 "proxy_validation_qty_ge_touch": disc.get("proxy_validation_qty_ge_touch")}
    return {"state": state, "checks": checks[:-1], "es": checks[-1], "reported_only": rep, "status": "observed", "family": "one family (rs = es - 2 mo)",
            "tally": _tally(checks[:-1]), "discovery_side": disc_side, "not_computed_on_test": NOT_COMPUTED["E001"]}


# ------------------------------------------------------------------------------------------------ E002
def e002_block(tables: Path, days: list[str], state: dict) -> dict:
    if state["status"] != "complete":
        return {"state": state, "checks": [], "reported_only": _lost_items(state), "not_computed_on_test": NOT_COMPUTED["E002"]}
    cfg = tomllib.loads((ROOT / "configs" / "e002_v1.toml").read_text())
    if not (tables / "e002_net_by_session.csv").exists():
        return {"state": state, "checks": [], "reported_only": {"note": "no valid session"}, "not_computed_on_test": NOT_COMPUTED["E002"]}
    net = pl.read_csv(tables / "e002_net_by_session.csv", infer_schema_length=None)
    net = net.sort(["policy", "fill_model", "latency", "fee_schedule", "day"])
    rng = np.random.default_rng(cfg["analysis"]["seed"])
    fee, models = cfg["fees"]["default"], cfg["fill_models"]["primary"]
    n = cfg["analysis"]["bootstrap_resamples"]
    k = cfg["analysis"].get("min_defined_sessions", 0)
    st = A2.scenario_table(net, fee, models, n, rng, k)
    pt = A2.paired_table(net, fee, models, n, rng, k)
    mp = A2.model_pairs_table(net, fee, models, n, rng, k)
    ranges = [{"policy": pol, "latency": lat, "range_bp_across_fill_models": float(g["mean"].max() - g["mean"].min())}
              for (pol, lat), g in st.group_by(["policy", "latency"], maintain_order=True)]
    rep = {"scenario_table": keep(st.to_dicts()), "paired_table": keep(pt.to_dicts()), "model_pairs_table": keep(mp.to_dicts()),
           "descriptive_range_of_means": keep(ranges)}
    outcome = A2.OUTCOME
    scen = net.filter((pl.col("fee_schedule") == fee) & pl.col("fill_model").is_in(models) & pl.col("policy").is_in(["P0", "P1"]))   # scenario_table's rows
    rep["scenario_t_intervals_95_descriptive_not_used"] = [
        {"policy": pol, "fill_model": model, "latency": lat, "t_interval": t_int(A2._vals(g, outcome))}
        for (pol, model, lat), g in sorted(scen.group_by(["policy", "fill_model", "latency"], maintain_order=True), key=lambda x: x[0])]
    rep["paired_t_intervals_95_descriptive_not_used"] = [{"fill_model": m, "latency": lat, "t_interval": t_int(x)} for (m, lat), x in e002_paired(net, fee, models).items()]
    rep["model_pair_t_intervals_95_descriptive_not_used"] = [{"policy": pol, "latency": lat, "pair": pair, "t_interval": t_int(x)} for (pol, lat, pair), x in e002_model_pairs(net, fee, models).items()]
    d2 = json.loads((ROOT / "results/e002/e002_h2.json").read_text())
    return {"state": state, "checks": [], "reported_only": rep, "status": "modeled historical replay; VIP0 attainable; other schedules hypothetical",
            "note": "E002 §10.10: the test sessions only report the same tables; no confirmation claim is made.", "not_computed_on_test": NOT_COMPUTED["E002"],
            "discovery_side": {"scenario_table": d2["scenario_table"], "paired_table": d2["paired_table"], "model_pairs_table": d2["materiality"],
                               "descriptive_range_of_means": d2["descriptive_range_of_means"]}}


def e002_paired(net: pl.DataFrame, fee: str, models: list[str]) -> dict[tuple, np.ndarray]:
    """Session values of P1 - P0, on e002_analysis.paired_table's pairing; its `mean` is their mean."""
    sub = net.filter((pl.col("fee_schedule") == fee) & pl.col("fill_model").is_in(models))
    p0 = sub.filter(pl.col("policy") == "P0").select("day", "fill_model", "latency", pl.col(A2.OUTCOME).alias("p0"))
    p1 = sub.filter(pl.col("policy") == "P1").select("day", "fill_model", "latency", pl.col(A2.OUTCOME).alias("p1"))
    j = p0.join(p1, on=["day", "fill_model", "latency"]).with_columns((pl.col("p1") - pl.col("p0")).alias("d"))
    return {k: A2._vals(g, "d") for k, g in sorted(j.group_by(["fill_model", "latency"], maintain_order=True), key=lambda x: x[0])}


def e002_model_pairs(net: pl.DataFrame, fee: str, models: list[str]) -> dict[tuple, np.ndarray]:
    """Session values of each fill-model difference, on e002_analysis.model_pairs_table's pairing; its `mean` is their mean."""
    sub = net.filter((pl.col("fee_schedule") == fee) & pl.col("policy").is_in(["P0", "P1"]))
    out = {}
    for a, b in itertools.combinations(models, 2):
        x = sub.filter(pl.col("fill_model") == a).select("day", "policy", "latency", pl.col(A2.OUTCOME).alias("a"))
        y = sub.filter(pl.col("fill_model") == b).select("day", "policy", "latency", pl.col(A2.OUTCOME).alias("b"))
        j = x.join(y, on=["day", "policy", "latency"]).with_columns((pl.col("b") - pl.col("a")).alias("d"))
        for (pol, lat), g in j.group_by(["policy", "latency"], maintain_order=True):
            out[(pol, lat, f"{b} - {a}")] = A2._vals(g, "d")
    return dict(sorted(out.items()))


# ------------------------------------------------------------------------------------------------ E003
def e003_block(tables: Path, days: list[str], state: dict) -> dict:
    disc = json.loads((ROOT / "results" / "e003" / "e003_analysis.json").read_text())
    ids = ("H1-F", "H1-T", "H3")
    if state["status"] != "complete":
        c = [_lost(i, state) for i in ids]
        return {"state": state, "checks": c, "tally": _tally(c), "reported_only": _lost_items(state), "not_computed_on_test": NOT_COMPUTED["E003"]}
    if not (tables / "e003_net_by_session.csv").exists():
        return {"state": state, "checks": [_undefined(i) for i in ids], "reported_only": {"note": "no valid session"},
                "tally": "0 of 3 confirmed", "not_computed_on_test": NOT_COMPUTED["E003"]}
    cfg = tomllib.loads((ROOT / "configs" / "e003_v1.toml").read_text())
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    net = pl.read_csv(tables / "e003_net_by_session.csv", infer_schema_length=None)
    net = net.sort(["policy", "fill_model", "latency", "fee_schedule", "day"])
    fc = pl.read_csv(tables / "e003_forecast_by_session.csv", infer_schema_length=None)
    c = A3.Ctx(net, fc, cfg)
    a = cfg["analysis"]
    vip0, lp = cfg["fees"]["default"], a["h3_fee_schedule"]
    s = lambda p, col, f: c.series(p, col, f)
    obs = c.days
    wide = lambda x: _expand(x, obs, days)
    # H1-F
    r2 = fc.filter((pl.col("horizon_s") == cfg["features"]["primary_horizon_s"]) & (pl.col("model") == "M2"))
    x = by_day(r2, "r2_os", obs)
    h1f_ok = definedness_ok(x)
    lab_f = NOT_CONFIRMABLE if not h1f_ok else CONFIRMED if mean_of(x) > 0 else NOT_CONFIRMED
    h1f = check_row("H1-F", lab_f, {"r2_os": wide(x)}, days, "observed", disc["H1"]["H1-F"]["mean"], rule="mean R²_OS (M2, 5 s) > 0 (E003 §10)",
                    reason=None if h1f_ok else "fewer than 4 sessions defined")
    # H1-T: literal rule; sign and materiality reported separately
    D = s("P3_M2", "gross_bp_per_notional", vip0) - s("P3_negM2", "gross_bp_per_notional", vip0)
    delta = a["h1_margin_bp"]
    activity = {p: float(np.nanmean(s(p, "gate_active_share", vip0))) for p in ("P3_M2", "P3_negM2")}
    m = mean_of(D)
    sign_ok, mat_ok = bool(m < 0), bool(m < delta)
    active = all(not math.isnan(v) and v >= a["h1_min_gate_activity"] for v in activity.values())
    why = "H1-F is not confirmed" if lab_f != CONFIRMED else "gate activity below 5%" if not active else "fewer than 4 sessions defined" if not definedness_ok(D) else None
    lab_t = NOT_CONFIRMABLE if why else CONFIRMED if sign_ok and mat_ok else NOT_CONFIRMED
    h1t = check_row("H1-T", lab_t, {"D_bp": wide(D)}, days, "modeled historical replay (gross, fee-free)", disc["H1"]["H1-T"]["mean"], reason=why,
                    rule="mean D < 0 (discovery sign) and mean D < δ = 0.5 bp (E003 §10, read literally)",
                    sign_same_as_discovery=sign_ok, economically_immaterial_below_delta=mat_ok, gate_activity=activity,
                    note=("A not-confirmed result with 0 <= mean D < δ means only that the sign differed. It is not evidence of "
                          "material translation, which would require D > δ."))
    # H3
    es = s("P4", "inc_es", lp) - s("P3F", "inc_es", lp)
    dd = s("P4", "max_drawdown", lp) - s("P3F", "max_drawdown", lp)
    nph = s("P4", "net_per_hour", lp) - s("P3F", "net_per_hour", lp)
    dh = disc["H3"]["noninferiority_margin"]
    if not definedness_ok(es, dd, nph):
        lab_h = NOT_CONFIRMABLE
    else:
        ok = mean_of(es) < 0 and mean_of(dd) < 0 and mean_of(nph) > 0 and mean_of(nph) > -dh
        lab_h = CONFIRMED if ok else NOT_CONFIRMED
    t4, t3 = s("P4", "turnover_per_hour", lp), s("P3F", "turnover_per_hour", lp)
    ratio = float(np.nanmean(t4) / np.nanmean(t3)) if np.nanmean(t3) > 0 else None
    ref = np.nanmean(s("P3_M2", "filled_notional", vip0))
    h3 = check_row("H3", lab_h, {"es_diff": wide(es), "drawdown_diff": wide(dd), "net_per_hour_diff": wide(nph)}, days,
                   "modeled historical replay; LP tier 4 fees are hypothetical, not attainable",
                   {"es": disc["H3"]["es_diff"]["mean"], "drawdown": disc["H3"]["drawdown_diff"]["mean"],
                    "net_per_hour": disc["H3"]["net_per_hour_diff"]["mean"]},
                   rule="mean ES diff < 0, mean drawdown diff < 0, mean net/h diff > 0 and > -δ_h (E003 §10)", delta_h=dh,
                   non_inferior=bool(mean_of(nph) > -dh), sign_net_per_hour_positive=bool(mean_of(nph) > 0),
                   reason=None if definedness_ok(es, dd, nph) else "fewer than 4 sessions defined in a component",
                   wording="non-inferior, but the sign differs" if -dh < mean_of(nph) <= 0 else None,
                   turnover_ratio_P4_over_P3F=ratio, partly_mechanical=ratio is not None and ratio < a["h3_mechanical_turnover_share"],
                   notional_share_of_P3_M2_lp_tier4={p: float(np.nanmean(s(p, "filled_notional", lp)) / ref) if ref > 0 else None for p in ("P3F", "P4")},
                   caveat="Passing 0.50 does not show that the risk reduction is independent of activity (A1).")
    # descriptive, through the allow-list
    full_h1, full_h3 = A3.h1(c), A3.h3(c)
    h3_rep = {"normalised": keep(full_h3["normalised"]), "other_schedules": keep(full_h3["other_schedules"])}
    e2net = tables / "e002_net_by_session.csv"
    ve = A3.versus_e002(c, pl.read_csv(e2net, infer_schema_length=None)) if e2net.exists() else None
    dsc = A3.descriptive(net, fc, rc)
    split = {}
    prim = c.prim
    for name, r in (("P3_M2_minus_P0_net_per_hour", ("P3_M2", "P0")), ("D_net_per_hour", ("P3_M2", "P3_negM2"))):
        g = s(r[0], "gross_per_hour", vip0) - s(r[1], "gross_per_hour", vip0)
        split[name] = {"gross_per_hour_mean": mean_of(g),
                       "maker_fees_per_hour_mean_mechanical": mean_of(fee_per_hour(net, r[0], prim, vip0, obs, "maker_fees") - fee_per_hour(net, r[1], prim, vip0, obs, "maker_fees")),
                       "taker_fees_per_hour_mean": mean_of(fee_per_hour(net, r[0], prim, vip0, obs, "taker_fees") - fee_per_hour(net, r[1], prim, vip0, obs, "taker_fees"))}
    policies = {}
    for p in a["participation_policies"]:
        nh = s(p, "net_per_hour", vip0)
        policies[p] = {"mean_net_per_hour": mean_of(nh), "difference_from_no_trade": mean_of(nh - s("NT", "net_per_hour", vip0)),
                       "gross_per_hour": mean_of(s(p, "gross_per_hour", vip0)),
                       "maker_fees_per_hour_mechanical": mean_of(fee_per_hour(net, p, prim, vip0, obs, "maker_fees")),
                       "taker_fees_per_hour": mean_of(fee_per_hour(net, p, prim, vip0, obs, "taker_fees")),
                       "turnover_per_hour": mean_of(s(p, "turnover_per_hour", vip0)),
                       "sessions_with_trades": int((s(p, "fills", vip0) > 0).sum()),
                       "session_values": dict(zip(obs, [None if np.isnan(v) else float(v) for v in nh])),
                       "discovery_mean_net_per_hour": disc["participation"]["policies"][p]["mean"]}
    checks = [h1f, h1t, h3]
    return {"state": state, "checks": checks, "tally": _tally(checks), "status": "forecasts observed; policies modeled historical replay; VIP0 attainable, other schedules hypothetical",
            "not_computed_on_test": NOT_COMPUTED["E003"],
            "reported_only": {"H1_reported": keep(full_h1["reported"]), "fee_split_per_hour_vip0": split, "H3": h3_rep,
                              "P0_versus_E002": keep(ve) if ve else "not run (E002 has no table)",
                              "descriptive": {"scenarios": keep(dsc["scenarios"]), "forecasts": keep(dsc["forecasts"])}},
            "discovery_side": {"H1_reported": disc["H1"]["reported"], "H3": {"normalised": disc["H3"]["normalised"], "other_schedules": disc["H3"]["other_schedules"]},
                               "P0_versus_E002": disc.get("P0_versus_E002"), "descriptive": {"scenarios": disc["descriptive"]["scenarios"], "forecasts": disc["descriptive"]["forecasts"]}},
            "policies_vip0_descriptive": {"status": "modeled historical replay; VIP0 attainable; descriptive, no label or rule",
                                          "note": ("A zero for P3F or P4 is mechanical: they abstained in every discovery session at VIP0. On discovery, preferring a policy to "
                                                   "not trading required a 99.29% interval above zero; a positive point estimate on five sessions does not show that."),
                                          "no_trade_net_per_hour": mean_of(s("NT", "net_per_hour", vip0)), "policies": policies}}


def fee_per_hour(net: pl.DataFrame, policy: str, prim: tuple, fee: str, days: list[str], col: str) -> np.ndarray:
    g = net.filter((pl.col("policy") == policy) & (pl.col("fill_model") == prim[0]) & (pl.col("latency") == prim[1])
                   & (pl.col("fee_schedule") == fee)).with_columns((pl.col(col) / pl.col("valid_hours")).alias("_f"))
    return by_day(g, "_f", days)


def _expand(x: np.ndarray, obs: list[str], days: list[str]) -> np.ndarray:
    """Session values on all listed days; a session absent from the table is NaN (marked undefined), never dropped."""
    v = dict(zip(obs, x))
    return np.array([v.get(d, np.nan) for d in days], float)


def _read_csv(p: Path) -> list[dict]:
    return pl.read_csv(p, infer_schema_length=None).to_dicts()


# ------------------------------------------------------------------------------------------------ E004
def h4w_check(w: pl.DataFrame, base: str, days: list[str], cfg: dict) -> dict:
    a = cfg["analysis"]
    ps = a["primary_scenario"]
    g = w.filter((pl.col("cell") == a["primary_cell"]) & (pl.col("base") == base) & (pl.col("fill_model") == ps["fill_model"])
                 & (pl.col("latency") == ps["latency"]))
    nmin, delta = a["h4w_min_orders_per_window"], a["h4w_margin_bp"]

    def series(dcol, ucol, pcol):
        x = by_day(g, dcol, days)
        u, p = by_day(g, ucol, days), by_day(g, pcol, days)
        return np.where((u >= nmin) & (p >= nmin), x, np.nan)

    x = series("D_W_bp", "orders_U", "orders_P")
    wd, ov = mean_of(by_day(g, "withdrawn_share", days)), mean_of(by_day(g, "overlap_share_of_wp", days))
    gates = {"withdrawn_share_mean": wd, "overlap_share_mean": ov, "sessions_defined": int((~np.isnan(x)).sum())}

    def label(v):
        count = int((v < delta).sum())
        if not (wd >= a["h4w_min_withdrawn_share"] and ov <= a["h4w_overlap_not_testable"]) or int((~np.isnan(v)).sum()) < NEED:
            return NOT_CONFIRMABLE, count
        return (CONFIRMED if mean_of(v) < delta and count >= NEED else NOT_CONFIRMED), count

    lab, count = label(x)
    stall = series("D_W_stall_bp", "orders_U_stall", "orders_P_stall")
    lab_s, _ = label(stall)
    stall_word = {CONFIRMED: "rule holds", NOT_CONFIRMED: "rule fails", NOT_CONFIRMABLE: "not computable"}[lab_s]
    d = x[~np.isnan(x)]
    disc = {"P0": -0.044, "P3_M2": -0.159}[base]
    return check_row(f"H4-W[{base}]", lab, {"D_W_bp": x, "D_W_stall_bp": stall}, days, "modeled historical replay under stress test",
                     disc, basis=("D_W_bp",), rule="mean D_W < 1 bp and D_W < 1 bp in at least 4 of 5 sessions (E004 §8; one-sided)", gates=gates,
                     sign_count_below_delta=count, sessions_D_W_negative=int((d < 0).sum()),
                     mean_D_W_sign="negative" if d.size and d.mean() < 0 else "non-negative",
                     stall_only_result=stall_word, sensitive_to_natural_staleness=lab_s != lab,
                     reason=None if lab != NOT_CONFIRMABLE else "a gate or the definedness rule failed",
                     interpretation=H4W_WORDING if lab == CONFIRMED else None, interpretation_note=H4W_NOTE,
                     withdrawn_and_shares={c: mean_of(by_day(g, c, days)) for c in ("wu_time_share_nostall", "wu_fill_share_nostall",
                                                                                     "wp_time_share_install", "wp_fill_share_install")})


def h4f_row(fc: pl.DataFrame, cell: str, tgt: str, days: list[str], cfg: dict) -> dict:
    a = cfg["analysis"]
    R = {}
    for m in H4F_MODELS:
        g = fc.filter((pl.col("cell") == cell) & (pl.col("target") == tgt) & (pl.col("model") == m))
        R[m] = by_day(g, "r2_os_pp", days)
    L, A, B, C = R["REF"] - R["NV"], R["UA-lambda"] - R["NV"], R["UA-lambda"] - R["PL-lambda"], R["RF-lambda"] - R["NV"]
    ok = ~(np.isnan(A) | np.isnan(L))
    sum_l = float(L[ok].sum()) if ok.any() else float("nan")
    rho_a = float(A[ok].sum() / sum_l) if ok.any() and sum_l != 0 else float("nan")
    okb = ~(np.isnan(B) | np.isnan(L))
    rho_b = float(B[okb].sum() / L[okb].sum()) if okb.any() and L[okb].sum() != 0 else float("nan")
    gate = bool(definedness_ok(L) and mean_of(L) >= a["h4f_immaterial_pp"] and int((L > 0).sum()) >= NEED)
    components_ok = definedness_ok(A, L)
    loo = [float(np.delete(A[ok], i).sum() / np.delete(L[ok], i).sum()) for i in range(int(ok.sum())) if np.delete(L[ok], i).sum() != 0]
    row = {"cell": cell, "target": tgt, "gate_passes": gate, "components_defined_ok": components_ok, "rho_A": rho_a, "rho_B": rho_b, "sum_L": sum_l,
           "status": "stress test", "leave_one_out_rho_A_range": [min(loo), max(loo)] if loo else None,
           "per_session": {d: {"A": _f(A[i]), "L": _f(L[i]), "A_over_L": _f(A[i] / L[i]) if L[i] else None} for i, d in enumerate(days)},
           **{k: {"mean": mean_of(v), "defined": int((~np.isnan(v)).sum()), "positive": int((v > 0).sum()),
                  "negative": int((v < 0).sum()), "t_interval_95_descriptive_not_used": t_int(v)}
              for k, v in (("L", L), ("A", A), ("B", B), ("C", C))}}
    if cell in ("D1_S", "D3"):
        proj = a["h4f_projection"][tgt]
        row.update(projection=proj, rho_A_minus_projection=rho_a - proj["rho_a"] if not math.isnan(rho_a) else None, note=H4F_NOTE)
    return row


def _f(v) -> float | None:
    return None if v is None or (isinstance(v, float) and math.isnan(v)) or np.isnan(v) else float(v)


def y_view_label(r: dict, rho_limit: float) -> str:
    if not (r["gate_passes"] and r["components_defined_ok"] and r["sum_L"] > 0):
        return NOT_CONFIRMABLE
    return CONFIRMED if r["rho_A"] < rho_limit else NOT_CONFIRMED


def y_view_row_label(labels: list[str]) -> str:
    return NOT_CONFIRMABLE if NOT_CONFIRMABLE in labels else CONFIRMED if all(x == CONFIRMED for x in labels) else NOT_CONFIRMED


def e004_block(tables: Path, days: list[str], state: dict) -> dict:
    ids = ("H4-W[P0]", "H4-W[P3_M2]")
    y_ids = ("H4-F[D1_S,y_view]", "H4-F[D3,y_view]")
    if state["status"] != "complete" or not (tables / "e004_windows_by_session.csv").exists():
        mk = (lambda i: _lost(i, state)) if state["status"] != "complete" else _undefined
        c = [mk(i) for i in ids]
        return {"state": state, "checks": c, "tally": _tally(c), "reported_only": _lost_items(state) if state["status"] != "complete" else {"note": "no valid session"},
                "h4f_y_view": {"status": "stress test", "row_label": NOT_CONFIRMABLE, "secondary": True, "note": H4F_NOTE, "pending_review_flag": False,
                               "cells": {i: mk(i) for i in y_ids}}}
    cfg = tomllib.loads((ROOT / "configs" / "e004_v1.toml").read_text())
    e3 = tomllib.loads((ROOT / cfg["scope"]["base_config"]).read_text())
    cfg["_fees"] = e3["fees"]
    cfg["policies"] = {**e3["policies"], **cfg["policies"]}
    disc4 = json.loads((ROOT / "results/e004/e004_analysis.json").read_text())
    w = pl.read_csv(tables / "e004_windows_by_session.csv", infer_schema_length=None)
    fc = pl.read_csv(tables / "e004_forecast_by_session.csv", infer_schema_length=None)
    gross = pl.read_csv(tables / "e004_policy_gross_by_session.csv", infer_schema_length=None)
    net = pl.read_csv(tables / "e004_policy_net_by_session.csv", infer_schema_length=None)
    obs = days
    hw = [h4w_check(w, b, obs, cfg) for b in ("P0", "P3_M2")]
    rows = {f"{c}:{t}": h4f_row(fc, c, t, obs, cfg) for c in H4F_CELLS for t in ("y_k", "y_view")}
    cells = {}
    for c in ("D1_S", "D3"):
        r = rows[f"{c}:y_view"]
        lab = y_view_label(r, cfg["analysis"]["h4f_rho_a"])
        cells[c] = {**r, "label": lab, "id": f"H4-F[{c},y_view]", "rule": "ρ_A = ΣA / ΣL < 0.25 (E004 §8)", "discovery_label": "not supported",
                    "discovery_rho_A": disc4["secondary"]["H4-F"][f"{c}:y_view"]["rho_A"]["value"],
                    "label_basis": f"point estimate, {min(r['A']['defined'], r['L']['defined'])} of {len(days)} defined",
                    "reason": None if lab != NOT_CONFIRMABLE else "the gate failed (mean L below 0.20 pp, or L > 0 in fewer than 4 sessions)" if not r["gate_passes"]
                    else "A or L is defined in fewer than 4 sessions" if not r["components_defined_ok"] else "ΣL ≤ 0 over the sessions where A and L are defined"}
        ma = r["A"]["mean"]
        if r["gate_passes"] and ma is not None and ma < 0:
            cells[c]["mean_A_below_0"] = {"mean_A": ma, "A_over_L": ma / r["L"]["mean"], "sessions_A_negative": r["A"]["negative"],
                                          "discovery_mean_A": DISCOVERY_MEAN_A[c], "discovery_sessions_negative": "6 of 10",
                                          "sentence": MEAN_A_SENTENCE if abs(r["rho_A"]) < 0.01 else None}
    labs = [cells["D1_S"]["label"], cells["D3"]["label"]]
    row_label = y_view_row_label(labs)
    d2_flag = any(rows[f"D2:{t}"]["gate_passes"] for t in ("y_k", "y_view"))
    x0 = by_day(fc.filter((pl.col("cell") == "D0") & (pl.col("target") == "y_k") & (pl.col("model") == "UA-lambda[D1_S]")), "r2_os_pp", obs) \
        - by_day(fc.filter((pl.col("cell") == "D0") & (pl.col("target") == "y_k") & (pl.col("model") == "REF")), "r2_os_pp", obs)
    other = {k: v for k, v in rows.items() if k not in ("D1_S:y_view", "D3:y_view")}
    desc = {"policy_D1_E": keep(A4.descriptive_policy(gross, net, w, cfg, "D1_E")),
            "policy_D1_S": keep(A4.descriptive_policy(gross, net, w, cfg, "D1_S")),
            "p3_ua_vs_pl_forecasts_D1_S": keep(A4.p3_forecast_variants(gross, net, cfg)),
            "window_quality": keep(A4.window_descriptive(w, cfg))}
    return {"state": state, "checks": hw, "tally": _tally(hw), "status": "modeled historical replay under stress test",
            "scope_note": "H4-W is a statement about fill selection (E004 §6). Realised U vs P and net per hour are descriptive replications.",
            "h4f_y_view": {"status": "stress test", "row_label": row_label, "cells": cells, "secondary": True, "note": H4F_NOTE,
                           "pending_review_flag": d2_flag},
            "reported_only": {"h4f_other": other, "H4_0": {"difference_pp": {"mean": mean_of(x0), "defined": int((~np.isnan(x0)).sum()),
                                                                               "t_interval_95_descriptive_not_used": t_int(x0)},
                                                           "status": "observed (model trained under stress test)",
                                                           "pending_review_flag": d2_flag, "discovery_label": "harmless"},
                              "descriptive": desc,
                              "status": "modeled historical replay under stress test; LP tier 4 fees hypothetical, not attainable"},
            "discovery_side": {"h4f_other": {k: v for k, v in disc4["secondary"]["H4-F"].items()}, "H4_0": disc4["secondary"]["H4-0"],
                               "descriptive": {k: disc4["descriptive"][k] for k in ("policy_D1_E", "policy_D1_S", "p3_ua_vs_pl_forecasts_D1_S", "window_quality")}}}


# ------------------------------------------------------------------------------------------------ assembling
def _tally(checks: list[dict]) -> str:
    return f"{sum(c['label'] == CONFIRMED for c in checks)} of {len(checks)} confirmed"


def _lost(cid: str, state: dict) -> dict:
    return {"id": cid, "label": NOT_CONFIRMABLE, "reason": f"software: {state.get('exception') or state.get('reason')}"}


def _undefined(cid: str) -> dict:
    return {"id": cid, "label": NOT_CONFIRMABLE, "reason": "no valid session"}


def _lost_items(state: dict) -> dict:
    return {"all": f"not run (software: {state.get('exception') or state.get('reason')})"}


NOT_COMPUTED = {"E001": {"exploratory tables": "exploratory by declaration (protocol section 11)"},
                "E002": {"cap-free addendum": "exploratory addendum (protocol section 11)",
                         "conditions (a), (b), h2_supported_on_discovery, material flags": "interval rules needing at least 12 sessions; false by construction on 5"},
                "E003": {"scenarios_by_period, forecasts_by_period": "discovery split; every test session would be labelled train-late",
                         "e003_models.json": "forwarded fit artifact, section 2"}}
# One entry per row of the protocol's Appendix A. `row` is text from that row's first two cells (a test compares them with the protocol).
# `kind`: check, reported or not_computed. `paths`: "/"-separated, within the experiment's block. `tables`: staged files. `count`: required lengths.
E001_CHECK_FIELDS = ["components", "label_basis", "sign_count", "rule"]
APPENDIX_A = [
    {"exp": "E001", "row": "primary metrics", "kind": "check", "paths": ["checks", "es"], "tables": ["e001_per_session.csv"], "count": {"checks": 6},
     "present": [f"checks[E001 {m}]/{k}" for m in E001_METRICS for k in E001_CHECK_FIELDS] + ["es/same_test_no_weight", "es/components"]},
    {"exp": "E001", "row": "cells (`e001_discovery_cells.csv`)", "kind": "reported", "tables": ["e001_cells.csv", "e001_sensitivity.csv"],
     "paths": ["reported_only/e001_cells.csv", "reported_only/e001_sensitivity.csv", "reported_only/sensitivity_specs", "reported_only/proxy_validation_qty_ge_touch",
               "reported_only/descriptive/secondary_horizons", "reported_only/descriptive/pre_state_age_ms_quantiles", "reported_only/exclusions"], "count": {"reported_only/sensitivity_specs": 12}},
    {"exp": "E001", "row": "exploratory", "kind": "not_computed", "paths": ["not_computed_on_test/exploratory tables"]},
    {"exp": "E002", "row": "`e002_gross_by_session.csv`", "kind": "reported", "tables": ["e002_gross_by_session.csv", "e002_net_by_session.csv"]},
    {"exp": "E002", "row": "`e002_h2.json`: scenario table", "kind": "reported",
     "paths": ["reported_only/scenario_table", "reported_only/paired_table", "reported_only/model_pairs_table", "reported_only/descriptive_range_of_means",
               "reported_only/scenario_t_intervals_95_descriptive_not_used", "reported_only/paired_t_intervals_95_descriptive_not_used", "reported_only/model_pair_t_intervals_95_descriptive_not_used"]},
    {"exp": "E002", "row": "`condition_a_sign_reversal`", "kind": "not_computed", "paths": ["not_computed_on_test/conditions (a), (b), h2_supported_on_discovery, material flags"]},
    {"exp": "E002", "row": "`results/e002/addenda/cap_free_subset.json`", "kind": "not_computed", "paths": ["not_computed_on_test/cap-free addendum"]},
    {"exp": "E003", "row": "`H1-F`, `H1-T`, gate activity", "kind": "check", "paths": ["checks"], "count": {"checks": 3},
     "present": ["checks[H1-F]/components", "checks[H1-F]/label_basis", "checks[H1-F]/rule", "checks[H1-T]/rule", "checks[H1-T]/label_basis", "checks[H1-T]/components", "checks[H1-T]/gate_activity", "checks[H1-T]/sign_same_as_discovery",
                 "checks[H1-T]/economically_immaterial_below_delta", "checks[H1-T]/note"]},
    {"exp": "E003", "row": "`H1.reported`", "kind": "reported",
     "paths": [f"reported_only/H1_reported/{k}" for k in ("D_net_per_hour", "P3_M2_minus_P0_gross_bp", "P3_M2_minus_P0_net_per_hour", "ranking_r2_M2_minus_M1", "ranking_P3_M2_minus_P3_M1_gross_bp", "P3_M2_net_per_hour_vip0")]
     + ["reported_only/fee_split_per_hour_vip0/P3_M2_minus_P0_net_per_hour", "reported_only/fee_split_per_hour_vip0/D_net_per_hour"]},
    {"exp": "E003", "row": "`H3` decision", "kind": "check", "paths": ["checks"],
     "present": ["checks[H3]/components", "checks[H3]/rule", "checks[H3]/delta_h", "checks[H3]/non_inferior", "checks[H3]/sign_net_per_hour_positive", "checks[H3]/wording", "checks[H3]/label_basis"]},
    {"exp": "E003", "row": "`H3.normalised`", "kind": "reported", "paths": ["reported_only/H3/normalised", "reported_only/H3/other_schedules"],
     "present": ["checks[H3]/turnover_ratio_P4_over_P3F", "checks[H3]/partly_mechanical", "checks[H3]/caveat"]},
    {"exp": "E003", "row": "LP tier 4 notional shares", "kind": "reported", "present": ["checks[H3]/notional_share_of_P3_M2_lp_tier4/P3F", "checks[H3]/notional_share_of_P3_M2_lp_tier4/P4"]},
    {"exp": "E003", "row": "`participation`", "kind": "reported", "paths": ["policies_vip0_descriptive/policies", "policies_vip0_descriptive/no_trade_net_per_hour"], "count": {"policies_vip0_descriptive/policies": 7},
     "present": [f"policies_vip0_descriptive/policies/{p}/{k}" for p in ("P0", "P1", "P3_M1", "P3_M2", "P3_negM2", "P3F", "P4")
                 for k in ("mean_net_per_hour", "difference_from_no_trade", "gross_per_hour", "maker_fees_per_hour_mechanical", "taker_fees_per_hour", "turnover_per_hour", "sessions_with_trades")]},
    {"exp": "E003", "row": "`descriptive.scenarios`", "kind": "reported", "paths": ["reported_only/descriptive/scenarios", "reported_only/descriptive/forecasts", "reported_only/P0_versus_E002"]},
    {"exp": "E003", "row": "`scenarios_by_period`", "kind": "not_computed", "paths": ["not_computed_on_test/scenarios_by_period, forecasts_by_period"]},
    {"exp": "E003", "row": "per-session forecast, calibration, gross and net tables", "kind": "reported",
     "tables": ["e003_forecast_by_session.csv", "e003_calibration.csv", "e003_gross_by_session.csv", "e003_net_by_session.csv", "e003_trades_without_receipt_time.json"]},
    {"exp": "E003", "row": "`e003_models.json`", "kind": "not_computed", "paths": ["not_computed_on_test/e003_models.json"]},
    {"exp": "E004", "row": "`primary` H4-W[P0]", "kind": "check", "paths": ["checks"], "count": {"checks": 2},
     "present": [f"checks[H4-W[{b}]]/{k}" for b in ("P0", "P3_M2") for k in ("components", "label_basis", "rule", "gates", "sign_count_below_delta", "sessions_D_W_negative", "mean_D_W_sign",
                                                                           "stall_only_result", "sensitive_to_natural_staleness", "withdrawn_and_shares", "interpretation_note")]},
    {"exp": "E004", "row": "`secondary` H4-F", "kind": "check", "paths": ["h4f_y_view/cells/D1_S", "h4f_y_view/cells/D3", "reported_only/h4f_other", "h4f_y_view/row_label", "h4f_y_view/note"],
     "count": {"reported_only/h4f_other": 12},
     "present": [f"h4f_y_view/cells/{c}/{k}" for c in ("D1_S", "D3") for k in ("label", "label_basis", "rule", "rho_A", "projection", "rho_A_minus_projection", "per_session", "leave_one_out_rho_A_range", "A", "L", "note")]
     + [f"reported_only/h4f_other/{c}:{t}/{k}" for c in ("D1_S", "D3") for t in ("y_k",) for k in ("projection", "rho_A_minus_projection", "note", "per_session")]
     + [f"reported_only/h4f_other/{c}:{t}/{k}" for c in ("D1_E", "D2", "D4", "D1_S1", "D1_S3") for t in ("y_k", "y_view") for k in ("rho_A", "per_session", "L", "A")]},
    {"exp": "E004", "row": "H4-0, D2 flag", "kind": "reported", "paths": ["reported_only/H4_0", "h4f_y_view/pending_review_flag"], "present": ["reported_only/H4_0/difference_pp", "reported_only/H4_0/pending_review_flag"]},
    {"exp": "E004", "row": "`descriptive` (policy D1-E and D1-S, P3 UA vs PL, window quality)", "kind": "reported",
     "paths": [f"reported_only/descriptive/{k}" for k in ("policy_D1_E", "policy_D1_S", "p3_ua_vs_pl_forecasts_D1_S", "window_quality")]},
    {"exp": "E004", "row": "per-session forecast, calibration, degradation", "kind": "reported",
     "tables": ["e004_forecast_by_session.csv", "e004_calibration.csv", "e004_degradation_by_session.csv", "e004_lambda.csv", "e004_policy_gross_by_session.csv", "e004_policy_net_by_session.csv", "e004_windows_by_session.csv"]},
    {"exp": "All", "row": "test relative tick per session", "kind": "reported", "top": ["relative_tick_bp", "undefined_sessions", "no_valid_unit"]},
]


def _segments(path: str) -> list[str]:
    """Split at "/" outside brackets: checks[H4-W[P0]]/gates -> ["checks[H4-W[P0]]", "gates"]."""
    out, cur, depth = [], "", 0
    for ch in path:
        depth += (ch == "[") - (ch == "]")
        if ch == "/" and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    return out + [cur]


def _at(block: dict, path: str):
    """The value at a "/"-separated path. A segment checks[ID] is the check row with that id. A missing key raises KeyError."""
    x = block
    for k in _segments(path):
        if k.startswith("checks[") and k.endswith("]"):
            rows = [c for c in x.get("checks", []) if c.get("id") == k[7:-1]] if isinstance(x, dict) else []
            if len(rows) != 1:
                raise KeyError(path)
            x = rows[0]
            continue
        if not isinstance(x, dict) or k not in x:
            raise KeyError(path)
        x = x[k]
    return x


def assert_appendix_a(res: dict, tables: Path | None = None) -> None:
    """Before anything is written (protocol section 7): every Appendix A row's items exist, with no null where a value is required. An experiment
    that was lost is marked not run, one with no valid session says so; `not computed on test` markers stay required in every state."""
    miss = []
    for row in APPENDIX_A:
        if row["exp"] == "All":
            miss += [f"All: {k}" for k in row["top"] if k not in res]
            continue
        b = res["experiments"].get(row["exp"], {})
        if "state" not in b or "reported_only" not in b:
            miss.append(f"{row['exp']}: block")
            continue
        lost = b["state"]["status"] != "complete" or bool({"all", "note"} & set(b["reported_only"]))
        if lost and row["kind"] != "not_computed":
            continue
        for p in row.get("paths", []):
            try:
                v = _at(b, p)
            except KeyError:
                miss.append(f"{row['exp']}: {row['row']}: {p}")
                continue
            if v is None or (isinstance(v, (list, dict, str)) and len(v) == 0) or (p in row.get("count", {}) and len(v) != row["count"][p]):
                miss.append(f"{row['exp']}: {row['row']}: {p} (null, empty or wrong length)")
        for p in row.get("present", []):            # values inside check rows may be undefined (None): they must exist
            try:
                v = _at(b, p)
            except KeyError:
                miss.append(f"{row['exp']}: {row['row']}: {p}")
                continue
            if p.endswith(("/label", "/rule", "/label_basis")) and not v:        # a check's label, rule and basis are never undefined
                miss.append(f"{row['exp']}: {row['row']}: {p} (null)")
        if tables is not None:
            miss += [f"{row['exp']}: {row['row']}: {t}" for t in row.get("tables", []) if not (tables / t).is_file()]
    if miss:
        raise AssertionError(f"Appendix A entries missing: {miss}")


def expected_staged(meta: dict) -> set[str]:
    """Exactly what staging must hold: the infrastructure files, and the tables of each experiment that ran to completion."""
    out = set(INFRASTRUCTURE)
    for e, tabs in EXPERIMENT_TABLES.items():
        st = meta["statuses"][e]
        if st["status"] == "complete" and st.get("note") != "no valid session":
            out |= set(tabs) | ({f"{t}.status.json" for t in tabs} if e in SIDECARS else set())
    return out


def verify_staged(tables: Path, meta: dict) -> None:
    """Before any table is read: the staged files are exactly the expected set, equal the metadata's listing with matching hashes, and each
    experiment's recorded outputs agree. Only the sealed log and the metadata itself sit outside the listing."""
    from lpx.research.closeout import sha256_file

    present = {str(p.relative_to(tables)) for p in tables.rglob("*") if p.is_file()} - set(NOT_STAGED_TABLES)
    if any(p.is_dir() for p in tables.rglob("*")):
        raise RuntimeError("staging holds a directory")
    listed, expected = set(meta["tables_sha256"]), expected_staged(meta)
    for name, have in (("missing", expected - present), ("unexpected", present - expected), ("unlisted", present - listed), ("listed but absent", listed - present)):
        if have:
            raise RuntimeError(f"staged files {name}: {sorted(have)}")
    for f, h in meta["tables_sha256"].items():
        if sha256_file(tables / f) != h:
            raise RuntimeError(f"{f} differs from the metadata")
    for e, st in meta["statuses"].items():
        for f, h in st.get("outputs", {}).items():
            if meta["tables_sha256"].get(f) != h:
                raise RuntimeError(f"{e}: {f} differs from the experiment's recorded outputs")


def analyse(tables: Path, ctx) -> dict:
    """Section 3 and Appendix A from the staged tables, after verifying the freeze record and the metadata's hashes."""
    meta = json.loads((tables / "closeout_meta.json").read_text())
    if getattr(ctx, "verify_for_analysis", None) is not None:
        ctx.verify_for_analysis(meta)
    elif ctx.mode != "dryrun":
        raise RuntimeError("the analysis must verify the freeze record")
    verify_staged(tables, meta)
    st = meta["statuses"]
    s = ctx.sessions
    wide = getattr(ctx, "all_days", None)
    inp, tick = tables / "closeout_input_status.json", tables / "closeout_relative_tick.json"
    status = json.loads(inp.read_text()) if inp.exists() else {}
    res = {"mode": ctx.mode, "sessions": s, "undefined_sessions": status.get("undefined", {}), "no_valid_unit": status.get("no_valid_unit", {}),
           "relative_tick_bp": json.loads(tick.read_text()) if tick.exists() else {},
           "not_refutation": NOT_REFUTATION, "fee_attainability": "VIP0 is the only attainable schedule; every other is hypothetical.",
           "experiments": {"E001": e001_block(tables, wide or s["E001"], st["E001"]), "E002": e002_block(tables, wide or s["E002"], st["E002"]),
                           "E003": e003_block(tables, wide or s["E003"], st["E003"]), "E004": e004_block(tables, wide or s["E004"], st["E004"])}}
    assert_appendix_a(res, tables)
    for block in (res["experiments"]["E001"]["reported_only"].get("e001_cells.csv"), res["experiments"]["E002"]["reported_only"].get("scenario_table")):
        if block:
            assert_allowed(block)
    if st["E003"]["status"] == "complete" and "H1_reported" in res["experiments"]["E003"]["reported_only"]:
        assert_allowed(res["experiments"]["E003"]["reported_only"]["H1_reported"])
    if st["E004"]["status"] == "complete" and "descriptive" in res["experiments"]["E004"]["reported_only"]:
        assert_allowed(res["experiments"]["E004"]["reported_only"]["descriptive"])
    return jsonable(res)


CHECK_IDS = {"E001": [f"E001 {m}" for m in E001_METRICS], "E003": ["H1-F", "H1-T", "H3"],
             "E004": ["H4-W[P0]", "H4-W[P3_M2]", "H4-F[D1_S,y_view]", "H4-F[D3,y_view]"]}
def _items(row: dict) -> list[str]:
    """Every item of an Appendix A row, named for the fail-closed report."""
    names = [p.replace("reported_only/", "").replace("policies_vip0_descriptive/", "") for p in row.get("paths", []) + row.get("present", [])] + row.get("tables", [])
    return [f"{row['row'].replace('`', '')}: {n}" for n in dict.fromkeys(names)]


def _reported_items(r: dict) -> list[str]:
    """The reported-only items of a row. A check row of E004 also carries reported parts (Appendix A: 'checks; the rest reported'): every
    item except the check cells themselves, their components and their label basis."""
    if r["kind"] == "reported":
        return _items(r)
    if r["kind"] == "check" and r["exp"] == "E004":
        cell_check = ("/label", "/label_basis", "/rule", "/rho_A", "/note")   # the y_view cells' check itself; the rest of a cell is reported
        keep = {**r, "paths": [p for p in r.get("paths", []) if not p.startswith("h4f_y_view/cells/") and p != "checks"],
                "present": [p for p in r.get("present", []) if not p.endswith(("/components", "/label_basis", "/rule")) and not (p.startswith("h4f_y_view/cells/") and p.endswith(cell_check))]
                + ([f"h4f_y_view/cells/{c}/mean_A_below_0 (when attached)" for c in ("D1_S", "D3")] if any(p.startswith("h4f_y_view/cells/") for p in r.get("present", [])) else [])}
        return _items(keep)
    return []


REPORTED_IDS = {e: (["primary metrics: es (reported only)"] if e == "E001" else []) + [i for r in APPENDIX_A if r["exp"] == e for i in _reported_items(r)]
                for e in ("E001", "E002", "E003", "E004")}
REPORTED_IDS["All"] = [f"test relative tick per session: {k}" for k in next(r for r in APPENDIX_A if r["exp"] == "All")["top"]]


def history(events: list[dict]) -> list[str]:
    keys = ("ledger_commit", "exception", "location", "path", "failure_class", "sealed_log_sha256", "freeze_record_sha256", "utc", "commit", "paths", "diff_sha256",
            "scope", "reason", "software_experiments", "integrity")
    return [f"- {e['event']} {e.get('n', '')}: " + ", ".join(f"{k}={e[k]}" for k in keys if e.get(k)) for e in events]


def fallback_report(events: list[dict]) -> str:
    """The fail-closed report (section 6): run history and labels, from no sealed table."""
    lines = ["# Close-out report: FAILED CLOSED", "", "Three technical attempts failed. No label was extracted from an incomplete execution, "
             "and every table stays sealed.", "", "## Run history", "", *history(events), "", "## Labels", "",
             "| Experiment | Item | Label |", "|---|---|---|"]
    for e, ids in CHECK_IDS.items():
        lines += [f"| {e} | {i} | not confirmable (run failure) |" for i in ids]
    for e, ids in REPORTED_IDS.items():
        lines += [f"| {e} | {i} | not run (run failure) |" for i in ids]
    return "\n".join(lines) + "\n"


def _n(v, spec: str = ".4g") -> str:
    return "undefined" if v is None else format(v, spec)


def flags_for(events: list[dict], cid: str) -> list[dict]:
    return [e for e in events if e["event"] == "compromised" and (e["scope"] == "all" or cid in e["scope"])]


def label_text(c: dict) -> str:
    if not c.get("label_basis"):
        return c["label"]
    return f"{'confirmed' if c['label'] == CONFIRMED else c['label']} ({c['label_basis']})"


def flag_text(cid: str, events: list[dict]) -> str:
    return "; ".join(f"COMPROMISED: {e['reason']}" + (f"; corrected: {e['corrected'][cid]}" if cid in e.get("corrected", {}) else "") for e in flags_for(events, cid))


def _row(c: dict, events: list[dict]) -> str:
    bits = []
    for k, v in (c.get("components") or {}).items():
        vals = ", ".join(f"{d}: {_n(x)}" for d, x in v["session_values"].items())
        bits.append(f"{k}: mean {_n(v['mean'])}; {v['defined']} defined, {v['positive']} +, {v['negative']} −; t-interval (descriptive, not used) "
                    f"{[_n(x) for x in v['t_interval_95_descriptive_not_used']]}; sessions {vals}")
    notes = [str(c[k]) for k in ("rule", "interpretation", "interpretation_note", "reason", "wording", "note", "caveat") if c.get(k)]
    for k in ("sign_count", "sign_count_below_delta", "sessions_D_W_negative", "mean_D_W_sign", "gates", "gate_activity", "sign_same_as_discovery", "economically_immaterial_below_delta",
              "stall_only_result", "sensitive_to_natural_staleness", "withdrawn_and_shares", "delta_h", "sign_net_per_hour_positive", "non_inferior", "turnover_ratio_P4_over_P3F",
              "partly_mechanical", "notional_share_of_P3_M2_lp_tier4", "same_test_no_weight"):
        if k in c:
            notes.append(f"{k}: {c[k]}")
    return f"| {c['id']} | **{label_text(c)}** | {c.get('discovery', '')} | {'<br>'.join(bits)} | {c.get('status', '')} | {'; '.join(notes)} | {flag_text(c['id'], events)} |"


def tally_line(checks: list[dict], events: list[dict], tally: str) -> str:
    flagged = [c for c in checks if flags_for(events, c["id"])]
    if not flagged:
        return tally
    corrected = sum((c["label"] == CONFIRMED and not any(c["id"] in e.get("corrected", {}) for e in flags_for(events, c["id"])))
                    or any(e.get("corrected", {}).get(c["id"], "").startswith("confirmed") for e in flags_for(events, c["id"])) for c in checks)
    return f"{tally} (original); {len(flagged)} compromised; corrected: {corrected} of {len(checks)}"


def flatten(obj, path: str = "") -> dict[str, object]:
    """Scalar leaves by path; list items are keyed by their identifying fields, so discovery and test rows align."""
    out: dict[str, object] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f"{path}.{k}" if path else str(k)))
    elif isinstance(obj, list):
        if obj and not isinstance(obj[0], dict):
            out[path] = str(obj)
        for i, r in enumerate(obj):
            if isinstance(r, dict):
                ident = "/".join(str(r[k]) for k in ("analysis", "spec", "cell", "policy", "fill_model", "latency", "fee_schedule", "pair", "model", "horizon_s", "metric") if k in r) or str(i)
                out.update(flatten({k: v for k, v in r.items() if k not in ("analysis", "spec", "cell", "policy", "fill_model", "latency", "fee_schedule", "pair", "model", "horizon_s", "metric")}, f"{path}[{ident}]"))
    else:
        out[path] = obj
    return out


def side_by_side(rep: dict, disc: dict | None) -> list[str]:
    """Every reported-only item with its discovery value beside it, at the same prominence as the checks."""
    t, d = flatten(rep), flatten(disc or {})
    d2 = dict(d)
    d2.update({k.replace("mean_p1_minus_p0", "mean"): v for k, v in d.items()})
    lines = ["| Item (reported only) | Discovery | Test |", "|---|---|---|"]
    lines += [f"| {k} | {d2.get(k, '')} | {'undefined' if v is None else v} |" for k, v in t.items()]
    return lines


def render_report(a: dict, events: list[dict]) -> str:
    """Every check and every reported-only item, per experiment, same prominence (section 8). Discovery and test side by side."""
    L = ["# Close-out report", "", f"Mode: {a['mode']}. {a['not_refutation']} {a['fee_attainability']}", "", "## Run history", "", *history(events), "",
         f"Undefined sessions (section 1's input rule; they leave every check): {a['undefined_sessions'] or 'none'}", "",
         f"Sessions with no valid unit in an experiment (not undefined): {a.get('no_valid_unit') or 'none'}", "", f"Test relative tick (bp), against 0.46–1.20 bp on discovery; applies to every bp result below; δ thresholds are not rescaled: {a.get('relative_tick_bp') or 'not available'}", ""]
    head = ["| Check | Label | Discovery | Test | Status | Notes | Flag |", "|---|---|---|---|---|---|---|"]
    for e, b in a["experiments"].items():
        L += [f"## {e}", "", f"State: {b['state'].get('status')}." + (f" Status: {b['status']}." if b.get("status") else ""), ""]
        for k in ("note", "scope_note", "family"):
            if b.get(k):
                L += [str(b[k]), ""]
        if b.get("tally"):
            L += [f"Tally (not independent replications): {tally_line(b.get('checks', []), events, b['tally'])}.", ""]
        if b.get("checks"):
            L += [*head, *[_row(c, events) for c in b["checks"]], ""]
        if e == "E001" and b.get("es"):
            L += ["es (reported only, no confirmatory weight):", "", *head, _row(b["es"], events), ""]
        if b.get("h4f_y_view"):
            y = b["h4f_y_view"]
            L += [f"H4-F y_view (secondary, shown separately): row label **{y['row_label']}**. {y['note']}" + (" Flag: pending review." if y["pending_review_flag"] else ""), ""]
            for c, r in y["cells"].items():
                flag = flag_text(r.get("id", c), events)
                if "rho_A" not in r:
                    L += [f"- {c}: **{r['label']}** ({r.get('reason', '')}). {flag}"]
                    continue
                why = f" Not confirmable because {r['reason']}." if r.get("reason") else ""
                L += [f"- {c}: **{label_text(r)}**.{why} ρ_A {_n(r['rho_A'], '.4f')} (discovery {_n(r.get('discovery_rho_A'), '.4f')}, {r.get('discovery_label', '')}), projection {r['projection']['rho_a']}, difference {_n(r['rho_A_minus_projection'], '.4f')}; "
                      f"L {_n(r['L']['mean'], '.3f')} pp; A {_n(r['A']['mean'], '.4f')} pp; leave-one-out ρ_A {r['leave_one_out_rho_A_range']}. Status: {r['status']}. {flag}"]
                for k in ("A", "L"):
                    v = r[k]
                    L += [f"  {k}: {v['defined']} defined, {v['positive']} +, {v['negative']} −; t-interval (descriptive, not used) {[_n(x) for x in v['t_interval_95_descriptive_not_used']]}."]
                L += ["  Sessions: " + "; ".join(f"{d}: A {_n(x['A'])}, L {_n(x['L'])}, A/L {_n(x['A_over_L'])}" for d, x in r["per_session"].items()) + "."]
                if r.get("mean_A_below_0"):
                    m = r["mean_A_below_0"]
                    L += [f"  Mean A below 0: {_n(m['mean_A'], '.4f')} pp, A/L {_n(m['A_over_L'], '.4f')}, {m['sessions_A_negative']} sessions negative "
                          f"(discovery {_n(m['discovery_mean_A'], '.4f')} pp, {m['discovery_sessions_negative']} sessions). " + (m["sentence"] or "")]
            L += [""]
        if b.get("policies_vip0_descriptive"):
            p0 = b["policies_vip0_descriptive"]
            L += [f"Seven policies and no-trade at VIP0 (descriptive; no label or rule). {p0['note']}", "",
                  "| Policy | Net per hour | Discovery net per hour | vs no-trade | Gross per hour | Maker fees per hour (mechanical) | Taker fees per hour | Turnover per hour | Sessions with trades |",
                  "|---|---|---|---|---|---|---|---|---|"]
            for p, r in p0["policies"].items():
                L += [f"| {p} | {_n(r['mean_net_per_hour'], '.2f')} | {_n(r.get('discovery_mean_net_per_hour'), '.2f')} | {_n(r['difference_from_no_trade'], '.2f')} | {_n(r['gross_per_hour'], '.2f')} | {_n(r['maker_fees_per_hour_mechanical'], '.2f')} | {_n(r['taker_fees_per_hour'], '.2f')} | {_n(r['turnover_per_hour'], '.0f')} | {r['sessions_with_trades']} |"]
            L += [""]
        L += side_by_side(b["reported_only"], b.get("discovery_side")) + [""]
        for k, v in (b.get("not_computed_on_test") or {}).items():
            L += [f"Not computed on test: {k} ({v})."]
        L += [""]
    return "\n".join(L) + "\n"
