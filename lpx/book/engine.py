"""Deterministic L2 order-book replay with explicit validity tracking.

The engine applies normalized book messages (``lpx.data.schema``) atomically and records, after every message,
the best bid/ask, the top ``n_levels`` per side, and a bit-mask of validity flags. It never repairs data:
a sequence gap, a crossed/locked book, or an unrepresentable level invalidates the book until the next
snapshot re-anchors it.

Snapshot-known region
---------------------
A depth-limited snapshot (e.g. 1000 levels per side) proves the full state of a side only *inside* the price
range it covers. The diff stream then reports changes, but levels outside that range that never change are
never observed. The engine therefore keeps, per side, the boundary of the region proven by the last anchor
(``bid_floor`` / ``ask_ceil``) and flags the book when its touch (``TOP_UNKNOWN``) or its top-N depth
(``DEPTH_PARTIAL``) extends beyond what the anchor proves. Optionally (``complete_below > 0``), a REST snapshot side
carrying fewer than ``complete_below`` levels is treated as the complete side; this is off by default because a
vendor's snapshot may merge buffered diffs into the exchange depth response. For the same reason the proven region
can be truncated to the ``proven_levels`` best levels of the snapshot (``0`` = the snapshot's full extent), so that
levels added beyond the exchange response while buffering cannot widen it.

Prices are integer ticks on a dense grid ``[grid_lo, grid_lo + grid_n)``. Bids below / asks above the grid are
deep levels that cannot reach the touch without first crossing the whole grid; they are counted and ignored.
Bids above / asks below the grid cannot be represented and invalidate the book (``OFF_GRID``).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import polars as pl
from numba import njit

from lpx.data.schema import BID, SNAPSHOT

# ---- validity flags (uint16 bit mask)
UNANCHORED = 1 << 0  # no anchor yet, or invalidated since the last snapshot
SEQ_GAP = 1 << 1  # this message's first update id skips past the previous message's last update id
CROSSED = 1 << 2  # best bid > best ask after this message
LOCKED = 1 << 3  # best bid == best ask after this message
EMPTY_SIDE = 1 << 4  # a side has no level inside the grid
TOP_UNKNOWN = 1 << 5  # touch lies outside the anchor-proven region; BBO unverifiable
DEPTH_PARTIAL = 1 << 6  # fewer than n_levels levels proven on a side (BBO may still be valid)
OFF_GRID = 1 << 7  # a level could not be represented on the price grid
STALE_SKIPPED = 1 << 8  # diff entirely covered by the anchor (u <= lastUpdateId); skipped per exchange procedure
IS_SNAPSHOT = 1 << 9  # message was a snapshot (anchor)
INVALIDATED = 1 << 10  # crossing/locking detected here; book unanchored until the next snapshot

BBO_INVALID = UNANCHORED | CROSSED | LOCKED | EMPTY_SIDE | TOP_UNKNOWN | OFF_GRID
FLAG_NAMES = {
    UNANCHORED: "unanchored", SEQ_GAP: "seq_gap", CROSSED: "crossed", LOCKED: "locked", EMPTY_SIDE: "empty_side",
    TOP_UNKNOWN: "top_unknown", DEPTH_PARTIAL: "depth_partial", OFF_GRID: "off_grid",
    STALE_SKIPPED: "stale_skipped", IS_SNAPSHOT: "snapshot", INVALIDATED: "invalidated",
}
COUNTER_NAMES = ("deep_rows_ignored", "off_grid_rows", "stale_msgs_skipped", "seq_gaps", "cross_invalidations",
                 "snapshots", "rows_applied", "absent_removals_in_region", "nonpositive_snapshot_rows",
                 "absent_removals_outside_region", "additions_outside_region")


@njit(cache=True)
def _replay(msg_ptr, kind, seq_first, seq_last, side, px, qty, grid_lo, grid_n, n_levels, complete_below,
            proven_levels, check_seq, dump_after, dump_k):
    M = msg_ptr.shape[0] - 1
    bidq = np.zeros(grid_n)
    askq = np.zeros(grid_n)
    bb = -1
    ba = grid_n
    anchored = False
    bid_floor = grid_n
    ask_ceil = -1
    prev_u = -1

    flags = np.zeros(M, np.uint16)
    bid_px = np.full((M, n_levels), -1, np.int64)
    ask_px = np.full((M, n_levels), -1, np.int64)
    bid_q = np.zeros((M, n_levels))
    ask_q = np.zeros((M, n_levels))
    floors = np.empty((M, 2), np.int64)
    raw = np.full((M, 2), -1, np.int64)  # engine best bid/ask ticks regardless of the proven region
    raw_q = np.zeros((M, 2))
    cnt = np.zeros(11, np.int64)

    D = dump_after.shape[0]
    d_bpx = np.full((D, dump_k), -1, np.int64)
    d_bq = np.zeros((D, dump_k))
    d_apx = np.full((D, dump_k), -1, np.int64)
    d_aq = np.zeros((D, dump_k))
    d_meta = np.zeros((D, 3), np.int64)  # flags, bid_floor_tick, ask_ceil_tick
    dp = 0

    for m in range(M):
        f = 0
        r0 = msg_ptr[m]
        r1 = msg_ptr[m + 1]
        if kind[m] == 0:  # SNAPSHOT
            bidq[:] = 0.0
            askq[:] = 0.0
            bb = -1
            ba = grid_n
            nb = 0
            na = 0
            bmin = grid_n
            amax = -1
            deep_b = False
            deep_a = False
            for r in range(r0, r1):
                idx = px[r] - grid_lo
                q = qty[r]
                if q <= 0.0:
                    cnt[8] += 1
                    continue
                if side[r] == 1:
                    nb += 1
                    if idx < 0:
                        deep_b = True
                        cnt[0] += 1
                        continue
                    if idx >= grid_n:
                        f |= 128
                        cnt[1] += 1
                        continue
                    bidq[idx] = q
                    if idx > bb:
                        bb = idx
                    if idx < bmin:
                        bmin = idx
                else:
                    na += 1
                    if idx >= grid_n:
                        deep_a = True
                        cnt[0] += 1
                        continue
                    if idx < 0:
                        f |= 128
                        cnt[1] += 1
                        continue
                    askq[idx] = q
                    if idx < ba:
                        ba = idx
                    if idx > amax:
                        amax = idx
            bid_floor = 0 if (deep_b or (complete_below > 0 and nb < complete_below)) else bmin
            ask_ceil = grid_n - 1 if (deep_a or (complete_below > 0 and na < complete_below)) else amax
            if proven_levels > 0:
                k = 0
                j = bb
                while j >= 0 and k < proven_levels:
                    if bidq[j] > 0.0:
                        k += 1
                        if k == proven_levels and j > bid_floor:
                            bid_floor = j
                    j -= 1
                k = 0
                j = ba
                while j < grid_n and k < proven_levels:
                    if askq[j] > 0.0:
                        k += 1
                        if k == proven_levels and j < ask_ceil:
                            ask_ceil = j
                    j += 1
            anchored = (f & 128) == 0
            prev_u = seq_last[m]
            f |= 512
            cnt[5] += 1
        else:
            apply = True
            if check_seq:
                U = seq_first[m]
                u = seq_last[m]
                if anchored and u <= prev_u:
                    f |= 256
                    cnt[2] += 1
                    apply = False
                elif prev_u >= 0 and U > prev_u + 1:
                    f |= 2
                    cnt[3] += 1
                    anchored = False
                if apply:
                    prev_u = u
            if apply:
                for r in range(r0, r1):
                    idx = px[r] - grid_lo
                    q = qty[r]
                    cnt[6] += 1
                    if side[r] == 1:
                        if idx < 0:
                            cnt[0] += 1
                            continue
                        if idx >= grid_n:
                            f |= 128
                            cnt[1] += 1
                            anchored = False
                            continue
                        if q <= 0.0:
                            if bidq[idx] == 0.0:
                                if idx >= bid_floor:
                                    cnt[7] += 1
                                else:
                                    cnt[9] += 1
                            bidq[idx] = 0.0
                            if idx == bb:
                                j = bb - 1
                                while j >= 0 and bidq[j] == 0.0:
                                    j -= 1
                                bb = j
                        else:
                            if idx < bid_floor:
                                cnt[10] += 1
                            bidq[idx] = q
                            if idx > bb:
                                bb = idx
                    else:
                        if idx >= grid_n:
                            cnt[0] += 1
                            continue
                        if idx < 0:
                            f |= 128
                            cnt[1] += 1
                            anchored = False
                            continue
                        if q <= 0.0:
                            if askq[idx] == 0.0:
                                if idx <= ask_ceil:
                                    cnt[7] += 1
                                else:
                                    cnt[9] += 1
                            askq[idx] = 0.0
                            if idx == ba:
                                j = ba + 1
                                while j < grid_n and askq[j] == 0.0:
                                    j += 1
                                ba = j
                        else:
                            if idx > ask_ceil:
                                cnt[10] += 1
                            askq[idx] = q
                            if idx < ba:
                                ba = idx

        # ---- post-message state checks
        if bb < 0 or ba >= grid_n:
            f |= 16
        else:
            if bb > ba:
                f |= 4
            elif bb == ba:
                f |= 8
            if (f & 12) != 0 and anchored:
                anchored = False
                f |= 1024
                cnt[4] += 1
            if bb < bid_floor or ba > ask_ceil:
                f |= 32
        if not anchored:
            f |= 1

        # ---- top-N inside the proven region
        k = 0
        j = bb
        while j >= 0 and j >= bid_floor and k < n_levels:
            if bidq[j] > 0.0:
                bid_px[m, k] = j + grid_lo
                bid_q[m, k] = bidq[j]
                k += 1
            j -= 1
        if k < n_levels:
            f |= 64
        k = 0
        j = ba
        while j < grid_n and j <= ask_ceil and k < n_levels:
            if askq[j] > 0.0:
                ask_px[m, k] = j + grid_lo
                ask_q[m, k] = askq[j]
                k += 1
            j += 1
        if k < n_levels:
            f |= 64
        flags[m] = f
        if bb >= 0:
            raw[m, 0] = bb + grid_lo
            raw_q[m, 0] = bidq[bb]
        if ba < grid_n:
            raw[m, 1] = ba + grid_lo
            raw_q[m, 1] = askq[ba]
        floors[m, 0] = bid_floor + grid_lo
        floors[m, 1] = ask_ceil + grid_lo

        # ---- full-depth dumps for cross-validation
        while dp < D and dump_after[dp] == m:
            k = 0
            j = bb
            while j >= 0 and k < dump_k:
                if bidq[j] > 0.0:
                    d_bpx[dp, k] = j + grid_lo
                    d_bq[dp, k] = bidq[j]
                    k += 1
                j -= 1
            k = 0
            j = ba
            while j < grid_n and k < dump_k:
                if askq[j] > 0.0:
                    d_apx[dp, k] = j + grid_lo
                    d_aq[dp, k] = askq[j]
                    k += 1
                j += 1
            d_meta[dp, 0] = f
            d_meta[dp, 1] = bid_floor + grid_lo
            d_meta[dp, 2] = ask_ceil + grid_lo
            dp += 1

    return flags, bid_px, bid_q, ask_px, ask_q, floors, raw, raw_q, cnt, d_bpx, d_bq, d_apx, d_aq, d_meta


@dataclass
class BookDump:
    msg: int
    flags: int
    bid_floor_tick: int
    ask_ceil_tick: int
    bids: np.ndarray  # (k, 2) [price_tick, qty], best first
    asks: np.ndarray


@dataclass
class ReplayResult:
    states: pl.DataFrame  # one row per message
    counters: dict
    tick: float
    grid: tuple[int, int]
    dumps: list[BookDump] = field(default_factory=list)


def tick_decimals(tick: float) -> int:
    r = repr(float(tick))
    return len(r.split(".")[1].rstrip("0")) if "." in r and "e" not in r else 12


def tick_to_price(ticks: np.ndarray, tick: float) -> np.ndarray:
    """Integer ticks -> the double nearest the decimal price (equal to a parsed decimal string)."""
    return np.round(ticks * tick, tick_decimals(tick))


def to_ticks(price: np.ndarray, tick: float, tol: float = 1e-6) -> tuple[np.ndarray, int]:
    """Convert prices to integer ticks; returns (ticks, number of prices off the tick grid)."""
    x = price / tick
    t = np.rint(x)
    off = int(np.count_nonzero(np.abs(x - t) > tol))
    return t.astype(np.int64), off


def replay(book: pl.DataFrame, *, tick: float, grid_px: tuple[float, float], n_levels: int = 10,
           complete_below: int = 0, proven_levels: int = 0, check_seq: bool = False, dump_after: list[int] | None = None,
           dump_k: int = 1000) -> ReplayResult:
    """Replay a normalized book frame (rows ordered by ``msg``) and return per-message states.

    ``grid_px``: (low, high) price bounds of the dense grid. ``check_seq`` enables exchange update-id
    continuity checks (requires ``seq_first``/``seq_last``). ``dump_after``: message ordinals after which the
    full book (up to ``dump_k`` levels per side) is captured.
    """
    msg = book["msg"].to_numpy()
    if msg.size and (np.any(np.diff(msg) < 0) or msg[0] != 0):
        raise ValueError("book rows must be ordered by msg starting at 0")
    M = int(msg[-1]) + 1 if msg.size else 0
    counts = np.bincount(msg, minlength=M)
    if np.any(counts == 0):
        raise ValueError("message ordinals must be contiguous")
    ptr = np.zeros(M + 1, np.int64)
    np.cumsum(counts, out=ptr[1:])
    first = ptr[:-1]

    ticks, off = to_ticks(book["price"].to_numpy(), tick)
    if off:
        raise ValueError(f"{off} prices are not on the {tick} tick grid")
    lo = int(np.floor(grid_px[0] / tick))
    hi = int(np.ceil(grid_px[1] / tick))
    kind = book["kind"].to_numpy()[first].astype(np.int8)
    sf = book["seq_first"].fill_null(-1).to_numpy()[first].astype(np.int64)
    sl = book["seq_last"].fill_null(-1).to_numpy()[first].astype(np.int64)
    if check_seq and np.any((sl < 0) & (kind != SNAPSHOT)):
        raise ValueError("check_seq requires update ids on every diff")
    side = book["side"].to_numpy().astype(np.int8)
    qty = book["qty"].to_numpy().astype(np.float64)
    dumps_idx = np.array(sorted(dump_after or []), np.int64)

    (flags, bpx, bq, apx, aq, floors, raw, raw_q, cnt, d_bpx, d_bq, d_apx, d_aq, d_meta) = _replay(
        ptr, kind, sf, sl, side, ticks, qty, lo, hi - lo + 1, n_levels, complete_below, proven_levels, check_seq,
        dumps_idx, dump_k)

    cols = {
        "msg": np.arange(M, dtype=np.int64),
        "kind": kind,
        "exch_us": book["exch_us"].gather(first),
        "local_us": book["local_us"].gather(first),
        "seq_first": book["seq_first"].gather(first),
        "seq_last": book["seq_last"].gather(first),
        "flags": flags,
        "bid_floor_px": tick_to_price(floors[:, 0], tick),
        "ask_ceil_px": tick_to_price(floors[:, 1], tick),
        # engine's best levels whatever their validity (diagnostics / engine-vs-vendor checks only)
        "raw_bid_px": np.where(raw[:, 0] >= 0, tick_to_price(raw[:, 0], tick), np.nan),
        "raw_bid_qty": raw_q[:, 0],
        "raw_ask_px": np.where(raw[:, 1] >= 0, tick_to_price(raw[:, 1], tick), np.nan),
        "raw_ask_qty": raw_q[:, 1],
    }
    for i in range(n_levels):
        cols[f"bid{i + 1}_px"] = np.where(bpx[:, i] >= 0, tick_to_price(bpx[:, i], tick), np.nan)
        cols[f"bid{i + 1}_qty"] = bq[:, i]
        cols[f"ask{i + 1}_px"] = np.where(apx[:, i] >= 0, tick_to_price(apx[:, i], tick), np.nan)
        cols[f"ask{i + 1}_qty"] = aq[:, i]
    states = pl.DataFrame(cols)
    dumps = []
    for d, m in enumerate(dumps_idx):
        nb = int(np.count_nonzero(d_bpx[d] >= 0))
        na = int(np.count_nonzero(d_apx[d] >= 0))
        dumps.append(BookDump(int(m), int(d_meta[d, 0]), int(d_meta[d, 1]), int(d_meta[d, 2]),
                              np.column_stack([d_bpx[d, :nb], d_bq[d, :nb]]), np.column_stack([d_apx[d, :na], d_aq[d, :na]])))
    return ReplayResult(states, dict(zip(COUNTER_NAMES, map(int, cnt))), tick, (lo, hi), dumps)


def state_times(states: pl.DataFrame) -> np.ndarray:
    """Exchange-clock time at which each replayed state is stamped: the running maximum of message times
    (exchange event time; collector receive time for snapshots, which carry no exchange time).

    A vendor snapshot is stamped with the collector's receive time, and buffered diffs applied after it can carry
    slightly earlier exchange times (observed once: 0.98 ms). The running maximum stamps such a state no earlier than the
    snapshot it builds on, so no state is ever placed before a state it supersedes (conservative: availability can only
    be delayed, never advanced)."""
    t = states.select(pl.coalesce("exch_us", "local_us")).to_series().to_numpy()
    return np.maximum.accumulate(t)


def bbo_valid(flags: pl.Expr | np.ndarray):
    return (flags & BBO_INVALID) == 0
