'use client';
// Teaching diagrams. Everything drawn from made-up values sits inside <Synth> (tagged "Synthetic example, not market
// data"). The two exceptions are labelled as what they are: WalkForward draws the study's real session design, and
// CountRule draws the protocol's own arithmetic.
import { useState } from 'react';
import { Synth } from '../components/Explain';
import { gauss, prng, useWidth } from '../components/hooks';
import { core } from '../data/core';
import { fmt, MINUS } from '../format';

const r1 = (v: number) => Math.round(v * 10) / 10;

/* ------------------------------------------------------------------ what an R² of a few percent looks like */
const POINTS = (() => {
  const rand = prng(20261105);
  return Array.from({ length: 240 }, () => [gauss(rand), gauss(rand)] as const);
})();

export function SkillCloud() {
  const ours = core.e003.skill.find((s) => s.side === 'held' && s.model === 'M2' && s.h === 5)!;
  const LEVELS = [
    { id: 'none', r2: 0, label: 'No skill', sub: '0%' },
    { id: 'ours', r2: ours.r2, label: 'Skill like our held-out forecast', sub: `${fmt(ours.r2 * 100, 1)}%` },
    { id: 'strong', r2: 0.3, label: 'Strong skill', sub: '30%' },
  ];
  const [lv, setLv] = useState('ours');
  const [moved, setMoved] = useState(false); // animate only changes the visitor makes, never the first layout
  const [ref, w] = useWidth<HTMLDivElement>(520);
  const L = LEVELS.find((x) => x.id === lv)!;
  const W = Math.max(280, w), H = Math.round(Math.min(320, W * 0.62)), m = { l: 40, r: 12, t: 12, b: 34 };
  const X = (v: number) => r1(m.l + ((v + 3) / 6) * (W - m.l - m.r));
  const Y = (v: number) => r1(m.t + ((3 - v) / 6) * (H - m.t - m.b));
  const b = Math.sqrt(L.r2), s = Math.sqrt(1 - L.r2);
  const pts = POINTS.map(([x, e]) => [x, b * x + s * e] as const).filter(([x, y]) => Math.abs(x) < 3 && Math.abs(y) < 3);
  return (
    <Synth title="What a forecast with a few percent R² looks like" note={<>Each dot pairs a forecast with the move that followed, both scaled to the same spread. The line is the forecast’s average relationship with the outcome. Made-up points drawn so that the forecast’s squared error is the chosen percentage lower than that of a zero-change forecast; the {fmt(ours.r2 * 100, 1)}% option matches our held-out five-second forecast.</>}>
      <div className="seg" role="radiogroup" aria-label="Forecast skill">
        {LEVELS.map((x) => (
          <button key={x.id} type="button" role="radio" aria-checked={lv === x.id} className="chip" onClick={() => { setMoved(true); setLv(x.id); }}>
            {x.label} <span className="id">{x.sub}</span>
          </button>
        ))}
      </div>
      <div ref={ref} className="mt-3">
        <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Synthetic scatter: forecast against outcome at an R squared of ${L.sub}`}>
          {[-2, 0, 2].map((t) => (
            <g key={t}>
              <line className={t === 0 ? 'axis' : 'grid'} x1={X(t)} x2={X(t)} y1={m.t} y2={H - m.b} />
              <line className={t === 0 ? 'axis' : 'grid'} x1={m.l} x2={W - m.r} y1={Y(t)} y2={Y(t)} />
            </g>
          ))}
          {pts.map(([x, y], i) => <circle key={i} className={moved ? 'syn-pt mv' : 'syn-pt'} cx={0} cy={0} r={2.3} style={{ transform: `translate(${X(x)}px, ${Y(y)}px)` }} />)}
          <line className="disc-l" x1={X(-3)} y1={Y(-3 * b)} x2={X(3)} y2={Y(3 * b)} />
          <text x={(m.l + W - m.r) / 2} y={H - 6} textAnchor="middle">forecast</text>
          <text x={m.l + 6} y={m.t + 12}>outcome</text>
          <text className="t-ink t-bold" x={W - m.r} y={m.t + 14} textAnchor="end">R² {L.sub}</text>
        </svg>
      </div>
    </Synth>
  );
}

/* ------------------------------------------------------------------ one passive fill, step by step */
const QF = [
  { k: 'Quote', t: 'We rest a bid', d: 'We offer to buy 1 SOL at the best bid, 100.000, below the mid of 100.005. If someone sells to us, we capture half the spread against the mid.' },
  { k: 'Fill', t: 'An aggressive seller trades with us', d: 'A seller who wants to trade now hits our bid. We bought 1 SOL at 100.000: half a spread, +0.5 bp, better than the mid at that moment.' },
  { k: 'Move', t: 'The price keeps moving in the seller’s direction', d: 'Over the next 30 seconds the mid falls to 99.990. A trader who sells aggressively may know, or may simply cause, a move the passive side does not see coming.' },
  { k: 'Result', t: 'Marked to the new mid, the fill lost money', d: 'The SOL we bought for 100.000 is now worth 99.990: +0.5 bp captured, −1.5 bp from the move, −1.0 bp in all, before a 10 bp maker fee is charged on top.' },
];

export function QuoteFill() {
  const [st, setSt] = useState(0);
  const [ref, w] = useWidth<HTMLDivElement>(560);
  const W = Math.max(300, w), H = 230, m = { l: 62, r: 16, t: 18, b: 34 };
  const P = (p: number) => r1(m.t + ((100.015 - p) / 0.03) * (H - m.t - m.b));
  const T = (t: number) => r1(m.l + (t / 40) * (W - m.l - m.r));
  const tf = 8; // fill time
  const mid = [[0, 100.005], [tf, 100.005], [tf + 2, 99.999], [tf + 8, 99.994], [tf + 18, 99.992], [tf + 30, 99.99], [40, 99.99]] as const;
  const shown = mid.filter(([t]) => st >= 2 || t <= tf);
  return (
    <Synth title="How a passive fill can turn against the market maker" note={<>Made-up prices for one fill. Real fills go both ways; E001 measures the <em>average</em> outcome after aggressive trades, shown below.</>}>
      <ol className="stepper" aria-label="Stages of one fill">
        {QF.map((q, i) => (
          <li key={q.k}><button type="button" className="chip" aria-pressed={st === i} aria-current={st === i ? 'step' : undefined} onClick={() => setSt(i)}><span className="id">{i + 1}</span> {q.k}</button></li>
        ))}
      </ol>
      <div ref={ref} className="mt-3">
        <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Synthetic example, stage ${st + 1}: ${QF[st].t}`}>
          {[100.01, 100.0, 99.99].map((p) => (
            <g key={p}>
              <line className="grid" x1={m.l} x2={W - m.r} y1={P(p)} y2={P(p)} />
              <text className="t-num" x={m.l - 8} y={P(p) + 4} textAnchor="end">{p.toFixed(3)}</text>
            </g>
          ))}
          <line className="axis" x1={m.l} x2={m.l} y1={m.t} y2={H - m.b} />
          <text className="t-ink2" x={T(1)} y={P(100.01) - 6}>best ask</text>
          <text className="t-ink2" x={T(1)} y={P(100.0) + 16}>best bid</text>
          <path className="disc-l" d={'M' + shown.map(([t, p]) => `${T(t)} ${P(p)}`).join('L')} />
          <text className="t-teal t-bold" x={T(st >= 2 ? 40 : tf) - 2} y={P(st >= 2 ? 99.99 : 100.005) - 8} textAnchor="end">mid</text>
          {st === 0 && <rect className="bar-held" x={T(tf) - 7} y={P(100.0) - 7} width={14} height={14} />}
          {st === 0 && <text className="t-ink" x={T(tf) + 12} y={P(100.0) + 4}>our bid, 1 SOL</text>}
          {st >= 1 && (
            <>
              <path className="leader" d={`M${T(tf - 5)} ${P(100.013)}L${T(tf) - 4} ${P(100.0) - 6}`} markerEnd="url(#qf-arr)" />
              <text className="t-ink2" x={T(tf - 5)} y={P(100.013) - 4} textAnchor="middle">seller</text>
              <circle className="bar-ink" cx={T(tf)} cy={P(100.0)} r={6} />
              <text className="t-ink" x={T(tf) + 10} y={P(100.0) + 18}>bought at 100.000</text>
            </>
          )}
          {st >= 3 && (
            <>
              <line className="ci-ink" x1={T(38)} x2={T(38)} y1={P(100.0)} y2={P(99.99)} />
              <line className="ci-ink" x1={T(37)} x2={T(39)} y1={P(100.0)} y2={P(100.0)} />
              <line className="ci-ink" x1={T(37)} x2={T(39)} y1={P(99.99)} y2={P(99.99)} />
              <text className="t-ink t-bold" x={T(38) - 8} y={P(99.995) + 4} textAnchor="end">{MINUS}1.0 bp</text>
            </>
          )}
          <defs><marker id="qf-arr" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L8 4L0 8Z" className="bar-ink" /></marker></defs>
          <text x={T(tf)} y={H - 12} textAnchor="middle">fill</text>
          <text x={T(tf + 30)} y={H - 12} textAnchor="middle">30 s later</text>
        </svg>
      </div>
      <div className="stage-t" aria-live="polite"><b>{QF[st].t}.</b> {QF[st].d}</div>
      <div className="stage-nav">
        <button type="button" className="btn" onClick={() => setSt((s) => Math.max(0, s - 1))} disabled={st === 0}>Back</button>
        <button type="button" className="btn primary" onClick={() => setSt((s) => Math.min(3, s + 1))} disabled={st === 3}>Next stage <span className="arr" aria-hidden="true">→</span></button>
      </div>
    </Synth>
  );
}

/* ------------------------------------------------------------------ the three fill models on one queue */
const FM = {
  conservative: { label: 'Conservative', ahead: 6, how: 'The 3 cancelled SOL are assumed to come from behind us. Nobody ahead leaves: 6 SOL still stand in front of our order.' },
  intermediate: { label: 'Intermediate (primary)', ahead: 4, how: 'The 3 SOL are spread pro rata over the queue: 6 of the 9 other SOL are ahead of us, so 2 of the 3 cancelled come from ahead. 4 SOL remain in front.' },
  optimistic: { label: 'Optimistic', ahead: 3, how: 'The 3 SOL are assumed to come from ahead first. Only 3 SOL remain in front, and an order would also fill if the price traded through it.' },
} as const;

export function QueueModels() {
  const [fm, setFm] = useState<keyof typeof FM>('intermediate');
  const [moved, setMoved] = useState(false);
  const mv = moved ? ' mv' : '';
  const [ref, w] = useWidth<HTMLDivElement>(560);
  const M = FM[fm];
  const W = Math.max(300, w), H = 150, unit = Math.min(40, (W - 40) / 11);
  const x0 = 16;
  const sold = 4; // an aggressive seller then sells 4 SOL at this price
  const filled = M.ahead < sold;
  return (
    <Synth title="Where is our order in the queue?" note="Made-up queue. Market data show how much rests at the best bid and that 3 SOL were cancelled there, but not whose orders they were or where our simulated order would stand. The three fill models are three answers to that question; the market replay itself is identical under all three.">
      <div className="seg" role="radiogroup" aria-label="Fill model">
        {(Object.keys(FM) as Array<keyof typeof FM>).map((k) => (
          <button key={k} type="button" role="radio" aria-checked={fm === k} className="chip" onClick={() => { setMoved(true); setFm(k); }}>{FM[k].label}</button>
        ))}
      </div>
      <div ref={ref} className="mt-3">
        <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Synthetic queue under the ${M.label} fill model: ${M.ahead} SOL ahead of our order; a 4 SOL sell ${filled ? 'fills' : 'does not fill'} our order`}>
          <text className="t-ink2" x={x0} y={16}>best bid, front of the queue →</text>
          <g style={{ transform: `translateX(${x0}px)` }}>
            <rect className={`bar-held${mv}`} x={0} y={30} width={1} height={34} style={{ transform: `scaleX(${unit * M.ahead})` }} vectorEffect="non-scaling-stroke" />
            <text className={`t-ink t-num${mv}`} x={0} y={52} style={{ transform: `translateX(${(unit * M.ahead) / 2}px)` }} textAnchor="middle">{M.ahead} SOL ahead</text>
            <rect className={`bar-disc${mv}`} x={0} y={30} width={unit} height={34} style={{ transform: `translateX(${unit * M.ahead + 2}px)` }} />
            <text className={`t-ink t-bold${mv}`} x={0} y={82} style={{ transform: `translateX(${unit * M.ahead + 2 + unit / 2}px)` }} textAnchor="middle">us</text>
          </g>
          <line className="leader" x1={x0} x2={x0 + unit * sold} y1={104} y2={104} />
          <line className="ci-ink" x1={x0 + unit * sold} x2={x0 + unit * sold} y1={96} y2={112} />
          <text className="t-ink2" x={x0} y={126}>a seller then sells {sold} SOL at this price</text>
          <text className={filled ? 't-teal t-bold' : 't-ink t-bold'} x={x0} y={144}>{filled ? 'Our order is filled.' : 'Our order is not reached: no fill.'}</text>
        </svg>
      </div>
      <p className="stage-t" aria-live="polite"><b>{M.label}.</b> {M.how}</p>
    </Synth>
  );
}

/* ------------------------------------------------------------------ E004: stale view, and the placebo window */
export function StaleWindow() {
  const [ref, w] = useWidth<HTMLDivElement>(560);
  const W = Math.max(300, w), H = 172, l = 92, r = 12;
  const T = (t: number) => r1(l + (t / 100) * (W - l - r));
  const ticks = Array.from({ length: 50 }, (_, i) => i * 2 + 1);
  return (
    <Synth title="A connection drop, a stale window and its placebo" note="Made-up timeline. During a drop, book updates never reach the participant, so it keeps acting on an old picture. E004 compares the quality of fills inside such stale windows with fills inside placebo windows of exactly the same lengths, placed at random times in the same run.">
      <div ref={ref}>
        <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Synthetic timeline: exchange updates continue; the participant's view misses updates during a drop; a placebo window of equal length sits at a random time">
          <text className="t-ink2" x={l - 10} y={34} textAnchor="end">exchange</text>
          <text className="t-ink2" x={l - 10} y={74} textAnchor="end">our view</text>
          <text className="t-ink2" x={l - 10} y={124} textAnchor="end">windows</text>
          {ticks.map((t) => <line key={`e${t}`} className="tick" x1={T(t)} x2={T(t)} y1={24} y2={40} />)}
          {ticks.filter((t) => t < 30 || t > 46).map((t) => <line key={`v${t}`} className="tick" x1={T(t)} x2={T(t)} y1={64} y2={80} />)}
          <rect className="band" x={T(30)} y={58} width={T(46) - T(30)} height={28} />
          <text className="t-ink" x={(T(30) + T(46)) / 2} y={98} textAnchor="middle">drop: updates lost</text>
          <defs>
            <pattern id="stale-hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <rect className="stale-bg" width="5" height="5" /><line className="stale-ln" x1="0" y1="0" x2="0" y2="5" />
            </pattern>
          </defs>
          <rect className="bar-stale" x={T(32)} y={112} width={T(48) - T(32)} height={18} />
          <text className="t-ink" x={T(32)} y={146}>stale window W<tspan dy="3" fontSize="9">U</tspan></text>
          <rect className="bar-held" x={T(70)} y={112} width={T(86) - T(70)} height={18} />
          <text className="t-ink" x={T(70)} y={146}>placebo W<tspan dy="3" fontSize="9">P</tspan>, random time</text>
          {[35, 41, 44].map((t) => <circle key={t} className="bar-ink" cx={T(t)} cy={121} r={3.2} />)}
          {[73, 80].map((t) => <circle key={t} className="bar-ink" cx={T(t)} cy={121} r={3} />)}
          <text x={l} y={H - 4}>dots: our fills inside each window</text>
        </svg>
      </div>
    </Synth>
  );
}

/* ------------------------------------------------------------------ a limit order book */
const BOOK = { asks: [[100.05, 14], [100.04, 9], [100.03, 22], [100.02, 6], [100.01, 11]], bids: [[100.0, 12], [99.99, 18], [99.98, 7], [99.97, 25], [99.96, 10]] } as const;

export function BookLadder() {
  const [ref, w] = useWidth<HTMLDivElement>(520);
  const W = Math.max(300, w), rowH = 22, H = rowH * 10 + 44, mid = W / 2, k = (mid - 70) / 26;
  return (
    <Synth title="A limit order book, top five levels" note="Made-up sizes and prices on a 0.01 tick. Resting orders wait at each price; the best bid and best ask together are the touch. A passive market maker posts at the touch and waits; an aggressive trader crosses the spread and trades with the resting orders immediately.">
      <div ref={ref}>
        <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Synthetic order book: five ask levels above five bid levels, one tick apart, with the spread between the best bid and best ask">
          <text className="t-ink2" x={mid - 8} y={14} textAnchor="end">size waiting, SOL</text>
          <text className="t-ink2" x={mid + 8} y={14}>price, USDT</text>
          {BOOK.asks.map(([p, s], i) => {
            const y = 24 + i * rowH;
            return (
              <g key={p}>
                <rect className="bar-held" x={mid - 4 - s * k} y={y + 3} width={s * k} height={rowH - 6} />
                <text className="t-num t-ink" x={mid + 8} y={y + rowH / 2 + 4}>{p.toFixed(2)}</text>
                <text className="t-num" x={mid - 8 - s * k} y={y + rowH / 2 + 4} textAnchor="end">{s}</text>
                {i === 4 && <text className="t-ink t-bold" x={mid + 64} y={y + rowH / 2 + 2}>best ask</text>}
              </g>
            );
          })}
          <line className="zero" x1={mid - 60} x2={mid + 56} y1={24 + 5 * rowH + 1} y2={24 + 5 * rowH + 1} />
          <text className="t-teal t-bold" x={mid + 64} y={24 + 5 * rowH + 6} fontSize="11">spread: 1 tick</text>
          {BOOK.bids.map(([p, s], i) => {
            const y = 24 + 5 * rowH + 4 + i * rowH;
            return (
              <g key={p}>
                <rect className="bar-disc" x={mid - 4 - s * k} y={y + 3} width={s * k} height={rowH - 6} />
                <text className="t-num t-ink" x={mid + 8} y={y + rowH / 2 + 4}>{p.toFixed(2)}</text>
                <text className="t-num" x={mid - 8 - s * k} y={y + rowH / 2 + 4} textAnchor="end">{s}</text>
                {i === 0 && <text className="t-ink t-bold" x={mid + 64} y={y + rowH / 2 + 8}>best bid</text>}
              </g>
            );
          })}
        </svg>
      </div>
    </Synth>
  );
}

/* ------------------------------------------------------------------ the study's real walk-forward design (not synthetic) */
export function WalkForward() {
  const { train, validation, test } = core.sample.splits;
  const disc = [...train, ...validation];
  const wf = core.sample.walkforward;
  const [ref, w] = useWidth<HTMLDivElement>(620);
  const W = Math.max(300, w), cols = 20, l = 78, r = 8, cell = (W - l - r) / cols, rowH = 15;
  const rows = [...wf.map((d) => ({ d, fit: disc.filter((x) => x < d), ev: [d] })), { d: 'held-out', fit: disc, ev: test }];
  const all = [...disc, ...test];
  const H = rows.length * rowH + 40;
  const lab = (d: string) => (d === 'held-out' ? 'held-out' : d.slice(0, 7));
  return (
    <figure className="panel" data-src={core.sample.splits_src}>
      <figcaption><b>Walk-forward evaluation, then one holdout</b><span>The study’s real design. Each row is one evaluation: hollow squares are the sessions its forecasts were fitted on, filled squares the session it was evaluated on. No row ever sees a later session.</span></figcaption>
      <div ref={ref}>
        <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Walk-forward design: ${wf.length} evaluation sessions, each fitted only on earlier sessions; the ${test.length} held-out sessions evaluated once with models fitted on all ${disc.length} discovery sessions`}>
          {rows.map((row, i) => {
            const y = 8 + i * rowH;
            return (
              <g key={row.d}>
                <text className="t-num" x={l - 8} y={y + 10} textAnchor="end" fontSize="11">{lab(row.d)}</text>
                {all.map((d, j) => {
                  const x = l + j * cell + 1.5, s = Math.min(cell - 3, 11);
                  if (row.ev.includes(d)) return <rect key={d} className={row.d === 'held-out' ? 'bar-ink' : 'bar-disc'} x={x} y={y + 1} width={s} height={s} />;
                  if (row.fit.includes(d)) return <rect key={d} className="abst" x={x + 0.75} y={y + 1.75} width={s - 1.5} height={s - 1.5} />;
                  return null;
                })}
              </g>
            );
          })}
          <line className="ref" x1={l + disc.length * cell} x2={l + disc.length * cell} y1={2} y2={H - 26} />
          <text x={l} y={H - 8}>{all[0].slice(0, 7)}</text>
          <text x={l + disc.length * cell - 4} y={H - 8} textAnchor="end">{disc[disc.length - 1].slice(0, 7)}</text>
          <text x={W - r} y={H - 8} textAnchor="end">{all[all.length - 1].slice(0, 7)}</text>
        </svg>
      </div>
    </figure>
  );
}

/* ------------------------------------------------------------------ the protocol's count rule (arithmetic, not data) */
export function CountRule() {
  const combos = Array.from({ length: 32 }, (_, i) => [0, 1, 2, 3, 4].map((b) => (i >> b) & 1));
  const meets = (c: number[]) => c.reduce((a, b) => a + b, 0) >= 4;
  const [ref, w] = useWidth<HTMLDivElement>(620);
  const W = Math.max(280, w), cols = W < 560 ? 16 : 32, bands = 32 / cols;
  const cell = (W - 8) / cols, s = Math.min(cell - 3, 13), bandH = 5 * (s + 2) + 14, H = bands * bandH;
  return (
    <figure className="panel" data-meta="protocol arithmetic">
      <figcaption><b>All 32 ways five sessions can fall</b><span>Arithmetic, not data. If each held-out session were a coin flip around the threshold, these 32 patterns would be equally likely. Each column is one pattern of five sessions; a filled square is a session on the discovery side.</span></figcaption>
      <div ref={ref}>
        <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="All 32 patterns of five sessions; 6 of them have at least four of five sessions on the discovery side">
          {combos.map((c, i) => {
            const x = 4 + (i % cols) * cell, y = Math.floor(i / cols) * bandH;
            return (
              <g key={i}>
                {meets(c) && <rect className="band" x={x - 1.5} y={y} width={s + 3} height={5 * (s + 2) + 2} />}
                {c.map((b, j) => <rect key={j} className={b ? (meets(c) ? 'bar-ink' : 'bar-disc') : 'abst'} x={x} y={y + 1 + j * (s + 2)} width={s} height={s} />)}
              </g>
            );
          })}
        </svg>
      </div>
      <p className="readline"><b>6 of the 32 patterns</b> (shaded, dark squares) meet a four-of-five rule by chance: 6/32 = 18.75%.</p>
    </figure>
  );
}
