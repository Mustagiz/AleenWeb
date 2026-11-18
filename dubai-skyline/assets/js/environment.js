import * as THREE from 'three';
import { makeGroundTexture, makeGroundEmissive } from './materials.js';

/* ------------------------------------------------------------------ *
 *  Dusk environment: sky, sun rig, sea, city ground.
 *  The environment map is built from a painted equirect canvas, so the
 *  glass reflects a plausible sunset instead of a grey studio.
 * ------------------------------------------------------------------ */

export const SUN_DIR = new THREE.Vector3(-0.86, 0.035, -0.28).normalize();

const SKY_VERT = /* glsl */ `
  varying vec3 vWorld;
  void main() {
    vec4 wp = modelMatrix * vec4(position, 1.0);
    vWorld = wp.xyz;
    gl_Position = projectionMatrix * viewMatrix * wp;
  }
`;

const SKY_FRAG = /* glsl */ `
  varying vec3 vWorld;
  uniform vec3 uSunDir;
  uniform vec3 uZenith;
  uniform vec3 uHorizonWarm;
  uniform vec3 uHorizonCool;
  uniform vec3 uSunColor;
  uniform float uExposure;

  float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
  }

  void main() {
    vec3 dir = normalize(vWorld);
    float h = clamp(dir.y, -0.2, 1.0);

    float az = dot(normalize(dir.xz + 1e-5), normalize(uSunDir.xz + 1e-5));
    vec3 horizon = mix(uHorizonCool, uHorizonWarm, smoothstep(-0.8, 1.0, az));

    float t = pow(clamp(h, 0.0, 1.0), 0.5);
    vec3 col = mix(horizon, uZenith, t);

    // low warm band, densest at the sun side
    float band = exp(-pow((h - 0.01) * 16.0, 2.0));
    col += uSunColor * band * (0.18 + 0.22 * smoothstep(-0.2, 1.0, az));

    // sun disc + glow
    float s = max(dot(dir, normalize(uSunDir)), 0.0);
    col += uSunColor * pow(s, 900.0) * 3.0;
    col += uSunColor * pow(s, 24.0) * 0.35;
    col += uSunColor * pow(s, 4.0) * 0.12;

    // thin cloud strata
    float bands = sin(dir.y * 34.0 + az * 3.0) * 0.5 + 0.5;
    bands *= smoothstep(0.02, 0.14, h) * smoothstep(0.42, 0.12, h);
    col += vec3(0.06, 0.05, 0.055) * bands;

    col *= uExposure;
    col += (hash(gl_FragCoord.xy) - 0.5) * 0.006;

    gl_FragColor = vec4(col, 1.0);
    #include <colorspace_fragment>
  }
`;

const WATER_VERT = /* glsl */ `
  varying vec3 vWorld;
  void main() {
    vec4 wp = modelMatrix * vec4(position, 1.0);
    vWorld = wp.xyz;
    gl_Position = projectionMatrix * viewMatrix * wp;
  }
`;

const WATER_FRAG = /* glsl */ `
  varying vec3 vWorld;
  uniform float uTime;
  uniform vec3 uSunDir;
  uniform vec3 uSunColor;
  uniform vec3 uDeep;
  uniform vec3 uShallow;
  uniform vec3 uSky;
  uniform vec3 uFogColor;
  uniform float uFogDensity;
  uniform vec3 uCamPos;

  vec3 waveNormal(vec2 p, float t) {
    vec3 n = vec3(0.0, 1.0, 0.0);
    vec2 d1 = normalize(vec2( 0.8,  0.4));
    vec2 d2 = normalize(vec2(-0.5,  0.9));
    vec2 d3 = normalize(vec2( 0.2, -1.0));
    vec2 d4 = normalize(vec2(-0.9, -0.3));

    float w1 = sin(dot(p, d1) * 0.5 + t * 0.8);
    float w2 = sin(dot(p, d2) * 1.1 + t * 1.2);
    float w3 = sin(dot(p, d3) * 2.6 + t * 1.9);
    float w4 = sin(dot(p, d4) * 6.2 + t * 3.1);

    n.x += d1.x * w1 * 0.022 + d2.x * w2 * 0.013 + d3.x * w3 * 0.006 + d4.x * w4 * 0.0026;
    n.z += d1.y * w1 * 0.022 + d2.y * w2 * 0.013 + d3.y * w3 * 0.006 + d4.y * w4 * 0.0026;
    return normalize(n);
  }

  void main() {
    vec3 viewDir = normalize(uCamPos - vWorld);
    vec3 n = waveNormal(vWorld.xz, uTime);

    float fres = pow(1.0 - clamp(dot(n, viewDir), 0.0, 1.0), 5.0);
    fres = mix(0.02, 1.0, fres);

    vec3 col = mix(uDeep, uShallow, 0.25 + 0.5 * fres);
    col = mix(col, uSky, clamp(fres * 1.15, 0.0, 0.96));
    col += uSky * 0.06;

    vec3 r = reflect(-normalize(uSunDir), n);
    float spec = pow(max(dot(r, viewDir), 0.0), 420.0);
    float glitter = pow(max(dot(r, viewDir), 0.0), 60.0) * 0.22;
    col += uSunColor * (spec * 2.2 + glitter);

    float dist = length(uCamPos - vWorld);
    float fogF = 1.0 - exp(-pow(dist * uFogDensity, 2.0));
    col = mix(col, uFogColor, clamp(fogF, 0.0, 1.0));

    gl_FragColor = vec4(col, 1.0);
    #include <colorspace_fragment>
  }
`;

/* Painted equirect panorama used for image-based lighting. */
function buildEnvironmentEquirect(sunDir) {
  const W = 1024;
  const H = 512;
  const c = document.createElement('canvas');
  c.width = W;
  c.height = H;
  const ctx = c.getContext('2d');

  // sky gradient by elevation
  const g = ctx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0.0, '#040910');
  g.addColorStop(0.24, '#0d2138');
  g.addColorStop(0.42, '#2f5878');
  g.addColorStop(0.485, '#7f6a5c');
  g.addColorStop(0.5, '#9a5f42');
  g.addColorStop(0.515, '#3a3f4a');
  g.addColorStop(0.6, '#151a20');
  g.addColorStop(1.0, '#0a0c0f');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, W, H);

  // sun glow at its equirect position
  const u = Math.atan2(sunDir.z, sunDir.x) / (Math.PI * 2) + 0.5;
  const v = Math.asin(sunDir.y) / Math.PI + 0.5;
  const sx = u * W;
  const sy = (1 - v) * H;

  const glow = ctx.createRadialGradient(sx, sy, 0, sx, sy, W * 0.34);
  glow.addColorStop(0, 'rgba(255,214,170,0.95)');
  glow.addColorStop(0.06, 'rgba(255,168,110,0.7)');
  glow.addColorStop(0.26, 'rgba(214,120,74,0.22)');
  glow.addColorStop(1, 'rgba(214,120,74,0)');
  ctx.fillStyle = glow;
  ctx.fillRect(0, 0, W, H);

  // warm band across the whole horizon
  const band = ctx.createLinearGradient(0, H * 0.4, 0, H * 0.58);
  band.addColorStop(0, 'rgba(255,180,120,0)');
  band.addColorStop(0.62, 'rgba(255,170,110,0.22)');
  band.addColorStop(1, 'rgba(255,150,90,0)');
  ctx.fillStyle = band;
  ctx.fillRect(0, H * 0.4, W, H * 0.18);

  const tex = new THREE.CanvasTexture(c);
  tex.mapping = THREE.EquirectangularReflectionMapping;
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.needsUpdate = true;
  return tex;
}

export function createEnvironment(renderer, scene) {
  const fogColor = new THREE.Color('#2b3b4c');
  scene.fog = new THREE.FogExp2(fogColor, 0.0012);
  scene.background = fogColor;

  /* env map */
  const equirect = buildEnvironmentEquirect(SUN_DIR);
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envRT = pmrem.fromEquirectangular(equirect);
  const envMap = envRT.texture;
  pmrem.dispose();
  equirect.dispose();

  /* sky dome */
  const skyUniforms = {
    uSunDir: { value: SUN_DIR.clone() },
    uZenith: { value: new THREE.Color('#03070e') },
    uHorizonWarm: { value: new THREE.Color('#a3593a') },
    uHorizonCool: { value: new THREE.Color('#3b5b78') },
    uSunColor: { value: new THREE.Color('#ff9d5e') },
    uExposure: { value: 1.0 },
  };

  const sky = new THREE.Mesh(
    new THREE.SphereGeometry(7000, 48, 24),
    new THREE.ShaderMaterial({
      vertexShader: SKY_VERT,
      fragmentShader: SKY_FRAG,
      uniforms: skyUniforms,
      side: THREE.BackSide,
      depthWrite: false,
      fog: false,
    })
  );
  sky.frustumCulled = false;
  scene.add(sky);

  /* lights */
  scene.add(new THREE.HemisphereLight(0x3d6893, 0x14100c, 0.85));

  const sun = new THREE.DirectionalLight(0xffab73, 0.85);
  sun.position.copy(SUN_DIR).multiplyScalar(900);
  scene.add(sun);

  const fill = new THREE.DirectionalLight(0x4d7eae, 0.7);
  fill.position.set(0.55, 0.4, 0.75).multiplyScalar(700);
  scene.add(fill);

  scene.add(new THREE.AmbientLight(0x16222f, 1.1));

  /* sea */
  const waterUniforms = {
    uTime: { value: 0 },
    uSunDir: { value: SUN_DIR.clone() },
    uSunColor: { value: new THREE.Color('#ffc38c') },
    uDeep: { value: new THREE.Color('#020b12') },
    uShallow: { value: new THREE.Color('#0a2230') },
    uSky: { value: new THREE.Color('#3c5872') },
    uFogColor: { value: fogColor.clone() },
    uFogDensity: { value: 0.00055 },
    uCamPos: { value: new THREE.Vector3() },
  };

  const water = new THREE.Mesh(
    new THREE.PlaneGeometry(12000, 12000, 1, 1),
    new THREE.ShaderMaterial({
      vertexShader: WATER_VERT,
      fragmentShader: WATER_FRAG,
      uniforms: waterUniforms,
      fog: false,
    })
  );
  water.rotation.x = -Math.PI / 2;
  water.position.set(0, 0, -2400);
  scene.add(water);

  /* land + beach */
  const groundTex = makeGroundTexture();
  groundTex.repeat.set(18, 12);

  const emissiveTex = makeGroundEmissive();
  emissiveTex.repeat.set(18, 12);

  const land = new THREE.Mesh(
    new THREE.PlaneGeometry(6000, 3000, 1, 1),
    new THREE.MeshStandardMaterial({
      map: groundTex,
      emissiveMap: emissiveTex,
      emissive: 0xffb066,
      emissiveIntensity: 0.28,
      color: 0x2a251f,
      roughness: 0.95,
      metalness: 0.0,
      envMap,
      envMapIntensity: 0.2,
    })
  );
  land.rotation.x = -Math.PI / 2;
  land.position.set(400, 0.4, 1500);
  scene.add(land);

  const beach = new THREE.Mesh(
    new THREE.PlaneGeometry(6000, 70, 1, 1),
    new THREE.MeshStandardMaterial({ color: 0x3a3226, roughness: 1 })
  );
  beach.rotation.x = -Math.PI / 2;
  beach.position.set(400, 0.45, 40);
  scene.add(beach);

  const update = (t, camera) => {
    waterUniforms.uTime.value = t;
    waterUniforms.uCamPos.value.copy(camera.position);
  };

  return { envMap, sun, sky, water, update, fogColor };
}

/* ------------------------------------------------------------------ *
 *  Fast hero environment
 *
 *  No PMREM, no sky shader, no water shader. A painted vertical
 *  gradient, two lights and a specular water plane give the same dusk
 *  read with one compile and a fraction of the startup cost.
 * ------------------------------------------------------------------ */
export function createFastEnvironment(renderer, scene) {
  const fogColor = new THREE.Color('#243447');
  scene.fog = new THREE.FogExp2(fogColor, 0.00115);

  const skyCanvas = document.createElement('canvas');
  skyCanvas.width = 16;
  skyCanvas.height = 512;
  const ctx = skyCanvas.getContext('2d');
  const grad = ctx.createLinearGradient(0, 0, 0, 512);
  grad.addColorStop(0, '#03070e');
  grad.addColorStop(0.42, '#15283c');
  grad.addColorStop(0.62, '#6d4e49');
  grad.addColorStop(0.74, '#ba7458');
  grad.addColorStop(1, '#1a2530');
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, 16, 512);
  const skyTex = new THREE.CanvasTexture(skyCanvas);
  skyTex.colorSpace = THREE.SRGBColorSpace;
  scene.background = skyTex;

  scene.add(new THREE.HemisphereLight(0x4f7898, 0x1a130c, 1.5));
  const sun = new THREE.DirectionalLight(0xffb079, 1.4);
  sun.position.copy(SUN_DIR).multiplyScalar(900);
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x4d7eae, 0.6);
  fill.position.set(0.55, 0.4, 0.75).multiplyScalar(700);
  scene.add(fill);

  const water = new THREE.Mesh(
    new THREE.PlaneGeometry(12000, 12000),
    new THREE.MeshPhongMaterial({ color: 0x081b27, specular: 0xffb06a, shininess: 110 })
  );
  water.rotation.x = -Math.PI / 2;
  water.position.set(0, -0.2, -2400);
  scene.add(water);

  const land = new THREE.Mesh(
    new THREE.PlaneGeometry(6000, 3000),
    new THREE.MeshLambertMaterial({ color: 0x211d18 })
  );
  land.rotation.x = -Math.PI / 2;
  land.position.set(400, 0.4, 1500);
  scene.add(land);

  return { envMap: null, sun, update() {} };
}
