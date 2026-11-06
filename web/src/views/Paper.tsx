'use client';
// Paper & Code: the frozen paper and supplement (copied byte-identical at build), checksums, citation and reproduction.
import { useState } from 'react';
import { Footer, ResearchNav } from '../components/Layout';
import { Inspect } from '../components/Explain';
import { Quote } from '../components/N';
import { core } from '../data/core';
import { REPO_URL } from '../site';

const SUBTITLE = 'Short-horizon predictability, adverse selection and the economics of passive market making: pre-registered evidence from Binance SOLUSDT with a one-time held-out evaluation';
const BIBTEX = `@misc{maniar2026liquidity,
  author = {Maniar, Vatsal},
  title  = {The Liquidity Paradox: ${SUBTITLE}},
  year   = {2026},
  month  = nov,
  note   = {Research paper}
}`;

const mb = (n: number) => `${(n / 1048576).toFixed(1)} MB`;

function CopyButton({ text }: { text: string }) {
  const [done, setDone] = useState(false);
  return (
    <button type="button" className="chip" aria-live="polite" onClick={() => { navigator.clipboard?.writeText(text).then(() => { setDone(true); setTimeout(() => setDone(false), 1600); }, () => setDone(false)); }}>
      {done ? 'Copied' : 'Copy BibTeX'}
    </button>
  );
}

export default function Paper() {
  return (
    <main id="main" className="wrap">
      <div className="page-head">
        <h1>Paper &amp; code</h1>
        <p className="lede">The full paper, its reproducibility supplement, and how to cite and check them.</p>
        <ResearchNav page="paper" />
      </div>

      <section className="sec" aria-labelledby="paper-h">
        <div className="res">
          <div>
            <h2 id="paper-h" className="paper-title">The Liquidity Paradox</h2>
            <p className="paper-sub">{SUBTITLE}</p>
            <p className="ink-3 mt-3">Vatsal Maniar · November 2026</p>
            <div className="prose mt-5">
              <p><b>From the abstract.</b> <Quote>Does short-horizon price predictability translate into economically viable passive market making? We reconstruct the Binance SOLUSDT limit order book on twenty first-of-month sessions and simulate passive execution.</Quote> <Quote>Experiments were specified before their discovery outcomes; a five-session holdout was evaluated once under a protocol frozen in advance.</Quote> …</p>
              <p><Quote>At the only attainable fee tier, every simulated policy that trades loses money in every session; lower losses come mainly from trading less.</Quote> <Quote>Linking adverse selection, forecast skill and costs, we find that predictability of this size did not make passive quoting profitable here.</Quote></p>
            </div>
          </div>
          <div>
            <h3 className="sub-h">Download</h3>
            <ul className="dl-list">
              {core.paper.files.map((f) => (
                <li key={f.file}>
                  <a href={`/paper/${f.file}`}><span>{f.title.replace(/ \((paper, )?PDF\)$/, '')}</span><small>{f.file.includes('Supplement') ? 'Every result traced to its specification and output' : 'Vatsal Maniar, November 2026'}</small></a>
                  <span className="ink-3 dl-meta" data-meta="file size">PDF · {mb(f.bytes)}</span>
                </li>
              ))}
            </ul>
            <div className="cite-h mt-5"><h3 className="sub-h">Cite</h3><CopyButton text={BIBTEX} /></div>
            <pre className="code" aria-label="BibTeX citation" tabIndex={0}>{BIBTEX}</pre>
          </div>
        </div>
      </section>

      <section className="sec" aria-labelledby="guide-h">
        <div className="sec-h"><h2 id="guide-h">How to read the paper</h2><p>Nine sections. Where to start depends on what you want from it.</p></div>
        <ol className="guide">
          <li><b>Two minutes</b><span>The abstract and the five numbered findings in Section 1, then Figure 4: net result per hour against turnover.</span></li>
          <li><b>Fifteen minutes</b><span>Section 5, Results, one subsection per experiment, then Section 6, the held-out evaluation and its label tables.</span></li>
          <li><b>Checking the method</b><span>Section 3 (data and sample) and Section 4 (methodology): evidence types, pre-registration, the replay engine, forecasts, policies and inference.</span></li>
          <li><b>Weighing the claims</b><span>Section 7, Discussion, and Section 8, Limitations, in order of importance, before the conclusion in Section 9.</span></li>
          <li><b>Reproducing a number</b><span>The reproducibility supplement maps every result to its specification, output file and version identifier.</span></li>
        </ol>
      </section>

      <section className="sec" aria-labelledby="verify-h">
        <div className="sec-h"><h2 id="verify-h">Verify and reproduce</h2><p>Every result traces to a specification, an output file and a version identifier, listed in the reproducibility supplement.</p></div>
        <Inspect title="Checksums and reproduction" note="for reviewers">
        <div className="res">
          <div>
            <h3 className="sub-h">Check a download</h3>
            <p className="ink-2">Each file’s SHA-256 checksum, to confirm a copy is unaltered:</p>
            <pre className="code" tabIndex={0}>shasum -a 256 The_Liquidity_Paradox.pdf</pre>
            <dl className="kv mt-3">
              {core.paper.files.map((f) => <div key={f.file}><dt>{f.file}</dt><dd className="mono-note">{f.sha256}</dd></div>)}
            </dl>
          </div>
          <div>
            <h3 className="sub-h">Rebuild the paper and figures</h3>
            <p className="ink-2">From the research repository. The figure script reads only the final result files and needs any Python with matplotlib.</p>
            <pre className="code" tabIndex={0}>{`python3 docs/memo/figures/make_figures.py
pdflatex The_Liquidity_Paradox && bibtex The_Liquidity_Paradox
pdflatex The_Liquidity_Paradox && pdflatex The_Liquidity_Paradox`}</pre>
            <h3 className="sub-h mt-5">Rerun the experiments</h3>
            <p className="ink-2">The research engine (Python, managed with uv) reruns each experiment from its fixed configuration. It needs the raw market data: free public samples that are not redistributed here. The supplement lists the exact sources, specifications and versions.</p>
            <pre className="code" tabIndex={0}>{`uv run pytest
uv run python -m lpx.research.e002
uv run python -m lpx.research.e003`}</pre>
            <h3 className="sub-h mt-5">Source code</h3>
            <p className="ink-2">The research code and this website’s source are public at <a href={REPO_URL}>github.com/VM25/liquidity-lab</a>, without the raw market data. The supplement documents every specification, output and version behind the results.</p>
          </div>
        </div>
        </Inspect>
      </section>
      <Footer />
    </main>
  );
}
