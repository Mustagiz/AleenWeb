import * as THREE from 'three';
import { applyFacadeUV } from './materials.js';

/* ------------------------------------------------------------------ *
 *  Procedural Dubai. All geometry is generated at runtime — no GLTF,
 *  no external assets, nothing to download but this file.
 * ------------------------------------------------------------------ */

const V = THREE.Vector3;

/** Box tower with taper, twist and a gentle bend. */
function towerGeometry({
  w = 8,
  d = 8,
  h = 20,
  taper = 0.9,
  twist = 0,
  bend = 0,
  segments = 12,
} = {}) {
  const g = new THREE.BoxGeometry(w, h, d, 2, segments, 2);
  g.translate(0, h / 2, 0);
  const p = g.attributes.position;

  for (let i = 0; i < p.count; i++) {
    const y = p.getY(i);
    const t = THREE.MathUtils.clamp(y / h, 0, 1);
    const s = 1 - (1 - taper) * Math.pow(t, 1.3);
    const x = p.getX(i) * s;
    const z = p.getZ(i) * s;
    const a = twist * t;
    const ca = Math.cos(a);
    const sa = Math.sin(a);
    p.setXYZ(i, x * ca - z * sa + bend * t * t, y, x * sa + z * ca);
  }

  p.needsUpdate = true;
  g.computeVertexNormals();
  applyFacadeUV(g, w, h, 0.3);
  return g;
}

function mesh(geo, mat, x, z, rotY = 0) {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(x, 0, z);
  m.rotation.y = rotY;
  m.matrixAutoUpdate = false;
  m.updateMatrix();
  return m;
}

function shadow(group, mat, x, z, size) {
  const s = new THREE.Mesh(new THREE.PlaneGeometry(size, size), mat);
  s.rotation.x = -Math.PI / 2;
  s.position.set(x, 0.5, z);
  s.renderOrder = 1;
  group.add(s);
}

/** Aircraft warning light — tiny emissive sphere. */
function beacon(group, x, y, z, color = 0xff3b2f, r = 0.28) {
  const m = new THREE.Mesh(
    new THREE.SphereGeometry(r, 8, 6),
    new THREE.MeshBasicMaterial({ color })
  );
  m.position.set(x, y, z);
  group.add(m);
}

/* ------------------------------------------------------------------ *
 *  Landmarks
 * ------------------------------------------------------------------ */

function burjKhalifa(mats, shadowMat) {
  const g = new THREE.Group();
  g.name = 'burj-khalifa';
  const H = 118;

  // Y-plan massing: three wings per tier, each tier stepping back.
  // The height is exaggerated against the background city on purpose:
  // in the hero frame the Burj has to read as the tallest thing on earth.
  const tiers = [
    { y: 0, h: 37, r: 5.9, w: 4.4, d: 2.0 },
    { y: 37, h: 22, r: 5.1, w: 3.9, d: 1.8 },
    { y: 59, h: 17, r: 4.3, w: 3.4, d: 1.6 },
    { y: 76, h: 12, r: 3.5, w: 2.8, d: 1.35 },
    { y: 88, h: 9, r: 2.8, w: 2.2, d: 1.1 },
  ];

  for (const t of tiers) {
    for (let i = 0; i < 3; i++) {
      const a = (i / 3) * Math.PI * 2 + 0.28;
      const geo = towerGeometry({
        w: t.w,
        d: t.d,
        h: t.h,
        taper: 0.8,
        twist: 0.05,
        segments: 8,
      });
      const wing = new THREE.Mesh(geo, mats.finned);
      wing.position.set(Math.cos(a) * t.r, t.y, Math.sin(a) * t.r);
      wing.rotation.y = Math.PI / 2 - a;
      g.add(wing);
    }

    // central core and a sky-lobby slab at the setback
    const core = new THREE.Mesh(
      new THREE.CylinderGeometry(t.r * 0.5, t.r * 0.58, t.h, 12, 1),
      mats.silver
    );
    core.position.y = t.y + t.h / 2;
    g.add(core);

    const slab = new THREE.Mesh(
      new THREE.CylinderGeometry(t.r + 1.1, t.r + 1.1, 0.3, 3, 1),
      mats.silver
    );
    slab.rotation.y = Math.PI / 6;
    slab.position.y = t.y + t.h;
    g.add(slab);
  }

  // spire — stepped mast, tapering to a needle
  const spireBase = 97;
  const spireH = H - spireBase;
  const spire = new THREE.Mesh(
    new THREE.CylinderGeometry(0.14, 1.25, spireH, 8, 1),
    mats.silver
  );
  spire.position.y = spireBase + spireH / 2;
  g.add(spire);

  const collar = new THREE.Mesh(
    new THREE.CylinderGeometry(1.35, 1.85, 1.2, 8, 1),
    mats.silver
  );
  collar.position.y = spireBase + 0.3;
  g.add(collar);

  const tip = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.12, 9, 4), mats.darkMetal);
  tip.position.y = H + 4.1;
  g.add(tip);

  // Crown lighting: a warm ring just below the spire and a pulse at the
  // very top. Small, emissive details read as scale at hero distance.
  const crown = new THREE.Mesh(
    new THREE.CylinderGeometry(2.1, 2.35, 0.22, 18, 1, true),
    new THREE.MeshBasicMaterial({
      color: 0xffd7a8,
      transparent: true,
      opacity: 0.6,
      side: THREE.DoubleSide,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
    })
  );
  crown.position.y = 96.9;
  g.add(crown);

  beacon(g, 0, H + 8.2, 0, 0xff3a2a, 0.34);
  beacon(g, 0, 40, 0, 0xff3a2a, 0.14);

  g.userData.landmarkTop = H + 8.2;
  g.position.set(-48, 0, 58);
  shadow(g, shadowMat, -48, 58, 44);
  return g;
}

/** Quay wall, promenade lights and a lit shoreline — grounds the skyline. */
function waterfront(mats) {
  const g = new THREE.Group();

  const quay = new THREE.Mesh(new THREE.BoxGeometry(1400, 2.6, 9), mats.lightStone);
  quay.position.set(120, 1.0, 12);
  g.add(quay);

  const promenade = new THREE.Mesh(
    new THREE.BoxGeometry(1400, 0.12, 5),
    new THREE.MeshBasicMaterial({ color: 0x3a2a1c })
  );
  promenade.position.set(120, 2.35, 12);
  g.add(promenade);

  const lampGeo = new THREE.SphereGeometry(0.16, 6, 5);
  const lampMat = new THREE.MeshBasicMaterial({ color: 0xffd2a0 });
  const lamps = new THREE.InstancedMesh(lampGeo, lampMat, 180);
  const d = new THREE.Object3D();
  for (let i = 0; i < 180; i++) {
    d.position.set(-560 + i * 7.6, 2.7, 10.4 + (i % 2) * 3.2);
    d.updateMatrix();
    lamps.setMatrixAt(i, d.matrix);
  }
  lamps.instanceMatrix.needsUpdate = true;
  g.add(lamps);

  return g;
}

function emiratesTowers(mats, shadowMat) {
  const g = new THREE.Group();
  const specs = [
    { x: -8, z: 88, h: 38, w: 9 },
    { x: 7, z: 107, h: 33, w: 8.5 },
  ];
  for (const s of specs) {
    const geo = new THREE.CylinderGeometry(s.w * 0.62, s.w * 0.86, s.h, 3, 1);
    geo.rotateY(Math.PI / 2);
    geo.translate(0, s.h / 2, 0);
    applyFacadeUV(geo, s.w * 3, s.h, 0.3);
    g.add(mesh(geo, mats.silver, s.x, s.z, 0.2));

    const crown = new THREE.Mesh(
      new THREE.CylinderGeometry(0.4, s.w * 0.55, 2.4, 3, 1),
      mats.silver
    );
    crown.rotation.y = Math.PI / 2;
    crown.position.set(s.x, s.h + 1.2, s.z);
    g.add(crown);
    beacon(g, s.x, s.h + 2.6, s.z, 0xff4a3a, 0.16);
  }
  shadow(g, shadowMat, -1, 97, 44);
  return g;
}

function museumOfFuture(mats, shadowMat) {
  const g = new THREE.Group();

  const mound = new THREE.Mesh(new THREE.SphereGeometry(7.6, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2), mats.stone);
  mound.scale.set(1.2, 0.3, 1);
  mound.position.set(22, 0.4, 48);
  g.add(mound);

  const ringGeo = new THREE.TorusGeometry(5.6, 2.5, 20, 64);
  applyFacadeUV(ringGeo, 40, 20, 0.32);
  const ring = new THREE.Mesh(ringGeo, mats.silver);
  ring.position.set(22, 7.4, 48);
  ring.rotation.y = -0.55;
  ring.rotation.z = 0.04;
  g.add(ring);

  // green inner glow
  const inner = new THREE.Mesh(
    new THREE.TorusGeometry(3.9, 0.1, 6, 64),
    new THREE.MeshBasicMaterial({ color: 0x63d9a0 })
  );
  inner.position.copy(ring.position);
  inner.rotation.copy(ring.rotation);
  g.add(inner);

  shadow(g, shadowMat, 22, 48, 34);
  return g;
}

function dubaiFrame(mats, shadowMat) {
  const g = new THREE.Group();
  const H = 15;
  const legGeo = new THREE.BoxGeometry(3.4, H, 1.6);
  applyFacadeUV(legGeo, 3.4, H, 0.3);

  for (const dx of [-6.4, 6.4]) {
    const leg = new THREE.Mesh(legGeo, mats.gold);
    leg.position.set(-96 + dx, H / 2, 30);
    g.add(leg);
  }

  const bridge = new THREE.Mesh(new THREE.BoxGeometry(16, 2.6, 2.2), mats.gold);
  bridge.position.set(-96, H - 1.2, 30);
  g.add(bridge);

  const glass = new THREE.Mesh(
    new THREE.BoxGeometry(15.6, 2.2, 0.1),
    new THREE.MeshStandardMaterial({
      color: 0x9fc0d4,
      metalness: 1,
      roughness: 0.05,
      envMap: mats.envMap,
      envMapIntensity: 2,
      transparent: true,
      opacity: 0.55,
    })
  );
  glass.position.set(-96, H - 1.2, 31.15);
  g.add(glass);

  shadow(g, shadowMat, -96, 30, 26);
  return g;
}

function cayanTower(mats, shadowMat) {
  const g = new THREE.Group();
  const H = 31;
  const geo = towerGeometry({
    w: 9.6,
    d: 9.6,
    h: H,
    taper: 0.99,
    twist: Math.PI / 2,
    segments: 60,
  });
  const m = new THREE.Mesh(geo, mats.glass);
  m.position.set(108, 0, 26);
  g.add(m);

  const cap = new THREE.Mesh(new THREE.BoxGeometry(9.2, 0.8, 9.2), mats.white);
  cap.position.set(108, H + 0.3, 26);
  cap.rotation.y = Math.PI / 2;
  g.add(cap);

  shadow(g, shadowMat, 108, 26, 30);
  return g;
}

function marinaTowers(mats, shadowMat) {
  const g = new THREE.Group();
  const specs = [
    [74, 44, 26, 8.4, 0.12, 0],
    [86, 62, 21, 7.6, -0.2, 0.12],
    [96, 14, 29, 9.2, 0.35, 0],
    [120, 58, 24, 8.0, 0, 0.22],
    [128, 24, 32, 9.8, -0.3, 0],
    [140, 66, 19, 7.2, 0.18, 0],
    [156, 40, 27, 8.8, 0, -0.16],
    [66, 12, 17, 7.0, 0.4, 0],
  ];

  for (const [x, z, h, w, twist, bend] of specs) {
    const geo = towerGeometry({ w, d: w * 0.86, h, taper: 0.93, twist, bend, segments: 26 });
    g.add(mesh(geo, twist ? mats.silver : mats.glass, x, z, x * 0.05));

    const roof = new THREE.Mesh(new THREE.BoxGeometry(w * 0.5, 1.2, w * 0.4), mats.darkMetal);
    roof.position.set(x, h + 0.5, z);
    roof.rotation.y = x * 0.05;
    g.add(roof);

    if (h > 26) beacon(g, x, h + 1.6, z, 0xff4a3a, 0.16);
  }

  shadow(g, shadowMat, 108, 40, 96);
  return g;
}

function ainDubai(mats) {
  const g = new THREE.Group();
  const R = 12.4;
  const cx = 150;
  const cz = 6;
  const cy = 15.5;

  const rim = new THREE.Mesh(new THREE.TorusGeometry(R, 0.32, 8, 72), mats.white);
  rim.position.set(cx, cy, cz);
  rim.rotation.y = -0.4;
  g.add(rim);

  const rimInner = new THREE.Mesh(new THREE.TorusGeometry(R - 1.1, 0.1, 6, 72), mats.darkMetal);
  rimInner.position.copy(rim.position);
  rimInner.rotation.copy(rim.rotation);
  g.add(rimInner);

  const spokeGeoC = new THREE.CylinderGeometry(0.07, 0.07, R, 4);
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2;
    const spoke = new THREE.Mesh(spokeGeoC, mats.darkMetal);
    spoke.position.set(cx + Math.cos(a) * R * 0.5, cy + Math.sin(a) * R * 0.5, cz);
    spoke.rotation.z = a + Math.PI / 2;
    spoke.rotation.y = -0.4;
    g.add(spoke);
  }

  // passenger capsules
  const capGeo = new THREE.BoxGeometry(1.5, 1.5, 1.5);
  const capMat = new THREE.MeshStandardMaterial({
    color: 0xbcd6e4,
    metalness: 0.6,
    roughness: 0.1,
    envMap: mats.envMap,
    envMapIntensity: 1.6,
  });
  for (let i = 0; i < 16; i++) {
    const a = (i / 16) * Math.PI * 2;
    const cap = new THREE.Mesh(capGeo, capMat);
    cap.position.set(cx + Math.cos(a) * R, cy + Math.sin(a) * R, cz);
    cap.rotation.z = a;
    g.add(cap);
  }

  // A-frame legs
  for (const side of [-1, 1]) {
    const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 1.0, cy + 1, 8), mats.white);
    leg.position.set(cx + side * 6.4, cy / 2, cz);
    leg.rotation.z = side * 0.24;
    g.add(leg);
  }

  const hub = new THREE.Mesh(new THREE.SphereGeometry(1.1, 16, 12), mats.darkMetal);
  hub.position.set(cx, cy, cz);
  g.add(hub);

  const island = new THREE.Mesh(new THREE.CylinderGeometry(13, 14, 1.4, 28), mats.sand);
  island.position.set(cx, 0.3, cz);
  g.add(island);

  const base = new THREE.Mesh(new THREE.CylinderGeometry(8, 9, 1.2, 24), mats.lightStone);
  base.position.set(cx, 1.1, cz);
  g.add(base);

  return g;
}

function burjAlArab(mats, shadowMat) {
  const g = new THREE.Group();
  const X = 205;
  const Z = -58;
  const H = 32;
  const W = 13.5;

  // island
  const island = new THREE.Mesh(new THREE.CylinderGeometry(23, 25, 1.6, 40), mats.sand);
  island.position.set(X, 0.2, Z);
  g.add(island);

  // causeway
  const causeway = new THREE.Mesh(new THREE.BoxGeometry(4, 1.1, 130), mats.lightStone);
  causeway.position.set(X, 0.5, Z + 66);
  g.add(causeway);

  // sail
  const shape = new THREE.Shape();
  shape.moveTo(0, 0);
  shape.lineTo(0, H * 0.93);
  shape.bezierCurveTo(W * 0.12, H * 1.0, W * 0.82, H * 0.79, W * 0.96, H * 0.33);
  shape.bezierCurveTo(W * 1.0, H * 0.17, W * 0.6, H * 0.02, W * 0.44, 0);
  shape.lineTo(0, 0);

  const sailGeo = new THREE.ExtrudeGeometry(shape, {
    depth: 1.5,
    bevelEnabled: true,
    bevelThickness: 0.25,
    bevelSize: 0.25,
    bevelSegments: 2,
    curveSegments: 24,
  });
  sailGeo.translate(-W * 0.42, 0, -0.75);
  applyFacadeUV(sailGeo, W, H, 0.34);

  const sail = new THREE.Mesh(sailGeo, mats.silver);
  sail.position.set(X, 1.6, Z);
  sail.rotation.y = -0.62;
  g.add(sail);

  // glass front strip
  const strip = new THREE.Mesh(
    new THREE.BoxGeometry(0.4, H * 0.78, 7.2),
    new THREE.MeshStandardMaterial({
      color: 0x6f9bb4,
      metalness: 1,
      roughness: 0.06,
      envMap: mats.envMap,
      envMapIntensity: 2.2,
    })
  );
  strip.position.set(X + 5.2, H * 0.45, Z);
  strip.rotation.y = -0.62;
  g.add(strip);

  // helipad
  const heli = new THREE.Mesh(new THREE.CylinderGeometry(3.4, 3.4, 0.5, 28), mats.white);
  heli.position.set(X - 6.2, H * 0.7, Z + 2.6);
  heli.rotation.y = -0.62;
  g.add(heli);
  const heliRing = new THREE.Mesh(new THREE.TorusGeometry(3.4, 0.12, 6, 32), mats.darkMetal);
  heliRing.position.copy(heli.position);
  heliRing.rotation.x = Math.PI / 2;
  g.add(heliRing);

  // mast
  const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.16, 8, 6), mats.white);
  mast.position.set(X - 8.4, H + 4.4, Z + 1.4);
  g.add(mast);
  beacon(g, X - 8.4, H + 8.6, Z + 1.4, 0xff4a3a, 0.16);

  shadow(g, shadowMat, X, Z, 62);
  return g;
}

function palmIsland(mats) {
  const g = new THREE.Group();

  // stylised Palm Jumeirah: trunk, crown, fronds
  const trunk = new THREE.Mesh(new THREE.BoxGeometry(9, 1.4, 70), mats.sand);
  trunk.position.set(250, 0.3, 40);
  g.add(trunk);

  const crown = new THREE.Mesh(new THREE.CylinderGeometry(30, 30, 1.3, 32), mats.sand);
  crown.position.set(250, 0.3, -32);
  g.add(crown);

  const frondGeo = new THREE.BoxGeometry(3.2, 1.2, 26);
  for (let i = 0; i < 12; i++) {
    const side = i % 2 === 0 ? 1 : -1;
    const row = Math.floor(i / 2);
    const f = new THREE.Mesh(frondGeo, mats.sand);
    f.position.set(250 + side * (11 + row * 2.4), 0.3, -30 - row * 7.5);
    f.rotation.y = side * (0.55 + row * 0.04);
    g.add(f);
  }

  // low-rise villas
  const villa = new THREE.BoxGeometry(2.2, 2.0, 2.2);
  const villaMat = new THREE.MeshStandardMaterial({
    color: 0xd9cdb8,
    roughness: 0.85,
    envMap: mats.envMap,
    envMapIntensity: 0.4,
  });
  for (let i = 0; i < 90; i++) {
    const m = new THREE.Mesh(villa, villaMat);
    const a = Math.random() * Math.PI * 2;
    const r = 6 + Math.random() * 22;
    m.position.set(250 + Math.cos(a) * r, 1.1, -32 + Math.sin(a) * r * 0.9);
    m.rotation.y = Math.random() * Math.PI;
    g.add(m);
  }

  return g;
}

function yachts(mats) {
  const g = new THREE.Group();
  const hull = new THREE.BoxGeometry(3.4, 1.1, 1.2);
  const cabin = new THREE.BoxGeometry(1.6, 0.8, 1.0);
  const white = new THREE.MeshStandardMaterial({ color: 0xf4f1ea, roughness: 0.4, metalness: 0.1 });
  const glassM = new THREE.MeshStandardMaterial({
    color: 0x2b3f4a,
    metalness: 0.9,
    roughness: 0.1,
    envMap: mats.envMap,
    envMapIntensity: 1.4,
  });

  const spots = [
    [96, -34, 0.4],
    [122, -52, -0.7],
    [140, -78, 0.2],
    [58, -60, 1.2],
    [176, -30, -0.3],
  ];

  for (const [x, z, r] of spots) {
    const y = new THREE.Group();
    const h = new THREE.Mesh(hull, white);
    y.add(h);
    const c = new THREE.Mesh(cabin, glassM);
    c.position.set(-0.4, 0.8, 0);
    y.add(c);
    y.position.set(x, 0.35, z);
    y.rotation.y = r;
    g.add(y);
  }
  return g;
}

/* ------------------------------------------------------------------ *
 *  Background city — three instanced meshes keep draw calls flat.
 * ------------------------------------------------------------------ */

function backgroundCity(mats, exclusions) {
  const group = new THREE.Group();

  const variants = [
    { h: 7, w: 5.0, count: 80, mat: mats.glassDim },
    { h: 14, w: 6.4, count: 90, mat: mats.glass },
    { h: 26, w: 7.6, count: 64, mat: mats.silver },
    { h: 46, w: 8.8, count: 30, mat: mats.glassCool },
  ];

  // built-up clusters, not an even carpet: leaves gaps and streets
  const clusters = [
    { x: -110, z: 95, r: 95, share: 0.24 },
    { x: -20, z: 150, r: 90, share: 0.2 },
    { x: 95, z: 55, r: 75, share: 0.2 },
    { x: 175, z: 120, r: 85, share: 0.12 },
    { x: -330, z: 240, r: 120, share: 0.12 },
    { x: 330, z: 260, r: 130, share: 0.12 },
  ];

  const dummy = new THREE.Object3D();
  const color = new THREE.Color();

  for (const v of variants) {
    const geo = new THREE.BoxGeometry(v.w, v.h, v.w * 0.92, 1, 1, 1);
    geo.translate(0, v.h / 2, 0);
    applyFacadeUV(geo, v.w, v.h, 0.3);

    const inst = new THREE.InstancedMesh(geo, v.mat, v.count);
    inst.instanceMatrix.setUsage(THREE.DynamicDrawUsage);

    let placed = 0;
    let guard = 0;
    while (placed < v.count && guard < v.count * 60) {
      guard++;
      const pick = Math.random();
      let acc = 0;
      let c = clusters[0];
      for (const cl of clusters) {
        acc += cl.share;
        if (pick <= acc) { c = cl; break; }
      }

      // gaussian-ish scatter inside the cluster
      const a = Math.random() * Math.PI * 2;
      const rr = Math.pow(Math.random(), 0.65) * c.r;
      const x = c.x + Math.cos(a) * rr;
      const z = c.z + Math.sin(a) * rr * 0.85;

      let blocked = false;
      for (const e of exclusions) {
        if (Math.hypot(x - e.x, z - e.z) < e.r) { blocked = true; break; }
      }
      if (blocked) continue;

      dummy.position.set(x, 0.35, z);
      dummy.rotation.y = Math.random() * Math.PI;
      dummy.scale.set(
        0.75 + Math.random() * 1.15,
        0.55 + Math.random() * 1.7,
        0.75 + Math.random() * 1.15
      );
      dummy.updateMatrix();
      inst.setMatrixAt(placed, dummy.matrix);

      const shade = 0.5 + Math.random() * 0.6;
      color.setRGB(shade, shade * 0.97, shade * 0.95);
      inst.setColorAt(placed, color);
      placed++;
    }
    inst.count = placed;
    inst.instanceMatrix.needsUpdate = true;
    if (inst.instanceColor) inst.instanceColor.needsUpdate = true;
    group.add(inst);
  }

  return group;
}

/* ------------------------------------------------------------------ *
 *  Assembly
 * ------------------------------------------------------------------ */

export function buildCity(mats, shadowMat) {
  const group = new THREE.Group();

  const exclusions = [
    { x: -48, z: 58, r: 34 },   // burj
    { x: 0, z: 97, r: 30 },     // emirates
    { x: 22, z: 48, r: 18 },    // museum
    { x: -96, z: 30, r: 16 },   // frame
    { x: 108, z: 26, r: 20 },   // cayan
    { x: 150, z: -14, r: 22 },  // ain dubai
    { x: 205, z: -58, r: 40 },  // burj al arab
    { x: 250, z: -10, r: 46 },  // palm
  ];

  group.add(backgroundCity(mats, exclusions));

  const burj = burjKhalifa(mats, shadowMat);
  group.userData.landmark = burj;
  group.userData.landmarkWorld = new THREE.Vector3(-48, burj.userData.landmarkTop, 58);

  group.add(waterfront(mats));
  group.add(burj);
  group.add(emiratesTowers(mats, shadowMat));
  group.add(museumOfFuture(mats, shadowMat));
  group.add(dubaiFrame(mats, shadowMat));
  group.add(cayanTower(mats, shadowMat));
  group.add(marinaTowers(mats, shadowMat));
  group.add(ainDubai(mats));
  group.add(burjAlArab(mats, shadowMat));
  group.add(palmIsland(mats));
  group.add(yachts(mats));

  return group;
}
