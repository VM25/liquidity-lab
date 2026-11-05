"""E004 participant information: delivery streams under each degradation (docs/experiments/E004.md section 2-3).

The exchange side is never touched: everything here builds what the *participant* receives — which depth states it gets
and when (their delivery time d on the recorder clock), with which sizes, and which trades. Withheld records stay in the
reference arrays for the exchange side and for targets only.

    none                      every state at d = t_recv; every trade (D0)
    book_stall_withhold       states received in a stall are lost; at the stall end the last state of the episode with
                              t_recv <= end is delivered (resync, d = end) if it was withheld; trades continue (D1-S*)
    connection_drop_withhold  as above, and trades received in a stall are lost too (D1-E)
    catchup_delay             states received in a stall are delivered in order at its end (D3); trades continue
    trade_outage_withhold     trades received in an outage are lost; states unaffected (D2)
    size_noise                states received in a noisy regime carry noisy level sizes; prices untouched (D4)

Delivered states keep their exchange time and prices; delivery is per episode (nothing crosses an episode boundary), and
within an episode delivered records are in index order with non-decreasing d >= t_recv (asserted).

The participant's state at a decision time t is j = the last delivered record of the episode with d(j) + md <= t, ties
broken by index <= k for a reference row k (its own state is never preceded by a later one). Features are E003's,
computed by the unchanged ``episode_features`` on the delivered arrays (d in place of the receipt time, so trade
admission follows delivery) and read at j.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import polars as pl
from numba import njit

from lpx.research import e003_features as F

KINDS = ("none", "book_stall_withhold", "connection_drop_withhold", "catchup_delay", "trade_outage_withhold",
         "size_noise")
AGE_KINDS = ("book_stall_withhold", "connection_drop_withhold", "catchup_delay")


@dataclass
class Arrays:
    """One session's valid states and exchange trades as arrays, extracted exactly as E003's ``session_features``."""
    day: str
    te: np.ndarray
    tr: np.ndarray
    bpx: np.ndarray
    bq: np.ndarray
    apx: np.ndarray
    aq: np.ndarray
    tt: np.ndarray
    tl: np.ndarray       # receipt time (float, NaN if unknown)
    tq: np.ndarray
    ta: np.ndarray
    tid: np.ndarray
    eps: list[tuple[int, int]]
    ep_states: list[tuple[int, int]] = field(default_factory=list)
    ep_trades: list[tuple[int, int]] = field(default_factory=list)

    def __post_init__(self):
        self.ep_states = [(int(np.searchsorted(self.te, a, side="left")), int(np.searchsorted(self.te, b, side="right")))
                          for a, b in self.eps]
        self.ep_trades = [(int(np.searchsorted(self.tt, a, side="right")), int(np.searchsorted(self.tt, b, side="right")))
                          for a, b in self.eps]
        lm = np.log((np.rint(self.bpx[:, 0] / 0.01) + np.rint(self.apx[:, 0] / 0.01)) / 2) * 1e4
        self.log_mid_bp = lm

    @property
    def rows(self) -> np.ndarray:
        """Session indices of the states inside episodes, in order (the rows of E003's feature table)."""
        return np.concatenate([np.arange(s0, s1) for s0, s1 in self.ep_states]) if self.ep_states else np.array([], int)


def from_frames(day: str, states: pl.DataFrame, trades: pl.DataFrame, eps: list[tuple[int, int]], tick: float) -> Arrays:
    if tick != 0.01:
        raise ValueError("log_mid_bp assumes the SOLUSDT tick of 0.01")
    lv = lambda side, f: np.column_stack([states[f"{side}{i}_{f}"].to_numpy() for i in range(1, 11)])
    return Arrays(day, states["t_exch_us"].to_numpy(), states["t_local_us"].to_numpy(), lv("bid", "px"), lv("bid", "qty"),
                  lv("ask", "px"), lv("ask", "qty"), trades["exch_us"].to_numpy(),
                  trades["recv_us"].cast(pl.Float64).fill_null(float("nan")).to_numpy(), trades["qty"].to_numpy(),
                  trades["aggressor"].to_numpy().astype(float), trades["trade_id"].to_numpy().astype(np.int64), eps)


def inside(t: np.ndarray, iv: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """For each time: whether it lies in a half-open interval [start, end) of the merged list, and that interval's end
    (undefined where outside). NaN times are outside."""
    t = np.asarray(t, float)
    iv = np.asarray(iv, np.int64).reshape(-1, 2)
    if iv.shape[0] == 0:
        return np.zeros(t.shape, bool), np.zeros(t.shape, np.int64)
    k = np.searchsorted(iv[:, 0], t, side="right") - 1
    kk = np.maximum(k, 0)
    ok = (k >= 0) & (t < iv[kk, 1])
    return ok, iv[kk, 1]


@dataclass
class Delivery:
    kind: str
    idx: np.ndarray            # delivered state indices (session), in delivery order
    d: np.ndarray              # delivery times, recorder clock
    resync: np.ndarray         # delivered at a stall end (resync or catch-up)
    ep_pos: list[tuple[int, int]]   # each episode's slice of idx / d
    bq: np.ndarray             # participant level sizes (the reference arrays unless noisy)
    aq: np.ndarray
    trade_ok: np.ndarray       # trade delivered (not withheld)
    noisy: np.ndarray          # state delivered with noisy sizes
    stats: dict


def deliver(A: Arrays, kind: str, iv: np.ndarray | None = None, noise: tuple[np.random.Generator, float, float] | None = None
            ) -> Delivery:
    """The participant's stream under one degradation. ``iv``: the cell's merged schedule (absolute microseconds);
    ``noise``: (noise stream, sigma, lot) for size_noise."""
    if kind not in KINDS:
        raise ValueError(kind)
    iv = np.empty((0, 2), np.int64) if iv is None else np.asarray(iv, np.int64)
    idx, d, rs, pos = [], [], [], []
    n_with, n_delay = 0, 0
    p = 0
    for s0, s1 in A.ep_states:
        k = np.arange(s0, s1)
        tr = A.tr[s0:s1]
        if kind in ("book_stall_withhold", "connection_drop_withhold"):
            w, end = inside(tr, iv)
            keep_i, keep_d, keep_r = list(k[~w]), list(tr[~w]), [False] * int((~w).sum())
            for e in np.unique(end[w]):
                r = int(np.searchsorted(tr, e, side="right")) - 1     # last episode state with t_recv <= stall end
                if w[r]:
                    keep_i.append(s0 + r)
                    keep_d.append(int(e))
                    keep_r.append(True)
            o = np.argsort(np.array(keep_i), kind="mergesort")
            ki, kd, kr = np.array(keep_i, np.int64)[o], np.array(keep_d, np.int64)[o], np.array(keep_r, bool)[o]
            n_with += int(w.sum() - kr.sum())
        elif kind == "catchup_delay":
            w, end = inside(tr, iv)
            ki, kd, kr = k, np.where(w, end, tr).astype(np.int64), w
            n_delay += int(w.sum())
        else:
            ki, kd, kr = k, tr.astype(np.int64), np.zeros(k.size, bool)
        if np.any(kd < A.tr[ki]) or np.any(np.diff(kd) < 0) or np.any(np.diff(ki) <= 0):
            raise AssertionError("delivery must be in index order with non-decreasing d >= t_recv")
        idx.append(ki)
        d.append(kd)
        rs.append(kr)
        pos.append((p, p + ki.size))
        p += ki.size
    idx = np.concatenate(idx) if idx else np.array([], np.int64)
    d = np.concatenate(d) if d else np.array([], np.int64)
    rs = np.concatenate(rs) if rs else np.array([], bool)
    trade_ok = np.ones(A.tt.size, bool)
    if kind in ("connection_drop_withhold", "trade_outage_withhold"):
        trade_ok = ~inside(A.tl, iv)[0]
    bq, aq, noisy = A.bq, A.aq, np.zeros(A.te.size, bool)
    if kind == "size_noise":
        rng, sigma, lot = noise
        eps_ = rng.standard_normal((A.te.size, 2, 10))       # indexed by state: same draw whatever the schedule
        noisy = inside(A.tr, iv)[0]
        bq, aq = A.bq.copy(), A.aq.copy()
        for side, arr in ((0, bq), (1, aq)):
            m = np.exp(sigma * eps_[noisy, side, :] - sigma ** 2 / 2)
            x = arr[noisy] * m
            arr[noisy] = np.where(np.isnan(x), np.nan, np.maximum(np.rint(x / lot), 1.0) * lot)
    in_ep = A.rows
    trades_in = np.concatenate([np.arange(j0, j1) for j0, j1 in A.ep_trades]) if A.ep_trades else np.array([], int)
    stats = {"kind": kind, "states": int(in_ep.size), "delivered": int(idx.size), "withheld": n_with,
             "delayed": n_delay, "resyncs": int(rs.sum()) if kind != "catchup_delay" else 0,
             "trades": int(trades_in.size), "trades_withheld": int((~trade_ok[trades_in]).sum()),
             "noisy_states": int(noisy[in_ep].sum()),
             "schedule_share_of_episodes": covered_share(iv, A.eps)}
    return Delivery(kind, idx, d, rs, pos, bq, aq, trade_ok, noisy, stats)


def covered_share(iv: np.ndarray, eps: list[tuple[int, int]]) -> float:
    """Share of episode time (recorder clock taken as the episode span) covered by the schedule's intervals."""
    tot = sum(b - a for a, b in eps)
    if not tot:
        return float("nan")
    cov = 0
    for a, b in eps:
        lo, hi = np.maximum(iv[:, 0], a), np.minimum(iv[:, 1], b)
        cov += int(np.clip(hi - lo, 0, None).sum())
    return cov / tot


def view_positions(A: Arrays, D: Delivery, t_dec_minus_md: np.ndarray) -> np.ndarray:
    """For every in-episode reference row k (``A.rows`` order): the global position in D of the participant's state, i.e.
    the last delivered record of the episode with d <= t_k - md and index <= k; -1 if there is none yet."""
    out = []
    o = 0
    for (s0, s1), (p0, p1) in zip(A.ep_states, D.ep_pos):
        k = np.arange(s0, s1)
        t = t_dec_minus_md[o:o + k.size]
        o += k.size
        a = np.minimum(np.searchsorted(D.d[p0:p1], t, side="right"), np.searchsorted(D.idx[p0:p1], k, side="right")) - 1
        out.append(np.where(a >= 0, a + p0, -1))
    return np.concatenate(out) if out else np.array([], np.int64)


def record_features(A: Arrays, D: Delivery, tick: float, decision_delay_us: int) -> dict[str, np.ndarray]:
    """E003's features of every delivered record (global positions of D), from the delivered arrays of each episode."""
    parts = []
    for (s0, s1), (j0, j1), (p0, p1), (a, b) in zip(A.ep_states, A.ep_trades, D.ep_pos, A.eps):
        ii = D.idx[p0:p1]
        ok = D.trade_ok[j0:j1]
        f = F.episode_features(A.te[ii], D.d[p0:p1], A.bpx[ii], D.bq[ii], A.apx[ii], D.aq[ii], A.tt[j0:j1][ok],
                               A.tl[j0:j1][ok], A.tq[j0:j1][ok], A.ta[j0:j1][ok], tick, a, b, decision_delay_us, [])
        parts.append(f)
    keys = list(F.REGRESSORS) + ["mid_ticks"]
    return {c: np.concatenate([p[c] for p in parts]) if parts else np.array([]) for c in keys}


@njit(cache=True)
def _gap_flags(te, T, tt, tl_adm, ok, tid, w):
    """Per record p: True if the trade ids admitted by T[p] (delivered, received by T[p], exchange time in
    (te[p] - w, te[p]]) are non-consecutive anywhere in that window."""
    n, m = te.size, tt.size
    out = np.zeros(n, np.bool_)
    lo, hi = 0, 0
    for p in range(n):
        while lo < m and tt[lo] <= te[p] - w:
            lo += 1
        while hi < m and tt[hi] <= te[p]:
            hi += 1
        last = -1
        for i in range(lo, hi):
            if ok[i] and tl_adm[i] <= T[p]:
                if last >= 0 and tid[i] != last + 1:
                    out[p] = True
                    break
                last = tid[i]
    return out


def gap_flags(A: Arrays, D: Delivery, trade_ok: np.ndarray, window_us: int) -> np.ndarray:
    """D2's trade-gap flag of every delivered record, with the given delivered-trade mask (actual or placebo)."""
    out = []
    tl_adm = np.where(np.isfinite(A.tl), A.tl, np.inf)
    for (j0, j1), (p0, p1) in zip(A.ep_trades, D.ep_pos):
        ii = D.idx[p0:p1]
        out.append(_gap_flags(A.te[ii].astype(np.int64), D.d[p0:p1].astype(float), A.tt[j0:j1].astype(np.int64),
                              tl_adm[j0:j1], trade_ok[j0:j1], A.tid[j0:j1], window_us))
    return np.concatenate(out) if out else np.array([], bool)
