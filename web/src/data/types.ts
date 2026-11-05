// Shapes of the bundles written by web/export/build_bundle.py.
export type Sample = 'discovery' | 'discovery_walkforward' | 'heldout' | 'parameter' | 'paper';

export interface Rec {
  v: number | null;
  u: string;
  d: number;
  st: string;
  smp: Sample;
  src: string;
  s?: boolean;
  pct?: boolean;
  lab?: string;
  printed?: string;
  frag?: string;
  note?: string;
  scale?: number;
  sessions?: Record<string, number>;
}

export interface FeeRange {
  id: string;
  label: string;
  status: 'attainable' | 'hypothetical';
  cfg_label: string;
  by_fill: Record<string, number>;
  lo: number;
  hi: number;
  src: string;
  op: string;
}

export interface MatrixRow {
  policy: string; fill: string; latency: string;
  disc: number; disc_lo: number; disc_hi: number; disc_n: number;
  held: number; held_n: number; src_disc: string; src_held: string;
}

export interface PolicyRow {
  policy: string; code: string;
  disc_net: number; disc_lo: number; disc_hi: number; disc_turnover: number; disc_pos: number;
  held_net: number; held_turnover: number; held_gross: number; held_maker: number; held_taker: number;
  held_with_trades: number; held_sessions: Record<string, number>;
  src_disc: string; src_held: string;
}

export interface SkillRow { side: 'disc' | 'held'; model: string; h: number; r2: number; ic: number; hit: number; src: string; smp: Sample }

export interface LabelRow {
  exp: string; id: string; title: string; status: string; rule?: string;
  discovery: { ids?: string[]; text?: string };
  heldout: { ids?: string[]; text?: string };
  label: string; interpretation?: string | null; comment?: string | null;
  kind: 'check' | 'secondary' | 'reported'; src?: string;
}

export interface Core {
  values: Record<string, Rec>;
  e001: { held_sessions: Record<string, Record<string, number>>; tally: string; family: string };
  e002: { fees: FeeRange[]; matrix: MatrixRow[]; status: string; heldout_label: string; note: string };
  e003: { skill: SkillRow[]; policies_vip0: PolicyRow[]; tally: string; policies_status: string; policies_note: string };
  e004: Record<string, unknown> & { tally: string; scope_note: string; yview: { row_label: string; note: string; secondary: boolean }; h40_label: string };
  holdout: {
    ledger: Array<Record<string, unknown>>; attempt: number; freeze_record_sha256: string;
    relative_tick_bp: Record<string, number>; tallies: Record<string, string | null>;
    not_refutation: string; fee_attainability: string; sessions: string[];
  };
  labels: LabelRow[];
  sample: { latency_labels: Record<string, string>; splits: Record<'train' | 'validation' | 'test', string[]>; splits_src: string; walkforward: string[] };
  paper: { files: Array<{ title: string; path: string; file: string; sha256: string; bytes: number }>; frozen: Array<{ path: string; sha256: string }>; frozen_src: string };
  meta: { sources: Record<string, string>; note: string };
}
