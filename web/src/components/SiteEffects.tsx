'use client';
// Page-wide behaviour that runs once the prerendered page has hydrated: the header's scrolled edge, opening the
// disclosure a link points at, scroll reveals and disclosure motion. Renders nothing.
import { useEffect } from 'react';
import { settle } from './hooks';

/** Opens the <details> a link points at (/research#e002, /methods#limits), then scrolls to it. */
function openTarget(smooth: boolean) {
  const id = decodeURIComponent(location.hash.slice(1));
  if (!id || id.includes('=')) return;
  const el = document.getElementById(id);
  if (!(el instanceof HTMLDetailsElement)) return;
  el.open = true;
  requestAnimationFrame(() => el.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto', block: 'start' }));
}

/** Scroll reveals for the few elements marked data-reveal, and only those still below the fold once the page is live:
 *  anything already on screen, printed, or seen with reduced motion is never hidden. */
function reveal(): () => void {
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) return () => {};
  const els = [...document.querySelectorAll<HTMLElement>('[data-reveal]')].filter((el) => el.getBoundingClientRect().top > innerHeight * 0.9);
  if (!els.length) return () => {};
  const show = (el: Element) => { el.classList.add('rv-in'); el.classList.remove('rv-wait'); };
  const io = new IntersectionObserver((es) => {
    for (const e of es) if (e.isIntersecting) { show(e.target); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -10% 0px' });
  for (const el of els) { el.classList.add('rv-wait'); io.observe(el); }
  const onPrint = () => { els.forEach(show); io.disconnect(); };
  addEventListener('beforeprint', onPrint, { once: true });
  return () => { io.disconnect(); removeEventListener('beforeprint', onPrint); };
}

/** A topic that opens settles its content in (the height itself eases where the browser supports it). */
function onToggle(e: Event) {
  const d = e.target;
  if (!(d instanceof HTMLDetailsElement) || !d.open || d.classList.contains('menu')) return;
  d.classList.remove('opening');
  void d.offsetWidth;
  d.classList.add('opening');
  setTimeout(() => d.classList.remove('opening'), 420);
}

export function SiteEffects() {
  useEffect(() => {
    // the header gains a soft edge once content scrolls beneath it
    let raf = 0;
    const hdr = document.querySelector('.hdr');
    const onScroll = () => {
      if (raf) return;
      raf = requestAnimationFrame(() => { raf = 0; hdr?.classList.toggle('scrolled', scrollY > 8); });
    };
    onScroll();
    addEventListener('scroll', onScroll, { passive: true });
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    openTarget(false);
    const onHash = () => openTarget(!reduced);
    addEventListener('hashchange', onHash);

    // .live is set two frames after hydration, so nothing animates its first layout, only later changes
    let undoReveal = () => {};
    const start = requestAnimationFrame(() => requestAnimationFrame(() => {
      document.documentElement.classList.add('live');
      settle();
      document.addEventListener('toggle', onToggle, true);
      undoReveal = reveal();
    }));
    return () => {
      removeEventListener('scroll', onScroll);
      removeEventListener('hashchange', onHash);
      cancelAnimationFrame(raf);
      cancelAnimationFrame(start);
      document.removeEventListener('toggle', onToggle, true);
      undoReveal();
    };
  }, []);
  return null;
}
