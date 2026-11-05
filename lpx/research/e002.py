"""E002 runner — execution sensitivity, as frozen in configs/e002_v1.toml and docs/experiments/E002.md.

Status of every output: **modeled historical replay**. Runs P0, P1 (and the no-trade baseline) on every accepted joint
window of at least ``min_episode_s`` in the discovery sessions, under each fill model x latency bracket. Fees do not
affect fills (the policies ignore them), so the simulation runs fee-free and every fee schedule is applied afterwards as
an exact accounting overlay: net = gross - maker_rate * filled notional - taker_rate * liquidation notional.

Usage (only after the acceptance criteria in docs/experiments/E002.md section 8 are met):
    uv run python -m lpx.research.e002
"""

from __future__ import annotations

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

OUT = ROOT / "results" / "e002"
CONFIG = ROOT / "configs" / "e002_v1.toml"


def episodes(windows: pl.DataFrame, min_s: float) -> list[tuple[int, int]]:
    return [(a, b) for a, b in windows.select("start_us", "end_us").iter_rows() if (b - a) / 1e6 >= min_s]


def to_states(df: pl.DataFrame, tick: float, n_levels: int = 10) -> list[X.State]:
    """Stage 1 state rows -> engine states (prices in integer ticks; levels best first, NaN levels dropped)."""
    out = []
    te, tl = df["t_exch_us"].to_numpy(), df["t_local_us"].to_numpy()
    bp = np.column_stack([df[f"bid{i}_px"].to_numpy() for i in range(1, n_levels + 1)])
    bq = np.column_stack([df[f"bid{i}_qty"].to_numpy() for i in range(1, n_levels + 1)])
    ap = np.column_stack([df[f"ask{i}_px"].to_numpy() for i in range(1, n_levels + 1)])
    aq = np.column_stack([df[f"ask{i}_qty"].to_numpy() for i in range(1, n_levels + 1)])
    bt = np.where(np.isnan(bp), -1, np.rint(bp / tick)).astype(np.int64)
    at = np.where(np.isnan(ap), -1, np.rint(ap / tick)).astype(np.int64)
    for k in range(len(te)):
        bids = tuple((int(bt[k, i]), float(bq[k, i])) for i in range(n_levels) if bt[k, i] >= 0)
        asks = tuple((int(at[k, i]), float(aq[k, i])) for i in range(n_levels) if at[k, i] >= 0)
        out.append(X.State(int(te[k]), int(tl[k]), bids, asks))
    return out


def to_trades(df: pl.DataFrame, tick: float) -> list[X.Trade]:
    px = np.rint(df["price"].to_numpy() / tick).astype(np.int64)
    return [X.Trade(int(t), int(p), float(q), int(a))
            for t, p, q, a in zip(df["exch_us"].to_numpy(), px, df["qty"].to_numpy(), df["aggressor"].to_numpy())]


def make_policy(name: str, pc: dict):
    if name == "no_trade":
        return X.no_trade
    if name == "P0":
        return X.p0_fixed(pc["size"], pc["inventory_limit"])
    if name == "P1":
        return X.p1_inventory_withdrawal(pc["size"], pc["inventory_limit"], pc["p1_threshold"])
    raise ValueError(name)


def own_fill_markouts(fills: list[X.Fill], eps: list[tuple[int, int]], t_states: np.ndarray, mid: np.ndarray,
                      horizons_s: list[float], tick: float) -> dict:
    """Diagnostics of own fills (exchange clock), notional-weighted, in bp of the fill price:
    ``own_edge_bp``        sign * (mid before the fill - price): the spread captured at the fill (the edge term);
    ``own_markout_{h}s_bp`` sign * (mid at T + h - price) = passive mark-to-mid at h, i.e. E001's rs(h)/2 measured on
                           our own fills. Fills whose T + h lies beyond their episode end are excluded (no valid state
                           there); the number of fills included is reported."""
    out = {"own_edge_bp": None}
    for h in horizons_s:
        out[f"own_markout_{h:g}s_bp"], out[f"own_markout_{h:g}s_fills"] = None, 0
    if not fills:
        return out
    T = np.array([f.t for f in fills])
    px = np.array([f.px * tick for f in fills])
    q = np.array([f.qty for f in fills])
    sgn = np.array([1.0 if f.side == X.BID else -1.0 for f in fills])
    m0 = np.array([f.mid_ticks * tick for f in fills])
    out["own_edge_bp"] = float(np.sum(sgn * (m0 - px) * q) / np.sum(px * q) * 1e4)
    ends = np.array([b for a, b in eps])
    if np.any(np.diff(ends) <= 0):
        raise AssertionError("episodes must be disjoint and in time order")
    ep_end = ends[np.searchsorted(ends, T, side="left")]  # episodes are disjoint and every fill lies inside one
    for h in horizons_s:
        th = T + int(h * 1e6)
        ok = th <= ep_end
        if ok.any():
            m = mid[np.searchsorted(t_states, th[ok], side="right") - 1]
            out[f"own_markout_{h:g}s_bp"] = float(np.sum(sgn[ok] * (m - px[ok]) * q[ok]) / np.sum(px[ok] * q[ok]) * 1e4)
            out[f"own_markout_{h:g}s_fills"] = int(ok.sum())
    return out


def check_order_limits(send_times: list[int], per_10s: int, per_day: int) -> None:
    """Independent check of the exchange limits from the recorded send times (not from the engine's own counters)."""
    t = np.sort(np.asarray(send_times, dtype=np.int64))
    if t.size > per_day:
        raise AssertionError("more orders than the daily limit")
    if t.size and (np.arange(t.size) - np.searchsorted(t, t - 10_000_000, side="right") + 1).max() > per_10s:
        raise AssertionError("more orders in a 10 s window than the limit")


def run_session(states: list[X.State], trades: list[X.Trade], eps: list[tuple[int, int]], cfg: dict) -> list[dict]:
    """All scenarios on one session, fee-free; fee schedules enter as overlays (``fee_overlay``) and as the fee paths
    of the session drawdown. Order-rate counters and the drawdown path carry across the session's episodes."""
    inst, pc = cfg["instrument"], cfg["policies"]
    fee_names = [k for k in cfg["fees"] if k != "default"]
    fee_paths = tuple((cfg["fees"][k]["maker"], cfg["fees"][k]["taker"]) for k in fee_names)
    t_states = np.array([s.t_exch for s in states])
    mid = np.array([s.mid_ticks * inst["tick"] for s in states])
    t_tr = np.array([t.t for t in trades])
    rows = []
    for policy in pc["run"]:
        models = ["none"] if policy == "no_trade" else cfg["fill_models"]["primary"] + cfg["fill_models"]["reference"]
        lats = ["none"] if policy == "no_trade" else list(cfg["latency"])
        for model in models:
            for lat in lats:
                L = cfg["latency"].get(lat, {"entry_us": 0, "ack_us": 0, "md_delay_us": 0})
                ec = X.ExecConfig(fill_model="conservative" if model == "none" else model, md_delay_us=L["md_delay_us"],
                                  entry_latency_us=L["entry_us"], ack_latency_us=L["ack_us"], maker_fee=0.0, taker_fee=0.0,
                                  tick=inst["tick"], lot=inst["lot"], min_notional=inst["min_notional"],
                                  max_orders_per_10s=inst["max_orders_per_10s"], max_orders_per_day=inst["max_orders_per_day"])
                carry = X.Carry(fee_paths=fee_paths)
                agg = dict(policy=policy, fill_model=model, latency=lat, episodes=0, valid_hours=0.0, fills=0,
                           fills_at_price=0, fills_through=0, fills_crossing=0,
                           filled_notional=0.0, gross_marked=0.0, edge=0.0, inventory_pnl=0.0, liquidation_slippage=0.0,
                           liquidation_notional=0.0, liquidation_shortfall=0.0, episodes_with_shortfall=0, orders_sent=0,
                           orders_rejected=0, rate_limited=0, rate_limited_daily=0, filled_qty=0.0, quoted_qty=0.0,
                           max_abs_inventory=0.0, tw_abs_inventory_s=0.0)
                all_fills, sends = [], []
                for a, b in eps:
                    i0, i1 = np.searchsorted(t_states, a, side="left"), np.searchsorted(t_states, b, side="right")
                    j0, j1 = np.searchsorted(t_tr, a, side="right"), np.searchsorted(t_tr, b, side="right")
                    r = X.Simulator(ec, make_policy(policy, pc), states[i0:i1], trades[j0:j1], t_start=a, t_end=b,
                                    carry=carry).run()
                    if any(not (a <= f.t <= b) for f in r.fills) or (model in ("conservative", "intermediate") and
                                                                      any(f.reason == "crossing" for f in r.fills)):
                        raise AssertionError("fill outside its episode or crossing fill outside the optimistic models")
                    agg["episodes"] += 1
                    agg["valid_hours"] += r.duration_s / 3600
                    agg["fills"] += len(r.fills)
                    for reason in ("at_price", "through", "crossing"):
                        agg[f"fills_{reason}"] += sum(f.reason == reason for f in r.fills)
                    agg["filled_notional"] += r.filled_notional
                    agg["gross_marked"] += r.marked_final
                    agg["edge"] += r.edge
                    agg["inventory_pnl"] += r.inventory_pnl
                    agg["liquidation_slippage"] += r.liquidation_slippage
                    agg["liquidation_notional"] += r.liquidation_proceeds
                    agg["liquidation_shortfall"] += r.liquidation_shortfall
                    agg["episodes_with_shortfall"] += r.liquidation_shortfall > 0
                    agg["orders_sent"] += r.orders_sent
                    agg["orders_rejected"] += r.orders_rejected
                    agg["rate_limited"] += r.rate_limited
                    agg["rate_limited_daily"] += r.rate_limited_daily
                    agg["filled_qty"] += r.filled_qty
                    agg["quoted_qty"] += r.quoted_qty
                    agg["max_abs_inventory"] = max(agg["max_abs_inventory"], r.max_abs_inventory)
                    agg["tw_abs_inventory_s"] += r.time_weighted_abs_inventory
                    all_fills += r.fills
                    sends += r.send_times
                check_order_limits(sends, inst["max_orders_per_10s"], inst["max_orders_per_day"])
                agg["fill_rate"] = agg["filled_qty"] / agg["quoted_qty"] if agg["quoted_qty"] > 0 else None
                agg["tw_abs_inventory_avg"] = agg["tw_abs_inventory_s"] / (agg["valid_hours"] * 3600) if agg["valid_hours"] > 0 else None
                for k, name in enumerate(fee_names):
                    agg[f"max_drawdown__{name}"] = carry.max_drawdown[k]
                agg["first_cap_bind_us"] = carry.first_cap_bind_us  # added after the E002 run (not in its tables)
                agg.update(own_fill_markouts(all_fills, eps, t_states, mid, cfg["analysis"]["markout_horizons_s"], inst["tick"]))
                rows.append(agg)
    return rows


def fee_overlay(rows: pl.DataFrame, fees: dict) -> pl.DataFrame:
    """Expand per-scenario gross rows into one row per fee schedule with net outcomes (liquidation-adjusted).
    ``net_bp_per_notional`` is undefined (null) for a session without fills; such sessions are reported, not imputed."""
    out = []
    dd = [c for c in rows.columns if c.startswith("max_drawdown__")]
    for name, f in fees.items():
        if name == "default":
            continue
        out.append(rows.with_columns(
            pl.lit(name).alias("fee_schedule"), pl.lit(f["label"]).alias("fee_label"),
            pl.col(f"max_drawdown__{name}").alias("max_drawdown"),
            (pl.col("filled_notional") * f["maker"]).alias("maker_fees"),
            (pl.col("liquidation_notional") * f["taker"]).alias("taker_fees")).with_columns(
            (pl.col("gross_marked") - pl.col("liquidation_slippage") - pl.col("maker_fees") - pl.col("taker_fees")).alias("net"),
        ).with_columns(
            pl.when(pl.col("filled_notional") > 0).then(pl.col("net") / pl.col("filled_notional") * 1e4).otherwise(None).alias("net_bp_per_notional"),
            pl.when(pl.col("valid_hours") > 0).then(pl.col("net") / pl.col("valid_hours")).otherwise(None)
            .alias("net_per_hour")).drop(dd))
    return pl.concat(out)


def run() -> dict:
    from lpx.provenance import provenance, require_clean, sha256_file
    from lpx.research.e001 import verify_inputs

    cfg = tomllib.loads(CONFIG.read_text())
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    if "test" in cfg["scope"]["session_sets"]:
        raise PermissionError("test sessions are sealed until the Stage 4 close-out")
    if cfg["scope"]["acceptance_git_commit"] != rc["dataset"]["acceptance_git_commit"]:
        raise RuntimeError("E002 and research_v1 name different acceptance runs")
    require_clean()
    spec = ROOT / "docs" / "experiments" / "E002.md"
    for doc in (spec, ROOT / "docs" / "experiments" / "E002_assumptions_evidence.md"):
        if subprocess.run(["git", "status", "--porcelain", "--", str(doc)], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.strip():
            raise SystemExit(f"{doc.name} has uncommitted changes: commit the specification first")
    # provenance of the code that runs, captured before any simulation and re-checked at the end
    prov = {**provenance(["configs/e002_v1.toml", "configs/research_v1.toml"]), "spec_sha256": sha256_file(spec),
            "assumptions_sha256": sha256_file(ROOT / "docs" / "experiments" / "E002_assumptions_evidence.md")}
    sym, tick = cfg["scope"]["symbol"], cfg["instrument"]["tick"]
    days = sorted(d for k in cfg["scope"]["session_sets"] for d in rc["splits"][k])
    inputs = verify_inputs(rc, days)
    rows = []
    for d in days:
        st = pl.read_parquet(S.STATES / sym / f"{d}.parquet")
        valid = f"valid_{cfg['scope']['validity_layer']}"
        if not st.filter(pl.col(valid))["bbo_ok"].all():
            raise AssertionError(f"{d}: invalid record inside an accepted window")
        win = S.load_windows(sym, d, cfg["scope"]["validity_layer"])
        eps = episodes(win, cfg["scope"]["min_episode_s"])
        st = st.filter(pl.col(valid))
        tr = pl.read_parquet(normalized_path("binance_vision", sym, "trades", d)).sort(["exch_us", "trade_id"])
        for r in run_session(to_states(st, tick), to_trades(tr, tick), eps, cfg):
            rows.append({"day": d, "split": "train" if d in rc["splits"]["train"] else "validation", **r})
        print(f"{d}: {len(eps)} episodes", flush=True)
    gross = pl.DataFrame(rows)
    net = fee_overlay(gross, cfg["fees"])
    end = provenance(["configs/e002_v1.toml", "configs/research_v1.toml"])
    if (end["git_commit"], end["code_fingerprint"], end["git_dirty"]) != (prov["git_commit"], prov["code_fingerprint"], False):
        raise RuntimeError("source revision changed during the run")
    if (OUT / "e002_meta.json").exists():
        raise FileExistsError("results/e002 already holds a run; a rerun needs a DECISIONS.md entry and a fresh directory")
    OUT.mkdir(parents=True, exist_ok=True)
    gross.write_csv(OUT / "e002_gross_by_session.csv")
    net.write_csv(OUT / "e002_net_by_session.csv")
    meta = {"experiment": "E002", "status": "modeled historical replay", "sessions": days,
            "run_at_utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
            "provenance": {**prov, "inputs": inputs},
            "outputs_sha256": {f: sha256_file(OUT / f) for f in ("e002_gross_by_session.csv", "e002_net_by_session.csv")}}
    tmp = OUT / "e002_meta.json.tmp"
    tmp.write_text(json.dumps(meta, indent=1))
    tmp.replace(OUT / "e002_meta.json")  # written last: a meta file always binds complete tables
    return meta


if __name__ == "__main__":
    run()
