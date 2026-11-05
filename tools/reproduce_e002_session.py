"""Acceptance check for E003 (E003.md section 9.2): at the current revision, with E002's configuration (every E003
engine option off), one E002 session reproduces the frozen ``results/e002/e002_gross_by_session.csv`` rows exactly.
Also reports, for that session, when the exchange daily cap first blocked (not recorded by the E002 run).

Status: modeled historical replay (a rerun of a frozen discovery computation; no new outcome).
Usage: uv run python tools/reproduce_e002_session.py 2025-08-01   (or: all)
"""

import json
import sys
import tomllib

import numpy as np
import polars as pl

from lpx.book import states as S
from lpx.data.normalize import normalized_path
from lpx.provenance import provenance, sha256_file
from lpx.research import e002 as E

FLOAT_TOL = 0.0    # exact: the engine keeps E002's arithmetic order, so every value must be bit-identical


def main(day: str) -> dict:
    cfg = tomllib.loads(E.CONFIG.read_text())
    meta = json.loads((E.OUT / "e002_meta.json").read_text())
    gross_path = E.OUT / "e002_gross_by_session.csv"
    if meta["outputs_sha256"]["e002_gross_by_session.csv"] != sha256_file(gross_path):
        raise RuntimeError("frozen gross table differs from the one the E002 run wrote")
    frozen = pl.read_csv(gross_path).filter(pl.col("day") == day)
    sym, tick = cfg["scope"]["symbol"], cfg["instrument"]["tick"]
    st = pl.read_parquet(S.STATES / sym / f"{day}.parquet")
    eps = E.episodes(S.load_windows(sym, day, "joint"), cfg["scope"]["min_episode_s"])
    st = st.filter(pl.col("valid_joint"))
    tr = pl.read_parquet(normalized_path("binance_vision", sym, "trades", day)).sort(["exch_us", "trade_id"])
    rows = pl.DataFrame(E.run_session(E.to_states(st, tick), E.to_trades(tr, tick), eps, cfg))
    key = ["policy", "fill_model", "latency"]
    j = frozen.join(rows, on=key, suffix="_now")
    mism = []
    for c in frozen.columns:
        if c in key + ["day", "split"]:
            continue
        if f"{c}_now" not in j.columns:          # a frozen column the rerun no longer produces is a mismatch
            mism.append((c, "missing from the rerun"))
            continue
        a, b = j[c].to_numpy(), j[f"{c}_now"].to_numpy()
        if a.dtype.kind in "fi":
            bad = ~((np.isnan(a.astype(float)) & np.isnan(b.astype(float)))
                    | np.isclose(a.astype(float), b.astype(float), rtol=FLOAT_TOL, atol=FLOAT_TOL))
        else:
            bad = a != b
        mism += [(c, *[r for r in j.filter(pl.Series(bad)).select(key).rows()][:3])] if bad.any() else []
    out = {"day": day, "scenarios_frozen": frozen.height, "scenarios_rerun": rows.height, "matched": j.height,
           "mismatched_columns": mism,
           "first_cap_bind_utc": {f"{r['policy']} {r['fill_model']} {r['latency']}":
                                  str(np.datetime64(r["first_cap_bind_us"], "us"))
                                  for r in rows.iter_rows(named=True) if r["first_cap_bind_us"] is not None}, "reproduced": not mism and j.height == frozen.height == rows.height,
           "provenance": provenance(["configs/e002_v1.toml"])}
    return out


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "2025-08-01"
    days = json.loads((E.OUT / "e002_meta.json").read_text())["sessions"] if arg == "all" else [arg]
    (E.OUT / "addenda").mkdir(exist_ok=True)
    results = []
    for day in days:
        res = main(day)
        results.append(res)
        print(day, "reproduced" if res["reproduced"] else f"MISMATCH {res['mismatched_columns']}", flush=True)
    name = "reproduction_all.json" if arg == "all" else f"reproduction_{arg}.json"
    (E.OUT / "addenda" / name).write_text(json.dumps(results if arg == "all" else results[0], indent=1, default=str))
    if not all(r["reproduced"] for r in results):
        raise SystemExit("E002 not reproduced")
