import { chromium } from 'playwright-core';
const browser = await chromium.launch({ channel: 'chrome', headless: true, args: ['--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'] });
for (let i=0;i<3;i++) {
  const ctx = await browser.newContext({ viewport:{width:1440,height:900} });
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page);
  await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
  await page.addInitScript(() => {
    window.__lt=[]; new PerformanceObserver(l => l.getEntries().forEach(e=>window.__lt.push({start:Math.round(e.startTime),dur:Math.round(e.duration)}))).observe({type:'longtask', buffered:true});
  });
  const t = Date.now();
  await page.goto('http://127.0.0.1:4173/', { waitUntil:'domcontentloaded' });
  await page.waitForFunction(() => document.body.classList.contains('is-loaded'), null, {timeout:30000});
  const ms = Date.now()-t;
  const data = await page.evaluate(() => ({
    now: Math.round(performance.now()),
    nav: (()=>{const n=performance.getEntriesByType('navigation')[0]; return {dcl:Math.round(n.domContentLoadedEventEnd),load:Math.round(n.loadEventEnd),responseEnd:Math.round(n.responseEnd)};})(),
    longtasks: window.__lt,
    body: document.body.className,
    loader: document.querySelector('#loader').className,
    loaderOpacity: getComputedStyle(document.querySelector('#loader')).opacity,
  }));
  console.log(i, 'is-loaded total', ms, JSON.stringify(data,null,2));
  await ctx.close();
}
await browser.close();
