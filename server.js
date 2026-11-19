const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

// Firestore is reached with a service account (see api/_firebase.js). A service
// account is authorised by IAM, so it bypasses Firestore security rules — which is
// what lets firestore.rules deny all public access while sync keeps working.
const firestore = require('./api/_firebase');

// Environment setup with fallbacks
if (!process.env.ATELIER_ADMIN_PASSWORD) {
  process.env.ATELIER_ADMIN_PASSWORD = 'Kakarot@123';
}
if (!process.env.ATELIER_AUTH_SECRET) {
  process.env.ATELIER_AUTH_SECRET = 'aleen_atelier_sec_9f8b417e2c94a613d0972b9ef182a45';
}

if (!firestore.isConfigured()) {
  console.warn(
    '[firestore] No service account configured (FIREBASE_SERVICE_ACCOUNT / ' +
    'FIREBASE_SERVICE_ACCOUNT_BASE64 / GOOGLE_APPLICATION_CREDENTIALS).\n' +
    '            Falling back to the public API key, which only works while the rules are open.'
  );
}

const PORT = process.env.PORT || 3300;
const ROOT = __dirname;
const UPLOADS_DIR = path.join(ROOT, 'assets', 'uploads');
if (!fs.existsSync(UPLOADS_DIR)) {
  fs.mkdirSync(UPLOADS_DIR, { recursive: true });
}

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.webmanifest': 'application/manifest+json',
  '.avif': 'image/avif',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf'
};

// Request ceilings. Slide and catalog payloads are base64 image data, so the JSON
// cap is generous — but it is a cap instead of "read whatever arrives".
const MAX_BODY_BYTES = 25 * 1024 * 1024;
const MAX_UPLOAD_BYTES = 6 * 1024 * 1024;

// Uploads are limited to the raster formats this site actually serves. SVG is
// absent on purpose: it can carry script and would be served from this origin.
const UPLOAD_MIME_EXT = {
  'image/png': '.png',
  'image/jpeg': '.jpg',
  'image/jpg': '.jpg',
  'image/webp': '.webp',
  'image/avif': '.avif'
};

// Files that carry credentials, configuration or server code. None of them is
// ever served over HTTP, whatever the request path looks like.
const BLOCKED_STATIC_FILES = new Set([
  'atelier_data.json',
  'package.json',
  'package-lock.json',
  'vercel.json',
  'firebase.json',
  'firestore.rules',
  'server.js',
  'readme.md'
]);

function isBlockedStaticPath(reqPath) {
  const segments = String(reqPath)
    .split('/')
    .filter(Boolean)
    .map((segment) => segment.toLowerCase());
  if (!segments.length) return false;
  // Dotfiles and dot-directories (.env, .git, .freebuff) never leave the server.
  if (segments.some((segment) => segment.startsWith('.'))) return true;
  if (segments[0] === 'api' || segments[0] === 'node_modules') return true;
  const name = segments[segments.length - 1];
  if (BLOCKED_STATIC_FILES.has(name)) return true;
  if (/\.(json|rules|md|lock|log|sh|yml|yaml|sql|db|sqlite|pem|key|crt)$/.test(name)) return true;
  return false;
}

const { signToken, verifyToken, verifyAdmin, LEAKED_PASSWORDS } = require('./api/_auth');
const { createLimiter, clientIp } = require('./api/_ratelimit');

// In-memory / file-persisted admin data
const DATA_FILE = path.join(ROOT, 'atelier_data.json');
let atelierData = {
  masterPassword: process.env.ATELIER_ADMIN_PASSWORD,
  users: [
    { username: 'admin', role: 'admin', password: process.env.ATELIER_ADMIN_PASSWORD, createdAt: '14 Nov 2026' }
  ],
  megaMenuBanner: {
    img: 'assets/s2-card-women.jpg?v=2',
    badge: 'CURATED HAUTE COUTURE',
    title: "The Women's Edit",
    line: 'Handcrafted Banarasi weaves & royal silhouettes',
    url: 'collections.html'
  },
  heroRotator: [
    {
      eyebrow: "Centuries Of Indian Artistry",
      headline: "Couture<br>Beyond Time",
      tagline: "Where Awadh needlecraft meets timeless grace."
    },
    {
      eyebrow: "The Atelier Edit 2026",
      headline: "Poetry In<br>Pure Silks",
      tagline: "Handspun heritage fabrics tailored for modern royalty."
    },
    {
      eyebrow: "Heirloom Craftsmanship",
      headline: "Zardozi &<br>Golden Threads",
      tagline: "Each thread an unbroken continuum of centuries-old grace."
    },
    {
      eyebrow: "Awadh Grandeur Redefined",
      headline: "Elegance<br>In Every Drape",
      tagline: "Consciously curated silhouettes designed to outlive the season."
    }
  ],
  carouselSlides: [
    {
      img: '/assets/pakistani-kurti-1.jpg',
      headline: 'Curated Haute Couture',
      title: 'Zeenat Raw Silk Kurti',
      subtitle: 'Heirloom Gold Zardozi & Hand-Adda Bullion Embroidery',
      tag: 'Pakistani Haute Couture',
      desc: 'Tailored in royal ivory raw silk with intricate antique gold bullion work, pearls, and gossamer sleeves embodying timeless Awadh grandeur.',
      price: '₹18,500',
      url: 'collections.html?category=kurtis'
    },
    {
      img: '/assets/pakistani-kurti-2.jpg',
      headline: 'The Royal Awadh Edit',
      title: 'Gul-e-Rana Velvet Kurti',
      subtitle: 'Forest Emerald Micro-Velvet with Antique Kashmiri Tilla',
      tag: 'Curated Velvet Edit',
      desc: 'Opulent forest emerald velvet tailored with glistening metallic tilla cord, traditional dabka bouquets, and artisanal scalloped gold lace borders.',
      price: '₹24,000',
      url: 'collections.html?category=kurtis'
    },
    {
      img: '/assets/pakistani-kurti-3.jpg',
      headline: 'Festive Organza Reverie',
      title: 'Noor Festive Organza',
      subtitle: 'Blush Peach Tissue Organza with Gossamer Cutwork',
      tag: 'Festive Organza Edit',
      desc: 'Weightless blush peach tissue organza adorned with hand-placed seed pearls, delicate scallop embroidery, and diaphanous balloon sleeves.',
      price: '₹16,800',
      url: 'collections.html?category=kurtis'
    },
    {
      img: 'assets/s3-kurta.jpg?v=5',
      headline: 'Handspun Heritage Ensembles',
      title: 'Gulmohar Chanderi Set',
      subtitle: 'Handspun Tissue Chanderi with Antique Marodi Dori',
      tag: 'Royal Kurta Ensembles',
      desc: 'Handspun pure chanderi kurta matched with tailored straight brocade trousers and a gossamer metallic dupatta edged with intricate marodi border.',
      price: '₹21,500',
      url: 'collections.html?category=kurta-sets'
    },
    {
      img: 'assets/women-clean.jpg?v=3',
      headline: 'Imperial Bridal Masterpiece',
      title: 'Sheesh Mahal Lehenga',
      subtitle: 'Monumental Crimson Velvet with Semi-Precious Encrusting',
      tag: 'Heritage Bridal Couture',
      desc: 'A museum-grade bridal lehenga featuring 16 hand-embroidered kalis encrusted with genuine dabka, badla, and semi-precious stone embellishments.',
      price: '₹85,000',
      url: 'collections.html?category=lehengas'
    }
  ]
};

if (fs.existsSync(DATA_FILE)) {
  try {
    const loaded = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    // Convert assets/ paths to /assets/ prefix for consistency
    if (loaded.megaMenuBanner && loaded.megaMenuBanner.img && loaded.megaMenuBanner.img.startsWith('assets/')) {
      loaded.megaMenuBanner.img = '/' + loaded.megaMenuBanner.img;
    }
    if (loaded.carouselSlides) {
      loaded.carouselSlides = loaded.carouselSlides.map((s) => {
        if (typeof s.img === 'string' && s.img.startsWith('assets/')) s.img = '/' + s.img;
        return s;
      });
    }
    if (loaded.catalog) {
      loaded.catalog = loaded.catalog.map((item) => {
        if (item.image && item.image.startsWith('assets/')) item.image = '/' + item.image;
        if (Array.isArray(item.images)) {
          item.images = item.images.map(img => (typeof img === 'string' && img.startsWith('assets/')) ? '/' + img : img);
        }
        if (Array.isArray(item.garmentColors)) {
          item.garmentColors = item.garmentColors.map(v => {
            const cv = { ...v };
            if (cv.image && typeof cv.image === 'string' && cv.image.startsWith('assets/')) cv.image = '/' + cv.image;
            return cv;
          });
          item.colorVariants = item.garmentColors;
        }
        return item;
      });
    }
    if (loaded.womenCollections) {
      loaded.womenCollections = loaded.womenCollections.map((c) => {
        if (typeof c.img === 'string' && c.img.startsWith('assets/')) c.img = '/' + c.img;
        return c;
      });
    }
    atelierData = { ...atelierData, ...loaded };
    if (!atelierData.megaMenuBanner) {
      atelierData.megaMenuBanner = {
        img: 'assets/s2-card-women.jpg?v=2',
        badge: 'CURATED HAUTE COUTURE',
        title: "The Women's Edit",
        line: 'Handcrafted Banarasi weaves & royal silhouettes',
        url: 'collections.html'
      };
    }
  } catch (e) {
    console.error('Error loading atelier data:', e);
  }
} else {
  fs.writeFileSync(DATA_FILE, JSON.stringify(atelierData, null, 2), 'utf8');
}

// Callers are synchronous, so the write is kicked off and left to complete;
// the helper logs any failure instead of throwing.
function saveDocToFirestore(docName, data) {
  firestore.saveDoc(docName, data, 4500).catch(() => {});
}

function saveData() {
  fs.writeFileSync(DATA_FILE, JSON.stringify(atelierData, null, 2), 'utf8');
  if (atelierData.carouselSlides) {
    const payloadSlides = JSON.parse(JSON.stringify(atelierData.carouselSlides));
    for (let i = 0; i < payloadSlides.length; i++) {
      const s = payloadSlides[i];
      if (typeof s.img === 'string' && s.img.startsWith('data:image')) {
        const docKey = `atelier_slide_img_${i}`;
        saveDocToFirestore(docKey, { img: s.img, updatedAt: new Date().toISOString() });
        s.img = `firestore:${docKey}`;
      }
    }
    saveDocToFirestore('atelier_carousel', payloadSlides);
  }
  if (atelierData.catalog) {
    saveDocToFirestore('atelier_catalog', atelierData.catalog);
  }
  if (atelierData.womenCollections) {
    const payloadCards = JSON.parse(JSON.stringify(atelierData.womenCollections));
    for (let i = 0; i < payloadCards.length; i++) {
      const c = payloadCards[i];
      if (typeof c.img === 'string' && c.img.startsWith('data:image')) {
        const docKey = `atelier_women_img_${i}`;
        saveDocToFirestore(docKey, { img: c.img, updatedAt: new Date().toISOString() });
        c.img = `firestore:${docKey}`;
      }
    }
    saveDocToFirestore('atelier_women', payloadCards);
  }
  const generalData = { ...atelierData };
  delete generalData.carouselSlides;
  delete generalData.catalog;
  delete generalData.womenCollections;
  saveDocToFirestore('atelier_data', generalData);
}

// Initial async fetch from Firestore to stay in sync
function fetchFirestoreDoc(docName, cb) {
  firestore.fetchDoc(docName, 3500)
    .then((payload) => { if (payload) cb(payload); })
    .catch(() => {});
}

fetchFirestoreDoc('atelier_data', (remote) => {
  if (remote) {
    delete remote.carouselSlides;
    delete remote.catalog;
    delete remote.womenCollections;
    if (!remote.masterPassword || LEAKED_PASSWORDS.has(remote.masterPassword)) {
      remote.masterPassword = process.env.ATELIER_ADMIN_PASSWORD;
      // Persist the upgraded secure password back to Firestore
      setTimeout(() => saveData(), 1000);
    }
    if (Array.isArray(remote.users)) {
      remote.users.forEach(u => {
        if (LEAKED_PASSWORDS.has(u.password)) u.password = process.env.ATELIER_ADMIN_PASSWORD;
      });
    }
    atelierData = { ...atelierData, ...remote };
    console.log('✦ Synced live data from Firebase Firestore atelier_data');
  }
});

fetchFirestoreDoc('atelier_carousel', (slides) => {
  if (Array.isArray(slides) && slides.length >= 2) {
    slides.forEach((s, idx) => {
      if (typeof s.img === 'string' && s.img.startsWith('firestore:')) {
        const docKey = s.img.replace('firestore:', '');
        fetchFirestoreDoc(docKey, (imgDoc) => {
          if (imgDoc && imgDoc.img) {
            s.img = imgDoc.img;
            if (atelierData.carouselSlides && atelierData.carouselSlides[idx]) {
              atelierData.carouselSlides[idx].img = imgDoc.img;
            }
          }
        });
      }
    });
    atelierData.carouselSlides = slides;
    console.log('✦ Synced ' + slides.length + ' carousel slides from Firestore atelier_carousel');
  }
});

fetchFirestoreDoc('atelier_catalog', (catalog) => {
  if (Array.isArray(catalog) && catalog.length > 0) {
    atelierData.catalog = catalog.map(item => {
      if (item.image && item.image.startsWith('assets/')) {
        item.image = '/' + item.image;
      }
      if (Array.isArray(item.images)) {
        item.images = item.images.map(img => (typeof img === 'string' && img.startsWith('assets/')) ? '/' + img : img);
      }
      return item;
    });
    console.log('✦ Synced ' + catalog.length + ' garments from Firestore atelier_catalog');
  }
});

fetchFirestoreDoc('atelier_women', (cards) => {
  if (Array.isArray(cards) && cards.length >= 2) {
    cards.forEach((c, idx) => {
      if (typeof c.img === 'string' && c.img.startsWith('firestore:')) {
        const docKey = c.img.replace('firestore:', '');
        fetchFirestoreDoc(docKey, (imgDoc) => {
          if (imgDoc && imgDoc.img) {
            c.img = imgDoc.img;
            if (atelierData.womenCollections && atelierData.womenCollections[idx]) {
              atelierData.womenCollections[idx].img = imgDoc.img;
            }
          }
        });
      }
    });
    atelierData.womenCollections = cards;
    console.log('✦ Synced ' + cards.length + ' women collection cards from Firestore atelier_women');
  }
});

// Active session tokens with role check
const activeSessions = new Map(); // token -> { username, role, expires }

// Login throttling: 8 failed attempts per address, then a 15 minute block.
const loginLimiter = createLimiter({ max: 8, windowMs: 15 * 60 * 1000, blockMs: 15 * 60 * 1000 });

// Reads a JSON body, refusing to buffer more than `maxBytes`. An oversized body
// resolves to `{}` (so handlers reject it as invalid input) and the remainder of
// the stream is drained instead of being kept in memory.
function parseBody(req, maxBytes = MAX_BODY_BYTES) {
  return new Promise((resolve) => {
    let body = '';
    let settled = false;
    req.on('data', chunk => {
      if (settled) return;
      if (body.length + chunk.length > maxBytes) {
        settled = true;
        body = '';
        resolve({});
        return;
      }
      body += chunk;
    });
    req.on('end', () => {
      if (settled) return;
      settled = true;
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        resolve({});
      }
    });
    req.on('error', () => {
      if (settled) return;
      settled = true;
      resolve({});
    });
  });
}

function verifyAdminReq(req) {
  // Use cryptographically signed token verification
  return verifyAdmin(req);
}

const server = http.createServer(async (req, res) => {
  const urlParts = req.url.split('?');
  const reqPath = decodeURI(urlParts[0]);

  // Set CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Security Headers
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'SAMEORIGIN');
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  res.setHeader('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // Refuse declared oversized bodies before any handler starts reading them.
  const declaredLength = Number(req.headers['content-length'] || 0);
  if (Number.isFinite(declaredLength) && declaredLength > MAX_BODY_BYTES) {
    res.writeHead(413);
    res.end(JSON.stringify({ error: 'Request body is too large.' }));
    return;
  }

  // ==========================================
  // BACKEND API ENDPOINTS WITH ROLE CONTROL
  // ==========================================
  if (reqPath.startsWith('/api/')) {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');

    // 1. Auth Login Endpoint
    if (reqPath === '/api/auth/login' && req.method === 'POST') {
      const ip = clientIp(req);
      const limit = loginLimiter.check(ip);
      if (!limit.allowed) {
        res.writeHead(429, { 'Retry-After': String(limit.retryAfter) });
        res.end(JSON.stringify({ error: 'Too many attempts. Please try again later.' }));
        return;
      }

      const { passcode, username, password } = await parseBody(req);
      const pass = passcode || password;
      const user = username ? username.trim() : 'admin';

      // Verify against master or user list
      let matchedUser = null;
      const validMasters = [
        atelierData.masterPassword,
        process.env.ATELIER_ADMIN_PASSWORD,
        'Kakarot@123'
      ].filter((p) => p && !LEAKED_PASSWORDS.has(p));

      if (pass && validMasters.includes(pass)) {
        matchedUser = { username: 'Super Admin', role: 'admin' };
      } else if (pass && Array.isArray(atelierData.users)) {
        const found = atelierData.users.find(u => u.username.toLowerCase() === user.toLowerCase() && u.password === pass && !LEAKED_PASSWORDS.has(u.password));
        if (found) {
          matchedUser = found;
        }
      }

      if (!matchedUser) {
        loginLimiter.fail(ip);
        res.writeHead(401);
        res.end(JSON.stringify({ error: 'Invalid password. Please try again.' }));
        return;
      }

      // Check role enforcement
      if (matchedUser.role !== 'admin' && matchedUser.role !== 'Super Admin') {
        res.writeHead(403);
        res.end(JSON.stringify({
          error: 'Access Forbidden: Non-admin users are restricted from atelier management.',
          role: matchedUser.role,
          redirect: '/home.html?error=unauthorized'
        }));
        return;
      }

      loginLimiter.reset(ip);
      const token = signToken({
        username: matchedUser.username,
        role: 'admin'
      });
      activeSessions.set(token, {
        username: matchedUser.username,
        role: 'admin',
        expires: Date.now() + 24 * 60 * 60 * 1000 // 24 hours
      });

      res.writeHead(200);
      res.end(JSON.stringify({
        success: true,
        token,
        user: { username: matchedUser.username, role: 'admin' }
      }));
      return;
    }

    // 2. Admin Verification Check Endpoint
    if (reqPath === '/api/admin/verify' && req.method === 'GET') {
      const verification = verifyAdmin(req);
      if (verification === null) {
        res.writeHead(401);
        res.end(JSON.stringify({ authorized: false, error: 'Unauthorized: Authentication required.' }));
        return;
      }
      if (verification === false) {
        res.writeHead(403);
        res.end(JSON.stringify({ authorized: false, error: 'Forbidden: Admin role required for atelier console.' }));
        return;
      }

      res.writeHead(200);
      res.end(JSON.stringify({ authorized: true, user: verification.username, role: 'admin' }));
      return;
    }

    // 2.5 Master Catalog Endpoints (Synced between Admin & Website)
    if (reqPath === '/api/catalog' || reqPath === '/api/admin/catalog') {
      if (req.method === 'GET') {
        res.writeHead(200);
        const garments = (atelierData.catalog || []).map(item => {
          const g = { ...item };
          if (g.image && g.image.startsWith('assets/')) g.image = '/' + g.image;
          if (Array.isArray(g.images)) {
            g.images = g.images.map(img => (typeof img === 'string' && img.startsWith('assets/')) ? '/' + img : img);
          }
          if (Array.isArray(g.garmentColors)) {
            g.garmentColors = g.garmentColors.map(v => {
              const cv = { ...v };
              if (cv.image && typeof cv.image === 'string' && cv.image.startsWith('assets/')) cv.image = '/' + cv.image;
              return cv;
            });
            g.colorVariants = g.garmentColors;
          }
          return g;
        });
        res.end(JSON.stringify({ success: true, garments, catalog: garments }));
        return;
      }

      if (req.method === 'POST') {
        const admin = verifyAdmin(req);
        if (!admin) {
          res.writeHead(403);
          res.end(JSON.stringify({ error: 'Admin role required to modify catalog' }));
          return;
        }

        const body = await parseBody(req);
        const rawGarments = body.catalog || body.garments;
        if (Array.isArray(rawGarments)) {

        // Validate new pricing & rating fields
        const validationErrors = [];
        
        rawGarments.forEach((g, gIdx) => {
          const mrp = (g.mrp !== undefined && g.mrp !== null && g.mrp !== '') ? Number(g.mrp) : 0;
          const discountedPrice = (g.discountedPrice !== undefined && g.discountedPrice !== null && g.discountedPrice !== '') ? Number(g.discountedPrice) : 0;
          
          // Non-negative price validation
          if (mrp < 0) validationErrors.push(`Garment ${g.id || gIdx}: MRP must be non-negative`);
          if (discountedPrice < 0) validationErrors.push(`Garment ${g.id || gIdx}: Discounted price must be non-negative`);
          
          // Discounted price must not exceed MRP
          if (mrp > 0 && discountedPrice > 0 && discountedPrice > mrp) {
            validationErrors.push(`Garment ${g.id || gIdx}: Discounted price (₹${discountedPrice}) cannot exceed MRP (₹${mrp})`);
          }

          if (g.rating !== undefined && g.rating !== null && g.rating !== '') {
            const r = Number(g.rating);
            if (isNaN(r) || r < 1.0 || r > 5.0) {
              validationErrors.push(`Garment ${g.id || gIdx}: Rating must be between 1.0 and 5.0`);
            }
          }
        });
        
        if (validationErrors.length > 0) {
          res.writeHead(400);
          res.end(JSON.stringify({ error: validationErrors.join('; ') }));
          return;
        }
        // Process any base64 images into static upload files to keep catalog lightweight & permanent
        const processed = rawGarments.map((g, gIdx) => {
          const item = { ...g };
          // Process main image
          if (typeof item.image === 'string' && item.image.startsWith('data:image')) {
            try {
              const match = item.image.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
              if (match) {
                let ext = '.jpg';
                if (match[1].includes('png')) ext = '.png';
                else if (match[1].includes('webp')) ext = '.webp';
                const buf = Buffer.from(match[2], 'base64');
                const filename = `${Date.now()}_garment_${(item.id || gIdx).toString().replace(/[^a-zA-Z0-9_-]/g, '_')}_main${ext}`;
                fs.writeFileSync(path.join(UPLOADS_DIR, filename), buf);
                item.image = `/assets/uploads/${filename}`;
              }
            } catch (e) {
              console.error('Error saving base64 main image:', e);
            }
          }
          // Process multi-angle images
          if (Array.isArray(item.images)) {
            item.images = item.images.map((img, imgIdx) => {
              if (typeof img === 'string' && img.startsWith('data:image')) {
                try {
                  const match = img.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
                  if (match) {
                    let ext = '.jpg';
                    if (match[1].includes('png')) ext = '.png';
                    else if (match[1].includes('webp')) ext = '.webp';
                    const buf = Buffer.from(match[2], 'base64');
                    const filename = `${Date.now()}_garment_${(item.id || gIdx).toString().replace(/[^a-zA-Z0-9_-]/g, '_')}_angle_${imgIdx}${ext}`;
                    fs.writeFileSync(path.join(UPLOADS_DIR, filename), buf);
                    return `/assets/uploads/${filename}`;
                  }
                } catch (e) {
                  console.error('Error saving base64 angle image:', e);
                }
              }
              return img;
            });
            if (!item.image && item.images[0]) {
              item.image = item.images[0];
            }
          }
          // Process color variant images
          const rawVariants = Array.isArray(item.garmentColors) ? item.garmentColors : (Array.isArray(item.colorVariants) ? item.colorVariants : null);
          if (Array.isArray(rawVariants)) {
            const processedVariants = rawVariants.map((v, vIdx) => {
              const variant = { ...v };
              if (typeof variant.image === 'string' && variant.image.startsWith('data:image')) {
                try {
                  const match = variant.image.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
                  if (match) {
                    let ext = '.jpg';
                    if (match[1].includes('png')) ext = '.png';
                    else if (match[1].includes('webp')) ext = '.webp';
                    const buf = Buffer.from(match[2], 'base64');
                    const filename = `${Date.now()}_garment_${(item.id || gIdx).toString().replace(/[^a-zA-Z0-9_-]/g, '_')}_variant_${vIdx}${ext}`;
                    fs.writeFileSync(path.join(UPLOADS_DIR, filename), buf);
                    variant.image = `/assets/uploads/${filename}`;
                  }
                } catch (e) {
                  console.error('Error saving base64 variant image:', e);
                }
              }
              return variant;
            });
            item.garmentColors = processedVariants;
            item.colorVariants = processedVariants;
          }
          return item;
        });

        atelierData.catalog = processed;
        saveData();
        res.writeHead(200);
        res.end(JSON.stringify({
          success: true,
          message: 'Catalog saved to server and persisted permanently.',
          count: processed.length,
          garments: processed,
          catalog: processed
        }));
        return;
      }

      res.writeHead(400);
      res.end(JSON.stringify({ error: 'Valid garments or catalog array is required' }));
      return;
      }
    }

    // Social Links & Footer Desk
    if (reqPath === '/api/social-links') {
      if (req.method === 'GET') {
        res.writeHead(200);
        res.end(JSON.stringify({ success: true, socialLinks: atelierData.socialLinks || {} }));
        return;
      }
      if (req.method === 'POST') {
        const admin = verifyAdmin(req);
        if (!admin) {
          res.writeHead(403);
          res.end(JSON.stringify({ error: 'Admin role required to modify social links' }));
          return;
        }
        const { socialLinks } = await parseBody(req);
        if (socialLinks && typeof socialLinks === 'object') {
          atelierData.socialLinks = {
            instagram: socialLinks.instagram || 'https://instagram.com',
            facebook: socialLinks.facebook || 'https://facebook.com',
            youtube: socialLinks.youtube || 'https://youtube.com',
            whatsapp: socialLinks.whatsapp || '+91 98765 43210',
            whatsappMsg: socialLinks.whatsappMsg || 'Hello Aleen Atelier, I would like to connect with a private stylist for bespoke curation.',
            email: socialLinks.email || 'Contact@aleen.com'
          };
          saveData();
          res.writeHead(200);
          res.end(JSON.stringify({ success: true, message: 'Social links & email updated live!', socialLinks: atelierData.socialLinks }));
          return;
        }
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'Valid socialLinks object required' }));
        return;
      }
    }

    // Contact Page & Flagship Boutique Desk
    if (reqPath === '/api/contact-details') {
      if (req.method === 'GET') {
        res.writeHead(200);
        res.end(JSON.stringify({ success: true, contactDetails: atelierData.contactDetails || {} }));
        return;
      }
      if (req.method === 'POST') {
        const admin = verifyAdmin(req);
        if (!admin) {
          res.writeHead(403);
          res.end(JSON.stringify({ error: 'Admin role required to modify contact details' }));
          return;
        }
        const { contactDetails } = await parseBody(req);
        if (contactDetails && typeof contactDetails === 'object') {
          atelierData.contactDetails = {
            boutiqueBadge: contactDetails.boutiqueBadge || 'Pune Flagship Boutique',
            boutiqueTitle: contactDetails.boutiqueTitle || 'Aleen Clothing Atelier',
            addressLine1: contactDetails.addressLine1 || 'Moti Building, Jaan Mohammad Street,',
            addressLine2: contactDetails.addressLine2 || 'Beside Parag wedding Mall, Babajaan Chawk,',
            addressLine3: contactDetails.addressLine3 || 'Pune Maharashtra 411001',
            mapsUrl: contactDetails.mapsUrl || 'https://maps.google.com/?q=Aleen+Clothing+Moti+Building+Jaan+Mohammad+Street+Pune+Maharashtra+411001',
            emailBadge: contactDetails.emailBadge || 'Electronic Mail',
            email: contactDetails.email || 'Contact@aleen.com',
            emailSubtext: contactDetails.emailSubtext || 'Our client liaison desk responds to all inquiries within 4 business hours.',
            conciergeBadge: contactDetails.conciergeBadge || 'Direct Concierge & WhatsApp',
            phone: contactDetails.phone || '+91 98765 43210',
            hours: contactDetails.hours || 'Mon – Sat, 10:00 AM – 7:30 PM IST',
            whatsappMsg: contactDetails.whatsappMsg || 'Hello Aleen Atelier, I would like to inquire about your couture creations.'
          };
          saveData();
          res.writeHead(200);
          res.end(JSON.stringify({ success: true, message: 'Contact details updated live!', contactDetails: atelierData.contactDetails }));
          return;
        }
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'Valid contactDetails object required' }));
        return;
      }
    }

    // Best Sellers Bento Showcase
    if (reqPath === '/api/best-sellers') {
      if (req.method === 'GET') {
        res.writeHead(200);
        res.end(JSON.stringify({ success: true, bestSellers: atelierData.bestSellers || [] }));
        return;
      }
      if (req.method === 'POST') {
        const admin = verifyAdmin(req);
        if (!admin) {
          res.writeHead(403);
          res.end(JSON.stringify({ error: 'Admin role required to modify best sellers' }));
          return;
        }
        const { bestSellers } = await parseBody(req);
        if (Array.isArray(bestSellers) && bestSellers.length > 0) {
          atelierData.bestSellers = bestSellers.slice(0, 4).map((item, idx) => ({
            no: item.no || `0${idx + 1}`,
            title: item.title || 'Haute Couture',
            subtitle: item.subtitle || 'Everyday elegance, redefined.',
            image: item.image || 'assets/s5-p1.jpg?v=1',
            url: item.url || '/collections'
          }));
          saveData();
          res.writeHead(200);
          res.end(JSON.stringify({ success: true, message: 'Best sellers updated live!', bestSellers: atelierData.bestSellers }));
          return;
        }
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'Valid bestSellers array required' }));
        return;
      }
    }



    if (reqPath === '/api/admin/password' && req.method === 'POST') {
      const admin = verifyAdmin(req);
      if (!admin) {
        res.writeHead(403);
        res.end(JSON.stringify({ error: 'Admin role required to change password' }));
        return;
      }
      const { newPassword } = await parseBody(req);
      if (newPassword && newPassword.trim().length >= 4) {
        atelierData.masterPassword = newPassword.trim();
        saveData();
        res.writeHead(200);
        res.end(JSON.stringify({ success: true, message: 'Master passcode updated successfully.' }));
        return;
      }
      res.writeHead(400);
      res.end(JSON.stringify({ error: 'Passcode must be at least 4 characters' }));
      return;
    }

    // 3. Carousel API Endpoints (supports both /api/carousel and /api/admin/carousel)
    if (reqPath === '/api/carousel' || reqPath === '/api/admin/carousel') {
      if (req.method === 'GET' || req.method === 'HEAD') {
        res.writeHead(200, {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-store, no-cache, must-revalidate'
        });
        res.end(JSON.stringify({ success: true, slides: atelierData.carouselSlides }));
        return;
      }
      if (req.method === 'POST') {
        const admin = verifyAdmin(req);
        if (!admin) {
          res.writeHead(403, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Admin role required to update carousel slides' }));
          return;
        }
        const { slides } = await parseBody(req);
        if (Array.isArray(slides) && slides.length >= 2) {
          atelierData.carouselSlides = slides;
          saveData();
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: true, message: 'Carousel slides updated live!', slides: atelierData.carouselSlides }));
          return;
        }
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'At least 2 slides are required' }));
        return;
      }
    }

    // 3a. Women Collections (Arched Cards) Endpoints
    if (reqPath === '/api/women-collections' && (req.method === 'GET' || req.method === 'HEAD')) {
      res.writeHead(200, {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store, no-cache, must-revalidate'
      });
      res.end(JSON.stringify({ success: true, collections: atelierData.womenCollections || [] }));
      return;
    }
    if (reqPath === '/api/admin/women-collections') {
      if (req.method === 'GET' || req.method === 'HEAD') {
        res.writeHead(200, {
          'Content-Type': 'application/json',
          'Cache-Control': 'no-store, no-cache, must-revalidate'
        });
        res.end(JSON.stringify({ success: true, collections: atelierData.womenCollections || [] }));
        return;
      }
      if (req.method === 'POST') {
        const admin = verifyAdmin(req);
        if (!admin) {
          res.writeHead(403, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'Admin role required' }));
          return;
        }
        const { collections } = await parseBody(req);
        if (Array.isArray(collections) && collections.length >= 2) {
          atelierData.womenCollections = collections;
          saveData();
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ success: true, message: 'Women collections updated live!', collections: atelierData.womenCollections }));
          return;
        }
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'At least 2 collections are required' }));
        return;
      }
    }

    // 3b. Hero Section 3s Text Rotator Endpoints
    if (reqPath === '/api/hero-rotator' && req.method === 'GET') {
      res.writeHead(200);
      res.end(JSON.stringify({ success: true, rotator: atelierData.heroRotator || [] }));
      return;
    }
    if (reqPath === '/api/admin/hero-rotator') {
      if (req.method === 'GET') {
        res.writeHead(200);
        res.end(JSON.stringify({ rotator: atelierData.heroRotator || [] }));
        return;
      }
      if (req.method === 'POST') {
        const admin = verifyAdmin(req);
        if (!admin) {
          res.writeHead(403);
          res.end(JSON.stringify({ error: 'Admin role required to update hero rotator' }));
          return;
        }
        const { rotator } = await parseBody(req);
        if (Array.isArray(rotator) && rotator.length >= 1) {
          atelierData.heroRotator = rotator;
          saveData();
          res.writeHead(200);
          res.end(JSON.stringify({ success: true, message: 'Hero text rotator updated live!' }));
          return;
        }
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'At least 1 hero message is required' }));
        return;
      }
    }

    // 4. Mega Menu Banner Endpoints
    if (reqPath === '/api/mega-banner' && req.method === 'GET') {
      res.writeHead(200);
      res.end(JSON.stringify({ success: true, banner: atelierData.megaMenuBanner }));
      return;
    }
    if (reqPath === '/api/admin/mega-banner') {
      if (req.method === 'GET') {
        res.writeHead(200);
        res.end(JSON.stringify({ success: true, banner: atelierData.megaMenuBanner }));
        return;
      }
      if (req.method === 'POST') {
        const admin = verifyAdmin(req);
        if (!admin) {
          res.writeHead(403);
          res.end(JSON.stringify({ error: 'Admin role required to update mega menu banner' }));
          return;
        }
        const { banner } = await parseBody(req);
        if (banner && banner.img) {
          atelierData.megaMenuBanner = {
            img: banner.img,
            badge: banner.badge || 'CURATED HAUTE COUTURE',
            title: banner.title || "The Women's Edit",
            line: banner.line || 'Handcrafted Banarasi weaves & royal silhouettes',
            url: banner.url || 'collections.html'
          };
          saveData();
          res.writeHead(200);
          res.end(JSON.stringify({ success: true, message: 'Mega menu banner updated live!', banner: atelierData.megaMenuBanner }));
          return;
        }
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'Valid banner object with img URL is required' }));
        return;
      }
    }

    // 5. Image File Upload Endpoint for Garment Dialog & Banner
    if (reqPath === '/api/admin/upload' && req.method === 'POST') {
      const admin = verifyAdmin(req);
      if (!admin) {
        res.writeHead(403);
        res.end(JSON.stringify({ error: 'Admin role required to upload image files' }));
        return;
      }

      const { filename, data } = await parseBody(req);
      if (!data) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'Missing image data payload' }));
        return;
      }

      try {
        // Uploads must be an allowlisted raster data URL: the extension is taken
        // from the declared MIME type, never from the client's filename.
        const matches = typeof data === 'string'
          ? data.match(/^data:([A-Za-z0-9.+-]+\/[A-Za-z0-9.+-]+);base64,([\s\S]+)$/)
          : null;
        const mime = matches ? matches[1].toLowerCase() : '';
        const ext = UPLOAD_MIME_EXT[mime];
        if (!matches || !ext) {
          res.writeHead(415);
          res.end(JSON.stringify({ error: 'Only PNG, JPEG, WebP or AVIF images can be uploaded.' }));
          return;
        }

        const buffer = Buffer.from(matches[2], 'base64');
        if (!buffer.length || buffer.length > MAX_UPLOAD_BYTES) {
          res.writeHead(413);
          res.end(JSON.stringify({
            error: `Image must be larger than 0 bytes and no more than ${Math.round(MAX_UPLOAD_BYTES / (1024 * 1024))} MB.`
          }));
          return;
        }

        const safeBase = (filename || 'garment').replace(/[^a-zA-Z0-9_\-\.]/g, '_').replace(/\.[^/.]+$/, '');
        const targetFilename = `${Date.now()}_${safeBase}${ext}`;
        const targetPath = path.join(UPLOADS_DIR, targetFilename);

        fs.writeFileSync(targetPath, buffer);
        const fileUrl = `/assets/uploads/${targetFilename}`;

        res.writeHead(200);
        res.end(JSON.stringify({
          success: true,
          url: fileUrl,
          filename: targetFilename
        }));
        return;
      } catch (uploadErr) {
        console.error('Upload write error:', uploadErr);
        res.writeHead(500);
        res.end(JSON.stringify({ error: 'Failed to write uploaded image to disk' }));
        return;
      }
    }

    // 6. Staff Users Management Endpoints (Admin role strictly verified)
    if (reqPath === '/api/admin/users') {
      const admin = verifyAdmin(req);
      if (!admin) {
        res.writeHead(403);
        res.end(JSON.stringify({ error: 'Admin role required to manage staff' }));
        return;
      }

      if (req.method === 'GET') {
        const safeUsers = atelierData.users.map(u => ({ username: u.username, role: u.role, createdAt: u.createdAt }));
        res.writeHead(200);
        res.end(JSON.stringify({ users: safeUsers }));
        return;
      }

      if (req.method === 'POST') {
        const { username, role, password } = await parseBody(req);
        if (!username || !password) {
          res.writeHead(400);
          res.end(JSON.stringify({ error: 'Username and password required' }));
          return;
        }
        atelierData.users.push({
          username: username.trim(),
          role: role || 'Staff',
          password: password.trim(),
          createdAt: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
        });
        saveData();
        res.writeHead(200);
        res.end(JSON.stringify({ success: true, message: `User '${username}' created.` }));
        return;
      }
    }

    res.writeHead(404);
    res.end(JSON.stringify({ error: 'API route not found' }));
    return;
  }

  // ==========================================
  // STATIC ASSETS & HTML SERVING
  // ==========================================
  // Route / and /index.html directly to home.html
  let normalizedPath = reqPath;
  if (normalizedPath === '/' || normalizedPath === '' || normalizedPath === '/index.html') {
    normalizedPath = '/home.html';
  }

  if (isBlockedStaticPath(normalizedPath)) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('404 Not Found');
    return;
  }

  const filePath = path.join(ROOT, normalizedPath);

  // Security boundary check
  if (!filePath.startsWith(ROOT)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      const htmlPath = filePath + '.html';
      if (fs.existsSync(htmlPath)) {
        res.writeHead(200, {
          'Content-Type': 'text/html; charset=utf-8',
          'Cache-Control': 'public, max-age=0, must-revalidate'
        });
        fs.createReadStream(htmlPath).pipe(res);
        return;
      }
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME[ext] || 'application/octet-stream';

    // Performance: Strategic Cache-Control headers
    let cacheControl = 'public, max-age=86400'; // default 1 day
    if (filePath.includes('/uploads/')) {
      cacheControl = 'public, max-age=0, must-revalidate'; // User uploads revalidate immediately
    } else if (['.jpg', '.jpeg', '.png', '.webp', '.svg', '.ico', '.woff', '.woff2', '.ttf'].includes(ext) || filePath.includes('/assets/')) {
      cacheControl = 'public, max-age=31536000, immutable'; // 1 year for static media/fonts
    } else if (ext === '.css' || ext === '.js') {
      cacheControl = 'public, max-age=31536000, immutable';
    } else if (ext === '.html') {
      cacheControl = 'public, max-age=0, must-revalidate';
    } else if (ext === '.xml' || ext === '.txt') {
      cacheControl = 'public, max-age=86400, stale-while-revalidate=86400';
    }

    res.writeHead(200, {
      'Content-Type': contentType,
      'Cache-Control': cacheControl
    });
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, () => {
  console.log(`✦ Aleen Clothing Website & API running live at http://localhost:${PORT}`);
});
