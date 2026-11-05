import { useEffect, useLayoutEffect, useRef, useState } from 'react';

export const useIso = typeof window === 'undefined' ? useEffect : useLayoutEffect;

/** A media query, false on the server and on the first client render (so hydration matches). */
export function useMedia(q: string) {
  const [on, set] = useState(false);
  useEffect(() => {
    const mq = matchMedia(q);
    set(mq.matches);
    const f = () => set(mq.matches);
    mq.addEventListener('change', f);
    return () => mq.removeEventListener('change', f);
  }, [q]);
  return on;
}

/** The rendered width of an element, so charts keep a constant text size instead of scaling down on phones. */
export function useWidth<T extends HTMLElement>(fallback: number): [React.RefObject<T | null>, number] {
  const ref = useRef<T>(null);
  const [w, setW] = useState(fallback);
  useIso(() => {
    const el = ref.current;
    if (!el) return;
    const read = () => setW(Math.round(el.clientWidth) || fallback);
    const ro = new ResizeObserver(read);
    ro.observe(el);
    read();
    return () => ro.disconnect();
  }, [fallback]);
  return [ref, w];
}

/** A deterministic pseudo-random generator, so synthetic teaching examples render identically on server and client. */
export function prng(seed: number) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function gauss(rand: () => number) {
  const u = Math.max(rand(), 1e-12), v = rand();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

// Entrances only for content that appears after the page has settled: what the server rendered never animates in.
let settled = false;
export function settle() { settled = true; }
/** ' enter' for an element mounted after the first render (a new step, a new view), '' otherwise. Fixed per mount.
 *  `quiet` skips it, for a child that mounts together with a parent that already makes the entrance. */
export function useEnter(quiet = false) {
  const [c] = useState(() => (settled && !quiet ? ' enter' : ''));
  return c;
}

/** False during a component's first render, true afterwards: lets children tell a remount from the parent's arrival. */
export function useMounted() {
  const r = useRef(false);
  useEffect(() => { r.current = true; }, []);
  return r;
}
