"""Close-out on the held-out sessions (docs/experiments/FINAL_EVALUATION.md, sections 6 and 7). Guarded entry point.

Modes:
    test       the five sealed sessions; needs a frozen protocol, a freeze record, an owner authorisation and an `authorised`
               ledger event; refuses everything else. No injection hook exists in this mode.
    dryrun     discovery sessions with walk-forward fits; reproduces the frozen discovery tables; no ledger.
    rehearsal  discovery stand-ins with fits on earlier sessions, in a scratch repository with its own ledger.

Functions named ``frozen_copy_*`` are the protocol's marked blocks: orchestration copied from the frozen ``run()``
functions (at baseline 5c9d93e), which cannot be called directly because they refuse test sessions and write to the discovery
directories. Tests compare them with the frozen source. Failure classes (protocol section 6):
- integrity, after the freeze: a pinned input (a session's four files, a fit artifact, a pinned data file under results/) missing, not
  pinned, or with bytes other than its pin: a failed attempt (IntegrityFailure, every finding recorded), never an undefined session. The
  pins are checked at the start, in the metadata step, and again before any other failure is classified, so a changed input is the
  recorded cause whatever exception it set off. Only the frozen verifiers' own verdict on bytes that match the pins makes a session
  undefined at the run;
- environment: an OSError (a denied or failed read or write of a present file), a memory error, an interrupt, a process death: a failed
  attempt (a pinned input found missing, even on an absent volume, is integrity);
- software: inside an experiment, while every pin still holds, an exception whose innermost project frame is baseline code or a marked
  block (a PermissionError that lpx code raised itself is such a frozen refusal): the experiment is not confirmable;
- close-out: anything else, including a frozen-frame exception outside an experiment: a failed attempt.

Nothing here prints a value: the console shows the experiment, the session date, the stage and the elapsed time. Everything
else, including what frozen functions print, goes to the sealed log inside the staging directory.
"""

from __future__ import annotations

import argparse
import dataclasses
import errno
import fcntl
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import time
import tomllib
import traceback
from pathlib import Path

import numpy as np
import polars as pl

from lpx.data.acquire import ROOT
from lpx.provenance import TRACKED_SCOPE
from lpx.research import e001 as E1
from lpx.research import e002 as E2
from lpx.research import e003 as E3
from lpx.research import e003_features as F
from lpx.research import e004 as E4
from lpx.research import e004_degrade as DG
from lpx.research import e004_forecast as FC
from lpx.research import e004_policy as PO
from lpx.research import e004_schedules as G
from lpx.research.e002 import episodes, to_states, to_trades
from lpx.research.e004 import (BASES, CELL_ORDER, POLICY_CELLS, STATUS_POLICY_DEG, STATUS_POLICY_REF, VARIANTS, _agg_equal,
                               _intersect, _offsets, cell_rows, check_models, check_ref_forecasts, check_ref_policy,
                               flow_window_us, kind_of, latest_age, md_us, model_forecasts, n_buckets, overlap_us,
                               overlaps_any, p3_rescaled, state_hash, status_forecast, views_hash, window_sums, windows,
                               xframe)

MAX_ATTEMPTS = 3
EXPERIMENTS = ("E001", "E002", "E003", "E004")
DEPENDS = {"E004": ("E003",)}
BASELINE = "5c9d93e"
ALLOWED_DIFF = sorted(f"A\t{p}" for p in ("configs/closeout_v1.toml", "lpx/research/closeout.py", "lpx/research/closeout_analysis.py",
                                          "tests/test_closeout.py", "tools/closeout_dryrun.py", "tools/closeout_fits.py", "tools/closeout_precheck.py"))
LEDGER = "results/closeout_attempts.jsonl"
STAGING = "results/closeout_staging"
PROMOTED = "results/closeout"
FREEZE_RECORD = "results/closeout_freeze/freeze_record.json"
PROTOCOL = "docs/experiments/FINAL_EVALUATION.md"
DIFF_SCOPE = ("lpx", "tools", "tests", "configs", "pyproject.toml", "uv.lock", ".python-version")
ADDED_LPX = ("closeout.py", "closeout_analysis.py")
INPUT_STATUS = "results/closeout_freeze/input_status.json"
FIT_MANIFEST = "results/closeout_fits/MANIFEST.json"
FREEZE_APPROVAL = "APPROVED close-out freeze record: {h}"      # the owner's line in docs/DECISIONS.md, exactly
TEST_MODE_PINS = (PROTOCOL, "docs/experiments/E002.md", "docs/experiments/E003.md", "docs/experiments/E004.md", "configs/research_v1.toml",
                  "configs/e002_v1.toml", "configs/e003_v1.toml", "configs/e004_v1.toml", "configs/closeout_v1.toml", "pyproject.toml", "uv.lock",
                  ".python-version", "results/e003/e003_analysis.json", "results/e001/e001_discovery.json",
                  "results/e004_prefreeze/schedule_hashes.json", "results/acceptance_001/summary.json", "results/acceptance_001/windows.csv",
                  "results/acceptance_001/windows_sensitivity.csv", "results/acceptance_001/sensitivity.json", INPUT_STATUS, FIT_MANIFEST,
                  *(x.split("\t", 1)[1] for x in ALLOWED_DIFF))
ENVIRONMENT = (MemoryError, OSError, KeyboardInterrupt)
INPUT_REASONS = ("input_missing:", "hash_mismatch:", "acceptance_record_missing", "acceptance_hash_missing:", "integrity_not_accepted")


class Refused(RuntimeError):
    """A guard refused to start; nothing was read and the ledger is unchanged."""


class IntegrityFailure(RuntimeError):
    """After the freeze, an input the input-status record pinned is missing, not pinned, or its bytes differ from the pinned SHA-256
    (protocol section 1). It never makes a session undefined: the attempt fails with this class, and the failed event records every
    finding of the check that raised it."""

    def __init__(self, findings: list[dict]):
        super().__init__("; ".join(f"{f['session']} {f['input']}: {f['finding']}" for f in findings))
        self.findings = findings

    def record(self) -> dict:
        return {"findings": self.findings}


class PinnedDataChanged(IntegrityFailure, Refused):
    """A data file the freeze record pins (a path under results/) is missing or differs from its pin, with code, configuration and
    documents intact. Outside an attempt it refuses like any guard; run_attempt records it as an integrity failure of the attempt before
    any read (section 6), so a changed data file is never a refusal without a trace."""
    rec: dict | None = None
    rec_hash: str | None = None


def integrity_finding(day: str | None, name: str, finding: str, observed: str | None = None) -> dict:
    """One finding; `day` is None for a run-wide input (a fit artifact)."""
    return {"session": day, "input": name, "finding": finding, "observed_sha256": observed}


def sha256_file(p: Path) -> str:
    with open(p, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


# ------------------------------------------------------------------------------------------------ workspace and ledger
@dataclasses.dataclass
class Workspace:
    """The repository holding the ledger, staging and freeze record: the project itself, or a scratch one in a rehearsal."""
    root: Path

    def git(self, *args: str, check: bool = True) -> str:
        r = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True)
        if check and r.returncode:
            raise RuntimeError(f"git {args[0]} failed")
        return r.stdout

    @property
    def ledger(self) -> Path:
        return self.root / LEDGER

    @property
    def staging(self) -> Path:
        return self.root / STAGING

    @property
    def promoted(self) -> Path:
        return self.root / PROMOTED

    def attempt_dir(self, n: int) -> Path:
        return self.root / f"results/closeout_attempt{n}"

    def events(self) -> list[dict]:
        """Ledger events in HEAD: an event counts only once it is committed."""
        r = subprocess.run(["git", "show", f"HEAD:{LEDGER}"], cwd=self.root, capture_output=True, text=True)
        return [json.loads(x) for x in r.stdout.splitlines() if x.strip()] if r.returncode == 0 else []

    def append(self, event: dict) -> None:
        """Append one event and commit it (the ledger file only)."""
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        with open(self.ledger, "a") as f:
            f.write(json.dumps(event, sort_keys=True) + "\n")
            f.flush()
            os.fsync(f.fileno())
        self.git("add", LEDGER)
        self.git("commit", "-q", "-m", f"close-out ledger: {event['event']} {event.get('n', '')}", "--", LEDGER)


def verify_ledger_history(ws: Workspace) -> None:
    """Append-only: each committed version of the ledger extends the previous one, and events are in a valid order. An ordinary
    commit that cuts the ledger back is refused; a history rewrite is outside what a local repository can detect (section 10)."""
    revs = ws.git("log", "--full-history", "--reverse", "--format=%H", "--", LEDGER).split()
    prev = ""
    for r in revs:
        now = subprocess.run(["git", "show", f"{r}:{LEDGER}"], cwd=ws.root, capture_output=True, text=True)
        if now.returncode or not now.stdout.startswith(prev):
            raise Refused("the ledger is not append-only")
        prev = now.stdout
    seen: set = set()
    for e in ws.events():
        k, n = e["event"], e.get("n")
        if k == "authorised" and n and n > 1 and ("failed", n - 1) not in seen:
            raise Refused(f"authorised {n} precedes the failure of attempt {n - 1}")
        if k == "started" and ("authorised", n) not in seen:
            raise Refused(f"started {n} has no authorised event")
        if k in ("failed", "completed") and ("started", n) not in seen:
            raise Refused(f"{k} {n} has no started event")
        if k == "closed" and ("failed", MAX_ATTEMPTS) not in seen:
            raise Refused("closed precedes the last failed attempt")
        seen.add((k, n))


def events_with_commits(ws: Workspace) -> list[dict]:
    """Ledger events with the commit that added each, for the report's run history."""
    out, seen = ws.events(), 0
    for r in ws.git("log", "--full-history", "--reverse", "--format=%H", "--", LEDGER).split():
        k = len([x for x in ws.git("show", f"{r}:{LEDGER}").splitlines() if x.strip()])
        for e in out[seen:k]:
            e["ledger_commit"] = r[:12]
        seen = max(seen, k)
    return out


def tree_listing(d: Path) -> dict[str, str]:
    """Every file's hash; a Finder .DS_Store is not content and is left out, so it cannot make a sealed directory look tampered."""
    return {str(p.relative_to(d)): sha256_file(p) for p in sorted(d.rglob("*")) if p.is_file() and p.name != ".DS_Store"}


# ------------------------------------------------------------------------------------------------ freeze record and guards
def fingerprint(root: Path) -> str | None:
    """The code fingerprint of ``lpx/provenance.code_fingerprint``, for any repository root (the sealed records store it)."""
    if not (root / "lpx").exists():
        return None
    h = hashlib.sha256()
    for p in sorted((root / "lpx").rglob("*.py")):
        h.update(p.relative_to(root).as_posix().encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def trees(ws: Workspace) -> dict[str, str]:
    out = {}
    for t in DIFF_SCOPE:
        r = subprocess.run(["git", "rev-parse", f"HEAD:{t}"], cwd=ws.root, capture_output=True, text=True)
        out[t] = r.stdout.strip() if r.returncode == 0 else None
    return out


def diff_listing(ws: Workspace, baseline: str) -> list[str]:
    return sorted(x for x in ws.git("diff", "--name-status", baseline, "HEAD", "--", *DIFF_SCOPE).splitlines() if x.strip())


def build_freeze_record(ws: Workspace, baseline: str, pinned: list[str]) -> dict:
    """The record of section 9, step 4 (used at the freeze, and by rehearsals and tests on scratch repositories)."""
    return {"baseline": baseline, "parent_commit": ws.git("rev-parse", "HEAD").strip(), "code_fingerprint": fingerprint(ws.root),
            "trees": trees(ws), "allowed_diff": diff_listing(ws, baseline),
            "pinned_sha256": {p: sha256_file(ws.root / p) for p in sorted(pinned)}}


def is_data_pin(path: str) -> bool:
    """A pinned data input (acceptance files, discovery references, the input-status record, the fit manifest), not code or documents."""
    return path.startswith("results/")


def current_sha256(p: Path) -> str | None:
    try:
        return sha256_file(p) if p.is_file() else None
    except FileNotFoundError:
        return None


def pinned_data_findings(ws: Workspace, rec: dict) -> list[dict]:
    return [integrity_finding(None, p, "missing" if now is None else "modified", now) for p, h in sorted(rec["pinned_sha256"].items())
            if is_data_pin(p) and (now := current_sha256(ws.root / p)) != h]


def data_scope(rec: dict) -> tuple[str, ...]:
    """Paths whose changes are integrity findings, not an unclean tree: the pinned data files, and the fit artifacts (checked against
    their pinned manifest inside the attempt)."""
    return tuple(p for p in rec["pinned_sha256"] if is_data_pin(p)) + (("results/closeout_fits",) if FIT_MANIFEST in rec["pinned_sha256"] else ())


def verify_pinned(ws: Workspace, rec: dict) -> None:
    """Every pinned file, the code fingerprint and the tree hashes. A difference in code, configuration or documents refuses; a pinned
    data file's difference alone is PinnedDataChanged, one finding per file."""
    for p, h in rec["pinned_sha256"].items():
        if not is_data_pin(p) and current_sha256(ws.root / p) != h:
            raise Refused(f"pinned file differs from the freeze record: {p}")
    if rec["code_fingerprint"] != fingerprint(ws.root):
        raise Refused("code fingerprint differs from the freeze record")
    if rec["trees"] != trees(ws):
        raise Refused("tree hashes differ from the freeze record")
    found = pinned_data_findings(ws, rec)
    if found:
        raise PinnedDataChanged(found)


def verify_freeze(ws: Workspace, require_frozen_text: bool, expected: tuple[str, list[str]] | None = None) -> tuple[dict, str]:
    """``expected`` (test mode): the baseline and allowed list are the protocol's, not whatever the record claims."""
    p = ws.root / FREEZE_RECORD
    if not p.exists():
        raise Refused("no freeze record: the protocol is not frozen")
    rec = json.loads(p.read_text())
    if expected is not None:
        same = ws.git("rev-parse", f"{rec['baseline']}^{{commit}}", check=False).strip() == ws.git("rev-parse", f"{expected[0]}^{{commit}}", check=False).strip()
        if not same or rec["allowed_diff"] != sorted(expected[1]):
            raise Refused("the freeze record's baseline or allowed diff is not the protocol's")
    if require_frozen_text:
        first = (ws.root / PROTOCOL).read_text().splitlines()[0]
        if "FROZEN" not in first or "DRAFT" in first:
            raise Refused("the protocol is not marked FROZEN")
        if PROTOCOL not in rec["pinned_sha256"]:
            raise Refused("the freeze record does not pin the protocol")
    if diff_listing(ws, rec["baseline"]) != rec["allowed_diff"]:
        raise Refused("code differs from the baseline by more than the allowed additions")
    if any(not x.startswith("A") for x in rec["allowed_diff"]):
        raise Refused("the allowed diff may only add files")
    h = sha256_file(p)
    try:
        verify_pinned(ws, rec)
    except PinnedDataChanged as exc:
        exc.rec, exc.rec_hash = rec, h
        raise
    return rec, h


def refuse_untrustworthy_git(ws: Workspace) -> None:
    """`git status` is evidence of a clean tree only if no GIT_* variable redirects it and no index entry hides changes."""
    redirect = sorted(k for k in os.environ if k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_COMMON_DIR",
                                                     "GIT_NAMESPACE", "GIT_CEILING_DIRECTORIES") or k.startswith("GIT_CONFIG"))
    if redirect:
        raise Refused(f"unset {redirect[0]}: git variables could hide the repository's state")
    hidden = [x[2:] for x in ws.git("ls-files", "-v").splitlines() if x[:1].islower() or x[:1] == "S"]
    if hidden:
        raise Refused(f"index flags hide changes to {hidden[0]} (assume-unchanged or skip-worktree)")
    scope = [t for t in DIFF_SCOPE if (ws.root / t).exists()]
    ignored = [x[3:] for x in ws.git("status", "--porcelain", "--ignored", "--untracked-files=all", "--", *scope).splitlines()
               if x.startswith("!! ") and not any(part in ("__pycache__", ".pytest_cache") for part in Path(x[3:]).parts)
               and not x.endswith((".pyc", ".DS_Store"))]
    if ignored:
        raise Refused(f"an ignored file sits in the close-out's scope: {ignored[0]}")


def unexpected_status(ws: Workspace, allowed: tuple[str, ...]) -> list[str]:
    """Paths in `git status` outside the allowed ones (whole repository, untracked files included)."""
    lines = [x[3:].strip().strip('"') for x in ws.git("-c", "status.showUntrackedFiles=all", "status", "--porcelain", "--untracked-files=all").splitlines() if x.strip()]
    return [x for x in lines if not any(x == a or x.startswith(a.rstrip("/") + "/") or a.startswith(x.rstrip("/") + "/") for a in allowed)]


def records_for_lineage(ws: Workspace) -> dict[str, dict]:
    """Every committed version of the freeze record, by the SHA-256 of its bytes."""
    out = {}
    for c in ws.git("log", "--format=%H", "--", FREEZE_RECORD).split():
        r = subprocess.run(["git", "show", f"{c}:{FREEZE_RECORD}"], cwd=ws.root, capture_output=True)
        if r.returncode == 0:
            out[hashlib.sha256(r.stdout).hexdigest()] = json.loads(r.stdout)
    return out


def authorisations(ev: list[dict]) -> dict[int, dict]:
    """The authorisation each attempt ran under: the last `authorised k` before `started k`, or, for an attempt not yet started, the
    last one so far. An `authorised k` after `started k` changes nothing: it is ignored, and stays visible in the ledger."""
    out: dict[int, dict] = {}
    started: set = set()
    for e in ev:
        if e["event"] == "started":
            started.add(e["n"])
        elif e["event"] == "authorised" and e["n"] not in started:
            out[e["n"]] = e
    return out


def verify_retry_lineage(ws: Workspace, ev: list[dict], n: int, rec: dict, rec_hash: str) -> None:
    """Retries cannot change research choices (section 6): an environment or integrity failure keeps the record; a close-out fix may
    change only added files' hashes, never a path, a baseline, a fit artifact or the input status."""
    if n == 1:
        return
    auth = authorisations(ev)
    failed = {e["n"]: e for e in ev if e["event"] == "failed"}
    recs = records_for_lineage(ws)
    first = recs.get(auth[1]["freeze_record_sha256"])
    if first is None:
        raise Refused("the first attempt's freeze record cannot be found")
    if failed[n - 1].get("failure_class") in ("environment", "integrity") and auth[n - 1]["freeze_record_sha256"] != rec_hash:
        raise Refused(f"an {failed[n - 1]['failure_class']} failure takes no new freeze record")
    if failed[n - 1].get("failure_class") not in ("environment", "integrity", "closeout"):
        raise Refused("the failed event has no failure class")
    added = {x.split("\t", 1)[1] for x in rec["allowed_diff"]}
    if rec["baseline"] != first["baseline"] or rec["allowed_diff"] != first["allowed_diff"] or set(rec["pinned_sha256"]) != set(first["pinned_sha256"]):
        raise Refused("a retry may not change the baseline, the allowed diff or the pinned paths")
    changed = {p for p, h in rec["pinned_sha256"].items() if first["pinned_sha256"][p] != h}
    if changed - added:
        raise Refused(f"a retry may not change {sorted(changed - added)[0]}")


def verify_environment(root: Path = ROOT) -> None:
    """Installed packages and Python match the pinned lock (section 2), and e001_discovery.json matches its frozen manifest."""
    lock = tomllib.loads((root / "uv.lock").read_text())
    norm = lambda s: s.lower().replace("_", "-").replace(".", "-")
    locked = {norm(p["name"]): p.get("version") for p in lock["package"] if p["name"] != "lpx"}
    for dist in importlib.metadata.distributions():
        name = norm(dist.metadata["Name"])
        if name != "lpx" and name in locked and locked[name] != dist.version:
            raise Refused(f"installed {name} {dist.version} differs from the lock {locked[name]}")
    pv = (root / ".python-version").read_text().strip()
    if not f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}".startswith(pv):
        raise Refused(f"Python differs from .python-version {pv}")
    man = json.loads((root / "results/e001/E001_frozen_manifest.json").read_text())
    if man["artifacts_sha256"]["e001_discovery.json"] != sha256_file(root / "results/e001/e001_discovery.json"):
        raise Refused("e001_discovery.json differs from its frozen manifest")


def check_guards(ws: Workspace, require_frozen_text: bool = True, required_pins: tuple[str, ...] = (),
                 expected: tuple[str, list[str]] | None = None, env_check=None) -> tuple[int, dict, str]:
    """Every refusal of section 6, in one place, before the first test-file read. Returns (attempt, record, record hash)."""
    if os.environ.get("LPX_ALLOW_DIRTY"):
        raise Refused("LPX_ALLOW_DIRTY must be unset")
    refuse_untrustworthy_git(ws)
    data_changed = False
    try:
        rec, rec_hash = verify_freeze(ws, require_frozen_text, expected)
    except PinnedDataChanged as exc:      # recorded by run_attempt as an integrity failure, once every other guard passes
        rec, rec_hash, data_changed = exc.rec, exc.rec_hash, True
    if env_check is not None and not data_changed:
        env_check()                       # with a pinned data file changed, nothing runs: the attempt is recorded as integrity first
    verify_ledger_history(ws)
    missing = [p for p in required_pins if p not in rec["pinned_sha256"]]
    if missing:
        raise Refused(f"the freeze record does not pin {missing[0]}")
    ev = ws.events()
    kinds = {(e["event"], e.get("n")) for e in ev}
    if any(e["event"] in ("completed", "closed") for e in ev):
        raise Refused("the close-out already completed or closed")
    open_auth = sorted({e["n"] for e in ev if e["event"] == "authorised" and ("started", e["n"]) not in kinds})
    if len(open_auth) != 1:
        raise Refused(f"exactly one authorised attempt is required, found {len(open_auth)}")
    n = open_auth[0]
    if n > MAX_ATTEMPTS or n < 1:
        raise Refused(f"attempt {n} is beyond the limit of {MAX_ATTEMPTS}")
    for k in range(1, n):
        if ("started", k) not in kinds or ("failed", k) not in kinds:
            raise Refused(f"attempt {k} has no started and failed events")
    auth = authorisations(ev)[n]                     # a mistaken record before the start is superseded, visibly
    if auth.get("freeze_record_sha256") != rec_hash:
        raise Refused("the authorised event names a different freeze record")
    verify_retry_lineage(ws, ev, n, rec, rec_hash)
    if ws.promoted.exists() or ws.staging.exists():
        raise Refused("results/closeout or results/closeout_staging already exists")
    listed = {}
    for e in ev:
        if e["event"] == "failed" and e.get("path"):
            listed[e["path"]] = e
    for d in sorted((ws.root / "results").glob("closeout_attempt*/")):
        rel = str(d.relative_to(ws.root))
        if rel not in listed:
            raise Refused(f"{rel} is not named in a failed event")
    for rel, e in listed.items():
        if not (ws.root / rel).is_dir() or tree_listing(ws.root / rel) != e["hashes"]:
            raise Refused(f"{rel} does not match its committed hashes")
    bad = unexpected_status(ws, tuple(listed) + data_scope(rec))
    if bad:
        raise Refused(f"the repository is not clean: {bad[:5]}")
    if not owner_line(ws, FREEZE_APPROVAL.format(h=rec_hash)):
        raise Refused(f"docs/DECISIONS.md has no committed owner line '{FREEZE_APPROVAL.format(h=rec_hash)}'")
    for e in ev:
        if e["event"] == "failed":
            try:
                software_experiments_of(ws, e)
            except (OSError, ValueError):
                raise Refused(f"attempt {e['n']}'s software statuses still cannot be read from its sealed directory: diagnose it before another attempt") from None
    return n, rec, rec_hash


def software_experiments_of(ws: Workspace, e: dict) -> list[str]:
    """A failed attempt's software-failed experiments. If they could not be read when the failure was recorded, they are read now from
    the sealed directory, whose hashes the failed event committed and the guards have just verified; a read error propagates."""
    if e.get("software_experiments") is not None:
        return e["software_experiments"]
    if not e.get("path"):
        return []
    d = ws.root / e["path"]
    if tree_listing(d) != e["hashes"]:
        raise ValueError(f"{e['path']} does not match its committed hashes")
    return software_statuses(d)


def owner_line(ws: Workspace, line: str) -> bool:
    """The exact line is in docs/DECISIONS.md as committed in HEAD, and the working copy equals HEAD."""
    r = subprocess.run(["git", "show", "HEAD:docs/DECISIONS.md"], cwd=ws.root, capture_output=True, text=True)
    p = ws.root / "docs/DECISIONS.md"
    return r.returncode == 0 and p.exists() and p.read_text() == r.stdout and any(x.strip() == line for x in r.stdout.splitlines())


# ------------------------------------------------------------------------------------------------ failure classification
def _frames(exc: BaseException) -> list:
    return [f.f_code for f, _ in traceback.walk_tb(exc.__traceback__)]


def _marked(code) -> bool:
    return code.co_qualname.split(".")[0].startswith("frozen_copy_")


def is_environment(exc: BaseException) -> bool:
    """A memory error, an interrupt, or an OSError from the system. A PermissionError is a frozen refusal only when lpx code raised it
    itself (its innermost frame is under lpx/). One from the operating system or a library, such as a denied write (polars sets no
    errno), is the environment's."""
    if isinstance(exc, PermissionError):
        if exc.errno is not None:
            return True
        frames = _frames(exc)
        return not (frames and (frames[-1].co_filename.startswith(str(ROOT / "lpx") + "/") or _marked(frames[-1])))
    return isinstance(exc, ENVIRONMENT)


def classify(exc: BaseException) -> str:
    """'integrity' (IntegrityFailure, including PinnedDataChanged), 'environment', 'software' (baseline frame or marked block, including
    its nested scopes) or 'closeout', from the innermost relevant frame."""
    if isinstance(exc, IntegrityFailure):
        return "integrity"
    if is_environment(exc):
        return "environment"
    lpx = str(ROOT / "lpx")
    rel = [c for c in _frames(exc) if c.co_filename.startswith(lpx) or _marked(c)]
    if not rel:
        return "closeout"
    if _marked(rel[-1]):
        return "software"
    return "closeout" if Path(rel[-1].co_filename).name in ADDED_LPX else "software"


def location(exc: BaseException) -> str:
    """The innermost project frame, and the last frame if that is a library's."""
    tb = traceback.extract_tb(exc.__traceback__)
    if not tb:
        return "unknown"
    lpx = [f for f in tb if f.filename.startswith(tuple(str(ROOT / d) + "/" for d in ("lpx", "tools", "tests")))]
    last = f"{Path(tb[-1].filename).name}:{tb[-1].lineno}"
    return last if not lpx or lpx[-1] is tb[-1] else f"{Path(lpx[-1].filename).name}:{lpx[-1].lineno} (raised at {last})"


# ------------------------------------------------------------------------------------------------ fit artifacts
def dump_json(path: Path, obj) -> None:
    """Deterministic serialisation: sorted keys, repr floats."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, sort_keys=True, indent=0))


def _model(d: dict | None) -> F.LinearModel | None:
    if d is None:
        return None
    return F.LinearModel(tuple(d["regressors"]), tuple(d["lo"]), tuple(d["hi"]), tuple(d["coef"]), tuple(d["trained_on"]), d["n_rows"])


def load_e003_fit(d: Path, horizons: list) -> tuple[dict, dict]:
    """(models by horizon and name, the artifact) from an e003_fit.json, in the shape of e003_models.json."""
    a = json.loads((d / "e003_fit.json").read_text())
    return {h: {m: _model(a[f"h{h:g}s_{m}"]) for m in ("M1", "M2")} for h in horizons}, a


def cell_fit_to_json(fit: E4.CellFit) -> dict:
    return {"groups": {f"{t}|{i}": v.tolist() for (t, i), v in fit.groups.items()},
            "lam": {f"{t}|{i}": v.tolist() for (t, i), v in fit.lam.items()},
            "beta": {t: [None if m is None else dataclasses.asdict(m) for m in g.models] for t, g in fit.beta.items()},
            "train_rows": fit.train_rows}


def cell_fit_from_json(a: dict) -> E4.CellFit:
    key = lambda s: tuple(s.split("|"))
    lam_order = [f"{t}|{i}" for t in FC.TARGETS for i in ("RF", "UA", "PL")]    # fit_cell's order: e004_lambda.csv depends on it
    if set(a["lam"]) != set(lam_order):
        raise RuntimeError("fit artifact holds other lambda keys than expected")
    return E4.CellFit({key(k): np.array(v, np.int64) for k, v in a["groups"].items()},
                      {key(k): np.array(a["lam"][k], float) for k in lam_order},
                      {t: FC.GroupModels(tuple(_model(m) for m in a["beta"][t])) for t in FC.TARGETS}, a["train_rows"])


def load_e004_fit(d: Path) -> tuple[dict, dict]:
    a = json.loads((d / "e004_fit.json").read_text())
    if set(a["cells"]) != set(CELL_ORDER):
        raise RuntimeError("fit artifact holds other cells than expected")
    return {c: cell_fit_from_json(a["cells"][c]) for c in CELL_ORDER}, a


# ------------------------------------------------------------------------------------------------ session context
@dataclasses.dataclass
class Ctx:
    mode: str
    out: Path
    rc: dict
    sessions: dict[str, list[str]]         # experiment -> sessions to run
    fit_dir: object                        # day -> directory of that session's fit artifacts
    expected_trained: object               # day -> the sessions its fits must have been trained on
    e003_ref: Path                         # directory of the E003 tables E004's identity checks compare with
    progress: object = print
    injection: tuple | None = None         # (stage, day or None, kind); never set in test mode
    recheck: object = None                 # end-of-run re-check of inputs and fits
    verify_for_analysis: object = None     # set by run_attempt: freeze record and metadata checks
    current: str | None = None             # the last session the experiment started, for the failure record
    trained: dict = dataclasses.field(default_factory=dict)
    statuses: dict = dataclasses.field(default_factory=dict)
    all_days: list = dataclasses.field(default_factory=list)
    check_inputs: object = None            # the pins check alone (IntegrityFailure); run before a failure is classified

    def __post_init__(self):
        if self.mode not in ("test", "dryrun", "rehearsal"):
            raise Refused(f"unknown mode {self.mode}")
        test = set(load_rc()["splits"]["test"])
        days = {d for v in self.sessions.values() for d in v}
        if self.mode != "test" and days & test:
            raise Refused("dry-run and rehearsal modes refuse every test day")
        if self.mode == "test" and not days <= test:
            raise Refused("test mode accepts only [splits].test")

    def hook(self, stage: str, day: str | None = None) -> None:
        self.current = day
        if self.injection is None:
            return
        if self.mode == "test":
            raise Refused("injection is not available in test mode")
        st, d, kind = self.injection
        if st == stage and (d is None or d == day):
            inject(kind)


def frozen_copy_injected_failure() -> None:
    raise AssertionError("injected failure in a marked block")


def inject(kind: str) -> None:
    """Synthetic failures for the rehearsal (never reachable in test mode)."""
    if kind == "death":
        os._exit(137)
    if kind == "permission":
        raise PermissionError("injected refusal")
    if kind == "environment":
        raise OSError("injected environment failure")
    if kind == "software":
        frozen_copy_injected_failure()
    if kind == "baseline":
        DG.inside(object(), None)                # raises inside baseline code
    if kind == "closeout":
        raise RuntimeError("injected close-out failure")
    raise ValueError(kind)


def split_of(rc: dict, d: str) -> str:
    return next(k for k in ("train", "validation", "test") if d in rc["splits"][k])


def write_status_sidecar(path: Path, status: str) -> None:
    path.with_name(path.name + ".status.json").write_text(json.dumps({"status": status}))


def check_trained(ctx: Ctx, d: str, art: dict) -> None:
    if list(art["sessions"]) != list(ctx.expected_trained(d)):
        raise RuntimeError(f"{d}: fit artifact trained on other sessions than expected")
    ctx.trained[d] = list(art["sessions"])


# ------------------------------------------------------------------------------------------------ E001
E001_KEEP = tuple(tomllib.loads((ROOT / "configs" / "closeout_v1.toml").read_text())["allow_list"]["e001_keys"])


def strip_intervals(rows: list[dict]) -> list[dict]:
    """Session-bootstrap intervals are not reported on five sessions (protocol section 4): dropped before any write."""
    return [{k: v for k, v in r.items() if k in E001_KEEP} for r in rows]


def frozen_copy_e001(cfg: dict, days: list[str], edges: tuple[float, float], hook) -> dict:
    """e001.run without its refusals, edge fitting, per-session block bootstrap, intervals and file writes."""
    S, Session, session_events, add_cells, summarize, PRIMARY, EXPLORATORY = (E1.S, E1.Session, E1.session_events, E1.add_cells,
                                                                               E1.summarize, E1.PRIMARY, E1.EXPLORATORY)
    e, sp = cfg["e001"], cfg["splits"]
    sym = cfg["dataset"]["symbol"]
    acc = json.loads((ROOT / "results" / "acceptance_001" / "summary.json").read_text())
    eligible = {r["day"] for r in acc["tardis"] if r["symbol"] == sym and r["eligibility"]["e001_eligible"]}
    hz, sec = e["horizons_s"], e["secondary_horizons_s"]
    all_h = hz + sec
    rng = np.random.default_rng(e["seed"])
    n_boot = e["bootstrap_resamples"]
    metrics = ["es"] + [f"mo_{h:g}s" for h in hz] + [f"rs_{h:g}s" for h in hz]
    wsens = pl.read_csv(ROOT / "results" / "acceptance_001" / "windows_sensitivity.csv").filter(pl.col("symbol") == sym)
    sessions = {}
    for d in days:
        hook("E001", d)
        sessions[d] = Session(sym, d)

    def evaluate(unit: str, timing: str, variant: str | None, day_subset: list[str]) -> pl.DataFrame:
        out = []
        for d in day_subset:
            if variant is None:
                w, base = S.load_windows(sym, d, "joint"), True
            else:
                w = wsens.filter((pl.col("day") == d) & (pl.col("variant") == variant)).select("start_us", "end_us").sort("start_us")
                base = False
            out.append(session_events(sessions[d], w, all_h, hz, unit=unit, timing=timing, baseline_windows=base))
        return pl.concat(out)

    prim_all = evaluate(e["unit_primary"], e["timing_primary"], None, days)
    prim_all = add_cells(prim_all, edges)
    prim = prim_all.filter(pl.col("primary"))
    if any(prim[m].is_nan().any() for m in metrics):
        raise AssertionError("primary events with a missing primary metric")
    res = {"experiment": "E001", "status": "observed", "symbol": sym, "sessions": days, "size_tercile_edges_base_qty": edges,
           "exclusions": {"primary": {k: int(v) for k, v in prim_all["reason"].value_counts().iter_rows()}},
           "events_total": prim_all.height, "events_primary": prim.height}
    pooled = summarize(prim, metrics, {"analysis": PRIMARY, "spec": "primary", "cell": "all"}, n_boot, rng)
    for c in e["conditioning"]:
        for val in sorted(prim[c].unique().to_list()):
            pooled += summarize(prim.filter(pl.col(c) == val), metrics,
                                {"analysis": PRIMARY, "spec": "primary", "cell": f"{c}={val}"}, n_boot, rng)
    per_session = []
    for d in days:
        f = prim.filter(pl.col("day") == d)
        row = {"analysis": PRIMARY, "day": d, "split": split_of({"splits": sp}, d), "events": f.height,
               "e001_eligible_posthoc": d in eligible, "excluded_events": int((prim_all["day"] == d).sum() - f.height)}
        for m in metrics:
            x = f[m].to_numpy()
            row.update({m: float(np.nanmean(x)) if np.any(~np.isnan(x)) else None})
        per_session.append(row)
    desc = {"secondary_horizons": [], "pre_state_age_ms_quantiles": {}}
    avail = prim_all.filter(~pl.col("reason").is_in(["t_outside_windows", "no_pre_state", "pre_state_record_invalid",
                                                      "pre_state_outside_windows", "pre_state_in_other_window"]))
    for h in sec:
        for m in (f"mo_{h:g}s", f"rs_{h:g}s"):
            per = avail.group_by("day").agg(pl.col(m).drop_nans().mean()).sort("day")[m].to_numpy().astype(float)
            desc["secondary_horizons"].append({"metric": m, "events": int(avail[m].drop_nans().len()),
                                               "mean_of_session_means": float(np.nanmean(per))})
    a = prim["pre_state_age_ms"]
    desc["pre_state_age_ms_quantiles"]["exchange (primary)"] = {str(q): float(a.quantile(q)) for q in (0.5, 0.9, 0.99)}
    pv = prim.filter(pl.col("touch_moved_next_state").is_not_nan()).group_by("qty_ge_touch").agg(
        pl.len().alias("events"), pl.col("touch_moved_next_state").mean().alias("share_touch_moved_next_state")).sort("qty_ge_touch")
    res["proxy_validation_qty_ge_touch"] = pv.to_dicts()
    sens_rows = []
    specs = [("unit=trade", "event unit", e["unit_sensitivity"][0], e["timing_primary"], None, days)]
    specs += [(f"timing={t}", "information clock", e["unit_primary"], t, None, days) for t in e["timing_sensitivity"]]
    specs += [("eligible_sessions_only(posthoc)", "session set", e["unit_primary"], e["timing_primary"], None, [d for d in days if d in eligible])]
    specs += [(f"windows:{v}", "validity windows", e["unit_primary"], e["timing_primary"], v, days) for v in e["window_variants"]]
    res["sensitivity_specs"] = []
    for name, factor, unit, timing, variant, dsub in specs:
        if name.startswith("eligible"):
            full = prim_all.filter(pl.col("day").is_in(dsub))
        else:
            full = evaluate(unit, timing, variant, dsub)
        frame = full.filter(pl.col("primary"))
        res["exclusions"][name] = {k: int(v) for k, v in full["reason"].value_counts().iter_rows()}
        res["sensitivity_specs"].append({"spec": name, "factor_changed": factor, "analysis": EXPLORATORY})
        sens_rows += summarize(frame, metrics, {"analysis": EXPLORATORY, "spec": name, "cell": "all"}, n_boot, rng)
        if timing != e["timing_primary"]:
            g = frame["pre_state_age_ms"]
            desc["pre_state_age_ms_quantiles"][timing] = {str(q): float(g.quantile(q)) for q in (0.5, 0.9, 0.99)}
    sens_rows += summarize(avail, metrics, {"analysis": EXPLORATORY, "spec": "available_case_per_horizon", "cell": "all"}, n_boot, rng)
    res["sensitivity_specs"].append({"spec": "available_case_per_horizon", "factor_changed": "event set per horizon",
                                     "analysis": EXPLORATORY})
    res["descriptive"] = desc
    res["primary"] = strip_intervals([r for r in pooled if r["cell"] == "all"])
    return {"res": res, "cells": strip_intervals(pooled), "per_session": per_session, "sensitivity": strip_intervals(sens_rows)}


def frozen_copy_e001_tables(r: dict, out: Path) -> None:
    """The file writes of e001.run, with close-out names."""
    (out / "e001_closeout.json").write_text(json.dumps(r["res"], indent=1))
    pl.DataFrame(r["cells"]).write_csv(out / "e001_cells.csv")
    pl.DataFrame(r["per_session"]).write_csv(out / "e001_per_session.csv")
    pl.DataFrame(r["sensitivity"]).write_csv(out / "e001_sensitivity.csv")


def run_e001(ctx: Ctx) -> list[Path]:
    days = ctx.sessions["E001"]
    disc = json.loads((ROOT / "results" / "e001" / "e001_discovery.json").read_text())
    r = frozen_copy_e001(ctx.rc, days, tuple(disc["size_tercile_edges_base_qty"]), ctx.hook)
    frozen_copy_e001_tables(r, ctx.out)
    out = [ctx.out / name for name in ("e001_closeout.json", "e001_cells.csv", "e001_per_session.csv", "e001_sensitivity.csv")]
    for q in out:
        write_status_sidecar(q, "observed")
    return out


# ------------------------------------------------------------------------------------------------ E002
def frozen_copy_e002(cfg: dict, rc: dict, days: list[str], hook) -> tuple[pl.DataFrame, pl.DataFrame]:
    """The session loop of e002.run; ``first_cap_bind_us`` was added after the E002 run and is not in its tables."""
    S, run_session, fee_overlay = E1.S, E2.run_session, E2.fee_overlay
    sym, tick = cfg["scope"]["symbol"], cfg["instrument"]["tick"]
    rows = []
    for d in days:
        hook("E002", d)
        st = pl.read_parquet(S.STATES / sym / f"{d}.parquet")
        valid = f"valid_{cfg['scope']['validity_layer']}"
        if not st.filter(pl.col(valid))["bbo_ok"].all():
            raise AssertionError(f"{d}: invalid record inside an accepted window")
        win = S.load_windows(sym, d, cfg["scope"]["validity_layer"])
        eps = episodes(win, cfg["scope"]["min_episode_s"])
        st = st.filter(pl.col(valid))
        tr = pl.read_parquet(E1.normalized_path("binance_vision", sym, "trades", d)).sort(["exch_us", "trade_id"])
        for r in run_session(to_states(st, tick), to_trades(tr, tick), eps, cfg):
            rows.append({"day": d, "split": split_of(rc, d), **r})
        print(f"{d}: {len(eps)} episodes", flush=True)
    gross = pl.DataFrame(rows).drop("first_cap_bind_us")
    net = fee_overlay(gross, cfg["fees"])
    return gross, net


def frozen_copy_e002_tables(gross: pl.DataFrame, net: pl.DataFrame, out: Path) -> None:
    """The file writes of e002.run."""
    gross.write_csv(out / "e002_gross_by_session.csv")
    net.write_csv(out / "e002_net_by_session.csv")


def run_e002(ctx: Ctx) -> list[Path]:
    cfg = tomllib.loads(E2.CONFIG.read_text())
    gross, net = frozen_copy_e002(cfg, ctx.rc, ctx.sessions["E002"], ctx.hook)
    frozen_copy_e002_tables(gross, net, ctx.out)
    out = [ctx.out / "e002_gross_by_session.csv", ctx.out / "e002_net_by_session.csv"]
    write_status_sidecar(out[0], "modeled historical replay")
    write_status_sidecar(out[1], "modeled historical replay; schedules other than vip0 are hypothetical")
    return out


# ------------------------------------------------------------------------------------------------ E003
def frozen_copy_e003(cfg: dict, ctx: Ctx, days: list[str]) -> tuple[list, list, list, dict, dict]:
    """The evaluation loop of e003.run, with M1/M2 and the volatility gate loaded instead of fitted."""
    fc = cfg["features"]
    gross, frows, cal, models_out, unrec = [], [], [], {}, {}
    for d in days:
        ctx.hook("E003", d)
        models, art = load_e003_fit(ctx.fit_dir(d), fc["horizons_s"])
        check_trained(ctx, d, art)
        rv_gate = art["rv_gate"]
        models_out[d] = {k: v for k, v in art.items() if k not in ("sessions", "before")}
        st, tr, eps = E3.load_session(cfg, d)
        ft = E3.features(cfg, st, tr, eps)
        unrec[d] = int(tr["recv_us"].null_count())
        fr, cl = E3.forecast_rows(d, ft, models, fc["primary_horizon_s"])
        frows += fr
        cal += cl
        states = to_states(st, cfg["instrument"]["tick"])
        E3.attach(states, ft, models[fc["primary_horizon_s"]], rv_gate)
        split = split_of(ctx.rc, d)
        for r in E3.run_session(states, to_trades(tr, cfg["instrument"]["tick"]), eps, cfg):
            gross.append({"day": d, "split": split, **r})
        print(f"{d}: evaluated ({len(eps)} episodes)", flush=True)
    return gross, frows, cal, models_out, unrec


def frozen_copy_e003_tables(cfg: dict, gross: list, frows: list, cal: list, models_out: dict, unrec: dict, out: Path) -> None:
    """The table construction and file writes of e003.run; its metadata field for trades without a receipt time becomes a file."""
    g = pl.DataFrame(gross, infer_schema_length=None)
    tables = {"e003_gross_by_session.csv": g, "e003_net_by_session.csv": E3.fee_overlay(g, cfg["fees"]),
              "e003_forecast_by_session.csv": pl.DataFrame(frows), "e003_calibration.csv": pl.DataFrame(cal)}
    for name, t in tables.items():
        t.write_csv(out / name)
    (out / "e003_models.json").write_text(json.dumps(models_out, indent=1))
    (out / "e003_trades_without_receipt_time.json").write_text(json.dumps(unrec, indent=1))


E003_STATUS = {"e003_gross_by_session.csv": "modeled historical replay", "e003_net_by_session.csv": "modeled historical replay; schedules other than vip0 are hypothetical",
               "e003_forecast_by_session.csv": "observed", "e003_calibration.csv": "observed", "e003_models.json": "observed", "e003_trades_without_receipt_time.json": "observed"}


def run_e003(ctx: Ctx) -> list[Path]:
    cfg = tomllib.loads(E3.CONFIG.read_text())
    gross, frows, cal, models_out, unrec = frozen_copy_e003(cfg, ctx, ctx.sessions["E003"])
    frozen_copy_e003_tables(cfg, gross, frows, cal, models_out, unrec, ctx.out)
    for name, status in E003_STATUS.items():
        write_status_sidecar(ctx.out / name, status)
    return [ctx.out / name for name in E003_STATUS]


# ------------------------------------------------------------------------------------------------ E004
def frozen_copy_e004_session(e4: dict, sc: dict, d: str, st, tr, eps, ft, models, rv_med, rv_gate, frozen_models, frozen_fc,
                             frozen_cal, frozen_gross, loaded_fits, reps, tick, frows, crows, drows, lrows, prows, wrows, inv) -> None:
    """One session of e004.run (the body between 'REF checks' and the policies' end), with lambda fits loaded."""
    t0 = time.time()
    check_models(d, models, rv_med, rv_gate, frozen_models)
    f_ref_all = check_ref_forecasts(d, ft, models, frozen_models, frozen_fc, frozen_cal)
    A = DG.from_frames(d, st, tr, eps, tick)
    el = ft["eligible"].to_numpy()
    y_k = ft["y_5s"].to_numpy()
    ref_mid, ref_spread = ft["mid_ticks"].to_numpy(), ft["spread"].to_numpy()
    m2 = models["M2"]

    # D0 through the participant path: identity
    D0, _, rec0, part0, b0, _ = cell_rows(e4, sc, A, "D0", "eval", 0, None)
    if not np.array_equal(part0["view_row"], A.rows) or not part0["has"].all():
        raise AssertionError("D0: j(k) must equal k")
    f_nv0 = m2.predict(xframe(part0)) * part0["has"]
    if not np.array_equal(f_nv0, f_ref_all) or any(not np.array_equal(part0[c], ft[c].to_numpy()) for c in F.REGRESSORS):
        raise AssertionError("D0: NV must equal REF bitwise")
    gap0 = DG.gap_flags(A, D0, D0.trade_ok, flow_window_us())
    tau_us = e4["indicators"]["tau_ms"] * 1000
    drows.append({"day": d, "cell": "D0", "replicate": 0, **D0.stats, "status": "synthetic",
                  "rows_eval": int(el.sum()), "rows_without_view": 0,
                  "age_ge_tau_share": float(np.mean(part0["age_us"][el] >= tau_us)),
                  "trade_gap_flag_share": float(np.mean(gap0[np.maximum(part0["pos"], 0)][el])),
                  **{f"bucket{b}_share": float(np.mean(b0[el] == b)) for b in range(5)}})
    fits = loaded_fits
    for cell, fit in fits.items():
        for (tgt, ind), lam in fit.lam.items():
            g = fit.groups.get((tgt, ind))
            for gi, lv in enumerate(lam):
                lrows.append({"day": d, "cell": cell, "target": tgt, "indicator": ind, "group": gi,
                              "buckets": "all" if g is None else ",".join(str(b) for b in np.flatnonzero(g == gi)),
                              "lambda": float(lv),
                              "train_rows": fit.train_rows[tgt], "status": "stress test"})

    # forecast level, every cell and its 3 evaluation draws
    keep_views = {}
    for cell in CELL_ORDER:
        fit = fits[cell]
        acc = {tgt: {} for tgt in FC.TARGETS}
        for r in reps:
            D, iv, rec, part, b_ua, b_pl = cell_rows(e4, sc, A, cell, "eval", r, "placebo_eval")
            f_nv = m2.predict(xframe(part)) * part["has"]
            yv = FC.y_view(A, part, y_k)
            if cell in POLICY_CELLS:
                keep_views[(cell, r)] = (D, m2.predict(pl.DataFrame({c: rec[c] for c in F.REGRESSORS})))
            mid_v = np.where(part["has"], part["view_mid_ticks"], ref_mid)
            spr_v = np.where(part["has"], part["spread"], ref_spread)
            for tgt, y in (("y_k", y_k), ("y_view", yv)):
                fs = {"REF": (f_ref_all, ref_mid, ref_spread),
                      **{m: (f, mid_v, spr_v) for m, f in model_forecasts(fit, tgt, part, f_nv, b_ua, b_pl).items()}}
                if cell == "D1_S" and tgt == "y_k":
                    keep_views[("lam", r)] = (fit.lam[(tgt, "UA")], fit.groups[(tgt, "UA")],
                                              fit.lam[(tgt, "PL")], fit.groups[(tgt, "PL")])
                if cell in ("D1_S1", "D1_S3"):
                    f1 = fits["D1_S"]
                    g = f1.groups[(tgt, "UA")]
                    fs["UA-lambda[D1_S]"] = (f1.lam[(tgt, "UA")][g[b_ua]] * f_nv, mid_v, spr_v)
                for m, (f, mm, ss) in fs.items():
                    a = acc[tgt].setdefault(m, {"y": [], "f": [], "mid": [], "spr": [], "b": []})
                    a["y"].append(y[el])
                    a["f"].append(f[el])
                    a["mid"].append(mm[el])
                    a["spr"].append(ss[el])
                    a["b"].append(b_ua[el])
            drows.append({"day": d, "cell": cell, "replicate": r, **D.stats, "status": "synthetic",
                          "rows_eval": int(el.sum()), "rows_without_view": int((~part["has"][el]).sum()),
                          "age_ge_tau_share": float(np.mean(part["age_us"][el] >= tau_us)),
                          "placebo_bucket_share_nonfresh": float(np.mean(b_pl[el] > 0)),
                          **{f"bucket{b}_share": float(np.mean(b_ua[el] == b)) for b in range(n_buckets(e4, cell))}})
        for tgt, ms in acc.items():
            for m, a in ms.items():
                y, f, mm, ss, bb = (np.concatenate(a[k]) for k in ("y", "f", "mid", "spr", "b"))
                frows.append({"day": d, "cell": cell, "target": tgt, "model": m, **FC.skill(y, f, mm, ss),
                              "replicates": len(a["y"]), "status": status_forecast(cell, m, tgt)})
                if m in ("REF", "NV", "UA-lambda"):
                    for b in np.unique(bb):
                        s = bb == b
                        crows.append({"day": d, "cell": cell, "target": tgt, "model": m, "bucket": int(b),
                                      "rows": int((s & ~np.isnan(y)).sum()), "slope": FC.calibration_slope(f[s], y[s]),
                                      "status": status_forecast(cell, m, tgt)})
    # H4-0: UA-lambda trained on D1-S, applied to clean rows (target y_k)
    f1 = fits["D1_S"]
    g = f1.groups[("y_k", "UA")]
    f_h40 = f1.lam[("y_k", "UA")][g[b0]] * f_ref_all
    for m, f in (("REF", f_ref_all), ("UA-lambda[D1_S]", f_h40)):
        frows.append({"day": d, "cell": "D0", "target": "y_k", "model": m,
                      **FC.skill(y_k[el], f[el], ref_mid[el], ref_spread[el]), "replicates": 1,
                      "status": status_forecast("D0", m)})
    print(f"{d}: forecasts ({time.time() - t0:.0f} s)", flush=True)

    # policies
    states = to_states(st, tick)
    E3.attach(states, ft, models, rv_gate)
    sd = E3.SessionData(states, to_trades(tr, tick), eps, sc)
    h0 = state_hash(sd.states, sd.trades)
    prim = sc["e004_primary"]
    scen = [prim] + [tuple(x) for x in e4["analysis"]["descriptive_scenarios"]]
    entry = sc["latency"][prim[1]]["entry_us"]
    h_us = int(e4["analysis"]["markout_s"] * 1e6)
    ref = {}
    for base in BASES:
        for model, lat in scen:
            agg, fills = E3.simulate(sd, base, model, lat, None)
            check_ref_policy(d, agg, frozen_gross)
            inv["ref_policy_rows_checked"] += 1
            ref[(base, model)] = (agg, fills)
            prows.append({"day": d, "cell": "REF", "replicate": 0, "base": base, "variant": "REF", **agg,
                          "status": STATUS_POLICY_REF})
    v0 = [PO.episode_views(sd.states, s0, D0.idx[p0:p1], D0.d[p0:p1], f_ref_all[o0:o1], md_us(sc), b)
          for (a, b), (s0, s1), (p0, p1), (o0, o1) in zip(A.eps, A.ep_states, D0.ep_pos, _offsets(A))]
    for base in BASES:
        agg, fills = E3.simulate(sd, base, *prim, None, views=v0)
        if not _agg_equal(agg, ref[(base, prim[0])][0]) or fills != ref[(base, prim[0])][1]:
            raise AssertionError(f"{d} {base}: D0 through the view path differs from REF")
        inv["d0_view_identity_jobs"] += 1
    for cell in POLICY_CELLS:
        pooled = {}
        for r in reps:
            D, f_rec = keep_views[(cell, r)]
            W = windows(e4, sc, sd, A, D, f_rec, cell, r)
            hv = views_hash(W.views)
            stall_iv = G.schedule(e4, cell, d, "eval", r) + md_us(sc)       # scheduled stalls, participant clock
            for base in BASES:
                jobs = [(prim, v) for v in VARIANTS]
                if cell == "D1_E" and r == 0:
                    jobs += [(sx, v) for sx in scen[1:] for v in VARIANTS]
                if cell == "D1_S" and base == "P3_M2":
                    jobs += [(prim, "N[UA-lambda]"), (prim, "N[PL-lambda]")]
                for (model, lat), var in jobs:
                    ust = {}
                    bpol = E3.make_policy(base, sc["policies"], None)
                    if var == "U":
                        pol = PO.withdraw_when_stale(bpol, W.vt, W.vte, tau_us, W.wu_full, ust)
                    elif var == "P":
                        pol = PO.withdraw_in_windows(bpol, W.wp, ust)
                    elif var == "N":
                        pol = bpol
                    else:
                        lam_ua, g_ua, lam_pl, g_pl = keep_views[("lam", r)]
                        if var == "N[UA-lambda]":
                            pol = p3_rescaled(sc["policies"], lam_ua, g_ua, e4["indicators"]["age_bucket_edges_s"],
                                              latest_age(W.vt, W.vte))
                        else:
                            Dp = DG.deliver(A, kind_of(e4, cell), G.schedule(e4, cell, d, "placebo_eval", r))
                            pt = Dp.d + md_us(sc)
                            pol = p3_rescaled(sc["policies"], lam_pl, g_pl, e4["indicators"]["age_bucket_edges_s"],
                                              latest_age(pt, A.te[Dp.idx]))
                    agg, fills = E3.simulate(sd, base, model, lat, None, pol=pol, views=W.views, extras=W.extras)
                    fa = PO.fill_arrays(fills, tick, eps)
                    p5, ok = PO.pi5(fa, eps, sd.t_states, sd.mid, h_us)
                    prows.append({"day": d, "cell": cell, "replicate": r, "base": base, "variant": var, **agg,
                                  "pi5_usdt": float(p5[ok].sum()), "pi5_notional": float((fa["px"] * fa["qty"])[ok].sum()),
                                  "pi5_fills_excluded": int((~ok).sum()),
                                  "u_or_p_decisions": ust.get("decisions"), "u_or_p_withdrawn": ust.get("withdrawn"),
                                  "superseded_state_decisions": ust.get("superseded_state"),
                                  "status": STATUS_POLICY_DEG})
                    if var != "N":
                        continue
                    key = (base, model, lat)
                    P = pooled.setdefault(key, {"reps": 0, "span": 0, "wu": 0, "wp": 0, "ov": 0, "redraws": 0,
                                                "max_redraws": 0, "excluded": 0, "wu_nostall": 0, "wp_install": 0,
                                                "excluded_fills": 0, "n_notional": 0.0, "hours": 0.0,
                                                **{w: {"pi5": 0.0, "notional": 0.0, "orders": set(), "fills": 0}
                                                   for w in ("U", "P", "U_stall", "P_stall", "U_nostall", "P_install")}})
                    st_hit = overlaps_any(W.wu_spells, stall_iv)
                    sel = {"U": W.wu, "P": W.wp, "U_stall": G.merge(W.wu_spells[st_hit]),
                           "P_stall": G.merge(W.wp_images[st_hit]), "U_nostall": G.merge(W.wu_spells[~st_hit])}
                    wp_in = _intersect(W.wp, stall_iv)
                    sel["P_install"] = wp_in
                    for w, spells in sel.items():
                        s = window_sums(fa, p5, ok, spells, entry, r)
                        P[w]["pi5"] += s["pi5"]
                        P[w]["notional"] += s["notional"]
                        P[w]["orders"] |= s["orders"]
                        P[w]["fills"] += s["fills"]
                    P["reps"] += 1
                    P["span"] += W.span_us
                    P["wu"] += int((W.wu[:, 1] - W.wu[:, 0]).sum())
                    P["wp"] += int((W.wp[:, 1] - W.wp[:, 0]).sum())
                    P["ov"] += overlap_us(W.wp, W.wu)
                    P["redraws"] += W.redraws
                    P["max_redraws"] = max(P["max_redraws"], W.max_redraws)
                    P["excluded"] += W.excluded
                    P["wu_nostall"] += int((sel["U_nostall"][:, 1] - sel["U_nostall"][:, 0]).sum())
                    P["wp_install"] += int((wp_in[:, 1] - wp_in[:, 0]).sum())
                    P["excluded_fills"] += int((~ok).sum())
                    P["n_notional"] += float((fa["px"] * fa["qty"])[ok].sum())
                    P["hours"] += agg["valid_hours"]
            if views_hash(W.views) != hv:
                raise AssertionError("view states were mutated")
        for (base, model, lat), P in pooled.items():
            q = {w: (1e4 * P[w]["pi5"] / P[w]["notional"] if P[w]["notional"] > 0 else None) for w in P if isinstance(P[w], dict)}
            wrows.append({"day": d, "cell": cell, "base": base, "fill_model": model, "latency": lat, "replicates": P["reps"],
                          "q_U_bp": q["U"], "q_P_bp": q["P"],
                          "D_W_bp": q["P"] - q["U"] if None not in (q["P"], q["U"]) else None,
                          "orders_U": len(P["U"]["orders"]), "orders_P": len(P["P"]["orders"]),
                          "fills_U": P["U"]["fills"], "fills_P": P["P"]["fills"],
                          "notional_U": P["U"]["notional"], "notional_P": P["P"]["notional"],
                          "pi5_U_usdt": P["U"]["pi5"], "pi5_P_usdt": P["P"]["pi5"],
                          "n_notional_defined": P["n_notional"], "n_valid_hours": P["hours"],
                          "withdrawn_share": P["wu"] / P["span"], "wp_share": P["wp"] / P["span"],
                          "overlap_share_of_wp": P["ov"] / P["wp"] if P["wp"] else None,
                          "q_U_stall_bp": q["U_stall"], "q_P_stall_bp": q["P_stall"],
                          "D_W_stall_bp": q["P_stall"] - q["U_stall"] if None not in (q["P_stall"], q["U_stall"]) else None,
                          "orders_U_stall": len(P["U_stall"]["orders"]), "orders_P_stall": len(P["P_stall"]["orders"]),
                          "wu_time_share_nostall": P["wu_nostall"] / P["wu"] if P["wu"] else None,
                          "wu_fill_share_nostall": P["U_nostall"]["fills"] / P["U"]["fills"] if P["U"]["fills"] else None,
                          "wp_time_share_install": P["wp_install"] / P["wp"] if P["wp"] else None,
                          "wp_fill_share_install": P["P_install"]["fills"] / P["P"]["fills"] if P["P"]["fills"] else None,
                          "placebo_redraws": P["redraws"], "placebo_max_redraws": P["max_redraws"],
                          "episodes_excluded": P["excluded"], "fills_beyond_episode_end": P["excluded_fills"],
                          "status": STATUS_POLICY_DEG})
    if state_hash(sd.states, sd.trades) != h0:
        raise AssertionError("the exchange-side states or trades were mutated")
    print(f"{d}: policies ({time.time() - t0:.0f} s)", flush=True)


def frozen_copy_e004_tables(sc: dict, frows, crows, drows, lrows, prows, wrows) -> dict:
    gross = pl.DataFrame(prows, infer_schema_length=None)
    net = E3.fee_overlay(gross, sc["fees"]).with_columns(
        pl.when(pl.col("fee_schedule") == "vip0").then(pl.col("status"))
        .otherwise(pl.col("status") + pl.lit("; hypothetical fees")).alias("status"))
    tables = {"e004_forecast_by_session.csv": pl.DataFrame(frows, infer_schema_length=None),
              "e004_calibration.csv": pl.DataFrame(crows, infer_schema_length=None),
              "e004_degradation_by_session.csv": pl.DataFrame(drows, infer_schema_length=None),
              "e004_lambda.csv": pl.DataFrame(lrows, infer_schema_length=None),
              "e004_policy_gross_by_session.csv": gross, "e004_policy_net_by_session.csv": net,
              "e004_windows_by_session.csv": pl.DataFrame(wrows, infer_schema_length=None)}
    return tables


def frozen_copy_e004(e4: dict, sc: dict, ctx: Ctx, days: list[str]) -> dict:
    fm = json.loads((ctx.e003_ref / "e003_models.json").read_text())
    gross_tab = pl.read_csv(ctx.e003_ref / "e003_gross_by_session.csv", infer_schema_length=None)
    fc_tab = pl.read_csv(ctx.e003_ref / "e003_forecast_by_session.csv", infer_schema_length=None)
    cal_tab = pl.read_csv(ctx.e003_ref / "e003_calibration.csv", infer_schema_length=None)
    reps = range(e4["seeds"]["eval_replicates"])
    tick = sc["instrument"]["tick"]
    frows, crows, drows, lrows, prows, wrows, inv = [], [], [], [], [], [], {"ref_policy_rows_checked": 0, "d0_view_identity_jobs": 0}
    for d in days:
        ctx.hook("E004", d)
        models_all, art3 = load_e003_fit(ctx.fit_dir(d), [5])
        check_trained(ctx, d, art3)
        loaded_fits, art4 = load_e004_fit(ctx.fit_dir(d))
        check_trained(ctx, d, art4)
        st, tr, eps = E3.load_session(sc, d)
        ft = E3.features(sc, st, tr, eps)
        frozen_copy_e004_session(e4, sc, d, st, tr, eps, ft, models_all[5], art3["rv_60s_training_median"], art3["rv_gate"], fm, fc_tab,
                                 cal_tab, gross_tab, loaded_fits, reps, tick, frows, crows, drows, lrows, prows, wrows, inv)
    return {"tables": frozen_copy_e004_tables(sc, frows, crows, drows, lrows, prows, wrows), "invariants": inv}


def frozen_copy_e004_write(r: dict, out: Path) -> None:
    """The file writes of e004.run; its metadata field for the invariants becomes a file."""
    for name, t in r["tables"].items():
        t.write_csv(out / name)
    (out / "e004_invariants.json").write_text(json.dumps(r["invariants"]))


def run_e004(ctx: Ctx) -> list[Path]:
    e4, sc = E4.load_cfg()
    r = frozen_copy_e004(e4, sc, ctx, ctx.sessions["E004"])
    frozen_copy_e004_write(r, ctx.out)
    return [ctx.out / name for name in r["tables"]] + [ctx.out / "e004_invariants.json"]


RUNNERS = {"E001": run_e001, "E002": run_e002, "E003": run_e003, "E004": run_e004}


# ------------------------------------------------------------------------------------------------ the attempt
class Streams:
    """Sends stdout, stderr, warnings and anything written to file descriptors 1 and 2 (native panics, child processes) to the
    sealed log; the console keeps only progress lines."""

    def __init__(self, log: Path):
        sys.stdout.flush()
        sys.stderr.flush()
        self.saved_fds = (os.dup(1), os.dup(2))
        self.console = os.fdopen(os.dup(self.saved_fds[0]), "w", buffering=1)
        self.log = open(log, "a", buffering=1)
        self.saved = (sys.stdout, sys.stderr)
        os.dup2(self.log.fileno(), 1)
        os.dup2(self.log.fileno(), 2)
        sys.stdout = sys.stderr = self.log

    def progress(self, msg: str) -> None:
        print(msg, file=self.console, flush=True)

    def close(self) -> None:
        """Always restores descriptors 1 and 2 and the Python streams, even if the log cannot be flushed."""
        try:
            self.log.flush()
            self.console.flush()
        finally:
            os.dup2(self.saved_fds[0], 1)
            os.dup2(self.saved_fds[1], 2)
            for fd in self.saved_fds:
                os.close(fd)
            sys.stdout, sys.stderr = self.saved
            for f in (self.console, self.log):
                try:
                    f.close()
                except OSError:
                    pass


def run_experiments(ctx: Ctx, runners: dict, progress, no_retry: dict | None = None) -> dict:
    """Each experiment writes into its own directory, moved into staging only when it completes. A software exception makes the
    experiment (and those depending on it) not confirmable, with nothing written; it gets no retry in a later attempt. Any other
    exception propagates and fails the attempt."""
    statuses = ctx.statuses
    staging = ctx.out
    for exp in EXPERIMENTS:
        t0 = time.time()
        blocked = [x for x in DEPENDS.get(exp, ()) if statuses[x]["status"] != "complete"]
        ctx.current = None
        if no_retry and exp in no_retry:
            statuses[exp] = {"status": "not_confirmable_software", "reason": f"software exception in attempt {no_retry[exp]}; no retry"}
        elif blocked:
            statuses[exp] = {"status": "not_confirmable_software", "reason": f"depends on {blocked[0]}"}
        elif not ctx.sessions[exp]:
            statuses[exp] = {"status": "complete", "outputs": {}, "note": "no valid session"}
        else:
            tmp = staging / f".writing_{exp}"
            tmp.mkdir()
            ctx.out = tmp
            try:
                paths = runners[exp](ctx)
                outputs = {p.name: sha256_file(p) for p in paths}
                for p in sorted(tmp.iterdir()):
                    p.rename(staging / p.name)
                statuses[exp] = {"status": "complete", "outputs": outputs}
            except BaseException as exc:      # noqa: BLE001 - classified; environment and close-out failures re-raise
                if classify(exc) != "software":
                    raise
                stop = None
                if ctx.check_inputs is not None:
                    try:
                        ctx.check_inputs()      # bytes changed under the experiment: the attempt fails as integrity, with no software record
                    except IntegrityFailure:
                        raise
                    except KeyboardInterrupt as interrupt:
                        stop = interrupt        # an operator's interrupt: the software record is written first, then it ends the attempt
                    except Exception:           # noqa: BLE001 - a check that cannot run leaves the software status and its no-retry record
                        pass
                # the last session the experiment started; the exception may come from later work in the same experiment
                statuses[exp] = {"status": "not_confirmable_software", "exception": type(exc).__name__, "location": location(exc), "last_session_started": ctx.current}
                write_atomic(staging / f"closeout_status_{exp}.json", statuses[exp])      # first: a dead log or a cleanup failure keeps the no-retry record
                if stop is not None:
                    raise stop
                quietly(lambda: print(traceback.format_exc(), flush=True))
                for p in tmp.iterdir():
                    p.unlink()
            finally:
                ctx.out = staging
            tmp.rmdir()
        write_atomic(staging / f"closeout_status_{exp}.json", statuses[exp])
        progress(f"{exp}: {'done' if statuses[exp]['status'] == 'complete' else 'not confirmable'} ({time.time() - t0:.0f} s)")
    return statuses


def durable_write(path: Path, text: str) -> None:
    """Write, fsync, rename and fsync the directory, so a crash leaves the old state or the whole file."""
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w") as f:
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_atomic(path: Path, obj) -> None:
    durable_write(path, json.dumps(obj, indent=1, sort_keys=True))


def write_exclusive(path: Path, text: str) -> None:
    """All or nothing, and never over an existing file: a crash leaves no record, and a second run is refused."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.tmp{os.getpid()}")
    try:
        with open(tmp, "w") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.link(tmp, path)
    except FileExistsError:
        raise Refused(f"{path.name} already exists and is never overwritten") from None
    finally:
        tmp.unlink(missing_ok=True)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def software_statuses(d: Path) -> list[str]:
    """Experiments a sealed attempt marked not confirmable (software): names only, from its status files; no table is read."""
    out = []
    for e in EXPERIMENTS:
        p = d / f"closeout_status_{e}.json"
        if not p.exists():
            continue
        if json.loads(p.read_text()).get("exception"):        # a read error propagates: --recover repeats this step
            out.append(e)
    return out


def fail_attempt(ws: Workspace, n: int, exc_type: str, loc: str | None, failure_class: str, integrity: dict | None = None) -> None:
    """Rename unread and commit `failed`; the third failure closes the evaluation."""
    d = ws.attempt_dir(n)
    if ws.staging.exists():
        ws.staging.rename(d)
    rel = str(d.relative_to(ws.root)) if d.exists() else None
    hashes = tree_listing(d) if d.exists() else {}
    if not any(e["event"] == "failed" and e["n"] == n for e in ws.events()):
        soft: list | None = []
        if d.exists():
            for _ in range(2):
                try:
                    soft = software_statuses(d)
                    break
                except (OSError, ValueError):
                    soft = None        # recorded as unknown: the next start is refused until the owner diagnoses it
        ws.append({"event": "failed", "n": n, "path": rel, "hashes": hashes, "exception": exc_type, "location": loc, "failure_class": failure_class,
                   "sealed_log_sha256": hashes.get("closeout.log"), "software_experiments": soft, **({"integrity": integrity} if integrity else {})})
    if n >= MAX_ATTEMPTS:
        close_terminal(ws)


def close_terminal(ws: Workspace) -> None:
    """Fail closed (section 6): no analysis, no partial label; a fallback report from no sealed table."""
    from lpx.research.closeout_analysis import fallback_report

    ws.promoted.mkdir(parents=True, exist_ok=True)
    p = ws.promoted / "CLOSEOUT_report.md"
    durable_write(p, fallback_report(events_with_commits(ws)))
    if not any(e["event"] == "closed" for e in ws.events()):
        ws.append({"event": "closed", "report_sha256": sha256_file(p)})


def promote_and_report(ws: Workspace) -> None:
    """Only the primary analysis is promoted or rendered: its hashes must equal the `completed` event's."""
    from lpx.research.closeout_analysis import render_report

    comp = [e for e in ws.events() if e["event"] == "completed"][-1]
    d = ws.staging if ws.staging.exists() and not ws.promoted.exists() else ws.promoted
    if sha256_file(d / "closeout_analysis.json") != comp["analysis_sha256"] or sha256_file(d / "closeout_meta.json") != comp["meta_sha256"]:
        raise Refused("the analysis or metadata differs from the completed event")
    if d == ws.staging:
        ws.staging.rename(ws.promoted)
    a = json.loads((ws.promoted / "closeout_analysis.json").read_text())
    durable_write(ws.promoted / "CLOSEOUT_report.md", render_report(a, events_with_commits(ws)))


def verify_run_scope(ws: Workspace, start_head: str) -> None:
    """Section 6, step 2: commits since the start touch the ledger only, and tracked paths are clean."""
    if subprocess.run(["git", "merge-base", "--is-ancestor", start_head, "HEAD"], cwd=ws.root).returncode:
        raise Refused("history changed during the run")
    touched = {x for x in ws.git("log", "--format=", "--name-only", f"{start_head}..HEAD").splitlines() if x}
    if touched - {LEDGER}:
        raise Refused(f"a commit during the run touched {sorted(touched - {LEDGER})[0]}")
    scope = sorted({*TRACKED_SCOPE, *DIFF_SCOPE} & {p.name for p in ws.root.iterdir()})
    if scope and ws.git("status", "--porcelain", "--", *scope).strip():
        raise Refused("tracked paths changed during the run")


def run_attempt(ws: Workspace, make_ctx, runners: dict, analyse, require_frozen_text: bool = True, required_pins: tuple[str, ...] = (),
                expected: tuple[str, list[str]] | None = None, env_check=None) -> dict:
    """One guarded test-path invocation: guards, `started`, experiments, metadata, analysis, `completed`, promotion, report."""
    if getattr(make_ctx, "mode", None) == "test" and (ws.root.resolve() != ROOT.resolve() or not require_frozen_text or not set(TEST_MODE_PINS) <= set(required_pins)
                                                      or expected is None or env_check is None):
        raise Refused("a test-mode context runs only in the project repository with every test-mode guard")
    lock_path = ws.root / ".git" / "closeout.lock"
    lock = open(lock_path, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise Refused("another close-out process is running") from None
    n, rec, rec_hash = check_guards(ws, require_frozen_text, required_pins, expected, env_check)
    no_retry = {x: e["n"] for e in ws.events() if e["event"] == "failed" for x in software_experiments_of(ws, e)}
    changed = pinned_data_findings(ws, rec)
    if getattr(make_ctx, "unread", False) and not changed:
        raise Refused("a pinned data file differed when the run began and no longer does: start again, so the input-status record is read")
    ws.append({"event": "started", "n": n})
    if changed:
        # a pinned data file changed after the freeze: an integrity failure of this attempt, recorded before anything is read (section 6)
        print(f"attempt failed: PinnedDataChanged ({len(changed)} pinned data file(s) differ from the freeze record)", flush=True)
        fail_attempt(ws, n, "PinnedDataChanged", "the freeze record's pins", "integrity", {"findings": changed})
        return {"attempt": n, "outcome": "failed", "class": "integrity"}
    start_head = ws.git("rev-parse", "HEAD").strip()
    ws.staging.mkdir(parents=True)
    streams = Streams(ws.staging / "closeout.log")
    ctx = None
    try:
        ctx = make_ctx(ws.staging, streams.progress)
        if ctx.check_inputs is not None:
            inner = ctx.check_inputs
            ctx.check_inputs = lambda: collect_findings(lambda: verify_pinned(ws, rec), inner)        # the pinned data files too (section 6)
        statuses = run_experiments(ctx, runners, streams.progress, no_retry)
        ctx.hook("meta")
        verify_pinned(ws, rec)
        verify_run_scope(ws, start_head)
        if env_check is not None:
            env_check()
        if ctx.recheck is not None:
            ctx.recheck()
        tables = {p.name: sha256_file(p) for p in sorted(ws.staging.iterdir()) if p.is_file() and p.name not in ("closeout.log", ".DS_Store")}
        write_atomic(ws.staging / "closeout_meta.json", {"attempt": n, "freeze_record_sha256": rec_hash, "mode": ctx.mode, "statuses": statuses,
                                                         "tables_sha256": tables, "sessions": ctx.sessions, "trained_on": ctx.trained})

        def verify_for_analysis(meta: dict) -> None:
            verify_pinned(ws, rec)
            if sha256_file(ws.root / FREEZE_RECORD) != rec_hash or meta["freeze_record_sha256"] != rec_hash or meta["attempt"] != n or meta["mode"] != ctx.mode:
                raise RuntimeError("the metadata or freeze record does not match this attempt")
            for d, s in meta["trained_on"].items():
                if list(s) != list(ctx.expected_trained(d)):
                    raise RuntimeError(f"{d}: trained-on sessions differ")

        ctx.verify_for_analysis = verify_for_analysis
        ctx.hook("analysis")
        result = analyse(ws.staging, ctx)
        write_atomic(ws.staging / "closeout_analysis.json", {**result, "meta_sha256": sha256_file(ws.staging / "closeout_meta.json")})
    except BaseException as exc:      # noqa: BLE001 - every failure before the analysis file is a failed attempt
        if complete_analysis(ws.staging):
            # the analysis file is complete (the failure came during its directory fsync): not a failed attempt; --recover takes branch 1
            quietly(streams.close)
            raise
        quietly(lambda: print(traceback.format_exc(), flush=True))
        built = getattr(make_ctx, "check_inputs", None)
        kind, integrity, name, loc = failure_record(exc, inputs_behind(ctx, exc, fallback=lambda: collect_findings(lambda: verify_pinned(ws, rec), built or (lambda: None))))
        if integrity is not None and not isinstance(exc, IntegrityFailure):
            quietly(lambda: print(f"the pinned inputs no longer hold, so the failure is recorded as integrity: {integrity}", flush=True))
        quietly(lambda: streams.progress(f"attempt failed: {name} at {loc}"))
        quietly(streams.close)
        fail_attempt(ws, n, name, loc, kind, integrity)
        return {"attempt": n, "outcome": "failed", "class": kind}
    streams.close()
    # after this point a failure is not a failed attempt: --recover repeats these steps from the primary analysis
    ctx.hook("after_analysis")
    ws.append({"event": "completed", "n": n, "analysis_sha256": sha256_file(ws.staging / "closeout_analysis.json"),
               "meta_sha256": sha256_file(ws.staging / "closeout_meta.json")})
    promote_and_report(ws)
    return {"attempt": n, "outcome": "completed", "statuses": statuses}


def inputs_behind(ctx, exc: BaseException, fallback=None) -> IntegrityFailure | None:
    """After any failure, the pins are checked once more (section 6): an input missing or changed since the start is recorded as the cause,
    whatever exception surfaced, and an integrity failure's own findings are completed with every other one. An operator's interrupt is
    not checked, and a check that cannot run leaves the failure as it was. Without a context (it failed while being built) the fallback
    check runs: the freeze record's pinned data files."""
    check = ctx.check_inputs if ctx is not None and ctx.check_inputs is not None else fallback
    if isinstance(exc, KeyboardInterrupt) or check is None:
        return None
    try:
        check()
    except IntegrityFailure as found:
        if isinstance(exc, IntegrityFailure):
            return IntegrityFailure(exc.findings + [f for f in found.findings if f not in exc.findings])
        return found
    except BaseException:      # noqa: BLE001 - the original failure is recorded
        return None
    return None


def failure_record(exc: BaseException, found: IntegrityFailure | None) -> tuple[str, dict | None, str, str | None]:
    """(class, integrity record, exception name, location) of a failed attempt, as plain values: an exception kept in a local of
    run_attempt would hold its frame, and the close-out lock, in a reference cycle."""
    err = exc if isinstance(exc, IntegrityFailure) or found is None else found          # an integrity failure keeps its own name and place
    kind = classify(err) if classify(err) in ("environment", "integrity") else "closeout"
    return kind, ((found or err).record() if isinstance(err, IntegrityFailure) else None), type(err).__name__, location(err)


def quietly(fn) -> None:
    """Best effort inside the failure handler: a sealed log that cannot be written must not stop the failure from being recorded."""
    try:
        fn()
    except Exception:      # noqa: BLE001
        pass


def complete_analysis(staging: Path) -> bool:
    """True if staging holds a whole closeout_analysis.json bound to the metadata beside it (recovery branch 1's test)."""
    an, meta = staging / "closeout_analysis.json", staging / "closeout_meta.json"
    if not (an.exists() and meta.exists()):
        return False
    try:
        parsed = json.loads(an.read_text())
    except ValueError:
        return False
    return isinstance(parsed, dict) and parsed.get("meta_sha256") == sha256_file(meta)


def restore_ledger_tail(ws: Workspace) -> None:
    """Section 6: an event counts only once in HEAD. Remove a stale index lock and drop one uncommitted appended tail line."""
    lock = ws.root / ".git" / "index.lock"
    if lock.exists():
        lock.unlink()
    head = subprocess.run(["git", "show", f"HEAD:{LEDGER}"], cwd=ws.root, capture_output=True, text=True)
    head_text = head.stdout if head.returncode == 0 else ""
    if not ws.ledger.exists():
        return
    now = ws.ledger.read_text()
    if now == head_text:
        ws.git("reset", "-q", "--", LEDGER, check=False)
        return
    if not now.startswith(head_text) or now[len(head_text):].rstrip("\n").count("\n") > 0:
        raise Refused("the ledger differs from HEAD by more than one appended line")
    if head.returncode == 0:
        ws.git("reset", "-q", "--", LEDGER)
        ws.ledger.write_text(head_text)
    else:
        ws.git("reset", "-q", "--", LEDGER, check=False)
        ws.ledger.unlink()


def recover(ws: Workspace) -> str:
    """`closeout.py --recover` (section 6). Chooses a branch from file existence and hashes only; reads no test table."""
    lock = open(ws.root / ".git" / "closeout.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise Refused("the attempt's process is still running") from None
    restore_ledger_tail(ws)
    verify_ledger_history(ws)
    ev = ws.events()
    started = [e["n"] for e in ev if e["event"] == "started"]
    if not started:
        raise Refused("nothing to recover")
    n = max(started)
    done = {(e["event"], e.get("n")) for e in ev}
    closed = any(e["event"] == "closed" for e in ev)
    report = ws.promoted / "CLOSEOUT_report.md"
    if ("completed", n) in done:
        if report.exists() and report.stat().st_size > 0:
            raise Refused("nothing to recover")
    elif ("failed", n) in done:
        if n < MAX_ATTEMPTS or closed:
            raise Refused("nothing to recover")
    try:
        rec, _ = verify_freeze(ws, False)
        changed = []
    except PinnedDataChanged as exc:          # recovery reads no test table: a data change does not block it, and is recorded below
        rec, changed = exc.rec, exc.findings
    if FIT_MANIFEST in rec["pinned_sha256"] and current_sha256(ws.root / FIT_MANIFEST) == rec["pinned_sha256"][FIT_MANIFEST]:
        try:
            check_fit_manifest(ws.root / "results" / "closeout_fits")
        except IntegrityFailure as exc:
            changed = changed + exc.findings
    allowed = (STAGING, f"results/closeout_attempt{n}", PROMOTED, *(e["path"] for e in ev if e["event"] == "failed" and e.get("path")), *data_scope(rec))
    bad = unexpected_status(ws, allowed)
    if bad:
        raise Refused(f"the repository is not clean: {bad[:5]}")
    an = ws.staging / "closeout_analysis.json"
    meta = ws.staging / "closeout_meta.json"
    noted = [e for e in ev if e["event"] == "integrity_noted" and e.get("n") == n]
    if changed and (("completed", n) in done or ("failed", n) in done or complete_analysis(ws.staging)) and not any(x["integrity"]["findings"] == changed for x in noted):
        # the analysis (if any) was made while every pin held; the difference found now is recorded, then the branch proceeds
        ws.append({"event": "integrity_noted", "n": n, "reason": "a pinned data file differs at recovery, after the attempt's own checks",
                   "integrity": {"findings": changed}})
    if ("completed", n) in done:
        promote_and_report(ws)
        return "repeated promotion and report"
    if ("failed", n) in done:                  # n == 3, not yet closed
        close_terminal(ws)
        return "closed"
    if complete_analysis(ws.staging):
        ws.append({"event": "completed", "n": n, "analysis_sha256": sha256_file(an), "meta_sha256": sha256_file(meta)})
        promote_and_report(ws)
        return "completed from the primary analysis"
    fail_attempt(ws, n, "process death", None, "integrity" if changed else "environment", {"findings": changed} if changed else None)
    return "closed" if n >= MAX_ATTEMPTS else f"attempt {n} failed"


def report_fix(ws: Workspace) -> str:
    """Section 6: re-render after a report-rendering fix in the added files; the primary analysis never changes. Every changed path
    must be an added close-out file, and the diff goes into the ledger and the run history."""
    lock = open(ws.root / ".git" / "closeout.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        raise Refused("another close-out process is running") from None
    verify_ledger_history(ws)
    ev = ws.events()
    comp = [e for e in ev if e["event"] == "completed"]
    if not comp or not (ws.promoted / "closeout_analysis.json").exists():
        raise Refused("no completed close-out to re-render")
    refuse_untrustworthy_git(ws)
    sealed = tuple(e["path"] for e in ev if e["event"] == "failed" and e.get("path"))
    bad = unexpected_status(ws, (PROMOTED, *sealed))
    if bad:
        raise Refused(f"a report fix renders committed code only; uncommitted: {bad[:5]}")
    rec = json.loads((ws.root / FREEZE_RECORD).read_text())
    auth = [e for e in ev if e["event"] == "authorised"][-1]
    if sha256_file(ws.root / FREEZE_RECORD) != auth["freeze_record_sha256"]:
        raise Refused("the freeze record differs from the authorised one")
    added = {x.split("\t", 1)[1] for x in rec["allowed_diff"]}
    diff = [x for x in ws.git("diff", "--name-status", rec["parent_commit"], "HEAD", "--", *DIFF_SCOPE).splitlines() if x.strip()]
    paths = []
    for x in diff:
        st, p = x.split("\t", 1)
        if not st.startswith("M") or p not in added:
            raise Refused(f"a report fix may only modify added close-out files: {x}")
        paths.append(p)
    if not paths:
        raise Refused("no committed report-rendering change to apply")
    for p, h in rec["pinned_sha256"].items():          # every pinned file outside the added files is as frozen
        if p not in added and (not (ws.root / p).exists() or sha256_file(ws.root / p) != h):
            raise Refused(f"pinned file differs from the freeze record: {p}")
    text = ws.git("diff", rec["parent_commit"], "HEAD", "--", *DIFF_SCOPE)
    ws.append({"event": "report_fix", "commit": ws.git("rev-parse", "HEAD").strip(), "paths": paths, "diff_sha256": hashlib.sha256(text.encode()).hexdigest()})
    promote_and_report(ws)
    return "report re-rendered"


def record_log_opening(ws: Workspace, n: int, reason: str) -> None:
    """Section 6: a sealed log is opened only to diagnose a failure, and the opening is a committed event. Call before opening it."""
    if not any(e["event"] == "failed" and e["n"] == n for e in ws.events()):
        raise Refused(f"attempt {n} has no failed event: its log stays sealed")
    ws.append({"event": "log_opened", "n": n, "reason": reason})


def flag_compromised(ws: Workspace, scope, reason: str, corrected: dict | None = None) -> None:
    """Section 6: a compromised flag sits on top of labels. It is a committed event and never changes closeout_analysis.json."""
    ws.append({"event": "compromised", "scope": scope, "reason": reason, "corrected": corrected or {}})
    if (ws.promoted / "closeout_analysis.json").exists():
        promote_and_report(ws)


# ------------------------------------------------------------------------------------------------ test-mode wiring
def load_rc() -> dict:
    return tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())


INPUT_NAMES = ("states", "book", "trades", "receipts")


def input_paths(sym: str, day: str) -> dict[str, Path]:
    """Every input file of a session. The state file has no acceptance hash: it is pinned by the input-status record."""
    return {"states": E1.S.STATES / sym / f"{day}.parquet", "book": E1.normalized_path("tardis", sym, "book", day),
            "trades": E1.normalized_path("binance_vision", sym, "trades", day), "receipts": E1.normalized_path("tardis", sym, "trades", day)}


ACCEPTANCE_AUDITED = ("book", "trades", "receipts")


def acceptance_dir() -> Path:
    return ROOT / "results" / "acceptance_001"


MISSING_RECHECKS, MISSING_RECHECK_DELAY_S = 3, 1.0     # a file absent at first is looked for again before it counts as missing


def sentinel_inputs(sym: str) -> list[Path]:
    """The inputs of the first discovery session: present whenever the data volume is whole."""
    rc = tomllib.loads((ROOT / "configs" / "research_v1.toml").read_text())
    return list(input_paths(sym, sorted(rc["splits"]["train"])[0]).values())


def require_data_roots(sym: str, day: str) -> None:
    """A missing data directory is a disk or mount problem, never a missing input of one session."""
    for p in input_paths(sym, day).values():
        if not p.parent.is_dir():
            raise NotADirectoryError(f"data directory absent: {p.parent}")


def require_whole_volume(sym: str) -> None:
    """Consulted only when an input is missing: if the discovery inputs are gone too (an unmounted disk leaving a stub tree), the
    volume is incomplete, which is not a missing input of one session."""
    for p in sentinel_inputs(sym):
        if not p.is_file():
            raise FileNotFoundError(errno.ENOENT, "a discovery input is absent too: the data volume is incomplete", str(p))


def acceptance_record(rc: dict, days: list[str]) -> dict[str, dict]:
    """The acceptance run's input hashes for the listed sessions. Only these leave this function: the rest of summary.json, which
    holds diagnostics of every session, is dropped here, unused. A summary that is not the run of record is no session's fault."""
    acc = json.loads((acceptance_dir() / "summary.json").read_text())
    if acc["provenance"]["git_commit"] != rc["dataset"]["acceptance_git_commit"] or acc["provenance"]["git_dirty"]:
        raise RuntimeError("results/acceptance_001 is not the acceptance run of record named in research_v1.toml")
    sym = rc["dataset"]["symbol"]
    return {r["day"]: r["normalized_inputs_sha256"] for r in acc["tardis"] if r["symbol"] == sym and r["day"] in days}


def input_mismatch(sym: str, day: str, recorded: dict | None) -> tuple[str | None, dict[str, str]]:
    """(the reason code of a genuine input problem or None, the hashes computed). A genuine problem is a missing file under a present
    directory, a hash differing from the acceptance run's, or no acceptance hash. Every other exception propagates and aborts."""
    require_data_roots(sym, day)
    paths, hashes = input_paths(sym, day), {}
    for name, p in paths.items():
        for k in range(MISSING_RECHECKS + 1):
            try:
                hashes[name] = sha256_file(p)
                break
            except FileNotFoundError:
                if p.is_symlink():                  # a dangling link points at storage that is not there: not a missing input
                    raise
                require_data_roots(sym, day)
                require_whole_volume(sym)
                if k == MISSING_RECHECKS:
                    return f"input_missing:{name}", hashes
                time.sleep(MISSING_RECHECK_DELAY_S)
    if recorded is None:
        return "acceptance_record_missing", hashes
    for name in ACCEPTANCE_AUDITED:
        want = recorded.get(str(paths[name].relative_to(ROOT)))
        if want is None:
            return f"acceptance_hash_missing:{name}", hashes
        if want != hashes[name]:
            return f"hash_mismatch:{name}", hashes
    return None, hashes


def verify_acceptance_run_of_record(rc: dict) -> None:
    """The run-wide provenance checks the frozen verifiers also make. Made here first, so a run-wide fault aborts instead of reaching the
    verifiers, where it would count as a mismatch of every session."""
    for f in ("summary.json", "sensitivity.json"):
        prov = json.loads((acceptance_dir() / f).read_text())["provenance"]
        if prov["git_commit"] != rc["dataset"]["acceptance_git_commit"] or prov["git_dirty"]:
            raise RuntimeError(f"results/acceptance_001/{f} is not from the acceptance run of record")


def frozen_verifier_result(exc: BaseException) -> bool:
    """True only for the mismatch the frozen verifiers raise themselves: exactly RuntimeError or KeyError, from their own frame."""
    frames = _frames(exc)
    return type(exc) in (RuntimeError, KeyError) and bool(frames) and frames[-1] in (E1.verify_inputs.__code__, E3.verify_receipt_inputs.__code__)


def pin_findings(rc: dict, day: str, status: dict) -> list[dict]:
    """Every pinned input of a session the record does not mark undefined: present as a file, pinned, and hashing to its pin. Returns
    the findings (empty when all hold). Reads bytes for hashes only; an unreadable file (an OSError other than not-found) propagates."""
    if status.get("undefined"):
        return []
    pinned, out = status.get("sha256") or {}, []
    for name, p in input_paths(rc["dataset"]["symbol"], day).items():
        if name not in pinned:
            out.append(integrity_finding(day, name, "not pinned by the input-status record"))
        elif not p.is_file():
            out.append(integrity_finding(day, name, "missing"))
        else:
            try:
                h = sha256_file(p)
            except FileNotFoundError:
                out.append(integrity_finding(day, name, "missing"))             # gone between the stat and the read
                continue
            if h != pinned[name]:
                out.append(integrity_finding(day, name, "modified", h))
    return out


def collect_findings(*checks) -> None:
    """Run every check; raise one IntegrityFailure with the findings of all of them. A check that cannot run re-raises its own exception
    only when no other check found anything (a finding is the recorded cause)."""
    found: list[dict] = []
    error: BaseException | None = None
    for check in checks:
        try:
            check()
        except IntegrityFailure as exc:
            found += [f for f in exc.findings if f not in found]
        except KeyboardInterrupt:
            raise
        except Exception as exc:          # noqa: BLE001 - re-raised below unless a finding takes precedence
            error = error or exc
    if found:
        raise IntegrityFailure(found)
    if error is not None:
        raise error


def verify_pins(rc: dict, days: list[str], input_status: dict) -> None:
    """The pins check of section 1 over every session with a record: IntegrityFailure with all findings, or nothing."""
    found = [f for d in days if input_status.get(d) is not None for f in pin_findings(rc, d, input_status[d])]
    if found:
        raise IntegrityFailure(found)


def verify_session_inputs(rc: dict, day: str, status: dict | None) -> str | None:
    """Input rule at the run (section 1). With the input-status record (`status`), every pinned input must be present with exactly its
    pinned bytes, or IntegrityFailure fails the attempt; no session is excluded for it. The one session-level verdict left is the frozen
    verifiers' own mismatch on bytes that match their pins (the state file's footer provenance, checked here by the owner's choice): the
    reason a session is undefined, or None. Without a record (unit tests only; stand-ins carry a record) the pre-check's rule applies. Any other
    exception, such as a disk or memory error or an unexpected software failure, propagates as a failed attempt."""
    sym = rc["dataset"]["symbol"]
    if status is not None and status.get("undefined"):
        return f"undefined (input: {status['reason']})" if status.get("reason") else "undefined (input)"
    if status is not None:
        # after the freeze the record is the reference: a missing input, or bytes other than the pinned ones, fail the attempt
        verify_pins(rc, [day], {day: status})
    else:
        reason, _ = input_mismatch(sym, day, acceptance_record(rc, [day]).get(day))
        if reason:
            return f"undefined (input mismatch: {reason})"
    verify_acceptance_run_of_record(rc)
    try:
        E1.verify_inputs(rc, [day])
        E3.verify_receipt_inputs(tomllib.loads(E3.CONFIG.read_text()), [day])
    except BaseException as exc:      # noqa: BLE001 - everything but the verifiers' own mismatch re-raises
        if not frozen_verifier_result(exc):
            raise
        return "undefined (input mismatch: frozen_verifier)"
    return None


def relative_ticks(rc: dict, days: list[str]) -> dict[str, float]:
    """The relative tick of each session (bp), from the first touch of its valid states; reported next to bp results."""
    out = {}
    for d in days:
        st = pl.read_parquet(E1.S.STATES / rc["dataset"]["symbol"] / f"{d}.parquet", columns=["bid1_px", "ask1_px", "valid_joint"]).filter(pl.col("valid_joint"))
        if st.height:
            out[d] = float(1e4 * 0.01 / ((st["bid1_px"] + st["ask1_px"]) / 2).mean())
    return out


def check_fit_manifest(fits_root: Path) -> None:
    """Every fit artifact, and nothing else, matches the pinned manifest (which the freeze record pins). The artifacts are inputs of the
    run: a difference is an integrity failure (section 6), with one finding per differing path."""
    manifest = json.loads((fits_root / "MANIFEST.json").read_text())
    now = {k: v for k, v in tree_listing(fits_root).items() if k != "MANIFEST.json"}
    found = [integrity_finding(None, f"{fits_root.name}/{k}", "missing" if k not in now else "modified" if k in manifest else "not in the pinned manifest", now.get(k))
             for k in sorted(set(manifest) | set(now)) if manifest.get(k) != now.get(k)]
    if found:
        raise IntegrityFailure(found)


def session_context(root: Path, mode: str, days: list[str], fit_set: str, trained: list[str], input_status: dict, injection=None, sessions: dict | None = None):
    """The context used in test mode and, with other sessions and fits, in the rehearsal. Fit artifacts are checked here and again
    at the end of the run; E003's references come from staging."""
    if mode == "test" and Path(root).resolve() != ROOT.resolve():
        raise Refused("test mode runs only in the project repository")
    test = set(load_rc()["splits"]["test"])
    every = set(days) | {d for v in (sessions or {}).values() for d in v}
    if mode != "test" and every & test:
        raise Refused("dry-run and rehearsal modes refuse every test day")
    if mode == "test" and not every <= test:
        raise Refused("test mode accepts only [splits].test")
    fits_root = ROOT / "results" / "closeout_fits" if mode != "test" else root / "results" / "closeout_fits"

    def check_fits() -> None:
        check_fit_manifest(fits_root)

    def make(out: Path, progress) -> Ctx:
        if mode == "test":
            ev = Workspace(ROOT).events()            # the project's own ledger, whatever repository a caller passed to run_attempt
            if not ev or ev[-1]["event"] != "started":
                raise Refused("test-day inputs are read only inside a started attempt of the project's ledger (run_attempt)")
        rc = load_rc()

        def pins() -> None:
            collect_findings(check_fits, lambda: verify_pins(rc, days, input_status))      # every finding of the fits and every session at once
        pins()
        e4, _ = E4.load_cfg()
        E4.verify_schedules(e4, days, e4["seeds"]["eval_replicates"])
        undefined = {d: r for d in days if (r := verify_session_inputs(rc, d, input_status[d]))}
        valid = {}
        no_unit: dict[str, dict] = {}
        for exp in EXPERIMENTS:
            key = "e001_valid" if exp == "E001" else "episode_valid"
            valid[exp] = [d for d in days if d not in undefined and input_status[d][key]]
            for d in days:
                if d not in undefined and d not in valid[exp]:
                    no_unit.setdefault(d, {})[exp] = input_status[d].get("e001_reason" if exp == "E001" else "episode_reason", "no valid unit")
        (out / "closeout_input_status.json").write_text(json.dumps({"undefined": undefined, "no_valid_unit": no_unit}, indent=1))
        (out / "closeout_relative_tick.json").write_text(json.dumps(relative_ticks(rc, [d for d in days if d not in undefined and input_status[d].get("e001_valid")]), indent=1))
        first = dict(undefined)

        def recheck() -> None:
            pins()
            again = {d: r for d in days if (r := verify_session_inputs(rc, d, input_status[d]))}
            if first != again:
                raise RuntimeError("inputs changed during the run")

        return Ctx(mode, out, rc, sessions or valid, lambda d: fits_root / fit_set, lambda d: trained, out, progress, injection, recheck=recheck,
                   check_inputs=pins, all_days=list(days))
    make.mode = mode
    # the pins check, also for a failure while the context is being built (run_attempt's fallback); reads only inside a started attempt
    make.check_inputs = lambda: collect_findings(lambda: check_fit_manifest(fits_root), lambda: verify_pins(load_rc(), days, input_status))
    return make


def test_context(root: Path):
    """Test mode: exactly [splits].test, the all-15 artifacts, E003 references from staging."""
    if Path(root).resolve() != ROOT.resolve():
        raise Refused("test mode runs only in the project repository")
    rc = load_rc()
    disc = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    record = json.loads((root / INPUT_STATUS).read_text())
    verify_input_status_record(Workspace(root), record, rc["splits"]["test"])
    make = session_context(root, "test", rc["splits"]["test"], "all15", disc, record["sessions"])
    return make


def unread_test_context():
    """Test mode when a pinned data file differs: the record cannot be trusted, so it is not read; run_attempt fails the attempt first."""
    def make(out: Path, progress) -> Ctx:
        raise Refused("a pinned data file differs from the freeze record; nothing is read")
    make.mode = "test"
    make.unread = True
    return make


NO_UNIT_REASONS = ("no_accepted_joint_windows", "no_qualifying_episodes")
AUTHORISATION = "results/closeout_freeze/precheck_authorisation.json"


def verify_input_status_record(ws: Workspace, record: dict, days: list[str]) -> None:
    """The record must come from step 3 itself, and be internally consistent: test mode; the committed authorisation's hash; a full commit
    SHA that is an ancestor of HEAD; the windows and acceptance files it read, unchanged; exactly the test days; and per session, only
    section 1's codes, with `undefined` and the validity flags agreeing with them, and a SHA-256 for each of the four inputs of every
    session that is not undefined."""
    prov = record.get("provenance") or {}
    if prov.get("mode") != "test":
        raise Refused("the input-status record was not made by an authorised step 3")
    auth = ws.root / AUTHORISATION
    if not auth.exists() or prov.get("authorisation_sha256") != sha256_file(auth):
        raise Refused("the input-status record does not name the committed step-3 authorisation")
    commit = prov.get("git_commit") or ""
    if len(commit) != 40 or subprocess.run(["git", "merge-base", "--is-ancestor", commit, "HEAD"], cwd=ws.root, capture_output=True).returncode:
        raise Refused("the input-status record names no commit that is an ancestor of HEAD")
    if prov.get("windows_csv_sha256") != sha256_file(ws.root / "results/acceptance_001/windows.csv") \
            or prov.get("acceptance_summary_sha256") != sha256_file(ws.root / "results/acceptance_001/summary.json"):
        raise Refused("windows.csv or summary.json changed since the input-status record was made")
    if sorted(record.get("sessions", {})) != sorted(days):
        raise Refused("the input-status record does not hold exactly the test sessions")
    for d, s in record["sessions"].items():
        if not isinstance(s, dict) or not isinstance(s.get("sha256") or {}, dict):
            raise Refused(f"{d}: the session's entry is malformed")
        reason = s.get("reason")
        if reason is not None and not reason.startswith(INPUT_REASONS):
            raise Refused(f"{d}: reason {reason!r} is not one of section 1's codes")
        if bool(s.get("undefined")) != (reason is not None):
            raise Refused(f"{d}: 'undefined' disagrees with its reason")
        pins = s.get("sha256") or {}
        if not s.get("undefined") and (sorted(pins) != sorted(INPUT_NAMES) or not all(isinstance(h, str) and len(h) == 64 and set(h) <= set("0123456789abcdef") for h in pins.values())):
            raise Refused(f"{d}: the record does not pin exactly the session's four inputs")      # a record defect: refused before any attempt
        for flag, key in (("e001_valid", "e001_reason"), ("episode_valid", "episode_reason")):
            code = s.get(key)
            if code is not None and not (code.startswith(INPUT_REASONS) or code in NO_UNIT_REASONS):
                raise Refused(f"{d}: {key} {code!r} is not one of section 1's codes")
            if bool(s.get(flag)) != (code is None):
                raise Refused(f"{d}: {flag} disagrees with {key}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--test-sessions", action="store_true", help="run the guarded close-out on the sealed sessions")
    ap.add_argument("--recover", action="store_true", help="recover after a process death")
    ap.add_argument("--report-fix", action="store_true", help="re-render the report after a listed report-rendering fix")
    ap.add_argument("--log-opening", nargs=2, metavar=("ATTEMPT", "REASON"), help="record that a failed attempt's sealed log will be opened")
    args = ap.parse_args()
    ws = Workspace(ROOT)
    if args.recover:
        print(recover(ws))
        return
    if args.report_fix:
        print(report_fix(ws))
        return
    if args.log_opening:
        record_log_opening(ws, int(args.log_opening[0]), args.log_opening[1])
        return
    if not args.test_sessions:
        ap.error("--test-sessions or --recover is required")
    from lpx.research.closeout_analysis import analyse

    # the guards run first: nothing below reads a test-day file until they pass
    try:
        verify_freeze(ws, True, (BASELINE, ALLOWED_DIFF))
        make = test_context(ROOT)
    except PinnedDataChanged:
        make = unread_test_context()           # run_attempt records the integrity failure before calling it
    r = run_attempt(ws, make, RUNNERS, analyse, required_pins=TEST_MODE_PINS, expected=(BASELINE, ALLOWED_DIFF), env_check=verify_environment)
    print(json.dumps({k: v for k, v in r.items() if k != "statuses"}))


if __name__ == "__main__":
    try:
        main()
    except Refused as e:
        raise SystemExit(f"refused: {e}") from None
