"""Unit tests for acceptance checks on small synthetic frames (engineering-only; not evidence about real data)."""

import numpy as np
import polars as pl
import pytest

from lpx.book import engine as E
from lpx.data.schema import BOOK_SCHEMA, TRADE_SCHEMA
from lpx.quality import checks as C


def trades(rows):
    return pl.DataFrame([dict(trade_id=i, exch_us=t, local_us=None, price=p, qty=q, aggressor=a, aggressor_status="exchange_flag")
                         for i, t, p, q, a in rows], schema=TRADE_SCHEMA)


def test_grid_audit_flags_off_tick_and_off_lot():
    df = pl.DataFrame({"price": [10.00, 10.005, 10.01], "qty": [0.001, 0.0015, 0.002]})
    a = C.grid_audit(df, 0.01, 0.001)
    assert a["off_tick_price"] == 1 and a["off_lot_qty"] == 1 and not C.grid_ok(a)
    assert C.grid_ok(C.grid_audit(pl.DataFrame({"price": [10.0, 72.45], "qty": [1.0, 0.003]}), 0.01, 0.001))


def test_trade_audit_completeness_and_fields():
    ref = trades([(1, 100, 10.0, 1.0, 1), (2, 200, 10.0, 2.0, -1), (3, 300, 10.01, 1.0, 1), (4, 400, 10.0, 1.0, -1)])
    cand = trades([(1, 100, 10.0, 1.0, 1), (2, 200, 10.0, 2.0, 1), (4, 400, 10.0, 1.0, -1), (9, 900, 10.0, 1.0, 1)])
    a, missing = C.trade_audit(cand, ref)
    assert a["missing_vs_reference"] == 1 and missing["trade_id"].to_list() == [3]
    assert a["extra_vs_reference"] == 1
    assert a["field_mismatch_aggressor"] == 1 and a["field_mismatch_price"] == 0
    assert a["internal_id_gaps"] == 2 and a["internal_missing_ids"] == 1 + 4
    assert a["completeness"] == pytest.approx(3 / 4)


def states(rows):
    """rows: (exch_us, flags, bid1, ask1)."""
    return pl.DataFrame([dict(kind=1, exch_us=t, local_us=t, flags=f, bid1_px=b, ask1_px=a) for t, f, b, a in rows])


def test_trade_book_alignment_inside_spread_and_silence():
    st = states([(1_000_000, 0, 10.00, 10.01), (1_100_000, 0, 10.00, 10.01), (5_000_000, 0, 10.00, 10.01)])
    tr = trades([
        (1, 1_050_000, 10.01, 1.0, 1),   # buy at the ask: consistent
        (2, 1_060_000, 10.00, 1.0, 1),   # buy at our bid: inside replayed spread AND through opposite touch
        (3, 1_200_000, 10.00, 1.0, -1),  # sell at bid, but next depth event 3.8 s later -> silence
    ])
    a, silent = C.trade_book_alignment(st, tr, silence_s=1.0)
    assert a["buy_inside_replayed_spread"] == 1 and a["trade_through_opposite_touch"] == 1
    assert a["silent_trades"] == 1 and silent["start_us"].to_list() == [1_200_000]
    assert silent["end_us"].to_list() == [5_000_000]


def test_trade_book_alignment_ignores_invalid_pre_state():
    st = states([(1_000_000, E.UNANCHORED, 10.00, 10.01)])
    a, _ = C.trade_book_alignment(st, trades([(1, 1_050_000, 9.0, 1.0, 1)]), silence_s=1.0)
    assert a["trades_with_valid_pre_state"] == 0 and a["buy_inside_replayed_spread"] == 0


def dump(bids, asks):
    return E.BookDump(0, 0, 0, 0, np.array(bids, float).reshape(-1, 2), np.array(asks, float).reshape(-1, 2))


def test_compare_books_buckets_and_scope():
    snap = dump([[1000, 1.0], [999, 2.0], [990, 1.0]], [[1001, 1.0], [1002, 3.0]])
    rep = dump([[1000, 1.0], [999, 2.5], [995, 1.0], [980, 7.0]], [[1001, 1.0], [1002, 3.0]])
    c = C.compare_books(rep, snap, 0.01)
    # 980 lies outside the snapshot's covered bid range [990, 1000] -> not compared
    assert sum(c["levels"]) == 6
    assert sum(c["match"]) == 3 and sum(c["qty_diff"]) == 1 and sum(c["only_replay"]) == 1 and sum(c["only_snapshot"]) == 1
    assert c["bbo_equal"] and c["touch_qty_equal"]


def test_windows_and_masks():
    t = np.array([0, 1_000_000, 2_000_000, 3_000_000, 4_000_000, 5_000_000])
    ok = np.array([1, 1, 0, 1, 1, 1])
    w = C.windows(t, ok)
    assert w["start_us"].to_list() == [0, 3_000_000] and w["end_us"].to_list() == [1_000_000, 5_000_000]
    assert w["duration_s"].to_list() == [1.0, 2.0]
    t2 = np.array([0, 2_000_000, 1_999_000, 3_000_000])  # small regression (snapshot on collector clock)
    m = C.mask_intervals(t2, [(1_999_500, 2_500_000)])
    assert m.tolist() == [False, True, False, False]


def test_cross_capture_matching():
    def bk(rows, sequenced):
        out = []
        for m, t, sf, sl, side, p, q in rows:
            out.append(dict(msg=m, kind=1, exch_us=None if sequenced else t, local_us=t if sequenced else None,
                            seq_first=sf, seq_last=sl, side=side, price=p, qty=q))
        return pl.DataFrame(out, schema=BOOK_SCHEMA)
    # reference: sequenced capture on a collector clock (~200 ms behind the exchange)
    ref = bk([(0, 1_200_000, 1, 2, 1, 10.0, 1.0), (0, 1_200_000, 1, 2, -1, 10.01, 2.0),
              (1, 1_300_000, 3, 3, 1, 10.0, 0.5),
              (2, 1_400_000, 4, 4, 1, 9.99, 1.0),
              (3, 1_500_000, 5, 5, -1, 10.02, 9.0)], sequenced=True)
    # candidate: exchange clock; message 2 is an extra event not in the reference chain; ref msg 3 never captured
    cand = bk([(0, 1_000_000, None, None, -1, 10.01, 2.0), (0, 1_000_000, None, None, 1, 10.0, 1.0),  # same content, other row order
               (1, 1_100_000, None, None, 1, 10.0, 0.5),
               (2, 1_150_000, None, None, 1, 9.98, 3.0),
               (3, 1_200_000, None, None, 1, 9.99, 1.0)], sequenced=False)
    out, bad = C.cross_capture(ref, cand, 0, 2_000_000)
    # run ids 1..5 is contiguous; candidate reproduces 1-2,3 then inserts an extra event, then 4; 5 is never captured
    assert out["reference_messages"] == 4 and out["reference_contiguous_runs"] == 1
    assert out["aligned_messages"] == 3 and out["unaligned_messages"] == 1
    assert out["realignments_within_runs"] == 1 and out["runs_reproduced_unbroken"] == 0
    assert out["reference_receive_lag_ms_quantiles"]["0.5"] == pytest.approx(200.0)
    assert bad["seq_first"].to_list() == [5]


def test_cross_capture_prefers_consecutive_alignment_over_nearest_duplicate():
    def bk(rows, sequenced):
        return pl.DataFrame([dict(msg=m, kind=1, exch_us=None if sequenced else t, local_us=t if sequenced else None,
                                  seq_first=sf, seq_last=sl, side=1, price=p, qty=q) for m, t, sf, sl, p, q in rows],
                            schema=BOOK_SCHEMA)
    # content "A" recurs: candidate A(0) B(1) A(2); reference A, B in sequence. Nearest-lag would map A->2; alignment maps A->0.
    cand = bk([(0, 1_000_000, None, None, 10.0, 1.0), (1, 1_100_000, None, None, 10.0, 2.0), (2, 1_200_000, None, None, 10.0, 1.0)], False)
    ref = bk([(0, 1_250_000, 1, 1, 10.0, 1.0), (1, 1_250_000, 2, 2, 10.0, 2.0)], True)
    out, _ = C.cross_capture(ref, cand, 0, 2_000_000)
    assert out["aligned_messages"] == 2 and out["runs_reproduced_unbroken"] == 1 and out["realignments_within_runs"] == 0


def test_subtract_intervals():
    w = C.windows(np.array([0, 10, 20, 30, 40]), np.array([1, 1, 1, 1, 1]))
    r = C.subtract_intervals(w, [(12, 25)], np.array([0, 10, 20, 30, 40]))
    assert r.select("start_us", "end_us").rows() == [(0, 11), (25, 40)]
    assert r["n_msgs"].to_list() == [2, 2]
