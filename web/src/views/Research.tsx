'use client';
// Research: E001–E004 as one connected investigation. Each experiment follows the same path: the question, why it
// matters, how it was tested, the evidence, what it means and its limitations; exact values sit in <Inspect>.
// Then the full held-out label table (paper Tables 6 and 7). Every number from the frozen bundle.
import type { CSSProperties, ReactNode } from 'react';
import { Inspect } from '../components/Explain';
import { Footer, ResearchNav } from '../components/Layout';
import { Held, N, Quote } from '../components/N';
import { Sized } from '../components/Sized';
import { Tag, Tags, Vip0 } from '../components/Tag';
import { HeroScatter, SkillBars } from '../charts/home';
import { CheckStrip, FeeRanges, MarkoutPanel } from '../charts/research';
import { QueueModels, QuoteFill, StaleWindow } from '../charts/teach';
import { core, rec } from '../data/core';
import { fmt, pct } from '../format';

const v = (id: string) => rec(id).v!;


const EV: Record<string, string> = { e001: 'Observed', e002: 'Modeled', e003: 'Observed and modeled', e004: 'Stress test' };

function Experiment({ id, code, question, answer, why, how, visual, means, limits, inspect, open }: {
  id: string; code: string; question: string; answer: string; why: ReactNode; how: ReactNode; visual: ReactNode; means: ReactNode; limits: ReactNode; inspect: ReactNode; open?: boolean;
}) {
  return (
    <details className="xp" id={id} open={open}>
      <summary>
        <span className="xp-code id">{code}</span>
        <span className="xp-q"><span className="xp-h" role="heading" aria-level={2}>{question}</span><span className="xp-a">{answer}</span></span>
        <span className="xp-ev">{EV[id]}</span>
        <span className="xp-x" aria-hidden="true" />
      </summary>
      <div className="xp-body">
        <div className="exp-grid">
          <div className="exp-txt">
            <div className="xb"><h3>Why it matters</h3>{why}</div>
            <div className="xb"><h3>How it was tested</h3>{how}</div>
          </div>
          <div className="exp-vis">{visual}</div>
        </div>
        <div className="exp-out">
          <div className="xb mean"><h3>What it means</h3>{means}</div>
          <div className="xb lim"><h3>Limitations</h3>{limits}</div>
        </div>
        <Inspect note="values, intervals and held-out labels">{inspect}</Inspect>
      </div>
    </details>
  );
}

function Table({ label, children }: { label: string; children: ReactNode }) {
  return <div className="tw" role="region" aria-label={label} tabIndex={0}>{children}</div>;
}

/** 2026-11-05T00:06:10+00:00 → 2026-11-05, 00:06 UTC */
const when = (utc: string) => utc.replace(/^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}).*$/, '$1, $2 UTC');

export default function Research() {
  const p3 = core.e003.policies_vip0;
  const authorised = core.holdout.ledger.find((e) => e.event === 'authorised')?.utc;
  return (
    <main id="main" className="wrap">
      <div className="page-head">
        <h1>Research</h1>
        <p className="lede">Four experiments, each specified before it was run, and a final check on five days kept sealed until the end.</p>
        <ResearchNav page="research" />
      </div>

      <div className="xps">
      <Experiment id="e001" code="E001" answer="Yes, on average. Observed in recorded trades, before any simulation."
        question="Is liquidity at the best prices adversely selected?"
        why={<p>If traders who trade against resting quotes tend to be right about the next move, a passive market maker starts every fill behind, before any fee or forecast enters. Everything later in the study builds on this measurement.</p>}
        how={<p>Only recorded trades and the replayed order book; no simulated orders. For each aggressive trade cluster we measured how far the mid moved in the aggressor’s direction after 1, 5 and 30 seconds (the markout), and what the passive side kept after that move (the realized spread). The session is the unit: means of session means with 95% session-bootstrap intervals, on <N id="e001.events.disc" /> clusters in 15 discovery sessions.</p>}
        visual={<>
          <QuoteFill />
          <figure className="panel">
            <figcaption><b>Markouts and realized spreads by horizon</b><span>Observed. Discovery 15 sessions; held-out 5 sessions, <N id="e001.events.held" /> clusters.</span></figcaption>
            <div className="duo2">
              <Sized fallback={360}>{(w) => <MarkoutPanel metric="mo" W={w} />}</Sized>
              <Sized fallback={360}>{(w) => <MarkoutPanel metric="rs" W={w} />}</Sized>
            </div>
            <ul className="legend">
              <li><svg viewBox="0 0 14 14" aria-hidden="true"><circle className="lg-disc" cx="7" cy="7" r="5" /></svg>Discovery mean, 95% interval at primary horizons</li>
              <li><svg viewBox="0 0 14 14" aria-hidden="true"><path className="lg-ho" d="M7 1.5L12.5 7L7 12.5L1.5 7Z" /></svg>Held-out mean (dashed)</li>
              <li><svg viewBox="0 0 14 14" aria-hidden="true"><circle className="lg-sess" cx="7" cy="7" r="2.5" /></svg>Held-out sessions</li>
            </ul>
          </figure>
        </>}
        means={<p>On average, the price kept moving in the aggressor’s direction after the trade: <N id="e001.mo_30s.disc" unit /> after 30 seconds in discovery. What the passive side kept was negative at every primary horizon: <N id="e001.rs_30s.disc" unit /> at 30 seconds, and <N id="e001.rs_30s.held" unit /> on the holdout. Resting at the touch is a losing position on average before any fee is paid.</p>}
        limits={<ul className="plain">
          <li>Averages over trade clusters, which are not verified orders: Binance publishes no parent-order identifiers.</li>
          <li>An average does not say that most individual fills lose.</li>
          <li>The held-out effect was about half as large, and the one-second held-out interval includes zero.</li>
        </ul>}
        inspect={<>
          <dl className="kv">
            <div><dt>Realized spread, 30 s</dt><dd><N id="e001.rs_30s.disc" unit /> [<N id="e001.rs_30s.disc_lo" />, <N id="e001.rs_30s.disc_hi" />] discovery; <N id="e001.rs_30s.held" unit /> held-out</dd></div>
            <div><dt>Realized spread, 1 s</dt><dd><N id="e001.rs_1s.disc" unit /> discovery; <N id="e001.rs_1s.held" unit /> held-out, t-interval [<N id="e001.rs_1s.held_tlo" />, <N id="e001.rs_1s.held_thi" />] (descriptive, not used)</dd></div>
            <div><dt>Markout, 30 s</dt><dd><N id="e001.mo_30s.disc" unit /> discovery; <N id="e001.mo_30s.held" unit /> held-out</dd></div>
            <div><dt>Effective spread</dt><dd><N id="e001.es.disc" unit /> discovery; <N id="e001.es.held" unit /> held-out, <Held>reported only</Held>: close to mechanical</dd></div>
          </dl>
          <p className="held">Held-out, all six checks: <Held check="E001">{core.e001.tally}</Held>, one family linked by rs = es − 2 mo. The realized spreads were <Quote>52 and 56% of discovery size</Quote> at 5 and 30 s.</p>
        </>}
      />

      <Experiment id="e002" code="E002" answer="No. Results moved by under a basis point; the fee is ten."
        question="Do execution assumptions change the answer?"
        why={<p>Historical data cannot say where our order would have stood in the queue, or how quickly it would have arrived. If the result hinged on those unknowns, no conclusion about profitability would be safe.</p>}
        how={<p>A replay engine simulated two fixed baselines, P0 and P1, each quoting one SOL at the best prices, under three queue models and three latency brackets (2, 30 and 115 ms). Fees were overlaid on the same fills under five schedules. The pre-registered H2 asked whether any scenario changes a sign or a ranking, or whether any paired fill-model difference reaches 1.0 bp, about one tick.</p>}
        visual={<>
          <QueueModels />
          <figure className="panel">
            <figcaption><b>Net result by fee schedule: fixed quoting, Tokyo-hosted latency</b><span>E002 discovery. Fills are identical across schedules; only the fee overlay changes. Each bar spans the three fill models; hatched schedules are hypothetical.</span></figcaption>
            <Sized>{(w) => <FeeRanges W={w} />}</Sized>
          </figure>
        </>}
        means={<p>Execution assumptions are second order: across all 18 combinations at VIP0 the mean result stayed between <N id="e002.range.disc" /> bp of traded notional, and H2 was not supported. The fee is first order: moving from VIP0 to a hypothetical rebate shifts the result by about ten basis points. <Quote>Lower latency produced more fills and slightly worse results per unit of notional: the fills it adds are more adverse.</Quote></p>}
        limits={<ul className="plain">
          <li>Queue position is inferred, never observed; the three fill models bracket it but are not proven bounds.</li>
          <li>Latency brackets are calibrations, not measurements of a real participant; our orders have no market impact.</li>
          <li>Only VIP0 is attainable; LP-programme taker rates are assumed.</li>
        </ul>}
        inspect={<>
          <Table label="Fee schedules">
            <table className="t">
              <caption>The fee schedules tested. LP-programme taker rates are assumed equal to VIP9’s.</caption>
              <thead><tr><th>Schedule</th><th>Maker, bp</th><th>Taker, bp</th><th>Status</th></tr></thead>
              <tbody>{core.e002.fees.map((f) => <tr key={f.id}><td>{f.label}</td><td className="num"><N id={`fee.${f.id}.maker`} /></td><td className="num"><N id={`fee.${f.id}.taker`} /></td><td>{f.status === 'attainable' ? <Vip0 text="attainable" /> : <Tag kind="hyp">hypothetical</Tag>}</td></tr>)}</tbody>
            </table>
          </Table>
          <p className="held">Held-out range across the 18 combinations: <N id="e002.range.held" /> bp (<Held>{core.e002.heldout_label}</Held>). Paired fill-model differences were <N id="e002.fill_diff" /> bp, all below the 1.0 bp threshold. The full matrix is in the <a href="/lab#view=e002">Scenario Lab</a>.</p>
        </>}
      />

      <Experiment id="e003" code="E003" answer="No. Skill was real, every trading rule still lost, and lower losses came from trading less."
        question="Does predicting prices make passive quoting pay?"
        why={<p>This is the central question. A forecast with real skill could let a quoter withdraw just before an adverse move and keep only the good fills. If that worked, prediction would be the edge a small market maker needs.</p>}
        how={<>
          <p>Two linear forecasts of the five-second price change, M1 (touch imbalance) and M2 (eight book and trade features), fitted walk-forward. Eight quoting policies, including a placebo that uses the same gate in the wrong direction and two fee-aware policies. Pre-registered decisions: H1-F (is there skill?), H1-T (are fills better per unit traded than the placebo’s?), H3 (do risk controls reduce risk?) and a participation decision (is any policy better than not trading?).</p>
          <dl className="contrast">
            <div><dt>Predicting prices asks</dt><dd>Does the forecast track the next move across all moments? Measured by R² on every book state.</dd></div>
            <div><dt>Earning from fills asks</dt><dd>What happens at the moments we are filled, after fees? Measured on our fills only.</dd></div>
          </dl>
        </>}
        visual={<>
          <figure className="panel">
            <figcaption><b>Prediction: out-of-sample R² of the eight-feature forecast</b><span>Observed.</span></figcaption>
            <Sized>{(w) => <SkillBars W={w} />}</Sized>
          </figure>
          <figure className="panel">
            <figcaption><b>Earning: net result per hour against turnover at VIP0</b><span>Primary scenario. Modeled (historical replay); held-out points <q className="lbl" data-label="policies">reported only, descriptive (no confirmation claim)</q>.</span></figcaption>
            <Sized>{(w) => <HeroScatter W={w} />}</Sized>
          </figure>
          <figure className="panel">
            <figcaption><b>H1-T: fill quality per unit traded against the placebo</b><span>D = gross bp of notional of P3[M2] minus the placebo P3[−M2], whose turnover is not matched. Modeled, fee-free. Margin δ = <N id="e003.h1t.delta" /> bp.</span></figcaption>
            <Sized>{(w) => <CheckStrip W={w} src={`${rec('e003.h1t.disc').src}; ${rec('e003.h1t.held').src}`} disc={v('e003.h1t.disc')} lo={v('e003.h1t.disc_lo')} hi={v('e003.h1t.disc_hi')} held={v('e003.h1t.held')} sessions={rec('e003.h1t.held_sessions').sessions!} threshold={{ v: v('e003.h1t.delta'), label: 'δ = 0.5 bp' }} domain={[-1, 1]} unit="bp" />}</Sized>
          </figure>
        </>}
        means={<>
          <p>Skill was real: R² at five seconds was <N id="e003.h1f.disc" /> in discovery and <N id="e003.h1f.held" /> held-out. It did not translate into better fills: against the placebo, the forecast-gated quoter showed no material improvement per unit traded (<N id="e003.h1t.held" unit /> held-out). Every policy that traded lost money in every session, at about 11 to 12 bp of each unit traded, so <Quote>A rule that trades less loses less when every unit of trading loses</Quote>.</p>
          <p className="mt-2">Under the hypothetical LP tier 4 schedule, where the fee-aware policies trade, P4’s risk controls lowered expected shortfall and drawdown relative to P3F and modestly improved its net result per hour, while both remained unprofitable (H3).</p>
        </>}
        limits={<ul className="plain">
          <li>Simple linear forecasts and fixed, a-priori rules, not optimised strategies.</li>
          <li>The placebo was not matched on turnover. H1-T held on the holdout by 0.01 bp with an interval spanning zero: the weakest label in the evaluation.</li>
          <li><Quote>Five held-out sessions cannot establish that the forecast has no economic value at all.</Quote></li>
          <li>H3 holds only under a fee schedule this project cannot attain.</li>
        </ul>}
        inspect={<>
          <Table label="Forecast skill by model and horizon">
            <table className="t">
              <caption>Out-of-sample R² against the zero forecast. Discovery: walk-forward, 10 sessions. Held-out: models fitted on all 15 discovery sessions. Observed.</caption>
              <thead><tr><th>Model</th><th>Horizon</th><th>Discovery</th><th>Held-out</th></tr></thead>
              <tbody>
                {['M1', 'M2'].flatMap((m) => [1, 5, 30].map((h) => {
                  const d = core.e003.skill.find((s) => s.side === 'disc' && s.model === m && s.h === h)!;
                  const o = core.e003.skill.find((s) => s.side === 'held' && s.model === m && s.h === h)!;
                  return <tr key={m + h}><td><span className="id">{m}</span></td><td>{h} s</td><td className="num" data-src={d.src}>{pct(d.r2, 2)}</td><td className="num" data-src={o.src}>{pct(o.r2, 2)}</td></tr>;
                }))}
              </tbody>
            </table>
          </Table>
          <p className="held">H1-F at 5 s: <N id="e003.h1f.disc" /> [<N id="e003.h1f.disc_lo" />, <N id="e003.h1f.disc_hi" />] discovery; <N id="e003.h1f.held" /> held-out, <Held check="H1-F">{rec('e003.h1f.held').lab!}</Held>, decided by the sign of a mean only.</p>
          <p className="held">H1-T: discovery <N id="e003.h1t.disc" /> [<N id="e003.h1t.disc_lo" />, <N id="e003.h1t.disc_hi" />]; held-out <N id="e003.h1t.held" />, t-interval [<N id="e003.h1t.held_tlo" />, <N id="e003.h1t.held_thi" />] (descriptive, not used). Held-out label: <Held check="H1-T">{rec('e003.h1t.held').lab!}</Held>, by a margin of 0.01 bp. It cannot establish that no improvement exists.</p>
          <Table label="Policies at VIP0">
            <table className="t">
              <caption>The eight policies at VIP0 (attainable), primary scenario. Turnover is traded notional per valid hour. Held-out columns are descriptive, with no test rule.</caption>
              <thead><tr><th>Policy</th><th>Discovery turnover <small>USDT/h</small></th><th>Discovery net <small>USDT/h</small></th><th>Held-out turnover</th><th>Held-out net</th></tr></thead>
              <tbody>
                {p3.map((r) => (
                  <tr key={r.policy}>
                    <td><span className="id">{r.code}</span></td>
                    <td className="num" data-src={r.src_disc}>{fmt(r.disc_turnover, 0)}</td>
                    <td className="num" data-src={r.src_disc}>{r.disc_turnover === 0 ? <span className="note">abstained</span> : fmt(r.disc_net, 1, true)}</td>
                    <td className="num" data-src={r.src_held}>{fmt(r.held_turnover, 0)}</td>
                    <td className="num" data-src={r.src_held}>{r.held_turnover === 0 ? <span className="note">abstained</span> : fmt(r.held_net, 1, true)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Table>
          <p className="held">P3[M2] lost <N id="e003.p3m2_p0.disc" nosign /> USDT/h less than P0 in discovery [<N id="e003.p3m2_p0.disc_lo" />, <N id="e003.p3m2_p0.disc_hi" />] and <N id="e003.p3m2_p0.held" nosign /> on the holdout, of which <N id="e003.p3m2_p0.held_fee_saving" /> is the maker fee it did not pay and <N id="e003.p3m2_p0.held_gross" /> comes from gross results. P3F and P4 abstained at VIP0: the zero is mechanical.</p>
          <Table label="H3 risk components">
            <table className="t">
              <caption>H3: P4 minus P3F under the hypothetical LP tier 4 schedule, where both trade. Lower expected shortfall and drawdown, and a modestly better net result per hour; both policies still lose. Modeled (historical replay).</caption>
              <thead><tr><th>Difference</th><th>Discovery <small>mean [95%]</small></th><th>Held-out</th></tr></thead>
              <tbody>
                <tr><td>Expected shortfall, 5-min increments, USDT</td><td className="num"><N id="e003.h3.es_diff.disc" /> <small>[<N id="e003.h3.es_diff.disc_lo" />, <N id="e003.h3.es_diff.disc_hi" />]</small></td><td className="num"><N id="e003.h3.es_diff.held" /></td></tr>
                <tr><td>Maximum drawdown, USDT</td><td className="num"><N id="e003.h3.drawdown_diff.disc" /> <small>[<N id="e003.h3.drawdown_diff.disc_lo" />, <N id="e003.h3.drawdown_diff.disc_hi" />]</small></td><td className="num"><N id="e003.h3.drawdown_diff.held" /></td></tr>
                <tr><td>Net per hour, USDT/h</td><td className="num"><N id="e003.h3.net_per_hour_diff.disc" /> <small>[<N id="e003.h3.net_per_hour_diff.disc_lo" />, <N id="e003.h3.net_per_hour_diff.disc_hi" />]</small></td><td className="num"><N id="e003.h3.net_per_hour_diff.held" /></td></tr>
              </tbody>
            </table>
          </Table>
          <p className="held">H3 held-out: <Held check="H3">{rec('e003.h3.es_diff.held').lab!}</Held>, under a fee schedule this project cannot attain; the net improvement shrank to about a fifth of its discovery size. <Quote>Risk controls reduced the variability and depth of losses; they did not create profit.</Quote></p>
          <Tags><Tag kind="hyp">Hypothetical: LP tier 4</Tag></Tags>
        </>}
      />

      <Experiment id="e004" code="E004" answer="No material deterioration under the specified threshold, a narrow result."
        question="Does stale information make fills worse?"
        why={<p>Real connections drop and data arrive late. A quoter acting on an old picture may leave orders at prices the market has already left, to be traded against by better-informed participants.</p>}
        how={<p>The participant’s view was degraded on purpose while the market was not: synthetic connection drops at a stress rate far above the observed reconnect rate, with fills on the exchange side identical across conditions. The pre-registered contrast D<sub>W</sub> compares the quality of fills arriving while the view was stale with fills in placebo windows of exactly the same durations at random times, against a 1 bp threshold.</p>}
        visual={<>
          <StaleWindow />
          {([['p0', 'P0', 'H4-W[P0]'], ['p3m2', 'P3[M2]', 'H4-W[P3_M2]']] as const).map(([k, code, check]) => (
            <figure className="panel" key={k}>
              <figcaption><b>H4-W, {code}: D<sub>W</sub>, random-window fill quality minus stale-window fill quality</b><span>D<sub>W</sub> = q(W<sub>P</sub>) − q(W<sub>U</sub>). {code}, fee-free 5-second mark-to-mid, bp of notional; positive would mean stale fills are worse.</span></figcaption>
              <Sized>{(w) => <CheckStrip W={w} src={`${rec(`e004.${k}.disc`).src}; ${rec(`e004.${k}.held`).src}`} disc={v(`e004.${k}.disc`)} lo={v(`e004.${k}.disc_lo`)} hi={v(`e004.${k}.disc_hi`)} held={v(`e004.${k}.held`)} sessions={rec(`e004.${k}.held_sessions`).sessions!} threshold={{ v: 1, label: 'δ = 1 bp' }} domain={[-1, 1.5]} unit="bp" />}</Sized>
              <p className="held">Held-out: <Held check={check}>{rec(`e004.${k}.held`).lab!}</Held>.</p>
            </figure>
          ))}
        </>}
        means={<p>Fills during staleness showed no material deterioration under the specified threshold: D<sub>W</sub> was <N id="e004.p0.disc" unit /> for P0 in discovery and <N id="e004.p0.held" unit /> held-out, if anything slightly better than fills at random times. P0 was filled less often in stale windows, because quotes left behind by a move are not filled while quotes the move runs into are. <Quote>these are findings of no material deterioration under the specified threshold: they are not equivalence, and they say nothing about effects smaller than one basis point.</Quote></p>}
        limits={<ul className="plain">
          <li>Not a finding that stale information is harmless: the test is silent below 1 bp.</li>
          <li>The drops are synthetic, at a stress rate and independent of market conditions; run at regional latency only.</li>
          <li>Withdrawing when stale gained nothing beyond the mechanical fee saving of trading less (descriptive).</li>
        </ul>}
        inspect={<>
          <Table label="Forecast-level results">
            <table className="t">
              <caption>Share of lost skill recovered by staleness-aware shrinkage, ρ<sub>A</sub>. Stress test; secondary, reported against pre-registered projections.</caption>
              <thead><tr><th>Target, cell</th><th>Discovery</th><th>Held-out</th><th>Label</th></tr></thead>
              <tbody>
                <tr><td>y<sub>view</sub>, D1-S</td><td className="num"><N id="e004.yview.D1_S.disc" /></td><td className="num"><N id="e004.yview.D1_S.held" /></td><td className="lbl-cell"><small><Held check="H4-F y_view">{rec('e004.yview.D1_S.held').lab!}</Held>: not supported holds; secondary, outside the tally</small></td></tr>
                <tr><td>y<sub>view</sub>, D3</td><td className="num"><N id="e004.yview.D3.disc" /></td><td className="num"><N id="e004.yview.D3.held" /></td><td className="lbl-cell"><small><Held check="H4-F y_view">{rec('e004.yview.D3.held').lab!}</Held>; largely implied by the target choice</small></td></tr>
                <tr><td>y<sub>k</sub>, D1-S</td><td className="num"><N id="e004.yk.disc" /></td><td className="num"><N id="e004.yk.D1_S.held" /></td><td className="lbl-cell"><small>reported only; projection <N id="e004.yk.D1_S.projection" /></small></td></tr>
                <tr><td>H4-0, clean data, pp</td><td className="num"><N id="e004.h40.disc" /></td><td className="num"><N id="e004.h40.held" /></td><td className="lbl-cell"><small>discovery {core.e004.h40_label}; held-out reported only</small></td></tr>
              </tbody>
            </table>
          </Table>
          <p className="held">H4-W[P3_M2]: discovery <N id="e004.p3m2.disc" /> [<N id="e004.p3m2.disc_lo" />, <N id="e004.p3m2.disc_hi" />]; held-out <N id="e004.p3m2.held" />. The withdrawal contrasts are in the <a href="/lab#view=e004">Scenario Lab</a>.</p>
        </>}
      />

      </div>

      <section className="sec" id="holdout" aria-labelledby="holdout-h">
        <div className="sec-h"><h2 id="holdout-h">The held-out evaluation</h2><p><Quote>A clean sweep of point-estimate checks is not the same as a set of statistically significant replications</Quote>. Each label below is quoted exactly as the evaluation recorded it.</p></div>
        <ul className="checks big" aria-label="Held-out tallies, per experiment" data-reveal="list">
          {(['E001', 'E002', 'E003', 'E004'] as const).map((e, i) => <li key={e} style={{ '--i': i } as CSSProperties}><span className="id">{e}</span><span>{{ E001: 'Observed markouts, six linked checks', E002: 'Execution sensitivity: tables reported only', E003: 'Signals and quoting, including H1-T, the weakest label', E004: 'Stale information, H4-W' }[e]}</span>{core.holdout.tallies[e] ? <b data-label="tally">{core.holdout.tallies[e]}</b> : <b className="none">no confirmation claim</b>}</li>)}
        </ul>
        <Inspect title="The full held-out label table" note="every check, its rule and its result">
        <Table label="Held-out label table">
          <table className="t labels">
            <caption>Confirmatory checks, the secondary y<sub>view</sub> row, and items reported only. Tallies are per experiment and are not counts of independent replications.</caption>
            <colgroup><col style={{ width: '17%' }} /><col style={{ width: '12%' }} /><col style={{ width: '31%' }} /><col style={{ width: '11%' }} /><col style={{ width: '29%' }} /></colgroup>
            <thead><tr><th>Check (status)</th><th>Discovery</th><th>Test rule, set in advance</th><th>Held-out</th><th>Label</th></tr></thead>
            <tbody>{(['E001', 'E002', 'E003', 'E004'] as const).map((exp) => <LabelGroup key={exp} exp={exp} />)}</tbody>
          </table>
        </Table>
        </Inspect>
        <Inspect title="How to read the labels, and the run history">
        <div className="res">
          <div>
            <h3 className="sub-h">How to read the labels</h3>
            <ul className="plain">
              <li><b>The checks are not independent.</b> E001’s six share one event set and an identity; H1-T depends on H1-F; the two H4-W checks share their windows.</li>
              <li><b>Several are weak by construction.</b> E003’s three are decided by the sign or side of a mean; a four-of-five count condition bounds the null probability at 18.75% under independent sessions.</li>
              <li><b>Some are narrow.</b> H1-T held by 0.01 bp; E001’s 1 s realized spread has a descriptive interval that includes zero.</li>
              <li><b>Magnitudes shrank.</b> The passive side’s realized spread was about half its discovery size; H3’s net improvement about a fifth.</li>
              <li><b>Not confirmed</b> would not have been a refutation: with five sessions, a failed check neither refutes the discovery result nor supports the opposite claim.</li>
            </ul>
          </div>
          <div>
            <h3 className="sub-h">Run history</h3>
            <dl className="kv">
              {authorised ? <div><dt>Evaluation authorised</dt><dd>{when(String(authorised))}</dd></div> : null}
              <div><dt>Completed</dt><dd>on attempt {core.holdout.attempt} of 3 permitted</dd></div>
              <div><dt>Outcome</dt><dd>no session undefined; no experiment failed</dd></div>
            </dl>
            <h3 className="sub-h mt-5">Relative tick per held-out session</h3>
            <dl className="kv">
              {Object.keys(core.holdout.relative_tick_bp).map((d) => <div key={d}><dt>{d}</dt><dd><N id={`holdout.tick.${d}`} unit /></dd></div>)}
            </dl>
            <p className="held mt-2">Discovery range <N id="sample.disc.tick" /> bp; δ thresholds were not rescaled.</p>
          </div>
        </div>
        </Inspect>
      </section>
      <Footer />
    </main>
  );
}

function Cell({ ids, text }: { ids?: string[]; text?: string }) {
  return <>{text && <span>{text}{ids && ids.length > 0 ? ': ' : ''}</span>}{ids?.map((id, i) => <span key={id}>{i > 0 && ' / '}<N id={id} /></span>)}</>;
}

function LabelGroup({ exp }: { exp: 'E001' | 'E002' | 'E003' | 'E004' }) {
  const rows = core.labels.filter((r) => r.exp === exp);
  const tally = core.holdout.tallies[exp];
  const names = { E001: 'E001, observed markouts', E002: 'E002, execution sensitivity', E003: 'E003, signals and quoting', E004: 'E004, information robustness' };
  return (
    <>
      <tr className="grp"><th colSpan={5} scope="colgroup">{names[exp]} · {tally ? <span data-label="tally">tally {tally}</span> : 'no confirmatory check'}</th></tr>
      {rows.map((r) => (
        <tr key={r.id} className={r.kind}>
          <td><b>{r.title}</b><small>{r.status}</small></td>
          <td className="num"><Cell {...r.discovery} /></td>
          <td className="rule" data-src={r.src}>{r.rule ?? (r.kind === 'reported' ? 'no test rule' : '')}</td>
          <td className="num"><Cell {...r.heldout} /></td>
          <td className="lbl-cell"><Held check={r.id}>{r.interpretation ? `${r.label}: ${r.interpretation}` : r.label}</Held>{r.comment && <small>{r.comment}</small>}</td>
        </tr>
      ))}
    </>
  );
}
