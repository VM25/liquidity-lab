// Integrity rules for the built site. Pure functions, tested in lint.test.ts; scripts/lint-built.mjs applies them to the
// Next.js build output.

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

// The production site's origin, and the only external pages a link may point to. Nothing is ever loaded from another origin.
export const SITE = 'https://liquidityparadox.netlify.app';
export const LINK_ALLOW = ['https://github.com/VM25/liquidity-lab'];

/** Violations in one page's HTML. `indexable` is true only for Netlify's production build: it must then carry its canonical
 *  URL and no noindex; every other build (deploy previews, branch deploys, local) must carry noindex. */
export function lintHtml(html, file = 'page', { indexable = false } = {}) {
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
  // No external resources. The only absolute URLs allowed are the page's canonical link to the production site and links
  // to the allowed pages (the public repository).
  for (const t of html.matchAll(/<([a-zA-Z][\w-]*)\b([^>]*)>/g)) {
    const [, tag, attrs] = t;
    for (const m of attrs.matchAll(/\b(src|href|srcset|poster|action)="((?:https?:)?\/\/[^"]*)"/g)) {
      const [, attr, url] = m;
      const canonical = tag === 'link' && /\brel="canonical"/.test(attrs) && (url === SITE || url.startsWith(`${SITE}/`));
      const link = tag === 'a' && attr === 'href' && LINK_ALLOW.some((a) => url === a || url.startsWith(`${a}/`));
      if (!canonical && !link) out.push(`${file}: external reference <${tag} ${attr}="${url}">`);
    }
  }
  const noindex = /<meta name="robots" content="noindex/.test(html);
  if (indexable) {
    if (noindex) out.push(`${file}: noindex in the production build`);
    if (!new RegExp(`<link rel="canonical" href="${SITE.replace(/\./g, '\\.')}[/"]`).test(html)) out.push(`${file}: missing canonical URL`);
  } else if (!noindex) out.push(`${file}: missing noindex outside the production build`);
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
