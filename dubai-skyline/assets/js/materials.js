import * as THREE from 'three';

/* ------------------------------------------------------------------ *
 *  Procedural facade textures.
 *  Generated on <canvas> so the site ships with zero external images.
 *  Scale contract: one world unit ≈ 10 m, one texture tile = 8 × 12
 *  window bays, so a pane lands at roughly 2.5–3 m.
 * ------------------------------------------------------------------ */

const TEX_COLS = 16;
const TEX_ROWS = 24;

function canvas2d(w, h) {
  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  return { c, ctx: c.getContext('2d') };
}

function toTexture(canvas, srgb = true) {
  const t = new THREE.CanvasTexture(canvas);
  t.wrapS = THREE.RepeatWrapping;
  t.wrapT = THREE.RepeatWrapping;
  t.anisotropy = 8;
  if (srgb) t.colorSpace = THREE.SRGBColorSpace;
  t.needsUpdate = true;
  return t;
}

/**
 * Dark reflective glass with a tight mullion grid, plus a matching
 * emissive map holding a sparse scatter of lit interiors.
 */
export function makeFacadeTextures({
  litRatio = 0.16,
  mullion = '#05080b',
  warm = '#ffb877',
  cool = '#dfe9f5',
  tint = [12, 24, 34],
} = {}) {
  const W = 512;
  const H = 768;
  const { c: colorCanvas, ctx } = canvas2d(W, H);
  const { c: emCanvas, ctx: ex } = canvas2d(W, H);

  ctx.fillStyle = mullion;
  ctx.fillRect(0, 0, W, H);
  ex.fillStyle = '#000';
  ex.fillRect(0, 0, W, H);

  const pw = W / TEX_COLS;
  const ph = H / TEX_ROWS;
  const gap = 1.4;

  for (let y = 0; y < TEX_ROWS; y++) {
    for (let x = 0; x < TEX_COLS; x++) {
      const jitter = ((x * 13 + y * 7) % 9) / 9;
      const r = tint[0] + jitter * 14;
      const g = tint[1] + jitter * 18;
      const b = tint[2] + jitter * 24;
      ctx.fillStyle = `rgb(${r | 0},${g | 0},${b | 0})`;
      ctx.fillRect(x * pw + gap, y * ph + gap, pw - gap * 2, ph - gap * 2);

      // glass picks up a slice of sky: bright top edge, dark floor
      const grad = ctx.createLinearGradient(0, y * ph, 0, (y + 1) * ph);
      grad.addColorStop(0, 'rgba(148,182,208,0.34)');
      grad.addColorStop(0.35, 'rgba(86,120,150,0.14)');
      grad.addColorStop(1, 'rgba(0,0,0,0.5)');
      ctx.fillStyle = grad;
      ctx.fillRect(x * pw + gap, y * ph + gap, pw - gap * 2, ph - gap * 2);
    }
  }

  // Occupancy: whole floors light up, not isolated panes. This is what
  // separates a believable office tower from a random dot grid.
  for (let y = 0; y < TEX_ROWS; y++) {
    if (Math.random() > litRatio * 2.6) continue;
    const runStart = Math.floor(Math.random() * TEX_COLS);
    const runLen = 1 + Math.floor(Math.random() * 5);
    const brightness = 0.35 + Math.random() * 0.65;
    const useCool = Math.random() < 0.18;

    for (let i = 0; i < runLen; i++) {
      const x = (runStart + i) % TEX_COLS;
      ex.globalAlpha = brightness * (0.6 + Math.random() * 0.4);
      ex.fillStyle = useCool ? cool : warm;
      const inset = gap + 1.2;
      ex.fillRect(x * pw + inset, y * ph + inset, pw - inset * 2, ph - inset * 2);
    }

  }

  ctx.fillStyle = 'rgba(200,222,240,0.10)';
  for (let y = 0; y < TEX_ROWS; y++) ctx.fillRect(0, y * ph, W, 1.2);
  ex.globalAlpha = 1;

  return {
    map: toTexture(colorCanvas),
    emissiveMap: toTexture(emCanvas),
  };
}

/** Vertical fins + dense floors — Burj Khalifa and the supertalls. */
export function makeFinnedTextures({ litRatio = 0.1 } = {}) {
  const W = 512;
  const H = 768;
  const { c, ctx } = canvas2d(W, H);
  const { c: e, ctx: ex } = canvas2d(W, H);

  ctx.fillStyle = '#06090c';
  ctx.fillRect(0, 0, W, H);
  ex.fillStyle = '#000';
  ex.fillRect(0, 0, W, H);

  const bays = 20;
  const floors = 30;
  for (let x = 0; x < bays; x++) {
    const g = ctx.createLinearGradient(x * (W / bays), 0, (x + 1) * (W / bays), 0);
    g.addColorStop(0, '#0a1219');
    g.addColorStop(0.3, '#41606f');
    g.addColorStop(0.5, '#9dc0ce');
    g.addColorStop(0.68, '#2f4a57');
    g.addColorStop(1, '#080f14');
    ctx.fillStyle = g;
    ctx.fillRect(x * (W / bays), 0, W / bays - 1, H);
  }

  ctx.fillStyle = 'rgba(0,0,0,0.55)';
  for (let y = 0; y < floors; y++) ctx.fillRect(0, y * (H / floors), W, 1.6);

  for (let x = 0; x < bays; x++) {
    for (let y = 0; y < floors; y++) {
      if (Math.random() > litRatio) continue;
      ex.globalAlpha = 0.3 + Math.random() * 0.7;
      ex.fillStyle = '#ffd0a0';
      ex.fillRect(x * (W / bays) + 2, y * (H / floors) + 2, W / bays - 5, H / floors - 3.5);
    }
  }
  ex.globalAlpha = 1;

  return { map: toTexture(c), emissiveMap: toTexture(e) };
}

/** Soft radial blob used as a cheap contact shadow under landmarks. */
export function makeShadowTexture() {
  const S = 256;
  const { c, ctx } = canvas2d(S, S);
  const g = ctx.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
  g.addColorStop(0, 'rgba(0,0,0,0.6)');
  g.addColorStop(0.5, 'rgba(0,0,0,0.28)');
  g.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, S, S);
  return toTexture(c, false);
}

/** Ground: dark city fabric with faint blocks and road seams. */
export function makeGroundTexture() {
  const S = 1024;
  const { c, ctx } = canvas2d(S, S);
  ctx.fillStyle = '#191612';
  ctx.fillRect(0, 0, S, S);

  for (let i = 0; i < 900; i++) {
    const x = Math.random() * S;
    const y = Math.random() * S;
    const w = 10 + Math.random() * 60;
    const h = 10 + Math.random() * 60;
    ctx.fillStyle = `rgba(${40 + Math.random() * 30},${36 + Math.random() * 26},${30 + Math.random() * 22},0.5)`;
    ctx.fillRect(x, y, w, h);
  }

  ctx.strokeStyle = 'rgba(120,104,84,0.20)';
  ctx.lineWidth = 2;
  for (let i = 0; i <= 8; i++) {
    ctx.beginPath();
    ctx.moveTo((i * S) / 8, 0);
    ctx.lineTo((i * S) / 8, S);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, (i * S) / 8);
    ctx.lineTo(S, (i * S) / 8);
    ctx.stroke();
  }

  const t = toTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(14, 10);
  return t;
}

/**
 * Scales UVs so one texture tile covers `tile` world units.
 * 8 bays × 0.28 ≈ 2.2 units → ~2.8 m per bay at 1 unit = 10 m.
 */
export function applyFacadeUV(geometry, width, height, bay = 0.3) {
  const uv = geometry.attributes.uv;
  if (!uv) return geometry;
  const su = Math.max(1, (width / (bay * TEX_COLS)));
  const sv = Math.max(1, (height / (bay * TEX_ROWS)));
  for (let i = 0; i < uv.count; i++) {
    uv.setXY(i, uv.getX(i) * su, uv.getY(i) * sv);
  }
  uv.needsUpdate = true;
  return geometry;
}

/* ------------------------------------------------------------------ *
 *  Materials
 * ------------------------------------------------------------------ */

export function createMaterials(envMap, shadowTexture, groundTexture) {
  const glass = makeFacadeTextures({ litRatio: 0.17, tint: [11, 22, 31] });
  const silverGlass = makeFacadeTextures({
    litRatio: 0.12,
    tint: [22, 36, 46],
    mullion: '#060a0e',
  });
  const warmGlass = makeFacadeTextures({
    litRatio: 0.2,
    tint: [26, 21, 16],
    mullion: '#070605',
  });
  const coolGlass = makeFacadeTextures({
    litRatio: 0.1,
    tint: [16, 30, 42],
    warm: '#dfeaf6',
    mullion: '#04070a',
  });
  const dimGlass = makeFacadeTextures({
    litRatio: 0.035,
    tint: [10, 18, 25],
    mullion: '#04070a',
  });
  const fins = makeFinnedTextures({ litRatio: 0.15 });

  const base = { envMap, envMapIntensity: 2.1 };

  const materials = {
    glass: new THREE.MeshStandardMaterial({
      ...base,
      color: 0x4d6579,
      map: glass.map,
      emissiveMap: glass.emissiveMap,
      emissive: 0xffc07a,
      emissiveIntensity: 0.95,
      metalness: 0.72,
      roughness: 0.14,
    }),
    silver: new THREE.MeshStandardMaterial({
      ...base,
      color: 0xa9bcc7,
      map: silverGlass.map,
      emissiveMap: silverGlass.emissiveMap,
      emissive: 0xffd2a4,
      emissiveIntensity: 0.75,
      metalness: 0.96,
      roughness: 0.12,
    }),
    bronze: new THREE.MeshStandardMaterial({
      ...base,
      color: 0xb08a5a,
      map: warmGlass.map,
      emissiveMap: warmGlass.emissiveMap,
      emissive: 0xffb673,
      emissiveIntensity: 0.8,
      metalness: 0.85,
      roughness: 0.18,
    }),
    finned: new THREE.MeshStandardMaterial({
      ...base,
      color: 0xc3d4de,
      map: fins.map,
      emissiveMap: fins.emissiveMap,
      emissive: 0xffd7ad,
      emissiveIntensity: 0.9,
      metalness: 0.92,
      roughness: 0.09,
      envMapIntensity: 1.8,
    }),
    glassCool: new THREE.MeshStandardMaterial({
      ...base,
      color: 0x54708a,
      map: coolGlass.map,
      emissiveMap: coolGlass.emissiveMap,
      emissive: 0xdce9f6,
      emissiveIntensity: 0.75,
      metalness: 0.8,
      roughness: 0.12,
    }),
    glassDim: new THREE.MeshStandardMaterial({
      ...base,
      color: 0x33495c,
      map: dimGlass.map,
      emissiveMap: dimGlass.emissiveMap,
      emissive: 0xffb877,
      emissiveIntensity: 0.5,
      metalness: 0.85,
      roughness: 0.16,
    }),
    stone: new THREE.MeshStandardMaterial({
      envMap,
      envMapIntensity: 0.5,
      color: 0x8f8574,
      roughness: 0.9,
      metalness: 0.05,
    }),
    lightStone: new THREE.MeshStandardMaterial({
      envMap,
      envMapIntensity: 0.6,
      color: 0xcfc3ae,
      roughness: 0.85,
      metalness: 0.04,
    }),
    darkMetal: new THREE.MeshStandardMaterial({
      envMap,
      envMapIntensity: 1.4,
      color: 0x22282e,
      roughness: 0.35,
      metalness: 0.9,
    }),
    gold: new THREE.MeshStandardMaterial({
      envMap,
      envMapIntensity: 2.0,
      color: 0xb8894a,
      roughness: 0.24,
      metalness: 1.0,
    }),
    white: new THREE.MeshStandardMaterial({
      envMap,
      envMapIntensity: 1.0,
      color: 0xe9e4da,
      roughness: 0.5,
      metalness: 0.1,
    }),
    sand: new THREE.MeshStandardMaterial({
      color: 0x8c7a5e,
      roughness: 1,
      metalness: 0,
    }),
    shadow: new THREE.MeshBasicMaterial({
      map: shadowTexture,
      transparent: true,
      opacity: 0.7,
      depthWrite: false,
    }),
  };

  materials.envMap = envMap;
  return materials;
}


/** Sparse warm street lights for the ground plane's emissive channel. */
export function makeGroundEmissive() {
  const S = 1024;
  const { c, ctx } = canvas2d(S, S);
  ctx.fillStyle = '#000';
  ctx.fillRect(0, 0, S, S);

  const grid = 8;
  const cell = S / grid;

  for (let gx = 0; gx < grid; gx++) {
    for (let gy = 0; gy < grid; gy++) {
      // street lights along the seams
      if (Math.random() < 0.5) {
        const x = gx * cell + cell / 2;
        const y = gy * cell + cell / 2;
        const grd = ctx.createRadialGradient(x, y, 0, x, y, cell * 0.3);
        grd.addColorStop(0, 'rgba(255,186,112,0.85)');
        grd.addColorStop(1, 'rgba(255,150,80,0)');
        ctx.fillStyle = grd;
        ctx.fillRect(x - cell * 0.3, y - cell * 0.3, cell * 0.6, cell * 0.6);
      }
      // a few lit blocks
      if (Math.random() < 0.12) {
        ctx.fillStyle = 'rgba(255,196,130,0.35)';
        ctx.fillRect(gx * cell + 8, gy * cell + 8, cell * 0.28, cell * 0.28);
      }
    }
  }

  const t = toTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  return t;
}

/* ------------------------------------------------------------------ *
 *  Fast hero materials
 *
 *  The full portfolio uses six facade sets and image-based lighting.
 *  For first paint we only need the same silhouettes with one shared
 *  window atlas and a handful of Lambert programs. This keeps the hero
 *  recognisably Dubai while cutting shader compilation and texture
 *  uploads to a minimum.
 * ------------------------------------------------------------------ */
export function createFastMaterials() {
  const facade = makeFacadeTextures({ litRatio: 0.2, tint: [13, 26, 38] });
  const fins = makeFinnedTextures({ litRatio: 0.2 });

  const mapped = (color, emissiveIntensity = 0.9, mapSet = facade) =>
    new THREE.MeshLambertMaterial({
      color,
      map: mapSet.map,
      emissive: 0xffc07a,
      emissiveMap: mapSet.emissiveMap,
      emissiveIntensity,
    });

  const materials = {
    glass: mapped(0x6f879b),
    silver: mapped(0xb7c8d2, 0.8),
    bronze: mapped(0xa9825c, 0.95),
    finned: mapped(0xd2dde3, 1.0, fins),
    glassCool: mapped(0x7e9bad, 0.8),
    glassDim: mapped(0x4c6172, 0.55),
    stone: new THREE.MeshLambertMaterial({ color: 0x8f8574 }),
    lightStone: new THREE.MeshLambertMaterial({ color: 0xcfc3ae }),
    darkMetal: new THREE.MeshLambertMaterial({ color: 0x2a3138 }),
    gold: new THREE.MeshLambertMaterial({ color: 0xb8894a, emissive: 0x3a230e, emissiveIntensity: 0.4 }),
    white: new THREE.MeshLambertMaterial({ color: 0xe9e4da }),
    sand: new THREE.MeshLambertMaterial({ color: 0x8c7a5e }),
    envMap: null,
    shadow: new THREE.MeshBasicMaterial({
      map: makeShadowTexture(),
      transparent: true,
      opacity: 0.7,
      depthWrite: false,
    }),
  };

  return materials;
}
