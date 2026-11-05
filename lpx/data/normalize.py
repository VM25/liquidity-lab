"""Source adapters: raw vendor/exchange files -> canonical normalized Parquet (see ``schema``).

Adapters respect each feed's own semantics and never invent fields:

* Tardis ``incremental_book_L2`` (Binance spot): rows are in capture order; consecutive rows sharing
  (``is_snapshot``, ``timestamp``, ``local_timestamp``) form one message. Snapshot rows carry the collector's
  receipt time in both timestamp columns (REST snapshots have no exchange time), so ``exch_us`` is null for them.
  Update ids are not published, so ``seq_*`` are null.
* crypto-lob-stream (Hugging Face) ``depth`` + ``snapshots``: one message per (U, u); snapshots carry ``lastUpdateId``.
  Messages are interleaved in exchange-sequence order: a diff with ``u <= L`` precedes snapshot ``L``; a diff with
  ``u >= L+1`` follows it (Binance local-book procedure). ``timestamp_ms`` is the collector's receive clock on depth
  and snapshot rows (verified: several distinct depth events share one millisecond, and depth rows trail the
  same events' exchange times by ~0.1-1 s), but exchange trade time truncated to ms on trade rows (verified
  against the exchange's own trade archive).
* data.binance.vision spot ``trades``: headerless CSV; ``time`` in microseconds for 2025+ files (asserted).
"""

from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import polars as pl

from lpx.data.acquire import RAW, ROOT, load_manifest
from lpx.data.schema import ASK, BID, BOOK_SCHEMA, DIFF, SNAPSHOT, TRADE_SCHEMA, conform

NORM = ROOT / "data" / "normalized"
ADAPTER_VERSION = "normalize/2"
VENUE = "binance-spot"

_side = pl.when(pl.col("side") == "bid").then(pl.lit(BID)).when(pl.col("side") == "ask").then(pl.lit(ASK))


# --------------------------------------------------------------------------- Tardis


def tardis_book(path: Path) -> pl.DataFrame:
    raw = pl.read_csv(
        path,
        columns=["timestamp", "local_timestamp", "is_snapshot", "side", "price", "amount"],
        schema_overrides={"timestamp": pl.Int64, "local_timestamp": pl.Int64, "is_snapshot": pl.Boolean,
                          "price": pl.Float64, "amount": pl.Float64},
    )
    if raw["side"].is_in(["bid", "ask"]).not_().any():
        raise ValueError(f"{path}: unexpected side labels {raw['side'].unique().to_list()}")
    snap = raw.filter(pl.col("is_snapshot"))
    if (snap["timestamp"] != snap["local_timestamp"]).any():
        raise ValueError(f"{path}: snapshot rows with distinct exchange timestamp; adapter assumption violated")
    key_change = (
        (pl.col("is_snapshot") != pl.col("is_snapshot").shift(1))
        | (pl.col("timestamp") != pl.col("timestamp").shift(1))
        | (pl.col("local_timestamp") != pl.col("local_timestamp").shift(1))
    ).fill_null(True)
    df = raw.with_columns(
        (key_change.cum_sum() - 1).cast(pl.Int64).alias("msg"),
        pl.when(pl.col("is_snapshot")).then(pl.lit(SNAPSHOT)).otherwise(pl.lit(DIFF)).alias("kind"),
        pl.when(pl.col("is_snapshot")).then(None).otherwise(pl.col("timestamp")).alias("exch_us"),
        pl.col("local_timestamp").alias("local_us"),
        pl.lit(None, pl.Int64).alias("seq_first"),
        pl.lit(None, pl.Int64).alias("seq_last"),
        _side.alias("side"),
        pl.col("amount").alias("qty"),
    )
    return conform(df, BOOK_SCHEMA)


def tardis_trades(path: Path) -> pl.DataFrame:
    raw = pl.read_csv(
        path,
        columns=["timestamp", "local_timestamp", "id", "side", "price", "amount"],
        schema_overrides={"timestamp": pl.Int64, "local_timestamp": pl.Int64, "id": pl.Int64,
                          "price": pl.Float64, "amount": pl.Float64},
    )
    if raw["side"].is_in(["buy", "sell"]).not_().any():
        raise ValueError(f"{path}: unexpected trade side labels {raw['side'].unique().to_list()}")
    df = raw.with_columns(
        pl.col("id").alias("trade_id"),
        pl.col("timestamp").alias("exch_us"),
        pl.col("local_timestamp").alias("local_us"),
        pl.col("amount").alias("qty"),
        pl.when(pl.col("side") == "buy").then(pl.lit(1)).otherwise(pl.lit(-1)).alias("aggressor"),
        pl.lit("exchange_flag").alias("aggressor_status"),
    )
    return conform(df, TRADE_SCHEMA)


# --------------------------------------------------------------------------- crypto-lob-stream (HF)


def hf_book(depth_path: Path, snapshot_path: Path) -> pl.DataFrame:
    d = pl.read_parquet(depth_path, columns=["timestamp_ms", "side", "price", "quantity", "first_update_id", "last_update_id"])
    d = d.with_row_index("_row").with_columns(
        pl.lit(DIFF).alias("kind"),
        pl.lit(None, pl.Int64).alias("exch_us"),
        (pl.col("timestamp_ms") * 1000).alias("local_us"),
        pl.col("first_update_id").alias("seq_first"),
        pl.col("last_update_id").alias("seq_last"),
        (pl.col("last_update_id") * 2).alias("_key"),
    )
    s = pl.read_parquet(snapshot_path, columns=["timestamp_ms", "side", "price", "quantity", "last_update_id"])
    s = s.with_row_index("_row").with_columns(
        pl.lit(SNAPSHOT).alias("kind"),
        pl.lit(None, pl.Int64).alias("exch_us"),
        (pl.col("timestamp_ms") * 1000).alias("local_us"),
        pl.lit(None, pl.Int64).alias("seq_first"),
        pl.col("last_update_id").alias("seq_last"),
        (pl.col("last_update_id") * 2 + 1).alias("_key"),
    )
    cols = ["_key", "_row", "kind", "exch_us", "local_us", "seq_first", "seq_last", "side", "price", "quantity"]
    both = pl.concat([d.select(cols), s.select(cols)]).sort(["_key", "kind", "_row"], maintain_order=True)
    # one message per (kind, key): a diff is keyed by its unique (U,u) via u; a snapshot by its lastUpdateId
    new_msg = ((pl.col("_key") != pl.col("_key").shift(1)) | (pl.col("kind") != pl.col("kind").shift(1))).fill_null(True)
    df = both.with_columns(
        (new_msg.cum_sum() - 1).cast(pl.Int64).alias("msg"),
        _side.alias("side"),
        pl.col("quantity").alias("qty"),
    )
    return conform(df, BOOK_SCHEMA)


def hf_trades(path: Path) -> pl.DataFrame:
    raw = pl.read_parquet(path, columns=["timestamp_ms", "trade_id", "price", "quantity", "buyer_maker"])
    df = raw.sort("trade_id").with_columns(
        (pl.col("timestamp_ms") * 1000).alias("exch_us"),
        pl.lit(None, pl.Int64).alias("local_us"),
        pl.col("quantity").alias("qty"),
        pl.when(pl.col("buyer_maker")).then(pl.lit(-1)).otherwise(pl.lit(1)).alias("aggressor"),
        pl.lit("exchange_flag").alias("aggressor_status"),
    )
    return conform(df, TRADE_SCHEMA)


# --------------------------------------------------------------------------- data.binance.vision


def binance_vision_trades(path: Path) -> pl.DataFrame:
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if len(names) != 1:
            raise ValueError(f"{path}: expected one member, found {names}")
        payload = z.read(names[0])
    raw = pl.read_csv(
        io.BytesIO(payload), has_header=False,
        new_columns=["trade_id", "price", "qty", "quote_qty", "time", "is_buyer_maker", "is_best_match"],
        schema_overrides={"trade_id": pl.Int64, "price": pl.Float64, "qty": pl.Float64, "time": pl.Int64},
    )
    if raw["time"].min() < 10**15:  # microseconds since epoch are >= 1e15 after 2001
        raise ValueError(f"{path}: 'time' is not in microseconds; adapter assumption violated")
    df = raw.with_columns(
        pl.col("time").alias("exch_us"),
        pl.lit(None, pl.Int64).alias("local_us"),
        pl.when(pl.col("is_buyer_maker")).then(pl.lit(-1)).otherwise(pl.lit(1)).alias("aggressor"),
        pl.lit("exchange_flag").alias("aggressor_status"),
    )
    return conform(df, TRADE_SCHEMA)


# --------------------------------------------------------------------------- writing


def write_normalized(df: pl.DataFrame, dest: Path, *, source: str, symbol: str, table: str, period: str,
                     raw_rel_paths: list[str], notes: str = "") -> Path:
    manifest = load_manifest()
    meta = {
        "source": source, "venue": VENUE, "symbol": symbol, "instrument_type": "spot", "table": table,
        "period": period, "adapter_version": ADAPTER_VERSION, "notes": notes,
        "raw_files": [{"rel_path": p, "sha256": manifest[p]["sha256"], "url": manifest[p]["url"]} for p in raw_rel_paths],
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".tmp")
    df.write_parquet(tmp, compression="zstd", statistics=True, metadata={"lpx": json.dumps(meta, sort_keys=True)})
    tmp.replace(dest)
    return dest


def read_meta(path: Path) -> dict:
    import pyarrow.parquet as pq

    return json.loads(pq.read_metadata(path).metadata[b"lpx"])


def normalized_path(source: str, symbol: str, table: str, period: str) -> Path:
    return NORM / source / VENUE / symbol / f"{table}_{period}.parquet"


def run_all(force: bool = False) -> list[Path]:
    """Normalize every acquired raw file listed in the manifest."""
    manifest = load_manifest()
    out: list[Path] = []

    def done(p: Path) -> bool:
        return p.exists() and not force

    for rel in sorted(manifest):
        parts = rel.split("/")
        if parts[0] == "tardis" and parts[2] in ("incremental_book_L2", "trades"):
            dtype, day, sym = parts[2], parts[3], parts[4].removesuffix(".csv.gz")
            table = "book" if dtype == "incremental_book_L2" else "trades"
            dest = normalized_path("tardis", sym, table, day)
            if not done(dest):
                df = tardis_book(RAW / rel) if table == "book" else tardis_trades(RAW / rel)
                write_normalized(df, dest, source="tardis", symbol=sym, table=table, period=day, raw_rel_paths=[rel])
            out.append(dest)
        elif parts[0] == "hf_lobstream" and parts[2] in ("depth", "trades"):
            dtype, sym, period = parts[2], parts[4], parts[5].removesuffix(".parquet")
            if dtype == "depth":
                snap_rel = "/".join([parts[0], parts[1], "snapshots", parts[3], sym, parts[5]])
                dest = normalized_path("hf_lobstream", sym, "book", period)
                if not done(dest):
                    df = hf_book(RAW / rel, RAW / snap_rel)
                    write_normalized(df, dest, source="hf_lobstream", symbol=sym, table="book", period=period,
                                     raw_rel_paths=[rel, snap_rel],
                                     notes="local_us is the collector receive clock (ms resolution); no exchange time")
            else:
                dest = normalized_path("hf_lobstream", sym, "trades", period)
                if not done(dest):
                    write_normalized(hf_trades(RAW / rel), dest, source="hf_lobstream", symbol=sym, table="trades",
                                     period=period, raw_rel_paths=[rel],
                                     notes="exch_us is exchange trade time truncated to milliseconds")
            out.append(dest)
        elif parts[0] == "binance_vision" and parts[3] == "trades" and rel.endswith(".zip"):
            sym = parts[4]
            day = parts[5].removesuffix(".zip").split("-trades-")[1]
            dest = normalized_path("binance_vision", sym, "trades", day)
            if not done(dest):
                write_normalized(binance_vision_trades(RAW / rel), dest, source="binance_vision", symbol=sym,
                                 table="trades", period=day, raw_rel_paths=[rel])
            out.append(dest)
    return out


if __name__ == "__main__":
    import sys

    paths = run_all(force="--force" in sys.argv)
    print(f"normalized {len(paths)} files under {NORM}")
