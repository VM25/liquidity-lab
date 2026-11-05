import raw from './core.json';
import type { Core, Rec } from './types';
import { fmt, pct } from '../format';

export const core = raw as unknown as Core;

export function rec(id: string): Rec {
  const r = core.values[id];
  if (!r) throw new Error(`unknown record ${id}`);
  return r;
}

/** The record formatted for display at its own precision. */
export function show(id: string): string {
  const r = rec(id);
  if (r.v === null) return r.printed ?? '';
  return (r.pct ? pct(r.v, r.d) : fmt(r.v, r.d, !!r.s)) ?? '';
}
