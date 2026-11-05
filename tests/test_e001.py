"""E001 unit tests on synthetic frames (engineering checks; not evidence about markets)."""

import numpy as np
import polars as pl
import pytest

from lpx.book import states as S
from lpx.data.schema import TRADE_SCHEMA
from lpx.research import e001


def trades(rows):
    return pl.DataFrame([dict(trade_id=i, exch_us=t, local_us=None, price=p, qty=q, aggressor=a, aggressor_status="exchange_flag")
                         for i, t, p, q, a in rows], schema=TRADE_SCHEMA)


def test_ts_side_clusters_group_by_time_and_side_only():
    tr = trades([(1, 100, 10.01, 1.0, 1), (2, 100, 10.02, 3.0, 1), (3, 100, 10.00, 2.0, -1), (4, 200, 10.0, 1.0, 1)])
    ev = e001.ts_side_clusters(tr)
    assert ev.height == 3
    buy = ev.filter((pl.col("exch_us") == 100) & (pl.col("aggressor") == 1)).row(0, named=True)
    assert buy["qty"] == 4.0 and buy["fills"] == 2 and buy["levels"] == 2
    assert buy["vwap"] == pytest.approx((10.01 * 1 + 10.02 * 3) / 4)
    assert e001.single_trades(tr).height == 4


def test_cells_and_spread_identity():
    ev = pl.DataFrame({"sign": [1.0, -1.0, 1.0], "qty": [0.5, 5.0, 50.0], "q_bid1": [10.0, 10.0, 1.0], "q_ask1": [1.0, 10.0, 40.0]})
    c = e001.add_cells(ev, (1.0, 10.0))
    assert c["size"].to_list() == ["S", "M", "L"]
    assert c["touch_imbalance"].to_list() == ["with", "neutral", "against"]  # buy into a bid-heavy book is "with"
    assert c["qty_ge_touch"].to_list() == [False, False, True]
    m0, mh, P, s = 100.0, 100.01, 100.005, 1.0
    es = 2 * s * (P - m0) / m0 * 1e4
    mo = s * (mh - m0) / m0 * 1e4
    assert es - 2 * mo == pytest.approx(2 * s * (P - mh) / m0 * 1e4)


def test_parse_timing():
    assert e001.parse_timing("exchange") == ("exchange", 0)
    assert e001.parse_timing("receipt+0ms") == ("receipt", 0)
    assert e001.parse_timing("receipt+50ms") == ("receipt", 50_000)


def synthetic_session():
    """States every second from t=1 s to 40 s; mid steps up by 0.01 at 10 s; receipt 3 ms after exchange time.
    The state at 20 s has no proven touch (record invalid). Window: [1 s, 40 s]."""
    s = e001.Session.__new__(e001.Session)
    s.day, s.symbol = "2099-01-01", "TEST"
    s.t_exch = np.arange(1, 41) * 1_000_000
    s.t_local = s.t_exch + 3_000
    s.bid = np.where(s.t_exch >= 10_000_000, 10.00, 9.99)
    s.ask = s.bid + 0.01
    s.mid = (s.bid + s.ask) / 2
    s.qb = np.full(40, 5.0)
    s.qa = np.full(40, 2.0)
    s.bbo_ok = np.ones(40, bool)
    s.bbo_ok[19] = False  # state at 20 s
    s.valid_joint = s.bbo_ok.copy()
    s.trades = trades([
        (1, 9_500_000, 9.995, 3.0, 1),     # buy before the up-step; pre-state 9 s, +1 s -> 10.5 s state (moved)
        (2, 9_500_000, 9.995, 1.0, 1),     # same time & side -> same cluster
        (3, 20_500_000, 10.005, 1.0, 1),   # pre-state = invalid record at 20 s -> excluded
        (4, 36_000_000, 10.005, 1.0, -1),  # +5 s horizon runs past the last state (40 s) -> excluded
        (5, 12_000_000, 10.005, 1.0, 1),   # an event exactly at a state time sees the state before it
    ])
    return s


W1 = pl.DataFrame({"start_us": [1_000_000], "end_us": [40_000_000]})


def test_session_events_validity_and_exclusions():
    s = synthetic_session()
    ev = e001.session_events(s, W1, [1, 5], [1, 5], unit="ts_side_cluster", timing="exchange").sort("t_us")
    assert ev.height == 4  # trades 1+2 form one cluster
    r = dict(zip(ev["t_us"].to_list(), ev["reason"].to_list()))
    assert r[9_500_000] == "included" and r[12_000_000] == "included"
    assert r[20_500_000] == "pre_state_record_invalid"
    assert r[36_000_000] == "horizon_beyond_session_data"
    first = ev.row(0, named=True)
    assert first["qty"] == 4.0 and first["pre_state_age_ms"] == pytest.approx(500.0)
    assert first["mo_1s"] == pytest.approx(1 * (10.005 - 9.995) / 9.995 * 1e4)  # state at 10 s is in force at 10.5 s
    assert first["touch_moved_next_state"] == 1.0
    at_state = ev.filter(pl.col("t_us") == 12_000_000).row(0, named=True)
    assert at_state["pre_state_age_ms"] == pytest.approx(1000.0)  # strict: the 12 s state is not "before" 12 s
    assert e001.session_events(s, W1, [1, 5], [1, 5], unit="trade", timing="exchange").height == 5


def test_receipt_clock_changes_only_the_pre_event_information():
    s = synthetic_session()
    ex = e001.session_events(s, W1, [1], [1], timing="exchange").sort("t_us")
    rc = e001.session_events(s, W1, [1], [1], timing="receipt+0ms").sort("t_us")
    dl = e001.session_events(s, W1, [1], [1], timing="receipt+998ms").sort("t_us")
    assert rc.filter(pl.col("t_us") == 12_000_000)["pre_state_age_ms"][0] == pytest.approx(1000.0)
    # with ~1 s extra latency the 9.5 s event can only use the 8 s state
    assert dl.filter(pl.col("t_us") == 9_500_000)["pre_state_age_ms"][0] == pytest.approx(1500.0)
    assert (rc["pre_state_age_ms"].drop_nans() >= ex["pre_state_age_ms"].drop_nans()).all()
    # the outcome mid m(T+h) is identical under every clock: only m0 changes
    def mh(f):
        return f.select("t_us", (pl.col("m0") * (1 + pl.col("sign") * pl.col("mo_1s") / 1e4)).alias("mh")).drop_nans()
    for other in (rc, dl):
        j = mh(ex).join(mh(other), on="t_us", suffix="_o")
        assert j.height > 0 and np.allclose(j["mh"], j["mh_o"])


def test_gap_boundaries_and_opposite_side_clusters():
    s = synthetic_session()
    s.bbo_ok[:] = True
    w = pl.DataFrame({"start_us": [1_000_000, 20_000_000], "end_us": [15_000_000, 40_000_000]})  # gap (15 s, 20 s)
    s.valid_joint = S.in_windows(s.t_exch, w) & s.bbo_ok
    s.trades = trades([
        (1, 14_500_000, 10.005, 1.0, 1),   # T in window 0, T + 1 s in the gap
        (2, 20_000_000, 10.005, 1.0, 1),   # T at window 1 start: the state before it (19 s) is in the gap
        (3, 25_500_000, 10.005, 1.0, 1),   # opposite-side clusters at the same T share m0 with opposite signs
        (4, 25_500_000, 10.000, 2.0, -1),
        (5, 17_000_000, 10.000, 1.0, 1),   # T itself in the gap
    ])
    ev = e001.session_events(s, w, [1], [1], timing="exchange", baseline_windows=True)
    r = {(t, sg): x for t, sg, x in ev.select("t_us", "sign", "reason").rows()}
    assert r[(14_500_000, 1.0)] == "horizon_leaves_window"
    assert r[(20_000_000, 1.0)] == "pre_state_outside_windows"
    assert r[(17_000_000, 1.0)] == "t_outside_windows"
    pair = ev.filter(pl.col("t_us") == 25_500_000)
    assert pair.height == 2 and pair["m0"].n_unique() == 1 and sorted(pair["sign"].to_list()) == [-1.0, 1.0]
    assert pair["primary"].all()


def test_invalid_outcome_record_excludes_event():
    s = synthetic_session()
    s.bbo_ok[:] = True
    s.bbo_ok[30] = False  # the state at 31 s has no proven touch
    s.trades = trades([(1, 30_500_000, 10.005, 1.0, 1)])
    ev = e001.session_events(s, W1, [1], [1], timing="exchange")
    assert ev["reason"][0] == "horizon_leaves_window" and not ev["primary"][0] and np.isnan(ev["mo_1s"][0])


def test_primary_requires_every_primary_horizon():
    s = synthetic_session()
    s.bbo_ok[:] = True
    s.bbo_ok[30] = False
    s.trades = trades([(1, 30_500_000, 10.005, 1.0, 1)])  # 1 s outcome invalid, 5 s outcome valid
    ev = e001.session_events(s, W1, [1, 5], [1, 5], timing="exchange")
    assert not ev["primary"][0] and np.isnan(ev["mo_1s"][0]) and not np.isnan(ev["mo_5s"][0])


def test_run_guards():
    with pytest.raises(PermissionError):
        e001.run(["train", "test"])
    with pytest.raises(ValueError, match="train"):
        e001.run(["validation"])


def test_bootstrap_intervals_cover_known_mean():
    rng = np.random.default_rng(0)
    x = rng.normal(1.0, 0.5, size=40)
    lo, hi = e001.session_bootstrap(x, 5000, np.random.default_rng(1))
    assert lo < 1.0 < hi
    t = np.arange(10_000) * 1_000_000
    lo, hi = e001.block_bootstrap(t, rng.normal(0.0, 1.0, size=t.size), 300.0, 2000, np.random.default_rng(2))
    assert lo < 0.0 < hi


def test_window_departure_near_session_end_is_not_labelled_end_of_data():
    s = synthetic_session()
    s.bbo_ok[:] = True
    w = pl.DataFrame({"start_us": [1_000_000, 37_000_000], "end_us": [36_000_000, 40_000_000]})  # gap (36 s, 37 s)
    s.trades = trades([(1, 35_500_000, 10.005, 1.0, 1)])  # 1 s horizon leaves the window; 30 s horizon beyond the data
    ev = e001.session_events(s, w, [1, 30], [1, 30], timing="exchange")
    assert ev["reason"][0] == "horizon_leaves_window"


def test_report_tables_render_from_run_shaped_outputs(tmp_path):
    import json

    from lpx.research import e001_report

    rng = np.random.default_rng(0)
    frame = pl.DataFrame({"day": ["2099-01-01"] * 50 + ["2099-02-01"] * 50,
                          **{m: rng.normal(size=100) for m in ["es", "mo_1s", "mo_5s", "mo_30s", "rs_1s", "rs_5s", "rs_30s"]}})
    metrics = ["es", "mo_1s", "mo_5s", "mo_30s", "rs_1s", "rs_5s", "rs_30s"]
    prim = e001.summarize(frame, metrics, {"analysis": e001.PRIMARY, "spec": "primary", "cell": "all"}, 200, rng)
    cells = prim + e001.summarize(frame, metrics, {"analysis": e001.PRIMARY, "spec": "primary", "cell": "size=S"}, 200, rng)
    sens = e001.summarize(frame, metrics, {"analysis": e001.EXPLORATORY, "spec": "unit=trade", "cell": "all"}, 200, rng)
    per = [{"analysis": e001.PRIMARY, "day": d, "split": "train", "events": 50, "e001_eligible_posthoc": True, "excluded_events": 0,
            **{k: v for m in metrics for k, v in ((m, 0.1), (f"{m}_ci95_lo", -0.1), (f"{m}_ci95_hi", 0.3))}}
           for d in ("2099-01-01", "2099-02-01")]
    res = {"run_at_utc": "x", "sessions": ["2099-01-01", "2099-02-01"], "session_sets": ["train"], "primary": prim,
           "provenance": {"git_commit": "a" * 40, "git_dirty": False, "code_fingerprint": "f",
                          "inputs": {"windows_csv_sha256": "b" * 64, "acceptance_git_commit": "c" * 40}},
           "exclusions": {"primary": {"included": 100}},
           "descriptive": {"secondary_horizons": [{"metric": "mo_0.1s", "events": 100, "mean_of_session_means": 0.0}],
                           "pre_state_age_ms_quantiles": {"exchange (primary)": {"0.5": 50.0, "0.9": 90.0, "0.99": 99.0}}},
           "proxy_validation_qty_ge_touch": [{"qty_ge_touch": False, "events": 10, "share_touch_moved_next_state": 0.1}]}
    (tmp_path / "e001_discovery.json").write_text(json.dumps(res))
    pl.DataFrame(cells).write_csv(tmp_path / "e001_discovery_cells.csv")
    pl.DataFrame(per).write_csv(tmp_path / "e001_discovery_per_session.csv")
    pl.DataFrame(sens).write_csv(tmp_path / "e001_discovery_sensitivity.csv")
    T = e001_report.tables(tmp_path)
    assert {"meta", "primary", "exclusions", "per_session", "cells", "sensitivity", "descriptive", "proxy"} <= set(T)
    assert "exploratory" in T["sensitivity"] and "pre-specified primary" in T["sensitivity"]
