// Display formatting only: rounding for display, true minus signs, and a nonzero value is never shown as zero.
export const MINUS = '−';

function abs(v: number, d: number): string {
  return Math.abs(v).toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
}

export function fmt(v: number | null | undefined, d: number, signed = false): string | null {
  if (v === null || v === undefined || Number.isNaN(v)) return null;
  let dd = d;
  let s = abs(v, dd);
  while (v !== 0 && Number(s.replace(/,/g, '')) === 0 && dd < 8) {
    dd += 1;
    s = abs(v, dd);
  }
  if (v < 0 && Number(s.replace(/,/g, '')) !== 0) return MINUS + s;
  if (signed && v > 0) return '+' + s;
  return s;
}

export function pct(v: number | null | undefined, d = 1): string | null {
  const s = fmt(v === null || v === undefined ? v : v * 100, d);
  return s === null ? null : s + '%';
}

/** Axis tick label: 1000s as k, true minus. */
export function axisLab(t: number): string {
  const a = Math.abs(t);
  const s = a >= 1000 ? `${+(a / 1000).toPrecision(6)}k` : String(+a.toPrecision(6));
  return (t < 0 ? MINUS : '') + s;
}

/** A "nice" step for axis domains (1, 2, 2.5, 5, 10 × 10^k). */
export function nice(x: number): number {
  if (x <= 0) return 1;
  const e = Math.pow(10, Math.floor(Math.log10(x)));
  const m = x / e;
  return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * e;
}

/** Replace ASCII hyphen-minus before digits with a true minus, for text drawn from data files. */
export function tx(t: string): string {
  return t.replace(/(^|[\s[(,=/])-(?=\.?\d)/g, `$1${MINUS}`);
}
