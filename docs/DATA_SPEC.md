# Market Data Specification & Acceptance

## Source hierarchy (all $0, all provisional)
1. **Tardis first-of-month L2/trade samples:** initial documented reconstruction smoke test; discontinuous sample days.
2. **Goooddy/crypto-lob-stream (Hugging Face):** candidate contiguous trades, snapshots, depth changes; must audit venue/month gaps.
3. **OKX historical L2:** advertised extensive coverage; access, U.S. regional restrictions and rights unresolved; do not bypass restrictions.
4. **Binance public trades / LOBSTER samples:** supplementary flow analysis / independent book validation, not assumed full continuous L2.
5. Alpha Vantage, CoinGecko, FRED: optional context only—not L2 substitutes.

## Canonical input contract (normalized, not fabricated)
- `source`, `venue`, `symbol`, `instrument_type`, `event_type` (snapshot/update/trade), `source_file`.
- Original event timestamp and unit; UTC-normalized event time; receipt/availability time **only when observed or explicitly modeled**.
- Exchange sequence/order key when supplied; stable source-specific tie-breaking rules.
- Book: side, price, **absolute level size** or documented provider semantics; trade: price, quantity, verified/inferred aggressor side.
- Instrument metadata: tick/lot sizes, contract multiplier, currency, fee schedule, effective date.

## Dataset Acceptance Test 001 (actual files required)
- Obtain raw snapshots, updates, and matching trades; record URLs, hashes, dates, row counts, sizes, schema, license notes.
- Rebuild from valid anchors using provider-specific update semantics, event ordering and sequence checks.
- Detect timestamp regression, missing periods, bad levels, crossed/locked book, duplicates and stale levels.
- On gaps: invalidate the interval, resynchronize, and report accepted coverage—**never silently forward-fill**.
- Match top-of-book against independent snapshots/quotes when available; report discrepancy rates.
- Quantify usable contiguous windows by instrument, venue, day and market state; sample a second source independently.
- Exclude invalid segments from forecasting and simulation, not merely from plots.

## Rights and publication
- Free download ≠ permission to redistribute. Confirm **source + underlying exchange** rights separately.
- Keep raw/vendor files local and gitignored; do not expose near-raw book playback without permission.
- Default public site to rights-cleared aggregates, derived research findings, and labeled synthetic illustrations.
- Record unresolved rights as release blockers for the affected visualizations, not for private analysis automatically.

## References
- Tardis: https://docs.tardis.dev/downloadable-csv-files/overview
- Community archive: https://huggingface.co/datasets/Goooddy/crypto-lob-stream
- OKX: https://www.okx.com/historical-data
- Binance: https://github.com/binance/binance-public-data
- LOBSTER: https://data.lobsterdata.com/info/DataSamples.php

**Current status:** Dataset Acceptance Test 001 passed on actual files (2026-10-14): Tardis Binance spot SOLUSDT, 20 first-of-month sessions accepted inside explicit windows; BTC/ETH accepted only inside proven windows; crypto-lob-stream (HF) retains ≈7.5% of the stream and is a verification source only. Evidence: `results/data_acceptance_report.md`; coverage: `results/acceptance_001/windows.csv`.
