// @vitest-environment node
import { describe, expect, it } from 'vitest';
// @ts-expect-error plain ESM module without types
import { lintCss, lintHtml } from './lint-core.mjs';

const page = (body: string) => `<html><head><meta name="robots" content="noindex, nofollow"></head><body>${body}</body></html>`;

describe('built-site integrity lint', () => {
  it('passes a sourced number, a verbatim label and the required H4-W wording', () => {
    const ok = page('<p>held-out <span data-src="x#/a">−0.59</span> <q class="lbl" data-label="H4-W[P0]">confirmed (point estimate, 5 of 5 defined): no material deterioration under the specified threshold</q></p>');
    expect(lintHtml(ok)).toEqual([]);
  });
  it('flags a decimal without a source', () => {
    expect(lintHtml(page('<p>the loss was −11.52 bp</p>'))[0]).toMatch(/without a source/);
  });
  it('flags a "confirmed" label outside a label element, and a summed tally', () => {
    expect(lintHtml(page('<p>confirmed (point estimate)</p>')).join()).toMatch(/outside a verbatim label/);
    expect(lintHtml(page('<p>11 of 11 checks</p>')).join()).toMatch(/banned phrase/);
  });
  it('flags H4-W wording that drops the required phrase, and claims of no effect', () => {
    expect(lintHtml(page('<q data-label="H4-W[P0]">confirmed (point estimate, 5 of 5 defined)</q>')).join()).toMatch(/required wording/);
    expect(lintHtml(page('<p>stale data were no worse</p>')).join()).toMatch(/banned phrase/);
  });
  it('flags external resources and a missing noindex', () => {
    expect(lintHtml('<html><body><script src="https://cdn.example/x.js"></script></body></html>').join()).toMatch(/external reference.*noindex/s);
    expect(lintHtml(page('<link rel="stylesheet" href="https://fonts.example/a.css"><a href="https://example.com/">x</a>')).length).toBe(2);
  });
  it('allows only the canonical link and links to the public repository', () => {
    const ok = page('<link rel="canonical" href="https://liquidityparadox.netlify.app/lab"><a href="https://github.com/VM25/liquidity-lab">source</a>');
    expect(lintHtml(ok)).toEqual([]);
    expect(lintHtml(page('<link rel="canonical" href="https://elsewhere.example/lab">')).join()).toMatch(/external reference/);
    expect(lintHtml(page('<img src="https://github.com/VM25/liquidity-lab/x.png">')).join()).toMatch(/external reference/);
  });
  it('requires noindex outside production, and a canonical URL without noindex in production', () => {
    const prod = '<html><head><link rel="canonical" href="https://liquidityparadox.netlify.app/methods"></head><body><p>ok</p></body></html>';
    expect(lintHtml(prod, 'p', { indexable: true })).toEqual([]);
    expect(lintHtml(prod, 'p').join()).toMatch(/missing noindex/);
    expect(lintHtml(page('<p>ok</p>'), 'p', { indexable: true }).join()).toMatch(/noindex in the production build.*missing canonical/s);
  });
  it('flags banned fonts but allows the approved families', () => {
    expect(lintCss('a{font-family:"Inter",sans-serif}')).toHaveLength(1);
    expect(lintCss('a{font-family:"Sofia Sans","Helvetica Neue",Helvetica,sans-serif}')).toEqual([]);
    expect(lintCss('a{font-family:"Martian Mono Variable",Menlo,monospace}')).toEqual([]);
    expect(lintCss('a{font-family:KaTeX_Main,Times New Roman,serif}')).toHaveLength(1);
  });
});
