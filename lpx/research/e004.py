"""E004 runner — information robustness, as frozen in configs/e004_v1.toml and docs/experiments/E004.md.

Pass 1, for every discovery session: E003's features (reference), E003's thinned training rows, and each degraded cell's
participant rows on the training draw (role 0) with its placebo indicator (role 2). Pass 2, for each evaluation session
s6..s15: E003's walk-forward M1/M2 (asserted equal to results/e003/e003_models.json), REF forecasts (asserted equal to
E003's per-row recomputation and aggregates), lambda fits on earlier sessions' degraded training rows, the participant
models on the 3 evaluation draws (role 1; placebo role 3), and the policies: REF (asserted equal to E003's frozen rows),
D0 through the view path (asserted equal to REF), and N / U / P under D1-E (primary) and D1-S (descriptive).

Status labels are written on every row (section "Status labels" of the specification).

Usage (only after the acceptance criteria of E004.md section 7 are met):
    uv run python -m lpx.research.e004
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import hashlib
import json
import math
import pickle
import subprocess
import time
import tomllib

import numpy as np
import polars as pl

from lpx.data.acquire import ROOT
from lpx.execution import sim as X
from lpx.research import e003 as E3
from lpx.research import e003_features as F
from lpx.research import e004_degrade as DG
from lpx.research import e004_forecast as FC
from lpx.research import e004_policy as PO
from lpx.research import e004_schedules as G
from lpx.research.e002 import to_states, to_trades

OUT = ROOT / "results" / "e004"
CONFIG = ROOT / "configs" / "e004_v1.toml"
SPEC = ROOT / "docs" / "experiments" / "E004.md"
HASHES = ROOT / "results" / "e004_prefreeze" / "schedule_hashes.json"
E003_OUT = ROOT / "results" / "e003"
BASE_SECTIONS = ("instrument", "pacing", "features", "latency", "fees", "fill_models", "policies")
# E003's policy-outcome definitions ("Policies as in E003", E004.md section 5): needed to reproduce E003's rows
E003_OUTCOME_KEYS = ("risk_grid_s", "expected_shortfall_q", "markout_horizons_s")
CELL_ORDER = ("D1_E", "D1_S", "D1_S1", "D1_S3", "D3", "D2", "D4")
POLICY_CELLS = ("D1_E", "D1_S")
BASES = ("P0", "P3_M2")
VARIANTS = ("N", "U", "P")
STATUS_POLICY_REF = "modeled historical replay"
STATUS_POLICY_DEG = "modeled historical replay under stress test"


def load_cfg() -> tuple[dict, dict]:
    """(E004 configuration, simulation configuration in E003's shape: its read sections plus E003's outcome
    definitions)."""
    e4 = tomllib.loads(CONFIG.read_text())
    e3 = tomllib.loads((ROOT / e4["scope"]["base_config"]).read_text())
    sc = {k: e3[k] for k in BASE_SECTIONS}
    sc["scope"] = e3["scope"]
    sc["analysis"] = {k: e3["analysis"][k] for k in E003_OUTCOME_KEYS}
    ps = e4["analysis"]["primary_scenario"]
    sc["e004_primary"] = (ps["fill_model"], ps["latency"])
    return e4, sc


def kind_of(e4: dict, cell: str) -> str:
    return "none" if cell == "D0" else e4["degradations"][cell]["kind"]


def draw(e4: dict, sc: dict, A: DG.Arrays, cell: str, role: str, rep: int) -> tuple[DG.Delivery, np.ndarray]:
    """One draw of a cell's delivery stream and its schedule; the role actually used is recorded on the delivery."""
    kind = kind_of(e4, cell)
    if role not in e4["seeds"]["roles"]:
        raise ValueError(role)
    if kind == "none":
        D = DG.deliver(A, "none")
        D.stats["seed_role"] = e4["seeds"]["roles"][role]
        return D, np.empty((0, 2), np.int64)
    iv = G.schedule(e4, cell, A.day, role, rep)
    noise = None
    if kind == "size_noise":
        s = e4["seeds"]
        rng = G.stream(s["entropy"], s["cell_codes"][cell], A.day, s["roles"][role], rep, s["noise_spawn_suffix"])
        noise = (rng, e4["degradations"][cell]["sigma"], sc["instrument"]["lot"])
    D = DG.deliver(A, kind, iv, noise)
    D.stats["seed_role"] = e4["seeds"]["roles"][role]
    return D, iv


def flow_window_us() -> int:
    return max(F.WINDOWS_S["flow"]) * 1_000_000


def indicator(e4: dict, sc: dict, A: DG.Arrays, D: DG.Delivery, part: dict, cell: str, iv: np.ndarray,
              trade_ok: np.ndarray | None = None) -> np.ndarray:
    """The participant's indicator bucket per row: age bucket (D0, D1, D3) or flag (D4 noisy regime, D2 trade gap) of
    its view record; rows without a view record get the stalest bucket / flag 1. ``trade_ok`` overrides D2's delivered
    trades (placebo)."""
    kind = kind_of(e4, cell)
    has, pos = part["has"], np.maximum(part["pos"], 0)
    if kind == "size_noise":
        return np.where(has, DG.inside(part["view_d"], iv)[0], True).astype(np.int64)
    if kind == "trade_outage_withhold":
        ok = D.trade_ok if trade_ok is None else trade_ok
        g = DG.gap_flags(A, D, ok, flow_window_us())
        return np.where(has, g[pos] if g.size else False, True).astype(np.int64)
    return FC.age_bucket(part["age_us"], e4["indicators"]["age_bucket_edges_s"])


def placebo_indicator(e4: dict, sc: dict, A: DG.Arrays, D: DG.Delivery, part: dict, cell: str, role: str, rep: int
                      ) -> np.ndarray:
    """The same indicator from an independent draw of the same law (placebo schedule), on the same rows."""
    kind = kind_of(e4, cell)
    iv = G.schedule(e4, cell, A.day, role, rep)
    if kind == "size_noise":
        return indicator(e4, sc, A, D, part, cell, iv)
    if kind == "trade_outage_withhold":
        return indicator(e4, sc, A, D, part, cell, iv, trade_ok=~DG.inside(A.tl, iv)[0])
    Dp = DG.deliver(A, kind, iv)
    fc = sc["features"]
    t_k = A.tr[A.rows] + fc["decision_delay_us"]
    pos = DG.view_positions(A, Dp, t_k - md_us(sc))
    j = np.where(pos >= 0, Dp.idx[np.maximum(pos, 0)], 0)
    age = np.where(pos >= 0, t_k - A.te[j], np.inf)
    return FC.age_bucket(age, e4["indicators"]["age_bucket_edges_s"])


def md_us(sc: dict) -> int:
    """Market-data delay of the primary latency bracket: the participant acts on a record at d + md."""
    return sc["latency"][sc["e004_primary"][1]]["md_delay_us"]


def cell_rows(e4: dict, sc: dict, A: DG.Arrays, cell: str, role: str, rep: int, pl_role: str | None):
    """Participant rows of one draw: (delivery, schedule, record features, rows dict, UA bucket, PL bucket)."""
    fc = sc["features"]
    D, iv = draw(e4, sc, A, cell, role, rep)
    rec = DG.record_features(A, D, sc["instrument"]["tick"], fc["decision_delay_us"])
    part = FC.participant_rows(A, D, rec, fc["decision_delay_us"], md_us(sc))
    b_ua = indicator(e4, sc, A, D, part, cell, iv)
    b_pl = placebo_indicator(e4, sc, A, D, part, cell, pl_role, rep) if pl_role else None
    return D, iv, rec, part, b_ua, b_pl


def xframe(part: dict) -> pl.DataFrame:
    return pl.DataFrame({c: part[c] for c in F.REGRESSORS})


def n_buckets(e4: dict, cell: str) -> int:
    k = kind_of(e4, cell)
    return 2 if k in ("size_noise", "trade_outage_withhold") else len(e4["indicators"]["age_bucket_edges_s"]) + 1


# ------------------------------------------------------------------------------------------------- training (pass 1)
def training_rows(e4: dict, sc: dict, A: DG.Arrays, ft: pl.DataFrame, cell: str) -> dict:
    """E003's thinned eligible rows (every fit_thinning-th eligible row of the session) of the training draw."""
    if not np.array_equal(ft["row"].to_numpy(), A.rows):
        raise AssertionError("participant rows must align with E003's feature rows")
    D, _, _, part, b_ua, b_pl = cell_rows(e4, sc, A, cell, "train", 0, "placebo_train")
    el = np.flatnonzero(ft["eligible"].to_numpy())[::sc["features"]["fit_thinning"]]
    y_k = ft["y_5s"].to_numpy()
    out = {c: part[c][el] for c in F.REGRESSORS}
    out.update(has=part["has"][el], b_ua=b_ua[el], b_pl=b_pl[el], y_k=y_k[el], y_view=FC.y_view(A, part, y_k)[el],
               day=np.full(el.size, A.day), seed_role=np.full(el.size, D.stats["seed_role"]))
    return out


def stack(rows: list[dict]) -> dict:
    return {k: np.concatenate([r[k] for r in rows]) for k in rows[0]}


@dataclasses.dataclass
class CellFit:
    """Per target: pooled groups and lambdas of RF, UA and PL, and UA-beta, from earlier sessions' training rows."""
    groups: dict
    lam: dict
    beta: dict
    train_rows: dict


def fit_cell(e4: dict, sc: dict, tr: dict, m2: F.LinearModel, cell: str, before: str) -> CellFit:
    """Fits for the evaluation session ``before`` from earlier sessions' training draws only (asserted)."""
    fc = sc["features"]
    if np.any(tr["seed_role"] != e4["seeds"]["roles"]["train"]) or max(tr["day"].tolist()) >= before:
        raise AssertionError("lambda fits may use only training draws of earlier sessions")
    f = m2.predict(pl.DataFrame({c: tr[c] for c in F.REGRESSORS})) * tr["has"]
    nb = n_buckets(e4, cell)
    groups, lam, beta, rows = {}, {}, {}, {}
    for tgt in FC.TARGETS:
        y = tr[tgt]
        ok = ~np.isnan(y)
        rows[tgt] = int(ok.sum())
        lam[(tgt, "RF")] = FC.fit_lambda(f[ok], y[ok], tr["day"][ok], np.zeros(ok.sum(), np.int64), 1)
        for ind in ("UA", "PL"):
            b = tr["b_ua" if ind == "UA" else "b_pl"][ok]
            g = FC.pool(np.bincount(b, minlength=nb), e4["indicators"]["min_bucket_training_rows"])
            groups[(tgt, ind)] = g
            lam[(tgt, ind)] = FC.fit_lambda(f[ok], y[ok], tr["day"][ok], g[b], int(g.max()) + 1)
        g = groups[(tgt, "UA")]
        m = ok & tr["has"]
        beta[tgt] = FC.fit_group_models(pl.DataFrame({c: tr[c][m] for c in F.REGRESSORS}), y[m], tr["day"][m],
                                        g[tr["b_ua"][m]], int(g.max()) + 1, tuple(fc["regressors_m2"]),
                                        tuple(fc["clip_quantiles"]))
    return CellFit(groups, lam, beta, rows)


# ------------------------------------------------------------------------------------------------- evaluation helpers
def model_forecasts(fit: CellFit, tgt: str, part: dict, f_nv: np.ndarray, b_ua: np.ndarray, b_pl: np.ndarray) -> dict:
    gu, gp = fit.groups[(tgt, "UA")], fit.groups[(tgt, "PL")]
    return {"NV": f_nv, "RF-lambda": fit.lam[(tgt, "RF")][0] * f_nv, "UA-lambda": fit.lam[(tgt, "UA")][gu[b_ua]] * f_nv,
            "PL-lambda": fit.lam[(tgt, "PL")][gp[b_pl]] * f_nv,
            "UA-beta": fit.beta[tgt].predict(xframe(part), gu[b_ua]) * part["has"]}


def status_forecast(cell: str, model: str, target: str = "y_k") -> str:
    if cell == "D0":
        return "observed (model trained under stress test)" if "[" in model else "observed"
    if model == "REF":
        return "observed" if target == "y_k" else "observed forecast; target under stress test"
    return "stress test"


def state_hash(states: list[X.State], trades: list[X.Trade]) -> str:
    h = hashlib.sha256()
    h.update(pickle.dumps([(s.t_exch, s.t_recv, s.bids, s.asks, s.aux) for s in states], protocol=5))
    h.update(pickle.dumps([(t.t, t.px, t.qty, t.aggressor) for t in trades], protocol=5))
    return h.hexdigest()


def views_hash(views: list) -> str:
    return hashlib.sha256(pickle.dumps([[(t, s, v.t_exch, v.t_recv, v.bids, v.asks, v.aux) for t, s, v in ep]
                                        for ep in views], protocol=5)).hexdigest()


def p3_rescaled(pc: dict, lam: np.ndarray, group: np.ndarray, edges_s: list[float], age_of):
    """P3[M2] on a lambda-rescaled NV forecast: lambda of the age bucket at the decision (UA: the participant's age;
    PL: the placebo stream's age). Descriptive and participation-changing."""
    base = X.p3_alpha(pc["size"], pc["inventory_limit"], "M2s")
    edges = np.array(edges_s) * 1e6

    def policy(v: X.View):
        b = int(np.searchsorted(edges, age_of(v.t), side="left"))
        s = v.state
        aux = {"M2s": float(lam[group[b]] * s.aux["M2"])}
        return base(X.View(v.t, X.State(s.t_exch, s.t_recv, s.bids, s.asks, aux), v.inventory, v.working))
    policy.stats = base.stats
    return policy


def latest_age(vt: np.ndarray, vte: np.ndarray):
    def age(t: int) -> float:
        i = int(np.searchsorted(vt, t, side="right")) - 1
        return t - vte[i] if i >= 0 else np.inf
    return age


@dataclasses.dataclass
class Windows:
    views: list            # per episode
    vt: np.ndarray         # session view times / exchange times (sorted)
    vte: np.ndarray
    wu_full: np.ndarray    # W_U including excluded episodes (U's rule)
    wu: np.ndarray         # analysis windows (excluded episodes removed)
    wp: np.ndarray
    wu_spells: np.ndarray  # spells aligned with their images (analysis episodes)
    wp_images: np.ndarray
    extras: list           # per episode
    span_us: int           # post-warm-up time of the analysed (not excluded) episodes
    redraws: int
    max_redraws: int
    excluded: int


def windows(e4: dict, sc: dict, sd: E3.SessionData, A: DG.Arrays, D: DG.Delivery, f_rec: np.ndarray, cell: str,
            rep: int) -> Windows:
    """View states, W_U, W_P and the extra decision times of one draw (participant clock)."""
    s = e4["seeds"]
    md = md_us(sc)
    tau = e4["indicators"]["tau_ms"] * 1000
    warm = int(sc["features"]["warmup_s"] * 1e6)
    pcfg = e4["policies"]
    rng = G.stream(s["entropy"], s["cell_codes"][cell], A.day, s["roles"]["placebo_window"], rep)
    views, extras, vts, vtes, wuf, wu, wp, sp, im = [], [], [], [], [], [], [], [], []
    span = redraws = max_rd = excluded = 0
    for (a, b), (s0, _), (p0, p1) in zip(A.eps, A.ep_states, D.ep_pos):
        ev = PO.episode_views(sd.states, s0, D.idx[p0:p1], D.d[p0:p1], f_rec[p0:p1], md, b)
        vt = np.array([t for t, _, _ in ev], np.int64)
        vte = np.array([v.t_exch for _, _, v in ev], np.int64)
        lo, hi = a + warm, b + 1
        spells = PO.stale_spells(vt, vte, lo, b, tau)
        img, rd = PO.placebo_images(spells, lo, hi, rng, *pcfg["placebo_offset_range"], pcfg["placebo_max_redraws"])
        max_rd = max(max_rd, rd)
        wuf.append(spells)
        if img is None:                              # excluded from both windows and from the gate denominators
            excluded += 1
            img = np.empty((0, 2), np.int64)
            ana = np.empty((0, 2), np.int64)
        else:
            redraws += rd
            span += hi - lo
            ana = spells
        wu.append(ana)
        sp.append(ana)
        im.append(img)
        wp_ep = G.merge(img)
        if wp_ep.shape[0] != img.shape[0]:
            raise AssertionError("placebo images must stay maximal spells")
        wp.append(wp_ep)
        ex = np.unique(np.concatenate([spells[:, 0], img[:, 0], img[:, 1]])) if spells.size else np.array([], np.int64)
        extras.append([int(x) for x in ex if lo <= x <= b])
        views.append(ev)
        vts.append(vt)
        vtes.append(vte)
    cat = lambda xs: np.concatenate(xs) if xs else np.empty((0, 2), np.int64)
    W = Windows(views, np.concatenate(vts), np.concatenate(vtes), cat(wuf), cat(wu), G.merge(cat(wp)), cat(sp), cat(im),
                extras, span, redraws, max_rd, excluded)
    if np.any(np.diff(W.vt) < 0):
        raise AssertionError("view times must be sorted across the session")
    if (W.wu[:, 1] - W.wu[:, 0]).sum() != (W.wp[:, 1] - W.wp[:, 0]).sum():
        raise AssertionError("W_P must match W_U's duration exactly")
    return W


def overlap_us(x: np.ndarray, y: np.ndarray) -> int:
    """Total length of the intersection of two merged spell lists."""
    tot, i, j = 0, 0, 0
    while i < x.shape[0] and j < y.shape[0]:
        lo, hi = max(x[i, 0], y[j, 0]), min(x[i, 1], y[j, 1])
        tot += max(0, hi - lo)
        if x[i, 1] < y[j, 1]:
            i += 1
        else:
            j += 1
    return int(tot)


def window_sums(fa: dict, p5: np.ndarray, ok: np.ndarray, spells: np.ndarray, entry_us: int, rep: int) -> dict:
    """Pi5 and notional of the defined fills inside W^x = W + entry latency, and their distinct (replicate, episode, order
    id) keys (order ids restart in every episode)."""
    m = PO.members(spells, fa["t"] - entry_us) & ok if fa["t"].size else np.zeros(0, bool)
    return {"pi5": float(p5[m].sum()), "notional": float((fa["px"] * fa["qty"])[m].sum()),
            "orders": {(rep, int(e), int(o)) for e, o in zip(fa["ep"][m], fa["oid"][m])}, "fills": int(m.sum())}


# ------------------------------------------------------------------------------------------------- the run
def verify_schedules(e4: dict, days: list[str], reps: int) -> int:
    """Every schedule used must match the committed date-only hash list."""
    ref = json.loads(HASHES.read_text())["schedules"]
    n = 0
    for d in days:
        for cell in G.cells(e4):
            for role in G.SCHEDULE_ROLES:
                for r in G.replicates(e4, role):
                    if G.schedule_hash(G.schedule(e4, cell, d, role, r)) != ref[d][cell][role][str(r)]["sha256"]:
                        raise RuntimeError(f"schedule {d} {cell} {role} {r} differs from the committed hash list")
                    n += 1
    return n


E003_FROZEN_FILES = ("e003_models.json", "e003_gross_by_session.csv", "e003_forecast_by_session.csv", "e003_calibration.csv")


def e003_frozen_hashes() -> dict[str, str]:
    """The frozen E003 files used as references, verified against the hashes the E003 run wrote."""
    from lpx.provenance import sha256_file

    meta = json.loads((E003_OUT / "e003_meta.json").read_text())
    if meta["provenance"]["git_dirty"]:
        raise RuntimeError("the E003 run of record must come from a clean tree")
    out = {}
    for f in E003_FROZEN_FILES:
        h = sha256_file(E003_OUT / f)
        if meta["outputs_sha256"][f] != h:
            raise RuntimeError(f"results/e003/{f} differs from the file the E003 run wrote")
        out[f] = h
    return out


def e003_frozen() -> tuple[dict, pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    e003_frozen_hashes()
    return (json.loads((E003_OUT / "e003_models.json").read_text()),
            pl.read_csv(E003_OUT / "e003_gross_by_session.csv", infer_schema_length=None),
            pl.read_csv(E003_OUT / "e003_forecast_by_session.csv", infer_schema_length=None),
            pl.read_csv(E003_OUT / "e003_calibration.csv", infer_schema_length=None))


def check_models(day: str, models: dict, rv_med: float, rv_gate: float, frozen: dict) -> None:
    fz = frozen[day]
    for m, mod in models.items():
        if dataclasses.asdict(mod) != {k: (tuple(v) if isinstance(v, list) else v) for k, v in fz[f"h5s_{m}"].items()}:
            raise AssertionError(f"{day} {m}: walk-forward model differs from E003's")
    if (rv_med, rv_gate) != (fz["rv_60s_training_median"], fz["rv_gate"]):
        raise AssertionError(f"{day}: volatility gate differs from E003's")


def check_ref_forecasts(day: str, ft: pl.DataFrame, models: dict, frozen: dict, fc_tab: pl.DataFrame,
                        cal_tab: pl.DataFrame) -> np.ndarray:
    """REF = E003 M2 at 5 s: per row against the forecast recomputed from e003_models.json (this follows from
    check_models; the independent row-level check is the calibration deciles, which depend on every row's forecast and
    feature), against E003's frozen calibration table, and per aggregate against E003's forecast table (every column).
    Returns the REF forecasts of every row."""
    f = models["M2"].predict(ft)
    js = frozen[day]["h5s_M2"]
    again = F.LinearModel(tuple(js["regressors"]), tuple(js["lo"]), tuple(js["hi"]), tuple(js["coef"]),
                          tuple(js["trained_on"]), js["n_rows"]).predict(ft)
    if not np.array_equal(f, again):
        raise AssertionError(f"{day}: REF forecasts differ from E003's recomputation")
    rows, cal = E3.forecast_rows(day, ft, {5: models}, 5)
    for r in rows:
        e = fc_tab.filter((pl.col("day") == day) & (pl.col("model") == r["model"]) & (pl.col("horizon_s") == 5))
        if e.height != 1 or set(r) != set(e.columns) or any(not _same(e[k][0], v) for k, v in r.items()):
            raise AssertionError(f"{day} {r['model']}: forecast aggregates differ from E003's")
    fz = cal_tab.filter(pl.col("day") == day).sort("decile")
    if fz.height != len(cal) or set(cal[0]) != set(fz.columns) or any(
            not _same(fz[k][i], v) for i, c in enumerate(sorted(cal, key=lambda x: x["decile"])) for k, v in c.items()):
        raise AssertionError(f"{day}: REF calibration deciles differ from E003's")
    return f


def _same(a, b) -> bool:
    """Exact equality: None only equals None, NaN only NaN, numbers by value and sign of zero (the CSV schema may read an
    integer column as float), everything else by ==."""
    if a is None or b is None:
        return a is None and b is None
    num = (int, float, np.integer, np.floating)
    if isinstance(a, num) and isinstance(b, num) and not isinstance(a, bool) and not isinstance(b, bool):
        fa, fb = float(a), float(b)
        if math.isnan(fa) or math.isnan(fb):
            return math.isnan(fa) and math.isnan(fb)
        return fa == fb and math.copysign(1, fa) == math.copysign(1, fb) and (a == b)
    return type(a) is type(b) and a == b


def check_ref_policy(day: str, agg: dict, gross: pl.DataFrame) -> None:
    e = gross.filter((pl.col("day") == day) & (pl.col("policy") == agg["policy"]) & (pl.col("fill_model") == agg["fill_model"])
                     & (pl.col("latency") == agg["latency"]) & (pl.col("fee_rule") == "none"))
    if e.height != 1:
        raise AssertionError(f"{day} {agg['policy']}: no unique E003 row")
    missing = (set(agg) ^ (set(e.columns) - {"day", "split"}))
    if missing:
        raise AssertionError(f"{day} {agg['policy']}: columns differ from E003's: {sorted(missing)}")
    bad = [k for k, v in agg.items() if not _same(e[k][0], v)]
    if bad:
        raise AssertionError(f"{day} {agg['policy']} {agg['fill_model']}: REF differs from E003 in {bad}")


def run(days_override: list[str] | None = None) -> dict:
    from lpx.provenance import provenance, require_clean, sha256_file
    from lpx.research.e001 import verify_inputs

    t_run = time.time()
    e4, sc = load_cfg()
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    if "test" in e4["scope"]["session_sets"]:
        raise PermissionError("test sessions are sealed")
    if e4["scope"]["acceptance_git_commit"] != rc["dataset"]["acceptance_git_commit"]:
        raise RuntimeError("E004 and research_v1 name different acceptance runs")
    require_clean()
    if subprocess.run(["git", "status", "--porcelain", "--", str(SPEC), str(HASHES)], cwd=ROOT, capture_output=True,
                      text=True, check=True).stdout.strip():
        raise SystemExit("E004.md or the schedule-hash list has uncommitted changes")
    if OUT.exists() and any(OUT.iterdir()):
        raise FileExistsError("results/e004 is not empty; a rerun needs a DECISIONS.md entry and a fresh directory")
    cfgs = ["configs/e004_v1.toml", "configs/e003_v1.toml", "configs/research_v1.toml"]
    prov = {**provenance(cfgs), "spec_sha256": sha256_file(SPEC), "schedule_hashes_sha256": sha256_file(HASHES)}
    days = sorted(d for k in e4["scope"]["session_sets"] for d in rc["splits"][k])
    if set(days) & set(rc["splits"]["test"]):
        raise PermissionError("test sessions are sealed")
    n_sched = verify_schedules(e4, days, e4["seeds"]["eval_replicates"])
    base_inputs, receipts = verify_inputs(rc, days), E3.verify_receipt_inputs(sc, days)
    inputs = {**base_inputs, "sessions": {d: {**x, "tardis_trades_sha256": receipts[d]} for d, x in base_inputs["sessions"].items()}}
    frozen_models, frozen_gross, frozen_fc, frozen_cal = e003_frozen()
    prov["e003_reference_files_sha256"] = e003_frozen_hashes()
    k0 = e4["scope"]["min_training_sessions"]
    fc = sc["features"]
    reps = range(e4["seeds"]["eval_replicates"])
    tick = sc["instrument"]["tick"]

    # pass 1: E003 training rows and every cell's degraded training rows
    thin, train = {}, {c: {} for c in CELL_ORDER}
    for i, d in enumerate(days):
        st, tr, eps = E3.load_session(sc, d)
        ft = E3.features(sc, st, tr, eps)
        thin[d] = ft.filter(pl.col("eligible")).gather_every(fc["fit_thinning"])
        if i < len(days) - 1:                       # the last session never trains
            A = DG.from_frames(d, st, tr, eps, tick)
            for cell in CELL_ORDER:
                train[cell][d] = training_rows(e4, sc, A, ft, cell)
        print(f"{d}: training rows ({time.time() - t_run:.0f} s)", flush=True)

    frows, crows, drows, lrows, prows, wrows, inv = [], [], [], [], [], [], {"ref_policy_rows_checked": 0,
                                                                              "d0_view_identity_jobs": 0}
    eval_days = days[k0:] if days_override is None else [d for d in days[k0:] if d in days_override]
    for d in eval_days:
        i = days.index(d)
        t0 = time.time()
        models = E3.fit_models(sc, {x: thin[x] for x in days[:i]}, d, 5)
        tr_rows = pl.concat([thin[x] for x in days[:i]])
        rv_med = float(tr_rows.filter(pl.col("y_5s").is_not_nan() & pl.col("y_5s").is_not_null())["rv_60s"].median())
        rv_gate = sc["policies"]["p4_vol_gate_multiple"] * rv_med
        check_models(d, models, rv_med, rv_gate, frozen_models)
        st, tr, eps = E3.load_session(sc, d)
        ft = E3.features(sc, st, tr, eps)
        f_ref_all = check_ref_forecasts(d, ft, models, frozen_models, frozen_fc, frozen_cal)
        A = DG.from_frames(d, st, tr, eps, tick)
        el = ft["eligible"].to_numpy()
        y_k = ft["y_5s"].to_numpy()
        ref_mid, ref_spread = ft["mid_ticks"].to_numpy(), ft["spread"].to_numpy()
        m2 = models["M2"]

        # D0 through the participant path: identity
        D0, _, rec0, part0, b0, _ = cell_rows(e4, sc, A, "D0", "eval", 0, None)
        if not np.array_equal(part0["view_row"], A.rows) or not part0["has"].all():
            raise AssertionError("D0: j(k) must equal k")
        f_nv0 = m2.predict(xframe(part0)) * part0["has"]
        if not np.array_equal(f_nv0, f_ref_all) or any(not np.array_equal(part0[c], ft[c].to_numpy()) for c in F.REGRESSORS):
            raise AssertionError("D0: NV must equal REF bitwise")
        gap0 = DG.gap_flags(A, D0, D0.trade_ok, flow_window_us())
        tau_us = e4["indicators"]["tau_ms"] * 1000
        drows.append({"day": d, "cell": "D0", "replicate": 0, **D0.stats, "status": "synthetic",
                      "rows_eval": int(el.sum()), "rows_without_view": 0,
                      "age_ge_tau_share": float(np.mean(part0["age_us"][el] >= tau_us)),
                      "trade_gap_flag_share": float(np.mean(gap0[np.maximum(part0["pos"], 0)][el])),
                      **{f"bucket{b}_share": float(np.mean(b0[el] == b)) for b in range(5)}})
        fits = {cell: fit_cell(e4, sc, stack([train[cell][x] for x in days[:i]]), m2, cell, d) for cell in CELL_ORDER}
        for cell, fit in fits.items():
            for (tgt, ind), lam in fit.lam.items():
                g = fit.groups.get((tgt, ind))
                for gi, lv in enumerate(lam):
                    lrows.append({"day": d, "cell": cell, "target": tgt, "indicator": ind, "group": gi,
                                  "buckets": "all" if g is None else ",".join(str(b) for b in np.flatnonzero(g == gi)),
                                  "lambda": float(lv),
                                  "train_rows": fit.train_rows[tgt], "status": "stress test"})

        # forecast level, every cell and its 3 evaluation draws
        keep_views = {}
        for cell in CELL_ORDER:
            fit = fits[cell]
            acc = {tgt: {} for tgt in FC.TARGETS}
            for r in reps:
                D, iv, rec, part, b_ua, b_pl = cell_rows(e4, sc, A, cell, "eval", r, "placebo_eval")
                f_nv = m2.predict(xframe(part)) * part["has"]
                yv = FC.y_view(A, part, y_k)
                if cell in POLICY_CELLS:
                    keep_views[(cell, r)] = (D, m2.predict(pl.DataFrame({c: rec[c] for c in F.REGRESSORS})))
                mid_v = np.where(part["has"], part["view_mid_ticks"], ref_mid)
                spr_v = np.where(part["has"], part["spread"], ref_spread)
                for tgt, y in (("y_k", y_k), ("y_view", yv)):
                    fs = {"REF": (f_ref_all, ref_mid, ref_spread),
                          **{m: (f, mid_v, spr_v) for m, f in model_forecasts(fit, tgt, part, f_nv, b_ua, b_pl).items()}}
                    if cell == "D1_S" and tgt == "y_k":
                        keep_views[("lam", r)] = (fit.lam[(tgt, "UA")], fit.groups[(tgt, "UA")],
                                                  fit.lam[(tgt, "PL")], fit.groups[(tgt, "PL")])
                    if cell in ("D1_S1", "D1_S3"):
                        f1 = fits["D1_S"]
                        g = f1.groups[(tgt, "UA")]
                        fs["UA-lambda[D1_S]"] = (f1.lam[(tgt, "UA")][g[b_ua]] * f_nv, mid_v, spr_v)
                    for m, (f, mm, ss) in fs.items():
                        a = acc[tgt].setdefault(m, {"y": [], "f": [], "mid": [], "spr": [], "b": []})
                        a["y"].append(y[el])
                        a["f"].append(f[el])
                        a["mid"].append(mm[el])
                        a["spr"].append(ss[el])
                        a["b"].append(b_ua[el])
                drows.append({"day": d, "cell": cell, "replicate": r, **D.stats, "status": "synthetic",
                              "rows_eval": int(el.sum()), "rows_without_view": int((~part["has"][el]).sum()),
                              "age_ge_tau_share": float(np.mean(part["age_us"][el] >= tau_us)),
                              "placebo_bucket_share_nonfresh": float(np.mean(b_pl[el] > 0)),
                              **{f"bucket{b}_share": float(np.mean(b_ua[el] == b)) for b in range(n_buckets(e4, cell))}})
            for tgt, ms in acc.items():
                for m, a in ms.items():
                    y, f, mm, ss, bb = (np.concatenate(a[k]) for k in ("y", "f", "mid", "spr", "b"))
                    frows.append({"day": d, "cell": cell, "target": tgt, "model": m, **FC.skill(y, f, mm, ss),
                                  "replicates": len(a["y"]), "status": status_forecast(cell, m, tgt)})
                    if m in ("REF", "NV", "UA-lambda"):
                        for b in np.unique(bb):
                            s = bb == b
                            crows.append({"day": d, "cell": cell, "target": tgt, "model": m, "bucket": int(b),
                                          "rows": int((s & ~np.isnan(y)).sum()), "slope": FC.calibration_slope(f[s], y[s]),
                                          "status": status_forecast(cell, m, tgt)})
        # H4-0: UA-lambda trained on D1-S, applied to clean rows (target y_k)
        f1 = fits["D1_S"]
        g = f1.groups[("y_k", "UA")]
        f_h40 = f1.lam[("y_k", "UA")][g[b0]] * f_ref_all
        for m, f in (("REF", f_ref_all), ("UA-lambda[D1_S]", f_h40)):
            frows.append({"day": d, "cell": "D0", "target": "y_k", "model": m,
                          **FC.skill(y_k[el], f[el], ref_mid[el], ref_spread[el]), "replicates": 1,
                          "status": status_forecast("D0", m)})
        print(f"{d}: forecasts ({time.time() - t0:.0f} s)", flush=True)

        # policies
        states = to_states(st, tick)
        E3.attach(states, ft, models, rv_gate)
        sd = E3.SessionData(states, to_trades(tr, tick), eps, sc)
        h0 = state_hash(sd.states, sd.trades)
        prim = sc["e004_primary"]
        scen = [prim] + [tuple(x) for x in e4["analysis"]["descriptive_scenarios"]]
        entry = sc["latency"][prim[1]]["entry_us"]
        h_us = int(e4["analysis"]["markout_s"] * 1e6)
        ref = {}
        for base in BASES:
            for model, lat in scen:
                agg, fills = E3.simulate(sd, base, model, lat, None)
                check_ref_policy(d, agg, frozen_gross)
                inv["ref_policy_rows_checked"] += 1
                ref[(base, model)] = (agg, fills)
                prows.append({"day": d, "cell": "REF", "replicate": 0, "base": base, "variant": "REF", **agg,
                              "status": STATUS_POLICY_REF})
        v0 = [PO.episode_views(sd.states, s0, D0.idx[p0:p1], D0.d[p0:p1], f_ref_all[o0:o1], md_us(sc), b)
              for (a, b), (s0, s1), (p0, p1), (o0, o1) in zip(A.eps, A.ep_states, D0.ep_pos, _offsets(A))]
        for base in BASES:
            agg, fills = E3.simulate(sd, base, *prim, None, views=v0)
            if not _agg_equal(agg, ref[(base, prim[0])][0]) or fills != ref[(base, prim[0])][1]:
                raise AssertionError(f"{d} {base}: D0 through the view path differs from REF")
            inv["d0_view_identity_jobs"] += 1
        for cell in POLICY_CELLS:
            pooled = {}
            for r in reps:
                D, f_rec = keep_views[(cell, r)]
                W = windows(e4, sc, sd, A, D, f_rec, cell, r)
                hv = views_hash(W.views)
                stall_iv = G.schedule(e4, cell, d, "eval", r) + md_us(sc)       # scheduled stalls, participant clock
                for base in BASES:
                    jobs = [(prim, v) for v in VARIANTS]
                    if cell == "D1_E" and r == 0:
                        jobs += [(sx, v) for sx in scen[1:] for v in VARIANTS]
                    if cell == "D1_S" and base == "P3_M2":
                        jobs += [(prim, "N[UA-lambda]"), (prim, "N[PL-lambda]")]
                    for (model, lat), var in jobs:
                        ust = {}
                        bpol = E3.make_policy(base, sc["policies"], None)
                        if var == "U":
                            pol = PO.withdraw_when_stale(bpol, W.vt, W.vte, tau_us, W.wu_full, ust)
                        elif var == "P":
                            pol = PO.withdraw_in_windows(bpol, W.wp, ust)
                        elif var == "N":
                            pol = bpol
                        else:
                            lam_ua, g_ua, lam_pl, g_pl = keep_views[("lam", r)]
                            if var == "N[UA-lambda]":
                                pol = p3_rescaled(sc["policies"], lam_ua, g_ua, e4["indicators"]["age_bucket_edges_s"],
                                                  latest_age(W.vt, W.vte))
                            else:
                                Dp = DG.deliver(A, kind_of(e4, cell), G.schedule(e4, cell, d, "placebo_eval", r))
                                pt = Dp.d + md_us(sc)
                                pol = p3_rescaled(sc["policies"], lam_pl, g_pl, e4["indicators"]["age_bucket_edges_s"],
                                                  latest_age(pt, A.te[Dp.idx]))
                        agg, fills = E3.simulate(sd, base, model, lat, None, pol=pol, views=W.views, extras=W.extras)
                        fa = PO.fill_arrays(fills, tick, eps)
                        p5, ok = PO.pi5(fa, eps, sd.t_states, sd.mid, h_us)
                        prows.append({"day": d, "cell": cell, "replicate": r, "base": base, "variant": var, **agg,
                                      "pi5_usdt": float(p5[ok].sum()), "pi5_notional": float((fa["px"] * fa["qty"])[ok].sum()),
                                      "pi5_fills_excluded": int((~ok).sum()),
                                      "u_or_p_decisions": ust.get("decisions"), "u_or_p_withdrawn": ust.get("withdrawn"),
                                      "superseded_state_decisions": ust.get("superseded_state"),
                                      "status": STATUS_POLICY_DEG})
                        if var != "N":
                            continue
                        key = (base, model, lat)
                        P = pooled.setdefault(key, {"reps": 0, "span": 0, "wu": 0, "wp": 0, "ov": 0, "redraws": 0,
                                                    "max_redraws": 0, "excluded": 0, "wu_nostall": 0, "wp_install": 0,
                                                    "excluded_fills": 0, "n_notional": 0.0, "hours": 0.0,
                                                    **{w: {"pi5": 0.0, "notional": 0.0, "orders": set(), "fills": 0}
                                                       for w in ("U", "P", "U_stall", "P_stall", "U_nostall", "P_install")}})
                        st_hit = overlaps_any(W.wu_spells, stall_iv)
                        sel = {"U": W.wu, "P": W.wp, "U_stall": G.merge(W.wu_spells[st_hit]),
                               "P_stall": G.merge(W.wp_images[st_hit]), "U_nostall": G.merge(W.wu_spells[~st_hit])}
                        wp_in = _intersect(W.wp, stall_iv)
                        sel["P_install"] = wp_in
                        for w, spells in sel.items():
                            s = window_sums(fa, p5, ok, spells, entry, r)
                            P[w]["pi5"] += s["pi5"]
                            P[w]["notional"] += s["notional"]
                            P[w]["orders"] |= s["orders"]
                            P[w]["fills"] += s["fills"]
                        P["reps"] += 1
                        P["span"] += W.span_us
                        P["wu"] += int((W.wu[:, 1] - W.wu[:, 0]).sum())
                        P["wp"] += int((W.wp[:, 1] - W.wp[:, 0]).sum())
                        P["ov"] += overlap_us(W.wp, W.wu)
                        P["redraws"] += W.redraws
                        P["max_redraws"] = max(P["max_redraws"], W.max_redraws)
                        P["excluded"] += W.excluded
                        P["wu_nostall"] += int((sel["U_nostall"][:, 1] - sel["U_nostall"][:, 0]).sum())
                        P["wp_install"] += int((wp_in[:, 1] - wp_in[:, 0]).sum())
                        P["excluded_fills"] += int((~ok).sum())
                        P["n_notional"] += float((fa["px"] * fa["qty"])[ok].sum())
                        P["hours"] += agg["valid_hours"]
                if views_hash(W.views) != hv:
                    raise AssertionError("view states were mutated")
            for (base, model, lat), P in pooled.items():
                q = {w: (1e4 * P[w]["pi5"] / P[w]["notional"] if P[w]["notional"] > 0 else None) for w in P if isinstance(P[w], dict)}
                wrows.append({"day": d, "cell": cell, "base": base, "fill_model": model, "latency": lat, "replicates": P["reps"],
                              "q_U_bp": q["U"], "q_P_bp": q["P"],
                              "D_W_bp": q["P"] - q["U"] if None not in (q["P"], q["U"]) else None,
                              "orders_U": len(P["U"]["orders"]), "orders_P": len(P["P"]["orders"]),
                              "fills_U": P["U"]["fills"], "fills_P": P["P"]["fills"],
                              "notional_U": P["U"]["notional"], "notional_P": P["P"]["notional"],
                              "pi5_U_usdt": P["U"]["pi5"], "pi5_P_usdt": P["P"]["pi5"],
                              "n_notional_defined": P["n_notional"], "n_valid_hours": P["hours"],
                              "withdrawn_share": P["wu"] / P["span"], "wp_share": P["wp"] / P["span"],
                              "overlap_share_of_wp": P["ov"] / P["wp"] if P["wp"] else None,
                              "q_U_stall_bp": q["U_stall"], "q_P_stall_bp": q["P_stall"],
                              "D_W_stall_bp": q["P_stall"] - q["U_stall"] if None not in (q["P_stall"], q["U_stall"]) else None,
                              "orders_U_stall": len(P["U_stall"]["orders"]), "orders_P_stall": len(P["P_stall"]["orders"]),
                              "wu_time_share_nostall": P["wu_nostall"] / P["wu"] if P["wu"] else None,
                              "wu_fill_share_nostall": P["U_nostall"]["fills"] / P["U"]["fills"] if P["U"]["fills"] else None,
                              "wp_time_share_install": P["wp_install"] / P["wp"] if P["wp"] else None,
                              "wp_fill_share_install": P["P_install"]["fills"] / P["P"]["fills"] if P["P"]["fills"] else None,
                              "placebo_redraws": P["redraws"], "placebo_max_redraws": P["max_redraws"],
                              "episodes_excluded": P["excluded"], "fills_beyond_episode_end": P["excluded_fills"],
                              "status": STATUS_POLICY_DEG})
        if state_hash(sd.states, sd.trades) != h0:
            raise AssertionError("the exchange-side states or trades were mutated")
        print(f"{d}: policies ({time.time() - t0:.0f} s)", flush=True)

    end = provenance(cfgs)
    if (end["git_commit"], end["code_fingerprint"], end["git_dirty"]) != (prov["git_commit"], prov["code_fingerprint"], False):
        raise RuntimeError("source revision changed during the run")
    if (end["configs"] != prov["configs"] or sha256_file(SPEC) != prov["spec_sha256"]
            or sha256_file(HASHES) != prov["schedule_hashes_sha256"] or verify_inputs(rc, days) != base_inputs
            or e003_frozen_hashes() != prov["e003_reference_files_sha256"]
            or E3.verify_receipt_inputs(sc, days) != receipts):
        raise RuntimeError("specification, configuration, schedules or inputs changed during the run")
    OUT.mkdir(parents=True, exist_ok=True)
    gross = pl.DataFrame(prows, infer_schema_length=None)
    net = E3.fee_overlay(gross, sc["fees"]).with_columns(
        pl.when(pl.col("fee_schedule") == "vip0").then(pl.col("status"))
        .otherwise(pl.col("status") + pl.lit("; hypothetical fees")).alias("status"))
    tables = {"e004_forecast_by_session.csv": pl.DataFrame(frows, infer_schema_length=None),
              "e004_calibration.csv": pl.DataFrame(crows, infer_schema_length=None),
              "e004_degradation_by_session.csv": pl.DataFrame(drows, infer_schema_length=None),
              "e004_lambda.csv": pl.DataFrame(lrows, infer_schema_length=None),
              "e004_policy_gross_by_session.csv": gross, "e004_policy_net_by_session.csv": net,
              "e004_windows_by_session.csv": pl.DataFrame(wrows, infer_schema_length=None)}
    for name, t in tables.items():
        t.write_csv(OUT / name)
    meta = {"experiment": "E004", "status": {"D0/REF forecasts": "observed", "degraded forecasts": "stress test",
                                             "REF policies": STATUS_POLICY_REF, "degraded policies": STATUS_POLICY_DEG,
                                             "degradation statistics": "synthetic", "non-VIP0 fees": "hypothetical",
                                             "H4-0 forecasts": "observed (model trained under stress test)"},
            "sessions": days, "evaluation_sessions": eval_days, "schedules_verified": n_sched, "invariants": inv,
            "runtime_s": round(time.time() - t_run, 1),
            "run_at_utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"), "provenance": {**prov, "inputs": inputs},
            "outputs_sha256": {f: sha256_file(OUT / f) for f in tables}}
    tmp = OUT / "e004_meta.json.tmp"
    tmp.write_text(json.dumps(meta, indent=1))
    tmp.replace(OUT / "e004_meta.json")
    return meta


def _agg_equal(a: dict, b: dict) -> bool:
    return a.keys() == b.keys() and all(_same(a[k], v) if isinstance(v, float) else a[k] == v for k, v in b.items())


def overlaps_any(spells: np.ndarray, iv: np.ndarray) -> np.ndarray:
    """Whether each half-open spell intersects any interval of a merged list."""
    if spells.shape[0] == 0 or iv.shape[0] == 0:
        return np.zeros(spells.shape[0], bool)
    k = np.searchsorted(iv[:, 0], spells[:, 1], side="left") - 1     # last interval starting before the spell ends
    return (k >= 0) & (iv[np.maximum(k, 0), 1] > spells[:, 0])


def _offsets(A: DG.Arrays) -> list[tuple[int, int]]:
    """Each episode's slice of the in-episode row order (``A.rows``)."""
    out, o = [], 0
    for s0, s1 in A.ep_states:
        out.append((o, o + s1 - s0))
        o += s1 - s0
    return out


def _intersect(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    out, i, j = [], 0, 0
    while i < x.shape[0] and j < y.shape[0]:
        lo, hi = max(x[i, 0], y[j, 0]), min(x[i, 1], y[j, 1])
        if hi > lo:
            out.append((lo, hi))
        if x[i, 1] < y[j, 1]:
            i += 1
        else:
            j += 1
    return np.array(out, np.int64).reshape(-1, 2)


if __name__ == "__main__":
    run()
