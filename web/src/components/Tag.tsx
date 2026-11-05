import type { ReactNode } from 'react';

// Evidence tags: the status lives in the same visual unit as the number.
const GLYPH = {
  obs: <svg viewBox="0 0 10 10" aria-hidden="true"><circle className="g-obs" cx="5" cy="5" r="4" /></svg>,
  mod: (
    <svg viewBox="0 0 10 10" aria-hidden="true">
      <circle className="g-mod" cx="5" cy="5" r="3.75" />
      <path className="g-mod-h" d="M5 1.25A3.75 3.75 0 0 0 5 8.75Z" />
    </svg>
  ),
  str: <svg viewBox="0 0 10 10" aria-hidden="true"><path className="g-str" d="M5 1.2L9 8.6H1Z" /></svg>,
  hyp: <svg viewBox="0 0 10 10" aria-hidden="true"><path className="g-hyp" d="M5 0.8L9.2 5L5 9.2L0.8 5Z M2.6 7.4L7.4 2.6" /></svg>,
  syn: <svg viewBox="0 0 10 10" aria-hidden="true"><rect className="g-syn" x="1" y="1" width="8" height="8" /></svg>,
};

export type TagKind = 'obs' | 'mod' | 'str' | 'hyp' | 'att' | 'id' | 'plain' | 'syn';

export function Tag({ kind, children }: { kind: TagKind; children: ReactNode }) {
  if (kind === 'att') return <span className="tag att">{children}</span>;
  if (kind === 'id') return <span className="tag"><span className="id">{children}</span></span>;
  if (kind === 'hyp') return <span className="tag hyp" data-fee="hypothetical">{GLYPH.hyp}{children}</span>;
  if (kind === 'syn') return <span className="tag syn" data-synthetic="true">{GLYPH.syn}{children}</span>;
  if (kind === 'plain') return <span className="tag">{children}</span>;
  return <span className="tag">{GLYPH[kind]}{children}</span>;
}

export function Tags({ children }: { children: ReactNode }) {
  return <span className="tags">{children}</span>;
}

export const Observed = () => <Tag kind="obs">Observed</Tag>;
export const Modeled = ({ long }: { long?: boolean }) => <Tag kind="mod">{long ? 'Modeled (historical replay)' : 'Modeled'}</Tag>;
export const Stress = () => <Tag kind="str">Stress test</Tag>;
export const Vip0 = ({ text = 'VIP0, attainable' }: { text?: string }) => <Tag kind="att">{text}</Tag>;
export const Synthetic = () => <Tag kind="syn">Synthetic example, not market data</Tag>;
