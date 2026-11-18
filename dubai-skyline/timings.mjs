import { chromium } from 'playwright-core';
const browser = await chromium.launch({ channel:'chrome', headless:true, args:['--disable-background-timer-throttling'] });
for(let i=0;i<2;i++){
 const page=await browser.newPage({viewport:{width:1280,height:800}});
 await page.addInitScript(()=>{window.__lt=[];new PerformanceObserver(l=>l.getEntries().forEach(e=>window.__lt.push({s:Math.round(e.startTime),d:Math.round(e.duration)}))).observe({type:'longtask',buffered:true});});
 await page.goto('http://127.0.0.1:4173/',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>document.body.classList.contains('is-scene-ready'),null,{timeout:20000});
 console.log(i, await page.evaluate(()=>({ms:window.__ms, lt:window.__lt})));
 await page.close();
}
await browser.close();
