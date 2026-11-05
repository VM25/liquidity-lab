// Homepage and Research figures drawn from the frozen bundle. No value is computed here beyond screen coordinates,
// except where a label says so. Every chart takes its rendered width so text keeps its size on a phone.
import { useState } from 'react';
import { core, rec } from '../data/core';
import { LAB, cellKey } from '../lab/model';
import { MINUS, axisLab, fmt } from '../format';

const pol = (p: string) => core.e003.policies_vip0.find((r) => r.policy === p)!;
const TRADED = ['P0', 'P1', 'P3_M1', 'P3_M2', 'P3_negM2'];
const r1 = (v: number) => Math.round(v * 10) / 10;
const skill = (side: 'disc' | 'held', h: number) => core.e003.skill.find((s) => s.side === side && s.model === 'M2' && s.h === h)!;
const NAME: Record<string, string> = { P0: 'P0', P1: 'P1', P3_M1: 'P3[M1]', P3_M2: 'P3[M2]', P3_negM2: `P3[${MINUS}M2]`, P3F: 'P3F', P4: 'P4' };

function diamond(x: number, y: number, k: number, cls: string) {
  return <path className={cls} d={`M${x} ${y - k}L${x + k} ${y}L${x} ${y + k}L${x - k} ${y}Z`} />;
}

/* ------------------------------------------------------------------ the hero: the paradox, simply */
/** Two separate measurements, each in its own region with its own axis and scale: forecast skill (R², from a 0% baseline)
 *  and the hourly trading result of two quoting rules (USDT per hour, from a break-even line). They share no axis. */
export function HeroDuo({ W }: { W: number }) {
  const stack = W < 460;
  const d5 = skill('disc', 5).r2, h5 = skill('held', 5).r2;
  const rules: Array<[string, string]> = [['P0', 'Fixed quoting'], ['P3_M2', 'Forecast-gated']];
  const ax = 34; // room for each region's own tick labels
  // region boxes: [x0, x1, top of plot, bottom of plot]
  const A = stack ? { x0: 0, x1: W, t: 58, b: 176 } : { x0: 0, x1: W * 0.36, t: 64, b: 268 };
  const B = stack ? { x0: 0, x1: W, t: 268, b: 436 } : { x0: W * 0.36 + 34, x1: W, t: 64, b: 268 };
  const H = stack ? 512 : 346;
  const titleY = (R: typeof A) => R.t - 44;
  const Ys = (v: number) => r1(A.b - (v / 0.05) * (A.b - A.t));
  const Yn = (v: number) => r1(B.t + (-v / 200) * (B.b - B.t));
  const bw = stack ? 28 : 30;
  const sx = A.x0 + ax + (A.x1 - A.x0 - ax) / 2;
  const colR = (B.x1 - B.x0 - ax) / 2;
  const v0 = (x: number) => fmt(x, 0, false);
  return (
    <svg className="fig duo-fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-labelledby="hd-t hd-d" data-src="results/e003/e003_analysis.json#/descriptive/forecasts; results/closeout/closeout_analysis.json#/experiments/E003/reported_only/descriptive/forecasts; results/e003/e003_analysis.json#/participation/policies; results/closeout/closeout_analysis.json#/experiments/E003/policies_vip0_descriptive/policies">
      <title id="hd-t">Two separate measurements: forecast skill, and the trading result of two quoting rules</title>
      <desc id="hd-d">{`Left, on its own scale: five-second forecast skill, out-of-sample R squared against a zero-change forecast, ${fmt(d5 * 100, 1)} percent in discovery and ${fmt(h5 * 100, 1)} percent held-out. Right, on its own scale: net result per hour at VIP0, below break-even for both rules: fixed quoting ${fmt(pol('P0').disc_net, 1, true)} USDT in discovery and ${fmt(pol('P0').held_net, 1, true)} held-out; forecast-gated quoting ${fmt(pol('P3_M2').disc_net, 1, true)} and ${fmt(pol('P3_M2').held_net, 1, true)}.`}</desc>

      <g className="region">
        <text className="t-strong" x={A.x0} y={titleY(A)}>Forecast skill</text>
        <text x={A.x0} y={titleY(A) + 17}>R² vs a zero-change forecast, 5 s ahead</text>
        {[0, 0.02, 0.04].map((t) => (
          <g key={t}>
            <line className={t === 0 ? 'axis' : 'grid'} x1={A.x0 + ax} x2={A.x1} y1={Ys(t)} y2={Ys(t)} />
            <text className="t-num" x={A.x0 + ax - 6} y={Ys(t) + 4} textAnchor="end">{t * 100}%</text>
          </g>
        ))}
        <rect className="bar-disc" x={sx - bw - 3} y={Ys(d5)} width={bw} height={r1(A.b - Ys(d5))} />
        <rect className="bar-held" x={sx + 3} y={Ys(h5)} width={bw} height={r1(A.b - Ys(h5))} />
        <text className="t-ink t-num" x={sx - 3 - bw / 2} y={Ys(d5) - 8} textAnchor="middle">{fmt(d5 * 100, 1)}%</text>
        <text className="t-ink t-num t-bold" x={sx + 3 + bw / 2} y={Ys(h5) - 8} textAnchor="middle">{fmt(h5 * 100, 1)}%</text>
      </g>

      {!stack && <line className="grid" x1={B.x0 - 17} x2={B.x0 - 17} y1={titleY(A) - 12} y2={A.b + 26} />}

      <g className="region">
        <text className="t-strong" x={B.x0} y={titleY(B)}>Trading result</text>
        <text x={B.x0} y={titleY(B) + 17}>USDT per hour after fees, at the attainable fee</text>
        {[-100, -200].map((t) => (
          <g key={t}>
            <line className="grid" x1={B.x0 + ax} x2={B.x1} y1={Yn(t)} y2={Yn(t)} />
            <text className="t-num" x={B.x0 + ax - 6} y={Yn(t) + 4} textAnchor="end">{MINUS}{-t}</text>
          </g>
        ))}
        <line className="zero-c" x1={B.x0 + ax} x2={B.x1} y1={B.t} y2={B.t} />
        <text className="t-num" x={B.x0 + ax - 6} y={B.t + 4} textAnchor="end">0</text>
        <text className="t-coral t-bold" x={B.x1} y={B.t - 8} textAnchor="end">break-even</text>
        {rules.map(([p, name], i) => {
          const cx = B.x0 + ax + colR * (i + 0.5), x = pol(p);
          return (
            <g key={p}>
              <rect className="bar-disc" x={cx - bw - 3} y={B.t} width={bw} height={r1(Yn(x.disc_net) - B.t)} />
              <rect className="bar-held" x={cx + 3} y={B.t} width={bw} height={r1(Yn(x.held_net) - B.t)} />
              <text className="t-ink t-num" x={cx - 3 - bw / 2} y={Yn(x.disc_net) + 18} textAnchor="middle">{MINUS}{v0(-x.disc_net)}</text>
              <text className="t-ink t-num t-bold" x={cx + 3 + bw / 2} y={Yn(x.held_net) + 18} textAnchor="middle">{MINUS}{v0(-x.held_net)}</text>
              <text className="t-ink" x={cx} y={B.b + 36} textAnchor="middle">{name}</text>
            </g>
          );
        })}
      </g>

      <g transform={`translate(0 ${H - 6})`}>
        <rect className="bar-disc" x={0} y={-10} width={11} height={11} /><text x={17} y={0}>Discovery</text>
        <rect className="bar-held" x={96} y={-10} width={11} height={11} /><text x={113} y={0}>Held-out</text>
      </g>
    </svg>
  );
}

/* ------------------------------------------------------------------ the paradox in one picture */
/** Above one zero line, forecast skill (observed); below it, the trading result at VIP0 (modeled). Two measures, two scales. */
export function ParadoxPair({ W }: { W: number }) {
  const compact = W < 520;
  const l = 4, r = 4, y0 = compact ? 178 : 196, topH = y0 - (compact ? 74 : 80), botH = compact ? 132 : 150;
  const split = l + (W - l - r) * (compact ? 0.37 : 0.36), gap = compact ? 10 : 18;
  const H = y0 + botH + (compact ? 44 : 30) + 44;
  const hs = [1, 5, 30];
  const pos = ['P0', 'P1', 'P3_M1', 'P3_M2', 'P3_negM2', 'P3F', 'P4'];
  const Ys = (v: number) => r1(y0 - (v / 0.06) * topH);
  const Yn = (v: number) => r1(y0 + (-v / 200) * botH);
  const colT = (split - gap - l) / 3, x0R = split + gap, colB = (W - r - x0R) / pos.length;
  const bwT = Math.min(W > 820 ? 30 : 18, colT * 0.27), bwB = Math.min(W > 820 ? 24 : 16, colB * 0.3);
  const lab = y0 + botH + 16;
  const desc = `Upper left: out-of-sample R squared of the eight-feature forecast, held-out ${hs.map((h) => fmt(skill('held', h).r2 * 100, 1)).join(', ')} percent at 1, 5 and 30 seconds, all above zero. Lower right: net result per hour at VIP0 in the primary scenario; every policy that trades is below zero in both samples, P0 ${fmt(pol('P0').held_net, 1, true)} USDT per hour held-out; P3F and P4 abstain.`;
  return (
    <svg className={`fig paradox${W > 820 ? ' big' : ''}`} viewBox={`0 0 ${W} ${H}`} role="img" aria-labelledby="pp-t pp-d" data-src="results/closeout/closeout_analysis.json#/experiments/E003/reported_only/descriptive/forecasts; results/closeout/closeout_analysis.json#/experiments/E003/policies_vip0_descriptive/policies; results/e003/e003_analysis.json#/participation/policies">
      <title id="pp-t">Forecast skill above zero, trading results below zero</title>
      <desc id="pp-d">{desc}</desc>
      <text className="t-strong" x={l} y={16}>Prediction: forecast skill</text>
      <text x={l} y={33}>{compact ? 'out-of-sample R² · observed' : 'out-of-sample R², eight-feature model · observed'}</text>
      <line className="ref" x1={split} x2={split} y1={44} y2={H - 50} />
      {hs.map((h, i) => {
        const cx = l + colT * (i + 0.5), d = skill('disc', h).r2, o = skill('held', h).r2;
        return (
          <g key={h}>
            <rect className="bar-disc" x={cx - bwT - 1.5} y={Ys(d)} width={bwT} height={r1(y0 - Ys(d))} />
            <rect className="bar-held" x={cx + 1.5} y={Ys(o)} width={bwT} height={r1(y0 - Ys(o))} />
            <text className="t-ink t-num t-bold" x={cx} y={Ys(Math.max(d, o)) - 7} textAnchor="middle">{fmt(o * 100, 1)}%</text>
            <text className="t-ink2" x={cx} y={y0 + 17} textAnchor="middle">{compact ? `${h} s` : `${h} s ahead`}</text>
          </g>
        );
      })}
      <line className="zero-c" x1={l} x2={W - r} y1={y0} y2={y0} />
      <text className="t-coral t-bold" x={split + 8} y={y0 - 9}>zero: break-even</text>
      {pos.map((p, i) => {
        const cx = x0R + colB * (i + 0.5), x = pol(p);
        const ly = lab + (compact && i % 2 ? 15 : 0);
        const name = <text className="t-ink" x={cx} y={ly} textAnchor="middle" fontSize={compact ? 11 : 12}>{NAME[p]}</text>;
        if (x.disc_turnover === 0) {
          return (
            <g key={p}>
              <rect className="abst" x={cx - 5} y={y0 - 5} width={10} height={10} />
              {name}
            </g>
          );
        }
        return (
          <g key={p}>
            <rect className="bar-disc" x={cx - bwB - 1.5} y={y0} width={bwB} height={r1(Yn(x.disc_net) - y0)} />
            <rect className="bar-held" x={cx + 1.5} y={y0} width={bwB} height={r1(Yn(x.held_net) - y0)} />
            {name}
          </g>
        );
      })}
      <text x={x0R + colB * 6} y={y0 - 12} textAnchor="middle" fontSize="11">abstain</text>
      <text className="t-strong" x={W - r} y={H - 24} textAnchor="end">Trading: net result per hour at VIP0</text>
      <text x={W - r} y={H - 7} textAnchor="end">{compact ? 'USDT/h · modeled replay' : 'USDT per hour, primary scenario · modeled (historical replay)'}</text>
    </svg>
  );
}

/* ------------------------------------------------------------------ step 1: real forecast skill */
export function SkillBars({ W }: { W: number }) {
  const H = 250, l = 44, r = 10, t = 20, b = 34;
  const hs = [1, 5, 30];
  const Y = (v: number) => r1(H - b - (v / 0.06) * (H - t - b));
  const col = (W - l - r) / 3, bw = Math.min(30, col * 0.26);
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Out-of-sample R squared of the eight-feature forecast at 1, 5 and 30 seconds: discovery ${hs.map((h) => fmt(skill('disc', h).r2 * 100, 2)).join(', ')} percent; held-out ${hs.map((h) => fmt(skill('held', h).r2 * 100, 2)).join(', ')} percent`} data-src={`${skill('disc', 5).src}; ${skill('held', 5).src}`}>
      {[0, 2, 4, 6].map((p) => (
        <g key={p}>
          <line className={p === 0 ? 'zero' : 'grid'} x1={l} x2={W - r} y1={Y(p / 100)} y2={Y(p / 100)} />
          <text className="t-num" x={l - 8} y={Y(p / 100) + 4} textAnchor="end">{p}%</text>
        </g>
      ))}
      {hs.map((h, i) => {
        const cx = l + col * (i + 0.5), d = skill('disc', h).r2, o = skill('held', h).r2;
        return (
          <g key={h}>
            <rect className="bar-disc" x={cx - bw - 3} y={Y(d)} width={bw} height={r1(Y(0) - Y(d))} />
            <rect className="bar-held" x={cx + 3} y={Y(o)} width={bw} height={r1(Y(0) - Y(o))} />
            <text className="t-ink t-num" x={cx - 3 - bw / 2} y={Y(d) - 6} textAnchor="middle">{fmt(d * 100, 1)}</text>
            <text className="t-ink t-num t-bold" x={cx + 3 + bw / 2} y={Y(o) - 6} textAnchor="middle">{fmt(o * 100, 1)}</text>
            <text className="t-ink2" x={cx} y={H - 12} textAnchor="middle">{h} s ahead</text>
          </g>
        );
      })}
    </svg>
  );
}

/* ------------------------------------------------------------------ step 2: the passive side's realized spread (E001) */
export function SpreadPath({ W }: { W: number }) {
  const H = 260, l = 48, r = 14, t = 16, b = 40;
  const hs = ['0.1', '1', '5', '30', '60'];
  const X = (h: string) => r1(l + ((Math.log10(Number(h)) + 1) / (Math.log10(60) + 1)) * (W - l - r));
  const Y = (v: number) => r1(t + ((0.5 - v) / 2) * (H - t - b));
  const v = (h: string, side: 'disc' | 'held') => rec(`e001.rs_${h}s.${side}`).v!;
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Realized spread of the passive side after aggressive trades, by horizon: 30 seconds ${fmt(v('30', 'disc'), 2, true)} bp in discovery, ${fmt(v('30', 'held'), 2, true)} bp held-out; below zero means the liquidity supplier lost on average`} data-src="results/e001/e001_discovery.json#/primary; results/closeout/closeout_analysis.json#/experiments/E001">
      {[0.5, 0, -0.5, -1, -1.5].map((g) => (
        <g key={g}>
          <line className={g === 0 ? 'zero' : 'grid'} x1={l} x2={W - r} y1={Y(g)} y2={Y(g)} />
          <text className="t-num" x={l - 8} y={Y(g) + 4} textAnchor="end">{g > 0 ? '+' + g : axisLab(g)}</text>
        </g>
      ))}
      <text className="t-ink2" x={W - r} y={Y(0) - 7} textAnchor="end">passive side breaks even</text>
      <text className="t-ink t-bold" x={W - r} y={Y(-1.5) - 6} textAnchor="end">passive side loses</text>
      {hs.map((h) => <text key={h} className="t-ink2" x={X(h)} y={H - 20} textAnchor="middle">{h} s</text>)}
      <text x={(l + W - r) / 2} y={H - 3} textAnchor="middle">time after the aggressive trade (log scale)</text>
      <path className="disc-l" d={'M' + hs.map((h) => `${X(h)} ${Y(v(h, 'disc'))}`).join('L')} />
      <path className="ho-l" d={'M' + hs.map((h) => `${X(h)} ${Y(v(h, 'held'))}`).join('L')} />
      {hs.map((h) => {
        const primary = h === '1' || h === '5' || h === '30';
        return (
          <g key={h}>
            {primary && <line className="disc-w" x1={X(h)} x2={X(h)} y1={Y(rec(`e001.rs_${h}s.disc_lo`).v!)} y2={Y(rec(`e001.rs_${h}s.disc_hi`).v!)} />}
            <circle className="disc" cx={X(h)} cy={Y(v(h, 'disc'))} r={4.2} />
            {diamond(X(h), Y(v(h, 'held')), 5.2, 'ho')}
          </g>
        );
      })}
      <text className="t-ink t-num t-bold" x={X('30') - 10} y={Y(v('30', 'disc')) + 4} textAnchor="end">{fmt(v('30', 'disc'), 2, true)}</text>
      <text className="t-ink t-num" x={X('30') - 10} y={Y(v('30', 'held')) - 8} textAnchor="end">{fmt(v('30', 'held'), 2, true)}</text>
    </svg>
  );
}

/* ------------------------------------------------------------------ step 3: P0 before and after fees (E003) */
export function FeeBreakdown({ W, side }: { W: number; side: 'disc' | 'held' }) {
  const H = 150, l = 10, r = 10;
  const X = (v: number) => r1(l + ((v + 13) / 14) * (W - l - r));
  const g = rec(side === 'disc' ? 'e003.p0_primary.gross_bp' : 'e003.p0_primary.held_gross_bp');
  const n = rec(side === 'disc' ? 'e003.p0_primary.net_bp' : 'e003.p0_primary.held_net_bp');
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`P0, primary scenario, ${side === 'disc' ? 'discovery' : 'held-out'}: ${fmt(g.v, 2, true)} bp of traded notional before fees and ${fmt(n.v, 2, true)} bp after the VIP0 fee`} data-src={`${g.src}; ${n.src}`}>
      {[-12, -9, -6, -3, 0].map((t) => (
        <g key={t}>
          <line className={t === 0 ? 'zero' : 'grid'} x1={X(t)} x2={X(t)} y1={18} y2={112} />
          <text className="t-num" x={X(t)} y={128} textAnchor="middle">{axisLab(t)}</text>
        </g>
      ))}
      <text x={W - r} y={146} textAnchor="end">bp of traded notional · zero is break-even</text>
      <rect className={`${side === 'disc' ? 'bar-disc' : 'bar-held'} mv`} x={X(g.v!)} y={30} width={r1(X(0) - X(g.v!))} height={26} />
      <text className="t-ink t-num" x={X(g.v!) - 6} y={48} textAnchor="end">before fees {fmt(g.v, 2, true)}</text>
      <rect className="bar-fee mv" x={X(n.v!)} y={70} width={r1(X(g.v!) - X(n.v!))} height={26} />
      <text className="t-ink t-bold" x={(X(n.v!) + X(g.v!)) / 2} y={88} textAnchor="middle">VIP0 fee</text>
      <text className="t-ink t-num t-bold" x={X(n.v!)} y={14} textAnchor="start">after fees {fmt(n.v, 2, true)}</text>
      <line className="leader" x1={X(n.v!)} x2={X(n.v!)} y1={18} y2={70} />
    </svg>
  );
}

/* ------------------------------------------------------------------ step 3: the same fills under five fee schedules (E002) */
export function FeeSchedules({ W, sel, onSel }: { W: number; sel: string; onSel: (id: string) => void }) {
  const fees = core.e002.fees;
  const compact = W < 520;
  const rowH = 40, l = compact ? 92 : 120, r = 12, t = 8, b = 36, H = t + b + rowH * fees.length;
  const X = (v: number) => r1(l + ((v + 13) / 14) * (W - l - r));
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Net result of P0 at Tokyo-hosted latency in discovery, by fee schedule; each bar spans the three fill models; fills are identical across schedules" data-src="results/e002/e002_net_by_session.csv">
      <defs>
        <pattern id="hatch-h" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect className="hatch-bg" width="6" height="6" /><line className="hatch-ln" x1="0" y1="0" x2="0" y2="6" />
        </pattern>
      </defs>
      {[-12, -9, -6, -3, 0].map((g) => <g key={g}><line className={g === 0 ? 'zero' : 'grid'} x1={X(g)} x2={X(g)} y1={t} y2={H - b} /><text className="t-num" x={X(g)} y={H - b + 16} textAnchor="middle">{axisLab(g)}</text></g>)}
      <text x={W - r} y={H - 4} textAnchor="end">net, bp of traded notional</text>
      {fees.map((f, i) => {
        const y = t + rowH * i + rowH / 2, on = f.id === sel;
        return (
          <g key={f.id} data-src={f.src} className="fee-row" onClick={() => onSel(f.id)} style={{ cursor: 'pointer' }}>
            {on && <rect className="band" x={0} y={y - rowH / 2 + 2} width={W} height={rowH - 4} />}
            <text className={`${on ? 't-ink' : 't-ink2'} t-bold`} x={l - 10} y={y - 1} textAnchor="end">{f.label}</text>
            <text x={l - 10} y={y + 13} textAnchor="end" fontSize="11">{f.status}</text>
            <rect className={f.status === 'attainable' ? 'bar-att' : 'bar-hyp'} fill={f.status === 'attainable' ? undefined : 'url(#hatch-h)'} x={X(f.lo)} y={y - 8} width={Math.max(r1(X(f.hi) - X(f.lo)), 3)} height={16} />
            {on && <text className="t-ink t-num t-bold" x={X(f.hi) + 8} y={y + 4}>{fmt(f.lo, 1, true)} to {fmt(f.hi, 1, true)}</text>}
          </g>
        );
      })}
    </svg>
  );
}

/* ------------------------------------------------------------------ step 4: P0 against P3[M2] (E003 primary cell) */
const cell = (side: 'disc' | 'held', p: string) => {
  const a = LAB.grid[side][cellKey(p, 'intermediate', 'regional', 'vip0')]!;
  return Object.fromEntries(LAB.metrics.map((m, i) => [m, a[i]])) as Record<string, number>;
};

export function TradeLess({ W }: { W: number }) {
  const [side, setSide] = useState<'disc' | 'held'>('disc');
  const src = `${LAB.grid_src[side]} [P0|intermediate|regional|vip0; P3_M2|intermediate|regional|vip0]`;
  const a = cell(side, 'P0'), b = cell(side, 'P3_M2');
  const rows: Array<{ k: string; label: string; unit: string; d: number; max: number; signed: boolean }> = [
    { k: 'turnover_per_hour', label: 'Turnover: how much it trades', unit: 'USDT/h', d: 0, max: side === 'disc' ? 180000 : 60000, signed: false },
    { k: 'net_per_hour', label: 'Net result per hour', unit: 'USDT/h', d: 1, max: side === 'disc' ? 200 : 70, signed: true },
    { k: 'net_bp_per_notional', label: 'Net result per unit traded', unit: 'bp', d: 2, max: 12, signed: true },
  ];
  const l = W < 520 ? 70 : 96, rr = 12;
  return (
    <div className="tradeless">
      <div className="seg" role="radiogroup" aria-label="Sample">
        {(['disc', 'held'] as const).map((s) => (
          <button key={s} type="button" role="radio" aria-checked={side === s} className="chip" onClick={() => setSide(s)}>
            {s === 'disc' ? 'Discovery, 10 sessions' : 'Held-out, 5 sessions'}
          </button>
        ))}
      </div>
      {rows.map((row) => {
        // Losses extend left of a zero line; turnover, which is never negative, extends right from zero.
        const H = 76, span = W - l - rr - 72, zx = row.signed ? l + span : l;
        const len = (v: number) => r1((Math.abs(v) / row.max) * span);
        return (
          <figure key={row.k} className="tl-row" data-src={src} data-status="modeled historical replay">
            <figcaption><b>{row.label}</b> <span>{row.unit}</span></figcaption>
            <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${row.label}: P0 ${fmt(a[row.k], row.d, row.signed)}, P3[M2] ${fmt(b[row.k], row.d, row.signed)} ${row.unit}`}>
              <line className="zero" x1={zx} x2={zx} y1={2} y2={H - 6} />
              {([['Fixed', a], ['Gated', b]] as const).map(([name, x], i) => {
                const y = 8 + i * 32, n = Math.max(1, len(x[row.k]));
                const x0 = row.signed ? zx - n : zx;
                return (
                  <g key={name}>
                    <text className="t-ink t-bold t-id" x={l - 10} y={y + 15} textAnchor="end">{name}</text>
                    <rect className={`${side === 'disc' ? 'bar-disc' : 'bar-held'} mv`} x={0} y={y} width={1} height={22} style={{ transform: `translateX(${x0}px) scaleX(${n})` }} vectorEffect="non-scaling-stroke" />
                    <text className="t-ink t-num mv" x={0} y={y + 16} style={{ transform: `translateX(${row.signed ? zx + 8 : zx + n + 8}px)` }}>{fmt(x[row.k], row.d, row.signed)}</text>
                  </g>
                );
              })}
            </svg>
          </figure>
        );
      })}
      <p className="held">
        Fixed: fixed quoting (P0). Gated: forecast-gated quoting (P3[M2]). Net results are losses, drawn to the left of zero. Held-out values: <q className="lbl" data-label="policies">{LAB.held_label}</q>.
      </p>
    </div>
  );
}

/** On the holdout, how much of P3[M2]'s smaller loss is the maker fee it did not pay (frozen close-out values). */
export function HeldSplit({ W }: { W: number }) {
  const o = rec('e003.p3m2_p0.held'), fee = rec('e003.p3m2_p0.held_fee_saving'), gross = rec('e003.p3m2_p0.held_gross');
  const H = 92, l = 8, r = 8, X = (v: number) => r1(l + (v / o.v!) * (W - l - r));
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Held-out: P3[M2] lost ${fmt(o.v, 1)} USDT per hour less than P0; ${fmt(fee.v, 1)} of it is the maker fee not paid, ${fmt(gross.v, 1)} comes from gross trading results`} data-src={`${o.src}; ${fee.src}; ${gross.src}`}>
      <rect className="bar-fee" x={X(0)} y={10} width={r1(X(fee.v!) - X(0))} height={30} />
      <rect className="bar-held" x={X(fee.v!)} y={10} width={r1(X(o.v!) - X(fee.v!))} height={30} />
      <text className="t-ink t-bold" x={X(0) + 10} y={30}>{fmt(fee.v, 1)} maker fee not paid</text>
      <text className="t-ink t-num" x={X(o.v!)} y={62} textAnchor="end">+ {fmt(gross.v, 1)} from gross trading results</text>
      <text className="t-ink2" x={X(0)} y={84}>= {fmt(o.v, 1)} USDT/h smaller loss than fixed quoting</text>
    </svg>
  );
}

/* ------------------------------------------------------------------ net per hour against turnover (paper Figure 4 data) */
export function HeroScatter({ W }: { W: number }) {
  const compact = W < 560;
  const H = compact ? 360 : 440;
  const x0 = 52, x1 = W - (compact ? 14 : 150), y0 = 28, y1 = H - 50;
  const X = (v: number) => r1(x0 + (v / 200000) * (x1 - x0));
  const Y = (v: number) => r1(y0 + (-v / 240) * (y1 - y0));
  const ang = (bp: number) => (Math.atan2(Y(-200000 * bp * 1e-4) - Y(0), X(200000) - X(0)) * 180) / Math.PI;
  const grid = [0, 50000, 100000, 150000, 200000];
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`Net result per hour against turnover at VIP0, primary scenario. Every policy that trades lies between reference lines of a constant 10 and 12 bp loss of traded notional. P0 traded ${fmt(pol('P0').disc_turnover, 0)} USDT per hour and lost ${fmt(-pol('P0').disc_net, 1)} USDT per hour in discovery; P3[M2] traded ${fmt(pol('P3_M2').disc_turnover, 0)} and lost ${fmt(-pol('P3_M2').disc_net, 1)}. P3F and P4 abstain.`} data-src="results/e003/e003_analysis.json#/participation/policies; results/closeout/closeout_analysis.json#/experiments/E003/policies_vip0_descriptive/policies">
      {grid.map((g) => (
        <g key={g}>
          <line className="grid" x1={X(g)} x2={X(g)} y1={y0} y2={y1} />
          {(!compact || g % 100000 === 0) && <text className="t-num" x={X(g)} y={y1 + 18} textAnchor="middle">{axisLab(g)}</text>}
        </g>
      ))}
      {[-50, -100, -150, -200].map((g) => (
        <g key={g}>
          <line className="grid" x1={x0} x2={x1} y1={Y(g)} y2={Y(g)} />
          <text className="t-num" x={x0 - 8} y={Y(g) + 4} textAnchor="end">{axisLab(g)}</text>
        </g>
      ))}
      <line className="zero" x1={x0} x2={x1} y1={y0} y2={y0} />
      <text className="t-ink2" x={x0 - 8} y={y0 + 4} textAnchor="end">0</text>
      <text className="t-ink2" x={x1} y={y0 - 8} textAnchor="end">break-even</text>
      <line className="ref" x1={X(0)} y1={Y(0)} x2={X(200000)} y2={Y(-200)} />
      <line className="ref" x1={X(0)} y1={Y(0)} x2={X(200000)} y2={Y(-240)} />
      <text transform={`translate(${X(compact ? 64000 : 100000)} ${Y(compact ? -64 : -100)}) rotate(${ang(10).toFixed(2)})`} y={-7}>{MINUS}10 bp of notional</text>
      <text transform={`translate(${X(compact ? 64000 : 100000)} ${Y(compact ? -76.8 : -120)}) rotate(${ang(12).toFixed(2)})`} y={16}>{MINUS}12 bp of notional</text>
      {TRADED.map((p) => {
        const q = pol(p);
        return <line key={`l${p}`} className="leader" x1={X(q.disc_turnover)} y1={Y(q.disc_net)} x2={X(q.held_turnover)} y2={Y(q.held_net)} strokeDasharray="2 3" />;
      })}
      {TRADED.map((p) => {
        const q = pol(p);
        return (
          <g key={`p${p}`}>
            {diamond(X(q.held_turnover), Y(q.held_net), 5.7, 'ho')}
            <circle className="disc" cx={X(q.disc_turnover)} cy={Y(q.disc_net)} r={5.2} />
          </g>
        );
      })}
      <rect className="abst" x={X(0) - 5} y={Y(0) - 5} width={10} height={10} />
      <text x={x0 + 14} y={y0 - 8}>{compact ? 'P3F, P4, NT at zero' : 'P3F, P4 abstain; NT never quotes'}</text>
      {!compact && (['P1', 'P3_negM2', 'P0'] as const).map((p) => {
        const q = pol(p);
        const y = Y(q.disc_net);
        return (
          <g key={`t${p}`}>
            <path className="leader" d={`M${r1(X(q.disc_turnover) + 9)} ${y}L${x1 + 8} ${y}`} />
            <text className="t-ink" x={x1 + 14} y={r1(y + 4)}>{NAME[p]}{p === 'P3_negM2' ? ' placebo' : ''} <tspan className="t-num t-dim">{fmt(q.disc_net, 1, true)}</tspan></text>
          </g>
        );
      })}
      {compact && <text className="t-ink" x={X(pol('P0').disc_turnover)} y={Y(pol('P0').disc_net) + 22} textAnchor="middle">P0</text>}
      <path className="leader" d={`M${r1(X(pol('P3_M1').disc_turnover) + 7)} ${r1(Y(pol('P3_M1').disc_net) - 5)}L${r1(X(pol('P3_M1').disc_turnover) + 40)} ${r1(Y(pol('P3_M1').disc_net) - 34)}`} />
      <text className="t-ink" x={r1(X(pol('P3_M1').disc_turnover) + 44)} y={r1(Y(pol('P3_M1').disc_net) - 36)}>{compact ? 'P3[M1], P3[M2]' : 'P3[M1], P3[M2]: forecast-gated, trade less'}</text>
      <text x={(x0 + x1) / 2} y={H - 8} textAnchor="middle">Turnover, USDT per hour</text>
      <text x={x0 - 8} y={y0 - 14} textAnchor="end">USDT/h</text>
    </svg>
  );
}
