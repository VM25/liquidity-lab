# The Liquidity Paradox

*Short-horizon predictability, adverse selection and the economics of passive market making: pre-registered evidence
from Binance SOLUSDT with a one-time held-out evaluation.*

Vatsal Maniar · November 2026

Order-book forecasts of the SOLUSDT price a few seconds ahead had real out-of-sample skill. Yet at the only attainable
fee tier, every simulated passive quoting rule that traded lost money in every session, and lower losses came mainly
from trading less. The four experiments (E001 to E004) were specified before their discovery outcomes, and five sealed
sessions were evaluated once under a protocol frozen in advance.

- **Paper:** [`docs/memo/The_Liquidity_Paradox.pdf`](docs/memo/The_Liquidity_Paradox.pdf)
- **Reproducibility supplement:** [`docs/memo/Reproducibility_Supplement.pdf`](docs/memo/Reproducibility_Supplement.pdf),
  which maps every result to its specification and output

## Contents

| Path | Contents |
|---|---|
| `docs/memo/` | The paper and the supplement (PDF and LaTeX), bibliography, figures and the script that draws them, and the freeze record with the SHA-256 of every approved file (`FROZEN.sha256`) |
| `docs/experiments/` | The pre-registered specifications of E002 to E004 and the frozen final-evaluation protocol |
| `docs/RESEARCH_SPEC.md`, `docs/DATA_SPEC.md` | The research design and the data specification |
| `configs/` | Sample design and splits, experiment configurations, fee schedules and latency brackets |
| `lpx/` | The research engine: data acquisition and normalisation, order-book replay, execution simulation, experiments and analyses |
| `tools/`, `tests/` | Reproduction and close-out tools, and the test suite |
| `results/` | Experiment outputs and reports (E001 to E004), the held-out close-out, and the data-acceptance report |
| `web/` | Source of the companion website (see `web/README.md`) |

## Verify

```bash
shasum -a 256 -c docs/memo/FROZEN.sha256    # the paper, supplement, sources and figures, byte for byte
uv sync --frozen                            # Python 3.12, pinned in .python-version
uv run pytest @pytest-public.args           # the test suite that runs from this repository alone
cd web && npm ci && npm run check           # the website: data export check, unit and browser tests, build
```

The website builds from the result files in this repository; its browser tests use Google Chrome. Re-running the
experiments themselves needs the raw market data, which are free public samples but are not redistributed here;
`results/data_acceptance_report.md` and the supplement describe how they were obtained.

`pytest-public.args` deselects 30 integrity tests of the held-out close-out procedure. They check that the frozen
close-out code, its pinned inputs and its reports are unchanged since the freeze, by comparing them with commits of the
private research history and with files withheld from this snapshot. They verify the provenance of the evaluation
procedure; none of them recomputes a result. All of them pass in the full research repository, and here they fail only
because that history and those files are absent.

## About this snapshot

This repository is a curated public snapshot of the private research repository, published as a single commit. Its
files are byte-identical to their committed versions in that repository, apart from four written for this snapshot:
this README, `DATA_NOTICE.md`, `pytest-public.args` and `.gitignore`.

The frozen records cite commits of the full development history, for example in `docs/memo/FROZEN.md`,
`results/closeout_freeze/` and the supplement. That history is kept privately as the audit record, so those commit
identifiers cannot be resolved here.

Not included:

- the raw and normalised market data, which were never committed;
- `results/acceptance_001/`, the listings of individual data-acceptance windows, which are finer than the data
  provider's terms allow to be redistributed; the aggregated findings are in `results/data_acceptance_report.md`;
- the fitted forecast coefficients and shrinkage parameters (`results/closeout_fits/`, `e003_models.json`,
  `e004_lambda.csv`), which are models trained on the data;
- development checks and rehearsal records, internal planning documents and review notes, and files unrelated to this
  study.

Some withheld files are pinned in `results/closeout_freeze/freeze_record.json` or cited in the supplement.

## Data and licensing

The market data come from [Tardis.dev](https://tardis.dev) (Binance order-book depth) and
[Binance Vision](https://data.binance.vision) (Binance trades). The statistics, tables and figures derived from them
are licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/), as the Binance Vision terms
require. No licence is granted for the source code or the text of the paper. [`DATA_NOTICE.md`](DATA_NOTICE.md) gives
the exact scope, the required credit and the source terms.

This is independent, non-commercial academic research. It was self-funded, used only free public data and local
computation, and involved no live trading.
