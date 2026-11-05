"""Canonical normalized schemas (DATA_SPEC "canonical input contract").

Normalization only renames, re-types and re-orders what the source supplies; it never fills a missing
field. Timestamps are integer microseconds since the Unix epoch (UTC). A null timestamp means the
source did not observe that clock for that event.

Book events (one row per price level carried by a message):
    msg      int64  message ordinal within the normalized file; rows of one message apply atomically
    kind     int8   SNAPSHOT (full side reset) or DIFF (absolute level sizes)
    exch_us  int64? exchange event time (Binance depth ``E``); null for REST snapshots (no exchange time)
    local_us int64? capture receipt time at the collector; null when the source did not record it
    seq_first, seq_last int64? exchange update-id range (Binance ``U``/``u``; snapshot ``lastUpdateId``)
    side     int8   BID=+1 / ASK=-1
    price    float64
    qty      float64 absolute resting size at that level after the message (0 = level removed)

Trades:
    trade_id int64  exchange trade id
    exch_us  int64  exchange trade time (Binance ``T``)
    local_us int64? capture receipt time, when recorded
    price, qty float64
    aggressor int8  +1 buyer-initiated, -1 seller-initiated
    aggressor_status str  "exchange_flag" when derived from the exchange's is-buyer-maker flag
"""

from __future__ import annotations

import polars as pl

SNAPSHOT: int = 0
DIFF: int = 1
BID: int = 1
ASK: int = -1

BOOK_SCHEMA = {
    "msg": pl.Int64,
    "kind": pl.Int8,
    "exch_us": pl.Int64,
    "local_us": pl.Int64,
    "seq_first": pl.Int64,
    "seq_last": pl.Int64,
    "side": pl.Int8,
    "price": pl.Float64,
    "qty": pl.Float64,
}

TRADE_SCHEMA = {
    "trade_id": pl.Int64,
    "exch_us": pl.Int64,
    "local_us": pl.Int64,
    "price": pl.Float64,
    "qty": pl.Float64,
    "aggressor": pl.Int8,
    "aggressor_status": pl.String,
}


def conform(df: pl.DataFrame, schema: dict) -> pl.DataFrame:
    """Select and cast to ``schema`` exactly; missing columns raise (never silently created)."""
    missing = [c for c in schema if c not in df.columns]
    if missing:
        raise ValueError(f"normalized frame missing columns {missing}")
    return df.select([pl.col(c).cast(t, strict=True) for c, t in schema.items()])
