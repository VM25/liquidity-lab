# The Liquidity Paradox — V1 research website (local build)

Design: navy, cream and coral with Mona Sans (owner approval 2026-11-05; replaces Mineral Analytical, archived at
`../design/archive/mineral-web-v1-2026-11-05.tar.gz`). Three destinations: Home (`index.html`), Explore (`lab.html`:
guided story by default, `#step=N`; full lab with any scenario hash) and Research (`research.html`, `methods.html`,
`paper.html`). Not published, not deployed; hosting is undecided and nothing here is configured for any provider. Plan
and boundaries: `../docs/WEBSITE_PLAN.md`.

## How the site explains the research

- **Three layers in one product.** Plain-language text and takeaways are always visible (understand); interactive
  figures and the Lab sit beside them (explore); exact values, intervals, labels and sources sit in `<Inspect>`
  disclosures (inspect). `src/components/Explain.tsx` holds `Inspect`, `Help`, `useHelp`, `Takeaway` and `Synth`.
- **Teaching diagrams** (`src/charts/teach.tsx`) use made-up values and are always framed by `Synth`, which tags them
  "Synthetic example, not market data". `WalkForward` draws the study's real session design and `CountRule` the
  protocol's own arithmetic; neither is synthetic and both say so.
- **Scenario Lab.** `src/lab/model.ts` resolves a selection to a tested cell or an explicit unavailable state (unchanged
  rules, plus a comparison policy `vs`). `src/lab/explain.ts` writes the "What changed, and why?" notes from frozen grid
  cells and paper statements; every number is a segment with its source. Two arithmetic identities are used and
  labelled where shown: fees paid = gross − net, and a ratio of two turnovers (in words). The guided story (`STORY` in `src/pages/Lab.tsx`) has six
  steps; each can open its scenario in the full lab.
- **Colour:** navy = discovery (filled marks) and text; outlined navy marks and diamonds = held-out; coral = the one
  datum a figure is about, the active state, and fees. Shape repeats every colour meaning.

## How the numbers get here

`export/build_bundle.py` (Python standard library only) reads a fixed registry of frozen research files
(`export/registry.py`) and writes `src/data/core.json` and `src/data/lab.json`. Every number is a record with its value,
display precision, verbatim status, sample, held-out label where one applies, and a `src` pointer back to the frozen
file. Held-out values come only from `results/closeout/closeout_analysis.json` and pre-outcome metadata; the per-session
held-out tables are not registered. Nothing is recomputed from market data.

## Reproduce from a clean checkout

Requires Node 24 and npm 11 (built with Node 24.8.0, npm 11.6.0); Python 3.12 via `uv` for the exporter tests; Google
Chrome for the Playwright browser checks. Raw market data are not needed: the site reads only frozen result files that
are in the repository.

```bash
cd web
npm ci                 # exact dependency versions from package-lock.json
npm run check          # bundle freshness, type check, unit tests, build (prebuild regenerates src/styles/katex.css), browser checks
npm run preview        # http://localhost:4323
```

Not in git, by design: `node_modules/`, `dist/`, `.ssr/`, test output and the generated `src/styles/katex.css` (all
rebuilt by the commands above); review screenshots (`node scripts/capture-screens.mjs` against a running preview writes
them to `../design/screenshots/`); superseded design prototypes and archived earlier builds under `../design/`.

## Commands (from `web/`)

```bash
npm ci                 # install pinned dependencies
npm run export         # rebuild the data bundles and the equation HTML from frozen artifacts
npm run dev            # local development server, http://localhost:4322
npm run build          # build, prerender every page, copy the frozen PDFs (hash-checked), run the integrity lint
npm run preview        # serve the build, http://localhost:4323 (restart it after each rebuild)
npm run check          # bundle freshness, type check, unit tests, build with lint, browser checks
```

```bash
uv run --frozen pytest web/export -q   # exporter tests and freeze guards, from the repository root
```

## What the checks enforce

- **Exporter tests:** the close-out freeze-pinned trees and `docs/memo/FROZEN.sha256` are unchanged; only registered
  files are read; every number resolves to its frozen source; held-out numbers cite only the frozen analysis; key values
  and paper Table 3 match the frozen paper; labels are verbatim; tallies are never summed; quotations are verbatim.
- **Unit tests:** formatting (true minus, a nonzero value never shown as zero, the paper's printed values), the Lab's
  tested cells and closed set of unavailable states, equations copied verbatim from the paper, and the Lab's
  explanations and tour: every number sourced, fee-unaware fills unchanged across fee schedules, hypothetical fees
  flagged, held-out values reported only, no banned wording, the participation finding stated correctly.
- **Integrity lint (`scripts/lint-built.mjs`):** every decimal in the built HTML carries a source; "confirmed" appears
  only inside verbatim held-out labels; H4-W keeps "no material deterioration under the specified threshold"; no
  banned phrase, banned font, external request, data file or secret; the frozen PDFs are byte-identical; a per-page
  size budget.
- **Browser checks (Playwright, installed Chrome):** axe accessibility on every page, no console errors, no horizontal
  scroll at 375 px, readable without JavaScript, every synthetic diagram tagged, the corrected wordings, the homepage's
  five steps, the guided tour end to end, the "What changed, and why?" panel, control help, the phone settings sheet,
  and the Research page's question-to-limitations structure.

`scripts/capture-screens.mjs` writes the review screenshots to `../design/screenshots/mineral/` from a running preview.

## Dependencies

All direct dependencies are free: React, React DOM, KaTeX and Vite (MIT); Mona Sans (SIL OFL, self-hosted via Fontsource); TypeScript and Playwright (Apache-2.0); axe-core for Playwright
(MPL-2.0, development only).
