// Shared data store for Vercel serverless functions
// Synchronized permanently with Firebase Firestore (aleen-a5c32)
// Uses dedicated documents for carousel slides and catalog to prevent document size limits

const fs = require('fs');
const path = require('path');
const https = require('https');

const PROJECT_ID = 'aleen-a5c32';
const API_KEY = 'AIzaSyDJOIWVS5LwRfhLLEa_lT51CI6ndQp1eXQ';
const BASE_FIRESTORE = `https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)/documents/settings`;
const DATA_FILE = path.join(process.cwd(), 'atelier_data.json');

const DEFAULT_DATA = {
  masterPassword: 'aleen',
  users: [
    { username: 'admin', role: 'admin', password: 'aleen', createdAt: '14 Nov 2026' }
  ],
  megaMenuBanner: {
    img: 'https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2',
    badge: 'CURATED HAUTE COUTURE',
    title: "The Women's Edit",
    line: 'Handcrafted Banarasi weaves & royal silhouettes',
    url: 'collections.html'
  },
  heroRotator: [],
  carouselSlides: [],
  catalog: []
};

let _cache = null;
let _lastFetchTime = 0;
const CACHE_TTL_MS = 2000;

function readLocalFallback() {
  try {
    if (fs.existsSync(DATA_FILE)) {
      const raw = fs.readFileSync(DATA_FILE, 'utf8');
      return { ...DEFAULT_DATA, ...JSON.parse(raw) };
    }
  } catch (e) {
    console.warn('readLocalFallback error:', e.message);
  }
  return { ...DEFAULT_DATA };
}

function fetchDoc(docName) {
  return new Promise((resolve) => {
    const url = `${BASE_FIRESTORE}/${docName}?key=${API_KEY}`;
    const req = https.get(url, { timeout: 3500 }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const doc = JSON.parse(body);
            const raw = doc.fields?.jsonPayload?.stringValue;
            if (raw) return resolve(JSON.parse(raw));
          } catch (e) {}
        }
        resolve(null);
      });
    });
    req.on('timeout', () => { req.destroy(); resolve(null); });
    req.on('error', () => resolve(null));
  });
}

function saveDoc(docName, data) {
  return new Promise((resolve) => {
    const url = new URL(`${BASE_FIRESTORE}/${docName}?key=${API_KEY}`);
    const payload = JSON.stringify({
      fields: {
        jsonPayload: { stringValue: JSON.stringify(data) },
        updatedAt: { stringValue: new Date().toISOString() }
      }
    });

    const req = https.request(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 4500
    }, (res) => {
      resolve(res.statusCode === 200);
    });

    req.on('timeout', () => { req.destroy(); resolve(false); });
    req.on('error', () => resolve(false));
    req.write(payload);
    req.end();
  });
}

async function getCarouselSlides() {
  const remote = await fetchDoc('atelier_carousel');
  if (Array.isArray(remote) && remote.length >= 2) {
    if (!_cache) _cache = readLocalFallback();
    _cache.carouselSlides = remote;
    return remote;
  }
  const data = await getData();
  return data.carouselSlides || [];
}

async function saveCarouselSlides(slides) {
  if (!_cache) _cache = readLocalFallback();
  _cache.carouselSlides = slides;
  _lastFetchTime = Date.now();
  await saveDoc('atelier_carousel', slides);
  return slides;
}

async function getCatalog() {
  const remote = await fetchDoc('atelier_catalog');
  if (Array.isArray(remote) && remote.length > 0) {
    if (!_cache) _cache = readLocalFallback();
    _cache.catalog = remote;
    return remote;
  }
  const data = await getData();
  return data.catalog || [];
}

async function saveCatalog(catalog) {
  if (!_cache) _cache = readLocalFallback();
  _cache.catalog = catalog;
  _lastFetchTime = Date.now();
  await saveDoc('atelier_catalog', catalog);
  return catalog;
}

async function getData() {
  const now = Date.now();
  if (_cache && (now - _lastFetchTime < CACHE_TTL_MS)) {
    return _cache;
  }

  const base = await fetchDoc('atelier_data') || readLocalFallback();
  _cache = { ...DEFAULT_DATA, ...base };
  _lastFetchTime = now;
  return _cache;
}

async function saveData(data) {
  _cache = { ..._cache, ...data };
  _lastFetchTime = Date.now();
  if (data.carouselSlides) await saveDoc('atelier_carousel', data.carouselSlides);
  if (data.catalog) await saveDoc('atelier_catalog', data.catalog);
  
  const generalData = { ..._cache };
  delete generalData.carouselSlides;
  delete generalData.catalog;
  await saveDoc('atelier_data', generalData);
  return _cache;
}

module.exports = {
  getData,
  saveData,
  getCarouselSlides,
  saveCarouselSlides,
  getCatalog,
  saveCatalog
};
