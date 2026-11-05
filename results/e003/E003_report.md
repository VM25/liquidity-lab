# E003 — Decision-time signals and quoting policies: discovery results

**Status labels.** Forecast skill is *observed*: forecasts and outcomes come from recorded data, with no own fills. Every policy number is *modeled historical replay*: our orders never existed, fills are inferred under stated queue, latency and fee assumptions, and no market impact is modeled.

**Sample.** 10 walk-forward evaluation sessions, s6–s15 (2025-08 → 2026-05): 19 episodes, 227.9 valid hours. Forecasts for session s_k were fitted only on sessions s1…s_{k−1}. The 5 test sessions remain sealed.

**Run.** Commit `f322ed7`, clean tree, under the specification frozen before any E003 outcome was computed (`docs/experiments/E003.md`; reviews in `docs/audits/2026-10-22_e003_*`).

**Acceptance checks before the run.**
- E002's frozen tables reproduce bit-for-bit at this revision on all 15 sessions (`results/e002/addenda/reproduction_all.json`).
- No run invariant failed: accounting identity, fills inside episodes, zero exchange-limit blocks, no orders during warm-up, forecasts attached by key.
- 36 of 25.7 million trades (2025-09-01, 2025-10-01) had no receipt time and were never used.

Raw outputs: `e003_*_by_session.csv`, `e003_models.json`. Pre-registered analysis: `e003_analysis.json`.

## Pre-registered decisions

Primary scenario: intermediate fill model, regional latency, VIP0 (10 / 10 bp). Intervals are 95% session-bootstrap intervals. "k/10" is the number of sessions where the value is positive. All three primary decisions are unchanged under the Bonferroni 98.33% intervals.

| Decision | Result | Label |
|---|---|---|
| **H1-F — forecast skill.** M2 R²_OS at 5 s vs the zero forecast | **+3.6%** [3.0, 4.4], 10/10 | **holds** |
| **H1-T — translation.** D = gross bp/notional of P3[M2] − placebo P3[−M2]; margin δ = 0.5 bp. Gate activity 50% and 58%, so the rule is active | **−0.12 bp** [−0.32, +0.07], 4/10 | **H1 supported** (skill without material per-fill translation) |
| **H3-risk** (hypothetical LP tier 4). P4 − P3F[M2] | 5-min ES −3.9 USDT [−5.4, −2.6]; max drawdown −69 USDT [−108, −38]; net/h +3.0 USDT [+1.6, +4.6] (non-inferiority margin −1.2); turnover ratio 0.78 | **H3 supported** (not mechanical) |
| **Participation** (VIP0; Bonferroni over 7 trading policies) | no trading policy has a net-per-hour interval above 0 | **abstention is the economically rational decision** |

## What the numbers say

### 1. The forecasts are real but small.

| | 1 s | 5 s | 30 s |
|---|---|---|---|
| M2 (8 decision-time features) R²_OS | 4.1% | 3.6% | 1.4% |
| M1 (touch imbalance only) R²_OS | 3.1% | 3.5% | 1.4% |

- At 5 s: IC 0.21, sign hit rate 65%. Skill is lower in the validation sessions (R²_OS 3.0%) than in train-late (4.2%).
- M2's gain over M1 at 5 s is +0.13 points [−0.01, +0.32], not significant. Touch imbalance carries almost all of the skill.

### 2. The forecast changes *how much* the policy trades, not *how good* its fills are. Both effects are reported because the pre-registered label covers only the second.

The table compares P0 (fixed quoting), P3[M2] (forecast-gated) and the placebo P3[−M2] (same gate, wrong direction) under the primary scenario at VIP0:

| | P0 | P3[M2] | P3[−M2] |
|---|---|---|---|
| Two-sided quote presence | 78% | 31% | 35% |
| Turnover (USDT/h) | 171,000 | 35,700 | 158,000 |
| Gross bp of notional | −1.51 | −1.71 | −1.58 |
| Own-fill 5 s markout (bp) | −1.37 | −1.72 | −1.44 |
| Net per hour (USDT) | −197 | **−42** | −184 |

- **Per fill.** The forecast-gated policy's fills are slightly *worse*, not better. It withdraws the side the forecast warns against, so the fills it still gets are disproportionately those where the forecast was wrong. That is adverse selection conditional on being filled. This is why D ≈ 0 and the pre-registered H1-T label is "supported".
- **Per hour.** The forecast avoids about 79% of P0's fills, and every fill loses money. P3[M2] − P0 is **+155 USDT/h** [84, 234], 10/10. The placebo comparison (D on net per hour) is +141 USDT/h [73, 216].
- **Why the placebo trades more.** Quote presence was matched (31% vs 35%), but turnover was not. The placebo keeps exactly the quote that the coming move will fill.
- **Better skill did not improve the ranking.** P3[M2] − P3[M1] is −0.07 bp per notional [−0.13, −0.02]. Net per hour is about equal.
- **The forecast does not make quoting profitable.** P3[M2] still loses before fees (gross −6.5 USDT/h, −1.7 bp), and its VIP0 net per hour is −42 [−56, −28], 0/10.

### 3. At the attainable fee schedule, the rational decision is not to trade.
- **VIP0 losses, primary scenario:** P0 −197, P1 −171, P3[M1] −42, P3[M2] −42 and P3[−M2] −184 USDT/h. All intervals are below zero, and so is every one of the 10 sessions.
- **Fee-aware policies abstain.** P3F and P4 do not trade at all, because a 10 bp maker fee is 8–17 ticks at the evaluation sessions' prices (about 83–172 USDT), while |forecast| averages 0.5 bp, about one tick or less. Their H3 contrast at VIP0 is therefore *not testable: abstention*.
- **No profitable session anywhere.** Across all 9 fill × latency scenarios, no trading policy has a single profitable session at VIP0. The best session-scenario is −5.8 USDT/h (P3[M1]).
- **Hypothetical schedules.**
  - VIP9 (1.1 / 2.3 bp): P3F and P4 trade only 9% and 7% of P3[M2]'s notional, and still lose (−1.1 and −0.7 USDT/h).
  - LP tier 4 (−0.8 bp rebate): every policy still loses on average; the smallest loss is P3[M1] at −3.4 USDT/h.

### 4. Risk controls help, but they do not create profit.
- **H3 (hypothetical LP tier 4).** P4 vs P3F:
  - Inventory: P4 halves time-averaged |inventory| (1.8 vs 5.5 SOL).
  - Tail risk: 5-minute expected shortfall falls from 6.5 to 2.6 USDT.
  - Drawdown: lower by 69 USDT.
  - Per hour: P4 loses 3.0 USDT/h less.
  - Robustness: these reductions hold per unit of turnover and with the same sign in all 9 scenarios (net per hour better in 8–10 of 10 sessions in each).
- **Caveat.** The fee-unaware P3[M2] loses less per hour than either fee-aware policy under the rebate (−3.7 vs P4 −8.8 USDT/h). The rebate loosens P3F/P4's gate, so they quote into forecasts that P3 avoids. The risk components improve on their own comparator, not on the best policy.
- **Inventory-aware P1 vs P0** (descriptive, VIP0): −171 vs −197 USDT/h, with time-averaged |inventory| 2.2 vs 5.4 SOL.

### 5. Order pacing removed E002's cap confound.
- Zero exchange-limit blocks in every run.
- Paced time share was 1–3% on average, and at most 9% (P0, primary scenario) or 13% (any scenario) in a single session.
- E003's P0 vs E002's P0 on the same sessions: +34 USDT/h [13, 57], from less turnover. Per notional the two are identical (−11.52 vs −11.54 bp).

## Robustness and caveats
- **Scenarios.**
  - D stays within ±0.35 bp in all 9 scenarios.
  - P3[M2] beats P0 per hour in all 9, by +88 to +315 USDT/h.
  - The H3 direction holds in all 9.
  - Optimistic fills and Tokyo latency enlarge the losses of the trading policies; they do not reverse any sign.
- **Inventory and liquidation.** Exchange-side |inventory| reached 10.99 SOL. Fills in flight can exceed the ±10 SOL limit, which applies to acknowledged inventory (as specified). In 24 VIP0 scenario-sessions, an episode-end liquidation went beyond the visible 10 levels; these are flagged in the tables.
- **Sample.** Ten sessions give limited power. Sign counts are reported next to every interval.
- **Forecast evaluation.** Target rows exclude moves beyond the episode end, which selects on the future path (disclosed in the spec).
- **Fill and fee gates.** P3's gate is a heuristic that ignores selection conditional on fill, and section 2 shows that this selection matters. P3F's and P4's fee gates overstate a rational quoter's participation.
- **Inherited limitations.** All E002 limitations apply: no market impact; modeled queue position; latency brackets are calibrations; VIP0 fees for 2025-03 → 2025-10 are inferred.

## Interpretation

Decision-time order-flow and imbalance features predict SOLUSDT mid moves a few seconds ahead out of sample: R²_OS of about 3.6% and a 65% sign hit rate at 5 s. That skill **does not make passive quoting profitable**, even before fees. Its whole economic value comes from **trading less**: the forecast steers the quoter away from fills that would have lost money. The fills that still happen are, if anything, more adversely selected.

At the only fee schedule this project can attain (VIP0), every fee-aware rule abstains, and every rule that trades loses in every session. **The economically rational decision is not to participate.**

Risk-aware quoting does cut inventory, drawdown and tail risk relative to an equally aggressive predictive quoter. But it cannot overcome adverse selection and fees.

These are statements about fixed, a-priori rules on 10 discovery sessions under modeled execution. They are not evidence that no passive strategy can be profitable, and they are not a verified trading result. Confirmation on the 5 sealed test sessions follows the protocol in `E003.md` §10, at the Stage 4 close-out.

---

**Close-out labels (pointer appended 2026-11-04; the body above is the frozen discovery report, unchanged).** The final held-out evaluation ran once on the five test sessions under `docs/experiments/FINAL_EVALUATION.md` (revision 9, frozen; attempt 1, ledger `completed 1` = `2447d2a`). This experiment's test labels are in `results/closeout/CLOSEOUT_report.md`, section E003: 3 of 3 confirmed (H1-F, H1-T, H3; each decided by the sign or side of a mean, the weakest confirmations in the protocol; H3 under hypothetical LP tier 4 fees). The seven-policy VIP0 results are descriptive. Labels are point-estimate checks on five sessions (protocol section 5); a tally is not a count of independent replications.
