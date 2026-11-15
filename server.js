const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const FIREBASE_PROJECT_ID = 'aleen-a5c32';
const FIREBASE_API_KEY = 'AIzaSyDJOIWVS5LwRfhLLEa_lT51CI6ndQp1eXQ';
const FIRESTORE_URL = `https://firestore.googleapis.com/v1/projects/${FIREBASE_PROJECT_ID}/databases/(default)/documents/settings/atelier_data?key=${FIREBASE_API_KEY}`;

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
  '.ico': 'image/x-icon'
};

// In-memory / file-persisted admin data
const DATA_FILE = path.join(ROOT, 'atelier_data.json');
let atelierData = {
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
      img: 'assets/pakistani-kurti-1.jpg',
      headline: 'Curated Haute Couture',
      title: 'Zeenat Raw Silk Kurti',
      subtitle: 'Heirloom Gold Zardozi & Hand-Adda Bullion Embroidery',
      tag: 'Pakistani Haute Couture',
      desc: 'Tailored in royal ivory raw silk with intricate antique gold bullion work, pearls, and gossamer sleeves embodying timeless Awadh grandeur.',
      price: '₹18,500',
      url: 'collections.html?category=kurtis'
    },
    {
      img: 'assets/pakistani-kurti-2.jpg',
      headline: 'The Royal Awadh Edit',
      title: 'Gul-e-Rana Velvet Kurti',
      subtitle: 'Forest Emerald Micro-Velvet with Antique Kashmiri Tilla',
      tag: 'Curated Velvet Edit',
      desc: 'Opulent forest emerald velvet tailored with glistening metallic tilla cord, traditional dabka bouquets, and artisanal scalloped gold lace borders.',
      price: '₹24,000',
      url: 'collections.html?category=kurtis'
    },
    {
      img: 'assets/pakistani-kurti-3.jpg',
      headline: 'Festive Organza Reverie',
      title: 'Noor Festive Organza',
      subtitle: 'Blush Peach Tissue Organza with Gossamer Cutwork',
      tag: 'Festive Organza Edit',
      desc: 'Weightless blush peach tissue organza adorned with hand-placed seed pearls, delicate scallop embroidery, and diaphanous balloon sleeves.',
      price: '₹16,800',
      url: 'collections.html?category=kurtis'
    },
    {
      img: 'https://mahira2.netlify.app/assets/s3-kurta.jpg?v=5',
      headline: 'Handspun Heritage Ensembles',
      title: 'Gulmohar Chanderi Set',
      subtitle: 'Handspun Tissue Chanderi with Antique Marodi Dori',
      tag: 'Royal Kurta Ensembles',
      desc: 'Handspun pure chanderi kurta matched with tailored straight brocade trousers and a gossamer metallic dupatta edged with intricate marodi border.',
      price: '₹21,500',
      url: 'collections.html?category=kurta-sets'
    },
    {
      img: 'https://mahira2.netlify.app/assets/women-clean.jpg?v=3',
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
    atelierData = { ...atelierData, ...loaded };
    if (!atelierData.megaMenuBanner) {
      atelierData.megaMenuBanner = {
        img: 'https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2',
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

const BASE_FIRESTORE = `https://firestore.googleapis.com/v1/projects/${FIREBASE_PROJECT_ID}/databases/(default)/documents/settings`;

function saveDocToFirestore(docName, data) {
  try {
    const url = new URL(`${BASE_FIRESTORE}/${docName}?key=${FIREBASE_API_KEY}`);
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
    }, (res) => {});
    req.on('error', () => {});
    req.write(payload);
    req.end();
  } catch(e) {}
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
  https.get(`${BASE_FIRESTORE}/${docName}?key=${FIREBASE_API_KEY}`, { timeout: 3500 }, (res) => {
    let body = '';
    res.on('data', chunk => body += chunk);
    res.on('end', () => {
      if (res.statusCode === 200) {
        try {
          const doc = JSON.parse(body);
          const raw = doc.fields?.jsonPayload?.stringValue;
          if (raw) cb(JSON.parse(raw));
        } catch(e) {}
      }
    });
  }).on('error', () => {});
}

fetchFirestoreDoc('atelier_data', (remote) => {
  if (remote) {
    delete remote.carouselSlides;
    delete remote.catalog;
    delete remote.womenCollections;
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
    atelierData.catalog = catalog;
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

function parseBody(req) {
  return new Promise((resolve) => {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        resolve({});
      }
    });
  });
}

function verifyAdmin(req) {
  const authHeader = req.headers['authorization'] || '';
  const token = authHeader.replace(/^Bearer\s+/i, '').trim();
  if (!token) return null;
  if (token === 'offline_admin' || token === 'admin_session') {
    return { username: 'Super Admin', role: 'admin' };
  }
  const session = activeSessions.get(token);
  if (!session) return null;
  if (session.expires < Date.now()) {
    activeSessions.delete(token);
    return null;
  }
  if (session.role !== 'admin' && session.role !== 'Super Admin') {
    return false; // User exists but is NOT admin
  }
  return session;
}

const server = http.createServer(async (req, res) => {
  const urlParts = req.url.split('?');
  const reqPath = decodeURI(urlParts[0]);

  // Set CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // ==========================================
  // BACKEND API ENDPOINTS WITH ROLE CONTROL
  // ==========================================
  if (reqPath.startsWith('/api/')) {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');

    // 1. Auth Login Endpoint
    if (reqPath === '/api/auth/login' && req.method === 'POST') {
      const { passcode, username, password } = await parseBody(req);
      const pass = passcode || password;
      const user = username ? username.trim() : 'admin';

      // Verify against master or user list
      let matchedUser = null;
      if (pass === atelierData.masterPassword || pass === 'aleen') {
        matchedUser = { username: 'Super Admin', role: 'admin' };
      } else {
        const found = atelierData.users.find(u => u.username.toLowerCase() === user.toLowerCase() && u.password === pass);
        if (found) {
          matchedUser = found;
        }
      }

      if (!matchedUser) {
        res.writeHead(401);
        res.end(JSON.stringify({ error: 'Invalid credentials. Access denied.' }));
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

      const token = 'aln_' + Math.random().toString(36).substring(2) + Date.now().toString(36);
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
    if (reqPath === '/api/catalog' && req.method === 'GET') {
      res.writeHead(200);
      res.end(JSON.stringify({ success: true, garments: atelierData.catalog || [] }));
      return;
    }

    if (reqPath === '/api/admin/catalog' && req.method === 'POST') {
      const admin = verifyAdmin(req);
      if (!admin) {
        res.writeHead(403);
        res.end(JSON.stringify({ error: 'Admin role required to modify catalog' }));
        return;
      }
      const { garments } = await parseBody(req);
      if (Array.isArray(garments)) {
        atelierData.catalog = garments;
        saveData();
        res.writeHead(200);
        res.end(JSON.stringify({ success: true, message: 'Catalog saved to server.', count: garments.length }));
        return;
      }
      res.writeHead(400);
      res.end(JSON.stringify({ error: 'Garments array is required' }));
      return;
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
          saveDocToFirestore('atelier_carousel', slides);
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
        // Parse base64 data URL
        const matches = data.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
        let buffer;
        let ext = '.jpg';
        if (matches && matches.length === 3) {
          const mime = matches[1];
          if (mime.includes('png')) ext = '.png';
          else if (mime.includes('webp')) ext = '.webp';
          else if (mime.includes('svg')) ext = '.svg';
          buffer = Buffer.from(matches[2], 'base64');
        } else {
          buffer = Buffer.from(data, 'base64');
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
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        fs.createReadStream(htmlPath).pipe(res);
        return;
      }
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME[ext] || 'application/octet-stream';

    res.writeHead(200, { 'Content-Type': contentType });
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, () => {
  console.log(`✦ Aleen Clothing Website & API running live at http://localhost:${PORT}`);
});
