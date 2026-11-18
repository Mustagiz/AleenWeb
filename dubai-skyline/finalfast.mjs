import { chromium } from 'playwright-core';
const browser=await chromium.launch({channel:'chrome',headless:true,args:['--disable-background-timer-throttling','--disable-renderer-backgrounding']});
const page=await browser.newPage({viewport:{width:1440,height:900}});
const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
const t=Date.now();
await page.goto('http://127.0.0.1:4174/',{waitUntil:'domcontentloaded'});
await page.waitForTimeout(300);
await page.screenshot({path:'shots/instant-hero.png'});
await page.waitForTimeout(2200);
const st=await page.evaluate(()=>({cls:document.body.className,h1:getComputedStyle(document.querySelector('.hero h1')).opacity,badge:getComputedStyle(document.querySelector('.render-badge')).visibility,label:document.querySelector('#render-label').textContent,scene:getComputedStyle(document.querySelector('#scene')).opacity}));
console.log('state at 2.5s',Date.now()-t,st,'errors',errors);
await page.screenshot({path:'shots/instant-2s.png'});
try { await page.waitForFunction(()=>document.body.classList.contains('is-scene-ready'),null,{timeout:15000}); console.log('scene ready at',Date.now()-t); } catch { console.log('scene not ready'); }
await page.waitForTimeout(1200);
await page.screenshot({path:'shots/instant-final.png'});
await browser.close();
