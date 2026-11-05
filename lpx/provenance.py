"""Run provenance: immutable source revision, input fingerprints, and a clean-tree guard for official artifacts.

Every result written under ``results/`` or ``data/derived/`` records ``provenance()``. Official runs refuse to start
from a working tree with uncommitted changes to code, configs or tests (set ``LPX_ALLOW_DIRTY=1`` for exploratory runs;
the artifact then records ``git_dirty: true`` and must not be cited as evidence).
"""

from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACKED_SCOPE = ("lpx", "configs", "tests", "pyproject.toml", "uv.lock", ".python-version")


def code_fingerprint() -> str:
    """SHA-256 (first 16 hex) over every lpx/*.py path and content — the algorithm used since Test 001."""
    h = hashlib.sha256()
    for p in sorted((ROOT / "lpx").rglob("*.py")):
        h.update(p.relative_to(ROOT).as_posix().encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:16]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def git_revision() -> tuple[str, bool]:
    """(HEAD commit, whether code/config/test files differ from it)."""
    commit = _git("rev-parse", "HEAD")
    dirty = bool(_git("status", "--porcelain", "--", *TRACKED_SCOPE))
    return commit, dirty


def provenance(configs: list[str]) -> dict:
    commit, dirty = git_revision()
    manifest = ROOT / "data" / "raw" / "manifest.jsonl"
    return {
        "git_commit": commit,
        "git_dirty": dirty,
        "code_fingerprint": code_fingerprint(),
        "configs": {c: sha256_file(ROOT / c) for c in configs},
        "raw_manifest_sha256": sha256_file(manifest) if manifest.exists() else None,
    }


def require_clean() -> None:
    _, dirty = git_revision()
    if dirty and os.environ.get("LPX_ALLOW_DIRTY") != "1":
        raise SystemExit("uncommitted changes to code/configs/tests: commit first (or LPX_ALLOW_DIRTY=1 for a "
                         "non-citable exploratory run)")
