import { chromium } from 'playwright-core';
const browser = await chromium.launch({ channel: 'chrome', headless: true, args:['--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows'] });
for (const blockRaf of [false,true]) {
  const page = await browser.newPage({ viewport:{width:1280,height:800} });
  const errors=[]; page.on('pageerror',e=>errors.push(e.message)); page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
  if (blockRaf) await page.addInitScript(() => { window.requestAnimationFrame = () => 0; });
  const t=Date.now();
  await page.goto('http://127.0.0.1:4173/', {waitUntil:'domcontentloaded'});
  try {
    await page.waitForFunction(() => document.body.classList.contains('is-scene-ready'), null, {timeout:12000});
    console.log('rafBlocked',blockRaf,'scene-ready in',Date.now()-t,'ms');
  } catch { console.log('rafBlocked',blockRaf,'TIMEOUT',Date.now()-t,'ms', await page.evaluate(()=>document.body.className)); }
  await page.screenshot({path:`shots/qa-raf-${blockRaf}.png`});
  console.log('errors',errors);
  await page.close();
}
await browser.close();
