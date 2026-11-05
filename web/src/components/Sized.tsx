import type { ReactNode } from 'react';
import { useWidth } from './hooks';

/** Measures its own width and draws the chart at that width, so labels keep their size on a phone. */
export function Sized({ fallback = 620, min = 280, className, children }: { fallback?: number; min?: number; className?: string; children: (w: number) => ReactNode }) {
  const [ref, w] = useWidth<HTMLDivElement>(fallback);
  return <div ref={ref} className={className}>{children(Math.max(min, w))}</div>;
}
