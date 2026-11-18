import { chromium } from 'playwright-core';
for (const args of [[],['--use-angle=metal'],['--use-gl=angle','--use-angle=metal','--enable-gpu'],['--enable-gpu']]) {
  let browser;
  try { browser = await chromium.launch({ channel:'chrome', headless:true, args:[...args,'--disable-background-timer-throttling'] }); } catch(e){ console.log(args,'launch fail'); continue; }
  const page = await browser.newPage({ viewport:{width:1280,height:800} });
  const t=Date.now();
  await page.goto('http://127.0.0.1:4173/', {waitUntil:'domcontentloaded'});
  let out=''; try { await page.waitForFunction(() => document.body.classList.contains('is-scene-ready'), null, {timeout:15000}); out=Date.now()-t+'ms'; } catch { out='timeout'; }
  const gpu = await page.evaluate(() => { const gl=document.createElement('canvas').getContext('webgl2'); if(!gl) return 'no webgl2'; const ext=gl.getExtension('WEBGL_debug_renderer_info'); return ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):'unknown'; });
  console.log(JSON.stringify(args), out, gpu);
  await browser.close();
}
