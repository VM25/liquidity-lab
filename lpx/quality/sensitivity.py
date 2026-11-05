"""Sensitivity of Test 001 coverage to its two judgment-based rules (one factor at a time, baseline held otherwise).

* ``proven_levels`` — how many of a snapshot's best levels per side are treated as proven (baseline 900 of a 1000-level
  REST response; 0 = the snapshot's full extent, i.e. no margin for vendor-merged buffered diffs).
* ``silence_s`` — a trade with no following depth event for this long cuts the window at the trade (baseline 1.0 s).

The variants are stress tests of modeling choices, not candidates for selection: the baseline stays the rule of record.
Outputs: results/acceptance_001/sensitivity.json and windows_sensitivity.csv (joint-layer windows per variant, used by
E001's inference-sensitivity runs).

Usage: ``uv run python -m lpx.quality.sensitivity``
"""

from __future__ import annotations

import datetime as dt
import json
import sys
import tomllib

import polars as pl

from lpx.book import engine as E
from lpx.data.acquire import ROOT
from lpx.data.normalize import normalized_path
from lpx.provenance import provenance, require_clean
from lpx.quality import checks as C
from lpx.quality.acceptance import OUT, day_bounds_us, instruments, missing_trade_intervals, validity_windows

PROVEN_VARIANTS = [0, 950, 900, 800, 600, 400]
SILENCE_VARIANTS = [0.5, 1.0, 2.0, 5.0]


def day_variants(sym: str, day: str, cfg: dict, inst: dict, min_s: float) -> tuple[list[dict], list[pl.DataFrame]]:
    book = pl.read_parquet(normalized_path("tardis", sym, "book", day))
    trades = pl.read_parquet(normalized_path("tardis", sym, "trades", day))
    ref = pl.read_parquet(normalized_path("binance_vision", sym, "trades", day))
    d0, d1 = day_bounds_us(day)
    _, missing = C.trade_audit(trades.filter(pl.col("exch_us").is_between(d0, d1)), ref)
    gaps_iv = missing_trade_intervals(missing, trades, (d0, d1))
    band = cfg["replay"]["grid_band"]
    grid = (ref["price"].min() * (1 - band), ref["price"].max() * (1 + band))
    base_pl, base_sil = cfg["replay"]["proven_levels"], cfg["rules"]["silence_s"]
    replays = {}

    def states(pl_):
        if pl_ not in replays:
            replays[pl_] = E.replay(book, tick=inst["tick_size"], grid_px=grid, n_levels=1,
                                    complete_below=cfg["replay"]["complete_below"], proven_levels=pl_).states
        return replays[pl_]

    rows, wins = [], []
    plan = [("proven_levels", v, v, base_sil) for v in PROVEN_VARIANTS] + \
           [("silence_s", v, base_pl, v) for v in SILENCE_VARIANTS]  # includes the baseline row
    for factor, value, pl_, sil in plan:
        st = states(pl_)
        flags = st["flags"].to_numpy()
        t_all = E.state_times(st)
        _, silent = C.trade_book_alignment(st, ref, sil)
        silent_iv = [(int(a), int(b)) for a, b in zip(silent["start_us"].to_list(), silent["end_us"].to_list())]
        _, joint_w = validity_windows(t_all, flags, silent_iv, gaps_iv, st["kind"].to_numpy())
        variant = f"{factor}={value:g}"
        baseline = pl_ == base_pl and sil == base_sil
        rows.append({"symbol": sym, "day": day, "factor": factor, "value": value, "variant": variant, "baseline": baseline,
                     "bbo_proven_fraction": float(((flags & E.BBO_INVALID) == 0).mean()),
                     "joint_hours": float(joint_w["duration_s"].sum() / 3600), "joint_windows": int(joint_w.height),
                     "hours_in_windows_ge_min": float(joint_w.filter(pl.col("duration_s") >= min_s)["duration_s"].sum() / 3600),
                     "silent_trades": len(silent_iv)})
        wins.append(joint_w.with_columns(pl.lit(sym).alias("symbol"), pl.lit(day).alias("day"), pl.lit(variant).alias("variant"),
                                         pl.lit(baseline).alias("baseline")))
    return rows, wins


def main() -> int:
    require_clean()
    cfg = tomllib.loads((ROOT / "configs" / "acceptance_001.toml").read_text())
    inst = instruments()
    rows, wins = [], []
    for sym in cfg["symbols"]:
        for day in sorted(cfg["tardis_days"] + cfg.get("extended_days", {}).get(sym, [])):
            r, w = day_variants(sym, day, cfg, inst[sym], cfg["rules"]["min_usable_window_s"])
            rows += r
            wins += w
            print(f"{sym} {day}: " + " ".join(f"{x['variant']}:{x['joint_hours']:.2f}h" for x in r), flush=True)
    out = {"run_at_utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
           "provenance": provenance(["configs/acceptance_001.toml", "configs/instruments.toml"]),
           "variants": rows}
    (OUT / "sensitivity.json").write_text(json.dumps(out, indent=1))
    pl.concat(wins, how="diagonal_relaxed").write_csv(OUT / "windows_sensitivity.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
