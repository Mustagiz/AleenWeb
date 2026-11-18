import { chromium } from 'playwright-core';
const browser = await chromium.launch({ channel: 'chrome', headless: true, args: ['--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'] });
for (const [w,h,cpu] of [[1600,900,1],[1440,900,4],[390,844,4]]) {
  const page = await browser.newPage({ viewport:{width:w,height:h}, deviceScaleFactor:1, isMobile:w<500, hasTouch:w<500 });
  if (cpu > 1) { const cdp = await page.context().newCDPSession(page); await cdp.send('Emulation.setCPUThrottlingRate', { rate: cpu }); }
  const nav = await page.goto('http://127.0.0.1:4173/', { waitUntil: 'load' });
  const t0 = Date.now();
  await page.waitForFunction(() => document.body.classList.contains('is-loaded'), null, { timeout: 30000 });
  const loaded = Date.now()-t0;
  const metrics = await page.evaluate(() => {
    const n = performance.getEntriesByType('navigation')[0];
    const res = performance.getEntriesByType('resource');
    return {
      dcl: Math.round(n.domContentLoadedEventEnd), load: Math.round(n.loadEventEnd),
      transfer: res.reduce((a,r)=>a+(r.transferSize||0),0),
      count: res.length,
      res: res.map(r=>({name:r.name.split('/').pop(), ms:Math.round(r.duration), size:r.transferSize})).sort((a,b)=>b.ms-a.ms).slice(0,8),
      dpr: devicePixelRatio,
      canvas: [document.querySelector('#scene').width, document.querySelector('#scene').height],
    };
  });
  console.log(w+'x'+h, 'cpu'+cpu, 'is-loaded after', loaded, 'ms', JSON.stringify(metrics,null,2));
  await page.close();
}
await browser.close();
