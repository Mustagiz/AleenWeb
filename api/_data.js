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
  catalog: [],
  womenCollections: [
    {
      id: "kurtis",
      kicker: "New Collection",
      title: "Pakistani Kurtis",
      desc: "Royal silhouettes in pure raw silk & velvet.",
      img: "assets/pakistani-kurti-1.jpg",
      url: "collections.html?category=kurtis"
    },
    {
      id: "kurta-sets",
      kicker: "New Collection",
      title: "Kurta Sets",
      desc: "Everyday elegance, elevated.",
      img: "https://mahira2.netlify.app/assets/s3-kurta.jpg?v=5",
      url: "collections.html?category=kurta-sets"
    },
    {
      id: "dresses",
      kicker: "New Collection",
      title: "Dresses & Sets",
      desc: "Modern silhouettes for every you.",
      img: "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5",
      url: "dresses.html"
    },
    {
      id: "lehengas",
      kicker: "New Collection",
      title: "Lehengas",
      desc: "Royal silhouettes, timeless grace.",
      img: "https://mahira2.netlify.app/assets/women-clean.jpg?v=3",
      url: "collections.html?category=lehengas"
    },
    {
      id: "anarkalis",
      kicker: "New Collection",
      title: "Anarkali Sets",
      desc: "Voluminous flares & royal grace.",
      img: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1",
      url: "collections.html?category=kurta-sets"
    },
    {
      id: "dupattas",
      kicker: "Heirloom Weaves",
      title: "Dupattas & Stoles",
      desc: "Handwoven organza & metallic gossamer.",
      img: "assets/pakistani-kurti-3.jpg",
      url: "collections.html?category=dupattas"
    },
    {
      id: "fabrics",
      kicker: "Atelier Curations",
      title: "Unstitched Fabrics",
      desc: "Pure Banarasi katan silks & brocades.",
      img: "https://mahira2.netlify.app/assets/s2-card-kala.jpg?v=2",
      url: "collections.html?category=fabrics"
    },
    {
      id: "velvet",
      kicker: "Limited Edition",
      title: "Royal Velvet Edit",
      desc: "Opulent micro-velvet with antique tilla.",
      img: "assets/pakistani-kurti-2.jpg",
      url: "collections.html?category=kurtis"
    }
  ]
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
      let b = '';
      res.on('data', c => b += c);
      res.on('end', () => {
        if (res.statusCode !== 200) {
          console.warn(`saveDoc(${docName}) failed with status ${res.statusCode}:`, b);
          resolve(false);
        } else {
          resolve(true);
        }
      });
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
    // If any slide references a dedicated high-resolution image document, resolve it
    for (let i = 0; i < remote.length; i++) {
      if (typeof remote[i].img === 'string' && remote[i].img.startsWith('firestore:')) {
        const docKey = remote[i].img.replace('firestore:', '');
        const imgDoc = await fetchDoc(docKey);
        if (imgDoc && imgDoc.img) {
          remote[i].img = imgDoc.img;
        }
      }
    }
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

  // Create clean copy of slides for persistence
  const payloadSlides = JSON.parse(JSON.stringify(slides));
  for (let i = 0; i < payloadSlides.length; i++) {
    const s = payloadSlides[i];
    // If slide image is a large base64 data URL (> 50KB), store in dedicated document to prevent 1MB limit
    if (typeof s.img === 'string' && s.img.startsWith('data:image')) {
      const docKey = `atelier_slide_img_${i}`;
      await saveDoc(docKey, { img: s.img, updatedAt: new Date().toISOString() });
      s.img = `firestore:${docKey}`;
    }
  }

  await saveDoc('atelier_carousel', payloadSlides);
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

async function getWomenCollections() {
  const remote = await fetchDoc('atelier_women');
  if (Array.isArray(remote) && remote.length >= 2) {
    if (!_cache) _cache = readLocalFallback();
    _cache.womenCollections = remote;
    return remote;
  }
  const data = await getData();
  return data.womenCollections || DEFAULT_DATA.womenCollections;
}

async function saveWomenCollections(cards) {
  if (!_cache) _cache = readLocalFallback();
  _cache.womenCollections = cards;
  _lastFetchTime = Date.now();
  await saveDoc('atelier_women', cards);
  return cards;
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
  if (data.womenCollections) await saveDoc('atelier_women', data.womenCollections);
  
  const generalData = { ..._cache };
  delete generalData.carouselSlides;
  delete generalData.catalog;
  delete generalData.womenCollections;
  await saveDoc('atelier_data', generalData);
  return _cache;
}

module.exports = {
  getData,
  saveData,
  getCarouselSlides,
  saveCarouselSlides,
  getCatalog,
  saveCatalog,
  getWomenCollections,
  saveWomenCollections
};
