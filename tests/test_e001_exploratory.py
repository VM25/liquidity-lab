"""Synthetic checks of the E001 exploratory decomposition (engineering only)."""

import numpy as np
import polars as pl
import pytest

from lpx.research import e001_exploratory as X
from tests.test_e001 import W1, synthetic_session, trades


def test_batch_decomposition_and_passive_side():
    s = synthetic_session()
    s.bbo_ok[:] = True
    s.valid_joint = s.bbo_ok.copy()
    s.trades = trades([(1, 9_500_000, 9.995, 3.0, 1),   # buy; the 10 s batch moves the ask up -> touch transition
                       (2, 12_500_000, 10.000, 1.0, -1)])  # sell; next batch (13 s) unchanged -> no transition
    f = X.session_frame(s, W1, [0.1, 1, 5], [1, 5]).sort("t_us")
    a, b = f.row(0, named=True), f.row(1, named=True)
    assert a["touch_transition"] and not b["touch_transition"]
    assert a["c_batch"] == pytest.approx((10.005 - 9.995) / 9.995 * 1e4)  # mid move inside the trade's batch
    assert a["mo_5s"] - a["c_batch"] == pytest.approx(0.0)                 # no further drift afterwards
    assert a["passive_side"].startswith("ask") and b["passive_side"].startswith("bid")
    # passive-side imbalance: bid queue 5, ask queue 2 -> ask side is the thinner one, bid side the thicker one
    assert a["imb_passive"] == pytest.approx((2 - 5) / 7) and b["imb_passive"] == pytest.approx((5 - 2) / 7)
    assert a["notional"] == pytest.approx(3.0 * 9.995)


def test_weighted_session_means():
    f = pl.DataFrame({"day": ["a", "a", "a", "b"], "x": [1.0, 3.0, float("nan"), 5.0], "qty": [1.0, 3.0, 100.0, 2.0]})
    ev = X.weighted_session_means(f, ["x"], "event")
    assert ev["x"].to_list() == pytest.approx([2.0, 5.0])
    q = X.weighted_session_means(f, ["x"], "qty")
    assert q["x"].to_list() == pytest.approx([(1 * 1 + 3 * 3) / 4, 5.0])  # the NaN event's weight is excluded
