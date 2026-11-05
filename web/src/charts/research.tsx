// Research figures (Mineral Analytical), drawn from the frozen bundle (the paper's Figures 2, 3 and 5 data).
import { core, rec } from '../data/core';
import { axisLab, fmt, nice } from '../format';

const r1 = (v: number) => Math.round(v * 10) / 10;
const DAYS = ['2026-06-01', '2026-07-01', '2026-08-01', '2026-09-01', '2026-10-01'];

function diamond(x: number, y: number, k: number, cls: string) {
  return <path className={cls} d={`M${x} ${y - k}L${x + k} ${y}L${x} ${y + k}L${x - k} ${y}Z`} />;
}

/** E001 markout (mo) or realized spread (rs) by horizon: discovery means with 95% intervals; held-out means and sessions. */
export function MarkoutPanel({ metric, W = 520 }: { metric: 'mo' | 'rs'; W?: number }) {
  const H = 300, l = 52, r = 16, t = 22, b = 44;
  const hs = ['0.1', '1', '5', '30', '60'];
  const X = (h: string) => r1(l + ((Math.log10(Number(h)) + 1) / (Math.log10(60) + 1)) * (W - l - r));
  const [lo, hi] = metric === 'mo' ? [0, 1.5] : [-1.5, 0.5];
  const Y = (v: number) => r1(t + ((hi - v) / (hi - lo)) * (H - t - b));
  const v = (h: string, side: 'disc' | 'held') => rec(`e001.${metric}_${h}s.${side}`).v!;
  const ticks = metric === 'mo' ? [0, 0.5, 1, 1.5] : [-1.5, -1, -0.5, 0, 0.5];
  const title = metric === 'mo' ? 'Midpoint markout mo(h), aggressor direction' : 'Realized spread rs(h); the passive side earns rs/2';
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${title}: discovery and held-out by horizon, bp of the pre-event mid`} data-src="results/e001/e001_discovery.json#/primary; results/closeout/closeout_analysis.json#/experiments/E001">
      {ticks.map((g) => <g key={g}><line className={g === 0 ? 'zero' : 'grid'} x1={l} x2={W - r} y1={Y(g)} y2={Y(g)} /><text className="t-num" x={l - 8} y={Y(g) + 4} textAnchor="end">{g > 0 ? '+' + g : axisLab(g)}</text></g>)}
      <rect className="band" x={X('1') - 8} y={t} width={X('30') - X('1') + 16} height={H - t - b} opacity={0.5} />
      <text x={(X('1') + X('30')) / 2} y={t - 6} textAnchor="middle">primary horizons</text>
      {hs.map((h) => <text key={h} className="t-ink2" x={X(h)} y={H - b + 18} textAnchor="middle">{h} s</text>)}
      <path className="disc-l" d={'M' + hs.map((h) => `${X(h)} ${Y(v(h, 'disc'))}`).join('L')} />
      <path className="ho-l" d={'M' + hs.map((h) => `${X(h)} ${Y(v(h, 'held'))}`).join('L')} />
      {hs.map((h) => {
        const primary = h === '1' || h === '5' || h === '30';
        const sess = primary ? core.e001.held_sessions[`${metric}_${h}s`] : null;
        return (
          <g key={h}>
            {primary && <line className="disc-w" x1={X(h) - 9} x2={X(h) - 9} y1={Y(rec(`e001.${metric}_${h}s.disc_lo`).v!)} y2={Y(rec(`e001.${metric}_${h}s.disc_hi`).v!)} />}
            {sess && DAYS.map((d, i) => <circle key={d} className="sess" cx={X(h) + 8 + (i - 2) * 2.2} cy={Y(sess[d])} r={2} />)}
            <circle className="disc" cx={primary ? X(h) - 9 : X(h)} cy={Y(v(h, 'disc'))} r={4} />
            {diamond(primary ? X(h) + 8 : X(h), Y(v(h, 'held')), 5, 'ho-in-panel')}
          </g>
        );
      })}
      <text x={W - r} y={H - 8} textAnchor="end">horizon h, log scale</text>
      <text x={l - 8} y={12} textAnchor="end">bp</text>
    </svg>
  );
}

/** E002: net result by fee schedule for P0 at Tokyo-hosted latency; each bar spans the three fill models (paper Figure 3). */
export function FeeRanges({ W = 620 }: { W?: number }) {
  const compact = W < 520;
  const rowH = 44, l = compact ? 96 : 150, r = compact ? 12 : 120, t = 10, b = 40;
  const fees = core.e002.fees;
  const H = t + b + rowH * fees.length;
  const X = (v: number) => r1(l + ((v + 13) / 13.6) * (W - l - r));
  return (
    <svg className="fig" viewBox={`0 0 ${W} ${H}`} role="img" aria-label="Net result by fee schedule, P0, Tokyo-hosted latency, discovery; each bar spans the conservative, intermediate and optimistic fill models" data-src="results/e002/e002_net_by_session.csv">
      <defs>
        <pattern id="hatch-r" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect className="hatch-bg" width="6" height="6" /><line className="hatch-ln" x1="0" y1="0" x2="0" y2="6" />
        </pattern>
      </defs>
      {[-12, -9, -6, -3, 0].map((g) => <g key={g}><line className={g === 0 ? 'zero' : 'grid'} x1={X(g)} x2={X(g)} y1={t} y2={H - b} /><text className="t-num" x={X(g)} y={H - b + 18} textAnchor="middle">{axisLab(g)}</text></g>)}
      <text x={W - r} y={H - 6} textAnchor="end">{compact ? 'net, bp of traded notional' : 'net P&L, bp of traded notional (liquidation-adjusted); zero is break-even'}</text>
      {fees.map((f, i) => {
        const y = t + rowH * i + rowH / 2;
        return (
          <g key={f.id} data-src={f.src}>
            <text className={f.status === 'attainable' ? 't-blue t-bold' : 't-ink t-bold'} x={l - 12} y={y - 2} textAnchor="end">{f.label}</text>
            <text x={l - 12} y={y + 13} textAnchor="end">{f.status}</text>
            <rect className={f.status === 'attainable' ? 'bar-att' : 'bar-hyp'} fill={f.status === 'attainable' ? undefined : 'url(#hatch-r)'} x={X(f.lo)} y={y - 9} width={Math.max(r1(X(f.hi) - X(f.lo)), 3)} height={18} />
            {!compact && <text className="t-ink t-num" x={X(f.hi) + 10} y={y + 4}>{fmt(f.lo, 1, true)} to {fmt(f.hi, 1, true)}</text>}
          </g>
        );
      })}
    </svg>
  );
}

/**
 * One pre-registered check, discovery against held-out (the paper's Figure 5 form): discovery mean and 95% interval,
 * the five held-out sessions and their mean, the threshold. No held-out interval is drawn (protocol: no interval decision).
 */
export function CheckStrip({ disc, lo, hi, held, sessions, threshold, domain, unit, src, scale = 1, W = 560 }: {
  src: string; disc: number; lo: number; hi: number; held: number; sessions: Record<string, number>;
  threshold?: { v: number; label: string }; domain: [number, number]; unit: string; scale?: number; W?: number;
}) {
  const H = 120, l = 20, r = 20;
  const X = (v: number) => r1(l + ((v * scale - domain[0]) / (domain[1] - domain[0])) * (W - l - r));
  const step = nice((domain[1] - domain[0]) / 5);
  const ticks: number[] = [];
  for (let g = Math.ceil(domain[0] / step) * step; g <= domain[1] + 1e-9; g += step) ticks.push(+g.toPrecision(6));
  return (
    <svg className="fig strip" viewBox={`0 0 ${W} ${H}`} role="img" data-src={src} aria-label={`Discovery ${fmt(disc * scale, 2, true)} ${unit} with interval ${fmt(lo * scale, 2, true)} to ${fmt(hi * scale, 2, true)}; held-out mean ${fmt(held * scale, 2, true)}`}>
      <line className="axis" x1={l} x2={W - r} y1={92} y2={92} />
      {ticks.map((g) => <g key={g}><line className="tick" x1={X(g / scale)} x2={X(g / scale)} y1={92} y2={97} /><text className="t-num" x={X(g / scale)} y={112} textAnchor="middle">{g > 0 ? '+' + g : axisLab(g)}</text></g>)}
      {domain[0] < 0 && domain[1] > 0 && <line className="zero" x1={X(0)} x2={X(0)} y1={14} y2={92} />}
      {threshold && (
        <>
          <line className="ref" x1={X(threshold.v / scale)} x2={X(threshold.v / scale)} y1={10} y2={92} />
          <text x={X(threshold.v / scale) + 5} y={18}>{threshold.label}</text>
        </>
      )}
      <text className="t-ink2" x={l} y={30}>discovery</text>
      <line className="disc-w" x1={X(lo)} x2={X(hi)} y1={40} y2={40} />
      <line className="disc-w" x1={X(lo)} x2={X(lo)} y1={35} y2={45} />
      <line className="disc-w" x1={X(hi)} x2={X(hi)} y1={35} y2={45} />
      <circle className="disc" cx={X(disc)} cy={40} r={5} />
      <text className="t-ink2" x={l} y={64}>held-out</text>
      {Object.values(sessions).map((s, i) => <circle key={i} className="sess" cx={X(s)} cy={74} r={2.6} />)}
      {diamond(X(held), 74, 6, 'ho-in-panel')}
    </svg>
  );
}

