# E004 — Information robustness: discovery results

**Status labels.**
- D0 and REF forecasts: *observed*.
- Degraded-cell forecasts: *stress test*. The degradations are synthetic changes to observed records.
- REF policy rows: *modeled historical replay*.
- Degraded-cell policy rows and windows: *modeled historical replay under stress test*.
- Degradation statistics: *synthetic*.
- Fee schedules other than VIP0: *hypothetical*.

Our orders never existed. Fills are inferred under the stated queue and latency assumptions, with no market impact.

**Sample.** 10 walk-forward evaluation sessions, s6–s15 (2025-08 → 2026-05). Every fit for s_k used s1…s_{k−1} only. The 5
test sessions remain sealed.

**Run.** Commit `5c9d93e`, clean tree, 8,519 s. Specification frozen at `b967c69`, before any E004 outcome; schedule-hash
list committed at `dfad3d0`, before the code review. Adversarial code review: 0 critical findings, 2 distinct major
findings fixed (`docs/audits/2026-10-28_e004_code_review.md`).

**Acceptance checks before the run** (`results/e004_dev/`):
- E002 reproduced bit for bit in all 15 sessions.
- E003 reproduced in every evaluation session: walk-forward models, REF forecasts, calibration deciles and REF policy rows.
  One full E003 session (100 rows, every column) also reproduced.
- The s1 development check passed every invariant.

**Inside the run:**
- 840 schedules were verified against the committed hashes.
- 60 REF policy rows matched E003's frozen rows.
- In 20 jobs, D0 through the view path was bit-identical to REF.
- States, trades and view lists were never mutated.

Raw tables: `e004_*_by_session.csv`, `e004_lambda.csv`, `e004_calibration.csv`. Pre-registered analysis: `e004_analysis.json`.

## Pre-registered decisions

**Setting.** Primary family: D1-E (connection drops; about 4.5% of time stalled), intermediate fill model, regional
latency, N run, 3 replicates.

**Contrast.** D_W = q(W_P) − q(W_U): the fee-free 5-second mark-to-mid per notional of fills in randomly timed,
duty-matched windows, minus that of fills in staleness-timed windows (age ≥ τ = 650 ms). Margin δ = 1 bp. Intervals are
95% session-bootstrap intervals. "k/10" counts the sessions where D_W > 0.

| Decision | D_W (bp) | Gates | Label |
|---|---|---|---|
| **H4-W[P0]** | **−0.04** [−0.11, +0.02]; 4/10 positive; below δ in 10/10 | W_U share 2.9%; W_P–W_U overlap 2.9%; ≥ 735 distinct orders per window and session | **immaterial selection (< δ)**; the interval includes 0 |
| **H4-W[P3[M2]]** | **−0.16** [−0.30, +0.003]; 2/10 positive; below δ in 10/10 | same windows; ≥ 202 orders | **immaterial selection (< δ)**; the interval includes 0 |

- **Robustness.** Both labels are unchanged under the Bonferroni 97.5% intervals and under paired t-intervals.
- **Stall-only check.** It gives the same label (P0 −0.05 [−0.11, +0.01]; P3 −0.17 [−0.30, −0.03]), so the labels are not
  *sensitive to natural staleness*.
- **Windows.** 94% of W_U time and 98–99% of W_U^x fills come from scheduled stalls. One episode (2025-09-01, one
  replicate) could not be rotated without cutting a spell at the seam; it was excluded and counted, as pre-registered.

| Secondary decision | Result | Label | Projection (section 0) |
|---|---|---|---|
| **H4-F, D1-S, target y_k** (book stalls, about 17%) | L = 0.98 pp [0.73, 1.25]; ρ_A = 0.57 [0.39, 0.75]; ρ_B = 0.16 [0.035, 0.32] | **inconclusive** (ρ_B's lower bound is below 0.10) | L ≈ 0.75, ρ_A ≈ 0.37, ρ_B ≈ 0.31: *supported* expected. Observed ρ_A is 0.20 above the projection, ρ_B below it. |
| H4-F, D1-S, target y_view | L = 0.83 pp; ρ_A = −0.01 [−0.02, +0.005] | **not supported** | ρ_A ≈ 0, as projected |
| H4-F, D3 (late, not lost) | same as D1-S to two decimals | y_k **inconclusive**; y_view **not supported** | equal to D1-S, as projected |
| H4-F, D1-E | L = 0.16 pp (< 0.20) | **not testable** | expected not testable |
| H4-F, D4 (size noise) | L = 0.25 pp [0.13, 0.39]; ρ_A = 0.42 [0.13, 0.55]; ρ_B = 0.04 | **inconclusive** (both targets) | none |
| H4-F, D2 (negative control) | L = 0.004 pp | **not testable**, as required (no *pending review* flag) | expected not testable |
| **H4-0**, do-no-harm on clean rows | UA-λ (trained on D1-S) − REF = +0.03 pp [+0.001, +0.065] | **harmless** | harmless expected |

D1-S1 and D1-S3, the dose-response cells, are descriptive and unlabelled:
- **y_k:** ρ_A ≈ 0.52 and 0.57; L = 0.06 and 2.75 pp.
- **y_view:** ρ_A ≈ 0 in both.

**No label rewards abstention, and no decision uses net per hour.**

## What the numbers say

### 1. Stale information did not select worse fills. The expected mechanical effect was not there.

The specification expected D_W > 0 mechanically: resting orders left at stale prices should be filled by trades that go
through them. In this sample the effect is not there, at any size. The fills that arrive while the participant's view is
stale are about as good as average.

| P0, D1-E, intermediate × regional | 5 s mark-to-mid (bp) |
|---|---|
| fills in staleness windows (q(W_U)) | −1.34 |
| fills in randomly timed windows (q(W_P)) | −1.38 |
| all N fills | −1.44 |

- **Sign across settings.** The sign is the same everywhere, though these runs are descriptive (1 replicate for the other
  fill models): conservative −0.08, optimistic −0.10, D1-S −0.14 (0/10 positive). For P3[M2]: −0.41, −0.31 and −0.32.
- **Fewer fills, same quality.** P0 is filled less often in staleness windows than in placebo windows: 127k against 176k
  fills pooled over the 3 replicates. Quotes left behind by a move are not filled, quotes the move runs into are. Per
  notional, quality is unchanged.
- **Session spread.** Between sessions the spread is small (σ_D ≈ 0.1 bp for P0). The interval is narrow and excludes
  any effect above 0.02 bp.

### 2. Withdrawing when stale is no better than withdrawing at random. Withdrawing at all costs a little per fill.

These comparisons are realised and descriptive: D1-E, primary scenario, pooled over replicates, VIP0 unless stated.

| P0 | U − P | U − N | P − N |
|---|---|---|---|
| Gross bp of notional | −0.01 [−0.03, 0.00] | −0.06 [−0.10, −0.02] | −0.04 [−0.08, −0.02] |
| 5 s mark-to-mid of all fills (bp) | 0.00 [−0.003, +0.003] | −0.05 | −0.05 |
| Notional ratio | 1.006 | 0.94 | 0.93 |
| Net per hour, VIP0 (USDT) | −1.2 [−1.8, −0.7] | +6.8 [+5.4, +8.4] | +8.0 [+6.2, +10.0] |
| of which mechanical fee saving | −1.0 | +6.3 | +7.2 |
| Net per hour, LP tier 4 (*hypothetical*) | −0.16 [−0.41, +0.03] | +0.03 | +0.20 |

- **U vs P.** Participation is matched (ratios 0.99–1.01), so the comparison is clean, and it shows no gain from
  timing withdrawal by staleness.
- **Withdrawal itself.** Both U and P have slightly worse fills per notional than N. One unverified explanation: after
  a withdrawal, re-quoting sends the order to the back of the queue, and a late queue position is filled more adversely
  (the queue-position mechanism of Garriott, van Kervel and Zoican, 2025).
- **Net per hour.** At VIP0, every net gain from withdrawing is almost entirely the mechanical fee saving on lower
  turnover. This is the same activity confound that E002, E003 and A1 found.
- **P3[M2].** It behaves the same way: U − P gross −0.02 [−0.07, +0.04], participation matched.

### 3. Staleness-aware recalibration improves the forecast of the true price, not of the price the participant quotes against.

| D1-S, mean R²_OS (pp) | REF (clean) | NV (naive) | RF-λ (one λ) | PL-λ (placebo buckets) | UA-λ (age buckets) |
|---|---|---|---|---|---|
| y_k (true current mid) | 3.64 | 2.66 | 3.07 | 3.06 | 3.22 |
| y_view (the participant's mid) | 4.38 | 3.55 | 3.54 | 3.54 | 3.55 |

- **y_k.** The NV forecast loses about 1 pp to staleness. Age-bucket shrinkage recovers 57% of that.
  - Most of the recovery, 0.41 of the 0.56 pp, comes from a single global shrinkage factor. The placebo-bucket model
    gets the same. The age-specific part adds 0.16 pp, which fails the pre-registered ρ_B > 0.10 lower bound.
  - That is why the label is *inconclusive*, not *supported*.
- **y_view.** Against the mid the participant prices off, which is what its quotes actually face, the naive forecast is
  already about optimal. Recalibration adds nothing (ρ_A ≈ 0), as projected.
- **Interpretation.** The y_k result is largely by construction (section 0), because imbalance has a short memory.
- **Descriptive P3 run.** A P3[M2] run on the UA-λ forecast (D1-S) quotes 9% less than the same rule on the PL-λ
  forecast, with gross −0.04 bp [−0.09, −0.003] per notional. Its +3.2 USDT/h at VIP0 is a participation change, not a
  quality gain.

### 4. Bottom line for H4

In this sample, a participant whose information is stale (synthetic connection drops and feed stalls on real books)
does not get worse fills during staleness. An uncertainty-aware rule that withdraws when its information is stale does
no better than the same amount of withdrawal at random times. Staleness-aware forecast shrinkage helps only against a
target the participant does not trade against.

The pre-registered labels are:
- H4-W: *immaterial selection* (both bases);
- H4-F: *inconclusive* (y_k) and *not supported* (y_view);
- H4-0: *harmless*.

## Limitations
- **Stress levels, not observed rates.** The degradations are synthetic. D1-E's 120 drops per hour are about 7,000×
  the observed reconnect rate; only the drop durations are empirical. Stalls are assumed independent of the market.
- **Unaffected channels.** Order entry and acknowledgements are assumed unaffected. During a drop, the participant still
  receives its own fills.
- **Model risk in fills.** Fill quality is modeled: queue position and fills are inferred, not observed. The negative
  D_W holds under all three fill models in the descriptive runs, but every one of them is a model.
- **Inference.** There are 10 sessions; percentile intervals can under-cover. The analysis is not blind (section 0 of the
  specification).
- **Scope.** Only P0 and P3[M2] were tested. A rule that re-prices aggressively on resync was not.
- **Earlier limitations.** All E002 and E003 limitations apply. Net results at every fee level remain negative.

**Next.** Section 8's forward set is fixed: models, cells, policies and seeds, with test-day schedules pinned by the
committed hashes. The test sessions open only under the separate final-evaluation protocol, after it is frozen.

---

**Close-out labels (pointer appended 2026-11-04; the body above is the frozen discovery report, unchanged).** The final held-out evaluation ran once on the five test sessions under `docs/experiments/FINAL_EVALUATION.md` (revision 9, frozen; attempt 1, ledger `completed 1` = `2447d2a`). This experiment's test labels are in `results/closeout/CLOSEOUT_report.md`, section E004: H4-W 2 of 2 confirmed (P0 and P3[M2]): no material deterioration under the specified threshold (one-sided, 1 bp). The secondary H4-F y_view row is confirmed, i.e. its discovery decision *not supported* holds, which is largely implied by the target choice. Labels are point-estimate checks on five sessions (protocol section 5); a tally is not a count of independent replications.
