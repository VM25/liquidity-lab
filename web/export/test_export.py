"""Tests for the website exporter. Run: uv run --frozen pytest web/export -q"""

import hashlib
import json
import math
import re
import statistics
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_bundle as B  # noqa: E402
import registry as R  # noqa: E402

ROOT = R.ROOT
CORE = json.loads((ROOT / "web/src/data/core.json").read_text())
LAB = json.loads((ROOT / "web/src/data/lab.json").read_text())


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)


# ------------------------------------------------------------------ guards: frozen research tree untouched
def test_freeze_pinned_trees_unchanged():
    rec = json.loads((ROOT / "results/closeout_freeze/freeze_record.json").read_text())
    for path, tree in rec["trees"].items():
        assert git("rev-parse", f"HEAD:{path}").stdout.strip() == tree, path
    assert git("diff", "--quiet", "HEAD", "--", *rec["trees"]).returncode == 0
    untracked = git("ls-files", "--others", "--exclude-standard", "--", *rec["trees"]).stdout.strip()
    assert untracked == "", untracked


def test_memo_frozen_hashes():
    for line in (ROOT / "docs/memo/FROZEN.sha256").read_text().splitlines():
        digest, path = line.split(maxsplit=1)
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path


# ------------------------------------------------------------------ source restrictions
def test_unregistered_source_raises():
    with pytest.raises(R.UnregisteredSource):
        R.path_of("results/closeout/e003_net_by_session.csv")


def test_registry_has_no_heldout_tables_or_raw_data():
    for path, _ in R.SOURCES.values():
        assert not re.fullmatch(r"results/closeout/.*\.csv", path), path
        assert not path.startswith("data/") and "fa636" not in path and not path.startswith("tracks/")


def test_bundle_cites_only_registered_files():
    registered = {p for p, _ in R.SOURCES.values()}
    assert set(CORE["meta"]["sources"]) <= registered
    for r in CORE["values"].values():
        assert r["src"].split("#")[0].split("?")[0] in registered, r["src"]


def test_heldout_records_cite_only_the_frozen_analysis():
    for rid, r in CORE["values"].items():
        if r["smp"] == "heldout":
            assert r["src"].split("#")[0] in R.HELDOUT_ALLOWED, (rid, r["src"])


# ------------------------------------------------------------------ every number resolves to its frozen source
@pytest.mark.parametrize("rid", sorted(CORE["values"]))
def test_value_resolves(rid):
    r = CORE["values"][rid]
    got = R.resolve(r["src"])
    if r["src"].split("#")[0].endswith(".tex"):
        assert r["frag"] in got, (rid, got)
        return
    if "sessions" in r:
        assert got == {k: v for k, v in got.items()} and isinstance(got, dict)
        return
    if r["v"] is None:
        assert got is None
        return
    assert math.isclose(got * r.get("scale", 1.0), r["v"], rel_tol=0, abs_tol=1e-12), (rid, got, r["v"])


def test_known_statuses_only():
    allowed = {"observed", "modeled historical replay", "modeled historical replay (gross, fee-free)",
               "modeled historical replay; LP tier 4 fees are hypothetical, not attainable",
               "modeled historical replay under stress test", "stress test", "observed (model trained under stress test)",
               "parameter", "metadata"}
    for rid, r in CORE["values"].items():
        assert r["st"] in allowed, (rid, r["st"])


# ------------------------------------------------------------------ the frozen paper as oracle
def fmt(v, d):
    return f"{v:.{d}f}".replace("-", "−")


def test_fee_ranges_match_paper_table3():
    printed = {"vip0": ("−11.9", "−11.4"), "vip0_bnb": ("−9.4", "−8.9"), "vip9": ("−3.0", "−2.5"),
               "lp_tier1": ("−1.9", "−1.4"), "lp_tier4": ("−1.1", "−0.6")}
    for f in CORE["e002"]["fees"]:
        assert (fmt(f["lo"], 1), fmt(f["hi"], 1)) == printed[f["id"]]
        rows = R.load("e002_net")
        for fm, mean in f["by_fill"].items():
            v = [float(r["net_bp_per_notional"]) for r in rows if r["policy"] == "P0" and r["latency"] == "tokyo"
                 and r["fee_schedule"] == f["id"] and r["fill_model"] == fm and r["net_bp_per_notional"]]
            assert statistics.mean(v) == mean


def test_key_numbers_match_the_paper():
    v = CORE["values"]
    pairs = {"e001.rs_30s.disc": "−1.06", "e001.rs_30s.held": "−0.59", "e001.mo_30s.held": "1.01", "e003.h1t.disc": "−0.12",
             "e003.h1t.held": "−0.01", "e003.h1t.held_tlo": "−0.48", "e003.h1t.held_thi": "0.46", "e004.p0.held": "−0.09",
             "e004.p3m2.held": "−0.08", "e003.h3.es_diff.held": "−1.87", "e003.h3.net_per_hour_diff.held": "0.65",
             "e003.p3m2_p0.held": "37.5", "e003.p3m2_p0.held_fee_saving": "33.2", "e003.p3m2_p0.held_gross": "4.4",
             "e001.rs_1s.held_tlo": "−0.77", "e001.rs_1s.held_thi": "0.22", "e003.p0_primary.net_bp": "−11.52"}
    for rid, s in pairs.items():
        assert fmt(v[rid]["v"], v[rid]["d"]) == s, rid
    assert f'{v["e003.h1f.disc"]["v"] * 100:.2f}' == "3.64" and f'{v["e003.h1f.held"]["v"] * 100:.2f}' == "4.20"


# ------------------------------------------------------------------ label table and tallies
def test_label_table_rows():
    ids = [(r["exp"], r["id"]) for r in CORE["labels"] if r["kind"] == "check"]
    assert ids == [("E001", f"E001 {m}") for m in ("mo_1s", "mo_5s", "mo_30s", "rs_1s", "rs_5s", "rs_30s")] + \
        [("E003", "H1-F"), ("E003", "H1-T"), ("E003", "H3"), ("E004", "H4-W[P0]"), ("E004", "H4-W[P3_M2]")]
    assert [r["id"] for r in CORE["labels"] if r["kind"] == "secondary"] == ["H4-F y_view"]
    for r in CORE["labels"]:
        if r["kind"] == "check":
            assert r["label"] == "confirmed (point estimate, 5 of 5 defined)"
        if r["id"].startswith("H4-W"):
            assert r["interpretation"] == "no material deterioration under the specified threshold"


def test_tallies_verbatim_and_never_summed():
    assert CORE["holdout"]["tallies"] == {"E001": "6 of 6 confirmed", "E002": None, "E003": "3 of 3 confirmed", "E004": "2 of 2 confirmed"}
    text = json.dumps(CORE)
    assert "11 of 11" not in text and "12 of 12" not in text


def test_display_labels_appear_in_closeout_report():
    report = (ROOT / "results/closeout/CLOSEOUT_report.md").read_text()
    for r in CORE["labels"]:
        if r["kind"] == "check":
            assert f"**{r['label']}**" in report


# ------------------------------------------------------------------ Scenario Lab grids
def test_lab_grid_complete_and_faithful():
    disc = R.load("e003")["descriptive"]["scenarios"]
    held = R.load("close")["experiments"]["E003"]["reported_only"]["descriptive"]["scenarios"]
    for side, rows in (("disc", disc), ("held", held)):
        assert len(LAB["grid"][side]) == 192
        for s in rows:
            k = f'{s["policy"]}|{s["fill_model"]}|{s["latency"]}|{s["fee_schedule"]}'
            assert LAB["grid"][side][k] == [s[m] for m in LAB["metrics"]]


def test_discovery_session_values_match_means():
    disc = R.load("e003")["descriptive"]["scenarios"]
    for s in disc:
        k = f'{s["policy"]}|{s["fill_model"]}|{s["latency"]}|{s["fee_schedule"]}'
        vals = [x[0] for x in LAB["disc_sessions"][k].values() if x[0] is not None]
        assert len(LAB["disc_sessions"][k]) == 10
        assert math.isclose(statistics.mean(vals), s["net_per_hour"], abs_tol=1e-9)


def test_heldout_lab_values_only_from_frozen_analysis():
    assert LAB["grid_src"]["held"].startswith("results/closeout/closeout_analysis.json#")
    assert LAB["held_sessions_src"].startswith("results/closeout/closeout_analysis.json#")
    assert set(LAB["held_sessions_primary_vip0"]) == {"P0", "P1", "P3_M1", "P3_M2", "P3_negM2", "P3F", "P4"}


# ------------------------------------------------------------------ quotations of the paper in page copy
def test_quotations_are_verbatim():
    paper = R.normalise_tex(R.load("paper"))
    found = 0
    for f in (ROOT / "web/src").rglob("*.tsx"):
        for q in re.findall(r"<Quote(?: [^>]*)?>(.*?)</Quote>", f.read_text(), flags=re.S):
            text = re.sub(r"\s+", " ", q.replace("&rsquo;", "’").replace("{' '}", " ")).strip()
            assert text in paper, (f.name, text)
            found += 1
    assert found >= 1


def test_bundles_up_to_date():
    assert B.main(["--check"]) == 0
