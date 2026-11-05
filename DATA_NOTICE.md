# Data sources, credits and licensing

This is independent, non-commercial academic research. It is not affiliated with, sponsored by or endorsed by Binance
or Tardis.dev.

## Sources

| Data | Source | Terms | In this repository |
|---|---|---|---|
| Binance spot incremental order-book depth: free first-of-month samples (SOLUSDT; BTCUSDT and ETHUSDT for data acceptance only) | [Tardis.dev](https://tardis.dev) | [Tardis.dev Terms of Service](https://docs.tardis.dev/legal/terms-of-service) | Not redistributed |
| Binance spot trades | [Binance Vision](https://data.binance.vision) | [Binance Vision Dataset Terms](https://github.com/binance/binance-public-data/blob/master/TERMS_AND_CONDITIONS.md) and [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) | Not redistributed |

## Derived materials

The following are statistics, tables and figures derived from the sources above:

- the data files and tables in `results/`;
- the figures in `docs/memo/figures/`, and the figures and tables in the paper and the reproducibility supplement;
- the website's data files in `web/src/data/`, and the charts the website draws from them.

They are licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International
licence](https://creativecommons.org/licenses/by-nc-sa/4.0/), as the Binance Vision Dataset Terms require for
redistributed derivative work. Please credit them as:

> Derived from Binance Vision trade data (CC BY-NC-SA 4.0) and Tardis.dev order-book data, in Vatsal Maniar,
> *The Liquidity Paradox* (2026).

Every value is a summary over at least one episode of ten minutes or more, usually a full session, and none can be
used to reconstruct the order book or the trade stream. The repository does not include the raw or normalised market
data, the listings of individual data-acceptance windows, or the fitted forecast coefficients and shrinkage parameters,
which are models trained on the data.

## Everything else

The source code, the documentation and the text of the paper and the supplement are © 2026 Vatsal Maniar. No licence
is granted for them. Third-party software used by the project is listed in `pyproject.toml`, `uv.lock` and
`web/package.json` and remains under its own licences.
