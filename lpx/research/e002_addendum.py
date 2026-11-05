"""E002 exploratory addendum: the daily order-cap confound (declared 2026-10-22 in DECISIONS.md before computation).

In E002, P0 cancel-replaced on every touch change and reached the exchange cap of 200,000 orders/day in 6 of 90
optimistic scenario-sessions; after that it stopped quoting for the rest of the day, at a time that differed by fill
model. This addendum recomputes the pre-registered E002 tables (VIP0) on the sessions where no P0/P1 scenario under a
primary fill model reached the cap, so the fill-model comparisons are free of it. It reads the frozen net table (hash
checked against the run metadata) and changes nothing in E002's frozen results. Descriptive; no decision.

Status: modeled historical replay. Usage: uv run python -m lpx.research.e002_addendum
"""

from __future__ import annotations

import json
import tomllib

import numpy as np
import polars as pl

from lpx.provenance import provenance, sha256_file
from lpx.research import e002_analysis as A
from lpx.research.e002 import CONFIG, OUT


def cap_free(net: pl.DataFrame, cfg: dict) -> dict:
    primary = cfg["fill_models"]["primary"]
    hit = net.filter(pl.col("fill_model").is_in(primary) & pl.col("policy").is_in(["P0", "P1"])
                     & (pl.col("rate_limited_daily") > 0))
    capped = sorted(hit["day"].unique().to_list())
    sub = net.filter(~pl.col("day").is_in(capped)).sort(["policy", "fill_model", "latency", "fee_schedule", "day"])
    a = cfg["analysis"]
    rng = np.random.default_rng(a["seed"])
    fee, n = cfg["fees"]["default"], a["bootstrap_resamples"]
    k = sub["day"].n_unique()
    return {"status": "exploratory addendum (declared before computation); modeled historical replay",
            "excluded_sessions": capped, "sessions": k,
            "capped_scenarios": hit.filter(pl.col("fee_schedule") == fee).select("day", "policy", "fill_model", "latency")
            .sort("day", "policy", "fill_model", "latency").rows(),
            "scenario_table": A.scenario_table(sub, fee, primary, n, rng).to_dicts(),
            "paired_p1_minus_p0": A.paired_table(sub, fee, primary, n, rng).to_dicts(),
            "fill_model_pairs": A.model_pairs_table(sub, fee, primary, n, rng).to_dicts()}


def run() -> dict:
    cfg = tomllib.loads(CONFIG.read_text())
    meta = json.loads((OUT / "e002_meta.json").read_text())
    path = OUT / "e002_net_by_session.csv"
    if meta["outputs_sha256"]["e002_net_by_session.csv"] != sha256_file(path):
        raise RuntimeError("net table differs from the one the E002 run wrote")
    res = cap_free(pl.read_csv(path), cfg)
    res["provenance"] = {**provenance(["configs/e002_v1.toml"]), "e002_run_git_commit": meta["provenance"]["git_commit"],
                         "net_table_sha256": sha256_file(path)}
    (OUT / "addenda").mkdir(exist_ok=True)
    (OUT / "addenda" / "cap_free_subset.json").write_text(json.dumps(A._no_nan(res), indent=1, allow_nan=False))
    return res


if __name__ == "__main__":
    r = run()
    print("excluded:", r["excluded_sessions"], "sessions kept:", r["sessions"])
    for row in r["fill_model_pairs"]:
        print(row["policy"], row["latency"], row["pair"], round(row["mean"], 3), round(row["ci95_lo"], 3), round(row["ci95_hi"], 3))
