'use client';
// Explore: the Scenario Lab. A six-step guided story (the default) and a full lab over the frozen, precomputed grid. The
// Lab selects tested cells; it simulates nothing, never interpolates, and explains each change from frozen values and
// paper statements.
import { useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { Help, Inspect } from '../components/Explain';
import { Footer } from '../components/Layout';
import { Sized } from '../components/Sized';
import { Tag, Tags } from '../components/Tag';
import { useEnter, useMedia, useMounted, useWidth } from '../components/hooks';
import { QueueModels, QuoteFill, SkillCloud, StaleWindow } from '../charts/teach';
import { HeldSplit, SkillBars, SpreadPath, TradeLess } from '../charts/home';
import { Held, N } from '../components/N';
import { core, rec } from '../data/core';
import { axisLab, fmt, nice, pct } from '../format';
import { explain, type Note, type Seg } from '../lab/explain';
import {
  DEF, LAB, METRIC, OPT, POL, PRESETS, REASON, cellKey, find, isPrimary, parseHash, resolve, serialize,
  type Key, type Metric, type Opt, type Resolved, type Row, type State,
} from '../lab/model';
import { share } from '../lab/explain';

type Ok = Extract<Resolved, { ok: true }>;
const MAKER = (id: string) => core.values[`fee.${id}.maker`]?.v ?? null;
const TAKER = (id: string) => core.values[`fee.${id}.taker`]?.v ?? null;
const sideOf = (S: State) => (S.sample === 'heldout' ? 'held' : 'disc');
const src = (S: State, pid: string) => `${LAB.grid_src[sideOf(S)]} [${cellKey(pid, S.fill, S.latency, S.fee)}]`;

function show(m: Metric, v: number | null | undefined) {
  if (v === null || v === undefined) return null;
  return m.pct ? pct(v, 1) : fmt(v, m.d, m.signed);
}

/** An axis domain that includes zero and ends on a tick, so the data fill the chart. */
function domain(vals: number[]): { lo: number; hi: number; step: number; ticks: number[] } {
  const a = Math.min(0, ...vals), b = Math.max(0, ...vals);
  const step = nice((b - a || 1) / 4);
  const lo = Math.floor(a / step - 1e-9) * step, hi = Math.ceil(b / step + 1e-9) * step || step;
  const ticks: number[] = [];
  for (let t = lo; t <= hi + 1e-9; t += step) ticks.push(Math.abs(t) < 1e-9 ? 0 : +t.toPrecision(6));
  return { lo, hi, step, ticks };
}

function Segs({ s }: { s: Seg[] }) {
  return <>{s.map((x, i) => (typeof x === 'string' ? <span key={i}>{x}</span> : <b key={i} className="num" data-src={x.src}>{x.v}</b>))}</>;
}

const feeTag = (fe: Opt) => (fe.attain === 'attainable' ? <Tag kind="att">{fe.label}, attainable</Tag> : <Tag kind="hyp">{fe.label}, hypothetical</Tag>);

/* ------------------------------------------------------------------ point-of-use explanations */
const HELP: Record<string, ReactNode> = {
  policy: <><p>A policy is a fixed rule for when to quote. All eight quote one SOL at the best price or not at all, and keep their position within ±10 SOL. Choose one to highlight and one to compare it with; clicking a row in the comparison also highlights it.</p></>,
  sample: <><p><b>Discovery</b>: ten walk-forward sessions, August 2025 to May 2026, where each pre-registered decision was made. Each session’s forecasts were fitted only on earlier sessions.</p><p><b>Held-out</b>: five later sessions, June to October 2026, sealed until every rule was fixed, then evaluated once. A result that appears only in the data used to design it may not survive new data; the holdout is that check. Its policy values are descriptive.</p></>,
  fill: <><p>Market data show how much is resting at each price, but not where our order would stand in the queue. When an order is cancelled, nobody knows whether it was ahead of us or behind.</p><p><b>Conservative</b>: cancellations come from behind us. <b>Intermediate</b> (primary): pro rata. <b>Optimistic</b>: from ahead first, and our order also fills when the price trades through it. Only which simulated orders count as filled changes; the market replay is identical. <b>Naive</b> was an E002 reference only.</p></>,
  latency: <><p>How long our simulated orders take to reach the exchange, and how long until we learn of a fill: <b>Tokyo-hosted</b> 2 ms, next to the exchange; <b>regional</b> 30 ms; <b>distant</b> 115 ms. Faster participants join queues and cancel stale quotes sooner. Depth updates arrive in 100 ms batches in every bracket.</p></>,
  fee: <><p>The exchange charges a fee on every fill. <b>VIP0</b>, 10 bp maker and taker (a tenth of one percent), is the standard schedule and the only one a participant like us can attain. Lower tiers and maker rebates are tied to very large trading volume or to market-maker programmes, so they are <b>hypothetical</b> here: what-ifs that show how much of the result is the fee.</p><p>Fee-unaware policies trade identically under every schedule; only the fee charged changes. P3F and P4 decide using the fee, so they were simulated per schedule. VIP0 + BNB and LP tier 1 were run for E002 only.</p></>,
  limits: <><p>Every policy keeps its position within ±10 SOL; P1 and P4 also stop adding at 3 SOL. These limits were fixed in advance and never varied, so no other setting has a result.</p></>,
  metric: <><p><b>Net</b> is after fees, <b>gross</b> before. <b>Per hour</b> is USDT per valid hour; <b>per notional</b> is basis points (hundredths of a percent) of the amount traded, which removes the effect of trading more or less. <b>Turnover</b> is USDT of SOL traded per hour. <b>Expected shortfall</b>: the mean of the worst 5% of five-minute changes in wealth. <b>Drawdown</b>: the largest fall from a peak. <b>Fill rate</b>: filled quantity over quoted quantity. <b>Own markout</b>: our fills marked to the mid 1, 5 or 30 s later; negative means the price moved against the fill.</p></>,
};

/* ------------------------------------------------------------------ "What changed, and why?" */
function NoteItem({ n }: { n: Note }) {
  return (
    <li className={`nt nt-${n.tone}`}>
      <span className="nt-k" aria-hidden="true">{n.tone === 'change' ? 'Changed' : n.tone === 'compare' ? 'Compare' : n.tone === 'caution' ? 'Caution' : 'Note'}</span>
      <p><b className="nt-h">{n.head}.</b> <Segs s={n.body} /></p>
    </li>
  );
}

/** Leads with what just changed; the standing comparison and cautions move into a "Context" disclosure once something
 *  has changed, except the cautions that must stay visible (hypothetical fees, held-out status). */
function Readout({ notes, first }: { notes: Note[]; first: boolean }) {
  const ch = notes.filter((n) => n.tone === 'change');
  const shown = [...(ch.length ? ch : notes.filter((n) => n.tone === 'compare').slice(0, 1)), ...notes.filter((n) => n.keep)];
  const rest = notes.filter((n) => !shown.includes(n));
  return (
    <section className="readout" aria-labelledby="ro-h">
      <div className="readout-h">
        <h2 id="ro-h">What changed, and why?</h2>
        {first && <p>Change a setting and this panel explains what moved, and why.</p>}
      </div>
      <ul className={`notes${ch.length ? ' has-change' : ''}`} aria-live="polite">
        {shown.map((n, i) => <NoteItem key={`${n.head}${i}`} n={n} />)}
      </ul>
      {rest.length > 0 && (
        <details className="ctx">
          <summary>More context ({rest.length})</summary>
          <ul className="notes">{rest.map((n, i) => <NoteItem key={`${n.head}${i}`} n={n} />)}</ul>
        </details>
      )}
    </section>
  );
}

function Unavailable({ r, set }: { r: Extract<Resolved, { ok: false }>; set: (p: Partial<State>) => void }) {
  const alts = r.k ? OPT[r.k].filter((o) => !o.un) : [];
  return (
    <section className="readout unav" data-unavailable={r.reason} aria-labelledby="un-h">
      <div className="readout-h"><h2 id="un-h">No result for this combination</h2></div>
      <p className="more"><b>{REASON[r.reason]}.</b> {r.which}: {r.why}.</p>
      {alts.length > 0 && (
        <>
          <p className="more mt-3">Tested options for this setting:</p>
          <div className="seg mt-2">
            {alts.map((o) => <button key={o.id} type="button" className="chip" onClick={() => set({ [r.k!]: o.id })}>{o.label}{o.small && <span className="ink-3"> · {o.small}</span>}</button>)}
          </div>
        </>
      )}
      <p className="closed">The Lab shows only what the study tested. It never estimates a value between tested settings.</p>
    </section>
  );
}

/* ------------------------------------------------------------------ focus against comparator: gross, fees, net */
function Breakdown({ r, S, W, unit }: { r: Ok; S: State; W: number; unit: 'hour' | 'bp' }) {
  const g = unit === 'hour' ? 'gross_per_hour' : 'gross_bp_per_notional', n = unit === 'hour' ? 'net_per_hour' : 'net_bp_per_notional';
  const rows = [S.focus, S.vs].filter((p, i, a) => a.indexOf(p) === i).map((p) => r.rows.find((x) => x.p.id === p)!);
  const { lo, hi, ticks } = domain(rows.flatMap((x) => (x.kind === 'traded' ? [x.v[g]!, x.v[n]!] : [])));
  const l = W < 480 ? 64 : 84, rr = 14, rowH = 78, top = 20, H = top + rowH * rows.length + 22;
  const X = (v: number) => l + ((v - lo) / (hi - lo)) * (W - l - rr);
  const ho = S.sample === 'heldout';
  const u = unit === 'hour' ? 'USDT/h' : 'bp', d = unit === 'hour' ? 1 : 2;
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Gross result, fees and net result ${unit === 'hour' ? 'per hour' : 'per unit traded'} for ${rows.map((x) => x.p.code).join(' and ')}`} data-src={rows.map((x) => src(S, x.p.id)).join('; ')}>
      <defs>
        <pattern id="rebate-hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect className="stale-bg" width="5" height="5" /><line className="stale-ln" x1="0" y1="0" x2="0" y2="5" />
        </pattern>
      </defs>
      <text x={W - rr} y={12} textAnchor="end">{u}</text>
      {ticks.map((t) => <g key={t}><line className={t === 0 ? 'zero' : 'grid'} x1={X(t)} x2={X(t)} y1={top - 2} y2={H - 20} /><text className="t-num" x={X(t)} y={H - 5} textAnchor="middle">{axisLab(t)}</text></g>)}
      {rows.map((x, i) => {
        const y = top + i * rowH;
        const label = <text className="t-ink t-bold t-id" x={l - 10} y={y + 22} textAnchor="end">{x.p.code}</text>;
        if (x.kind !== 'traded') return <g key={x.p.id}>{label}<text className="t-ink2" x={X(0) + 8} y={y + 22}>{x.kind === 'baseline' ? 'never quotes' : 'does not trade: a mechanical zero'}</text></g>;
        const gv = x.v[g]!, nv = x.v[n]!, fee = gv - nv;
        const a = Math.min(X(0), X(gv)), b = Math.max(X(0), X(gv));
        const fa = Math.min(X(gv), X(nv)), fb = Math.max(X(gv), X(nv));
        return (
          <g key={x.p.id}>
            {label}
            <rect className={`${ho ? 'bar-held' : 'bar-disc'} mv`} x={0} y={y + 6} width={1} height={15} style={{ transform: `translateX(${a}px) scaleX(${Math.max(1, b - a)})` }} vectorEffect="non-scaling-stroke" />
            <rect className={`${fee >= 0 ? 'bar-fee' : 'bar-rebate'} mv`} x={0} y={y + 24} width={1} height={15} style={{ transform: `translateX(${fa}px) scaleX(${Math.max(1, fb - fa)})` }} vectorEffect="non-scaling-stroke" />
            <line className="ci-ink" x1={X(nv)} x2={X(nv)} y1={y + 2} y2={y + 43} />
            <text className="t-ink t-num" x={l} y={y + 60}>
              <tspan className="t-bold">net {fmt(nv, d, true)}</tspan>  ·  gross {fmt(gv, d, true)}  ·  {fee >= 0 ? 'fees' : 'net rebate'} {fmt(Math.abs(fee), d)}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

function Risk({ r, S, W }: { r: Ok; S: State; W: number }) {
  const ms: Array<[string, string, number]> = [['inc_es', 'Expected shortfall, 5 min, USDT', 1], ['max_drawdown', 'Maximum drawdown, USDT', 0], ['tw_abs_inventory_avg', 'Average |inventory|, SOL', 2]];
  const rows = [S.focus, S.vs].filter((p, i, a) => a.indexOf(p) === i).map((p) => r.rows.find((x) => x.p.id === p)!);
  const l = 64, rr = 64, ho = S.sample === 'heldout';
  return (
    <div className="risk">
      {ms.map(([k, label, d]) => {
        const mx = Math.max(1e-9, ...rows.map((x) => x.v[k] ?? 0));
        const H = 14 + rows.length * 22;
        return (
          <figure key={k} className="risk-m" data-src={rows.map((x) => src(S, x.p.id)).join('; ')}>
            <figcaption>{label}</figcaption>
            <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${label}: ${rows.map((x) => `${x.p.code} ${fmt(x.v[k], d) ?? 'undefined'}`).join(', ')}`}>
              {rows.map((x, i) => {
                const v = x.v[k] ?? 0, y = 4 + i * 22, w = Math.max(1, (v / mx) * (W - l - rr));
                return (
                  <g key={x.p.id}>
                    <text className="t-ink t-id" x={l - 8} y={y + 13} textAnchor="end">{x.p.code}</text>
                    <rect className={`${ho ? 'bar-held' : 'bar-disc'} mv`} x={0} y={y + 2} width={1} height={14} style={{ transform: `translateX(${l}px) scaleX(${w})` }} vectorEffect="non-scaling-stroke" />
                    <text className="t-ink t-num" x={l + w + 6} y={y + 13}>{x.kind === 'traded' ? fmt(v, d) : '0'}</text>
                  </g>
                );
              })}
            </svg>
          </figure>
        );
      })}
    </div>
  );
}

/* ------------------------------------------------------------------ eight policies, one measure */
function Comparison({ r, S, set, width }: { r: Ok; S: State; set: (p: Partial<State>) => void; width: number }) {
  const m = METRIC.find((x) => x.id === S.metric)!;
  const primary = isPrimary(S), ho = S.sample === 'heldout';
  const part = LAB.disc_ci_primary_vip0, hos = LAB.held_sessions_primary_vip0;
  const vals: number[] = [0];
  r.rows.forEach((x) => {
    const v = x.v[m.id];
    if (v !== null && v !== undefined) vals.push(v);
    if (m.sess !== undefined && x.sess) for (const d in x.sess) { const sv = x.sess[d][m.sess]; if (sv !== null) vals.push(sv); }
    if (m.id === 'net_per_hour' && primary && !ho && part[x.p.id]) vals.push(part[x.p.id].lo, part[x.p.id].hi);
    if (m.id === 'net_per_hour' && primary && ho && hos[x.p.id]) for (const d in hos[x.p.id]) vals.push(hos[x.p.id][d]);
  });
  const { lo, hi, ticks } = domain(vals);
  const W = Math.max(160, Math.round(width));
  const X = (v: number) => 4 + ((v - lo) / (hi - lo)) * (W - 8);
  const hyp = find(OPT.fee, S.fee)!.attain === 'hypothetical';
  return (
    <section className="cmp" id="lab-compare" aria-labelledby="cmp-h">
      <div className="cmp-h">
        <h2 id="cmp-h">All eight policies, one measure</h2>
        <div className="metrics">
          <label htmlFor="metric">Measure</label>
          <select id="metric" value={S.metric} onChange={(e) => set({ metric: e.target.value })}>
            {METRIC.map((mm) => <option key={mm.id} value={mm.id}>{mm.label}{mm.unit ? `, ${mm.unit}` : ''}</option>)}
          </select>
          <Help label="these measures">{HELP.metric}</Help>
        </div>
      </div>
      <ul className="rows" aria-label={`Policy comparison: ${m.label}`}>
        <li className="axisrow" aria-hidden="true">
          <span />
          <svg viewBox={`0 0 ${W} 18`}>{ticks.map((t) => <text key={t} x={X(t)} y={12} textAnchor="middle">{m.pct ? `${Math.round(t * 100)}%` : axisLab(t)}</text>)}</svg>
          <span />
        </li>
        {r.rows.map((x) => {
          const v = x.v[m.id];
          const sv = show(m, v);
          const note = x.kind === 'baseline' ? 'never quotes' : x.kind === 'abstained' ? 'abstained: the zero is mechanical' : '';
          const isF = x.p.id === S.focus, isC = x.p.id === S.vs && !isF;
          return (
            <li key={x.p.id} className={`row${isF ? ' focus' : ''}${isC ? ' vs' : ''}`} onClick={() => set({ focus: x.p.id })}>
              <button type="button" className="who" aria-pressed={isF}><b>{x.p.code}</b><span>{x.p.name}</span>{isC && <i className="vs-t">compared</i>}</button>
              <div className="scalecell">
                {x.kind !== 'traded' ? <span className="note">{note}</span> : (
                  <svg viewBox={`0 0 ${W} 26`} aria-hidden="true">
                    <line className="z" x1={X(0)} x2={X(0)} y1={1} y2={25} />
                    {v !== null && v !== undefined && (
                      <rect className={`${ho ? 'b-h' : 'b-d'} mv`} x={0} y={6} width={1} height={11} style={{ transform: `translateX(${Math.min(X(0), X(v))}px) scaleX(${Math.max(Math.abs(X(v) - X(0)), 1)})` }} vectorEffect="non-scaling-stroke" />
                    )}
                    {m.sess !== undefined && x.sess && Object.entries(x.sess).map(([d, s]) => (s[m.sess!] === null ? null : <circle key={d} className="sd" cx={X(s[m.sess!]!)} cy={22} r={1.9} />))}
                    {m.id === 'net_per_hour' && primary && !ho && part[x.p.id] && (
                      <>
                        <line className="ci" x1={X(part[x.p.id].lo)} x2={X(part[x.p.id].hi)} y1={11.5} y2={11.5} />
                        <line className="ci" x1={X(part[x.p.id].lo)} x2={X(part[x.p.id].lo)} y1={7} y2={16} />
                        <line className="ci" x1={X(part[x.p.id].hi)} x2={X(part[x.p.id].hi)} y1={7} y2={16} />
                      </>
                    )}
                    {m.id === 'net_per_hour' && primary && ho && hos[x.p.id] && Object.entries(hos[x.p.id]).map(([d, hv]) => <circle key={d} className="sh" cx={X(hv)} cy={22} r={1.9} />)}
                  </svg>
                )}
              </div>
              <div className="val" data-src={src(S, x.p.id)} data-status="modeled historical replay">
                {x.kind !== 'traded' ? <span className="note">{sv === null ? 'undefined' : sv}</span>
                  : sv === null ? <span className="note">undefined</span>
                    : <>{sv}{m.unit && !m.pct && <small>{m.unit.split(',')[0]}</small>}{hyp && <span className="tag hyp" data-fee="hypothetical">hypothetical</span>}</>}
              </div>
            </li>
          );
        })}
      </ul>
      <div className="rowkey">
        <span><svg viewBox="0 0 22 12"><rect className={ho ? 'k-held' : 'k-disc'} x="1" y="2" width="20" height="8" /></svg>{ho ? 'held-out mean' : 'discovery mean'}</span>
        {m.sess !== undefined && !ho && <span><svg viewBox="0 0 22 12"><circle className="k-sess" cx="5" cy="6" r="1.8" /><circle className="k-sess" cx="11" cy="6" r="1.8" /><circle className="k-sess" cx="17" cy="6" r="1.8" /></svg>the 10 discovery sessions</span>}
        {m.id === 'net_per_hour' && primary && !ho && <span><svg viewBox="0 0 22 12"><path className="k-ci" d="M2 6H20M2 2V10M20 2V10" /></svg>95% session-bootstrap interval</span>}
        {m.id === 'net_per_hour' && primary && ho && <span><svg viewBox="0 0 22 12"><circle className="k-sess-h" cx="5" cy="6" r="1.8" /><circle className="k-sess-h" cx="11" cy="6" r="1.8" /><circle className="k-sess-h" cx="17" cy="6" r="1.8" /></svg>the 5 held-out sessions</span>}
        {hyp && <span><Tag kind="hyp">hypothetical</Tag> under a fee schedule a participant like us cannot attain</span>}
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ charts */
function diamond(x: number, y: number, r: number, cls: string) {
  const k = r * 1.3;
  return <path className={cls} d={`M${x} ${y - k}L${x + k} ${y}L${x} ${y + k}L${x - k} ${y}Z`} />;
}

function Scatter({ r, S, W }: { r: Ok; S: State; W: number }) {
  const H = W < 420 ? 310 : 340, m = { l: 52, r: 16, t: 28, b: 40 };
  const traded = r.rows.filter((x) => x.kind === 'traded');
  const xs = [1], ys = [0];
  traded.forEach((x) => {
    xs.push(x.v.turnover_per_hour!); ys.push(x.v.net_per_hour!);
    if (x.sess) for (const d in x.sess) { if (x.sess[d][1] !== null) xs.push(x.sess[d][1]!); if (x.sess[d][0] !== null) ys.push(x.sess[d][0]!); }
  });
  const xmax = nice(Math.max(...xs));
  let ymin = Math.min(...ys), ymax = Math.max(...ys);
  ymin = ymin < 0 ? -nice(-ymin) : 0; ymax = ymax > 0 ? nice(ymax) : 0; if (ymin === ymax) ymin = -1;
  const X = (v: number) => m.l + (v / xmax) * (W - m.l - m.r);
  const Y = (v: number) => m.t + ((ymax - v) / (ymax - ymin)) * (H - m.t - m.b);
  const ho = S.sample === 'heldout';
  const ystep = nice((ymax - ymin) / 4);
  const yt: number[] = [];
  for (let t = Math.ceil(ymin / ystep) * ystep; t <= ymax + 1e-9; t += ystep) yt.push(Math.abs(t) < 1e-9 ? 0 : t);
  const mark = (x: Row, k: 'f' | 'c') => {
    const px = X(x.v.turnover_per_hour!), py = Y(x.v.net_per_hour!), right = px < W * 0.62;
    return (
      <g key={k}>
        <circle className={k === 'f' ? 'ring-f' : 'ring-c'} cx={px} cy={py} r={k === 'f' ? 10 : 8.5} />
        <text className={`t-ink t-id${k === 'f' ? ' t-bold' : ''}`} x={px + (right ? 14 : -14)} y={py + (k === 'f' ? -10 : 16)} textAnchor={right ? 'start' : 'end'}>{x.p.code} {fmt(x.v.net_per_hour, 1, true)}</text>
      </g>
    );
  };
  const F = traded.find((x) => x.p.id === S.focus), C = traded.find((x) => x.p.id === S.vs && x.p.id !== S.focus);
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Turnover against net result per hour for the policies that trade in this scenario" data-src={`${LAB.grid_src[ho ? 'held' : 'disc']}; ${LAB.disc_sessions_src}`}>
      {[0, 1, 2, 3, 4].map((i) => {
        const t = (xmax * i) / 4;
        return <g key={i}><line className="grid" x1={X(t)} x2={X(t)} y1={m.t} y2={H - m.b} />{(W >= 420 || i % 2 === 0) && <text className="t-num" x={X(t)} y={H - m.b + 16} textAnchor="middle">{axisLab(t)}</text>}</g>;
      })}
      {yt.map((t) => <g key={t}><line className={t === 0 ? 'zero' : 'grid'} x1={m.l} x2={W - m.r} y1={Y(t)} y2={Y(t)} /><text className="t-num" x={m.l - 6} y={Y(t) + 4} textAnchor="end">{axisLab(t)}</text></g>)}
      {S.fee === 'vip0' && [10, 12].map((bp) => {
        const xe = Math.min(xmax, ymin / (-bp * 1e-4));
        return <line key={bp} className="ref" x1={X(0)} y1={Y(0)} x2={X(xe)} y2={Y(-xe * bp * 1e-4)} />;
      })}
      {traded.map((x) => x.sess && Object.entries(x.sess).map(([d, s]) => (s[0] === null || s[1] === null ? null : <circle key={x.p.id + d} className="sess-d" cx={X(s[1])} cy={Y(s[0])} r={2} />)))}
      {traded.map((x) => <g key={x.p.id} className="mv" style={{ transform: `translate(${X(x.v.turnover_per_hour!)}px, ${Y(x.v.net_per_hour!)}px)` }}>{ho ? diamond(0, 0, 4.2, 'ho') : <circle className="disc" cx={0} cy={0} r={4.4} />}</g>)}
      {C && mark(C, 'c')}
      {F && mark(F, 'f')}
      <text x={(m.l + W - m.r) / 2} y={H - 6} textAnchor="middle">Turnover, USDT/h</text>
      <text x={m.l - 6} y={m.t - 14} textAnchor="end">USDT/h</text>
    </svg>
  );
}

function FeeStrip({ S, W }: { S: State; W: number }) {
  const fees = OPT.fee, fills = ['conservative', 'intermediate', 'optimistic'], lats = ['tokyo', 'regional', 'distant'];
  const m = { l: W < 420 ? 80 : 96, r: 14, t: 10, b: 36 }, rowH = 40, H = m.t + m.b + rowH * fees.length, lo = -13, hi = 1;
  const X = (v: number) => m.l + ((v - lo) / (hi - lo)) * (W - m.l - m.r);
  const side = sideOf(S);
  const iNet = LAB.metrics.indexOf('net_bp_per_notional');
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Net per unit traded for the highlighted policy under each fee schedule (rows) and each of nine fill-model and latency assumptions (marks)" data-src={LAB.grid_src[side]}>
      {[-12, -9, -6, -3, 0].map((t) => <g key={t}><line className={t === 0 ? 'zero' : 'grid'} x1={X(t)} x2={X(t)} y1={m.t} y2={H - m.b} /><text className="t-num" x={X(t)} y={H - m.b + 16} textAnchor="middle">{axisLab(t)}</text></g>)}
      <text x={W - m.r} y={H - 4} textAnchor="end">net, bp of notional</text>
      {fees.map((fe, i) => {
        const y = m.t + rowH * i + rowH / 2;
        const marks: ReactNode[] = [];
        let n = 0;
        if (!fe.un) fills.forEach((fl) => lats.forEach((la) => {
          const c = LAB.grid[side][cellKey(S.focus, fl, la, fe.id)];
          const v = c ? c[iNet] : null;
          if (v === null || v === undefined) return;
          n += 1;
          const cur = fl === S.fill && la === S.latency && fe.id === S.fee;
          marks.push(<rect key={fl + la} className={side === 'held' ? 'exm-h' : 'exm'} x={X(v) - 1.5} y={y - 8} width={3} height={16} />);
          if (cur) marks.push(<g key="cur"><rect className="exm-cur" x={X(v) - 5} y={y - 12} width={10} height={24} /><text className="t-ink t-num t-bold" x={X(v) + (v < -6 ? 9 : -9)} y={y - 14} textAnchor={v < -6 ? 'start' : 'end'}>{fmt(v, 2, true)}</text></g>);
        }));
        return (
          <g key={fe.id}>
            <text className={`${fe.id === S.fee ? 't-ink' : 't-ink2'} t-bold`} x={m.l - 10} y={y - 1} textAnchor="end">{fe.label}</text>
            <text x={m.l - 10} y={y + 12} textAnchor="end" fontSize="11">{fe.un ? 'not tested' : fe.attain}</text>
            {fe.un ? <rect className="untested" x={m.l} y={y - 10} width={W - m.l - m.r} height={20} /> : marks}
            {fe.un && <text className="t-dim" x={m.l + 8} y={y + 4} fontSize="11">E002 only</text>}
            {!fe.un && n === 0 && <text className="t-ink2" x={m.l + 8} y={y + 4}>{S.focus === 'NT' ? 'never quotes' : 'does not trade under any execution assumption'}</text>}
          </g>
        );
      })}
    </svg>
  );
}

function ViewE003({ r, S, set, notes, first }: { r: Resolved; S: State; set: (p: Partial<State>) => void; notes: Note[]; first: boolean }) {
  const [unit, setUnit] = useState<'hour' | 'bp'>('hour');
  // the breakdown follows the measure: a per-notional measure shows it per unit traded, an hourly one per hour
  useEffect(() => {
    if (S.metric.endsWith('bp_per_notional')) setUnit('bp');
    else if (S.metric.endsWith('per_hour')) setUnit('hour');
  }, [S.metric]);
  const [rowsRef, rowsW] = useWidth<HTMLDivElement>(820);
  const mobile = useMedia('(max-width: 760px)');
  if (!r.ok) return <Unavailable r={r} set={set} />;
  const F = POL.find((p) => p.id === S.focus)!, C = POL.find((p) => p.id === S.vs)!;
  const fe = find(OPT.fee, S.fee)!;
  return (
    <>
      <Readout notes={notes} first={first} />
      <section className="duo" aria-label="Highlighted policy against its comparison">
        <figure className="panel" id="lab-breakdown">
          <div className="cap">
            <b>{F.code} against {C.code}: where the result comes from</b>
            <span>The result before fees, the fees paid, and what remains after them.</span>
          </div>
          <div className="seg" role="radiogroup" aria-label="Units">
            <button type="button" role="radio" aria-checked={unit === 'hour'} className="chip" onClick={() => setUnit('hour')}>Per hour</button>
            <button type="button" role="radio" aria-checked={unit === 'bp'} className="chip" onClick={() => setUnit('bp')}>Per unit traded</button>
          </div>
          <Sized className="mt-3" fallback={420}>{(w) => <Breakdown r={r} S={S} W={w} unit={unit} />}</Sized>
          <ul className="legend">
            <li><svg viewBox="0 0 14 14" aria-hidden="true"><rect className={S.sample === 'heldout' ? 'lg-ho' : 'lg-disc'} x="2" y="3" width="10" height="8" /></svg>gross, before fees</li>
            <li><svg viewBox="0 0 14 14" aria-hidden="true"><rect className="lg-fee" x="2" y="3" width="10" height="8" /></svg>fees paid</li>
            {find(OPT.fee, S.fee)!.id === 'lp_tier4' && <li><svg viewBox="0 0 14 14" aria-hidden="true"><rect className="lg-rebate" x="2" y="3" width="10" height="8" /></svg>net rebate received</li>}
            <li><svg viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1V13" stroke="currentColor" strokeWidth="1.5" /></svg>net, after fees</li>
          </ul>
        </figure>
        <figure className="panel">
          <div className="cap"><b>Risk while trading</b><span>Downside and inventory measures for the same two policies. Lower is less risk, not more profit.</span></div>
          <Sized fallback={420}>{(w) => <Risk r={r} S={S} W={w} />}</Sized>
        </figure>
      </section>
      <div ref={rowsRef}><Comparison r={r} S={S} set={set} width={mobile ? rowsW - 4 : rowsW - 400} /></div>
      <section className="duo" aria-label="Scenario charts">
        <figure className="panel">
          <div className="cap"><b>Losses scale with turnover</b><span>{S.sample === 'heldout' ? 'Held-out means' : 'Discovery means and the 10 session values'}; {find(OPT.fill, S.fill)!.label.toLowerCase()} fill, {find(OPT.latency, S.latency)!.label.toLowerCase()} latency, {fe.label}.</span></div>
          <Sized fallback={420}>{(w) => <Scatter r={r} S={S} W={w} />}</Sized>
          <p className="held mt-2">{S.fee === 'vip0' ? 'Dashed lines: a constant loss of 10 and 12 bp of traded notional, as in the paper’s Figure 4. ' : 'Reference lines are drawn only for VIP0. '}Large ring: {F.code}; small ring: {C.code}.</p>
        </figure>
        <figure className="panel" id="lab-fees">
          <div className="cap"><b>Fees outweigh execution assumptions</b><span>{F.code}: each row is a fee schedule; each mark is one of the nine tested fill-model and latency combinations.</span></div>
          <Sized fallback={420}>{(w) => <FeeStrip S={S} W={w} />}</Sized>
          <p className="held mt-2">Marks within a row sit close together; the rows sit far apart. The boxed mark is the current scenario.</p>
        </figure>
      </section>
      <Tags>
        <Tag kind="mod">Modeled (historical replay)</Tag>
        {feeTag(fe)}
        <Tag kind="plain">{S.sample === 'heldout' ? 'Held-out, 5 sessions' : 'Discovery walk-forward, 10 sessions'}</Tag>
      </Tags>
    </>
  );
}

function ViewE002({ S }: { S: State }) {
  const latLabel = (la: string) => find(OPT.latency, la)!.label;
  const ms = { tokyo: 2, regional: 30, distant: 115 } as Record<string, number>;
  return (
    <>
      <section className="readout" aria-labelledby="e2-h">
        <div className="readout-h"><h2 id="e2-h">Do execution assumptions change the answer?</h2></div>
        <p className="more">E002 replayed the two fixed baselines, P0 and P1, under three queue models and three latency brackets, at VIP0. If a plausible execution assumption could turn the loss into a profit, it would show here. Across the 18 combinations the mean net result lies between <b data-src={core.values['e002.range.disc'].src}>{core.values['e002.range.disc'].printed}</b> bp of notional in discovery and between <b data-src={core.values['e002.range.held'].src}>{core.values['e002.range.held'].printed}</b> bp held-out (<q className="lbl" data-label="e002">{core.e002.heldout_label}</q>): differences of under a basis point, against a fee of ten.</p>
        <Tags><Tag kind="mod">Modeled (historical replay)</Tag><Tag kind="att">VIP0, attainable</Tag></Tags>
      </section>
      <QueueModels />
      {['P0', 'P1'].map((p) => (
        <div className="sec2" key={p}>
          <h3>{p}: net per unit traded by fill model and latency</h3>
          <div className="tw" role="region" aria-label={`${p} execution scenarios`} tabIndex={0}>
            <table className="t">
              <caption>bp of traded notional, VIP0. Discovery: mean of 15 sessions with 95% interval. Held-out: mean of 5 sessions, {core.e002.heldout_label}. The highlighted row follows your fill-model setting.</caption>
              <thead><tr><th>Fill model</th>{['tokyo', 'regional', 'distant'].map((la) => <th key={la}>{latLabel(la)} <small>{ms[la]} ms</small></th>)}</tr></thead>
              <tbody>
                {['conservative', 'intermediate', 'optimistic'].map((fl) => (
                  <tr key={fl} className={fl === S.fill ? 'cur' : undefined}>
                    <td>{find(OPT.fill, fl)!.label}</td>
                    {['tokyo', 'regional', 'distant'].map((la) => {
                      const c = core.e002.matrix.find((q) => q.policy === p && q.fill === fl && q.latency === la)!;
                      return (
                        <td key={la} className="num" data-src={c.src_disc}>
                          {fmt(c.disc, 2, true)}<small>[{fmt(c.disc_lo, 2, true)}, {fmt(c.disc_hi, 2, true)}]</small>
                          <small data-src={c.src_held}>held-out {fmt(c.held, 2, true)}</small>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
      <p className="closed">This fixed-quoting run differs slightly from the one in the Policies view, which adds order pacing, so the two are always shown separately.</p>
    </>
  );
}

function ViewE004({ S }: { S: State }) {
  const E = LAB.e004;
  const dw = E.disc_window['D1_E:P0:intermediate:regional'].D_W_bp, dwh = E.held_window['D1_E:P0:intermediate:regional'].D_W_bp;
  const lab0 = core.values['e004.p0.held'].lab!, lab2 = core.values['e004.p3m2.held'].lab!;
  const names: Record<string, string> = { 'U-P': 'withdraw when stale minus withdraw at random times', 'U-N': 'withdraw when stale minus never withdraw', 'P-N': 'withdraw at random times minus never withdraw' };
  return (
    <>
      <section className="readout" aria-labelledby="e4-h">
        <div className="readout-h"><h2 id="e4-h">Does stale information hurt fills?</h2></div>
        <p className="more">A quoter that loses its data feed keeps acting on an old picture of the market, so its resting orders could be picked off. E004 cut the participant’s connection on purpose, far more often than it really drops, and compared fills that arrived while its view was stale with fills in random windows of the same length. For P0 the difference D<sub>W</sub> was <b data-src={`${E.src_disc}/window_quality`}>{fmt(dw.mean, 2, true)} bp</b> in discovery and <b data-src={`${E.src_held}/window_quality`}>{fmt(dwh.mean, 2, true)} bp</b> held-out, against a pre-registered 1 bp threshold.</p>
        <p className="more mt-3"><b>The result is narrow:</b> <q className="lbl" data-label="H4-W[P0]">{lab0}</q>. It is not a finding of equivalence, it says nothing about effects smaller than 1 bp, and it does not show that stale information is harmless in general.</p>
        <Tags><Tag kind="str">Stress test</Tag><Tag kind="mod">Modeled (historical replay)</Tag></Tags>
      </section>
      <StaleWindow />
      {S.latency !== 'regional' && <p className="closed"><b>Not tested at {find(OPT.latency, S.latency)!.label.toLowerCase()} latency.</b> {LAB.untested.e004_latency}. The tables show the regional runs.</p>}
      <div className="sec2">
        <h3>Window quality, D<sub>W</sub></h3>
        <p className="ink-2">D<sub>W</sub> = q(W<sub>P</sub>) − q(W<sub>U</sub>): random-window fill quality minus stale-window fill quality, fee-free 5-second mark-to-mid, bp of notional; positive would mean stale fills are worse. Status: {E.status}.</p>
        <div className="tw" role="region" aria-label="Window quality" tabIndex={0}>
          <table className="t">
            <thead><tr><th>Condition, base, fill</th><th>Discovery <small>mean [95% interval]</small></th><th>Held-out <small>mean</small></th><th>Label</th></tr></thead>
            <tbody>
              {Object.keys(E.disc_window).map((k) => {
                const [cond, base, fill] = k.split(':');
                const d = E.disc_window[k].D_W_bp, o = E.held_window[k]?.D_W_bp;
                const pre = cond === 'D1_E' && fill === 'intermediate';
                return (
                  <tr key={k} className={fill === S.fill ? 'cur' : undefined}>
                    <td>{cond.replace('_', '-')}{cond === 'D1_E' ? ' drops' : ' stalls'}, <span className="id">{base === 'P3_M2' ? 'P3[M2]' : base}</span>, {fill}</td>
                    <td className="num" data-src={`${E.src_disc}/window_quality/${k}`}>{fmt(d.mean, 2, true)}<small>[{fmt(d.ci95![0], 2, true)}, {fmt(d.ci95![1], 2, true)}]</small></td>
                    <td className="num" data-src={`${E.src_held}/window_quality/${k}`}>{o ? fmt(o.mean, 2, true) : <span className="note">not part of the held-out evaluation</span>}</td>
                    <td className="lbl-cell"><small>{pre ? <>H4-W: <q className="lbl" data-label={base === 'P0' ? 'H4-W[P0]' : 'H4-W[P3_M2]'}>{base === 'P0' ? lab0 : lab2}</q></> : 'descriptive'}</small></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
      <div className="sec2">
        <h3>Does withdrawing when stale help?</h3>
        <p className="ink-2">Connection drops (D1-E), regional latency. Change in net per hour at VIP0, and the mechanical maker-fee saving that comes with trading less. Held-out: <q className="lbl" data-label="e004-contrasts">{E.held_label}</q>.</p>
        {['P0', 'P3_M2'].map((b) => (
          <div className="tw" key={b} role="region" aria-label={`Withdrawal contrasts, ${b}`} tabIndex={0}>
            <table className="t">
              <caption><span className="id">{b === 'P3_M2' ? 'P3[M2]' : 'P0'}</span>, USDT/h at VIP0 unless stated</caption>
              <thead><tr><th>Contrast</th><th>Net per hour <small>discovery [95%]</small></th><th>of which fee saving <small>mechanical</small></th><th>Held-out <small>net per hour</small></th></tr></thead>
              <tbody>
                {['U-P', 'U-N', 'P-N'].map((k) => {
                  const d = E.disc_contrasts[b][k], o = E.held_contrasts[b][k];
                  return (
                    <tr key={k}>
                      <td>{names[k]}</td>
                      <td className="num" data-src={`${E.src_disc}/policy_D1_E/${b}/${k}`}>{fmt(d.delta_net_per_hour_vip0.mean, 2, true)}<small>[{fmt(d.delta_net_per_hour_vip0.ci95![0], 2, true)}, {fmt(d.delta_net_per_hour_vip0.ci95![1], 2, true)}]</small></td>
                      <td className="num" data-src={`${E.src_disc}/policy_D1_E/${b}/${k}`}>{fmt(d.fee_saving_per_hour_vip0_mechanical.mean, 2, true)}</td>
                      <td className="num" data-src={`${E.src_held}/policy_D1_E/${b}/${k}`}>{fmt(o.delta_net_per_hour_vip0.mean, 2, true)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ))}
        <p className="closed">The paper: “Every net gain from withdrawing at all came almost entirely from the mechanical fee saving on lower turnover, the same participation effect as in E003.”</p>
      </div>
    </>
  );
}

/* ------------------------------------------------------------------ inspection layer */
function Details({ S, r }: { S: State; r: Resolved }) {
  const fe = find(OPT.fee, S.fee)!, fl = find(OPT.fill, S.fill)!, la = find(OPT.latency, S.latency)!;
  const ho = S.sample === 'heldout';
  const hours = core.values[ho ? 'sample.held.hours' : 'sample.wf.hours'];
  const maker = MAKER(fe.id), taker = TAKER(fe.id);
  const vip0 = <>VIP0: maker <span data-src={core.values['fee.vip0.maker'].src}>{fmt(MAKER('vip0'), 1)}</span> bp, taker <span data-src={core.values['fee.vip0.taker'].src}>{fmt(TAKER('vip0'), 1)}</span> bp; attainable</>;
  const hl = fl.un ? 'none highlighted' : `${fl.label.toLowerCase()} highlighted`;
  const fixedRows: Record<string, Array<[string, ReactNode]>> = {
    e002: [
      ['Experiment', 'E002, execution sensitivity'],
      ['Sample', 'Discovery: all 15 sessions, 2025-03 to 2026-05, with the 5 held-out sessions beside each value'],
      ['Policies', 'P0 and P1'],
      ['Fill model', `all three tested models shown; ${hl}`],
      ['Latency', 'all three brackets shown: Tokyo-hosted 2 ms, regional 30 ms, distant 115 ms'],
      ['Fees', vip0],
      ['Evidence', 'Modeled (historical replay)'],
      ['Held-out', core.e002.heldout_label],
      ['Source', <span key="s" data-meta="paper section">The paper, §5.2 and §6</span>],
    ],
    e004: [
      ['Experiment', 'E004, information robustness'],
      ['Sample', 'Discovery walk-forward: 10 sessions, 2025-08 to 2026-05, with the 5 held-out sessions beside each value'],
      ['Policies', 'P0 and P3[M2] as bases'],
      ['Fill model', `three models for connection drops, intermediate only for stalls; ${hl}`],
      ['Latency', 'regional, 30 ms (the only bracket run)'],
      ['Fees', <>window quality fee-free; net-per-hour contrasts at {vip0}</>],
      ['Evidence', LAB.e004.status],
      ['Source', <span key="s" data-meta="paper section">The paper, §5.6 and §6</span>],
    ],
  };
  const rows: Array<[string, ReactNode]> = fixedRows[S.view] ?? [
    ['Experiment', 'E003, signals and quoting'],
    ['Sample', <>{ho ? 'Held-out: 5 sessions, 2026-06 to 2026-10, ' : 'Discovery walk-forward: 10 sessions, 2025-08 to 2026-05, '}<span data-src={hours.src}>{fmt(hours.v, 1)}</span> valid hours</>],
    ['Fill model', fl.label + (fl.un ? ' (not tested)' : '')],
    ['Latency', `${la.label}, ${la.small}`],
    ['Fees', <>{fe.label}{maker !== null && <>: maker <span data-src={core.values[`fee.${fe.id}.maker`].src}>{fmt(maker, 1)}</span> bp, taker <span data-src={core.values[`fee.${fe.id}.taker`].src}>{fmt(taker, 1)}</span> bp</>}; {fe.un ? 'not tested' : fe.attain}</>],
    ['Quoting', 'one SOL at the touch; ±10 SOL hard limit; new orders paced at about one per second per side'],
    ['Limits', 'fixed per policy; not varied'],
    ['Evidence', S.view === 'e004' ? LAB.e004.status : 'Modeled (historical replay)'],
    ['Held-out', ho ? LAB.held_label : 'not shown; change the sample to see it'],
    ['Source', <span key="s" data-meta="paper section">{ho ? 'The paper, §6' : 'The paper, §5.3 to §5.5'}</span>],
  ];
  return (
    <section className="inspect-zone" aria-label="Assumptions, method and limits">
      <Inspect title="Conditions of this scenario" note="sample, fees and fixed rules" open>
        <dl className="kv">{rows.map(([k, v]) => <div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}</dl>
        {!r.ok && S.view === 'e003' && <p><b className="ink">No result</b> for this combination.</p>}
      </Inspect>
      <Inspect title="How the replay works" note="method in brief">
        <ul className="plain">
          <li>The engine replays the historical order book and trade stream and simulates our one-SOL orders against it without altering it: our orders have no market impact.</li>
          <li>Orders join the back of their price level; trades at that price consume the queue ahead first. The three fill models bracket the unknown attribution of cancellations.</li>
          <li>Fees are accounting overlays on fixed fills, except for P3F and P4, whose decisions depend on the fee.</li>
          <li>Marked wealth obeys an accounting identity: the sum of fill edges against the mid, plus inventory revaluation, minus fees. Every episode starts flat and ends liquidated.</li>
        </ul>
        <p><a href="/methods">Methods &amp; Data</a> has the full design, equations and limitations.</p>
      </Inspect>
      <Inspect title="What these results cannot tell you" note="limits">
        <ul className="plain">
          <li><b>Modeled execution.</b> Every policy result is a replay; queue position is inferred, not observed; the fill models bracket the unknown but are not proven bounds.</li>
          <li><b>A five-session holdout.</b> A confirmed label means a discovery decision did not reverse on five later days; it is not a significance test.</li>
          <li><b>Hypothetical fees and synthetic stresses.</b> H3 is tested only under a rebate tier this project cannot reach; E004’s degradations are far above observed rates.</li>
          <li><b>Fixed, simple policies.</b> A-priori rules, not optimised strategies; the forecasts are linear.</li>
          <li><b>One market and venue.</b> Binance spot SOLUSDT on a free data sample.</li>
          <li><b>Not shown.</b> Inventory paths, individual orders and order-book playback are not published with this study.</li>
        </ul>
      </Inspect>
      <Inspect title="How to read the marks" note="colours, shapes, tags">
        <dl className="kv">
          <div><dt><Tag kind="obs">Observed</Tag></dt><dd>recorded trades and replayed book states; no hypothetical orders</dd></div>
          <div><dt><Tag kind="mod">Modeled</Tag></dt><dd>historical replay: fills inferred under stated queue, latency and fee assumptions</dd></div>
          <div><dt><Tag kind="str">Stress test</Tag></dt><dd>observed records deliberately degraded</dd></div>
          <div><dt><Tag kind="hyp">Hypothetical</Tag></dt><dd>a fee schedule a participant like us cannot attain</dd></div>
          <div><dt><Tag kind="syn">Synthetic example</Tag></dt><dd>a teaching diagram with made-up values, never market data</dd></div>
          <div><dt>Colour and shape</dt><dd>In charts, filled navy marks are discovery and outlined marks or diamonds are held-out. Coral marks fees and the scenario you have highlighted.</dd></div>
        </dl>
      </Inspect>
    </section>
  );
}

/* ------------------------------------------------------------------ full lab: one compact settings bar */
const TESTED_FILLS = ['conservative', 'intermediate', 'optimistic'];
const optLabel = (o: Opt) => `${o.label}${o.un ? ', not tested' : o.attain === 'hypothetical' ? ', hypothetical' : ''}`;
const SHORT: Record<string, string> = { NT: 'No trade', P0: 'Fixed quoting', P1: 'Inventory withdrawal', P3_M1: 'Gated, imbalance', P3_M2: 'Gated, 8 features', P3_negM2: 'Placebo', P3F: 'Fee-aware', P4: 'Fee-aware, risk controls' };

function Field({ id, label, children }: { id: string; label: string; children: ReactNode }) {
  return <div className="fld"><label htmlFor={id}>{label}</label>{children}</div>;
}

/** Only the settings that change what is on screen. Fixed assumptions are stated, never offered as controls. */
function ScenarioBar({ S, set, reset }: { S: State; set: (p: Partial<State>) => void; reset: () => void }) {
  const [help, setHelp] = useState(false);
  const [more, setMore] = useState(false);
  const F = POL.find((p) => p.id === S.focus)!;
  if (S.view !== 'e003') {
    return (
      <div className="sbar-wrap">
        <div className="sbar" role="group" aria-label={`${S.view === 'e002' ? 'E002' : 'E004'} settings`}>
          <Field id="sb-fill" label="Highlighted fill model">
            <select id="sb-fill" value={TESTED_FILLS.includes(S.fill) ? S.fill : ''} onChange={(e) => set({ fill: e.target.value })}>
              {!TESTED_FILLS.includes(S.fill) && <option value="" disabled>none</option>}
              {OPT.fill.filter((o) => TESTED_FILLS.includes(o.id)).map((o) => <option key={o.id} value={o.id}>{o.label}</option>)}
            </select>
          </Field>
          <p className="sbar-fixed">
            <b>Fixed in this experiment.</b>{' '}
            {S.view === 'e002'
              ? 'P0 and P1, both shown; VIP0 fees; all nine fill-model and latency combinations; discovery values, with the held-out mean beside each.'
              : 'P0 and P3[M2] as bases, both shown; run at regional latency only; window quality measured before fees; discovery values, with the held-out mean beside each.'}
          </p>
        </div>
      </div>
    );
  }
  const fe = find(OPT.fee, S.fee)!, fl = find(OPT.fill, S.fill)!, la = find(OPT.latency, S.latency)!;
  return (
    <div className="sbar-wrap">
      <div className="sbar sbar-top" role="group" aria-label="Strategy">
        <Field id="sb-focus" label="Policy">
          <select id="sb-focus" value={S.focus} onChange={(e) => set({ focus: e.target.value })}>{POL.map((p) => <option key={p.id} value={p.id}>{p.code} · {SHORT[p.id]}</option>)}</select>
        </Field>
        <Field id="sb-vs" label="Compared with">
          <select id="sb-vs" value={S.vs} onChange={(e) => set({ vs: e.target.value })}>{POL.map((p) => <option key={p.id} value={p.id}>{p.code} · {SHORT[p.id]}</option>)}</select>
        </Field>
        <div className="assume">
          <span className="as-k">Assumptions</span>
          <span className="as-v">{S.sample === 'heldout' ? 'Held-out' : 'Discovery'} · {fe.label}{fe.attain === 'hypothetical' ? ' (hypothetical)' : ''} · {fl.label} fill · {la.label.replace('-hosted', '')} {la.small?.replace(', primary', '')}</span>
          <button type="button" className="btn quiet" aria-expanded={more} aria-controls="sbar-more" onClick={() => setMore((m) => !m)}>{more ? 'Done' : 'Change assumptions'}</button>
        </div>
      </div>
      <div id="sbar-more" className="sbar sbar-more" role="group" aria-label="Assumptions" hidden={!more}>
        <Field id="sb-sample" label="Sample">
          <select id="sb-sample" value={S.sample} onChange={(e) => set({ sample: e.target.value })}>{OPT.sample.map((o) => <option key={o.id} value={o.id}>{o.label}</option>)}</select>
        </Field>
        <Field id="sb-fee" label="Fee schedule">
          <select id="sb-fee" value={S.fee} onChange={(e) => set({ fee: e.target.value })}>{OPT.fee.map((o) => <option key={o.id} value={o.id}>{o.id === 'vip0' ? 'VIP0, attainable' : optLabel(o)}</option>)}</select>
        </Field>
        <Field id="sb-fill" label="Fill model">
          <select id="sb-fill" value={S.fill} onChange={(e) => set({ fill: e.target.value })}>{OPT.fill.map((o) => <option key={o.id} value={o.id}>{optLabel(o)}</option>)}</select>
        </Field>
        <Field id="sb-latency" label="Latency">
          <select id="sb-latency" value={S.latency} onChange={(e) => set({ latency: e.target.value })}>{OPT.latency.map((o) => <option key={o.id} value={o.id}>{o.label.replace('-hosted', '')}, {o.small?.replace(', primary', '')}</option>)}</select>
        </Field>
      </div>
      <div className="sbar-foot">
        <p className="sbar-fixed">Fixed in every scenario: one SOL at the best price or no quote; a ±10 SOL position limit (P1 and P4 also stop adding at 3 SOL).</p>
        <div className="sbar-act">
          <button type="button" className="btn quiet" aria-expanded={help} aria-controls="sbar-help" onClick={() => setHelp((h) => !h)}>{help ? 'Hide' : 'What do these mean?'}</button>
          <button type="button" className="btn quiet" onClick={reset}>Reset</button>
        </div>
      </div>
      <div id="sbar-help" className="sbar-help" hidden={!help}>
        <div><h3>Policy: {F.code}</h3><p>{F.does}</p></div>
        <div><h3>Sample</h3>{HELP.sample}</div>
        <div><h3>Fee schedule</h3>{HELP.fee}</div>
        <div><h3>Fill model</h3>{HELP.fill}</div>
        <div><h3>Latency</h3>{HELP.latency}</div>
      </div>
    </div>
  );
}

/** The result area, remounted per experiment view so a new view settles in. */
function ResultPanel({ quiet, children }: { quiet: boolean; children: ReactNode }) {
  const enter = useEnter(quiet);
  return <section className={`result${enter}`} id="result" role="tabpanel">{children}</section>;
}

function FullLab({ S, r, set, reset, notes, first }: { S: State; r: Resolved; set: (p: Partial<State>) => void; reset: () => void; notes: Note[]; first: boolean }) {
  const enter = useEnter();
  const mounted = useMounted();
  const views: Array<[string, string, string]> = [['e003', 'Policies', 'E003'], ['e002', 'Execution', 'E002'], ['e004', 'Stale data', 'E004']];
  return (
    <div className={`full${enter}`}>
      <div className="views" role="tablist" aria-label="Experiments" onKeyDown={(e) => {
        if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
        const ids = views.map((v) => v[0]); const i = ids.indexOf(S.view);
        const next = ids[(i + (e.key === 'ArrowRight' ? 1 : 2)) % 3];
        set({ view: next });
        (e.currentTarget.querySelector(`[data-view=${next}]`) as HTMLElement | null)?.focus();
      }}>
        {views.map(([id, label, exp]) => (
          <button key={id} role="tab" type="button" data-view={id} aria-selected={S.view === id} aria-controls="result" tabIndex={S.view === id ? 0 : -1} onClick={() => set({ view: id })}>
            {label}<small>{exp}</small>
          </button>
        ))}
      </div>
      <ScenarioBar S={S} set={set} reset={reset} />
      <div className="presets" role="group" aria-label="Starting scenarios">
        <span>Start from</span>
        {Object.entries(PRESETS).map(([id, p]) => (
          <button key={id} type="button" className="chip" aria-pressed={Object.entries(p.set).every(([k, v]) => S[k as Key] === v) && S.view === 'e003'} title={p.small} onClick={() => set({ ...p.set, view: 'e003' })}>{p.label}</button>
        ))}
      </div>
      <ResultPanel key={S.view} quiet={!mounted.current}>
        {S.view === 'e002' ? <ViewE002 S={S} /> : S.view === 'e004' ? <ViewE004 S={S} /> : <ViewE003 r={r} S={S} set={set} notes={notes} first={first} />}
      </ResultPanel>
      <Details S={S} r={r} />
    </div>
  );
}

/* ------------------------------------------------------------------ the guided story (the default) */
const P = (S: Partial<State>): State => ({ ...DEF, ...S });
const ok = (S: State) => resolve(S, []) as Ok;
const cell = (S: State, pid: string, m: string) => ok(S).rows.find((x) => x.p.id === pid)!.v[m]!;

/** Step 3: one figure for both points. Rows are fee schedules (far apart); marks within a row are the nine tested
 *  execution assumptions (close together). The chips move the highlighted scenario between schedules. */
function StoryFee({ fee }: { fee: string }) {
  const S = P({ focus: 'P0', vs: 'P0', fee });
  const fe = find(OPT.fee, fee)!;
  return (
    <figure className="panel story-panel">
      <Sized fallback={560}>{(w) => <FeeStrip S={S} W={w} />}</Sized>
      <div className="annot">
        <p><b>Within a row</b> the nine queue-model and speed assumptions sit within about a basis point.</p>
        <p><b>Between rows</b> the fee schedule moves the result by about ten.</p>
      </div>
      <p className="held">Fixed quoting, net result per unit traded, discovery sessions; the boxed mark is {fe.label}. {fe.attain === 'attainable' ? 'VIP0 is the only schedule this project can attain.' : `${fe.label} is hypothetical: a schedule this project cannot attain.`} Simulated on the historical market.</p>
    </figure>
  );
}

function StoryMeaning() {
  const rows: Array<[string, string]> = [
    ['A good forecast is not a good strategy', 'Real skill coexisted with a loss on every unit traded once fills and fees were counted.'],
    ['Fees and fee tiers decide the economics', 'At the attainable 10 bp fee nothing that traded broke even. Only a rebate tier this project cannot reach brings results near zero, and still below it.'],
    ['Being traded against is the core cost', 'What matters is the price move after you are filled, and it ran against the passive side on average.'],
    ['Losing less is not alpha', 'A rule that trades less loses less when every trade loses. Compare results per unit traded.'],
  ];
  return (
    <figure className="panel story-panel">
      <ol className="means-list">{rows.map(([h, t]) => <li key={h}><b>{h}</b><span>{t}</span></li>)}</ol>
      <p className="held">These follow from the tested rules on one market. They are not universal trading laws: better models, other venues or a market maker with scale and rebates could differ.</p>
    </figure>
  );
}

function StorySure() {
  const rows: Array<[string, string]> = [
    ['Rules fixed first', 'Every test rule was set before the five sealed days were opened.'],
    ['Checked once', 'The sealed days were evaluated a single time, on the first attempt.'],
    ['The pattern held', 'Skill, the cost of being traded against, and losses at the attainable fee all reappeared; the cost of being traded against was about half as large.'],
    ['Five days is few', 'Enough to see whether a result reversed, not enough to prove it is real. Fills are simulated, not observed.'],
  ];
  return (
    <figure className="panel story-panel">
      <ol className="means-list">{rows.map(([h, t]) => <li key={h}><b>{h}</b><span>{t}</span></li>)}</ol>
    </figure>
  );
}

interface StoryStep { short: string; title: string; lead: ReactNode; num: (fee: string) => ReactNode; visual: (fee: string) => ReactNode; chips?: boolean; more?: { title: string; body: ReactNode }; evidence: ReactNode; full: Partial<State> }

const p0 = P({});
const STORY: StoryStep[] = [
  {
    short: 'The forecast works', title: 'The forecast works',
    lead: <>Eight features of the order book forecast the price five seconds ahead. On days the model had never seen, it had real skill, but most of each move stayed unpredictable.</>,
    num: () => <><N id="e003.h1f.held" strong /><span>lower squared prediction error than a zero-change forecast, out of sample (five seconds ahead, on the sealed days)</span></>,
    visual: () => <figure className="panel story-panel"><Sized fallback={560}>{(w) => <SkillBars W={w} />}</Sized><ul className="legend"><li><svg viewBox="0 0 14 14" aria-hidden="true"><rect className="lg-disc" x="2" y="2" width="10" height="10" /></svg>Discovery</li><li><svg viewBox="0 0 14 14" aria-hidden="true"><rect className="lg-ho" x="2.5" y="2.5" width="9" height="9" /></svg>Held-out</li></ul><p className="held">Out-of-sample R² of the eight-feature forecast, 1, 5 and 30 seconds ahead. Measured on market data; no simulation.</p></figure>,
    more: { title: 'What does an R² of a few percent look like?', body: <SkillCloud /> },
    evidence: <p className="held">H1-F at 5 s: discovery <N id="e003.h1f.disc" /> [<N id="e003.h1f.disc_lo" />, <N id="e003.h1f.disc_hi" />]; held-out <N id="e003.h1f.held" />, <Held check="H1-F">{rec('e003.h1f.held').lab!}</Held>, a check decided by the sign of a mean only.</p>,
    full: { focus: 'P3_M2', vs: 'P0', metric: 'net_per_hour' },
  },
  {
    short: 'Fills come at the wrong moment', title: 'Fills come at the wrong moment',
    lead: <>Traders who cross the spread tend to be ahead of the next move. After they trade with a resting quote, the price keeps going their way, so the market maker holds a position that just lost value.</>,
    num: () => <><N id="e001.rs_30s.disc" strong unit /><span>kept by the passive side 30 seconds after a trade, on average</span></>,
    visual: () => <figure className="panel story-panel"><Sized fallback={560}>{(w) => <SpreadPath W={w} />}</Sized><p className="held">Observed: recorded trades only. Discovery mean with 95% intervals (filled), held-out mean (outlined). An average over millions of trades, not a claim about every fill.</p></figure>,
    more: { title: 'See one fill, step by step', body: <QuoteFill /> },
    evidence: <p className="held">Realized spread at 30 s: discovery <N id="e001.rs_30s.disc" unit /> [<N id="e001.rs_30s.disc_lo" />, <N id="e001.rs_30s.disc_hi" />]; held-out <N id="e001.rs_30s.held" unit />. All six E001 checks: <Held check="E001">{core.e001.tally}</Held>, one family of linked measures.</p>,
    full: { focus: 'P0', vs: 'P3_M2', metric: 'own_markout_30s_bp' },
  },
  {
    short: 'The fee decides', title: 'The fee decides',
    lead: <>A typical forecast is about half a basis point; the maker fee is ten, on every fill. Switch the fee schedule: the fills stay the same, only the fee changes, and the result stays below zero.</>,
    chips: true,
    num: (fee) => { const S = P({ focus: 'P0', fee }); return <><b data-src={src(S, 'P0')}>{fmt(cell(S, 'P0', 'net_bp_per_notional'), 2, true)} bp</b><span>per unit traded after fees, fixed quoting, {find(OPT.fee, fee)!.label}</span></>; },
    visual: (fee) => <StoryFee fee={fee} />,
    evidence: <p className="held">Fixed quoting (P0), primary scenario, discovery: <N id="e003.p0_primary.gross_bp" unit /> before fees, <N id="e003.p0_primary.net_bp" unit /> after VIP0 fees. In E002, the 18 execution scenarios at VIP0 stayed between <N id="e002.range.disc" /> bp; paired fill-model differences were <N id="e002.fill_diff" /> bp, all below the 1.0 bp materiality threshold.</p>,
    full: { focus: 'P0', vs: 'NT', metric: 'net_bp_per_notional' },
  },
  {
    short: 'Trading less loses less', title: 'Trading less loses less',
    lead: <>A forecast-gated quoter steps aside when it expects a move against its quote. It lost far less per hour than fixed quoting, mainly because it traded far less. Per unit traded it was no better.</>,
    num: () => <><b data-src={`${src(p0, 'P3_M2')}; ${src(p0, 'P0')}`}>{Math.round((1 - cell(p0, 'P3_M2', 'turnover_per_hour') / cell(p0, 'P0', 'turnover_per_hour')) * 100)}%</b><span>less traded value (turnover) than fixed quoting, {share(cell(p0, 'P3_M2', 'turnover_per_hour'), cell(p0, 'P0', 'turnover_per_hour')).replace(/ of$/, '')} as much; not a count of fills</span></>,
    visual: () => <figure className="panel story-panel"><Sized fallback={560}>{(w) => <TradeLess W={w} />}</Sized></figure>,
    more: { title: 'Where the smaller held-out loss came from', body: <figure className="panel"><Sized fallback={520}>{(w) => <HeldSplit W={w} />}</Sized><p className="held">Held-out sessions, USDT per hour. Coral is the maker fee saved by trading less.</p></figure> },
    evidence: <p className="held">Forecast-gated (P3[M2]) minus fixed quoting (P0), net per hour: discovery <N id="e003.p3m2_p0.disc" /> [<N id="e003.p3m2_p0.disc_lo" />, <N id="e003.p3m2_p0.disc_hi" />]; held-out <N id="e003.p3m2_p0.held" />, of which <N id="e003.p3m2_p0.held_fee_saving" /> is fee saving. Fill quality against a placebo (H1-T): held-out <N id="e003.h1t.held" unit />, interval [<N id="e003.h1t.held_tlo" />, <N id="e003.h1t.held_thi" />] spanning zero, placebo not matched on turnover; <Held check="H1-T">{rec('e003.h1t.held').lab!}</Held>.</p>,
    full: { focus: 'P3_M2', vs: 'P0', metric: 'turnover_per_hour' },
  },
  {
    short: 'What it means', title: 'What it means for real market makers',
    lead: <>For a small passive quoter, prediction is not the scarce input. The fee tier and the cost of being traded against decide the outcome; queue and speed assumptions barely move it.</>,
    num: () => <><b data-src={core.values['fee.vip0.maker'].src}>{fmt(core.values['fee.vip0.maker'].v, 0)} bp</b><span>maker fee on every fill at VIP0, the only tier this project can attain</span></>,
    visual: () => <StoryMeaning />,
    evidence: <p className="held">Under the hypothetical LP tier 4 rebate, P4’s risk controls lowered expected shortfall and drawdown relative to P3F and modestly improved its net result per hour (<N id="e003.h3.net_per_hour_diff.disc" /> USDT/h in discovery, <N id="e003.h3.net_per_hour_diff.held" /> held-out), while both remained unprofitable. Lower latency produced more fills and slightly worse results per unit traded.</p>,
    full: { focus: 'P4', vs: 'P3F', fee: 'lp_tier4', metric: 'net_per_hour' },
  },
  {
    short: 'How sure we are', title: 'How sure we are',
    lead: <>Every rule was fixed before five sealed days were opened, and they were evaluated once. The pattern held, some effects were smaller, and five days cannot settle everything.</>,
    num: () => <><N id="sample.held.sessions" strong /><span>sealed days, evaluated once, after every rule was fixed</span></>,
    visual: () => <StorySure />,
    evidence: (
      <>
        <ul className="checks" aria-label="Held-out checks, per experiment">
          <li><span className="id">E001</span><span>Fills come at the wrong moment</span><b data-label="tally">{core.holdout.tallies.E001}</b></li>
          <li><span className="id">E003</span><span>Forecast skill, fill quality, risk controls</span><b data-label="tally">{core.holdout.tallies.E003}</b></li>
          <li><span className="id">E004</span><span>Stale data: <q className="lbl" data-label="H4-W[P0]">no material deterioration under the specified threshold</q></span><b data-label="tally">{core.holdout.tallies.E004}</b></li>
          <li><span className="id">E002</span><span>Execution assumptions</span><b className="none">reported only</b></li>
        </ul>
        <p className="held">Each label is a point-estimate check on five sessions, not a significance test, and a tally is not that many independent replications. Held-out trading results are <Held>reported only, descriptive (no confirmation claim)</Held>. Every policy result is a replay: queue position is inferred and our orders have no market impact.</p>
      </>
    ),
    full: { sample: 'heldout', focus: 'P3_M2', vs: 'P0', metric: 'net_per_hour' },
  },
];

/** One step of the story, remounted per step: it arrives from the direction you moved in. */
function Stage({ dir, quiet, children }: { dir: 'fwd' | 'back'; quiet: boolean; children: ReactNode }) {
  const enter = useEnter(quiet);
  return <div className={`story-stage${enter}`} data-dir={dir}>{children}</div>;
}

function Story({ i, dir, go, openFull }: { i: number; dir: 'fwd' | 'back'; go: (j: number) => void; openFull: (s: Partial<State>) => void }) {
  const st = STORY[i];
  const [fee, setFee] = useState('vip0');
  const enter = useEnter();
  const mounted = useMounted();
  return (
    <section className={`story${enter}`} aria-labelledby="story-h">
      <ol className="story-rail" aria-label="Steps">
        {STORY.map((s, j) => (
          <li key={s.short}><button type="button" aria-current={j === i ? 'step' : undefined} className={j < i ? 'done' : undefined} onClick={() => go(j)}><span className="sr-n">{j + 1}</span><span className="sr-t">{s.short}</span></button></li>
        ))}
      </ol>
      <Stage key={i} dir={dir} quiet={!mounted.current}>
        <div className="story-t">
          <p className="story-n">Step {i + 1} of {STORY.length}</p>
          <h2 id="story-h" tabIndex={-1}>{st.title}</h2>
          <p className="story-lead">{st.lead}</p>
          {st.chips && (
            <div className="seg" role="radiogroup" aria-label="Fee schedule">
              {['vip0', 'vip9', 'lp_tier4'].map((id) => {
                const o = find(OPT.fee, id)!;
                return <button key={id} type="button" role="radio" aria-checked={fee === id} className="chip" onClick={() => setFee(id)}>{o.label}<span className="chip-s"> {o.attain}</span></button>;
              })}
            </div>
          )}
          <div className="story-num">{st.num(fee)}</div>
        </div>
        <div className="story-v">
          {st.visual(fee)}
          {st.more && <Inspect title={st.more.title}>{st.more.body}</Inspect>}
          <Inspect title="The evidence" note="exact values and labels">{st.evidence}</Inspect>
          <button type="button" className="btn quiet story-open" onClick={() => openFull(st.full)}>Open this step in the full lab</button>
        </div>
      </Stage>
      <div className="story-bar" role="group" aria-label="Step navigation">
        <button type="button" className="btn" onClick={() => go(i - 1)} disabled={i === 0}>Back</button>
        <span className="sb-where"><b>{i + 1}</b> / {STORY.length} · {st.short}</span>
        {i < STORY.length - 1
          ? <button type="button" className="btn primary" onClick={() => go(i + 1)}>Next <span className="arr" aria-hidden="true">→</span></button>
          : <button type="button" className="btn primary" onClick={() => openFull({})}>Explore freely <span className="arr" aria-hidden="true">→</span></button>}
      </div>
    </section>
  );
}

/* ------------------------------------------------------------------ page */
type Mode = 'guided' | 'full';
const STEP_RE = /(^|[#&])step=(\d+)(&|$)/;

export default function Lab() {
  const [mode, setMode] = useState<Mode>('guided');
  const [step, setStep] = useState(0);
  const [dir, setDir] = useState<'fwd' | 'back'>('fwd');
  const [S, setS] = useState<State>(DEF);
  const [bad, setBad] = useState<string[]>([]);
  const [prev, setPrev] = useState<{ S: State; r: Resolved } | null>(null);
  const [ready, setReady] = useState(false);
  const reduced = useMedia('(prefers-reduced-motion: reduce)');
  const r = useMemo(() => resolve(S, bad), [S, bad]);
  const cur = useRef({ S, r });
  cur.current = { S, r };
  const notes = useMemo(() => explain(prev, S, r), [prev, S, r]);

  useEffect(() => {
    const read = (first: boolean) => {
      const h = location.hash;
      const m = h.match(STEP_RE);
      if (m || /(^|[#&])tour=1(&|$)/.test(h) || h.replace(/^#/, '') === '') {
        setMode('guided');
        setStep(m ? Math.min(STORY.length, Math.max(1, Number(m[2]))) - 1 : 0);
        return;
      }
      const p = parseHash(h);
      if (!first) setPrev(cur.current);
      setMode('full'); setS(p.state); setBad(p.bad);
    };
    read(true);
    setReady(true);
    const onHash = () => read(false);
    addEventListener('hashchange', onHash);
    return () => removeEventListener('hashchange', onHash);
  }, []);
  useEffect(() => {
    if (!ready) return;
    if (mode === 'guided') history.replaceState(null, '', `#step=${step + 1}`);
    else if (bad.length === 0) history.replaceState(null, '', serialize(S));
  }, [mode, step, S, bad, ready]);

  const set = (p: Partial<State>) => { setPrev(cur.current); setBad([]); setS((s) => ({ ...s, ...p })); };
  const reset = () => set({ ...PRESETS.primary.set, view: 'e003' });
  const top = () => document.querySelector('.x-head')?.scrollIntoView({ behavior: reduced ? 'auto' : 'smooth', block: 'start' });
  const go = (j: number) => {
    if (j < 0 || j >= STORY.length) return;
    setDir(j < step ? 'back' : 'fwd');
    setStep(j);
    requestAnimationFrame(() => { top(); document.getElementById('story-h')?.focus({ preventScroll: true }); });
  };
  const openFull = (p: Partial<State>) => { setPrev(null); setBad([]); setS({ ...DEF, ...p }); setMode('full'); requestAnimationFrame(top); };

  return (
    <main id="main" className="wrap lab">
      <div className="x-head">
        <div>
          <h1>Explore</h1>
          <p>{mode === 'guided' ? 'Six short steps, from a working forecast to a losing market maker.' : 'Every scenario the study tested. Settings it never tested say so.'}</p>
        </div>
        <div className="mode" role="group" aria-label="Mode" data-mode={mode}>
          <button type="button" aria-pressed={mode === 'guided'} onClick={() => setMode('guided')}>Guided</button>
          <button type="button" aria-pressed={mode === 'full'} onClick={() => openFull(mode === 'full' ? S : {})}>Full lab</button>
        </div>
      </div>
      {mode === 'guided' ? <Story i={step} dir={dir} go={go} openFull={openFull} /> : <FullLab S={S} r={r} set={set} reset={reset} notes={notes} first={prev === null} />}
      <Footer />
    </main>
  );
}
