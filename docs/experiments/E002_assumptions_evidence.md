# E002 — Evidence for date-appropriate execution assumptions (compiled 2026-10-20)

Scope: Binance spot SOLUSDT on the 20 sample days 2025-03-01 → 2026-10-01. Sources are primary or archived primary
(Internet Archive captures of Binance pages and of the public `exchangeInfo` / trade-level endpoints, the official
`binance-spot-api-docs` repository) unless marked otherwise. No geo-restricted endpoint was queried directly.
"Inferred" means not directly evidenced for every sample date; such values are used with the inference stated.

## Instrument filters (Gate C condition: **met**)

| Item | Value | Evidence | Coverage |
|---|---|---|---|
| tickSize | 0.01 USDT | archived `exchangeInfo` 2025-04-26, 2025-12-09, 2026-10-06; 34 archived product-list snapshots 2025-02-28 → 2026-09-03 (two on sample days: 2025-03-01, 2025-12-01) | whole window; no change found after either spot tick-size round (2025-05-16, 2026-06-04) |
| stepSize / minQty | 0.001 SOL | archived `exchangeInfo` (3 dates); CCXT fixtures 2025-01-25 → 2026-09-28 (secondary) | whole window (values between snapshots inferred unchanged) |
| minNotional | 5 USDT | archived `exchangeInfo` (3 dates) | whole window (inferred between snapshots) |
| Order rate limits | 100 new orders / 10 s and 200,000 / UTC day per account; first fill decrements the count, cancels do not | archived `exchangeInfo` 2025-04-26, 2025-12-09, 2026-10-06; `faqs/order_count_decrement.md` | March 2025 inferred (earliest archived capture 2025-04-26) |
| Matching | price-time priority; cancel-replace goes to the back of the queue; `LIMIT_MAKER` rejected if it would match | `faqs/order_amend_keep_priority.md`; `rest-api.md` | stated in docs from 2025-04-07; earlier inferred |
| Amend keep-priority (reduce quantity only) | available from 2025-05-07 | changelog | not used by the E002 baselines (fixed size) |
| Iceberg orders | hidden quantity invisible in L2; queue priority of hidden parts undocumented | changelog, FAQ | limitation: visible queue may understate the true queue |

## Fees (Gate C condition: **met, with one inference**)

| Item | Value | Evidence | Coverage |
|---|---|---|---|
| Regular user (VIP0) spot, USDT pairs | maker 0.100%, taker 0.100% | archived fee page 2025-10-14, 2025-12-04, 2026-01-29, 2026-03-07, 2026-10-02; archived trade-level endpoint 2024-08-19 (same VIP0–2 values) | 2025-10 → 2026-10 evidenced; **2025-03 → 2025-10 inferred** (identical values on both sides, no change announcement found) |
| BNB payment | 25% off standard commission (VIP0 → 0.075% / 0.075%); requires holding BNB | fee page header; `faqs/commission_faq.md` | whole window |
| SOLUSDT promotions | none: SOLUSDT absent from all 22 monthly archived zero-fee lists 2025-01 → 2026-10 | archived `symbol-activity-list` | whole window |
| VIP9 | 0.011% / 0.023% (2025-10 → 2026-10); 0.012% / 0.024% in 2024-08; change date unknown | archived fee page / endpoint | requires ≥ 4B USD 30-day volume and 5,500 BNB (thresholds lowered 2026-03-19) |
| Spot Liquidity Provider program | Tier 1 0.000% maker (≥ 0.05% of weekly exchange maker volume or ≥ $25M weekly maker volume); Tier 2 −0.004%; Tier 3 −0.006%; Tier 4 −0.008%; taker per VIP level | archived 2024-09-09 announcement; June 2025 press release ("max 0.8 bps"); persistence to 2026-10 inferred | eligibility far beyond a small participant |
| Fee charging | buy: fee taken in the received base asset; sell: in quote; or in BNB when enabled | `faqs/commission_faq.md` | E002 books every fee in quote currency at the fill price (exact in value at the fill; ignores the later revaluation of a base-asset fee, a second-order term rate × Δprice) |

**Feasibility for this project ($0 budget, no capital for BNB):** only the regular VIP0 schedule without BNB is attainable. BNB-discounted, VIP and LP schedules are reported as explicitly labelled hypothetical scenarios, never as the default.

## Latency (calibration; inferred brackets)

| Bracket | One-way order entry / acknowledgement | Market-data delay beyond the Tardis recorder (Tokyo) | Basis |
|---|---|---|---|
| Tokyo co-located (optimistic) | 2 ms | 0 ms | Albers, Cucuringu, Howison & Shestopaloff (2025), *Quantitative Finance* 25(6): message time from an AWS-Tokyo server mean ≈ 2 ms (sd ≈ 1 ms), Binance perpetual 2023 |
| Regional Asia host (intermediate) | 30 ms | 30 ms | CCXT measurement 2026-07-16 (secondary): REST first-byte from Hong Kong 58 ms, Singapore 73 ms (round trip) |
| Distant host, e.g. Europe (conservative) | 115 ms | 115 ms | same source: London 229 ms, Frankfurt 230 ms round trip |

No primary measurement of Binance spot order-entry latency for 2025–2026 was found; these brackets are calibrations, reported side by side and never selected after seeing results. The recorder's own receipt latency (≈ 1–3 ms after the exchange timestamp in the data) is already contained in the replayed receipt times.

## Queue-model references

| E002 model | Equivalent | Reference |
|---|---|---|
| conservative: queue ahead advances only by executions at the price; capped at the level size | hftbacktest `RiskAdverseQueueModel` | nkaz001/hftbacktest, `queue.rs` |
| intermediate: net non-trade decreases allocated ahead in proportion to the queue ahead | hftbacktest `ProbQueueModel` with the identity function; Rigtorp (2013) | Rigtorp, "Estimating order queue position" (2013) |
| optimistic: net decreases allocated ahead first; fills also when the opposite side moves to or through the order's price | upper bound | — |
| naive (reference only): any trade at the price fills the order | the touch-fill rule that hypothetical-execution studies show to be optimistic | Lo, MacKinlay & Zhang (2002), *JFE* 65 |

Supporting literature: Moallemi & Yuan (2017) on queue-position value (of the order of the spread for large-tick assets); Cont & de Larrard (2013) and Huang, Lehalle & Rosenbaum (2015) on queue dynamics; Gould & Bonart (2016) on queue imbalance; Lehalle & Mounjid (2017) on imbalance, adverse selection and latency; Albers et al. (2025, arXiv 2502.18625) on maker fill probability versus post-fill returns on Binance perpetuals (not transferable as spot parameters).
