"""Counterfactual passive execution against historical L2 states and exchange trades (Stage 3 / E002).

Status label of everything produced here: **modeled historical replay** — our orders never existed; fills are inferred
under explicit assumptions and are not observations. No market impact: our orders change neither historical trades nor
the historical book.

Event timeline (one UTC axis; ties resolved conservatively in this order):
    0 exchange trade (time T)          — may fill orders that were active strictly before T
    1 depth state (exchange time E)    — updates queue estimates of resting orders
    2 order arrival / cancel effective — at decision time + entry latency
    3 participant decision             — at the state's recorder receipt time + market-data delay, or at a fill notice;
                                         never after the episode end

Participant view: a decision sees only the latest received state, inventory from acknowledged fills, and its own working
orders as last acknowledged. Exchange-side fills reach it after the acknowledgement latency, post-only rejections after
the same latency (the order counts as working until then). A working order whose price the policy still wants is kept,
partially filled or not (queue position retained; no top-up); any other working order is cancelled.

Queue position (an order joins the back of its price level; historical L2 gives level sizes, not queue positions):
    at arrival      ahead = visible level size at the latest state with E <= arrival, minus executions at that price
                    since that state;
    trade at price  executions consume ``ahead`` first; the remainder fills the order (partial fills allowed);
    trade through   a trade at a worse price for our side implies the level was exhausted: fill up to the trade size;
    depth update    net non-trade change N = L_new - L_old + executions_at_price; if N < 0 (net cancellations):
                      conservative  — no credit (cancellations assumed behind us);
                      intermediate  — credit pro rata: ahead -= |N| * ahead / (L_old - executions);
                      optimistic    — cancellations assumed ahead of us first: ahead -= |N|;
                    in every model ahead <= L_new afterwards; additions join behind us.
    naive (reference only, not plausible): any trade at our price fills us, queue ignored.
    crossing (optimistic and naive only): when a new state shows the opposite side at or through a resting order's
                    price, the order fills up to the opposite visible size there (it would have taken that liquidity);
                    once per crossing episode — the order must see an uncrossed state before it can fill this way again.

Accounting: cash in quote currency, inventory in base; fee = rate * notional (negative rate = rebate); marked wealth =
cash + inventory * mid. Identity checked at run time: marked P&L = fill edge vs mid + inventory revaluation - fees.
Drawdown: per fee path (maker, taker) in ``Carry``, of the session wealth path sampled at every depth state and at each
episode end (liquidation-adjusted), carried across the episodes of a session.

Options added for E003 (all off under E002's configuration, which therefore reproduces E002 exactly):
    pacing          per-side token bucket for new orders (cancels free), carried across episodes; a wanted order without
                    a token is not sent and is counted as ``paced``;
    warm-up         no decision during the first ``warmup_us`` of an episode;
    held rejection  a price rejected as post-only is not re-sent on the same received state (e.g. when a fill notice
                    triggers a re-decision before the next state arrives);
    wealth grid     fee-free marked wealth and filled notional every ``grid_us`` of exchange time from the episode start,
                    plus the liquidation-adjusted end, for interval P&L and tail metrics under any fee overlay.
Always recorded (no effect on behaviour): send times, the time the exchange daily cap first blocks, quote presence,
paced spells and the time a side was wanted but unquoted for lack of a pacing token.

Options added for E004 (both off by default, so E002 and E003 reproduce exactly):
    view            a list of (decision time, source index, State) that replaces the per-state decisions: the participant
                    decides on these (possibly late, missing or altered) states, while exchange events always use the true
                    states. Each view state must carry its source's exchange time and prices (sizes may differ);
    extra decisions re-decisions on the last view state at given times (like a fill notice: held rejections are kept).
                    At equal times, view decisions run before extra decisions and acknowledgements (event order).
"""

from __future__ import annotations

import heapq
import math
from dataclasses import dataclass, field

FILL_MODELS = ("conservative", "intermediate", "optimistic", "naive")
BID, ASK = 1, -1


@dataclass(frozen=True)
class ExecConfig:
    fill_model: str
    md_delay_us: int          # extra market-data delay after the recorder's receipt time
    entry_latency_us: int     # decision -> order arrival / cancel effective at the exchange
    ack_latency_us: int       # exchange fill -> participant learns of it
    maker_fee: float          # fraction of notional (negative = rebate)
    taker_fee: float
    tick: float
    lot: float
    min_notional: float
    max_orders_per_10s: int = 100
    max_orders_per_day: int = 200_000
    pace_rate_per_s: float = 0.0          # 0 = no pacing (E002)
    pace_burst: float = 0.0
    warmup_us: int = 0
    hold_rejected_until_new_state: bool = False
    grid_us: int = 0                      # 0 = no wealth grid

    def __post_init__(self):
        if self.fill_model not in FILL_MODELS:
            raise ValueError(f"unknown fill model {self.fill_model}")


@dataclass
class State:
    """A verified book state. Levels are (price_ticks, qty) best first, up to N per side."""
    t_exch: int
    t_recv: int
    bids: tuple[tuple[int, float], ...]
    asks: tuple[tuple[int, float], ...]
    aux: object = None   # decision-time information attached to the state (E003: forecast and gates); never future data

    @property
    def mid_ticks(self) -> float:
        return (self.bids[0][0] + self.asks[0][0]) / 2

    def level(self, side: int, px: int) -> float | None:
        """Visible size at px on side; 0.0 if px lies inside the visible range but is empty; None if beyond it."""
        lv = self.bids if side == BID else self.asks
        for p, q in lv:
            if p == px:
                return q
        deepest = lv[-1][0]
        inside = px >= deepest if side == BID else px <= deepest
        return 0.0 if inside else None


@dataclass(frozen=True)
class Trade:
    t: int
    px: int           # ticks
    qty: float
    aggressor: int    # +1 buyer-initiated (hits asks), -1 seller-initiated (hits bids)


@dataclass
class Order:
    oid: int
    side: int
    px: int
    qty: float
    sent: int
    arrival: int
    status: str = "in_flight"   # exchange side: in_flight -> active -> (filled | canceled) ; or rejected
    ahead: float = 0.0
    level_seen: float | None = None
    exec_at_px: float = 0.0     # executions at our price since the last depth state, already reflected in ahead
    filled: float = 0.0
    cancel_effective: int | None = None
    known_filled: float = 0.0   # participant side: fills acknowledged so far
    crossing: bool = False      # optimistic models: currently matched against a crossing opposite side

    @property
    def remaining(self) -> float:
        return self.qty - self.filled


@dataclass
class Fill:
    t: int
    oid: int
    side: int
    px: int
    qty: float
    fee: float
    mid_ticks: float  # mid of the latest state before the fill (for the edge decomposition)
    reason: str       # "at_price" | "through" | "crossing"


@dataclass
class Quote:
    px: int
    qty: float


@dataclass(frozen=True)
class WorkingOrder:
    """The participant's knowledge of one of its working orders (acknowledged fills only)."""
    oid: int
    side: int
    px: int
    known_remaining: float


@dataclass
class View:
    """What the participant knows at a decision: latest received state, acknowledged inventory, own working orders."""
    t: int
    state: State
    inventory: float
    working: dict[int, WorkingOrder]


@dataclass
class Carry:
    """State carried across the episodes of one session (one UTC day): order-rate counters and, per fee path
    (maker, taker), the session wealth path used for the drawdown (liquidation-adjusted at each episode end)."""
    fee_paths: tuple[tuple[float, float], ...] = ((0.0, 0.0),)
    orders_sent_today: int = 0
    recent_sends: list[int] = field(default_factory=list)
    offset: list[float] = field(default_factory=list)
    peak: list[float] = field(default_factory=list)
    max_drawdown: list[float] = field(default_factory=list)
    tokens: dict[int, float] = field(default_factory=dict)       # pacing: per side, refilled at pace_rate_per_s
    token_t: dict[int, int] = field(default_factory=dict)
    first_cap_bind_us: int | None = None

    def __post_init__(self):
        k = len(self.fee_paths)
        self.offset = self.offset or [0.0] * k
        self.peak = self.peak or [0.0] * k
        self.max_drawdown = self.max_drawdown or [0.0] * k

    def mark(self, k: int, w: float) -> None:
        self.peak[k] = max(self.peak[k], w)
        self.max_drawdown[k] = max(self.max_drawdown[k], self.peak[k] - w)


@dataclass
class Result:
    fills: list[Fill] = field(default_factory=list)
    cash: float = 0.0
    inventory: float = 0.0
    fees: float = 0.0
    filled_notional: float = 0.0
    edge: float = 0.0               # sum over fills of (mid - price) * signed qty, in quote currency
    inventory_pnl: float = 0.0      # sum of inventory * mid changes between states
    marked_final: float = 0.0       # cash + inventory * final mid
    liquidation_cost: float = 0.0   # walking cost vs final mid + taker fee (cfg.taker_fee)
    liquidation_slippage: float = 0.0   # walking cost vs final mid only (unliquidated remainder at the deepest visible price)
    liquidation_shortfall: float = 0.0  # inventory beyond the visible book (valued at the deepest visible price)
    liquidation_proceeds: float = 0.0   # quote notional of the liquidating market order (for fee overlays)
    filled_qty: float = 0.0
    quoted_qty: float = 0.0         # quantity of orders that reached the book (arrived, not rejected): fill-rate base
    orders_sent: int = 0
    orders_rejected: int = 0
    rate_limited: int = 0           # all blocked sends (10 s window + daily cap)
    rate_limited_daily: int = 0     # of which blocked by the daily cap
    paced: int = 0                  # refused sends for lack of a pacing token (counted at every retry)
    paced_spells: int = 0           # distinct spells: from a refused wanted order to the next send or the side unwanted
    paced_time_s: dict[str, float] = field(default_factory=lambda: {"bid": 0.0, "ask": 0.0})
    send_times: list[int] = field(default_factory=list)
    quote_time_s: dict[str, float] = field(default_factory=lambda: {"bid": 0.0, "ask": 0.0, "both": 0.0})
    grid: list[tuple[int, float, float, float]] = field(default_factory=list)  # (t, fee-free wealth, notional, liq. proceeds)
    max_abs_inventory: float = 0.0
    time_weighted_abs_inventory: float = 0.0
    duration_s: float = 0.0


class Simulator:
    """Event-driven replay of one episode (one accepted validity window)."""

    def __init__(self, cfg: ExecConfig, policy, states: list[State], trades: list[Trade], *, t_start: int, t_end: int,
                 carry: Carry | None = None, view: list[tuple[int, int, State]] | None = None,
                 extra_decision_times: list[int] | None = None):
        self.cfg, self.policy = cfg, policy
        self.states = states
        self.view_states = view
        self.extra_times = extra_decision_times or []
        self.trades = trades
        self.t_start, self.t_end = t_start, t_end
        self.carry = carry if carry is not None else Carry(fee_paths=((cfg.maker_fee, cfg.taker_fee),))
        self.orders: dict[int, Order] = {}      # exchange side: live orders
        self.view: dict[int, Order] = {}        # participant side: orders it believes working
        self.next_oid = 1
        self.res = Result()
        self.cur: State | None = None           # exchange-side current state
        self.known_inv = 0.0                    # acknowledged inventory (participant view)
        self.q: list = []
        self.seq = 0
        self.last_view_state: State | None = None
        self.exec_since_state: dict[tuple[int, int], float] = {}
        self.held: set[tuple[int, int]] = set()   # (side, px) rejected since the last received state
        self.starved = {BID: False, ASK: False}   # wanted but refused for lack of a pacing token
        self.next_grid = t_start

    # ---------------------------------------------------------------- event queue
    def push(self, t: int, prio: int, kind: str, payload) -> None:
        self.seq += 1
        heapq.heappush(self.q, (t, prio, self.seq, kind, payload))

    def run(self) -> Result:
        for s in self.states:
            if self.t_start <= s.t_exch <= self.t_end:
                self.push(s.t_exch, 1, "state", s)
                t_dec = s.t_recv + self.cfg.md_delay_us
                if self.view_states is None and t_dec <= self.t_end:
                    self.push(t_dec, 3, "decide", s)
        if self.view_states is not None:
            last = None
            for t_dec, src, vs in self.view_states:
                true = self.states[src]
                if (vs.t_exch != true.t_exch or [p for p, _ in vs.bids] != [p for p, _ in true.bids]
                        or [p for p, _ in vs.asks] != [p for p, _ in true.asks]):
                    raise AssertionError("a view state must carry its source state's exchange time and prices")
                if not self.t_start <= vs.t_exch <= self.t_end or (last is not None and t_dec < last):
                    raise AssertionError("view states must belong to the episode and be in delivery order")
                last = t_dec
                if t_dec <= self.t_end:
                    self.push(t_dec, 3, "decide", vs)
        for t_x in self.extra_times:
            if t_x <= self.t_end:
                self.push(t_x, 3, "extra", None)
        for tr in self.trades:
            if self.t_start < tr.t <= self.t_end:
                self.push(tr.t, 0, "trade", tr)
        last_t = None
        while self.q:
            t, prio, _, kind, payload = heapq.heappop(self.q)
            if self.cur is not None and last_t is not None:
                # same expression as E002 (bit-identical reproduction)
                self.res.time_weighted_abs_inventory += abs(self.res.inventory) * (min(t, self.t_end) - min(last_t, self.t_end)) / 1e6
                dt = (min(t, self.t_end) - min(last_t, self.t_end)) / 1e6
                if dt > 0:
                    self.quote_presence(dt)
            if kind == "state":
                self.on_state(payload)
            elif kind == "trade":
                self.on_trade(payload)
            elif kind == "arrive":
                self.on_arrive(payload, t)
            elif kind == "cancel":
                self.on_cancel_effective(payload)
            elif kind == "decide":
                self.held.clear()
                self.on_decide(t, payload)
            elif kind == "extra":
                self.redecide(t)
            elif kind == "ack":
                o, signed = payload
                self.known_inv += signed
                o.known_filled += abs(signed)
                if o.known_filled >= o.qty - 1e-12:
                    self.view.pop(o.oid, None)
                self.redecide(t)
            elif kind == "reject_ack":  # no immediate re-decision: the next received state carries the new book
                self.view.pop(payload.oid, None)
                if self.cfg.hold_rejected_until_new_state:
                    self.held.add((payload.side, payload.px))
            if self.cur is not None:
                last_t = t
        if last_t is not None and last_t < self.t_end:
            self.res.time_weighted_abs_inventory += abs(self.res.inventory) * (self.t_end - last_t) / 1e6
            self.quote_presence((self.t_end - last_t) / 1e6)
        self.finish()
        return self.res

    def quote_presence(self, dt: float) -> None:
        """Exchange-side participation: time with a resting (arrived, not yet filled or cancelled) order per side."""
        sides = {o.side for o in self.orders.values() if o.status == "active"}
        q = self.res.quote_time_s
        q["bid"] += dt * (BID in sides)
        q["ask"] += dt * (ASK in sides)
        q["both"] += dt * (len(sides) == 2)
        self.res.paced_time_s["bid"] += dt * self.starved[BID]
        self.res.paced_time_s["ask"] += dt * self.starved[ASK]

    def redecide(self, t: int) -> None:
        if self.last_view_state is not None and t <= self.t_end:
            self.on_decide(t, self.last_view_state)

    # ---------------------------------------------------------------- exchange side
    def wealth_points(self, mid_ticks: float) -> None:
        gross = self.res.cash + self.res.fees + self.res.inventory * mid_ticks * self.cfg.tick
        for k, (maker, _) in enumerate(self.carry.fee_paths):
            self.carry.mark(k, self.carry.offset[k] + gross - maker * self.res.filled_notional)

    def on_state(self, s: State) -> None:
        if self.cur is not None and self.cfg.fill_model in ("optimistic", "naive"):
            self.crossing_fills(s)
        if self.cur is not None:
            dm = (s.mid_ticks - self.cur.mid_ticks) * self.cfg.tick
            self.res.inventory_pnl += self.res.inventory * dm
        self.cur = s
        self.wealth_points(s.mid_ticks)
        if self.cfg.grid_us and s.t_exch >= self.next_grid:
            r = self.res
            r.grid.append((s.t_exch, r.cash + r.fees + r.inventory * s.mid_ticks * self.cfg.tick, r.filled_notional, 0.0))
            while self.next_grid <= s.t_exch:
                self.next_grid += self.cfg.grid_us
        self.exec_since_state = {}
        for o in self.orders.values():
            if o.status != "active":
                continue
            L_new = s.level(o.side, o.px)
            if L_new is None:  # level beyond the visible depth: no queue information, keep the estimate
                o.exec_at_px = 0.0
                o.level_seen = None
                continue
            if o.level_seen is None:  # level visible again (or for the first time): only the cap applies
                o.ahead = min(o.ahead, L_new)
                o.level_seen = L_new
                o.exec_at_px = 0.0
                continue
            N = L_new - o.level_seen + o.exec_at_px
            if N < 0:
                c = -N
                if self.cfg.fill_model == "intermediate":
                    base = o.level_seen - o.exec_at_px
                    o.ahead -= c * o.ahead / base if base > 0 else o.ahead
                elif self.cfg.fill_model == "optimistic":
                    o.ahead -= c
            o.ahead = min(max(o.ahead, 0.0), L_new)
            o.level_seen = L_new
            o.exec_at_px = 0.0

    def crossing_fills(self, s: State) -> None:
        """Optimistic models: a resting order whose price the opposite side has reached or crossed in the new state
        would have been taken by that liquidity; fill up to the opposite visible size at or through its price, once per
        crossing episode, at the order's price, measured against the mid in force before the new state."""
        for o in list(self.orders.values()):
            if o.status != "active" or o.remaining <= 0 or (o.cancel_effective is not None and o.cancel_effective <= s.t_exch):
                continue
            opp = s.asks if o.side == BID else s.bids
            avail = sum(q for p, q in opp if (p <= o.px if o.side == BID else p >= o.px))
            if avail > 0 and not o.crossing:
                o.crossing = True
                self.fill(o, min(avail, o.remaining), s.t_exch, "crossing")
            elif avail <= 0:
                o.crossing = False

    def on_trade(self, tr: Trade) -> None:
        hit_side = BID if tr.aggressor == -1 else ASK
        key = (hit_side, tr.px)
        self.exec_since_state[key] = self.exec_since_state.get(key, 0.0) + tr.qty
        for o in list(self.orders.values()):
            if o.status != "active" or o.remaining <= 0 or o.side != hit_side:
                continue
            if o.cancel_effective is not None and tr.t >= o.cancel_effective:
                continue
            through = (tr.px < o.px) if o.side == BID else (tr.px > o.px)
            if tr.px == o.px:
                if self.cfg.fill_model == "naive":
                    q = min(tr.qty, o.remaining)
                else:
                    eat = min(tr.qty, o.ahead)
                    o.ahead -= eat
                    q = min(tr.qty - eat, o.remaining)
                o.exec_at_px += tr.qty
                reason = "at_price"
            elif through:
                o.ahead = 0.0
                q = min(tr.qty, o.remaining)
                reason = "through"
            else:
                continue
            if q > 0:
                self.fill(o, q, tr.t, reason)

    def fill(self, o: Order, q: float, t: int, reason: str) -> None:
        cfg = self.cfg
        # real fills are lot multiples: round down (also removes float residue of the queue estimate)
        q = min(math.floor(q / cfg.lot + 1e-6) * cfg.lot, o.remaining)
        if q <= 1e-12:
            return
        if t < o.arrival or not (self.t_start <= t <= self.t_end):
            raise AssertionError("fill before the order reached the exchange or outside the episode")
        if reason == "crossing" and cfg.fill_model not in ("optimistic", "naive"):
            raise AssertionError("crossing fill outside the optimistic models")
        price = o.px * cfg.tick
        fee = cfg.maker_fee * price * q
        signed = q if o.side == BID else -q
        mid = self.cur.mid_ticks
        self.res.cash -= signed * price + fee
        self.res.inventory += signed
        self.res.fees += fee
        self.res.filled_notional += price * q
        self.res.filled_qty += q
        self.res.edge += (mid * cfg.tick - price) * signed
        self.res.max_abs_inventory = max(self.res.max_abs_inventory, abs(self.res.inventory))
        self.res.fills.append(Fill(t, o.oid, o.side, o.px, q, fee, mid, reason))
        o.filled += q
        if o.remaining <= 1e-12:
            o.status = "filled"
            self.orders.pop(o.oid, None)
        self.push(t + cfg.ack_latency_us, 3, "ack", (o, signed))

    def on_arrive(self, o: Order, t: int) -> None:
        if o.status != "in_flight":
            return
        if t > self.t_end:  # arrives after data validity ends: never active, never judged against a stale book
            o.status = "canceled"
            self.orders.pop(o.oid, None)
            return
        s = self.cur
        if o.cancel_effective is not None and o.cancel_effective <= t:
            o.status = "canceled"
            self.orders.pop(o.oid, None)
            return
        opp_best = s.asks[0][0] if o.side == BID else s.bids[0][0]
        crosses = o.px >= opp_best if o.side == BID else o.px <= opp_best
        if crosses:  # post-only (LIMIT_MAKER) is rejected; the participant learns of it after the response latency
            o.status = "rejected"
            self.res.orders_rejected += 1
            self.orders.pop(o.oid, None)
            self.push(t + self.cfg.ack_latency_us, 3, "reject_ack", o)
            return
        L = s.level(o.side, o.px)
        o.level_seen = L
        done = self.exec_since_state.get((o.side, o.px), 0.0)
        # executions since the last state already happened ahead of us: they reduce the queue now and must not be
        # counted again as cancellations at the next state
        o.exec_at_px = done
        o.ahead = math.inf if L is None else max(L - done, 0.0)
        o.status = "active"
        self.res.quoted_qty += o.qty

    def on_cancel_effective(self, o: Order) -> None:
        if o.status in ("active", "in_flight"):
            o.status = "canceled"
        if o.status != "in_flight":
            self.orders.pop(o.oid, None)

    # ---------------------------------------------------------------- participant side
    def on_decide(self, t: int, s: State) -> None:
        self.last_view_state = s
        if t < self.t_start + self.cfg.warmup_us:
            return
        working = {oid: WorkingOrder(oid, o.side, o.px, o.qty - o.known_filled) for oid, o in self.view.items()}
        want = self.policy(View(t, s, self.known_inv, working))
        for side in (BID, ASK):
            target = want.get(side)
            keep = None
            for oid, w in working.items():
                if w.side != side:
                    continue
                if target is not None and keep is None and w.px == target.px:
                    keep = oid  # same price: keep the order and its queue position, partially filled or not
                else:
                    self.cancel(self.view.pop(oid), t)
            if target is None or keep is not None:
                self.starved[side] = False
            else:
                self.send(side, target, t)

    def cancel(self, o: Order, t: int) -> None:
        o.cancel_effective = t + self.cfg.entry_latency_us
        self.push(o.cancel_effective, 2, "cancel", o)

    def send(self, side: int, qt: Quote, t: int) -> None:
        cfg, c = self.cfg, self.carry
        if (side, qt.px) in self.held:
            self.starved[side] = False  # unquoted because of the held rejection, not for lack of a token
            return
        c.recent_sends[:] = [x for x in c.recent_sends if x > t - 10_000_000]
        if len(c.recent_sends) >= cfg.max_orders_per_10s or c.orders_sent_today >= cfg.max_orders_per_day:
            self.res.rate_limited += 1
            if c.orders_sent_today >= cfg.max_orders_per_day:
                self.res.rate_limited_daily += 1
                if c.first_cap_bind_us is None:
                    c.first_cap_bind_us = t
            return
        qty = math.floor(qt.qty / cfg.lot + 1e-9) * cfg.lot
        if qty <= 0 or qty * qt.px * cfg.tick < cfg.min_notional:
            return
        if cfg.pace_rate_per_s > 0:
            tok = min(cfg.pace_burst, c.tokens.get(side, cfg.pace_burst)
                      + cfg.pace_rate_per_s * (t - c.token_t.get(side, t)) / 1e6)
            c.token_t[side] = t
            if tok < 1.0:
                c.tokens[side] = tok
                self.res.paced += 1
                if not self.starved[side]:
                    self.res.paced_spells += 1
                    self.starved[side] = True
                return
            c.tokens[side] = tok - 1.0
        o = Order(self.next_oid, side, qt.px, qty, sent=t, arrival=t + cfg.entry_latency_us)
        self.next_oid += 1
        self.orders[o.oid] = o
        self.view[o.oid] = o
        c.recent_sends.append(t)
        c.orders_sent_today += 1
        self.res.orders_sent += 1
        self.res.send_times.append(t)
        self.starved[side] = False
        self.push(o.arrival, 2, "arrive", o)

    # ---------------------------------------------------------------- episode end
    def finish(self) -> None:
        cfg, r, s = self.cfg, self.res, self.cur
        if s is None:
            return
        for o in self.orders.values():
            if o.status in ("in_flight", "active"):
                o.status = "canceled"  # data validity ends here; no fill can be inferred beyond it
        mid = s.mid_ticks * cfg.tick
        r.marked_final = r.cash + r.inventory * mid
        r.duration_s = (self.t_end - self.t_start) / 1e6
        inv = r.inventory
        if inv != 0:
            book = s.bids if inv > 0 else s.asks
            left, proceeds = abs(inv), 0.0
            for p, q in book:
                take = min(left, q)
                proceeds += take * p * cfg.tick
                left -= take
                if left <= 1e-12:
                    left = 0.0
                    break
            if left > 0:  # beyond the visible book: valued at the deepest visible price (flagged as shortfall)
                proceeds += left * book[-1][0] * cfg.tick
            vwap = proceeds / abs(inv)
            r.liquidation_slippage = (mid - vwap) * abs(inv) if inv > 0 else (vwap - mid) * abs(inv)
            r.liquidation_cost = r.liquidation_slippage + cfg.taker_fee * proceeds
            r.liquidation_shortfall = left
            r.liquidation_proceeds = proceeds
        if abs(r.marked_final - (r.edge + r.inventory_pnl - r.fees)) > 1e-6:
            raise AssertionError("accounting identity violated")
        if cfg.grid_us:  # liquidation-adjusted end of the episode (taker fee left to the overlay via the proceeds)
            r.grid.append((self.t_end, r.marked_final + r.fees - r.liquidation_slippage, r.filled_notional,
                           r.liquidation_proceeds))
        gross = r.marked_final + r.fees
        c = self.carry
        for k, (maker, taker) in enumerate(c.fee_paths):
            final = c.offset[k] + gross - r.liquidation_slippage - taker * r.liquidation_proceeds - maker * r.filled_notional
            c.mark(k, final)
            c.offset[k] = final


def p0_fixed(size: float, inv_limit: float):
    """P0: quote both sides at the visible touch with a fixed size; a side is posted only if a full fill would keep
    the acknowledged inventory within +/- inv_limit (at most one working order per side)."""
    def policy(v: View) -> dict[int, Quote]:
        out = {}
        if v.inventory + size <= inv_limit + 1e-12:
            out[BID] = Quote(v.state.bids[0][0], size)
        if v.inventory - size >= -inv_limit - 1e-12:
            out[ASK] = Quote(v.state.asks[0][0], size)
        return out
    return policy


def p1_inventory_withdrawal(size: float, inv_limit: float, threshold: float):
    """P1: as P0, but withdraw the side that would add to inventory once |inventory| >= threshold."""
    base = p0_fixed(size, inv_limit)

    def policy(v: View) -> dict[int, Quote]:
        out = base(v)
        if v.inventory >= threshold - 1e-9:  # tolerance: inventory is a float sum of lot-sized fills
            out.pop(BID, None)
        if v.inventory <= -threshold + 1e-9:
            out.pop(ASK, None)
        return out
    return policy


def no_trade(_: View) -> dict[int, Quote]:
    return {}



def _gates(v: View, key: str, sign: float, maker_fee: float, kappa: float = 0.0) -> tuple[bool, bool] | None:
    """(bid ok, ask ok) of the forecast gates: bid iff s/2 + f_t - c > 0, ask iff s/2 - f_t - c > 0, where f_t is the
    forecast (bp of mid, ``aux[key]``, times ``sign``) in ticks minus kappa * inventory and c = maker_fee * mid in ticks.
    None if the state carries no forecast."""
    a = v.state.aux
    if a is None or a.get(key) is None:
        return None
    m = v.state.mid_ticks
    ft = sign * a[key] * m / 1e4 - kappa * v.inventory
    half = (v.state.asks[0][0] - v.state.bids[0][0]) / 2
    c = maker_fee * m
    return half + ft - c > 0, half - ft - c > 0


def p3_alpha(size: float, inv_limit: float, key: str, sign: float = 1.0, maker_fee: float = 0.0):
    """P3 (E003; heuristic): quote a side at the touch only if the forecast mark-to-mid of a touch fill (from the
    decision, not conditional on the fill) exceeds the maker fee: bid iff s/2 + f_t - c > 0, ask iff s/2 - f_t - c > 0.
    sign = -1 gives the placebo P3[-M] (same withdrawal frequency, wrong direction); maker_fee = 0 gives P3, the
    schedule's maker rate gives P3F. No forecast -> no quotes."""
    base = p0_fixed(size, inv_limit)
    stats = {"decisions": 0, "gated": 0, "vol_closed": 0}

    def policy(v: View) -> dict[int, Quote]:
        g = _gates(v, key, sign, maker_fee)
        stats["decisions"] += 1
        if g is None:
            return {}
        out = base(v)
        n = len(out)
        if not g[0]:
            out.pop(BID, None)
        if not g[1]:
            out.pop(ASK, None)
        stats["gated"] += len(out) < n
        return out
    policy.stats = stats  # activity of the forecast gate: decisions on which it removed a side the base rule wanted
    return policy


def p4_combined(size: float, inv_limit: float, threshold: float, kappa: float, maker_fee: float, key: str):
    """P4 (E003): P3F with the inventory-shifted forecast f_t - kappa * q, P1's withdrawal at |q| >= threshold and a
    volatility gate (no quotes while ``aux['vol_ok']`` is false)."""
    base = p1_inventory_withdrawal(size, inv_limit, threshold)
    stats = {"decisions": 0, "gated": 0, "vol_closed": 0}

    def policy(v: View) -> dict[int, Quote]:
        g = _gates(v, key, 1.0, maker_fee, kappa)
        stats["decisions"] += 1
        if g is None:
            return {}
        if not v.state.aux.get("vol_ok", False):
            stats["vol_closed"] += 1
            return {}
        out = base(v)
        n = len(out)
        if not g[0]:
            out.pop(BID, None)
        if not g[1]:
            out.pop(ASK, None)
        stats["gated"] += len(out) < n
        return out
    policy.stats = stats
    return policy
