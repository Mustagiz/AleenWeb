import { chromium } from 'playwright-core';
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:900}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
const t=Date.now();
await page.goto('http://127.0.0.1:4174/',{waitUntil:'domcontentloaded'});
await page.waitForTimeout(500);
console.log('500ms state', Date.now()-t, await page.evaluate(()=>({cls:document.body.className,h1:getComputedStyle(document.querySelector('.hero h1')).opacity,fallback:getComputedStyle(document.querySelector('.fallback')).opacity,scene:getComputedStyle(document.querySelector('#scene')).opacity,label:document.querySelector('.render-badge').textContent.trim()})),'errors',errors);
await page.screenshot({path:'shots/instant-final-500.png'});
await page.click('#launch-3d');
try { await page.waitForFunction(()=>document.body.classList.contains('is-scene-ready'),null,{timeout:25000}); console.log('live 3D ready',Date.now()-t); } catch { console.log('live 3D timeout',Date.now()-t); }
await page.waitForTimeout(1200);
await page.screenshot({path:'shots/instant-live.png'});
await browser.close();
