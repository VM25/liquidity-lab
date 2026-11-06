# The Liquidity Paradox: website

The companion website for *The Liquidity Paradox*, live at **<https://liquidityparadox.netlify.app>**. It presents the
study's results, with a guided walkthrough and a Scenario Lab covering every tested scenario. For the research itself,
see the [root README](../README.md) and the [paper](../docs/memo/The_Liquidity_Paradox.pdf).

| | |
|---|---|
| Framework | [Next.js](https://nextjs.org) (App Router), React, TypeScript; every page prerendered as static HTML |
| Hosting | Netlify, project `liquidityparadox` ([dashboard](https://app.netlify.com/projects/liquidityparadox)) |
| Production URL | <https://liquidityparadox.netlify.app> |
| Source | [VM25/liquidity-lab](https://github.com/VM25/liquidity-lab), directory `web/`, production branch `main` |
| Deployment | Netlify's GitHub integration: every push to `main` builds and publishes production |

## Pages

| Route | Contents |
|---|---|
| `/` (Home) | The paradox in one figure, and the study in four sentences |
| `/lab` (Explore) | A six-step guided story (`#step=1` to `#step=6`) and the full Scenario Lab, whose settings are kept in the URL hash, for example `/lab#view=e002` |
| `/research` | The four experiments, each from its question to its limitations, and the held-out results |
| `/methods` | Data, simulation, inference, equations and limitations |
| `/paper` | The paper and the reproducibility supplement (served at `/paper/*.pdf`), a reading guide and a citation |

The addresses of the earlier flat-file build (`/lab.html`, `/research.html` and so on) redirect permanently to these
routes, keeping any `#` settings.

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

## Code layout

```
src/app/            Next.js routes: layout.tsx (metadata, fonts, base styles), one page.tsx per route, robots.ts, sitemap.ts
src/views/          the five page components (Lab, Overview, Research, Methods, Paper)
src/components/     header and footer (Layout), disclosures, labels, SiteEffects (page-wide behaviour after hydration)
src/charts/         SVG figures; teaching diagrams in teach.tsx
src/lab/            the Scenario Lab's model and its "What changed, and why?" notes
src/data/           data bundles exported from the result files (see below)
src/site.ts         production URL, indexing rule and page metadata
public/             favicon and share image; public/paper/ is generated before each build
scripts/            build steps and the integrity lint
e2e/                browser tests (Playwright)
export/             the Python exporter and its tests
```

Every route renders static HTML at build time. The route files, the layout and the Methods page are server components;
client components (`'use client'`) are used where a page is interactive: the Scenario Lab, the Home and Research
views (their figures measure their own width), the Paper view (its citation button), the teaching diagrams, the help
toggles and `SiteEffects`. There are no API routes, server actions, middleware, databases or runtime data fetches; the site
loads nothing from other origins (fonts are self-hosted, there is no analytics). Links between pages are plain anchors,
so each page loads in full, as a prerendered document.

## Data flow

The site reads only result files committed to this repository. No market data are needed, and nothing is recomputed
from market data.

1. `export/build_bundle.py` (Python standard library only) reads the files listed in `export/registry.py` and writes
   `src/data/core.json` and `src/data/lab.json`. Each number is a record with its value, display precision, evidence
   type, sample, held-out label where one applies, and a pointer to its source file. Held-out values come only from
   `results/closeout/closeout_analysis.json`.
2. `scripts/equations.mjs` renders the paper's equations from `docs/memo/The_Liquidity_Paradox.tex` with KaTeX into
   `src/data/equations.json`, and generates `src/styles/katex.css`, so the browser loads no maths library.
3. `scripts/copy-frozen.mjs` copies the paper and the supplement into `public/paper/`, after checking each against
   `docs/memo/FROZEN.sha256`.
4. `next build` prerenders every route to static HTML, which is readable without JavaScript and hydrates in the
   browser. `scripts/lint-built.mjs` then checks the build output (see below).

Steps 2 and 3 run automatically before every build and development run (`npm run assets`).

## Local development

Requirements: Node 24 and npm 11; Python 3.11 or later as `python3`, for the bundle check; Google Chrome, for the
browser tests.

```bash
cd web
npm ci                 # install the exact dependency versions in package-lock.json
npm run dev            # development server at http://localhost:4322
```

Production build, as Netlify runs it, and a local server for it:

```bash
npm run build          # equations and PDFs, next build, integrity lint
npm run start          # serve the production build at http://localhost:4323
```

Other commands, from `web/`:

```bash
npm run export         # regenerate the data bundles and equations from the repository's result files
npm run typecheck      # route types (next typegen) and TypeScript
npm run check          # bundle check, type check, unit tests, build with lint, browser tests
```

A local build is never indexable. To check the production variant, set Netlify's context variable:
`CONTEXT=production npm run build`, then `CONTEXT=production npm run e2e`.

## Deployment (Netlify)

The Netlify project `liquidityparadox` is connected to this repository through Netlify's GitHub integration (the
Netlify GitHub App). Netlify detects Next.js and deploys it with its Next.js runtime, `@netlify/plugin-nextjs`
(OpenNext). The runtime is a project setting managed by Netlify (major version 5, kept up to date by Netlify), the same
one it adds when a project is imported from Git in its UI; nothing is pinned in the repository. A deploy log that uses
the runtime shows "Next.js cache saved" and the `___netlify-server-handler` function.

- **Production:** every push to `main` starts a production build. A successful build replaces the live site at
  <https://liquidityparadox.netlify.app>; a failed build leaves the previous deploy live.
- **Build settings** are in [`../netlify.toml`](../netlify.toml): base directory `web`, build command `npm run build`,
  publish directory `.next`, Node 24. Settings in that file take precedence over the Netlify UI.
- **Indexing:** Netlify sets `CONTEXT=production` for production builds, and only those are indexable (no `noindex`,
  canonical URLs, `robots.txt` allowing crawlers, `sitemap.xml`). Deploy previews and branch deploys are built with
  `noindex` and a `robots.txt` that disallows crawling. The rule is in `src/site.ts`; the integrity lint enforces it.
- **No secrets** are needed: the build uses no environment variables beyond those Netlify sets.
- **What Netlify adds at its edge**, outside this repository: an HTML comment at the top of each page's `<head>`
  ("This site is hosted on Netlify…") and, while the project's *Powered by Netlify badge* setting is on, the badge
  script. The comment arrives with a line break that would otherwise break React's hydration; the head script in
  `src/app/layout.tsx` removes it before hydration, and a browser test simulates the injection.

### When a build fails

1. Open the failed deploy in the Netlify dashboard (Deploys) and read the log from the first error.
2. Reproduce it locally from a clean checkout: `cd web && npm ci && CONTEXT=production npm run build`.
3. Typical causes:
   - **`lint-built` violations:** the build output broke an integrity rule (a number without a source, an external
     reference, the indexing rule, a missing or altered PDF). The message names the page and the rule.
   - **`copy-frozen` checksum error:** a file in `docs/memo/` no longer matches `docs/memo/FROZEN.sha256`. The frozen
     files must not change.
   - **Dependency or Node errors:** `npm ci` failing on a lockfile mismatch (run `npm install` and commit
     `package-lock.json`), or a Node version below 24.
   - **The deploy succeeds but every page returns 404:** the build ran without the Next.js runtime and published the raw
     `.next` folder. Check that the deploy log mentions "Next.js cache saved"; if not, make sure the project lists the
     Next.js runtime under its build plugins (*Project configuration → Build & deploy*), then redeploy.
4. Fix, push to `main`, and confirm the new deploy shows *Published* and the live site has the change. To retry
   without a code change, use *Trigger deploy → Deploy site* in the dashboard.

To roll back, publish an earlier successful deploy from the dashboard's Deploys list, then fix `main`.

## Verification

`npm run check` runs, in order:

- **Bundle check:** the committed data bundles are exactly what the exporter produces from the result files.
- **Type check** with TypeScript.
- **Unit tests** (Vitest): display formatting against the values the paper prints; every tested Scenario Lab scenario,
  its unavailable states and its URL round trip; equations copied verbatim from the paper; the "What changed, and
  why?" notes (every number sourced, wording consistent with the pre-registered protocol); and the lint rules.
- **Build and integrity lint:** every decimal in the prerendered HTML carries a source; "confirmed" appears only inside
  a verbatim held-out label; E004's result keeps its required wording; no banned phrase or font, external request,
  data file or secret; the indexing rule, `robots.txt` and the sitemap; the PDFs are byte-identical to
  `docs/memo/FROZEN.sha256`; each page stays within a size budget.
- **Browser tests** (Playwright with the installed Chrome, against `next start`): accessibility (axe) and no console
  errors on every page; no horizontal scroll at phone width; readable without JavaScript; synthetic diagrams tagged;
  the guided story end to end; the Scenario Lab's explanations, unavailable states, held-out labels and
  experiment-specific controls; the Research and Methods structure; the PDFs served; the redirects from the earlier
  addresses; hydration with the comment Netlify inserts into `<head>`; titles, canonical URLs, the share image,
  `robots.txt` and the sitemap. To run them against the live site, use a Playwright config with `baseURL` set to the
  production URL, no `webServer`, and `CONTEXT=production`.

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

- **In the built site:** Next.js, React and React DOM (MIT); KaTeX (MIT), whose fonts are bundled; and Mona Sans
  through `@fontsource-variable/mona-sans` (SIL Open Font License 1.1), self-hosted.
- **Development only:** Vite, Vitest, jsdom and Testing Library (MIT); TypeScript and Playwright (Apache-2.0); axe-core
  for Playwright (MPL-2.0).
