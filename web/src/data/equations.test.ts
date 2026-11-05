// @vitest-environment node
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import eqs from './equations.json';

const squash = (s: string) => s.replace(/\s+/g, ' ').trim();
const paper = squash(readFileSync(resolve(process.cwd(), '../docs/memo/The_Liquidity_Paradox.tex'), 'utf8'));

describe('equations', () => {
  it('copies every equation verbatim from the frozen paper', () => {
    for (const [id, e] of Object.entries(eqs)) expect(paper.includes(squash(e.tex)), id).toBe(true);
  });
  it('renders MathML for assistive technology', () => {
    for (const e of Object.values(eqs)) expect(e.html).toContain('<math');
  });
});
