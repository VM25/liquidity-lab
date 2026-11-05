"""E004 on synthetic inputs (no market data): delivery streams, causality, windows, engine options and labels."""

import dataclasses

import numpy as np
import polars as pl
import pytest

from lpx.execution import sim as X
from lpx.research import e003 as E3
from lpx.research import e003_features as F
from lpx.research import e004 as E4
from lpx.research import e004_analysis as AN
from lpx.research import e004_degrade as DG
from lpx.research import e004_forecast as FC
from lpx.research import e004_policy as PO
from lpx.research import e004_schedules as G

DAY = "2030-01-01"
T0 = G.day_start_us(DAY) + 3_600_000_000
E4CFG, SC = E4.load_cfg()
MD = E4.md_us(SC)
DD = SC["features"]["decision_delay_us"]


def synth(n=6_000, seed=0) -> DG.Arrays:
    rng = np.random.default_rng(seed)
    te = T0 + np.cumsum(rng.integers(50_000, 150_000, n))
    te[3_000:3_003] = te[2_999] + 120_000             # tied exchange times
    te = np.maximum.accumulate(te)
    tr = te + 2_000
    tr[4_000:4_004] = tr[4_000]                       # a batch received together
    tr = np.maximum.accumulate(tr)
    mid = 10_000 + np.cumsum(rng.choice([-1, 0, 0, 0, 1], n))
    bpx = np.column_stack([(mid - k) * 0.01 for k in range(10)])
    apx = np.column_stack([(mid + 1 + k) * 0.01 for k in range(10)])
    bq = np.round(rng.uniform(0.5, 20, (n, 10)), 3)
    aq = np.round(rng.uniform(0.5, 20, (n, 10)), 3)
    m = 12_000
    tt = np.sort(rng.integers(te[0] + 1, te[-1], m))
    tl = (tt + rng.integers(1_000, 40_000, m)).astype(float)
    tl[::997] = np.nan                                # some trades never received
    tq = np.round(rng.uniform(0.01, 5, m), 3)
    ta = rng.choice([-1.0, 1.0], m)
    tid = 1_000 + np.arange(m, dtype=np.int64)
    tid[5_000:] += 1                                  # a natural gap in the archive ids
    eps = [(int(te[0]), int(te[2_499])), (int(te[2_520]), int(te[-1]))]
    return DG.Arrays(DAY, te, tr, bpx, bq, apx, aq, tt, tl, tq, ta, tid, eps)


def stalls(A: DG.Arrays, every_us=20_000_000, dur_us=2_500_000) -> np.ndarray:
    s = np.arange(int(A.te[0]) + 70_000_000, int(A.te[-1]), every_us)
    return G.merge(np.column_stack([s, s + dur_us]))


def part_of(A, kind, iv=None, noise=None):
    D = DG.deliver(A, kind, iv, noise)
    rec = DG.record_features(A, D, 0.01, DD)
    return D, rec, FC.participant_rows(A, D, rec, DD, MD)


def copy_arrays(A: DG.Arrays) -> DG.Arrays:
    return DG.Arrays(A.day, *(np.array(getattr(A, f), copy=True) for f in
                              ("te", "tr", "bpx", "bq", "apx", "aq", "tt", "tl", "tq", "ta", "tid")), list(A.eps))


# ------------------------------------------------------------------------------------------------ delivery streams
def test_d0_is_the_identity_and_matches_e003_features():
    A = synth()
    D, rec, part = part_of(A, "none")
    assert np.array_equal(part["view_row"], A.rows) and part["has"].all()
    for (s0, s1), (j0, j1), (a, b) in zip(A.ep_states, A.ep_trades, A.eps):
        ref = F.episode_features(A.te[s0:s1], A.tr[s0:s1], A.bpx[s0:s1], A.bq[s0:s1], A.apx[s0:s1], A.aq[s0:s1],
                                 A.tt[j0:j1], A.tl[j0:j1], A.tq[j0:j1], A.ta[j0:j1], 0.01, a, b, DD, [])
        o = np.searchsorted(A.rows, s0)
        for c in F.REGRESSORS:
            assert np.array_equal(part[c][o:o + s1 - s0], ref[c])


@pytest.mark.parametrize("kind", ["book_stall_withhold", "connection_drop_withhold", "catchup_delay"])
def test_delivery_order_resync_and_fifo(kind):
    A = synth()
    iv = stalls(A)
    D = DG.deliver(A, kind, iv)
    w, end = DG.inside(A.tr, iv)
    assert np.all(D.d >= A.tr[D.idx]) and np.all(np.diff(D.d) >= 0) and np.all(np.diff(D.idx) > 0)
    if kind == "catchup_delay":                       # every record, in order, stalled ones at the stall end (FIFO)
        assert np.array_equal(D.idx, A.rows)
        assert np.array_equal(D.d, np.where(w[A.rows], end[A.rows], A.tr[A.rows]))
    else:
        lost = set(A.rows[w[A.rows]].tolist()) - set(D.idx.tolist())
        assert lost and not (set(D.idx[~D.resync].tolist()) & set(A.rows[w[A.rows]].tolist()))
        for p in np.flatnonzero(D.resync):            # a resync is the last state received by the stall end
            j = D.idx[p]
            assert w[j] and D.d[p] == end[j]
            later = A.rows[(A.rows > j)]
            assert later.size == 0 or A.tr[later[0]] > D.d[p] or not any(
                s0 <= j < s1 and s0 <= later[0] < s1 for s0, s1 in A.ep_states)
    trades_lost = (~D.trade_ok).sum()
    assert (trades_lost > 0) == (kind == "connection_drop_withhold")


def test_poison_withheld_records_do_not_reach_the_participant():
    for kind in ("book_stall_withhold", "connection_drop_withhold", "trade_outage_withhold"):
        A = synth()
        iv = stalls(A)
        D, rec, part = part_of(A, kind, iv)
        g = DG.gap_flags(A, D, D.trade_ok, 10_000_000)
        P = copy_arrays(A)
        delivered = np.zeros(A.te.size, bool)
        delivered[D.idx] = True
        bad = ~delivered
        P.bq[bad], P.aq[bad] = 1e9, 7e8                  # withheld states: garbage sizes and prices
        P.bpx[bad] += 3.0
        P.apx[bad] += 3.0
        lost = ~D.trade_ok
        P.tq[lost], P.ta[lost], P.tid[lost] = 999.0, -P.ta[lost], -12345   # withheld trades and ids
        P = DG.Arrays(P.day, P.te, P.tr, P.bpx, P.bq, P.apx, P.aq, P.tt, P.tl, P.tq, P.ta, P.tid, P.eps)
        D2, rec2, part2 = part_of(P, kind, iv)
        assert np.array_equal(D.idx, D2.idx) and np.array_equal(D.d, D2.d)
        for c in F.REGRESSORS:
            assert np.array_equal(part[c], part2[c]), (kind, c)
        assert np.array_equal(g, DG.gap_flags(P, D2, D2.trade_ok, 10_000_000))
        assert bad.any() or lost.any()


def test_poison_true_sizes_of_noisy_states_do_not_reach_the_participant():
    A = synth()
    iv = np.array([[int(A.tr[1_000]), int(A.tr[3_000])]], np.int64)
    D = DG.deliver(A, "size_noise", iv, (G.stream(1, 7, DAY, 1, 0, 1), 0.5, 0.001))
    rec = DG.record_features(A, D, 0.01, DD)
    A.bq[D.noisy], A.aq[D.noisy] = 1e9, 1e9            # true sizes of noisy states: garbage after delivery
    rec2 = DG.record_features(A, D, 0.01, DD)
    for c in F.REGRESSORS:
        assert np.array_equal(rec[c], rec2[c]), c


def test_participant_features_are_causal():
    A = synth()
    iv = stalls(A)
    for kind in ("connection_drop_withhold", "catchup_delay"):
        D, rec, part = part_of(A, kind, iv)
        k = int(np.searchsorted(A.rows, 4_100))
        cut = A.tr[A.rows[k]] + DD - MD                  # records delivered after t_k - md must not matter
        d_state = np.full(A.te.size, np.iinfo(np.int64).max)
        d_state[D.idx] = D.d
        P = copy_arrays(A)
        late = d_state > cut
        P.bq[late] *= 3.3
        P.bpx[late] -= 0.07
        P.apx[late] -= 0.07
        lt = ~(A.tl <= cut) | ~D.trade_ok
        P.tq[lt] *= 5.0
        P.ta[lt] *= -1
        P = DG.Arrays(P.day, P.te, P.tr, P.bpx, P.bq, P.apx, P.aq, P.tt, P.tl, P.tq, P.ta, P.tid, P.eps)
        _, _, part2 = part_of(P, kind, iv)
        before = (A.tr[A.rows] + DD - MD) <= cut          # every row decided by the cut, not just row k
        for c in F.REGRESSORS:
            assert np.array_equal(part[c][before], part2[c][before]), (kind, c)
        assert np.array_equal(part["age_us"][before], part2["age_us"][before])
        assert before.sum() > 1_000 and late.any() and lt.any()
        assert not all(np.array_equal(part[c], part2[c]) for c in F.REGRESSORS)   # the perturbation bites later


def test_targets_never_enter_participant_rows_or_indicators():
    A = synth()
    iv = stalls(A)
    D, rec, part = part_of(A, "book_stall_withhold", iv)
    y = np.random.default_rng(0).standard_normal(A.rows.size)
    ft = pl.DataFrame({"row": A.rows, "eligible": np.ones(A.rows.size, bool), "y_5s": y})
    b1 = E4.indicator(E4CFG, SC, A, D, part, "D1_S", iv)
    yv = FC.y_view(A, part, y)
    ft2 = ft.with_columns(pl.Series("y_5s", y * 7 + 3))
    _, _, part2 = part_of(A, "book_stall_withhold", iv)
    assert all(np.array_equal(part[c], part2[c]) for c in F.REGRESSORS)
    assert np.array_equal(b1, E4.indicator(E4CFG, SC, A, D, part2, "D1_S", iv))
    # y_view = 1e4 log(mid_ref(t_k + 5 s) / mid(S_j(k))) = y_k + log-mid(k) - log-mid(j(k)); exact y_k where j = k
    j = part["view_row"]
    lm = A.log_mid_bp
    assert np.allclose(yv, y + lm[A.rows] - lm[j]) and np.array_equal(yv[j == A.rows], y[j == A.rows])
    assert ft2["y_5s"][0] != ft["y_5s"][0]


def test_size_noise_properties():
    A = synth()
    iv = np.array([[int(A.tr[1_000]), int(A.tr[3_000])]], np.int64)
    rng = G.stream(1, 7, DAY, 1, 0, 1)
    D = DG.deliver(A, "size_noise", iv, (rng, 0.5, 0.001))
    noisy = D.noisy
    assert noisy.sum() == 2_000 and np.array_equal(D.idx, A.rows)
    assert np.array_equal(D.bq[~noisy], A.bq[~noisy]) and np.array_equal(D.aq[~noisy], A.aq[~noisy])
    lots = D.bq[noisy] / 0.001
    assert np.allclose(lots, np.rint(lots)) and D.bq[noisy].min() >= 0.001
    assert abs(np.mean(D.bq[noisy] / A.bq[noisy]) - 1) < 0.02    # mean-preserving multiplier
    # same stream, same draw indexed by state
    D2 = DG.deliver(A, "size_noise", iv, (G.stream(1, 7, DAY, 1, 0, 1), 0.5, 0.001))
    assert np.array_equal(D.bq, D2.bq)
    D3 = DG.deliver(A, "size_noise", iv, (G.stream(1, 7, DAY, 3, 0, 1), 0.5, 0.001))
    assert not np.array_equal(D.bq, D3.bq)
    big = A.bq[noisy] > 5                                # rounding to lots negligible: log ratio ~ N(-s^2/2, s^2)
    lr = np.log(D.bq[noisy][big] / A.bq[noisy][big])
    assert abs(lr.std() - 0.5) < 0.01 and abs(lr.mean() + 0.125) < 0.01
    # indexed by state: a different regime schedule elsewhere leaves a state's noisy sizes unchanged
    iv2 = np.array([[int(A.tr[2_000]), int(A.tr[5_000])]], np.int64)
    D4 = DG.deliver(A, "size_noise", iv2, (G.stream(1, 7, DAY, 1, 0, 1), 0.5, 0.001))
    both = D.noisy & D4.noisy
    assert both.sum() == 1_000 and np.array_equal(D.bq[both], D4.bq[both])


def test_gap_flag_triggers_on_withheld_ids_and_natural_gaps():
    A = synth()
    D0 = DG.deliver(A, "none")
    g0 = DG.gap_flags(A, D0, D0.trade_ok, 10_000_000)
    iv = stalls(A, dur_us=4_000_000)
    D2 = DG.deliver(A, "trade_outage_withhold", iv)
    g2 = DG.gap_flags(A, D2, D2.trade_ok, 10_000_000)
    assert g0.any() and g2.mean() > g0.mean()          # natural recorder gaps (missing receipt, archive gap) and outages


# ------------------------------------------------------------------------------------------------ forecast level
def test_bucket_edges_and_pooling():
    assert FC.age_bucket(np.array([0, 650_000, 650_001, 1_000_000, 3_000_001, 10_000_001, np.inf]),
                         [0.65, 1, 3, 10]).tolist() == [0, 0, 1, 1, 3, 4, 4]
    assert FC.pool(np.array([10_000, 3_000, 6_000, 100, 0]), 5_000).tolist() == [0, 0, 1, 1, 1]
    assert FC.pool(np.array([100, 6_000, 6_000, 6_000, 6_000]), 5_000).tolist() == [0, 0, 1, 2, 3]
    assert FC.pool(np.array([10, 10]), 5_000).tolist() == [0, 0]


@pytest.mark.parametrize("target", ["y_k", "y_view"])
def test_lambda_recovery_on_a_known_ar_process(target):
    """Mid increments r_t = phi r_(t-1) + e. REF forecasts y_k = lm(k+h) - lm(k) with c_h r_k; NV uses r_(k-a).
    Then lambda(a) = phi^a for y_k, and phi^a + (1 - phi^a) / (1 - phi^h) for y_view = lm(k+h) - lm(k-a)."""
    rng = np.random.default_rng(3)
    phi, h, n = 0.6, 3, 400_000
    r = np.zeros(n)
    e = rng.standard_normal(n)
    for t in range(1, n):
        r[t] = phi * r[t - 1] + e[t]
    lm = np.cumsum(r)
    c = phi * (1 - phi ** h) / (1 - phi)
    ages = rng.integers(0, 4, n)
    k = np.arange(10, n - h)
    a = ages[k]
    f = c * r[k - a]
    y = lm[k + h] - lm[k] if target == "y_k" else lm[k + h] - lm[k - a]
    day = np.where(k % 5 == 0, "s1", "s2")             # unequal session sizes: weights 1 / rows of the session
    lam = FC.fit_lambda(f, y, day, a, 4)
    expect = phi ** np.arange(4) if target == "y_k" else phi ** np.arange(4) + (1 - phi ** np.arange(4)) / (1 - phi ** h)
    assert np.allclose(lam, expect, atol=0.02), (lam, expect)
    w = FC.session_weights(day)
    assert np.isclose(w[day == "s1"].sum(), 1.0) and np.isclose(w[day == "s2"].sum(), 1.0)


def test_training_uses_only_training_draws_of_earlier_sessions(monkeypatch):
    A = synth()
    roles = []
    real = G.schedule

    def spy(cfg, cell, day, role, rep):
        roles.append(role)
        return real(cfg, cell, day, role, rep)
    monkeypatch.setattr(G, "schedule", spy)
    ft = pl.DataFrame({"row": A.rows, "eligible": A.te[A.rows] >= A.te[A.rows][0] + 60_000_000,
                       "y_5s": np.zeros(A.rows.size)})
    tr = E4.training_rows(E4CFG, SC, A, ft, "D1_S")
    assert set(roles) == {"train", "placebo_train"}
    m2 = F.LinearModel(tuple(F.REGRESSORS), (-1e9,) * 8, (1e9,) * 8, (0.0, 1.0) + (0.0,) * 7, ("x",), 1)
    with pytest.raises(AssertionError):
        E4.fit_cell(E4CFG, SC, tr, m2, "D1_S", DAY)       # same session: not earlier
    bad = dict(tr, seed_role=np.ones_like(tr["seed_role"]))
    with pytest.raises(AssertionError):
        E4.fit_cell(E4CFG, SC, bad, m2, "D1_S", "2031-01-01")


# ------------------------------------------------------------------------------------------------ windows
def test_stale_spells_and_placebo_images():
    vt = np.array([100, 200, 1_000, 1_100, 3_000])
    vte = np.array([90, 150, 300, 1_090, 2_990])
    sp = PO.stale_spells(vt, vte, lo=0, b=5_000, tau_us=500)
    # record 2 (te 300) is stale on delivery at 1000 (max(1000, 800)); record 1 stale from 650 until 1000
    assert sp.tolist() == [[650, 1_100], [1_590, 3_000], [3_490, 5_001]]
    rng = np.random.default_rng(0)
    img, rd = PO.placebo_images(sp, 0, 5_001, rng, 0.25, 0.75, 1_000)
    L = 5_001
    assert sorted((img[:, 1] - img[:, 0]).tolist()) == sorted((sp[:, 1] - sp[:, 0]).tolist())
    assert np.all(img[:, 0] >= 0) and np.all(img[:, 1] <= L)
    k = np.argsort(img[:, 0])
    assert np.all(img[k][1:, 0] > img[k][:-1, 1])     # no touching images: still maximal spells
    full = np.array([[0, 2_400], [2_500, 5_001]])     # nearly the whole span: no valid rotation exists
    assert PO.placebo_images(full, 0, 5_001, np.random.default_rng(0), 0.25, 0.75, 50) == (None, 50)


def test_placebo_seam_rule_redraws_cut_images():
    # a long spell is cut by many offsets: those are redrawn, the accepted images are whole
    sp = np.array([[0, 10], [500, 900]])
    rds = []
    for seed in range(30):
        img, rd = PO.placebo_images(sp, 0, 1_000, np.random.default_rng(seed), 0.25, 0.75, 1_000)
        rds.append(rd)
        k = np.argsort(img[:, 0])
        assert img[k][1, 0] > img[k][0, 1] and np.all(img[:, 0] >= 0) and np.all(img[:, 1] <= 1_000)
        assert sorted((img[:, 1] - img[:, 0]).tolist()) == [10, 400]
    assert max(rds) > 0
    # spells adjacent across the seam: every rotation either cuts one or makes them touch -> excluded at the cap
    assert PO.placebo_images(np.array([[0, 10], [990, 1_000]]), 0, 1_000, np.random.default_rng(0), 0.25, 0.75,
                             1_000) == (None, 1_000)


# ------------------------------------------------------------------------------------------------ engine options
def to_engine(A: DG.Arrays):
    st = [X.State(int(A.te[i]), int(A.tr[i]),
                  tuple((int(round(A.bpx[i, l] / 0.01)), float(A.bq[i, l])) for l in range(10)),
                  tuple((int(round(A.apx[i, l] / 0.01)), float(A.aq[i, l])) for l in range(10)), {"M2": 0.0})
          for i in range(A.te.size)]
    px = np.rint((A.bpx[0, 0] / 0.01)).astype(int)
    trades = [X.Trade(int(t), int(px + (3 if a > 0 else -3)), float(q), int(a)) for t, q, a in zip(A.tt, A.tq, A.ta)]
    return st, trades


def sim_views(A, D, states, f=None):
    f = np.zeros(D.idx.size) if f is None else f
    return [PO.episode_views(states, s0, D.idx[p0:p1], D.d[p0:p1], f[p0:p1], MD, b)
            for (a, b), (s0, _), (p0, p1) in zip(A.eps, A.ep_states, D.ep_pos)]


def test_view_path_with_d0_reproduces_per_state_decisions_and_mutates_nothing():
    A = synth()
    states, trades = to_engine(A)
    sd = E3.SessionData(states, trades, A.eps, SC)
    h = E4.state_hash(states, trades)
    ref, fr = E3.simulate(sd, "P0", "intermediate", "regional", None)
    D = DG.deliver(A, "none")
    v = sim_views(A, D, states)
    hv = E4.views_hash(v)
    agg, fills = E3.simulate(sd, "P0", "intermediate", "regional", None, views=v)
    assert E4._agg_equal(agg, ref) and fills == fr and len(fills) > 0
    assert E4.state_hash(states, trades) == h and E4.views_hash(v) == hv


def test_view_prices_must_equal_true_prices():
    A = synth()
    states, trades = to_engine(A)
    D = DG.deliver(A, "none")
    v = sim_views(A, D, states)
    t, src, s = v[0][100]
    v[0][100] = (t, src, X.State(s.t_exch, s.t_recv, ((s.bids[0][0] - 1, 1.0),) + s.bids[1:], s.asks, s.aux))
    with pytest.raises(AssertionError):
        E3.simulate(E3.SessionData(states, trades, A.eps, SC), "P0", "intermediate", "regional", None, views=v)


def test_scripted_extra_decision_policy_has_identical_fills_under_clean_and_degraded_views():
    A = synth()
    states, trades = to_engine(A)
    low = min(s.bids[0][0] for s in states) - 2        # never crosses the ask: never rejected
    sell = [X.Trade(int(t), int(low - 1), 0.5, -1) for t in A.tt[::40]]   # trades through the quote fill it
    trades = sorted(trades + sell, key=lambda x: x.t)
    sd = E3.SessionData(states, trades, A.eps, SC)
    xs = np.arange(int(A.te[0]) + 80_000_000, int(A.te[-1]), 7_000_000)

    def scripted(v: X.View):
        i = int(np.searchsorted(xs, v.t, side="right")) - 1
        return {X.BID: X.Quote(int(low), 1.0)} if i >= 0 and i % 2 == 0 else {}
    ex = [[int(x) for x in xs if a <= x <= b] for a, b in A.eps]
    out = []
    for kind, iv in (("none", None), ("connection_drop_withhold", stalls(A)), ("catchup_delay", stalls(A))):
        D = DG.deliver(A, kind, iv)
        v = sim_views(A, D, states)
        h, hv = E4.state_hash(states, trades), E4.views_hash(v)
        agg, fills = E3.simulate(sd, "P0", "intermediate", "regional", None, pol=scripted, views=v, extras=ex)
        assert E4.state_hash(states, trades) == h and E4.views_hash(v) == hv
        out.append(fills)
    assert len(out[0]) > 10 and out[0] == out[1] == out[2]


def run_variants(A, states, trades, tau_us, iv):
    sd = E3.SessionData(states, trades, A.eps, SC)
    D = DG.deliver(A, "connection_drop_withhold", iv)
    W = E4.windows(E4CFG, SC, sd, A, D, np.zeros(D.idx.size), "D1_E", 0) if tau_us is None else None
    return sd, D, W


def test_u_rule_equals_w_u_membership_and_empty_windows_give_identical_variants(monkeypatch):
    A = synth()
    states, trades = to_engine(A)
    sd = E3.SessionData(states, trades, A.eps, SC)
    D = DG.deliver(A, "connection_drop_withhold", stalls(A))
    W = E4.windows(E4CFG, SC, sd, A, D, np.zeros(D.idx.size), "D1_E", 0)
    assert W.wu.shape[0] > 0 and (W.wu[:, 1] - W.wu[:, 0]).sum() == (W.wp[:, 1] - W.wp[:, 0]).sum()
    assert sorted((W.wu_spells[:, 1] - W.wu_spells[:, 0]).tolist()) == sorted((W.wp_images[:, 1] - W.wp_images[:, 0]).tolist())
    for ep, x in enumerate(W.extras):                    # extras at every W_U start and both W_P edges (inside the episode)
        a, b = A.eps[ep]
        want = {int(s) for s in np.concatenate([W.wu_full[:, 0], W.wp[:, 0], W.wp[:, 1]]) if a + 60_000_000 <= s <= b}
        assert set(x) == want
    st = {}
    h, hv = E4.state_hash(states, trades), E4.views_hash(W.views)
    pol = PO.withdraw_when_stale(X.p0_fixed(1.0, 10.0), W.vt, W.vte, 650_000, W.wu_full, st)
    E3.simulate(sd, "P0", "intermediate", "regional", None, pol=pol, views=W.views, extras=W.extras)
    assert st["decisions"] > 0 and st["withdrawn"] > 0           # the assertion inside held at every decision
    assert E4.state_hash(states, trades) == h and E4.views_hash(W.views) == hv
    # empty windows (tau beyond any age): U = P = N bit for bit
    cfg = dict(E4CFG, indicators=dict(E4CFG["indicators"], tau_ms=10 ** 9))
    W0 = E4.windows(cfg, SC, sd, A, D, np.zeros(D.idx.size), "D1_E", 0)
    assert W0.wu.shape[0] == 0 and W0.wp.shape[0] == 0 and not any(W0.extras)
    res = []
    for var in ("N", "U", "P"):
        b = X.p0_fixed(1.0, 10.0)
        p = b if var == "N" else (PO.withdraw_when_stale(b, W0.vt, W0.vte, 10 ** 15, W0.wu_full, {}) if var == "U"
                                  else PO.withdraw_in_windows(b, W0.wp, {}))
        res.append(E3.simulate(sd, "P0", "intermediate", "regional", None, pol=p, views=W0.views, extras=W0.extras))
    assert E4._agg_equal(res[0][0], res[1][0]) and E4._agg_equal(res[0][0], res[2][0])
    assert res[0][1] == res[1][1] == res[2][1]


def test_window_sums_count_orders_once_per_replicate_and_episode():
    # order id 1 is filled twice in episode 0 and once in episode 1 (ids restart per episode): two distinct orders
    fills = [X.Fill(100, 1, X.BID, 1000, 1.0, 0.0, 1000.5, "at_price"), X.Fill(150, 1, X.BID, 1000, 1.0, 0.0, 1000.5, "at_price"),
             X.Fill(1_200, 1, X.ASK, 1001, 2.0, 0.0, 1000.5, "at_price"), X.Fill(1_290, 2, X.ASK, 1001, 1.0, 0.0, 1000.5, "at_price")]
    eps = [(0, 1_000), (1_100, 2_000)]
    fa = PO.fill_arrays(fills, 0.01, eps)
    assert fa["ep"].tolist() == [0, 0, 1, 1]
    p5, ok = np.array([0.5, -0.1, 0.2, 0.3]), np.array([True, True, True, False])
    # W = [0, 1170) on the participant clock; W^x = W + 30: the fill at 1200 is inside (1200 - 30 = 1170 is not)
    s = E4.window_sums(fa, p5, ok, np.array([[0, 1_170]]), entry_us=30, rep=2)
    assert s["orders"] == {(2, 0, 1)} and s["fills"] == 2
    s = E4.window_sums(fa, p5, ok, np.array([[0, 1_171]]), entry_us=30, rep=2)
    assert s["orders"] == {(2, 0, 1), (2, 1, 1)} and s["notional"] == pytest.approx(10 + 10 + 20.02)
    assert s["pi5"] == pytest.approx(0.6)                 # the fill beyond its episode end (ok False) is excluded


def test_pi5_excludes_fills_whose_horizon_passes_the_episode_end():
    fills = [X.Fill(100, 1, X.BID, 1000, 1.0, 0.0, 1000.5, "at_price"), X.Fill(900, 2, X.ASK, 1001, 1.0, 0.0, 1000.5, "at_price")]
    eps = [(0, 1_000)]
    fa = PO.fill_arrays(fills, 0.01, eps)
    p5, ok = PO.pi5(fa, eps, np.array([0, 300]), np.array([10.0, 10.5]), h_us=200)
    assert ok.tolist() == [True, False] and p5[0] == pytest.approx(1.0 * (10.5 - 10.0))


# ------------------------------------------------------------------------------------------------ labels
A_CFG = {**E4CFG["analysis"]}


def test_h4w_labels_on_synthetic_sessions():
    lab = lambda x, ci: AN.h4w_label(np.array(x, float), ci, A_CFG)[0]
    ten = [2.0] * 10
    assert lab(ten, [1.5, 2.5]) == AN.SUPPORTED
    assert lab([2.0] * 7 + [-1.0] * 3, [1.2, 2.5]) == AN.INCONCLUSIVE           # sign count 7 < 8
    assert lab([0.2] * 10, [0.0, 0.5]) == AN.IMMATERIAL
    assert lab([0.2] * 7 + [np.nan] * 3, [0.0, 0.5]) == AN.NOT_TESTABLE        # 7 defined sessions
    assert lab([0.2] * 8 + [np.nan] * 2, [0.0, 0.5]) == AN.IMMATERIAL           # undefined sessions excluded
    assert AN.h4w_label(np.array([1.0] * 10), [-1.0, 2.0], A_CFG) == (AN.INCONCLUSIVE, ["underpowered"])


def windows_table(dw, orders=100, wd=0.03, ov=0.02, stall=None):
    days = [f"2026-0{i}-01" for i in range(1, 10)] + ["2026-10-01"]
    stall = dw if stall is None else stall
    return pl.DataFrame({"day": days, "cell": "D1_E", "base": "P0", "fill_model": "intermediate", "latency": "regional",
                         "D_W_bp": dw, "orders_U": orders, "orders_P": orders, "withdrawn_share": wd,
                         "overlap_share_of_wp": ov, "D_W_stall_bp": stall, "orders_U_stall": orders,
                         "orders_P_stall": orders, "q_U_bp": -3.0, "q_P_bp": -1.0, "wu_time_share_nostall": 0.1,
                         "wu_fill_share_nostall": 0.1, "wp_time_share_install": 0.05, "wp_fill_share_install": 0.05,
                         "placebo_redraws": 0, "episodes_excluded": 0})


def test_h4w_gates_qualifiers_and_undefined_sessions():
    cfg = E4CFG
    rng = np.random.default_rng(1)
    dw = list(2.0 + 0.1 * rng.standard_normal(10))
    assert AN.h4w(windows_table(dw), "P0", cfg)["label"] == AN.SUPPORTED
    assert AN.h4w(windows_table(dw, wd=0.004), "P0", cfg)["label"] == AN.NOT_TESTABLE
    assert AN.h4w(windows_table(dw, ov=0.2), "P0", cfg)["label"] == AN.NOT_TESTABLE
    assert AN.h4w(windows_table(dw, orders=[19] * 3 + [100] * 7), "P0", cfg)["label"] == AN.NOT_TESTABLE
    r = AN.h4w(windows_table(dw, stall=[0.1] * 10), "P0", cfg)
    assert r["label"] == AN.SUPPORTED and "sensitive to natural staleness" in r["notes"]


def forecast_table(L, A_, B_, cells=("D1_S",), target="y_k"):
    rows = []
    days = [f"2026-0{i}-01" for i in range(1, 10)] + ["2026-10-01"]
    for c in cells:
        for i, d in enumerate(days):
            ref = 4.0
            nv = ref - L[i]
            ua = nv + A_[i]
            rows += [{"day": d, "cell": c, "target": target, "model": m, "r2_os_pp": v} for m, v in
                     (("REF", ref), ("NV", nv), ("UA-lambda", ua), ("PL-lambda", ua - B_[i]), ("RF-lambda", nv))]
    return pl.DataFrame(rows), days


def test_h4f_labels_in_order():
    fc, days = forecast_table([0.8] * 10, [0.3] * 10, [0.25] * 10)
    assert AN.h4f(fc, "D1_S", "y_k", E4CFG, days)["label"] == "supported"
    fc, days = forecast_table([0.1] * 10, [0.05] * 10, [0.04] * 10)
    assert AN.h4f(fc, "D1_S", "y_k", E4CFG, days)["label"] == AN.NOT_TESTABLE        # L below 0.20 pp
    fc, days = forecast_table([0.8] * 10, [0.3] * 10, [0.0] * 10)
    assert AN.h4f(fc, "D1_S", "y_k", E4CFG, days)["label"] == "recalibration only"
    fc, days = forecast_table([0.8] * 10, [-0.1] * 10, [0.0] * 10)
    r = AN.h4f(fc, "D1_S", "y_k", E4CFG, days)
    assert r["label"] == "not supported" and r["notes"] == ["UA harmful"]


def test_h40_labels():
    days = [f"2026-0{i}-01" for i in range(1, 10)] + ["2026-10-01"]
    for diff, lab in ((-0.01, "harmless"), (-0.2, "costly")):
        fc = pl.DataFrame([{"day": d, "cell": "D0", "target": "y_k", "model": m, "r2_os_pp": v}
                           for d in days for m, v in (("REF", 4.0), ("UA-lambda[D1_S]", 4.0 + diff))])
        assert AN.h40(fc, E4CFG, days)["label"] == lab


def test_descriptive_policy_and_window_tables_run_on_synthetic_rows():
    rng = np.random.default_rng(5)
    days = [f"2026-0{i}-01" for i in range(1, 10)] + ["2026-10-01"]
    g, n = [], []
    for d in days:
        for base in ("P0", "P3_M2"):
            for var in ("N", "U", "P"):
                for r in range(3):
                    row = {"day": d, "cell": "D1_E", "replicate": r, "base": base, "variant": var,
                           "fill_model": "intermediate", "latency": "regional", "gross_marked": rng.normal(-50, 5),
                           "liquidation_slippage": 1.0, "filled_notional": 1e5 * rng.uniform(0.8, 1.2),
                           "valid_hours": 10.0, "pi5_usdt": rng.normal(-20, 2), "pi5_notional": 9e4,
                           "quote_both_s": 3e4 * rng.uniform(0.8, 1.0), "fills": int(rng.integers(500, 800))}
                    g.append(row)
                    for fee in ("vip0", "lp_tier4"):
                        n.append({**row, "fee_schedule": fee, "net": row["gross_marked"] - 100.0})
    w = pl.concat([windows_table([1.0] * 10), windows_table([1.0] * 10).with_columns(pl.lit("P3_M2").alias("base"))])
    w = w.with_columns(pl.lit(4e3).alias("notional_U"), pl.lit(1e5).alias("n_notional_defined"),
                                                pl.lit(-5.0).alias("pi5_U_usdt"), pl.lit(-2.0).alias("pi5_P_usdt"),
                                                pl.lit(30.0).alias("n_valid_hours"), pl.lit(3).alias("replicates"))
    cfg = dict(E4CFG, _fees=SC["fees"], policies={**SC["policies"], **E4CFG["policies"]})
    out = AN.descriptive_policy(pl.DataFrame(g), pl.DataFrame(n), w, cfg, "D1_E")
    up = out["P0"]["U-P"]
    assert up["delta_gross_bp"]["defined"] == 10 and "avoided_loss_rate_usdt_per_hour" in up
    assert up["n_notional_share_in_wu"] == pytest.approx(0.04)
    assert set(AN.window_descriptive(w, cfg)) == {"D1_E:P0:intermediate:regional", "D1_E:P3_M2:intermediate:regional"}


def test_more_label_branches():
    a = A_CFG
    # mean above delta but lower bound below delta: inconclusive, not supported
    assert AN.h4w_label(np.array([1.5] * 10), [0.8, 2.2], a)[0] == AN.INCONCLUSIVE
    # sign count for immaterial uses D_W < delta: values in (0, delta) count
    assert AN.h4w_label(np.array([0.5] * 8 + [3.0] * 2), [0.2, 0.9], a)[0] == AN.IMMATERIAL
    assert AN.h4w_label(np.array([0.5] * 7 + [3.0] * 3), [0.2, 0.9], a)[0] == AN.INCONCLUSIVE
    # Bonferroni flip: a label that changes under 97.5% intervals is marked
    rng = np.random.default_rng(3)
    for s in range(200):
        dw = list(1.0 + 0.6 + 0.35 * np.random.default_rng(s).standard_normal(10))
        r = AN.h4w(windows_table(dw), "P0", E4CFG)
        if r["label"] == AN.SUPPORTED and r["bonferroni_label"] != AN.SUPPORTED:
            assert "not robust to multiplicity" in r["notes"]
            break
    else:
        pytest.fail("no Bonferroni flip found in 200 synthetic draws")
    # identical stall-only data never adds the natural-staleness qualifier
    dw = list(2.0 + 0.3 * rng.standard_normal(10))
    assert "sensitive to natural staleness" not in AN.h4w(windows_table(dw, stall=dw), "P0", E4CFG)["notes"]


def test_h4f_inconclusive_interval_rule_projection_and_descriptive_cells():
    rng = np.random.default_rng(2)
    L = [1.5, -1.0, 1.4, -0.9, 1.2, -0.8, 1.3, -1.1, 0.9, 0.0]   # mean 0.25 >= 0.20 but the interval includes 0
    fc, days = forecast_table(L, [0.2] * 10, [0.1] * 10)
    assert AN.h4f(fc, "D1_S", "y_k", E4CFG, days)["label"] == AN.NOT_TESTABLE
    A_ = list(0.2 + 0.15 * rng.standard_normal(10))
    fc, days = forecast_table([0.8] * 10, A_, [0.05] * 10, cells=("D1_S", "D4", "D1_S1"))
    r = AN.h4f(fc, "D1_S", "y_k", E4CFG, days)
    assert r["label"] == AN.INCONCLUSIVE and r["rho_A"]["sessions"] == 10 and r["projection"]["rho_a"] == 0.37
    assert AN.h4f(fc, "D4", "y_k", E4CFG, days)["projection"] is None
    assert AN.h4f(fc, "D4", "y_k", E4CFG, days)["rho_A_minus_projection"] is None
    assert AN.h4f(fc, "D1_S1", "y_k", E4CFG, days)["label"] == "descriptive (no label)"


def test_h40_inconclusive_and_not_testable():
    days = [f"2026-0{i}-01" for i in range(1, 10)] + ["2026-10-01"]
    rng = np.random.default_rng(4)
    diffs = -0.05 + 0.1 * rng.standard_normal(10)
    fc = pl.DataFrame([{"day": d, "cell": "D0", "target": "y_k", "model": m, "r2_os_pp": v}
                       for d, x in zip(days, diffs) for m, v in (("REF", 4.0), ("UA-lambda[D1_S]", 4.0 + x))])
    assert AN.h40(fc, E4CFG, days)["label"] == AN.INCONCLUSIVE
    fc = fc.with_columns(pl.when((pl.col("model") == "REF") & (pl.col("day") < "2026-04-01")).then(None)
                         .otherwise(pl.col("r2_os_pp")).alias("r2_os_pp"))
    assert AN.h40(fc, E4CFG, days)["label"] == AN.NOT_TESTABLE
