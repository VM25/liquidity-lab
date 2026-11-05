"""Close-out guards, ledger, failure classes, recovery and fail-closed terminal state, in scratch git repositories with synthetic
experiments and synthetic tables (no market data; no test session). Process deaths are real: a subprocess dies with os._exit."""

import json
import os
import re
import subprocess
import sys
import textwrap
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import polars as pl
import pytest

from lpx.data.acquire import ROOT
from lpx.research import closeout as C
from lpx.research import closeout_analysis as A

HELP = Path(__file__)


# ------------------------------------------------------------------------------------------------ scratch repository
def repo(tmp: Path) -> tuple[C.Workspace, str]:
    root = tmp / "repo"
    root.mkdir()
    ws = C.Workspace(root)
    ws.git("init", "-q")
    ws.git("config", "user.email", "t@example.invalid")
    ws.git("config", "user.name", "t")
    for rel, text in ((C.PROTOCOL, "# protocol (FROZEN)\n"), ("docs/DECISIONS.md", "d\n"), ("configs/x.toml", "a = 1\n"), ("lpx/x.py", "x = 1\n"),
                      ("uv.lock", "lock\n")):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "baseline")
    base = ws.git("rev-parse", "HEAD").strip()
    (root / "lpx/closeout_added.py").write_text("y = 2\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "added")
    p = root / C.FREEZE_RECORD
    p.parent.mkdir(parents=True)
    p.write_text(json.dumps(C.build_freeze_record(ws, base, [C.PROTOCOL, "configs/x.toml", "uv.lock"])))
    h = C.sha256_file(p)
    with open(root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h) + "\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "freeze")
    return ws, h


def authorise(ws: C.Workspace, h: str, n: int) -> None:
    ws.append({"event": "authorised", "n": n, "freeze_record_sha256": h, "utc": "t"})


def fake_analyse(tables: Path, ctx) -> dict:
    meta = json.loads((tables / "closeout_meta.json").read_text())
    for f, x in meta["tables_sha256"].items():
        if C.sha256_file(tables / f) != x:
            raise RuntimeError("table differs from the metadata")
    return {"mode": ctx.mode, "not_refutation": "", "fee_attainability": "", "undefined_sessions": {}, "experiments": {},
            "statuses": meta["statuses"]}


def writer(name: str):
    def run(ctx):
        p = ctx.out / f"{name}.csv"
        p.write_text("a\n1\n")
        ctx.hook(name, "d")
        return [p]
    return run


def runners() -> dict:
    return {e: writer(e) for e in C.EXPERIMENTS}


def ctx_factory(injection=None):
    def make(out, progress):
        return C.Ctx("rehearsal", out, {}, {e: ["d"] for e in C.EXPERIMENTS}, None, None, out, progress, injection)
    return make


def attempt(ws, injection=None, rn=None, analyse=fake_analyse):
    return C.run_attempt(ws, ctx_factory(injection), rn or runners(), analyse)


def events(ws):
    return [(e["event"], e.get("n")) for e in ws.events()]


def run_dying(ws: C.Workspace, stage: str) -> int:
    """A real process death at a stage (os._exit in a subprocess)."""
    code = textwrap.dedent(f"""
        import sys
        from pathlib import Path
        sys.path.insert(0, {str(ROOT)!r})
        import tests.test_closeout as T
        from lpx.research import closeout as C
        C.run_attempt(C.Workspace(Path({str(ws.root)!r})), T.ctx_factory(({stage!r}, None, "death")), T.runners(), T.fake_analyse)
    """)
    return subprocess.run([sys.executable, "-c", code], env={**os.environ, "PYTHONPATH": str(ROOT)}, capture_output=True).returncode


# ------------------------------------------------------------------------------------------------ guards and refusals
def test_clean_success_commits_ledger_and_promotes(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    r = attempt(ws)
    assert r["outcome"] == "completed"
    assert events(ws) == [("authorised", 1), ("started", 1), ("completed", 1)]
    assert (ws.promoted / "closeout_analysis.json").exists() and (ws.promoted / "CLOSEOUT_report.md").exists()
    assert not ws.staging.exists()


def test_refuses_without_an_authorised_event_freeze_record_or_authorisation(tmp_path):
    ws, h = repo(tmp_path)
    with pytest.raises(C.Refused, match="exactly one authorised"):
        attempt(ws)
    authorise(ws, "wrong", 1)
    with pytest.raises(C.Refused, match="different freeze record"):
        attempt(ws)
    (tmp_path / "b").mkdir()
    ws2, h2 = repo(tmp_path / "b")
    (ws2.root / "docs/DECISIONS.md").write_text("no authorisation\n")
    ws2.git("add", "-A")
    ws2.git("commit", "-q", "-m", "remove")
    authorise(ws2, h2, 1)
    with pytest.raises(C.Refused, match="no committed owner line"):
        attempt(ws2)


def test_the_real_repository_refuses_test_mode_now():
    """The project has no freeze record and a DRAFT protocol: the entry point refuses before reading anything."""
    with pytest.raises(C.Refused):
        C.check_guards(C.Workspace(ROOT))
    if not (ROOT / C.FREEZE_RECORD).exists():
        r = subprocess.run([sys.executable, "-m", "lpx.research.closeout", "--test-sessions"], cwd=ROOT, capture_output=True, text=True)
        assert r.returncode != 0 and "refused" in r.stderr and "not frozen" in r.stderr


@pytest.mark.parametrize("path,msg", [(C.PROTOCOL, "pinned file"), ("configs/x.toml", "pinned file"), ("uv.lock", "pinned file")])
def test_hash_mismatch_on_a_pinned_file_refuses(tmp_path, path, msg):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    (ws.root / path).write_text("tampered (FROZEN)\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "tamper")
    with pytest.raises(C.Refused, match=msg + "|code differs"):
        attempt(ws)
    assert ("started", 1) not in events(ws)


def test_code_outside_the_allowed_diff_refuses(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    (ws.root / "lpx/x.py").write_text("x = 2\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "change baseline code")
    with pytest.raises(C.Refused, match="allowed additions"):
        attempt(ws)


def test_dirty_tree_and_allow_dirty_refuse(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    (ws.root / "stray.txt").write_text("x")
    with pytest.raises(C.Refused, match="not clean"):
        attempt(ws)
    (ws.root / "stray.txt").unlink()
    monkeypatch.setenv("LPX_ALLOW_DIRTY", "1")
    with pytest.raises(C.Refused, match="LPX_ALLOW_DIRTY"):
        attempt(ws)


def test_draft_protocol_refuses(tmp_path):
    ws, h = repo(tmp_path)
    (ws.root / C.PROTOCOL).write_text("# protocol (DRAFT, not frozen)\n")
    with pytest.raises(C.Refused, match="not marked FROZEN"):
        C.check_guards(ws)


def test_repeated_attempt_refused_after_completion_and_ledger_counts_from_head(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws)
    authorise(ws, h, 2)
    with pytest.raises(C.Refused, match="precedes the failure|already completed"):
        attempt(ws)
    ws.git("reset", "-q", "--hard", "HEAD~1")
    # deleting the outputs does not reopen it: the ledger in HEAD still says completed
    import shutil

    shutil.rmtree(ws.promoted)
    with pytest.raises(C.Refused, match="already completed"):
        attempt(ws)


def test_rerun_of_a_consumed_record_and_skipped_numbers_refuse(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "closeout"))
    with pytest.raises(C.Refused, match="exactly one authorised"):
        attempt(ws)                                  # attempt 1's record is consumed
    authorise(ws, h, 3)
    with pytest.raises(C.Refused, match="precedes the failure"):
        attempt(ws)


def test_attempt_beyond_the_limit_refuses(tmp_path):
    ws, h = repo(tmp_path)
    for n in (1, 2, 3):
        authorise(ws, h, n)
        attempt(ws, ("E001", None, "environment"))
    (ws.promoted / "CLOSEOUT_report.md").unlink()
    ws.promoted.rmdir()
    authorise(ws, h, 4)
    with pytest.raises(C.Refused):
        attempt(ws)
    # and with no closed event in the way, the cap itself refuses
    ws2 = SimpleNamespace(events=lambda: [])
    assert C.MAX_ATTEMPTS == 3 and ws2.events() == []


def test_tampered_or_unlisted_attempt_directory_refuses(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E002", None, "closeout"))
    authorise(ws, h, 2)
    with open(ws.attempt_dir(1) / "E001.csv", "a") as f:
        f.write("9\n")
    with pytest.raises(C.Refused, match="does not match"):
        attempt(ws)
    (tmp_path / "c").mkdir()
    ws3, h3 = repo(tmp_path / "c")
    (ws3.root / "results/closeout_attempt7").mkdir(parents=True)
    (ws3.root / "results/closeout_attempt7/x").write_text("x")
    authorise(ws3, h3, 1)
    with pytest.raises(C.Refused, match="not named in a failed event"):
        attempt(ws3)


def test_existing_staging_refuses(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    ws.staging.mkdir(parents=True)
    with pytest.raises(C.Refused, match="already exists"):
        attempt(ws)


# ------------------------------------------------------------------------------------------------ failure classes
def test_software_exception_makes_the_experiment_not_confirmable_not_a_session(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    r = attempt(ws, ("E002", None, "software"))
    assert r["outcome"] == "completed" and ("failed", 1) not in events(ws)
    st = r["statuses"]
    assert st["E002"]["status"] == "not_confirmable_software" and st["E001"]["status"] == st["E003"]["status"] == "complete"
    assert st["E002"]["exception"] == "AssertionError" and st["E002"]["location"].startswith("closeout.py:")
    assert st["E002"]["last_session_started"] == "d" and not (ws.promoted / "E002.csv").exists()


def test_software_exception_in_baseline_code_is_software(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    r = attempt(ws, ("E001", None, "baseline"))
    assert r["outcome"] == "completed" and r["statuses"]["E001"]["status"] == "not_confirmable_software"


def test_e003_software_exception_blocks_e004(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    r = attempt(ws, ("E003", None, "software"))
    assert r["statuses"]["E003"]["status"] == r["statuses"]["E004"]["status"] == "not_confirmable_software"
    assert r["statuses"]["E004"]["reason"] == "depends on E003"
    assert not (ws.promoted / "E004.csv").exists() and not (ws.promoted / "E003.csv").exists()   # nothing partial survives


@pytest.mark.parametrize("kind,cls", [("environment", "environment"), ("closeout", "closeout")])
def test_environment_and_closeout_failures_are_failed_attempts_with_sealed_outputs(tmp_path, kind, cls):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    r = attempt(ws, ("E002", None, kind))
    assert r["outcome"] == "failed" and r["class"] == cls
    assert events(ws)[-1] == ("failed", 1) and not ws.staging.exists() and not ws.promoted.exists()
    assert ws.attempt_dir(1).exists() and (ws.attempt_dir(1) / "closeout.log").exists()
    f = ws.events()[-1]
    assert f["hashes"] == C.tree_listing(ws.attempt_dir(1)) and f["sealed_log_sha256"] == f["hashes"]["closeout.log"]


def test_retry_after_environment_failure_under_the_same_freeze_record(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "environment"))
    authorise(ws, h, 2)
    r = attempt(ws)
    assert r["outcome"] == "completed" and r["attempt"] == 2
    assert ws.attempt_dir(1).exists()               # still sealed, never analysed


def test_analysis_failure_and_metadata_failure_are_failed_attempts(tmp_path):
    for i, stage in enumerate(("analysis", "meta")):
        d = tmp_path / str(i)
        d.mkdir()
        ws, h = repo(d)
        authorise(ws, h, 1)
        r = attempt(ws, (stage, None, "closeout"))
        assert r["outcome"] == "failed" and not ws.promoted.exists() and ws.attempt_dir(1).exists()


def staged(tmp: Path, lost=()) -> dict:
    """A staging directory holding exactly the expected files, with its metadata."""
    statuses = {}
    for e, tabs in A.EXPERIMENT_TABLES.items():
        if e in lost:
            statuses[e] = {"status": "not_confirmable_software", "exception": "AssertionError"}
            continue
        for t in tabs:
            (tmp / t).write_text(f"{t}\n")
            if e in A.SIDECARS:
                (tmp / f"{t}.status.json").write_text("{}")
        statuses[e] = {"status": "complete", "outputs": {t: C.sha256_file(tmp / t) for t in tabs}}
    for f in A.INFRASTRUCTURE:
        (tmp / f).write_text("{}")
    (tmp / "closeout.log").write_text("sealed")
    meta = {"statuses": statuses, "tables_sha256": {p.name: C.sha256_file(p) for p in tmp.iterdir() if p.name != "closeout.log"}}
    return meta


def test_staged_set_exact_passes_and_ignores_only_the_log_and_metadata(tmp_path):
    meta = staged(tmp_path)
    (tmp_path / "closeout_meta.json").write_text(json.dumps(meta))
    A.verify_staged(tmp_path, meta)


@pytest.mark.parametrize("damage,why", [
    (lambda t, m: (t / "stray.csv").write_text("x"), "unexpected"),
    (lambda t, m: (t / "e003_calibration.csv").unlink(), "missing"),
    (lambda t, m: (t / "closeout_relative_tick.json").unlink(), "missing"),
    (lambda t, m: (t / "e002_net_by_session.csv.status.json").unlink(), "missing"),
    (lambda t, m: m["tables_sha256"].pop("e001_cells.csv"), "unlisted"),
    (lambda t, m: m["tables_sha256"].update({"ghost.csv": "0"}), "listed but absent"),
    (lambda t, m: (t / "e004_lambda.csv").write_text("tampered"), "differs from the metadata"),
    (lambda t, m: m["statuses"]["E002"]["outputs"].update({"e002_net_by_session.csv": "0"}), "recorded outputs"),
    (lambda t, m: (t / ".writing_E001").mkdir(), "directory"),
])
def test_staged_set_refuses_any_difference_before_a_table_is_read(tmp_path, damage, why):
    meta = staged(tmp_path)
    damage(tmp_path, meta)
    with pytest.raises(RuntimeError, match=why):
        A.verify_staged(tmp_path, meta)


def test_lost_experiment_may_leave_no_tables(tmp_path):
    meta = staged(tmp_path, lost=("E003",))
    A.verify_staged(tmp_path, meta)
    (tmp_path / "e003_net_by_session.csv").write_text("partial")
    meta["tables_sha256"]["e003_net_by_session.csv"] = C.sha256_file(tmp_path / "e003_net_by_session.csv")
    with pytest.raises(RuntimeError, match="unexpected"):
        A.verify_staged(tmp_path, meta)


def test_classifier_uses_the_innermost_relevant_frame():
    def closeout_frame():
        raise ValueError("plain")
    with pytest.raises(ValueError) as e:
        closeout_frame()
    assert C.classify(e.value) == "closeout"
    with pytest.raises(AssertionError) as e:
        C.frozen_copy_injected_failure()
    assert C.classify(e.value) == "software"
    with pytest.raises(Exception) as e:
        C.DG.inside(object(), None)
    assert C.classify(e.value) == "software"
    assert C.classify(OSError("disk")) == "environment" and C.classify(MemoryError()) == "environment"
    assert C.classify(KeyboardInterrupt()) == "environment"


def frozen_copy_nested_probe(kind):
    def evaluate():
        raise ValueError("library-style")
    if kind == "nested":
        evaluate()
    if kind == "genexpr":
        return any(1 / x for x in [0])
    return (lambda: 1 / 0)()


@pytest.mark.parametrize("kind", ["nested", "genexpr", "lambda"])
def test_nested_scopes_of_marked_blocks_are_software(kind):
    with pytest.raises(Exception) as e:
        frozen_copy_nested_probe(kind)
    assert C.classify(e.value) == "software"


def test_a_helper_called_from_a_marked_block_stays_closeout():
    with pytest.raises(RuntimeError) as e:
        C.check_trained(SimpleNamespace(expected_trained=lambda d: ["a"], trained={}), "d", {"sessions": ["b"]})
    assert C.classify(e.value) == "closeout"


def test_frozen_permission_refusal_is_not_an_environment_failure():
    with pytest.raises(PermissionError) as e:
        frozen_copy_raise_permission()
    assert C.classify(e.value) == "software"


def frozen_copy_raise_permission():
    raise PermissionError("a session failed the integrity checks")


def test_injection_is_impossible_in_test_mode(tmp_path):
    ctx = C.Ctx("test", tmp_path, {}, {}, None, None, tmp_path, print, ("E001", None, "closeout"))
    with pytest.raises(C.Refused, match="not available in test mode"):
        ctx.hook("E001", "d")


# ------------------------------------------------------------------------------------------------ fail closed
def test_third_failed_attempt_fails_closed_with_no_partial_labels(tmp_path):
    ws, h = repo(tmp_path)
    for n in (1, 2, 3):
        authorise(ws, h, n)
        r = attempt(ws, ("E003", None, "closeout"))         # E001 and E002 finished before each failure
        assert r["outcome"] == "failed"
    assert events(ws)[-2:] == [("failed", 3), ("closed", None)]
    rep = (ws.promoted / "CLOSEOUT_report.md").read_text()
    assert "FAILED CLOSED" in rep and "**confirmed" not in rep
    for ids in A.CHECK_IDS.values():
        for i in ids:
            assert f"| {i} | not confirmable (run failure) |" in rep
    for ids in A.REPORTED_IDS.values():
        for i in ids:
            assert f"| {i} | not run (run failure) |" in rep
    assert not (ws.promoted / "closeout_analysis.json").exists() and not (ws.promoted / "E001.csv").exists()
    assert (ws.attempt_dir(3) / "E001.csv").exists()        # sealed, not analysed
    authorise(ws, h, 4)
    with pytest.raises(C.Refused):
        attempt(ws)


def test_fourth_attempt_refused_even_if_results_are_removed(tmp_path):
    import shutil

    ws, h = repo(tmp_path)
    for n in (1, 2, 3):
        authorise(ws, h, n)
        attempt(ws, ("E001", None, "environment"))
    shutil.rmtree(ws.promoted)
    authorise(ws, h, 4)
    with pytest.raises(C.Refused, match="already completed or closed"):
        attempt(ws)


# ------------------------------------------------------------------------------------------------ crash recovery (real deaths)
@pytest.mark.parametrize("stage", ["E001", "E003", "meta", "analysis"])
def test_process_death_before_the_analysis_file_uses_up_the_attempt(tmp_path, stage):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    assert run_dying(ws, stage) == 137
    assert events(ws)[-1] == ("started", 1) and ws.staging.exists()
    authorise(ws, h, 2)
    with pytest.raises(C.Refused):
        attempt(ws)                                         # refuses until recovered
    ws.git("reset", "-q", "--hard", "HEAD~1")               # (undo the premature authorisation for the next step)
    assert C.recover(ws) == "attempt 1 failed"
    assert events(ws)[-1] == ("failed", 1) and ws.events()[-1]["exception"] == "process death"
    assert not ws.staging.exists() and ws.attempt_dir(1).exists()
    authorise(ws, h, 2)
    assert attempt(ws)["outcome"] == "completed"


def test_process_death_after_the_analysis_file_keeps_the_primary_analysis(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    assert run_dying(ws, "after_analysis") == 137
    assert (ws.staging / "closeout_analysis.json").exists() and ("completed", 1) not in events(ws)
    before = C.sha256_file(ws.staging / "closeout_analysis.json")
    assert C.recover(ws) == "completed from the primary analysis"
    assert events(ws)[-1] == ("completed", 1) and C.sha256_file(ws.promoted / "closeout_analysis.json") == before
    assert (ws.promoted / "CLOSEOUT_report.md").exists()
    with pytest.raises(C.Refused, match="nothing to recover"):
        C.recover(ws)


def test_process_death_after_completed_before_promotion(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    orig = C.promote_and_report
    C.promote_and_report = lambda w: (_ for _ in ()).throw(SystemExit(0))
    try:
        with pytest.raises(SystemExit):
            attempt(ws)
    finally:
        C.promote_and_report = orig
    assert events(ws)[-1] == ("completed", 1) and ws.staging.exists()
    assert C.recover(ws) == "repeated promotion and report"
    assert (ws.promoted / "CLOSEOUT_report.md").exists()


def test_process_death_after_promotion_before_the_report(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws)
    (ws.promoted / "CLOSEOUT_report.md").unlink()
    assert C.recover(ws) == "repeated promotion and report"
    assert (ws.promoted / "CLOSEOUT_report.md").exists()


def test_process_death_on_attempt_three_closes(tmp_path):
    ws, h = repo(tmp_path)
    for n in (1, 2):
        authorise(ws, h, n)
        attempt(ws, ("E001", None, "environment"))
    authorise(ws, h, 3)
    assert run_dying(ws, "E003") == 137
    assert C.recover(ws) == "closed"
    assert events(ws)[-2:] == [("failed", 3), ("closed", None)]
    assert "FAILED CLOSED" in (ws.promoted / "CLOSEOUT_report.md").read_text() and ws.attempt_dir(3).exists()


def test_death_between_rename_and_failed_commit_adopts_the_directory(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    run_dying(ws, "E002")
    ws.staging.rename(ws.attempt_dir(1))
    assert C.recover(ws) == "attempt 1 failed"
    assert ws.events()[-1]["path"] == "results/closeout_attempt1" and ws.events()[-1]["hashes"]


def test_death_on_attempt_three_between_failed_and_closed(tmp_path):
    ws, h = repo(tmp_path)
    for n in (1, 2):
        authorise(ws, h, n)
        attempt(ws, ("E001", None, "environment"))
    authorise(ws, h, 3)
    run_dying(ws, "E002")
    orig = C.close_terminal
    C.close_terminal = lambda w: (_ for _ in ()).throw(SystemExit(0))
    try:
        with pytest.raises(SystemExit):
            C.recover(ws)
    finally:
        C.close_terminal = orig
    assert events(ws)[-1] == ("failed", 3)
    assert C.recover(ws) == "closed"
    with pytest.raises(C.Refused, match="nothing to recover"):
        C.recover(ws)


@pytest.mark.parametrize("line", ['{"event": "failed", "n": 1}\n', '{"event": "fail'])
def test_uncommitted_ledger_tail_and_stale_lock_are_recovered(tmp_path, line):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    run_dying(ws, "E001")
    with open(ws.ledger, "a") as f:
        f.write(line)
    (ws.root / ".git/index.lock").write_text("")
    assert C.recover(ws) == "attempt 1 failed"
    assert [json.loads(x) for x in ws.ledger.read_text().splitlines()][-1]["event"] == "failed"


def test_uncommitted_started_line_leaves_the_record_unconsumed(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    with open(ws.ledger, "a") as f:
        f.write('{"event": "started", "n": 1}\n')
    with pytest.raises(C.Refused, match="nothing to recover"):
        C.recover(ws)                                       # the tail is restored; no attempt was consumed
    assert attempt(ws)["outcome"] == "completed"


def test_ledger_edited_beyond_one_tail_line_refuses_recovery(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    run_dying(ws, "E001")
    ws.ledger.write_text("{}\n")
    with pytest.raises(C.Refused, match="more than one appended"):
        C.recover(ws)


def test_recovery_refuses_a_dirty_repository(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    run_dying(ws, "E001")
    (ws.root / "stray.txt").write_text("x")
    with pytest.raises(C.Refused, match="not clean"):
        C.recover(ws)


def test_recovery_refuses_a_committed_pinned_mismatch(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    run_dying(ws, "E001")
    (ws.root / C.PROTOCOL).write_text("# changed (FROZEN)\n")
    ws.git("add", C.PROTOCOL)
    ws.git("commit", "-q", "-m", "tamper")
    with pytest.raises(C.Refused, match="pinned file differs"):
        C.recover(ws)


def test_recovery_with_a_metadata_mismatch_takes_the_failed_branch(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    run_dying(ws, "after_analysis")
    (ws.staging / "closeout_meta.json").write_text("{}")
    assert C.recover(ws) == "attempt 1 failed"
    assert ("completed", 1) not in events(ws) and not ws.promoted.exists() and ws.attempt_dir(1).exists()


def test_recovery_with_a_truncated_analysis_takes_the_failed_branch(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    run_dying(ws, "after_analysis")
    (ws.staging / "closeout_analysis.json").write_text("{")
    assert C.recover(ws) == "attempt 1 failed"


def test_recovery_refuses_while_the_attempt_process_is_alive(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    run_dying(ws, "E001")
    import fcntl

    lock = open(ws.root / ".git/closeout.lock", "w")
    fcntl.flock(lock, fcntl.LOCK_EX)
    code = f"import sys; sys.path.insert(0, {str(ROOT)!r}); from pathlib import Path; from lpx.research import closeout as C; C.recover(C.Workspace(Path({str(ws.root)!r})))"
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert r.returncode != 0 and "still running" in r.stderr


def test_failure_after_the_analysis_file_is_not_a_failed_attempt(tmp_path):
    for i, n in enumerate((1, 3)):
        d = tmp_path / str(i)
        d.mkdir()
        ws, h = repo(d)
        for k in range(1, n):
            authorise(ws, h, k)
            attempt(ws, ("E001", None, "environment"))
        authorise(ws, h, n)
        with pytest.raises(RuntimeError):
            attempt(ws, ("after_analysis", None, "closeout"))
        assert ("failed", n) not in events(ws)
        assert C.recover(ws) == "completed from the primary analysis"
        assert (ws.promoted / "CLOSEOUT_report.md").exists() and ("closed", None) not in events(ws)


def test_tampered_analysis_is_not_promoted_after_completed(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws)
    (ws.promoted / "CLOSEOUT_report.md").unlink()
    (ws.promoted / "closeout_analysis.json").write_text('{"mode": "tampered"}')
    with pytest.raises(C.Refused, match="differs from the completed event"):
        C.recover(ws)


def test_truncated_report_is_rerendered(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws)
    (ws.promoted / "CLOSEOUT_report.md").write_text("")
    assert C.recover(ws) == "repeated promotion and report"
    assert (ws.promoted / "CLOSEOUT_report.md").stat().st_size > 0


# ------------------------------------------------------------------------------------------------ retries and tampering
def test_retry_after_environment_failure_refuses_a_new_freeze_record(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "environment"))
    (ws.root / C.FREEZE_RECORD).write_text(json.dumps({**json.loads((ws.root / C.FREEZE_RECORD).read_text()), "note": "changed"}))
    h2 = C.sha256_file(ws.root / C.FREEZE_RECORD)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h2) + "\n")
    ws.git("add", "-A", "docs", "results/closeout_freeze")
    ws.git("commit", "-q", "-m", "new record")
    authorise(ws, h2, 2)
    with pytest.raises(C.Refused, match="takes no new freeze record"):
        attempt(ws)


def new_record_after_fix(ws, change_path, text):
    (ws.root / change_path).write_text(text)
    ws.git("add", "-A", change_path)
    ws.git("commit", "-q", "-m", "fix")
    old = json.loads((ws.root / C.FREEZE_RECORD).read_text())
    rec = C.build_freeze_record(ws, old["baseline"], list(old["pinned_sha256"]))
    (ws.root / C.FREEZE_RECORD).write_text(json.dumps(rec))
    h2 = C.sha256_file(ws.root / C.FREEZE_RECORD)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h2) + "\n")
    ws.git("add", "-A", "docs", "results/closeout_freeze")
    ws.git("commit", "-q", "-m", "new record")
    return h2


def test_retry_after_closeout_fix_may_change_added_files_only(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "closeout"))
    h2 = new_record_after_fix(ws, "lpx/closeout_added.py", "y = 3\n")
    authorise(ws, h2, 2)
    assert attempt(ws)["outcome"] == "completed"


def test_retry_may_not_change_a_pinned_research_input(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "closeout"))
    h2 = new_record_after_fix(ws, "uv.lock", "other lock\n")
    authorise(ws, h2, 2)
    with pytest.raises(C.Refused, match="may only add files|may not change"):
        attempt(ws)


def test_software_experiment_gets_no_retry_in_a_later_attempt(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)

    def rn():
        r = runners()
        r["E002"] = lambda ctx: C.frozen_copy_injected_failure()
        return r
    # E002 hits a software exception, then E004 hits an environment failure: attempt 1 fails with E002 recorded
    r1 = attempt(ws, ("E004", None, "environment"), rn=rn())
    assert r1["outcome"] == "failed" and ws.events()[-1]["software_experiments"] == ["E002"]
    authorise(ws, h, 2)
    r2 = attempt(ws)                                   # E002 would now succeed, but gets no retry
    assert r2["outcome"] == "completed" and r2["statuses"]["E002"]["status"] == "not_confirmable_software"
    assert "no retry" in r2["statuses"]["E002"]["reason"] and not (ws.promoted / "E002.csv").exists()


def test_ledger_cut_back_by_an_ordinary_commit_refuses(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "environment"))
    import shutil

    shutil.rmtree(ws.attempt_dir(1))
    first = ws.ledger.read_text().splitlines()[0] + "\n"
    ws.ledger.write_text(first)
    ws.git("add", C.LEDGER)
    ws.git("commit", "-q", "-m", "cut")
    with pytest.raises(C.Refused, match="not append-only"):
        attempt(ws)


def test_removed_sealed_directory_refuses(tmp_path):
    import shutil

    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "environment"))
    shutil.rmtree(ws.attempt_dir(1))
    authorise(ws, h, 2)
    with pytest.raises(C.Refused, match="does not match"):
        attempt(ws)


def test_mistaken_authorisation_is_superseded_visibly(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, "wrong", 1)
    authorise(ws, h, 1)
    assert attempt(ws)["outcome"] == "completed"
    assert sum(e == ("authorised", 1) for e in events(ws)) == 2


def mid_run(ws, action):
    def run(ctx):
        action()
        return writer("E002")(ctx)
    r = runners()
    r["E002"] = run
    return r


def test_commit_during_the_run_fails_the_attempt(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)

    def act():
        (ws.root / "docs/other.md").write_text("x")
        ws.git("add", "docs/other.md")
        ws.git("commit", "-q", "-m", "mid-run")
    assert attempt(ws, rn=mid_run(ws, act))["outcome"] == "failed"
    assert "Refused" in ws.events()[-1]["exception"]


def test_reverted_commit_during_the_run_fails_the_attempt(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)

    def act():
        (ws.root / "docs/other.md").write_text("x")
        ws.git("add", "docs/other.md")
        ws.git("commit", "-q", "-m", "mid-run")
        ws.git("rm", "-q", "docs/other.md")
        ws.git("commit", "-q", "-m", "revert")
    assert attempt(ws, rn=mid_run(ws, act))["outcome"] == "failed"


def test_uncommitted_tracked_edit_during_the_run_fails_the_attempt(tmp_path):
    ws, h = repo(tmp_path)
    (ws.root / "configs/unpinned.toml").write_text("b = 1\n")
    ws2 = ws
    ws2.git("add", "-A", "configs/unpinned.toml")
    ws2.git("commit", "-q", "-m", "more")
    old = json.loads((ws.root / C.FREEZE_RECORD).read_text())
    (ws.root / C.FREEZE_RECORD).write_text(json.dumps(C.build_freeze_record(ws, old["baseline"], list(old["pinned_sha256"]))))
    h2 = C.sha256_file(ws.root / C.FREEZE_RECORD)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h2) + "\n")
    ws.git("add", "-A", "docs", "results/closeout_freeze")
    ws.git("commit", "-q", "-m", "rec")
    authorise(ws, h2, 1)
    assert attempt(ws, rn=mid_run(ws, lambda: (ws.root / "configs/unpinned.toml").write_text("b = 2\n")))["outcome"] == "failed"


def test_input_or_fit_change_during_the_run_fails_the_attempt(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)

    def make(out, progress):
        return C.Ctx("rehearsal", out, {}, {e: ["d"] for e in C.EXPERIMENTS}, None, None, out, progress, None,
                     recheck=lambda: (_ for _ in ()).throw(RuntimeError("inputs changed during the run")))
    r = C.run_attempt(ws, make, runners(), fake_analyse)
    assert r["outcome"] == "failed" and ws.events()[-1]["exception"] == "RuntimeError"


def test_test_mode_baseline_and_allowed_list_come_from_the_protocol(tmp_path):
    ws, h = repo(tmp_path)
    with pytest.raises(C.Refused, match="baseline or allowed diff"):
        C.verify_freeze(ws, True, ("HEAD~1", C.ALLOWED_DIFF))
    assert len(C.ALLOWED_DIFF) == 7 and all(x.startswith("A\t") for x in C.ALLOWED_DIFF)


def test_test_mode_refuses_a_missing_required_pin(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    before = events(ws)
    with pytest.raises(C.Refused, match="does not pin"):
        C.run_attempt(ws, ctx_factory(), runners(), fake_analyse, required_pins=C.TEST_MODE_PINS)
    assert events(ws) == before


def test_modes_refuse_the_wrong_days():
    rc = C.load_rc()
    td, dd = rc["splits"]["test"][0], rc["splits"]["train"][0]
    for m in ("dryrun", "rehearsal"):
        with pytest.raises(C.Refused, match="refuse every test day"):
            C.Ctx(m, Path("."), {}, {"E001": [td]}, None, None, Path("."))
    with pytest.raises(C.Refused, match="only \\[splits\\].test"):
        C.Ctx("test", Path("."), {}, {"E001": [dd]}, None, None, Path("."))
    with pytest.raises(C.Refused, match="unknown mode"):
        C.Ctx("other", Path("."), {}, {}, None, None, Path("."))
    with pytest.raises(C.Refused, match="only in the project repository"):
        C.test_context(Path("/tmp"))


def test_environment_check_passes_here_and_refuses_a_version_mismatch(tmp_path):
    C.verify_environment()
    (tmp_path / "results/e001").mkdir(parents=True)
    import shutil

    for f in ("uv.lock", ".python-version"):
        shutil.copy(ROOT / f, tmp_path / f)
    for f in ("E001_frozen_manifest.json", "e001_discovery.json"):
        shutil.copy(ROOT / "results/e001" / f, tmp_path / "results/e001" / f)
    (tmp_path / ".python-version").write_text("2.7\n")
    with pytest.raises(C.Refused, match="Python differs"):
        C.verify_environment(tmp_path)
    shutil.copy(ROOT / ".python-version", tmp_path / ".python-version")
    with open(tmp_path / "results/e001/e001_discovery.json", "a") as f:
        f.write(" ")
    with pytest.raises(C.Refused, match="frozen manifest"):
        C.verify_environment(tmp_path)
    shutil.copy(ROOT / "results/e001/e001_discovery.json", tmp_path / "results/e001/e001_discovery.json")
    (tmp_path / "uv.lock").write_text((ROOT / "uv.lock").read_text().replace('name = "numpy"\nversion = "', 'name = "numpy"\nversion = "0.'))
    with pytest.raises(C.Refused, match="numpy"):
        C.verify_environment(tmp_path)


def test_report_fix_only_touches_added_files_and_keeps_the_primary_analysis(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws)
    before = C.sha256_file(ws.promoted / "closeout_analysis.json")
    (ws.root / "lpx/closeout_added.py").write_text("y = 9\n")
    ws.git("add", "-A", "lpx/closeout_added.py")
    ws.git("commit", "-q", "-m", "report fix")
    assert C.report_fix(ws) == "report re-rendered"
    assert C.sha256_file(ws.promoted / "closeout_analysis.json") == before and ws.events()[-1]["event"] == "report_fix"
    (ws.root / "lpx/x.py").write_text("x = 9\n")
    ws.git("add", "-A", "lpx/x.py")
    ws.git("commit", "-q", "-m", "not a report fix")
    with pytest.raises(C.Refused, match="only modify added"):
        C.report_fix(ws)


def test_console_shows_progress_only_and_native_stderr_goes_to_the_sealed_log(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    code = textwrap.dedent(f"""
        import os, sys, warnings
        from pathlib import Path
        sys.path.insert(0, {str(ROOT)!r})
        import tests.test_closeout as T
        from lpx.research import closeout as C
        def noisy(ctx):
            print("SENTINEL_PRINT"); warnings.warn("SENTINEL_WARN"); os.write(2, b"SENTINEL_FD2"); os.write(1, b"SENTINEL_FD1")
            os.system("echo SENTINEL_CHILD 1>&2")
            return T.writer("E001")(ctx)
        r = T.runners(); r["E001"] = noisy
        C.run_attempt(C.Workspace(Path({str(ws.root)!r})), T.ctx_factory(), r, T.fake_analyse)
    """)
    p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env={**os.environ, "PYTHONPATH": str(ROOT)})
    assert "SENTINEL" not in p.stdout and "SENTINEL" not in p.stderr
    log = (ws.promoted / "closeout.log").read_text()
    for s in ("SENTINEL_PRINT", "SENTINEL_WARN", "SENTINEL_FD2", "SENTINEL_FD1", "SENTINEL_CHILD"):
        assert s in log
    assert "E001: done" in p.stdout


REAL_RC = C.load_rc()


@pytest.fixture
def inputs(tmp_path, monkeypatch):
    """Four synthetic input files, an acceptance record matching them, and the wiring pointing at them. No market data."""
    root = tmp_path / "root"
    paths = {n: root / "data" / n / "2026-synthetic.parquet" for n in ("states", "book", "trades", "receipts")}
    for n, p in paths.items():
        p.parent.mkdir(parents=True)
        p.write_text(n)
    monkeypatch.setattr(C, "input_paths", lambda sym, day: paths)
    monkeypatch.setattr(C, "sentinel_inputs", lambda sym: [paths["states"]])
    monkeypatch.setattr(C, "verify_acceptance_run_of_record", lambda rc: None)
    monkeypatch.setattr(C, "MISSING_RECHECK_DELAY_S", 0.0)
    monkeypatch.setattr(C, "ROOT", root)
    rec = {str(paths[n].relative_to(root)): C.sha256_file(paths[n]) for n in C.ACCEPTANCE_AUDITED}
    return SimpleNamespace(paths=paths, root=root, record=rec, status={"sha256": {n: C.sha256_file(p) for n, p in paths.items()}})


@pytest.mark.parametrize("exc", [OSError, MemoryError, ValueError, RuntimeError, PermissionError])
def test_input_check_lets_every_unexpected_failure_through(inputs, monkeypatch, exc):
    monkeypatch.setattr(C, "sha256_file", lambda p: (_ for _ in ()).throw(exc("x")))
    with pytest.raises(exc):
        C.input_mismatch("S", "d", inputs.record)


@pytest.mark.parametrize("name", C.ACCEPTANCE_AUDITED)
def test_input_check_names_a_genuine_hash_mismatch_including_the_book(inputs, name):
    inputs.paths[name].write_text("changed")
    assert C.input_mismatch("S", "d", inputs.record)[0] == f"hash_mismatch:{name}"


def test_input_check_names_missing_files_records_and_hashes(inputs):
    assert C.input_mismatch("S", "d", inputs.record)[0] is None
    assert C.input_mismatch("S", "d", None)[0] == "acceptance_record_missing"
    no_book = {k: v for k, v in inputs.record.items() if "book" not in k}
    assert C.input_mismatch("S", "d", no_book)[0] == "acceptance_hash_missing:book"
    inputs.paths["trades"].unlink()
    assert C.input_mismatch("S", "d", inputs.record)[0] == "input_missing:trades"


def test_a_vanished_data_directory_aborts_and_never_marks_a_session(inputs):
    import shutil

    shutil.rmtree(inputs.paths["book"].parent)
    with pytest.raises(NotADirectoryError):
        C.input_mismatch("S", "d", inputs.record)


def test_data_directory_vanishing_during_hashing_aborts_too(inputs, monkeypatch):
    import shutil

    real = C.sha256_file

    def gone(p):
        if p == inputs.paths["trades"]:
            shutil.rmtree(p.parent)
        return real(p)
    monkeypatch.setattr(C, "sha256_file", gone)
    with pytest.raises(NotADirectoryError):
        C.input_mismatch("S", "d", inputs.record)


def test_run_time_input_rule_never_excludes_a_session_for_its_inputs(inputs, monkeypatch):
    rc = REAL_RC
    called = []
    monkeypatch.setattr(C.E1, "verify_inputs", lambda *a: called.append("e1"))
    monkeypatch.setattr(C.E3, "verify_receipt_inputs", lambda *a: called.append("e3"))
    assert C.verify_session_inputs(rc, "d", inputs.status) is None and called == ["e1", "e3"]
    assert C.verify_session_inputs(rc, "d", {"undefined": True, "reason": "hash_mismatch:book"}) == "undefined (input: hash_mismatch:book)"     # decided before the freeze
    with pytest.raises(C.IntegrityFailure) as e:
        C.verify_session_inputs(rc, "d", {"sha256": {**inputs.status["sha256"], "states": "0"}})
    assert e.value.record() == {"findings": [{"session": "d", "input": "states", "finding": "modified", "observed_sha256": inputs.status["sha256"]["states"]}]}
    inputs.paths["book"].write_text("changed")
    with pytest.raises(C.IntegrityFailure) as e:
        C.verify_session_inputs(rc, "d", inputs.status)
    assert e.value.record() == {"findings": [{"session": "d", "input": "book", "finding": "modified", "observed_sha256": C.sha256_file(inputs.paths["book"])}]}
    assert C.classify(e.value) == "integrity"


@pytest.mark.parametrize("exc", [OSError, MemoryError, ValueError, RuntimeError, KeyError])
def test_run_time_verifier_failures_from_other_frames_are_not_input_results(inputs, monkeypatch, exc):
    monkeypatch.setattr(C, "acceptance_record", lambda rc_, days: {"d": inputs.record})
    monkeypatch.setattr(C.E1, "verify_inputs", lambda *a: (_ for _ in ()).throw(exc("x")))
    with pytest.raises(exc):
        C.verify_session_inputs(REAL_RC, "d", inputs.status)


def test_frozen_verifier_mismatch_from_its_own_frame_is_an_input_result(tmp_path, monkeypatch):
    """The real frozen verifier on a discovery session, with a windows file whose hash differs from the one the state file records."""
    rc = C.load_rc()
    d = sorted(rc["splits"]["train"])[0]
    w = tmp_path / "windows.csv"
    w.write_text("not the windows\n")
    monkeypatch.setattr(C.E1.S, "WINDOWS", w)
    with pytest.raises(RuntimeError) as e:
        C.E1.verify_inputs(rc, [d])
    assert C.frozen_verifier_result(e.value)
    assert not C.frozen_verifier_result(RuntimeError("elsewhere"))
    assert C.verify_session_inputs(rc, d, None) == "undefined (input mismatch: frozen_verifier)"
    pins = {"sha256": {n: C.sha256_file(p) for n, p in C.input_paths(rc["dataset"]["symbol"], d).items()}}
    assert C.verify_session_inputs(rc, d, pins) == "undefined (input mismatch: frozen_verifier)"     # the record's path: bytes match their pins


# ------------------------------------------------------------------------------------------------ the pre-check tool
def precheck_tool():
    sys.path.insert(0, str(ROOT))
    import tools.closeout_precheck as P

    return P


def windows_frame(day="d", status="accepted", spans=((0, 2_000_000_000),)):
    rows = [{"start_us": a, "end_us": b, "duration_s": (b - a) / 1e6, "layer": "joint", "source": "tardis", "symbol": "S", "day": day, "integrity_status": status} for a, b in spans]
    return pl.DataFrame(rows, schema={"start_us": pl.Int64, "end_us": pl.Int64, "duration_s": pl.Float64, "layer": pl.String, "source": pl.String, "symbol": pl.String, "day": pl.String, "integrity_status": pl.String})


def test_session_record_reason_categories_are_distinct(inputs):
    P = precheck_tool()
    good = P.session_record("S", "d", windows_frame(), inputs.record, 600.0)
    assert good["reason"] is None and good["e001_valid"] and good["episode_valid"] and good["e001_reason"] is None and good["episode_reason"] is None and set(good["sha256"]) == {"states", "book", "trades", "receipts"}
    bad = P.session_record("S", "d", windows_frame(status="rejected"), inputs.record, 600.0)
    assert bad["undefined"] and bad["reason"] == "integrity_not_accepted" and not bad["e001_valid"] and bad["e001_reason"] == bad["episode_reason"] == "integrity_not_accepted"
    none = P.session_record("S", "d", windows_frame().clear(), inputs.record, 600.0)
    assert not none["undefined"] and none["reason"] is None and none["e001_reason"] == none["episode_reason"] == "no_accepted_joint_windows"
    short = P.session_record("S", "d", windows_frame(spans=((0, 1_000_000),)), inputs.record, 600.0)
    assert not short["undefined"] and short["e001_valid"] and not short["episode_valid"] and short["e001_reason"] is None and short["episode_reason"] == "no_qualifying_episodes"
    inputs.paths["book"].write_text("changed")
    mismatch = P.session_record("S", "d", windows_frame(), inputs.record, 600.0)
    assert mismatch["undefined"] and mismatch["reason"] == "hash_mismatch:book" and not mismatch["e001_valid"] and not mismatch["episode_valid"]


def test_one_window_not_accepted_undefines_the_session(inputs):
    P = precheck_tool()
    mixed = P.session_record("S", "d", pl.concat([windows_frame(), windows_frame(status="rejected", spans=((3_000_000_000, 4_000_000_000),))]), inputs.record, 600.0)
    assert mixed["reason"] == "integrity_not_accepted" and mixed["undefined"]


def precheck_repo(tmp: Path, monkeypatch, evidence: dict | None = None) -> C.Workspace:
    """A scratch repository on main holding the files an authorisation names (code commit), then passing evidence on that code."""
    ws, _ = repo(tmp)
    ws.git("branch", "-M", "main")
    P = precheck_tool()
    for f in P.PRECHECK_CODE:
        (ws.root / f).parent.mkdir(parents=True, exist_ok=True)
        (ws.root / f).write_text(f"{f}\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "code")
    ws.code_commit = ws.git("rev-parse", "HEAD").strip()
    trees = C.trees(ws)
    for f in P.EVIDENCE:
        e = {"passed": True, "provenance": {"trees": trees}, **(evidence or {}).get(f, {})}
        (ws.root / "results/closeout_dev").mkdir(parents=True, exist_ok=True)
        (ws.root / "results/closeout_dev" / f).write_text(json.dumps(e))
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "evidence")
    return ws


def authorisation(ws: C.Workspace, line: str | None = None, **over) -> str:
    """Commit a valid authorisation naming the code commit, with the owner's entry naming it, plus any overrides."""
    P = precheck_tool()
    a = {"step": P.AUTHORISATION_STEP, "code_commit": ws.code_commit, "sha256": {f: C.sha256_file(ws.root / f) for f in P.PRECHECK_CODE + (C.PROTOCOL,)}, **over}
    p = ws.root / P.AUTHORISATION
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(a))
    h = C.sha256_file(p)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write((line or P.STEP3_APPROVAL).format(h=h) + "\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "authorise")
    return h


def test_step3_authorisation_accepts_only_a_complete_committed_record(tmp_path, monkeypatch):
    P = precheck_tool()
    ws = precheck_repo(tmp_path, monkeypatch)
    out = ws.root / C.INPUT_STATUS
    with pytest.raises(C.Refused, match="no committed authorisation"):
        P.verify_authorisation(ws, out)
    h = authorisation(ws)
    assert P.verify_authorisation(ws, out) == h
    with pytest.raises(C.Refused, match="writes only"):
        P.verify_authorisation(ws, ws.root / "elsewhere.json")
    (ws.root / "untracked.txt").write_text("x")
    with pytest.raises(C.Refused, match="not clean"):
        P.verify_authorisation(ws, out)
    (ws.root / "untracked.txt").unlink()
    monkeypatch.setenv("LPX_ALLOW_DIRTY", "1")
    with pytest.raises(C.Refused, match="LPX_ALLOW_DIRTY"):
        P.verify_authorisation(ws, out)
    monkeypatch.delenv("LPX_ALLOW_DIRTY")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("{}")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "a record exists")
    with pytest.raises(C.Refused, match="already exists"):
        P.verify_authorisation(ws, out)


@pytest.mark.parametrize("over,why", [({"step": "other"}, "not for step 3"), ({"code_commit": "0" * 40}, "strict ancestor"), ({"code_commit": "HEAD"}, "strict ancestor"),
                                      ({"code_commit": "main"}, "strict ancestor"), ({"sha256": {}}, "other files")])
def test_step3_authorisation_refuses_a_wrong_record(tmp_path, monkeypatch, over, why):
    P = precheck_tool()
    ws = precheck_repo(tmp_path, monkeypatch)
    authorisation(ws, **over)
    with pytest.raises(C.Refused, match=why):
        P.verify_authorisation(ws, ws.root / C.INPUT_STATUS)


def test_step3_authorisation_refuses_changed_code_or_no_owner_entry(tmp_path, monkeypatch):
    P = precheck_tool()
    ws = precheck_repo(tmp_path, monkeypatch)
    authorisation(ws)
    (ws.root / "lpx/x.py").write_text("x = 2\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "change after authorisation")
    with pytest.raises(C.Refused, match="changed since"):
        P.verify_authorisation(ws, ws.root / C.INPUT_STATUS)
    ws2 = precheck_repo(tmp_path / "second", monkeypatch) if (tmp_path / "second").mkdir() is None else None
    authorisation(ws2)
    text = (ws2.root / "docs/DECISIONS.md").read_text().splitlines()[0]
    (ws2.root / "docs/DECISIONS.md").write_text(text + "\n")
    ws2.git("add", "-A")
    ws2.git("commit", "-q", "-m", "drop the entry")
    with pytest.raises(C.Refused, match="no owner entry"):
        P.verify_authorisation(ws2, ws2.root / C.INPUT_STATUS)


def test_step3_authorisation_binds_values_commit_branch_entry_and_once(tmp_path, monkeypatch):
    P = precheck_tool()
    out = lambda ws: ws.root / C.INPUT_STATUS
    ws = precheck_repo(tmp_path / "a", monkeypatch) if (tmp_path / "a").mkdir() is None else None
    authorisation(ws, sha256={**{f: C.sha256_file(ws.root / f) for f in P.PRECHECK_CODE + (C.PROTOCOL,)}, "tools/closeout_precheck.py": "0" * 64})
    with pytest.raises(C.Refused, match="other files"):                     # a hash value, not only the names
        P.verify_authorisation(ws, out(ws))
    ws = precheck_repo(tmp_path / "b", monkeypatch) if (tmp_path / "b").mkdir() is None else None
    ws.git("checkout", "-q", "-b", "side")
    (ws.root / "side.txt").write_text("x")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "side")
    side = ws.git("rev-parse", "HEAD").strip()
    ws.git("checkout", "-q", "main")
    authorisation(ws, code_commit=side)
    with pytest.raises(C.Refused, match="strict ancestor"):                 # a real commit that is not an ancestor
        P.verify_authorisation(ws, out(ws))
    ws = precheck_repo(tmp_path / "c", monkeypatch) if (tmp_path / "c").mkdir() is None else None
    authorisation(ws, line="owner note naming {h} for something else")
    with pytest.raises(C.Refused, match="no owner entry"):
        P.verify_authorisation(ws, out(ws))
    ws = precheck_repo(tmp_path / "d", monkeypatch) if (tmp_path / "d").mkdir() is None else None
    authorisation(ws)
    ws.git("checkout", "-q", "-b", "other")
    with pytest.raises(C.Refused, match="only on main"):
        P.verify_authorisation(ws, out(ws))
    ws.git("checkout", "-q", "main")
    out(ws).parent.mkdir(parents=True, exist_ok=True)
    out(ws).write_text("{}")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "record")
    ws.git("rm", "-q", C.INPUT_STATUS)
    ws.git("commit", "-q", "-m", "removed")
    with pytest.raises(C.Refused, match="once existed"):
        P.verify_authorisation(ws, out(ws))


def test_step3_authorisation_reads_the_committed_record_and_entry(tmp_path, monkeypatch):
    P = precheck_tool()
    ws = precheck_repo(tmp_path, monkeypatch)
    authorisation(ws)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write("uncommitted\n")
    ws.git("update-index", "--assume-unchanged", "docs/DECISIONS.md")
    with pytest.raises(C.Refused, match="index flags"):
        P.verify_authorisation(ws, ws.root / C.INPUT_STATUS)
    ws.git("update-index", "--no-assume-unchanged", "docs/DECISIONS.md")
    ws.git("checkout", "--", "docs/DECISIONS.md")
    monkeypatch.setenv("GIT_INDEX_FILE", str(tmp_path / "other_index"))
    with pytest.raises(C.Refused, match="GIT_INDEX_FILE"):
        P.verify_authorisation(ws, ws.root / C.INPUT_STATUS)


@pytest.mark.parametrize("evidence,why", [({"precheck_faults.json": {"passed": False}}, "did not pass"), ({"dryrun_check3_rehearsal.json": {"provenance": {"trees": {"lpx": "0"}}}}, "other code")])
def test_step3_waits_for_passing_evidence_on_the_authorised_code(tmp_path, monkeypatch, evidence, why):
    P = precheck_tool()
    ws = precheck_repo(tmp_path, monkeypatch, evidence)
    authorisation(ws)
    with pytest.raises(C.Refused, match=why):
        P.verify_authorisation(ws, ws.root / C.INPUT_STATUS)


def test_step3_refuses_a_scratch_repository_since_reads_come_from_the_project(tmp_path):
    P = precheck_tool()
    ws, _ = repo(tmp_path)
    with pytest.raises(C.Refused, match="only in the project repository"):
        P.run(ws.root / C.INPUT_STATUS, True, ws)


def test_precheck_lists_and_pins_everything_its_result_depends_on():
    P = precheck_tool()
    for f in ("tools/closeout_precheck.py", "lpx/research/closeout.py", "configs/research_v1.toml", "configs/e003_v1.toml", "configs/e004_v1.toml", "configs/closeout_v1.toml",
              "results/acceptance_001/windows.csv", "results/acceptance_001/summary.json", "results/e004_prefreeze/schedule_hashes.json"):
        assert f in P.PRECHECK_CODE, f
    for f in ("dryrun_check2_reproduction.json", "dryrun_check3_rehearsal.json", "fault_injection_realpath.json", "precheck_faults.json", "comparison_key_inventory.json"):
        assert f in P.EVIDENCE, f
    section2 = (C.PROTOCOL, "docs/experiments/E002.md", "docs/experiments/E003.md", "docs/experiments/E004.md", "configs/research_v1.toml", "configs/e002_v1.toml", "configs/e003_v1.toml",
                "configs/e004_v1.toml", "configs/closeout_v1.toml", "pyproject.toml", "uv.lock", ".python-version", "results/e003/e003_analysis.json", "results/e001/e001_discovery.json",
                "results/e004_prefreeze/schedule_hashes.json", "results/acceptance_001/summary.json", "results/acceptance_001/sensitivity.json", "results/acceptance_001/windows.csv",
                "results/acceptance_001/windows_sensitivity.csv", C.INPUT_STATUS, C.FIT_MANIFEST, "lpx/research/closeout.py", "lpx/research/closeout_analysis.py", "tools/closeout_fits.py",
                "tools/closeout_precheck.py", "tools/closeout_dryrun.py", "tests/test_closeout.py", "configs/closeout_v1.toml")
    for f in section2:
        assert f in C.TEST_MODE_PINS, f


def write_windows_csv(path: Path, rows: list[dict]) -> None:
    pl.DataFrame(rows).write_csv(path)


def test_accepted_windows_keeps_only_this_symbols_joint_tardis_rows_on_the_listed_days(tmp_path, monkeypatch):
    P = precheck_tool()
    base = {"start_us": 0, "end_us": 2_000_000_000, "duration_s": 2000.0, "layer": "joint", "source": "tardis", "symbol": "S", "day": "d1", "integrity_status": "accepted", "extra": "unlisted"}
    rows = [base, {**base, "layer": "book"}, {**base, "source": "other"}, {**base, "symbol": "BTC"}, {**base, "day": "d9"}, {**base, "day": "d2", "start_us": 5}]
    w = tmp_path / "windows.csv"
    write_windows_csv(w, rows)
    monkeypatch.setattr(P.S, "WINDOWS", w)
    got = P.accepted_windows("S", ["d1", "d2"])
    assert got.columns == P.COLUMNS and sorted(got["day"].to_list()) == ["d1", "d2"]


def test_build_status_gives_each_session_its_own_windows_and_the_frozen_episode_threshold(tmp_path, monkeypatch):
    P = precheck_tool()
    seen = []
    monkeypatch.setattr(C, "acceptance_record", lambda rc, days: {})
    monkeypatch.setattr(P, "accepted_windows", lambda sym, days: pl.concat([windows_frame(day="d1"), windows_frame(day="d2", spans=((7, 8),))]))
    monkeypatch.setattr(P, "session_record", lambda sym, d, g, rec, ep: seen.append((d, g["day"].unique().to_list(), ep)) or {})
    P.build_status(REAL_RC, ["d1", "d2"], 600.0)
    assert seen == [("d1", ["d1"], 600.0), ("d2", ["d2"], 600.0)]
    cfg3 = __import__("tomllib").loads((ROOT / "configs/e003_v1.toml").read_text())
    assert cfg3["scope"]["min_episode_s"] == 600


def test_precheck_record_contents_provenance_and_write_once(inputs, tmp_path, monkeypatch):
    P = precheck_tool()
    calls = []
    monkeypatch.setattr(C, "acceptance_record", lambda rc, days: {d: inputs.record for d in days})
    monkeypatch.setattr(P, "accepted_windows", lambda sym, days: pl.concat([windows_frame(day=d) for d in days]))
    monkeypatch.setattr(P, "schedule_check", lambda days: calls.append(len(days)) or 7)
    monkeypatch.setattr(P, "refuse_dirty_scope", lambda ws: None)
    monkeypatch.setattr(C, "load_rc", lambda: REAL_RC)
    out = tmp_path / "status.json"
    res = P.run(out, False, C.Workspace(ROOT))
    rec = json.loads(out.read_text())
    assert rec == json.loads(json.dumps(res)) and calls == [20] and rec["schedules_verified_date_only"] == 7
    prov = rec["provenance"]
    for k in ("mode", "git_commit", "code_fingerprint", "trees", "precheck_sha256", "uv_lock_sha256", "python_version", "packages", "windows_csv_sha256", "acceptance_summary_sha256", "authorisation_sha256", "utc"):
        assert k in prov, k
    assert prov["mode"] == "stand-ins" and prov["authorisation_sha256"] is None and prov["windows_csv_sha256"] == C.sha256_file(P.S.WINDOWS)
    s = next(iter(rec["sessions"].values()))
    assert s["windows"] and s["episodes"] and set(s["sha256"]) == {"states", "book", "trades", "receipts"}
    with pytest.raises(C.Refused, match="never overwritten"):
        P.run(out, False, C.Workspace(ROOT))


def test_precheck_main_rejects_both_or_neither_mode_and_reports_a_written_record(tmp_path, monkeypatch, capsys):
    P = precheck_tool()
    for argv in (["p", str(tmp_path / "o.json"), "--stand-ins", "--test-days"], ["p", str(tmp_path / "o.json")]):
        monkeypatch.setattr(sys, "argv", argv)
        with pytest.raises(SystemExit):
            P.main()
    out = tmp_path / "w.json"

    def written_then_fail(o, test_days):
        o.write_text("{}")
        raise OSError("directory fsync")
    monkeypatch.setattr(P, "run", written_then_fail)
    monkeypatch.setattr(sys, "argv", ["p", str(out), "--stand-ins"])
    assert P.main() == 3 and "a complete record exists" in capsys.readouterr().err


def test_no_parquet_reader_is_called_by_the_input_check(inputs, monkeypatch):
    import pyarrow.parquet as pq

    called = []
    import pyarrow.dataset as pds
    import pyarrow.parquet.core as pqc

    for mod, names in ((pq, ("read_metadata", "read_schema", "read_table", "ParquetFile")), (pqc, ("read_metadata", "read_schema", "read_table", "ParquetFile")),
                       (pds, ("dataset",)), (pl, ("read_parquet", "scan_parquet", "read_parquet_schema", "read_parquet_metadata"))):
        for n in names:
            if hasattr(mod, n):
                monkeypatch.setattr(mod, n, lambda *a, n=n, **k: called.append(n))
    P = precheck_tool()
    P.session_record("S", "d", windows_frame(), inputs.record, 600.0)
    C.input_mismatch("S", "d", inputs.record)
    assert called == []


def test_step3_refused_in_this_repository_before_any_input_is_read(tmp_path, monkeypatch):
    P = precheck_tool()
    read = []
    monkeypatch.setattr(C, "input_mismatch", lambda *a: read.append(a))
    monkeypatch.setattr(P, "accepted_windows", lambda *a: read.append(a))
    monkeypatch.setattr(C, "acceptance_record", lambda *a: read.append(a))
    with pytest.raises(C.Refused):
        P.run(tmp_path / "o.json", True)
    assert read == [] and not (tmp_path / "o.json").exists()


def test_exclusive_write_is_atomic_and_never_overwrites(tmp_path, monkeypatch):
    p = tmp_path / "status.json"
    C.write_exclusive(p, "first")
    with pytest.raises(C.Refused, match="never overwritten"):
        C.write_exclusive(p, "second")
    assert p.read_text() == "first" and [x.name for x in tmp_path.iterdir()] == ["status.json"]
    q = tmp_path / "other.json"
    monkeypatch.setattr(C.os, "link", lambda a, b: (_ for _ in ()).throw(OSError("disk")))
    with pytest.raises(OSError):
        C.write_exclusive(q, "x")
    assert not q.exists() and [x.name for x in tmp_path.iterdir()] == ["status.json"]


def test_precheck_on_real_stand_ins_reads_only_the_declared_files(tmp_path):
    """Real discovery stand-ins, in a fresh process: Parquet readers are disabled, and every file opened from Python is recorded."""
    out = tmp_path / "status.json"
    sys.path.insert(0, str(ROOT))
    from tools.closeout_dryrun import READ_AUDIT

    r = subprocess.run([sys.executable, "-c", READ_AUDIT.format(root=str(ROOT), out=str(out), skip_clean=True)], capture_output=True, text=True, env={k: v for k, v in {**os.environ, "PYTHONPATH": str(ROOT)}.items() if k != "LPX_ALLOW_DIRTY"})
    assert r.returncode == 0, r.stderr[-400:]
    got = json.loads(r.stdout.strip().splitlines()[-1])
    rc = C.load_rc()
    assert got["days"] == sorted(rc["splits"]["train"] + rc["splits"]["validation"])[10:]
    allowed = {str(p) for d in got["days"] for p in C.input_paths(rc["dataset"]["symbol"], d).values()} | {str(ROOT / "results/acceptance_001/summary.json"), str(ROOT / "results/acceptance_001/windows.csv")}
    assert set(got["opened"]) == allowed, got["opened"]                # exactly the declared reads, nothing missing and nothing extra
    res = json.loads(out.read_text())
    assert res["provenance"]["mode"] == "stand-ins" and res["provenance"]["git_commit"] and res["provenance"]["trees"] and all(set(s["sha256"]) == {"states", "book", "trades", "receipts"} for s in res["sessions"].values())
    assert all(not s["undefined"] and s["e001_valid"] for s in res["sessions"].values())


@pytest.mark.parametrize("exc", [OSError, MemoryError, ValueError, RuntimeError])
def test_precheck_tool_aborts_on_real_stand_ins_with_no_record(tmp_path, monkeypatch, capsys, exc):
    """An injected failure on the second file of a real discovery stand-in: exit code 3, no record, type and place only on the console."""
    P = precheck_tool()
    real, n = C.sha256_file, []

    def fail(p):
        if "/data/" in str(p):
            n.append(p)
            if len(n) == 2:
                raise exc("secret-value")
        return real(p)
    monkeypatch.setattr(C, "sha256_file", fail)
    monkeypatch.setattr(P, "refuse_dirty_scope", lambda ws: None)
    out = tmp_path / "status.json"
    monkeypatch.setattr(sys, "argv", ["closeout_precheck.py", str(out), "--stand-ins"])
    assert P.main() == 3
    err = capsys.readouterr().err
    assert not out.exists() and not list(tmp_path.iterdir()) and exc.__name__ in err and "secret-value" not in err


def test_precheck_source_has_no_footer_or_verifier_reads():
    import inspect

    for fn in (C.input_mismatch, C.acceptance_record, C.require_data_roots, C.require_whole_volume, C.sentinel_inputs, C.input_paths):
        body = inspect.getsource(fn)
        for x in ("read_metadata", "read_schema", "read_parquet", "ParquetFile", "pyarrow", "dataset("):
            assert x not in body, (fn.__name__, x)
    src = (ROOT / "tools/closeout_precheck.py").read_text()
    for x in ("read_metadata", "verify_inputs", "verify_receipt_inputs", "read_parquet", "sensitivity.json", "except Exception"):
        assert x not in src, x


def test_session_context_on_stand_ins_input_status_and_fit_manifest(tmp_path, monkeypatch):
    rc = C.load_rc()
    d = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    days = d[10:12]
    monkeypatch.setattr(C, "verify_session_inputs", lambda rc_, day, st: st.get("undefined_reason"))
    monkeypatch.setattr(C, "verify_pins", lambda *a: None)          # these status records carry no pins
    monkeypatch.setattr(C, "relative_ticks", lambda rc_, ds: {x: 1.0 for x in ds})
    status = {days[0]: {"e001_valid": True, "episode_valid": False, "undefined_reason": None}, days[1]: {"e001_valid": False, "episode_valid": False, "undefined_reason": "undefined (input)"}}
    ctx = C.session_context(ROOT, "rehearsal", days, "rehearsal", d[:10], status)(tmp_path, print)
    assert ctx.sessions["E001"] == [days[0]] and ctx.sessions["E002"] == [] and ctx.all_days == days
    assert ctx.expected_trained(days[0]) == d[:10]
    written = json.loads((tmp_path / "closeout_input_status.json").read_text())
    assert written["undefined"][days[1]] == "undefined (input)" and written["no_valid_unit"][days[0]]["E002"] == "no valid unit"
    ctx.recheck()                                       # unchanged: passes
    monkeypatch.setattr(C, "verify_session_inputs", lambda rc_, day, st: "undefined (input mismatch)")
    monkeypatch.setattr(C, "verify_pins", lambda *a: None)          # these status records carry no pins
    with pytest.raises(RuntimeError, match="inputs changed"):
        ctx.recheck()


def test_nothing_to_recover_on_a_fresh_ledger(tmp_path):
    ws, h = repo(tmp_path)
    with pytest.raises(C.Refused, match="nothing to recover"):
        C.recover(ws)


# ------------------------------------------------------------------------------------------------ fit artifacts
def test_fit_artifacts_round_trip_exactly(tmp_path):
    fits, a = C.load_e004_fit(ROOT / "results/closeout_fits/all15")
    assert a["before"] == "2026-06-01" and len(a["sessions"]) == 15
    for cell, fit in fits.items():
        assert json.loads(json.dumps(C.cell_fit_to_json(fit), sort_keys=True)) == json.loads(json.dumps(a["cells"][cell], sort_keys=True))
    assert list(fits) == list(C.CELL_ORDER)            # the order e004_lambda.csv depends on
    assert list(fits["D1_S"].lam)[:3] == [("y_k", "RF"), ("y_k", "UA"), ("y_k", "PL")]
    models, a3 = C.load_e003_fit(ROOT / "results/closeout_fits/all15", [1, 5, 30])
    assert list(a3["sessions"]) == a["sessions"] and set(models) == {1, 5, 30}
    rc = C.load_rc()
    assert not set(a["sessions"]) & set(rc["splits"]["test"])


def test_wrong_trained_on_is_refused():
    ctx = SimpleNamespace(expected_trained=lambda d: ["a"])
    with pytest.raises(RuntimeError, match="trained on other sessions"):
        C.check_trained(ctx, "d", {"sessions": ["a", "b"]})


def test_fit_tool_refuses_test_days():
    sys.path.insert(0, str(ROOT))
    import tools.closeout_fits as T

    rc = C.load_rc()
    with pytest.raises(PermissionError):
        T.prepare([rc["splits"]["test"][0]], rc)


def test_precheck_refuses_test_days_in_this_repository(tmp_path):
    r = subprocess.run([sys.executable, str(ROOT / "tools/closeout_precheck.py"), str(tmp_path / "o.json"), "--test-days"], capture_output=True, text=True,
                       env={**os.environ, "PYTHONPATH": str(ROOT)})
    assert r.returncode == 2 and "refused" in r.stderr and not (tmp_path / "o.json").exists()


def test_operating_system_permission_errors_are_environment_and_frozen_refusals_are_not(tmp_path):
    import errno as E

    assert C.classify(PermissionError(E.EACCES, "denied", "/data/x.parquet")) == "environment"
    assert C.is_environment(PermissionError(E.EPERM, "operation not permitted"))
    ro = tmp_path / "read_only"
    ro.mkdir()
    ro.chmod(0o500)
    try:
        with pytest.raises(PermissionError) as e:
            C.frozen_copy_e002_tables(pl.DataFrame({"a": [1]}), pl.DataFrame({"a": [1]}), ro)     # polars: a denied write with no errno
    finally:
        ro.chmod(0o700)
    assert e.value.errno is None and C.classify(e.value) == "environment"
    with pytest.raises(PermissionError) as e:
        C.E1.run(["test"])                                     # frozen code's own refusal
    assert not C.is_environment(e.value) and C.classify(e.value) == "software"


@pytest.mark.parametrize("how", ["deleted", "dangling link", "directory gone", "not pinned"])
def test_a_missing_pinned_input_at_run_time_is_an_integrity_failure(inputs, tmp_path, how):
    import shutil

    p = inputs.paths["trades"]
    status = inputs.status
    if how == "deleted":
        p.unlink()
    elif how == "dangling link":
        p.unlink()
        p.symlink_to(tmp_path / "unmounted" / "trades.parquet")
    elif how == "directory gone":
        shutil.rmtree(p.parent)
    else:
        status = {"sha256": {k: v for k, v in status["sha256"].items() if k != "trades"}}
    with pytest.raises(C.IntegrityFailure) as e:
        C.verify_session_inputs(REAL_RC, "d", status)
    assert [(f["input"], f["finding"]) for f in e.value.findings] == [("trades", "not pinned by the input-status record" if how == "not pinned" else "missing")]
    assert C.classify(e.value) == "integrity"


def test_a_pinned_input_gone_between_its_stat_and_its_read_is_an_integrity_failure(inputs, monkeypatch):
    monkeypatch.setattr(C, "sha256_file", lambda p: (_ for _ in ()).throw(FileNotFoundError(2, "gone", str(p))))
    with pytest.raises(C.IntegrityFailure) as e:
        C.verify_session_inputs(REAL_RC, "d", inputs.status)
    assert [f["finding"] for f in e.value.findings] == ["missing"] * 4 and C.classify(e.value) == "integrity"


@pytest.mark.parametrize("name", ["states", "book", "trades", "receipts"])
def test_a_pinned_input_with_other_bytes_is_an_integrity_failure_never_an_undefined_session(inputs, name):
    inputs.paths[name].write_text("other bytes")
    with pytest.raises(C.IntegrityFailure) as e:
        C.verify_session_inputs(REAL_RC, "d", inputs.status)
    assert e.value.findings == [C.integrity_finding("d", name, "modified", C.sha256_file(inputs.paths[name]))] and C.classify(e.value) == "integrity"


def test_an_unreadable_pinned_input_is_an_environment_failure_not_an_exclusion(inputs, monkeypatch):
    monkeypatch.setattr(C, "sha256_file", lambda p: (_ for _ in ()).throw(OSError(5, "EIO")))
    with pytest.raises(OSError) as e:
        C.verify_session_inputs(REAL_RC, "d", inputs.status)
    assert C.classify(e.value) == "environment"


def test_a_stub_tree_or_dangling_link_is_not_a_missing_input(inputs, monkeypatch, tmp_path):
    gone = tmp_path / "gone.parquet"
    monkeypatch.setattr(C, "sentinel_inputs", lambda sym: [gone])
    content = inputs.paths["trades"].read_text()
    inputs.paths["trades"].unlink()                               # a miss on a volume whose discovery inputs are gone too
    with pytest.raises(FileNotFoundError) as e:
        C.input_mismatch("S", "d", inputs.record)
    inputs.paths["trades"].write_text(content)
    assert C.classify(e.value) == "environment"
    monkeypatch.setattr(C, "sentinel_inputs", lambda sym: [inputs.paths["states"]])
    inputs.paths["book"].unlink()
    inputs.paths["book"].symlink_to(tmp_path / "unmounted" / "book.parquet")
    with pytest.raises(FileNotFoundError):
        C.input_mismatch("S", "d", inputs.record)


def summary_files(root: Path, commit: str, sens_commit: str | None = None) -> None:
    (root / "results/acceptance_001").mkdir(parents=True, exist_ok=True)
    (root / "results/acceptance_001/summary.json").write_text(json.dumps({"provenance": {"git_commit": commit, "git_dirty": False}, "tardis": []}))
    (root / "results/acceptance_001/sensitivity.json").write_text(json.dumps({"provenance": {"git_commit": sens_commit or commit, "git_dirty": False}}))


def test_a_summary_not_from_the_run_of_record_aborts_and_never_undefines_sessions(inputs, monkeypatch):
    summary_files(inputs.root, "not-the-run-of-record")
    with pytest.raises(RuntimeError, match="run of record") as e:
        C.acceptance_record(REAL_RC, ["d"])
    assert not C.frozen_verifier_result(e.value)
    with pytest.raises(RuntimeError, match="run of record"):
        C.verify_session_inputs(REAL_RC, "d", None)
    monkeypatch.undo()                                               # the real run-of-record check, on the record's path too
    monkeypatch.setattr(C, "input_paths", lambda sym, day: inputs.paths)
    monkeypatch.setattr(C, "ROOT", inputs.root)
    called = []
    monkeypatch.setattr(C.E1, "verify_inputs", lambda *a: called.append(1))
    with pytest.raises(RuntimeError, match="run of record"):
        C.verify_session_inputs(REAL_RC, "d", inputs.status)
    assert called == []


def test_a_run_wide_sensitivity_fault_aborts_before_the_frozen_verifiers(inputs, monkeypatch):
    monkeypatch.setattr(C, "acceptance_record", lambda rc_, days: {"d": inputs.record})
    monkeypatch.undo()
    monkeypatch.setattr(C, "input_paths", lambda sym, day: inputs.paths)
    monkeypatch.setattr(C, "sentinel_inputs", lambda sym: [inputs.paths["states"]])
    monkeypatch.setattr(C, "ROOT", inputs.root)
    monkeypatch.setattr(C, "acceptance_record", lambda rc_, days: {"d": inputs.record})
    summary_files(inputs.root, REAL_RC["dataset"]["acceptance_git_commit"], sens_commit="other")
    called = []
    monkeypatch.setattr(C.E1, "verify_inputs", lambda *a: called.append(1))
    with pytest.raises(RuntimeError, match="sensitivity.json is not from the acceptance run of record"):
        C.verify_session_inputs(REAL_RC, "d", inputs.status)
    assert called == []


def test_session_context_refuses_test_days_before_any_read(monkeypatch):
    read = []
    monkeypatch.setattr(C, "verify_session_inputs", lambda *a: read.append(a))
    monkeypatch.setattr(C, "relative_ticks", lambda *a: read.append(a))
    rc = C.load_rc()
    disc = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    with pytest.raises(C.Refused, match="refuse every test day"):
        C.session_context(ROOT, "rehearsal", [rc["splits"]["test"][0]], "rehearsal", disc[:10], {})
    with pytest.raises(C.Refused, match="refuse every test day"):
        C.session_context(ROOT, "rehearsal", disc[10:11], "rehearsal", disc[:10], {}, sessions={"E001": [rc["splits"]["test"][0]]})
    with pytest.raises(C.Refused, match="accepts only"):
        C.session_context(ROOT, "test", disc[:1], "all15", disc, {})
    assert read == []


def status_ws(tmp: Path) -> tuple[C.Workspace, dict]:
    """A scratch repository with a committed step-3 authorisation and acceptance files, and a valid input-status record for it."""
    ws, _ = repo(tmp)
    for rel, text in (("results/acceptance_001/windows.csv", "w\n"), ("results/acceptance_001/summary.json", "{}"), (C.AUTHORISATION, '{"step": "x"}')):
        (ws.root / rel).parent.mkdir(parents=True, exist_ok=True)
        (ws.root / rel).write_text(text)
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "step 3 inputs")
    days = REAL_RC["splits"]["test"]
    rec = {"provenance": {"mode": "test", "authorisation_sha256": C.sha256_file(ws.root / C.AUTHORISATION), "git_commit": ws.git("rev-parse", "HEAD").strip(),
                          "windows_csv_sha256": C.sha256_file(ws.root / "results/acceptance_001/windows.csv"), "acceptance_summary_sha256": C.sha256_file(ws.root / "results/acceptance_001/summary.json")},
           "sessions": {d: {"undefined": False, "reason": None, "e001_valid": True, "episode_valid": True, "e001_reason": None, "episode_reason": None,
                            "sha256": {n: "ab" * 32 for n in C.INPUT_NAMES}} for d in days}}
    return ws, rec


@pytest.mark.parametrize("change,why", [
    (lambda r, ws: r["provenance"].update(mode="stand-ins"), "not made by an authorised step 3"),
    (lambda r, ws: r["provenance"].update(authorisation_sha256="a" * 64), "does not name the committed step-3 authorisation"),
    (lambda r, ws: r["provenance"].update(git_commit="HEAD"), "no commit that is an ancestor"),
    (lambda r, ws: r["provenance"].update(git_commit="0" * 40), "no commit that is an ancestor"),
    (lambda r, ws: (ws.root / "results/acceptance_001/windows.csv").write_text("changed"), "changed since"),
    (lambda r, ws: r.update(sessions={}), "exactly the test sessions"),
    (lambda r, ws: next(iter(r["sessions"].values())).update(undefined=True), "disagrees with its reason"),
    (lambda r, ws: next(iter(r["sessions"].values())).update(undefined=True, reason="OSError"), "not one of section 1's codes"),
    (lambda r, ws: next(iter(r["sessions"].values())).update(e001_valid=False, e001_reason="anything"), "not one of section 1's codes"),
    (lambda r, ws: next(iter(r["sessions"].values())).update(episode_valid=False), "disagrees with episode_reason"),
    (lambda r, ws: next(iter(r["sessions"].values()))["sha256"].pop("receipts"), "does not pin exactly the session's four inputs"),
    (lambda r, ws: next(iter(r["sessions"].values()))["sha256"].update(extra="ab" * 32), "does not pin exactly the session's four inputs"),
    (lambda r, ws: next(iter(r["sessions"].values()))["sha256"].update(book="AB" * 32), "does not pin exactly the session's four inputs"),
    (lambda r, ws: next(iter(r["sessions"].values())).pop("sha256"), "does not pin exactly the session's four inputs"),
])
def test_input_status_record_must_come_from_step3_and_agree_with_itself(tmp_path, change, why):
    ws, rec = status_ws(tmp_path)
    C.verify_input_status_record(ws, rec, REAL_RC["splits"]["test"])
    change(rec, ws)
    with pytest.raises(C.Refused, match=why):
        C.verify_input_status_record(ws, rec, REAL_RC["splits"]["test"])


def test_input_status_record_accepts_section1_codes_and_no_unit_codes(tmp_path):
    ws, rec = status_ws(tmp_path)
    d0, d1 = REAL_RC["splits"]["test"][:2]
    rec["sessions"][d0] = {"undefined": True, "reason": "hash_mismatch:book", "e001_valid": False, "episode_valid": False, "e001_reason": "hash_mismatch:book", "episode_reason": "hash_mismatch:book"}
    rec["sessions"][d1] = {"undefined": False, "reason": None, "e001_valid": True, "episode_valid": False, "e001_reason": None, "episode_reason": "no_qualifying_episodes",
                           "sha256": {n: "ab" * 32 for n in C.INPUT_NAMES}}
    C.verify_input_status_record(ws, rec, REAL_RC["splits"]["test"])


def test_test_context_runs_the_record_check(tmp_path, monkeypatch):
    p = tmp_path / "input_status.json"
    p.write_text(json.dumps({"provenance": {"mode": "stand-ins"}, "sessions": {}}))
    monkeypatch.setattr(C, "INPUT_STATUS", str(p))
    with pytest.raises(C.Refused, match="not made by an authorised step 3"):
        C.test_context(ROOT)


def test_input_integrity_rule_is_separate_from_software_failures():
    assert C.verify_session_inputs(C.load_rc(), "2025-03-01", {"undefined": True}) == "undefined (input)"


# ------------------------------------------------------------------------------------------------ marked blocks against frozen source
def frozen_source(name: str) -> list[str]:
    """The frozen file at the baseline commit, not the working tree."""
    return subprocess.run(["git", "show", f"{C.BASELINE}:lpx/research/{name}"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()


def clean(lines: list[str]) -> list[str]:
    """Code lines with indentation kept (a line moved out of a loop must not pass), comments and docstrings dropped."""
    out = []
    for x in lines:
        s = x.split("  # ")[0].rstrip() if "  # " in x and '"' not in x.split("  # ")[1] else x.rstrip()
        if s.strip() and not s.strip().startswith("#") and not s.strip().startswith('"""'):
            out.append(s)
    return out


def func_src(path: Path, name: str) -> list[str]:
    import ast

    src = path.read_text()
    node = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == name)
    return src.splitlines()[node.lineno:node.end_lineno]


def ordered_new_and_deleted(frozen: list[str], copy: list[str]) -> tuple[list[str], list[str]]:
    """Lines added to and deleted from the frozen sequence, by an order-preserving diff."""
    import difflib

    a, b = [x.strip() + f"@{(len(x) - len(x.lstrip())) // 4}" for x in frozen], [x.strip() + f"@{(len(x) - len(x.lstrip())) // 4}" for x in copy]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    new, gone = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            gone += a[i1:i2]
        if tag in ("replace", "insert"):
            new += b[j1:j2]
    return new, gone


def body_of_run(name: str, start: str, end: str) -> list[str]:
    src = frozen_source(name)
    i = next(k for k, x in enumerate(src) if start in x)
    j = next(k for k, x in enumerate(src) if k > i and end in x)
    return src[i:j + 1]


def test_e004_marked_block_equals_the_frozen_session_body_in_order_with_indentation():
    want = clean(body_of_run("e004.py", "# D0 through the participant path: identity", "policies ({time.time() - t0:.0f} s)"))
    want = [x[4:] for x in want]                       # the copy is one level shallower than run()'s loop
    want = ["    fits = loaded_fits" if "fits = {cell: fit_cell(" in x else x for x in want]
    got = clean(func_src(ROOT / "lpx/research/closeout.py", "frozen_copy_e004_session"))
    i = got.index(want[0])
    assert got[i:] == want


def test_e004_table_block_equals_the_frozen_tables():
    want = [x[0:] for x in clean(body_of_run("e004.py", "gross = pl.DataFrame(prows, infer_schema_length=None)", '"e004_windows_by_session.csv": pl.DataFrame(wrows'))]
    got = clean(func_src(ROOT / "lpx/research/closeout.py", "frozen_copy_e004_tables"))
    assert got[:len(want)] == want


# every difference between a marked block and frozen run() is listed here and was reviewed; anything else fails
MARKED = {
    "frozen_copy_e002": ("e002.py", "for d in days:", 'net = fee_overlay(gross, cfg["fees"])', "S, run_session, fee_overlay",
                         {"new": ['hook("E002", d)', 'E1.normalized_path("binance_vision"', '"split": split_of(rc, d)', 'drop("first_cap_bind_us")', "sym, tick =", "rows = []", "return gross, net"],
                          "gone": ['normalized_path("binance_vision"', '"split": "train" if d in rc', "gross = pl.DataFrame(rows)"]}),
    "frozen_copy_e003": ("e003.py", "gross, frows, cal, models_out = [], [], [], {}", 'print(f"{d}: evaluated', "fc = cfg",
                         {"new": ["gross, frows, cal, models_out, unrec =", "for d in days:", 'ctx.hook("E003", d)', "load_e003_fit(ctx.fit_dir(d)", "check_trained(ctx, d, art)", 'rv_gate = art["rv_gate"]',
                                  "models_out[d] =", "E3.load_session(cfg, d)", "E3.features(cfg, st, tr, eps)", "unrec[d] =", "E3.forecast_rows", "E3.attach(states", "split = split_of(ctx.rc, d)",
                                  "E3.run_session(states", "return gross, frows", 'fc = cfg["features"]', "to_trades(tr"],
                          "gone": ["gross, frows, cal, models_out = [], [], [], {}", "for i, d in enumerate(days):", "if i < k0:", "continue", "train = {x: thin[x]", "models = {h: fit_models", "rv_med =", '["rv_60s"].median())',
                                   "rv_gate = pc[", "models_out[d] = {", "**{f\"h{h:g}s_{m}\"", "st, tr, eps = load_session", "ft = features", "forecast_rows(d, ft", "attach(states", "split = \"train\"", "for r in run_session(states"]}),
}


@pytest.mark.parametrize("name", list(MARKED))
def test_e002_e003_marked_blocks_differ_from_frozen_only_as_listed(name):
    file, start, end, skip, allowed = MARKED[name]
    frozen = clean(body_of_run(file, start, end))
    copy = [x for x in clean(func_src(ROOT / "lpx/research/closeout.py", name))]
    new, gone = ordered_new_and_deleted(frozen, copy)
    bad_new = [x for x in new if not any(k in x for k in allowed["new"] + [skip])]
    bad_gone = [x for x in gone if not any(k in x for k in allowed["gone"])]
    assert bad_new == [] and bad_gone == []


E001_REMOVED = ["e, sp =", "sets = session_sets", 'if "test" in sets:', "raise PermissionError", 'if "train" not in sets:', "raise ValueError", "require_clean()", "days = sorted(", 'sym = cfg["dataset"]["symbol"]',
                "inputs = verify_inputs", "sessions = {d: Session", "train_q =", "edges = (float", '"run_at_utc"', '"provenance"', '"windows_sensitivity_csv_sha256"', '"primary_spec"', '"sessions": "all discovery"', '"size_tercile_edges_base_qty": edges',
                '"multiplicity_note"', 'f"{len(metrics)} metrics', '"several intervals', 'res = {"experiment"', '"exclusions": {"primary"', '"events_total"', 'row = {"analysis": PRIMARY', 'lo, hi = block_bootstrap', 'row.update({m:',
                'print(f"sensitivity', 'res["primary"] =', "OUT.mkdir", "e001_discovery.json", "e001_discovery_cells.csv", "e001_discovery_per_session.csv", "e001_discovery_sensitivity.csv", "return res"]
E001_ADDED = ["S, Session, session_events", "E1.summarize", 'e, sp = cfg["e001"]', 'sym = cfg["dataset"]["symbol"]', "sessions = {}", "for d in days:", 'hook("E001", d)', "sessions[d] = Session(sym, d)",
              'res = {"experiment"', '"exclusions": {"primary"', '"events_total"', 'row = {"analysis": PRIMARY', "row.update({m:", 'res["primary"] =', 'return {"res": res', 'split_of({"splits": sp}, d)']


def test_e001_marked_block_differs_from_frozen_only_as_listed():
    frozen = clean(body_of_run("e001.py", 'e, sp = cfg["e001"], cfg["splits"]', 'pl.DataFrame(sens_rows).write_csv'))
    copy = clean(func_src(ROOT / "lpx/research/closeout.py", "frozen_copy_e001"))
    new, gone = ordered_new_and_deleted(frozen, copy)
    assert [x for x in new if not any(k in x for k in E001_ADDED)] == []
    assert [x for x in gone if not any(k in x for k in E001_REMOVED)] == []


# the frozen file writes, in order and with indentation: (copy line, the frozen line it equals except for close-out names and the directory,
# or None for a line the protocol lists as added)
TABLE_BLOCKS = {
    "frozen_copy_e001_tables": ("e001.py", [('    (out / "e001_closeout.json").write_text(json.dumps(r["res"], indent=1))', '    (OUT / "e001_discovery.json").write_text(json.dumps(res, indent=1))'),
                                            ('    pl.DataFrame(r["cells"]).write_csv(out / "e001_cells.csv")', '    pl.DataFrame(pooled).write_csv(OUT / "e001_discovery_cells.csv")'),
                                            ('    pl.DataFrame(r["per_session"]).write_csv(out / "e001_per_session.csv")', '    pl.DataFrame(per_session).write_csv(OUT / "e001_discovery_per_session.csv")'),
                                            ('    pl.DataFrame(r["sensitivity"]).write_csv(out / "e001_sensitivity.csv")', '    pl.DataFrame(sens_rows).write_csv(OUT / "e001_discovery_sensitivity.csv")')]),
    "frozen_copy_e002_tables": ("e002.py", [('    gross.write_csv(out / "e002_gross_by_session.csv")', '    gross.write_csv(OUT / "e002_gross_by_session.csv")'),
                                            ('    net.write_csv(out / "e002_net_by_session.csv")', '    net.write_csv(OUT / "e002_net_by_session.csv")')]),
    "frozen_copy_e003_tables": ("e003.py", [("    g = pl.DataFrame(gross, infer_schema_length=None)", "    g = pl.DataFrame(gross, infer_schema_length=None)"),
                                            ('    tables = {"e003_gross_by_session.csv": g, "e003_net_by_session.csv": E3.fee_overlay(g, cfg["fees"]),', '    tables = {"e003_gross_by_session.csv": g, "e003_net_by_session.csv": fee_overlay(g, cfg["fees"]),'),
                                            ('              "e003_forecast_by_session.csv": pl.DataFrame(frows), "e003_calibration.csv": pl.DataFrame(cal)}', '              "e003_forecast_by_session.csv": pl.DataFrame(frows), "e003_calibration.csv": pl.DataFrame(cal)}'),
                                            ("    for name, t in tables.items():", "    for name, t in tables.items():"), ("        t.write_csv(out / name)", "        t.write_csv(OUT / name)"),
                                            ('    (out / "e003_models.json").write_text(json.dumps(models_out, indent=1))', '    (OUT / "e003_models.json").write_text(json.dumps(models_out, indent=1))'),
                                            ('    (out / "e003_trades_without_receipt_time.json").write_text(json.dumps(unrec, indent=1))', None)]),
    "frozen_copy_e004_write": ("e004.py", [('    for name, t in r["tables"].items():', None), ("        t.write_csv(out / name)", "        t.write_csv(OUT / name)"),
                                           ('    (out / "e004_invariants.json").write_text(json.dumps(r["invariants"]))', None)]),
}


@pytest.mark.parametrize("name", list(TABLE_BLOCKS))
def test_table_blocks_equal_the_frozen_writes_in_order_with_indentation(name):
    file, pairs = TABLE_BLOCKS[name]
    body = clean(func_src(ROOT / "lpx/research/closeout.py", name))
    assert body == [c for c, _ in pairs]
    frozen = frozen_source(file)
    pos = [next((i for i, x in enumerate(frozen) if x.strip() == f.strip()), None) for _, f in pairs if f is not None]
    assert None not in pos and pos == sorted(pos)
    indent = lambda x: len(x) - len(x.lstrip())
    mapped = [(c, f) for c, f in pairs if f is not None]
    assert [indent(f) - indent(mapped[0][1]) for _, f in mapped] == [indent(c) - indent(mapped[0][0]) for c, _ in mapped]


@pytest.mark.parametrize("name", ["run_e001", "run_e002", "run_e003", "run_e004"])
def test_runners_hold_no_table_code_of_their_own(name):
    src = "\n".join(func_src(ROOT / "lpx/research/closeout.py", name))
    for x in (".write_csv(", "pl.DataFrame(", "fee_overlay("):
        assert x not in src, x
    assert "json.dumps" not in src.replace('json.loads', '')


@pytest.mark.parametrize("exc,want", [(ValueError, "software"), (pl.exceptions.ComputeError, "software"), (OSError, "environment"), (MemoryError, "environment")])
def test_table_failures_classify_by_the_declared_rule(tmp_path, monkeypatch, exc, want):
    monkeypatch.setattr(pl.DataFrame, "write_csv", lambda self, p: (_ for _ in ()).throw(exc("x")))
    with pytest.raises(exc) as e:
        C.frozen_copy_e002_tables(pl.DataFrame({"a": [1]}), pl.DataFrame({"a": [1]}), tmp_path)
    assert C.classify(e.value) == want


# every frozen line a marked block rewrites, with the exact line that must replace it (a deletion of both forms must fail)
REPLACED = {
    "frozen_copy_e002": {'normalized_path("binance_vision"': 'tr = pl.read_parquet(E1.normalized_path("binance_vision", sym, "trades", d)).sort(["exch_us", "trade_id"])',
                         '"split": "train" if d in rc': 'rows.append({"day": d, "split": split_of(rc, d), **r})', "gross = pl.DataFrame(rows)": 'gross = pl.DataFrame(rows).drop("first_cap_bind_us")'},
    "frozen_copy_e003": {"gross, frows, cal, models_out = [], [], [], {}": "gross, frows, cal, models_out, unrec = [], [], [], {}, {}", "for i, d in enumerate(days):": "for d in days:",
                         "rv_gate = pc[": 'rv_gate = art["rv_gate"]', "st, tr, eps = load_session": "st, tr, eps = E3.load_session(cfg, d)", "ft = features": "ft = E3.features(cfg, st, tr, eps)",
                         "forecast_rows(d, ft": 'fr, cl = E3.forecast_rows(d, ft, models, fc["primary_horizon_s"])', "attach(states": 'E3.attach(states, ft, models[fc["primary_horizon_s"]], rv_gate)',
                         'split = "train"': "split = split_of(ctx.rc, d)", "for r in run_session(states": 'for r in E3.run_session(states, to_trades(tr, cfg["instrument"]["tick"]), eps, cfg):'},
    "frozen_copy_e001": {"row.update({m:": "row.update({m: float(np.nanmean(x)) if np.any(~np.isnan(x)) else None})",
                         'row = {"analysis": PRIMARY': 'row = {"analysis": PRIMARY, "day": d, "split": split_of({"splits": sp}, d), "events": f.height,',
                         'res["primary"] =': 'res["primary"] = strip_intervals([r for r in pooled if r["cell"] == "all"])'},
}


@pytest.mark.parametrize("name", list(REPLACED))
def test_every_rewritten_frozen_line_has_its_exact_replacement(name):
    file = {"frozen_copy_e002": "e002.py", "frozen_copy_e003": "e003.py", "frozen_copy_e001": "e001.py"}[name]
    frozen = "\n".join(frozen_source(file))
    copy = [x.strip() for x in func_src(ROOT / "lpx/research/closeout.py", name)]
    for old, new in REPLACED[name].items():
        assert old in frozen, old
        assert new in copy, new


def test_runners_refuse_fits_trained_on_other_sessions_before_reading_a_session(monkeypatch):
    rc = C.load_rc()
    d = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    read = []
    monkeypatch.setattr(C.E3, "load_session", lambda *a: read.append(a))
    ctx = C.Ctx("dryrun", Path("."), rc, {"E003": [d[5]], "E004": [d[5]]}, lambda x: ROOT / "results/closeout_fits/walkforward" / x, lambda x: ["wrong"], ROOT / "results/e003")
    import tomllib

    with pytest.raises(RuntimeError, match="trained on other sessions"):
        C.frozen_copy_e003(tomllib.loads(C.E3.CONFIG.read_text()), ctx, [d[5]])
    e4, sc = C.E4.load_cfg()
    with pytest.raises(RuntimeError, match="trained on other sessions"):
        C.frozen_copy_e004(e4, sc, ctx, [d[5]])
    assert read == []


def test_marked_blocks_keep_every_frozen_check():
    src = (ROOT / "lpx/research/closeout.py").read_text()
    for m in ("check_models(d, models, rv_med, rv_gate, frozen_models)", "check_ref_forecasts(d, ft, models, frozen_models, frozen_fc, frozen_cal)", "check_ref_policy(d, agg, frozen_gross)",
              "check_trained(ctx, d, art)", "check_trained(ctx, d, art3)", "check_trained(ctx, d, art4)", 'raise AssertionError("primary events with a missing primary metric")', 'raise AssertionError(f"{d}: invalid record inside an accepted window")',
              'raise AssertionError("D0: j(k) must equal k")', 'raise AssertionError("D0: NV must equal REF bitwise")',
              'D0 through the view path differs from REF', 'raise AssertionError("view states were mutated")',
              'raise AssertionError("the exchange-side states or trades were mutated")'):
        assert m in src, m


# ------------------------------------------------------------------------------------------------ analysis on synthetic tables
DAYS = [f"2026-0{i}-01" for i in range(6, 10)] + ["2026-10-01"]


def h4w_table(dw, orders=100, wd=0.03, ov=0.02, stall=None, base="P0"):
    n = len(DAYS)
    stall = dw if stall is None else stall
    return pl.DataFrame({"day": DAYS, "cell": ["D1_E"] * n, "base": [base] * n, "fill_model": ["intermediate"] * n, "latency": ["regional"] * n,
                         "D_W_bp": dw, "orders_U": orders if isinstance(orders, list) else [orders] * n, "orders_P": [100] * n, "withdrawn_share": [wd] * n,
                         "overlap_share_of_wp": [ov] * n, "D_W_stall_bp": stall, "orders_U_stall": [100] * n, "orders_P_stall": [100] * n,
                         "wu_time_share_nostall": [0.1] * n, "wu_fill_share_nostall": [0.1] * n, "wp_time_share_install": [0.05] * n, "wp_fill_share_install": [0.05] * n})


def e4cfg():
    import tomllib

    return tomllib.loads((ROOT / "configs/e004_v1.toml").read_text())


def test_h4w_confirmed_carries_the_required_wording_and_stays_one_sided():
    r = A.h4w_check(h4w_table([0.5, -0.5, 0.2, 0.9, -3.0]), "P0", DAYS, e4cfg())
    assert r["label"] == A.CONFIRMED and r["interpretation"] == "no material deterioration under the specified threshold"
    assert "not equivalence" in r["interpretation_note"] and "proof of no effect" in r["interpretation_note"]
    # large negative values still pass: the rule is one-sided, as frozen
    assert A.h4w_check(h4w_table([-5.0] * 5), "P0", DAYS, e4cfg())["label"] == A.CONFIRMED


def test_h4w_labels_on_failures_counts_and_gates():
    cfg = e4cfg()
    assert A.h4w_check(h4w_table([2.0, 2.0, 0.0, 0.0, 0.0]), "P0", DAYS, cfg)["label"] == A.NOT_CONFIRMED      # count 3 < 4
    assert A.h4w_check(h4w_table([-9.0, 2.0, -9.0, -9.0, -9.0]), "P0", DAYS, cfg)["label"] == A.CONFIRMED       # count 4, mean below δ
    assert A.h4w_check(h4w_table([3.0, 3.0, 3.0, 3.0, -9.0]), "P0", DAYS, cfg)["label"] == A.NOT_CONFIRMED      # count 1
    assert A.h4w_check(h4w_table([0.5] * 5, wd=0.004), "P0", DAYS, cfg)["label"] == A.NOT_CONFIRMABLE
    assert A.h4w_check(h4w_table([0.5] * 5, ov=0.2), "P0", DAYS, cfg)["label"] == A.NOT_CONFIRMABLE
    assert A.h4w_check(h4w_table([0.5] * 5, orders=[19, 19, 100, 100, 100]), "P0", DAYS, cfg)["label"] == A.NOT_CONFIRMABLE
    # 4 of 5 defined: an undefined (input) session is a failure in the count, and 4 still suffice only if all 4 pass
    assert A.h4w_check(h4w_table([0.5, 0.5, 0.5, 0.5, 0.5], orders=[19, 100, 100, 100, 100]), "P0", DAYS, cfg)["label"] == A.CONFIRMED
    assert A.h4w_check(h4w_table([3.0, 0.5, 0.5, 0.5, 0.5], orders=[100, 19, 100, 100, 100]), "P0", DAYS, cfg)["label"] == A.NOT_CONFIRMED


def test_h4w_stall_only_qualifier_never_changes_the_label():
    r = A.h4w_check(h4w_table([0.5] * 5, stall=[3.0] * 5), "P0", DAYS, e4cfg())
    assert r["label"] == A.CONFIRMED and r["stall_only_result"] == "rule fails" and r["sensitive_to_natural_staleness"]


def e1_tables(tmp: Path, vals: dict) -> None:
    pl.DataFrame({"day": DAYS, **vals}).write_csv(tmp / "e001_per_session.csv")


def test_e001_rule_sign_and_count_with_es_unweighted(tmp_path):
    good = {**{f"mo_{h}s": [1.0] * 5 for h in (1, 5, 30)}, **{f"rs_{h}s": [-1.0] * 5 for h in (1, 5, 30)}, "es": [1.0] * 5}
    e1_tables(tmp_path, good)
    b = A.e001_block(tmp_path, DAYS, {"status": "complete"})
    assert b["tally"] == "6 of 6 confirmed" and b["es"]["label"] == A.REPORTED and b["es"]["same_test_no_weight"] == "sign rule holds"
    good["mo_1s"] = [5.0, 5.0, 5.0, -1.0, -1.0]        # mean positive but only 3 of 5
    good["rs_1s"] = [-1.0, -1.0, -1.0, -1.0, None]     # 4 of 5 defined and correct
    good["rs_5s"] = [-1.0, -1.0, -1.0, None, None]     # 3 defined
    e1_tables(tmp_path, good)
    b = A.e001_block(tmp_path, DAYS, {"status": "complete"})
    lab = {c["id"]: c["label"] for c in b["checks"]}
    assert lab["E001 mo_1s"] == A.NOT_CONFIRMED and lab["E001 rs_1s"] == A.CONFIRMED and lab["E001 rs_5s"] == A.NOT_CONFIRMABLE


def test_software_state_labels_every_check_not_confirmable_and_reported_not_run(tmp_path):
    st = {"status": "not_confirmable_software", "exception": "AssertionError"}
    for fn, n in ((A.e001_block, 6), (A.e003_block, 3), (A.e004_block, 2)):
        b = fn(tmp_path, DAYS, st)
        assert len(b["checks"]) == n and all(c["label"] == A.NOT_CONFIRMABLE and "software" in c["reason"] for c in b["checks"])
        assert "not run (software" in b["reported_only"]["all"]
    assert "not run (software" in A.e002_block(tmp_path, DAYS, st)["reported_only"]["all"]


def test_allow_list_drops_intervals_labels_and_multiplicity_keys():
    full = {"mean": 1.0, "defined": 5, "positive": 3, "ci95": [0, 1], "ci98.33": [0, 1], "eligible": True, "label": "supported",
            "robust_to_multiplicity": True, "nested": [{"mean": 2.0, "ci95_lo": 0.1, "eligible": False, "policy": "P0"}], "t_interval_95": [0, 1]}
    k = A.keep(full)
    assert k == {"mean": 1.0, "defined": 5, "positive": 3, "nested": [{"mean": 2.0, "policy": "P0"}]}
    A.assert_allowed(k)
    with pytest.raises(AssertionError, match="outside the allow-list"):
        A.assert_allowed({"mean": 1.0, "ci95": [0, 1]})


def test_fallback_report_lists_everything_and_no_seven_policy_rule():
    txt = A.fallback_report([{"event": "failed", "n": 3, "exception": "OSError"}])
    assert "not confirmable (run failure)" in txt and "not run (run failure)" in txt
    src = (ROOT / "lpx/research/closeout_analysis.py").read_text()
    assert "A3.participation(" not in src and "A4.h4w(" not in src and "A4.h4f(" not in src and "A4.h40(" not in src


def test_exploratory_tables_are_not_run_on_test():
    src = (ROOT / "lpx/research/closeout.py").read_text()
    assert "e001_exploratory" not in src and "e002_addendum" not in src


# ------------------------------------------------------------------------------------------------ E003 labels on synthetic tables
def e3_tables(tmp: Path, r2=None, d=None, activity=0.5, es=-1.0, dd=-1.0, nph=1.0, days=DAYS):
    """Minimal net and forecast tables with the frozen schema's columns used by the analysis."""
    n = len(days)
    r2 = [3.0] * n if r2 is None else r2
    d = [-0.2] * n if d is None else d
    fc = [{"day": x, "model": m, "horizon_s": 5, "r2_os": v, "ic": 0.1, "hit_rate": 0.6, "mean_abs_forecast": 0.5,
           "share_abs_forecast_ge_half_tick": 0.1, "share_abs_forecast_ge_half_spread": 0.1, "rows": 10} for x, v in zip(days, r2) for m in ("M1", "M2")]
    pl.DataFrame(fc).write_csv(tmp / "e003_forecast_by_session.csv")
    rows = []
    base = dict(valid_hours=10.0, filled_notional=1000.0, fills=10, maker_fees=1.0, taker_fees=0.1, turnover_per_hour=100.0, gross_per_hour=-1.0, net_per_hour=-2.0,
                gross_bp_per_notional=-1.0, gate_active_share=activity, inc_es=5.0, max_drawdown=9.0, es_per_k_turnover=1.0, inventory_per_k_turnover=1.0)
    for i, x in enumerate(days):
        for fee in ("vip0", "vip9", "lp_tier4"):
            for p in ("P0", "P1", "P3_M1", "P3_M2", "P3_negM2", "P3F", "P4"):
                r = dict(base, day=x, policy=p, fill_model="intermediate", latency="regional", fee_schedule=fee)
                if p == "P3_negM2":
                    r["gross_bp_per_notional"] = -1.0 - (d[i] if d[i] is not None else float("nan"))
                if p == "P4" and fee == "lp_tier4":
                    r.update(inc_es=5.0 + es, max_drawdown=9.0 + dd, net_per_hour=-2.0 + nph)
                rows.append(r)
            rows.append(dict(base, day=x, policy="NT", fill_model="none", latency="none", fee_schedule=fee, net_per_hour=0.0, filled_notional=0.0, fills=0))
    pl.DataFrame(rows, infer_schema_length=None).write_csv(tmp / "e003_net_by_session.csv")


def e3_labels(tmp, **kw):
    e3_tables(tmp, **kw)
    b = A.e003_block(tmp, DAYS, {"status": "complete"})
    return {c["id"]: c for c in b["checks"]}, b


def test_h1f_h1t_h3_confirmed_and_policies_are_descriptive(tmp_path):
    c, b = e3_labels(tmp_path)
    assert {k: v["label"] for k, v in c.items()} == {"H1-F": A.CONFIRMED, "H1-T": A.CONFIRMED, "H3": A.CONFIRMED}
    assert c["H1-T"]["sign_same_as_discovery"] and c["H1-T"]["economically_immaterial_below_delta"]
    assert "hypothetical" in c["H3"]["status"] and b["tally"] == "3 of 3 confirmed"
    pol = b["policies_vip0_descriptive"]
    assert set(pol["policies"]) == {"P0", "P1", "P3_M1", "P3_M2", "P3_negM2", "P3F", "P4"} and "no label or rule" in pol["status"]
    assert pol["policies"]["P0"]["difference_from_no_trade"] == pytest.approx(-2.0)
    assert not any("label" in v for v in pol["policies"].values())


def test_h1t_literal_rule_sign_and_materiality_reported_separately(tmp_path):
    c, _ = e3_labels(tmp_path, d=[0.2] * 5)           # 0 <= D < delta: the sign differs, not material
    assert c["H1-T"]["label"] == A.NOT_CONFIRMED and not c["H1-T"]["sign_same_as_discovery"] and c["H1-T"]["economically_immaterial_below_delta"]
    c, _ = e3_labels(tmp_path, d=[0.9] * 5)
    assert c["H1-T"]["label"] == A.NOT_CONFIRMED and not c["H1-T"]["economically_immaterial_below_delta"]


def test_h1t_depends_on_h1f_and_the_activity_gate(tmp_path):
    c, _ = e3_labels(tmp_path, r2=[-1.0] * 5)
    assert c["H1-F"]["label"] == A.NOT_CONFIRMED and c["H1-T"]["label"] == A.NOT_CONFIRMABLE and "H1-F" in c["H1-T"]["reason"]
    c, _ = e3_labels(tmp_path, activity=0.01)
    assert c["H1-T"]["label"] == A.NOT_CONFIRMABLE and "activity" in c["H1-T"]["reason"]
    c, _ = e3_labels(tmp_path, activity=None)
    assert c["H1-T"]["label"] == A.NOT_CONFIRMABLE


def test_h1f_definedness(tmp_path):
    c, _ = e3_labels(tmp_path, r2=[1.0, 1.0, 1.0, None, None])
    assert c["H1-F"]["label"] == A.NOT_CONFIRMABLE and "4 sessions" in c["H1-F"]["reason"]
    c, _ = e3_labels(tmp_path, r2=[1.0, 1.0, 1.0, 1.0, None])
    assert c["H1-F"]["label"] == A.CONFIRMED and c["H1-F"]["label_basis"] == "point estimate, 4 of 5 defined"


@pytest.mark.parametrize("kw", [{"es": 1.0}, {"dd": 1.0}, {"nph": -0.5}, {"nph": -5.0}, {"es": 0.0}, {"nph": 0.0}])
def test_h3_needs_all_three_discovery_signs(tmp_path, kw):
    c, _ = e3_labels(tmp_path, **kw)
    assert c["H3"]["label"] == A.NOT_CONFIRMED


def test_h3_non_inferior_wording_when_only_the_sign_differs(tmp_path):
    c, _ = e3_labels(tmp_path, nph=-0.5)
    assert c["H3"]["non_inferior"] and c["H3"]["wording"] == "non-inferior, but the sign differs"
    assert c["H3"]["delta_h"] == pytest.approx(1.1754724725329382, abs=1e-12)


def test_session_absent_from_tables_stays_visible_and_counts(tmp_path):
    e3_tables(tmp_path, days=DAYS[:4])
    b = A.e003_block(tmp_path, DAYS, {"status": "complete"})
    c = b["checks"][0]["components"]["r2_os"]
    assert c["session_values"][DAYS[4]] is None and c["defined"] == 4 and b["checks"][0]["label"] == A.CONFIRMED


def test_duplicate_sessions_are_refused():
    with pytest.raises(ValueError, match="duplicate"):
        A.by_day(pl.DataFrame({"day": ["a", "a"], "x": [1.0, 2.0]}), "x", ["a"])


# ------------------------------------------------------------------------------------------------ H4-F labels on synthetic tables
def h4f_fc(L, A_, B_=None, cell="D1_S", tgt="y_view"):
    B_ = A_ if B_ is None else B_
    rows = []
    for i, d in enumerate(DAYS):
        nv = 3.0
        ref = None if L[i] is None else nv + L[i]
        ua = None if A_[i] is None else nv + A_[i]
        pl_ = None if ua is None or B_[i] is None else ua - B_[i]
        rows += [{"day": d, "cell": cell, "target": tgt, "model": m, "r2_os_pp": v} for m, v in (("REF", ref), ("NV", nv), ("UA-lambda", ua), ("PL-lambda", pl_), ("RF-lambda", nv))]
    return pl.DataFrame(rows, schema_overrides={"r2_os_pp": pl.Float64})


def y_label(L, A_):
    return A.y_view_label(A.h4f_row(h4f_fc(L, A_), "D1_S", "y_view", DAYS, e4cfg()), 0.25)


def test_h4f_y_view_labels():
    assert y_label([0.8] * 5, [-0.01] * 5) == A.CONFIRMED
    assert y_label([0.8] * 5, [0.3] * 5) == A.NOT_CONFIRMED                     # rho_A 0.375
    assert y_label([0.1] * 5, [0.0] * 5) == A.NOT_CONFIRMABLE                   # mean L below 0.20
    assert y_label([0.9, 0.9, 0.9, -0.1, -0.1], [0.0] * 5) == A.NOT_CONFIRMABLE  # L > 0 in 3 of 5
    assert y_label([0.8] * 5, [0.0, 0.0, None, None, None]) == A.NOT_CONFIRMABLE  # A defined in 2 of 5
    assert y_label([0.8] * 5, [0.0, 0.0, 0.0, 0.0, None]) == A.CONFIRMED         # A defined in 4 of 5


def test_h4f_row_tally_when_cells_disagree():
    assert A.y_view_row_label([A.CONFIRMED, A.CONFIRMED]) == A.CONFIRMED
    assert A.y_view_row_label([A.CONFIRMED, A.NOT_CONFIRMED]) == A.NOT_CONFIRMED
    assert A.y_view_row_label([A.CONFIRMED, A.NOT_CONFIRMABLE]) == A.NOT_CONFIRMABLE
    assert A.y_view_row_label([A.NOT_CONFIRMED, A.NOT_CONFIRMABLE]) == A.NOT_CONFIRMABLE


def test_h4f_projection_only_for_d1s_and_d3():
    assert "projection" in A.h4f_row(h4f_fc([0.8] * 5, [0.0] * 5), "D1_S", "y_view", DAYS, e4cfg())
    assert "projection" not in A.h4f_row(h4f_fc([0.8] * 5, [0.0] * 5, cell="D4"), "D4", "y_view", DAYS, e4cfg())


def h4f_cells(tmp, A_):
    """A complete E004 fixture is built from frozen functions' inputs; only the y_view logic is exercised through e004_block's helpers."""
    r = A.h4f_row(h4f_fc([0.8] * 5, A_), "D1_S", "y_view", DAYS, e4cfg())
    return r


def test_mean_a_row_and_sentence_branches():
    r = h4f_cells(None, [-0.001] * 5)
    assert r["A"]["mean"] < 0 and abs(r["rho_A"]) < 0.01
    r2 = h4f_cells(None, [-0.1] * 5)
    assert abs(r2["rho_A"]) >= 0.01
    src = (ROOT / "lpx/research/closeout_analysis.py").read_text()
    assert 'MEAN_A_SENTENCE if abs(r["rho_A"]) < 0.01 else None' in src and "ma < 0" in src and "UA harmful" not in src


# ------------------------------------------------------------------------------------------------ report
def full_result(tmp) -> dict:
    e3_tables(tmp)
    e1_tables(tmp, {**{f"mo_{h}s": [1.0] * 5 for h in (1, 5, 30)}, **{f"rs_{h}s": [-1.0] * 5 for h in (1, 5, 30)}, "es": [1.0] * 5})
    return A.jsonable({"mode": "rehearsal", "undefined_sessions": {DAYS[0]: "undefined (input)"}, "relative_tick_bp": {DAYS[1]: 1.1}, "not_refutation": A.NOT_REFUTATION,
                       "fee_attainability": "x", "experiments": {"E001": A.e001_block(tmp, DAYS, {"status": "complete"}), "E002": A.e002_block(tmp, DAYS, {"status": "not_confirmable_software", "exception": "AssertionError"}),
                                                                 "E003": A.e003_block(tmp, DAYS, {"status": "complete"}), "E004": A.e004_block(tmp, DAYS, {"status": "not_confirmable_software", "reason": "depends on E003"})}})


def test_report_lists_labels_session_values_and_required_wording(tmp_path):
    txt = A.render_report(full_result(tmp_path), [{"event": "started", "n": 1}])
    assert "not a refutation" in txt.lower() or "not a \nrefutation" in txt
    assert "point estimate, 5 of 5 defined" in txt and DAYS[0] in txt and "descriptive, not used" in txt
    assert "Seven policies and no-trade at VIP0 (descriptive; no label or rule)" in txt
    assert "Not computed on test: exploratory tables" in txt and "Not computed on test: cap-free addendum" in txt
    assert "not run (software" in txt and "| Item (reported only) | Discovery | Test |" in txt
    assert "H1_reported.D_net_per_hour.mean" in txt          # reported-only items are in the report itself


def test_report_renders_undefined_values_without_crashing():
    r = A.h4f_row(h4f_fc([None] * 5, [None] * 5), "D1_S", "y_view", DAYS, e4cfg())
    r = {**A.jsonable(r), "label": A.NOT_CONFIRMABLE}
    a = {"mode": "t", "not_refutation": "", "fee_attainability": "", "undefined_sessions": {}, "experiments": {
        "E004": {"state": {"status": "complete"}, "checks": [], "reported_only": {}, "h4f_y_view": {"row_label": A.NOT_CONFIRMABLE, "note": "", "pending_review_flag": False, "cells": {"D1_S": r}}},
        "E003": {"state": {"status": "complete"}, "checks": [], "reported_only": {}, "policies_vip0_descriptive": {"note": "", "policies": {"P0": {"mean_net_per_hour": None, "difference_from_no_trade": None, "gross_per_hour": None,
                 "maker_fees_per_hour_mechanical": None, "taker_fees_per_hour": None, "turnover_per_hour": None, "sessions_with_trades": 0}}}}}}
    txt = A.render_report(a, [])
    assert "undefined" in txt and "not confirmable" in txt


def test_compromised_flag_sits_on_top_and_shows_both_tallies(tmp_path):
    a = full_result(tmp_path)
    ev = [{"event": "compromised", "scope": ["E001 mo_1s"], "reason": "a table was viewed", "corrected": {"E001 mo_1s": "not confirmed"}}]
    txt = A.render_report(a, ev)
    assert "COMPROMISED: a table was viewed" in txt and "6 of 6 confirmed (original); 1 compromised; corrected: 5 of 6" in txt
    assert "| E001 mo_1s | **confirmed (point estimate, 5 of 5 defined)**" in txt


def test_flag_compromised_never_changes_the_primary_analysis(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws)
    before = C.sha256_file(ws.promoted / "closeout_analysis.json")
    C.flag_compromised(ws, "all", "out-of-ledger invocation")
    assert ws.events()[-1]["event"] == "compromised" and C.sha256_file(ws.promoted / "closeout_analysis.json") == before


def appendix_stub() -> dict:
    """A result holding exactly what Appendix A requires, built from the table itself (an independent list is checked separately)."""
    res = {"relative_tick_bp": {}, "undefined_sessions": {}, "no_valid_unit": {}, "experiments": {e: {"state": {"status": "complete"}, "reported_only": {}, "not_computed_on_test": {}} for e in C.EXPERIMENTS}}
    for row in A.APPENDIX_A:
        if row["exp"] == "All":
            continue
        for p in row.get("present", []) + row.get("paths", []):
            x = res["experiments"][row["exp"]]
            ks = A._segments(p)
            for k in ks[:-1]:
                if k.startswith("checks["):
                    rows = x.setdefault("checks", [])
                    if not isinstance(rows, list):
                        rows = x["checks"] = []
                    hit = [r for r in rows if r.get("id") == k[7:-1]]
                    x = hit[0] if hit else (rows.append({"id": k[7:-1]}) or rows[-1])
                else:
                    x = x.setdefault(k, {})
            if ks[-1] not in x:
                x[ks[-1]] = [] if ks[-1] == "checks" else "present"
    for row in A.APPENDIX_A:                       # lengths last, once every row has added its check rows and keys
        for p, n in row.get("count", {}).items():
            x = res["experiments"][row["exp"]]
            ks = A._segments(p)
            for k in ks[:-1]:
                x = x[k]
            v = x[ks[-1]]
            if isinstance(v, dict):
                v.update({f"pad{i}": {} for i in range(n - len(v))})
            elif ks[-1] == "checks":
                v += [{"id": f"pad{i}"} for i in range(n - len(v))]
            else:
                x[ks[-1]] = list(range(n))
    return res


ALL_APPENDIX_PATHS = [(r["exp"], p) for r in A.APPENDIX_A for p in r.get("paths", []) + r.get("present", [])]


def test_appendix_a_table_covers_every_protocol_row_and_nothing_else():
    text = (ROOT / C.PROTOCOL).read_text().split("## Appendix A")[1]
    rows = [x for x in text.splitlines() if x.startswith("| ") and not x.startswith("| Experiment")]
    assert len(rows) == len(A.APPENDIX_A)
    for x in rows:
        exp, out = [c.strip() for c in x.split("|")[1:3]]
        hit = [r for r in A.APPENDIX_A if r["exp"] == exp and (r["row"] in out or r["row"] in x)]
        assert len(hit) == 1, x


def test_appendix_a_stub_passes_and_each_item_is_required():
    A.assert_appendix_a(appendix_stub())


def test_appendix_a_holds_an_independent_list_of_protocol_items():
    """Written from the protocol text, not from APPENDIX_A, so dropping an item from the table fails here."""
    rows = {(r["exp"], r["row"]): r for r in A.APPENDIX_A}
    items = {p for r in A.APPENDIX_A for p in r.get("paths", []) + r.get("present", []) + r.get("tables", [])}
    for p in ("es", "reported_only/sensitivity_specs", "reported_only/proxy_validation_qty_ge_touch", "reported_only/exclusions", "reported_only/paired_table", "reported_only/model_pairs_table",
              "reported_only/paired_t_intervals_95_descriptive_not_used", "reported_only/model_pair_t_intervals_95_descriptive_not_used", "reported_only/scenario_t_intervals_95_descriptive_not_used",
              "reported_only/H1_reported/ranking_r2_M2_minus_M1", "reported_only/H3/other_schedules", "checks[H1-T]/gate_activity", "checks[H3]/notional_share_of_P3_M2_lp_tier4/P4",
              "checks[H3]/turnover_ratio_P4_over_P3F", "checks[H3]/partly_mechanical", "policies_vip0_descriptive/no_trade_net_per_hour", "reported_only/descriptive/forecasts", "reported_only/P0_versus_E002",
              "checks[H4-W[P0]]/gates", "checks[H4-W[P3_M2]]/stall_only_result", "h4f_y_view/cells/D3/projection", "reported_only/H4_0/pending_review_flag", "h4f_y_view/pending_review_flag",
              "reported_only/descriptive/window_quality", "e004_windows_by_session.csv", "e003_trades_without_receipt_time.json", "not_computed_on_test/cap-free addendum", "not_computed_on_test/exploratory tables"):
        assert p in items, p
    counts = {(r["exp"], p): n for r in A.APPENDIX_A for p, n in r.get("count", {}).items()}
    assert counts[("E001", "checks")] == 6 and counts[("E001", "reported_only/sensitivity_specs")] == 12 and counts[("E003", "checks")] == 3 and counts[("E004", "checks")] == 2
    assert counts[("E003", "policies_vip0_descriptive/policies")] == 7 and counts[("E004", "reported_only/h4f_other")] == 12
    assert {"relative_tick_bp", "undefined_sessions", "no_valid_unit"} <= set(rows[("All", "test relative tick per session")]["top"])


def test_fallback_report_names_every_appendix_a_item():
    txt = A.fallback_report([])
    for e, items in A.REPORTED_IDS.items():
        for i in items:
            assert f"| {e} | {i} | not run (run failure) |" in txt, i
    assert "primary metrics: es (reported only)" in txt
    # written from Appendix A, independently of REPORTED_IDS: E004's reported parts of its check rows, and the All row
    for item in ("checks[H4-W[P0]]/gates", "checks[H4-W[P3_M2]]/withdrawn_and_shares", "checks[H4-W[P0]]/stall_only_result", "checks[H4-W[P0]]/mean_D_W_sign", "checks[H4-W[P0]]/sessions_D_W_negative",
                 *[f"h4f_other/{c}:{t}/rho_A" for c in ("D1_E", "D2", "D4", "D1_S1", "D1_S3") for t in ("y_k", "y_view")], "h4f_other/D1_S:y_k/projection", "h4f_other/D3:y_k/per_session",
                 "relative_tick_bp", "undefined_sessions", "no_valid_unit"):
        assert item in txt, item


@pytest.mark.parametrize("exp,path", ALL_APPENDIX_PATHS)
def test_appendix_a_refuses_each_missing_item(exp, path):
    res = appendix_stub()
    x = res["experiments"][exp]
    ks = A._segments(path)
    for k in ks[:-1]:
        x = next(r for r in x["checks"] if r.get("id") == k[7:-1]) if k.startswith("checks[") else x[k]
    if isinstance(x, dict):
        del x[ks[-1]]
    else:
        pytest.skip("a list position")
    with pytest.raises(AssertionError, match="Appendix A"):
        A.assert_appendix_a(res)


def test_appendix_a_refuses_null_wrong_length_and_missing_tables_and_top_level(tmp_path):
    res = appendix_stub()
    res["experiments"]["E003"]["reported_only"]["H3"]["normalised"] = None
    with pytest.raises(AssertionError, match="normalised"):
        A.assert_appendix_a(res)
    res = appendix_stub()
    res["experiments"]["E001"]["reported_only"]["sensitivity_specs"] = [1]
    with pytest.raises(AssertionError, match="wrong length"):
        A.assert_appendix_a(res)
    with pytest.raises(AssertionError, match="e002_net_by_session.csv"):
        A.assert_appendix_a(appendix_stub(), tmp_path)
    res = appendix_stub()
    del res["relative_tick_bp"]
    with pytest.raises(AssertionError, match="relative_tick_bp"):
        A.assert_appendix_a(res)


def test_appendix_a_lost_or_empty_experiment_keeps_only_its_not_computed_markers():
    res = appendix_stub()
    res["experiments"]["E002"] = {"state": {"status": "not_confirmable_software"}, "checks": [], "reported_only": {"all": "not run"}, "not_computed_on_test": A.NOT_COMPUTED["E002"]}
    A.assert_appendix_a(res)
    res["experiments"]["E002"]["not_computed_on_test"] = {}
    with pytest.raises(AssertionError, match="cap-free"):
        A.assert_appendix_a(res)


def e002_net() -> pl.DataFrame:
    rng = np.random.default_rng(7)
    rows = [{"day": d, "policy": p, "fill_model": m, "latency": lat, "fee_schedule": "vip0", "net_bp_per_notional": float(rng.normal())}
            for d in DAYS for p in ("P0", "P1") for m in ("conservative", "intermediate", "optimistic") for lat in ("tokyo", "regional", "distant")]
    return pl.DataFrame(rows)


def test_e002_descriptive_t_intervals_cover_scenario_paired_and_fill_model_tables(tmp_path):
    e002_net().write_csv(tmp_path / "e002_net_by_session.csv")
    b = A.e002_block(tmp_path, DAYS, {"status": "complete"})
    rep = b["reported_only"]
    assert len(rep["paired_t_intervals_95_descriptive_not_used"]) == len(rep["paired_table"]) == 9
    assert len(rep["model_pair_t_intervals_95_descriptive_not_used"]) == len(rep["model_pairs_table"]) == 18
    net = pl.read_csv(tmp_path / "e002_net_by_session.csv").sort(["policy", "fill_model", "latency", "fee_schedule", "day"])
    models = ["conservative", "intermediate", "optimistic"]
    want = {(r["fill_model"], r["latency"]): r["mean_p1_minus_p0"] for r in rep["paired_table"]}
    for k, x in A.e002_paired(net, "vip0", models).items():
        assert float(x.mean()) == want[k]            # the same pairing as the frozen table
    want = {(r["policy"], r["latency"], r["pair"]): r["mean"] for r in rep["model_pairs_table"]}
    for k, x in A.e002_model_pairs(net, "vip0", models).items():
        assert float(x.mean()) == want[k]
    for block in ("paired", "model_pair"):
        for r in rep[f"{block}_t_intervals_95_descriptive_not_used"]:
            assert r["t_interval"][0] < r["t_interval"][1]
    assert "paired_t_intervals_95_descriptive_not_used" in "\n".join(A.side_by_side(rep, b.get("discovery_side")))


# ------------------------------------------------------------------------------------------------ protocol-conformance check
def test_run_history_names_ledger_commits_and_log_openings(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    with pytest.raises(C.Refused, match="stays sealed"):
        C.record_log_opening(ws, 1, "before any failure")
    attempt(ws, ("E001", None, "closeout"))
    C.record_log_opening(ws, 1, "diagnose the failure")
    assert events(ws)[-1] == ("log_opened", 1)
    authorise(ws, h, 2)
    attempt(ws)
    txt = A.history(C.events_with_commits(ws))
    commits = {e["ledger_commit"] for e in C.events_with_commits(ws)}
    assert len(commits) == len(ws.events()) and all(f"ledger_commit={c}" in "\n".join(txt) for c in commits)
    assert any("log_opened 1" in x and "diagnose the failure" in x for x in txt)


@pytest.mark.parametrize("line,why", [({"event": "failed", "n": 1}, "failed 1 has no started"), ({"event": "completed", "n": 1}, "completed 1 has no started"),
                                      ({"event": "closed"}, "closed precedes")])
def test_ledger_order_refuses_terminal_events_without_their_predecessors(tmp_path, line, why):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    ws.append(line)
    with pytest.raises(C.Refused, match=why):
        C.verify_ledger_history(ws)


def test_test_mode_requires_every_added_file_to_be_pinned():
    for x in C.ALLOWED_DIFF:
        assert x.split("\t", 1)[1] in C.TEST_MODE_PINS


def test_e001_with_no_valid_session_is_reported_not_a_failed_analysis(tmp_path):
    b = A.e001_block(tmp_path, DAYS, {"status": "complete"})
    assert b["reported_only"] == {"note": "no valid session"} and all(c["label"] == A.NOT_CONFIRMABLE for c in b["checks"])
    A.assert_appendix_a({"experiments": {"E001": b, **{e: {"state": {"status": "not_confirmable_software"}, "reported_only": {"all": "x"}, "not_computed_on_test": A.NOT_COMPUTED.get(e, {})} for e in ("E002", "E003", "E004")}}, "relative_tick_bp": {}, "undefined_sessions": {}, "no_valid_unit": {}})


def test_h4w_label_basis_counts_the_main_statistic_not_the_stall_qualifier():
    r = A.h4w_check(h4w_table([0.5] * 5, stall=[None, None, 3.0, 3.0, 3.0]), "P0", DAYS, e4cfg())
    assert r["label"] == A.CONFIRMED and r["label_basis"] == "point estimate, 5 of 5 defined"
    assert A.label_text(r) == "confirmed (point estimate, 5 of 5 defined)"


def test_report_rows_show_gates_counts_and_qualifiers(tmp_path):
    a = full_result(tmp_path)
    a["experiments"]["E004"]["checks"] = [A.jsonable(A.h4w_check(h4w_table([0.5] * 5), "P0", DAYS, e4cfg()))]
    txt = A.render_report(a, [])
    for k in ("sign_count_below_delta", "sessions_D_W_negative", "gates:", "gate_activity", "sign_count:", "turnover_ratio_P4_over_P3F", "notional_share_of_P3_M2_lp_tier4", "delta_h"):
        assert k in txt, k


def test_y_view_cells_show_session_values_basis_and_the_compromised_flag():
    r = A.h4f_row(h4f_fc([0.8] * 5, [0.0] * 5), "D1_S", "y_view", DAYS, e4cfg())
    cell = {**A.jsonable(r), "label": A.CONFIRMED, "id": "H4-F[D1_S,y_view]", "label_basis": "point estimate, 5 of 5 defined"}
    a = {"mode": "t", "not_refutation": "", "fee_attainability": "", "undefined_sessions": {}, "experiments": {
        "E004": {"state": {"status": "complete"}, "checks": [], "reported_only": {}, "h4f_y_view": {"row_label": A.CONFIRMED, "note": "", "pending_review_flag": False, "cells": {"D1_S": cell}}}}}
    txt = A.render_report(a, [{"event": "compromised", "scope": "all", "reason": "viewed early"}])
    assert "confirmed (point estimate, 5 of 5 defined)" in txt and "COMPROMISED: viewed early" in txt and f"{DAYS[0]}: A 0, L 0.8" in txt and "descriptive, not used" in txt


def test_test_mode_context_binds_test_days_all15_fits_and_staging_references(tmp_path, monkeypatch):
    """The wiring of test mode, without touching a test-day file: the two steps that read one are replaced; schedules are date-only."""
    rc = C.load_rc()
    days = rc["splits"]["test"]
    status = {d: {"undefined": False, "reason": None, "e001_valid": d != days[0], "episode_valid": True, "e001_reason": "no_accepted_joint_windows" if d == days[0] else None, "episode_reason": None} for d in days}
    p = tmp_path / "input_status.json"
    p.write_text(json.dumps({"provenance": {"mode": "test"}, "sessions": status}))
    monkeypatch.setattr(C, "INPUT_STATUS", str(p))
    checked = []
    monkeypatch.setattr(C, "verify_input_status_record", lambda ws, rec, ds: checked.append(ds))
    read = []
    monkeypatch.setattr(C, "verify_session_inputs", lambda rc_, d, s: (read.append(d), "undefined (input mismatch)" if d == days[1] else None)[1])
    monkeypatch.setattr(C, "verify_pins", lambda *a: None)          # these status records carry no pins
    monkeypatch.setattr(C, "relative_ticks", lambda rc_, ds: {d: 1.0 for d in ds})
    out = tmp_path / "staging"
    out.mkdir()
    make = C.test_context(ROOT)
    assert checked == [days] and make.mode == "test" and not hasattr(make, "preflight")
    monkeypatch.setattr(C.Workspace, "events", lambda self: [{"event": "started", "n": 1}])
    ctx = make(out, print)
    disc = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    assert ctx.mode == "test" and ctx.injection is None and ctx.e003_ref == out and ctx.all_days == days
    assert ctx.fit_dir(days[0]) == ROOT / "results/closeout_fits/all15" and ctx.expected_trained(days[0]) == disc
    assert ctx.sessions["E001"] == days[2:] and ctx.sessions["E004"] == [days[0], *days[2:]] and read == days
    written = json.loads((out / "closeout_input_status.json").read_text())
    assert written["undefined"][days[1]] == "undefined (input mismatch)" and written["no_valid_unit"][days[0]] == {"E001": "no_accepted_joint_windows"}
    assert days[1] not in json.loads((out / "closeout_relative_tick.json").read_text())
    with pytest.raises(C.Refused, match="injection is not available"):
        dataclass_ctx = C.Ctx("test", out, rc, {"E001": days}, None, None, out, print, ("E001", None, "closeout"))
        dataclass_ctx.hook("E001", days[0])
    with pytest.raises(C.Refused, match="accepts only"):
        C.Ctx("test", out, rc, {"E001": [disc[0]]}, None, None, out, print)


# ------------------------------------------------------------------------------------------------ review round 2: remaining branches
def shaped(monkeypatch, out: Path) -> C.Ctx:
    """The real runners with the frozen session work replaced by stubs, so their own writing code runs as on test."""
    df = pl.DataFrame({"day": ["d"], "fee_schedule": ["vip0"], "status": ["s"], "a": [1.0]})
    monkeypatch.setattr(C, "frozen_copy_e001", lambda *a: {"res": {"x": 1}, "cells": [{"metric": "m"}], "per_session": [{"day": "d"}], "sensitivity": [{"metric": "m"}]})
    monkeypatch.setattr(C, "frozen_copy_e002", lambda *a: (df, df))
    monkeypatch.setattr(C, "frozen_copy_e003", lambda *a: ([{"day": "d", "a": 1.0}], [{"day": "d"}], [{"day": "d"}], {"d": {}}, {"d": 0}))
    monkeypatch.setattr(C.E3, "fee_overlay", lambda g, fees: g)
    names = A.EXPERIMENT_TABLES["E004"][:-1]
    monkeypatch.setattr(C, "frozen_copy_e004", lambda *a: {"tables": {n: df for n in names}, "invariants": {"n": 1}})
    return C.Ctx("rehearsal", out, REAL_RC, {e: ["d"] for e in C.EXPERIMENTS}, None, None, out, lambda m: None)


def test_real_runners_write_exactly_the_expected_staged_set(tmp_path, monkeypatch):
    ctx = shaped(monkeypatch, tmp_path)
    statuses = C.run_experiments(ctx, C.RUNNERS, lambda m: None)
    for f in ("closeout_input_status.json", "closeout_relative_tick.json"):
        (tmp_path / f).write_text("{}")
    (tmp_path / "closeout.log").write_text("sealed")
    (tmp_path / ".DS_Store").write_text("finder")
    meta = {"statuses": statuses, "tables_sha256": {p.name: C.sha256_file(p) for p in tmp_path.iterdir() if p.name not in ("closeout.log", ".DS_Store")}}
    assert {p.name for p in tmp_path.iterdir()} - {"closeout.log", ".DS_Store"} == A.expected_staged(meta)
    A.verify_staged(tmp_path, meta)
    (tmp_path / "stray.csv").write_text("x")
    with pytest.raises(RuntimeError, match="unexpected"):
        A.verify_staged(tmp_path, meta)


def test_no_valid_session_expects_no_tables():
    meta = {"statuses": {e: {"status": "complete", "outputs": {}, "note": "no valid session"} for e in C.EXPERIMENTS}}
    assert A.expected_staged(meta) == set(A.INFRASTRUCTURE)


def test_analysis_checks_the_staged_set_before_reading_and_passes_tables_to_appendix_a(tmp_path, monkeypatch):
    lost = {e: {"status": "not_confirmable_software", "exception": "AssertionError"} for e in C.EXPERIMENTS}
    for f in A.INFRASTRUCTURE:
        (tmp_path / f).write_text("{}")
    (tmp_path / "closeout_input_status.json").write_text(json.dumps({"undefined": {}, "no_valid_unit": {}}))
    meta = {"statuses": lost, "tables_sha256": {p.name: C.sha256_file(p) for p in tmp_path.iterdir()}}
    (tmp_path / "closeout_meta.json").write_text(json.dumps(meta))
    order = []
    real_verify, real_read, real_assert = A.verify_staged, pl.read_csv, A.assert_appendix_a
    monkeypatch.setattr(A, "verify_staged", lambda t, m: (order.append("verify"), real_verify(t, m))[1])
    monkeypatch.setattr(A.pl, "read_csv", lambda *a, **k: (order.append("read"), real_read(*a, **k))[1])
    monkeypatch.setattr(A, "assert_appendix_a", lambda res, tables=None: (order.append(("appendix", tables)), real_assert(res, tables))[1])
    A.analyse(tmp_path, SimpleNamespace(mode="dryrun", sessions={e: [] for e in C.EXPERIMENTS}))
    assert order[0] == "verify" and ("appendix", tmp_path) in order


def test_e002_t_intervals_are_95_percent_vip0_only_and_exactly_the_scenario_rows(tmp_path):
    net = e002_net()
    other = net.with_columns(pl.lit("vip9").alias("fee_schedule"), (pl.col("net_bp_per_notional") * 100).alias("net_bp_per_notional"))
    nt = net.filter(pl.col("policy") == "P0").with_columns(pl.lit("NT").alias("policy"))
    pl.concat([net, other, nt]).write_csv(tmp_path / "e002_net_by_session.csv")
    rep = A.e002_block(tmp_path, DAYS, {"status": "complete"})["reported_only"]
    scen = rep["scenario_t_intervals_95_descriptive_not_used"]
    assert [(r["policy"], r["fill_model"], r["latency"]) for r in scen] == sorted((r["policy"], r["fill_model"], r["latency"]) for r in rep["scenario_table"])
    g = net.filter((pl.col("policy") == "P0") & (pl.col("fill_model") == "conservative") & (pl.col("latency") == "tokyo")).sort("day")["net_bp_per_notional"].to_numpy()
    assert next(r for r in scen if (r["policy"], r["fill_model"], r["latency"]) == ("P0", "conservative", "tokyo"))["t_interval"] == A4_t(g)
    x = A.e002_paired(pl.read_csv(tmp_path / "e002_net_by_session.csv").sort(["policy", "fill_model", "latency", "fee_schedule", "day"]), "vip0", ["conservative", "intermediate", "optimistic"])
    assert len(x) == 9 and all(np.abs(v).max() < 20 for v in x.values())        # the vip9 rows (x100) are not pooled in


def A4_t(x):
    from lpx.research import e004_analysis as A4

    return A4.t_interval(np.asarray(x, float), 95.0)


def test_status_is_written_before_cleanup_and_survives_a_cleanup_failure(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)

    def leaves_a_file(ctx):
        (ctx.out / "partial.csv").write_text("x")
        C.frozen_copy_injected_failure()
    rn = {**runners(), "E002": leaves_a_file}
    real = Path.unlink
    monkeypatch.setattr(Path, "unlink", lambda self, *a, **k: (_ for _ in ()).throw(OSError("busy")) if self.name == "partial.csv" else real(self, *a, **k))
    r = attempt(ws, rn=rn)
    assert r["outcome"] == "failed" and r["class"] == "environment"
    assert ws.events()[-1]["software_experiments"] == ["E002"]           # the no-retry record survived the cleanup failure


def test_software_statuses_propagates_read_errors(tmp_path):
    (tmp_path / "closeout_status_E001.json").mkdir()
    with pytest.raises(OSError):
        C.software_statuses(tmp_path)


def test_location_names_project_frames_not_the_virtual_environment():
    try:
        pl.read_csv("/nonexistent/x.csv")
    except Exception as e:      # noqa: BLE001
        loc = C.location(e)
    assert ".venv" not in loc and "test_closeout.py" in loc


def test_failure_handler_records_the_failure_even_when_the_log_cannot_be_written(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    monkeypatch.setattr(C.Streams, "progress", lambda self, m: (_ for _ in ()).throw(OSError("log disk full")))
    r = attempt(ws, ("E001", None, "closeout"))
    assert r["outcome"] == "failed" and ws.events()[-1]["event"] == "failed"


def test_session_in_progress_is_reset_for_each_experiment(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)

    def fails_before_any_session(ctx):
        C.frozen_copy_injected_failure()
    r = attempt(ws, rn={**runners(), "E004": fails_before_any_session})
    assert r["statuses"]["E004"]["last_session_started"] is None


def test_a_failure_after_the_analysis_file_is_complete_leaves_it_for_recovery(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    real = C.write_atomic

    def then_fail(path, obj):
        real(path, obj)
        if path.name == "closeout_analysis.json":
            raise OSError("directory fsync")
    monkeypatch.setattr(C, "write_atomic", then_fail)
    with pytest.raises(OSError):
        attempt(ws)
    assert ("failed", 1) not in events(ws) and ws.staging.exists()
    monkeypatch.setattr(C, "write_atomic", real)
    assert C.recover(ws) == "completed from the primary analysis"


# ------------------------------------------------------------------------------------------------ verification round: remaining findings and mutants
def test_a_real_denied_read_inside_lpx_code_is_environment(tmp_path):
    f = tmp_path / "locked.parquet"
    f.write_text("x")
    f.chmod(0o000)
    try:
        with pytest.raises(PermissionError) as e:
            C.sha256_file(f)                       # builtin open in closeout.py: errno set, innermost frame under lpx/
    finally:
        f.chmod(0o600)
    assert e.value.errno is not None and C.classify(e.value) == "environment"


def test_a_denied_read_inside_an_experiment_fails_the_attempt_not_the_experiment(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    f = tmp_path / "locked.parquet"
    f.write_text("x")
    f.chmod(0o000)

    def reads_a_locked_file(ctx):
        C.sha256_file(f)
    try:
        r = attempt(ws, rn={**runners(), "E002": reads_a_locked_file})
    finally:
        f.chmod(0o600)
    assert r["outcome"] == "failed" and r["class"] == "environment"


def test_test_mode_context_is_refused_away_from_the_project_repository_before_started(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    make = ctx_factory()
    make.mode = "test"
    with pytest.raises(C.Refused, match="only in the project repository"):
        C.run_attempt(ws, make, runners(), fake_analyse, required_pins=C.TEST_MODE_PINS, expected=(C.BASELINE, C.ALLOWED_DIFF), env_check=lambda: None)
    assert ("started", 1) not in events(ws)


def integrity_factory(finding="modified"):
    def make(out, progress):
        raise C.IntegrityFailure([C.integrity_finding("2026-synthetic", "trades", finding, None if finding == "missing" else "ab" * 32)])
    return make


def test_an_integrity_failure_is_a_recorded_failed_attempt_with_its_finding(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    r = C.run_attempt(ws, integrity_factory(), runners(), fake_analyse)
    e = ws.events()[-1]
    assert r == {"attempt": 1, "outcome": "failed", "class": "integrity"}
    assert e["event"] == "failed" and e["failure_class"] == "integrity" and e["exception"] == "IntegrityFailure"
    assert e["path"] == "results/closeout_attempt1" and ws.attempt_dir(1).exists() and not ws.staging.exists()      # the sealed rename
    assert e["integrity"] == {"findings": [{"session": "2026-synthetic", "input": "trades", "finding": "modified", "observed_sha256": "ab" * 32}]}
    assert "failure_class=integrity" in (h := "\n".join(A.history(C.events_with_commits(ws)))) and "'finding': 'modified'" in h and "'input': 'trades'" in h


def test_integrity_failures_take_no_new_freeze_record_and_fail_closed_on_the_third(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    C.run_attempt(ws, integrity_factory("missing"), runners(), fake_analyse)
    p = ws.root / C.FREEZE_RECORD
    first = p.read_bytes()
    rec = json.loads(first)
    rec["note"] = "a changed record"
    p.write_text(json.dumps(rec))
    h2 = C.sha256_file(p)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h2) + "\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "a new record after an integrity failure")
    authorise(ws, h2, 2)
    with pytest.raises(C.Refused, match="integrity failure takes no new freeze record"):
        C.check_guards(ws)
    p.write_bytes(first)                                             # the record of attempt 1 again
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "the first record restored")
    assert C.sha256_file(p) == h
    authorise(ws, h, 2)
    C.run_attempt(ws, integrity_factory(), runners(), fake_analyse)
    authorise(ws, h, 3)
    C.run_attempt(ws, integrity_factory(), runners(), fake_analyse)
    assert [e["event"] for e in ws.events()][-2:] == ["failed", "closed"] and (ws.promoted / "CLOSEOUT_report.md").exists()
    assert not (ws.promoted / "closeout_analysis.json").exists()
    rep = (ws.promoted / "CLOSEOUT_report.md").read_text()
    assert "FAILED CLOSED" in rep and rep.count("failure_class=integrity") == 3 and "'finding': 'missing'" in rep and "'finding': 'modified'" in rep


def real_context(inputs, tmp_path, monkeypatch):
    """The real session_context on two stand-in sessions whose four inputs are the synthetic files, with an authorised scratch ledger."""
    rc = REAL_RC
    d = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    for name in ("check_fit_manifest", "relative_ticks"):
        monkeypatch.setattr(C, name, lambda *a: {})
    monkeypatch.setattr(C.E4, "verify_schedules", lambda *a: 0)
    monkeypatch.setattr(C.E1, "verify_inputs", lambda *a: None)
    monkeypatch.setattr(C.E3, "verify_receipt_inputs", lambda *a: None)
    monkeypatch.setattr(C, "load_rc", lambda: rc)
    status = {x: {"undefined": False, "e001_valid": True, "episode_valid": True, "sha256": inputs.status["sha256"]} for x in d[10:12]}
    make = C.session_context(ROOT, "rehearsal", d[10:12], "rehearsal", d[:10], status)
    (tmp_path / "w").mkdir()
    ws, h = repo(tmp_path / "w")
    authorise(ws, h, 1)
    return make, ws, d


def test_an_input_modified_during_the_run_is_an_integrity_failure(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)

    def modifies_an_input(ctx):
        inputs.paths["receipts"].write_text("changed during the run")
        return []
    r = C.run_attempt(ws, make, {**runners(), "E002": modifies_an_input}, fake_analyse)
    e = ws.events()[-1]
    assert r["outcome"] == "failed" and r["class"] == "integrity"
    assert [(f["session"], f["input"], f["finding"]) for f in e["integrity"]["findings"]] == [(d[10], "receipts", "modified"), (d[11], "receipts", "modified")]


def test_the_volume_is_consulted_only_when_an_input_is_missing(inputs, tmp_path, monkeypatch):
    monkeypatch.setattr(C, "sentinel_inputs", lambda sym: [tmp_path / "gone.parquet"])
    assert C.input_mismatch("S", "d", inputs.record)[0] is None              # every input present: no dependence on the discovery volume


def test_a_missing_file_that_reappears_during_its_rechecks_is_not_missing(inputs, monkeypatch):
    content = inputs.paths["trades"].read_text()
    inputs.paths["trades"].unlink()
    monkeypatch.setattr(C.time, "sleep", lambda s: inputs.paths["trades"].write_text(content))
    assert C.input_mismatch("S", "d", inputs.record)[0] is None


def test_a_stray_authorisation_after_a_start_is_ignored_and_cannot_change_the_lineage(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "environment"))                       # an environment failure: the next attempt keeps the record
    p = ws.root / C.FREEZE_RECORD
    rec = json.loads(p.read_text())
    rec["note"] = "a changed record"
    p.write_text(json.dumps(rec))
    h2 = C.sha256_file(p)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h2) + "\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "new record")
    authorise(ws, h2, 1)                                             # stray: attempt 1 has started
    authorise(ws, h2, 2)
    C.verify_ledger_history(ws)                                      # not fatal
    assert C.authorisations(ws.events())[1]["freeze_record_sha256"] == h
    with pytest.raises(C.Refused, match="environment failure takes no new freeze record"):
        C.check_guards(ws)


def test_a_stray_authorisation_does_not_block_recovery(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    assert run_dying(ws, "after_analysis") == 137
    authorise(ws, h, 1)                                              # an operator's mistake after the start
    assert C.recover(ws) == "completed from the primary analysis"


def test_freeze_approval_must_be_the_exact_committed_line(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    text = (ws.root / "docs/DECISIONS.md").read_text().replace(C.FREEZE_APPROVAL.format(h=h), f"REJECTED, do not run: {h}")
    (ws.root / "docs/DECISIONS.md").write_text(text)
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "reject")
    with pytest.raises(C.Refused, match="no committed owner line"):
        C.check_guards(ws)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h) + "\n")              # right line, not committed
    assert not C.owner_line(ws, C.FREEZE_APPROVAL.format(h=h))


def test_unreadable_software_statuses_are_recorded_unknown_and_block_the_next_start(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    real = C.software_statuses
    monkeypatch.setattr(C, "software_statuses", lambda d: (_ for _ in ()).throw(OSError("EIO")))
    attempt(ws, ("E003", None, "closeout"), rn={**runners(), "E002": lambda ctx: C.frozen_copy_injected_failure()})
    assert ws.events()[-1]["event"] == "failed" and ws.events()[-1]["software_experiments"] is None
    authorise(ws, h, 2)
    with pytest.raises(C.Refused, match="still cannot be read"):
        C.check_guards(ws)
    monkeypatch.setattr(C, "software_statuses", real)                 # readable again: re-derived from the sealed, hash-checked directory
    C.check_guards(ws)
    r = attempt(ws)
    assert r["statuses"]["E002"]["status"] == "not_confirmable_software" and "no retry" in r["statuses"]["E002"]["reason"]


def test_streams_close_restores_descriptors_even_when_the_log_cannot_be_flushed(tmp_path):
    before = os.fstat(1).st_ino, sys.stdout
    st = C.Streams(tmp_path / "closeout.log")
    st.log.flush = lambda: (_ for _ in ()).throw(OSError("disk full"))
    with pytest.raises(OSError):
        st.close()
    assert (os.fstat(1).st_ino, sys.stdout) == before


def test_exclusive_write_leaves_no_temporary_file_when_the_write_fails(tmp_path, monkeypatch):
    monkeypatch.setattr(C.os, "fsync", lambda fd: (_ for _ in ()).throw(OSError("EIO")))
    with pytest.raises(OSError):
        C.write_exclusive(tmp_path / "rec.json", "x")
    assert list(tmp_path.iterdir()) == []


def test_an_ignored_file_in_scope_and_git_variables_are_refused_on_the_test_mode_path(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    (ws.root / ".git/info").mkdir(exist_ok=True)
    (ws.root / ".git/info/exclude").write_text("lpx/hidden.py\n")
    (ws.root / "lpx/hidden.py").write_text("x = 1\n")
    with pytest.raises(C.Refused, match="ignored file sits in the close-out's scope"):
        C.check_guards(ws)
    (ws.root / "lpx/hidden.py").unlink()
    (ws.root / "lpx/__pycache__").mkdir()
    (ws.root / "lpx/__pycache__/x.cpython-312.pyc").write_bytes(b"")          # bytecode is not a hidden change
    (ws.root / ".git/info/exclude").write_text("__pycache__/\n")
    C.refuse_untrustworthy_git(ws)
    monkeypatch.setenv("GIT_DIR", str(ws.root / ".git"))
    with pytest.raises(C.Refused, match="GIT_DIR"):
        C.check_guards(ws)
    monkeypatch.delenv("GIT_DIR")
    ws.git("update-index", "--skip-worktree", "configs/x.toml")
    with pytest.raises(C.Refused, match="index flags"):
        C.check_guards(ws)


def completed(tmp_path) -> C.Workspace:
    ws, h = repo(tmp_path)
    (ws.root / "lpx/closeout_added.py").write_text("y = 2\n")
    authorise(ws, h, 1)
    attempt(ws)
    return ws


def test_report_fix_refuses_uncommitted_code_no_change_and_changed_pins(tmp_path):
    ws = completed(tmp_path)
    with pytest.raises(C.Refused, match="no committed report-rendering change"):
        C.report_fix(ws)
    (ws.root / "lpx/x.py").write_text("x = 3\n")
    with pytest.raises(C.Refused, match="renders committed code only"):
        C.report_fix(ws)
    ws.git("checkout", "--", "lpx/x.py")
    (ws.root / "lpx/closeout_added.py").write_text("y = 3\n")
    (ws.root / C.PROTOCOL).write_text("# protocol (FROZEN), edited after the run\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "report fix and a protocol edit")
    with pytest.raises(C.Refused, match="pinned file differs"):
        C.report_fix(ws)


def h4f_full_fc(L=0.8, A=-0.001, D2L=0.0, cells=("D1_S", "D1_E", "D3", "D4", "D2", "D1_S1", "D1_S3")) -> pl.DataFrame:
    """A complete synthetic E004 forecast table: REF - NV = L, UA - NV = A, PL = RF = NV = 0, per session and cell; D0 rows for H4-0."""
    rows = []
    for d in DAYS:
        for c in cells:
            for t in ("y_k", "y_view"):
                l = D2L if c == "D2" else (L[DAYS.index(d)] if isinstance(L, list) else L)
                a = A[DAYS.index(d)] if isinstance(A, list) else A
                for m, v in (("REF", l), ("NV", 0.0), ("UA-lambda", a), ("PL-lambda", 0.0), ("RF-lambda", 0.0)):
                    rows.append({"day": d, "cell": c, "target": t, "model": m, "r2_os_pp": v})
        rows += [{"day": d, "cell": "D0", "target": "y_k", "model": m, "r2_os_pp": v} for m, v in (("REF", 0.5), ("UA-lambda[D1_S]", 0.5))]
    return pl.DataFrame(rows)


def e004_complete(tmp: Path, monkeypatch, **fc) -> dict:
    h4f_full_fc(**fc).write_csv(tmp / "e004_forecast_by_session.csv")
    pl.concat([h4w_table([0.5] * 5), h4w_table([0.5] * 5, base="P3_M2")]).write_csv(tmp / "e004_windows_by_session.csv")
    for f in ("e004_policy_gross_by_session.csv", "e004_policy_net_by_session.csv"):
        pl.DataFrame({"day": DAYS}).write_csv(tmp / f)
    for fn in ("descriptive_policy", "p3_forecast_variants", "window_descriptive"):
        monkeypatch.setattr(A.A4, fn, lambda *a, **k: {"stub": {"mean": 1.0}})
    return A.e004_block(tmp, DAYS, {"status": "complete"})


def test_e004_block_mean_a_row_sentence_and_its_gate(tmp_path, monkeypatch):
    b = e004_complete(tmp_path, monkeypatch, A=-0.001)
    c = b["h4f_y_view"]["cells"]["D1_S"]
    assert c["label"] == A.CONFIRMED and c["mean_A_below_0"]["sentence"] == A.MEAN_A_SENTENCE and c["mean_A_below_0"]["A_over_L"] == pytest.approx(-0.00125)
    c = e004_complete(tmp_path, monkeypatch, A=-0.1)["h4f_y_view"]["cells"]["D1_S"]
    assert c["mean_A_below_0"]["sentence"] is None
    assert "mean_A_below_0" not in e004_complete(tmp_path, monkeypatch, A=0.001)["h4f_y_view"]["cells"]["D1_S"]
    gate_fails = e004_complete(tmp_path, monkeypatch, L=0.1, A=-0.001)["h4f_y_view"]["cells"]["D1_S"]
    assert "mean_A_below_0" not in gate_fails and gate_fails["label"] == A.NOT_CONFIRMABLE and "gate failed" in gate_fails["reason"]


def test_e004_block_d2_flag_and_the_y_view_row(tmp_path, monkeypatch):
    b = e004_complete(tmp_path, monkeypatch, D2L=0.8)
    assert b["h4f_y_view"]["pending_review_flag"] and b["reported_only"]["H4_0"]["pending_review_flag"]
    b = e004_complete(tmp_path, monkeypatch, D2L=0.0)
    assert not b["h4f_y_view"]["pending_review_flag"] and b["h4f_y_view"]["row_label"] == A.CONFIRMED
    A.assert_appendix_a({"relative_tick_bp": {}, "undefined_sessions": {}, "no_valid_unit": {}, "experiments": {
        **{e: {"state": {"status": "not_confirmable_software"}, "reported_only": {"all": "x"}, "not_computed_on_test": A.NOT_COMPUTED.get(e, {})} for e in ("E001", "E002", "E003")}, "E004": b}})


def test_sum_l_safeguard_is_reachable_with_the_gate_passing_and_decides_the_label(tmp_path, monkeypatch):
    L, A_ = [10.0, 0.1, 0.1, 0.1, -5.0], [None, 0.0, 0.0, 0.0, 0.5]
    r = A.h4f_row(h4f_fc(L, A_), "D1_S", "y_view", DAYS, e4cfg())
    assert r["gate_passes"] and r["components_defined_ok"] and r["sum_L"] < 0
    assert A.y_view_label(r, 0.25) == A.NOT_CONFIRMABLE
    c = e004_complete(tmp_path, monkeypatch, L=L, A=A_)["h4f_y_view"]["cells"]["D1_S"]
    assert c["label"] == A.NOT_CONFIRMABLE and "ΣL ≤ 0" in c["reason"]


def test_y_view_cells_name_why_they_are_not_confirmable(tmp_path, monkeypatch):
    c = e004_complete(tmp_path, monkeypatch, A=[None, None, 0.0, 0.0, 0.0])["h4f_y_view"]["cells"]["D1_S"]
    assert c["label"] == A.NOT_CONFIRMABLE and "fewer than 4" in c["reason"]
    txt = A.render_report({"mode": "t", "not_refutation": "", "fee_attainability": "", "undefined_sessions": {}, "experiments": {"E004": {**A.jsonable(
        e004_complete(tmp_path, monkeypatch, A=[None, None, 0.0, 0.0, 0.0])), "state": {"status": "complete"}}}}, [])
    assert "Not confirmable because A or L is defined in fewer than 4 sessions" in txt and "(discovery" in txt and "not supported" in txt


def test_report_separates_undefined_sessions_from_sessions_with_no_valid_unit(tmp_path):
    a = full_result(tmp_path)
    a["no_valid_unit"] = {DAYS[2]: {"E002": "no_qualifying_episodes"}}
    txt = A.render_report(a, [])
    und = next(x for x in txt.splitlines() if x.startswith("Undefined sessions"))
    nou = next(x for x in txt.splitlines() if x.startswith("Sessions with no valid unit"))
    assert DAYS[0] in und and DAYS[2] not in und and DAYS[2] in nou and "not undefined" in nou


def test_fit_manifest_check_refuses_a_changed_or_extra_artifact(tmp_path):
    (tmp_path / "all15").mkdir()
    (tmp_path / "all15/e003_fit.json").write_text("{}")
    (tmp_path / "MANIFEST.json").write_text(json.dumps({"all15/e003_fit.json": C.sha256_file(tmp_path / "all15/e003_fit.json")}))
    C.check_fit_manifest(tmp_path)
    (tmp_path / "all15/extra.json").write_text("{}")
    with pytest.raises(C.IntegrityFailure) as e:
        C.check_fit_manifest(tmp_path)
    assert [(f["session"], f["input"], f["finding"]) for f in e.value.findings] == [(None, f"{tmp_path.name}/all15/extra.json", "not in the pinned manifest")]
    (tmp_path / "all15/extra.json").unlink()
    (tmp_path / "all15/e003_fit.json").write_text('{"changed": 1}')
    with pytest.raises(C.IntegrityFailure) as e:
        C.check_fit_manifest(tmp_path)
    assert [f["finding"] for f in e.value.findings] == ["modified"] and C.classify(e.value) == "integrity"
    (tmp_path / "all15/e003_fit.json").unlink()
    with pytest.raises(C.IntegrityFailure) as e:
        C.check_fit_manifest(tmp_path)
    assert [f["finding"] for f in e.value.findings] == ["missing"]


def test_schedule_verification_failure_stops_the_context(tmp_path, monkeypatch):
    rc = C.load_rc()
    d = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    monkeypatch.setattr(C.E4, "verify_schedules", lambda *a: (_ for _ in ()).throw(RuntimeError("schedule differs from the committed hash list")))
    monkeypatch.setattr(C, "verify_session_inputs", lambda *a: pytest.fail("an input was read before the schedules were verified"))
    with pytest.raises(RuntimeError, match="schedule differs"):
        C.session_context(ROOT, "rehearsal", d[10:12], "rehearsal", d[:10], {})(tmp_path, print)


def test_a_pinned_file_changed_during_the_run_fails_the_attempt(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)

    def edits_the_protocol(ctx):
        (ws.root / C.PROTOCOL).write_text("# protocol (FROZEN), edited mid-run\n")
        return []
    r = attempt(ws, rn={**runners(), "E004": edits_the_protocol})
    assert r["outcome"] == "failed" and r["class"] == "closeout"


def test_a_freeze_record_edit_between_metadata_and_analysis_fails_the_attempt(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)

    def edit_then_analyse(tables, ctx):
        (ws.root / C.FREEZE_RECORD).write_text((ws.root / C.FREEZE_RECORD).read_text() + " ")
        return A.analyse(tables, ctx)
    r = attempt(ws, analyse=edit_then_analyse)
    assert r["outcome"] == "failed"


@pytest.mark.parametrize("n", [2, 3])
def test_an_analysis_failure_on_a_later_attempt(tmp_path, n):
    ws, h = repo(tmp_path)
    for k in range(1, n + 1):
        authorise(ws, h, k)
        attempt(ws, ("analysis", None, "closeout"))
    assert ("failed", n) in events(ws)
    assert (("closed", None) in events(ws)) == (n == 3)


def test_staged_ledger_tail_and_the_neither_directory_branch_are_recovered(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    assert run_dying(ws, "E001") == 137
    with open(ws.ledger, "a") as f:
        f.write('{"event": "failed", "n": 1}\n')
    ws.git("add", C.LEDGER)                                      # staged, not committed
    import shutil

    shutil.rmtree(ws.staging)                                    # neither staging nor an attempt directory
    assert C.recover(ws) == "attempt 1 failed"
    e = ws.events()[-1]
    assert e["event"] == "failed" and e["path"] is None and e["exception"] == "process death"


def test_a_real_death_between_appending_and_committing_a_ledger_line(tmp_path):
    ws, h = repo(tmp_path)
    code = textwrap.dedent(f"""
        import os, sys
        from pathlib import Path
        sys.path.insert(0, {str(ROOT)!r})
        from lpx.research import closeout as C
        ws = C.Workspace(Path({str(ws.root)!r}))
        real = ws.git
        ws.git = lambda *a, **k: os._exit(137) if a and a[0] == "commit" else real(*a, **k)
        ws.append({{"event": "authorised", "n": 1, "freeze_record_sha256": {h!r}, "utc": "t"}})
    """)
    assert subprocess.run([sys.executable, "-c", code], env={**os.environ, "PYTHONPATH": str(ROOT)}).returncode == 137
    assert ws.events() == []                                     # the line is not in HEAD, so it does not count
    C.restore_ledger_tail(ws)
    assert ws.git("status", "--porcelain", "--", C.LEDGER).strip() == ""


def test_frozen_checks_are_live_statements_in_the_e004_blocks():
    import ast

    src = (ROOT / "lpx/research/closeout.py").read_text()
    tree = ast.parse(src)
    calls = {}
    for fn in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name in ("frozen_copy_e004_session", "frozen_copy_e004", "frozen_copy_e003")):
        def visit(node, guarded):
            for ch in ast.iter_child_nodes(node):
                g = guarded or isinstance(ch, (ast.If, ast.IfExp, ast.Try, ast.While))
                if isinstance(ch, ast.Call) and isinstance(ch.func, ast.Name):
                    calls.setdefault(ch.func.id, []).append(g)
                visit(ch, g)
        visit(fn, False)
    for name in ("check_models", "check_ref_forecasts", "check_ref_policy", "check_trained"):
        assert name in calls and not all(calls[name]), name           # called, and not only under a condition


def test_run_passes_the_frozen_episode_threshold_writes_once_and_refuses_before_reading(tmp_path, monkeypatch):
    P = precheck_tool()
    got, wrote = [], []
    monkeypatch.setattr(P, "build_status", lambda rc, days, ep: got.append(ep) or {})
    monkeypatch.setattr(P, "schedule_check", lambda days: 0)
    monkeypatch.setattr(P, "refuse_dirty_scope", lambda ws: None)
    monkeypatch.setattr(C, "write_exclusive", lambda o, t: wrote.append(o))
    P.run(tmp_path / "a.json", False, C.Workspace(ROOT))
    assert got == [600.0] and wrote == [tmp_path / "a.json"]
    (tmp_path / "b.json").write_text("x")
    got.clear()
    with pytest.raises(C.Refused, match="never overwritten"):
        P.run(tmp_path / "b.json", False, C.Workspace(ROOT))
    assert got == []                                              # refused before any input was read


def test_stand_ins_refuse_a_dirty_scope_and_the_official_path(tmp_path):
    P = precheck_tool()
    ws, _ = repo(tmp_path)
    (ws.root / "lpx/x.py").write_text("x = 9\n")
    with pytest.raises(C.Refused, match="uncommitted changes"):
        P.run(tmp_path / "o.json", False, ws)
    with pytest.raises(C.Refused, match="never write under results/closeout_freeze"):
        P.run(ws.root / "results/closeout_freeze/input_status.json", False, ws)


def test_step3_records_the_authorisation_hash_in_its_provenance(tmp_path, monkeypatch):
    P = precheck_tool()
    monkeypatch.setattr(P, "verify_authorisation", lambda ws, out: "h" * 64)
    monkeypatch.setattr(P, "build_status", lambda rc, days, ep: {d: {} for d in days})
    monkeypatch.setattr(P, "schedule_check", lambda days: 0)
    monkeypatch.setattr(C, "input_mismatch", lambda *a: pytest.fail("a test-day input was read"))
    res = P.run(tmp_path / "r.json", True, C.Workspace(ROOT))
    assert res["provenance"]["mode"] == "test" and res["provenance"]["authorisation_sha256"] == "h" * 64


def test_committed_refuses_a_working_copy_that_differs_from_head(tmp_path):
    P = precheck_tool()
    ws, _ = repo(tmp_path)
    assert P.committed(ws, "docs/DECISIONS.md")
    (ws.root / "docs/DECISIONS.md").write_text("edited\n")
    with pytest.raises(C.Refused, match="not committed as it stands"):
        P.committed(ws, "docs/DECISIONS.md")


@pytest.mark.parametrize("evidence", [{"precheck_faults.json": {"provenance": {}}}, {"fits_recomputation.json": {"provenance": None}}])
def test_step3_refuses_evidence_that_records_no_code(tmp_path, monkeypatch, evidence):
    P = precheck_tool()
    ws = precheck_repo(tmp_path, monkeypatch, evidence)
    authorisation(ws)
    with pytest.raises(C.Refused, match="records no code"):
        P.verify_authorisation(ws, ws.root / C.INPUT_STATUS)


def test_step3_owner_line_must_be_exact(tmp_path, monkeypatch):
    P = precheck_tool()
    ws = precheck_repo(tmp_path, monkeypatch)
    authorisation(ws, line="REJECTED closeout pre-check step 3: {h}")
    with pytest.raises(C.Refused, match="reads exactly"):
        P.verify_authorisation(ws, ws.root / C.INPUT_STATUS)


def test_real_input_paths_name_all_four_inputs():
    paths = C.input_paths("SOLUSDT", "2025-03-01")
    assert set(paths) == {"states", "book", "trades", "receipts"} and paths["book"].name == "book_2025-03-01.parquet" and "tardis" in str(paths["book"])
    assert set(C.ACCEPTANCE_AUDITED) == {"book", "trades", "receipts"}


def test_a_verifier_type_error_from_its_own_frame_is_not_an_input_result(monkeypatch):
    d = sorted(REAL_RC["splits"]["train"])[0]
    import pyarrow.parquet as pq

    monkeypatch.setattr(pq, "read_metadata", lambda p: SimpleNamespace(metadata=None))      # a footer with no key-value metadata
    with pytest.raises(TypeError) as e:
        C.E1.verify_inputs(REAL_RC, [d])
    assert C._frames(e.value)[-1] is C.E1.verify_inputs.__code__ and not C.frozen_verifier_result(e.value)


def test_the_receipt_verifiers_own_mismatch_is_an_input_result(tmp_path, monkeypatch):
    acc = tmp_path / "results/acceptance_001"
    acc.mkdir(parents=True)
    (acc / "summary.json").write_text(json.dumps({"tardis": []}))
    f = tmp_path / "trades.parquet"
    f.write_text("x")
    monkeypatch.setattr(C.E3, "ROOT", tmp_path)
    monkeypatch.setattr(C.E3, "normalized_path", lambda *a: f)
    with pytest.raises(KeyError) as e:
        C.E3.verify_receipt_inputs({"scope": {"symbol": "S"}}, ["d"])
    assert C.frozen_verifier_result(e.value)


def test_staged_check_runs_before_any_table_is_read(tmp_path, monkeypatch):
    statuses = {e: {"status": "not_confirmable_software", "exception": "AssertionError"} for e in C.EXPERIMENT_TABLES if e != "E001"} if hasattr(C, "EXPERIMENT_TABLES") else {}
    statuses = {e: {"status": "not_confirmable_software", "exception": "AssertionError"} for e in ("E002", "E003", "E004")}
    for t in A.EXPERIMENT_TABLES["E001"]:
        (tmp_path / t).write_text("x")
        (tmp_path / f"{t}.status.json").write_text("{}")
    statuses["E001"] = {"status": "complete", "outputs": {t: C.sha256_file(tmp_path / t) for t in A.EXPERIMENT_TABLES["E001"]}}
    for f in A.INFRASTRUCTURE:
        (tmp_path / f).write_text("{}")
    meta = {"statuses": statuses, "tables_sha256": {p.name: C.sha256_file(p) for p in tmp_path.iterdir()}}
    (tmp_path / "closeout_meta.json").write_text(json.dumps(meta))
    (tmp_path / "stray.csv").write_text("x")
    reads = []
    monkeypatch.setattr(A.pl, "read_csv", lambda *a, **k: reads.append(a) or pytest.fail("a table was read"))
    with pytest.raises(RuntimeError, match="unexpected"):
        A.analyse(tmp_path, SimpleNamespace(mode="dryrun", sessions={e: [] for e in C.EXPERIMENTS}))
    assert reads == []


def test_run_attempt_lists_exactly_the_staged_tables(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    seen = {}

    def make(out, progress):
        ctx = shaped(monkeypatch, out)
        ctx.progress = progress
        for f in ("closeout_input_status.json", "closeout_relative_tick.json"):
            (out / f).write_text("{}")
        (out / ".DS_Store").write_text("finder")
        return ctx

    def check(tables, ctx):
        meta = json.loads((tables / "closeout_meta.json").read_text())
        seen["listed"] = set(meta["tables_sha256"])
        A.verify_staged(tables, meta)
        return {"mode": ctx.mode, "not_refutation": "", "fee_attainability": "", "undefined_sessions": {}, "experiments": {}}
    r = C.run_attempt(ws, make, C.RUNNERS, check)
    assert r["outcome"] == "completed" and "closeout.log" not in seen["listed"] and ".DS_Store" not in seen["listed"]


def test_test_mode_context_reads_nothing_outside_a_started_attempt(tmp_path, monkeypatch):
    rc = C.load_rc()
    monkeypatch.setattr(C, "verify_session_inputs", lambda *a: pytest.fail("a test-day input was read"))
    make = C.session_context(ROOT, "test", rc["splits"]["test"], "all15", [], {})
    with pytest.raises(C.Refused, match="only inside a started attempt"):
        make(tmp_path, print)


def test_fill_model_pairs_do_not_pool_fee_schedules(tmp_path):
    net = e002_net()
    other = net.with_columns(pl.lit("vip9").alias("fee_schedule"), (pl.col("net_bp_per_notional") * 100).alias("net_bp_per_notional"))
    x = A.e002_model_pairs(pl.concat([net, other]).sort(["policy", "fill_model", "latency", "fee_schedule", "day"]), "vip0", ["conservative", "intermediate", "optimistic"])
    assert len(x) == 18 and all(np.abs(v).max() < 20 for v in x.values()) and all(len(v) == 5 for v in x.values())


def test_scenario_intervals_skip_the_reference_fill_model(tmp_path):
    net = e002_net()
    naive = net.filter(pl.col("fill_model") == "conservative").with_columns(pl.lit("naive").alias("fill_model"))
    pl.concat([net, naive]).write_csv(tmp_path / "e002_net_by_session.csv")
    rep = A.e002_block(tmp_path, DAYS, {"status": "complete"})["reported_only"]
    assert len(rep["scenario_t_intervals_95_descriptive_not_used"]) == len(rep["scenario_table"]) == 18
    assert all(r["fill_model"] != "naive" for r in rep["scenario_t_intervals_95_descriptive_not_used"])


def test_e001_tables_with_a_column_outside_the_allow_list_are_refused(tmp_path):
    e1_tables(tmp_path, {**{f"mo_{h}s": [1.0] * 5 for h in (1, 5, 30)}, **{f"rs_{h}s": [-1.0] * 5 for h in (1, 5, 30)}, "es": [1.0] * 5})
    pl.DataFrame({"analysis": ["a"], "metric": ["m"], "mean_of_session_means": [1.0], "ci95_lo": [0.0]}).write_csv(tmp_path / "e001_sensitivity.csv")
    with pytest.raises(AssertionError, match="outside the allow-list"):
        A.e001_block(tmp_path, DAYS, {"status": "complete"})


def test_appendix_a_present_items_include_an_independent_list_of_check_fields():
    present = {p for r in A.APPENDIX_A for p in r.get("present", [])}
    for p in ("es/same_test_no_weight", "checks[E001 rs_30s]/sign_count", "checks[H1-T]/note", "checks[H3]/delta_h", "checks[H3]/non_inferior", "checks[H3]/caveat",
              "checks[H4-W[P0]]/interpretation_note", "checks[H4-W[P3_M2]]/sensitive_to_natural_staleness", "h4f_y_view/cells/D1_S/leave_one_out_rho_A_range",
              "h4f_y_view/cells/D3/rho_A_minus_projection", "reported_only/H4_0/difference_pp", "policies_vip0_descriptive/policies/P4/taker_fees_per_hour"):
        assert p in present, p


def test_fits_tool_refuses_a_dirty_tree_and_records_provenance(monkeypatch):
    sys.path.insert(0, str(ROOT))
    import tools.closeout_fits as T

    monkeypatch.setenv("LPX_ALLOW_DIRTY", "1")
    with pytest.raises(SystemExit, match="LPX_ALLOW_DIRTY"):
        T.require_clean_tree()
    monkeypatch.delenv("LPX_ALLOW_DIRTY")
    prov = T.provenance_record()
    assert {"git_commit", "code_fingerprint", "uv_lock_sha256", "python_version", "packages", "status"} <= set(prov)


def test_fits_verify_flags_any_difference_and_records_its_checkout(tmp_path, monkeypatch):
    sys.path.insert(0, str(ROOT))
    import shutil
    import tools.closeout_fits as T

    monkeypatch.setattr(T, "main", lambda base: shutil.copytree(ROOT / "results/closeout_fits", base, dirs_exist_ok=True))
    res = T.verify(tmp_path / "same")
    assert res["byte_identical"] and res["provenance"]["trees"] and "fresh_clone" in res["provenance"]
    monkeypatch.setattr(T, "main", lambda base: (shutil.copytree(ROOT / "results/closeout_fits", base, dirs_exist_ok=True), (base / "all15/e003_fit.json").write_text("{}")))
    with pytest.raises(SystemExit, match="differs"):
        T.verify(tmp_path / "other")


# ------------------------------------------------------------------------------------------------ final check: survivors and round-4 changes
@pytest.mark.parametrize("drop", ["pins", "expected", "env_check", "frozen_text"])
def test_test_mode_run_needs_each_of_its_guards(tmp_path, drop):
    make = ctx_factory()
    make.mode = "test"
    kw = {"required_pins": C.TEST_MODE_PINS, "expected": (C.BASELINE, C.ALLOWED_DIFF), "env_check": lambda: None, "require_frozen_text": True}
    kw.update({"pins": {"required_pins": ()}, "expected": {"expected": None}, "env_check": {"env_check": None},
               "frozen_text": {"require_frozen_text": False}}[drop])
    ws = C.Workspace(ROOT)
    with pytest.raises(C.Refused, match="every test-mode guard"):
        C.run_attempt(ws, make, runners(), fake_analyse, **kw)


def test_test_mode_context_needs_the_project_repository_and_its_open_attempt(tmp_path, monkeypatch):
    rc = C.load_rc()
    with pytest.raises(C.Refused, match="only in the project repository"):
        C.session_context(tmp_path, "test", rc["splits"]["test"], "all15", [], {})
    monkeypatch.setattr(C, "verify_session_inputs", lambda *a: pytest.fail("a test-day input was read"))
    make = C.session_context(ROOT, "test", rc["splits"]["test"], "all15", [], {})
    for ev in ([{"event": "started", "n": 1}, {"event": "failed", "n": 1}], [{"event": "started", "n": 1}, {"event": "completed", "n": 1}]):
        monkeypatch.setattr(C.Workspace, "events", lambda self, ev=ev: ev)
        with pytest.raises(C.Refused, match="only inside a started attempt"):
            make(tmp_path, print)


def test_input_status_record_refuses_a_changed_summary(tmp_path):
    ws, rec = status_ws(tmp_path)
    (ws.root / "results/acceptance_001/summary.json").write_text('{"changed": true}')
    with pytest.raises(C.Refused, match="changed since"):
        C.verify_input_status_record(ws, rec, REAL_RC["splits"]["test"])


def test_software_statuses_are_read_again_once_before_recording_unknown(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    real, calls = C.software_statuses, []

    def flaky(d):
        calls.append(d)
        if len(calls) == 1:
            raise OSError("EIO")
        return real(d)
    monkeypatch.setattr(C, "software_statuses", flaky)
    attempt(ws, ("E003", None, "closeout"), rn={**runners(), "E002": lambda ctx: C.frozen_copy_injected_failure()})
    assert len(calls) == 2 and ws.events()[-1]["software_experiments"] == ["E002"]


@pytest.mark.parametrize("line", ["NOT APPROVED close-out freeze record: {h}", "APPROVED close-out freeze record: {h} (pending)", "  # APPROVED close-out freeze record: {h}"])
def test_owner_line_is_an_exact_line(tmp_path, line):
    ws, h = repo(tmp_path)
    text = (ws.root / "docs/DECISIONS.md").read_text().replace(C.FREEZE_APPROVAL.format(h=h), line.format(h=h))
    (ws.root / "docs/DECISIONS.md").write_text(text)
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "other wording")
    assert not C.owner_line(ws, C.FREEZE_APPROVAL.format(h=h))


def test_owner_line_requires_the_working_copy_to_equal_head(tmp_path):
    ws, h = repo(tmp_path)
    assert C.owner_line(ws, C.FREEZE_APPROVAL.format(h=h))
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write("an uncommitted note\n")
    assert not C.owner_line(ws, C.FREEZE_APPROVAL.format(h=h))


def test_failure_handler_survives_a_dead_log_and_a_failing_close(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    monkeypatch.setattr(C.traceback, "format_exc", lambda: (_ for _ in ()).throw(OSError("log disk full")))
    real_close = C.Streams.close

    def close_then_fail(self):
        real_close(self)
        raise OSError("close failed")
    monkeypatch.setattr(C.Streams, "close", close_then_fail)
    r = attempt(ws, ("E001", None, "closeout"))
    assert r["outcome"] == "failed" and ws.events()[-1]["event"] == "failed"


def test_a_software_failure_is_recorded_even_when_its_traceback_cannot_be_logged(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    monkeypatch.setattr(C.traceback, "format_exc", lambda: (_ for _ in ()).throw(OSError("log disk full")))
    r = attempt(ws, ("E002", None, "software"))
    assert r["outcome"] == "completed" and r["statuses"]["E002"]["status"] == "not_confirmable_software"


def test_report_fix_works_after_a_failed_attempt_and_keeps_its_guards(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    (ws.root / "lpx/closeout_added.py").write_text("y = 2\n")
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "closeout"))
    authorise(ws, h, 2)
    attempt(ws)
    (ws.root / "lpx/closeout_added.py").write_text("y = 3\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "report-rendering fix")
    monkeypatch.setenv("GIT_INDEX_FILE", str(tmp_path / "x"))
    with pytest.raises(C.Refused, match="GIT_INDEX_FILE"):
        C.report_fix(ws)
    monkeypatch.delenv("GIT_INDEX_FILE")
    import fcntl

    held = open(ws.root / ".git/closeout.lock", "w")
    fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
    with pytest.raises(C.Refused, match="another close-out process"):
        C.report_fix(ws)
    held.close()
    assert C.report_fix(ws) == "report re-rendered"


def test_report_fix_refuses_a_ledger_that_was_cut_back(tmp_path):
    ws = completed(tmp_path)
    ws.ledger.write_text(ws.ledger.read_text().splitlines()[0] + "\n")
    ws.git("add", C.LEDGER)
    ws.git("commit", "-q", "-m", "cut back")
    with pytest.raises(C.Refused, match="not append-only"):
        C.report_fix(ws)


def test_check_trained_guards_each_fit_artifact_in_its_own_block():
    import ast

    tree = ast.parse((ROOT / "lpx/research/closeout.py").read_text())
    fns = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    args = lambda fn: {ast.unparse(c.args[2]) for c in ast.walk(fns[fn]) if isinstance(c, ast.Call) and getattr(c.func, "id", None) == "check_trained"}
    assert args("frozen_copy_e004") == {"art3", "art4"} and args("frozen_copy_e003") == {"art"}


def test_d2_flag_needs_only_one_target_and_the_y_view_row_needs_both_cells(tmp_path, monkeypatch):
    fc = h4f_full_fc(D2L=0.8).with_columns(pl.when((pl.col("cell") == "D2") & (pl.col("target") == "y_view") & (pl.col("model") == "REF")).then(0.0).otherwise(pl.col("r2_os_pp")).alias("r2_os_pp"))
    fc.write_csv(tmp_path / "fc.csv")
    b = e004_complete(tmp_path, monkeypatch, D2L=0.8)
    fc.write_csv(tmp_path / "e004_forecast_by_session.csv")
    b = A.e004_block(tmp_path, DAYS, {"status": "complete"})
    assert b["h4f_y_view"]["pending_review_flag"]                     # D2 y_k passes, y_view does not: flagged
    fc2 = h4f_full_fc().with_columns(pl.when((pl.col("cell") == "D3") & (pl.col("model") == "REF")).then(0.01).otherwise(pl.col("r2_os_pp")).alias("r2_os_pp"))
    fc2.write_csv(tmp_path / "e004_forecast_by_session.csv")
    b = A.e004_block(tmp_path, DAYS, {"status": "complete"})
    cells = b["h4f_y_view"]["cells"]
    assert cells["D1_S"]["label"] == A.CONFIRMED and cells["D3"]["label"] == A.NOT_CONFIRMABLE and b["h4f_y_view"]["row_label"] == A.NOT_CONFIRMABLE


def test_h3_and_h1t_definedness_make_them_not_confirmable(tmp_path):
    c, _ = e3_labels(tmp_path, es=None) if False else (None, None)
    e3_tables(tmp_path)
    net = pl.read_csv(tmp_path / "e003_net_by_session.csv")
    net = net.with_columns(pl.when((pl.col("policy") == "P4") & (pl.col("fee_schedule") == "lp_tier4") & pl.col("day").is_in(DAYS[:2])).then(None).otherwise(pl.col("inc_es")).alias("inc_es"))
    net.write_csv(tmp_path / "e003_net_by_session.csv")
    b = A.e003_block(tmp_path, DAYS, {"status": "complete"})
    h3 = next(x for x in b["checks"] if x["id"] == "H3")
    assert h3["label"] == A.NOT_CONFIRMABLE and "fewer than 4" in h3["reason"]
    c, _ = e3_labels(tmp_path, d=[-0.2, -0.2, -0.2, None, None])
    assert c["H1-T"]["label"] == A.NOT_CONFIRMABLE and "fewer than 4" in c["H1-T"]["reason"]


def test_seven_policy_table_keeps_maker_and_taker_fees_apart_and_shows_discovery(tmp_path):
    _, b = e3_labels(tmp_path)
    p0 = b["policies_vip0_descriptive"]["policies"]["P0"]
    assert p0["maker_fees_per_hour_mechanical"] == pytest.approx(0.1) and p0["taker_fees_per_hour"] == pytest.approx(0.01)
    assert p0["discovery_mean_net_per_hour"] == json.loads((ROOT / "results/e003/e003_analysis.json").read_text())["participation"]["policies"]["P0"]["mean"]
    txt = A.render_report(A.jsonable({"mode": "t", "not_refutation": "", "fee_attainability": "", "undefined_sessions": {}, "experiments": {"E003": b}}), [])
    assert "| Policy | Net per hour | Discovery net per hour |" in txt and f"{p0['discovery_mean_net_per_hour']:.2f}" in txt


def test_mean_a_row_renders_a_over_l_and_the_discovery_values(tmp_path, monkeypatch):
    b = e004_complete(tmp_path, monkeypatch, A=-0.001)
    txt = A.render_report(A.jsonable({"mode": "t", "not_refutation": "", "fee_attainability": "", "undefined_sessions": {}, "experiments": {"E004": b}}), [])
    line = next(x for x in txt.splitlines() if "Mean A below 0" in x and "D1_S" not in x)
    assert "A/L -0.0013" in line and "discovery -0.0055 pp, 6 of 10 sessions" in line


def test_sealed_listings_ignore_a_finder_file(tmp_path):
    (tmp_path / "t.csv").write_text("x")
    before = C.tree_listing(tmp_path)
    (tmp_path / ".DS_Store").write_text("finder")
    assert C.tree_listing(tmp_path) == before


def test_the_end_of_run_recheck_rechecks_the_fit_manifest(tmp_path, monkeypatch):
    rc = C.load_rc()
    d = sorted(rc["splits"]["train"] + rc["splits"]["validation"])
    calls = []
    monkeypatch.setattr(C, "check_fit_manifest", lambda root: calls.append(root))
    monkeypatch.setattr(C, "verify_session_inputs", lambda *a: None)
    monkeypatch.setattr(C, "verify_pins", lambda *a: None)          # these status records carry no pins
    monkeypatch.setattr(C, "relative_ticks", lambda *a: {})
    monkeypatch.setattr(C.E4, "verify_schedules", lambda *a: 0)
    ctx = C.session_context(ROOT, "rehearsal", d[10:12], "rehearsal", d[:10], {x: {"e001_valid": True, "episode_valid": True} for x in d[10:12]})(tmp_path, print)
    n = len(calls)
    ctx.recheck()
    assert n == 1 and len(calls) == 2


def test_analysis_rechecks_pins_and_trained_on_sessions(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)

    def pin_edit_then_analyse(tables, ctx):
        (ws.root / "uv.lock").write_text("changed after the metadata\n")
        return A.analyse(tables, ctx)
    assert attempt(ws, analyse=pin_edit_then_analyse)["outcome"] == "failed"
    ws2, h2 = repo(tmp_path / "second") if (tmp_path / "second").mkdir() is None else (None, None)
    authorise(ws2, h2, 1)

    def wrong_trained(ctx):
        ctx.trained["d"] = ["some", "sessions"]
        ctx.expected_trained = lambda day: ["other", "sessions"]
        return []
    def verifying_analyse(tables, ctx):
        ctx.verify_for_analysis(json.loads((tables / "closeout_meta.json").read_text()))
        return fake_analyse(tables, ctx)
    assert attempt(ws2, rn={**runners(), "E003": wrong_trained}, analyse=verifying_analyse)["outcome"] == "failed"


# ------------------------------------------------------------------------------------------------ final mutation rerun: the remaining test gaps
def test_report_fix_accepts_an_untracked_sealed_attempt_directory(tmp_path):
    ws, h = repo(tmp_path)
    (ws.root / "lpx/closeout_added.py").write_text("y = 2\n")
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "closeout"))
    authorise(ws, h, 2)
    attempt(ws)
    (ws.root / "lpx/closeout_added.py").write_text("y = 3\n")
    ws.git("add", "lpx/closeout_added.py")
    ws.git("commit", "-q", "-m", "report-rendering fix only", "--", "lpx/closeout_added.py")
    assert "results/closeout_attempt1/" in ws.git("status", "--porcelain", "--untracked-files=all")      # sealed and untracked, as in the real run
    assert C.report_fix(ws) == "report re-rendered"


@pytest.mark.parametrize("exp,path", [("E003", "reported_only/H3/normalised"), ("E002", "reported_only/paired_table"), ("E004", "reported_only/descriptive/window_quality")])
def test_appendix_a_refuses_an_empty_required_item(exp, path):
    res = appendix_stub()
    x = res["experiments"][exp]
    ks = path.split("/")
    for k in ks[:-1]:
        x = x[k]
    x[ks[-1]] = [] if path.endswith("table") else {}
    with pytest.raises(AssertionError, match="null, empty or wrong length"):
        A.assert_appendix_a(res)


@pytest.mark.parametrize("cid,key", [("H3", "label_basis"), ("H1-T", "rule"), ("H4-W[P0]", "rule"), ("E001 mo_5s", "label_basis")])
def test_appendix_a_refuses_a_null_check_basis_or_rule(cid, key):
    res = appendix_stub()
    exp = {"H3": "E003", "H1-T": "E003", "H4-W[P0]": "E004", "E001 mo_5s": "E001"}[cid]
    row = next(r for r in res["experiments"][exp]["checks"] if r.get("id") == cid)
    row[key] = None
    with pytest.raises(AssertionError, match=r"\(null\)"):
        A.assert_appendix_a(res)


def test_appendix_a_refuses_a_null_y_view_label():
    res = appendix_stub()
    res["experiments"]["E004"]["h4f_y_view"]["cells"]["D3"]["label"] = None
    with pytest.raises(AssertionError, match=r"\(null\)"):
        A.assert_appendix_a(res)


def test_fallback_lists_the_y_view_cells_reported_parts_and_mean_a_rows():
    txt = A.fallback_report([])
    for c in ("D1_S", "D3"):
        for item in ("leave_one_out_rho_A_range", "projection", "rho_A_minus_projection", "per_session", "mean_A_below_0 (when attached)"):
            assert f"h4f_y_view/cells/{c}/{item}" in txt, (c, item)
        assert f"h4f_y_view/cells/{c}/label |" not in txt                 # the check itself is not a reported-only item


def test_appendix_a_requires_every_checks_rule():
    present = {p for r in A.APPENDIX_A for p in r.get("present", [])}
    for p in ("checks[H1-F]/rule", "checks[H1-T]/rule", "checks[H3]/rule", "checks[H4-W[P0]]/rule", "checks[H4-W[P3_M2]]/rule", "h4f_y_view/cells/D1_S/rule", "h4f_y_view/cells/D3/rule",
              *[f"checks[E001 {m}]/rule" for m in A.E001_METRICS]):
        assert p in present, p


def test_a_sealed_status_file_that_is_not_json_refuses_the_start_cleanly(tmp_path, monkeypatch):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    monkeypatch.setattr(C, "software_statuses", lambda d: (_ for _ in ()).throw(OSError("EIO")))
    attempt(ws, ("E003", None, "closeout"))
    monkeypatch.undo()
    monkeypatch.setattr(C, "software_statuses", lambda d: (_ for _ in ()).throw(ValueError("not JSON")))
    authorise(ws, h, 2)
    with pytest.raises(C.Refused, match="still cannot be read"):
        C.check_guards(ws)


# ------------------------------------------------------------------------------------------------ round 6: inputs that change under an experiment
def test_a_software_exception_on_changed_inputs_is_an_integrity_failure_with_no_software_record(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)

    def changes_an_input_then_frozen_code_raises(ctx):
        inputs.paths["trades"].write_text("changed under the experiment")
        C.frozen_copy_injected_failure()                 # a marked-block exception: software, if the pins still held
    r = C.run_attempt(ws, make, {**runners(), "E002": changes_an_input_then_frozen_code_raises}, fake_analyse)
    e = ws.events()[-1]
    assert r == {"attempt": 1, "outcome": "failed", "class": "integrity"}
    assert e["failure_class"] == "integrity" and e["software_experiments"] == [] and C.software_experiments_of(ws, e) == []
    assert {(f["input"], f["finding"]) for f in e["integrity"]["findings"]} == {("trades", "modified")}
    assert not (ws.attempt_dir(1) / "closeout_status_E002.json").exists()


def test_an_input_vanishing_under_an_experiment_is_an_integrity_failure_not_environment(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)

    def deletes_an_input_then_reads_it(ctx):
        inputs.paths["book"].unlink()
        inputs.paths["book"].read_bytes()                # FileNotFoundError: environment, if the pins still held
    r = C.run_attempt(ws, make, {**runners(), "E003": deletes_an_input_then_reads_it}, fake_analyse)
    e = ws.events()[-1]
    assert r["class"] == "integrity" and e["exception"] == "IntegrityFailure"
    assert [(f["session"], f["input"], f["finding"]) for f in e["integrity"]["findings"]] == [(d[10], "book", "missing"), (d[11], "book", "missing")]


def test_a_software_exception_on_intact_inputs_stays_software(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)
    r = C.run_attempt(ws, make, {**runners(), "E002": lambda ctx: C.frozen_copy_injected_failure()}, fake_analyse)
    assert r["outcome"] == "completed" and r["statuses"]["E002"]["status"] == "not_confirmable_software"


def test_a_fit_artifact_changed_during_the_run_is_an_integrity_failure(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)
    calls = []

    def manifest(root):
        calls.append(root)
        if len(calls) > 1:
            raise C.IntegrityFailure([C.integrity_finding(None, "closeout_fits/rehearsal/e003_fit.json", "modified", "cd" * 32)])
    monkeypatch.setattr(C, "check_fit_manifest", manifest)
    r = C.run_attempt(ws, make, {**runners(), "E001": lambda ctx: C.frozen_copy_injected_failure()}, fake_analyse)
    assert r["class"] == "integrity" and ws.events()[-1]["integrity"]["findings"][0]["input"] == "closeout_fits/rehearsal/e003_fit.json"
    assert ws.events()[-1]["software_experiments"] == []


def test_an_interrupt_is_not_attributed_to_the_inputs(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)

    def changes_then_interrupted(ctx):
        inputs.paths["trades"].write_text("changed")
        raise KeyboardInterrupt
    r = C.run_attempt(ws, make, {**runners(), "E001": changes_then_interrupted}, fake_analyse)
    assert r["class"] == "environment" and "integrity" not in ws.events()[-1]


def test_inputs_behind_reports_only_a_finding_and_never_masks_the_failure():
    found = C.IntegrityFailure([C.integrity_finding("d", "book", "missing")])

    def raises(x):
        def f():
            raise x
        return f
    ctx = SimpleNamespace(check_inputs=raises(found))
    assert C.inputs_behind(ctx, OSError("disk")) is found
    assert C.inputs_behind(ctx, ValueError("frozen")) is found
    other = C.IntegrityFailure([C.integrity_finding("e", "trades", "modified", "ab" * 32)])
    assert C.inputs_behind(ctx, other).findings == other.findings + found.findings          # an integrity failure's findings are completed
    assert C.inputs_behind(ctx, found).findings == found.findings                          # never duplicated
    assert C.inputs_behind(ctx, KeyboardInterrupt()) is None
    assert C.inputs_behind(None, OSError("x")) is None and C.inputs_behind(SimpleNamespace(check_inputs=None), OSError("x")) is None
    assert C.inputs_behind(SimpleNamespace(check_inputs=raises(OSError(5, "EIO"))), ValueError("x")) is None
    assert C.inputs_behind(SimpleNamespace(check_inputs=lambda: None), ValueError("x")) is None


def test_every_pin_finding_is_recorded_in_order(inputs):
    status = {"a": inputs.status, "b": inputs.status, "u": {"undefined": True, "reason": "hash_mismatch:book"}, "n": None}
    inputs.paths["book"].write_text("changed")
    inputs.paths["receipts"].unlink()
    with pytest.raises(C.IntegrityFailure) as e:
        C.verify_pins(REAL_RC, ["a", "b", "u", "n"], status)
    got = [(f["session"], f["input"], f["finding"]) for f in e.value.findings]
    assert got == [("a", "book", "modified"), ("a", "receipts", "missing"), ("b", "book", "modified"), ("b", "receipts", "missing")]
    assert str(e.value).startswith("a book: modified; a receipts: missing")



def test_a_pinned_input_changed_before_the_start_fails_before_any_experiment(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)
    inputs.paths["states"].write_text("changed after the freeze")
    ran = []
    r = C.run_attempt(ws, make, {e: (lambda ctx, e=e: ran.append(e) or []) for e in C.EXPERIMENTS}, fake_analyse)
    assert r["class"] == "integrity" and ran == [] and not (ws.attempt_dir(1) / "closeout_input_status.json").exists()
    assert {f["finding"] for f in ws.events()[-1]["integrity"]["findings"]} == {"modified"}


def test_a_directory_at_a_pinned_path_is_a_missing_input(inputs):
    inputs.paths["receipts"].unlink()
    inputs.paths["receipts"].mkdir()
    with pytest.raises(C.IntegrityFailure) as e:
        C.verify_session_inputs(REAL_RC, "d", inputs.status)
    assert [(f["input"], f["finding"]) for f in e.value.findings] == [("receipts", "missing")]


def test_an_integrity_failure_at_attempt_2_keeps_the_record_attempt_2_ran_under(tmp_path):
    ws, h = repo(tmp_path)
    authorise(ws, h, 1)
    attempt(ws, ("E001", None, "closeout"))
    h2 = new_record_after_fix(ws, "lpx/closeout_added.py", "y = 3\n")              # a close-out fix: a new record is allowed
    authorise(ws, h2, 2)
    C.run_attempt(ws, integrity_factory(), runners(), fake_analyse)
    h3 = new_record_after_fix(ws, "lpx/closeout_added.py", "y = 4\n")
    authorise(ws, h3, 3)
    with pytest.raises(C.Refused, match="integrity failure takes no new freeze record"):
        C.check_guards(ws)


# ------------------------------------------------------------------------------------------------ round 6: pinned data files after the freeze
DATA = "results/acceptance_001/windows.csv"


def repo_with_data_pin(tmp: Path) -> tuple[C.Workspace, str]:
    """The scratch repository with a pinned data file too, as test mode pins the acceptance files."""
    ws, _ = repo(tmp)
    (ws.root / DATA).parent.mkdir(parents=True)
    (ws.root / DATA).write_text("windows\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "data")
    p = ws.root / C.FREEZE_RECORD
    rec = json.loads(p.read_text())
    rec["pinned_sha256"][DATA] = C.sha256_file(ws.root / DATA)
    p.write_text(json.dumps(rec))
    h = C.sha256_file(p)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h) + "\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "freeze with a data pin")
    return ws, h


def never_read(out, progress):
    pytest.fail("the context was built: something was read")


@pytest.mark.parametrize("how", ["committed", "uncommitted", "deleted"])
def test_a_pinned_data_file_changed_after_the_freeze_is_an_integrity_failure_before_any_read(tmp_path, how):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    if how == "deleted":
        (ws.root / DATA).unlink()
    else:
        (ws.root / DATA).write_text("other windows\n")
    if how == "committed":
        ws.git("commit", "-q", "-am", "a changed data file")
    with pytest.raises(C.PinnedDataChanged):
        C.verify_freeze(ws, True)                                   # outside an attempt it refuses like a guard
    assert C.check_guards(ws)[0] == 1                               # every other guard passes: the attempt is recorded, not refused
    r = C.run_attempt(ws, never_read, runners(), fake_analyse)
    e = ws.events()[-1]
    assert r == {"attempt": 1, "outcome": "failed", "class": "integrity"} and events(ws)[-2:] == [("started", 1), ("failed", 1)]
    assert e["integrity"] == {"findings": [C.integrity_finding(None, DATA, "missing" if how == "deleted" else "modified", None if how == "deleted" else C.sha256_file(ws.root / DATA))]}
    assert e["path"] is None and not ws.staging.exists() and "failure_class=integrity" in "\n".join(A.history(C.events_with_commits(ws)))


def test_a_code_pin_change_still_refuses_even_with_a_data_change(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    (ws.root / DATA).write_text("other windows\n")
    (ws.root / "configs/x.toml").write_text("a = 2\n")
    ws.git("commit", "-q", "-am", "both")
    with pytest.raises(C.Refused, match="code differs from the baseline|pinned file differs from the freeze record: configs") as e:
        C.run_attempt(ws, never_read, runners(), fake_analyse)
    assert not isinstance(e.value, C.PinnedDataChanged) and ("started", 1) not in events(ws)


def test_three_data_pin_failures_close_the_evaluation(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    (ws.root / DATA).unlink()
    for n in (1, 2, 3):
        authorise(ws, h, n)
        assert C.run_attempt(ws, never_read, runners(), fake_analyse)["class"] == "integrity"
    assert [e["event"] for e in ws.events()][-2:] == ["failed", "closed"] and "FAILED CLOSED" in (ws.promoted / "CLOSEOUT_report.md").read_text()


def test_a_pinned_data_file_changed_during_the_run_is_an_integrity_failure(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)

    def changes_the_data(ctx):
        (ws.root / DATA).write_text("changed during the run\n")
        return []
    r = attempt(ws, rn={**runners(), "E002": changes_the_data})
    e = ws.events()[-1]
    assert r["class"] == "integrity" and e["exception"] == "PinnedDataChanged" and e["integrity"]["findings"][0]["input"] == DATA


def test_recovery_after_a_death_records_a_changed_data_pin_as_integrity(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    assert run_dying(ws, "E001") == 137
    (ws.root / DATA).write_text("changed\n")
    assert C.recover(ws) == "attempt 1 failed"
    e = ws.events()[-1]
    assert e["failure_class"] == "integrity" and e["integrity"]["findings"][0]["finding"] == "modified"


# ------------------------------------------------------------------------------------------------ round 6 corrections: the two failure-path defects
def broken_check(make, exc):
    def built(out, progress):
        ctx = make(out, progress)
        ctx.check_inputs = lambda: (_ for _ in ()).throw(exc)
        return ctx
    return built


def test_a_pins_check_that_cannot_run_keeps_the_software_status_and_its_no_retry_record(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)
    rn = {**runners(), "E002": lambda ctx: C.frozen_copy_injected_failure(), "E004": lambda ctx: (_ for _ in ()).throw(OSError("disk"))}
    r = C.run_attempt(ws, broken_check(make, OSError(5, "EIO")), rn, fake_analyse)
    e = ws.events()[-1]
    assert r["class"] == "environment" and e["software_experiments"] == ["E002"] and C.software_experiments_of(ws, e) == ["E002"]
    assert json.loads((ws.attempt_dir(1) / "closeout_status_E002.json").read_text())["status"] == "not_confirmable_software"


def test_a_software_exception_with_a_broken_pins_check_still_lets_the_attempt_complete(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)
    r = C.run_attempt(ws, broken_check(make, ValueError("cannot hash")), {**runners(), "E002": lambda ctx: C.frozen_copy_injected_failure()}, fake_analyse)
    assert r["outcome"] == "completed" and r["statuses"]["E002"]["status"] == "not_confirmable_software"


def test_an_interrupt_during_the_pins_check_writes_the_software_record_first(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)
    r = C.run_attempt(ws, broken_check(make, KeyboardInterrupt()), {**runners(), "E002": lambda ctx: C.frozen_copy_injected_failure()}, fake_analyse)
    e = ws.events()[-1]
    assert r["class"] == "environment" and e["software_experiments"] == ["E002"]


def test_recovery_promoting_a_complete_analysis_records_a_changed_data_pin(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    assert run_dying(ws, "after_analysis") == 137
    (ws.root / DATA).write_text("changed after the analysis\n")
    assert C.recover(ws) == "completed from the primary analysis"
    ev = ws.events()
    assert [e["event"] for e in ev][-2:] == ["integrity_noted", "completed"]
    assert ev[-2]["integrity"]["findings"] == [C.integrity_finding(None, DATA, "modified", C.sha256_file(ws.root / DATA))]
    assert "integrity_noted 1" in (ws.promoted / "CLOSEOUT_report.md").read_text()


def test_recovery_repeating_promotion_records_a_changed_data_pin(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    assert attempt(ws)["outcome"] == "completed"
    (ws.promoted / "CLOSEOUT_report.md").unlink()
    (ws.root / DATA).unlink()
    assert C.recover(ws) == "repeated promotion and report"
    assert ws.events()[-1]["event"] == "integrity_noted" and ws.events()[-1]["integrity"]["findings"][0]["finding"] == "missing"
    assert "integrity_noted 1" in (ws.promoted / "CLOSEOUT_report.md").read_text()


def test_recovery_closing_after_the_third_failure_records_a_changed_data_pin(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    for n in (1, 2):
        authorise(ws, h, n)
        attempt(ws, ("E001", None, "environment"))
    authorise(ws, h, 3)
    run_dying(ws, "E002")
    orig = C.close_terminal
    C.close_terminal = lambda w: (_ for _ in ()).throw(SystemExit(0))
    try:
        with pytest.raises(SystemExit):
            C.recover(ws)
    finally:
        C.close_terminal = orig
    (ws.root / DATA).write_text("changed before closing\n")
    assert C.recover(ws) == "closed"
    assert [e["event"] for e in ws.events()][-2:] == ["integrity_noted", "closed"]
    assert "integrity_noted 3" in (ws.promoted / "CLOSEOUT_report.md").read_text()


def test_recovery_with_intact_pins_records_nothing_extra(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    assert run_dying(ws, "after_analysis") == 137
    assert C.recover(ws) == "completed from the primary analysis"
    assert "integrity_noted" not in [e["event"] for e in ws.events()]


def test_without_a_record_a_genuine_input_problem_is_an_undefined_reason(inputs):
    inputs.paths["trades"].write_text("other than the acceptance run's")
    import unittest.mock as um
    with um.patch.object(C, "acceptance_record", lambda rc_, days: {"d": inputs.record}):
        assert C.verify_session_inputs(REAL_RC, "d", None) == "undefined (input mismatch: hash_mismatch:trades)"


def test_an_attempt_completes_with_intact_pinned_data_and_fit_manifest(tmp_path):
    ws, _ = repo_with_data_pin(tmp_path)
    fits = ws.root / "results/closeout_fits"
    (fits / "rehearsal").mkdir(parents=True)
    (fits / "rehearsal/e003_fit.json").write_text("{}")
    (fits / "MANIFEST.json").write_text(json.dumps({"rehearsal/e003_fit.json": C.sha256_file(fits / "rehearsal/e003_fit.json")}))
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "fits")
    p = ws.root / C.FREEZE_RECORD
    rec = json.loads(p.read_text())
    rec["pinned_sha256"][C.FIT_MANIFEST] = C.sha256_file(ws.root / C.FIT_MANIFEST)
    p.write_text(json.dumps(rec))
    h = C.sha256_file(p)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h) + "\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "record pins the fit manifest")
    authorise(ws, h, 1)
    assert set(C.data_scope(rec)) == {DATA, C.FIT_MANIFEST, "results/closeout_fits"}
    r = attempt(ws)
    assert r["outcome"] == "completed" and [e["event"] for e in ws.events()][-2:] == ["started", "completed"]
    assert all("integrity" not in e for e in ws.events())


def test_a_directory_in_place_of_a_fit_artifact_is_missing(tmp_path):
    (tmp_path / "all15").mkdir()
    (tmp_path / "MANIFEST.json").write_text(json.dumps({"all15/e003_fit.json": "ab" * 32}))
    (tmp_path / "all15/e003_fit.json").mkdir()
    with pytest.raises(C.IntegrityFailure) as e:
        C.check_fit_manifest(tmp_path)
    assert [f["finding"] for f in e.value.findings] == ["missing"]


# ------------------------------------------------------------------------------------------------ the scoped-validation review's corrections
def data_pinned_context(inputs, tmp_path, monkeypatch):
    make, _, d = real_context(inputs, tmp_path, monkeypatch)
    (tmp_path / "dp").mkdir()
    ws, h = repo_with_data_pin(tmp_path / "dp")
    authorise(ws, h, 1)
    return make, ws, d


def test_a_software_exception_set_off_by_a_changed_data_pin_is_integrity_with_no_software_record(inputs, tmp_path, monkeypatch):
    make, ws, d = data_pinned_context(inputs, tmp_path, monkeypatch)

    def changes_the_data_then_frozen_code_raises(ctx):
        (ws.root / DATA).write_text("changed under the experiment\n")
        C.frozen_copy_injected_failure()
    r = C.run_attempt(ws, make, {**runners(), "E002": changes_the_data_then_frozen_code_raises}, fake_analyse)
    e = ws.events()[-1]
    assert r["class"] == "integrity" and e["software_experiments"] == [] and [f["input"] for f in e["integrity"]["findings"]] == [DATA]


def test_a_data_pin_vanishing_under_an_experiment_is_integrity_not_environment(inputs, tmp_path, monkeypatch):
    make, ws, d = data_pinned_context(inputs, tmp_path, monkeypatch)

    def deletes_the_data_then_reads_it(ctx):
        (ws.root / DATA).unlink()
        (ws.root / DATA).read_text()
    r = C.run_attempt(ws, make, {**runners(), "E001": deletes_the_data_then_reads_it}, fake_analyse)
    assert r["class"] == "integrity" and ws.events()[-1]["integrity"]["findings"][0]["finding"] == "missing"


def test_every_finding_of_data_fits_and_session_inputs_is_recorded_together(inputs, tmp_path, monkeypatch):
    make, ws, d = data_pinned_context(inputs, tmp_path, monkeypatch)
    calls = []

    def fits(root):
        calls.append(root)
        if len(calls) > 1:
            raise C.IntegrityFailure([C.integrity_finding(None, "closeout_fits/rehearsal/e003_fit.json", "modified", "cd" * 32)])
    monkeypatch.setattr(C, "check_fit_manifest", fits)

    def changes_everything(ctx):
        (ws.root / DATA).write_text("changed\n")
        inputs.paths["book"].write_text("changed")
        return []
    r = C.run_attempt(ws, make, {**runners(), "E002": changes_everything}, fake_analyse)
    e = ws.events()[-1]
    got = {(f["session"], f["input"]) for f in e["integrity"]["findings"]}
    assert r["class"] == "integrity" and e["exception"] == "PinnedDataChanged"
    assert (None, DATA) in got and (None, "closeout_fits/rehearsal/e003_fit.json") in got and (d[10], "book") in got and (d[11], "book") in got


def test_collect_findings_lets_a_finding_win_over_a_check_that_cannot_run():
    finding = C.IntegrityFailure([C.integrity_finding("d", "book", "missing")])
    with pytest.raises(C.IntegrityFailure) as e:
        C.collect_findings(lambda: (_ for _ in ()).throw(OSError("EIO")), lambda: (_ for _ in ()).throw(finding))
    assert e.value.findings == finding.findings
    with pytest.raises(OSError):
        C.collect_findings(lambda: (_ for _ in ()).throw(OSError("EIO")), lambda: None)
    C.collect_findings(lambda: None, lambda: None)


def test_the_unread_context_never_consumes_an_attempt_once_the_data_is_back(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    make = C.unread_test_context()
    make.mode = "rehearsal"                              # the wiring only; test mode itself runs only in the project repository
    with pytest.raises(C.Refused, match="start again"):
        C.run_attempt(ws, make, runners(), fake_analyse)
    assert ("started", 1) not in events(ws)


def test_recovery_after_a_death_records_a_changed_fit_artifact_as_integrity(tmp_path):
    ws, _ = repo_with_data_pin(tmp_path)
    fits = ws.root / "results/closeout_fits"
    (fits / "rehearsal").mkdir(parents=True)
    (fits / "rehearsal/e003_fit.json").write_text("{}")
    (fits / "MANIFEST.json").write_text(json.dumps({"rehearsal/e003_fit.json": C.sha256_file(fits / "rehearsal/e003_fit.json")}))
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "fits")
    p = ws.root / C.FREEZE_RECORD
    rec = json.loads(p.read_text())
    rec["pinned_sha256"][C.FIT_MANIFEST] = C.sha256_file(ws.root / C.FIT_MANIFEST)
    p.write_text(json.dumps(rec))
    h = C.sha256_file(p)
    with open(ws.root / "docs/DECISIONS.md", "a") as f:
        f.write(C.FREEZE_APPROVAL.format(h=h) + "\n")
    ws.git("add", "-A")
    ws.git("commit", "-q", "-m", "pins the manifest")
    authorise(ws, h, 1)
    assert run_dying(ws, "E001") == 137
    (fits / "rehearsal/e003_fit.json").write_text('{"changed": 1}')
    assert C.recover(ws) == "attempt 1 failed"
    e = ws.events()[-1]
    assert e["failure_class"] == "integrity" and e["integrity"]["findings"][0]["input"] == "closeout_fits/rehearsal/e003_fit.json"


def test_a_death_before_the_third_attempt_records_integrity_without_a_note(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    assert run_dying(ws, "E001") == 137
    (ws.root / DATA).write_text("changed\n")
    assert C.recover(ws) == "attempt 1 failed"
    assert "integrity_noted" not in [e["event"] for e in ws.events()] and ws.events()[-1]["failure_class"] == "integrity"


def test_repeated_recovery_does_not_repeat_the_same_note(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    assert attempt(ws)["outcome"] == "completed"
    (ws.promoted / "CLOSEOUT_report.md").unlink()
    (ws.root / DATA).write_text("changed\n")
    findings = C.pinned_data_findings(ws, json.loads((ws.root / C.FREEZE_RECORD).read_text()))
    ws.append({"event": "integrity_noted", "n": 1, "reason": "an earlier recovery", "integrity": {"findings": findings}})
    assert C.recover(ws) == "repeated promotion and report"
    assert [e["event"] for e in ws.events()].count("integrity_noted") == 1


def test_a_protocol_change_with_a_data_change_is_a_refusal_not_an_attempt(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    (ws.root / DATA).write_text("changed\n")
    (ws.root / C.PROTOCOL).write_text("# protocol (FROZEN)\nedited\n")
    ws.git("commit", "-qam", "both")
    with pytest.raises(C.Refused, match="pinned file differs from the freeze record: docs") as e:
        C.run_attempt(ws, never_read, runners(), fake_analyse)
    assert not isinstance(e.value, C.PinnedDataChanged) and ("started", 1) not in events(ws)


@pytest.mark.parametrize("entry", [["not", "a", "dict"], {"undefined": False, "reason": None, "e001_valid": True, "episode_valid": True, "e001_reason": None,
                                                          "episode_reason": None, "sha256": ["states", "book", "trades", "receipts"]}])
def test_a_malformed_session_entry_is_refused(tmp_path, entry):
    ws, rec = status_ws(tmp_path)
    rec["sessions"][next(iter(rec["sessions"]))] = entry
    with pytest.raises(C.Refused, match="malformed"):
        C.verify_input_status_record(ws, rec, REAL_RC["splits"]["test"])


def test_a_data_pin_changed_while_the_context_is_built_is_integrity(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)

    def builds_then_fails(out, progress):
        (ws.root / DATA).write_text("changed while the context is built\n")
        raise OSError("a read failed")
    r = C.run_attempt(ws, builds_then_fails, runners(), fake_analyse)
    e = ws.events()[-1]
    assert r["class"] == "integrity" and e["integrity"]["findings"][0]["input"] == DATA


def test_a_death_on_attempt_three_with_a_changed_data_pin_closes_with_the_finding(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    for n in (1, 2):
        authorise(ws, h, n)
        attempt(ws, ("E001", None, "environment"))
    authorise(ws, h, 3)
    assert run_dying(ws, "E002") == 137
    (ws.root / DATA).write_text("changed\n")
    assert C.recover(ws) == "closed"
    ev = ws.events()
    assert [e["event"] for e in ev][-2:] == ["failed", "closed"] and ev[-2]["failure_class"] == "integrity" and "integrity_noted" not in [e["event"] for e in ev]


# ------------------------------------------------------------------------------------------------ release-candidate review: the two blocking findings
def test_a_changed_discovery_reference_is_recorded_as_integrity_not_refused_by_the_environment_guard(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    (ws.root / DATA).write_text("changed after the freeze\n")
    called = []

    def environment_guard():
        called.append(1)
        raise C.Refused("a pinned reference differs from its frozen manifest")     # what verify_environment does for e001_discovery.json
    r = C.run_attempt(ws, never_read, runners(), fake_analyse, env_check=environment_guard)
    assert r["class"] == "integrity" and called == [] and events(ws)[-2:] == [("started", 1), ("failed", 1)]


def test_the_environment_guard_still_runs_when_every_pin_holds(tmp_path):
    ws, h = repo_with_data_pin(tmp_path)
    authorise(ws, h, 1)
    with pytest.raises(C.Refused, match="frozen manifest"):
        C.run_attempt(ws, never_read, runners(), fake_analyse, env_check=lambda: (_ for _ in ()).throw(C.Refused("a pinned reference differs from its frozen manifest")))
    assert ("started", 1) not in events(ws)


def test_a_session_input_vanishing_while_the_context_is_built_is_integrity(inputs, tmp_path, monkeypatch):
    make, ws, d = real_context(inputs, tmp_path, monkeypatch)

    def verifier_reads_a_vanished_input(rc, days):
        inputs.paths["book"].unlink()
        inputs.paths["book"].read_bytes()
    monkeypatch.setattr(C.E1, "verify_inputs", verifier_reads_a_vanished_input)
    r = C.run_attempt(ws, make, runners(), fake_analyse)
    e = ws.events()[-1]
    assert r["class"] == "integrity" and {(f["input"], f["finding"]) for f in e["integrity"]["findings"]} == {("book", "missing")}

