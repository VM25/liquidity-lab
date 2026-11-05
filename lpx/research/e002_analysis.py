"""E002 pre-registered analysis (configs/e002_v1.toml [analysis]; docs/experiments/E002.md section 7 and its pre-run
amendments).

Input: the per-session net table written by ``lpx.research.e002``. Sessions are the unit; intervals are 95% percentile
intervals of a session bootstrap. Only the default fee schedule and the three primary fill models enter the H2 decision;
everything else is descriptive. A session without fills has no bp outcome; it is reported, never imputed, and a scenario
enters the decision only if its outcome is defined in at least ``min_defined_sessions`` sessions.

Usage (after ``python -m lpx.research.e002``):
    uv run python -m lpx.research.e002_analysis
"""

from __future__ import annotations

import itertools
import json
import tomllib

import numpy as np
import polars as pl

OUTCOME = "net_bp_per_notional"


def boot_mean(x: np.ndarray, n: int, rng: np.random.Generator) -> tuple[float, float, float]:
    x = x[~np.isnan(x)]
    if x.size < 2:
        return (float(x.mean()) if x.size else float("nan"), float("nan"), float("nan"))
    m = x[rng.integers(0, x.size, size=(n, x.size))].mean(axis=1)
    return float(x.mean()), float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def _vals(g: pl.DataFrame, col: str) -> np.ndarray:
    return g.sort("day")[col].cast(pl.Float64).fill_null(float("nan")).to_numpy()


def scenario_table(net: pl.DataFrame, fee: str, models: list[str], n: int, rng: np.random.Generator,
                   min_defined: int = 0) -> pl.DataFrame:
    rows = []
    sub = net.filter((pl.col("fee_schedule") == fee) & pl.col("fill_model").is_in(models) & pl.col("policy").is_in(["P0", "P1"]))
    for (pol, model, lat), g in sub.group_by(["policy", "fill_model", "latency"], maintain_order=True):
        x = _vals(g, OUTCOME)
        mean, lo, hi = boot_mean(x, n, rng)
        k = int((~np.isnan(x)).sum())
        rows.append({"policy": pol, "fill_model": model, "latency": lat, "sessions": g.height, "sessions_defined": k,
                     "eligible": k >= min_defined, "mean": mean, "ci95_lo": lo, "ci95_hi": hi})
    return pl.DataFrame(rows).sort(["policy", "fill_model", "latency"])


def paired_table(net: pl.DataFrame, fee: str, models: list[str], n: int, rng: np.random.Generator,
                 min_defined: int = 0) -> pl.DataFrame:
    """P1 - P0 on the same session, fill model and latency (sessions where both outcomes are defined)."""
    sub = net.filter((pl.col("fee_schedule") == fee) & pl.col("fill_model").is_in(models))
    p0 = sub.filter(pl.col("policy") == "P0").select("day", "fill_model", "latency", pl.col(OUTCOME).alias("p0"))
    p1 = sub.filter(pl.col("policy") == "P1").select("day", "fill_model", "latency", pl.col(OUTCOME).alias("p1"))
    j = p0.join(p1, on=["day", "fill_model", "latency"]).with_columns((pl.col("p1") - pl.col("p0")).alias("d"))
    rows = []
    for (model, lat), g in j.group_by(["fill_model", "latency"], maintain_order=True):
        x = _vals(g, "d")
        mean, lo, hi = boot_mean(x, n, rng)
        k = int((~np.isnan(x)).sum())
        rows.append({"fill_model": model, "latency": lat, "sessions": g.height, "sessions_defined": k,
                     "eligible": k >= min_defined, "mean_p1_minus_p0": mean, "ci95_lo": lo, "ci95_hi": hi})
    return pl.DataFrame(rows).sort(["fill_model", "latency"])


def model_pairs_table(net: pl.DataFrame, fee: str, models: list[str], n: int, rng: np.random.Generator,
                      min_defined: int = 0) -> pl.DataFrame:
    """Paired fill-model differences (b - a for each ordered pair in ``models``) per policy and latency, on the same
    sessions — the materiality test."""
    sub = net.filter((pl.col("fee_schedule") == fee) & pl.col("policy").is_in(["P0", "P1"]))
    rows = []
    for a, b in itertools.combinations(models, 2):
        A = sub.filter(pl.col("fill_model") == a).select("day", "policy", "latency", pl.col(OUTCOME).alias("a"))
        B = sub.filter(pl.col("fill_model") == b).select("day", "policy", "latency", pl.col(OUTCOME).alias("b"))
        j = A.join(B, on=["day", "policy", "latency"]).with_columns((pl.col("b") - pl.col("a")).alias("d"))
        for (pol, lat), g in j.group_by(["policy", "latency"], maintain_order=True):
            x = _vals(g, "d")
            mean, lo, hi = boot_mean(x, n, rng)
            k = int((~np.isnan(x)).sum())
            rows.append({"policy": pol, "latency": lat, "pair": f"{b} - {a}", "sessions_defined": k,
                         "eligible": k >= min_defined, "mean": mean, "ci95_lo": lo, "ci95_hi": hi})
    return pl.DataFrame(rows).sort(["policy", "latency", "pair"])


def opposite_signs(t: pl.DataFrame, lo: str = "ci95_lo", hi: str = "ci95_hi") -> list[tuple]:
    t = t.filter(pl.col("eligible")) if "eligible" in t.columns else t
    pos = [r for r in t.iter_rows(named=True) if r[lo] > 0]
    neg = [r for r in t.iter_rows(named=True) if r[hi] < 0]
    return [((a["fill_model"], a["latency"]), (b["fill_model"], b["latency"])) for a, b in itertools.product(pos, neg)]


def h2(net: pl.DataFrame, cfg: dict) -> dict:
    a = cfg["analysis"]
    net = net.sort(["policy", "fill_model", "latency", "fee_schedule", "day"])  # intervals invariant to input row order
    rng = np.random.default_rng(a["seed"])
    fee = cfg["fees"]["default"]
    models = cfg["fill_models"]["primary"]
    k = a.get("min_defined_sessions", 0)
    st = scenario_table(net, fee, models, a["bootstrap_resamples"], rng, k)
    pt = paired_table(net, fee, models, a["bootstrap_resamples"], rng, k)
    mp = model_pairs_table(net, fee, models, a["bootstrap_resamples"], rng, k)
    cond_a = {pol: opposite_signs(st.filter(pl.col("policy") == pol)) for pol in ("P0", "P1")}
    cond_b = opposite_signs(pt)
    mat = mp.with_columns((pl.col("eligible") & (pl.col("mean").abs() >= a["materiality_bp"])
                           & ((pl.col("ci95_lo") > 0) | (pl.col("ci95_hi") < 0))).alias("material"))
    ranges = [{"policy": pol, "latency": lat, "range_bp_across_fill_models": float(g["mean"].max() - g["mean"].min())}
              for (pol, lat), g in st.group_by(["policy", "latency"], maintain_order=True)]
    return {"fee_schedule": fee, "min_defined_sessions": k, "scenario_table": st.to_dicts(), "paired_table": pt.to_dicts(),
            "condition_a_sign_reversal": {p: [list(map(list, x)) for x in v] for p, v in cond_a.items()},
            "condition_b_ranking_reversal": [list(map(list, x)) for x in cond_b],
            "h2_supported_on_discovery": bool(any(cond_a.values()) or cond_b),
            "materiality": mat.to_dicts(), "material_sensitivity": bool(mat["material"].any()),
            "descriptive_range_of_means": ranges}


def _no_nan(x):
    """NaN (undefined mean or interval) -> null, so the output is valid JSON."""
    if isinstance(x, float) and x != x:
        return None
    if isinstance(x, dict):
        return {k: _no_nan(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_no_nan(v) for v in x]
    return x


def run() -> dict:
    from lpx.data.acquire import ROOT
    from lpx.provenance import code_fingerprint, provenance, require_clean, sha256_file
    from lpx.research.e002 import CONFIG, OUT

    require_clean()
    cfg = tomllib.loads(CONFIG.read_text())
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    meta = json.loads((OUT / "e002_meta.json").read_text())
    pv = meta["provenance"]
    allowed = {d for k in cfg["scope"]["session_sets"] for d in rc["splits"][k]}
    if set(meta["sessions"]) - allowed or set(rc["splits"]["test"]) & set(meta["sessions"]):
        raise PermissionError("the E002 outputs contain sessions outside the discovery sets")
    if pv["git_dirty"]:
        raise RuntimeError("the E002 run was made from a dirty tree and cannot be cited")
    if pv["configs"]["configs/e002_v1.toml"] != sha256_file(CONFIG):
        raise RuntimeError("configs/e002_v1.toml changed after the run")
    if pv["spec_sha256"] != sha256_file(ROOT / "docs" / "experiments" / "E002.md"):
        raise RuntimeError("docs/experiments/E002.md changed after the run")
    if pv["configs"]["configs/research_v1.toml"] != sha256_file(ROOT / "configs" / "research_v1.toml"):
        raise RuntimeError("configs/research_v1.toml (session splits) changed after the run")
    if pv["code_fingerprint"] != code_fingerprint():
        raise RuntimeError("code changed after the run")
    if meta["outputs_sha256"]["e002_net_by_session.csv"] != sha256_file(OUT / "e002_net_by_session.csv"):
        raise RuntimeError("net table differs from the one the run wrote")
    net = pl.read_csv(OUT / "e002_net_by_session.csv")
    if set(net["day"].unique()) != set(meta["sessions"]):
        raise RuntimeError("net table sessions differ from the run metadata")
    res = h2(net, cfg)
    res["provenance"] = {**provenance(["configs/e002_v1.toml"]), "run_git_commit": pv["git_commit"],
                         "net_table_sha256": sha256_file(OUT / "e002_net_by_session.csv")}
    (OUT / "e002_h2.json").write_text(json.dumps(_no_nan(res), indent=1, allow_nan=False))
    return res


if __name__ == "__main__":
    run()
