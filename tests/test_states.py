"""Time-alignment tests: as-of lookups must never use a future or unreceived state, an invalid record, or a state from
another accepted window."""

import numpy as np
import polars as pl
import pytest

from lpx.book import states as S

T = np.array([100, 200, 300, 400, 600, 700])  # exchange times of states (us)
OK = np.ones(T.size, bool)
W = pl.DataFrame({"start_us": [100, 600], "end_us": [400, 700]})  # gap (400, 600): e.g. capture loss / silence cut


def test_window_id_closed_intervals():
    assert S.window_id(np.array([99, 100, 400, 401, 600, 700, 701]), W).tolist() == [-1, 0, 0, -1, 1, 1, -1]


def test_asof_strict_uses_information_before_the_event():
    idx, ok = S.asof(T, np.array([200, 250]), W, state_ok=OK, strict=True)
    assert idx.tolist() == [0, 1] and ok.tolist() == [True, True]  # an event at 200 sees the state from 100
    idx, _ = S.asof(T, np.array([200]), W, state_ok=OK, strict=False)
    assert idx.tolist() == [1]


def test_simultaneous_events_share_the_same_pre_state():
    idx, ok = S.asof(T, np.array([250, 250, 250]), W, state_ok=OK, strict=True)
    assert idx.tolist() == [1, 1, 1] and ok.all()


def test_asof_never_crosses_a_window_boundary():
    # 450 lies after the first window's end: the state from 400 is in force but unverifiable there
    idx, ok = S.asof(T, np.array([450, 650, 701, 50, 600]), W, state_ok=OK, strict=True)
    assert idx.tolist() == [3, 4, 5, -1, 3]
    # an event exactly at the first state of the next window sees (strictly before) the last state of the previous one
    assert ok.tolist() == [False, True, False, False, False]


def test_invalid_record_inside_a_window_is_rejected():
    ok_rec = OK.copy()
    ok_rec[2] = False  # e.g. a record without a proven touch
    idx, ok = S.asof(T, np.array([350, 450 - 100]), W, state_ok=ok_rec, strict=True)
    assert idx.tolist() == [2, 2] and ok.tolist() == [False, False]


def test_receipt_clock_excludes_states_not_yet_received():
    t_local = T + np.array([5, 5, 80, 5, 5, 5])  # state at 300 arrived late (380)
    q = np.array([350, 390])
    idx_x, _ = S.asof(T, q, W, state_ok=OK, strict=True)
    idx_r, ok_r = S.asof(t_local, q, W, state_ok=OK, t_window=T, strict=True)
    assert idx_x.tolist() == [2, 2]  # exchange clock: published at 300
    assert idx_r.tolist() == [1, 2] and ok_r.all()  # receipt clock: at 350 it had not arrived yet
    idx_d, _ = S.asof(t_local + 150, q, W, state_ok=OK, t_window=T, strict=True)  # +150 us extra latency
    assert idx_d.tolist() == [0, 1]  # at 350 only the 100-state (seen at 255) is usable; at 390 also the 200-state


def test_receipt_clock_still_respects_windows():
    t_local = T + 10
    idx, ok = S.asof(t_local, np.array([605]), W, state_ok=OK, t_window=T, strict=True)
    assert idx.tolist() == [3] and ok.tolist() == [False]  # last received state belongs to the previous window


def test_overlapping_windows_rejected():
    with pytest.raises(ValueError, match="overlap"):
        S.window_id(np.array([1]), pl.DataFrame({"start_us": [0, 5], "end_us": [10, 20]}))


def test_decreasing_information_clock_rejected():
    # a later state stamped earlier would let a query at 299.5 see content of the 300-message; refuse instead
    t = np.array([100, 300, 299, 400])
    with pytest.raises(ValueError, match="non-decreasing"):
        S.asof(t, np.array([350]), pl.DataFrame({"start_us": [100], "end_us": [400]}), state_ok=np.ones(4, bool))
