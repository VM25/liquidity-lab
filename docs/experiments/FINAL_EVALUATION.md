# Final held-out evaluation — protocol (FROZEN)

**Status:** frozen, revision 9, of 2026-11-04, with the owner's choices applied and the owner audit's corrections. The owner approved
this revision on 2026-11-04 (section 9, step 1); the step-3 pre-check ran the same day under the owner's authorisation
(`results/closeout_freeze/input_status.json`); the freeze commit holds this text and `results/closeout_freeze/freeze_record.json` (step 4).
Only the title and this status paragraph changed at the freeze. Revision 9 adds the round-6 corrections and the recovery record `integrity_noted`. A drafted rule for carrying check 2 forward
from an earlier commit, and a scoped check 3, were withdrawn by the owner on 2026-11-04 after independent review found the rule unsound;
section 7's full evidence requirement stands unchanged (audit record, section 6d). **The run needs the owner's approval of the freeze record in `docs/DECISIONS.md` (step 5) and a separate `authorised` record (section 6).** The protocol has had two adversarial reviews and three
targeted re-reviews (`docs/audits/2026-10-29_final_evaluation_protocol_review.md`, `docs/audits/2026-11-01_final_evaluation_protocol_review_r2.md`).
The close-out code has had one adversarial review and a conformance check (`docs/audits/2026-11-02_closeout_code_review.md`), the owner's
independent audit, and a focused independent review of the corrections with a verification pass on its fixes
(`docs/audits/2026-11-03_closeout_audit_response.md`, which holds every disposition and the evidence index).

No test-session outcome exists. The five test sessions are sealed. The `lpx` research runners refuse them. Three existing
tools (`tools/reproduce_e002_session.py`, `tools/verify_e001_stdlib.py`, `tools/verify_stdlib.py`) have no test-day
refusal and must not be pointed at test days.

This protocol takes effect only when it is frozen (section 9). The owner's choices are recorded in section 11.

**Purpose.** Run the frozen flagship experiments E001–E004 on the five test sessions and check whether each discovery
decision holds out of sample. The experiments' code and configuration are unchanged. Every rule is fixed before any test
outcome exists. This is the Stage 4 close-out in `configs/research_v1.toml`.

**Out of scope:**
- Track A: A1's specification excludes the test sessions.
- New models, policies, parameters or hypotheses.
- Selection among variants: E003 and E004 forward every variant they ran.
- Pooled discovery-plus-test estimates.
- Discovery-rule labels or session-bootstrap intervals reported on five sessions.

## 1. Sample, validity and inputs

**Test sessions:** 2026-06-01, 2026-07-01, 2026-08-01, 2026-09-01, 2026-10-01 (`[splits].test`).

**Input status is fixed before the freeze (step 3 of section 9).** The pre-check parses no price, trade or state row and reads no
Parquet footer. **These are its only reads of data and acceptance files:**

| File | Read | Used | Why it is needed |
|---|---|---|---|
| The four inputs of each test session: `book_states/SOLUSDT/<day>.parquet`, Tardis `book_<day>.parquet`, Tardis `trades_<day>.parquet`, Binance Vision `trades_<day>.parquet` | whole-file bytes, for a hash only; never parsed | SHA-256 | Pins the exact inputs. The bytes pass through the hash and are not kept |
| `results/acceptance_001/windows.csv` | every column of every row, test days and other symbols included, passes through the parser and through a whole-file hash for the record's provenance; only the listed columns of SOLUSDT joint rows of the listed days are kept | `start_us`, `end_us`, `duration_s`, `layer`, `source`, `symbol`, `day`, `integrity_status` | Windows, episodes and integrity status |
| `results/acceptance_001/summary.json` | parsed whole; its provenance is checked inside the parsing function and **only** the listed sessions' `normalized_inputs_sha256` leave it. Also hashed whole for provenance | those fields | The acceptance hashes live only in this file. It also holds the test days' acceptance diagnostics, already listed as known below. They are not used, kept, written or printed |
| `results/e004_prefreeze/schedule_hashes.json`, `configs/*.toml` (including `closeout_v1.toml`, read at import and unused) | parsed | date-only schedule hashes and settings | No market data |

Its other reads hold no market data: `lpx/**/*.py`, the tool and `uv.lock` (hashed for provenance), git's metadata, and at step 3 the
authorisation record, `docs/DECISIONS.md`, this protocol and the evidence files (section 7's guard). On stand-ins too, `summary.json` is
parsed whole and `windows.csv` scanned, so test-day metadata rows pass through the parser; nothing of them is kept.

For each test session it records:
- the SHA-256 of each of the four inputs, with the three normalised inputs checked against `summary.json`. The state file has no
  acceptance hash, so its hash pins it from here on;
- the session's accepted joint windows and integrity status;
- its E002–E004 episodes (at least `min_episode_s` = 600 s);
- a machine-readable reason, below.

The record is written whole, with its provenance (commit, code fingerprint, tree hashes, tool hash, package versions, input-list
hashes), and never over an existing file. It is committed at step 3 and pinned by the freeze record.

**Reads deferred to the run (owner choice, section 11).** The frozen `verify_inputs` reads each state file's Parquet footer (its `lpx`
provenance key) and `sensitivity.json`. A footer can hold price and quantity statistics, so the pre-check does not call it. It runs at the
start of an attempt, after the guards, when test files are about to be opened anyway. So the state file's provenance is confirmed at the
run, not before the freeze, with these consequences, all independent of outcomes because the bytes are pinned:
- a footer naming other windows, a dirty export or no `lpx` key among its key-value metadata is the frozen verifier's own mismatch: that
  session is *undefined (input mismatch: frozen_verifier)*;
- a footer with no key-value metadata at all (a `TypeError` in the verifier), an `lpx` value that is not JSON, or a footer that cannot be
  parsed is not an input result: the attempt fails, the same bytes fail every retry, and after the third the evaluation closes with no
  labels (section 6);
- a run-wide fault, `summary.json` or `sensitivity.json` not from the acceptance run of record, aborts the attempt; it never counts
  against a session. `sensitivity.json` is pinned by hash at the freeze.

**Pass or fail, per experiment.** Before the run, only these reason codes can make a session unusable:

| Reason code | Meaning | Effect |
|---|---|---|
| `input_missing:<input>` | the file is still absent after three rechecks one second apart, its directory exists, the discovery inputs are present (the volume is whole), and the path is not a dangling link | *undefined (input)*, every experiment |
| `hash_mismatch:<input>` | the hash differs from the acceptance run's (`book`, `trades`, `receipts`) | *undefined (input)*, every experiment |
| `acceptance_record_missing`, `acceptance_hash_missing:<input>` | the acceptance run has no record or no hash for it | *undefined (input)*, every experiment |
| `integrity_not_accepted` | a window's integrity status is not accepted | *undefined (input)*, every experiment |
| `no_accepted_joint_windows` | no accepted joint window | no valid unit in every experiment; not undefined |
| `no_qualifying_episodes` | no episode of at least 600 s | E001 stays valid; no valid unit in E002–E004; not undefined |

**Anything else aborts the pre-check with no record written**, and it is rerun after the cause is fixed. That covers a disk or memory
error, an absent data directory, a volume whose discovery inputs are missing too, a dangling link, an acceptance summary that is not the
run of record, a parsing error and any unexpected software exception. No such failure can remove a session.

These statuses are decided before the freeze, except the state file's provenance, which is confirmed at the run (above).

**At run time** the close-out first checks that the input-status record came from step 3 and agrees with itself: test mode; the hash of the
committed step-3 authorisation; a full commit SHA that is an ancestor of HEAD; `windows.csv` and `summary.json` unchanged since it was made;
exactly the five sessions; only the codes above; `undefined` and the validity flags agreeing with them; and a SHA-256 for each of the
four inputs of every session that is not undefined. A record that fails any of these is refused before an attempt starts. Test-day inputs
are read only inside a started attempt.

**After the freeze, the record is the reference for every input it pins.** Each of the four inputs of every session the record does not
mark undefined must be present as a file and hash to exactly its pinned SHA-256. The check runs at the start of each attempt, again in the
metadata step (section 6), and again whenever the attempt fails or an experiment raises, before the failure is classified. An input that is
**missing** (a deleted file, a dangling link, a directory in its place or an absent directory alike), whose bytes are **modified** (any
SHA-256 other than the pinned one), or that the record does **not pin**, is an **integrity failure** of the attempt (section 6). This holds
whatever exception the change set off: a frozen function that raises on changed bytes, or a read of a vanished file, is recorded as
integrity, not as software or environment, and leaves no software record that would bar a retry. An integrity failure is never an input
result: it never makes a session undefined and never removes a session from any check. The `failed` event records every finding of the
check (session, input, finding and, for modified bytes, the SHA-256 observed), and the report's run history shows them. The fit artifacts
and the data files the freeze record pins follow the same class (section 6). Data are never repaired or re-acquired, so a finding that
persists fails every retry, and the third failed attempt closes the evaluation with no labels. An input that is present but cannot be read
(an operating-system error) is an environment failure; it too removes no session.

Only on inputs whose bytes match their pins do the frozen verifiers run. Their own mismatch, `frozen_verifier` (the state file's
provenance, above), is the one run-time verdict that makes a session *undefined (input mismatch)*. It is written to the run metadata, and
the `DECISIONS.md` entry is made after the run. Any other exception follows section 6's classes and never removes a session.

**Validity (as frozen):**
- **E001** uses all accepted joint windows under its frozen event rule. It has no minimum window length.
- **E002–E004** use episodes of at least 600 s.

**Already known about these sessions, none of it an outcome:**
- The acceptance diagnostics.
- The relative tick: 0.85–1.37 bp, against 0.46–1.20 bp on discovery.
- The E004 test-day schedules, fixed by `results/e004_prefreeze/schedule_hashes.json` (SHA-256 `99ca1a82…`). That list
  covers roles 0–3 of all 7 cells on all 20 days. Role-4 placebo windows and D4 noise are fixed by the seed derivation in
  `configs/e004_v1.toml`.

## 2. What is frozen and forwarded

**Code baseline.** The `lpx` tree of the E004 run of record, `5c9d93e`, with code fingerprint `2a594e2dc1a22940`.

The same fingerprint produced the step-5 evidence:
- E002 reproduced bit for bit (`f92bb6c`);
- E003's models at 5 s, REF forecasts, calibration and REF policy rows reproduced (`f92bb6c`);
- one full E003 session reproduced (`eb1b1cf`).

E001's code (`lpx/research/e001.py`) is unchanged since its discovery run (`c034d6b`).

**Allowed difference.** `git diff --name-status 5c9d93e <freeze commit> -- lpx tools tests configs pyproject.toml uv.lock .python-version`
must list exactly these **added** files:
- `lpx/research/closeout.py` and `lpx/research/closeout_analysis.py`;
- `tools/closeout_fits.py`, `tools/closeout_precheck.py` and `tools/closeout_dryrun.py`;
- their tests;
- `configs/closeout_v1.toml`.

No existing file may be modified. The orchestration inside the frozen `run()` functions is therefore **re-implemented**
in `closeout.py`, calling the frozen experiment functions. Its equivalence is established by the dry run (section 7), not
assumed.

**Pinned references.** The freeze record lists SHA-256 values that are verified at the start of the run, at its end, and
by the analysis. `results/acceptance_001/` here means `summary.json`, `sensitivity.json` and the windows CSVs:
- this protocol and the specifications `E002.md`, `E003.md`, `E004.md`;
- the configurations: `research_v1`, `e002_v1`, `e003_v1`, `e004_v1`, `closeout_v1`;
- `pyproject.toml`, `uv.lock` and `.python-version`, with installed package versions verified at run time;
- `results/e003/e003_analysis.json` (source of δ_h);
- `results/e001/e001_discovery.json`, checked against `E001_frozen_manifest.json`;
- `results/e004_prefreeze/schedule_hashes.json`;
- `results/acceptance_001/summary.json`, `sensitivity.json` and the windows CSVs;
- the input-status record;
- every fit artifact;
- every file in the allowed-diff list above.

**Forwarded fits.** These are computed before the freeze by `tools/closeout_fits.py` from the 15 discovery sessions only,
committed with their SHA-256 values, and loaded (never refitted) at run time. Every artifact records its trained-on
sessions, and the run and the analysis assert that this list equals the 15 discovery days.

| Experiment | Forwarded |
|---|---|
| E001 | the size-tercile edges `size_tercile_edges_base_qty` from `e001_discovery.json` |
| E002 | none |
| E003 | Walk-forward machinery called with `before = "2026-06-01"`: training rows thinned as E003 does (every 5th eligible row); M1/M2 for h ∈ {1, 5, 30} s (regressors, clip bounds, coefficients, trained-on sessions, row counts); the rv-60s training median and P4 gate (E003 §10) |
| E004 | NV = the all-15 M2 at 5 s. For every cell and target: UA and PL pooled groups; RF, UA and PL λ; UA-β; training-row counts. These come from `training_rows` on all 15 sessions (role 0, including s15) with placebo-training draws (role 2), and `fit_cell(..., before = "2026-06-01")` (E004 §8). |

**Test-day randomness (E004).** 3 evaluation replicates (role 1), placebo indicators (role 3) and placebo windows
(role 4).

## 3. Confirmation rules

### 3.1 General

**Fee attainability.** VIP0 is the only attainable fee schedule. Every other schedule is *hypothetical* (VIP0+BNB, VIP9,
LP tier 1, LP tier 4). Every check, table and number carries its status label (*observed* / *modeled historical replay* /
*… under stress test* / *stress test* / *synthetic*), and, where fees enter, an attainability tag.

**Definedness:**
- A session value is defined when the experiment's frozen rule defines it. Examples: a bp contrast needs fills for both
  policies; D_W needs at least 20 distinct filled orders in both windows; R²_OS needs evaluation rows.
- The only session-level exclusions are the pre-specified session input-status rules (section 1). **A software exception never
  excludes a session** (section 6).
- Means and ratios of sums use defined sessions only. Nothing is imputed.
- A check with several components averages each component over its own defined sessions. The check is **not
  confirmable** if any component is defined in fewer than 4 of the 5 sessions, or if a gate fails.

**Sign and side counts.** Where a confirmation rule in this protocol contains a sign or side count, whether the rule is
frozen or protocol-supplied:
- the count is over all 5 sessions;
- an undefined session counts as a failure;
- sign and side counts appear in no other rule.

**Gates.** Share gates (activity, withdrawn share, overlap) are means over the sessions valid for the experiment
(section 1) and not undefined at run time, of per-session values, in the check's own scenario and fee schedule. For E004 the per-session values are
pooled over replicates. This is the discovery aggregation (DECISIONS 2026-10-28). The H4-F gate's mean L uses the sessions
where L is defined.

**Labels per check.** Each label states its basis.

| Label | Meaning |
|---|---|
| **confirmed (point estimate, k of 5 defined)** | Every condition of the frozen check holds. It is a replication of the discovery decision at the point estimate, not an equivalence test and not an independent proof. |
| **not confirmed** | A condition fails. With five sessions this is **not a refutation** of the discovery result and not evidence for the opposite claim. It means the point estimate failed the frozen check. |
| **not confirmable** | The definedness rule or a gate fails, or an unexpected software exception affected the experiment (*software*), or the close-out failed closed (*run failure*) (section 6). |
| **reported only** | The discovery decision was inconclusive, not testable or descriptive, or the frozen specification makes it reported only (E002 §10 when H2 is not supported; E004 §8 for H4-0). If its experiment is not confirmable for a software or run-failure reason, it is labelled *not run (reason)*. |

**Compromised** is a flag on top of a label, never a replacement (section 6).

Every check row shows:
- its five session values, with undefined sessions marked;
- the number of defined sessions;
- the sign and side counts;
- a t-interval on the session values where one is defined, labelled *descriptive, not used*. For ρ_A it is shown on A and
  L.

**Qualifiers and reported counterparts** have the test forms given below. They are computed on test, are final, trigger
no review, and never change a label.

**Regime shift** can affect confirmations and non-confirmations alike. Neither is reinterpreted after the outcome.

### 3.2 E001 — observed markouts (status *observed*)

E001's discovery specification gives no confirmation rule. This protocol supplies one (section 10):
- Primary specification only: timestamp-side clusters and exchange-clock conditioning.
- A metric is **confirmed** if its mean of session means has its discovery sign **and** that sign holds in at least 4 of
  the 5 sessions.

| Metric | Discovery sign | Check |
|---|---|---|
| mo(1 s), mo(5 s), mo(30 s) | > 0 (15/15 sessions) | yes |
| rs(1 s), rs(5 s), rs(30 s) | < 0 (14/15, 14/15, 15/15) | yes |
| es | > 0 (15/15) | **reported only**. The same sign test is shown beside it with no confirmatory weight: a positive effective spread is close to mechanical for aggressive trades. |

- **One family.** rs = es − 2 mo links the checks, so E001 is reported as one family, "k of 6".
- **Reported only:** the conditioning cells, all 12 entries of `sensitivity_specs`, the proxy validation, the secondary
  horizons, the pre-state ages and the exclusions.
- **Not computed on test** (section 11): the E001 exploratory tables. They were declared exploratory, not
  pre-registered.

### 3.3 E002 — execution sensitivity (status *modeled historical replay*)

E002 §10.10 applies: "If H2 is not supported on discovery, the test sessions only report the same tables; no confirmation
claim is made." H2 was *not supported* and no fill-model difference was material, so every E002 table is **reported
only**.

Conditions (a) and (b), `h2_supported_on_discovery` and the `material` flags are **not computed on test**. They are
interval rules needing at least 12 defined sessions and are false by construction on five.

### 3.4 E003 — signals and quoting (forecasts *observed*; policies *modeled historical replay*)

E003 §10 applies, with the all-15 fits. §10 contains no sign or side counts, so they are reported, not used.
H1-F is evaluated first.

| Decision (discovery) | Setting | Test rule (E003 §10; gates from §8) |
|---|---|---|
| **H1-F holds** (M2 R²_OS > 0) | h = 5 s, regional decision clock, evaluation rows, zero-forecast benchmark | **confirmed** if the mean R²_OS > 0 |
| **H1-T supported** (D = gross bp/notional of P3[M2] − P3[−M2]; discovery −0.12 bp [−0.32, +0.07], 4/10 positive; δ = 0.5 bp) | intermediate × regional; gross bp, fee-free | **confirmed** if the mean D < 0 (discovery sign) **and** the mean D < δ (§10: "the same sign on the test sessions and, for H1-T, the same side of δ"). **Not confirmable** if H1-F is not confirmed (§8: "**Not testable** if H1-F fails"), or if the mean `gate_active_share` of P3_M2 or P3_negM2 is below `h1_min_gate_activity` = 0.05 (§8). |
| **H3 supported** (P4 − P3F[M2], LP tier 4, *hypothetical*) | intermediate × regional; LP tier 4 rows | **confirmed** if the mean 5-min ES difference < 0, the mean maximum-drawdown difference < 0, the mean net-per-hour difference > 0 (discovery sign), and the mean net-per-hour difference > −δ_h |

**H1-T, read literally** (owner choice, section 11). The frozen rule is preserved. Sign and economic materiality are reported
separately: the sign (D < 0: yes/no) and materiality (D < δ = 0.5 bp: yes/no). Discovery could not distinguish D from zero,
so the sign condition is the binding one and implies the δ condition. A **not confirmed** result with 0 ≤ mean D < δ means
only that the sign differed. It is not evidence of material translation, which would require D > δ, E003's *refuted* side.

**δ_h.** δ_h = `H3.noninferiority_margin` = 1.1754724725329382 USDT/h, read from the pinned `e003_analysis.json`. The
discovery sign of the net-per-hour difference is positive, so the −δ_h condition is implied by the sign condition and
cannot change the label. It is reported separately, and a mean in (−δ_h, 0] is described as "non-inferior, but the sign
differs".

**H3 abstention.** H3 has no abstention gate: E003 §8 applies *not testable: abstention* only to the descriptive VIP0 and
VIP9 contrasts. Those contrasts are reported with that label, as in `e003_analysis.h3`'s `other_schedules`. The LP tier 4
notional shares of P3F[M2] and P4 relative to P3[M2] are reported next to H3.

**Reported next to H3** (qualifiers, no effect on the label):
- **partly mechanical**, if mean(P4 `turnover_per_hour`) / mean(P3F[M2] `turnover_per_hour`) over the defined test
  sessions is < 0.50 (§8);
- the participation-normalised differences `es_per_k_turnover` and `inventory_per_k_turnover`;
- A1's caveat: passing 0.50 does not show that the risk reduction is independent of activity.

**Participation at VIP0 has no decision rule on test** (owner choice, section 11). The seven trading policies' results and
the no-trade comparison are reported as **descriptive results only**, with no label and no yes/no outcome, and none of them
is ever called confirmed. For P0, P1, P3[M1], P3[M2], P3[−M2] (VIP0 overlay rows) and P3F[M2], P4 (their own VIP0 fee-rule
rows), at intermediate × regional, the report shows:
- mean `net_per_hour` and the difference from no-trade (NT, net 0);
- gross per hour, maker fees per hour (labelled *mechanical*), taker fees per hour, turnover, and the number of sessions with
  trades.

P3F[M2] and P4 abstained in every discovery session at VIP0, so a zero for them is mechanical. On discovery, preferring a
policy to not trading required a 99.29% interval above zero; a positive point estimate on five sessions does not show that.

**E003 §8's "also reported" quantities are required test outputs** (the `H1.reported` block): D on net per hour; P3[M2] −
P0 in gross bp and net per hour; the ranking check (M2 − M1 in R²_OS against P3[M2] − P3[M1] in gross bp); and P3[M2]'s net
per hour at VIP0. Every VIP0 per-hour contrast is shown with gross and fee terms split, and the fee term labelled
*mechanical*.

### 3.5 E004 — information robustness (statuses as in E004)

E004 §8 applies. Its scope is limited by E004 §6: "A *supported* label is a statement about fill selection. A claim that
the uncertainty-aware **policy** outperforms also requires the realised U-vs-P comparison below."

The realised U vs P, U vs N and P vs N comparisons and every net-per-hour figure are **descriptive test replications,
never confirmations**. They are produced through the allow-list in section 7:
- VIP0 is shown with the mechanical fee saving separated;
- LP tier 4 is *hypothetical*;
- P3 under UA-λ vs PL-λ is *participation-changing; descriptive*.

**H4-W gates**, in test form: D1-E, intermediate × regional, the N run, 3 replicates:
- the withdrawn share is ≥ 0.5% (mean);
- at least 20 distinct filled orders in both windows, with D_W defined, in at least 4 of 5 sessions;
- the overlap of W_P with W_U is ≤ 10%, as the mean of the per-session pooled shares.

**H4-F gates**, for each cell and target: mean L ≥ 0.20 pp, and L > 0 in at least 4 of 5 sessions. ρ_A uses the sessions
where both A and L are defined.

| Decision (discovery) | Test rule (E004 §8) |
|---|---|
| **H4-W[P0] immaterial selection (< δ)** (D_W −0.04 bp) | **confirmed** if the mean D_W < δ = 1 bp **and** D_W < δ in at least 4 of 5 sessions. One-sided, as frozen. |
| **H4-W[P3[M2]] immaterial selection (< δ)** (D_W −0.16 bp) | the same rule |
| **H4-F D1-S, y_view: not supported** (ρ_A −0.007) | **confirmed** if ρ_A = ΣA / ΣL < 0.25. Not confirmable if ΣL ≤ 0 over the sessions where A and L are both defined. The gate uses every defined L, so this case is reachable when A is undefined in a session with a large L, and the safeguard then decides the label. |
| **H4-F D3, y_view: not supported** (ρ_A −0.008) | the same rule |
| H4-F y_k (D1-S, D3) *inconclusive*; D1-E and D2 *not testable*; D4 *inconclusive*; D1-S1 and D1-S3 descriptive; H4-0 *harmless* | reported only, with their test values |

**The y_view row.** D1-S and D3 are projected to match (E004 §0) and are nearly identical on discovery, so they are shown as
one row with two cells. Each cell carries its own E004 §8 label. For the tally, the row is:
- *not confirmable* if either cell's gate or definedness fails;
- *confirmed* only if both cells are confirmed;
- otherwise *not confirmed*.

**H4-F is secondary and is reported against its projections.** E004's header says it is "reported against pre-registered
projections, not as a discovery". Every D1-S and D3 H4-F row therefore shows:
- the projection from the pinned `h4f_projection` (y_view: ρ_A 0.0; y_k: ρ_A 0.37, ρ_B 0.31, L 0.75 pp);
- the observed ρ_A minus that projection (E004 §6: "the informative quantity");
- this fixed note: "Secondary. Largely implied by the target choice (E004 §0, §9); reported against the projection, not as
  a discovery."

Projections apply to D1-S and D3 only.

**Required interpretation of H4-W.** The E004 rule stays one-sided at 1 bp. A confirmed H4-W is always worded "**no material
deterioration under the specified threshold**". It is never worded as equivalence or as proof of no effect. It says nothing
about improvement, and nothing about deterioration smaller than 1 bp.

**Reported next to the H4-W checks** (no effect on the label): the sign of the mean D_W and the number of sessions with
D_W < 0.

**Test forms of E004 qualifiers and counterparts** (reported only; final):
- **Stall-only qualifier.** The H4-W rule (mean < δ, at least 4 of 5) is applied to the stall-only D_W. As in `h4w()`, it
  reuses the main withdrawn-share and overlap gates and recomputes stall-window definedness (at least 20 orders in both
  stall windows, in at least 4 of 5 sessions). The qualifier is attached if that label differs from the main label.
- **Mean A below 0** (y_view row, only when its gates pass): the mean A < 0 over the defined sessions, shown with the mean
  A, A/L and the number of sessions with A < 0, next to the discovery values (D1-S −0.0055 pp, D3 −0.0066 pp; 6 of 10
  sessions in both). The row is attached only if the mean A < 0. E004 §6's *UA harmful* flag is an interval rule, so it is
  **not computed on test**, and this row does not carry that name. For each cell, this fixed sentence is printed only if
  the cell's mean A < 0 and |ρ_A| < 0.01: "Discovery had the same sign without a flag, under 1% of L, and E004 §0 projects
  ρ_A ≈ 0 on y_view. A negative mean of this size is not evidence that uncertainty-aware shrinkage does harm." Otherwise
  the row shows the values with no interpretive sentence.
- **D2 pending review.** D2 is *not testable* on test for a target exactly when its H4-F test gates fail. If either target
  passes its gates, every H4-F check and H4-0 carries the flag *pending review*. The flag is final, opens no review that
  could change any label, and is shown next to the H4-F labels.

Per-session A, L and A/L, and the leave-one-session-out range of ρ_A, are reported as descriptive.

## 4. Descriptive reporting

Every discovery output has a test counterpart listed in Appendix A, marked *check*, *reported only*, or *not computed on
test (reason)*, with the code that produces it. Nothing outside Appendix A is written or shown on test.

Each item is shown next to its discovery value:
- The discovery side is walk-forward for E003 and E004; the test side uses the all-15 fits.
- The test relative tick of each session is shown at the head of the report, against the discovery range, and applies to every
  bp result. δ thresholds are not rescaled.

Test-side intervals are descriptive t-intervals or session minimum/maximum, labelled *descriptive*. Discovery-rule labels
and session-bootstrap intervals are **not reported** on five sessions. Where a frozen function computes them internally,
they are discarded in memory, before anything is written, logged or displayed (allow-list, section 7).

## 5. Multiplicity and evidential weight

Confirmations are reported **per experiment**, as tallies, never as one total.

| Experiment | Checks | Dependence and role |
|---|---|---|
| E001 | 6, one family | they share events and are linked by an identity |
| E002 | 0 | reported only (E002 §10.10) |
| E003 | 3 from §10 | H1-T depends on H1-F; the seven-policy results are descriptive and outside the tally |
| E004, H4-W | 2 (the primary family) | they share windows |
| E004, H4-F y_view | 1 row, two cells | **secondary; shown separately with its note and not added to the H4-W tally** |

**A tally "k of N" is not N independent replications.**

**Evidential weight:**
- A check decided by the sign or side of a mean alone (E003's three) has a probability of up to 1/2 of being confirmed
  under a null distribution symmetric about its threshold. These are the weakest primary confirmations in this protocol.
- A single count condition (at least 4 of 5 sessions, with independent sessions and a null whose median is at the
  threshold) has probability 6/32 = 18.75%. A check that combines a mean with a count is bounded above by that figure.
- E004's y_view check is also decided by the side of a ratio, but the 1/2 figure does not describe it. E004 §0 projects
  ρ_A ≈ 0 against a threshold of 0.25, so once the gate passes, confirmation is largely implied by the target choice. Its
  informative quantity is ρ_A minus the projection.

## 6. Execution, one-time guarantee and failure handling

### Attempt ledger

`results/closeout_attempts.jsonl` is append-only, and each event is committed:

| Event | Committed by | Content |
|---|---|---|
| `authorised N` | the operator, before the run | attempt number, freeze-record hash, UTC time |
| `started N` | the entry point, after every guard passes and before its first test-file read | attempt number |
| `closed` | the terminal state | fallback report hash |
| `report_fix` | `closeout.py --report-fix` | commit, paths and diff hash of a report-rendering fix |
| `compromised` | the operator, when section 6's condition arises | scope, reason, optional corrected labels; never changes `closeout_analysis.json` |
| `log_opened` | `closeout.py --log-opening`, before a failed attempt's sealed log is opened | attempt number, reason |
| `failed N` | the failure path, or the recovery step after a process death | renamed path, listing, hashes, sealed-log SHA-256, exception type and location, failure class, the experiments that had a software exception, and for an integrity failure every finding: session (none for a fit artifact or a pinned data file), input, finding and observed SHA-256 |
| `completed N` | the entry point, as soon as `closeout_analysis.json` exists, or the recovery step | hashes of it and of `closeout_meta.json` |
| `integrity_noted N` | the recovery step, when it promotes a complete analysis, or closes the evaluation after a committed `failed 3`, while a pinned data file or fit artifact differs | the findings (once per distinct set); the analysis it promotes was made while every pin held |

If `authorised N` is committed more than once before it starts, the latest counts and the earlier stays visible. A record is consumed once its `started` event is in HEAD. A crash after that point, and before `closeout_analysis.json`
exists, uses up the attempt.

**The entry point refuses to start unless all of these hold:**
- HEAD has exactly one `authorised` record without a `started` event, and N is at most 3;
- every earlier attempt has both `started` and `failed`, and no `completed` event exists;
- `results/closeout/` and `results/closeout_staging/` do not exist;
- every `results/closeout_attempt<k>/` directory is named in a `failed` event, and every directory named exists and matches its hashes;
- each committed version of the ledger extends the previous one, and events are in a valid order;
- a retry's freeze record meets the limits below (compared with the first attempt's record, recovered from git);
- the freeze record's baseline and allowed list equal section 2's, and it pins every required reference;
- installed packages and Python match `uv.lock` and `.python-version`;
- `git status --porcelain` over the whole repository, untracked files included, is empty except for those listed
  directories, the pinned data files and the fit artifacts (whose changes are integrity findings, below);
- `LPX_ALLOW_DIRTY` is unset, every pinned code, configuration and document hash matches, no git variable redirects the repository or its index, no index entry is
  marked assume-unchanged or skip-worktree, and no ignored file other than bytecode caches sits in the close-out's scope;
- each attempt runs under the last `authorised N` before its `started N`; a later `authorised N` is ignored (it stays visible) and cannot
  change the retry lineage. Every earlier failed attempt's software statuses are known: if they could not be read when the failure was
  recorded, they are read at this start from the sealed directory, after its committed hashes are verified, and the start is refused
  while they still cannot be read;
- the `authorised` record's hash equals the SHA-256 of the freeze record in HEAD, and the committed `docs/DECISIONS.md` holds exactly the
  line `APPROVED close-out freeze record: <that SHA-256>`.

`results/closeout_dryrun/` is not exempt from the status check, so re-dry-run outputs are removed before an attempt.

**A pinned data file that differs is not a refusal.** A pinned file under `results/` (the acceptance files, the discovery references, the
input-status record, the fit manifest) that is missing or differs from the freeze record, while every guard above holds, is recorded as an
integrity failure of the attempt right after its `started` event, before anything is read; the input-status record is then not read
either. If the file is back to its pinned bytes by the time the guards run, the start is refused instead and no attempt is used, so the
record is read at the next start. Refusing instead would leave the evaluation waiting for those exact bytes to be put back, which is the restoration route section
11 rejects.

Any test-mode invocation outside this ledger flags every check **compromised** and is disclosed in the run history.

### One guarded invocation

All of these happen inside `results/closeout_staging/`, in this order:
1. E001, E002, E003, E004. Each experiment writes its tables only when all its sessions are done. Its
   `closeout_status_<experiment>.json` records *complete* with output hashes, or *not confirmable (software)* with the
   last session the experiment started (the exception may come from later work in the experiment), the exception type and location.
2. `closeout_meta.json`, written atomically, with every table's hash, the attempt number and the freeze-record hash. Pinned
   hashes are re-checked here, with the code fingerprint, the tree hashes, `TRACKED_SCOPE` cleanliness, the environment, every
   session's input hashes and the fit artifacts against their manifest. Commits since the run's start may touch
   `results/closeout_attempts.jsonl` only. An input missing or differing from its pin here (a session input, a fit artifact or a pinned
   data file) is an integrity failure (section 1); any other mismatch found here, after tables exist, is a close-out failure. Fit artifacts are checked by their pinned hashes and the
   trained-on assertion; their recorded commit and fingerprint are not compared with the current tree.
3. The analysis, which verifies that metadata and reads the staged tables.
4. `closeout_analysis.json`, written atomically, recording the metadata hash. The `completed` event is then committed.
5. Promotion to `results/closeout/`.

**No person reads any test table before promotion.**

**Console and log.** The console shows only the experiment, its outcome and the elapsed time. On a failure it shows "attempt
failed" with the exception type and the source location. stderr, warnings and full
tracebacks go to the sealed log, `closeout.log`, inside the staging directory.

**E004's built-in identity checks.** E003 staging tables are written in the frozen column layout, with status labels in a
sidecar `<table>.status.json`. They are hashed before E004 reads them. On test, `check_models`, `check_ref_forecasts` and
`check_ref_policy` run against the staging E003 outputs and the committed artifacts. There they are determinism and
no-mutation checks, not independent replications.

### Classifying a failure

The entry point classifies every exception automatically, with no human choice. The wrapper catches `BaseException`, so a
library panic cannot escape it. Classification uses the innermost frame under `lpx/`; library frames are skipped. **The pins come first:**
before an exception inside an experiment is accepted as software, and before any failure of the attempt is classified, every pinned input
is checked again: the sessions' inputs, the fit artifacts and the freeze record's data files (section 1); if one is missing or changed, the
failure is recorded as integrity with every finding of all three checks, and an integrity failure's findings are completed the same way.
A check that cannot run never hides another check's finding. An operator's
interrupt is not checked, and a check that cannot itself run leaves the failure's class as it was. A process death has no handler: the
recovery step records it as environment (it reads no test-day file), or as integrity if a pinned data file differs.

| Class | What it covers | Consequence |
|---|---|---|
| **Session input status** (not a failure) | the statuses step 3 fixed before the freeze (section 1's reason codes), and at the run the frozen input verifiers' own mismatch (exactly `RuntimeError` or `KeyError`, raised in the verifier's own frame) on inputs whose bytes match their pins | the pre-specified rule of section 1: the session is *undefined (input: <code>)* for a step-3 status, or *undefined (input mismatch: frozen_verifier)* at the run, on one session or on all. It is the only route by which a session leaves a check. Any other exception during an input check is not an input result: it falls to the classes below. |
| **Input integrity** | after the freeze, a pinned input that is missing, has bytes other than its pin, or is not pinned: a session's four inputs (input-status record), a fit artifact (pinned manifest) or a pinned data file (freeze record). Found at the start of an attempt, in its metadata step, or by the check made before any other failure is classified (above) | a failed attempt; no session is excluded. The rename (if staging exists) and the `failed` event apply, and the event records every finding. There is no fix, no re-dry-run and no new freeze record: the next `authorised` record names the same freeze-record hash. |
| **Environment** | `MemoryError`, `KeyboardInterrupt`, process death, and every `OSError` except a `PermissionError` that `lpx` code or a marked block raised itself (a frozen refusal). A denied read or write raised by the operating system or a library is environment | a failed attempt. The rename and the `failed` event apply. There is no fix, no re-dry-run and no new freeze record: the next `authorised` record names the same freeze-record hash. |
| **Unexpected software exception** | an innermost frame in baseline code or in a marked block, inside an experiment, while every pinned input still matches its pin (checked when the exception is caught; otherwise it is integrity) | the **experiment is not confirmable (software)**, whichever session raised. Its remaining sessions are not run and its tables are not written. Experiments depending on it are not confirmable too (E004 depends on E003). The last session the experiment started, the exception type and location are recorded, and the run continues with the other experiments. It is not a failed attempt, there is no retry (if a later failure of any class causes another attempt, that experiment stays not confirmable and is not rerun), and frozen code is never changed. |
| **Close-out failure** | anything else, including a frozen-frame exception raised outside an experiment, a helper of `closeout.py` (an artifact loader, a sidecar write), and the analysis step | a failed attempt, with the fix rules below. |

**Why an exception does not exclude a session.** Dropping the session and confirming on the other four would make the sample
depend on a failure that may be related to the data. Losing the whole experiment removes that selection. This costs the
experiment's labels, even if the cause was a close-out input surfacing in a frozen frame; the rehearsal exists to find such
causes before the freeze.

**Marked blocks.** Blocks copied from frozen `run()` bodies into `closeout.py` count as frozen code, including their nested
scopes. They are the functions named `frozen_copy_*`. Tests compare them, in order and with indentation, with `run()` at `5c9d93e`, allowing
only listed differences, each rewritten line with its exact replacement. The exceptions are the outer E004 orchestration
(`frozen_copy_e004`) and the first lines of `frozen_copy_e004_session`: a test asserts that their frozen checks are live statements, not
under a condition, and dry-run check 2 compares their output byte for byte. The table construction and writes of every experiment are marked blocks
(`frozen_copy_e001_tables`, `_e002_tables`, `_e003_tables`, `_e004_tables`, `_e004_write`), so an exception they raise on the data
is *software*, and an `OSError` or `MemoryError` there is *environment*. The runners hold no table code of their own. They
include the checks `e001.py:277` (pooled in the frozen code and kept pooled here), `e002.py:227`, `e004.py:517`, `:520`,
`:617`, `:693`, `:717`, and copied arithmetic such as `e004.py:704`. Whole-run provenance guards stay unmarked, so a failure
there is a close-out failure.

### Close-out failure before `closeout_analysis.json` exists

This covers the analysis step as well.
- The staging directory, including its sealed log, is renamed unread (`mv` only, inside `results/`) to
  `results/closeout_attempt<N>/`, and the `failed` event is committed.
- A fix goes into the added files only. It must not change which sessions or rows enter any check, may not change any rule,
  threshold or research choice, and may not remove or weaken a marked block.
- A fix is diff-reviewed with only the exception type and location, re-dry-run (checks 2 and 3), and given a new freeze
  record. That record may change only the parent commit SHA, the code fingerprint, the tree hashes of the trees containing
  touched files, and the hashes of the touched files. No file path may be added, so the allowed-diff listing stays
  identical, as do the fit artifacts and the input-status record. The owner authorises the new freeze record.
- The next `authorised` record is then committed.

After `closeout_analysis.json` exists, a failure is not a failed attempt, including on attempt 3. Only the `completed`
event, the promotion or the report is repeated, from the primary analysis. The analysis is never rerun. A report-rendering
bug may be fixed in the added files through `closeout.py --report-fix`, which commits a `report_fix` event with the diff's
hash and refuses any change outside the added files; it cannot change `closeout_analysis.json`.

### Up to three technical attempts: a disclosed qualification of "run once"

E002 §10.10 and E003 §10 say the test sessions are run once. This protocol pre-authorises up to three technical attempts,
**only** under these conditions, each enforced as stated:
- **Failed outcomes stay uninspected.** A failed attempt's directory is renamed unread and sealed, and nothing in it is
  analysed. The console shows no values.
- **Every attempt is auditable.** Each attempt has committed `authorised`, `started` and `failed` or `completed` events, with
  hashes of everything in its directory.
- **Retries cannot change research choices.** A retry reruns identical rules, fits and inputs: their hashes are pinned and
  the allowed-diff rule holds. A fix may touch only close-out plumbing and cannot change any rule.
- A software exception in frozen code gets no retry.

### Terminal state: fail closed

The third failed attempt is final. No fix, no rerun and no partial labels: **no label is extracted from an incomplete
execution, even for experiments that finished before the failure.**
- The sequence is `started 3`, then the rename to `results/closeout_attempt3/` and `failed 3`.
- Every check is *not confirmable (run failure)*, and every reported-only item is *not run (run failure)*.
- All tables stay sealed, with their hashes committed, and are never analysed.
- `closeout.py`, not the analysis, writes a fallback report to `results/closeout/CLOSEOUT_report.md`. It holds the run history
  and the labels above, from no sealed table, and a `closed` event is committed.

### Recovery after a process death

`closeout.py --recover` is part of the ledger. It needs no `authorised` record and reads no test table.

An event counts only once it is in HEAD. Before any other check, `--recover` removes a stale `.git/index.lock` and, if
`results/closeout_attempts.jsonl` differs from HEAD only by one appended tail line (complete or partial, staged or not),
restores that file to HEAD. Any other difference refuses. A discarded `started` means no test file was read and the
`authorised` record stays unconsumed; a discarded `failed` or `completed` is re-derived by the branches below.

It runs only when one of these holds:
- the last `started N` has no `failed` or `completed` event;
- `completed N` exists without promotion, or `CLOSEOUT_report.md` is absent or empty;
- `failed 3` exists with no `closed` event.

It requires a clean repository apart from `results/closeout_staging/`, `results/closeout/`, the listed attempt directories and
`results/closeout_attempt<N>/` for the last started N, re-checks every pinned hash, and refuses while the attempt's process
still holds its lock. Promotion and the report use only an analysis whose hashes equal the `completed` event's.

A pinned data file or fit artifact that differs from its pin does not stop recovery, which reads no test table. If recovery then promotes a
complete analysis, or closes the evaluation after a committed `failed 3`, it first commits `integrity_noted N` with the findings (not again
for the same findings), shown in the run history; the analysis was made while every pin held, since the analysis step checks them first.
After a process death (branches 2 and 3) the `failed` event records the class integrity with the findings instead of environment.

It takes the first branch that matches, using file-existence and hash checks only:
1. `closeout_analysis.json` exists, and the metadata hash it records matches: commit `completed N` if missing, then promote
   and report.
2. N < 3: rename staging to `results/closeout_attempt<N>/` if it is still there, or adopt that directory if it was already
   renamed. If neither exists, record the path as null. Commit `failed N` with exception type `process death` and location
   null. The next `authorised` record follows.
3. N = 3: the same rename or adoption and `failed 3` if not yet committed, then the terminal state.

### After outcomes are read

- The first complete `closeout_analysis.json` is primary.
- A later correction is reported beside it, and the affected checks carry the **compromised** flag. Every tally line shows
  both forms, for example "E001: 4 of 6 confirmed (original); 1 compromised; corrected: 3 of 6".
- If a person views a test table before promotion, every check is flagged compromised.

**Sealed log access.** A sealed log may be opened only to diagnose a failure, and each opening is first committed as a
`log_opened` event. Renamed staging
directories stay sealed, with committed hashes, and are never analysed.

**Later analyses.** Any analysis of the test sessions after the close-out is labelled *post hoc, exploratory* and is never
cited as confirmation.

**Freeze is final.** No threshold, gate, margin or rule changes after the freeze.

## 7. Implementation and dry run (before the freeze)

**Fit tool** (`tools/closeout_fits.py`):
- refuses any test day before loading anything, and takes its sessions from `[splits].train + validation`;
- runs from a clean tree and records provenance, package versions, and `before`;
- serialises deterministically: sorted keys, repr floats, tuple keys encoded, None kept;
- an independent recomputation, in a separate clone made for it and set up with `uv sync --frozen`, must give byte-identical artifacts.

**Pre-check tool** (`tools/closeout_precheck.py`) produces the section 1 input-status record, with exactly section 1's reads. It also
verifies the test-day schedule hashes, which is a date-only computation. These are the only permitted reads of test-day files before the
run, and any other failure aborts it with no record. The whole-file hashing of test-day files happens only at step 3 of section 9; until
then the tool runs on discovery stand-ins, where the test-day metadata rows of `summary.json` and `windows.csv` pass through the parser
as section 1 says.

**Step 3's guard.** Before any test-day file is opened, the tool refuses unless all of these hold:
- it runs in the project repository, on `main`, with `LPX_ALLOW_DIRTY` unset, no git variable that redirects the repository or its index,
  and no index entry marked assume-unchanged or skip-worktree;
- the whole repository is clean, untracked files included;
- the output is `results/closeout_freeze/input_status.json`, which does not exist and was never committed. The record is committed straight
  after the run; from then on the guard refuses step 3. A record that is never committed leaves no git trace, so the owner's
  `DECISIONS.md` entry for step 3 is the record that it ran;
- `results/closeout_freeze/precheck_authorisation.json` is committed as it stands, names this step, names the code commit as a full SHA that
  is a strict ancestor of HEAD with no change since in the close-out's scope, and names the SHA-256 of every file in `PRECHECK_CODE` (the
  tool, `closeout.py`, the configurations it reads, `windows.csv`, `summary.json`, the schedule hashes) and of this protocol;
- every evidence file (section 9, step 3) is committed, passed, and records the code it ran on (its tree hashes), which equals the
  authorised commit's; a file that records no code is refused;
- the committed `docs/DECISIONS.md` holds exactly the line `APPROVED closeout pre-check step 3: <that record's SHA-256>`.

Stand-in runs never write under `results/closeout_freeze/`. The fit recomputation runs in a separate clone set up with `uv sync --frozen` by the
evidence script (which is published with the evidence); its record names the checkout, its origin and the code, but cannot itself prove that the
clone was fresh. It records
the clone and the code it ran.

This makes approval checkable and auditable. It does not prove who wrote the record, so it does not replace the owner's approval.

**Entry point** (`lpx/research/closeout.py`) calls the frozen functions:
- E001: `session_events`, `add_cells` and `summarize` with the forwarded edges, never `e001.run`;
- E002: `run_session` and `fee_overlay`;
- E003: `load_session`, `features`, `attach`, `forecast_rows`, `run_session` and `fee_overlay`;
- E004: its delivery, forecast, window and policy functions.

It checks the input-status record's provenance (section 1), then runs section 1's input checks and `verify_inputs` and
`verify_receipt_inputs` per session. A `load_session` exception is software or
environment, not an input result. Every guard runs before the first test-file read. Test mode requires the `--test-sessions` flag and accepts exactly `[splits].test`. Dry-run and rehearsal
modes refuse every test day and write to `results/closeout_dryrun/`, with their evidence in `results/closeout_dev/`.

**Analysis** (`lpx/research/closeout_analysis.py`) implements section 3 and Appendix A exactly. Before reading any table it verifies the freeze
record, the attempt and the trained-on sessions. It then requires the staged files to be **exactly** the expected set: the infrastructure
files (input status, relative tick, four experiment status files) and the tables of each experiment that ran to completion, with no
directory and no other file. Only `closeout.log`, `closeout_meta.json` and a Finder `.DS_Store` sit outside that set. The set must equal the metadata's listing, with
matching hashes and matching experiment outputs. Before the report is written, it asserts item by item that every row of Appendix A is
present with no required value null or empty, or marked *not run (reason)*, or carries its *not computed on test (reason)* marker. Inside a check row
a value may be undefined, so there it must be present; a check's label, rule and basis may never be null.

**Allow-list**, kept in the pinned `configs/closeout_v1.toml`. An allow-list is used so that unlisted keys cannot pass.
Frozen functions are called unchanged and only listed keys are kept, at leaf level: inside any listed block, only the leaf
keys in that file are written. They are `mean`, `defined`, `positive`, session and event counts, identifying keys (such as
`policy`, `fill_model`, `latency`, `fee_schedule`, `model`, `horizon_s`, `metric`, `spec`, `cell`, `pair`), the rows' `status`
label, `participation_differs`, participation ratios and shares, `not_testable_abstention`, the table means named by
`e003_analysis.DESCRIPTIVE`, and the forecast means.

The listed blocks are:
- `e001.summarize`: `sessions`, `events`, `mean_of_session_means`, `event_weighted_mean`, `sessions_positive`;
- `e002_analysis.scenario_table`, `paired_table`, `model_pairs_table`: means and session counts;
- `e003_analysis.h1`: `reported` only (`participation` is not called; section 3.4's descriptive results are computed
  directly from the net table);
- `e003_analysis.h3`: `normalised`, `other_schedules` (including `not_testable_abstention`) and the turnover ratio;
- `e003_analysis.descriptive`: `scenarios` and `forecasts` only;
- `e003_analysis.versus_e002`, `e004_analysis.descriptive_policy`, `p3_forecast_variants`, `window_descriptive`: means,
  `defined`, `positive`, participation ratios and shares.

Every interval, `eligible`, label and multiplicity key is excluded by not being listed. Descriptive t-intervals come from
frozen `e004_analysis.t_interval`. `e003_analysis.participation`, `e004_analysis.h4w`, `h4f` and `h40` are **not called on
test**: `closeout_analysis.py` produces their section 3 forms and values.

**Tests**, on synthetic tables:
- every label branch, qualifier and counterpart;
- undefined sessions, failed gates, ΣL ≤ 0 and the H1-F dependency;
- the y_view cells disagreeing;
- the mean-A row and sentence branches: mean A ≥ 0, and mean A < 0 with |ρ_A| below and at or above 0.01;
- the compromised flag;
- an experiment not confirmable (software), alone and through the E003 → E004 dependency;
- the fail-closed terminal state, and a failure in the analysis on each attempt;
- every ledger refusal;
- every classifier branch, by synthetic raises;
- recovery after a simulated death at each point: before the rename; between the rename and the `failed` commit; between
  appending any ledger line and its commit, with and without a stale `index.lock`; after `closeout_analysis.json`; after
  promotion and before the report; on attempt 3; and between `failed 3` and the `closed` event;
- partial outputs, hash mismatches (pinned files, inputs, attempt directories, metadata) and repeated-attempt refusals;
- a recursive check that every written key is on the allow-list;
- the ledger's order rules, the commits and `log_opened` events in the run history, and a session list with no valid session;
- the pre-check's reason codes, aborts, read scope, record contents and step 3's guard; the input-status record checks; the real runners'
  outputs against the expected staged set; and mutations of these checks (the mutation table is in the audit response record).

**Dry run** (`tools/closeout_dryrun.py`), three checks and two separate evidence runs:
1. **Fit tool against the frozen walk-forward fits.** `closeout_fits.py` with `before` set to each of s6…s15 reproduces
   `e003_models.json` exactly (all horizons, rv median, gate) and `e004_lambda.csv` exactly (λ, groups, training rows).
2. **Code path.** With those walk-forward artifacts loaded through the same loader the test mode uses, the entry point in
   dry-run mode reproduces every frozen discovery table:
   - E002's gross and net tables bit for bit;
   - every E003 table, including `e003_net_by_session.csv`, and `e003_models.json`;
   - every E004 table for the 10 evaluation sessions (forecast, calibration, degradation, λ, gross, net, windows);
   - E001's per-session means, sessions, events, `mean_of_session_means`, `sessions_positive` and edges, field by field,
     and its cells, sensitivities and proxy validation (means and counts).

   Every walked block (the allow-listed leaves of the listed blocks, compared in both directions) and every named value (check
   components, gates, shares, descriptive t-intervals, ρ values) equals the frozen JSON. The counts are reported by type, with the E002
   session series counted apart. `comparison_key_inventory.json` classifies every leaf of the four frozen JSONs, from the same lists the
   comparison uses, as walked, named, compared by E001's field and table checks, or excluded with a stated reason; an unexplained leaf fails.
3. **Test-mode rehearsal** on discovery stand-ins, under a non-test flag that refuses test days: fits on s1…s10, with
   s11…s15 standing in for the test days, a scratch ledger, and a synthetic freeze record in a temporary repository.
   - It uses the same context builder as test mode and differs only in the fit artifacts, the session list and those paths. The trained-on assertion and
     the freeze-record checks are exercised separately, against the synthetic record.
   - It runs staging, the E004 identity path against staging E003, the metadata, the analysis and the promotion.
   - It injects no failure.
   - Its outputs are discarded unread and are never reported. Only their schema is asserted, with the analysis's own staged-set and
     Appendix A checks. **It does not test label values.**

**Fault injection, separate from check 3,** on one stand-in session rather than the five, through the same runners and analysis: one failure of each
classifier kind, table-write failures (`ValueError` and `OSError`), an analysis failure, an unexpected staged file, a pinned input with other
bytes and a pinned input missing after the freeze (each an integrity failure, with the next attempt allowed on the same freeze record), a
pinned input changed under an experiment whose frozen code then raises (integrity, with no software record), a pinned data file changed after
the freeze (integrity, recorded before any read), three integrity failures in a row, real process deaths, and the fail-closed terminal path.
Unit tests cover a pins check that cannot run after a software exception (the software status and its no-retry record stay), an interrupt
during that check, and recovery recording `integrity_noted` when it promotes or closes with a changed data file.

**Pre-check scenarios, separate from check 3,** with the real tool on real stand-in sessions: injected `OSError`, `MemoryError`, `ValueError` and
`RuntimeError`, an absent data directory, an acceptance summary not from the run of record, each genuine input problem, an existing output, a refused
step 3, and a record of the files opened with every Parquet reader disabled.

## 8. Reporting and binding

`results/closeout/` holds:
- the tables, with a status label on every row or in the table's sidecar `<table>.status.json`;
- `closeout_analysis.json`, with status and attainability on every check;
- `CLOSEOUT_report.md`.

The report:
- **opens with the run history:** attempts, commits, renamed directories, sealed logs and any openings of them, undefined
  sessions and their reasons, and, separately, sessions with no valid unit in an experiment (which are not undefined);
- **lists every check and every reported-only item**, per experiment, in one table with discovery and test values side by
  side;
- gives not-confirmed, not-confirmable, reported-only and compromised items **the same prominence** as confirmed ones;
- is still issued if the close-out stops, with checks labelled as in section 6 and reported-only items
  labelled *not run (reason)*.

**Binding:**
- The memo and the website reproduce the full per-experiment label table.
- Any discovery finding they restate carries its test label, or "reported only / no confirmation claim".
- Only the check labels in section 3 may be called "confirmed". Every other test number is worded as a descriptive
  replication.
- A confirmed H4-W is worded "no material deterioration under the specified threshold", never as equivalence or proof of no
  effect.
- Hypothetical fee tiers are never presented as attainable performance.
- Each `E00x_report.md` gets an appended, dated pointer to its close-out labels. Its frozen body is unchanged.

## 9. Freeze sequence

1. Owner review and final approval of this revision. No critical or major protocol finding may remain unresolved.
2. The close-out files and `configs/closeout_v1.toml` are written and committed, then adversarially code-reviewed. No
   critical or major finding may remain unresolved.
3. The fit artifacts and every evidence file are committed: dry-run checks 1–3, the key inventory, the separate-clone fit recomputation,
   the fault injection and the pre-check scenarios, each passing on one code state. **Only then, on the owner's explicit approval,** the
   owner's authorisation record and `DECISIONS.md` entry are committed, the pre-check runs on the test days (section 7's guard, which
   checks the evidence), and its record is committed.
4. **Freeze commit.** It contains this protocol (status FROZEN) and the freeze record:
   - the parent commit SHA, the code fingerprint, and the tree hashes of `lpx`, `tools`, `tests` and `configs`;
   - the allowed-diff listing;
   - every pinned hash (section 2).
5. The freeze commit's SHA and the owner's authorisation, the exact line `APPROVED close-out freeze record: <freeze-record SHA-256>`, are
   committed to `DECISIONS.md`.
   Then come the first `authorised` record, the run, the analysis and the report.

## 10. Known limitations

- **Five sessions.** Every check is weak evidence (section 5). All sessions are first-of-month days.
- **Regime shift.** The test sessions come later and have a coarser relative tick (section 3.1).
- **Not blind.** Choosing the instrument and sample used acceptance metadata of the test days (`research_v1.toml`).
- **Limited BTCUSDT metadata exposure.** During the second-round re-review, an agent printed the first two rows of
  `results/acceptance_001/windows.csv`: BTCUSDT acceptance metadata dated 2026-06-01. BTCUSDT is not the research symbol, and
  these rows hold data-quality metadata. No SOLUSDT test-day row, no test-session data file and no outcome was read. This
  exposure is recorded for completeness and **is not evidence of SOLUSDT outcome leakage**.
- **Rules and test forms written after discovery and before any test outcome:**
  - E001's confirmation rule;
  - the 4-of-5 definedness rule, and an undefined session counting as a failure;
  - H1-T's §8 gates carried to test, and its literal reading;
  - the fixed δ_h;
  - the test forms of E004's stall-only qualifier and D2 flag, and the mean-A row replacing *UA harmful*;
  - the y_view pair as one row with a combined tally rule;
  - the exception classifier, and an unexpected software exception making the experiment not confirmable;
  - the fail-closed terminal state;
  - the allow-list;
  - the recovery step;
  - the ΣL ≤ 0 safeguard;
  - not computing `scenarios_by_period` and `forecasts_by_period`, although E003 §10 says "the same tables" (no number is
    lost).
- **"Run once" is qualified.** E002 §10.10, E003 §10 and `TRACKS.md` say the sessions are run once. This protocol allows up
  to 3 technical attempts that open the test files, under the conditions in section 6: failed outcomes uninspected, every
  attempt auditable, and retries unable to change research choices.
- **A software exception costs a whole experiment.** This removes a data-dependent selection, at the price of losing labels
  even when the cause is plumbing.
- **Limits of the ledger.** The repository has no remote. The guards detect an ordinary commit that cuts the ledger back, but
  a local history rewrite (`git reset`) followed by deleting the outputs would leave at most a reflog trace. So, after each
  ledger event, the owner records the ledger commit hash outside the repository, and an audit compares that note with HEAD.
- **Fits differ.** The test side uses all-15 fits; the discovery side used walk-forward fits.
- **Pre-check reads.** Hashing loads every byte of the test-day inputs and of `windows.csv`; `summary.json` is parsed whole and every row of
  `windows.csv` passes through the parser, though nothing else is kept. The state file's own provenance is confirmed at the run, not before
  the freeze (section 1).
- **A window in the software-failure record.** If the status file of a software-failed experiment cannot be written at all, the attempt fails
  as environment and that experiment may run again in the next attempt.
- **A lost or altered pinned file.** An input missing or modified after the freeze fails each attempt as an integrity failure; if it persists,
  the third failure closes the evaluation with no labels (sections 1 and 6). No restoration rule is defined for this close-out, and
  this is procedural: the check compares bytes with their pins, so a file absent during one attempt (an unmounted volume, say) and present
  with its pinned bytes at the next passes then. The failed attempt and its findings stay in the ledger and the report. A transient storage
  fault that leaves a pinned file absent costs an attempt.
- **Checks are at points, not continuous.** The pins are checked at the start, in the metadata step and on every failure; a change undone
  before the next check is not seen. A process death in the failure path is recorded by the recovery step as environment, without the
  session-input finding (recovery reads no test-day file); the next attempt's start check finds a persisting change again.
- **Orchestration is re-implemented.** The dry run establishes its equivalence. The marked blocks are compared line by line with the frozen
  source, except as section 6 states.
- **State-file provenance at the run.** By the owner's choice, an unparsable state-file footer is found only at the run, where it costs every
  attempt and closes the evaluation with no labels (section 1).
- **Inherited limitations.** Every experiment's own limitations apply. Every policy number is modeled, and E004's
  degradations are synthetic stress levels.

## 11. Owner choices (recommended by the owner, subject to final approval)

1. **H1-T:** the literal frozen rule is preserved, with sign and economic materiality reported separately.
2. **Participation:** the protocol-added seven-policy decision rule is removed. All seven policy results and the no-trade
   comparison remain as descriptive reporting.
3. **Exploratory tables:** the E001 exploratory tables and the E002 cap-free addendum are not run on the test sessions.
4. **After three failed attempts:** fail closed, with no partial confirmatory labels from an incomplete execution.
5. **Attempts:** up to three pre-authorised technical attempts, on the conditions in section 6.
6. **Software exceptions:** they make the affected experiment not confirmable, never a selective four-session confirmation.
   The pre-specified session input-status rules (section 1) and the integrity class (section 6) stay separate.
7. **H4-W wording:** the 1 bp rule stays one-sided, with the required interpretation "no material deterioration under the
   specified threshold".
8. **BTCUSDT metadata exposure:** documented in section 10 as not evidence of SOLUSDT outcome leakage.
9. **State-file footer check** (2026-11-03): it stays at the start of the run, not in the pre-check, so the pre-check reads no Parquet
   footer. Its consequences are in section 1.
10. **Pinned inputs after the freeze** (2026-11-03): no restoration rule for this close-out (the proposed one is rejected). A pinned input
    that is missing, modified or hash-mismatched after the freeze is an explicit, recorded integrity failure under the fail-closed rules,
    never a silent exclusion of the session (sections 1 and 6). This covers each session's four inputs, the fit artifacts and the pinned
    data files, at whatever point of an attempt the change is found.

## Appendix A — test-side outputs

`closeout.py` owns the session-level tables. `closeout_analysis.py` owns everything derived from them.

| Experiment | Discovery output | Test counterpart | Producer |
|---|---|---|---|
| E001 | primary metrics (`e001_discovery.json` `primary`; per-session CSV) | check (6); es reported only | `closeout.py` (via `summarize`) |
| E001 | cells (`e001_discovery_cells.csv`), `sensitivity_specs` (12), proxy validation, `descriptive` (secondary horizons, pre-state ages), `exclusions` | reported only | `closeout.py`, re-implementing the inline aggregation of `e001.run` |
| E001 | exploratory (`e001_exploratory*.csv`, `.json`) | not computed on test (exploratory by declaration; section 11) | — |
| E002 | `e002_gross_by_session.csv`, `e002_net_by_session.csv` | reported only (E002 §10.10) | `closeout.py` |
| E002 | `e002_h2.json`: scenario table, P1 − P0 paired table, fill-model paired differences, `descriptive_range_of_means` | reported only: means, defined counts, descriptive t-intervals on the scenario, paired and fill-model rows | `closeout_analysis.py` (allow-list; the range and t-intervals computed directly) |
| E002 | `condition_a_sign_reversal`, `condition_b_ranking_reversal`, `h2_supported_on_discovery`, `materiality`, `material_sensitivity` | not computed on test (interval rules needing ≥ 12 sessions; false by construction on 5) | — |
| E002 | `results/e002/addenda/cap_free_subset.json` | not computed on test (exploratory addendum; section 11); `rate_limited_daily` stays in the net table | — |
| E003 | `H1-F`, `H1-T`, gate activity | checks | `closeout_analysis.py` |
| E003 | `H1.reported` (6 quantities), with the VIP0 gross and fee split of each per-hour contrast | reported only | `closeout_analysis.py` (allow-list; the split computed directly) |
| E003 | `H3` decision | check | `closeout_analysis.py` |
| E003 | `H3.normalised`, turnover ratio, `other_schedules` (VIP0; VIP9, *hypothetical*; with abstention labels) | reported only | `closeout_analysis.py` (allow-list) |
| E003 | LP tier 4 notional shares of P3F[M2] and P4 relative to P3[M2] | reported only | `closeout_analysis.py` (computed directly) |
| E003 | `participation`: replaced by the 7 policies' results and the no-trade comparison (VIP0), with discovery net per hour, gross, maker-fee, taker-fee, turnover and sessions-with-trades columns | descriptive, no label or rule (section 3.4) | `closeout_analysis.py` (computed directly) |
| E003 | `descriptive.scenarios`, `descriptive.forecasts`, `P0_versus_E002` | reported only | `closeout_analysis.py` (allow-list) |
| E003 | `scenarios_by_period`, `forecasts_by_period` | not computed on test (discovery split; every test session would be labelled "train-late", and the numbers duplicate `scenarios` and `forecasts`) | — |
| E003 | per-session forecast, calibration, gross and net tables; `trades_without_receipt_time` | reported only | `closeout.py` |
| E003 | `e003_models.json` | not computed on test (forwarded fit artifact, section 2) | — |
| E004 | `primary` H4-W[P0], H4-W[P3]: gates, shares, stall-only, sign of mean D_W, sessions with D_W < 0 | checks; the rest reported | `closeout_analysis.py` |
| E004 | `secondary` H4-F: all cells and targets, projections, ρ_A minus projection, per-session A, L, A/L, leave-one-out ρ_A, mean-A row | the y_view row is a check; the rest reported only | `closeout_analysis.py` |
| E004 | H4-0, D2 flag | reported only | `closeout_analysis.py` |
| E004 | `descriptive` (policy D1-E and D1-S, P3 UA vs PL, window quality) | reported only | `closeout_analysis.py` (allow-list) |
| E004 | per-session forecast, calibration, degradation, λ, gross, net and window tables | reported only | `closeout.py` |
| All | test relative tick per session; descriptive t-intervals; run history; input status; run metadata (`closeout_meta.json`, experiment status files, E004 invariant counts) | reported | `closeout.py`, `closeout_analysis.py` |
