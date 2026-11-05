import { rec, show } from '../data/core';

/**
 * A frozen number. Renders the record at its own display precision, with its source, status and sample as data
 * attributes, so every displayed result is traceable (Gate D) and the built-site lint can find numbers without one.
 */
export function N({ id, unit = false, strong = false, nosign = false }: { id: string; unit?: boolean; strong?: boolean; nosign?: boolean }) {
  const r = rec(id);
  const base = nosign ? show(id).replace(/^\+/, '') : show(id);
  const text = base + (unit && r.u && !r.pct ? ` ${r.u}` : '');
  const props = { 'data-src': r.src, 'data-status': r.st, 'data-sample': r.smp, className: 'num' } as const;
  return strong ? <strong {...props}>{text}</strong> : <span {...props}>{text}</span>;
}

/** A held-out label, verbatim from the frozen close-out analysis. */
export function Held({ children, check }: { children: string; check?: string }) {
  return <q className="lbl" data-label={check ?? 'label'}>{children}</q>;
}

/** A verbatim quotation of the frozen paper (checked against the .tex by web/export/test_export.py). */
export function Quote({ children }: { children: string }) {
  return <q className="pq" data-quote="paper">{children}</q>;
}
