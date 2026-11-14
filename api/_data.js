// Shared data store for Vercel serverless functions
// Since Vercel filesystem is ephemeral (read-only source), changes persist per warm instance only
// Data is seeded from atelier_data.json at cold start

const fs = require('fs');
const path = require('path');

// cwd() is the project root on Vercel
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

function loadData() {
  if (_cache) return _cache;
  try {
    if (fs.existsSync(DATA_FILE)) {
      const raw = fs.readFileSync(DATA_FILE, 'utf8');
      _cache = { ...DEFAULT_DATA, ...JSON.parse(raw) };
    } else {
      _cache = { ...DEFAULT_DATA };
    }
  } catch (e) {
    console.error('_data loadData error:', e.message);
    _cache = { ...DEFAULT_DATA };
  }
  return _cache;
}

function saveData(data) {
  _cache = data;
  try {
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2), 'utf8');
  } catch (e) {
    // Vercel source filesystem is read-only — changes are in-memory per warm instance
    console.warn('Could not persist to disk:', e.message);
  }
}

function getData() {
  return loadData();
}

module.exports = { getData, saveData };
