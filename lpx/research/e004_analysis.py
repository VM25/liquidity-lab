"""E004 pre-registered analysis (docs/experiments/E004.md section 6; configs/e004_v1.toml [analysis]).

Unit: evaluation session (s6..s15). Session-bootstrap percentile intervals (10,000 draws, one deterministic stream per
contrast; E003's ``boot``), paired t-intervals as a sensitivity, sign counts of the defined sessions. Undefined sessions
are excluded from the bootstrap and from the sign counts; a contrast enters a decision only if it is defined in at least
``min_defined_sessions`` sessions. Gate shares (withdrawn share, overlap) are each session's value pooled over replicates;
a decision's gate uses their mean over the evaluation sessions (as E003's activity gate).

Usage (after ``python -m lpx.research.e004``):
    uv run python -m lpx.research.e004_analysis
"""

from __future__ import annotations

import json
import tomllib
import zlib

import numpy as np
import polars as pl
from scipy import stats

from lpx.data.acquire import ROOT
from lpx.research.e003_analysis import boot, ckey

OUT = ROOT / "results" / "e004"
CONFIG = ROOT / "configs" / "e004_v1.toml"
SUPPORTED, IMMATERIAL, INCONCLUSIVE, NOT_TESTABLE = ("stale-fill selection supported", "immaterial selection (< delta)",
                                                     "inconclusive", "not testable")


def t_interval(x: np.ndarray, level: float) -> list:
    x = x[~np.isnan(x)]
    if x.size < 2:
        return [None, None]
    h = stats.t.ppf(1 - (1 - level / 100) / 2, x.size - 1) * x.std(ddof=1) / np.sqrt(x.size)
    return [float(x.mean() - h), float(x.mean() + h)]


def h4w_label(x: np.ndarray, ci: list, a: dict) -> tuple[str, list[str]]:
    """Label of D_W = q(W_P) - q(W_U) from its session values (NaN = undefined) and an interval; gates are applied by
    the caller. Returns (label, notes)."""
    x = x[~np.isnan(x)]
    delta, k = a["h4w_margin_bp"], a["h4w_min_sign_count"]
    if x.size < a["min_defined_sessions"]:
        return NOT_TESTABLE, [f"defined in {x.size} sessions"]
    lo, hi = ci
    if lo > delta and (x > 0).sum() >= k:
        return SUPPORTED, []
    if hi < delta and (x < delta).sum() >= k:
        return IMMATERIAL, ["interval excludes 0" if (lo > 0 or hi < 0) else "interval includes 0"]
    return INCONCLUSIVE, ["underpowered"] if hi - lo > a["h4w_underpowered_width"] * delta else []


def h4w(w: pl.DataFrame, base: str, cfg: dict) -> dict:
    a = cfg["analysis"]
    ps = a["primary_scenario"]
    g = w.filter((pl.col("cell") == a["primary_cell"]) & (pl.col("base") == base) & (pl.col("fill_model") == ps["fill_model"])
                 & (pl.col("latency") == ps["latency"])).sort("day")
    if g["day"].n_unique() != g.height:
        raise ValueError(f"{base}: duplicated sessions")
    n_min = a["h4w_min_orders_per_window"]

    def series(d_col: str, u_col: str, p_col: str) -> np.ndarray:
        ok = (g[u_col] >= n_min) & (g[p_col] >= n_min) & g[d_col].is_not_null()
        return np.where(ok.to_numpy(), g[d_col].cast(pl.Float64).fill_null(float("nan")).to_numpy(), np.nan)

    x = series("D_W_bp", "orders_U", "orders_P")
    lv = (95.0, 100 * (1 - a["alpha"] / a["primary_family_size"]))
    name = f"H4-W[{base}]"
    b = boot(x, a["bootstrap_resamples"], cfg["seeds"]["bootstrap_seed"], name, lv)
    wd, ov = float(g["withdrawn_share"].mean()), float(g["overlap_share_of_wp"].cast(pl.Float64).mean())
    gates = {"withdrawn_share_mean": wd, "withdrawn_share_min": float(g["withdrawn_share"].min()),
             "overlap_share_mean": ov, "overlap_share_max": float(g["overlap_share_of_wp"].cast(pl.Float64).max()),
             "defined_sessions": int((~np.isnan(x)).sum())}
    gate_fail = []
    if wd < a["h4w_min_withdrawn_share"]:
        gate_fail.append("rule inactive (withdrawn share < 0.5%)")
    if gates["defined_sessions"] < a["min_defined_sessions"]:
        gate_fail.append("fewer than 8 defined sessions")
    if ov > a["h4w_overlap_not_testable"]:
        gate_fail.append("W_P overlaps W_U in more than 10% of W_P time")

    def label(xs: np.ndarray, ci: list) -> tuple[str, list[str]]:
        return (NOT_TESTABLE, list(gate_fail)) if gate_fail else h4w_label(xs, ci, a)

    lab, notes = label(x, b[ckey(95.0)])
    lab_b, _ = label(x, b[ckey(lv[1])])
    if lab_b != lab:
        notes.append("not robust to multiplicity")
    xs = series("D_W_stall_bp", "orders_U_stall", "orders_P_stall")
    # same stream as the main contrast (common random numbers): identical data cannot give a different label
    bs = boot(xs, a["bootstrap_resamples"], cfg["seeds"]["bootstrap_seed"], name, (95.0,))
    lab_s, _ = label(xs, bs[ckey(95.0)])
    if a["h4w_natural_staleness_qualifier"] and lab_s != lab:
        notes.append("sensitive to natural staleness")
    return {"label": lab, "notes": notes, "status": "modeled historical replay under stress test", "D_W_bp": b,
            "t_interval_95": t_interval(x, 95.0),
            "below_delta": int((x[~np.isnan(x)] < a["h4w_margin_bp"]).sum()), "gates": gates,
            "bonferroni_label": lab_b, "stall_only": {"label": lab_s, "D_W_bp": bs},
            "sessions": dict(zip(g["day"].to_list(), [None if np.isnan(v) else float(v) for v in x])),
            "q_U_bp_mean": float(g["q_U_bp"].cast(pl.Float64).mean()), "q_P_bp_mean": float(g["q_P_bp"].cast(pl.Float64).mean()),
            "shares": {c: float(g[c].cast(pl.Float64).mean()) for c in ("wu_time_share_nostall", "wu_fill_share_nostall",
                                                                         "wp_time_share_install", "wp_fill_share_install")},
            "orders_U_min": int(g["orders_U"].min()), "orders_P_min": int(g["orders_P"].min()),
            "placebo_redraws": int(g["placebo_redraws"].sum()), "episodes_excluded": int(g["episodes_excluded"].sum())}


def r2(fc: pl.DataFrame, cell: str, target: str, model: str, days: list[str]) -> np.ndarray:
    g = fc.filter((pl.col("cell") == cell) & (pl.col("target") == target) & (pl.col("model") == model)).sort("day")
    if g["day"].to_list() != days:
        raise ValueError(f"{cell} {target} {model}: sessions missing or duplicated")
    return g["r2_os_pp"].cast(pl.Float64).fill_null(float("nan")).to_numpy()


def ratio_boot(nums: dict[str, np.ndarray], den: np.ndarray, n: int, seed: int, name: str) -> dict:
    """Ratios of session sums sum(num)/sum(den), bootstrapped jointly: one resample of the sessions defined for all of
    them drives every ratio (numerators and the denominator move together)."""
    ok = ~np.isnan(den)
    for v in nums.values():
        ok &= ~np.isnan(v)
    den = den[ok]
    out = {k: {"value": float(v[ok].sum() / den.sum()) if den.sum() else None, "ci95": [None, None]} for k, v in nums.items()}
    if den.size < 2:
        return out
    rng = np.random.default_rng([seed, zlib.crc32(name.encode())])
    k = rng.integers(0, den.size, size=(n, den.size))
    d = den[k].sum(1)
    for key, v in nums.items():
        r = np.where(d != 0, v[ok][k].sum(1) / np.where(d != 0, d, 1), np.nan)
        r = r[~np.isnan(r)]
        out[key]["ci95"] = [float(np.quantile(r, 0.025)), float(np.quantile(r, 0.975))]
        out[key]["sessions"] = int(den.size)
    return out


def h4f(fc: pl.DataFrame, cell: str, target: str, cfg: dict, days: list[str]) -> dict:
    a, s = cfg["analysis"], cfg["seeds"]
    R = {m: r2(fc, cell, target, m, days) for m in ("REF", "NV", "UA-lambda", "PL-lambda", "RF-lambda")}
    L, A = R["REF"] - R["NV"], R["UA-lambda"] - R["NV"]
    B, C = R["UA-lambda"] - R["PL-lambda"], R["RF-lambda"] - R["NV"]
    n = a["bootstrap_resamples"]
    nm = f"H4-F[{cell},{target}]"
    out = {c: {**boot(v, n, s["bootstrap_seed"], f"{nm}:{c}", (95.0,)), "t_interval_95": t_interval(v, 95.0)}
           for c, v in (("L", L), ("A", A), ("B", B), ("C", C))}
    rr = ratio_boot({"rho_A": A, "rho_B": B}, L, n, s["bootstrap_seed"], nm + ":rho")
    ra, rb = rr["rho_A"], rr["rho_B"]
    out.update(rho_A=ra, rho_B=rb)
    Lb = out["L"]
    lci = Lb[ckey(95.0)]
    notes = []
    if Lb["defined"] < a["min_defined_sessions"]:
        lab = NOT_TESTABLE
    elif Lb["mean"] < a["h4f_immaterial_pp"] or lci[0] is None or (lci[0] <= 0 <= lci[1]):
        lab = NOT_TESTABLE
    elif ra["ci95"][0] > a["h4f_rho_a"] and rb["ci95"][0] > a["h4f_rho_b"]:
        lab = "supported"
    elif ra["ci95"][0] > a["h4f_rho_a"] and rb["ci95"][1] < a["h4f_rho_b"]:
        lab = "recalibration only"
    elif ra["ci95"][1] < a["h4f_rho_a"]:
        lab = "not supported"
        if out["A"][ckey(95.0)][1] is not None and out["A"][ckey(95.0)][1] < 0:
            notes.append("UA harmful")
    else:
        lab = INCONCLUSIVE
    # pre-registered projections exist for D1-S, and D3 is projected to match D1-S (E004.md section 0); none elsewhere
    proj = a["h4f_projection"].get(target, {}) if cell in ("D1_S", "D3") else {}
    if cell in ("D1_S1", "D1_S3"):
        lab, notes = "descriptive (no label)", []
    out.update(label=lab, notes=notes, projection=proj or None, status="stress test",
               rho_A_minus_projection=(ra["value"] - proj["rho_a"]) if ra["value"] is not None and "rho_a" in proj else None,
               sessions={m: dict(zip(days, map(float, v))) for m, v in R.items()})
    return out


def h40(fc: pl.DataFrame, cfg: dict, days: list[str]) -> dict:
    a = cfg["analysis"]
    x = r2(fc, "D0", "y_k", "UA-lambda[D1_S]", days) - r2(fc, "D0", "y_k", "REF", days)
    b = boot(x, a["bootstrap_resamples"], cfg["seeds"]["bootstrap_seed"], "H4-0", (95.0,))
    lo, hi = b[ckey(95.0)]
    m = -a["h40_margin_pp"]
    if b["defined"] < a["min_defined_sessions"]:
        lab = NOT_TESTABLE
    else:
        lab = "harmless" if lo > m else "costly" if hi < m else INCONCLUSIVE
    return {"label": lab, "difference_pp": b, "t_interval_95": t_interval(x, 95.0),
            "status": "observed (model trained under stress test)"}


def descriptive_policy(gross: pl.DataFrame, net: pl.DataFrame, w: pl.DataFrame, cfg: dict, cell: str) -> dict:
    """Realised U vs P (and vs N) per base, primary scenario, pooled over replicates within a session. No labels."""
    a = cfg["analysis"]
    ps = a["primary_scenario"]
    n, seed = a["bootstrap_resamples"], cfg["seeds"]["bootstrap_seed"]
    band = cfg["policies"]["participation_ratio_band"]
    out = {}
    for base in ("P0", "P3_M2"):
        f = ((pl.col("cell") == cell) & (pl.col("base") == base) & (pl.col("fill_model") == ps["fill_model"])
             & (pl.col("latency") == ps["latency"]))
        g = gross.filter(f).group_by("day", "variant").agg(
            pl.col("gross_marked").sum(), pl.col("liquidation_slippage").sum(), pl.col("filled_notional").sum(),
            pl.col("valid_hours").sum(), pl.col("pi5_usdt").sum(), pl.col("pi5_notional").sum(),
            pl.col("quote_both_s").sum(), pl.col("fills").sum()).sort("day")
        nt = net.filter(f & pl.col("fee_schedule").is_in(["vip0", "lp_tier4"])).group_by("day", "variant", "fee_schedule").agg(
            pl.col("net").sum(), pl.col("valid_hours").sum())
        v = {}
        for var in ("N", "U", "P"):
            h = g.filter(pl.col("variant") == var).sort("day")
            v[var] = {"days": h["day"].to_list(),
                      "gross_bp": ((h["gross_marked"] - h["liquidation_slippage"]) / h["filled_notional"] * 1e4).to_numpy(),
                      "pi5_bp": (h["pi5_usdt"] / h["pi5_notional"] * 1e4).to_numpy(),
                      "notional": h["filled_notional"].to_numpy(), "presence": h["quote_both_s"].to_numpy(),
                      "fills": h["fills"].to_numpy().astype(float)}
            for fee in ("vip0", "lp_tier4"):
                k = nt.filter((pl.col("variant") == var) & (pl.col("fee_schedule") == fee)).sort("day")
                v[var][f"net_per_hour_{fee}"] = (k["net"] / k["valid_hours"]).to_numpy()
        ww = w.filter((pl.col("cell") == cell) & (pl.col("base") == base) & (pl.col("fill_model") == ps["fill_model"])
                      & (pl.col("latency") == ps["latency"])).sort("day")
        if ww["day"].to_list() != v["N"]["days"] or any(v[k]["days"] != v["N"]["days"] for k in v):
            raise ValueError(f"{cell} {base}: sessions missing or misaligned between policy and window tables")
        s_share = (ww["notional_U"] / ww["n_notional_defined"]).to_numpy()
        res = {}
        for x, y in (("U", "P"), ("U", "N"), ("P", "N")):
            db = v[x]["gross_bp"] - v[y]["gross_bp"]
            r = {"delta_gross_bp": boot(db, n, seed, f"{cell}:{base}:{x}-{y}:gross", (95.0,)),
                 "delta_pi5_bp": boot(v[x]["pi5_bp"] - v[y]["pi5_bp"], n, seed, f"{cell}:{base}:{x}-{y}:pi5", (95.0,))}
            for fee in ("vip0", "lp_tier4"):
                r[f"delta_net_per_hour_{fee}"] = boot(v[x][f"net_per_hour_{fee}"] - v[y][f"net_per_hour_{fee}"], n, seed,
                                                      f"{cell}:{base}:{x}-{y}:net:{fee}", (95.0,))
            maker = cfg["_fees"]["vip0"]["maker"]
            hours = g.filter(pl.col("variant") == x).sort("day")["valid_hours"].to_numpy()
            r["fee_saving_per_hour_vip0_mechanical"] = boot(-maker * (v[x]["notional"] - v[y]["notional"]) / hours, n, seed,
                                                            f"{cell}:{base}:{x}-{y}:feesave", (95.0,))
            ratios = {k: float(np.mean(v[x][k] / v[y][k])) for k in ("notional", "presence", "fills")}
            r["participation_ratios"] = ratios
            r["participation_differs"] = any(not band[0] <= q <= band[1] for q in ratios.values())
            if (x, y) == ("U", "P"):
                r["delta_gross_bp_over_s"] = boot(db / s_share, n, seed, f"{cell}:{base}:U-P:scaled", (95.0,))
                r["n_notional_share_in_wu"] = float(np.mean(s_share))
                # Pi5 per valid hour of N's fills in W_U^x / W_P^x: the loss a withdrawal there removes (fee-free)
                hrs = ww["n_valid_hours"].to_numpy()
                r["avoided_loss_rate_usdt_per_hour"] = {
                    "W_U": boot(-ww["pi5_U_usdt"].to_numpy() / hrs, n, seed, f"{cell}:{base}:avoid:U", (95.0,)),
                    "W_P": boot(-ww["pi5_P_usdt"].to_numpy() / hrs, n, seed, f"{cell}:{base}:avoid:P", (95.0,))}
            res[f"{x}-{y}"] = r
        out[base] = res
    return out


def p3_forecast_variants(gross: pl.DataFrame, net: pl.DataFrame, cfg: dict) -> dict:
    """D1-S, P3[M2] on UA-lambda vs PL-lambda rescaled NV forecasts (N variant): participation-changing; descriptive."""
    a = cfg["analysis"]
    n, seed = a["bootstrap_resamples"], cfg["seeds"]["bootstrap_seed"]
    f = (pl.col("cell") == "D1_S") & (pl.col("base") == "P3_M2")
    g = gross.filter(f).group_by("day", "variant").agg(
        pl.col("gross_marked").sum(), pl.col("liquidation_slippage").sum(), pl.col("filled_notional").sum(),
        pl.col("valid_hours").sum(), pl.col("pi5_usdt").sum(), pl.col("pi5_notional").sum(), pl.col("quote_both_s").sum())
    nt = net.filter(f & (pl.col("fee_schedule") == "vip0")).group_by("day", "variant").agg(pl.col("net").sum(),
                                                                                             pl.col("valid_hours").sum())
    v = {}
    for var in ("N[UA-lambda]", "N[PL-lambda]", "N"):
        h = g.filter(pl.col("variant") == var).sort("day")
        k = nt.filter(pl.col("variant") == var).sort("day")
        v[var] = {"gross_bp": ((h["gross_marked"] - h["liquidation_slippage"]) / h["filled_notional"] * 1e4).to_numpy(),
                  "pi5_bp": (h["pi5_usdt"] / h["pi5_notional"] * 1e4).to_numpy(), "notional": h["filled_notional"].to_numpy(),
                  "presence": h["quote_both_s"].to_numpy(), "net_per_hour_vip0": (k["net"] / k["valid_hours"]).to_numpy()}
    out = {"status": "modeled historical replay under stress test; participation-changing; descriptive"}
    for x, y in (("N[UA-lambda]", "N[PL-lambda]"), ("N[UA-lambda]", "N")):
        out[f"{x} - {y}"] = {k: boot(v[x][k] - v[y][k], n, seed, f"p3fc:{x}-{y}:{k}", (95.0,))
                             for k in ("gross_bp", "pi5_bp", "net_per_hour_vip0")}
        out[f"{x} - {y}"]["participation_ratios"] = {k: float(np.mean(v[x][k] / v[y][k])) for k in ("notional", "presence")}
    return out


def window_descriptive(w: pl.DataFrame, cfg: dict) -> dict:
    """D_W (no labels) for every cell x base x scenario that was run: D1-E's other fill models (1 replicate) and D1-S."""
    a = cfg["analysis"]
    out = {}
    for (cell, base, fm, lat), g in w.group_by("cell", "base", "fill_model", "latency", maintain_order=True):
        ok = (g["orders_U"] >= a["h4w_min_orders_per_window"]) & (g["orders_P"] >= a["h4w_min_orders_per_window"])
        x = np.where(ok.to_numpy(), g["D_W_bp"].cast(pl.Float64).fill_null(float("nan")).to_numpy(), np.nan)
        out[f"{cell}:{base}:{fm}:{lat}"] = {"D_W_bp": boot(x, a["bootstrap_resamples"], cfg["seeds"]["bootstrap_seed"],
                                                           f"desc:{cell}:{base}:{fm}", (95.0,)),
                                            "withdrawn_share_mean": float(g["withdrawn_share"].mean()),
                                            "replicates": int(g["replicates"].max())}
    return out


def run() -> dict:
    from lpx.provenance import provenance, require_clean, sha256_file

    require_clean()
    cfg = tomllib.loads(CONFIG.read_text())
    e3 = tomllib.loads((ROOT / cfg["scope"]["base_config"]).read_text())
    cfg["_fees"] = e3["fees"]
    cfg["policies"] = {**e3["policies"], **cfg["policies"]}
    meta = json.loads((OUT / "e004_meta.json").read_text())
    if meta["provenance"]["git_dirty"]:
        raise RuntimeError("the E004 run must come from a clean tree")
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    if set(meta["sessions"]) & set(rc["splits"]["test"]):
        raise PermissionError("test sessions are sealed")
    for f, h in meta["outputs_sha256"].items():
        if sha256_file(OUT / f) != h:
            raise RuntimeError(f"{f} differs from the table the E004 run wrote")
    prov = provenance(["configs/e004_v1.toml", "configs/e003_v1.toml", "configs/research_v1.toml"])
    if prov["configs"] != {k: v for k, v in meta["provenance"]["configs"].items() if k in prov["configs"]}:
        raise RuntimeError("configuration changed since the run")
    days = meta["evaluation_sessions"]
    fc = pl.read_csv(OUT / "e004_forecast_by_session.csv", infer_schema_length=None)
    w = pl.read_csv(OUT / "e004_windows_by_session.csv", infer_schema_length=None)
    gross = pl.read_csv(OUT / "e004_policy_gross_by_session.csv", infer_schema_length=None)
    net = pl.read_csv(OUT / "e004_policy_net_by_session.csv", infer_schema_length=None)
    res = {"status": meta["status"], "evaluation_sessions": days,
           "provenance": {**prov, "run_git_commit": meta["provenance"]["git_commit"]},
           "primary": {f"H4-W[{b}]": h4w(w, b, cfg) for b in ("P0", "P3_M2")}}
    cells = ["D1_S", "D1_E", "D3", "D4", "D2", "D1_S1", "D1_S3"]
    res["secondary"] = {"H4-F": {f"{c}:{t}": h4f(fc, c, t, cfg, days) for c in cells for t in ("y_k", "y_view")},
                        "H4-0": h40(fc, cfg, days)}
    if any(res["secondary"]["H4-F"][f"D2:{t}"]["label"] != NOT_TESTABLE for t in ("y_k", "y_view")):
        res["secondary"]["forecast_level_flag"] = "pending review (negative control D2 is not 'not testable')"
    for c in ("D1_S1", "D1_S3"):
        for t in ("y_k", "y_view"):
            res["secondary"]["H4-F"][f"{c}:{t}"]["role"] = "descriptive (dose-response)"
    res["descriptive"] = {"status": "modeled historical replay under stress test (LP tier 4 fees hypothetical); no labels",
                          "policy_D1_E": descriptive_policy(gross, net, w, cfg, "D1_E"),
                          "policy_D1_S": descriptive_policy(gross, net, w, cfg, "D1_S"),
                          "p3_ua_vs_pl_forecasts_D1_S": p3_forecast_variants(gross, net, cfg),
                          "window_quality": window_descriptive(w, cfg)}
    (OUT / "e004_analysis.json").write_text(json.dumps(res, indent=1, default=float))
    return res


if __name__ == "__main__":
    run()
