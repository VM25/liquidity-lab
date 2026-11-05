// Prerender each page to static HTML (readable without JavaScript); the client then hydrates it.
import { readFile, writeFile, rm } from 'node:fs/promises';

const { render } = await import('../.ssr/entry-server.js');
const FILES = { overview: 'index.html', research: 'research.html', lab: 'lab.html', methods: 'methods.html', paper: 'paper.html' };
for (const [page, file] of Object.entries(FILES)) {
  const url = new URL(`../dist/${file}`, import.meta.url);
  const html = await readFile(url, 'utf8');
  if (!html.includes('<!--app-->')) throw new Error(`${file}: no <!--app--> placeholder`);
  await writeFile(url, html.replace('<!--app-->', render(page)));
  console.log(`prerendered ${file}`);
}
await rm(new URL('../.ssr', import.meta.url), { recursive: true, force: true });
