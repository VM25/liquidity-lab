import { describe, expect, it } from 'vitest';
import { explain, share, text, type Note } from './explain';
import { DEF, LAB, resolve, type State } from './model';

const ok = (S: State) => {
  const r = resolve(S, []);
  if (!r.ok) throw new Error('expected a tested cell');
  return r;
};
const after = (from: Partial<State>, to: Partial<State>) => {
  const P = { ...DEF, ...from }, S = { ...P, ...to };
  return explain({ S: P, r: resolve(P, []) }, S, ok(S));
};
const all = (ns: Note[]) => ns.map(text).join(' | ');
const BANNED = [/\bno effect\b/i, /\bequivalent\b/i, /mostly when/i, /\bguaranteed\b/i, /\bbest\b/i, /\bprofitable\b(?! quoting)/i];

describe('"What changed, and why?"', () => {
  it('explains the default scenario: the comparison, the caution about fill quality and the abstainers', () => {
    const ns = explain(null, DEF, ok(DEF));
    const t = all(ns);
    expect(t).toContain('P3[M2] against P0');
    expect(t).toContain('about a fifth of P0’s notional');
    expect(t).toContain('A smaller loss is not better fills');
    expect(t).toContain('spans zero');
    expect(t).toContain('P3F and P4 abstain');
  });

  it('gives every number a source pointer', () => {
    const cases = [explain(null, DEF, ok(DEF)), after({}, { fee: 'lp_tier4' }), after({}, { fill: 'optimistic' }), after({}, { latency: 'tokyo' }), after({}, { sample: 'heldout' }), after({ focus: 'P3F' }, { fee: 'lp_tier4' })];
    for (const ns of cases) for (const n of ns) for (const s of n.body) {
      if (typeof s === 'string') { expect(s).not.toMatch(/\d\.\d/); continue; }
      expect(s.v).not.toBe('undefined');
      expect(s.src.length).toBeGreaterThan(10);
    }
  });

  it('says that a fee change leaves a fee-unaware policy’s fills unchanged, and flags hypothetical schedules', () => {
    const t = all(after({}, { fee: 'lp_tier4' }));
    expect(t).toContain('Fee schedule: VIP0 → LP tier 4');
    expect(t).toContain('simulated fills are identical under both schedules');
    expect(t).toContain('LP tier 4 is hypothetical');
    expect(t).toContain('Every policy that trades still loses money on average');
  });

  it('says that a fee-aware policy is simulated per schedule and only trades when its gate opens', () => {
    const t = all(after({ focus: 'P3F' }, { fee: 'lp_tier4' }));
    expect(t).toContain('simulated separately under each schedule');
    expect(t).toContain('Turnover 0 →');
    const back = all(after({ focus: 'P3F', fee: 'lp_tier4' }, { fee: 'vip0' }));
    expect(back).toContain('its gate never opens');
    expect(all(explain(null, { ...DEF, focus: 'P3F' }, ok({ ...DEF, focus: 'P3F' })))).toContain('8 to 17 ticks');
  });

  it('treats a fill model as an assumption, never as evidence about live fills', () => {
    expect(all(after({}, { fill: 'optimistic' }))).toContain('not evidence of what live fills would have been');
  });

  it('labels held-out policy values as reported only and compares them per unit traded', () => {
    const t = all(after({}, { sample: 'heldout' }));
    expect(t).toContain(LAB.held_label);
    expect(t).toContain('compare results per unit traded');
    expect(t).not.toMatch(/confirmed \(/);
  });

  it('never uses wording the protocol rules out', () => {
    const states: Partial<State>[] = [{}, { fee: 'vip9' }, { fee: 'lp_tier4' }, { sample: 'heldout' }, { focus: 'P0', vs: 'P3_M2' }, { focus: 'P4', vs: 'P3F', fee: 'lp_tier4' }, { focus: 'NT' }];
    for (const s of states) {
      const S = { ...DEF, ...s };
      const t = all(explain(null, S, ok(S)));
      for (const re of BANNED) expect(t).not.toMatch(re);
    }
  });

  it('describes turnover ratios in words', () => {
    expect(share(35692, 171156)).toBe('about a fifth of');
    expect(share(171156, 35692)).toBe('about five times');
    expect(share(100, 101)).toBe('about the same as');
  });
});
