"""Data-quality checks used by Dataset Acceptance Test 001.

Every function is pure: it takes normalized frames / replay results and returns plain dicts or frames,
so each check is independently testable and its evidence can be serialized into the acceptance report.
Time is exchange time (``exch_us``) unless stated; snapshot messages, which carry no exchange time, are
placed on the collector clock (``local_us``).
"""

from __future__ import annotations

import numpy as np
import polars as pl

from lpx.book import engine as E


def event_time(states: pl.DataFrame) -> pl.Expr:
    return pl.coalesce(pl.col("exch_us"), pl.col("local_us"))


# --------------------------------------------------------------------------- field-level audits


def grid_audit(df: pl.DataFrame, tick: float, lot: float, tol: float = 1e-6) -> dict:
    """Prices on the tick grid, quantities on the lot grid, no NaN/negative values."""
    px = df["price"].to_numpy()
    q = df["qty"].to_numpy()
    xp = px / tick
    xq = q / lot
    return {
        "rows": int(df.height),
        "nan_price": int(np.isnan(px).sum()),
        "nan_qty": int(np.isnan(q).sum()),
        "nonpositive_price": int((px <= 0).sum()),
        "negative_qty": int((q < 0).sum()),
        "off_tick_price": int((np.abs(xp - np.rint(xp)) > tol).sum()),
        "off_lot_qty": int((np.abs(xq - np.rint(xq)) > tol * np.maximum(1.0, np.abs(xq))).sum()),
    }


def grid_ok(a: dict) -> bool:
    return all(a[k] == 0 for k in ("nan_price", "nan_qty", "nonpositive_price", "negative_qty", "off_tick_price", "off_lot_qty"))


def book_ordering_audit(book: pl.DataFrame) -> dict:
    """Capture-order and exchange-time monotonicity, duplicate levels within a message."""
    msgs = book.group_by("msg", maintain_order=True).agg(
        pl.col("kind").first(), pl.col("exch_us").first(), pl.col("local_us").first(), pl.col("seq_first").first(),
        pl.col("seq_last").first(), pl.len().alias("n"), pl.struct("side", "price").n_unique().alias("n_levels"))
    diffs = msgs.filter(pl.col("kind") == 1)
    out = {"messages": int(msgs.height), "snapshot_messages": int(msgs.height - diffs.height)}
    lt = msgs["local_us"].drop_nulls()
    if lt.len():
        d = lt.diff().drop_nulls()
        out["local_time_regressions"] = int((d < 0).sum())
    et = diffs["exch_us"].drop_nulls()
    d = et.diff().drop_nulls()
    out["exch_time_regressions"] = int((d < 0).sum())
    out["exch_time_max_regression_us"] = int(-d.min()) if d.len() and d.min() < 0 else 0
    out["equal_exch_time_consecutive_diffs"] = int((d == 0).sum())
    out["duplicate_levels_within_message"] = int((msgs["n"] - msgs["n_levels"]).sum())
    if diffs["seq_first"].null_count() == 0 and diffs.height:
        sf, sl = diffs["seq_first"], diffs["seq_last"]
        out["seq_first_gt_last"] = int((sf > sl).sum())
        out["seq_nonmonotone"] = int((sf.diff().drop_nulls() <= 0).sum())
    return out


# --------------------------------------------------------------------------- trades


def trade_audit(cand: pl.DataFrame, ref: pl.DataFrame | None = None) -> tuple[dict, pl.DataFrame]:
    """Internal id continuity, and (if ``ref`` given) completeness/field agreement against a reference record.

    Returns (summary, missing) where ``missing`` lists reference trades absent from ``cand`` (empty without ref).
    """
    c = cand.sort("trade_id")
    ids = c["trade_id"]
    jumps = ids.diff().drop_nulls()
    out = {
        "trades": int(c.height),
        "first_id": int(ids.min()), "last_id": int(ids.max()),
        "duplicate_ids": int(c.height - ids.n_unique()),
        "internal_id_gaps": int((jumps > 1).sum()),
        "internal_missing_ids": int((jumps.filter(jumps > 1) - 1).sum()),
        "exch_time_regressions_in_id_order": int((c["exch_us"].diff().drop_nulls() < 0).sum()),
    }
    if c["local_us"].null_count() < c.height:
        lat = (c["local_us"] - c["exch_us"]).drop_nulls()
        out["receipt_latency_ms_quantiles"] = {str(q): float(lat.quantile(q) / 1000) for q in (0.01, 0.5, 0.99, 0.999)}
        out["receipt_latency_ms_max"] = float(lat.max() / 1000)
    missing = pl.DataFrame()
    if ref is not None:
        r = ref
        j = r.join(c, on="trade_id", how="left", suffix="_c")
        present = j.filter(pl.col("exch_us_c").is_not_null())
        missing = j.filter(pl.col("exch_us_c").is_null()).select("trade_id", "exch_us", "price", "qty", "aggressor")
        extra = c.join(r, on="trade_id", how="anti")
        out.update({
            "reference_trades": int(r.height),
            "missing_vs_reference": int(missing.height),
            "extra_vs_reference": int(extra.height),
            "field_mismatch_price": int((present["price"] != present["price_c"]).sum()),
            "field_mismatch_qty": int((present["qty"] != present["qty_c"]).sum()),
            "field_mismatch_aggressor": int((present["aggressor"] != present["aggressor_c"]).sum()),
            # candidate clocks may be truncated (e.g. ms); report the offset range rather than assuming equality
            "time_offset_us_min": int((present["exch_us_c"] - present["exch_us"]).min()) if present.height else None,
            "time_offset_us_max": int((present["exch_us_c"] - present["exch_us"]).max()) if present.height else None,
            "completeness": float(present.height / r.height) if r.height else None,
        })
    return out, missing


# --------------------------------------------------------------------------- book vs trades


def trade_book_alignment(states: pl.DataFrame, trades: pl.DataFrame, silence_s: float) -> tuple[dict, pl.DataFrame]:
    """Consistency of executed trades with the replayed book, on the exchange clock.

    * pre-trade state: last diff with ``exch_us < T`` (Binance depth events batch changes up to ``E``).
    * a buyer-initiated trade below the pre-trade best ask (or seller-initiated above the best bid) executed
      inside the replayed spread: either a sub-batch order that never appeared in a depth event, or a book error.
    * silence: time from a trade to the next depth event; every execution changes a resting level, so a long
      silence after a trade indicates missing book data. Returns (summary, silent_intervals).
    """
    s = states.filter(pl.col("kind") == 1).select(
        pl.col("exch_us").alias("t"), "flags", "bid1_px", "ask1_px").sort("t")
    tr = trades.select(pl.col("exch_us").alias("T"), "price", "aggressor", "trade_id").sort("T")
    pre = tr.join_asof(s, left_on="T", right_on="t", strategy="backward", allow_exact_matches=False)
    nxt = tr.join_asof(s.select(pl.col("t").alias("t_next")), left_on="T", right_on="t_next", strategy="forward")
    valid = pre.filter(pl.col("t").is_not_null() & ((pl.col("flags") & E.BBO_INVALID) == 0))
    buys = valid.filter(pl.col("aggressor") == 1)
    sells = valid.filter(pl.col("aggressor") == -1)
    inside_buy = buys.filter(pl.col("price") < pl.col("ask1_px") - 1e-9)
    inside_sell = sells.filter(pl.col("price") > pl.col("bid1_px") + 1e-9)
    through_buy = buys.filter(pl.col("price") <= pl.col("bid1_px") + 1e-9)  # bought at/below our best bid
    through_sell = sells.filter(pl.col("price") >= pl.col("ask1_px") - 1e-9)
    delay = (nxt["t_next"] - nxt["T"]).cast(pl.Float64) / 1e6
    d = delay.drop_nulls()
    silent = nxt.with_columns(delay.alias("delay_s")).filter(pl.col("delay_s") > silence_s).select(
        "trade_id", pl.col("T").alias("start_us"), pl.col("t_next").alias("end_us"), "delay_s")
    out = {
        "trades": int(tr.height),
        "trades_with_valid_pre_state": int(valid.height),
        "buy_inside_replayed_spread": int(inside_buy.height),
        "sell_inside_replayed_spread": int(inside_sell.height),
        "inside_spread_rate": float((inside_buy.height + inside_sell.height) / max(valid.height, 1)),
        "trade_through_opposite_touch": int(through_buy.height + through_sell.height),
        "trade_through_rate": float((through_buy.height + through_sell.height) / max(valid.height, 1)),
        "next_depth_event_delay_s_quantiles": {str(q): float(d.quantile(q)) for q in (0.5, 0.99, 0.999, 1.0)} if d.len() else {},
        "silent_trades": int(silent.height),
        "silence_threshold_s": silence_s,
    }
    return out, silent


def proven_vs_unproven_consistency(states: pl.DataFrame, trades: pl.DataFrame) -> dict:
    """Empirical test of touches that lie outside the snapshot-proven region.

    For trades whose pre-trade book is anchored and uncrossed, compare the rate of executions strictly inside the
    engine's raw spread when the touch is proven versus unproven. An unknown resting level better than the replayed
    touch would surface as executions inside the replayed spread, so similar rates support (but do not prove) the
    unproven touches; a materially higher unproven rate rejects them."""
    hard = E.UNANCHORED | E.CROSSED | E.LOCKED | E.EMPTY_SIDE | E.OFF_GRID
    s = states.filter(pl.col("kind") == 1).select(pl.col("exch_us").alias("t"), "flags", "raw_bid_px", "raw_ask_px").sort("t")
    tr = trades.select(pl.col("exch_us").alias("T"), "price", "aggressor").sort("T")
    pre = tr.join_asof(s, left_on="T", right_on="t", strategy="backward", allow_exact_matches=False)
    pre = pre.filter(pl.col("t").is_not_null() & ((pl.col("flags") & hard) == 0))
    inside = ((pl.col("aggressor") == 1) & (pl.col("price") < pl.col("raw_ask_px") - 1e-9)) | (
        (pl.col("aggressor") == -1) & (pl.col("price") > pl.col("raw_bid_px") + 1e-9))
    pre = pre.with_columns(inside.alias("inside"), ((pl.col("flags") & E.TOP_UNKNOWN) != 0).alias("unproven"))
    out = {}
    for name, g in (("proven", pre.filter(~pl.col("unproven"))), ("unproven", pre.filter(pl.col("unproven")))):
        n = g.height
        k = int(g["inside"].sum()) if n else 0
        out[name] = {"trades": int(n), "inside_raw_spread": k, "rate": (k / n) if n else None}
    return out


# --------------------------------------------------------------------------- resync comparisons


def compare_books(replayed: E.BookDump, snapshot: E.BookDump, tick: float, buckets_bps=(1, 5, 25, 100),
                  proven_only: bool = True) -> dict:
    """Level-by-level comparison of a replayed book against an independent snapshot of (nearly) the same instant.

    Compared prices must lie inside both the snapshot's own covered range (a depth-limited snapshot is silent beyond
    it) and the replay's proven region (``bid_floor_tick``/``ask_ceil_tick``; the replay cannot vouch for levels
    beyond it). Levels outside the proven region are counted separately. Discrepancies are bucketed by distance from
    the snapshot mid in basis points.
    """
    sb, sa = snapshot.bids, snapshot.asks
    if len(sb) == 0 or len(sa) == 0:
        return {"comparable": False}
    mid = (sb[0, 0] + sa[0, 0]) / 2
    edges = np.array((0,) + tuple(buckets_bps) + (np.inf,))
    res = {"comparable": True, "snapshot_mid": float(mid * tick),
           "buckets_bps": [f"[{edges[i]},{edges[i+1]})" for i in range(len(edges) - 1)]}
    tot = {k: np.zeros(len(edges) - 1, np.int64) for k in ("levels", "match", "qty_diff", "only_replay", "only_snapshot")}
    outside = 0
    for rep, snp, is_bid in ((replayed.bids, sb, True), (replayed.asks, sa, False)):
        lo, hi = snp[:, 0].min(), snp[:, 0].max()
        lo_p, hi_p = lo, hi
        if proven_only and is_bid and replayed.bid_floor_tick:
            lo_p = max(lo, replayed.bid_floor_tick)
        if proven_only and not is_bid and replayed.ask_ceil_tick:
            hi_p = min(hi, replayed.ask_ceil_tick)
        r = {int(p): q for p, q in rep if lo_p <= p <= hi_p}
        s_ = {int(p): q for p, q in snp if lo_p <= p <= hi_p}
        outside += int(sum(1 for p, _ in snp if not (lo_p <= p <= hi_p)))
        for p in set(r) | set(s_):
            dist = abs(p - mid) / mid * 1e4
            b = int(np.searchsorted(edges, dist, side="right") - 1)
            tot["levels"][b] += 1
            if p in r and p in s_:
                if abs(r[p] - s_[p]) <= 1e-12 * max(1.0, s_[p]):
                    tot["match"][b] += 1
                else:
                    tot["qty_diff"][b] += 1
            elif p in r:
                tot["only_replay"][b] += 1
            else:
                tot["only_snapshot"][b] += 1
    res.update({k: v.tolist() for k, v in tot.items()})
    res["snapshot_levels_outside_replay_proven_region"] = outside
    rb, ra = replayed.bids, replayed.asks
    res["bbo_equal"] = bool(len(rb) and len(ra) and rb[0, 0] == sb[0, 0] and ra[0, 0] == sa[0, 0])
    res["touch_qty_equal"] = bool(res["bbo_equal"] and rb[0, 1] == sb[0, 1] and ra[0, 1] == sa[0, 1])
    return res


# --------------------------------------------------------------------------- windows


def windows(t_us: np.ndarray, ok: np.ndarray, min_s: float = 0.0, break_before: np.ndarray | None = None) -> pl.DataFrame:
    """Contiguous runs of ``ok`` messages -> [start_us, end_us] (end = time of the last valid message; conservative).

    ``break_before[i]`` forces a new run to start at message i even if message i-1 was valid — used at every vendor
    resynchronization snapshot, because the interval between the last pre-gap message and the snapshot is unobserved.
    """
    ok = ok.astype(bool)
    if not ok.any():
        return pl.DataFrame(schema={"start_us": pl.Int64, "end_us": pl.Int64, "n_msgs": pl.Int64, "duration_s": pl.Float64})
    start = ok & ~np.concatenate([[False], ok[:-1]])
    if break_before is not None:
        start |= ok & break_before.astype(bool)
    run = np.cumsum(start)
    idx = np.flatnonzero(ok)
    rid = run[idx]
    starts = idx[np.concatenate([[True], rid[1:] != rid[:-1]])]
    ends = idx[np.concatenate([rid[1:] != rid[:-1], [True]])]
    w = pl.DataFrame({"start_us": t_us[starts], "end_us": t_us[ends], "n_msgs": (ends - starts + 1).astype(np.int64)})
    w = w.with_columns(((pl.col("end_us") - pl.col("start_us")) / 1e6).alias("duration_s"))
    return w.filter(pl.col("duration_s") >= min_s)


def subtract_intervals(w: pl.DataFrame, cuts: list[tuple[int, int]], t_us: np.ndarray) -> pl.DataFrame:
    """Remove half-open cut intervals [a, b) from windows; recount messages per resulting window."""
    if not cuts or w.height == 0:
        return w
    cuts = sorted(cuts)
    out = []
    for s0, e0 in w.select("start_us", "end_us").iter_rows():
        segs = [(s0, e0)]
        for a, b in cuts:
            if b <= s0 or a > e0:
                continue
            nxt = []
            for x, y in segs:
                if b <= x or a > y:
                    nxt.append((x, y))
                    continue
                if a > x:
                    nxt.append((x, a - 1))
                if b <= y:
                    nxt.append((b, y))
            segs = nxt
        out.extend(segs)
    ts = np.sort(t_us)
    starts = np.array([a for a, _ in out], np.int64)
    ends = np.array([b for _, b in out], np.int64)
    n = np.searchsorted(ts, ends, side="right") - np.searchsorted(ts, starts, side="left")
    r = pl.DataFrame({"start_us": starts, "end_us": ends, "n_msgs": n.astype(np.int64)})
    return r.with_columns(((pl.col("end_us") - pl.col("start_us")) / 1e6).alias("duration_s")).filter(pl.col("end_us") > pl.col("start_us"))


def mask_intervals(t_us: np.ndarray, intervals: list[tuple[int, int]]) -> np.ndarray:
    """Boolean mask of messages whose time falls inside any closed interval."""
    order = np.argsort(t_us, kind="stable")  # message clocks can regress by ~ms around snapshots
    ts = t_us[order]
    hit = np.zeros(t_us.shape[0], bool)
    for a, b in intervals:
        hit[np.searchsorted(ts, a, side="left"):np.searchsorted(ts, b, side="right")] = True
    m = np.zeros(t_us.shape[0], bool)
    m[order] = hit
    return m


# --------------------------------------------------------------------------- cross-capture


def _msg_content(b: pl.DataFrame) -> pl.DataFrame:
    return (b.filter(pl.col("kind") == 1).sort(["msg", "side", "price"])
            .group_by("msg", maintain_order=True)
            .agg(pl.col("exch_us").first(), pl.col("local_us").first(), pl.col("seq_first").first(), pl.col("seq_last").first(),
                 pl.len().alias("n"),
                 pl.concat_str([pl.col("side"), pl.col("price"), pl.col("qty")], separator=":").str.join("|").alias("content")))


def cross_capture(ref_book: pl.DataFrame, cand_book: pl.DataFrame, t0_us: int, t1_us: int,
                  max_lag_s: float = 5.0) -> tuple[dict, pl.DataFrame]:
    """Independent-capture check of a candidate feed (no update ids; exchange clock) against a sequenced capture of the
    same exchange stream (update ids; collector clock).

    Reference diff messages (receive time in [t0, t1]) are grouped into runs with contiguous update ids
    (U == previous u + 1). Each run is aligned to the candidate's capture order: an anchor is any candidate message
    with identical content (multiset of side/price/qty) whose exchange time precedes the reference receive time by at
    most ``max_lag_s``; from the anchor, reference message k must equal candidate message anchor+k. The best anchor
    (longest exact consecutive agreement) is kept; after a divergence the remainder of the run is re-aligned. A complete
    candidate reproduces every run as one unbroken consecutive block.
    """
    ref = ref_book.filter(pl.col("local_us").is_between(t0_us, t1_us))
    r = _msg_content(ref).sort("seq_first")
    if r.height == 0:
        return {"reference_messages": 0}, pl.DataFrame()
    lo, hi = int(r["local_us"].min() - max_lag_s * 1e6), int(r["local_us"].max())
    c = _msg_content(cand_book.filter(pl.col("exch_us").is_between(lo, hi))).sort("msg")
    cc = c["content"].to_numpy()
    ce = c["exch_us"].to_numpy()
    pos: dict[str, list[int]] = {}
    for i, x in enumerate(cc):
        pos.setdefault(x, []).append(i)
    rc = r["content"].to_numpy()
    rl = r["local_us"].to_numpy()
    sf, sl = r["seq_first"].to_numpy(), r["seq_last"].to_numpy()
    brk = np.concatenate([[True], sf[1:] != sl[:-1] + 1])
    run_starts = np.flatnonzero(brk)
    run_ends = np.concatenate([run_starts[1:], [len(rc)]])
    aligned = np.zeros(len(rc), bool)
    lags = []
    divergences = 0
    runs_unbroken = 0
    for a, b in zip(run_starts, run_ends):
        k = a
        segments = 0
        while k < b:
            best_len, best_s = 0, -1
            for s0 in pos.get(rc[k], ()):
                lag = (rl[k] - ce[s0]) / 1e6
                if lag < -0.05 or lag > max_lag_s:
                    continue
                n = min(b - k, len(cc) - s0)
                eq = rc[k:k + n] == cc[s0:s0 + n]
                L = n if eq.all() else int(np.argmin(eq))
                if L > best_len:
                    best_len, best_s = L, s0
            if best_len == 0:
                k += 1  # reference message with no candidate counterpart
                continue
            aligned[k:k + best_len] = True
            lags.append((rl[k:k + best_len] - ce[best_s:best_s + best_len]) / 1e3)
            segments += 1
            k += best_len
        if segments == 1 and aligned[a:b].all():
            runs_unbroken += 1
        divergences += max(segments - 1, 0)
    lag = np.concatenate(lags) if lags else np.array([])
    out = {
        "reference_messages": int(len(rc)),
        "reference_contiguous_runs": int(len(run_starts)),
        "runs_reproduced_unbroken": int(runs_unbroken),
        "aligned_messages": int(aligned.sum()),
        "unaligned_messages": int((~aligned).sum()),
        "match_rate": float(aligned.mean()),
        "realignments_within_runs": int(divergences),
        "reference_receive_lag_ms_quantiles": {str(q): float(np.quantile(lag, q)) for q in (0.01, 0.5, 0.99)} if lag.size else {},
    }
    bad = r.with_columns(pl.Series("aligned", aligned)).filter(~pl.col("aligned")).select("msg", "seq_first", "seq_last", "local_us", "n")
    return out, bad.head(50)


def trade_depth_linkage(book: pl.DataFrame, trades: pl.DataFrame, valid_windows: pl.DataFrame) -> dict:
    """Every execution changes the maker's price level, so the first one or two depth events at or after an exchange
    trade should carry a row for (maker side, trade price). Measured on trades inside valid book windows only."""
    msgs = book.filter(pl.col("kind") == 1).group_by("msg", maintain_order=True).agg(pl.col("exch_us").first()).sort("exch_us")
    tr = trades.select("trade_id", pl.col("exch_us").alias("T"), "price", (-pl.col("aggressor")).cast(pl.Int8).alias("side"))
    if valid_windows.height:
        keep = np.zeros(tr.height, bool)
        T = tr["T"].to_numpy()
        for a, b in valid_windows.select("start_us", "end_us").iter_rows():
            keep |= (T >= a) & (T <= b)
        tr = tr.filter(pl.Series(keep))
    tr = tr.sort("T").join_asof(msgs.rename({"exch_us": "E"}), left_on="T", right_on="E", strategy="forward")
    tr = tr.filter(pl.col("msg").is_not_null())
    rows = book.filter(pl.col("kind") == 1).select("msg", "side", "price").unique()
    k1 = tr.join(rows, on=["msg", "side", "price"], how="semi")
    rest = tr.join(rows, on=["msg", "side", "price"], how="anti").with_columns((pl.col("msg") + 1).alias("msg"))
    k2 = rest.join(rows, on=["msg", "side", "price"], how="semi")
    n = max(tr.height, 1)
    return {"trades_checked": int(tr.height), "linked_next_event": int(k1.height), "linked_within_two_events": int(k1.height + k2.height),
            "linkage_rate_next_event": k1.height / n, "linkage_rate_two_events": (k1.height + k2.height) / n}
