import { useEffect, useRef, type ReactNode } from 'react';

export type PageId = 'overview' | 'research' | 'lab' | 'methods' | 'paper';

// Three destinations. Methods & Data and Paper & Code are part of Research.
export const NAV: Array<{ id: 'home' | 'explore' | 'research'; href: string; label: string; sub: string; pages: PageId[] }> = [
  { id: 'home', href: './index.html', label: 'Home', sub: 'the paradox', pages: ['overview'] },
  { id: 'explore', href: './lab.html', label: 'Explore', sub: 'the Scenario Lab', pages: ['lab'] },
  { id: 'research', href: './research.html', label: 'Research', sub: 'experiments, methods, paper', pages: ['research', 'methods', 'paper'] },
];

export const RESEARCH_NAV: Array<{ id: PageId; href: string; label: string }> = [
  { id: 'research', href: './research.html', label: 'Experiments' },
  { id: 'methods', href: './methods.html', label: 'Methods & data' },
  { id: 'paper', href: './paper.html', label: 'Paper & code' },
];

/** Opens the <details> a link points at (research.html#e002, methods.html#limits), then scrolls to it. */
function openTarget(smooth: boolean) {
  const id = decodeURIComponent(location.hash.slice(1));
  if (!id || id.includes('=')) return;
  const el = document.getElementById(id);
  if (!(el instanceof HTMLDetailsElement)) return;
  el.open = true;
  requestAnimationFrame(() => el.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' }));
}

export function Layout({ page, children }: { page: PageId; children: ReactNode }) {
  const hdr = useRef<HTMLElement>(null);
  useEffect(() => {
    // the header gains a soft edge once content scrolls beneath it
    let raf = 0;
    const onScroll = () => {
      if (raf) return;
      raf = requestAnimationFrame(() => { raf = 0; hdr.current?.classList.toggle('scrolled', scrollY > 8); });
    };
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    openTarget(false);
    const onHash = () => openTarget(!reduced);
    addEventListener('hashchange', onHash);
    return () => { removeEventListener('scroll', onScroll); removeEventListener('hashchange', onHash); cancelAnimationFrame(raf); };
  }, []);
  return (
    <>
      <a className="skip" href="#main">Skip to content</a>
      <header className="hdr" ref={hdr}>
        <div className="wrap">
          <a className="mark" href="./index.html"><i aria-hidden="true" />The Liquidity Paradox</a>
          <nav aria-label="Primary">
            <ul className="nav">
              {NAV.map((n) => (
                <li key={n.id}><a href={n.href} aria-current={n.pages.includes(page) ? 'page' : undefined}>{n.label}</a></li>
              ))}
              <li className="pdf"><a href="./paper/The_Liquidity_Paradox.pdf">Paper (PDF)</a></li>
            </ul>
            <details className="menu">
              <summary>Menu</summary>
              <ul>
                {NAV.map((n) => (
                  <li key={n.id}><a href={n.href} aria-current={n.pages.includes(page) ? 'page' : undefined}>{n.label} <span>{n.sub}</span></a></li>
                ))}
                <li><a href="./paper/The_Liquidity_Paradox.pdf">Paper <span>PDF</span></a></li>
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
    <footer className="site-foot">
      <p>
        Results come from the study and its paper, <cite>The Liquidity Paradox</cite>, rounded for display. Trading results are
        simulated replays of the historical market, not live trading. Diagrams marked “synthetic example” use made-up values to
        explain an idea.
      </p>
      <p>Vatsal Maniar · November 2026<br />Independent research</p>
    </footer>
  );
}
