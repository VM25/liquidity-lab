'use client';
// Progressive disclosure: Layer 1 (understand) is always visible, Layer 2 (explore) is interactive, Layer 3 (inspect)
// sits one click away in <Inspect>. Help explains a control at the point of use without crowding the interface.
import { useId, useState, type ReactNode } from 'react';
import { Synthetic } from './Tag';

/** Layer 3: the exact values, labels, intervals and sources behind a visible statement. Closed by default. */
export function Inspect({ title = 'Inspect the evidence', note, children, open }: { title?: string; note?: string; children: ReactNode; open?: boolean }) {
  return (
    <details className="inspect" open={open}>
      <summary>{title}{note && <small>{note}</small>}</summary>
      <div className="inspect-b">{children}</div>
    </details>
  );
}

/** A small "?" toggle that reveals a short explanation directly below its label. */
export function Help({ label, children }: { label: string; children: ReactNode }) {
  const [open, setOpen] = useState(false);
  const id = useId();
  return (
    <>
      <button type="button" className="help-b" aria-expanded={open} aria-controls={id} aria-label={`What is ${label}?`} onClick={() => setOpen((o) => !o)}>?</button>
      <div id={id} className="help-t" hidden={!open}>{children}</div>
    </>
  );
}

/** The same toggle split in two, for a fieldset: the button goes inside the <legend>, the text after it. */
export function useHelp(label: string, content: ReactNode) {
  const [open, setOpen] = useState(false);
  const id = useId();
  return {
    button: <button type="button" className="help-b" aria-expanded={open} aria-controls={id} aria-label={`What is ${label}?`} onClick={() => setOpen((o) => !o)}>?</button>,
    panel: <div id={id} className="help-t" hidden={!open}>{content}</div>,
  };
}

/** The plain-English conclusion of a step. */
export function Takeaway({ children }: { children: ReactNode }) {
  return (
    <div className="takeaway">
      <span>Takeaway</span>
      <p>{children}</p>
    </div>
  );
}

/** A frame for an illustrative diagram built from made-up values. Always tagged; never mixed with market data. */
export function Synth({ title, children, note }: { title: string; children: ReactNode; note?: ReactNode }) {
  return (
    <figure className="synth" data-synthetic="true" data-meta="synthetic example">
      <div className="synth-h"><b>{title}</b><Synthetic /></div>
      {children}
      {note && <figcaption className="held mt-3">{note}</figcaption>}
    </figure>
  );
}
