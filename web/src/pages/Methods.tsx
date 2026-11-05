// Methods & Data: how the study was done, explained step by step for a reader without a trading background, with the
// exact assumptions, equations and limitations one click away. Quotations are verbatim from the frozen paper.
import type { CSSProperties, JSX } from 'react';
import { Inspect } from '../components/Explain';
import { Footer, ResearchNav } from '../components/Layout';
import { N, Quote } from '../components/N';
import { Modeled, Observed, Stress, Synthetic, Tag, Vip0 } from '../components/Tag';
import { BookLadder, CountRule, WalkForward } from '../charts/teach';
import { core } from '../data/core';
import eqs from '../data/equations.json';

const ACC = 'results/data_acceptance_report.md';

function Eq({ id }: { id: keyof typeof eqs }) {
  // wide equations scroll sideways on a phone, so the block is a focusable region like the tables
  return <div className="eq" data-quote="paper-tex" role="region" aria-label="Equation" tabIndex={0} dangerouslySetInnerHTML={{ __html: eqs[id].html }} />;
}

const KIND: Record<string, JSX.Element | null> = { data: null, obs: <Observed />, mod: <Modeled />, str: <Stress />, ho: <Tag kind="plain">Held-out, once</Tag> };
const PIPE: Array<[string, string, string]> = [
  ['Collect', 'Free public samples of Binance’s order-book updates and trades for 20 first-of-month days.', 'data'],
  ['Rebuild', 'Replay every book update in order to reconstruct the top ten price levels at each moment.', 'data'],
  ['Validate', 'Keep only intervals where the rebuilt book is provably correct; drop the rest.', 'data'],
  ['Measure', 'What happened after real aggressive trades, with no simulated orders.', 'obs'],
  ['Simulate', 'Replay our own hypothetical one-SOL orders against the recorded market.', 'mod'],
  ['Stress', 'Degrade the participant’s information on purpose and replay again.', 'str'],
  ['Check once', 'Evaluate five sealed sessions a single time, under rules fixed in advance.', 'ho'],
];

export default function Methods() {
  const { train, validation, test } = core.sample.splits;
  const days = [...train, ...validation, ...test];
  const wf = new Set(core.sample.walkforward);
  const kind = (d: string) => (train.includes(d) ? 'train' : validation.includes(d) ? 'validation' : 'test');
  const done = core.holdout.ledger.find((e) => e.event === 'completed') ?? core.holdout.ledger[core.holdout.ledger.length - 1];
  return (
    <main id="main" className="wrap">
      <div className="page-head">
        <h1>Methods &amp; data</h1>
        <p className="lede">How the evidence was produced, and how the study guarded against fooling itself.</p>
        <ResearchNav page="methods" />
      </div>

      <section className="sec" id="pipeline" aria-labelledby="pipeline-h">
        <div className="sec-h"><h2 id="pipeline-h">The study in seven steps</h2><p>From raw exchange messages to a single check on sealed data. Steps four to seven each produce one kind of evidence, and every result on this site says which.</p></div>
        <ol className="pipe" data-reveal="list">
          {PIPE.map(([t, d, k], i) => (
            <li key={t} style={{ '--i': i } as CSSProperties}><span className="pp-n id">{i + 1}</span><b>{t}</b><span>{d}</span>{KIND[k] && <span className="pp-k">{KIND[k]}</span>}</li>
          ))}
        </ol>
      </section>

      <div className="accs">
      <section className="acc-group" aria-label="Data">
        <h2 className="acc-gh">Data</h2>
      <details className="acc" id="why">
        <summary><span className="acc-h" role="heading" aria-level={2}>Why Binance spot SOLUSDT</span><span className="acc-l">A study of passive market making needs a market where the queue at the best price matters, and data good enough to rebuild that queue.</span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <div className="three">
          <div className="xb"><h3>Data that can be verified</h3><p>All 20 SOLUSDT sample days passed the integrity checks, and <span data-src={`${ACC} §1`}>97.73%</span> of the 480 sampled hours were provably valid. The bitcoin and ether samples were provably valid for only <span data-src={`${ACC} §1`}>40% and 64%</span> of their hours.</p></div>
          <div className="xb"><h3>A tick that matters</h3><p>SOL’s 0.01 USDT price step was <N id="sample.disc.tick" /> bp of the price in discovery, and the quoted spread was one tick almost all the time. Orders compete for position in a queue at a single price: the setting passive market making is about. On bitcoin the step is a tiny fraction of a basis point.</p></div>
          <div className="xb"><h3>Chosen before any result, but not blind</h3><p><Quote>The instrument, sample and splits were chosen with knowledge of all twenty days' data-quality metadata, though not their outcomes.</Quote></p></div>
        </div>
        </div>
      </details>

      <details className="acc" id="book">
        <summary><span className="acc-h" role="heading" aria-level={2}>What a limit order book is</span><span className="acc-l">Every resting buy and sell order, grouped by price. The highest bid and the lowest ask are “the touch”; the gap between them is the spread.</span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <div className="res">
          <BookLadder />
          <div className="prose">
            <p><b>Two ways to trade.</b> A passive trader, like a market maker, posts an order at a price and waits in the queue at that price. An aggressive trader crosses the spread and trades immediately against resting orders, paying the spread for speed.</p>
            <p><b>Why the queue matters.</b> Orders at one price fill first-come, first-served. A new order joins the back. Whether a market maker’s order fills depends on how much stands ahead of it and how much of that is cancelled.</p>
            <p><b>What market data show, and what they do not.</b> The data show the total size at each price and every change to it. They do not show who owns each order, so the position of any one order in the queue can only be inferred.</p>
          </div>
        </div>
        </div>
      </details>

      <details className="acc" id="rebuild">
        <summary><span className="acc-h" role="heading" aria-level={2}>Rebuilding the book, and why some data were rejected</span><span className="acc-l">An exchange publishes the order book as a stream of changes. Miss one, and the rebuilt book is silently wrong from then on.</span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <div className="res">
          <div className="prose">
            <p>The replay starts from a full snapshot of the book and applies every subsequent change in sequence. <Quote>A data-acceptance test, run before any experiment, rebuilds the book from snapshot anchors and marks a time interval valid only while the book is provably correct</Quote>: sequence numbers unbroken, the best prices inside the region proven by the last snapshot, the book never crossed, and no reconnection by the data vendor.</p>
            <p><Quote>Invalid intervals are excluded rather than repaired.</Quote> Guessing what a missing update contained would put invented prices into every later result. An episode, the unit every simulation runs on, is an accepted window of at least ten minutes; each starts flat and ends with all orders cancelled and any position closed against the visible book.</p>
          </div>
          <div className="tw" role="region" aria-label="Sample" tabIndex={0}>
            <table className="t">
              <caption>Sample (paper Table 1). Valid hours are the total duration of accepted episodes.</caption>
              <thead><tr><th /><th>Discovery</th><th>Walk-forward evaluation</th><th>Held-out test</th></tr></thead>
              <tbody>
                <tr><td>Sessions</td><td className="num"><N id="sample.disc.sessions" /></td><td className="num"><N id="sample.wf.sessions" /></td><td className="num"><N id="sample.held.sessions" /></td></tr>
                <tr><td>Period</td><td>2025-03 to 2026-05</td><td>2025-08 to 2026-05</td><td>2026-06 to 2026-10</td></tr>
                <tr><td>Episodes</td><td className="num"><N id="sample.disc.episodes" /></td><td className="num"><N id="sample.wf.episodes" /></td><td className="num"><N id="sample.held.episodes" /></td></tr>
                <tr><td>Valid hours</td><td className="num"><N id="sample.disc.hours" /></td><td className="num"><N id="sample.wf.hours" /></td><td className="num"><N id="sample.held.hours" /></td></tr>
                <tr><td>Aggressive events (E001)</td><td className="num"><N id="e001.events.disc" /></td><td className="num">—</td><td className="num"><N id="e001.events.held" /></td></tr>
                <tr><td>Relative tick, bp</td><td className="num"><N id="sample.disc.tick" /></td><td className="num">—</td><td className="num"><N id="sample.held.tick" /></td></tr>
              </tbody>
            </table>
          </div>
        </div>
        </div>
      </details>

      <details className="acc" id="sessions">
        <summary><span className="acc-h" role="heading" aria-level={2}>Twenty sessions, three splits, one sealed holdout</span><span className="acc-l">Each session is one first-of-month UTC day. Splitting them in time order means every result is judged on days that come after the days used to build it.</span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <figure className="panel">
          <figcaption><b>The twenty sessions</b><span>The splits were fixed before any experiment was run. The test sessions stayed sealed until the final protocol was fixed, then were evaluated once.</span></figcaption>
          <div className="design-row" role="img" aria-label={`Sessions ${days[0]} to ${days[days.length - 1]}: ${train.length} train, ${validation.length} validation, ${test.length} held-out test; ${wf.size} walk-forward evaluation sessions`} data-src={core.sample.splits_src}>
            {days.map((d) => <span key={d} className={`${kind(d)}${wf.has(d) ? ' wf' : ''}`} title={`${d}: ${kind(d)}${wf.has(d) ? ', walk-forward evaluation' : ''}`} />)}
          </div>
          <div className="design-axis"><span>{days[0].slice(0, 7)}</span><span>{train[train.length - 1].slice(0, 7)}</span><span>{validation[validation.length - 1].slice(0, 7)}</span><span>{test[test.length - 1].slice(0, 7)}</span></div>
          <div className="design-key"><span><i className="train" />train ({train.length})</span><span><i className="validation" />validation ({validation.length})</span><span><i className="test" />held-out test ({test.length})</span><span><i className="wf" />walk-forward evaluation ({wf.size})</span></div>
        </figure>
        <div className="three mt-5">
          <div className="xb"><h3>Discovery</h3><p>The first fifteen sessions. Every experiment was run here once and decided by its pre-registered rule. E001 and E002 use all fifteen.</p></div>
          <div className="xb"><h3>Walk-forward</h3><p>E003 and E004 fit their forecasts only on sessions before the one being evaluated, then step forward a session at a time: ten evaluations, none of which sees its own future.</p></div>
          <div className="xb"><h3>The final holdout</h3><p>Five later sessions, unopened until every rule was fixed. Models fitted on all fifteen discovery sessions were carried forward unchanged and evaluated once.</p></div>
        </div>
        <div className="mt-5"><WalkForward /></div>
        </div>
      </details>

      </section>
      <section className="acc-group" aria-label="Simulation">
        <h2 className="acc-gh">Simulation</h2>
      <details className="acc" id="simulate">
        <summary><span className="acc-h" role="heading" aria-level={2}>Simulating orders that never existed</span><span className="acc-l"><Quote>Modeled results are historical replays in which our orders never existed: fills are inferred under stated queue, latency and fee assumptions, and our orders have no market impact.</Quote></span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <div className="res">
          <div className="prose">
            <p><b>Joining the queue.</b> A simulated order joins the back of its price level. Trades at that price use up the queue ahead of it first. Because cancellations cannot be attributed, three fill models bracket the unknown: cancellations from behind us (conservative), pro rata (intermediate, the primary model), or from ahead first with fills when the price trades through (optimistic). The <a href="./research.html#e002">Research page</a> has an interactive example.</p>
            <p><b>Speed.</b> The participant decides on the book it has received, after a data delay; its order reaches the exchange after an entry latency; it learns of fills after an acknowledgement latency. Depth updates arrive in 100 ms batches, so even the fastest bracket decides on batched information.</p>
            <p><b>Fees.</b> Charged on every fill as an accounting overlay. Policies that ignore fees trade identically under every schedule; P3F and P4, whose rules use the fee, were simulated per schedule.</p>
            <p><b>Bookkeeping.</b> Marked wealth obeys an accounting identity throughout: the sum of fill edges against the mid, plus inventory revaluation, minus fees.</p>
          </div>
          <div>
            <div className="tw" role="region" aria-label="Latency brackets" tabIndex={0}>
              <table className="t">
                <caption>Latency brackets: one-way order entry and acknowledgement, and the extra market-data delay.</caption>
                <thead><tr><th>Bracket</th><th>Entry, ms</th><th>Data delay, ms</th></tr></thead>
                <tbody>{(['tokyo', 'regional', 'distant'] as const).map((l) => <tr key={l}><td>{l === 'tokyo' ? 'Tokyo-hosted' : l === 'regional' ? 'Regional (primary)' : 'Distant'}</td><td className="num"><N id={`lat.${l}.entry_ms`} /></td><td className="num"><N id={`lat.${l}.md_ms`} /></td></tr>)}</tbody>
              </table>
            </div>
            <div className="tw mt-5" role="region" aria-label="Fee schedules" tabIndex={0}>
              <table className="t">
                <caption>Fee schedules. Accounting overlays on fixed fills; only VIP0 is attainable.</caption>
                <thead><tr><th>Schedule</th><th>Maker, bp</th><th>Taker, bp</th><th>Status</th></tr></thead>
                <tbody>{core.e002.fees.map((f) => <tr key={f.id}><td>{f.label}<small>{f.cfg_label}</small></td><td className="num"><N id={`fee.${f.id}.maker`} /></td><td className="num"><N id={`fee.${f.id}.taker`} /></td><td>{f.status === 'attainable' ? <Vip0 text="attainable" /> : <Tag kind="hyp">hypothetical</Tag>}</td></tr>)}</tbody>
              </table>
            </div>
          </div>
        </div>
        <Inspect title="The eight quoting policies" note="exact rules (paper Table 3)">
          <div className="tw" role="region" aria-label="Quoting policies" tabIndex={0}>
            <table className="t txt">
              <caption>All quote <N id="pol.size" /> SOL at the touch or not at all, within ±<N id="pol.limit" /> SOL, drawing new orders from a token bucket of <N id="pacing.rate" /> orders per second per side. s: spread in ticks; f: forecast in ticks; c: maker fee in ticks; q: inventory.</caption>
              <thead><tr><th>Policy</th><th>Quote the bid when</th><th>Role</th></tr></thead>
              <tbody>
                <tr><td className="id">NT</td><td>never</td><td>no-trade baseline</td></tr>
                <tr><td className="id">P0</td><td>always</td><td>fixed quoting (E002)</td></tr>
                <tr><td className="id">P1</td><td>q &lt; <N id="pol.p1" /> (the ask mirrors)</td><td>inventory withdrawal (E002)</td></tr>
                <tr><td className="id">P3[M]</td><td>s/2 + f &gt; 0</td><td>forecast-gated, fee-unaware; M1 or M2</td></tr>
                <tr><td className="id">P3[−M2]</td><td>s/2 − f &gt; 0</td><td>placebo: same gate, wrong direction</td></tr>
                <tr><td className="id">P3F</td><td>s/2 + f − c &gt; 0</td><td>forecast- and fee-aware</td></tr>
                <tr><td className="id">P4</td><td>P3F’s condition with f − κq, q &lt; 3, volatility gate open</td><td>P3F plus skew (κ = <N id="pol.kappa" /> tick/SOL), withdrawal and a volatility gate</td></tr>
              </tbody>
            </table>
          </div>
        </Inspect>
        </div>
      </details>

      <details className="acc" id="evidence">
        <summary><span className="acc-h" role="heading" aria-level={2}>Five kinds of evidence</span><span className="acc-l">Every result on this site is one of these, and is labelled where it appears.</span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <dl className="kv">
          <div><dt><Observed /></dt><dd><Quote>Observed results are computed from recorded exchange trades and replayed book states, with no hypothetical orders.</Quote></dd></div>
          <div><dt><Modeled /></dt><dd><Quote>Modeled results are historical replays in which our orders never existed: fills are inferred under stated queue, latency and fee assumptions, and our orders have no market impact.</Quote></dd></div>
          <div><dt><Stress /></dt><dd><Quote>Stress-test results are computed on observed records that were deliberately degraded.</Quote></dd></div>
          <div><dt><Tag kind="hyp">Hypothetical</Tag></dt><dd><Quote>Hypothetical marks a fee schedule that a participant like us cannot attain; only the 10 bp VIP0 schedule is attainable.</Quote></dd></div>
          <div><dt><Synthetic /></dt><dd>A teaching diagram built from made-up values to explain an idea. Never a market observation, and always framed with a dashed border.</dd></div>
        </dl>
        </div>
      </details>

      </section>
      <section className="acc-group" aria-label="Inference">
        <h2 className="acc-gh">Inference</h2>
      <details className="acc" id="stages">
        <summary><span className="acc-h" role="heading" aria-level={2}>Why the rules were fixed in stages</span><span className="acc-l">Rules chosen after seeing results can be bent, often unknowingly, to fit them. Each stage below removed one way of doing that. <Quote>A pre-registered rule that turned out to be weak was not changed afterwards.</Quote></span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <ol className="stages">
          <li><b>Data accepted</b><span>The acceptance test ran before any experiment.</span></li>
          <li><b>Market, sample and splits fixed</b><span>From data-quality metadata only, before any experiment outcome existed.</span></li>
          <li><b>Each experiment specified, then run once</b><span>E001 to E004 in turn: specification reviewed and fixed, then run on discovery and decided by its own rules. Each later experiment lists the earlier results it could not be blind to.</span></li>
          <li><b>Held-out protocol fixed</b><span>Written after the four discovery experiments and fixed before the test sessions were opened; models carried forward without refitting.</span></li>
          <li><b>One evaluation</b><span>The five sealed sessions were evaluated once and completed on the first of three permitted attempts{done?.utc ? <> (<span className="mono-note">{String(done.utc)}</span>)</> : null}.</span></li>
          <li><b>Paper finalised</b><span>Written after the evaluation and not changed since; any further analysis of the held-out sessions is post hoc.</span></li>
        </ol>
        </div>
      </details>

      <details className="acc" id="five">
        <summary><span className="acc-h" role="heading" aria-level={2}>Why five held-out sessions limit certainty</span><span className="acc-l">Five days is enough to see whether a discovery result reversed, not enough to prove it is real. The protocol says in advance how weak each check is.</span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <div className="res">
          <CountRule />
          <div className="prose">
            <p><b>Sign checks are coin flips at worst.</b> A rule decided only by the sign of a five-session mean could be met with probability up to one half even if nothing were there.</p>
            <p><b>Count rules are stronger, but not by much.</b> Requiring at least four of five sessions on the discovery side is met by chance 6 times in 32, or 18.75%, under independent sessions.</p>
            <p><b>So a label is a check, not a test.</b> <q className="lbl" data-label="definition">confirmed (point estimate)</q> means a discovery decision did not reverse on five later days; on five sessions <q className="lbl" data-label="definition">not confirmed</q> would not have been a refutation. Descriptive t-intervals printed beside held-out values are never used for a label.</p>
          </div>
        </div>
        </div>
      </details>

      <details className="acc" id="equations">
        <summary><span className="acc-h" role="heading" aria-level={2}>Equations</span><span className="acc-l">The paper’s definitions, each with its symbols explained.</span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <Inspect title="Effective spread, markout and realized spread (E001)" open>
          <Eq id="spreads" />
          <p className="held">s = +1 for buyer-initiated and −1 for seller-initiated clusters; P the cluster’s volume-weighted price; m<sub>0</sub> the mid before the trade; m<sub>T+h</sub> the mid h seconds after. In basis points of m<sub>0</sub>. The passive side’s mark-to-mid result per unit of liquidity hit is rs(h)/2.</p>
        </Inspect>
        <Inspect title="Out-of-sample skill (E003)">
          <Eq id="r2" />
          <p className="held">Against the zero forecast, computed per evaluation session and averaged.</p>
        </Inspect>
        <Inspect title="Stale-window fill quality (E004)">
          <Eq id="dw" />
          <p className="held">q(W) is the fee-free five-second mark-to-mid of fills inside window set W, in bp of their notional; W<sub>U</sub> the stale windows, W<sub>P</sub> placebo windows of identical duration at random times. Positive when fills during staleness are worse.</p>
        </Inspect>
        <Inspect title="Recovered share of lost skill (E004, secondary)">
          <Eq id="rhoa" />
          <p className="held">L is the skill lost to degradation, A the part recovered by staleness-aware shrinkage.</p>
        </Inspect>
        <Inspect title="Inference on discovery sessions">
          <p className="prose">On discovery sessions the session is the unit: means of session values with 10,000-draw session-bootstrap percentile intervals. <Quote>On the five held-out sessions the protocol makes no interval decision.</Quote> Confirmations are tallied per experiment; a tally is not a count of independent replications.</p>
        </Inspect>
        </div>
      </details>

      </section>
      <section className="acc-group" aria-label="Limits and sources">
        <h2 className="acc-gh">Limits and sources</h2>
      <details className="acc" id="limits">
        <summary><span className="acc-h" role="heading" aria-level={2}>Limitations</span><span className="acc-l">In rough order of importance, as stated in the paper.</span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <dl className="kv">
          <div><dt>A five-session holdout</dt><dd><Quote>Five sessions give little statistical power.</Quote> <Quote>All twenty sessions are first-of-month days, which may not represent other days.</Quote></dd></div>
          <div><dt>Not blind</dt><dd><Quote>The instrument, sample and splits were chosen with knowledge of all twenty days' data-quality metadata, though not their outcomes.</Quote></dd></div>
          <div><dt>Modeled execution</dt><dd><Quote>Every policy result is a replay.</Quote> <Quote>Our orders have no market impact, queue position is inferred rather than observed, hidden and intra-batch flows are invisible, and the latency brackets are calibrations, not measurements of a real participant.</Quote></dd></div>
          <div><dt>Synthetic stresses, hypothetical fees</dt><dd><Quote>E004's degradations are synthetic, at stress levels far above observed rates and independent of market conditions.</Quote> <Quote>H3 is tested only under a rebate tier this project cannot reach, and every LP-programme taker rate is assumed.</Quote></dd></div>
          <div><dt>Fixed, simple policies</dt><dd><Quote>The policies are a-priori rules, not optimised strategies, and the forecasts are linear.</Quote></dd></div>
          <div><dt>One market and venue</dt><dd><Quote>All results concern Binance spot SOLUSDT on a free data sample.</Quote></dd></div>
          <div><dt>After the evaluation</dt><dd><Quote>Any further analysis of the held-out sessions is post hoc and exploratory.</Quote></dd></div>
        </dl>
        </div>
      </details>

      <details className="acc" id="data">
        <summary><span className="acc-h" role="heading" aria-level={2}>Data sources</span><span className="acc-l">Free public samples, used for research. The raw market data are not redistributed here.</span><span className="acc-x" aria-hidden="true" /></summary>
        <div className="acc-b">
        <dl className="kv">
          <div><dt>Book states</dt><dd>Tardis.dev free first-of-month samples of Binance’s incremental depth stream. Their published terms allow internal research and educational use and restrict redistribution. This site shows aggregated research statistics only: no book playback, tick paths or reconstructable data.</dd></div>
          <div><dt>Trades</dt><dd>Binance’s public trade archive (Binance Vision), published under its own licence terms.</dd></div>
          <div><dt>Verification only</dt><dd>An independent community capture was used privately to verify the reconstruction.</dd></div>
        </dl>
        </div>
      </details>
      </section>
      </div>
      <Footer />
    </main>
  );
}
