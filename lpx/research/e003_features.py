"""E003 decision-time features, targets and walk-forward linear forecasts (docs/experiments/E003.md sections 2-4).

Causality: the features of state k use only (i) states of the same episode with index <= k (states are in exchange-time
order; ties broken by index, so a later state with the same exchange time is never used) and (ii) exchange trades of the
same episode with exchange time <= t_exch(k) that the recorder had received by the state's receipt time t_recv(k)
(admitted from the first state from which on every receipt time is >= the trade's; a trade without a receipt time is never
used). Nothing outside the episode is read. Prices and moves are in bp of mid (log), so they do not drift with the price
level; the spread is in ticks. Targets use the future by definition
and are used only for fitting (training sessions) and for evaluation; they never enter a feature or a forecast.

Status of forecast evaluation: observed (no own fills).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import polars as pl
from numba import njit

LOT = 0.001                                                          # SOLUSDT stepSize (E002 assumptions evidence)
WINDOWS_S = {"ofi": (1, 10), "flow": (1, 10), "ret": 10, "rv": 60}   # must equal configs/e003_v1.toml [features]
REGRESSORS = ("imb1", "imb5", "ofi_1s", "ofi_10s", "flow_1s", "flow_10s", "ret_10s", "spread")


def _window_sum(prefix: np.ndarray, lo: np.ndarray, hi: np.ndarray) -> np.ndarray:
    """Sum of x[lo:hi] from prefix sums (prefix[0] = 0, prefix[i] = x[0] + ... + x[i-1])."""
    return prefix[hi] - prefix[lo]


@njit(cache=True)
def _received_window_sums(te, admit, tt, x, w):
    """For each state k: sum of the integers x_j over trades with admit_j <= k and te[k] - w < tt_j (tt sorted). Two
    pointers: a trade enters when admitted, leaves (or is never entered) once its time falls out of the window. Integer
    arithmetic (quantities in lots), so the running sum is exact over millions of trades."""
    n, m = te.size, tt.size
    order = np.argsort(admit, kind="mergesort")
    added = np.zeros(m, np.bool_)
    expired = np.zeros(m, np.bool_)
    out = np.zeros(n, np.int64)
    acc, ia, ir = 0, 0, 0
    for k in range(n):
        lo = te[k] - w
        while ir < m and tt[ir] <= lo:
            if added[ir]:
                acc -= x[ir]
            expired[ir] = True
            ir += 1
        while ia < m and admit[order[ia]] <= k:
            j = order[ia]
            if not expired[j]:
                acc += x[j]
                added[j] = True
            ia += 1
        out[k] = acc
    return out


def admission_index(te: np.ndarray, tr: np.ndarray, tt: np.ndarray, tl: np.ndarray) -> np.ndarray:
    """First state index at which a trade may be used: its exchange time <= t_exch and its receipt time <= t_recv of
    that state. Receipt times must be non-decreasing (they are in every discovery episode), so admission is monotone and
    depends on no later state. Trades without a receipt time (NaN or negative) are never admitted (index n)."""
    n = te.size
    if np.any(np.diff(tr) < 0):
        raise ValueError("state receipt times must be non-decreasing within an episode")
    a = np.maximum(np.searchsorted(te, tt, side="left"), np.searchsorted(tr.astype(float), tl, side="left"))
    bad = ~np.isfinite(tl) | (tl < 0)
    return np.where(bad, n, a).astype(np.int64)


def episode_features(te: np.ndarray, tr: np.ndarray, bpx: np.ndarray, bq: np.ndarray, apx: np.ndarray, aq: np.ndarray,
                     tt: np.ndarray, tl: np.ndarray, tq: np.ndarray, ta: np.ndarray, tick: float, t_start: int,
                     t_end: int, decision_delay_us: int, horizons_s: list[float]) -> dict[str, np.ndarray]:
    """Features and targets for the states of one episode.

    te, tr: exchange and receipt times of the episode's valid states (te non-decreasing); bpx/bq/apx/aq: (n, 10) level
    prices and sizes (NaN = no level); tt/tl/tq/ta: exchange time, receipt time (NaN if unknown), size, aggressor
    (+1 buy / -1 sell) of the episode's trades (t_start < tt <= t_end, sorted by tt). Returns arrays aligned with the
    states.
    """
    n = te.size
    if n and (np.any(np.diff(te) < 0) or te[0] < t_start or te[-1] > t_end):
        raise ValueError("states must be the episode's, in exchange-time order")
    if tt.size and (np.any(np.diff(tt) < 0) or tt[0] <= t_start or tt[-1] > t_end):
        raise ValueError("trades must be the episode's, in time order")
    bq0, aq0 = np.nan_to_num(bq), np.nan_to_num(aq)
    pb = np.rint(bpx[:, 0] / tick)
    pa = np.rint(apx[:, 0] / tick)
    mid = (pb + pa) / 2
    lm = np.log(mid) * 1e4                       # log mid in bp
    out: dict[str, np.ndarray] = {"mid_ticks": mid}
    out["imb1"] = (bq0[:, 0] - aq0[:, 0]) / (bq0[:, 0] + aq0[:, 0])
    b5, a5 = bq0[:, :5].sum(1), aq0[:, :5].sum(1)
    out["imb5"] = (b5 - a5) / (b5 + a5)
    out["spread"] = pa - pb - 1
    # Cont-Kukanov-Stoikov best-level OFI per transition (0 for the episode's first state)
    e = np.zeros(n)
    if n > 1:
        e[1:] = (bq0[1:, 0] * (pb[1:] >= pb[:-1]) - bq0[:-1, 0] * (pb[1:] <= pb[:-1])
                 - aq0[1:, 0] * (pa[1:] <= pa[:-1]) + aq0[:-1, 0] * (pa[1:] >= pa[:-1]))
    dm2 = np.zeros(n)
    dm2[1:] = np.diff(lm) ** 2
    pe = np.concatenate([[0.0], np.cumsum(e)])
    pd = np.concatenate([[0.0], np.cumsum((bq0[:, 0] + aq0[:, 0]) / 2)])
    pv = np.concatenate([[0.0], np.cumsum(dm2)])
    k = np.arange(n)
    hi = k + 1                                   # states 0..k (index order: same-time later states excluded)

    def lo_of(w_us: int) -> np.ndarray:          # first state with te > te_k - w  (window (te_k - w, te_k])
        return np.minimum(np.searchsorted(te, te - w_us, side="right"), k)

    for w_s in WINDOWS_S["ofi"]:
        name, w = f"{w_s}s", w_s * 1_000_000
        lo = lo_of(w)
        # transitions inside the window: those into states lo..k (state lo changed inside the window; e[0] = 0)
        ofi = _window_sum(pe, lo, hi)
        depth = _window_sum(pd, lo, hi) / (hi - lo)
        out[f"ofi_{name}"] = np.where(depth > 0, ofi / np.where(depth > 0, depth, 1.0), 0.0)
    lo60 = lo_of(WINDOWS_S["rv"] * 1_000_000)
    out["rv_60s"] = np.sqrt(_window_sum(pv, lo60, hi))
    # trade flow: received trades with t_exch(k) - w < t <= t_exch(k)
    admit = admission_index(te, tr, tt, tl)
    out["trades_unreceived"] = np.full(n, int((admit >= n).sum()))
    lots = np.rint(tq / LOT).astype(np.int64)
    if tq.size and np.max(np.abs(lots * LOT - tq)) > 1e-6:
        raise ValueError("trade quantities are not multiples of the lot")
    for w_s in WINDOWS_S["flow"]:
        w = w_s * 1_000_000
        sv = _received_window_sums(te.astype(np.int64), admit, tt.astype(np.int64), lots * ta.astype(np.int64), w)
        vol = _received_window_sums(te.astype(np.int64), admit, tt.astype(np.int64), lots, w)
        out[f"flow_{w_s}s"] = np.where(vol > 0, sv / np.where(vol > 0, vol, 1), 0.0)
    # 10 s log mid change in bp: last state with te <= te_k - 10 s; 0 if the episode is younger than that
    j = np.searchsorted(te, te - WINDOWS_S["ret"] * 1_000_000, side="right") - 1
    out["ret_10s"] = np.where(j >= 0, lm - lm[np.maximum(j, 0)], 0.0)
    # targets (future; fitting/evaluation only): mid at exchange time t + h, t = receipt + decision delay
    t_dec = tr + decision_delay_us
    for h in horizons_s:
        th = t_dec + int(h * 1e6)
        idx = np.searchsorted(te, th, side="right") - 1
        ok = (th <= t_end) & (idx >= 0)
        out[f"y_{h:g}s"] = np.where(ok, lm[np.maximum(idx, 0)] - lm, np.nan)
    out["t_exch_us"], out["t_recv_us"] = te, tr
    return out


def session_features(states: pl.DataFrame, trades: pl.DataFrame, eps: list[tuple[int, int]], tick: float,
                     decision_delay_us: int, horizons_s: list[float], warmup_s: float) -> pl.DataFrame:
    """Features of every valid state inside an episode. ``states``: Stage 1 rows already filtered to the validity layer,
    ``trades``: exchange trades with ``recv_us`` (recorder receipt time, null if unknown). Adds ``episode``, ``row`` (index
    into ``states``) and ``eligible`` (past the warm-up)."""
    te_all = states["t_exch_us"].to_numpy()
    tt_all = trades["exch_us"].to_numpy()
    if np.any(np.diff(te_all) < 0) or np.any(np.diff(tt_all) < 0):
        raise ValueError("inputs must be in time order")
    lv = lambda side, f: np.column_stack([states[f"{side}{i}_{f}"].to_numpy() for i in range(1, 11)])
    bpx, bq, apx, aq = lv("bid", "px"), lv("bid", "qty"), lv("ask", "px"), lv("ask", "qty")
    tr_all = states["t_local_us"].to_numpy()
    tq_all, ta_all = trades["qty"].to_numpy(), trades["aggressor"].to_numpy().astype(float)
    tl_all = trades["recv_us"].cast(pl.Float64).fill_null(float("nan")).to_numpy()
    parts = []
    for i, (a, b) in enumerate(eps):
        s0, s1 = np.searchsorted(te_all, a, side="left"), np.searchsorted(te_all, b, side="right")
        j0, j1 = np.searchsorted(tt_all, a, side="right"), np.searchsorted(tt_all, b, side="right")
        f = episode_features(te_all[s0:s1], tr_all[s0:s1], bpx[s0:s1], bq[s0:s1], apx[s0:s1], aq[s0:s1],
                             tt_all[j0:j1], tl_all[j0:j1], tq_all[j0:j1], ta_all[j0:j1], tick, a, b, decision_delay_us,
                             horizons_s)
        df = pl.DataFrame(f).with_columns(pl.lit(i).alias("episode"), pl.Series("row", np.arange(s0, s1)))
        parts.append(df.with_columns((pl.col("t_exch_us") >= a + int(warmup_s * 1e6)).alias("eligible")))
    return pl.concat(parts) if parts else pl.DataFrame()


@dataclass(frozen=True)
class LinearModel:
    """Session-weighted OLS forecast of a target in bp with an intercept; regressors clipped to training quantiles."""
    regressors: tuple[str, ...]
    lo: tuple[float, ...]
    hi: tuple[float, ...]
    coef: tuple[float, ...]           # intercept first
    trained_on: tuple[str, ...]
    n_rows: int

    def design(self, df: pl.DataFrame) -> np.ndarray:
        x = np.column_stack([df[c].to_numpy().astype(float) for c in self.regressors])
        x = np.clip(x, np.array(self.lo), np.array(self.hi))
        return np.column_stack([np.ones(x.shape[0]), x])

    def predict(self, df: pl.DataFrame) -> np.ndarray:
        return self.design(df) @ np.array(self.coef)


def training_rows(tables: dict[str, pl.DataFrame], target: str, thinning: int) -> pl.DataFrame:
    """Every ``thinning``-th eligible row of each session (in time order) that has a defined target (deterministic)."""
    out = []
    for day in sorted(tables):
        t = tables[day].filter(pl.col("eligible")).gather_every(thinning)
        out.append(t.filter(pl.col(target).is_not_null() & pl.col(target).is_not_nan()).with_columns(pl.lit(day).alias("day")))
    return pl.concat(out)


def fit_linear(tables: dict[str, pl.DataFrame], before: str, regressors: tuple[str, ...], target: str, thinning: int,
               clip_q: tuple[float, float]) -> LinearModel:
    """Walk-forward fit: only sessions strictly before ``before`` (ISO dates) are used."""
    train = {d: t for d, t in tables.items() if d < before}
    if not train or max(train) >= before:
        raise ValueError("walk-forward fit needs sessions strictly before the evaluation session")
    rows = training_rows(train, target, thinning)
    x = np.column_stack([rows[c].to_numpy().astype(float) for c in regressors])
    lo, hi = np.quantile(x, clip_q[0], axis=0), np.quantile(x, clip_q[1], axis=0)
    X = np.column_stack([np.ones(x.shape[0]), np.clip(x, lo, hi)])
    w = np.sqrt(1.0 / rows.select(pl.len().over("day"))[:, 0].to_numpy())   # sessions weighted equally
    coef, *_ = np.linalg.lstsq(X * w[:, None], rows[target].to_numpy().astype(float) * w, rcond=None)
    return LinearModel(tuple(regressors), tuple(map(float, lo)), tuple(map(float, hi)), tuple(map(float, coef)),
                       tuple(sorted(train)), rows.height)


def forecast_skill(y: np.ndarray, f: np.ndarray, f_ticks: np.ndarray | None = None,
                   half_spread: np.ndarray | None = None) -> dict:
    """Out-of-sample skill against the zero forecast: R2_OS = 1 - SSE(f) / SSE(0); IC = corr(f, y); sign hit rate on
    rows with f != 0 and y != 0; share of rows with |f in ticks| >= 0.5 tick (E003 section 7) and >= the state's half
    spread (where P3's gate withdraws a side; equal at a one-tick spread)."""
    ok = ~np.isnan(y)
    y, f = y[ok], f[ok]
    ft = f if f_ticks is None else f_ticks[ok]
    hs = np.full(ft.size, 0.5) if half_spread is None else half_spread[ok]
    nz = (f != 0) & (y != 0)
    sd = np.std(f) * np.std(y)
    return {"rows": int(y.size), "r2_os": float(1 - np.sum((y - f) ** 2) / np.sum(y ** 2)) if np.any(y) else float("nan"),
            "ic": float(np.mean((f - f.mean()) * (y - y.mean())) / sd) if sd > 0 else float("nan"),
            "hit_rate": float(np.mean(np.sign(f[nz]) == np.sign(y[nz]))) if nz.any() else float("nan"),
            "mean_abs_forecast": float(np.mean(np.abs(f))), "share_abs_forecast_ge_half_tick": float(np.mean(np.abs(ft) >= 0.5)),
            "share_abs_forecast_ge_half_spread": float(np.mean(np.abs(ft) >= hs))}


def calibration(y: np.ndarray, f: np.ndarray, bins: int = 10) -> list[dict]:
    ok = ~np.isnan(y)
    y, f = y[ok], f[ok]
    edges = np.quantile(f, np.linspace(0, 1, bins + 1))
    k = np.clip(np.searchsorted(edges, f, side="right") - 1, 0, bins - 1)
    return [{"decile": int(i), "mean_forecast": float(f[k == i].mean()), "mean_outcome": float(y[k == i].mean()),
             "rows": int((k == i).sum())} for i in range(bins) if (k == i).any()]
