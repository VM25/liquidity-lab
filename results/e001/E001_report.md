# E001 — Observed post-trade markouts (discovery sessions)

<!-- BEGIN:meta -->
E001 discovery run 2026-10-20T00:59:36+00:00 · git `c034d6bc6adb` · code fingerprint `7a976639b03c1db2` · sessions: 15 (train, validation) · windows.csv sha256 `d543187a263d2829` · acceptance run `50807dc1219d`
<!-- END:meta -->

**Status label: observed** (exchange trades and replayed vendor-captured book states; no hypothetical orders, fills or P&L).
**Scope:** the 15 *discovery* sessions (10 train + 5 validation). The 5 test sessions (2026-06-01 → 2026-10-01) are sealed: the code refuses to evaluate them, and no outcome on them has been computed. **Inferential status:** the primary specification is *pre-specified* — fixed before any E001 outcome existed (`configs/research_v1.toml`, frozen 2026-10-14, amended 2026-10-19 twice, both times before any outcome) — but it is evaluated here on discovery sessions, so it is **not a confirmation**. Every other specification is *exploratory* robustness and is never used to redefine the primary. Confirmation is the single run on the 5 test sessions at the Stage 4 close-out, with identical code.

## Design (as specified)

| Element | Definition |
|---|---|
| Instrument / data | Binance spot SOLUSDT; book = Stage 1 verified states (Tardis capture, replayed); trades = Binance Vision exchange archive (complete trade ids, exchange aggressor flag) |
| Event (primary) | **timestamp-side cluster**: exchange trades sharing trade time T and aggressor side. Binance publishes no parent-order id, so a cluster is not a verified aggressive order (it can merge simultaneous orders). Sensitivity: every trade id as its own event. |
| Information clock (primary) | **retrospective exchange-time conditioning**: pre-event book = last state with exchange time E < T; outcome = last state with E ≤ T + h. This is the book as the exchange had published it, *not* the information a live participant held at T. |
| Availability-safe variants | pre-event book = last state the Tardis recorder (Tokyo) had *received* d ms before T (receipt + d < T); d ∈ {0, 50, 200} ms. Only the conditioning information changes: outcomes are always the exchange-clock state at exactly T + h. |
| Metrics (bp of pre-event mid m0) | mo(h) = s (m(T+h) − m0)/m0 · es = 2 s (P − m0)/m0 · rs(h) = es − 2 mo(h); s = +1 buyer-initiated, P = event VWAP; h ∈ {1, 5, 30} s |
| Validity | pre-event and every primary-horizon outcome *record* must carry a proven uncrossed touch inside an accepted joint window, and T, T + h and the records must lie in the same window — required for all of h = 1, 5, 30 s (one common event set). Windows end at every vendor reconnect. |
| Inference | session = unit; mean of session means with a 10,000-draw session bootstrap (95% percentile); per-session 5-minute block bootstrap |
| Conditioning cells | size terciles (edges from train sessions only); touch imbalance signed by s; `qty_ge_touch` (event size ≥ pre-event touch size on the side hit — a **proxy**, not observed queue depletion) |

## Results

### Primary specification

<!-- BEGIN:primary -->
| metric (bp) | mean of session means [95% session-bootstrap CI] | event-weighted mean | sessions > 0 | events |
|---|---|---|---|---|
| es | +1.276 [+1.135, +1.434] | +1.298 | 15/15 | 4,120,728 |
| mo_1s | +0.985 [+0.859, +1.107] | +1.051 | 15/15 | 4,120,728 |
| mo_5s | +1.101 [+0.971, +1.230] | +1.165 | 15/15 | 4,120,728 |
| mo_30s | +1.167 [+1.052, +1.289] | +1.211 | 15/15 | 4,120,728 |
| rs_1s | -0.695 [-0.884, -0.484] | -0.804 | 1/15 | 4,120,728 |
| rs_5s | -0.926 [-1.115, -0.715] | -1.032 | 1/15 | 4,120,728 |
| rs_30s | -1.059 [-1.237, -0.859] | -1.124 | 0/15 | 4,120,728 |
<!-- END:primary -->

Event accounting (primary specification):

<!-- BEGIN:exclusions -->
| reason | events |
|---|---|
| included | 4,120,728 |
| t_outside_windows | 176,450 |
| horizon_leaves_window | 13,194 |
| horizon_beyond_session_data | 562 |
<!-- END:exclusions -->

### Per session

<!-- BEGIN:per_session -->
| session | split | eligible (post hoc) | events | es | mo 1 s | mo 30 s | rs 30 s |
|---|---|---|---|---|---|---|---|
| 2025-03-01 | train | yes | 321,388 | +1.288 [+1.106, +1.448] | +1.165 [+1.049, +1.278] | +1.225 [+0.884, +1.537] | -1.161 [-1.688, -0.590] |
| 2025-04-01 | train | yes | 264,069 | +1.207 [+1.138, +1.280] | +1.057 [+0.973, +1.140] | +1.102 [+0.834, +1.325] | -0.997 [-1.439, -0.492] |
| 2025-05-01 | train | yes | 254,833 | +0.982 [+0.928, +1.042] | +0.700 [+0.629, +0.785] | +0.811 [+0.711, +0.911] | -0.639 [-0.841, -0.455] |
| 2025-06-01 | train | yes | 234,871 | +1.143 [+1.098, +1.186] | +0.921 [+0.872, +0.973] | +1.171 [+1.049, +1.299] | -1.199 [-1.443, -0.965] |
| 2025-07-01 | train | yes | 237,902 | +1.056 [+1.001, +1.115] | +0.869 [+0.776, +0.968] | +1.102 [+0.910, +1.324] | -1.148 [-1.581, -0.747] |
| 2025-08-01 | train | yes | 382,465 | +1.157 [+1.104, +1.212] | +1.231 [+1.165, +1.295] | +1.472 [+1.190, +1.814] | -1.786 [-2.383, -1.227] |
| 2025-09-01 | train | yes | 521,138 | +1.273 [+1.206, +1.334] | +1.103 [+1.043, +1.174] | +1.205 [+1.040, +1.401] | -1.138 [-1.473, -0.814] |
| 2025-10-01 | train | no | 232,367 | +1.014 [+0.918, +1.112] | +1.032 [+0.923, +1.151] | +1.160 [+0.964, +1.364] | -1.307 [-1.660, -0.979] |
| 2025-11-01 | train | yes | 162,780 | +0.797 [+0.710, +0.860] | +0.675 [+0.628, +0.726] | +0.943 [+0.852, +1.037] | -1.090 [-1.310, -0.901] |
| 2025-12-01 | train | yes | 379,822 | +1.287 [+1.182, +1.369] | +1.105 [+1.022, +1.189] | +1.095 [+0.900, +1.300] | -0.902 [-1.383, -0.490] |
| 2026-01-01 | validation | yes | 131,530 | +1.157 [+1.100, +1.224] | +0.601 [+0.527, +0.692] | +1.061 [+0.914, +1.218] | -0.964 [-1.263, -0.671] |
| 2026-02-01 | validation | yes | 358,975 | +1.707 [+1.634, +1.778] | +1.324 [+1.257, +1.386] | +1.515 [+1.283, +1.737] | -1.323 [-1.789, -0.861] |
| 2026-03-01 | validation | yes | 278,833 | +1.914 [+1.855, +1.975] | +1.360 [+1.284, +1.435] | +1.660 [+1.408, +1.937] | -1.406 [-1.935, -0.888] |
| 2026-04-01 | validation | yes | 247,561 | +1.731 [+1.674, +1.795] | +1.064 [+1.001, +1.132] | +1.213 [+0.960, +1.445] | -0.694 [-1.185, -0.168] |
| 2026-05-01 | validation | yes | 112,194 | +1.422 [+1.371, +1.481] | +0.572 [+0.506, +0.639] | +0.773 [+0.679, +0.871] | -0.124 [-0.296, +0.041] |
<!-- END:per_session -->

### Conditioning cells (primary specification)

<!-- BEGIN:cells -->
| cell | events | es | mo 1 s | mo 30 s | rs 30 s |
|---|---|---|---|---|---|
| size=L | 1,456,489 | +1.602 [+1.441, +1.777] | +1.577 [+1.440, +1.704] | +1.778 [+1.643, +1.933] | -1.953 [-2.180, -1.722] |
| size=M | 1,393,365 | +1.100 [+0.942, +1.284] | +0.746 [+0.606, +0.895] | +0.937 [+0.801, +1.078] | -0.775 [-0.973, -0.550] |
| size=S | 1,270,874 | +1.038 [+0.923, +1.153] | +0.529 [+0.413, +0.641] | +0.660 [+0.535, +0.797] | -0.282 [-0.558, -0.014] |
| touch_imbalance=against | 905,189 | +0.886 [+0.762, +1.017] | +0.308 [+0.225, +0.395] | +0.127 [+0.004, +0.278] | +0.631 [+0.380, +0.886] |
| touch_imbalance=neutral | 954,175 | +1.206 [+1.060, +1.365] | +0.795 [+0.676, +0.910] | +0.931 [+0.789, +1.083] | -0.656 [-0.956, -0.398] |
| touch_imbalance=with | 2,261,364 | +1.465 [+1.302, +1.644] | +1.348 [+1.193, +1.493] | +1.710 [+1.595, +1.834] | -1.956 [-2.118, -1.788] |
| qty_ge_touch=False | 3,667,002 | +1.235 [+1.098, +1.384] | +0.896 [+0.782, +1.008] | +1.071 [+0.964, +1.180] | -0.907 [-1.060, -0.734] |
| qty_ge_touch=True | 453,726 | +1.662 [+1.434, +1.917] | +1.816 [+1.655, +1.985] | +2.035 [+1.860, +2.234] | -2.409 [-2.663, -2.140] |
<!-- END:cells -->

### Robustness (exploratory)

<!-- BEGIN:sensitivity -->
| analysis | specification | events | es | mo 1 s | mo 5 s | mo 30 s | rs 30 s |
|---|---|---|---|---|---|---|---|
| pre-specified primary | primary (cluster · exchange clock · baseline windows · all sessions) | 4,120,728 | +1.276 [+1.135, +1.434] | +0.985 [+0.859, +1.107] | +1.101 [+0.971, +1.230] | +1.167 [+1.052, +1.289] | -1.059 [-1.237, -0.859] |
| exploratory | unit=trade | 24,522,089 | +1.557 [+1.396, +1.728] | +1.595 [+1.463, +1.734] | +1.761 [+1.628, +1.899] | +1.801 [+1.671, +1.949] | -2.046 [-2.216, -1.878] |
| exploratory | timing=receipt+0ms | 4,120,722 | +1.295 [+1.153, +1.445] | +0.995 [+0.870, +1.119] | +1.110 [+0.980, +1.235] | +1.177 [+1.061, +1.296] | -1.059 [-1.234, -0.863] |
| exploratory | timing=receipt+50ms | 4,120,688 | +1.410 [+1.247, +1.587] | +1.052 [+0.918, +1.186] | +1.168 [+1.028, +1.308] | +1.234 [+1.105, +1.369] | -1.058 [-1.237, -0.867] |
| exploratory | timing=receipt+200ms | 4,120,561 | +1.536 [+1.355, +1.735] | +1.115 [+0.964, +1.260] | +1.231 [+1.081, +1.385] | +1.297 [+1.155, +1.446] | -1.058 [-1.235, -0.864] |
| exploratory | eligible_sessions_only(posthoc) | 3,888,361 | +1.294 [+1.149, +1.456] | +0.982 [+0.850, +1.111] | +1.099 [+0.960, +1.231] | +1.168 [+1.045, +1.296] | -1.041 [-1.226, -0.844] |
| exploratory | windows:silence_s=0.5 | 4,120,728 | +1.276 [+1.135, +1.432] | +0.985 [+0.858, +1.106] | +1.101 [+0.973, +1.226] | +1.167 [+1.052, +1.287] | -1.059 [-1.236, -0.864] |
| exploratory | windows:silence_s=2 | 4,120,730 | +1.276 [+1.134, +1.434] | +0.985 [+0.860, +1.103] | +1.101 [+0.972, +1.228] | +1.167 [+1.050, +1.289] | -1.059 [-1.240, -0.864] |
| exploratory | windows:silence_s=5 | 4,120,730 | +1.276 [+1.135, +1.432] | +0.985 [+0.858, +1.104] | +1.101 [+0.973, +1.225] | +1.167 [+1.048, +1.287] | -1.059 [-1.237, -0.864] |
| exploratory | windows:proven_levels=800 | 4,023,446 | +1.278 [+1.133, +1.430] | +0.989 [+0.862, +1.106] | +1.104 [+0.974, +1.226] | +1.162 [+1.050, +1.278] | -1.046 [-1.213, -0.862] |
| exploratory | windows:proven_levels=600 | 3,684,122 | +1.285 [+1.146, +1.440] | +1.002 [+0.870, +1.127] | +1.118 [+0.986, +1.248] | +1.172 [+1.060, +1.291] | -1.059 [-1.225, -0.870] |
| exploratory | windows:proven_levels=400 | 3,039,729 | +1.273 [+1.132, +1.427] | +0.984 [+0.856, +1.107] | +1.105 [+0.975, +1.226] | +1.147 [+1.040, +1.257] | -1.021 [-1.194, -0.834] |
| exploratory | available_case_per_horizon | 4,134,484 / 4,120,728 | +1.275 [+1.133, +1.433] | +0.985 [+0.861, +1.108] | +1.100 [+0.973, +1.228] | +1.167 [+1.054, +1.289] | -1.059 [-1.236, -0.861] |
<!-- END:sensitivity -->

Exploratory specifications change one factor at a time from the primary. `available_case_per_horizon` admits an event for horizon h whenever its own h-outcome is valid (the primary requires all three), which shows how much the common-event-set rule matters. Intervals are unadjusted for multiplicity.

### Descriptive (declared secondary horizons; pre-event state staleness)

<!-- BEGIN:descriptive -->
| metric (all events with a valid pre-state) | events | mean of session means (bp) |
|---|---|---|
| mo_0.1s | 4,134,210 | +0.597 |
| rs_0.1s | 4,134,210 | +0.082 |
| mo_60s | 4,114,986 | +1.168 |
| rs_60s | 4,114,986 | -1.060 |

| information clock | pre-event state age p50 (ms) | p90 | p99 |
|---|---|---|---|
| exchange (primary) | 51 | 95 | 252 |
| receipt+0ms | 56 | 101 | 256 |
| receipt+50ms | 104 | 148 | 310 |
| receipt+200ms | 256 | 301 | 469 |
<!-- END:descriptive -->

### Proxy check: `qty_ge_touch`

<!-- BEGIN:proxy -->
| qty_ge_touch (proxy) | events with a valid next state | share whose touch price moved by the next state |
|---|---|---|
| False | 3,667,002 | 39.1% |
| True | 453,726 | 93.3% |
<!-- END:proxy -->

## Limitations declared before the run (2026-10-19)

- **Selection by future price path (missing-not-at-random).** Accepted windows end when the touch leaves the snapshot-proven region, i.e. after the price has drifted far from the last anchor. Requiring T + 30 s inside the same window therefore removes events according to what the price did *after* them; on sessions with large drifts the retained events under-represent such paths. Reported: the exclusion breakdown (`horizon_leaves_window` vs `horizon_beyond_session_data`), the exploratory `available_case_per_horizon` specification, and the post-hoc eligible-sessions specification.
- **Retrospective conditioning.** The primary pre-event book is the exchange-published state before T, not what a participant had received; the receipt-clock rows show how much that matters for one recorder in Tokyo, not for any particular trader.
- **Event identity.** Timestamp-side clusters are not verified parent orders. The per-trade specification is a different estimand (one event per fill, so larger clusters weigh more), not a bound on the effect of that choice. *(Wording corrected 2026-10-20; the original text said the per-trade specification "bounds" the effect.)*
- **100 ms batching.** The pre-event state can be up to ~100 ms stale even on the exchange clock (see the pre-event state age table); executions inside the published spread exist for that reason.
- **Inference.** 15 discovery sessions (10 train, 5 validation) are the independent units; cell and sensitivity intervals are unadjusted for multiplicity; the relative tick differs between train (0.46–0.80 bp) and validation (0.80–1.20 bp) sessions.
- **Holdout.** Instrument and sample selection were not blind to the test sessions' data quality and tick regime; only their outcomes are sealed.

## Interpretation (discovery sessions only; not a confirmation) — revised 2026-10-20

*Revised after the independent E001 review (`docs/audits/2026-10-19_e001_independent_review.md`). The primary specification and its numbers above are unchanged; the 2026-10-19 wording overstated three points (per-unit loss, timing robustness, trade-unit sensitivity) and presented trade-direction-conditioned cells as if they were decision-time signals. Corrections and the review response are listed at the end.*

1. **Aggressive flow is followed by persistent price moves in its direction; passive liquidity at the touch is, on average, adversely selected.** Over 4.12 million timestamp-side clusters in 15 sessions the aggressor pays an effective spread of +1.28 bp [+1.13, +1.43] and the mid moves +0.99 bp in its direction after 1 s and +1.17 bp after 30 s. The realized spread — a *doubled* quantity, rs = 2 s (P − m(T+h))/m0 — is −0.70 bp at 1 s and −1.06 bp [−1.24, −0.86] at 30 s, negative in all 15 sessions at 30 s (one session's interval includes zero). The passive side's **mark-to-mid result per unit of the hit liquidity is rs/2: −0.35 bp at 1 s and −0.53 bp at 30 s per cluster**, before fees. Weighting by size changes the estimand: per unit of traded quantity or notional (exploratory, below) it is **−1.10 bp at 30 s**, because large clusters carry larger moves. None of these is the result of any quoting policy: they average *all* liquidity hit at the touch, whereas a policy chooses where to rest, joins at the back of the queue, and cancels (E002/E003).
2. **Timing.** On one paired event set (exploratory), the markout is +0.60 bp by 0.1 s, then +0.39 bp more by 1 s, +0.12 bp by 5 s and +0.07 bp by 30 s. The pooled passive result passes through zero around 100 ms (rs/2 = +0.04 bp), but this pools two opposite profiles: the 49% of events whose hit-side touch price differs in the depth batch containing the trade are adverse to the passive side at once (rs/2 = −0.38 bp at 0.1 s, −1.23 bp at 30 s; 1.43 bp of their 2.16 bp markout occurs inside the trade's own 100 ms batch, which also contains other activity), while events that left the touch in place start favourable (+0.39 bp) and decay to about zero (+0.06 bp at 30 s). That subset mixes two directions: in about 45% of all events the touch moved away from the aggressor (the touch was taken out or withdrawn) and in about 4% it moved toward the aggressor (a better quote appeared on the hit side within the batch), shares derived from the frozen proxy-validation table (`touch_moved_next_state`) and the subset size. The second group has the opposite, passive-favourable profile, so the subset's averages understate how adverse the first group is. A split by direction was not declared and is not reported.
3. **What the timing and unit sensitivities do and do not show.** The realized spread is almost unchanged under receipt-clock conditioning (−1.06 bp with up to 200 ms extra latency) largely *by construction*: rs = 2 s (P − m(T+h))/m0 depends on the pre-event state only through the normalising mid, while es shifts by twice the shift in mo, leaving rs = es − 2 mo unchanged. This is **not** evidence that passive outcomes are immune to latency — latency matters for which orders rest and fill, which E001 does not model. Changing the event unit from clusters to individual trade ids moves the 30 s realized spread from −1.06 to −2.05 bp: that is a **material** difference between two estimands that weight executions differently (one event per cluster vs one per fill), not a bound and not an immaterial sensitivity; the quantity- and notional-weighted views (−2.20 bp as rs, −1.10 bp as rs/2) are the relevant size-weighted description.
4. **Queue imbalance — descriptive, trade-direction-conditioned; no decision-time signal is tested.** The *with/against* cells condition on the pre-event imbalance **and on the realized aggressor side**, which is not known when a quote is posted; they are an event-study description, not an executable rule. The exploratory passive-side table re-expresses **the same partition of the same clusters** from the side that was hit (a resting bid is filled only by sellers, a resting ask only by buyers), so it is equally conditioned on the trade's direction. Its imbalance is measured at the exchange-clock pre-event state — a median 51 ms before the trade — not when any quote was posted, and every row is conditional on that side being hit. In that description, clusters hitting the **thinner** side of the book (53–57% of each side's clusters) have rs/2 ≈ −1.0 bp at 30 s, a **balanced** book −0.3 to −0.4 bp, and the **thicker** side +0.24 bp (asks; interval lower bound +0.001) to +0.40 bp (bids). This is not what a newly posted order would earn: the averages cover all touch liquidity, and an order joining the long queue on the thicker side sits at its back, fills less often, and is filled disproportionately in the clusters that exhaust the queue. E001 does not test whether an imbalance observed at posting time improves a quoting policy; that needs a genuine decision-time design with a queue model (E003), fitted on train sessions and evaluated out of sample. *(Corrected 2026-10-20: the earlier text called the passive-side view "observable at posting" and "decision-time". The declared exploratory configuration carries the same inaccurate comment; it is left unchanged because its hash is part of the frozen record.)*
5. **Session heterogeneity.** Effective spreads are higher in the validation sessions (1.16–1.91 bp vs 0.80–1.29 bp), in line with their larger relative tick; 30 s realized spreads range from −1.79 bp to −0.12 bp across sessions: the sign is stable, the magnitude is not.

**What this does and does not support.** On observed data with explicit validity rules, the average liquidity hit at the SOLUSDT touch is adversely selected: the passive side's mark-to-mid result is −0.53 bp per cluster and −1.10 bp per unit of volume at 30 s, before fees, against a one-tick spread of 0.46–1.20 bp in the discovery sessions. It does not show that any market-making policy is profitable or unprofitable — fill selection, queue position, cancellation latency and date-appropriate fees decide that (E002). Confirmation of the primary result on the sealed test sessions happens once, at the Stage 4 close-out.

## Exploratory addenda (declared 2026-10-20 before computation; `configs/e001_exploratory_v1.toml`)

<!-- BEGIN:x_meta -->
Exploratory addenda run 2026-10-20T01:13:21+00:00 · git `5452053023de` · declared in `configs/e001_exploratory_v1.toml` · 4,120,728 primary events · touch transition in 49.1%
<!-- END:x_meta -->

**Paired horizons and batch decomposition** (same events throughout; `c` is the mid move inside the depth batch that contains the trade — it includes the mechanical touch transition and any other activity in those 100 ms):

<!-- BEGIN:x_paired -->
| paired quantity (bp of m0; same events) | all (4,120,728) | touch transition (2,022,899) | no touch transition (2,097,829) |
|---|---|---|---|
| mo(0.1 s) | +0.597 [+0.517, +0.680] | +1.311 [+1.216, +1.409] | +0.002 [+0.002, +0.002] |
| mo(1) − mo(0.1) | +0.388 [+0.336, +0.438] | +0.635 [+0.584, +0.687] | +0.172 [+0.151, +0.194] |
| mo(5) − mo(1) | +0.115 [+0.092, +0.137] | +0.159 [+0.120, +0.194] | +0.075 [+0.053, +0.096] |
| mo(30) − mo(5) | +0.067 [+0.018, +0.120] | +0.051 [-0.018, +0.115] | +0.076 [+0.031, +0.129] |
| mo(30 s) | +1.167 [+1.052, +1.290] | +2.157 [+2.047, +2.275] | +0.325 [+0.263, +0.386] |
| c: move within the trade's 100 ms batch | +0.651 [+0.563, +0.743] | +1.432 [+1.329, +1.540] | +0.000 [+0.000, +0.000] |
| drift: mo(30) − c | +0.516 [+0.460, +0.574] | +0.725 [+0.640, +0.808] | +0.325 [+0.262, +0.386] |
| passive mark-to-mid rs/2 at 0.1 s | +0.041 [-0.012, +0.103] | -0.383 [-0.414, -0.353] | +0.387 [+0.330, +0.448] |
| rs/2 at 1 s | -0.347 [-0.442, -0.242] | -1.018 [-1.066, -0.967] | +0.215 [+0.155, +0.279] |
| rs/2 at 30 s | -0.529 [-0.620, -0.431] | -1.228 [-1.312, -1.139] | +0.064 [-0.013, +0.145] |
<!-- END:x_paired -->

**Weighting** (descriptive of all liquidity hit; not a policy return):

<!-- BEGIN:x_weighting -->
| metric (bp) | cluster-weighted (= primary) | quantity-weighted | notional-weighted |
|---|---|---|---|
| es | +1.276 [+1.131, +1.429] | +2.393 [+2.120, +2.678] | +2.396 [+2.124, +2.677] |
| mo_1s | +0.985 [+0.861, +1.105] | +2.181 [+1.991, +2.370] | +2.182 [+1.990, +2.378] |
| mo_30s | +1.167 [+1.052, +1.289] | +2.298 [+2.075, +2.529] | +2.298 [+2.074, +2.533] |
| rs_30s | -1.059 [-1.242, -0.865] | -2.202 [-2.547, -1.866] | -2.201 [-2.558, -1.854] |
| rs/2 at 30 s (passive mark-to-mid; per cluster / per unit of quantity / per unit of notional) | -0.529 [-0.621, -0.434] | -1.101 [-1.279, -0.935] | -1.100 [-1.275, -0.930] |
<!-- END:x_weighting -->

**Passive-side re-expression of the imbalance cells** (exploratory; the same partition as the trade-direction-conditioned with/against cells, relabelled by the side hit; imbalance at the exchange-clock pre-event state, a median 51 ms before the trade, not at posting; outcomes conditional on that side being hit — not a decision-time signal):

<!-- BEGIN:x_decision -->
| side hit (passive side) | its queue vs the opposite touch, at the pre-event state | clusters | share of the side's clusters | mo 30 s | rs/2 at 1 s | rs/2 at 30 s [95% CI] |
|---|---|---|---|---|---|---|
| ask (filled by buyer) | thinner side | 1,120,222 | 53.0% | +1.704 | -0.602 | -1.017 [-1.184, -0.859] |
| ask (filled by buyer) | balanced | 500,590 | 23.7% | +0.952 | -0.153 | -0.374 [-0.562, -0.187] |
| ask (filled by buyer) | thicker side | 490,928 | 23.2% | +0.175 | +0.184 | +0.242 [+0.001, +0.466] |
| bid (filled by seller) | thinner side | 1,141,142 | 56.8% | +1.730 | -0.638 | -0.955 [-1.075, -0.834] |
| bid (filled by seller) | balanced | 453,585 | 22.6% | +0.915 | -0.239 | -0.283 [-0.517, -0.044] |
| bid (filled by seller) | thicker side | 414,261 | 20.6% | +0.076 | +0.072 | +0.402 [+0.242, +0.580] |
<!-- END:x_decision -->

## Independent checks

`tools/verify_e001_stdlib.py` (standard library only; imports nothing from `lpx`) replays the raw Tardis book with plain dicts, derives the validity window itself for single-window sessions (no reconnect, no missing trades, exactly one joint window: 8 of the 15 discovery sessions; it refuses the others), builds clusters from the exchange archive and recomputes the primary per-session metrics. On 2025-11-01 (train), 2026-03-01 and 2026-05-01 (validation) it reproduces the event counts (162,780; 278,833; 112,194) and every primary metric to six decimals; its windows equal the pipeline's to the microsecond except a start 18 ms later on 2025-11-01, where the pipeline applies the 1 s silence cut to a pre-snapshot trade (the checker does not apply silence cuts). It shares the vendor capture with the pipeline, so it checks the computation, not the data source; it is not a third-party reproduction.

## Response to the independent E001 review (2026-10-19)

| Review item | Response |
|---|---|
| 1. Realized spread vs maker P&L | rs kept as defined; per-unit passive mark-to-mid stated as rs/2 (−0.53 bp per cluster, −1.10 bp per unit volume at 30 s); "~1 bp loss" wording withdrawn |
| 2. Hindsight conditioning | **Partly addressed.** with/against cells labelled trade-direction-conditioned and descriptive; the exploratory passive-side table is the same partition relabelled (measured ~51 ms before the trade, conditional on the side being hit), not a decision-time signal. Open: a genuine decision-time test is deferred to E003 |
| 3. Timing sensitivity | invariance of rs attributed to the identity; no latency-immunity claim |
| 4. Trade unit | difference described as material between estimands; quantity/notional-weighted views added |
| 5. Horizon/coverage selection | MNAR and first-of-month disclosures kept; paired-horizon decomposition on one event set; batch vs drift split |
| 6. Economic viability | historical fees, filters and rebate eligibility verified before E002 (see `docs/experiments/E002.md`) |
| 7. Reproduction limits | `verify_stdlib.py` limits stated; `verify_e001_stdlib.py` added for code-level reproduction of E001 on single-window sessions (8 of 15; refuses the rest) |

---

**Close-out labels (pointer appended 2026-11-04; the body above is the frozen discovery report, unchanged).** The final held-out evaluation ran once on the five test sessions under `docs/experiments/FINAL_EVALUATION.md` (revision 9, frozen; attempt 1, ledger `completed 1` = `2447d2a`). This experiment's test labels are in `results/closeout/CLOSEOUT_report.md`, section E001: 6 of 6 confirmed (point estimate; one family linked by an identity: mo and rs at 1, 5 and 30 s); es reported only. Labels are point-estimate checks on five sessions (protocol section 5); a tally is not a count of independent replications.
