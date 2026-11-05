"""Stage 1 — verified book states for accepted sessions, and look-ahead-safe time alignment.

A *state* is the book after one depth event, stamped with the exchange-clock time ``t_exch_us`` (running maximum of
Binance ``E``, with the collector clock for snapshots — see ``engine.state_times``) and the collector receive time
``t_local_us`` (Tardis recorder, Tokyo). A state is valid on a layer
only if its exchange time lies inside one of that layer's accepted windows from Dataset Acceptance Test 001
(``results/acceptance_001/windows.csv``) *and* the record itself carries a proven, uncrossed touch (``bbo_ok``).
Nothing is interpolated: time between a window's last state and the next anchor is invalid by construction.

Two information clocks are supported by ``asof``:

* exchange time — the book as the exchange published it before an event (retrospective conditioning; a live
  participant could not have known it at that instant);
* receipt time (+ delay) — only states the collector had received before the event, optionally ``delay_us`` earlier
  (availability-safe for a participant at that recorder with that extra latency).

Usage: ``uv run python -m lpx.book.states SOLUSDT``  (writes data/derived/book_states/<SYM>/<day>.parquet)
"""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

import numpy as np
import polars as pl

from lpx.book import engine as E
from lpx.data.acquire import ROOT
from lpx.data.normalize import normalized_path

STATES = ROOT / "data" / "derived" / "book_states"
WINDOWS = ROOT / "results" / "acceptance_001" / "windows.csv"
LAYERS = ("book", "joint")


def load_windows(symbol: str, day: str, layer: str, source: str = "tardis") -> pl.DataFrame:
    """Accepted windows of one session; refuses a session that failed the Test 001 integrity checks."""
    w = pl.read_csv(WINDOWS).filter((pl.col("source") == source) & (pl.col("symbol") == symbol) & (pl.col("day") == day)
                                    & (pl.col("layer") == layer))
    if "integrity_status" in w.columns and w.height and (w["integrity_status"] != "accepted").any():
        raise PermissionError(f"{symbol} {day} failed the Test 001 integrity checks; its windows may not be used")
    return w.select("start_us", "end_us").sort("start_us")


def window_id(t: np.ndarray, w: pl.DataFrame) -> np.ndarray:
    """Index of the closed window [start_us, end_us] containing each time, -1 if none (windows must not overlap)."""
    if w.height == 0:
        return np.full(t.shape[0], -1, np.int64)
    s, e = w["start_us"].to_numpy(), w["end_us"].to_numpy()
    if np.any(s[1:] <= e[:-1]):
        raise ValueError("accepted windows overlap")
    i = np.searchsorted(s, t, side="right") - 1
    ok = i >= 0
    ok[ok] = t[ok] <= e[i[ok]]
    return np.where(ok, i, -1)


def in_windows(t: np.ndarray, w: pl.DataFrame) -> np.ndarray:
    return window_id(t, w) >= 0


def asof(t_select: np.ndarray, times_us: np.ndarray, windows: pl.DataFrame, *, state_ok: np.ndarray,
         t_window: np.ndarray | None = None, strict: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """State in force at each query time on a given information clock, and whether it is valid there.

    ``t_select``: per-state time on the information clock (exchange time, or receipt time + delay). The selected state
    is the last one with ``t_select < query`` (``strict``) or ``<=``; ``t_select`` must be non-decreasing in message
    order (raises otherwise). ``t_window``: per-state exchange time used for
    window membership (defaults to ``t_select``). Valid requires (i) the selected *record* is valid (``state_ok``) and
    (ii) the state and the query time lie in the same accepted window, so no query borrows a state across a gap, a
    silence cut or a window end. Returns (index or -1, valid).
    """
    t_window = t_select if t_window is None else t_window
    if np.any(np.diff(t_select) < 0):
        # a later state stamped earlier would let a query see content from after it (or a superseded state)
        raise ValueError("information clock must be non-decreasing in message order")
    idx = np.searchsorted(t_select, times_us, side="left" if strict else "right") - 1
    j = np.clip(idx, 0, None)
    ws = np.where(idx >= 0, window_id(t_window[j], windows), -1)
    valid = (idx >= 0) & state_ok[j] & (ws >= 0) & (ws == window_id(times_us, windows))
    return idx, valid


def session_states(symbol: str, day: str, n_levels: int = 10) -> pl.DataFrame:
    acc = tomllib.loads((ROOT / "configs" / "acceptance_001.toml").read_text())
    inst = tomllib.loads((ROOT / "configs" / "instruments.toml").read_text())["binance-spot"][symbol]
    book = pl.read_parquet(normalized_path("tardis", symbol, "book", day))
    ref = pl.read_parquet(normalized_path("binance_vision", symbol, "trades", day))
    band = acc["replay"]["grid_band"]
    r = E.replay(book, tick=inst["tick_size"], grid_px=(ref["price"].min() * (1 - band), ref["price"].max() * (1 + band)),
                 n_levels=n_levels, complete_below=acc["replay"]["complete_below"], proven_levels=acc["replay"]["proven_levels"])
    st = r.states
    t = E.state_times(st)
    cols = {f"valid_{layer}": in_windows(t, load_windows(symbol, day, layer)) for layer in LAYERS}
    lv = [f"{s}{i}_{k}" for i in range(1, n_levels + 1) for s in ("bid", "ask") for k in ("px", "qty")]
    out = st.select(
        pl.Series("t_exch_us", t), pl.col("local_us").alias("t_local_us"), "kind", "flags", *lv,
    ).with_columns(
        (pl.col("bid1_px").is_not_nan() & pl.col("ask1_px").is_not_nan() & (pl.col("bid1_px") < pl.col("ask1_px"))
         & ((pl.col("flags") & E.BBO_INVALID) == 0)).fill_null(False).alias("bbo_ok"),
        **{k: pl.Series(v) for k, v in cols.items()})
    # windows are built from valid messages, so every state inside one must itself carry a proven, uncrossed touch
    bad = out.filter(pl.col("valid_book") & ~pl.col("bbo_ok"))
    if bad.height:
        raise AssertionError(f"{symbol} {day}: {bad.height} states inside accepted windows without a proven uncrossed touch")
    if out["t_local_us"].null_count():
        raise AssertionError(f"{symbol} {day}: states without a receipt time")
    # clock invariants that asof() relies on; a session violating them must fail loudly, not mis-select
    te, tl = out["t_exch_us"].to_numpy(), out["t_local_us"].to_numpy()
    if np.any(np.diff(te) < 0) or np.any(np.diff(tl) < 0):
        raise AssertionError(f"{symbol} {day}: exchange or receipt clock decreases in message order")
    if np.any(tl < te):
        raise AssertionError(f"{symbol} {day}: receipt time precedes exchange time")
    # windows never span a vendor reconnect: the message before each resync snapshot ends its window
    for layer in LAYERS:
        w = load_windows(symbol, day, layer)
        wid = window_id(te, w)
        m = np.flatnonzero((out["kind"].to_numpy() == 0) & (np.arange(out.height) > 0))
        if np.any((wid[m] >= 0) & (wid[m] == wid[m - 1])):
            raise AssertionError(f"{symbol} {day}: a {layer} window spans a vendor reconnect")
    return out


def export(symbol: str, days: list[str]) -> list[Path]:
    from lpx.provenance import provenance, require_clean, sha256_file

    require_clean()
    prov = provenance(["configs/acceptance_001.toml", "configs/instruments.toml"])
    prov["windows_csv_sha256"] = sha256_file(WINDOWS)
    STATES.joinpath(symbol).mkdir(parents=True, exist_ok=True)
    out = []
    for day in days:
        df = session_states(symbol, day)
        p = STATES / symbol / f"{day}.parquet"
        meta = {"symbol": symbol, "day": day, "provenance": prov, "windows": str(WINDOWS.relative_to(ROOT)),
                "status": "observed (replayed from vendor capture; validity per Acceptance Test 001)"}
        df.write_parquet(p, compression="zstd", metadata={"lpx": json.dumps(meta)})
        print(f"{symbol} {day}: {df.height:,} states, valid_joint {df['valid_joint'].mean():.4f}", flush=True)
        out.append(p)
    return out


if __name__ == "__main__":
    sym = sys.argv[1] if len(sys.argv) > 1 else "SOLUSDT"
    rcfg = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())["splits"]
    export(sym, sorted(rcfg["train"] + rcfg["validation"] + rcfg["test"]))
