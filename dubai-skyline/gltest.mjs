import { chromium } from 'playwright-core';
const variants=[
 {powerPreference:'high-performance',antialias:true},
 {powerPreference:'default',antialias:true},
 {powerPreference:'low-power',antialias:true},
 {powerPreference:'high-performance',antialias:false},
 {powerPreference:'default',antialias:false},
];
const html = (opts)=>`<!doctype html><html><body><canvas id=c style="width:800px;height:600px"></canvas><script type="module">
import * as THREE from '/vendor/three.module.js';
const t=performance.now();
const r=new THREE.WebGLRenderer({canvas:document.getElementById('c'), ...${JSON.stringify(opts)}});
r.setPixelRatio(1); r.setSize(800,600);
const gl=r.getContext();
window.__t=performance.now()-t;
window.__renderer=gl.getParameter(gl.RENDERER);
</script></body></html>`;
const browser=await chromium.launch({channel:'chrome',headless:true});
for (const v of variants) {
 const ctx=await browser.newContext({viewport:{width:900,height:700}});
 const page=await ctx.newPage();
 await page.route('http://127.0.0.1:4173/__gltest', r=>r.fulfill({contentType:'text/html',body:html(v)}));
 await page.goto('http://127.0.0.1:4173/__gltest');
 await page.waitForFunction(()=>window.__t!==undefined,{timeout:20000}).catch(()=>{});
 console.log(v, await page.evaluate(()=>({t:Math.round(window.__t), r:window.__renderer})));
 await ctx.close();
}
await browser.close();
