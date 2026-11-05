"""Dataset Acceptance Test 001 — orchestration.

For every Tardis symbol-day: field/grid and ordering audits, deterministic replay with validity flags, engine-vs-vendor
top-of-book agreement, resync-snapshot comparisons, trade completeness against the exchange archive, trade/book
alignment, and accepted windows on two layers (``book``; ``joint`` = book valid and trade record complete).
For every crypto-lob-stream symbol-month: sequence census, sequenced replay windows, trade audits. On days captured by
both collectors: message-level cross-capture matching and comparison against the archive's independent REST snapshots.

Outputs (results/acceptance_001/): ``summary.json`` and ``windows.csv`` (machine-readable coverage). Derived per-message
states are written under data/derived/ (local only).

Usage: ``uv run python -m lpx.quality.acceptance``
"""

from __future__ import annotations

import datetime as dt
import json
import sys
import time
import tomllib
from pathlib import Path

import numpy as np
import polars as pl

from lpx.book import engine as E
from lpx.data.acquire import RAW, ROOT
from lpx.data.normalize import normalized_path, read_meta
from lpx.data.schema import SNAPSHOT
from lpx.provenance import code_fingerprint, provenance, require_clean, sha256_file  # noqa: F401  (code_fingerprint re-exported)
from lpx.quality import checks as C

OUT = ROOT / "results" / "acceptance_001"
DERIVED = ROOT / "data" / "derived" / "acceptance_001"


def instruments() -> dict:
    return tomllib.loads((ROOT / "configs" / "instruments.toml").read_text())["binance-spot"]


def day_bounds_us(day: str) -> tuple[int, int]:
    d = dt.datetime.fromisoformat(day).replace(tzinfo=dt.UTC)
    t0 = int(d.timestamp() * 1e6)
    return t0, t0 + 86_400_000_000 - 1


def flag_summary(flags: np.ndarray) -> dict:
    n = len(flags)
    out = {"messages": n, "bbo_valid_fraction": float(np.mean((flags & E.BBO_INVALID) == 0)) if n else None}
    for bit, name in E.FLAG_NAMES.items():
        c = int(np.count_nonzero(flags & bit))
        if c:
            out[name] = c
    return out


def window_stats(w: pl.DataFrame, states: pl.DataFrame, trades: pl.DataFrame, tick: float) -> pl.DataFrame:
    """Market-state descriptors per window.

    * ``twa_spread_ticks``: time-weighted average quoted spread, each depth state weighted by how long it was in force
      inside the window (until the next state or the window end).
    * ``event_mean_spread_ticks``: unweighted mean over depth events (state updates) — not a time average.
    * ``rv_1min_bp``: realized volatility estimator = sample standard deviation (ddof=1) of 1-minute log-mid returns,
      the mid at each minute mark being the last valid state at or before it (previous-tick sampling), in basis points
      per sqrt(minute); requires a window of at least 3 minutes (>= 3 returns), else null.
    """
    if w.height == 0:
        return w
    st = states.select(pl.Series("t", E.state_times(states)), "bid1_px", "ask1_px", "bid1_qty", "ask1_qty", "flags")
    rows = []
    for r in w.iter_rows(named=True):
        a, b = r["start_us"], r["end_us"]
        s = st.filter(pl.col("t").is_between(a, b) & ((pl.col("flags") & E.BBO_INVALID) == 0))
        tr = trades.filter(pl.col("exch_us").is_between(a, b))
        mid = ((s["bid1_px"] + s["ask1_px"]) / 2).to_numpy()
        ts = s["t"].to_numpy()
        spread = (s["ask1_px"] - s["bid1_px"]).to_numpy() / tick
        twa = None
        if len(ts) and b > ts[0]:
            dur = np.diff(np.append(ts, b)).astype(float)
            twa = float(np.sum(spread * dur) / np.sum(dur)) if np.sum(dur) > 0 else None
        rv = None
        if len(ts) > 1 and (b - a) >= 180e6:
            grid = np.arange(a, b + 1, 60_000_000)
            idx = np.searchsorted(ts, grid, side="right") - 1
            m = mid[idx[idx >= 0]]
            if len(m) >= 4:
                rv = float(np.std(np.diff(np.log(m)), ddof=1) * 1e4)
        rows.append({
            "trades": int(tr.height),
            "notional_quote": float((tr["price"] * tr["qty"]).sum()) if tr.height else 0.0,
            "twa_spread_ticks": twa,
            "event_mean_spread_ticks": float(np.mean(spread)) if s.height else None,
            "n_valid_states": int(s.height),
            "median_touch_qty": float(np.median(np.concatenate([s["bid1_qty"].to_numpy(), s["ask1_qty"].to_numpy()]))) if s.height else None,
            "mid_first": float(mid[0]) if len(mid) else None,
            "rv_1min_bp": rv,
        })
    return pl.concat([w, pl.DataFrame(rows, schema_overrides={k: pl.Float64 for k in (
        "twa_spread_ticks", "event_mean_spread_ticks", "median_touch_qty", "mid_first", "rv_1min_bp")} | {"n_valid_states": pl.Int64})],
        how="horizontal")


def validity_windows(t_all: np.ndarray, flags: np.ndarray, silent_iv: list[tuple[int, int]],
                     gaps_iv: list[tuple[int, int]], kind: np.ndarray) -> tuple[pl.DataFrame, pl.DataFrame]:
    """Book layer = runs of BBO-valid messages, broken at every resynchronization snapshot, minus silence cuts
    [trade, next depth event); joint layer = book layer minus closed intervals around missing exchange trades.

    A run ends at its last valid message (conservative). A snapshot after the first message marks a vendor reconnect:
    the time between the last pre-gap message and the snapshot is unobserved, so a new run always starts at the
    snapshot even when the pre-gap state was valid (fix of 2026-10-19; previously such gaps were spanned)."""
    resync = (kind == SNAPSHOT) & (np.arange(kind.shape[0]) > 0)
    runs = C.windows(t_all, (flags & E.BBO_INVALID) == 0, break_before=resync)
    book_w = C.subtract_intervals(runs, silent_iv, t_all)
    joint_w = C.subtract_intervals(book_w, [(a, b + 1) for a, b in gaps_iv], t_all)
    return book_w, joint_w


def missing_trade_intervals(missing: pl.DataFrame, present: pl.DataFrame, day: tuple[int, int]) -> list[tuple[int, int]]:
    """Each run of missing trade ids -> [time of last present trade before it, time of first present trade after it].

    A run before the first (after the last) present trade extends to the start (end) of the exchange day ``day``, so
    missing trades at the edges of a vendor file are never left inside the joint layer."""
    if missing.height == 0:
        return []
    ids = missing.sort("trade_id")
    runs = (ids.with_columns((pl.col("trade_id").diff().fill_null(2) != 1).cum_sum().alias("run"))
            .group_by("run", maintain_order=True).agg(pl.col("trade_id").min().alias("a"), pl.col("trade_id").max().alias("b"))
            .sort("a"))
    p = present.sort("trade_id")
    pid, pt = p["trade_id"].to_numpy(), p["exch_us"].to_numpy()
    out = []
    for a, b in runs.select("a", "b").iter_rows():
        i = np.searchsorted(pid, a) - 1
        j = np.searchsorted(pid, b, side="right")
        out.append((int(pt[i]) if i >= 0 else int(day[0]), int(pt[j]) if j < len(pt) else int(day[1])))
    return out


def vendor_quotes_agreement(sym: str, day: str, states: pl.DataFrame) -> dict:
    """Compare engine BBO with Tardis' own derived ``quotes`` at identical message timestamps (engine correctness)."""
    q = pl.read_csv(RAW / f"tardis/binance/quotes/{day}/{sym}.csv.gz",
                    columns=["timestamp", "local_timestamp", "ask_amount", "ask_price", "bid_price", "bid_amount"])
    s = states.select(pl.coalesce("exch_us", "local_us").alias("timestamp"), pl.col("local_us").alias("local_timestamp"),
                      pl.col("raw_bid_px").alias("bid1_px"), pl.col("raw_bid_qty").alias("bid1_qty"),
                      pl.col("raw_ask_px").alias("ask1_px"), pl.col("raw_ask_qty").alias("ask1_qty"), "flags")
    s = s.unique(subset=["timestamp", "local_timestamp"], keep="last", maintain_order=True)
    j = q.join(s, on=["timestamp", "local_timestamp"], how="left")
    found = j.filter(pl.col("bid1_px").is_not_null())
    eq = found.filter((pl.col("bid_price") == pl.col("bid1_px")) & (pl.col("ask_price") == pl.col("ask1_px"))  # same decimal doubles
                      & (pl.col("bid_amount") == pl.col("bid1_qty")) & (pl.col("ask_amount") == pl.col("ask1_qty")))
    return {"vendor_quote_rows": int(q.height), "matched_to_message": int(found.height),
            "exact_bbo_and_size_agreement": int(eq.height),
            "agreement_rate": float(eq.height / max(found.height, 1))}


def run_tardis_day(sym: str, day: str, cfg: dict, inst: dict) -> tuple[dict, pl.DataFrame]:
    tick, lot = inst["tick_size"], inst["lot_size"]
    book = pl.read_parquet(normalized_path("tardis", sym, "book", day))
    trades = pl.read_parquet(normalized_path("tardis", sym, "trades", day))
    ref = pl.read_parquet(normalized_path("binance_vision", sym, "trades", day))
    rep = {"source": "tardis", "symbol": sym, "day": day,
           "raw_files": read_meta(normalized_path("tardis", sym, "book", day))["raw_files"]
           + read_meta(normalized_path("tardis", sym, "trades", day))["raw_files"]
           + read_meta(normalized_path("binance_vision", sym, "trades", day))["raw_files"]}
    rep["normalized_inputs_sha256"] = {str(p.relative_to(ROOT)): sha256_file(p) for p in (
        normalized_path("tardis", sym, "book", day), normalized_path("tardis", sym, "trades", day),
        normalized_path("binance_vision", sym, "trades", day))}
    rep["grid_book"] = C.grid_audit(book, tick, lot)
    rep["grid_trades"] = C.grid_audit(trades, tick, lot)
    rep["grid_reference_trades"] = C.grid_audit(ref, tick, lot)
    rep["ordering"] = C.book_ordering_audit(book)

    snaps = book.filter(pl.col("kind") == 0).group_by("msg", maintain_order=True).agg(
        pl.col("local_us").first(), pl.len().alias("rows"), (pl.col("qty") > 0).sum().alias("nonzero_rows"))
    resync_msgs = [int(m) for m in snaps["msg"].to_list() if m > 0]
    dump_after = sorted(set([m - 1 for m in resync_msgs] + resync_msgs))
    band = cfg["replay"]["grid_band"]
    grid = (ref["price"].min() * (1 - band), ref["price"].max() * (1 + band))
    r = E.replay(book, tick=tick, grid_px=grid, n_levels=cfg["replay"]["n_levels"],
                 complete_below=cfg["replay"]["complete_below"], proven_levels=cfg["replay"]["proven_levels"],
                 dump_after=dump_after)
    st = r.states
    flags = st["flags"].to_numpy()
    rep["replay_counters"] = r.counters
    rep["flags"] = flag_summary(flags)
    rep["snapshots"] = [{"msg": int(m), "local_time": str(dt.datetime.fromtimestamp(t / 1e6, dt.UTC)), "rows": int(n), "nonzero_rows": int(z)}
                        for m, t, n, z in snaps.select("msg", "local_us", "rows", "nonzero_rows").iter_rows()]
    rep["engine_vs_vendor_quotes"] = vendor_quotes_agreement(sym, day, st)

    # resync comparisons: replayed book immediately before vs the fresh exchange snapshot
    dumps = {d.msg: d for d in r.dumps}
    t_all = E.state_times(st)
    raw_t = st.select(pl.coalesce("exch_us", "local_us")).to_series().to_numpy()
    rep["raw_time_regressions"] = int(np.count_nonzero(np.diff(raw_t) < 0))  # absorbed by engine.state_times
    d0, d1 = day_bounds_us(day)
    boundary = trades.filter(~pl.col("exch_us").is_between(d0, d1))  # vendor files split by receive time
    tr_audit, missing = C.trade_audit(trades.filter(pl.col("exch_us").is_between(d0, d1)), ref)
    tr_audit["vendor_trades_outside_exchange_day"] = int(boundary.height)
    rep["trades"] = tr_audit
    resyncs = []
    for m in resync_msgs:
        before, snap = dumps.get(m - 1), dumps.get(m)
        cmp = C.compare_books(before, snap, tick) if before is not None and snap is not None else {"comparable": False}
        if cmp.get("comparable"):
            raw = C.compare_books(before, snap, tick, proven_only=False)
            cmp["unrestricted"] = {k: raw[k] for k in ("levels", "match", "qty_diff", "only_replay", "only_snapshot")}
        t_prev, t_snap = int(t_all[m - 1]), int(st["local_us"][m])
        miss = missing.filter(pl.col("exch_us").is_between(t_prev - 60_000_000, t_snap))
        resyncs.append({"msg": m, "snapshot_local_time": str(dt.datetime.fromtimestamp(t_snap / 1e6, dt.UTC)),
                        "gap_last_diff_to_snapshot_ms": (t_snap - t_prev) / 1000, "missing_trades_near": int(miss.height),
                        "pre_resync_flags_valid": bool((flags[m - 1] & E.BBO_INVALID) == 0), **cmp})
    rep["resyncs"] = resyncs

    align, silent = C.trade_book_alignment(st, ref, cfg["rules"]["silence_s"])
    rep["trade_book_alignment_vs_exchange_trades"] = align
    rep["proven_vs_unproven_touch_consistency"] = C.proven_vs_unproven_consistency(st, ref)
    an = st.filter(pl.col("kind") == 0)
    rep["proven_region_halfwidth_bps_at_anchors"] = {
        "bid": ((an["raw_bid_px"] - an["bid_floor_px"]) / an["raw_bid_px"] * 1e4).round(1).to_list(),
        "ask": ((an["ask_ceil_px"] - an["raw_ask_px"]) / an["raw_ask_px"] * 1e4).round(1).to_list()}
    rep["day_price_range_bps"] = float((ref["price"].max() - ref["price"].min()) / ref["price"].min() * 1e4)

    # ---- validity layers (time intervals on the exchange clock; conservative: a run of valid messages ends at its
    # last message and every resync snapshot starts a new run, so the unobserved time between a last pre-gap message
    # and a resync snapshot is never counted)
    silent_iv = [(int(a), int(b)) for a, b in zip(silent["start_us"].to_list(), silent["end_us"].to_list())]
    gaps_iv = missing_trade_intervals(missing, trades, (d0, d1))
    book_w, joint_w = validity_windows(t_all, flags, silent_iv, gaps_iv, st["kind"].to_numpy())
    rep["invalid_intervals"] = {"book_silence": [list(x) for x in silent_iv], "trade_record_gaps": [list(x) for x in gaps_iv]}
    rep["trade_depth_linkage"] = C.trade_depth_linkage(book, ref, book_w)
    wins = []
    for layer, w in (("book", book_w), ("joint", joint_w)):
        wins.append(window_stats(w, st, ref, tick).with_columns(pl.lit(layer).alias("layer")))
    W = pl.concat(wins, how="diagonal_relaxed").with_columns(
        pl.lit("tardis").alias("source"), pl.lit(sym).alias("symbol"), pl.lit(day).alias("day"))
    for layer in ("book", "joint"):
        wl = W.filter(pl.col("layer") == layer)
        rep[f"coverage_{layer}"] = {
            "windows": int(wl.height), "covered_hours": float(wl["duration_s"].sum() / 3600),
            "day_fraction": float(wl["duration_s"].sum() / 86400),
            "longest_window_h": float(wl["duration_s"].max() / 3600) if wl.height else 0.0,
            "usable_windows_ge_min": int(wl.filter(pl.col("duration_s") >= cfg["rules"]["min_usable_window_s"]).height),
            "usable_hours_ge_min": float(wl.filter(pl.col("duration_s") >= cfg["rules"]["min_usable_window_s"])["duration_s"].sum() / 3600),
        }
    rep["decision"] = decide_tardis_day(rep, cfg)
    W = W.with_columns(pl.lit(rep["decision"]["status"]).alias("integrity_status"))
    DERIVED.mkdir(parents=True, exist_ok=True)
    st.select("msg", "kind", "exch_us", "local_us", "flags", "bid1_px", "bid1_qty", "ask1_px", "ask1_qty",
              "bid_floor_px", "ask_ceil_px", "raw_bid_px", "raw_ask_px").write_parquet(DERIVED / f"tardis_{sym}_{day}_bbo.parquet", compression="zstd")
    return rep, W


def decide_tardis_day(rep: dict, cfg: dict) -> dict:
    """Pre-declared integrity rules for a Tardis symbol-day (DATA_SPEC Acceptance Test 001).

    ``accepted`` means the day's data passed the integrity checks and has some valid joint coverage; it says nothing
    about how much of the day is usable. Analysis eligibility is a separate, explicitly dated rule
    (configs/eligibility_v1.toml, ``eligibility()``)."""
    fails, notes = [], []
    for k in ("grid_book", "grid_trades", "grid_reference_trades"):
        if not C.grid_ok(rep[k]):
            fails.append(f"{k}: values off the instrument grid or invalid")
    o = rep["ordering"]
    if o.get("local_time_regressions", 0):
        fails.append("capture-order (local) timestamp regressions")
    if o.get("exch_time_regressions", 0):
        notes.append(f"{o['exch_time_regressions']} exchange-time regressions among diffs")
    if o.get("duplicate_levels_within_message", 0):
        fails.append("duplicate price levels inside a message")
    if rep["engine_vs_vendor_quotes"]["agreement_rate"] < cfg["rules"]["min_engine_vendor_bbo_agreement"]:
        fails.append("engine does not reproduce the vendor-derived top of book")
    t = rep["trades"]
    if t["field_mismatch_price"] or t["field_mismatch_qty"] or t["field_mismatch_aggressor"] or t["extra_vs_reference"]:
        fails.append("trade fields disagree with the exchange archive")
    if t["missing_vs_reference"]:
        notes.append(f"{t['missing_vs_reference']} exchange trades absent from the vendor trade file (joint layer excludes them)")
    f = rep["flags"]
    for k in ("crossed", "locked", "off_grid"):
        if f.get(k):
            notes.append(f"{f[k]} messages {k} (invalidated until next snapshot)")
    if f.get("top_unknown"):
        notes.append(f"{f['top_unknown']} messages with touch outside the snapshot-proven region (excluded)")
    for r in rep["resyncs"]:
        if r.get("comparable") and sum(r["only_replay"]):
            notes.append(f"resync {r['snapshot_local_time']}: {sum(r['only_replay'])} replayed levels absent from fresh snapshot")
    status = "rejected" if fails else ("accepted" if rep["coverage_joint"]["covered_hours"] > 0 else "rejected")
    if not fails and rep["coverage_joint"]["covered_hours"] == 0:
        fails.append("no valid joint coverage")
    return {"status": status, "failures": fails, "notes": notes}


def run_hf_month(sym: str, per: str, cfg: dict, inst: dict) -> tuple[dict, pl.DataFrame, pl.DataFrame]:
    tick, lot = inst["tick_size"], inst["lot_size"]
    book = pl.read_parquet(normalized_path("hf_lobstream", sym, "book", per))
    trades = pl.read_parquet(normalized_path("hf_lobstream", sym, "trades", per))
    rep = {"source": "hf_lobstream", "symbol": sym, "period": per,
           "raw_files": read_meta(normalized_path("hf_lobstream", sym, "book", per))["raw_files"]
           + read_meta(normalized_path("hf_lobstream", sym, "trades", per))["raw_files"]}
    rep["normalized_inputs_sha256"] = {str(p.relative_to(ROOT)): sha256_file(p) for p in (
        normalized_path("hf_lobstream", sym, "book", per), normalized_path("hf_lobstream", sym, "trades", per))}
    rep["grid_book"] = C.grid_audit(book, tick, lot)
    rep["grid_trades"] = C.grid_audit(trades, tick, lot)
    rep["ordering"] = C.book_ordering_audit(book)
    band = cfg["replay"]["grid_band"]
    grid = (trades["price"].min() * (1 - band), trades["price"].max() * (1 + band))
    r = E.replay(book, tick=tick, grid_px=grid, n_levels=1, complete_below=cfg["replay"]["complete_below"],
                 proven_levels=cfg["replay"]["proven_levels"], check_seq=True)
    st = r.states
    flags = st["flags"].to_numpy()
    rep["replay_counters"] = r.counters
    rep["flags"] = flag_summary(flags)
    # sequence census on diffs (independent of anchoring)
    diffs = st.filter(pl.col("kind") == 1).sort("seq_first")
    g = diffs["seq_first"] - diffs["seq_last"].shift(1) - 1
    dts = diffs["local_us"].diff()  # collector clock (crypto-lob-stream depth carries no exchange time)
    total_ids = int(diffs["seq_last"].max() - diffs["seq_first"].min() + 1)
    present_ids = int((diffs["seq_last"] - diffs["seq_first"] + 1).sum())
    span_s = float((diffs["local_us"].max() - diffs["local_us"].min()) / 1e6)
    rep["sequence_census"] = {
        "diff_messages": int(diffs.height), "sequence_breaks": int((g > 0).sum()), "overlaps": int((g < 0).sum()),
        "update_ids_present_fraction": present_ids / total_ids,
        "span_hours": span_s / 3600, "time_inside_breaks_hours": float(dts.filter(g > 0).sum() / 3.6e9),
        "time_retained_fraction": 1 - float(dts.filter(g > 0).sum() / 1e6) / span_s,
    }
    # contiguous capture blocks (sequence-continuous runs of diffs), independent of snapshot anchoring
    brk = np.concatenate([[True], (g.to_numpy()[1:] != 0)])
    blk = diffs.with_columns(pl.Series("blk", np.cumsum(brk))).group_by("blk").agg(
        pl.col("local_us").min().alias("start_us"), pl.col("local_us").max().alias("end_us"), pl.len().alias("n_msgs"))
    blk = blk.with_columns(((pl.col("end_us") - pl.col("start_us")) / 1e6).alias("duration_s"))
    rep["capture_blocks"] = {"blocks": int(blk.height), "median_block_min": float(blk["duration_s"].median() / 60),
                             "max_block_min": float(blk["duration_s"].max() / 60)}
    tr_audit, _ = C.trade_audit(trades)
    rep["trades"] = tr_audit
    t_all = st.select(pl.coalesce("exch_us", "local_us")).to_series().to_numpy()
    ok = (flags & E.BBO_INVALID) == 0
    w = C.windows(t_all, ok).with_columns(pl.lit("book").alias("layer"), pl.lit("hf_lobstream").alias("source"),
                                          pl.lit(sym).alias("symbol"), pl.lit(per).alias("day"))
    rep["coverage_book"] = {"windows": int(w.height), "covered_hours": float(w["duration_s"].sum() / 3600),
                            "longest_window_min": float(w["duration_s"].max() / 60) if w.height else 0.0}
    return rep, w, book


def rest_snapshot_check(sym: str, day: str, hf_book: pl.DataFrame, cfg: dict, inst: dict) -> list[dict]:
    """Compare the Tardis replay with crypto-lob-stream's independent REST snapshots taken on the same day.

    REST depth responses carry an update id but no exchange time; the collector timestamp is used to search the
    replay within a short window for the best-matching message (alignment uncertainty is reported, not hidden)."""
    tick = inst["tick_size"]
    d0, d1 = day_bounds_us(day)
    snaps = hf_book.filter((pl.col("kind") == 0) & pl.col("local_us").is_between(d0, d1))
    if snaps.height == 0:
        return []
    book = pl.read_parquet(normalized_path("tardis", sym, "book", day))
    ref = pl.read_parquet(normalized_path("binance_vision", sym, "trades", day))
    msgs = book.group_by("msg", maintain_order=True).agg(pl.coalesce("exch_us", "local_us").first().alias("t"))
    t = msgs["t"].to_numpy()
    before_s, after_s = cfg["rules"]["snapshot_align_window_s"]
    out = []
    for (m,), g in snaps.group_by(["msg"], maintain_order=True):
        ts = int(g["local_us"][0])
        cand = np.flatnonzero((t >= ts - before_s * 1e6) & (t <= ts + after_s * 1e6))
        if len(cand) == 0:
            out.append({"hf_snapshot_local_time": str(dt.datetime.fromtimestamp(ts / 1e6, dt.UTC)), "comparable": False})
            continue
        band = cfg["replay"]["grid_band"]
        r = E.replay(book, tick=tick, grid_px=(ref["price"].min() * (1 - band), ref["price"].max() * (1 + band)),
                     n_levels=1, proven_levels=cfg["replay"]["proven_levels"], dump_after=cand.tolist())
        g_ticks, _ = E.to_ticks(g["price"].to_numpy(), tick)
        sd = g.with_columns(pl.Series("pt", g_ticks))
        snapdump = E.BookDump(-1, 0, 0, 0,
                              sd.filter(pl.col("side") == 1).sort("pt", descending=True).select("pt", "qty").to_numpy(),
                              sd.filter(pl.col("side") == -1).sort("pt").select("pt", "qty").to_numpy())
        best = None
        profile = []
        for d in r.dumps:
            c = C.compare_books(d, snapdump, tick)
            mism = sum(c["qty_diff"]) + sum(c["only_replay"]) + sum(c["only_snapshot"])
            profile.append((float((t[d.msg] - ts) / 1000), int(mism)))
            if best is None or mism < best[0]:
                best = (mism, d, c)
        mism, d, c = best
        at_min = [o for o, k in profile if k == mism]
        c["alignment"] = {
            "candidates_at_minimum": len(at_min), "minimum_offsets_ms": [min(at_min), max(at_min)],
            "mismatch_by_candidate_quantiles": [int(np.quantile([k for _, k in profile], q)) for q in (0.0, 0.5, 1.0)],
            "note": "best match selected by search; equality at the minimum does not identify a unique snapshot instant"}
        raw = C.compare_books(d, snapdump, tick, proven_only=False)
        c["unrestricted"] = {k: raw[k] for k in ("levels", "match", "qty_diff", "only_replay", "only_snapshot")}
        out.append({"hf_snapshot_local_time": str(dt.datetime.fromtimestamp(ts / 1e6, dt.UTC)),
                    "hf_snapshot_last_update_id": int(g["seq_last"][0]),
                    "candidates_searched": int(len(cand)),
                    "best_match_offset_ms": float((t[d.msg] - ts) / 1000),
                    "best_match_replay_flags_valid": bool((d.flags & E.BBO_INVALID) == 0),
                    "mismatched_levels": int(mism), **c})
    return out


def eligibility(rep: dict, rule: dict) -> dict:
    """Analysis eligibility under configs/eligibility_v1.toml (declared after Test 001 coverage was seen)."""
    cj = rep["coverage_joint"]
    e001 = rep["decision"]["status"] == "accepted" and cj["covered_hours"] >= rule["e001_min_joint_hours"]
    return {"rule": "eligibility_v1", "declared": rule["declared"], "declared_after_coverage_seen": True,
            "e001_eligible": bool(e001), "joint_hours": cj["covered_hours"],
            "simulation_hours_in_windows_ge_min": cj["usable_hours_ge_min"]}


def main() -> int:
    require_clean()
    cfg = tomllib.loads((ROOT / "configs" / "acceptance_001.toml").read_text())
    elig = tomllib.loads((ROOT / "configs" / "eligibility_v1.toml").read_text())
    inst = instruments()
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"test_id": cfg["test_id"], "run_at_utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
               "provenance": provenance(["configs/acceptance_001.toml", "configs/instruments.toml", "configs/eligibility_v1.toml"]),
               "code_fingerprint": code_fingerprint(), "config": cfg, "eligibility_rule": elig,
               "tardis": [], "hf_lobstream": [], "cross_capture": [], "rest_snapshot_checks": [], "reference_trades": []}
    all_w = []
    t0 = time.time()
    for sym in cfg["symbols"]:
        for day in sorted(cfg["tardis_days"] + cfg.get("extended_days", {}).get(sym, [])):
            rep, w = run_tardis_day(sym, day, cfg, inst[sym])
            rep["eligibility"] = eligibility(rep, elig)
            summary["tardis"].append(rep)
            all_w.append(w)
            print(f"[{time.time() - t0:6.0f}s] tardis {sym} {day}: {rep['decision']['status']} bbo_valid={rep['flags']['bbo_valid_fraction']:.4f} "
                  f"book={rep['coverage_book']['day_fraction']:.4f} joint={rep['coverage_joint']['day_fraction']:.4f} "
                  f"link={rep['trade_depth_linkage']['linkage_rate_two_events']:.5f}", flush=True)
            ref = pl.read_parquet(normalized_path("binance_vision", sym, "trades", day))
            a, _ = C.trade_audit(ref)
            summary["reference_trades"].append({"symbol": sym, "day": day, **a})
        for per in cfg["hf_periods"]:
            rep, w, hf_book = run_hf_month(sym, per, cfg, inst[sym])
            summary["hf_lobstream"].append(rep)
            all_w.append(w)
            print(f"[{time.time() - t0:6.0f}s] hf {sym} {per}: ids_present={rep['sequence_census']['update_ids_present_fraction']:.4f} "
                  f"valid_hours={rep['coverage_book']['covered_hours']:.2f}", flush=True)
            for day in cfg["cross_capture_days"]:
                if not day.startswith(per):
                    continue
                d0, d1 = day_bounds_us(day)
                tb = pl.read_parquet(normalized_path("tardis", sym, "book", day))
                cc, unmatched = C.cross_capture(hf_book, tb, d0, d1, max_lag_s=cfg["rules"]["cross_capture_max_lag_s"])
                summary["cross_capture"].append({"symbol": sym, "day": day, **cc,
                                                 "unmatched_examples": unmatched.head(20).to_dicts()})
                for chk in rest_snapshot_check(sym, day, hf_book, cfg, inst[sym]):
                    summary["rest_snapshot_checks"].append({"symbol": sym, "day": day, **chk})
                print(f"[{time.time() - t0:6.0f}s] cross-capture {sym} {day}: match={cc.get('match_rate')} "
                      f"runs={cc.get('runs_reproduced_unbroken')}/{cc.get('reference_contiguous_runs')} "
                      f"realign={cc.get('realignments_within_runs')}", flush=True)
            del hf_book
            for per_day in [d for d in ("2026-06-15", "2026-07-15", "2026-08-15") if d.startswith(per)]:
                ref = pl.read_parquet(normalized_path("binance_vision", sym, "trades", per_day))
                hf_tr = pl.read_parquet(normalized_path("hf_lobstream", sym, "trades", per))
                d0, d1 = day_bounds_us(per_day)
                a, _ = C.trade_audit(ref)
                summary["reference_trades"].append({"symbol": sym, "day": per_day, **a})
                hf_day = hf_tr.filter(pl.col("exch_us").is_between(d0, d1))
                ha, _ = C.trade_audit(hf_day, ref.join(hf_day.select("trade_id"), on="trade_id", how="semi"))
                summary.setdefault("hf_trade_field_checks", []).append({"symbol": sym, "day": per_day,
                                                                        "hf_trades_in_day": int(hf_day.height),
                                                                        "reference_trades_in_day": int(ref.height), **ha})
    W = pl.concat(all_w, how="diagonal_relaxed")
    W = W.with_columns(
        pl.from_epoch("start_us", time_unit="us").alias("start_utc"), pl.from_epoch("end_us", time_unit="us").alias("end_utc"))
    W.write_csv(OUT / "windows.csv")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, default=str))
    print(f"done in {time.time() - t0:.0f}s -> {OUT}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
