"""Close-out pre-check (docs/experiments/FINAL_EVALUATION.md, section 1): the input-status record, from whole-file hashes, the acceptance
hash list and the listed acceptance-metadata columns only. Parses no price, trade or state row, and reads no Parquet footer.

    --stand-ins    s11..s15 (rehearsal); the default use until the owner authorises step 3
    --test-days    the five test days; refused without a committed authorisation naming this code (section 9, step 3)

A session is undefined only for a genuine input problem, recorded as a reason code. Anything else, such as a disk or memory error or an
unexpected software failure, aborts with no record written. The record is written once, whole, and never over an existing file.

Status: metadata and hashes. Usage: PYTHONPATH=. uv run python tools/closeout_precheck.py OUT.json --stand-ins
"""

import argparse
import datetime as dt
import importlib.metadata
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import polars as pl

from lpx.book import states as S
from lpx.data.acquire import ROOT
from lpx.research import closeout as C
from lpx.research import e003 as E3
from lpx.research import e004 as E4

COLUMNS = ["start_us", "end_us", "duration_s", "layer", "source", "symbol", "day", "integrity_status"]
AUTHORISATION = C.AUTHORISATION
AUTHORISATION_STEP = "closeout pre-check step 3"
STEP3_APPROVAL = "APPROVED closeout pre-check step 3: {h}"      # the owner's line in docs/DECISIONS.md, exactly
# Everything the tool's result depends on: its code, the configurations it reads (closeout_v1.toml at import, unused), and its input lists
PRECHECK_CODE = ("tools/closeout_precheck.py", "lpx/research/closeout.py", "configs/research_v1.toml", "configs/e003_v1.toml", "configs/e004_v1.toml", "configs/closeout_v1.toml",
                 "results/acceptance_001/windows.csv", "results/acceptance_001/summary.json", "results/e004_prefreeze/schedule_hashes.json")
# The evidence step 3 waits for (section 9): each must have passed, on the code the authorisation names
EVIDENCE = ("dryrun_check1_fits.json", "fits_recomputation.json", "dryrun_check2_reproduction.json", "comparison_key_inventory.json", "dryrun_check3_rehearsal.json",
            "fault_injection_realpath.json", "precheck_faults.json")


def schedule_check(days: list[str]) -> int:
    """Date-only: the generator against the committed hash list. Reads no market data."""
    e4, _ = E4.load_cfg()
    return E4.verify_schedules(e4, days, e4["seeds"]["eval_replicates"])


def accepted_windows(sym: str, days: list[str]) -> pl.DataFrame:
    """The listed columns of this symbol's joint windows on the listed days; no other row is kept."""
    return (pl.scan_csv(S.WINDOWS).select(COLUMNS).filter((pl.col("source") == "tardis") & (pl.col("symbol") == sym) & (pl.col("layer") == "joint") & pl.col("day").is_in(days))
            .collect())


def session_record(sym: str, d: str, g: pl.DataFrame, recorded: dict | None, min_episode_s: float) -> dict:
    """One session's status. Exceptions are not caught: only genuine input problems become reason codes (closeout.input_mismatch)."""
    reason, hashes = C.input_mismatch(sym, d, recorded)
    if reason is None and g.height and (g["integrity_status"] != "accepted").any():
        reason = "integrity_not_accepted"
    windows = [list(x) for x in g.select("start_us", "end_us").iter_rows()]
    eps = [list(x) for x in C.episodes(g.select("start_us", "end_us"), min_episode_s)]
    none = "no_accepted_joint_windows" if not windows else None
    return {"undefined": reason is not None, "reason": reason, "sha256": hashes, "windows": windows, "episodes": eps,
            "e001_valid": reason is None and bool(windows), "episode_valid": reason is None and bool(eps),
            "e001_reason": reason or none, "episode_reason": reason or none or ("no_qualifying_episodes" if not eps else None)}


def build_status(rc: dict, days: list[str], min_episode_s: float) -> dict:
    sym = rc["dataset"]["symbol"]
    recorded = C.acceptance_record(rc, days)
    w = accepted_windows(sym, days)
    out = {}
    for d in days:
        out[d] = session_record(sym, d, w.filter(pl.col("day") == d).sort("start_us"), recorded.get(d), min_episode_s)
    return out


def refuse_dirty_scope(ws: C.Workspace) -> None:
    if os.environ.get("LPX_ALLOW_DIRTY"):
        raise C.Refused("LPX_ALLOW_DIRTY must be unset")
    C.refuse_untrustworthy_git(ws)
    if ws.git("status", "--porcelain", "--untracked-files=all", "--", *C.DIFF_SCOPE).strip():
        raise C.Refused("uncommitted changes in the close-out's scope")


def committed(ws: C.Workspace, rel: str) -> str:
    """A file's content as committed in HEAD, which must equal the working copy: the record is what the history holds."""
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ws.root, capture_output=True, text=True)
    if r.returncode or not (ws.root / rel).exists() or r.stdout != (ws.root / rel).read_text():
        raise C.Refused(f"{rel} is not committed as it stands")
    return r.stdout


def verify_evidence(ws: C.Workspace, commit: str) -> None:
    """Every evidence run passed, on code whose trees equal the authorised commit's."""
    want = {}
    for t in C.DIFF_SCOPE:
        r = subprocess.run(["git", "rev-parse", "--verify", "--quiet", f"{commit}:{t}"], cwd=ws.root, capture_output=True, text=True)
        want[t] = r.stdout.strip() if r.returncode == 0 else None
    for f in EVIDENCE:
        rel = f"results/closeout_dev/{f}"
        if not (ws.root / rel).exists():
            raise C.Refused(f"evidence missing: {rel}")
        e = json.loads(committed(ws, rel))
        if not (e.get("passed") or e.get("byte_identical")):
            raise C.Refused(f"evidence did not pass: {rel}")
        trees = (e.get("provenance") or {}).get("trees")
        if trees != want:
            raise C.Refused(f"evidence is from other code than the authorised commit, or records no code: {rel}")


def verify_authorisation(ws: C.Workspace, out: Path) -> str:
    """Step 3 only: a clean repository and a committed authorisation naming this code, with the owner's DECISIONS.md entry naming its hash.
    Every check runs before any test-day file is opened. It proves a record exists, not who wrote it: the owner's approval stays a human act."""
    refuse_dirty_scope(ws)
    bad = ws.git("status", "--porcelain", "--untracked-files=all").strip()
    if bad:
        raise C.Refused("the repository is not clean")
    if ws.git("symbolic-ref", "--quiet", "HEAD", check=False).strip() != "refs/heads/main":
        raise C.Refused("step 3 runs only on main")
    if out.resolve() != (ws.root / C.INPUT_STATUS).resolve():
        raise C.Refused(f"step 3 writes only {C.INPUT_STATUS}")
    if out.exists() or ws.git("log", "--all", "--format=%H", "--", C.INPUT_STATUS).strip():
        raise C.Refused(f"{C.INPUT_STATUS} already exists or once existed: step 3 runs once")
    if not (ws.root / AUTHORISATION).exists():
        raise C.Refused("no committed authorisation for step 3")
    a = json.loads(committed(ws, AUTHORISATION))
    if a.get("step") != AUTHORISATION_STEP:
        raise C.Refused("the authorisation is not for step 3")
    commit = a.get("code_commit", "")
    head = ws.git("rev-parse", "HEAD").strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit) or ws.git("cat-file", "-t", commit, check=False).strip() != "commit" or commit == head \
            or subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=ws.root, capture_output=True).returncode:
        raise C.Refused("the authorised commit must be a full SHA of a commit that is a strict ancestor of HEAD")
    if ws.git("diff", "--name-only", commit, "HEAD", "--", *C.DIFF_SCOPE).strip():
        raise C.Refused("code or configuration changed since the authorised commit")
    want = {f: C.sha256_file(ws.root / f) for f in PRECHECK_CODE + (C.PROTOCOL,)}
    if a.get("sha256") != want:
        raise C.Refused("the authorisation names other files than these")
    verify_evidence(ws, commit)
    h = C.sha256_file(ws.root / AUTHORISATION)
    committed(ws, "docs/DECISIONS.md")
    if not C.owner_line(ws, STEP3_APPROVAL.format(h=h)):
        raise C.Refused(f"no owner entry in docs/DECISIONS.md reads exactly '{STEP3_APPROVAL.format(h=h)}'")
    return h


def provenance_record(ws: C.Workspace, mode: str, authorisation: str | None) -> dict:
    return {"mode": mode, "git_commit": ws.git("rev-parse", "HEAD").strip(), "code_fingerprint": C.fingerprint(ws.root), "trees": C.trees(ws),
            "precheck_sha256": C.sha256_file(ws.root / "tools/closeout_precheck.py"), "uv_lock_sha256": C.sha256_file(ws.root / "uv.lock"), "python_version": sys.version.split()[0],
            "packages": {d.metadata["Name"]: d.version for d in importlib.metadata.distributions() if d.metadata["Name"] in ("numpy", "polars", "pyarrow")},
            "windows_csv_sha256": C.sha256_file(S.WINDOWS), "acceptance_summary_sha256": C.sha256_file(ROOT / "results/acceptance_001/summary.json"),
            "authorisation_sha256": authorisation, "utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds")}


def run(out: Path, test_days: bool, ws: C.Workspace | None = None) -> dict:
    """Guards first, then the reads, then one exclusive write. No exception is caught here: an abort leaves no record."""
    ws = ws or C.Workspace(ROOT)
    rc = C.load_rc()
    if test_days and ws.root.resolve() != ROOT.resolve():
        raise C.Refused("step 3 runs only in the project repository, whose files are the ones read")
    if out.exists():
        raise C.Refused(f"{out.name} already exists and is never overwritten")
    if test_days:
        authorisation, days = verify_authorisation(ws, out), rc["splits"]["test"]
    else:
        if (ws.root / "results" / "closeout_freeze") in out.resolve().parents:
            raise C.Refused("stand-ins never write under results/closeout_freeze/")
        refuse_dirty_scope(ws)
        authorisation, days = None, sorted(rc["splits"]["train"] + rc["splits"]["validation"])[10:]
        if set(days) & set(rc["splits"]["test"]):
            raise C.Refused("stand-ins may not include a test day")
    cfg3 = C.tomllib.loads(E3.CONFIG.read_text())
    res = {"status": "metadata and whole-file hashes; no price, trade or state row and no Parquet footer read", "provenance": provenance_record(ws, "test" if test_days else "stand-ins", authorisation),
           "schedules_verified_date_only": schedule_check(sorted(sum((rc["splits"][k] for k in ("train", "validation", "test")), []))),
           "sessions": build_status(rc, days, cfg3["scope"]["min_episode_s"])}
    C.write_exclusive(out, json.dumps(res, sort_keys=True, indent=0))
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--stand-ins", action="store_true")
    ap.add_argument("--test-days", action="store_true")
    a = ap.parse_args()
    if a.test_days == a.stand_ins:
        ap.error("choose --stand-ins or --test-days")
    try:
        res = run(a.out, a.test_days)
    except C.Refused as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    except BaseException as e:      # noqa: BLE001 - reported by type and place only
        state = "a complete record exists (the failure came after it was written)" if a.out.exists() else "no record written"
        print(f"aborted, {state}: {type(e).__name__} at {C.location(e)}", file=sys.stderr)
        return 3
    print(json.dumps({d: {"undefined": r["undefined"], "reason": r["reason"], "e001": r["e001_valid"], "e001_reason": r["e001_reason"], "episodes": len(r["episodes"]),
                          "episode_reason": r["episode_reason"]} for d, r in res["sessions"].items()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
