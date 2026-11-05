"""Randomized differential test: lpx.book.engine.replay vs an independent brute-force dict reference of the documented
semantics (reference written separately during the 2026-10-19 code review; it shares no code with the engine).

Reference semantics (from engine docstring/comments):
  snapshot: reset; q<=0 rows ignored; bids below grid = deep (floor -> grid bottom), bids above grid = OFF_GRID (unanchored);
            asks symmetric; floor = lowest on-grid snapshot bid (or grid bottom if deep); truncated to the proven_levels-th
            best snapshot level; anchored iff no off-grid row.
  diff: absolute sizes; deep rows ignored; off-grid rows -> OFF_GRID and unanchored; q<=0 removes.
  after each message: EMPTY_SIDE if a side has no on-grid level; else CROSSED/LOCKED (and INVALIDATED+unanchored if was
  anchored); TOP_UNKNOWN if bid touch < floor or ask touch > ceil; UNANCHORED if not anchored; DEPTH_PARTIAL if fewer than
  n proven levels on a side (levels within [floor, touch]).
"""
import numpy as np
import polars as pl

from lpx.book import engine as E
from lpx.data.schema import ASK, BID, BOOK_SCHEMA, DIFF, SNAPSHOT

TICK = 0.01
LO_PX, HI_PX = 10.00, 10.40  # grid [1000, 1040] ticks
LO, HI = 1000, 1040
N = 3


def ref_replay(msgs, proven_levels, complete_below=0):
    bids, asks = {}, {}
    anchored = False
    floor, ceil = HI + 1, LO - 1  # nothing proven
    out = []
    for kind, levels in msgs:
        f = 0
        if kind == SNAPSHOT:
            bids, asks = {}, {}
            deep_b = deep_a = False
            for side, tk, q in levels:
                if q <= 0:
                    continue
                if side == BID:
                    if tk < LO:
                        deep_b = True
                    elif tk > HI:
                        f |= E.OFF_GRID
                    else:
                        bids[tk] = q
                else:
                    if tk > HI:
                        deep_a = True
                    elif tk < LO:
                        f |= E.OFF_GRID
                    else:
                        asks[tk] = q
            nb = sum(1 for s_, _, q_ in levels if s_ == BID and q_ > 0); na = sum(1 for s_, _, q_ in levels if s_ == ASK and q_ > 0)
            floor = LO if (deep_b or (complete_below > 0 and nb < complete_below)) else (min(bids) if bids else HI + 1)
            ceil = HI if (deep_a or (complete_below > 0 and na < complete_below)) else (max(asks) if asks else LO - 1)
            if proven_levels > 0:
                sb = sorted(bids, reverse=True)
                if len(sb) >= proven_levels:
                    floor = max(floor, sb[proven_levels - 1])
                sa = sorted(asks)
                if len(sa) >= proven_levels:
                    ceil = min(ceil, sa[proven_levels - 1])
            anchored = not (f & E.OFF_GRID)
            f |= E.IS_SNAPSHOT
        else:
            for side, tk, q in levels:
                if side == BID:
                    if tk < LO:
                        continue
                    if tk > HI:
                        f |= E.OFF_GRID
                        anchored = False
                        continue
                    if q <= 0:
                        bids.pop(tk, None)
                    else:
                        bids[tk] = q
                else:
                    if tk > HI:
                        continue
                    if tk < LO:
                        f |= E.OFF_GRID
                        anchored = False
                        continue
                    if q <= 0:
                        asks.pop(tk, None)
                    else:
                        asks[tk] = q
        bb = max(bids) if bids else None
        ba = min(asks) if asks else None
        if bb is None or ba is None:
            f |= E.EMPTY_SIDE
        else:
            if bb > ba:
                f |= E.CROSSED
            elif bb == ba:
                f |= E.LOCKED
            if f & (E.CROSSED | E.LOCKED) and anchored:
                anchored = False
                f |= E.INVALIDATED
            if bb < floor or ba > ceil:
                f |= E.TOP_UNKNOWN
        if not anchored:
            f |= E.UNANCHORED
        pb = [(p, bids[p]) for p in sorted(bids, reverse=True) if p >= floor][:N]
        pa = [(p, asks[p]) for p in sorted(asks) if p <= ceil][:N]
        # engine: top-N walk starts at the touch and stops at the floor; if touch < floor nothing is proven
        if bb is not None and bb < floor:
            pb = []
        if ba is not None and ba > ceil:
            pa = []
        if len(pb) < N or len(pa) < N:
            f |= E.DEPTH_PARTIAL
        out.append((f, pb, pa, bb, ba))
    return out


def to_frame(msgs):
    rows = []
    for m, (kind, levels) in enumerate(msgs):
        for side, tk, q in levels:
            rows.append(dict(msg=m, kind=kind, exch_us=1000 * m, local_us=1000 * m + 1, seq_first=None, seq_last=None,
                             side=side, price=round(tk * TICK, 2), qty=float(q)))
    return pl.DataFrame(rows, schema=BOOK_SCHEMA)


def rand_msgs(rng):
    msgs = []
    mid = rng.integers(LO + 5, HI - 5)
    for k in range(rng.integers(5, 40)):
        if k == 0 or rng.random() < 0.08:
            levels = []
            for _ in range(rng.integers(1, 12)):
                levels.append((BID, int(mid - rng.integers(0, 12)), float(rng.integers(0, 4))))
                levels.append((ASK, int(mid + rng.integers(-1, 12)), float(rng.integers(0, 4))))
            if rng.random() < 0.1:
                levels.append((BID, LO - 3, 1.0))  # deep
            if rng.random() < 0.05:
                levels.append((ASK, LO - 2, 1.0))  # off-grid ask
            if not levels:
                continue
            msgs.append((SNAPSHOT, levels))
        else:
            levels = []
            for _ in range(rng.integers(1, 5)):
                side = BID if rng.random() < 0.5 else ASK
                tk = int(mid + rng.integers(-14, 15))
                if rng.random() < 0.02:
                    tk = HI + 2 if side == BID else LO - 2  # off grid
                levels.append((side, tk, float(rng.integers(0, 4))))
            msgs.append((DIFF, levels))
    return msgs


MASK = (E.UNANCHORED | E.CROSSED | E.LOCKED | E.EMPTY_SIDE | E.TOP_UNKNOWN | E.DEPTH_PARTIAL | E.OFF_GRID
        | E.IS_SNAPSHOT | E.INVALIDATED)


def test_engine_matches_brute_force_reference():
    rng = np.random.default_rng(11)
    for trial in range(600):
        msgs = rand_msgs(rng)
        pl_ = int(rng.choice([0, 2, 3, 5]))
        cb = int(rng.choice([0, 0, 4, 8]))
        st = E.replay(to_frame(msgs), tick=TICK, grid_px=(LO_PX, HI_PX), n_levels=N, proven_levels=pl_, complete_below=cb).states
        for m, (f, pb, pa, bb, ba) in enumerate(ref_replay(msgs, pl_, cb)):
            row = st.row(m, named=True)
            got_pb = [(round(row[f"bid{i}_px"] / TICK), row[f"bid{i}_qty"]) for i in range(1, N + 1) if not np.isnan(row[f"bid{i}_px"])]
            got_pa = [(round(row[f"ask{i}_px"] / TICK), row[f"ask{i}_qty"]) for i in range(1, N + 1) if not np.isnan(row[f"ask{i}_px"])]
            rb = None if np.isnan(row["raw_bid_px"]) else round(row["raw_bid_px"] / TICK)
            ra = None if np.isnan(row["raw_ask_px"]) else round(row["raw_ask_px"] / TICK)
            assert (row["flags"] & MASK, got_pb, got_pa, rb, ra) == (f, pb, pa, bb, ba), f"trial {trial} msg {m}: {msgs[: m + 1]}"
