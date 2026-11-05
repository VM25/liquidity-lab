// Integrity lint over the built site. Exits non-zero on any violation.
import { createHash } from 'node:crypto';
import { readFile, readdir, stat } from 'node:fs/promises';
import { gzipSync } from 'node:zlib';
import { SECRET_PATTERNS, lintCss, lintHtml } from './lint-core.mjs';

const DIST = new URL('../dist/', import.meta.url);
const ROOT = new URL('../../', import.meta.url);
const BUDGET_GZ = 360 * 1024; // per page: scripts and stylesheets, gzip
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

const files = await walk(DIST);
for (const f of files) {
  if (/\.(csv|parquet|gz|zip|jsonl|feather|arrow)$/i.test(f) || f.startsWith('data/')) out.push(`${f}: data file in the build`);
  if (/\.(html|css|js|json|svg|txt)$/.test(f)) {
    const text = await readFile(new URL(f, DIST), 'utf8');
    for (const re of SECRET_PATTERNS) if (re.test(text)) out.push(`${f}: matches secret pattern ${re}`);
    if (f.endsWith('.css')) out.push(...lintCss(text, f));
    if (f.endsWith('.html')) {
      out.push(...lintHtml(text, f));
      let gz = 0;
      for (const m of text.matchAll(/(?:src|href)="\.\/(assets\/[^"]+\.(?:js|css))"/g)) gz += gzipSync(await readFile(new URL(m[1], DIST))).length;
      if (gz > BUDGET_GZ) out.push(`${f}: ${Math.round(gz / 1024)} KB of scripts and styles (gzip) exceeds ${BUDGET_GZ / 1024} KB`);
      console.log(`${f.padEnd(14)} scripts and styles ${Math.round(gz / 1024)} KB gzip`);
    }
  }
}
// The frozen PDFs must be byte-identical to docs/memo/FROZEN.sha256.
const pins = Object.fromEntries((await readFile(new URL('docs/memo/FROZEN.sha256', ROOT), 'utf8')).trim().split('\n').map((l) => l.split(/\s+/)).map(([h, p]) => [p.split('/').pop(), h]));
for (const f of files.filter((x) => x.endsWith('.pdf'))) {
  const sha = createHash('sha256').update(await readFile(new URL(f, DIST))).digest('hex');
  if (pins[f.split('/').pop()] !== sha) out.push(`${f}: not byte-identical to the frozen file`);
}
const total = (await Promise.all(files.map(async (f) => (await stat(new URL(f, DIST))).size))).reduce((a, b) => a + b, 0);
console.log(`lint-built: ${files.length} files, ${(total / 1048576).toFixed(1)} MB`);
if (out.length) {
  console.error(`lint-built: ${out.length} violation(s)\n` + out.map((o) => '  ' + o).join('\n'));
  process.exit(1);
}
console.log('lint-built: no violations');
