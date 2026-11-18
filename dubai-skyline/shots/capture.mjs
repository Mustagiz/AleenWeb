import { chromium } from 'playwright-core';

const url = 'http://127.0.0.1:4173/';
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 1600, height: 900 }, deviceScaleFactor: 1 });

const logs = [];
page.on('console', m => logs.push(`[${m.type()}] ${m.text()}`));
page.on('pageerror', e => logs.push(`[pageerror] ${e.message}`));
page.on('requestfailed', r => logs.push(`[reqfail] ${r.url()} ${r.failure()?.errorText}`));

await page.goto(url, { waitUntil: 'load' });
await page.waitForFunction(() => document.body.classList.contains('is-scene-ready'), null, { timeout: 30000 });
await page.waitForTimeout(1600);

const steps = [0, 0.2, 0.4, 0.6, 0.8, 1];
for (const p of steps) {
  await page.evaluate((pp) => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    window.scrollTo({ top: max * pp, behavior: 'instant' });
  }, p);
  await page.waitForTimeout(1800);
  await page.screenshot({ path: `shots/shot-${String(Math.round(p * 100)).padStart(3, '0')}.png` });
}

// mobile
const m = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
await m.goto(url, { waitUntil: 'load' });
await m.waitForFunction(() => document.body.classList.contains('is-scene-ready'), null, { timeout: 30000 });
await m.waitForTimeout(1600);
await m.screenshot({ path: 'shots/mobile-hero.png' });

console.log(logs.join('\n') || 'no console output');
await browser.close();
