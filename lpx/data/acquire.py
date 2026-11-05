"""Raw data acquisition with provenance.

Every downloaded file is written atomically under ``data/raw/<source>/``, hashed with SHA-256,
verified against a publisher checksum when one exists, and appended to ``data/raw/manifest.jsonl``.
Re-running is idempotent: a file whose on-disk hash matches its manifest entry is skipped.

Usage::

    uv run python -m lpx.data.acquire --config configs/acquisition_001.toml [--source tardis]
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import sys
import tomllib
from dataclasses import asdict, dataclass
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
MANIFEST = RAW / "manifest.jsonl"
USER_AGENT = "liquidity-lab-research/0.1 (academic, non-commercial)"
CHUNK = 1 << 20


@dataclass(frozen=True)
class Target:
    source: str
    url: str
    rel_path: str  # relative to data/raw
    expected_sha256: str | None = None
    checksum_origin: str | None = None  # where expected_sha256 came from
    checksum_url: str | None = None  # publisher checksum file to fetch at download time


@dataclass
class ManifestEntry:
    source: str
    url: str
    rel_path: str
    bytes: int
    sha256: str
    retrieved_at_utc: str
    http_status: int
    etag: str | None
    last_modified: str | None
    content_type: str | None
    checksum_origin: str | None
    checksum_verified: bool | None


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def load_manifest() -> dict[str, dict]:
    if not MANIFEST.exists():
        return {}
    out: dict[str, dict] = {}
    for line in MANIFEST.read_text().splitlines():
        if line.strip():
            rec = json.loads(line)
            out[rec["rel_path"]] = rec  # last write wins
    return out


def _append_manifest(entry: ManifestEntry) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("a") as f:
        f.write(json.dumps(asdict(entry), sort_keys=True) + "\n")


def fetch(client: httpx.Client, t: Target, manifest: dict[str, dict]) -> ManifestEntry | None:
    dest = RAW / t.rel_path
    prior = manifest.get(t.rel_path)
    if dest.exists() and prior and sha256_file(dest) == prior["sha256"]:
        return None  # already acquired and unchanged

    expected = t.expected_sha256
    if t.checksum_url:
        r = client.get(t.checksum_url)
        r.raise_for_status()
        expected = r.text.split()[0].strip().lower()

    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + ".part")
    h = hashlib.sha256()
    n = 0
    with client.stream("GET", t.url) as r:
        r.raise_for_status()
        with part.open("wb") as f:
            for block in r.iter_bytes(CHUNK):
                f.write(block)
                h.update(block)
                n += len(block)
        status, headers = r.status_code, r.headers
    digest = h.hexdigest()
    verified = None if expected is None else (digest == expected)
    if verified is False:
        part.unlink()
        raise RuntimeError(f"checksum mismatch for {t.url}: got {digest}, expected {expected}")
    os.replace(part, dest)
    entry = ManifestEntry(
        source=t.source,
        url=t.url,
        rel_path=t.rel_path,
        bytes=n,
        sha256=digest,
        retrieved_at_utc=dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        http_status=status,
        etag=headers.get("etag"),
        last_modified=headers.get("last-modified"),
        content_type=headers.get("content-type"),
        checksum_origin=t.checksum_origin,
        checksum_verified=verified,
    )
    _append_manifest(entry)
    return entry


# --------------------------------------------------------------------------- target builders


def tardis_targets(cfg: dict) -> list[Target]:
    out = []
    for d in cfg["dates"]:
        y, m, day = d.split("-")
        for dtype in cfg["data_types"]:
            for sym in cfg["symbols"]:
                url = f"{cfg['base_url']}/{cfg['exchange']}/{dtype}/{y}/{m}/{day}/{sym}.csv.gz"
                rel = f"tardis/{cfg['exchange']}/{dtype}/{d}/{sym}.csv.gz"
                out.append(Target("tardis", url, rel))
    return out


def hf_targets(cfg: dict, client: httpx.Client) -> list[Target]:
    repo, rev = cfg["repo"], cfg["revision"]
    r = client.get(f"https://huggingface.co/api/datasets/{repo}/tree/{rev}", params={"recursive": "true", "expand": "true"})
    r.raise_for_status()
    out = []
    for item in r.json():
        if item.get("type") != "file":
            continue
        path = item["path"]
        if not (path in cfg["include_docs"] or any(path.startswith(p) for p in cfg["include_prefixes"])):
            continue
        lfs = item.get("lfs") or {}
        out.append(
            Target(
                source="hf_lobstream",
                url=f"https://huggingface.co/datasets/{repo}/resolve/{rev}/{path}",
                rel_path=f"hf_lobstream/{rev[:12]}/{path}",
                expected_sha256=lfs.get("oid"),
                checksum_origin="hf_lfs_oid" if lfs.get("oid") else None,
            )
        )
    return out


def binance_vision_targets(cfg: dict) -> list[Target]:
    out = []
    for sym in cfg["symbols"]:
        for d in cfg["dates"]:
            name = f"{sym}-trades-{d}.zip"
            url = f"{cfg['base_url']}/{sym}/{name}"
            out.append(
                Target(
                    source="binance_vision",
                    url=url,
                    rel_path=f"binance_vision/spot/daily/trades/{sym}/{name}",
                    checksum_origin="binance_CHECKSUM",
                    checksum_url=url + ".CHECKSUM",
                )
            )
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--config", default=str(ROOT / "configs" / "acquisition_001.toml"))
    ap.add_argument("--source", choices=["tardis", "hf_lobstream", "binance_vision"], action="append")
    args = ap.parse_args(argv)
    cfg = tomllib.loads(Path(args.config).read_text())
    sources = args.source or ["binance_vision", "tardis", "hf_lobstream"]

    manifest = load_manifest()
    failures = 0
    with httpx.Client(headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=httpx.Timeout(60.0, read=300.0)) as client:
        targets: list[Target] = []
        if "tardis" in sources:
            targets += tardis_targets(cfg["tardis"])
        if "hf_lobstream" in sources:
            targets += hf_targets(cfg["hf_lobstream"], client)
        if "binance_vision" in sources:
            targets += binance_vision_targets(cfg["binance_vision"])
        for i, t in enumerate(targets, 1):
            try:
                e = fetch(client, t, manifest)
                msg = "skip (present)" if e is None else f"{e.bytes / 1e6:9.1f} MB  verified={e.checksum_verified}"
            except Exception as exc:  # report and continue; failures are listed, never silently ignored
                failures += 1
                msg = f"FAILED: {exc!r}"
            print(f"[{i}/{len(targets)}] {t.rel_path}: {msg}", flush=True)
    print(f"done; failures={failures}", flush=True)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
