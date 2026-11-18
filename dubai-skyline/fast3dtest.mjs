import { chromium } from 'playwright-core';
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--disable-background-timer-throttling','--disable-renderer-backgrounding']});
const page=await browser.newPage({viewport:{width:1440,height:900}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
const t=Date.now();
await page.goto('http://127.0.0.1:4174/',{waitUntil:'domcontentloaded'});
await page.waitForTimeout(250);
await page.screenshot({path:'shots/fast3d-early.png'});
try { await page.waitForFunction(()=>document.body.classList.contains('is-scene-ready'),null,{timeout:20000}); console.log('3D ready',Date.now()-t,'ms'); } catch { console.log('3D timeout',Date.now()-t,await page.evaluate(()=>document.body.className)); }
await page.waitForTimeout(1200);
await page.screenshot({path:'shots/fast3d-final.png'});
console.log('errors',errors);
await browser.close();
