"""Synthetic tests of the validity-layer and window-statistics code of Acceptance Test 001 (engineering only)."""

import numpy as np
import polars as pl
import pytest

from lpx.data.schema import SNAPSHOT, TRADE_SCHEMA
from lpx.quality import acceptance as A

NO_TRADES = pl.DataFrame(schema={"exch_us": pl.Int64, "price": pl.Float64, "qty": pl.Float64})


def test_windows_break_at_resync_even_when_pre_gap_state_is_valid():
    t = np.array([100, 200, 300, 1300, 1400])  # resync snapshot received at 1300 after a capture gap
    kind = np.array([SNAPSHOT, 1, 1, SNAPSHOT, 1])
    book, joint = A.validity_windows(t, np.zeros(5, np.uint16), [], [], kind)
    assert book.select("start_us", "end_us").rows() == [(100, 300), (1300, 1400)]
    assert joint.select("start_us", "end_us").rows() == [(100, 300), (1300, 1400)]


def test_missing_trades_at_file_edges_are_cut_to_the_day_boundary():
    def tr(rows):
        return pl.DataFrame([dict(trade_id=i, exch_us=t, local_us=None, price=1.0, qty=1.0, aggressor=1, aggressor_status="exchange_flag")
                             for i, t in rows], schema=TRADE_SCHEMA)
    present = tr([(5, 500), (6, 600), (9, 900)])
    missing = tr([(3, 300), (4, 400), (7, 700), (10, 1000)])
    assert sorted(A.missing_trade_intervals(missing, present, (0, 2000))) == [(0, 500), (600, 900), (900, 2000)]


def states(t, bid, ask):
    n = len(t)
    return pl.DataFrame({"kind": [1] * n, "exch_us": t, "local_us": t, "bid1_px": bid, "ask1_px": ask,
                         "bid1_qty": [1.0] * n, "ask1_qty": [1.0] * n, "flags": [0] * n}, schema_overrides={"flags": pl.UInt16})


def test_window_stats_time_weighted_spread():
    # spread 1 tick for 90 s then 2 ticks for 10 s: time-weighted 1.1, event mean 1.5
    st = states([0, 90_000_000], [10.00, 10.00], [10.01, 10.02])
    w = pl.DataFrame({"start_us": [0], "end_us": [100_000_000], "n_msgs": [2], "duration_s": [100.0]})
    out = A.window_stats(w, st, NO_TRADES, 0.01).row(0, named=True)
    assert out["twa_spread_ticks"] == pytest.approx(1.1) and out["event_mean_spread_ticks"] == pytest.approx(1.5)
    assert out["n_valid_states"] == 2 and out["rv_1min_bp"] is None  # window shorter than 3 minutes


def test_window_stats_rv_estimator():
    mids = np.array([10.0, 10.01, 10.0, 10.01, 10.0, 10.01])
    t = (np.arange(6) * 60_000_000).tolist()
    st = states(t, (mids - 0.005).tolist(), (mids + 0.005).tolist())
    w = pl.DataFrame({"start_us": [0], "end_us": [300_000_000], "n_msgs": [6], "duration_s": [300.0]})
    rv = A.window_stats(w, st, NO_TRADES, 0.01)["rv_1min_bp"][0]
    assert rv == pytest.approx(np.std(np.diff(np.log(mids)), ddof=1) * 1e4)


def _rep(vendor_ok=True, hours=24.0):
    g = {k: 0 for k in ("nan_price", "nan_qty", "nonpositive_price", "negative_qty", "off_tick_price", "off_lot_qty")}
    return {"grid_book": g, "grid_trades": g, "grid_reference_trades": g, "ordering": {},
            "engine_vs_vendor_quotes": {"agreement_rate": 1.0 if vendor_ok else 0.5},
            "trades": {"field_mismatch_price": 0, "field_mismatch_qty": 0, "field_mismatch_aggressor": 0,
                       "extra_vs_reference": 0, "missing_vs_reference": 0},
            "flags": {}, "resyncs": [], "coverage_joint": {"covered_hours": hours, "usable_hours_ge_min": hours}}


def test_integrity_and_post_hoc_eligibility_are_separate():
    cfg = {"rules": {"min_engine_vendor_bbo_agreement": 0.9999}}
    rule = {"declared": "2026-10-19", "e001_min_joint_hours": 20.0}
    short = _rep(hours=15.0)
    short["decision"] = A.decide_tardis_day(short, cfg)
    assert short["decision"]["status"] == "accepted"
    el = A.eligibility(short, rule)
    assert el["e001_eligible"] is False and el["declared_after_coverage_seen"] is True
    bad = _rep(vendor_ok=False)
    bad["decision"] = A.decide_tardis_day(bad, cfg)
    assert bad["decision"]["status"] == "rejected" and A.eligibility(bad, rule)["e001_eligible"] is False
