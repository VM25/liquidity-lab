"""E003 pre-registered analysis (docs/experiments/E003.md section 8; configs/e003_v1.toml [analysis]).

Unit: evaluation session (s6..s15). Mean of session values, session-bootstrap percentile intervals (each contrast has its
own deterministic random stream, so results do not depend on evaluation order), paired differences on the sessions where
both sides are defined, and the count of sessions with a positive value. A contrast enters a decision only if it is
defined in at least ``min_defined_sessions`` sessions.

Usage (after ``python -m lpx.research.e003``):
    uv run python -m lpx.research.e003_analysis
"""

from __future__ import annotations

import json
import tomllib
import zlib

import numpy as np
import polars as pl


def ckey(lv: float) -> str:
    return f"ci{round(lv, 2):g}"


def boot(x: np.ndarray, n: int, seed: int, name: str, levels: tuple[float, ...]) -> dict:
    """Mean and percentile intervals (one per level) of a session sample; NaN entries are undefined sessions."""
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    out = {"defined": int(x.size), "positive": int((x > 0).sum()), "mean": float(x.mean()) if x.size else None}
    if x.size < 2:
        for lv in levels:
            out[ckey(lv)] = [None, None]
        return out
    rng = np.random.default_rng([seed, zlib.crc32(name.encode())])
    m = x[rng.integers(0, x.size, size=(n, x.size))].mean(axis=1)
    for lv in levels:
        a = (1 - lv / 100) / 2
        out[ckey(lv)] = [float(np.quantile(m, a)), float(np.quantile(m, 1 - a))]
    return out


class Ctx:
    def __init__(self, net: pl.DataFrame, fc: pl.DataFrame, cfg: dict):
        self.net, self.fc, self.cfg = net, fc, cfg
        a = cfg["analysis"]
        self.n, self.seed, self.k = a["bootstrap_resamples"], a["seed"], a["min_defined_sessions"]
        self.lv = (95.0, 100 * (1 - a["alpha"] / a["primary_family_size"]))   # exact level; keys are rounded
        self.days = sorted(net["day"].unique().to_list())
        ps = a["primary_scenario"]
        self.prim = (ps["fill_model"], ps["latency"])

    def series(self, policy: str, col: str, fee: str, scen: tuple[str, str] | None = None) -> np.ndarray:
        """Session values (sorted by day; NaN if undefined) of one policy under a fee schedule. Fee-aware policies use
        their own fee rule; the others the overlay of that schedule."""
        model, lat = scen or self.prim
        f = (pl.col("policy") == policy) & (pl.col("fee_schedule") == fee)
        if policy != "NT":
            f = f & (pl.col("fill_model") == model) & (pl.col("latency") == lat)
        g = self.net.filter(f).sort("day")
        if g["day"].to_list() != self.days:
            raise ValueError(f"{policy} {fee} {model} {lat}: sessions missing or duplicated")
        return g[col].cast(pl.Float64).fill_null(float("nan")).to_numpy()

    def b(self, x: np.ndarray, name: str, levels=None) -> dict:
        r = boot(x, self.n, self.seed, name, levels or self.lv)
        r["eligible"] = r["defined"] >= self.k
        return r


def side(ci: list, margin: float = 0.0) -> str:
    lo, hi = ci
    if lo is None:
        return "undefined"
    return "above" if lo > margin else "below" if hi < margin else "straddles"


def h1(c: Ctx) -> dict:
    a = c.cfg["analysis"]
    fc = c.fc.filter((pl.col("horizon_s") == c.cfg["features"]["primary_horizon_s"])).sort("day")
    r2 = {}
    for m in ("M1", "M2"):
        g = fc.filter(pl.col("model") == m)
        if g["day"].to_list() != c.days:
            raise ValueError(f"forecast table for {m}: sessions differ from the policy table")
        r2[m] = g["r2_os"].to_numpy()
    skill = c.b(r2["M2"], "H1-F r2 M2")
    out = {"H1-F": skill, "skill_holds": skill["eligible"] and side(skill["ci95"]) == "above"}
    vip0 = c.cfg["fees"]["default"]
    D = c.series("P3_M2", "gross_bp_per_notional", vip0) - c.series("P3_negM2", "gross_bp_per_notional", vip0)
    d = c.b(D, "H1-T D")
    delta = a["h1_margin_bp"]
    activity = {p: float(np.nanmean(c.series(p, "gate_active_share", vip0))) for p in ("P3_M2", "P3_negM2")}
    active = min(activity.values()) >= a["h1_min_gate_activity"]

    def label(ci, holds):
        if not holds:
            return "not testable: no forecast skill"
        if not active:
            return "not testable: rule inactive"
        if not d["eligible"] or ci[0] is None:
            return "not testable: too few defined sessions"
        return "supported" if ci[1] < delta else "refuted" if ci[0] > delta else "inconclusive"

    out["H1-T"] = {**d, "margin_bp": delta, "gate_activity": activity, "label": label(d["ci95"], out["skill_holds"])}
    lv2 = ckey(c.lv[1])
    skill_b = side(skill[lv2]) == "above" and skill["eligible"]
    out["H1-T"]["label_bonferroni"] = label(d[lv2], skill_b)
    out["H1-T"]["robust_to_multiplicity"] = out["H1-T"]["label_bonferroni"] == out["H1-T"]["label"]
    out["H1-F"]["robust_to_multiplicity"] = skill_b == out["skill_holds"]
    out["reported"] = {
        "D_net_per_hour": c.b(c.series("P3_M2", "net_per_hour", vip0) - c.series("P3_negM2", "net_per_hour", vip0), "D nph"),
        "P3_M2_minus_P0_gross_bp": c.b(c.series("P3_M2", "gross_bp_per_notional", vip0)
                                       - c.series("P0", "gross_bp_per_notional", vip0), "P3-P0 gbp"),
        "P3_M2_minus_P0_net_per_hour": c.b(c.series("P3_M2", "net_per_hour", vip0) - c.series("P0", "net_per_hour", vip0),
                                           "P3-P0 nph"),
        "ranking_r2_M2_minus_M1": c.b(r2["M2"] - r2["M1"], "rank r2"),
        "ranking_P3_M2_minus_P3_M1_gross_bp": c.b(c.series("P3_M2", "gross_bp_per_notional", vip0)
                                                  - c.series("P3_M1", "gross_bp_per_notional", vip0), "rank gbp"),
        "P3_M2_net_per_hour_vip0": c.b(c.series("P3_M2", "net_per_hour", vip0), "P3 nph"),
    }
    return out


def h3(c: Ctx) -> dict:
    a = c.cfg["analysis"]
    fee = a["h3_fee_schedule"]
    s = lambda p, col, f=fee: c.series(p, col, f)
    es, dd = c.b(s("P4", "inc_es") - s("P3F", "inc_es"), "H3 es"), c.b(s("P4", "max_drawdown") - s("P3F", "max_drawdown"), "H3 dd")
    nph = c.b(s("P4", "net_per_hour") - s("P3F", "net_per_hour"), "H3 nph")
    base = c.b(s("P3F", "net_per_hour"), "H3 base")
    dh = None if base["mean"] is None else a["h3_noninferiority_share"] * abs(base["mean"])

    def label(lv):
        k = ckey(lv)
        if not (es["eligible"] and dd["eligible"] and nph["eligible"]) or dh is None:
            return "not testable: too few defined sessions"
        if nph[k][1] < -dh or es[k][0] > 0:
            return "refuted"
        if es[k][1] < 0 and dd[k][1] < 0 and nph[k][0] > -dh:
            return "supported"
        return "inconclusive"

    t4, t3 = s("P4", "turnover_per_hour"), s("P3F", "turnover_per_hour")
    ratio = float(np.nanmean(t4) / np.nanmean(t3)) if np.nanmean(t3) > 0 else None
    out = {"fee_schedule": fee, "es_diff": es, "drawdown_diff": dd, "net_per_hour_diff": nph, "P3F_net_per_hour": base,
           "noninferiority_margin": dh, "turnover_ratio_P4_over_P3F": ratio,
           "label": label(c.lv[0]), "label_bonferroni": label(c.lv[1]),
           "partly_mechanical": ratio is not None and ratio < a["h3_mechanical_turnover_share"],
           "normalised": {"es_per_k_turnover_diff": c.b(s("P4", "es_per_k_turnover") - s("P3F", "es_per_k_turnover"), "H3 esn"),
                          "inventory_per_k_turnover_diff": c.b(s("P4", "inventory_per_k_turnover")
                                                               - s("P3F", "inventory_per_k_turnover"), "H3 invn")}}
    out["robust_to_multiplicity"] = out["label"] == out["label_bonferroni"]
    # descriptive: the same contrast under the other schedules, with the abstention label
    ref = np.nanmean(c.series("P3_M2", "filled_notional", c.cfg["fees"]["default"]))
    out["other_schedules"] = {}
    for f in (k for k in c.cfg["fees"] if k not in ("default", fee)):
        share = {p: float(np.nanmean(c.series(p, "filled_notional", f)) / ref) if ref > 0 else None for p in ("P3F", "P4")}
        out["other_schedules"][f] = {
            "notional_share_of_P3_M2": share,
            "not_testable_abstention": any(v is not None and v < a["abstention_share"] for v in share.values()),
            "es_diff": c.b(c.series("P4", "inc_es", f) - c.series("P3F", "inc_es", f), f"H3 es {f}"),
            "drawdown_diff": c.b(c.series("P4", "max_drawdown", f) - c.series("P3F", "max_drawdown", f), f"H3 dd {f}"),
            "net_per_hour_diff": c.b(c.series("P4", "net_per_hour", f) - c.series("P3F", "net_per_hour", f), f"H3 nph {f}")}
    return out


def participation(c: Ctx) -> dict:
    a = c.cfg["analysis"]
    pols = a["participation_policies"]
    lv = 100 * (1 - a["alpha"] / len(pols))
    vip0 = c.cfg["fees"]["default"]
    rows = {}
    for p in pols:
        r = c.b(c.series(p, "net_per_hour", vip0), f"part {p}", (95.0, lv))
        r["preferred_to_no_trade"] = r["eligible"] and side(r[ckey(lv)]) == "above"
        r["turnover_per_hour"] = float(np.nanmean(c.series(p, "turnover_per_hour", vip0)))
        r["quote_presence_both"] = float(np.nanmean(c.series(p, "quote_presence_both", vip0)))
        rows[p] = r
    return {"fee_schedule": vip0, "bonferroni_level": round(lv, 2), "policies": rows,
            "abstention_rational": not any(r["preferred_to_no_trade"] for r in rows.values())}


DESCRIPTIVE = ["gate_active_share", "vol_closed_share", "net_per_hour", "gross_per_hour", "net_bp_per_notional", "gross_bp_per_notional", "turnover_per_hour",
               "quote_presence_bid", "quote_presence_ask", "quote_presence_both", "fill_rate", "orders_per_fill",
               "paced_time_share", "paced_spells", "max_abs_inventory", "tw_abs_inventory_avg", "max_drawdown", "inc_std",
               "inc_es", "inc_worst", "own_edge_bp", "own_markout_1s_bp", "own_markout_5s_bp", "own_markout_30s_bp",
               "liquidation_shortfall", "net_per_hour_over_inc_std"]


def descriptive(net: pl.DataFrame, fc: pl.DataFrame, rc: dict) -> dict:
    cols = [c for c in DESCRIPTIVE if c in net.columns]
    agg = [pl.col(c).cast(pl.Float64).mean().alias(c) for c in cols] + [pl.len().alias("sessions")]
    keys = ["policy", "fill_model", "latency", "fee_schedule"]
    split = net.with_columns(pl.when(pl.col("day").is_in(rc["splits"]["validation"])).then(pl.lit("validation"))
                             .otherwise(pl.lit("train-late")).alias("period"))
    fcs = fc.with_columns(pl.when(pl.col("day").is_in(rc["splits"]["validation"])).then(pl.lit("validation"))
                          .otherwise(pl.lit("train-late")).alias("period"))
    fagg = [pl.col(c).mean().alias(c) for c in ("r2_os", "ic", "hit_rate", "mean_abs_forecast", "share_abs_forecast_ge_half_tick",
                                                 "share_abs_forecast_ge_half_spread")
            if c in fc.columns]
    return {"scenarios": net.group_by(keys).agg(agg).sort(keys).to_dicts(),
            "scenarios_by_period": split.group_by(keys + ["period"]).agg(agg).sort(keys + ["period"]).to_dicts(),
            "forecasts": fc.group_by("model", "horizon_s").agg(fagg).sort("model", "horizon_s").to_dicts(),
            "forecasts_by_period": fcs.group_by("model", "horizon_s", "period").agg(fagg).sort("model", "horizon_s", "period").to_dicts()}


def versus_e002(c: Ctx, e002_net: pl.DataFrame | None) -> dict | None:
    """Descriptive: E003 P0 (paced, warm-up) vs the frozen E002 P0 on the same sessions, primary scenario, VIP0."""
    if e002_net is None:
        return None
    vip0 = c.cfg["fees"]["default"]
    g = e002_net.filter((pl.col("policy") == "P0") & (pl.col("fill_model") == c.prim[0]) & (pl.col("latency") == c.prim[1])
                        & (pl.col("fee_schedule") == vip0) & pl.col("day").is_in(c.days)).sort("day")
    if g["day"].to_list() != c.days:
        return None
    out = {}
    for col in ("net_per_hour", "net_bp_per_notional"):
        e3 = c.series("P0", col, vip0)
        e2 = g[col].cast(pl.Float64).fill_null(float("nan")).to_numpy()
        out[col] = {"e003_mean": float(np.nanmean(e3)), "e002_mean": float(np.nanmean(e2)),
                    "difference": c.b(e3 - e2, f"vs e002 {col}")}
    return out


def analyse(net: pl.DataFrame, fc: pl.DataFrame, cfg: dict, rc: dict, e002_net: pl.DataFrame | None = None) -> dict:
    net = net.sort(["policy", "fill_model", "latency", "fee_schedule", "day"])
    c = Ctx(net, fc, cfg)
    return {"evaluation_sessions": c.days, "primary_scenario": list(c.prim), "levels": [round(x, 2) for x in c.lv],
            "H1": h1(c), "H3": h3(c), "participation": participation(c), "descriptive": descriptive(net, fc, rc),
            "P0_versus_E002": versus_e002(c, e002_net)}


def _no_nan(x):
    if isinstance(x, float) and x != x:
        return None
    if isinstance(x, dict):
        return {k: _no_nan(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_no_nan(v) for v in x]
    return x


def run() -> dict:
    from lpx.data.acquire import ROOT
    from lpx.provenance import code_fingerprint, provenance, require_clean, sha256_file
    from lpx.research.e003 import CONFIG, OUT, SPEC

    require_clean()
    cfg = tomllib.loads(CONFIG.read_text())
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    meta = json.loads((OUT / "e003_meta.json").read_text())
    pv = meta["provenance"]
    if set(meta["sessions"]) & set(rc["splits"]["test"]):
        raise PermissionError("the E003 outputs contain test sessions")
    if pv["git_dirty"]:
        raise RuntimeError("the E003 run was made from a dirty tree and cannot be cited")
    if pv["configs"]["configs/e003_v1.toml"] != sha256_file(CONFIG):
        raise RuntimeError("configs/e003_v1.toml changed after the run")
    if pv["configs"]["configs/research_v1.toml"] != sha256_file(ROOT / "configs" / "research_v1.toml"):
        raise RuntimeError("configs/research_v1.toml changed after the run")
    if pv["spec_sha256"] != sha256_file(SPEC):
        raise RuntimeError("docs/experiments/E003.md changed after the run")
    if pv["code_fingerprint"] != code_fingerprint():
        raise RuntimeError("code changed after the run")
    for f in ("e003_net_by_session.csv", "e003_forecast_by_session.csv"):
        if meta["outputs_sha256"][f] != sha256_file(OUT / f):
            raise RuntimeError(f"{f} differs from the one the run wrote")
    net = pl.read_csv(OUT / "e003_net_by_session.csv", infer_schema_length=None)
    fc = pl.read_csv(OUT / "e003_forecast_by_session.csv")
    if set(net["day"].unique()) != set(meta["evaluation_sessions"]) or set(fc["day"].unique()) != set(meta["evaluation_sessions"]):
        raise RuntimeError("tables and run metadata name different sessions")
    e2 = ROOT / "results" / "e002"
    e2meta = json.loads((e2 / "e002_meta.json").read_text())
    if e2meta["outputs_sha256"]["e002_net_by_session.csv"] != sha256_file(e2 / "e002_net_by_session.csv"):
        raise RuntimeError("frozen E002 net table changed")
    res = analyse(net, fc, cfg, rc, pl.read_csv(e2 / "e002_net_by_session.csv"))
    res["provenance"] = {**provenance(["configs/e003_v1.toml"]), "run_git_commit": pv["git_commit"],
                         "net_table_sha256": sha256_file(OUT / "e003_net_by_session.csv")}
    (OUT / "e003_analysis.json").write_text(json.dumps(_no_nan(res), indent=1, allow_nan=False))
    return res


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: r[k] for k in ("H1", "H3", "participation")}, indent=1, default=str)[:6000])
