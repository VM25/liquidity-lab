"""E003 features, walk-forward forecasts and policies on synthetic inputs (no market data)."""

import numpy as np
import polars as pl
import pytest

from lpx.execution import sim as X
from lpx.execution.sim import ASK, BID, Quote, State, View
from lpx.research import e003_features as F


def synthetic_episode(n=3_000, seed=0, t0=1_000_000):
    rng = np.random.default_rng(seed)
    te = t0 + np.cumsum(rng.integers(50_000, 150_000, n))
    tr = te + 2_000
    mid = 10_000 + np.cumsum(rng.choice([-1, 0, 0, 0, 1], n))
    bpx = np.column_stack([(mid - k) * 0.01 for k in range(10)])
    apx = np.column_stack([(mid + 1 + k) * 0.01 for k in range(10)])
    bq, aq = rng.uniform(0.5, 20, (n, 10)), rng.uniform(0.5, 20, (n, 10))
    tt = np.sort(rng.integers(te[0] + 1, te[-1], 5_000))
    tl = (tt + rng.integers(1_000, 40_000, tt.size)).astype(float)
    tq, ta = np.round(rng.uniform(0.01, 5, tt.size), 3), rng.choice([-1.0, 1.0], tt.size)
    return te, tr, bpx, bq, apx, aq, tt, tl, tq, ta


def feats(ep, t_start, t_end, horizons=(1, 5)):
    return F.episode_features(*ep, tick=0.01, t_start=t_start, t_end=t_end, decision_delay_us=30_000, horizons_s=list(horizons))


def test_features_are_causal_under_perturbation_of_the_future():
    ep = synthetic_episode()
    te = ep[0]
    a, b = int(te[0]), int(te[-1])
    tau = int(te[1_500])
    j = np.searchsorted(ep[6], tau, side="right") - 1
    ep[7][j] = ep[1][1_500] + 50_000            # a trade printed before tau but received after the state at tau
    base = feats(ep, a, b)
    # perturb every state after tau and every trade after tau
    te2, tr2, bpx, bq, apx, aq, tt, tl, tq, ta = (x.copy() for x in ep)
    later = te2 > tau
    bq[later] *= 3.7
    aq[later] = aq[later][::-1]
    bpx[later] -= 0.05
    apx[later] -= 0.05
    tq[tt > tau] *= 9.0
    ta[tt > tau] *= -1
    # trades at or before tau but received after the receipt time of the state at tau: also perturbed
    late = (tt <= tau) & (tl > tr2[1_500])
    assert late.any()
    tq[late] *= 7.0
    ta[late] *= -1
    pert = feats((te2, tr2, bpx, bq, apx, aq, tt, tl, tq, ta), a, b)
    keep = te <= tau
    for c in F.REGRESSORS + ("rv_60s",):
        assert np.array_equal(base[c][keep], pert[c][keep]), c
    # targets do look ahead (by definition) and must differ somewhere before tau: proves the perturbation bites
    assert not np.allclose(np.nan_to_num(base["y_5s"][keep]), np.nan_to_num(pert["y_5s"][keep]))


def test_trades_need_exchange_time_and_receipt_by_the_state():
    te = np.array([1_000_000, 2_000_000, 3_000_000, 4_000_000])
    px = np.column_stack([np.full(4, 100.0 - 0.01 * k) for k in range(10)])
    q = np.ones((4, 10))
    ap = np.column_stack([np.full(4, 100.01 + 0.01 * k) for k in range(10)])
    tt = np.array([2_000_000, 2_000_001, 2_500_000, 2_600_000])
    tl = np.array([2_000_002, 2_000_003, 3_000_500, np.nan])   # third received after state 3; fourth never
    f = F.episode_features(te, te + 2, px, q, ap, q, tt, tl, np.array([1.0, 5.0, 2.0, 9.0]),
                           np.array([1.0, -1.0, 1.0, 1.0]), 0.01, 0, 4_000_000, 0, [1])
    # state 2 (t=2 s, received 2 s + 2 us): only the buy at exactly 2 s (received at +2 us); state 3: the 2.0 buy is
    # not yet received (window (2 s, 3 s]); state 4: window (3 s, 4 s] holds no trade
    assert f["flow_1s"].tolist() == [0.0, 1.0, -1.0, 0.0]
    assert f["flow_10s"].tolist() == [0.0, 1.0, -4 / 6, -2 / 8]
    assert f["trades_unreceived"][0] == 1


def test_features_never_read_outside_the_episode():
    ep = synthetic_episode()
    te = ep[0]
    a, b = int(te[1000]), int(te[2000])
    with pytest.raises(ValueError):
        feats(ep, a, b)  # states outside [a, b] are refused
    s = slice(1000, 2001)
    sl = tuple(x[s] for x in ep[:6])
    tt, tl, tq, ta = ep[6:]
    m = (tt > a) & (tt <= b)
    f = F.episode_features(*sl, tt[m], tl[m], tq[m], ta[m], 0.01, a, b, 30_000, [5])
    assert f["ofi_10s"][0] == 0.0 and f["ret_10s"][0] == 0.0 and f["rv_60s"][0] == 0.0
    assert np.isnan(f["y_5s"][-1])  # target beyond the episode end is undefined


def test_ols_recovers_known_coefficients_and_walk_forward_guard():
    rng = np.random.default_rng(3)
    tables = {}
    for d, n, slope in (("2025-03-01", 40_000, 0.8), ("2025-04-01", 4_000, 0.4), ("2025-05-01", 20_000, 0.8)):
        x = rng.normal(size=(n, 2))
        y = 0.1 + slope * x[:, 0] - 0.3 * x[:, 1] + rng.normal(0, 0.1, n)
        tables[d] = pl.DataFrame({"imb1": x[:, 0], "imb5": x[:, 1], "y_5s": y, "eligible": [True] * n})
    m = F.fit_linear(tables, "2025-05-01", ("imb1", "imb5"), "y_5s", 1, (0.0, 1.0))
    assert m.trained_on == ("2025-03-01", "2025-04-01")
    # sessions weighted equally despite 10x more rows in the first: slope = (0.8 + 0.4) / 2
    assert m.coef == pytest.approx((0.1, 0.6, -0.3), abs=0.01)
    with pytest.raises(ValueError):
        F.fit_linear(tables, "2025-03-01", ("imb1",), "y_5s", 1, (0.0, 1.0))
    f = m.predict(tables["2025-05-01"])
    sk = F.forecast_skill(tables["2025-05-01"]["y_5s"].to_numpy(), f)
    assert sk["r2_os"] > 0.8 and sk["ic"] > 0.9
    assert F.forecast_skill(np.array([1.0, -1.0, np.nan]), np.zeros(3))["r2_os"] == 0.0  # zero forecast: R2_OS = 0


def view(f_ticks=None, inv=0.0, vol_ok=True, bid=15000, ask=15001):
    """aux carries the forecast in bp of mid; tests state it in ticks for readability."""
    mid = (bid + ask) / 2
    f = None if f_ticks is None else f_ticks / mid * 1e4
    s = State(0, 0, ((bid, 5.0),), ((ask, 5.0),), aux={"f": f, "vol_ok": vol_ok})
    return View(0, s, inv, {})


def test_p3_quotes_only_sides_with_positive_expected_mark_to_mid():
    pol = X.p3_alpha(1.0, 10.0, "f")
    assert set(pol(view(0.0))) == {BID, ASK}
    assert set(pol(view(0.6))) == {BID}          # expected up-move > half spread: selling at the ask loses
    assert set(pol(view(-0.6))) == {ASK}
    assert set(pol(view(0.5 + 1e-9))) == {BID}   # just beyond the boundary s/2 - f = 0
    assert pol(view(None)) == {}
    assert set(pol(view(0.6, bid=15000, ask=15002))) == {BID, ASK}  # 2-tick spread: half spread 1 > 0.6
    assert set(pol(view(0.0, inv=9.5))) == {ASK}  # inventory limit as P0
    placebo = X.p3_alpha(1.0, 10.0, "f", sign=-1.0)
    assert set(placebo(view(0.6))) == {ASK} and set(placebo(view(-0.6))) == {BID}
    p3f = X.p3_alpha(1.0, 10.0, "f", maker_fee=0.001)              # c ~ 15 ticks at mid 15000.5
    assert p3f(view(10.0)) == {} and set(p3f(view(16.0))) == {BID}


def test_p4_fee_inventory_and_volatility_gates():
    vip0 = X.p4_combined(1.0, 10.0, 3.0, 0.25, 0.001, "f")      # c = 0.001 * 15000.5 ~ 15 ticks
    assert vip0(view(0.0)) == {} and vip0(view(10.0)) == {}
    assert set(vip0(view(16.0))) == {BID}                       # forecast beyond the fee: buy side only
    reb = X.p4_combined(1.0, 10.0, 3.0, 0.25, -0.00008, "f")    # c ~ -1.2 ticks (rebate)
    assert set(reb(view(0.0))) == {BID, ASK}
    assert set(reb(view(0.0, inv=2.0))) == {BID, ASK}           # f_r = -0.5: still inside the rebate edge
    assert set(reb(view(0.0, inv=3.0))) == {ASK}                # P1 withdrawal at 3 SOL
    assert set(reb(view(-1.0, inv=2.9))) == {ASK}               # f_r = -1.725: bid edge 0.5 - 1.725 + 1.2 < 0
    assert reb(view(0.0, vol_ok=False)) == {}
    assert reb(view(None)) == {}


def test_paced_spells_and_time():
    flip = lambda v: {BID: Quote(100 if (v.t // 10) % 2 else 99, 1.0)} if v.t < 200 else {}
    book = lambda t: State(t, t, ((100, 5.0), (99, 5.0)), ((101, 5.0),))
    c = X.ExecConfig("conservative", 0, 1, 1, 0.0, 0.0, 0.01, 0.001, 0.0, pace_rate_per_s=1.0, pace_burst=2)
    r = X.Simulator(c, flip, [book(i * 10) for i in range(40)], [], t_start=0, t_end=400).run()
    # two sends use the burst; from t=20 the side is wanted but refused until t=200, when it is no longer wanted
    assert r.orders_sent == 2 and r.paced > 1 and r.paced_spells == 1
    assert r.paced_time_s["bid"] == pytest.approx(180 / 1e6) and r.paced_time_s["ask"] == 0.0


# ---------------------------------------------------------------- runner and analysis (synthetic)
import tomllib
from pathlib import Path

from lpx.research import e003, e003_analysis as A

CFG = tomllib.loads((Path(__file__).resolve().parents[1] / "configs" / "e003_v1.toml").read_text())
RC = tomllib.loads((Path(__file__).resolve().parents[1] / "configs" / "research_v1.toml").read_text())


def test_config_windows_match_the_code():
    w = CFG["features"]["windows_s"]
    assert (tuple(w["ofi"]), tuple(w["flow"]), w["ret"], w["rv"]) == (F.WINDOWS_S["ofi"], F.WINDOWS_S["flow"],
                                                                      F.WINDOWS_S["ret"], F.WINDOWS_S["rv"])
    assert tuple(CFG["features"]["regressors_m2"]) == F.REGRESSORS


def test_expected_shortfall_estimator():
    g = [[(0, 0.0, 0.0, 0.0), (1, -5.0, 0.0, 0.0), (2, -4.0, 0.0, 0.0), (3, -4.0, 0.0, 0.0)],
         [(10, 0.0, 0.0, 0.0)] + [(10 + i, float(i % 2), 0.0, 0.0) for i in range(1, 18)]]
    r = e003.risk_from_grid(g, 0.0, 0.0, 0.05)
    # 3 + 17 = 20 increments; ceil(0.05 * 20) = 1 smallest = -5 -> ES = 5 (a positive loss)
    assert r["inc_n"] == 20 and r["inc_es"] == pytest.approx(5.0) and r["inc_worst"] == -5.0
    # fee overlay on the grid: maker on notional, taker on the liquidation proceeds of the end point
    r = e003.risk_from_grid([[(0, 0.0, 0.0, 0.0), (1, 0.0, 100.0, 0.0), (2, 0.0, 100.0, 50.0)]], 0.001, 0.002, 0.5)
    assert r["inc_worst"] == pytest.approx(-0.1)


def synthetic_market(seed=0, n=4_000):
    rng = np.random.default_rng(seed)
    states, t, mid = [], 1_000_000, 10_000
    for _ in range(n):
        t += int(rng.integers(50_000, 150_000))
        mid += int(rng.choice([-1, 0, 0, 0, 1]))
        states.append(X.State(t, t + 2_000, tuple((mid - k, 10.0) for k in range(10)), tuple((mid + 1 + k, 10.0) for k in range(10)),
                              aux={"M1": float(rng.normal(0, 3)), "M2": float(rng.normal(0, 6)), "vol_ok": bool(rng.random() < 0.9)}))
    ts = np.array([s.t_exch for s in states])
    trades = []
    for tt in np.sort(rng.integers(ts[0] + 1, ts[-1], 6_000)):
        s = states[np.searchsorted(ts, tt) - 1]
        a = int(rng.choice([-1, 1]))
        trades.append(X.Trade(int(tt), s.asks[0][0] if a > 0 else s.bids[0][0], float(rng.uniform(0.5, 6.0)), a))
    return states, trades, [(int(ts[0]), int(ts[n // 2])), (int(ts[n // 2 + 100]), int(ts[-1]))]


def test_run_session_overlay_and_invariants_on_a_synthetic_market():
    states, trades, eps = synthetic_market()
    cfg = {**CFG, "fill_models": {"primary": ["intermediate"]}, "latency": {"regional": CFG["latency"]["regional"]}}
    rows = pl.DataFrame(e003.run_session(states, trades, eps, cfg), infer_schema_length=None)
    pols = rows["policy"].to_list()
    assert pols.count("NT") == 1 and pols.count("P0") == 1 and pols.count("P3F") == 3 and pols.count("P4") == 3
    assert (rows["rate_limited"] == 0).all() and rows.filter(pl.col("policy") == "NT")["fills"][0] == 0
    p0 = rows.filter(pl.col("policy") == "P0").row(0, named=True)
    assert p0["fills"] > 0 and 0 < p0["quote_presence_bid"] <= 1 and p0["paced_time_share"] >= 0
    assert p0["gate_active_share"] is None
    p3 = rows.filter(pl.col("policy") == "P3_M2").row(0, named=True)
    assert 0 < p3["gate_active_share"] < 1
    p4 = rows.filter((pl.col("policy") == "P4") & (pl.col("fee_rule") == "lp_tier4")).row(0, named=True)
    assert 0.05 < p4["vol_closed_share"] < 0.2               # synthetic gate closed on ~10% of states
    net = e003.fee_overlay(rows, CFG["fees"])
    for pol, n in (("P0", 3), ("P3_negM2", 3), ("P3F", 3), ("P4", 3), ("NT", 3)):
        assert net.filter(pl.col("policy") == pol).height == n
    # fee-aware rows appear only under their own schedule
    assert (net.filter(pl.col("policy").is_in(["P3F", "P4"]))["fee_rule"] == net.filter(pl.col("policy").is_in(["P3F", "P4"]))["fee_schedule"]).all()
    r = net.filter((pl.col("policy") == "P0") & (pl.col("fee_schedule") == "vip0")).row(0, named=True)
    assert r["net"] == pytest.approx(r["gross_marked"] - r["liquidation_slippage"] - 0.001 * r["filled_notional"]
                                     - 0.001 * r["liquidation_notional"])
    assert r["inc_es"] is not None and r["max_drawdown"] >= 0
    # placebo withdraws as often as P3[M2] (same |forecast|), in the other direction
    q3 = rows.filter(pl.col("policy") == "P3_M2").row(0, named=True)
    qn = rows.filter(pl.col("policy") == "P3_negM2").row(0, named=True)
    assert abs(q3["quote_presence_both"] - qn["quote_presence_both"]) < 0.2


def test_attach_refuses_a_shifted_state():
    states, _, _ = synthetic_market(n=300)
    states = states[:50]
    ft = pl.DataFrame({"t_exch_us": [s.t_exch for s in states[1:]], "t_recv_us": [s.t_recv for s in states[1:]],
                       "row": list(range(49)), "rv_60s": [1.0] * 49, "imb1": [0.0] * 49})
    m = F.LinearModel(("imb1",), (-1.0,), (1.0,), (0.0, 1.0), ("d",), 1)
    with pytest.raises(AssertionError):
        e003.attach(states, ft, {"M1": m, "M2": m}, 2.0)       # rows off by one
    e003.attach(states, ft.with_columns(pl.Series("row", list(range(1, 50)))), {"M1": m, "M2": m}, 2.0)


POLICIES = ["NT", "P0", "P1", "P3_M1", "P3_M2", "P3_negM2", "P3F", "P4"]


def synthetic_tables(eff: dict, r2=(0.02, 0.05), seed=0):
    """eff[(policy, fee)] = {column: session mean}; 10 sessions, small noise."""
    rng = np.random.default_rng(seed)
    days = RC["splits"]["train"][5:] + RC["splits"]["validation"]
    rows = []
    for d in days:
        for pol in POLICIES:
            for fee in ("vip0", "vip9", "lp_tier4"):
                vals = {c: v + rng.normal(0, 0.02 * (1 + abs(v))) for c, v in eff.get((pol, fee), {}).items()}
                base = {"net_per_hour": -100.0, "gross_bp_per_notional": -1.5, "inc_es": 10.0, "max_drawdown": 50.0,
                        "turnover_per_hour": 1e5, "filled_notional": 1e6, "es_per_k_turnover": 0.1,
                        "inventory_per_k_turnover": 0.05, "quote_presence_both": 0.5, "gate_active_share": 0.3}
                rows.append({"day": d, "policy": pol, "fill_model": "none" if pol == "NT" else "intermediate",
                             "latency": "none" if pol == "NT" else "regional", "fee_schedule": fee,
                             **{**base, **vals}})
    fc = pl.DataFrame([{"day": d, "model": m, "horizon_s": 5, "r2_os": v + rng.normal(0, 0.002)}
                       for d in days for m, v in zip(("M1", "M2"), r2)])
    return pl.DataFrame(rows), fc


def test_h1_labels():
    eff = {("P3_M2", "vip0"): {"gross_bp_per_notional": -1.4}, ("P3_negM2", "vip0"): {"gross_bp_per_notional": -1.5}}
    res = A.analyse(*synthetic_tables(eff), CFG, RC)
    assert res["H1"]["skill_holds"] and res["H1"]["H1-T"]["label"] == "supported"        # D ~ 0.1 < 0.5
    eff[("P3_negM2", "vip0")] = {"gross_bp_per_notional": -2.5}
    assert A.analyse(*synthetic_tables(eff), CFG, RC)["H1"]["H1-T"]["label"] == "refuted"  # D ~ 1.1 > 0.5
    eff[("P3_negM2", "vip0")] = {"gross_bp_per_notional": -1.9}
    assert A.analyse(*synthetic_tables(eff), CFG, RC)["H1"]["H1-T"]["label"] == "inconclusive"  # D ~ 0.5
    res = A.analyse(*synthetic_tables(eff, r2=(0.0, -0.01)), CFG, RC)
    assert not res["H1"]["skill_holds"] and res["H1"]["H1-T"]["label"].startswith("not testable")
    eff = {("P3_M2", "vip0"): {"gross_bp_per_notional": -1.5, "gate_active_share": 0.01},
           ("P3_negM2", "vip0"): {"gross_bp_per_notional": -1.5, "gate_active_share": 0.01}}
    assert A.analyse(*synthetic_tables(eff), CFG, RC)["H1"]["H1-T"]["label"] == "not testable: rule inactive"


def test_h3_labels_and_participation():
    eff = {("P4", "lp_tier4"): {"inc_es": 6.0, "max_drawdown": 30.0, "net_per_hour": -99.0, "turnover_per_hour": 8e4},
           ("P3F", "lp_tier4"): {"inc_es": 10.0, "max_drawdown": 50.0, "net_per_hour": -100.0}}
    res = A.analyse(*synthetic_tables(eff), CFG, RC)
    assert res["H3"]["label"] == "supported" and not res["H3"]["partly_mechanical"]
    eff[("P4", "lp_tier4")]["net_per_hour"] = -130.0                     # beyond the 10% margin
    assert A.analyse(*synthetic_tables(eff), CFG, RC)["H3"]["label"] == "refuted"
    eff[("P4", "lp_tier4")].update(net_per_hour=-99.0, turnover_per_hour=3e4)
    assert A.analyse(*synthetic_tables(eff), CFG, RC)["H3"]["partly_mechanical"]
    part = res["participation"]
    assert part["abstention_rational"] and part["bonferroni_level"] == pytest.approx(99.29)
    eff = {("P1", "vip0"): {"net_per_hour": 50.0}}
    part = A.analyse(*synthetic_tables(eff), CFG, RC)["participation"]
    assert part["policies"]["P1"]["preferred_to_no_trade"] and not part["abstention_rational"]


def test_runner_refuses_test_sessions(tmp_path, monkeypatch):
    text = Path(e003.CONFIG).read_text().replace('session_sets = ["train", "validation"]',
                                                 'session_sets = ["train", "validation", "test"]')
    (tmp_path / "e003.toml").write_text(text)
    monkeypatch.setattr(e003, "CONFIG", tmp_path / "e003.toml")
    with pytest.raises(PermissionError):
        e003.run()


def test_flow_is_exact_and_bounded_over_many_trades():
    rng = np.random.default_rng(5)
    n, m = 2_000, 200_000
    te = np.arange(1, n + 1) * 1_000_000
    px = np.column_stack([np.full(n, 100.0 - 0.01 * k) for k in range(10)])
    ap = np.column_stack([np.full(n, 100.01 + 0.01 * k) for k in range(10)])
    q = np.ones((n, 10))
    tt = np.sort(rng.integers(1, te[-1], m))
    tq = np.round(rng.lognormal(0, 2, m), 3) + 0.001
    ta = rng.choice([-1.0, 1.0], m)
    f = F.episode_features(te, te + 1, px, q, ap, q, tt, tt.astype(float), tq, ta, 0.01, 0, int(te[-1]), 0, [1])
    assert np.abs(f["flow_1s"]).max() <= 1.0 and np.abs(f["flow_10s"]).max() <= 1.0
    k = n - 7                                   # equals a direct recomputation at a late state
    sel = (tt > te[k] - 1_000_000) & (tt <= te[k])
    assert f["flow_1s"][k] == pytest.approx(np.sum(tq[sel] * ta[sel]) / np.sum(tq[sel]), abs=1e-12)


def test_runner_refuses_a_non_empty_output_directory(tmp_path, monkeypatch):
    from lpx import provenance as P
    (tmp_path / "out").mkdir()
    (tmp_path / "out" / "e003_net_by_session.csv").write_text("partial")
    monkeypatch.setattr(e003, "OUT", tmp_path / "out")
    monkeypatch.setattr(P, "require_clean", lambda: None)
    monkeypatch.setattr(e003, "SPEC", Path(e003.CONFIG))   # committed file: passes the spec check
    with pytest.raises(FileExistsError):
        e003.run()


def test_receipt_inputs_match_the_acceptance_record():
    d = CFG["scope"]["development_session"]
    if not (Path(e003.ROOT) / "data" / "normalized" / "tardis").exists():
        pytest.skip("market data not present")
    assert len(e003.verify_receipt_inputs(CFG, [d])[d]) == 64


def test_ofi_includes_the_transition_into_the_first_window_state():
    te = np.array([0, 500_000, 1_200_000, 1_700_000])
    px = np.column_stack([np.full(4, 100.0 - 0.01 * k) for k in range(10)])
    ap = np.column_stack([np.full(4, 100.01 + 0.01 * k) for k in range(10)])
    bq = np.ones((4, 10))
    bq[2:, 0] = 5.0                                  # bid size 1 -> 5 at 1.2 s
    f = F.episode_features(te, te, px, bq, ap, np.ones((4, 10)), np.array([], np.int64), np.array([]), np.array([]),
                           np.array([]), 0.01, 0, 1_700_000, 0, [1])
    # at 1.7 s the 1 s window (0.7 s, 1.7 s] holds the +4 change into the state at 1.2 s
    assert f["ofi_1s"][3] == pytest.approx(4.0 / np.mean([3.0, 3.0]))


def test_non_monotone_receipt_times_are_refused():
    with pytest.raises(ValueError):
        F.admission_index(np.array([1, 2]), np.array([5, 4]), np.array([1]), np.array([1.0]))
