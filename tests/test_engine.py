"""Toy-book tests for the replay engine: update semantics, sequencing, invalidation, proven-region logic."""

import numpy as np
import polars as pl
import pytest

from lpx.book import engine as E
from lpx.data.schema import ASK, BID, BOOK_SCHEMA, DIFF, SNAPSHOT

TICK = 0.01


def book(messages):
    """messages: list of (kind, seq_first, seq_last, [(side, price, qty), ...])."""
    rows = []
    for m, (kind, sf, sl, levels) in enumerate(messages):
        for side, price, qty in levels:
            rows.append(dict(msg=m, kind=kind, exch_us=1000 * m, local_us=1000 * m + 1, seq_first=sf, seq_last=sl,
                             side=side, price=price, qty=qty))
    return pl.DataFrame(rows, schema=BOOK_SCHEMA)


SNAP = [(BID, 10.00, 1.0), (BID, 9.99, 2.0), (BID, 9.97, 3.0), (ASK, 10.01, 1.5), (ASK, 10.02, 2.5), (ASK, 10.05, 4.0)]


def run(msgs, **kw):
    kw.setdefault("grid_px", (5.0, 15.0))
    kw.setdefault("n_levels", 3)
    return E.replay(book(msgs), tick=TICK, **kw)


def test_snapshot_then_absolute_diffs():
    r = run([
        (SNAPSHOT, None, None, SNAP),
        (DIFF, None, None, [(BID, 10.00, 0.5)]),  # absolute size, not delta
        (DIFF, None, None, [(BID, 10.00, 0.0), (ASK, 10.01, 0.0)]),  # remove both touches
        (DIFF, None, None, [(BID, 10.00, 7.0), (BID, 9.98, 1.0)]),
    ], complete_below=0)
    s = r.states
    assert s["bid1_px"].to_list() == pytest.approx([10.00, 10.00, 9.99, 10.00])
    assert s["bid1_qty"].to_list() == pytest.approx([1.0, 0.5, 2.0, 7.0])
    assert s["ask1_px"].to_list() == pytest.approx([10.01, 10.01, 10.02, 10.02])
    assert s.row(3, named=True)["bid2_px"] == pytest.approx(9.99)
    assert s.row(3, named=True)["bid3_px"] == pytest.approx(9.98)
    assert all(E.bbo_valid(f) for f in s["flags"].to_list())
    assert s["flags"][0] & E.IS_SNAPSHOT


def test_unanchored_before_first_snapshot():
    r = run([(DIFF, None, None, [(BID, 10.0, 1.0), (ASK, 10.01, 1.0)]), (SNAPSHOT, None, None, SNAP)])
    f = r.states["flags"].to_list()
    assert f[0] & E.UNANCHORED and not E.bbo_valid(f[0])
    assert E.bbo_valid(f[1])


def test_sequence_rules_stale_straddle_gap_and_reanchor():
    r = run([
        (SNAPSHOT, None, 100, SNAP),
        (DIFF, 95, 100, [(BID, 10.00, 99.0)]),  # u <= lastUpdateId: skipped (already in snapshot)
        (DIFF, 98, 103, [(BID, 10.00, 5.0)]),  # straddles lastUpdateId+1: applied
        (DIFF, 104, 106, [(ASK, 10.01, 9.0)]),  # contiguous
        (DIFF, 110, 112, [(ASK, 10.01, 3.0)]),  # gap (107..109 missing)
        (DIFF, 113, 115, [(ASK, 10.02, 1.0)]),  # contiguous again but still unanchored
        (SNAPSHOT, None, 200, SNAP),
        (DIFF, 201, 202, [(BID, 9.99, 4.0)]),
    ], check_seq=True, complete_below=0)
    f = r.states["flags"].to_list()
    assert f[1] & E.STALE_SKIPPED and r.states["bid1_qty"][1] == pytest.approx(1.0)
    assert r.states["bid1_qty"][2] == pytest.approx(5.0) and E.bbo_valid(f[2])
    assert E.bbo_valid(f[3])
    assert f[4] & E.SEQ_GAP and f[4] & E.UNANCHORED
    assert f[5] & E.UNANCHORED and not f[5] & E.SEQ_GAP
    assert E.bbo_valid(f[6]) and E.bbo_valid(f[7])
    assert r.counters["seq_gaps"] == 1 and r.counters["stale_msgs_skipped"] == 1


def test_crossed_book_invalidates_until_next_snapshot():
    r = run([
        (SNAPSHOT, None, None, SNAP),
        (DIFF, None, None, [(BID, 10.03, 1.0)]),  # bid above best ask -> crossed (stale ask)
        (DIFF, None, None, [(ASK, 10.01, 0.0), (ASK, 10.02, 0.0)]),  # uncrossed again, but no silent repair
        (SNAPSHOT, None, None, SNAP),
    ])
    f = r.states["flags"].to_list()
    assert f[1] & E.CROSSED and f[1] & E.INVALIDATED and not E.bbo_valid(f[1])
    assert f[2] & E.UNANCHORED and not f[2] & E.CROSSED
    assert E.bbo_valid(f[3])


def test_locked_book_is_invalid():
    r = run([(SNAPSHOT, None, None, SNAP), (DIFF, None, None, [(BID, 10.01, 1.0)])])
    assert r.states["flags"][1] & E.LOCKED and not E.bbo_valid(r.states["flags"][1])


def test_proven_region_limits_touch_and_depth():
    # default: a snapshot proves a side only within the price range it covers -> bids proven on [9.97, +inf)
    r = run([
        (SNAPSHOT, None, None, SNAP),
        (DIFF, None, None, [(BID, 10.00, 0.0), (BID, 9.99, 0.0)]),  # touch 9.97: still proven, depth partial
        (DIFF, None, None, [(BID, 9.97, 0.0), (BID, 9.90, 2.0)]),  # touch 9.90 < floor: unknown levels may sit above
    ], complete_below=0)
    f = r.states["flags"].to_list()
    assert E.bbo_valid(f[1]) and f[1] & E.DEPTH_PARTIAL
    assert f[2] & E.TOP_UNKNOWN and not E.bbo_valid(f[2])
    assert r.states["bid_floor_px"][2] == pytest.approx(9.97)
    # proven top-N withholds the unverifiable touch; the raw engine level is still reported for diagnostics
    assert np.isnan(r.states["bid1_px"][2]) and r.states["raw_bid_px"][2] == pytest.approx(9.90)


def test_side_below_snapshot_limit_is_complete():
    r = run([
        (SNAPSHOT, None, None, SNAP),
        (DIFF, None, None, [(BID, 10.00, 0.0), (BID, 9.99, 0.0), (BID, 9.97, 0.0), (BID, 9.50, 1.0)]),
    ], complete_below=1000)
    assert E.bbo_valid(r.states["flags"][1]) and r.states["bid1_px"][1] == pytest.approx(9.50)


def test_grid_edges():
    r = run([
        (SNAPSHOT, None, None, SNAP + [(BID, 1.00, 5.0)]),  # deep bid below grid: ignored, counted
        (DIFF, None, None, [(ASK, 20.00, 1.0)]),  # deep ask above grid: ignored
        (DIFF, None, None, [(BID, 16.00, 1.0)]),  # bid above grid: cannot represent -> invalid
    ], complete_below=0)
    f = r.states["flags"].to_list()
    assert E.bbo_valid(f[0]) and E.bbo_valid(f[1])
    assert f[2] & E.OFF_GRID and not E.bbo_valid(f[2])
    assert r.counters["deep_rows_ignored"] == 2


def test_midday_snapshot_clears_stale_levels():
    r = run([
        (SNAPSHOT, None, None, SNAP),
        (DIFF, None, None, [(BID, 9.98, 9.0)]),
        (SNAPSHOT, None, None, [(BID, 9.99, 1.0), (ASK, 10.02, 1.0)]),  # resync: 10.00 and 9.98 must disappear
    ], complete_below=0)
    s = r.states.row(2, named=True)
    assert s["bid1_px"] == pytest.approx(9.99) and np.isnan(s["bid2_px"]) and s["ask1_px"] == pytest.approx(10.02)


def test_dump_captures_full_book():
    r = run([(SNAPSHOT, None, None, SNAP), (DIFF, None, None, [(BID, 9.98, 1.0)])], dump_after=[1], complete_below=0)
    d = r.dumps[0]
    assert d.msg == 1
    assert (d.bids[:, 0] * TICK).tolist() == pytest.approx([10.00, 9.99, 9.98, 9.97])
    assert (d.asks[:, 0] * TICK).tolist() == pytest.approx([10.01, 10.02, 10.05])


def test_off_tick_prices_rejected():
    with pytest.raises(ValueError, match="tick grid"):
        run([(SNAPSHOT, None, None, [(BID, 10.005, 1.0), (ASK, 10.01, 1.0)])])


def test_check_seq_requires_ids():
    with pytest.raises(ValueError, match="update ids"):
        run([(SNAPSHOT, None, 1, SNAP), (DIFF, None, None, [(BID, 10.0, 1.0)])], check_seq=True)


def test_proven_levels_truncates_region():
    # 3 bid levels in the snapshot, but only the best 2 count as proven (buffered-merge guard)
    r = run([
        (SNAPSHOT, None, None, SNAP),
        (DIFF, None, None, [(BID, 10.00, 0.0)]),  # touch 9.99 still inside proven region [9.99, inf)
        (DIFF, None, None, [(BID, 9.99, 0.0)]),  # touch 9.97 is outside it
    ], proven_levels=2)
    f = r.states["flags"].to_list()
    assert r.states["bid_floor_px"][0] == pytest.approx(9.99) and r.states["ask_ceil_px"][0] == pytest.approx(10.02)
    assert E.bbo_valid(f[1]) and f[2] & E.TOP_UNKNOWN


def test_state_times_are_monotone_and_never_advance_a_state():
    st = pl.DataFrame({"exch_us": [None, 1000, 2000, None, 2900, 3500], "local_us": [10, 1003, 2003, 3000, 3002, 3503]},
                      schema={"exch_us": pl.Int64, "local_us": pl.Int64})
    # snapshot at collector time 3000, then a buffered diff with exchange time 2900: stamped 3000, not earlier
    assert E.state_times(st).tolist() == [10, 1000, 2000, 3000, 3000, 3500]
