import { StrictMode, type ComponentType } from 'react';
import { createRoot, hydrateRoot } from 'react-dom/client';
import { Layout, type PageId } from './components/Layout';
import { settle } from './components/hooks';
import './fonts';
import './styles/base.css';

/** Scroll reveals for the few elements marked data-reveal, and only those still below the fold once the page is live:
 *  anything already on screen, printed, or seen with reduced motion is never hidden. */
function reveal() {
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const els = [...document.querySelectorAll<HTMLElement>('[data-reveal]')].filter((el) => el.getBoundingClientRect().top > innerHeight * 0.9);
  if (!els.length) return;
  const show = (el: Element) => { el.classList.add('rv-in'); el.classList.remove('rv-wait'); };
  const io = new IntersectionObserver((es) => {
    for (const e of es) if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -10% 0px' });
  for (const el of els) { el.classList.add('rv-wait'); io.observe(el); }
  addEventListener('beforeprint', () => { els.forEach(show); io.disconnect(); }, { once: true });
}

/** A topic that opens settles its content in (the height itself eases where the browser supports it). */
function disclosures() {
  document.addEventListener('toggle', (e) => {
    const d = e.target;
    if (!(d instanceof HTMLDetailsElement) || !d.open || d.classList.contains('menu')) return;
    d.classList.remove('opening');
    void d.offsetWidth;
    d.classList.add('opening');
    setTimeout(() => d.classList.remove('opening'), 420);
  }, true);
}

/** Hydrate the prerendered page, or render it in the dev server where no prerendered markup exists. */
export function boot(page: PageId, Page: ComponentType) {
  const root = document.getElementById('root')!;
  const app = (
    <StrictMode>
      <Layout page={page}><Page /></Layout>
    </StrictMode>
  );
  if (root.firstElementChild) hydrateRoot(root, app);
  else createRoot(root).render(app);
  requestAnimationFrame(() => requestAnimationFrame(() => {
    document.documentElement.classList.add('live');
    settle();
    disclosures();
    reveal();
  }));
}
