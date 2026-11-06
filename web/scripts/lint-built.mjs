// Integrity lint over the Next.js build: the five prerendered pages, robots.txt and the sitemap in .next/server/app/,
// the browser assets in .next/static/ and the public files in public/. Runs after `next build`; exits non-zero on any
// violation, which fails the build (locally and on Netlify).
import { createHash } from 'node:crypto';
import { readFile, readdir, stat } from 'node:fs/promises';
import { gzipSync } from 'node:zlib';
import { SECRET_PATTERNS, SITE, lintCss, lintHtml } from './lint-core.mjs';

const WEB = new URL('../', import.meta.url);
const ROOT = new URL('../../', import.meta.url);
const APP = new URL('.next/server/app/', WEB);
const PAGES = { '/': 'index.html', '/lab': 'lab.html', '/research': 'research.html', '/methods': 'methods.html', '/paper': 'paper.html' };
const BUDGET_GZ = 360 * 1024; // per page: scripts and stylesheets, gzip
// The same rule as src/site.ts: only Netlify's production build may be indexed.
const indexable = process.env.CONTEXT === 'production';
const out = [];

async function walk(dir, rel = '') {
  const files = [];
  for (const e of await readdir(new URL(rel, dir), { withFileTypes: true })) {
    const r = rel + e.name + (e.isDirectory() ? '/' : '');
    if (e.isDirectory()) files.push(...(await walk(dir, r)));
    else files.push(r);
  }
  return files;
}

// Everything the deploy serves: browser assets, public files and the prerendered output.
const served = [
  ...(await walk(new URL('.next/static/', WEB))).map((f) => ['.next/static/' + f, new URL('.next/static/' + f, WEB)]),
  ...(await walk(new URL('public/', WEB))).map((f) => ['public/' + f, new URL('public/' + f, WEB)]),
  ...(await walk(APP)).filter((f) => !f.endsWith('.map')).map((f) => ['.next/server/app/' + f, new URL(f, APP)]),
];
for (const [name, url] of served) {
  if (/\.(csv|parquet|gz|zip|jsonl|feather|arrow)$/i.test(name)) out.push(`${name}: data file in the build`);
  if (/\.(html|css|js|json|svg|txt|rsc|body|xml)$/.test(name)) {
    const text = await readFile(url, 'utf8');
    for (const re of SECRET_PATTERNS) if (re.test(text)) out.push(`${name}: matches secret pattern ${re}`);
    if (name.endsWith('.css')) out.push(...lintCss(text, name));
  }
}

// The five pages: provenance, wording, external references, indexing, and a script-and-style budget.
for (const [route, file] of Object.entries(PAGES)) {
  let html;
  try { html = await readFile(new URL(file, APP), 'utf8'); } catch { out.push(`${route}: not prerendered (${file} missing)`); continue; }
  out.push(...lintHtml(html, route, { indexable }));
  const assets = new Set([...html.matchAll(/(?:src|href)="\/_next\/static\/([^"?]+\.(?:js|css))"/g)].map((m) => m[1]));
  let gz = 0;
  for (const a of assets) gz += gzipSync(await readFile(new URL(`.next/static/${a}`, WEB))).length;
  if (gz > BUDGET_GZ) out.push(`${route}: ${Math.round(gz / 1024)} KB of scripts and styles (gzip) exceeds ${BUDGET_GZ / 1024} KB`);
  console.log(`${route.padEnd(10)} scripts and styles ${Math.round(gz / 1024)} KB gzip`);
}

// robots.txt and the sitemap follow the same indexing rule.
const robots = await readFile(new URL('robots.txt.body', APP), 'utf8').catch(() => '');
if (indexable ? !/Allow: \//.test(robots) || !robots.includes(`Sitemap: ${SITE}/sitemap.xml`) : !/Disallow: \/\s*$/m.test(robots)) {
  out.push(`robots.txt does not match the ${indexable ? 'production' : 'non-production'} rule:\n${robots}`);
}
const sitemap = await readFile(new URL('sitemap.xml.body', APP), 'utf8').catch(() => '');
for (const route of Object.keys(PAGES)) if (!sitemap.includes(`<loc>${SITE}${route === '/' ? '' : route}</loc>`)) out.push(`sitemap.xml: ${route} missing`);

// The frozen PDFs must be present and byte-identical to docs/memo/FROZEN.sha256.
const pins = Object.fromEntries((await readFile(new URL('docs/memo/FROZEN.sha256', ROOT), 'utf8')).trim().split('\n').map((l) => l.split(/\s+/)).map(([h, p]) => [p.split('/').pop(), h]));
for (const pdf of ['The_Liquidity_Paradox.pdf', 'Reproducibility_Supplement.pdf']) {
  const bytes = await readFile(new URL(`public/paper/${pdf}`, WEB)).catch(() => null);
  if (!bytes) out.push(`public/paper/${pdf}: missing`);
  else if (createHash('sha256').update(bytes).digest('hex') !== pins[pdf]) out.push(`public/paper/${pdf}: not byte-identical to the frozen file`);
}

const total = (await Promise.all(served.map(async ([, url]) => (await stat(url)).size))).reduce((a, b) => a + b, 0);
console.log(`lint-built: ${served.length} files, ${(total / 1048576).toFixed(1)} MB (${indexable ? 'production: indexable' : 'not production: noindex'})`);
if (out.length) {
  console.error(`lint-built: ${out.length} violation(s)\n` + out.map((o) => '  ' + o).join('\n'));
  process.exit(1);
}
console.log('lint-built: no violations');
