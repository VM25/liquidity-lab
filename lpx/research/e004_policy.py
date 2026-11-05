"""E004 policy level (docs/experiments/E004.md sections 4-5): view states, the staleness windows W_U and their
duty-matched placebo W_P, the U and P variants, and fee-free fill quality inside windows.

Clocks. View decisions happen at d + md (the participant's clock). W_U = {t : alpha(t) >= tau} on that clock, restricted
to the post-warm-up span [a + warm-up, b] of each episode, where alpha(t) = t - t_exch of the last view record with
d + md <= t (the latest record of a tied batch: all records delivered by t are known at t). Concretely, record i (view time
v_i) contributes [max(v_i, t_exch_i + tau), v_{i+1}), with v_{n} = b + 1 so that a decision at b itself is covered; the
union is merged into maximal spells. Exchange-clock windows W^x = W + entry latency (cancels take effect then).

W_P: every maximal W_U spell of an episode is shifted circularly by floor(u L) on the span (length L), one u ~ U[0.25,
0.75] per episode from the role-4 stream, redrawn while any image would be cut at the seam or touch another image (so
images are maximal spells with the same multiset of lengths). After ``cap`` redraws the episode is excluded from both
windows (U still follows its causal rule there).
"""

from __future__ import annotations

import numpy as np

from lpx.execution import sim as X
from lpx.research.e004_schedules import merge


def member(spells: np.ndarray, t: float) -> bool:
    """t in the union of sorted, disjoint half-open spells."""
    k = int(np.searchsorted(spells[:, 0], t, side="right")) - 1
    return k >= 0 and t < spells[k, 1]


def members(spells: np.ndarray, t: np.ndarray) -> np.ndarray:
    if spells.shape[0] == 0:
        return np.zeros(np.shape(t), bool)
    k = np.searchsorted(spells[:, 0], t, side="right") - 1
    return (k >= 0) & (t < spells[np.maximum(k, 0), 1])


def episode_views(states: list[X.State], i0: int, idx: np.ndarray, d: np.ndarray, f_m2: np.ndarray, md_us: int,
                  t_end: int) -> list[tuple[int, int, X.State]]:
    """(decision time, episode-local source index, view state) of one episode's delivered records; the view state is a
    copy of the true state (same exchange time, prices and sizes) with its receipt time set to the delivery time and the
    participant's (NV) M2 forecast attached."""
    out = []
    for j, dj, f in zip(idx.tolist(), d.tolist(), f_m2.tolist()):
        t = dj + md_us
        if t > t_end:
            break
        s = states[j]
        out.append((t, j - i0, X.State(s.t_exch, dj, s.bids, s.asks, {"M2": f})))
    return out


def stale_spells(vt: np.ndarray, vte: np.ndarray, lo: int, b: int, tau_us: int) -> np.ndarray:
    """Maximal spells of W_U in one episode (participant clock), within [lo, b + 1)."""
    if vt.size == 0:
        return np.empty((0, 2), np.int64)
    nxt = np.append(vt[1:], b + 1)
    s = np.clip(np.maximum(vt, vte + tau_us), lo, b + 1)
    e = np.clip(nxt, lo, b + 1)
    return merge(np.column_stack([s, e]))


def placebo_images(spells: np.ndarray, lo: int, hi: int, rng: np.random.Generator, lo_u: float, hi_u: float,
                   cap: int) -> tuple[np.ndarray | None, int]:
    """Images of the spells (same order) under one circular shift of the span [lo, hi), and the number of redraws; None
    if ``cap`` redraws did not give an image set without seam cuts or touching images."""
    if spells.shape[0] == 0:
        return np.empty((0, 2), np.int64), 0
    L = hi - lo
    ln = spells[:, 1] - spells[:, 0]
    for redraws in range(cap + 1):
        o = int(np.floor(rng.uniform(lo_u, hi_u) * L))
        x = (spells[:, 0] - lo + o) % L
        if np.any(x + ln > L):
            continue
        k = np.argsort(x, kind="mergesort")
        if np.any(x[k][1:] <= x[k][:-1] + ln[k][:-1]):
            continue
        img = np.column_stack([x + lo, x + lo + ln]).astype(np.int64)
        if not np.array_equal(np.sort(img[:, 1] - img[:, 0]), np.sort(ln)):
            raise AssertionError("placebo spells must keep the spell multiset")
        return img, redraws
    return None, cap


def withdraw_when_stale(base, vt: np.ndarray, vte: np.ndarray, tau_us: int, wu: np.ndarray, stats: dict):
    """U: the base rule, but no order on either side while the information is stale (alpha(t) >= tau), checked causally on
    the view records delivered by t and asserted equal to W_U membership at every decision."""
    stats.update(decisions=0, withdrawn=0, superseded_state=0)

    def policy(v: X.View):
        out = base(v)
        i = int(np.searchsorted(vt, v.t, side="right")) - 1
        if i < 0:
            raise AssertionError("a decision before any view record")
        stale = v.t - vte[i] >= tau_us
        if stale != member(wu, v.t):
            raise AssertionError("U's causal rule disagrees with W_U membership")
        stats["decisions"] += 1
        stats["superseded_state"] += v.state.t_exch != vte[i]     # a decision on an earlier record of a tied batch
        if stale:
            stats["withdrawn"] += 1
            return {}
        return out
    policy.stats = getattr(base, "stats", None)
    return policy


def withdraw_in_windows(base, wp: np.ndarray, stats: dict):
    """P: the base rule, but no order on either side while t is in W_P."""
    stats.update(decisions=0, withdrawn=0)

    def policy(v: X.View):
        out = base(v)
        stats["decisions"] += 1
        if member(wp, v.t):
            stats["withdrawn"] += 1
            return {}
        return out
    policy.stats = getattr(base, "stats", None)
    return policy


def fill_arrays(fills: list[X.Fill], tick: float, eps: list[tuple[int, int]]) -> dict[str, np.ndarray]:
    """Fill arrays with the episode index of each fill: order ids restart in every episode's simulator, so an order is
    identified by (episode, order id)."""
    t = np.array([f.t for f in fills], np.int64)
    ends = np.array([b for _, b in eps], np.int64)
    return {"t": t, "ep": np.searchsorted(ends, t, side="left"), "oid": np.array([f.oid for f in fills], np.int64),
            "sgn": np.array([1.0 if f.side == X.BID else -1.0 for f in fills]),
            "px": np.array([f.px * tick for f in fills]), "qty": np.array([f.qty for f in fills])}


def pi5(fa: dict, eps: list[tuple[int, int]], t_states: np.ndarray, mid: np.ndarray, h_us: int) -> tuple[np.ndarray, np.ndarray]:
    """Fee-free mark-to-mid of each fill at T + h on the exchange-side states (USDT), and whether it is defined
    (T + h within the fill's episode)."""
    t = fa["t"]
    if t.size == 0:
        return np.zeros(0), np.zeros(0, bool)
    ends = np.array([b for _, b in eps])
    ep_end = ends[np.searchsorted(ends, t, side="left")]
    th = t + h_us
    ok = th <= ep_end
    m = mid[np.maximum(np.searchsorted(t_states, th, side="right") - 1, 0)]
    return np.where(ok, fa["sgn"] * (m - fa["px"]) * fa["qty"], 0.0), ok
