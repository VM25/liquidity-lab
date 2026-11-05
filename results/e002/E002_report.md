# E002 — Execution sensitivity: discovery results

**Status of every number: modeled historical replay.** Our orders never existed. Fills are inferred under the stated queue, latency and fee assumptions, and no market impact is modeled. Sample: 15 discovery sessions (10 train, 5 validation), 29 episodes, 347.5 valid hours. The 5 test sessions remain sealed. The run was made from commit `be3fe77`, a clean tree, under the specification frozen and amended *before* this run (`docs/experiments/E002.md`, §10). Raw outputs: `e002_gross_by_session.csv` and `e002_net_by_session.csv`. Pre-registered analysis: `e002_h2.json`.

## Pre-registered H2 decision (default fee schedule VIP0, 10 bp maker / 10 bp taker)

**H2 is not supported on discovery sessions.** There is no sign reversal across fill-model × latency scenarios (condition a), and no reversal of the P1 − P0 ranking (condition b). **No sensitivity is material:** paired fill-model differences are 0.16–0.55 bp, all below the pre-registered 1.0 bp threshold, although every one of their intervals excludes zero. All 18 scenarios are eligible: every session has fills.

| net bp of traded notional, liquidation-adjusted (mean of 15 session means [95% session-bootstrap CI]) | Tokyo-hosted | regional | distant |
|---|---|---|---|
| P0 conservative | −11.87 [−11.99, −11.75] | −11.65 [−11.76, −11.54] | −11.63 [−11.74, −11.51] |
| P0 intermediate | −11.69 [−11.82, −11.58] | −11.49 [−11.60, −11.39] | −11.44 [−11.56, −11.33] |
| P0 optimistic | −11.37 [−11.47, −11.29] | −11.16 [−11.24, −11.08] | −11.10 [−11.19, −11.00] |
| P1 conservative | −11.79 [−11.90, −11.69] | −11.64 [−11.74, −11.56] | −11.62 [−11.71, −11.53] |
| P1 intermediate | −11.61 [−11.72, −11.51] | −11.46 [−11.56, −11.37] | −11.42 [−11.52, −11.33] |
| P1 optimistic | −11.30 [−11.39, −11.21] | −11.14 [−11.22, −11.06] | −11.07 [−11.16, −10.98] |

P1 − P0 (paired): between +0.01 and +0.08 bp. The interval excludes zero (P1 better) in 6 of 9 scenarios, but the difference is economically negligible.

## Descriptive decomposition (not part of the H2 decision)

- **Before fees the policies still lose.** Gross liquidation-adjusted P&L is −1.1 to −1.9 bp of notional across the primary models. That splits into a spread capture (edge vs the mid before the fill) of only +0.2 to +0.4 bp and inventory revaluation of −1.5 to −2.2 bp. Own-fill 30 s markouts (rs/2 on our own fills) are −1.1 to −1.9 bp. This matches E001's −1.10 bp per unit of hit volume: the modeled fills are adversely selected about as much as the average touch liquidity.
- **Fees dominate.** Holding fills fixed, net bp for P0 (Tokyo-hosted) by schedule is: VIP0 −11.4 to −11.9; VIP0+BNB −8.9 to −9.4; VIP9 −2.5 to −3.0; LP tier 1 −1.4 to −1.9; LP tier 4 (−0.8 bp rebate, a hypothetical upper bound) −0.6 to −1.1. **No fee schedule and no fill model produces a positive mean**, including the hypothetical rebate tiers.
- **Latency.** Lower latency means more fills and slightly *worse* bp per notional (Tokyo-hosted is about 0.2 bp below distant). The fills it adds are more adverse. Per hour, losses scale with volume (P0 VIP0: −217 to −471 USDT per valid hour).
- **Risk.** Max |inventory| reached the ±10 SOL limit under P0 and stayed within about 5 SOL under P1. Time-averaged |inventory| was about 5.5 SOL (P0) and 2.2 SOL (P1). One P0 episode ran past the visible book at liquidation and is flagged.
- **Naive reference** (never a result): gross −0.3 to −0.7 bp with roughly double the volume. This shows how much a touch-fill rule flatters a strategy.

## Caveats that bound these results
- **The daily order cap binds in some optimistic and naive scenarios.** The P0 policy cancel-replaces on every touch change, and 200,000 orders per day is reached in 6 of 90 optimistic scenario-sessions and 20 of 90 naive ones (5 distinct days); conservative and intermediate never reach it. In those sessions quoting stops for the rest of the day, so optimistic-vs-conservative comparisons there are partly confounded with when the cap binds. The direction of the decision is unaffected: all intervals are far from zero and all model differences are below 1 bp.
- With reactive policies the fill models are assumption brackets, not per-session bounds (§10.13).
- No market impact; queue position modeled, not observed; latency brackets are calibrations; VIP0 fees for 2025-03 → 2025-10 are inferred (assumptions evidence).
- Discovery only. Confirmation on the test sessions requires the guarded close-out entry point (§10.10, §10.13), which is not yet implemented.

## Interpretation
On these sessions, simple touch-quoting (P0) and its inventory-withdrawal variant (P1) lose money under every pre-registered fill, latency and fee assumption. The loss is about one tick of adverse selection before fees, plus the fee. The execution assumptions move the result by less than the pre-registered materiality threshold. **The fee schedule and adverse selection decide the outcome, not the queue model.** This is a statement about two fixed baseline policies under modeled execution. It is not evidence that no passive policy can be profitable, and it is not a verified trading result.

---

**Close-out labels (pointer appended 2026-11-04; the body above is the frozen discovery report, unchanged).** The final held-out evaluation ran once on the five test sessions under `docs/experiments/FINAL_EVALUATION.md` (revision 9, frozen; attempt 1, ledger `completed 1` = `2447d2a`). This experiment's test labels are in `results/closeout/CLOSEOUT_report.md`, section E002: no confirmation claim (E002 §10.10): the test sessions report the same tables only. Labels are point-estimate checks on five sessions (protocol section 5); a tally is not a count of independent replications.
