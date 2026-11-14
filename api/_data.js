// Shared data store for Vercel serverless functions
// Synchronized permanently with Firebase Firestore (aleen-a5c32)

const fs = require('fs');
const path = require('path');
const https = require('https');

const PROJECT_ID = 'aleen-a5c32';
const API_KEY = 'AIzaSyDJOIWVS5LwRfhLLEa_lT51CI6ndQp1eXQ';
const FIRESTORE_URL = `https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)/documents/settings/atelier_data?key=${API_KEY}`;
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
const CACHE_TTL_MS = 3000; // 3-second cache to ensure fast responses and fresh data

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

function fetchFromFirestore() {
  return new Promise((resolve) => {
    const req = https.get(FIRESTORE_URL, { timeout: 3500 }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            const doc = JSON.parse(body);
            const raw = doc.fields?.jsonPayload?.stringValue;
            if (raw) {
              const data = JSON.parse(raw);
              return resolve({ ...DEFAULT_DATA, ...data });
            }
          } catch (e) {
            console.warn('Firestore doc parse error:', e.message);
          }
        }
        resolve(null);
      });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve(null);
    });

    req.on('error', (err) => {
      console.warn('Firestore fetch error:', err.message);
      resolve(null);
    });
  });
}

function saveToFirestore(data) {
  return new Promise((resolve) => {
    const url = new URL(FIRESTORE_URL);
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
      timeout: 4000
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        resolve(res.statusCode === 200);
      });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve(false);
    });

    req.on('error', (err) => {
      console.warn('Firestore write error:', err.message);
      resolve(false);
    });

    req.write(payload);
    req.end();
  });
}

async function getData() {
  const now = Date.now();
  if (_cache && (now - _lastFetchTime < CACHE_TTL_MS)) {
    return _cache;
  }

  const firestoreData = await fetchFromFirestore();
  if (firestoreData) {
    _cache = firestoreData;
    _lastFetchTime = now;
    return _cache;
  }

  if (!_cache) {
    _cache = readLocalFallback();
    _lastFetchTime = now;
  }
  return _cache;
}

async function saveData(data) {
  _cache = { ..._cache, ...data };
  _lastFetchTime = Date.now();

  try {
    fs.writeFileSync(DATA_FILE, JSON.stringify(_cache, null, 2), 'utf8');
  } catch (e) {
    // Vercel source fs is read-only
  }

  await saveToFirestore(_cache);
  return _cache;
}

module.exports = { getData, saveData };
