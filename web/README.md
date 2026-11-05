# The Liquidity Paradox: website

The companion website for *The Liquidity Paradox*. It is a static, multi-page site that presents the study's results,
with a guided walkthrough and a Scenario Lab covering every tested scenario. For the research itself, see the
[root README](../README.md) and the [paper](../docs/memo/The_Liquidity_Paradox.pdf).

## Pages

| Page | Contents |
|---|---|
| `index.html` (Home) | The paradox in one figure, and the study in four sentences |
| `lab.html` (Explore) | A six-step guided story (`#step=1` to `#step=6`) and the full Scenario Lab, whose settings are kept in the URL hash, for example `lab.html#view=e002` |
| `research.html` | The four experiments, each from its question to its limitations, and the held-out results |
| `methods.html` | Data, simulation, inference, equations and limitations |
| `paper.html` | The paper and the reproducibility supplement, a reading guide and a citation |

## How it presents the evidence

- **Layers.** Plain-language text and takeaways are always visible, interactive figures sit beside them, and the
  exact values, intervals, held-out labels and sources sit one click away in disclosures.
- **Evidence labels.** Every value is marked as observed, modeled (a historical replay), a stress test or a
  hypothetical fee. Teaching diagrams use made-up values and are always tagged "Synthetic example, not market data".
- **Scenario Lab.** Each selection resolves to one of the study's tested scenarios, or to an explicit unavailable state
  with its reason (not tested, not varied, not part of the held-out evaluation, not published, unknown value). Nothing
  is interpolated. The "What changed, and why?" notes are written from tested values and statements in the paper. Two
  quantities are computed on the page, and labelled where shown: fees paid as gross minus net, and ratios of turnover,
  in words.
- **Colour and shape.** Filled navy marks are discovery results; outlined marks and diamonds are held-out results;
  coral marks fees and the highlighted item. Shape repeats every colour meaning.

## Data flow

The site reads only result files committed to this repository. No market data are needed, and nothing is recomputed
from market data.

1. `export/build_bundle.py` (Python standard library only) reads the files listed in `export/registry.py` and writes
   `src/data/core.json` and `src/data/lab.json`. Each number is a record with its value, display precision, evidence
   type, sample, held-out label where one applies, and a pointer to its source file. Held-out values come only from
   `results/closeout/closeout_analysis.json`.
2. `scripts/equations.mjs` renders the paper's equations from `docs/memo/The_Liquidity_Paradox.tex` with KaTeX into
   `src/data/equations.json`, and generates `src/styles/katex.css`, so the browser loads no maths library.
3. Vite builds the five pages with React and TypeScript. A server-side build prerenders each page to static HTML,
   which is readable without JavaScript and hydrates in the browser.
4. `scripts/copy-frozen.mjs` copies the paper and the supplement into `dist/paper/`, after checking each against
   `docs/memo/FROZEN.sha256`. `scripts/lint-built.mjs` then checks the built site (see below).

The built site makes no external requests: the fonts are self-hosted and there is no analytics.

## Build and run

Requirements: Node 24 and npm 11; Python 3.11 or later as `python3`, for the bundle check; Google Chrome, for the
browser tests.

```bash
cd web
npm ci                 # install the exact dependency versions in package-lock.json
npm run build          # generate equations, build and prerender every page, copy the PDFs, run the integrity lint
npm run preview        # serve the build at http://localhost:4323
```

Other commands, also from `web/`:

```bash
npm run dev            # development server at http://localhost:4322
npm run export         # regenerate the data bundles and equations from the repository's result files
npm run check          # bundle check, type check, unit tests, build with lint, browser tests
```

`npm run dev` needs `src/styles/katex.css`, which `npm run build` generates; the PDFs are served only from a build.
Generated output is not committed: `node_modules/`, `dist/`, `.ssr/`, test results and `src/styles/katex.css`.

## Verification

`npm run check` runs, in order:

- **Bundle check:** the committed data bundles are exactly what the exporter produces from the result files.
- **Type check** with TypeScript.
- **Unit tests** (Vitest): display formatting against the values the paper prints; every tested Scenario Lab scenario,
  its unavailable states and its URL round trip; equations copied verbatim from the paper; the "What changed, and
  why?" notes (every number sourced, wording consistent with the pre-registered protocol); and the lint rules.
- **Build and integrity lint:** every decimal in the built HTML carries a source; "confirmed" appears only inside a
  verbatim held-out label; E004's result keeps its required wording; no banned phrase or font, external request, data
  file or secret; every page carries a `noindex` directive; the PDFs are byte-identical to `docs/memo/FROZEN.sha256`;
  each page stays within a size budget.
- **Browser tests** (Playwright with the installed Chrome): accessibility (axe) and no console errors on every page; no
  horizontal scroll at phone width; readable without JavaScript; synthetic diagrams tagged; the guided story end to
  end; the Scenario Lab's explanations, unavailable states, held-out labels and experiment-specific controls; the
  Research and Methods structure; and the PDFs served.

The exporter has its own tests, run from the repository root:

```bash
uv sync --frozen
uv run --frozen pytest web/export --deselect web/export/test_export.py::test_freeze_pinned_trees_unchanged
```

They check that only registered files are read, that every number resolves to its source, that held-out values cite
only the close-out analysis, and that key numbers, the fee table, held-out labels, tallies and quotations match the
paper verbatim. The deselected test compares directory hashes recorded in the close-out freeze record, which cover
files not included in this repository; the repository's `pytest-public.args` sets it aside for the same reason.

## Data and licences

The data files in `src/data/`, and the charts drawn from them, are statistics derived from Tardis.dev order-book data
and Binance Vision trade data. They are licensed under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) with attribution to Binance Vision; see
[`DATA_NOTICE.md`](../DATA_NOTICE.md) for the scope, the required credit and the source terms. No licence is granted for
the website's source code.

Third-party software, with licence texts included in each package:

- **In the built site:** React and React DOM (MIT); KaTeX (MIT), whose fonts are bundled; and Mona Sans through
  `@fontsource-variable/mona-sans` (SIL Open Font License 1.1), self-hosted.
- **Development only:** Vite, Vitest, jsdom, `@vitejs/plugin-react` and Testing Library (MIT); TypeScript and
  Playwright (Apache-2.0); axe-core for Playwright (MPL-2.0).
