import { describe, expect, it } from 'vitest';
import { DEF, LAB, OPT, POL, cellKey, parseHash, resolve, serialize } from './model';

describe('Scenario Lab model', () => {
  it('resolves every one of the 192 tested E003 cells on both samples', () => {
    let n = 0;
    for (const sample of ['discovery', 'heldout'])
      for (const fill of ['conservative', 'intermediate', 'optimistic'])
        for (const latency of ['tokyo', 'regional', 'distant'])
          for (const fee of ['vip0', 'vip9', 'lp_tier4']) {
            const r = resolve({ ...DEF, sample, fill, latency, fee }, []);
            expect(r.ok).toBe(true);
            n += 1;
          }
    expect(n).toBe(54);
    expect(Object.keys(LAB.grid.disc)).toHaveLength(192);
    expect(Object.keys(LAB.grid.held)).toHaveLength(192);
  });

  it('shows P3F and P4 at VIP0 as abstained (the zero is mechanical) on both samples', () => {
    for (const sample of ['discovery', 'heldout']) {
      const r = resolve({ ...DEF, sample }, []);
      if (!r.ok) throw new Error('expected a tested cell');
      expect(r.rows.filter((x) => x.kind === 'abstained').map((x) => x.p.id)).toEqual(['P3F', 'P4']);
      expect(r.rows.find((x) => x.p.id === 'NT')!.kind).toBe('baseline');
    }
  });

  it('answers untested selections with an explicit reason, never a substitute cell', () => {
    const naive = resolve({ ...DEF, fill: 'naive' }, []);
    expect(naive).toMatchObject({ ok: false, reason: 'not_tested', k: 'fill' });
    expect(resolve({ ...DEF, fee: 'vip0_bnb' }, [])).toMatchObject({ ok: false, reason: 'not_tested', k: 'fee' });
    expect(resolve({ ...DEF, fee: 'lp_tier1' }, [])).toMatchObject({ ok: false, reason: 'not_tested' });
    expect(resolve({ ...DEF, limits: 'other' }, [])).toMatchObject({ ok: false, reason: 'not_varied' });
  });

  it('keeps unknown link values visible as an unknown-value state (Review Focus 1)', () => {
    const { state, bad } = parseHash('#focus=P9&fill=naive&fee=vip0');
    expect(bad).toEqual(['focus = P9']);
    expect(state.fill).toBe('naive');
    expect(resolve(state, bad)).toMatchObject({ ok: false, reason: 'unknown_value' });
  });

  it('round-trips every tested selection through the URL', () => {
    for (const fill of OPT.fill) for (const fee of OPT.fee) {
      const s = { ...DEF, fill: fill.id, fee: fee.id };
      expect(parseHash(serialize(s))).toEqual({ state: s, bad: [] });
    }
  });

  it('reads held-out values only from the frozen close-out analysis', () => {
    expect(LAB.grid_src.held.startsWith('results/closeout/closeout_analysis.json#')).toBe(true);
    const r = resolve({ ...DEF, sample: 'heldout' }, []);
    if (!r.ok) throw new Error('expected a tested cell');
    expect(r.rows.every((x) => x.sess === null)).toBe(true);
  });

  it('has a key for every policy in every fee schedule', () => {
    for (const p of POL) for (const fee of ['vip0', 'vip9', 'lp_tier4']) expect(LAB.grid.disc[cellKey(p.id, 'intermediate', 'regional', fee)]).toBeDefined();
  });
});
