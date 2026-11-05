"""E001 — observed signed post-trade markouts (RESEARCH_SPEC), as specified in configs/research_v1.toml (amended
2026-10-19, before any E001 outcome was computed).

Status label: **observed**. Inputs are the exchange trade archive (complete trade ids, exchange aggressor flag) and the
Stage 1 verified book states; no order of ours is assumed and nothing is filled.

Event units
    ``ts_side_cluster`` (primary): exchange trades sharing trade time T and aggressor side. Binance publishes no parent
    order id, so a cluster is *not* a verified aggressive order — it may merge orders or, in principle, split one.
    ``trade`` (sensitivity): every exchange trade id is its own event.

Information clocks (``timing``)
    ``exchange`` (primary): book state = last state with exchange time E < T; outcome = last state with E <= T+h.
        Retrospective conditioning on the book as published by the exchange; not information a live participant held.
    ``receipt+<d>ms``: the pre-event state is the last one the recorder had *received* d ms before T (receipt time +
        d < T) — availability-safe for a participant at the Tardis recorder (Tokyo) with d ms of extra latency. Only the
        conditioning information changes: outcomes are always measured on the exchange clock at exactly T+h, so every
        timing variant measures the same 1/5/30 s post-trade horizons (amended 2026-10-19, before any outcome).

Per event, in basis points of the pre-event mid m0 (s = +1 buyer-initiated, -1 seller-initiated, P = event VWAP):
    mo(h) = s (m(T+h) - m0) / m0      es = 2 s (P - m0) / m0      rs(h) = es - 2 mo(h)

Validity: the selected pre-event and outcome *records* must each be valid (proven uncrossed touch, inside an accepted
joint window) and T, T+h and both states must lie in the same window. The primary sample requires this for every
primary horizon (one common event set). Sessions are the inference unit. Labels: the primary specification is
"pre-specified primary (discovery)" — fixed before any outcome, but evaluated on discovery sessions, so it is not a
confirmation; confirmation is the single test-session run at the Stage 4 close-out. Everything else is "exploratory".

Usage: ``uv run python -m lpx.research.e001``   (discovery sessions only; test sessions are refused)
"""

from __future__ import annotations

import datetime as dt
import json
import sys
import tomllib

import numpy as np
import polars as pl

from lpx.book import states as S
from lpx.data.acquire import ROOT
from lpx.data.normalize import normalized_path

OUT = ROOT / "results" / "e001"
STATE_COLS = ["t_exch_us", "t_local_us", "bid1_px", "ask1_px", "bid1_qty", "ask1_qty", "bbo_ok", "valid_joint"]


def ts_side_clusters(trades: pl.DataFrame) -> pl.DataFrame:
    """Group exchange trades by (trade time, aggressor side). Not verified parent orders."""
    return (trades.group_by(["exch_us", "aggressor"], maintain_order=True)
            .agg(pl.col("qty").sum().alias("qty"), (pl.col("price") * pl.col("qty")).sum().alias("notional"),
                 pl.col("price").n_unique().alias("levels"), pl.len().alias("fills"), pl.col("trade_id").min().alias("first_id"))
            .with_columns((pl.col("notional") / pl.col("qty")).alias("vwap"))
            .sort(["exch_us", "first_id"]))


def single_trades(trades: pl.DataFrame) -> pl.DataFrame:
    return trades.select("exch_us", "aggressor", "qty", (pl.col("price") * pl.col("qty")).alias("notional"),
                         pl.lit(1, pl.UInt32).alias("levels"), pl.lit(1, pl.UInt32).alias("fills"),
                         pl.col("trade_id").alias("first_id"), pl.col("price").alias("vwap")).sort(["exch_us", "first_id"])


def parse_timing(timing: str) -> tuple[str, int]:
    if timing == "exchange":
        return "exchange", 0
    if timing.startswith("receipt"):
        d = timing.removeprefix("receipt").removeprefix("+").removesuffix("ms")
        return "receipt", int(round(float(d or 0) * 1000))
    raise ValueError(f"unknown timing {timing!r}")


class Session:
    """Inputs for one session, loaded once and reused across specifications."""

    def __init__(self, symbol: str, day: str):
        self.day = day
        st = pl.read_parquet(S.STATES / symbol / f"{day}.parquet", columns=STATE_COLS)
        self.t_exch = st["t_exch_us"].to_numpy()
        self.t_local = st["t_local_us"].to_numpy()
        self.mid = ((st["bid1_px"] + st["ask1_px"]) / 2).to_numpy()
        self.bid = st["bid1_px"].to_numpy()
        self.ask = st["ask1_px"].to_numpy()
        self.qb = st["bid1_qty"].to_numpy()
        self.qa = st["ask1_qty"].to_numpy()
        self.bbo_ok = st["bbo_ok"].to_numpy()
        self.valid_joint = st["valid_joint"].to_numpy()
        self.trades = pl.read_parquet(normalized_path("binance_vision", symbol, "trades", day))
        self.symbol = symbol


def session_events(sess: Session, windows: pl.DataFrame, horizons_s: list[float], primary_horizons_s: list[float],
                   unit: str = "ts_side_cluster", timing: str = "exchange", baseline_windows: bool = False) -> pl.DataFrame:
    ev = ts_side_clusters(sess.trades) if unit == "ts_side_cluster" else single_trades(sess.trades)
    clock, delay = parse_timing(timing)
    t_pre = sess.t_exch if clock == "exchange" else sess.t_local + delay  # information clock for the pre-event state
    in_w = S.in_windows(sess.t_exch, windows)
    state_ok = sess.bbo_ok & in_w  # record-level validity under the windows in use
    if baseline_windows and not np.array_equal(in_w, sess.valid_joint):
        raise AssertionError(f"{sess.day}: exported valid_joint disagrees with the accepted windows")
    T = ev["exch_us"].to_numpy()
    s = ev["aggressor"].to_numpy().astype(float)
    i0, ok0 = S.asof(t_pre, T, windows, state_ok=state_ok, t_window=sess.t_exch, strict=True)
    j0 = np.clip(i0, 0, None)
    if np.any(ok0 & ~state_ok[j0]):
        raise AssertionError("asof returned an invalid pre-event record as valid")
    m0 = np.where(ok0, sess.mid[j0], np.nan)
    wid_T = S.window_id(T, windows)
    cols = {
        "day": [sess.day] * len(T), "t_us": T, "sign": s, "qty": ev["qty"].to_numpy(), "vwap": ev["vwap"].to_numpy(),
        "fills": ev["fills"].to_numpy(), "levels": ev["levels"].to_numpy(), "m0": m0,
        "q_bid1": np.where(ok0, sess.qb[j0], np.nan), "q_ask1": np.where(ok0, sess.qa[j0], np.nan),
        "pre_state_age_ms": np.where(ok0, (T - sess.t_exch[j0]) / 1e3, np.nan),
    }
    cols["es"] = np.where(ok0, 2 * s * (cols["vwap"] - m0) / m0 * 1e4, np.nan)
    horizon_ok = {}
    for h in horizons_s:
        th = T + int(round(h * 1e6))
        # outcomes always on the exchange clock at exactly T + h, whatever the information clock of the pre-state
        ih, okh = S.asof(sess.t_exch, th, windows, state_ok=state_ok, strict=False)
        same = ok0 & okh & (S.window_id(th, windows) == wid_T)
        horizon_ok[h] = same
        mh = np.where(same, sess.mid[np.clip(ih, 0, None)], np.nan)
        mo = s * (mh - m0) / m0 * 1e4
        cols[f"mo_{h:g}s"] = mo
        cols[f"rs_{h:g}s"] = cols["es"] - 2 * mo
    all_ok = np.logical_and.reduce([horizon_ok[h] for h in primary_horizons_s])
    rec_bad = (i0 >= 0) & ~sess.bbo_ok[j0]
    rec_out = (i0 >= 0) & sess.bbo_ok[j0] & ~in_w[j0]
    last_t = sess.t_exch.max()
    # "beyond session data" only when every primary horizon that ends within the data is valid; otherwise the event
    # left its window first, which is the price-path (missing-not-at-random) mechanism and is labelled as such
    inside_ok = np.logical_and.reduce([horizon_ok[h] | (T + int(round(h * 1e6)) > last_t) for h in primary_horizons_s])
    beyond = (T + int(round(max(primary_horizons_s) * 1e6)) > last_t) & inside_ok
    reason = np.select(
        [wid_T < 0, i0 < 0, rec_bad, rec_out, ~ok0, ~all_ok & beyond, ~all_ok],
        ["t_outside_windows", "no_pre_state", "pre_state_record_invalid", "pre_state_outside_windows",
         "pre_state_in_other_window", "horizon_beyond_session_data", "horizon_leaves_window"], default="included")
    cols["reason"] = reason
    cols["primary"] = reason == "included"
    # observed post-event touch move (proxy validation; exchange clock; descriptive only, never a conditioning input)
    k = np.searchsorted(sess.t_exch, T, side="left")  # first state with E >= T (the batch containing the trade)
    kk = np.clip(k, 0, len(sess.t_exch) - 1)
    ok_next = (k < len(sess.t_exch)) & state_ok[kk] & (S.window_id(sess.t_exch[kk], windows) == wid_T) & ok0
    moved = np.where(s > 0, sess.ask[kk] > sess.ask[j0], sess.bid[kk] < sess.bid[j0])
    cols["touch_moved_next_state"] = np.where(ok_next, moved.astype(float), np.nan)
    return pl.DataFrame(cols)


def add_cells(ev: pl.DataFrame, size_edges: tuple[float, float]) -> pl.DataFrame:
    """Pre-declared conditioning cells. ``qty_ge_touch`` is a proxy (event size >= pre-event touch size on the side it
    hits); it does not establish that the queue was depleted (orders may be added within the same 100 ms batch)."""
    a, b = size_edges
    imb = pl.col("sign") * (pl.col("q_bid1") - pl.col("q_ask1")) / (pl.col("q_bid1") + pl.col("q_ask1"))
    touch = pl.when(pl.col("sign") > 0).then(pl.col("q_ask1")).otherwise(pl.col("q_bid1"))
    return ev.with_columns(
        pl.when(pl.col("qty") <= a).then(pl.lit("S")).when(pl.col("qty") <= b).then(pl.lit("M")).otherwise(pl.lit("L")).alias("size"),
        pl.when(imb <= -1 / 3).then(pl.lit("against")).when(imb < 1 / 3).then(pl.lit("neutral")).otherwise(pl.lit("with")).alias("touch_imbalance"),
        (pl.col("qty") >= touch).alias("qty_ge_touch"),
    )


def session_bootstrap(per_session: np.ndarray, n: int, rng: np.random.Generator) -> tuple[float, float]:
    x = per_session[~np.isnan(per_session)]
    if x.size < 2:
        return (np.nan, np.nan)
    m = x[rng.integers(0, x.size, size=(n, x.size))].mean(axis=1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def block_bootstrap(t_us: np.ndarray, x: np.ndarray, block_s: float, n: int, rng: np.random.Generator) -> tuple[float, float]:
    ok = ~np.isnan(x)
    t_us, x = t_us[ok], x[ok]
    if x.size < 2:
        return (np.nan, np.nan)
    blk = ((t_us - t_us.min()) // int(block_s * 1e6)).astype(np.int64)
    ub, inv = np.unique(blk, return_inverse=True)
    sums = np.bincount(inv, weights=x)
    cnts = np.bincount(inv).astype(float)
    draws = rng.integers(0, ub.size, size=(n, ub.size))
    m = sums[draws].sum(axis=1) / cnts[draws].sum(axis=1)
    return float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def summarize(frame: pl.DataFrame, metrics: list[str], label: dict, n_boot: int, rng: np.random.Generator) -> list[dict]:
    """Per-metric mean of session means with a session-bootstrap 95% interval (unadjusted for multiplicity)."""
    rows = []
    per = frame.group_by("day").agg([pl.col(m).drop_nans().mean().alias(m) for m in metrics]).sort("day")
    for m in metrics:
        v = per[m].to_numpy().astype(float)
        lo, hi = session_bootstrap(v, n_boot, rng)
        x = frame[m].drop_nans().drop_nulls()
        rows.append({**label, "metric": m, "sessions": int(np.sum(~np.isnan(v))), "events": int(x.len()),
                     "mean_of_session_means": float(np.nanmean(v)) if np.any(~np.isnan(v)) else None,
                     "ci95_lo": lo, "ci95_hi": hi, "event_weighted_mean": float(x.mean()) if x.len() else None,
                     "sessions_positive": int(np.sum(v > 0))})
    return rows


PRIMARY = "pre-specified primary (discovery)"
EXPLORATORY = "exploratory"


def verify_inputs(cfg: dict, days: list[str]) -> dict:
    """Stage 1 state files must come from the acceptance run of record and carry the current windows hash."""
    import pyarrow.parquet as pq

    from lpx.provenance import sha256_file

    want_commit = cfg["dataset"]["acceptance_git_commit"]
    acc = json.loads((ROOT / "results" / "acceptance_001" / "summary.json").read_text())
    if acc["provenance"]["git_commit"] != want_commit or acc["provenance"]["git_dirty"]:
        raise RuntimeError("results/acceptance_001 is not the acceptance run of record named in research_v1.toml")
    sens = json.loads((ROOT / "results" / "acceptance_001" / "sensitivity.json").read_text())
    if sens["provenance"]["git_commit"] != want_commit or sens["provenance"]["git_dirty"]:
        raise RuntimeError("windows_sensitivity.csv is not from the acceptance run of record")
    recorded = {(r["symbol"], r["day"]): r["normalized_inputs_sha256"] for r in acc["tardis"]}
    w_hash = sha256_file(S.WINDOWS)
    out = {"acceptance_git_commit": want_commit, "windows_csv_sha256": w_hash, "sessions": {}}
    for d in days:
        p = S.STATES / cfg["dataset"]["symbol"] / f"{d}.parquet"
        meta = json.loads(pq.read_metadata(p).metadata[b"lpx"])
        if meta["provenance"]["windows_csv_sha256"] != w_hash or meta["provenance"]["git_dirty"]:
            raise RuntimeError(f"{p} was not exported from the current windows on a clean tree")
        tr = normalized_path("binance_vision", cfg["dataset"]["symbol"], "trades", d)
        tr_hash = sha256_file(tr)
        if recorded[(cfg["dataset"]["symbol"], d)].get(str(tr.relative_to(ROOT))) != tr_hash:
            raise RuntimeError(f"{tr} differs from the trade file audited by the acceptance run of record")
        out["sessions"][d] = {"states_sha256": sha256_file(p), "states_export_commit": meta["provenance"]["git_commit"],
                              "trades_sha256": tr_hash}
    return out


def run(session_sets: list[str] | None = None) -> dict:
    from lpx.provenance import provenance, require_clean, sha256_file

    cfg = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    e, sp = cfg["e001"], cfg["splits"]
    sets = session_sets or e["discovery_sessions"]
    if "test" in sets:
        raise PermissionError("test sessions are held out until the Stage 4 close-out (configs/research_v1.toml)")
    if "train" not in sets:
        raise ValueError("size-tercile edges are fitted on train sessions; include 'train'")
    require_clean()
    days = sorted(d for k in sets for d in sp[k])
    sym = cfg["dataset"]["symbol"]
    inputs = verify_inputs(cfg, days)
    acc = json.loads((ROOT / "results" / "acceptance_001" / "summary.json").read_text())
    eligible = {r["day"] for r in acc["tardis"] if r["symbol"] == sym and r["eligibility"]["e001_eligible"]}
    hz, sec = e["horizons_s"], e["secondary_horizons_s"]
    all_h = hz + sec
    rng = np.random.default_rng(e["seed"])
    n_boot = e["bootstrap_resamples"]
    metrics = ["es"] + [f"mo_{h:g}s" for h in hz] + [f"rs_{h:g}s" for h in hz]
    wsens = pl.read_csv(ROOT / "results" / "acceptance_001" / "windows_sensitivity.csv").filter(pl.col("symbol") == sym)
    sessions = {d: Session(sym, d) for d in days}

    def evaluate(unit: str, timing: str, variant: str | None, day_subset: list[str]) -> pl.DataFrame:
        out = []
        for d in day_subset:
            if variant is None:
                w, base = S.load_windows(sym, d, "joint"), True
            else:
                w = wsens.filter((pl.col("day") == d) & (pl.col("variant") == variant)).select("start_us", "end_us").sort("start_us")
                base = False
            out.append(session_events(sessions[d], w, all_h, hz, unit=unit, timing=timing, baseline_windows=base))
        return pl.concat(out)

    # ---- pre-specified primary: ts_side_cluster x exchange clock x baseline windows x all discovery sessions
    prim_all = evaluate(e["unit_primary"], e["timing_primary"], None, days)
    train_q = prim_all.filter(pl.col("primary") & pl.col("day").is_in(sp["train"]))["qty"]
    edges = (float(train_q.quantile(1 / 3)), float(train_q.quantile(2 / 3)))
    prim_all = add_cells(prim_all, edges)
    prim = prim_all.filter(pl.col("primary"))
    if any(prim[m].is_nan().any() for m in metrics):
        raise AssertionError("primary events with a missing primary metric")
    res = {"experiment": "E001", "status": "observed", "symbol": sym, "sessions": days, "session_sets": sets,
           "run_at_utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
           "provenance": {**provenance(["configs/research_v1.toml", "configs/eligibility_v1.toml"]), "inputs": inputs,
                          "windows_sensitivity_csv_sha256": sha256_file(ROOT / "results" / "acceptance_001" / "windows_sensitivity.csv")},
           "primary_spec": {"unit": e["unit_primary"], "timing": e["timing_primary"], "windows": "acceptance_001 joint (baseline)",
                            "sessions": "all discovery", "analysis": PRIMARY},
           "size_tercile_edges_base_qty": edges,
           "exclusions": {"primary": {k: int(v) for k, v in prim_all["reason"].value_counts().iter_rows()}},
           "events_total": prim_all.height, "events_primary": prim.height,
           "multiplicity_note": ("cell intervals are unadjusted 95% session-bootstrap intervals; with "
                                 f"{len(metrics)} metrics x {sum(prim[c].n_unique() for c in e['conditioning'])} cells, "
                                 "several intervals excluding zero are expected by chance even under no effect")}

    pooled = summarize(prim, metrics, {"analysis": PRIMARY, "spec": "primary", "cell": "all"}, n_boot, rng)
    for c in e["conditioning"]:
        for val in sorted(prim[c].unique().to_list()):
            pooled += summarize(prim.filter(pl.col(c) == val), metrics,
                                {"analysis": PRIMARY, "spec": "primary", "cell": f"{c}={val}"}, n_boot, rng)

    per_session = []
    for d in days:
        f = prim.filter(pl.col("day") == d)
        row = {"analysis": PRIMARY, "day": d, "split": "train" if d in sp["train"] else "validation", "events": f.height,
               "e001_eligible_posthoc": d in eligible, "excluded_events": int((prim_all["day"] == d).sum() - f.height)}
        for m in metrics:
            x = f[m].to_numpy()
            lo, hi = block_bootstrap(f["t_us"].to_numpy(), x, e["block_s"], e["block_bootstrap_resamples"], rng)
            row.update({m: float(np.nanmean(x)) if np.any(~np.isnan(x)) else None, f"{m}_ci95_lo": lo, f"{m}_ci95_hi": hi})
        per_session.append(row)

    # ---- descriptive (declared secondary horizons; pre-state staleness; proxy check)
    desc = {"secondary_horizons": [], "pre_state_age_ms_quantiles": {}}
    avail = prim_all.filter(~pl.col("reason").is_in(["t_outside_windows", "no_pre_state", "pre_state_record_invalid",
                                                      "pre_state_outside_windows", "pre_state_in_other_window"]))
    for h in sec:
        for m in (f"mo_{h:g}s", f"rs_{h:g}s"):
            per = avail.group_by("day").agg(pl.col(m).drop_nans().mean()).sort("day")[m].to_numpy().astype(float)
            desc["secondary_horizons"].append({"metric": m, "events": int(avail[m].drop_nans().len()),
                                               "mean_of_session_means": float(np.nanmean(per))})
    a = prim["pre_state_age_ms"]
    desc["pre_state_age_ms_quantiles"]["exchange (primary)"] = {str(q): float(a.quantile(q)) for q in (0.5, 0.9, 0.99)}
    pv = prim.filter(pl.col("touch_moved_next_state").is_not_nan()).group_by("qty_ge_touch").agg(
        pl.len().alias("events"), pl.col("touch_moved_next_state").mean().alias("share_touch_moved_next_state")).sort("qty_ge_touch")
    res["proxy_validation_qty_ge_touch"] = pv.to_dicts()

    # ---- exploratory robustness (one factor changed at a time from the primary)
    sens_rows = []
    specs = [("unit=trade", "event unit", e["unit_sensitivity"][0], e["timing_primary"], None, days)]
    specs += [(f"timing={t}", "information clock", e["unit_primary"], t, None, days) for t in e["timing_sensitivity"]]
    specs += [("eligible_sessions_only(posthoc)", "session set", e["unit_primary"], e["timing_primary"], None, [d for d in days if d in eligible])]
    specs += [(f"windows:{v}", "validity windows", e["unit_primary"], e["timing_primary"], v, days) for v in e["window_variants"]]
    res["sensitivity_specs"] = []
    for name, factor, unit, timing, variant, dsub in specs:
        if name.startswith("eligible"):
            full = prim_all.filter(pl.col("day").is_in(dsub))
        else:
            full = evaluate(unit, timing, variant, dsub)
        frame = full.filter(pl.col("primary"))
        res["exclusions"][name] = {k: int(v) for k, v in full["reason"].value_counts().iter_rows()}
        res["sensitivity_specs"].append({"spec": name, "factor_changed": factor, "analysis": EXPLORATORY})
        sens_rows += summarize(frame, metrics, {"analysis": EXPLORATORY, "spec": name, "cell": "all"}, n_boot, rng)
        if timing != e["timing_primary"]:
            g = frame["pre_state_age_ms"]
            desc["pre_state_age_ms_quantiles"][timing] = {str(q): float(g.quantile(q)) for q in (0.5, 0.9, 0.99)}
        print(f"sensitivity {name}: events {frame.height:,}", flush=True)
    # available-case per horizon: an event counts for horizon h if its h-outcome is valid, whatever the longer horizons
    sens_rows += summarize(avail, metrics, {"analysis": EXPLORATORY, "spec": "available_case_per_horizon", "cell": "all"}, n_boot, rng)
    res["sensitivity_specs"].append({"spec": "available_case_per_horizon", "factor_changed": "event set per horizon",
                                     "analysis": EXPLORATORY})
    res["descriptive"] = desc
    res["primary"] = [r for r in pooled if r["cell"] == "all"]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "e001_discovery.json").write_text(json.dumps(res, indent=1))
    pl.DataFrame(pooled).write_csv(OUT / "e001_discovery_cells.csv")
    pl.DataFrame(per_session).write_csv(OUT / "e001_discovery_per_session.csv")
    pl.DataFrame(sens_rows).write_csv(OUT / "e001_discovery_sensitivity.csv")
    return res


if __name__ == "__main__":
    res = run(sys.argv[1:] or None)
    print(json.dumps({k: v for k, v in res.items() if k not in ("primary",)}, indent=1)[:3000])
    for r in res["primary"]:
        print(f"{r['metric']:>8}: {r['mean_of_session_means']:+.4f} bp  95% CI [{r['ci95_lo']:+.4f}, {r['ci95_hi']:+.4f}]  "
              f"sessions>0 {r['sessions_positive']}/{r['sessions']}  events {r['events']:,}")
