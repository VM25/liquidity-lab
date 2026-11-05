"""E004 date-only degradation schedules: determinism, role independence, merging and realised shares (no market data)."""

import tomllib

import numpy as np

from lpx.data.acquire import ROOT
from lpx.research import e004_schedules as G

CFG = tomllib.loads((ROOT / "configs" / "e004_v1.toml").read_text())


def test_merge_unions_overlapping_and_touching_intervals():
    iv = np.array([[10, 20], [15, 25], [25, 30], [40, 40], [50, 60], [0, 5]])
    assert G.merge(iv).tolist() == [[0, 5], [10, 30], [50, 60]]
    assert G.merge(np.empty((0, 2))).shape == (0, 2)


def test_schedules_are_deterministic_and_keyed_by_cell_day_role_and_replicate():
    a = G.schedule(CFG, "D1_S", "2025-03-01", "eval", 0)
    assert np.array_equal(a, G.schedule(CFG, "D1_S", "2025-03-01", "eval", 0))
    others = [G.schedule(CFG, "D1_S", "2025-03-01", "eval", 1), G.schedule(CFG, "D1_S", "2025-03-01", "train", 0),
              G.schedule(CFG, "D1_S", "2025-03-01", "placebo_eval", 0), G.schedule(CFG, "D1_S", "2025-04-01", "eval", 0),
              G.schedule(CFG, "D1_S1", "2025-03-01", "eval", 0)]
    for b in others:
        assert not np.array_equal(a, b)
    # D3 delays D1-S's records on D1-S's own schedule
    assert np.array_equal(a, G.schedule(CFG, "D3", "2025-03-01", "eval", 0))


def test_schedules_stay_inside_the_day_and_are_merged_integers():
    for cell in G.cells(CFG):
        iv = G.schedule(CFG, cell, "2026-01-01", "eval", 2)
        t0 = G.day_start_us("2026-01-01")
        assert iv.dtype == np.int64 and iv.shape[1] == 2 and iv.shape[0] > 0
        assert iv[0, 0] >= t0 and iv[-1, 1] <= t0 + G.DAY_US
        assert np.all(iv[:, 1] > iv[:, 0]) and np.all(iv[1:, 0] > iv[:-1, 1])


def test_d1e_stalls_are_unions_of_the_configured_reconnect_gaps():
    dur = np.rint(np.array(CFG["degradations"]["D1_E"]["durations_ms"]) * 1e3).astype(np.int64)
    rng = G.stream(1, 1, "2025-03-01", 1, 0)
    raw = G.poisson(rng, CFG["degradations"]["D1_E"]["onsets_per_hour"], CFG["degradations"]["D1_E"]["durations_ms"])
    assert set((raw[:, 1] - raw[:, 0]).tolist()) <= set(dur.tolist())
    d = CFG["degradations"]["D1_S"]
    rs = G.renewal(G.stream(1, 2, "2025-03-01", 1, 0), d["up_mean_s"], 1e9, d["stall_cap_s"])
    assert np.all(rs[:, 1] - rs[:, 0] <= d["stall_cap_s"] * 1e6)


def test_realised_shares_match_the_design_on_the_schedules_used():
    """Over the evaluation schedules actually used (15 discovery days x 3 replicates, 3.9e6 s). At exactly 1e6 s the D4
    tolerance (2 pp) is about 2.2 standard deviations: a first check on 12 non-research days (2030-01-01..12, replicate 0)
    gave D4 22.3%, while six such blocks average 25.2% (D1-S 16.7%, D1-E 4.46%, D2 14.3%), i.e. sampling noise, not bias."""
    import tomllib as tl

    rc = tl.loads((ROOT / "configs" / "research_v1.toml").read_text())
    days = rc["splits"]["train"] + rc["splits"]["validation"]
    for cell, (target, tol) in CFG["degradations"]["realised_share_targets"].items():
        covered = sum(int((iv[:, 1] - iv[:, 0]).sum()) for d in days for r in range(3)
                      for iv in [G.schedule(CFG, cell, d, "eval", r)])
        share = covered / (3 * len(days) * G.DAY_US)
        assert abs(share - target) <= tol, (cell, share)


def test_schedule_hash_is_sha256_of_little_endian_int64_endpoints():
    import hashlib

    iv = np.array([[1, 2], [3, 4]], np.int64)
    expect = hashlib.sha256(b"".join(int(x).to_bytes(8, "little", signed=True) for x in (1, 2, 3, 4))).hexdigest()
    assert G.schedule_hash(iv) == expect


def test_hash_list_covers_every_cell_role_and_replicate():
    h = G.hash_list(CFG, ["2025-03-01"])["2025-03-01"]
    assert list(h) == G.cells(CFG) == ["D1_E", "D1_S", "D1_S1", "D1_S3", "D3", "D2", "D4"]
    for cell in h:
        assert set(h[cell]) == set(G.SCHEDULE_ROLES)
        assert len(h[cell]["train"]) == 1 and len(h[cell]["eval"]) == 3 and len(h[cell]["placebo_eval"]) == 3
    assert h["D3"] == h["D1_S"]
