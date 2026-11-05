"""E002 runner and pre-registered analysis on synthetic inputs (no market data)."""

import tomllib
from pathlib import Path

import numpy as np
import polars as pl
import pytest

from lpx.execution import sim as X
from lpx.research import e002, e002_analysis as A

CFG = tomllib.loads((Path(__file__).resolve().parents[1] / "configs" / "e002_v1.toml").read_text())


def test_episodes_respect_minimum_length():
    w = pl.DataFrame({"start_us": [0, 10_000_000_000], "end_us": [599_000_000, 10_700_000_000]})
    assert e002.episodes(w, 600) == [(10_000_000_000, 10_700_000_000)]


def test_run_session_and_fee_overlay_on_a_synthetic_market():
    rng = np.random.default_rng(0)
    states, t, mid = [], 1_000_000, 10_000
    for _ in range(3_000):
        t += int(rng.integers(50_000, 150_000))
        mid += int(rng.choice([-1, 0, 0, 0, 1]))
        states.append(X.State(t, t + 2_000, tuple((mid - k, 10.0) for k in range(10)), tuple((mid + 1 + k, 10.0) for k in range(10))))
    ts = np.array([s.t_exch for s in states])
    trades = []
    for tt in np.sort(rng.integers(ts[0] + 1, ts[-1], size=4_000)):
        s = states[np.searchsorted(ts, tt) - 1]
        a = int(rng.choice([-1, 1]))
        trades.append(X.Trade(int(tt), s.asks[0][0] if a > 0 else s.bids[0][0], float(rng.uniform(0.5, 6.0)), a))
    eps = [(int(ts[0]), int(ts[1500])), (int(ts[1600]), int(ts[-1]))]
    rows = e002.run_session(states, trades, eps, CFG)
    df = pl.DataFrame(rows)
    nt = df.filter(pl.col("policy") == "no_trade")
    assert nt.height == 1 and nt["fills"][0] == 0 and nt["gross_marked"][0] == 0.0
    p0 = df.filter(pl.col("policy") == "P0")
    assert p0.height == 4 * 3 and (p0["episodes"] == 2).all()
    # optimism ordering of fills on identical paths: conservative <= intermediate <= optimistic <= naive
    for lat in CFG["latency"]:
        f = {r["fill_model"]: r["fills"] for r in p0.filter(pl.col("latency") == lat).iter_rows(named=True)}
        vol = {r["fill_model"]: r["filled_notional"] for r in p0.filter(pl.col("latency") == lat).iter_rows(named=True)}
        assert vol["conservative"] <= vol["intermediate"] + 1e-9 <= vol["optimistic"] + 2e-9 and f["naive"] >= f["conservative"]
    net = e002.fee_overlay(df, CFG["fees"])
    assert set(net["fee_schedule"].unique()) == {"vip0", "vip0_bnb", "vip9", "lp_tier1", "lp_tier4"}
    r = net.filter((pl.col("policy") == "P0") & (pl.col("fill_model") == "intermediate") & (pl.col("latency") == "tokyo"))
    v = {x["fee_schedule"]: x for x in r.iter_rows(named=True)}
    assert v["vip0"]["maker_fees"] == pytest.approx(0.001 * v["vip0"]["filled_notional"])
    assert v["lp_tier4"]["net"] > v["vip0"]["net"]  # rebate schedule strictly better on identical fills
    assert v["vip0"]["net"] == pytest.approx(v["vip0"]["gross_marked"] - v["vip0"]["liquidation_slippage"]
                                             - v["vip0"]["maker_fees"] - v["vip0"]["taker_fees"])
    # session drawdown follows each fee path: never smaller under higher fees on identical fills
    assert v["vip0"]["max_drawdown"] >= v["lp_tier4"]["max_drawdown"] - 1e-12
    assert not any(c.startswith("max_drawdown__") for c in net.columns)
    # crossing fills only in the optimistic models; fill reasons add up; orders carried across episodes
    cons = p0.filter(pl.col("fill_model").is_in(["conservative", "intermediate"]))
    assert (cons["fills_crossing"] == 0).all()
    assert (p0["fills_at_price"] + p0["fills_through"] + p0["fills_crossing"] == p0["fills"]).all()
    assert (p0["own_markout_30s_fills"] <= p0["fills"]).all()
    assert ((p0["fill_rate"] >= 0) & (p0["fill_rate"] <= 1 + 1e-9)).all()


def test_own_fill_markouts_exclude_horizons_beyond_the_episode():
    states_t = np.array([0, 1_000_000, 2_000_000, 10_000_000, 11_000_000])
    mid = np.array([1.00, 1.01, 1.02, 2.00, 2.00])
    fills = [X.Fill(500_000, 1, X.BID, 100, 1.0, 0.0, 100.5, "at_price"),      # ep 1, +1 s inside; +30 s outside
             X.Fill(1_900_000, 2, X.ASK, 101, 1.0, 0.0, 100.5, "at_price")]    # ep 1, +1 s outside (ends at 2.0 s)
    out = e002.own_fill_markouts(fills, [(0, 2_000_000), (10_000_000, 11_000_000)], states_t, mid, [1, 30], 0.01)
    assert out["own_markout_1s_fills"] == 1 and out["own_markout_1s_bp"] == pytest.approx((1.01 - 1.00) / 1.00 * 1e4)
    assert out["own_markout_30s_fills"] == 0 and out["own_markout_30s_bp"] is None
    assert out["own_edge_bp"] == pytest.approx(((1.005 - 1.00) + (1.01 - 1.005)) / 2.01 * 1e4)


def synthetic_net(effects: dict) -> pl.DataFrame:
    """effects[(policy, model, latency)] = session-mean outcome; 15 sessions (as in discovery) with small noise."""
    rng = np.random.default_rng(1)
    rows = []
    for (pol, model, lat), mu in effects.items():
        for i in range(15):
            rows.append({"day": f"d{i}", "policy": pol, "fill_model": model, "latency": lat, "fee_schedule": "vip0",
                         "net_bp_per_notional": mu + rng.normal(0, 0.1)})
    return pl.DataFrame(rows)


def test_h2_rule_detects_sign_reversal_and_materiality():
    eff = {}
    for model, mu in (("conservative", -3.0), ("intermediate", -0.5), ("optimistic", 2.0)):
        for lat in ("tokyo", "regional", "distant"):
            eff[("P0", model, lat)] = mu
            eff[("P1", model, lat)] = mu + 0.2
    res = A.h2(synthetic_net(eff), CFG)
    assert res["condition_a_sign_reversal"]["P0"] and res["h2_supported_on_discovery"]
    assert res["material_sensitivity"]
    assert not res["condition_b_ranking_reversal"]  # P1 better than P0 everywhere: no ranking reversal


def test_h2_rule_not_supported_when_outcomes_are_stable():
    eff = {(pol, m, lat): -2.0 + (0.1 if pol == "P1" else 0.0) for pol in ("P0", "P1")
           for m in ("conservative", "intermediate", "optimistic") for lat in ("tokyo", "regional", "distant")}
    res = A.h2(synthetic_net(eff), CFG)
    assert not res["h2_supported_on_discovery"] and not res["material_sensitivity"]


def test_scenarios_without_enough_defined_sessions_do_not_enter_the_decision():
    eff = {(pol, m, lat): -2.0 for pol in ("P0", "P1") for m in ("conservative", "intermediate", "optimistic")
           for lat in ("tokyo", "regional", "distant")}
    eff[("P0", "optimistic", "tokyo")] = 3.0
    net = synthetic_net(eff)
    # the only positive scenario has fills in just 3 of 15 sessions: its outcome is undefined elsewhere
    sparse = (pl.col("policy") == "P0") & (pl.col("fill_model") == "optimistic") & (pl.col("latency") == "tokyo")
    net = net.with_columns(pl.when(sparse & ~pl.col("day").is_in(["d0", "d1", "d2"])).then(None)
                           .otherwise(pl.col("net_bp_per_notional")).alias("net_bp_per_notional"))
    res = A.h2(net, CFG)  # pre-registered: >= 12 of 15 sessions defined
    row = [r for r in res["scenario_table"] if r["policy"] == "P0" and r["fill_model"] == "optimistic" and r["latency"] == "tokyo"][0]
    assert row["sessions_defined"] == 3 and not row["eligible"]
    assert not res["h2_supported_on_discovery"]


# ---------------------------------------------------------------- E002 re-review test gaps (runner plumbing, guards)

def test_to_states_drops_missing_levels_and_rounds_to_ticks():
    row = {"t_exch_us": [100], "t_local_us": [103]}
    for i in range(1, 11):
        row[f"bid{i}_px"] = [150.0 - 0.01 * i + 1e-9 if i <= 3 else float("nan")]
        row[f"bid{i}_qty"] = [float(i)]
        row[f"ask{i}_px"] = [150.0 + 0.01 * (i - 1) - 1e-9]
        row[f"ask{i}_qty"] = [2.0 * i]
    s = e002.to_states(pl.DataFrame(row), 0.01)[0]
    assert (s.t_exch, s.t_recv) == (100, 103)
    assert s.bids == ((14999, 1.0), (14998, 2.0), (14997, 3.0)) and len(s.asks) == 10 and s.asks[0] == (15000, 2.0)


def test_to_trades_maps_price_size_and_aggressor():
    df = pl.DataFrame({"exch_us": [5, 7], "price": [150.01 - 1e-9, 149.99], "qty": [0.5, 2.0], "aggressor": [1, -1]})
    assert e002.to_trades(df, 0.01) == [X.Trade(5, 15001, 0.5, 1), X.Trade(7, 14999, 2.0, -1)]


def test_independent_order_limit_check():
    e002.check_order_limits([0, 5_000_000, 9_999_999], per_10s=3, per_day=3)
    with pytest.raises(AssertionError):
        e002.check_order_limits([0, 5_000_000, 9_999_999], per_10s=2, per_day=10)
    e002.check_order_limits([0, 10_000_000, 20_000_000], per_10s=1, per_day=10)  # windows are (t - 10 s, t]
    with pytest.raises(AssertionError):
        e002.check_order_limits(list(range(4)), per_10s=10, per_day=3)


def test_net_per_hour_undefined_without_valid_time():
    rows = pl.DataFrame({"gross_marked": [0.0], "liquidation_slippage": [0.0], "filled_notional": [0.0],
                         "liquidation_notional": [0.0], "valid_hours": [0.0],
                         **{f"max_drawdown__{k}": [0.0] for k in CFG["fees"] if k != "default"}})
    net = e002.fee_overlay(rows, CFG["fees"])
    assert net["net_per_hour"].is_null().all() and net["net_bp_per_notional"].is_null().all()


def test_runner_refuses_test_sessions(tmp_path, monkeypatch):
    text = (Path(e002.CONFIG)).read_text().replace('session_sets = ["train", "validation"]',
                                                   'session_sets = ["train", "validation", "test"]')
    (tmp_path / "e002.toml").write_text(text)
    monkeypatch.setattr(e002, "CONFIG", tmp_path / "e002.toml")
    with pytest.raises(PermissionError):
        e002.run()


def _fake_run(tmp_path, monkeypatch, **meta_over):
    """A results directory that passes every analysis guard, then one field broken by ``meta_over``."""
    import json
    from lpx import provenance as P
    out = tmp_path / "e002"
    out.mkdir()
    rc = tomllib.loads((Path(e002.CONFIG).parents[0] / "research_v1.toml").read_text())
    days = rc["splits"]["train"] + rc["splits"]["validation"]
    pl.DataFrame({"day": days}).write_csv(out / "e002_net_by_session.csv")
    root = Path(e002.CONFIG).parents[1]
    pv = {"git_dirty": False, "git_commit": "x", "code_fingerprint": P.code_fingerprint(),
          "configs": {"configs/e002_v1.toml": P.sha256_file(e002.CONFIG),
                      "configs/research_v1.toml": P.sha256_file(root / "configs" / "research_v1.toml")},
          "spec_sha256": P.sha256_file(root / "docs" / "experiments" / "E002.md")}
    meta = {"sessions": days, "provenance": pv,
            "outputs_sha256": {"e002_net_by_session.csv": P.sha256_file(out / "e002_net_by_session.csv")}}
    for k, v in meta_over.items():
        (pv if k in pv else meta)[k] = v
    (out / "e002_meta.json").write_text(json.dumps(meta))
    monkeypatch.setattr(e002, "OUT", out)
    monkeypatch.setattr(P, "require_clean", lambda: None)
    monkeypatch.setattr(A, "h2", lambda net, cfg: {"ok": True})


@pytest.mark.parametrize("override,error", [
    ({"git_dirty": True}, RuntimeError),
    ({"sessions": ["2026-06-01"]}, PermissionError),
    ({"code_fingerprint": "0" * 16}, RuntimeError),
    ({"spec_sha256": "0" * 64}, RuntimeError),
    ({"outputs_sha256": {"e002_net_by_session.csv": "0" * 64}}, RuntimeError),
])
def test_analysis_refuses_runs_it_cannot_cite(tmp_path, monkeypatch, override, error):
    _fake_run(tmp_path, monkeypatch, **override)
    with pytest.raises(error):
        A.run()


def test_analysis_accepts_a_consistent_run(tmp_path, monkeypatch):
    _fake_run(tmp_path, monkeypatch)
    assert A.run()["ok"]
