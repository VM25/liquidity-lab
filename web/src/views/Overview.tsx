'use client';
// Home: the paradox and one simple figure on the first screen, the research in four short sentences, and a way in.
// Depth lives in Explore (interactive) and Research (rigour). Numbers come only from the frozen bundle.
import type { CSSProperties } from 'react';
import { Inspect } from '../components/Explain';
import { Footer } from '../components/Layout';
import { Held } from '../components/N';
import { Sized } from '../components/Sized';
import { HeroDuo } from '../charts/home';
import { rec } from '../data/core';

const STRIP: Array<{ k: string; t: string; href: string }> = [
  { k: 'Question', t: 'Can predicting the next few seconds make passive market making profitable?', href: '/lab#step=1' },
  { k: 'Method', t: 'Rebuilt the order book, fixed four experiments in advance, tested once on sealed days.', href: '/methods' },
  { k: 'Finding', t: 'The forecasts worked. Every quoting rule still lost money; the best simply traded least.', href: '/lab#step=4' },
  { k: 'Meaning', t: 'Fees and being traded against, not prediction, decide a small market maker’s result.', href: '/lab#step=5' },
];

export default function Overview() {
  return (
    <main id="main">
      <section className="hero wrap" aria-labelledby="h1">
        <div className="hero-t">
          <p className="kicker">An independent study of market making on Binance SOLUSDT</p>
          <h1 id="h1">We could predict the market. We couldn’t <em>profitably</em> make it.</h1>
          <p className="qual">Within the quoting rules, execution models and attainable fees tested, not every possible strategy.</p>
          <div className="cta">
            <a className="btn primary" href="/lab">Explore the findings <span className="arr" aria-hidden="true">→</span></a>
            <a className="btn quiet" href="/research">Read the research</a>
          </div>
        </div>
        <figure className="hero-fig">
          <Sized fallback={520}>{(w) => <HeroDuo W={w} />}</Sized>
          <Inspect title="About this figure">
            <p className="held">
              Forecast skill is measured directly on market data, for the eight-feature forecast. Trading results are simulated replays of the
              historical market at VIP0, the standard fee and the only one a participant like this can attain, under the study’s primary
              assumptions. On the sealed days, forecast skill was <Held check="H1-F">{rec('e003.h1f.held').lab!}</Held>; trading results on those
              days are <Held>reported only, descriptive (no confirmation claim)</Held>.
            </p>
          </Inspect>
        </figure>
      </section>

      <section className="strip wrap" aria-label="The research in four sentences">
        <ol data-reveal="list">
          {STRIP.map((x, i) => (
            <li key={x.k} style={{ '--i': i } as CSSProperties}><a href={x.href}><b>{x.k}</b><span>{x.t}</span></a></li>
          ))}
        </ol>
      </section>

      <section className="invite" aria-labelledby="inv-h">
        <div className="wrap invite-in" data-reveal="">
          <h2 id="inv-h">See it for yourself</h2>
          <p>Six short steps from a working forecast to a losing market maker, then every tested scenario.</p>
          <div className="cta">
            <a className="btn light" href="/lab">Open the Scenario Lab <span className="arr" aria-hidden="true">→</span></a>
            <a className="btn ghost" href="/research">Experiments and methods</a>
          </div>
        </div>
      </section>

      <div className="wrap"><Footer /></div>
    </main>
  );
}
