# Research Specification

## Core question
Can accurate short-horizon signals fail to generate executable profits, and can execution-aware, inventory-aware decisions improve the resulting risk/return trade-offs?

## Falsifiable hypotheses
- **H1 / Alpha:** Better out-of-sample price prediction does **not necessarily** imply better after-cost simulated market-making performance.
- **H2 / Execution:** Policy rankings and simulated P&L can change materially across plausible queue/fill and latency assumptions.
- **H3 / Inventory:** Risk-aware quoting may improve downside exposure or risk-adjusted outcomes relative to more aggressive predictive quoting.
- **H4 / Information:** When information degrades, an uncertainty-aware policy may outperform an otherwise identical policy that ignores degraded-data signals.

## Experiments (in dependency order)
1. **E001 — Observed markouts:** On accepted trade/book windows, study signed post-trade midpoint changes at preselected 1s/5s/30s horizons. No hypothetical order fills.
2. **E002 — Execution sensitivity:** Same policies/market paths, different explicit queue, latency, cancellation, fee assumptions.
3. **E003 — Quoting policies:** P0 fixed; P1 inventory skew; P2 adaptive spread/size; P3 alpha aware; P4 execution- and risk-aware. (As frozen in `experiments/E003.md`: P2 deferred, a placebo and a fee-aware P3F added; see DECISIONS 2026-10-22.)
4. **E004 — Information robustness:** Withhold/delay/noise selected *features* against an accepted reference path, retaining hidden records only for evaluation.

## Methods and comparison rules
- Source-side trade aggressor labels must be verified; otherwise mark inferred labels and their uncertainty.
- Define horizons, event filters, labeling, primary metrics, and exclusion rules **before** looking at held-out outcomes.
- Chronological training/validation/test splits; purge or embargo overlapping forecast labels where necessary.
- Use matched accepted sessions, cost models, position limits, and comparable risk budgets across policies.
- Benchmark simple order-flow/statistical models before gradient boosting; advanced ML is earned, not assumed.
- Report confidence/uncertainty at suitable session or block granularity; correlated events are not independent trials.
- Disclose regime coverage, sampling biases (e.g., first-of-month days), and multiple-testing limits.

## Primary evidence
- **Observed:** conditional signed mid-price markouts, spread/depth/imbalance diagnostics, predictive calibration.
- **Modeled:** after-cost marked wealth, trade participation, inventory exposure, adverse-selection markouts, drawdown, execution sensitivity.
- **Risk:** downside P&L and tail metrics only if sample size/horizon justify them; otherwise report limits honestly.
- Negative or inconclusive results count as valid findings; never target a predetermined shocking result.
