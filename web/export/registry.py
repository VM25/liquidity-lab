"""Source registry for the website exporter: the only files it may read, and how a source pointer resolves.

Standard library only. Nothing here writes to the research tree. Held-out values may come only from the frozen
close-out analysis and pre-outcome metadata (WEBSITE_PLAN section 7.4); the per-session held-out tables in
results/closeout/*.csv are deliberately not registered.
"""

import csv
import hashlib
import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SOURCES = {
    "e001": ("results/e001/e001_discovery.json", "discovery"),
    "e001_expl_paired": ("results/e001/e001_exploratory_paired.csv", "discovery"),
    "e001_expl_weight": ("results/e001/e001_exploratory_weighting.csv", "discovery"),
    "e002": ("results/e002/e002_h2.json", "discovery"),
    "e002_net": ("results/e002/e002_net_by_session.csv", "discovery"),
    "e003": ("results/e003/e003_analysis.json", "discovery"),
    "e003_net": ("results/e003/e003_net_by_session.csv", "discovery"),
    "e004": ("results/e004/e004_analysis.json", "discovery"),
    "close": ("results/closeout/closeout_analysis.json", "heldout_analysis"),
    "close_e001": ("results/closeout/e001_closeout.json", "heldout_analysis"),
    "close_meta": ("results/closeout/closeout_meta.json", "heldout_analysis"),
    "ledger": ("results/closeout_attempts.jsonl", "heldout_metadata"),
    "input_status": ("results/closeout_freeze/input_status.json", "heldout_metadata"),
    "cfg_e002": ("configs/e002_v1.toml", "parameters"),
    "cfg_e003": ("configs/e003_v1.toml", "parameters"),
    "cfg_research": ("configs/research_v1.toml", "parameters"),
    "paper": ("docs/memo/The_Liquidity_Paradox.tex", "paper"),
    "memo_frozen": ("docs/memo/FROZEN.sha256", "paper"),
    "paper_pdf": ("docs/memo/The_Liquidity_Paradox.pdf", "paper"),
    "supplement_pdf": ("docs/memo/Reproducibility_Supplement.pdf", "paper"),
}

# Files a held-out ("heldout") record may cite.
HELDOUT_ALLOWED = {
    "results/closeout/closeout_analysis.json",
    "results/closeout/e001_closeout.json",
    "results/closeout/closeout_meta.json",
    "results/closeout_attempts.jsonl",
    "results/closeout_freeze/input_status.json",
    "docs/memo/The_Liquidity_Paradox.tex",
}


class UnregisteredSource(KeyError):
    pass


_cache = {}


def path_of(key):
    if key not in SOURCES:
        raise UnregisteredSource(key)
    return SOURCES[key][0]


def raw_bytes(key):
    rel = path_of(key)
    if rel not in _cache:
        _cache[rel] = (ROOT / rel).read_bytes()
    return _cache[rel]


def sha256(key):
    return hashlib.sha256(raw_bytes(key)).hexdigest()


def load(key):
    rel = path_of(key)
    if rel.endswith(".pdf"):
        return raw_bytes(key)
    data = raw_bytes(key).decode("utf-8")
    if rel.endswith(".json"):
        return json.loads(data)
    if rel.endswith(".jsonl"):
        return [json.loads(line) for line in data.splitlines() if line.strip()]
    if rel.endswith(".csv"):
        return list(csv.DictReader(data.splitlines()))
    if rel.endswith(".toml"):
        return tomllib.loads(data)
    return data


def json_pointer(obj, pointer):
    """RFC 6901 pointer into parsed JSON (lists indexed by position)."""
    if pointer in ("", "/"):
        return obj
    for part in pointer.lstrip("/").split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
    return obj


def csv_cell(rows, query, column):
    """The single row matching every key=value pair of `query`, then its column (float, or None if empty)."""
    hits = [r for r in rows if all(r[k] == v for k, v in query.items())]
    if len(hits) != 1:
        raise LookupError(f"{query}: {len(hits)} rows")
    cell = hits[0][column]
    return None if cell in ("", "nan", "None") else float(cell)


def resolve(src):
    """Resolve a record's `src` string back to the frozen value it cites.

    Forms: "<path>#<json pointer>", "<path>?k=v&k=v#<column>" (CSV row), "<path>#L<line>" (paper line; returns the line).
    """
    path, _, frag = src.partition("#")
    query = ""
    if "?" in path:
        path, _, query = path.partition("?")
    key = next(k for k, (p, _) in SOURCES.items() if p == path)
    if path.endswith(".tex"):
        return load(key).splitlines()[int(frag[1:]) - 1]
    if path.endswith(".csv"):
        q = dict(kv.split("=", 1) for kv in query.split("&"))
        return csv_cell(load(key), q, frag)
    return json_pointer(load(key), frag)


def paper_line(fragment):
    """1-based line number of the unique line of the frozen paper that contains `fragment`."""
    lines = load("paper").splitlines()
    hits = [i + 1 for i, line in enumerate(lines) if fragment in line]
    if len(hits) != 1:
        raise LookupError(f"paper fragment {fragment!r}: {len(hits)} matching lines")
    return hits[0]


def normalise_tex(text):
    """The frozen paper as plain text, for checking quotations (WEBSITE_PLAN section 7.3)."""
    t = text
    for macro, word in (("\\obs{}", "observed"), ("\\obs", "observed"), ("\\mhr{}", "modeled"), ("\\mhr", "modeled"),
                        ("\\stress{}", "stress test"), ("\\stress", "stress test"), ("\\hyp{}", "hypothetical"),
                        ("\\hyp", "hypothetical"), ("\\bp{}", " bp"), ("\\bp", " bp")):
        t = t.replace(macro, word)
    t = re.sub(r"\\(emph|textbf|textit)\{([^{}]*)\}", r"\2", t)
    t = re.sub(r"\\citep?\{[^}]*\}", "", t)
    t = re.sub(r"~?\\ref\{[^}]*\}", "", t)
    t = t.replace("$-$", "−").replace("{,}", ",").replace("\\,", " ").replace("\\%", "%").replace("``", "“").replace("''", "”")
    t = re.sub(r"\$([^$]*)\$", lambda m: m.group(1).replace("-", "−"), t)
    t = t.replace("~", " ").replace("--", "–")
    return re.sub(r"\s+", " ", t)
