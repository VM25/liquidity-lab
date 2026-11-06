// Captures the review screenshot set from the running local preview (http://localhost:4323). Not part of the build.
import { chromium } from '@playwright/test';

const BASE = process.env.BASE ?? 'http://localhost:4323/';
const OUT = new URL(`../../design/screenshots/${process.env.SET ?? 'polish'}/`, import.meta.url).pathname;
const PAGES = [['', 'home'], ['lab', 'explore'], ['research', 'research'], ['methods', 'methods'], ['paper', 'paper']];
const browser = await chromium.launch({ channel: 'chrome' });
const shot = async (page, name, opts = {}) => { await page.waitForTimeout(500); await page.screenshot({ path: `${OUT}${name}.jpg`, type: 'jpeg', quality: 84, ...opts }); console.log(name); };
const fresh = async (page, url) => { await page.goto(BASE + 'paper'); await page.goto(BASE + url); await page.waitForLoadState('networkidle'); await page.waitForTimeout(url === '' ? 1700 : 300); };
// Below-the-fold reveals wait for the reader to arrive; walk the page once so a full-page capture shows everything.
const walk = async (page) => {
  await page.evaluate(async () => {
    const step = Math.round(innerHeight * 0.7);
    for (let y = 0; y < document.documentElement.scrollHeight; y += step) { scrollTo({ top: y, behavior: 'instant' }); await new Promise((r) => setTimeout(r, 120)); }
    scrollTo({ top: 0, behavior: 'instant' });
  });
  await page.waitForTimeout(1000);
};

for (const [vp, w, h, mobile] of [['desktop', 1440, 900, false], ['mobile', 390, 844, true]]) {
  const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: mobile ? 2 : 1, isMobile: mobile, hasTouch: mobile });
  const page = await ctx.newPage();
  for (const [file, name] of PAGES) {
    await fresh(page, file);
    await shot(page, `${name}-${vp}-first-screen`);
    await walk(page);
    await shot(page, `${name}-${vp}-full`, { fullPage: true, quality: 72 });
  }
  await ctx.close();
}

const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await ctx.newPage();
for (let i = 1; i <= 6; i += 1) {
  await fresh(page, `lab#step=${i}`);
  await page.evaluate(() => { document.querySelector('.story-rail').scrollIntoView(); scrollBy(0, -90); });
  await shot(page, `explore-story-step-${i}`);
}
await fresh(page, 'lab#step=3');
await page.locator('.story').getByRole('radio', { name: /LP tier 4/ }).click();
await page.evaluate(() => { document.querySelector('.story-rail').scrollIntoView(); scrollBy(0, -90); });
await shot(page, 'explore-story-step-3-lp-tier4');
await fresh(page, 'lab#view=e003');
await page.evaluate(() => { document.querySelector('.views').scrollIntoView(); scrollBy(0, -90); });
await shot(page, 'explore-full-lab');
await page.getByRole('button', { name: 'Change assumptions' }).click();
await page.locator('#sb-fee').selectOption('lp_tier4');
await page.evaluate(() => { document.querySelector('.readout').scrollIntoView(); scrollBy(0, -90); });
await shot(page, 'explore-full-lab-what-changed');
await page.getByRole('button', { name: 'What do these mean?' }).click();
await page.evaluate(() => { document.querySelector('.sbar-wrap').scrollIntoView(); scrollBy(0, -90); });
await shot(page, 'explore-full-lab-settings-help');
await fresh(page, 'lab#view=e004');
await page.evaluate(() => { document.querySelector('.views').scrollIntoView(); scrollBy(0, -90); });
await shot(page, 'explore-full-lab-e004');
await fresh(page, 'research');
await page.locator('#e003 summary').first().click();
await page.evaluate(() => { document.getElementById('e003').scrollIntoView(); scrollBy(0, -90); });
await shot(page, 'research-e003-open');
await fresh(page, 'methods');
await page.locator('#sessions summary').first().click();
await page.evaluate(() => { document.getElementById('sessions').scrollIntoView(); scrollBy(0, -90); });
await shot(page, 'methods-sessions-open');
await ctx.close();

const m = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
const mp = await m.newPage();
await fresh(mp, 'lab#step=3');
await mp.evaluate(() => { document.querySelector('.story-n').scrollIntoView(); scrollBy(0, -90); });
await shot(mp, 'explore-mobile-story-step-3');
await mp.evaluate(() => { document.querySelector('.story-v').scrollIntoView(); scrollBy(0, -80); });
await shot(mp, 'explore-mobile-story-step-3-visual');
await fresh(mp, 'lab#view=e003');
await mp.evaluate(() => { document.querySelector('.views').scrollIntoView(); scrollBy(0, -80); });
await shot(mp, 'explore-mobile-full-lab');
await m.close();
await browser.close();
