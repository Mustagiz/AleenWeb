import { chromium } from 'playwright-core';
const browser = await chromium.launch({ channel: 'chrome', headless: true, args:['--disable-background-timer-throttling'] });
const page = await browser.newPage({ viewport:{width:1440,height:900} });
const t=Date.now();
await page.goto('http://127.0.0.1:4173/', {waitUntil:'load'});
await page.waitForTimeout(2500);
console.log('total',Date.now()-t, await page.evaluate(()=>window.__phase));
await browser.close();
