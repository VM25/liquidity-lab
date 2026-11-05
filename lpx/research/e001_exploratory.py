"""E001 exploratory addenda (configs/e001_exploratory_v1.toml, declared 2026-10-20 before computation).

Status: **observed, exploratory**. Uses the frozen E001 event construction and validity rules (``e001.session_events``
on the exchange clock, baseline joint windows, timestamp-side clusters, primary event set) on discovery sessions only.
Nothing here changes the primary specification or its results.

1. Paired horizons — onset timing on one event set, and a split of the markout into the move inside the depth batch
   that contains the trade (c) and the drift after it.
2. Weighting — event-, quantity- and notional-weighted session means; passive mark-to-mid per unit notional = rs/2.
3. Decision-time imbalance — the touch-imbalance cells re-expressed from the passive side's point of view.

Usage: ``uv run python -m lpx.research.e001_exploratory``
"""

from __future__ import annotations

import datetime as dt
import json
import tomllib

import numpy as np
import polars as pl

from lpx.book import states as S
from lpx.data.acquire import ROOT
from lpx.research import e001

OUT = ROOT / "results" / "e001"
LABEL = "exploratory"


def session_frame(sess: e001.Session, windows: pl.DataFrame, horizons: list[float], primary_h: list[float]) -> pl.DataFrame:
    ev = e001.session_events(sess, windows, horizons, primary_h, unit="ts_side_cluster", timing="exchange", baseline_windows=True)
    ev = ev.filter(pl.col("primary"))
    in_w = S.in_windows(sess.t_exch, windows)
    state_ok = sess.bbo_ok & in_w
    T = ev["t_us"].to_numpy()
    s = ev["sign"].to_numpy()
    i0, ok0 = S.asof(sess.t_exch, T, windows, state_ok=state_ok, strict=True)
    if not ok0.all():
        raise AssertionError("primary event without a valid pre-event state")
    k = np.searchsorted(sess.t_exch, T, side="left")  # first state with exchange time >= T: the batch containing the trade
    kk = np.clip(k, 0, len(sess.t_exch) - 1)
    ok_next = (k < len(sess.t_exch)) & state_ok[kk] & (S.window_id(sess.t_exch[kk], windows) == S.window_id(T, windows))
    m0 = ev["m0"].to_numpy()
    c = np.where(ok_next, s * (sess.mid[kk] - m0) / m0 * 1e4, np.nan)
    touch_before = np.where(s > 0, sess.ask[i0], sess.bid[i0])
    touch_after = np.where(s > 0, sess.ask[kk], sess.bid[kk])
    q_passive = np.where(s > 0, ev["q_ask1"].to_numpy(), ev["q_bid1"].to_numpy())
    q_opp = np.where(s > 0, ev["q_bid1"].to_numpy(), ev["q_ask1"].to_numpy())
    return ev.with_columns(
        pl.Series("c_batch", c),
        pl.Series("touch_transition", np.where(ok_next, touch_after != touch_before, False)),
        pl.Series("ok_next", ok_next),
        (pl.col("qty") * pl.col("vwap")).alias("notional"),
        pl.when(pl.col("sign") > 0).then(pl.lit("ask (filled by buyer)")).otherwise(pl.lit("bid (filled by seller)")).alias("passive_side"),
        pl.Series("imb_passive", (q_passive - q_opp) / (q_passive + q_opp)),
    )


def weighted_session_means(f: pl.DataFrame, metrics: list[str], weight: str) -> pl.DataFrame:
    """Per-session weighted mean of each metric over events where it is defined (NaN excluded)."""
    aggs = []
    for m in metrics:
        ok = pl.col(m).is_not_nan() & pl.col(m).is_not_null()
        if weight == "event":
            aggs.append(pl.col(m).filter(ok).mean().alias(m))
        else:
            aggs.append(((pl.col(m) * pl.col(weight)).filter(ok).sum() / pl.col(weight).filter(ok).sum()).alias(m))
    return f.group_by("day").agg(aggs).sort("day")


def boot(x: np.ndarray, n: int, rng: np.random.Generator) -> tuple[float, float, float]:
    x = x[~np.isnan(x)]
    m = x[rng.integers(0, x.size, size=(n, x.size))].mean(axis=1)
    return float(x.mean()), float(np.quantile(m, 0.025)), float(np.quantile(m, 0.975))


def run() -> dict:
    from lpx.provenance import provenance, require_clean

    xc = tomllib.loads((ROOT / "configs" / "e001_exploratory_v1.toml").read_text())
    cfg = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    if "test" in xc["session_sets"]:
        raise PermissionError("test sessions are sealed")
    require_clean()
    sp, sym = cfg["splits"], cfg["dataset"]["symbol"]
    days = sorted(d for k in xc["session_sets"] for d in sp[k])
    inputs = e001.verify_inputs(cfg, days)
    hz = xc["paired_horizons"]["horizons_s"]
    primary_h = cfg["e001"]["horizons_s"]
    frames = []
    for d in days:
        frames.append(session_frame(e001.Session(sym, d), S.load_windows(sym, d, "joint"), hz, primary_h))
    F = pl.concat(frames)
    rng = np.random.default_rng(xc["seed"])
    n = xc["bootstrap_resamples"]
    res = {"analysis": LABEL, "declared_in": "configs/e001_exploratory_v1.toml", "sessions": days,
           "run_at_utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
           "provenance": {**provenance(["configs/research_v1.toml", "configs/e001_exploratory_v1.toml"]), "inputs": inputs},
           "events_primary_set": F.height}

    # 1. paired horizons on one event set
    P = F.filter(pl.col("mo_0.1s").is_not_nan() & pl.col("ok_next")).with_columns(
        (pl.col("mo_1s") - pl.col("mo_0.1s")).alias("d_0.1_1"), (pl.col("mo_5s") - pl.col("mo_1s")).alias("d_1_5"),
        (pl.col("mo_30s") - pl.col("mo_5s")).alias("d_5_30"), (pl.col("mo_30s") - pl.col("c_batch")).alias("drift_30"),
        (pl.col("rs_0.1s") / 2).alias("half_rs_0.1s"), (pl.col("rs_1s") / 2).alias("half_rs_1s"), (pl.col("rs_30s") / 2).alias("half_rs_30s"))
    paired = []
    for sub_name, sub in (("all", P), ("touch transition", P.filter(pl.col("touch_transition"))),
                          ("no touch transition", P.filter(~pl.col("touch_transition")))):
        sm = weighted_session_means(sub, ["mo_0.1s", "d_0.1_1", "d_1_5", "d_5_30", "mo_30s", "c_batch", "drift_30",
                                          "half_rs_0.1s", "half_rs_1s", "half_rs_30s"], "event")
        for m in sm.columns[1:]:
            mean, lo, hi = boot(sm[m].to_numpy().astype(float), n, rng)
            paired.append({"analysis": LABEL, "subset": sub_name, "events": sub.height, "metric": m, "mean_of_session_means": mean,
                           "ci95_lo": lo, "ci95_hi": hi})
    res["paired_events"] = P.height
    res["touch_transition_share"] = float(P["touch_transition"].mean())

    # 2. weighting
    W = F.with_columns((pl.col("rs_1s") / 2).alias("half_rs_1s"), (pl.col("rs_30s") / 2).alias("half_rs_30s"))
    wm = ["es", "mo_1s", "mo_30s", "rs_1s", "rs_30s", "half_rs_1s", "half_rs_30s"]
    weighting = []
    for wt in xc["weighting"]["weights"]:
        sm = weighted_session_means(W, wm, "qty" if wt == "quantity" else wt)
        for m in wm:
            mean, lo, hi = boot(sm[m].to_numpy().astype(float), n, rng)
            weighting.append({"analysis": LABEL, "weight": wt, "metric": m, "mean_of_session_means": mean, "ci95_lo": lo, "ci95_hi": hi})

    # 3. decision-time imbalance from the passive side
    b = xc["decision_time_imbalance"]["bins"]
    D = F.with_columns(
        pl.when(pl.col("imb_passive") <= b[1]).then(pl.lit("thinner side")).when(pl.col("imb_passive") < b[2])
        .then(pl.lit("balanced")).otherwise(pl.lit("thicker side")).alias("passive_queue"),
        (pl.col("rs_1s") / 2).alias("half_rs_1s"), (pl.col("rs_30s") / 2).alias("half_rs_30s"))
    dec = []
    for (side, bucket), g in D.group_by(["passive_side", "passive_queue"], maintain_order=True):
        sm = weighted_session_means(g, ["mo_30s", "half_rs_1s", "half_rs_30s"], "event")
        row = {"analysis": LABEL, "passive_side": side, "passive_queue": bucket, "events": g.height,
               "share_of_side_events": g.height / D.filter(pl.col("passive_side") == side).height}
        for m in ("mo_30s", "half_rs_1s", "half_rs_30s"):
            mean, lo, hi = boot(sm[m].to_numpy().astype(float), n, rng)
            row.update({m: mean, f"{m}_ci95_lo": lo, f"{m}_ci95_hi": hi})
        dec.append(row)
    dec.sort(key=lambda r: (r["passive_side"], ["thinner side", "balanced", "thicker side"].index(r["passive_queue"])))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "e001_exploratory.json").write_text(json.dumps(res, indent=1))
    pl.DataFrame(paired).write_csv(OUT / "e001_exploratory_paired.csv")
    pl.DataFrame(weighting).write_csv(OUT / "e001_exploratory_weighting.csv")
    pl.DataFrame(dec).write_csv(OUT / "e001_exploratory_decision_time.csv")
    return res


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: v for k, v in r.items() if k != "provenance"}, indent=1)[:1500])
