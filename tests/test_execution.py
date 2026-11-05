"""Toy-case acceptance tests for the counterfactual execution engine (Gate C). Synthetic markets only."""

import math

import numpy as np

import pytest

from lpx.execution import sim as X
from lpx.execution.sim import ASK, BID, Quote, State, Trade


def cfg(model="conservative", entry=10, ack=10, md=0, maker=0.0, taker=0.0, limit=50, min_notional=0.0, per_day=200_000):
    return X.ExecConfig(fill_model=model, md_delay_us=md, entry_latency_us=entry, ack_latency_us=ack, maker_fee=maker,
                        taker_fee=taker, tick=0.01, lot=0.001, min_notional=min_notional, max_orders_per_10s=limit,
                        max_orders_per_day=per_day)


def st(t, bids, asks, recv=None):
    return State(t, t if recv is None else recv, tuple(bids), tuple(asks))


def scripted(quotes):
    """Always want the same quotes (keeps a matching working order, so queue position is retained)."""
    return lambda v: dict(quotes)


def run(model, states, trades, policy=None, t_end=1000, **kw):
    pol = policy or scripted({BID: Quote(100, 1.0)})
    return X.Simulator(cfg(model, **kw), pol, states, trades, t_start=0, t_end=t_end).run()


BOOK = [st(0, [(100, 5.0), (99, 5.0)], [(101, 5.0), (102, 5.0)])]


def test_queue_consumed_by_trades_then_partial_fills():
    r = run("conservative", BOOK, [Trade(20, 100, 3.0, -1), Trade(30, 100, 2.5, -1), Trade(40, 100, 1.0, -1)])
    assert [f.qty for f in r.fills] == pytest.approx([0.5, 0.5]) and r.inventory == pytest.approx(1.0)


@pytest.mark.parametrize("model,fill", [("conservative", 0.0), ("intermediate", 0.25), ("optimistic", 1.0), ("naive", 1.0)])
def test_cancellation_attribution_by_model(model, fill):
    states = BOOK + [st(50, [(100, 8.0), (99, 5.0)], [(101, 5.0), (102, 5.0)]),   # +3 joins behind us
                     st(60, [(100, 6.0), (99, 5.0)], [(101, 5.0), (102, 5.0)])]   # -2 net cancellations
    # ahead after t=60: conservative 5, intermediate 5 - 2*5/8 = 3.75, optimistic 3 ; then a 4-lot sell at our price
    r = run(model, states, [Trade(70, 100, 4.0, -1)])
    assert sum(f.qty for f in r.fills) == pytest.approx(fill)


def test_queue_never_exceeds_visible_level():
    states = BOOK + [st(50, [(100, 2.0), (99, 5.0)], [(101, 5.0), (102, 5.0)])]  # level shrank below our queue estimate
    r = run("conservative", states, [Trade(60, 100, 2.5, -1)])
    assert sum(f.qty for f in r.fills) == pytest.approx(0.5)


def test_trade_through_fills_up_to_trade_size():
    r = run("conservative", BOOK, [Trade(20, 99, 0.4, -1)])
    assert [f.qty for f in r.fills] == pytest.approx([0.4]) and r.fills[0].px == 100


def test_order_not_fillable_before_arrival_or_by_own_side_trades():
    r = run("naive", BOOK, [Trade(5, 100, 9.0, -1), Trade(20, 100, 9.0, 1)])  # arrival at t=10; buyer trades do not hit bids
    assert r.fills == []


def test_cancel_takes_effect_after_latency():
    calls = []

    def policy(v):
        calls.append(v.t)
        return {BID: Quote(100, 1.0)} if v.t < 25 else {}

    states = BOOK + [st(25, [(100, 5.0), (99, 5.0)], [(101, 5.0), (102, 5.0)])]
    r = run("naive", states, [Trade(30, 100, 0.3, -1), Trade(36, 100, 0.3, -1)], policy=policy)
    assert [f.t for f in r.fills] == [30]  # cancel sent at 25 is effective at 35


def test_post_only_rejection_when_book_moves_before_arrival():
    states = BOOK + [st(5, [(99, 5.0), (98, 5.0)], [(100, 5.0), (101, 5.0)], recv=10_000)]  # ask moved onto our price
    r = run("naive", states, [Trade(20, 100, 1.0, -1)], policy=scripted({BID: Quote(100, 1.0)}))
    assert r.orders_rejected == 1 and r.fills == []


def test_inventory_limit_in_p0():
    states = BOOK + [st(100 + 10 * i, [(100, 5.0), (99, 5.0)], [(101, 5.0), (102, 5.0)]) for i in range(5)]
    trades = [Trade(20, 100, 1.0, -1), Trade(150, 100, 1.0, -1)]
    r = run("naive", states, trades, policy=X.p0_fixed(1.0, 1.0))
    assert r.inventory == pytest.approx(1.0)  # second sell finds no bid: limit reached after the first fill


def test_decisions_use_only_received_states():
    seen = []

    def policy(v):
        seen.append((v.t, v.state.t_exch))
        return {}

    states = [st(0, [(100, 5.0)], [(101, 5.0)], recv=3), st(100, [(100, 5.0)], [(101, 5.0)], recv=180)]
    X.Simulator(cfg(md=20), policy, states, [], t_start=0, t_end=1000).run()
    assert seen == [(23, 0), (200, 100)]


def test_unknown_queue_is_infinitely_far_back():
    deep = [st(0, [(105, 5.0)], [(106, 5.0)])]  # our bid at 100 lies beyond the visible depth
    r = run("conservative", deep, [Trade(20, 100, 50.0, -1)])
    assert r.fills == []
    r = run("conservative", deep, [Trade(20, 99, 0.2, -1)])  # but a trade through our price still fills
    assert [f.qty for f in r.fills] == pytest.approx([0.2])


def test_rate_limit_and_lot_and_notional():
    flip = {"n": 0}

    def churn(v):
        flip["n"] += 1
        return {BID: Quote(100 if flip["n"] % 2 else 99, 1.0)}

    states = [st(i * 10, [(100, 5.0), (99, 5.0)], [(101, 5.0)]) for i in range(100)]
    r = X.Simulator(cfg(limit=5), churn, states, [], t_start=0, t_end=10_000).run()
    assert r.orders_sent == 5 and r.rate_limited > 0
    r = X.Simulator(cfg(min_notional=5.0), scripted({BID: Quote(100, 4.0)}), BOOK, [], t_start=0, t_end=100).run()
    assert r.orders_sent == 0  # 4 * 1.00 < 5 quote currency
    r = X.Simulator(cfg(), scripted({BID: Quote(100, 1.2345)}), BOOK, [Trade(20, 99, 9.0, -1)], t_start=0, t_end=100).run()
    assert r.fills[0].qty == pytest.approx(1.234)  # rounded down to the 0.001 lot


def test_accounting_identity_fees_and_liquidation():
    states = [st(0, [(100, 5.0), (99, 2.0), (98, 50.0)], [(101, 5.0), (102, 5.0)]),
              st(100, [(101, 5.0), (100, 1.0), (99, 2.0)], [(102, 5.0), (103, 5.0)]),
              st(200, [(99, 1.0), (98, 1.0), (97, 0.5)], [(101, 5.0), (102, 5.0)])]
    trades = [Trade(20, 100, 3.0, -1), Trade(150, 102, 0.5, 1), Trade(160, 101, 3.0, -1)]
    pol = scripted({BID: Quote(100, 3.0), ASK: Quote(102, 0.5)})
    r = X.Simulator(cfg("naive", maker=-0.0001, taker=0.001), pol, states, trades, t_start=0, t_end=300).run()
    assert r.fees < 0  # maker rebate credited
    assert r.marked_final == pytest.approx(r.edge + r.inventory_pnl - r.fees, abs=1e-9)
    mid = (99 + 101) / 2 * 0.01
    assert r.marked_final == pytest.approx(r.cash + r.inventory * mid, abs=1e-12)
    # liquidation walks the visible bids 0.99 x1, 0.98 x1, 0.97 x0.5 for a 2.5 long position
    assert r.inventory == pytest.approx(2.5)
    proceeds = 0.99 + 0.98 + 0.97 * 0.5
    assert r.liquidation_cost == pytest.approx((mid - proceeds / 2.5) * 2.5 + 0.001 * proceeds, abs=1e-12)
    assert r.liquidation_shortfall == pytest.approx(0.0)


def test_no_trade_baseline_is_flat():
    r = run("optimistic", BOOK, [Trade(20, 100, 9.0, -1)], policy=X.no_trade)
    assert r.fills == [] and r.marked_final == 0.0 and math.isclose(r.inventory, 0.0)


@pytest.mark.parametrize("model,fill", [("conservative", 0.0), ("intermediate", 0.0), ("optimistic", 0.6), ("naive", 0.6)])
def test_crossing_fills_only_in_optimistic_models(model, fill):
    # the book drops through our resting bid at 100: asks now at 100 (0.6) - an optimistic model fills us there
    states = BOOK + [st(50, [(99, 5.0), (98, 5.0)], [(100, 0.6), (101, 5.0)])]
    r = run(model, states, [])
    assert sum(f.qty for f in r.fills) == pytest.approx(fill)
    if fill:
        assert r.fills[0].mid_ticks == pytest.approx(100.5)  # measured against the mid before the crossing state
        assert r.marked_final == pytest.approx(r.edge + r.inventory_pnl - r.fees, abs=1e-12)


def test_daily_order_limit_counts_across_episodes():
    churn = lambda v: {BID: Quote(100 if v.t % 20 else 99, 1.0)}
    states = [st(i * 10, [(100, 5.0), (99, 5.0)], [(101, 5.0)]) for i in range(50)]
    carry = X.Carry(orders_sent_today=7)
    r = X.Simulator(cfg(per_day=10, limit=1000), churn, states, [], t_start=0, t_end=10_000, carry=carry).run()
    assert r.orders_sent == 3 and r.rate_limited > 0 and carry.orders_sent_today == 10


def test_max_drawdown_of_marked_wealth():
    states = [st(0, [(100, 5.0)], [(101, 5.0)]), st(100, [(90, 5.0)], [(91, 5.0)]), st(200, [(95, 5.0)], [(96, 5.0)])]
    carry = X.Carry()
    r = X.Simulator(cfg("conservative"), scripted({BID: Quote(100, 1.0)}), states, [Trade(20, 99, 1.0, -1)],
                    t_start=0, t_end=300, carry=carry).run()
    # bought 1 at 1.00 by a trade-through; wealth sampled at states: 0 (peak) -> -1.00 + 0.905 -> -1.00 + 0.955, then
    # liquidated at 0.95 (end point -0.05)
    assert r.inventory == pytest.approx(1.0) and carry.max_drawdown[0] == pytest.approx(0.095, abs=1e-12)
    assert carry.offset[0] == pytest.approx(-0.05, abs=1e-12)


def test_drawdown_per_fee_path_carried_across_episodes_with_liquidation_point():
    ep1 = [st(0, [(100, 5.0)], [(101, 5.0)]), st(100, [(100, 5.0)], [(101, 5.0)])]
    ep2 = [st(1000, [(100, 5.0)], [(101, 5.0)]), st(1100, [(100, 0.5), (90, 5.0)], [(101, 5.0)])]
    carry = X.Carry(fee_paths=((0.0, 0.0), (0.001, 0.002)))
    pol = scripted({BID: Quote(100, 1.0)})
    X.Simulator(cfg("conservative"), pol, ep1, [Trade(20, 99, 1.0, -1)], t_start=0, t_end=200, carry=carry).run()
    # episode 1: bought 1 at 1.00 (mid 1.005), liquidated at 1.00 -> fee-free 0; fee path: -0.001 maker - 0.002 taker
    assert carry.offset == pytest.approx([0.0, -0.003], abs=1e-12)
    X.Simulator(cfg("conservative"), pol, ep2, [Trade(1020, 99, 1.0, -1)], t_start=1000, t_end=1200, carry=carry).run()
    # episode 2 starts from the carried offset; marked wealth at the last state = -1.00 + 0.955; liquidation walks
    # 0.5 at 1.00 and 0.5 at 0.90 -> final -0.05; the drawdown includes the liquidation-adjusted end point
    assert carry.offset[0] == pytest.approx(-0.05, abs=1e-12)
    assert carry.max_drawdown[0] == pytest.approx(0.05 + 0.005, abs=1e-12)  # peak 0.005 (mid gain at the first fill state)
    assert carry.max_drawdown[1] > carry.max_drawdown[0]


def test_executions_before_arrival_are_not_credited_twice():
    # 2 lots trade at our price before our order arrives (t=10): ahead = 5 - 2 = 3. The next state shows the level at 3,
    # which is fully explained by those executions: no cancellation credit even in the optimistic model.
    states = BOOK + [st(50, [(100, 3.0), (99, 5.0)], [(101, 5.0), (102, 5.0)])]
    r = run("optimistic", states, [Trade(5, 100, 2.0, -1), Trade(60, 100, 3.5, -1)])
    assert sum(f.qty for f in r.fills) == pytest.approx(0.5)


def test_participant_sees_fills_only_after_acknowledgement():
    seen = []

    def policy(v):
        seen.append((v.t, v.inventory, {w.oid: w.known_remaining for w in v.working.values()}))
        return {BID: Quote(100, 1.0)}

    states = [st(0, [(100, 5.0)], [(101, 5.0)]), st(50, [(100, 5.0)], [(101, 5.0)]), st(150, [(100, 5.0)], [(101, 5.0)])]
    r = X.Simulator(cfg("conservative", ack=100), policy, states, [Trade(20, 99, 0.4, -1)], t_start=0, t_end=300).run()
    assert r.fills[0].t == 20 and r.orders_sent == 1  # partial fill: same price wanted -> order kept, no top-up
    by_t = {t: (inv, w) for t, inv, w in seen}
    assert by_t[50] == (0.0, {1: 1.0})                    # fill at 20 not yet acknowledged (ack at 120)
    assert by_t[120][0] == pytest.approx(0.4) and by_t[120][1][1] == pytest.approx(0.6)


def test_no_decisions_after_episode_end_and_inventory_time_bounded():
    calls = []

    def policy(v):
        calls.append(v.t)
        return {BID: Quote(100, 1.0)}

    states = [st(0, [(100, 5.0)], [(101, 5.0)]), st(280, [(100, 5.0)], [(101, 5.0)], recv=320)]
    r = X.Simulator(cfg("conservative", ack=100), policy, states, [Trade(250, 99, 1.0, -1)], t_start=0, t_end=300).run()
    assert max(calls) <= 300  # the state received at 320 and the ack at 350 come after the episode end
    assert r.time_weighted_abs_inventory == pytest.approx(50 / 1e6)
    # without any event after the last fill, inventory still accrues up to the episode end (and not beyond)
    r = X.Simulator(cfg("conservative", ack=10), policy, states[:1], [Trade(250, 99, 1.0, -1)], t_start=0, t_end=300).run()
    assert r.time_weighted_abs_inventory == pytest.approx(50 / 1e6)


@pytest.mark.parametrize("model", ["optimistic", "naive"])
def test_crossing_fills_once_per_crossing(model):
    cross = st(50, [(99, 5.0)], [(100, 0.3), (101, 5.0)])
    states = BOOK + [cross, st(60, [(99, 5.0)], [(100, 0.3), (101, 5.0)]),     # still crossed: no second fill
                     st(70, [(100, 5.0)], [(101, 5.0)]),                        # uncrossed
                     st(80, [(99, 5.0)], [(100, 0.3), (101, 5.0)])]             # crossed again: fills again
    r = run(model, states, [])
    assert [f.reason for f in r.fills] == ["crossing", "crossing"] and [f.t for f in r.fills] == [50, 80]


def test_liquidation_beyond_visible_book_valued_at_deepest_price_and_flagged():
    states = [st(0, [(100, 5.0)], [(101, 5.0)]), st(100, [(99, 1.0), (98, 1.0)], [(101, 5.0)])]
    r = X.Simulator(cfg("conservative", taker=0.001), scripted({BID: Quote(100, 3.0)}), states,
                    [Trade(20, 99, 3.0, -1)], t_start=0, t_end=200).run()
    proceeds = 0.99 + 0.98 + 1.0 * 0.98
    assert r.liquidation_shortfall == pytest.approx(1.0) and r.liquidation_proceeds == pytest.approx(proceeds)
    assert r.liquidation_cost == pytest.approx(1.0 * 3 - proceeds + 0.001 * proceeds)


def test_p1_withdraws_at_threshold_despite_float_sums():
    inv = sum([0.1] * 30)  # 2.9999999999999996
    book = st(0, [(100, 5.0)], [(101, 5.0)])
    pol = X.p1_inventory_withdrawal(1.0, 10.0, 3.0)
    assert set(pol(X.View(0, book, inv, {}))) == {ASK}
    assert set(pol(X.View(0, book, -inv, {}))) == {BID}
    assert set(pol(X.View(0, book, 2.9, {}))) == {BID, ASK}


def test_fills_are_lot_multiples_without_float_residue():
    # queue ahead 0.7 - 0.4 = 0.29999999999999993; a 0.3 trade exhausts it: no phantom 1e-17 fill
    states = [st(0, [(100, 0.7)], [(101, 5.0)])]
    r = run("conservative", states, [Trade(20, 100, 0.4, -1), Trade(30, 100, 0.3, -1), Trade(40, 100, 0.25, -1)])
    assert [f.qty for f in r.fills] == pytest.approx([0.25])
    assert all(abs(f.qty / 0.001 - round(f.qty / 0.001)) < 1e-6 for f in r.fills)


def test_order_arriving_after_episode_end_is_not_judged_or_counted():
    states = [st(0, [(99, 5.0)], [(101, 5.0)]), st(95, [(100, 5.0)], [(101, 5.0)]),
              st(98, [(99, 5.0)], [(100, 5.0)], recv=200)]  # the ask reaches 100 just before the episode end
    touch = lambda v: {BID: Quote(v.state.bids[0][0], 1.0)}
    r = X.Simulator(cfg("conservative", entry=10), touch, states, [], t_start=0, t_end=100).run()
    # the bid at 100 decided at 95 arrives at 105 > t_end: not judged against the stale book, never on the book
    assert r.orders_sent == 2 and r.orders_rejected == 0 and r.quoted_qty == pytest.approx(1.0)


# ---------------------------------------------------------------- E002 re-review test gaps and E003 engine options

def test_ten_second_window_expires_and_carries_across_episodes():
    churn = lambda v: {BID: Quote(100 if (v.t // 10) % 2 else 99, 1.0)}
    book = lambda t: st(t, [(100, 5.0), (99, 5.0)], [(101, 5.0)])
    carry = X.Carry()
    r1 = X.Simulator(cfg(limit=3), churn, [book(i * 10) for i in range(10)], [], t_start=0, t_end=100, carry=carry).run()
    assert r1.orders_sent == 3 and r1.rate_limited > 0
    # a new episode 5 s later: the three sends are still inside the 10 s window -> still blocked
    r2 = X.Simulator(cfg(limit=3), churn, [book(5_000_000 + i * 10) for i in range(5)], [], t_start=5_000_000,
                     t_end=5_000_100, carry=carry).run()
    assert r2.orders_sent == 0
    # 10 s after the first sends the window has expired
    r3 = X.Simulator(cfg(limit=3), churn, [book(10_000_100 + i * 10) for i in range(5)], [], t_start=10_000_100,
                     t_end=10_000_200, carry=carry).run()
    assert r3.orders_sent == 3 and carry.orders_sent_today == 6


def test_post_only_rejection_reaches_the_participant_after_the_ack_latency():
    seen = []

    def policy(v):
        seen.append((v.t, sorted(w.px for w in v.working.values())))
        return {BID: Quote(100, 1.0)}

    states = BOOK + [st(5, [(99, 5.0)], [(100, 5.0)], recv=6),        # ask moves onto 100 before our bid arrives (t=10)
                     st(60, [(99, 5.0)], [(100, 5.0)], recv=60)]
    r = X.Simulator(cfg(ack=40), policy, states, [], t_start=0, t_end=1000).run()
    # rejected at arrival t=10; learned at 50. At t=6 the order is still believed working (no resend);
    # the next decision on a received state (t=60) re-sends.
    assert r.orders_rejected == 2 and r.orders_sent == 2
    assert seen[1] == (6, [100]) and seen[2] == (60, [])


@pytest.mark.parametrize("hold,sent", [(False, 4), (True, 3)])
def test_fill_notice_after_rejection_does_not_resend_on_the_stale_state(hold, sent):
    # bid at 100 is rejected (ask moved to 100); an ask order at 101 fills; its notice arrives before the next state.
    states = [st(0, [(100, 5.0)], [(101, 5.0)]), st(5, [(99, 5.0)], [(100, 5.0), (101, 5.0)], recv=1000)]
    pol = scripted({BID: Quote(100, 1.0), ASK: Quote(101, 1.0)})
    c = X.ExecConfig("conservative", 0, 10, 10, 0.0, 0.0, 0.01, 0.001, 0.0, hold_rejected_until_new_state=hold)
    r = X.Simulator(c, pol, states, [Trade(15, 102, 1.0, 1)], t_start=0, t_end=500).run()
    # sends: bid@100 and ask@101 at t=0; reject learned at 20; ask fill at 15 acknowledged at 25 -> re-decision on the
    # stale state re-sends ask@101 and, without the hold, also the just-rejected bid@100
    assert r.orders_sent == sent


def test_pacing_token_bucket_per_side_carried_across_episodes():
    flip = lambda v: {BID: Quote(100 if (v.t // 10) % 2 else 99, 1.0), ASK: Quote(101 if (v.t // 10) % 2 else 102, 1.0)}
    book = lambda t: st(t, [(100, 5.0), (99, 5.0)], [(101, 5.0), (102, 5.0)])
    c = X.ExecConfig("conservative", 0, 1, 1, 0.0, 0.0, 0.01, 0.001, 0.0, pace_rate_per_s=1.0, pace_burst=3)
    carry = X.Carry()
    r = X.Simulator(c, flip, [book(i * 10) for i in range(20)], [], t_start=0, t_end=300, carry=carry).run()
    assert r.orders_sent == 6 and r.paced > 0          # 3 tokens of burst per side, no refill within 300 us
    r = X.Simulator(c, flip, [book(1_500_000 + i * 10) for i in range(20)], [], t_start=1_500_000, t_end=1_500_300,
                    carry=carry).run()
    assert r.orders_sent == 2                          # 1.5 s later: one token refilled per side (1/s), carried
    assert carry.orders_sent_today == 8 and carry.first_cap_bind_us is None


def test_pacing_rate_keeps_exchange_limits_unreachable():
    rate, burst = 1.15, 20
    assert 2 * (rate * 86_400 + burst) < 200_000 and 2 * (burst + rate * 10) < 100
    every = lambda v: {BID: Quote(100 if (v.t // 1000) % 2 else 99, 1.0)}
    states = [st(i * 1000, [(100, 5.0), (99, 5.0)], [(101, 5.0)]) for i in range(30_000)]  # a decision every 1 ms
    c = X.ExecConfig("conservative", 0, 1, 1, 0.0, 0.0, 0.01, 0.001, 0.0, pace_rate_per_s=rate, pace_burst=burst)
    r = X.Simulator(c, every, states, [], t_start=0, t_end=30_000_000).run()
    t = np.array(r.send_times)
    in_window = np.arange(t.size) - np.searchsorted(t, t - 10_000_000, side="right") + 1
    assert r.rate_limited == 0 and in_window.max() <= burst + rate * 10 + 1
    assert r.orders_sent <= burst + rate * 30 + 1


def test_first_daily_cap_bind_time_is_recorded():
    churn = lambda v: {BID: Quote(100 if (v.t // 10) % 2 else 99, 1.0)}
    carry = X.Carry(orders_sent_today=8)
    X.Simulator(cfg(per_day=10, limit=1000), churn, [st(i * 10, [(100, 5.0), (99, 5.0)], [(101, 5.0)]) for i in range(10)],
                [], t_start=0, t_end=1000, carry=carry).run()
    assert carry.first_cap_bind_us == 20


def test_warmup_quote_presence_and_wealth_grid():
    states = [st(t, [(100, 5.0)], [(101, 5.0)]) for t in range(0, 1001, 50)]
    c = X.ExecConfig("conservative", 0, 10, 10, 0.0, 0.0, 0.01, 0.001, 0.0, warmup_us=200, grid_us=300)
    r = X.Simulator(c, scripted({BID: Quote(100, 1.0)}), states, [Trade(600, 99, 1.0, -1)], t_start=0, t_end=1000).run()
    assert r.send_times == [200, 610]          # nothing before the warm-up ends; re-sent after the fill notice
    assert r.quote_time_s["bid"] == pytest.approx((600 - 210 + 1000 - 620) / 1e6) and r.quote_time_s["both"] == 0.0
    assert [g[0] for g in r.grid] == [0, 300, 600, 900, 1000]
    assert r.grid[0][1] == 0.0 and r.grid[2][2] == pytest.approx(1.0)  # bought 1 at 1.00 by the trade-through at 600
    # end point: liquidation-adjusted fee-free wealth (sell 1 at 1.00 vs bought at 1.00 -> 0)
    assert r.grid[-1][1] == pytest.approx(0.0, abs=1e-12) and r.grid[-1][3] == pytest.approx(1.0)
