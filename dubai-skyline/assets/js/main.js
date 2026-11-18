import * as THREE from 'three';

import { createFastMaterials } from './materials.js';
import { createFastEnvironment } from './environment.js';
import { buildCity } from './city.js';

/* ------------------------------------------------------------------ *
 *  Camera choreography: one keyframe per scene chapter.
 * ------------------------------------------------------------------ */
const KEYS = [
  { p: 0.0, pos: [-118, 26, -152], look: [-8, 62, 60] },
  { p: 0.2, pos: [-78, 36, -92], look: [-46, 58, 58] },
  { p: 0.4, pos: [52, 24, -108], look: [116, 30, 24] },
  { p: 0.6, pos: [150, 22, -124], look: [206, 30, -52] },
  { p: 0.8, pos: [18, 108, -250], look: [58, 10, 66] },
  { p: 1.0, pos: [-104, 20, -168], look: [-46, 58, 60] },
];

const INTRO_START = { pos: [-210, 92, -320], look: [-20, 46, 70] };

const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const isSmall = () => window.innerWidth < 820;

const canvas = document.getElementById('scene');
const renderLabel = document.getElementById('render-label');
const body = document.body;

/* ------------------------------------------------------------------ *
 *  Boot
 *
 *  The poster and the editorial UI are painted first. The WebGL scene is
 *  built on the next task and crossfades in when its first frame is ready,
 *  so a cold shader compile never blocks the page from appearing.
 * ------------------------------------------------------------------ */
let renderer;
/* Never gate scene startup on requestAnimationFrame: background tabs and
   embedded previews can throttle it indefinitely, leaving only the poster. */
setTimeout(boot, 0);

function boot() {
  try {
    renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: false,
      powerPreference: 'high-performance',
      stencil: false,
    });
  } catch (err) {
    body.classList.add('no-webgl');
    console.error(err);
    return;
  }

  start().catch((err) => {
    body.classList.add('no-webgl');
    console.error(err);
  });
}

async function start() {
  const nextFrame = () => new Promise((resolve) => setTimeout(resolve, 0));
  const DPR_CAP = isSmall() ? 1.25 : 1.5;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, DPR_CAP));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.toneMapping = THREE.NeutralToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(47, window.innerWidth / window.innerHeight, 0.5, 12000);
  camera.position.set(...INTRO_START.pos);

  const env = createFastEnvironment(renderer, scene);
  await nextFrame();
  const mats = createFastMaterials();
  const city = buildCity(mats, mats.shadow);
  scene.add(city);

  /* ---------------- state ---------------- */
  const pointer = new THREE.Vector2(0, 0);
  const pointerSmooth = new THREE.Vector2(0, 0);
  let scrollP = 0;
  let scrollSmooth = 0;
  let introT = prefersReduced ? 1 : 0;
  const clock = new THREE.Clock();

  const keyPosA = new THREE.Vector3();
  const keyPosB = new THREE.Vector3();
  const keyLookA = new THREE.Vector3();
  const keyLookB = new THREE.Vector3();

  function sampleCamera(p) {
    let i = 0;
    while (i < KEYS.length - 2 && p > KEYS[i + 1].p) i++;
    const a = KEYS[i];
    const b = KEYS[i + 1];
    const span = b.p - a.p || 1;
    let t = THREE.MathUtils.clamp((p - a.p) / span, 0, 1);
    t = t * t * t * (t * (t * 6 - 15) + 10); // smootherstep

    keyPosA.set(...a.pos);
    keyPosB.set(...b.pos);
    keyLookA.set(...a.look);
    keyLookB.set(...b.look);

    return {
      pos: keyPosA.clone().lerp(keyPosB, t),
      look: keyLookA.clone().lerp(keyLookB, t),
    };
  }

  function onResize() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    camera.aspect = w / h;
    camera.fov = w < 700 ? 60 : 47;
    camera.updateProjectionMatrix();
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, DPR_CAP));
    renderer.setSize(w, h);
  }
  window.addEventListener('resize', onResize, { passive: true });
  onResize();

  window.addEventListener('pointermove', (e) => {
    pointer.x = (e.clientX / window.innerWidth) * 2 - 1;
    pointer.y = (e.clientY / window.innerHeight) * 2 - 1;
  }, { passive: true });

  const readScroll = () => {
    const max = document.documentElement.scrollHeight - window.innerHeight;
    scrollP = max > 0 ? THREE.MathUtils.clamp(window.scrollY / max, 0, 1) : 0;
  };
  window.addEventListener('scroll', readScroll, { passive: true });
  readScroll();

  /* ---------------- loop ---------------- */
  const lookTarget = new THREE.Vector3();
  let elapsed = 0;

  /* 3D-anchored landmark label. Project a point on the Burj into screen
     space each frame so the annotation sits on the tower, not on the page. */
  const marker = document.getElementById('hero-marker');
  const markerWorld = city.userData.landmarkWorld.clone();
  markerWorld.y -= 16;
  const markerScreen = new THREE.Vector2(-9999, -9999);
  const markerTarget = new THREE.Vector2();
  const projected = new THREE.Vector3();

  function updateMarker(dt) {
    if (!marker) return;
    projected.copy(markerWorld).project(camera);
    const inFrame = projected.z > 0 && projected.z < 1
      && Math.abs(projected.x) < 0.94 && Math.abs(projected.y) < 0.9;
    const on = introT > 0.72 && scrollP < 0.1 && inFrame;

    if (!on) {
      marker.classList.remove('is-on');
      return;
    }

    markerTarget.set(
      (projected.x * 0.5 + 0.5) * window.innerWidth + 12,
      (-projected.y * 0.5 + 0.5) * window.innerHeight
    );
    markerScreen.lerp(markerTarget, Math.min(1, dt * 9));
    marker.style.setProperty('--mx', `${markerScreen.x.toFixed(1)}px`);
    marker.style.setProperty('--my', `${markerScreen.y.toFixed(1)}px`);
    marker.classList.add('is-on');
  }

  function frame() {
    requestAnimationFrame(frame);
    const dt = Math.min(clock.getDelta(), 0.05);
    elapsed += dt;

    introT = Math.min(1, introT + dt * 0.9);
    const introEase = 1 - Math.pow(1 - introT, 3);

    scrollSmooth += (scrollP - scrollSmooth) * Math.min(1, dt * 5);
    pointerSmooth.x += (pointer.x - pointerSmooth.x) * Math.min(1, dt * 3);
    pointerSmooth.y += (pointer.y - pointerSmooth.y) * Math.min(1, dt * 3);

    const shot = sampleCamera(scrollSmooth);

    const startPos = new THREE.Vector3(...INTRO_START.pos);
    const startLook = new THREE.Vector3(...INTRO_START.look);
    const pos = startPos.lerp(shot.pos, introEase);
    const look = startLook.lerp(shot.look, introEase);

    const drift = prefersReduced ? 0 : 1;
    pos.x += Math.sin(elapsed * 0.23) * 1.6 * drift + pointerSmooth.x * 5.5 * drift;
    pos.y += Math.cos(elapsed * 0.19) * 1.1 * drift - pointerSmooth.y * 3.2 * drift;
    look.x += pointerSmooth.x * 2.4 * drift;
    look.y += -pointerSmooth.y * 1.6 * drift;

    camera.position.lerp(pos, Math.min(1, dt * 3.2));
    lookTarget.lerp(look, Math.min(1, dt * 3.6));
    camera.lookAt(lookTarget);

    env.update(elapsed, camera);
    updateMarker(dt);
    renderer.render(scene, camera);
  }

  /* Compile programs off the critical path where the driver supports it. */
  /* first frame before revealing */
  env.update(0, camera);
  camera.lookAt(new THREE.Vector3(...INTRO_START.look));
  renderer.render(scene, camera);
  requestAnimationFrame(frame);

  /* Reveal the live canvas only once it has something to show. */
  body.classList.add('is-scene-ready');
  body.classList.remove('is-static-ready');
  if (renderLabel) renderLabel.textContent = 'Live 3D render';
  document.dispatchEvent(new CustomEvent('scene:ready'));

  /* pause rendering when the tab is hidden */
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) clock.stop();
    else clock.start();
  });
}
