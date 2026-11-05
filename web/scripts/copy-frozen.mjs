// Copy the frozen paper and reproducibility supplement into the build, byte-identical, checked against
// docs/memo/FROZEN.sha256. Fails the build on any mismatch (the frozen files are never modified).
import { createHash } from 'node:crypto';
import { copyFile, mkdir, readFile } from 'node:fs/promises';

const ROOT = new URL('../../', import.meta.url);
const FILES = ['docs/memo/The_Liquidity_Paradox.pdf', 'docs/memo/Reproducibility_Supplement.pdf'];
const pins = Object.fromEntries(
  (await readFile(new URL('docs/memo/FROZEN.sha256', ROOT), 'utf8')).trim().split('\n').map((l) => l.split(/\s+/)).map(([h, p]) => [p, h]),
);
await mkdir(new URL('../dist/paper/', import.meta.url), { recursive: true });
for (const f of FILES) {
  const bytes = await readFile(new URL(f, ROOT));
  const sha = createHash('sha256').update(bytes).digest('hex');
  if (sha !== pins[f]) throw new Error(`${f}: SHA-256 ${sha} does not match FROZEN.sha256 (${pins[f]})`);
  const name = f.split('/').pop();
  await copyFile(new URL(f, ROOT), new URL(`../dist/paper/${name}`, import.meta.url));
  const back = createHash('sha256').update(await readFile(new URL(`../dist/paper/${name}`, import.meta.url))).digest('hex');
  if (back !== sha) throw new Error(`${name}: copy differs`);
  console.log(`copied ${name} (${sha.slice(0, 12)}…, matches FROZEN.sha256)`);
}
