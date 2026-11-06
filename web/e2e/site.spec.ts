import AxeBuilder from '@axe-core/playwright';
import { expect, test, type Page } from '@playwright/test';

const PAGES = ['/', '/research', '/lab', '/methods', '/paper'];

for (const p of PAGES) {
  test(`${p}: no console errors and no serious accessibility violations`, async ({ page }) => {
    const errors: string[] = [];
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.goto(p);
    await page.waitForLoadState('networkidle');
    const axe = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    const bad = axe.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
    expect(bad.map((v) => `${v.id}: ${v.nodes.slice(0, 3).map((n) => n.target.join(' ')).join(' | ')}`)).toEqual([]);
    expect(errors).toEqual([]);
  });

  test(`${p}: no horizontal scroll at phone width`, async ({ browser }) => {
    const ctx = await browser.newContext({ viewport: { width: 375, height: 812 }, isMobile: true, hasTouch: true });
    const page = await ctx.newPage();
    await page.goto(p);
    await page.waitForLoadState('networkidle');
    const [sw, iw] = await page.evaluate(() => [document.documentElement.scrollWidth, innerWidth]);
    expect(sw).toBeLessThanOrEqual(375);
    expect(iw).toBe(375);
    await ctx.close();
  });

  test(`${p}: readable without JavaScript`, async ({ browser }) => {
    const ctx = await browser.newContext({ javaScriptEnabled: false });
    const page = await ctx.newPage();
    await page.goto(p);
    await expect(page.locator('h1').first()).toBeVisible();
    expect((await page.locator('main').innerText()).length).toBeGreaterThan(300);
    await ctx.close();
  });

  test(`${p}: synthetic diagrams are tagged, and the corrected wordings hold`, async ({ page }) => {
    await page.goto(p);
    const frames = page.locator('[data-synthetic="true"].synth');
    const n = await frames.count();
    for (let i = 0; i < n; i += 1) await expect(frames.nth(i).locator('.tag.syn')).toHaveText('Synthetic example, not market data');
    const body = page.locator('body');
    await expect(body).not.toContainText(/mostly when the price is about to move/i);
    await expect(body).not.toContainText(/reduce risk,? not losses/i);
    await expect(body).not.toContainText(/stale-window fills minus random-window/i);
    await expect(body).not.toContainText(/79% of P0’s fills/);
    await expect(body).not.toContainText(/price moves explained/);
    await expect(body).not.toContainText(/1[12] of 1[12]/);
  });

  test(`${p}: three destinations in the header`, async ({ page }) => {
    await page.goto(p);
    await expect(page.locator('.nav > li:not(.pdf) > a')).toHaveText(['Home', 'Explore', 'Research']);
    await expect(page.locator('.nav a[aria-current="page"]')).toHaveCount(1);
  });
}

test('home: the paradox, its qualification, four questions and a way in', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toHaveText('We could predict the market. We couldn’t profitably make it.');
  await expect(page.locator('.qual')).toContainText('not every possible strategy');
  await expect(page.locator('.hero .cta a.primary')).toHaveAttribute('href', '/lab');
  await expect(page.locator('.strip li')).toHaveCount(4);
  await expect(page.locator('.hero-fig svg')).toBeVisible();
  await expect(page.locator('.hero-fig')).toContainText('reported only, descriptive (no confirmation claim)');
  // two separate measurements, each on its own scale; break-even belongs to the trading result only
  const fig = page.locator('.hero-fig svg');
  await expect(fig.locator('.region')).toHaveCount(2);
  await expect(fig.locator('.region').nth(0)).toContainText('R² vs a zero-change forecast');
  await expect(fig.locator('.region').nth(0)).not.toContainText('break-even');
  await expect(fig.locator('.region').nth(1)).toContainText('break-even');
});

const lab = async (page: Page, hash = '') => {
  await page.goto(`/lab${hash}`);
  await page.waitForLoadState('networkidle');
};
const assumptions = async (page: Page) => {
  const b = page.getByRole('button', { name: 'Change assumptions' });
  if (await b.isVisible()) await b.click();
};

test('explore: the guided story is the default and walks six steps', async ({ page }) => {
  await lab(page);
  await expect(page).toHaveURL(/#step=1$/);
  const stage = page.locator('.story');
  await expect(stage.locator('h2')).toHaveText('The forecast works');
  await expect(stage.locator('.story-num')).toContainText('lower squared prediction error than a zero-change forecast, out of sample');
  const titles = ['Fills come at the wrong moment', 'The fee decides', 'Trading less loses less', 'What it means for real market makers', 'How sure we are'];
  for (const [i, t] of titles.entries()) {
    await stage.locator('.story-bar').getByRole('button', { name: /^Next/ }).click();
    await expect(stage.locator('h2')).toHaveText(t);
    await expect(page).toHaveURL(new RegExp(`#step=${i + 2}$`));
    if (t === 'Trading less loses less') {
      await expect(stage.locator('.story-num')).toContainText('79%');
      await expect(stage.locator('.story-num')).toContainText('not a count of fills');
    }
  }
  await expect(stage).toContainText('6 of 6 confirmed');
  await expect(stage).toContainText('3 of 3 confirmed');
  await expect(stage).toContainText('2 of 2 confirmed');
  await expect(stage).toContainText('no material deterioration under the specified threshold');
});

test('explore: the fee step shows that only the fee changes and flags hypothetical schedules', async ({ page }) => {
  await lab(page, '#step=3');
  const v = page.locator('.story');
  const vip0 = await v.locator('.story-num b').innerText();
  await v.getByRole('radio', { name: /LP tier 4/ }).click();
  await expect(v.locator('.story-num b')).not.toHaveText(vip0);
  await expect(v.locator('.story-v')).toContainText('LP tier 4 is hypothetical');
  await expect(v.locator('.annot')).toContainText('Between rows');
});

test('explore: a story step opens in the full lab with its scenario', async ({ page }) => {
  await lab(page, '#step=4');
  await page.getByRole('button', { name: 'Open this step in the full lab' }).click();
  await expect(page.getByRole('button', { name: 'Full lab' })).toHaveAttribute('aria-pressed', 'true');
  await expect(page).toHaveURL(/metric=turnover_per_hour/);
  await expect(page.locator('#sb-focus')).toHaveValue('P3_M2');
});

test('full lab: "What changed, and why?" explains each change from frozen values', async ({ page }) => {
  await lab(page, '#view=e003');
  const ro = page.locator('.readout');
  await expect(ro).toContainText('P3[M2] against P0');
  await assumptions(page);
  await page.locator('#sb-fee').selectOption('lp_tier4');
  await expect(ro).toContainText('Fee schedule: VIP0 → LP tier 4');
  await expect(ro).toContainText('simulated fills are identical under both schedules');
  await expect(ro).toContainText('LP tier 4 is hypothetical');
  await page.locator('#sb-fill').selectOption('optimistic');
  await expect(ro).toContainText('not evidence of what live fills would have been');
  for (const b of await ro.locator('b.num').all()) expect(await b.getAttribute('data-src')).toBeTruthy();
  const rows = page.locator('.row');
  for (let i = 0; i < 8; i += 1) {
    const row = rows.nth(i);
    if ((await row.locator('.note').count()) === 0) await expect(row.locator('.val [data-fee="hypothetical"]')).toHaveCount(1);
  }
});

test('full lab: untested, unknown and not-varied selections show an explicit unavailable state', async ({ page }) => {
  await lab(page, '#view=e003');
  await assumptions(page);
  await page.locator('#sb-fill').selectOption('naive');
  await expect(page.locator('.readout.unav')).toContainText('Not tested.');
  await page.goto('about:blank');
  await lab(page, '#focus=P9&fill=intermediate');
  await expect(page.locator('.readout.unav')).toContainText('Unknown value.');
  await page.goto('about:blank');
  await lab(page, '#limits=other');
  await expect(page.locator('.readout.unav')).toContainText('Not varied.');
});

test('full lab: held-out values are reported only; abstainers are mechanical zeros', async ({ page }) => {
  await lab(page, '#view=e003');
  await expect(page.locator('.row').filter({ has: page.locator('.who b', { hasText: /^P3F$/ }) })).toContainText('abstained: the zero is mechanical');
  await assumptions(page);
  await page.locator('#sb-sample').selectOption('heldout');
  await expect(page.locator('.readout')).toContainText('reported only, descriptive (no confirmation claim)');
  await expect(page.locator('#result')).not.toContainText('confirmed (point');
});

test('full lab: controls follow the experiment; E004 defines D_W correctly', async ({ page }) => {
  await lab(page, '#view=e003');
  await expect(page.locator('.sbar select')).toHaveCount(6);
  await page.getByRole('tab', { name: /Execution/ }).click();
  await expect(page.locator('.sbar select')).toHaveCount(1);
  await expect(page.locator('.sbar')).toContainText('P0 and P1, both shown');
  await page.getByRole('tab', { name: /Execution/ }).press('ArrowRight');
  await expect(page.getByRole('tab', { name: /Stale data/ })).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('.sbar')).toContainText('regional latency only');
  await expect(page.locator('#result')).toContainText('random-window fill quality minus stale-window fill quality');
  await expect(page.locator('#result')).toContainText('no material deterioration under the specified threshold');
});

test('full lab: settings explain themselves on request', async ({ page }) => {
  await lab(page, '#view=e003');
  await expect(page.locator('#sbar-help')).toBeHidden();
  await page.getByRole('button', { name: 'What do these mean?' }).click();
  await expect(page.locator('#sbar-help')).toContainText('Market data show how much is resting');
});

test('research: experiments open one at a time, each from question to limits', async ({ page }) => {
  await page.goto('/research');
  await expect(page.locator('details.xp')).toHaveCount(4);
  for (const id of ['e001', 'e002', 'e003', 'e004']) {
    const xp = page.locator(`#${id}`);
    await xp.locator('summary').first().click();
    for (const h of ['Why it matters', 'How it was tested', 'What it means', 'Limitations']) await expect(xp.locator('h3', { hasText: h })).toBeVisible();
  }
  await expect(page.locator('#e004')).toContainText('random-window fill quality minus stale-window fill quality');
  const tallies = page.locator('.checks.big');
  await expect(tallies).toContainText('6 of 6 confirmed');
  await expect(tallies).toContainText('no confirmation claim');
});

test('methods: the seven steps are visible and topics open on demand', async ({ page }) => {
  await page.goto('/methods');
  await expect(page.locator('.pipe li')).toHaveCount(7);
  await expect(page.locator('details.acc')).toHaveCount(11);
  await expect(page.locator('.acc-gh')).toHaveText(['Data', 'Simulation', 'Inference', 'Limits and sources']);
  await page.locator('#why summary').click();
  await expect(page.locator('#why')).toContainText('A tick that matters');
});

test('paper: frozen PDFs are served', async ({ request }) => {
  for (const f of ['/paper/The_Liquidity_Paradox.pdf', '/paper/Reproducibility_Supplement.pdf']) {
    const r = await request.get(f);
    expect(r.status()).toBe(200);
    expect(r.headers()['content-type']).toContain('pdf');
  }
});

test('paper: the source-code note links to the public repository', async ({ page }) => {
  await page.goto('/paper');
  await expect(page.locator('a[href="https://github.com/VM25/liquidity-lab"]')).toHaveText('github.com/VM25/liquidity-lab');
});

test('routing: the earlier .html addresses redirect permanently, keeping the hash', async ({ page, request }) => {
  for (const [from, to] of [['/index.html', '/'], ['/lab.html', '/lab'], ['/research.html', '/research'], ['/methods.html', '/methods'], ['/paper.html', '/paper']]) {
    const r = await request.get(from, { maxRedirects: 0 });
    expect(r.status()).toBe(308);
    expect(r.headers().location).toBe(to);
  }
  await page.goto('/lab.html#step=3');
  await expect(page).toHaveURL(/\/lab#step=3$/);
  await expect(page.locator('.story h2')).toHaveText('The fee decides');
});

test('hydration survives the line break and comment Netlify inserts at the top of <head>', async ({ page }) => {
  for (const p of PAGES) {
    const errors: string[] = [];
    page.on('pageerror', (e) => errors.push(String(e)));
    await page.route((u) => u.pathname === p, async (route) => {
      const r = await route.fetch();
      const html = (await r.text()).replace(/(<meta charSet="utf-8"\/>)(?!\n<!-- This site)/, '$1\n<!-- This site is hosted on Netlify. -->');
      await route.fulfill({ response: r, body: html });
    });
    await page.goto(p);
    await page.waitForLoadState('networkidle');
    expect(errors, p).toEqual([]);
    await page.unrouteAll();
    page.removeAllListeners('pageerror');
  }
});

test('routing: an unknown address returns 404', async ({ request }) => {
  expect((await request.get('/no-such-page')).status()).toBe(404);
});

test('metadata: titles, canonical URLs, share image, robots.txt and sitemap', async ({ page, request }) => {
  const titles: Record<string, string> = { '/': 'The Liquidity Paradox', '/lab': 'Scenario Lab · The Liquidity Paradox', '/research': 'Research · The Liquidity Paradox', '/methods': 'Methods & Data · The Liquidity Paradox', '/paper': 'Paper & Code · The Liquidity Paradox' };
  const indexable = process.env.CONTEXT === 'production';
  for (const p of PAGES) {
    await page.goto(p);
    await expect(page).toHaveTitle(titles[p]);
    await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', `https://liquidityparadox.netlify.app${p === '/' ? '' : p}`);
    await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', 'https://liquidityparadox.netlify.app/og-image.png');
    await expect(page.locator('meta[name="robots"]')).toHaveAttribute('content', indexable ? 'index, follow' : 'noindex, nofollow');
  }
  const og = await request.get('/og-image.png');
  expect(og.status()).toBe(200);
  expect(og.headers()['content-type']).toContain('image/png');
  const robots = await (await request.get('/robots.txt')).text();
  expect(robots).toMatch(indexable ? /Allow: \/[\s\S]*Sitemap: https:\/\/liquidityparadox\.netlify\.app\/sitemap\.xml/ : /Disallow: \//);
  const sitemap = await (await request.get('/sitemap.xml')).text();
  for (const p of PAGES) expect(sitemap).toContain(`<loc>https://liquidityparadox.netlify.app${p === '/' ? '' : p}</loc>`);
});
