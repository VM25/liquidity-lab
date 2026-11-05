"""E004 forecast level (docs/experiments/E004.md section 3): participant rows, indicators, buckets and the models
REF, NV, RF-lambda, UA-lambda, PL-lambda and UA-beta.

Rows are E003's in-episode state rows k (decision time t_k = t_recv(k) + decision delay). The participant's features are
read at its view record j(k) (``e004_degrade.view_positions``); a row without a view record yet gets f = 0 under every
participant model and the stalest age bucket. Targets:
    y_k    = E003's y_5s, the move from the true current mid mid(S_k) (hidden from the participant during a stall);
    y_view = 1e4 log(mid_ref(t_k + 5 s) / mid(S_j(k))) = y_k + log-mid(k) - log-mid(j(k)) in bp (undefined without j(k)).
Fits are session-weighted least squares (each training session weighs equally within a fit) on degraded training rows
(training seeds only); lambda fits have no intercept and are unconstrained.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import polars as pl

from lpx.research import e003_features as F
from lpx.research import e004_degrade as DG

TARGETS = ("y_k", "y_view")


def participant_rows(A: DG.Arrays, D: DG.Delivery, rec: dict, decision_delay_us: int, md_us: int) -> dict[str, np.ndarray]:
    """Per in-episode reference row: features of the view record (0 without one), view position, age and view mid."""
    rows = A.rows
    t_k = A.tr[rows] + decision_delay_us
    pos = DG.view_positions(A, D, t_k - md_us)
    has = pos >= 0
    pp = np.maximum(pos, 0)
    j = np.where(has, D.idx[pp] if D.idx.size else 0, -1)
    out = {c: np.where(has, rec[c][pp], 0.0) if D.idx.size else np.zeros(rows.size) for c in F.REGRESSORS}
    out.update(row=rows, pos=pos, has=has, view_row=j,
               age_us=np.where(has, t_k - A.te[np.maximum(j, 0)], np.inf),
               view_mid_ticks=np.where(has, rec["mid_ticks"][pp], np.nan) if D.idx.size else np.full(rows.size, np.nan),
               view_d=np.where(has, D.d[pp], -1) if D.idx.size else np.full(rows.size, -1))
    return out


def y_view(A: DG.Arrays, part: dict, y_k: np.ndarray) -> np.ndarray:
    lm = A.log_mid_bp
    j = part["view_row"]
    return np.where(part["has"], y_k + (lm[part["row"]] - lm[np.maximum(j, 0)]), np.nan)   # j = k gives y_k exactly


def age_bucket(age_us: np.ndarray, edges_s: list[float]) -> np.ndarray:
    """[0, e0], (e0, e1], ..., (e_last, inf): the number of edges strictly below the age."""
    return np.searchsorted(np.array(edges_s) * 1e6, age_us, side="left").astype(np.int64)


def pool(counts: np.ndarray, min_rows: int) -> np.ndarray:
    """Bucket -> pooled group (0 = freshest). Cumulatively from the stalest end, a bucket (or the group already merged
    into it) with fewer than ``min_rows`` training rows merges into its fresher neighbour; then the freshest group merges
    upward if it is still too small. Disclosed reading: a fresher bucket below the threshold is kept if a staler one
    merged into it brings the group to the threshold."""
    groups = [[b] for b in range(len(counts))]
    i = len(groups) - 1
    while i > 0:
        if counts[groups[i]].sum() < min_rows:
            groups[i - 1] += groups.pop(i)
        i -= 1
    if len(groups) > 1 and counts[groups[0]].sum() < min_rows:
        first = groups.pop(0)
        groups[0] = first + groups[0]
    out = np.empty(len(counts), np.int64)
    for g, bs in enumerate(groups):
        out[bs] = g
    return out


def session_weights(day: np.ndarray) -> np.ndarray:
    """1 / rows of the row's session within the fit sample (every session weighs equally in each fit; for per-group fits,
    within the group — E003's equal-session weighting applied to each fit, a disclosed reading)."""
    _, inv, cnt = np.unique(day, return_inverse=True, return_counts=True)
    return 1.0 / cnt[inv]


def fit_lambda(f: np.ndarray, y: np.ndarray, day: np.ndarray, group: np.ndarray, n_groups: int) -> np.ndarray:
    """lambda_g = sum w f y / sum w f^2 per group (session weights within the group); 0 where f is identically 0."""
    lam = np.zeros(n_groups)
    for g in range(n_groups):
        m = group == g
        if not m.any():
            continue
        w = session_weights(day[m])
        den = np.sum(w * f[m] ** 2)
        lam[g] = np.sum(w * f[m] * y[m]) / den if den > 0 else 0.0
    return lam


@dataclass(frozen=True)
class GroupModels:
    """UA-beta: M2's regressors refitted (intercept, clipping at the group's training quantiles) in each pooled group."""
    models: tuple[F.LinearModel | None, ...]

    def predict(self, x: pl.DataFrame, group: np.ndarray) -> np.ndarray:
        out = np.zeros(x.height)
        for g, m in enumerate(self.models):
            sel = group == g
            if m is not None and sel.any():
                out[sel] = m.predict(x.filter(pl.Series(sel)))
        return out


def fit_group_models(x: pl.DataFrame, y: np.ndarray, day: np.ndarray, group: np.ndarray, n_groups: int,
                     regressors: tuple[str, ...], clip_q: tuple[float, float]) -> GroupModels:
    out = []
    for g in range(n_groups):
        m = group == g
        if m.sum() <= len(regressors) + 1:
            out.append(None)
            continue
        xs = np.column_stack([x[c].to_numpy()[m].astype(float) for c in regressors])
        lo, hi = np.quantile(xs, clip_q[0], axis=0), np.quantile(xs, clip_q[1], axis=0)
        X = np.column_stack([np.ones(xs.shape[0]), np.clip(xs, lo, hi)])
        w = np.sqrt(session_weights(day[m]))
        coef, *_ = np.linalg.lstsq(X * w[:, None], y[m] * w, rcond=None)
        out.append(F.LinearModel(tuple(regressors), tuple(map(float, lo)), tuple(map(float, hi)), tuple(map(float, coef)),
                                 tuple(sorted(set(day[m].tolist()))), int(m.sum())))
    return GroupModels(tuple(out))


def calibration_slope(f: np.ndarray, y: np.ndarray) -> float:
    ok = ~np.isnan(y)
    f, y = f[ok], y[ok]
    v = np.sum((f - f.mean()) ** 2) if f.size else 0.0
    return float(np.sum((f - f.mean()) * (y - y.mean())) / v) if v > 0 else float("nan")


def skill(y: np.ndarray, f: np.ndarray, mid_ticks: np.ndarray, spread: np.ndarray) -> dict:
    """E003's skill measures (R2_OS in percentage points) with the gate shares on the given (view or true) state."""
    s = F.forecast_skill(y, f, f * mid_ticks / 1e4, (spread + 1) / 2)
    return {"rows": s["rows"], "r2_os_pp": 100 * s["r2_os"], "ic": s["ic"], "hit_rate": s["hit_rate"],
            "mean_abs_forecast": s["mean_abs_forecast"],
            "share_abs_forecast_ge_half_spread": s["share_abs_forecast_ge_half_spread"]}
