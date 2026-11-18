import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import gsap from 'gsap';
import './style.css';

/* =========================================================================
   AURELIA TOWER — ARCHITECTURAL MAQUETTE MASTERPLAN
   High-angle axonometric model inspired by architectural exhibition maquettes:
   - Elegant matte ivory/chalk surrounding urban blocks, courtyards, and trees
   - Serene blue waterfront lake & park promenade
   - Featured hero skyscraper rendered in physical glass, concrete, and champagne metal
   ========================================================================= */

const host = document.getElementById('scene-host');
const canvas = document.getElementById('world');
const loader = document.getElementById('loader');
const error = document.getElementById('error');

let renderer, scene, camera, orbit;

try {
  renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: false,
    powerPreference: 'high-performance'
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2.0));
  renderer.setSize(host.clientWidth, host.clientHeight, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.35;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
} catch (e) {
  if (loader) loader.remove();
  if (error) error.hidden = false;
  console.error('WebGL init error:', e);
  throw e;
}

scene = new THREE.Scene();

// High architectural studio background & subtle depth fog
const BG_COLOR = '#ede9e1';
scene.background = new THREE.Color(BG_COLOR);
scene.fog = new THREE.FogExp2(BG_COLOR, 0.00065);

// Camera setup: 38° FOV for crisp architectural telephoto axonometric perspective
camera = new THREE.PerspectiveCamera(38, host.clientWidth / Math.max(host.clientHeight, 1), 1, 3500);
// Start elevated for GSAP fly-in
camera.position.set(-360, 420, 450);

orbit = new OrbitControls(camera, canvas);
orbit.target.set(0, 60, 0);
orbit.enableDamping = true;
orbit.dampingFactor = 0.045;
orbit.maxPolarAngle = Math.PI / 2.06;
orbit.minPolarAngle = 0.15;
orbit.minDistance = 80;
orbit.maxDistance = 1200;
orbit.screenSpacePanning = true;
orbit.update();

// =========================================================================
// LIGHTING SETUP (Architectural Clay Maquette / Exhibition Studio)
// =========================================================================

// Primary Directional Sun (high angle casting crisp contact shadows across courtyards)
const sun = new THREE.DirectionalLight('#fffaf0', 2.8);
sun.position.set(-280, 420, 240);
sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048);
sun.shadow.camera.left = -460;
sun.shadow.camera.right = 460;
sun.shadow.camera.top = 460;
sun.shadow.camera.bottom = -460;
sun.shadow.camera.near = 20;
sun.shadow.camera.far = 1400;
sun.shadow.bias = -0.00015;
scene.add(sun);

// Soft cool fill light from opposite quadrant
const fillLight = new THREE.DirectionalLight('#dce6f2', 0.85);
fillLight.position.set(320, 280, -220);
scene.add(fillLight);

// Hemisphere light (Warm studio ceiling bounce + soft ground bounce)
const hemiLight = new THREE.HemisphereLight('#fcfbf7', '#ded8cd', 1.4);
scene.add(hemiLight);

// PRNG for consistent cityscape generation
const rand = (() => {
  let state = 839217;
  return () => ((state = (Math.imul(state, 1664525) + 1013904223) >>> 0) / 4294967296);
})();
const between = (a, b) => a + (b - a) * rand();
const choice = arr => arr[Math.floor(rand() * arr.length)];

// =========================================================================
// PBR MATERIAL SYSTEM
// =========================================================================
const pbr = (color, roughness = 0.5, metalness = 0.1) =>
  new THREE.MeshStandardMaterial({ color, roughness, metalness });

const phys = (opts) => new THREE.MeshPhysicalMaterial(opts);

// Procedural Curtain Wall Texture Generator for the Featured Skyscraper
function createTowerFacadeTexture() {
  const c = document.createElement('canvas');
  c.width = 512;
  c.height = 1024;
  const ctx = c.getContext('2d');

  // Deep tinted glass base
  ctx.fillStyle = '#14202a';
  ctx.fillRect(0, 0, 512, 1024);

  const cols = 16;
  const rows = 64;
  const cw = 512 / cols;
  const rh = 1024 / rows;

  for (let j = 0; j < rows; j++) {
    for (let i = 0; i < cols; i++) {
      const x = i * cw;
      const y = j * rh;

      // Champagne metal mullions
      ctx.fillStyle = '#7a6c56';
      ctx.fillRect(x, y, cw, rh);

      // Glass pane
      ctx.fillStyle = '#192b38';
      ctx.fillRect(x + 1.5, y + 1.5, cw - 3, rh - 3);

      // Subtle warm interior floor illumination (evening mood)
      if (rand() > 0.4) {
        ctx.fillStyle = 'rgba(255, 225, 170, 0.45)';
        ctx.fillRect(x + 2, y + 2, cw - 4, rh - 4);
      }

      // Fresnel reflection sheen
      ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.fillRect(x + 2, y + 2, cw - 4, (rh - 4) * 0.4);
    }
  }

  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = Math.min(renderer.capabilities.getMaxAnisotropy(), 8);
  return tex;
}

const towerFacadeMap = createTowerFacadeTexture();

const mat = {
  // Surrounding Ivory City Maquette
  ivoryBuilding: pbr('#ede9e1', 0.88, 0.04),       // Smooth chalk/clay plaster
  ivoryBuildingAccent: pbr('#dfdad0', 0.78, 0.08), // Window reveals, setbacks
  ivoryPlinth: pbr('#d5cfc4', 0.75, 0.1),          // Rooftop plant rooms, mechanicals
  ivoryCourtyard: pbr('#e5e0d7', 0.9, 0.0),        // Courtyard ground
  groundBase: pbr('#f5f2eb', 0.94, 0.0),           // Masterplan baseboard
  roadSurface: pbr('#dbd6cc', 0.88, 0.02),         // Paved avenues
  roadMarking: pbr('#fbf9f5', 0.6, 0.0),           // White lane markings
  sidewalk: pbr('#eae5dc', 0.9, 0.0),              // Raised curbs/sidewalks
  parkGrass: pbr('#cfdccd', 0.85, 0.0),            // Muted architectural sage/mint grass
  treeTrunk: pbr('#d8d3c8', 0.85, 0.0),            // Slender ivory tree stems
  treeFoliage: pbr('#c2d4c0', 0.78, 0.0),          // Sage-clay deciduous canopies
  treeFoliageIvory: pbr('#e6e2d8', 0.82, 0.0),     // Chalk-white trees in courtyards
  carIvory: pbr('#ded8ce', 0.65, 0.15),            // Stylized maquette vehicles

  // Waterfront Lake (Calm, serene blue water matching reference image)
  lakeWater: phys({
    color: '#4a7b99',
    roughness: 0.06,
    metalness: 0.12,
    transmission: 0.42,
    ior: 1.333,
    reflectivity: 0.88,
    clearcoat: 1.0,
    clearcoatRoughness: 0.02
  }),
  lakeBorder: pbr('#dfdad0', 0.72, 0.05),

  // THE FEATURED HERO SKYSCRAPER (High-End Realistic Materials)
  towerGlass: phys({
    color: '#1a2a35',
    roughness: 0.05,
    metalness: 0.35,
    clearcoat: 1.0,
    clearcoatRoughness: 0.02,
    transmission: 0.48,
    ior: 1.54,
    reflectivity: 0.94,
    transparent: true,
    opacity: 0.92,
    map: towerFacadeMap
  }),
  towerConcrete: pbr('#eae7e1', 0.64, 0.05),       // Fluted architectural precast concrete
  towerChampagne: pbr('#c9b086', 0.22, 0.88),      // Champagne titanium metal trims
  towerDarkMetal: pbr('#2c333a', 0.35, 0.75),      // Recessed shadow louvers
  atriumGarden: pbr('#386b44', 0.82, 0.0),         // Biophilic sky garden vegetation
  spireBeacon: new THREE.MeshBasicMaterial({ color: '#ff2525' }),
  podiumGlass: phys({
    color: '#3d5c6f',
    roughness: 0.04,
    metalness: 0.1,
    transmission: 0.75,
    transparent: true,
    opacity: 0.85,
    clearcoat: 1.0
  })
};

const cityRoot = new THREE.Group();
scene.add(cityRoot);

const hitMeshes = [];
const landmarks = {};
let lakeMesh = null;

// Geometry Builder Helpers
function mesh(geo, material, x = 0, y = 0, z = 0, parent = cityRoot, shadow = true) {
  const m = new THREE.Mesh(geo, material);
  m.position.set(x, y, z);
  m.receiveShadow = true;
  m.castShadow = shadow;
  parent.add(m);
  return m;
}

function box(w, h, d, material, x = 0, y = 0, z = 0, parent = cityRoot, shadow = true) {
  return mesh(new THREE.BoxGeometry(w, h, d), material, x, y, z, parent, shadow);
}

function cylinder(r1, r2, h, material, x = 0, y = 0, z = 0, parent = cityRoot, segments = 16, shadow = true) {
  return mesh(new THREE.CylinderGeometry(r1, r2, h, segments), material, x, y, z, parent, segments > 8 && shadow);
}

// Tree Builder Helper (Stylized Architectural Model Tree)
function createTree(x, z, parent = cityRoot, isIvory = false, scale = 1.0) {
  const g = new THREE.Group();
  g.position.set(x, 0, z);
  g.scale.setScalar(scale);
  parent.add(g);

  // Trunk
  cylinder(0.4, 0.6, 5.5, mat.treeTrunk, 0, 2.75, 0, g, 8, true);

  // Stylized Foliage (Cluster of soft spheres/ellipsoids)
  const foliageMat = isIvory ? mat.treeFoliageIvory : mat.treeFoliage;
  const fGeo = new THREE.DodecahedronGeometry(3.2, 1);
  const f = mesh(fGeo, foliageMat, 0, 7.2, 0, g, true);
  f.scale.set(1.0, 1.25, 1.0);
}

// Stylized Miniature Maquette Car
function createCar(x, z, angle, parent = cityRoot) {
  const car = box(2.4, 1.3, 4.8, mat.carIvory, x, 0.7, z, parent, true);
  car.rotation.y = angle;
  // Cabin greenhouse
  box(2.0, 0.9, 2.4, mat.ivoryBuildingAccent, x, 1.5, z - 0.2, parent);
}

// =========================================================================
// 1. MASTERPLAN GROUND BASE & ROAD GRID
// =========================================================================
// Main Baseboard Plinth
box(1400, 6, 1400, mat.groundBase, 0, -3, 0, cityRoot, false);

// Urban Grid Streets
const GRID_SIZE = 7;
const BLOCK_STEP = 86;
const HALF_EXTENT = (GRID_SIZE - 1) * BLOCK_STEP * 0.5;

// Continuous Road Base Mat
box(660, 0.4, 660, mat.roadSurface, 0, 0.2, 0, cityRoot, false);

// Road Dashed Markings
for (let i = -3; i <= 3; i++) {
  const coord = i * BLOCK_STEP;
  // Longitude Avenues
  for (let k = -280; k <= 280; k += 16) {
    box(0.5, 0.05, 7, mat.roadMarking, coord, 0.45, k, cityRoot, false);
  }
  // Latitude Streets
  for (let k = -280; k <= 280; k += 16) {
    box(7, 0.05, 0.5, mat.roadMarking, k, 0.45, coord, cityRoot, false);
  }
}

// =========================================================================
// 2. WATERFRONT LAKE & PARK (Bottom-Left zone, matching reference image)
// =========================================================================
const parkGroup = new THREE.Group();
cityRoot.add(parkGroup);

// Park Landscape Plateau
const parkShape = new THREE.Shape();
parkShape.moveTo(-280, 70);
parkShape.lineTo(-90, 70);
parkShape.lineTo(-90, 260);
parkShape.lineTo(-280, 260);
parkShape.closePath();

const parkGeo = new THREE.ShapeGeometry(parkShape);
const parkMesh = new THREE.Mesh(parkGeo, mat.parkGrass);
parkMesh.rotation.x = -Math.PI / 2;
parkMesh.position.y = 0.5;
parkMesh.receiveShadow = true;
parkGroup.add(parkMesh);

// The Curvilinear Lake Basin (Exact organic curve from reference photo)
const lakeCurve = new THREE.Shape();
const lx0 = -185, lz0 = 165;
lakeCurve.moveTo(lx0 - 65, lz0);
lakeCurve.bezierCurveTo(lx0 - 65, lz0 - 45, lx0 - 20, lz0 - 55, lx0 + 35, lz0 - 40);
lakeCurve.bezierCurveTo(lx0 + 75, lz0 - 30, lx0 + 70, lz0 + 25, lx0 + 40, lz0 + 45);
lakeCurve.bezierCurveTo(lx0 - 10, lz0 + 60, lx0 - 65, lz0 + 35, lx0 - 65, lz0);

const lakeGeo = new THREE.ShapeGeometry(lakeCurve);
lakeMesh = new THREE.Mesh(lakeGeo, mat.lakeWater);
lakeMesh.rotation.x = -Math.PI / 2;
lakeMesh.position.y = 0.7;
lakeMesh.receiveShadow = true;
parkGroup.add(lakeMesh);

// Stone Promenade Coping Rim around Lake
const lakeBorderPoints = lakeCurve.getPoints(64);
const rimSpline = new THREE.CatmullRomCurve3(
  lakeBorderPoints.map(p => new THREE.Vector3(p.x, 0.8, -p.y))
);
rimSpline.closed = true;
const rimGeo = new THREE.TubeGeometry(rimSpline, 64, 1.2, 8, true);
const rimMesh = new THREE.Mesh(rimGeo, mat.lakeBorder);
rimMesh.castShadow = true;
rimMesh.receiveShadow = true;
parkGroup.add(rimMesh);

// Waterfront Trees lining the curved park promenade
for (let i = 0; i < 28; i++) {
  const pt = rimSpline.getPoint(i / 28);
  const normal = rimSpline.getTangent(i / 28).cross(new THREE.Vector3(0, 1, 0)).normalize();
  const tx = pt.x + normal.x * (between(6, 18));
  const tz = pt.z + normal.z * (between(6, 18));
  createTree(tx, tz, parkGroup, false, between(0.85, 1.2));
}

// Benches and pedestrian stroll paths in park
for (let b = 0; b < 12; b++) {
  const pt = rimSpline.getPoint((b + 0.5) / 12);
  box(4, 0.6, 1.4, mat.ivoryPlinth, pt.x + 4, 1.1, pt.z + 4, parkGroup, true);
}

landmarks.lake = {
  name: 'WATERFRONT PARK & LAKE',
  description: 'An organic curved freshwater basin with stone promenade, shaded pedestrian plazas, and lush tree groves.',
  point: new THREE.Vector3(lx0, 2, lz0),
  target: new THREE.Vector3(lx0, 0, lz0),
  camera: new THREE.Vector3(-290, 110, 260)
};

// =========================================================================
// 3. ELEGANT IVORY SURROUNDING BUILDINGS (Courtyard blocks & Mid-rises)
// =========================================================================

// Courtyard Perimeter Block Generator (as seen throughout reference image)
function createCourtyardBlock(bx, bz, blockSize = 64) {
  const g = new THREE.Group();
  g.position.set(bx, 0, bz);
  cityRoot.add(g);

  // Raised Sidewalk Island
  box(blockSize + 6, 0.8, blockSize + 6, mat.sidewalk, 0, 0.4, 0, g);

  // 4 Wings forming the perimeter block
  const wallThick = 12;
  const innerSize = blockSize - wallThick * 2;
  const baseH = between(18, 38);

  // North wing
  box(blockSize, baseH, wallThick, mat.ivoryBuilding, 0, baseH / 2 + 0.8, -blockSize / 2 + wallThick / 2, g, true);
  // South wing (varied height for terracing)
  const southH = baseH * between(0.6, 0.85);
  box(blockSize, southH, wallThick, mat.ivoryBuilding, 0, southH / 2 + 0.8, blockSize / 2 - wallThick / 2, g, true);
  // West wing
  box(wallThick, baseH * 0.9, innerSize, mat.ivoryBuilding, -blockSize / 2 + wallThick / 2, (baseH * 0.9) / 2 + 0.8, 0, g, true);
  // East wing
  box(wallThick, baseH * 0.75, innerSize, mat.ivoryBuilding, blockSize / 2 - wallThick / 2, (baseH * 0.75) / 2 + 0.8, 0, g, true);

  // Inner Courtyard Garden Lawn
  box(innerSize, 0.2, innerSize, mat.parkGrass, 0, 0.9, 0, g);

  // 2-3 Stylized Trees inside the courtyard
  createTree(-innerSize * 0.22, -innerSize * 0.2, g, true, 0.75);
  createTree(innerSize * 0.25, innerSize * 0.18, g, true, 0.8);

  // Rooftop mechanical boxes & elevator overruns
  box(10, 4, 8, mat.ivoryPlinth, -blockSize * 0.25, baseH + 2.8, -blockSize * 0.35, g, true);
  box(7, 3, 6, mat.ivoryPlinth, blockSize * 0.2, baseH + 2.3, -blockSize * 0.35, g, true);

  // Street Trees on outer curbs
  createTree(-blockSize * 0.5 - 3.5, blockSize * 0.35, g, false, 0.65);
  createTree(blockSize * 0.5 + 3.5, -blockSize * 0.25, g, false, 0.65);

  // Parked cars along sidewalk curb
  createCar(-blockSize * 0.5 - 5, -blockSize * 0.2, 0, g);
  createCar(-blockSize * 0.5 - 5, blockSize * 0.1, 0, g);
}

// Stepped Mid-Rise Commercial Tower Generator
function createMidRiseTower(bx, bz, blockSize = 64) {
  const g = new THREE.Group();
  g.position.set(bx, 0, bz);
  cityRoot.add(g);

  // Sidewalk Plinth
  box(blockSize + 6, 0.8, blockSize + 6, mat.sidewalk, 0, 0.4, 0, g);

  // Podium Base (Ground + 2 levels)
  const podiumH = 14;
  box(blockSize - 4, podiumH, blockSize - 4, mat.ivoryBuilding, 0, podiumH / 2 + 0.8, 0, g, true);

  // Tower Shaft with Setbacks
  const towerW = blockSize * between(0.48, 0.62);
  const towerD = blockSize * between(0.48, 0.62);
  const towerH = between(55, 110);
  const towerX = between(-6, 6);
  const towerZ = between(-6, 6);

  box(towerW, towerH, towerD, mat.ivoryBuilding, towerX, podiumH + towerH / 2 + 0.8, towerZ, g, true);

  // Architectural Setback Tier
  if (towerH > 75) {
    const tierH = 22;
    box(towerW * 0.7, tierH, towerD * 0.7, mat.ivoryBuildingAccent,
      towerX, podiumH + towerH + tierH / 2 + 0.8, towerZ, g, true);
    // Rooftop chiller housing & antenna
    box(towerW * 0.4, 5, towerD * 0.4, mat.ivoryPlinth,
      towerX, podiumH + towerH + tierH + 3.3, towerZ, g, true);
    cylinder(0.3, 0.6, 12, mat.ivoryPlinth, towerX, podiumH + towerH + tierH + 11.5, towerZ, g, 8);
  } else {
    box(towerW * 0.5, 4.5, towerD * 0.5, mat.ivoryPlinth, towerX, podiumH + towerH + 3.0, towerZ, g, true);
  }

  // Street Trees
  createTree(-blockSize * 0.5 - 3.5, -blockSize * 0.3, g, false, 0.7);
  createTree(blockSize * 0.5 + 3.5, blockSize * 0.3, g, false, 0.7);
}

// Generate the 7x7 Superblock City Grid
for (let gx = 0; gx < GRID_SIZE; gx++) {
  for (let gz = 0; gz < GRID_SIZE; gz++) {
    const x = (gx - (GRID_SIZE - 1) / 2) * BLOCK_STEP;
    const z = (gz - (GRID_SIZE - 1) / 2) * BLOCK_STEP;

    // Center reserved for our Hero Featured Skyscraper
    if (Math.abs(x) < 40 && Math.abs(z) < 40) continue;

    // Bottom-Left quadrant reserved for the Waterfront Lake & Park
    if (x < -45 && z > 35) continue;

    // Mix between Courtyard Blocks (60%) and Stepped Mid-Rise Towers (40%)
    if (rand() > 0.42) {
      createCourtyardBlock(x, z, 62);
    } else {
      createMidRiseTower(x, z, 62);
    }
  }
}

// =========================================================================
// 4. THE FEATURED HERO SKYSCRAPER — "THE AURELIA TOWER"
// Rendered in High-End Realistic Glass, Concrete & Champagne Titanium Metal
// =========================================================================
const heroTower = new THREE.Group();
heroTower.position.set(0, 0, 0);
cityRoot.add(heroTower);
heroTower.userData.place = 'aurelia';

// Grand Plaza Podium Base
box(74, 1.2, 74, mat.sidewalk, 0, 0.6, 0, heroTower);
box(66, 0.3, 66, mat.ivoryCourtyard, 0, 1.35, 0, heroTower);

// Podium Colonnade (Double-height transparent glass galleria + concrete fluted pillars)
const podiumH = 22;
box(52, podiumH, 52, mat.podiumGlass, 0, podiumH / 2 + 1.5, 0, heroTower, true);

// Fluted Architectural Concrete Corner Pylons
const colDist = 25.5;
for (const [cx, cz] of [[-colDist, -colDist], [colDist, -colDist], [-colDist, colDist], [colDist, colDist]]) {
  cylinder(2.6, 3.2, podiumH, mat.towerConcrete, cx, podiumH / 2 + 1.5, cz, heroTower, 16, true);
}

// Champagne Metal Entrance Canopy
box(34, 1.4, 16, mat.towerChampagne, 0, 7.5, 27, heroTower, true);

// =========================================================================
// Tower Shaft Composition (320m Luxury Sculptural Supertall)
// =========================================================================
let currentH = podiumH + 1.5;

// Lower Body: Sculptural Faceted Glass & Concrete Tier (Levels 5-30)
const lowerH = 105;
const lowerShaft = box(46, lowerH, 46, mat.towerGlass, 0, currentH + lowerH / 2, 0, heroTower, true);
hitMeshes.push(lowerShaft);

// Structural White Precast Concrete Vertical Ribs running up the corners
for (const [rx, rz] of [[-23.2, -23.2], [23.2, -23.2], [-23.2, 23.2], [23.2, 23.2]]) {
  box(2.8, lowerH, 2.8, mat.towerConcrete, rx, currentH + lowerH / 2, rz, heroTower, true);
}

// Champagne Titanium Spandrel Floor Trims
for (let f = 0; f < 8; f++) {
  box(47.2, 1.0, 47.2, mat.towerChampagne, 0, currentH + f * 13, 0, heroTower);
}

currentH += lowerH;

// =========================================================================
// Mid-Tower: Biophilic Suspended Sky Garden Atrium (Levels 31-35)
// =========================================================================
const gardenH = 26;
// Recessed Core
box(28, gardenH, 28, mat.towerDarkMetal, 0, currentH + gardenH / 2, 0, heroTower, true);
// Suspended Garden Slabs
box(44, 1.6, 44, mat.towerConcrete, 0, currentH + 0.8, 0, heroTower, true);
box(42, 0.4, 42, mat.atriumGarden, 0, currentH + 1.8, 0, heroTower);
box(44, 1.6, 44, mat.towerConcrete, 0, currentH + gardenH, 0, heroTower, true);

// Sky Garden Trees & Biophilic Flora
createTree(-14, -12, heroTower, false, 0.7);
createTree(14, -12, heroTower, false, 0.7);
createTree(-14, 12, heroTower, false, 0.7);
createTree(14, 12, heroTower, false, 0.7);

// Structural Champagne Exoskeleton Diagonal Trusses flanking the garden
for (const [exX, exRot] of [[-22, Math.PI / 6], [22, -Math.PI / 6]]) {
  const truss = cylinder(1.2, 1.2, gardenH * 1.15, mat.towerChampagne, exX, currentH + gardenH / 2, 0, heroTower, 12, true);
  truss.rotation.z = exRot;
}

landmarks.skygarden = {
  name: 'BIOPHILIC SKY GARDEN',
  description: 'Triple-height open-air suspended atrium garden with full panoramic 360° views across the masterplan.',
  point: new THREE.Vector3(0, currentH + gardenH / 2, 24),
  target: new THREE.Vector3(0, currentH + gardenH / 2, 0),
  camera: new THREE.Vector3(-65, currentH + gardenH + 20, 75)
};

currentH += gardenH;

// =========================================================================
// Upper Tower: Tapered Executive Glass Shaft (Levels 36-60)
// =========================================================================
const upperH = 95;
const upperShaft = box(36, upperH, 36, mat.towerGlass, 0, currentH + upperH / 2, 0, heroTower, true);
hitMeshes.push(upperShaft);

// Concrete Pilasters tapering upwards
for (const [rx, rz] of [[-18.2, -18.2], [18.2, -18.2], [-18.2, 18.2], [18.2, 18.2]]) {
  box(2.2, upperH, 2.2, mat.towerConcrete, rx, currentH + upperH / 2, rz, heroTower, true);
}

// Champagne Spandrel Bands
for (let f = 0; f < 7; f++) {
  box(37.0, 0.9, 37.0, mat.towerChampagne, 0, currentH + f * 13.5, 0, heroTower);
}

currentH += upperH;

// =========================================================================
// Sculptural Crown & Titanium Spire (Levels 61-75)
// =========================================================================
const crownH = 38;
// Tapering Champagne Titanium Crown Framework
const crownGeo = new THREE.CylinderGeometry(8, 19, crownH, 4, 1, false);
const crownMesh = mesh(crownGeo, mat.towerChampagne, 0, currentH + crownH / 2, 0, heroTower, true);
crownMesh.rotation.y = Math.PI / 4;

// Crystal Glass Lantern Core inside the crown
const lanternGeo = new THREE.CylinderGeometry(5, 14, crownH * 0.9, 4, 1, false);
const lanternMesh = mesh(lanternGeo, mat.towerGlass, 0, currentH + crownH / 2, 0, heroTower);
lanternMesh.rotation.y = Math.PI / 4;

currentH += crownH;

// Architectural Spire Finial (piercing to 330m)
cylinder(0.5, 2.8, 48, mat.towerChampagne, 0, currentH + 24, 0, heroTower, 12, true);
cylinder(0.15, 0.5, 30, mat.towerDarkMetal, 0, currentH + 63, 0, heroTower, 8);

const totalTowerHeight = currentH + 78;

// Red Aviation Warning Strobe Beacon at the summit
const beacon = mesh(new THREE.SphereGeometry(1.2, 8, 8), mat.spireBeacon, 0, totalTowerHeight, 0, heroTower);

landmarks.aurelia = {
  name: 'AURELIA TOWER',
  description: 'An iconic 330m luxury supertall rendered in physical glass, precast concrete, and champagne titanium, commanding the masterplan.',
  point: new THREE.Vector3(0, totalTowerHeight * 0.65, 0),
  target: new THREE.Vector3(0, 110, 0),
  camera: new THREE.Vector3(-140, 190, 210)
};

// =========================================================================
// 5. CAMERA PRESETS & ATMOSPHERIC LIGHTING MODES
// =========================================================================
const cameraPresets = {
  axon: {
    pos: new THREE.Vector3(-280, 320, 360),
    target: new THREE.Vector3(0, 50, 0)
  },
  tower: {
    pos: new THREE.Vector3(-120, 180, 180),
    target: new THREE.Vector3(0, 130, 0)
  },
  lake: {
    pos: new THREE.Vector3(-280, 95, 270),
    target: new THREE.Vector3(-180, 10, 160)
  }
};

let cameraTransition = null;
let isOrbitTour = false;
let isTabVisible = true;

function flyTo(targetPos, lookTarget, duration = 2.2) {
  isOrbitTour = false;
  cameraTransition = {
    pos: targetPos.clone(),
    target: lookTarget.clone()
  };
}

// Atmospheric Moods
const moods = [
  {
    name: 'STUDIO DAYLIGHT',
    bg: '#ede9e1',
    sunCol: '#fffaf0',
    sunInt: 2.8,
    fillCol: '#dce6f2',
    fillInt: 0.85,
    hemiSky: '#fcfbf7',
    hemiGround: '#ded8cd',
    exposure: 1.35
  },
  {
    name: 'SUNSET GOLD',
    bg: '#ded3c5',
    sunCol: '#ffaa55',
    sunInt: 3.4,
    fillCol: '#8ca4bf',
    fillInt: 0.95,
    hemiSky: '#ffedd6',
    hemiGround: '#9e8c7a',
    exposure: 1.42
  },
  {
    name: 'BLUE HOUR TWILIGHT',
    bg: '#252e3d',
    sunCol: '#4b6f9e',
    sunInt: 1.2,
    fillCol: '#202f48',
    fillInt: 0.7,
    hemiSky: '#364968',
    hemiGround: '#141c28',
    exposure: 1.55
  }
];

let currentMood = 0;
function applyMood(idx) {
  const m = moods[idx];
  currentMood = idx;

  scene.background.set(m.bg);
  scene.fog.color.set(m.bg);
  sun.color.set(m.sunCol);
  sun.intensity = m.sunInt;
  fillLight.color.set(m.fillCol);
  fillLight.intensity = m.fillInt;
  hemiLight.color.set(m.hemiSky);
  hemiLight.groundColor.set(m.hemiGround);
  renderer.toneMappingExposure = m.exposure;

  const label = document.getElementById('mood-label');
  if (label) label.textContent = m.name;
}

// UI Buttons Event Binding
document.getElementById('time-mode')?.addEventListener('click', () => {
  applyMood((currentMood + 1) % moods.length);
});

document.getElementById('view-axon')?.addEventListener('click', () => {
  flyTo(cameraPresets.axon.pos, cameraPresets.axon.target);
});

document.getElementById('view-tower')?.addEventListener('click', () => {
  flyTo(cameraPresets.tower.pos, cameraPresets.tower.target);
});

document.getElementById('view-lake')?.addEventListener('click', () => {
  flyTo(cameraPresets.lake.pos, cameraPresets.lake.target);
});

document.getElementById('tour')?.addEventListener('click', () => {
  isOrbitTour = !isOrbitTour;
  document.getElementById('tour').classList.toggle('active', isOrbitTour);
});

document.getElementById('reset')?.addEventListener('click', () => {
  flyTo(cameraPresets.axon.pos, cameraPresets.axon.target);
});

document.getElementById('explore')?.addEventListener('click', () => {
  flyTo(cameraPresets.tower.pos, cameraPresets.tower.target);
});

// Interactive Pin Clicks
for (const [id, btnId] of [['aurelia', 'pin-aurelia'], ['lake', 'pin-lake'], ['skygarden', 'pin-skygarden']]) {
  document.getElementById(btnId)?.addEventListener('click', () => {
    const l = landmarks[id];
    if (l) flyTo(l.camera, l.target);
  });
}

// Contact Modal Handling
const contactModal = document.getElementById('contact-modal');
document.getElementById('enquire')?.addEventListener('click', () => contactModal.showModal());
document.getElementById('close-modal')?.addEventListener('click', () => contactModal.close());
document.getElementById('modal-demo')?.addEventListener('click', () => {
  alert('Thank you for your enquiry. In production, this records to the sales CRM.');
  contactModal.close();
});

// Raycasting for Direct 3D Mesh Clicks
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
let lastPointer = null;
let isUserDragging = false;

canvas.addEventListener('pointerdown', ev => {
  lastPointer = { x: ev.clientX, y: ev.clientY };
  isUserDragging = true;
});

window.addEventListener('pointerup', () => {
  isUserDragging = false;
});

canvas.addEventListener('pointerup', ev => {
  if (!lastPointer || Math.hypot(ev.clientX - lastPointer.x, ev.clientY - lastPointer.y) > 6) return;
  const rect = canvas.getBoundingClientRect();
  pointer.x = ((ev.clientX - rect.left) / rect.width) * 2 - 1;
  pointer.y = -((ev.clientY - rect.top) / rect.height) * 2 + 1;

  raycaster.setFromCamera(pointer, camera);
  const hits = raycaster.intersectObjects(hitMeshes, true);
  if (hits.length) {
    flyTo(landmarks.aurelia.camera, landmarks.aurelia.target);
  }
});

// Subtle Mouse Parallax
let mouseParallax = { x: 0, y: 0 };
let targetParallax = { x: 0, y: 0 };

window.addEventListener('pointermove', ev => {
  const normX = (ev.clientX / window.innerWidth - 0.5) * 2;
  const normY = (ev.clientY / window.innerHeight - 0.5) * 2;
  targetParallax.x = normX * 12;
  targetParallax.y = -normY * 8;
});

// =========================================================================
// 6. ANIMATION & RENDER LOOP
// =========================================================================
const clock = new THREE.Clock();
const projPoint = new THREE.Vector3();

function animate() {
  requestAnimationFrame(animate);
  const dt = Math.min(clock.getDelta(), 0.05);
  const t = clock.elapsedTime;

  if (!isTabVisible) return;

  // 1. Water Ripple & Specular Shimmer on Lake
  if (lakeMesh) {
    mat.lakeWater.roughness = 0.06 + Math.sin(t * 1.8) * 0.02;
  }

  // 2. Beacon Strobe Flashing on Tower Spire
  const strobeVal = Math.sin(t * 5.0) > 0.8 ? 1.0 : 0.08;
  beacon.scale.setScalar(strobeVal > 0.5 ? 1.4 : 0.9);
  mat.spireBeacon.opacity = strobeVal;

  // 3. 360 Turntable Orbit Tour
  if (isOrbitTour) {
    orbit.autoRotate = true;
    orbit.autoRotateSpeed = 1.0;
  } else {
    orbit.autoRotate = false;
  }

  // 4. Smooth Camera Easing on Navigation
  const ease = 1 - Math.exp(-dt * 3.0);
  if (cameraTransition) {
    camera.position.lerp(cameraTransition.pos, ease);
    orbit.target.lerp(cameraTransition.target, ease);
    if (camera.position.distanceTo(cameraTransition.pos) < 1.0 &&
        orbit.target.distanceTo(cameraTransition.target) < 0.8) {
      cameraTransition = null;
    }
  }

  // 5. Idle Mouse Parallax Drift
  mouseParallax.x += (targetParallax.x - mouseParallax.x) * 0.04;
  mouseParallax.y += (targetParallax.y - mouseParallax.y) * 0.04;
  if (!cameraTransition && !isUserDragging && orbit.state === -1 && !isOrbitTour) {
    orbit.target.x = mouseParallax.x * 0.25;
    orbit.target.y = 50 + mouseParallax.y * 0.25;
  }

  orbit.update();

  // 6. 3D Spatial Annotation Pins Projection
  for (const [id, pinElId] of [['aurelia', 'pin-aurelia'], ['lake', 'pin-lake'], ['skygarden', 'pin-skygarden']]) {
    const l = landmarks[id];
    if (!l) continue;

    projPoint.copy(l.point).project(camera);
    const pinEl = document.getElementById(pinElId);
    if (pinEl) {
      const px = (projPoint.x * 0.5 + 0.5) * host.clientWidth;
      const py = (-projPoint.y * 0.5 + 0.5) * host.clientHeight;
      const inView = projPoint.z > -1 && projPoint.z < 1 &&
        px > 25 && px < host.clientWidth - 25 && py > 60 && py < host.clientHeight - 80;

      pinEl.style.display = inView ? 'flex' : 'none';
      if (inView) {
        pinEl.style.left = `${px}px`;
        pinEl.style.top = `${py}px`;
      }
    }
  }

  renderer.render(scene, camera);
}

function handleResize() {
  const w = Math.max(1, host.clientWidth);
  const h = Math.max(1, host.clientHeight);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2.0));
  renderer.setSize(w, h, false);
}

new ResizeObserver(handleResize).observe(host);
new IntersectionObserver(entries => {
  isTabVisible = entries[0].isIntersecting;
}, { threshold: 0 }).observe(document.getElementById('hero'));

document.addEventListener('visibilitychange', () => {
  isTabVisible = !document.hidden;
});

// Initialization & Cinematic GSAP Entrance
try {
  handleResize();
  applyMood(0);

  requestAnimationFrame(() => {
    if (loader) loader.remove();

    // GSAP Cinematic Entrance Fly-in to the reference axonometric angle
    const introTl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    introTl.to(camera.position, {
      x: cameraPresets.axon.pos.x,
      y: cameraPresets.axon.pos.y,
      z: cameraPresets.axon.pos.z,
      duration: 3.0,
      onUpdate: () => orbit.update()
    }, 0);

    introTl.to(orbit.target, {
      x: cameraPresets.axon.target.x,
      y: cameraPresets.axon.target.y,
      z: cameraPresets.axon.target.z,
      duration: 3.0,
      onUpdate: () => orbit.update()
    }, 0);

    // Editorial text mask reveals
    introTl.from('.hero-content .title-line-mask h1', {
      y: '110%',
      duration: 1.3,
      stagger: 0.15,
      ease: 'power4.out'
    }, 0.5);

    introTl.from('.kicker, .hero-content p, .actions', {
      opacity: 0,
      y: 22,
      stagger: 0.12,
      duration: 1.0,
      ease: 'power3.out'
    }, 0.9);

    introTl.from('.status, .controls-group button', {
      opacity: 0,
      y: -10,
      stagger: 0.08,
      duration: 0.8,
      ease: 'back.out(1.5)'
    }, 1.2);
  });

  animate();
} catch (e) {
  if (loader) loader.remove();
  if (error) error.hidden = false;
  console.error('Scene initialization failed:', e);
}
