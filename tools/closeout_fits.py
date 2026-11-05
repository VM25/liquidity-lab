"""Close-out fit artifacts (docs/experiments/FINAL_EVALUATION.md, sections 2 and 7), from discovery sessions only.

    all15        M1/M2 for 1, 5, 30 s, the rv gate and E004's lambda fits on all 15 discovery sessions (the forwarded fits)
    walkforward  the same with `before` = each of s6..s15 (dry-run check 1 and the code-path reproduction)
    rehearsal    fits on s1..s10, for the stand-ins s11..s15

Refuses any test day before loading anything. Writes deterministic JSON under results/closeout_fits/<set>/.
Status: observed (forecast coefficients) / stress test (lambda fits). Usage: PYTHONPATH=. uv run python tools/closeout_fits.py [out_dir]
"""

import dataclasses
import importlib.metadata
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import polars as pl

from lpx.data.acquire import ROOT
from lpx.provenance import code_fingerprint
from lpx.research import closeout as C
from lpx.research import e003 as E3
from lpx.research import e004 as E4

TEST_DAYS_REFUSED = "the fit tool refuses test days"


def discovery_days(rc: dict) -> list[str]:
    days = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    if set(days) & set(rc["splits"]["test"]):
        raise PermissionError(TEST_DAYS_REFUSED)
    return days


def prepare(days: list[str], rc: dict) -> tuple[dict, dict]:
    """E003's thinned rows and every cell's degraded training rows, for the frozen training_rows (roles 0 and 2)."""
    if set(days) & set(rc["splits"]["test"]):
        raise PermissionError(TEST_DAYS_REFUSED)
    e4, sc = E4.load_cfg()
    thin, train = {}, {c: {} for c in E4.CELL_ORDER}
    tick = sc["instrument"]["tick"]
    for d in days:
        st, tr, eps = E3.load_session(sc, d)
        ft = E3.features(sc, st, tr, eps)
        thin[d] = ft.filter(pl.col("eligible")).gather_every(sc["features"]["fit_thinning"])
        A = C.DG.from_frames(d, st, tr, eps, tick)
        for cell in E4.CELL_ORDER:
            train[cell][d] = E4.training_rows(e4, sc, A, ft, cell)
        print(f"{d}: prepared", flush=True)
    return thin, train


def write_fit(out, before: str, sessions: list[str], thin: dict, train: dict) -> None:
    e4, sc = E4.load_cfg()
    fc = sc["features"]
    sub = {x: thin[x] for x in sessions}
    models = {h: E3.fit_models(sc, sub, before, h) for h in fc["horizons_s"]}
    rows = pl.concat([sub[x] for x in sessions])
    rv_med = float(rows.filter(pl.col("y_5s").is_not_nan() & pl.col("y_5s").is_not_null())["rv_60s"].median())
    art3 = {"rv_60s_training_median": rv_med, "rv_gate": sc["policies"]["p4_vol_gate_multiple"] * rv_med,
            **{f"h{h:g}s_{m}": dataclasses.asdict(mod) for h, ms in models.items() for m, mod in ms.items()},
            "sessions": sessions, "before": before}
    m2 = models[5]["M2"]
    cells = {c: C.cell_fit_to_json(E4.fit_cell(e4, sc, E4.stack([train[c][x] for x in sessions]), m2, c, before)) for c in E4.CELL_ORDER}
    C.dump_json(out / "e003_fit.json", art3)
    C.dump_json(out / "e004_fit.json", {"cells": cells, "sessions": sessions, "before": before})


def require_clean_tree() -> None:
    """A clean tree over the close-out's own scope, with no override (section 7)."""
    if os.environ.get("LPX_ALLOW_DIRTY"):
        raise SystemExit("refused: LPX_ALLOW_DIRTY must be unset")
    if subprocess.run(["git", "status", "--porcelain", "--", *C.DIFF_SCOPE], cwd=ROOT, capture_output=True, text=True).stdout.strip():
        raise SystemExit("refused: uncommitted changes in the close-out's scope")


def provenance_record() -> dict:
    return {"git_commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip(), "code_fingerprint": code_fingerprint(),
            "uv_lock_sha256": C.sha256_file(ROOT / "uv.lock"), "python_version": sys.version.split()[0],
            "packages": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions() if d.metadata["Name"] in ("numpy", "polars", "scipy", "numba", "pyarrow")},
            "status": "observed (forecast coefficients) / stress test (lambda fits); discovery sessions only"}


def main(base=None) -> dict:
    t0 = time.time()
    require_clean_tree()
    rc = C.load_rc()
    days = discovery_days(rc)
    base = base or (ROOT / "results" / "closeout_fits")
    thin, train = prepare(days, rc)
    write_fit(base / "all15", "2026-06-01", days, thin, train)
    write_fit(base / "rehearsal", days[10], days[:10], thin, train)
    for i, d in enumerate(days):
        if i >= 5:
            write_fit(base / "walkforward" / d, d, days[:i], thin, train)
    C.dump_json(base / "PROVENANCE.json", provenance_record())
    listing = C.tree_listing(base)
    (base / "MANIFEST.json").write_text(json.dumps({k: v for k, v in listing.items() if k != "MANIFEST.json"}, indent=1, sort_keys=True))
    print(f"fits written in {time.time() - t0:.0f} s", flush=True)
    return listing


def verify(tmp: Path) -> dict:
    """Recomputation in a fresh process: every artifact must be byte-identical to the committed one (the provenance sidecar aside). Run it
    in a fresh clone after `uv sync --frozen` (section 7); the record says which checkout ran it and whether it is a clone."""
    main(tmp)
    a, b = C.tree_listing(ROOT / "results" / "closeout_fits"), C.tree_listing(tmp)
    skip = {"MANIFEST.json", "PROVENANCE.json"}
    diff = sorted(k for k in set(a) | set(b) if k not in skip and a.get(k) != b.get(k))
    ws = C.Workspace(ROOT)
    origin = ws.git("config", "--get", "remote.origin.url", check=False).strip() or None
    res = {"status": "recomputation of every fit artifact in a separate process", "artifacts": len(set(a) - skip), "differing": diff, "byte_identical": not diff,
           "provenance": {**provenance_record(), "trees": C.trees(ws), "checkout": str(ROOT), "clone_of": origin, "fresh_clone": origin is not None}}
    print(json.dumps(res))
    if diff:
        raise SystemExit("recomputation differs")
    return res


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--verify":
        r = verify(Path(sys.argv[2]))
        (ROOT / "results" / "closeout_dev").mkdir(exist_ok=True)
        (ROOT / "results" / "closeout_dev" / "fits_recomputation.json").write_text(json.dumps(r, indent=1))
    else:
        main(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
