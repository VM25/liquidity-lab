import { describe, expect, it } from 'vitest';
import { core, show } from './data/core';
import { MINUS, fmt, pct } from './format';

describe('display formatting', () => {
  it('uses a true minus and an explicit plus for signed values', () => {
    expect(fmt(-1.0585, 2, true)).toBe(`${MINUS}1.06`);
    expect(fmt(0.65, 2, true)).toBe('+0.65');
    expect(fmt(171156.6114, 0)).toBe('171,157');
  });
  it('never shows a nonzero value as zero (Review Focus 3)', () => {
    expect(fmt(-0.009701, 2, true)).toBe(`${MINUS}0.01`);
    expect(fmt(0.0016507, 2, true)).toBe('+0.002');
    expect(fmt(-0.00004, 2)).toBe(`${MINUS}0.00004`);
    for (const r of Object.values(core.values)) {
      if (typeof r.v !== 'number' || r.v === 0) continue;
      const s = (r.pct ? pct(r.v, r.d) : fmt(r.v, r.d, !!r.s))!;
      expect(/[1-9]/.test(s), `${r.src} -> ${s}`).toBe(true);
    }
  });
  it('renders undefined values as missing, not zero (Review Focus 2)', () => {
    expect(fmt(null, 2)).toBeNull();
    expect(fmt(Number.NaN, 2)).toBeNull();
  });
  it('matches the numbers the frozen paper prints', () => {
    const paper: Record<string, string> = {
      'e001.rs_30s.disc': `${MINUS}1.06`, 'e001.rs_30s.held': `${MINUS}0.59`, 'e003.h1f.disc': '3.64%', 'e003.h1f.held': '4.20%',
      'e003.h1t.disc': `${MINUS}0.12`, 'e003.h1t.held': `${MINUS}0.01`, 'e004.p0.held': `${MINUS}0.09`, 'e004.p3m2.held': `${MINUS}0.08`,
      'e003.h3.net_per_hour_diff.held': '+0.65', 'e003.p3m2_p0.held': '+37.5', 'e003.p3m2_p0.held_fee_saving': '33.2',
    };
    for (const [id, s] of Object.entries(paper)) expect(show(id), id).toBe(s);
  });
});
