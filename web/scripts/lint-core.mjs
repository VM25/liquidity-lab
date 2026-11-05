// Integrity rules for the built site (WEBSITE_PLAN section 7 and Task 9). Pure functions, tested in lint.test.ts.

export const BANNED_FONTS = ['anthropic', 'fraunces', 'archivo', 'ibm plex', 'inter', 'geist', 'grotesk', 'grotesque', 'big shoulder',
  'saira', 'public sans', 'spline', 'arial', 'calibre', 'times new roman', 'jetbrains', 'dm mono', 'dm sans', 'dm serif', 'newsreader',
  'red hot', 'red hat', 'sora', 'libre franklin', 'source serif', 'source sans', 'terminal', 'cascadia', 'b612', 'spectral'];

// Banned claims and patterns in visible text. A tally is never summed across experiments.
export const BANNED_PHRASES = [/\bno worse\b/i, /\b1[12] of 1[12]\b/, /trader mode/i, /\bsharpe\b/i, /\bguaranteed\b/i, /\bno effect\b/i, /\bequivalent\b/i];

// Decimal parameters stated in prose (horizons, thresholds, evidential weights); every other decimal needs a source.
export const ALLOWED_DECIMALS = new Set(['0.1', '0.01', '0.5', '1.0', '18.75', '0.97']);

const VOID = new Set(['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr', 'path', 'circle', 'line', 'rect', 'stop', 'use']);
const PROVENANCE = /\bdata-(src|quote|label|meta)=|aria-hidden="true"|class="[^"]*\bcode\b/;

/** Walk text nodes with their ancestor tags. */
export function* textNodes(html) {
  const stack = [];
  const re = /<!--[\s\S]*?-->|<\/?([a-zA-Z][\w:-]*)([^>]*)>|([^<]+)/g;
  let m;
  while ((m = re.exec(html))) {
    if (m[0].startsWith('<!--')) continue;
    if (m[3] !== undefined) { yield { text: m[3], stack }; continue; }
    const tag = m[1].toLowerCase();
    if (m[0].startsWith('</')) {
      const i = stack.map((s) => s.tag).lastIndexOf(tag);
      if (i >= 0) stack.length = i;
    } else if (!VOID.has(tag) && !m[2].trim().endsWith('/')) {
      stack.push({ tag, attrs: m[2] });
    }
  }
}

const decode = (t) => t.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"');

/** Violations in one page's HTML. */
export function lintHtml(html, file = 'page') {
  const out = [];
  const body = html.slice(html.indexOf('<body'));
  for (const { text, stack } of textNodes(body)) {
    const t = decode(text);
    const tags = stack.map((s) => s.tag);
    if (tags.includes('script') || tags.includes('style')) continue;
    const provenance = stack.some((s) => PROVENANCE.test(s.attrs));
    for (const d of t.match(/(?<![§\d.])\d+\.\d+/g) ?? []) { // section references (§10.10) are not results
      if (!provenance && !ALLOWED_DECIMALS.has(d)) out.push(`${file}: decimal "${d}" without a source in "${t.trim().slice(0, 80)}"`);
    }
    const inLabel = stack.some((s) => /\bdata-label=/.test(s.attrs));
    if (/confirmed \(|\d of \d confirmed/.test(t) && !inLabel) out.push(`${file}: a "confirmed" label outside a verbatim label element: "${t.trim().slice(0, 80)}"`);
    for (const re of BANNED_PHRASES) if (re.test(t)) out.push(`${file}: banned phrase ${re} in "${t.trim().slice(0, 80)}"`);
  }
  // H4-W labels must carry the required wording.
  for (const m of body.matchAll(/<q[^>]*data-label="H4-W[^"]*"[^>]*>([\s\S]*?)<\/q>/g)) {
    if (!m[1].includes('no material deterioration under the specified threshold')) out.push(`${file}: an H4-W label without the required wording`);
  }
  // No external resources; local builds are not for indexing.
  for (const m of html.matchAll(/\b(?:src|href)="(https?:)?\/\/[^"]*"/g)) out.push(`${file}: external reference ${m[0]}`);
  if (!/<meta name="robots" content="noindex/.test(html)) out.push(`${file}: missing noindex`);
  return out;
}

/** Violations in a stylesheet: banned font families and external url() loads. */
export function lintCss(css, file = 'style.css') {
  const out = [];
  for (const m of css.matchAll(/font(?:-family)?\s*:\s*([^;}]+)/gi)) {
    const fam = m[1].toLowerCase();
    for (const b of BANNED_FONTS) if (new RegExp(`(^|[^a-z])${b}([^a-z]|$)`).test(fam)) out.push(`${file}: banned font "${b}" in font-family ${m[1].trim()}`);
  }
  for (const m of css.matchAll(/url\((['"]?)(https?:)?\/\//gi)) out.push(`${file}: external url() ${m[0]}`);
  return out;
}

export const SECRET_PATTERNS = [/AKIA[0-9A-Z]{16}/, /-----BEGIN [A-Z ]*PRIVATE KEY-----/, /\b(api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*["'][^"']{8,}/i];
