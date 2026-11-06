import type { ReactNode } from 'react';

export type PageId = 'overview' | 'research' | 'lab' | 'methods' | 'paper';

// Three destinations. Methods & Data and Paper & Code are part of Research. Links are plain anchors: every page is
// prerendered, and a full page load keeps each page's first render free of entrance motion (see useEnter).
export const NAV: Array<{ id: 'home' | 'explore' | 'research'; href: string; label: string; sub: string; pages: PageId[] }> = [
  { id: 'home', href: '/', label: 'Home', sub: 'the paradox', pages: ['overview'] },
  { id: 'explore', href: '/lab', label: 'Explore', sub: 'the Scenario Lab', pages: ['lab'] },
  { id: 'research', href: '/research', label: 'Research', sub: 'experiments, methods, paper', pages: ['research', 'methods', 'paper'] },
];

export const RESEARCH_NAV: Array<{ id: PageId; href: string; label: string }> = [
  { id: 'research', href: '/research', label: 'Experiments' },
  { id: 'methods', href: '/methods', label: 'Methods & data' },
  { id: 'paper', href: '/paper', label: 'Paper & code' },
];

export function Layout({ page, children }: { page: PageId; children: ReactNode }) {
  return (
    <>
      <a className="skip" href="#main">Skip to content</a>
      <header className="hdr">
        <div className="wrap">
          <a className="mark" href="/"><i aria-hidden="true" />The Liquidity Paradox</a>
          <nav aria-label="Primary">
            <ul className="nav">
              {NAV.map((n) => (
                <li key={n.id}><a href={n.href} aria-current={n.pages.includes(page) ? 'page' : undefined}>{n.label}</a></li>
              ))}
              <li className="pdf"><a href="/paper/The_Liquidity_Paradox.pdf">Paper (PDF)</a></li>
            </ul>
            <details className="menu">
              <summary>Menu</summary>
              <ul>
                {NAV.map((n) => (
                  <li key={n.id}><a href={n.href} aria-current={n.pages.includes(page) ? 'page' : undefined}>{n.label} <span>{n.sub}</span></a></li>
                ))}
                <li><a href="/paper/The_Liquidity_Paradox.pdf">Paper <span>PDF</span></a></li>
              </ul>
            </details>
          </nav>
        </div>
      </header>
      {children}
    </>
  );
}

/** The sub-navigation shared by the three Research pages. */
export function ResearchNav({ page }: { page: PageId }) {
  return (
    <nav className="rnav" aria-label="Research">
      {RESEARCH_NAV.map((n) => <a key={n.id} href={n.href} aria-current={n.id === page ? 'page' : undefined}>{n.label}</a>)}
    </nav>
  );
}

export function Footer() {
  return (
    <footer className="site-foot" data-deploy-check="2026-11-06">
      <p>
        Results come from the study and its paper, <cite>The Liquidity Paradox</cite>, rounded for display. Trading results are
        simulated replays of the historical market, not live trading. Diagrams marked “synthetic example” use made-up values to
        explain an idea.
      </p>
      <p>Vatsal Maniar · November 2026<br />Independent research</p>
    </footer>
  );
}
