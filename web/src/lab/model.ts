// Scenario Lab model: tested cells, the closed set of unavailable states, URL state and presets.
// Ported from design/proposals/a-refined/lab.js. It derives no statistics and never interpolates: a selection either
// names a tested cell of the frozen grid or resolves to one explicit unavailable state.
import labRaw from '../data/lab.json';

export interface LabData {
  metrics: string[];
  policies: string[];
  codes: Record<string, string>;
  fees: Record<string, string>;
  fee_status: Record<string, 'attainable' | 'hypothetical'>;
  grid: { disc: Record<string, (number | null)[]>; held: Record<string, (number | null)[]> };
  grid_src: { disc: string; held: string };
  disc_sessions: Record<string, Record<string, [number | null, number | null]>>;
  disc_sessions_src: string;
  disc_ci_primary_vip0: Record<string, { lo: number; hi: number }>;
  disc_ci_src: string;
  held_sessions_primary_vip0: Record<string, Record<string, number>>;
  held_sessions_src: string;
  held_label: string;
  e004: {
    status: string; held_label: string; src_disc: string; src_held: string;
    disc_window: Record<string, { D_W_bp: { mean: number; ci95?: number[]; defined: number; positive: number }; withdrawn_share_mean: number }>;
    held_window: Record<string, { D_W_bp: { mean: number; defined: number; positive: number }; withdrawn_share_mean: number }>;
    disc_contrasts: Record<string, Record<string, Record<string, { mean: number; ci95?: number[]; defined: number; positive: number }>>>;
    held_contrasts: Record<string, Record<string, Record<string, { mean: number; defined: number; positive: number }>>>;
  };
  untested: Record<string, string>;
}

export const LAB = labRaw as unknown as LabData;

export type Key = 'view' | 'sample' | 'fill' | 'latency' | 'fee' | 'limits' | 'metric' | 'focus' | 'vs';
export type State = Record<Key, string>;
export interface Opt { id: string; label: string; small?: string; un?: Reason; why?: string; attain?: 'attainable' | 'hypothetical' }
export type Reason = 'not_tested' | 'not_varied' | 'heldout_not_in_frozen_analysis' | 'not_exported' | 'unknown_value';

export const REASON: Record<Reason, string> = {
  not_tested: 'Not tested',
  not_varied: 'Not varied',
  heldout_not_in_frozen_analysis: 'Not part of the held-out evaluation',
  not_exported: 'Not published',
  unknown_value: 'Unknown value',
};

export const POL: Array<{ id: string; code: string; name: string; does: string; feeAware: boolean }> = [
  { id: 'NT', code: 'NT', name: 'No trade (baseline)', feeAware: false,
    does: 'Never quotes. It is the baseline every other policy must beat: zero turnover, zero result.' },
  { id: 'P0', code: 'P0', name: 'Fixed quoting at the touch', feeAware: false,
    does: 'Always quotes one SOL on both sides at the best bid and ask, and re-quotes whenever the best price changes. The simplest passive market maker.' },
  { id: 'P1', code: 'P1', name: 'P0 with inventory withdrawal', feeAware: false,
    does: 'Like P0, but stops quoting the side that would add to its position once it holds 3 SOL or more in either direction.' },
  { id: 'P3_M1', code: 'P3[M1]', name: 'Forecast-gated, touch imbalance', feeAware: false,
    does: 'Quotes a side only while a one-feature forecast (order-book imbalance at the best prices) does not predict a move through that quote larger than half the spread. Ignores fees.' },
  { id: 'P3_M2', code: 'P3[M2]', name: 'Forecast-gated, eight features', feeAware: false,
    does: 'The same gate as P3[M1], using the eight-feature five-second forecast. Ignores fees.' },
  { id: 'P3_negM2', code: 'P3[−M2]', name: 'Placebo: gate in the wrong direction', feeAware: false,
    does: 'A placebo: the same gate with the forecast’s sign reversed. It withdraws about as often as P3[M2] but on the wrong side, keeping exactly the quote the coming move will fill. Its turnover is not matched to P3[M2]’s.' },
  { id: 'P3F', code: 'P3F', name: 'Forecast- and fee-aware', feeAware: true,
    does: 'Quotes only when half the spread plus the forecast exceeds the maker fee. Because it depends on the fee, it is simulated separately under each fee schedule.' },
  { id: 'P4', code: 'P4', name: 'P3F with risk controls', feeAware: true,
    does: 'P3F plus inventory skew, withdrawal at 3 SOL and a volatility gate: the risk controls tested by H3.' },
];

export const OPT: Record<'sample' | 'fill' | 'latency' | 'fee' | 'limits', Opt[]> = {
  sample: [{ id: 'discovery', label: 'Discovery', small: '10 sessions' }, { id: 'heldout', label: 'Held-out', small: '5 sessions' }],
  fill: [
    { id: 'conservative', label: 'Conservative' },
    { id: 'intermediate', label: 'Intermediate', small: 'primary' },
    { id: 'optimistic', label: 'Optimistic' },
    { id: 'naive', label: 'Naive', small: 'not tested', un: 'not_tested', why: LAB.untested.fill_naive },
  ],
  latency: [
    { id: 'tokyo', label: 'Tokyo-hosted', small: '2 ms' },
    { id: 'regional', label: 'Regional', small: '30 ms, primary' },
    { id: 'distant', label: 'Distant', small: '115 ms' },
  ],
  fee: [
    { id: 'vip0', label: 'VIP0', small: 'attainable', attain: 'attainable' },
    { id: 'vip9', label: 'VIP9', small: 'hypothetical', attain: 'hypothetical' },
    { id: 'lp_tier4', label: 'LP tier 4', small: 'hypothetical', attain: 'hypothetical' },
    { id: 'vip0_bnb', label: 'VIP0 + BNB', small: 'not tested', attain: 'hypothetical', un: 'not_tested', why: LAB.untested.fee_untested },
    { id: 'lp_tier1', label: 'LP tier 1', small: 'not tested', attain: 'hypothetical', un: 'not_tested', why: LAB.untested.fee_untested },
  ],
  limits: [
    { id: 'fixed', label: 'As tested', small: 'fixed per policy' },
    { id: 'other', label: 'Other', small: 'not varied', un: 'not_varied', why: LAB.untested.limits },
  ],
};

export interface Metric { id: string; label: string; unit: string; d: number; signed?: boolean; pct?: boolean; sess?: number }
export const METRIC: Metric[] = [
  { id: 'net_per_hour', label: 'Net per hour', unit: 'USDT/h', d: 1, signed: true, sess: 0 },
  { id: 'net_bp_per_notional', label: 'Net per notional', unit: 'bp', d: 2, signed: true },
  { id: 'turnover_per_hour', label: 'Turnover', unit: 'USDT/h', d: 0, sess: 1 },
  { id: 'gross_per_hour', label: 'Gross per hour', unit: 'USDT/h, fee-free', d: 1, signed: true },
  { id: 'gross_bp_per_notional', label: 'Gross per notional', unit: 'bp, fee-free', d: 2, signed: true },
  { id: 'max_drawdown', label: 'Maximum drawdown', unit: 'USDT', d: 0 },
  { id: 'inc_es', label: 'Expected shortfall, 5 min', unit: 'USDT', d: 1 },
  { id: 'tw_abs_inventory_avg', label: 'Average |inventory|', unit: 'SOL', d: 2 },
  { id: 'max_abs_inventory', label: 'Maximum |inventory|', unit: 'SOL', d: 2 },
  { id: 'quote_presence_both', label: 'Two-sided quote presence', unit: '', d: 1, pct: true },
  { id: 'fill_rate', label: 'Fill rate', unit: '', d: 1, pct: true },
  { id: 'own_markout_1s_bp', label: 'Own markout, 1 s', unit: 'bp', d: 2, signed: true },
  { id: 'own_markout_5s_bp', label: 'Own markout, 5 s', unit: 'bp', d: 2, signed: true },
  { id: 'own_markout_30s_bp', label: 'Own markout, 30 s', unit: 'bp', d: 2, signed: true },
];

export const DEF: State = { view: 'e003', sample: 'discovery', fill: 'intermediate', latency: 'regional', fee: 'vip0', limits: 'fixed', metric: 'net_per_hour', focus: 'P3_M2', vs: 'P0' };

// Starting scenarios are named for what they set, never ranked as "best" or "most favourable".
export const PRESETS: Record<string, { label: string; small: string; set: Partial<State> }> = {
  primary: { label: 'Pre-registered primary scenario', small: 'intermediate fill, regional latency, VIP0', set: { sample: 'discovery', fill: 'intermediate', latency: 'regional', fee: 'vip0', limits: 'fixed' } },
  optimistic: { label: 'Optimistic fill model, Tokyo latency', small: 'the most generous queue assumption, fastest bracket', set: { sample: 'discovery', fill: 'optimistic', latency: 'tokyo', fee: 'vip0', limits: 'fixed' } },
  rebate: { label: 'Hypothetical maker rebate', small: 'LP tier 4, not attainable', set: { sample: 'discovery', fill: 'intermediate', latency: 'regional', fee: 'lp_tier4', limits: 'fixed' } },
  holdout: { label: 'Five held-out sessions', small: 'evaluated once, primary scenario', set: { sample: 'heldout', fill: 'intermediate', latency: 'regional', fee: 'vip0', limits: 'fixed' } },
};

export const find = (list: Opt[], id: string) => list.find((o) => o.id === id);

const LISTS: Record<Key, string[]> = {
  view: ['e003', 'e002', 'e004'],
  sample: OPT.sample.map((o) => o.id),
  fill: OPT.fill.map((o) => o.id),
  latency: OPT.latency.map((o) => o.id),
  fee: OPT.fee.map((o) => o.id),
  limits: OPT.limits.map((o) => o.id),
  metric: METRIC.map((m) => m.id),
  focus: POL.map((p) => p.id),
  vs: POL.map((p) => p.id),
};

/** Parse a URL hash. Unknown values are reported, never replaced by a tested cell (Review Focus 1). */
export function parseHash(hash: string): { state: State; bad: string[] } {
  const state: State = { ...DEF };
  const bad: string[] = [];
  hash.replace(/^#/, '').split('&').forEach((kv) => {
    if (!kv) return;
    const [k0, v0 = ''] = kv.split('=');
    const k = decodeURIComponent(k0) as Key;
    const v = decodeURIComponent(v0);
    if (!(k in DEF)) return;
    if (LISTS[k].includes(v)) state[k] = v;
    else bad.push(`${k} = ${v}`);
  });
  return { state, bad };
}

export function serialize(s: State): string {
  return '#' + (Object.keys(DEF) as Key[]).map((k) => `${k}=${encodeURIComponent(s[k])}`).join('&');
}

export const cellKey = (p: string, fill: string, lat: string, fee: string) => (p === 'NT' ? `NT|none|none|${fee}` : `${p}|${fill}|${lat}|${fee}`);

export interface Row {
  p: (typeof POL)[number];
  v: Record<string, number | null>;
  kind: 'baseline' | 'abstained' | 'traded';
  sess: Record<string, [number | null, number | null]> | null;
}
export type Resolved =
  | { ok: true; rows: Row[]; fee: Opt; fill: Opt; lat: Opt }
  | { ok: false; reason: Reason; which: string; why: string; k?: 'fill' | 'fee' | 'limits' };

export function resolve(S: State, bad: string[]): Resolved {
  if (bad.length) return { ok: false, reason: 'unknown_value', which: `Link value ${bad.join(', ')}`, why: 'the link names a value that is not one of the options on this page' };
  const f = find(OPT.fill, S.fill)!, fe = find(OPT.fee, S.fee)!, li = find(OPT.limits, S.limits)!;
  if (f.un) return { ok: false, reason: f.un, which: `${f.label} fill model`, why: f.why!, k: 'fill' };
  if (fe.un) return { ok: false, reason: fe.un, which: `${fe.label} fee schedule`, why: fe.why!, k: 'fee' };
  if (li.un) return { ok: false, reason: li.un, which: 'Inventory limits other than the policies’ fixed ones', why: li.why!, k: 'limits' };
  const side = S.sample === 'heldout' ? 'held' : 'disc';
  const rows: Row[] = POL.map((p) => {
    const key = cellKey(p.id, S.fill, S.latency, S.fee);
    const arr = LAB.grid[side][key];
    if (!arr) throw new Error(`missing tested cell ${key}`);
    const v = Object.fromEntries(LAB.metrics.map((m, i) => [m, arr[i]])) as Record<string, number | null>;
    const kind: Row['kind'] = p.id === 'NT' ? 'baseline' : v.turnover_per_hour === 0 ? 'abstained' : 'traded';
    return { p, v, kind, sess: side === 'disc' ? LAB.disc_sessions[key] ?? null : null };
  });
  return { ok: true, rows, fee: fe, fill: f, lat: find(OPT.latency, S.latency)! };
}

export const isPrimary = (S: State) => S.fill === 'intermediate' && S.latency === 'regional' && S.fee === 'vip0';
