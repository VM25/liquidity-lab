// "What changed, and why?": plain-language notes for the Scenario Lab, built only from tested grid cells and from
// statements in the frozen paper. Every number is a segment that carries its source pointer. Two arithmetic identities
// are used and labelled where shown: fees paid = gross − net, and a ratio of two turnovers.
import { core } from '../data/core';
import { fmt } from '../format';
import { LAB, OPT, cellKey, find, type Resolved, type Row, type State } from './model';

export type Seg = string | { v: string; src: string };
export interface Note { tone: 'change' | 'compare' | 'fact' | 'caution'; head: string; body: Seg[]; keep?: boolean }

type Ok = Extract<Resolved, { ok: true }>;
const side = (S: State) => (S.sample === 'heldout' ? 'held' : 'disc');
export const cellSrc = (S: State, pid: string) => `${LAB.grid_src[side(S)]} [${cellKey(pid, S.fill, S.latency, S.fee)}]`;
const n = (v: number | null | undefined, d: number, signed: boolean, src: string): Seg => ({ v: fmt(v, d, signed) ?? 'undefined', src });
const row = (r: Ok, pid: string) => r.rows.find((x) => x.p.id === pid)!;
const MS: Record<string, number> = { tokyo: 2, regional: 30, distant: 115 };
const rec = (id: string) => core.values[id];

/** Ratio of two turnovers in words, for explanation only (labelled as computed on this page). */
export function share(a: number, b: number): string {
  const q = a / b;
  if (q > 0.9 && q < 1.1) return 'about the same as';
  if (q < 1) {
    const parts: Array<[number, string]> = [[0.04, 'under a twentieth of'], [0.08, 'about a twentieth of'], [0.12, 'about a tenth of'], [0.15, 'about a seventh of'], [0.18, 'about a sixth of'], [0.24, 'about a fifth of'], [0.29, 'about a quarter of'], [0.37, 'about a third of'], [0.45, 'about two fifths of'], [0.58, 'about half of'], [0.7, 'about two thirds of'], [0.8, 'about three quarters of'], [0.9, 'about four fifths of']];
    return parts.find(([lim]) => q < lim)?.[1] ?? 'about nine tenths of';
  }
  if (q < 1.75) return 'about one and a half times';
  if (q < 2.5) return 'about twice';
  const W = ['', '', '', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'];
  const k = Math.round(q);
  return k <= 10 ? `about ${W[k]} times` : 'more than ten times';
}

function traded(x: Row) { return x.kind === 'traded'; }

/** The comparison between the focused policy and its comparator, in the current scenario. */
export function compare(S: State, r: Ok): Note[] {
  const F = row(r, S.focus), C = row(r, S.vs);
  const out: Note[] = [];
  if (S.focus === 'NT') return [{ tone: 'compare', head: 'NT never quotes', body: ['The no-trade baseline sits at zero on every measure. Every other policy is judged against it: a policy is worth running only if it beats zero after fees.'] }];
  if (!traded(F)) {
    const body: Seg[] = [`${F.p.code} never quoted in this scenario, so its turnover is zero and its zero result is mechanical. Not trading avoids the loss; it does not show that the strategy would earn money.`];
    if (F.p.feeAware && S.fee === 'vip0') body.push(' Its gate requires half the spread plus the forecast to exceed the maker fee. At VIP0 the fee is about 8 to 17 ticks, against a forecast of about one tick or less, so the condition was never met.');
    return [{ tone: 'compare', head: `${F.p.code} does not trade here`, body }];
  }
  if (S.focus === S.vs || !traded(C)) {
    return [{
      tone: 'compare', head: `${F.p.code} in this scenario`,
      body: [
        `${F.p.code} trades `, n(F.v.turnover_per_hour, 0, false, cellSrc(S, F.p.id)), ' USDT of SOL per hour and ', (F.v.net_per_hour ?? 0) < 0 ? 'loses ' : 'makes ',
        n(Math.abs(F.v.net_per_hour ?? 0), 1, false, cellSrc(S, F.p.id)), ' USDT per hour: ', n(F.v.net_bp_per_notional, 2, true, cellSrc(S, F.p.id)),
        ` bp of every unit traded. ${S.vs === S.focus ? 'Choose a different comparison policy to see the difference between two rules.' : `${C.p.code} does not trade here, so there is nothing to compare per unit traded.`}`,
      ],
    }];
  }
  const nf = F.v.net_per_hour!, nc = C.v.net_per_hour!, bf = F.v.net_bp_per_notional!, bc = C.v.net_bp_per_notional!;
  const tf = F.v.turnover_per_hour!, tc = C.v.turnover_per_hour!;
  const less = nf > nc;
  const verb = (v: number) => (v < 0 ? 'loses' : 'makes');
  const body: Seg[] = [
    `${F.p.code} ${verb(nf)} `, n(Math.abs(nf), 1, false, cellSrc(S, F.p.id)), ` USDT per hour; ${C.p.code} ${verb(nc)} `, n(Math.abs(nc), 1, false, cellSrc(S, C.p.id)), '. ',
    `It trades ${share(tf, tc)} ${C.p.code}’s notional (`, n(tf, 0, false, cellSrc(S, F.p.id)), ' against ', n(tc, 0, false, cellSrc(S, C.p.id)), ' USDT/h), ',
    'and per unit traded its net result is ', n(bf, 2, true, cellSrc(S, F.p.id)), ' bp against ', n(bc, 2, true, cellSrc(S, C.p.id)), ' bp.',
  ];
  const close = Math.abs(bf - bc) < 1;
  if (close && Math.abs(tf / tc - 1) > 0.25) body.push(' Per unit traded the two are within ', { v: fmt(Math.abs(bf - bc), 2)!, src: `computed on this page: difference of ${cellSrc(S, F.p.id)} and ${cellSrc(S, C.p.id)}` }, ' bp of each other, so the gap in hourly loss comes mainly from how much each trades, not from a better result per unit traded.');
  out.push({ tone: 'compare', head: `${F.p.code} against ${C.p.code}`, body });
  if (less && tf < tc) {
    out.push({
      tone: 'caution', head: 'A smaller loss is not better fills',
      body: [
        'Trading less loses less when every unit traded loses. The pre-registered test of fill quality per unit traded (H1-T, P3[M2] against its placebo) found ',
        n(rec('e003.h1t.held').v, 2, true, rec('e003.h1t.held').src), ' bp on the held-out sessions, with a descriptive interval of [', n(rec('e003.h1t.held_tlo').v, 2, true, rec('e003.h1t.held_tlo').src), ', ',
        n(rec('e003.h1t.held_thi').v, 2, true, rec('e003.h1t.held_thi').src), '] that spans zero; the placebo was not matched on turnover.',
      ],
    });
  }
  return out;
}

/** Notes about what just changed between two states. Only the keys that changed produce a note. */
export function changes(P: State, S: State, rp: Resolved, r: Ok): Note[] {
  const out: Note[] = [];
  const F = row(r, S.focus);
  const pf = rp.ok ? row(rp, S.focus) : null;
  const pair = (metric: 'turnover_per_hour' | 'net_bp_per_notional', d: number, signed: boolean): Seg[] => (pf && traded(pf) && traded(F) ? [n(pf.v[metric], d, signed, cellSrc(P, F.p.id)), ' → ', n(F.v[metric], d, signed, cellSrc(S, F.p.id))] : []);
  const stats = (): Seg[] => (pf && traded(pf) && traded(F) ? [` ${F.p.code}: turnover `, ...pair('turnover_per_hour', 0, false), ' USDT/h; net per unit traded ', ...pair('net_bp_per_notional', 2, true), ' bp.'] : []);

  if (P.sample !== S.sample) {
    if (S.sample === 'heldout') {
      const d = LAB.grid.disc[cellKey(F.p.id, S.fill, S.latency, S.fee)];
      out.push({
        tone: 'change', head: 'Now showing the five held-out sessions',
        body: [
          'June to October 2026: sealed until every rule was fixed, then evaluated once. Policy values here are ', `“${LAB.held_label}”. `,
          ...(traded(F) && d && d[4] ? [`${F.p.code} loses `, n(-(F.v.net_per_hour ?? 0), 1, false, cellSrc(S, F.p.id)), ' USDT/h here against ', n(-(d[0] ?? 0), 1, false, cellSrc({ ...S, sample: 'discovery' }, F.p.id)), ' in discovery, but it also traded less (', n(F.v.turnover_per_hour, 0, false, cellSrc(S, F.p.id)), ' against ', n(d[4], 0, false, cellSrc({ ...S, sample: 'discovery' }, F.p.id)), ' USDT/h), so compare results per unit traded, not per hour.'] as Seg[] : []),
        ],
      });
    } else {
      out.push({ tone: 'change', head: 'Now showing the ten discovery sessions', body: ['August 2025 to May 2026, evaluated walk-forward: each session’s forecasts were fitted only on earlier sessions. Discovery is where every pre-registered decision was made; its means carry 95% session-bootstrap intervals.'] });
    }
  }
  if (P.fee !== S.fee) {
    const a = find(OPT.fee, P.fee)!, b = find(OPT.fee, S.fee)!;
    const body: Seg[] = [];
    if (F.p.id === 'NT') body.push('NT never quotes, so no fee applies to it.');
    else if (!F.p.feeAware) {
      if (pf && traded(pf) && traded(F) && pf.v.turnover_per_hour === F.v.turnover_per_hour) {
        body.push(`${F.p.code} ignores fees, so its simulated fills are identical under both schedules (turnover `, n(F.v.turnover_per_hour, 0, false, cellSrc(S, F.p.id)), ' USDT/h); only the fee charged on them changed. Net per unit traded moved from ', ...pair('net_bp_per_notional', 2, true).slice(0, 1), ' to ', n(F.v.net_bp_per_notional, 2, true, cellSrc(S, F.p.id)), ' bp.');
      } else body.push(...stats());
    } else {
      body.push(`${F.p.code} compares its forecast with the maker fee before it quotes, so it was simulated separately under each schedule: its trading itself changes, not only the fee. `);
      if (pf) body.push('Turnover ', n(pf.v.turnover_per_hour, 0, false, cellSrc(P, F.p.id)), ' → ', n(F.v.turnover_per_hour, 0, false, cellSrc(S, F.p.id)), ' USDT/h.');
      if (!traded(F)) body.push(` Under ${b.label} its gate never opens.`);
    }
    const lose = r.rows.filter(traded);
    if (lose.length) body.push(lose.every((x) => (x.v.net_per_hour ?? 0) < 0) ? ' Every policy that trades still loses money on average.' : ' Not every policy that trades loses money on average under this schedule.');
    out.push({ tone: 'change', head: `Fee schedule: ${a.label} → ${b.label}`, body });
  }
  if (P.fill !== S.fill) {
    const a = find(OPT.fill, P.fill)!, b = find(OPT.fill, S.fill)!;
    out.push({ tone: 'change', head: `Fill model: ${a.label} → ${b.label}`, body: ['The historical market is identical. Only the assumption about our place in the queue changed, which changes which simulated orders count as filled. It is an assumption about the queue, not evidence of what live fills would have been.', ...stats()] });
  }
  if (P.latency !== S.latency) {
    const a = find(OPT.latency, P.latency)!, b = find(OPT.latency, S.latency)!;
    const body: Seg[] = [`Our simulated orders now reach the exchange ${MS[S.latency]} ms after each decision, against ${MS[P.latency]} ms before; depth updates still arrive in 100 ms batches.`, ...stats()];
    if (pf && traded(pf) && traded(F) && MS[S.latency] < MS[P.latency] && F.v.turnover_per_hour! > pf.v.turnover_per_hour! && F.v.net_bp_per_notional! < pf.v.net_bp_per_notional!) {
      body.push(' Faster meant more fills and a slightly worse result per unit traded, consistent with the paper’s E002 finding that the fills lower latency adds are more adverse.');
    }
    out.push({ tone: 'change', head: `Latency: ${a.label} → ${b.label}`, body });
  }
  return out;
}

/** Standing facts about the current scenario. */
export function facts(S: State, r: Ok): Note[] {
  const out: Note[] = [];
  const abst = r.rows.filter((x) => x.kind === 'abstained').map((x) => x.p.code);
  if (abst.length && S.focus !== 'P3F' && S.focus !== 'P4') out.push({ tone: 'fact', head: `${abst.join(' and ')} ${abst.length > 1 ? 'abstain' : 'abstains'}`, body: ['Their gates never opened in this scenario, so their zero is mechanical, not a result.'] });
  const fe = find(OPT.fee, S.fee)!;
  if (fe.attain === 'hypothetical') out.push({ tone: 'caution', keep: true, head: `${fe.label} is hypothetical`, body: ['A participant like us cannot attain this fee schedule. Read the values as a what-if about fees, not as an achievable result.'] });
  if (S.sample === 'heldout') out.push({ tone: 'fact', keep: true, head: 'Held-out values carry no confirmation claim', body: [`“${LAB.held_label}”: the protocol set no test rule for these policy results. Five sessions give little statistical power.`] });
  return out;
}

/** Everything the panel shows: what changed (if anything), the comparison, then standing facts. */
export function explain(prev: { S: State; r: Resolved } | null, S: State, r: Resolved): Note[] {
  if (!r.ok) return [];
  const ch = prev ? changes(prev.S, S, prev.r, r) : [];
  return [...ch, ...compare(S, r), ...facts(S, r)];
}

/** Plain text of a note, for tests and accessible summaries. */
export const text = (x: Note) => `${x.head}. ${x.body.map((s) => (typeof s === 'string' ? s : s.v)).join('')}`;
