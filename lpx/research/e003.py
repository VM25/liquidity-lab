"""E003 runner — decision-time signals and quoting policies, as frozen in configs/e003_v1.toml and
docs/experiments/E003.md.

Pass 1 computes the features of every discovery session and keeps the thinned training rows. Pass 2, for each evaluation
session s6..s15, fits M1 and M2 on the sessions before it (walk-forward), evaluates the forecasts (status: observed), and
simulates every policy under every fill model x latency scenario (status: modeled historical replay). NT, P0, P1, P3[.]
and the placebo ignore fees: they run fee-free and every fee schedule is an exact overlay. P3F's and P4's rules use the
maker fee, so they are simulated once per fee schedule and only that schedule is applied to them.

Usage (only after the acceptance criteria of E003.md section 9 are met):
    uv run python -m lpx.research.e003
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import json
import subprocess
import tomllib

import numpy as np
import polars as pl

from lpx.book import states as S
from lpx.data.acquire import ROOT
from lpx.data.normalize import normalized_path
from lpx.execution import sim as X
from lpx.research import e003_features as F
from lpx.research.e002 import check_order_limits, episodes, own_fill_markouts, to_states, to_trades

OUT = ROOT / "results" / "e003"
CONFIG = ROOT / "configs" / "e003_v1.toml"
SPEC = ROOT / "docs" / "experiments" / "E003.md"


def load_session(cfg: dict, day: str):
    sym = cfg["scope"]["symbol"]
    st = pl.read_parquet(S.STATES / sym / f"{day}.parquet")
    valid = f"valid_{cfg['scope']['validity_layer']}"
    if not st.filter(pl.col(valid))["bbo_ok"].all():
        raise AssertionError(f"{day}: invalid record inside an accepted window")
    eps = episodes(S.load_windows(sym, day, cfg["scope"]["validity_layer"]), cfg["scope"]["min_episode_s"])
    tr = pl.read_parquet(normalized_path("binance_vision", sym, "trades", day)).sort(["exch_us", "trade_id"])
    # recorder receipt time of each exchange trade (Tardis trade stream, matched by trade id; null if not recorded)
    recv = pl.read_parquet(normalized_path("tardis", sym, "trades", day)).select("trade_id", pl.col("local_us").alias("recv_us"))
    if recv["trade_id"].is_duplicated().any():
        raise AssertionError(f"{day}: duplicate trade ids in the Tardis trade stream")
    tr = tr.drop("local_us", strict=False).join(recv, on="trade_id", how="left", maintain_order="left")
    return st.filter(pl.col(valid)), tr, eps


def features(cfg: dict, st: pl.DataFrame, tr: pl.DataFrame, eps) -> pl.DataFrame:
    fc = cfg["features"]
    return F.session_features(st, tr, eps, cfg["instrument"]["tick"], fc["decision_delay_us"], fc["horizons_s"],
                              fc["warmup_s"])


def fit_models(cfg: dict, train: dict[str, pl.DataFrame], before: str, h: float) -> dict[str, F.LinearModel]:
    fc = cfg["features"]
    clip = tuple(fc["clip_quantiles"])
    return {m: F.fit_linear(train, before, tuple(fc[f"regressors_{m.lower()}"]), f"y_{h:g}s", 1, clip)
            for m in ("M1", "M2")}


def risk_from_grid(grids: list[list[tuple]], maker: float, taker: float, q: float) -> dict:
    """Interval P&L of the session under one fee schedule: increments of liquidation-adjusted marked wealth on the
    exchange-clock grid of each episode (the last increment of an episode includes the liquidation)."""
    inc = []
    for g in grids:
        if len(g) > 1:
            w = np.array([x[1] - maker * x[2] - taker * x[3] for x in g])
            inc.append(np.diff(w))
    x = np.concatenate(inc) if inc else np.array([])
    if x.size == 0:
        return {"inc_n": 0, "inc_std": None, "inc_es": None, "inc_worst": None}
    k = int(np.ceil(q * x.size))
    es = -float(np.sort(x)[:k].mean())          # expected shortfall as a positive loss
    return {"inc_n": int(x.size), "inc_std": float(np.std(x)), "inc_es": es, "inc_worst": float(x.min())}


def make_policy(name: str, pc: dict, maker_rule: float | None):
    if name == "NT":
        return X.no_trade
    if name == "P0":
        return X.p0_fixed(pc["size"], pc["inventory_limit"])
    if name == "P1":
        return X.p1_inventory_withdrawal(pc["size"], pc["inventory_limit"], pc["p1_threshold"])
    if name in ("P3_M1", "P3_M2"):
        return X.p3_alpha(pc["size"], pc["inventory_limit"], name[-2:])
    if name == "P3_negM2":
        return X.p3_alpha(pc["size"], pc["inventory_limit"], "M2", sign=-1.0)
    if name == "P3F":
        return X.p3_alpha(pc["size"], pc["inventory_limit"], pc["p4_model"], maker_fee=maker_rule)
    if name == "P4":
        return X.p4_combined(pc["size"], pc["inventory_limit"], pc["p1_threshold"], pc["p4_kappa_ticks_per_unit"],
                             maker_rule, pc["p4_model"])
    raise ValueError(name)


@dataclasses.dataclass
class SessionData:
    """One evaluation session as the simulator sees it: true states (forecasts attached), exchange trades, episodes."""
    states: list[X.State]
    trades: list[X.Trade]
    eps: list[tuple[int, int]]
    cfg: dict

    def __post_init__(self):
        tick = self.cfg["instrument"]["tick"]
        self.t_states = np.array([s.t_exch for s in self.states])
        self.mid = np.array([s.mid_ticks * tick for s in self.states])
        self.t_tr = np.array([t.t for t in self.trades])


def simulate(sd: SessionData, policy: str, model: str, lat: str, rule: str | None, pol=None, views=None,
             extras=None) -> tuple[dict, list[X.Fill]]:
    """One policy x scenario (x fee rule) on one session: the aggregate row and every fill. ``pol`` overrides the policy
    built from ``policy`` (same name in the row); ``views`` / ``extras`` give each episode's view states and extra decision
    times (E004; None = E003's per-state decisions)."""
    cfg = sd.cfg
    inst, pc, pace, fc, an = cfg["instrument"], cfg["policies"], cfg["pacing"], cfg["features"], cfg["analysis"]
    fees = {k: v for k, v in cfg["fees"].items() if k != "default"}
    warm = int(fc["warmup_s"] * 1e6)
    L = cfg["latency"].get(lat, {"entry_us": 0, "ack_us": 0, "md_delay_us": 0})
    ec = X.ExecConfig(fill_model="conservative" if model == "none" else model, md_delay_us=L["md_delay_us"],
                      entry_latency_us=L["entry_us"], ack_latency_us=L["ack_us"], maker_fee=0.0, taker_fee=0.0,
                      tick=inst["tick"], lot=inst["lot"], min_notional=inst["min_notional"],
                      max_orders_per_10s=inst["max_orders_per_10s"], max_orders_per_day=inst["max_orders_per_day"],
                      pace_rate_per_s=pace["rate_per_s"], pace_burst=pace["burst"], warmup_us=warm,
                      hold_rejected_until_new_state=True, grid_us=int(an["risk_grid_s"] * 1e6))
    sched = [rule] if rule else list(fees)
    carry = X.Carry(fee_paths=tuple((fees[k]["maker"], fees[k]["taker"]) for k in sched))
    if pol is None:
        pol = make_policy(policy, pc, fees[rule]["maker"] if rule else None)
    agg = dict(policy=policy, fill_model=model, latency=lat, fee_rule=rule or "none", episodes=0, valid_hours=0.0,
               fills=0, fills_at_price=0, fills_through=0, fills_crossing=0, filled_notional=0.0, gross_marked=0.0,
               edge=0.0, inventory_pnl=0.0, liquidation_slippage=0.0, liquidation_notional=0.0,
               liquidation_shortfall=0.0, episodes_with_shortfall=0, orders_sent=0, orders_rejected=0,
               rate_limited=0, paced=0, paced_spells=0, paced_bid_s=0.0, paced_ask_s=0.0, filled_qty=0.0, quoted_qty=0.0, max_abs_inventory=0.0,
               tw_abs_inventory_s=0.0, quote_bid_s=0.0, quote_ask_s=0.0, quote_both_s=0.0)
    all_fills, sends, grids = [], [], []
    for e, (a, b) in enumerate(sd.eps):
        i0, i1 = np.searchsorted(sd.t_states, a, side="left"), np.searchsorted(sd.t_states, b, side="right")
        j0, j1 = np.searchsorted(sd.t_tr, a, side="right"), np.searchsorted(sd.t_tr, b, side="right")
        r = X.Simulator(ec, pol, sd.states[i0:i1], sd.trades[j0:j1], t_start=a, t_end=b, carry=carry,
                        view=None if views is None else views[e],
                        extra_decision_times=None if extras is None else extras[e]).run()
        if any(not (a <= f.t <= b) for f in r.fills) or (model != "optimistic" and
                                                          any(f.reason == "crossing" for f in r.fills)):
            raise AssertionError("fill outside its episode or crossing fill outside the optimistic model")
        if any(t < a + warm for t in r.send_times):
            raise AssertionError("order sent during the warm-up")
        if r.rate_limited:
            raise AssertionError("an exchange order limit bound despite pacing")
        agg["episodes"] += 1
        agg["valid_hours"] += r.duration_s / 3600
        agg["fills"] += len(r.fills)
        for reason in ("at_price", "through", "crossing"):
            agg[f"fills_{reason}"] += sum(f.reason == reason for f in r.fills)
        for k_res, k_agg in (("filled_notional", "filled_notional"), ("marked_final", "gross_marked"),
                             ("edge", "edge"), ("inventory_pnl", "inventory_pnl"),
                             ("liquidation_slippage", "liquidation_slippage"),
                             ("liquidation_proceeds", "liquidation_notional"),
                             ("liquidation_shortfall", "liquidation_shortfall"), ("orders_sent", "orders_sent"),
                             ("orders_rejected", "orders_rejected"), ("paced", "paced"), ("filled_qty", "filled_qty"),
                             ("quoted_qty", "quoted_qty"), ("time_weighted_abs_inventory", "tw_abs_inventory_s")):
            agg[k_agg] += getattr(r, k_res)
        agg["episodes_with_shortfall"] += r.liquidation_shortfall > 0
        agg["max_abs_inventory"] = max(agg["max_abs_inventory"], r.max_abs_inventory)
        for side in ("bid", "ask", "both"):
            agg[f"quote_{side}_s"] += r.quote_time_s[side]
        agg["paced_spells"] += r.paced_spells
        agg["paced_bid_s"] += r.paced_time_s["bid"]
        agg["paced_ask_s"] += r.paced_time_s["ask"]
        all_fills += r.fills
        sends += r.send_times
        grids.append(r.grid)
    check_order_limits(sends, inst["max_orders_per_10s"], inst["max_orders_per_day"])
    ps = getattr(pol, "stats", None)
    agg["decisions"] = ps["decisions"] if ps else None
    agg["gate_active_share"] = ps["gated"] / ps["decisions"] if ps and ps["decisions"] else None
    agg["vol_closed_share"] = ps["vol_closed"] / ps["decisions"] if ps and ps["decisions"] else None
    secs = agg["valid_hours"] * 3600
    agg["fill_rate"] = agg["filled_qty"] / agg["quoted_qty"] if agg["quoted_qty"] > 0 else None
    agg["tw_abs_inventory_avg"] = agg["tw_abs_inventory_s"] / secs if secs > 0 else None
    for side in ("bid", "ask", "both"):
        agg[f"quote_presence_{side}"] = agg[f"quote_{side}_s"] / secs if secs > 0 else None
    agg["paced_time_share"] = (agg["paced_bid_s"] + agg["paced_ask_s"]) / (2 * secs) if secs > 0 else None
    for k, name in enumerate(sched):
        agg[f"max_drawdown__{name}"] = carry.max_drawdown[k]
        for m, v in risk_from_grid(grids, fees[name]["maker"], fees[name]["taker"], an["expected_shortfall_q"]).items():
            agg[f"{m}__{name}"] = v
    agg.update(own_fill_markouts(all_fills, sd.eps, sd.t_states, sd.mid, an["markout_horizons_s"], inst["tick"]))
    return agg, all_fills


def run_session(states: list[X.State], trades: list[X.Trade], eps, cfg: dict) -> list[dict]:
    """Every policy x scenario (x fee rule for P4) on one evaluation session whose states carry their forecasts."""
    pc = cfg["policies"]
    fees = {k: v for k, v in cfg["fees"].items() if k != "default"}
    sd = SessionData(states, trades, eps, cfg)
    jobs = []
    for policy in pc["run"]:
        if policy == "NT":
            jobs.append((policy, "none", "none", None))
            continue
        for model in cfg["fill_models"]["primary"]:
            for lat in cfg["latency"]:
                for rule in (fees if policy in pc["fee_aware"] else [None]):
                    jobs.append((policy, model, lat, rule))
    return [simulate(sd, *job)[0] for job in jobs]


def fee_overlay(rows: pl.DataFrame, fees: dict) -> pl.DataFrame:
    """One row per (scenario, fee schedule): every schedule for fee-unaware policies, only its own rule for P3F and P4.
    Net is liquidation-adjusted; ``net_bp_per_notional`` is undefined without fills, ``net_per_hour`` without time."""
    out = []
    per_fee = [c for c in rows.columns if "__" in c]
    for name, f in fees.items():
        if name == "default":
            continue
        sub = rows.filter((pl.col("fee_rule") == "none") | (pl.col("fee_rule") == name))
        out.append(sub.with_columns(
            pl.lit(name).alias("fee_schedule"),
            *[pl.col(c).alias(c.split("__")[0]) for c in per_fee if c.endswith(f"__{name}")],
            (pl.col("filled_notional") * f["maker"]).alias("maker_fees"),
            (pl.col("liquidation_notional") * f["taker"]).alias("taker_fees")).with_columns(
            (pl.col("gross_marked") - pl.col("liquidation_slippage") - pl.col("maker_fees") - pl.col("taker_fees")).alias("net"),
            (pl.col("gross_marked") - pl.col("liquidation_slippage")).alias("gross_liq"),
        ).with_columns(
            pl.when(pl.col("filled_notional") > 0).then(pl.col("net") / pl.col("filled_notional") * 1e4).otherwise(None)
            .alias("net_bp_per_notional"),
            pl.when(pl.col("valid_hours") > 0).then(pl.col("net") / pl.col("valid_hours")).otherwise(None).alias("net_per_hour"),
            pl.when(pl.col("valid_hours") > 0).then(pl.col("gross_liq") / pl.col("valid_hours")).otherwise(None)
            .alias("gross_per_hour"),
            pl.when(pl.col("valid_hours") > 0).then(pl.col("filled_notional") / pl.col("valid_hours")).otherwise(None)
            .alias("turnover_per_hour"),
            pl.when(pl.col("fills") > 0).then(pl.col("orders_sent") / pl.col("fills")).otherwise(None).alias("orders_per_fill"),
            pl.when(pl.col("filled_notional") > 0).then(pl.col("gross_liq") / pl.col("filled_notional") * 1e4).otherwise(None)
            .alias("gross_bp_per_notional"),
        ).with_columns(
            # participation-normalised risk: per 1,000 USDT of hourly turnover
            pl.when(pl.col("turnover_per_hour") > 0).then(pl.col("inc_es") / pl.col("turnover_per_hour") * 1e3)
            .otherwise(None).alias("es_per_k_turnover"),
            pl.when(pl.col("turnover_per_hour") > 0).then(pl.col("tw_abs_inventory_avg") / pl.col("turnover_per_hour") * 1e3)
            .otherwise(None).alias("inventory_per_k_turnover"),
            pl.when(pl.col("inc_std") > 0).then(pl.col("net_per_hour") / pl.col("inc_std")).otherwise(None)
            .alias("net_per_hour_over_inc_std"),           # descriptive risk-adjusted ratio
        ).drop(per_fee))
    return pl.concat(out, how="diagonal")


def forecast_rows(day: str, ft: pl.DataFrame, models: dict[float, dict[str, F.LinearModel]], primary_h: float) -> tuple[list, list]:
    """Out-of-sample skill of M1 and M2 on one evaluation session (eligible rows, regional decision clock)."""
    ev = ft.filter(pl.col("eligible"))
    rows, cal = [], []
    mid, half = ev["mid_ticks"].to_numpy(), (ev["spread"].to_numpy() + 1) / 2
    for h, ms in models.items():
        y = ev[f"y_{h:g}s"].to_numpy()
        for m, mod in ms.items():
            f = mod.predict(ev)
            rows.append({"day": day, "model": m, "horizon_s": h, **F.forecast_skill(y, f, f * mid / 1e4, half)})
            if h == primary_h and m == "M2":
                cal += [{"day": day, **c} for c in F.calibration(y, f)]
    return rows, cal


def attach(states: list[X.State], ft: pl.DataFrame, models: dict[str, F.LinearModel], rv_gate: float) -> None:
    """Attach each episode state's forecasts (bp) and volatility gate, computed from that state's information set only.
    The feature row must carry exactly the state's (t_exch, t_recv): an off-by-one would hand a state the next one's."""
    f1, f2 = models["M1"].predict(ft), models["M2"].predict(ft)
    rv = ft["rv_60s"].to_numpy()
    te, tr = ft["t_exch_us"].to_numpy(), ft["t_recv_us"].to_numpy()
    for i, row in enumerate(ft["row"].to_numpy()):
        s = states[row]
        if (s.t_exch, s.t_recv) != (int(te[i]), int(tr[i])):
            raise AssertionError("forecast attached to the wrong state")
        s.aux = {"M1": float(f1[i]), "M2": float(f2[i]), "vol_ok": bool(rv[i] <= rv_gate)}


def verify_receipt_inputs(cfg: dict, days: list[str]) -> dict[str, str]:
    """The Tardis trade files (receipt times decide which trades enter the flow features) must be the ones audited by the
    acceptance run of record."""
    from lpx.provenance import sha256_file

    acc = json.loads((ROOT / "results" / "acceptance_001" / "summary.json").read_text())
    sym = cfg["scope"]["symbol"]
    recorded = {(r["symbol"], r["day"]): r["normalized_inputs_sha256"] for r in acc["tardis"]}
    out = {}
    for d in days:
        p = normalized_path("tardis", sym, "trades", d)
        h = sha256_file(p)
        if recorded[(sym, d)].get(str(p.relative_to(ROOT))) != h:
            raise RuntimeError(f"{p} differs from the trade file audited by the acceptance run of record")
        out[d] = h
    return out


def run() -> dict:
    from lpx.provenance import provenance, require_clean, sha256_file
    from lpx.research.e001 import verify_inputs

    cfg = tomllib.loads(CONFIG.read_text())
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    if "test" in cfg["scope"]["session_sets"]:
        raise PermissionError("test sessions are sealed until the Stage 4 close-out")
    if cfg["scope"]["acceptance_git_commit"] != rc["dataset"]["acceptance_git_commit"]:
        raise RuntimeError("E003 and research_v1 name different acceptance runs")
    require_clean()
    if subprocess.run(["git", "status", "--porcelain", "--", str(SPEC)], cwd=ROOT, capture_output=True, text=True,
                      check=True).stdout.strip():
        raise SystemExit("E003.md has uncommitted changes: commit the specification first")
    if OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError("results/e003 is not empty; a rerun needs a DECISIONS.md entry and a fresh directory")
    prov = {**provenance(["configs/e003_v1.toml", "configs/research_v1.toml"]), "spec_sha256": sha256_file(SPEC)}
    days = sorted(d for k in cfg["scope"]["session_sets"] for d in rc["splits"][k])
    if set(days) & set(rc["splits"]["test"]):
        raise PermissionError("test sessions are sealed until the Stage 4 close-out")
    base_inputs, receipts = verify_inputs(rc, days), verify_receipt_inputs(cfg, days)
    inputs = {**base_inputs, "sessions": {d: {**x, "tardis_trades_sha256": receipts[d]}
                                          for d, x in base_inputs["sessions"].items()}}
    k0 = cfg["scope"]["min_training_sessions"]
    fc, pc = cfg["features"], cfg["policies"]
    # pass 1: thinned training rows of every discovery session (features only depend on the session itself)
    thin, unrec = {}, {}
    for d in days:
        st, tr, eps = load_session(cfg, d)
        ft = features(cfg, st, tr, eps)
        thin[d] = ft.filter(pl.col("eligible")).gather_every(fc["fit_thinning"])
        unrec[d] = int(tr["recv_us"].null_count())
        print(f"{d}: features ({ft.height} rows; {unrec[d]} trades without receipt time)", flush=True)
    # pass 2: walk-forward evaluation sessions
    gross, frows, cal, models_out = [], [], [], {}
    for i, d in enumerate(days):
        if i < k0:
            continue
        train = {x: thin[x] for x in days[:i]}
        models = {h: fit_models(cfg, train, d, h) for h in fc["horizons_s"]}
        rv_med = float(pl.concat([train[x] for x in train]).filter(pl.col("y_5s").is_not_nan() & pl.col("y_5s").is_not_null())
                       ["rv_60s"].median())   # training rows: thinned eligible rows with a defined target
        rv_gate = pc["p4_vol_gate_multiple"] * rv_med
        models_out[d] = {"rv_60s_training_median": rv_med, "rv_gate": rv_gate,
                         **{f"h{h:g}s_{m}": dataclasses.asdict(mod) for h, ms in models.items() for m, mod in ms.items()}}
        st, tr, eps = load_session(cfg, d)
        ft = features(cfg, st, tr, eps)
        fr, cl = forecast_rows(d, ft, models, fc["primary_horizon_s"])
        frows += fr
        cal += cl
        states = to_states(st, cfg["instrument"]["tick"])
        attach(states, ft, models[fc["primary_horizon_s"]], rv_gate)
        split = "train" if d in rc["splits"]["train"] else "validation"
        for r in run_session(states, to_trades(tr, cfg["instrument"]["tick"]), eps, cfg):
            gross.append({"day": d, "split": split, **r})
        print(f"{d}: evaluated ({len(eps)} episodes)", flush=True)
    end = provenance(["configs/e003_v1.toml", "configs/research_v1.toml"])
    if (end["git_commit"], end["code_fingerprint"], end["git_dirty"]) != (prov["git_commit"], prov["code_fingerprint"], False):
        raise RuntimeError("source revision changed during the run")
    if (end["configs"] != prov["configs"] or sha256_file(SPEC) != prov["spec_sha256"]
            or verify_inputs(rc, days) != base_inputs or verify_receipt_inputs(cfg, days) != receipts):
        raise RuntimeError("specification, configuration or inputs changed during the run")
    OUT.mkdir(parents=True, exist_ok=True)
    g = pl.DataFrame(gross, infer_schema_length=None)
    tables = {"e003_gross_by_session.csv": g, "e003_net_by_session.csv": fee_overlay(g, cfg["fees"]),
              "e003_forecast_by_session.csv": pl.DataFrame(frows), "e003_calibration.csv": pl.DataFrame(cal)}
    for name, t in tables.items():
        t.write_csv(OUT / name)
    (OUT / "e003_models.json").write_text(json.dumps(models_out, indent=1))
    meta = {"experiment": "E003", "status": {"forecasts": "observed", "policies": "modeled historical replay"},
            "sessions": days, "evaluation_sessions": days[k0:], "trades_without_receipt_time": unrec,
            "run_at_utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"), "provenance": {**prov, "inputs": inputs},
            "outputs_sha256": {f: sha256_file(OUT / f) for f in [*tables, "e003_models.json"]}}
    tmp = OUT / "e003_meta.json.tmp"
    tmp.write_text(json.dumps(meta, indent=1))
    tmp.replace(OUT / "e003_meta.json")  # written last: a meta file always binds complete tables
    return meta


if __name__ == "__main__":
    run()
