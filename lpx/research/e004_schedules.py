"""E004 degradation schedules (docs/experiments/E004.md section 2) — date only: no market data is read.

Every schedule lives on the recorder (delivery) clock over one whole UTC day [00:00, 24:00), independently of episodes,
as merged half-open intervals [start, end) in integer microseconds since the Unix epoch. A record received exactly at an
interval's end is outside it.

Draws (one PCG64 stream per (cell code, yyyymmdd, role, replicate); times are drawn as float microseconds from 00:00 and
floored to integers before merging, so the hashed endpoints are rounded toward -inf):
    renewal  (D1-S, D1-S1, D1-S3, D2, D4)  start in an up spell; repeat: up ~ Exp(up mean), then a down spell
             ~ Exp(down mean), capped where the cell has a cap. D4's down spells are its noisy regimes.
    poisson  (D1-E)  repeat: inter-onset gap ~ Exp(3600 / rate s), then a duration drawn uniformly from the configured
             reconnect gaps (an integer index into the list); overlapping or touching stalls merge.
    D3 uses D1-S's schedule (same draws, same hash).
Intervals are clipped to the day end. Noise draws (D4 sizes) and placebo-window offsets (role 4) are separate streams and
are not covered by the schedule hashes.

Usage (writes results/e004_prefreeze/schedule_hashes.json for all 20 research days; reads only configs):
    uv run python -m lpx.research.e004_schedules
"""

from __future__ import annotations

import datetime as dt
import hashlib
import json
import tomllib

import numpy as np

from lpx.data.acquire import ROOT

CONFIG = ROOT / "configs" / "e004_v1.toml"
OUT = ROOT / "results" / "e004_prefreeze" / "schedule_hashes.json"
DAY_US = 86_400_000_000
SCHEDULE_ROLES = ("train", "eval", "placebo_train", "placebo_eval")


def day_start_us(day: str) -> int:
    d = dt.datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=dt.UTC)
    return int(d.timestamp()) * 1_000_000


def stream(entropy: int, cell_code: int, day: str, role: int, replicate: int, *suffix: int) -> np.random.Generator:
    """The deterministic stream of one (cell, day, role, replicate) key; ``suffix`` selects a sub-stream (noise: 1)."""
    key = (cell_code, int(day.replace("-", "")), role, replicate, *suffix)
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence(entropy=entropy, spawn_key=key)))


def merge(iv: np.ndarray) -> np.ndarray:
    """Union of half-open integer intervals (k, 2), sorted; overlapping or touching intervals merge; empty ones drop."""
    iv = np.asarray(iv, np.int64).reshape(-1, 2)
    iv = iv[iv[:, 1] > iv[:, 0]]
    if iv.shape[0] == 0:
        return iv
    iv = iv[np.argsort(iv[:, 0], kind="mergesort")]
    out = [list(iv[0])]
    for s, e in iv[1:]:
        if s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return np.array(out, np.int64)


def renewal(rng: np.random.Generator, up_mean_s: float, down_mean_s: float, cap_s: float | None) -> np.ndarray:
    """Down spells of an alternating renewal process over one day, in microseconds from 00:00 (unmerged)."""
    t, out = 0.0, []
    while True:
        t += rng.exponential(up_mean_s * 1e6)
        if t >= DAY_US:
            break
        d = rng.exponential(down_mean_s * 1e6)
        if cap_s is not None:
            d = min(d, cap_s * 1e6)
        out.append((np.floor(t), np.floor(t + d)))
        t += d
    return np.array(out, np.int64).reshape(-1, 2)


def poisson(rng: np.random.Generator, onsets_per_hour: float, durations_ms: list[float]) -> np.ndarray:
    """Stalls with Poisson onsets and durations drawn uniformly from ``durations_ms``, in microseconds from 00:00."""
    dur = np.rint(np.array(durations_ms) * 1e3).astype(np.int64)
    if np.any(np.abs(dur - np.array(durations_ms) * 1e3) > 1e-6):
        raise ValueError("reconnect gaps must be whole microseconds")
    t, out = 0.0, []
    while True:
        t += rng.exponential(3600e6 / onsets_per_hour)
        if t >= DAY_US:
            break
        s = int(np.floor(t))
        out.append((s, s + int(dur[rng.integers(dur.size)])))
    return np.array(out, np.int64).reshape(-1, 2)


def schedule(cfg: dict, cell: str, day: str, role: str, replicate: int) -> np.ndarray:
    """Merged intervals (absolute microseconds) of one cell's schedule: stalls (D1-*), outages (D2) or noisy regimes (D4)."""
    deg = cfg["degradations"]
    spec = deg[cell]
    if spec["kind"] == "catchup_delay":
        return schedule(cfg, spec["schedule_of"], day, role, replicate)
    seeds = cfg["seeds"]
    rng = stream(seeds["entropy"], seeds["cell_codes"][cell], day, seeds["roles"][role], replicate)
    if spec["kind"] == "connection_drop_withhold":
        iv = poisson(rng, spec["onsets_per_hour"], spec["durations_ms"])
    elif spec["kind"] in ("book_stall_withhold", "trade_outage_withhold"):
        up = spec["up_mean_s"]
        down = spec["stall_mean_s"] if "stall_mean_s" in spec else spec["outage_mean_s"]
        iv = renewal(rng, up, down, spec.get("stall_cap_s"))
    elif spec["kind"] == "size_noise":
        iv = renewal(rng, spec["clean_mean_s"], spec["noisy_mean_s"], None)
    else:
        raise ValueError(f"{cell}: unknown degradation kind {spec['kind']}")
    iv = merge(np.minimum(iv, DAY_US))
    return iv + day_start_us(day)


def schedule_hash(iv: np.ndarray) -> str:
    """SHA-256 of the little-endian int64 endpoints (start0, end0, start1, ...) after merging."""
    return hashlib.sha256(np.ascontiguousarray(np.asarray(iv, "<i8")).tobytes()).hexdigest()


def cells(cfg: dict) -> list[str]:
    """Degraded cells, in configuration order (D0 has no schedule)."""
    return [k for k, v in cfg["degradations"].items() if isinstance(v, dict) and "kind" in v]


def replicates(cfg: dict, role: str) -> range:
    s = cfg["seeds"]
    return range(s["training_draws"] if role in ("train", "placebo_train") else max(s["eval_replicates"], s["test_replicates"]))


def hash_list(cfg: dict, days: list[str]) -> dict:
    out = {}
    for d in days:
        out[d] = {}
        for cell in cells(cfg):
            out[d][cell] = {}
            for role in SCHEDULE_ROLES:
                out[d][cell][role] = {}
                for r in replicates(cfg, role):
                    iv = schedule(cfg, cell, d, role, r)
                    out[d][cell][role][str(r)] = {"sha256": schedule_hash(iv), "intervals": int(iv.shape[0]),
                                                  "covered_s": float((iv[:, 1] - iv[:, 0]).sum() / 1e6)}
    return out


def main() -> dict:
    from lpx.provenance import provenance, require_clean, sha256_file

    require_clean()
    cfg = tomllib.loads(CONFIG.read_text())
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    days = sorted(rc["splits"]["train"] + rc["splits"]["validation"] + rc["splits"]["test"])
    gen = ROOT / "lpx" / "research" / "e004_schedules.py"
    out = {"status": "synthetic (date-only schedules; no market data read)",
           "hash": cfg["seeds"]["schedule_hash"], "days": days,
           "provenance": {**provenance(["configs/e004_v1.toml", "configs/research_v1.toml"]),
                          "generator_sha256": sha256_file(gen)},
           "schedules": hash_list(cfg, days)}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main()
