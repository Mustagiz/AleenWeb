import { chromium } from 'playwright-core';
const browser = await chromium.launch({ channel: 'chrome', headless: true, args: ['--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'] });
for (const [w,h,name] of [[1280,800,'1280'],[1024,768,'1024'],[768,1024,'768']]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log(name,'PAGEERROR', e.message));
  page.on('response', r => { if (r.status() >= 400) console.log(name,'HTTP', r.status(), r.url()); });
  await page.goto('http://127.0.0.1:4173/', { waitUntil: 'load' });
  await page.waitForTimeout(4200);
  await page.screenshot({ path: `shots/resp-${name}.png` });
  await page.close();
}
await browser.close();
