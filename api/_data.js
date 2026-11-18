// Shared data store for Vercel serverless functions
// Synchronized permanently with Firebase Firestore (aleen-a5c32)
// Uses dedicated documents for carousel slides and catalog to prevent document size limits

const fs = require('fs');
const path = require('path');
const firestore = require('./_firebase');

const DATA_FILE = path.join(process.cwd(), 'atelier_data.json');

const DEFAULT_DATA = {
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
  heroRotator: [],
  carouselSlides: [],
  catalog: [],
    socialLinks: {
    instagram: "https://instagram.com",
    facebook: "https://facebook.com",
    youtube: "https://youtube.com",
    whatsapp: "+91 98765 43210",
    whatsappMsg: "Hello Aleen Atelier, I would like to connect with a private stylist for bespoke curation.",
    email: "Contact@aleen.com"
  },
  contactDetails: {
    boutiqueBadge: "Pune Flagship Boutique",
    boutiqueTitle: "Aleen Clothing Atelier",
    addressLine1: "Moti Building, Jaan Mohammad Street,",
    addressLine2: "Beside Parag wedding Mall, Babajaan Chawk,",
    addressLine3: "Pune Maharashtra 411001",
    mapsUrl: "https://maps.google.com/?q=Aleen+Clothing+Moti+Building+Jaan+Mohammad+Street+Pune+Maharashtra+411001",
    emailBadge: "Electronic Mail",
    email: "Contact@aleen.com",
    emailSubtext: "Our client liaison desk responds to all inquiries within 4 business hours.",
    conciergeBadge: "Direct Concierge & WhatsApp",
    phone: "+91 98765 43210",
    hours: "Mon – Sat, 10:00 AM – 7:30 PM IST",
    whatsappMsg: "Hello Aleen Atelier, I would like to inquire about your couture creations."
  },
  bestSellers: [
    {
      no: "01",
      title: "Pakistani<br>Kurtis",
      subtitle: "Royal grace in<br>every stitch.",
      image: "assets/s5-p1.jpg?v=1",
      url: "/collections?category=kurtis"
    },
    {
      no: "02",
      title: "Kurta Sets",
      subtitle: "Everyday<br>elegance,<br>redefined.",
      image: "assets/s5-p2.jpg?v=1",
      url: "/collections?category=kurta-sets"
    },
    {
      no: "03",
      title: "Organza<br>Kurtis",
      subtitle: "Art in<br>every thread.",
      image: "assets/s5-p3.jpg?v=1",
      url: "/collections?category=kurtis"
    },
    {
      no: "04",
      title: "Kalakaari<br>Collection",
      subtitle: "Stories<br>woven in<br>tradition.",
      image: "assets/s5-p4.jpg?v=1",
      url: "/collections"
    }
  ],
  womenCollections: [
    {
      id: "kurtis",
      kicker: "New Collection",
      title: "Pakistani Kurtis",
      desc: "Royal silhouettes in pure raw silk & velvet.",
      img: "/assets/pakistani-kurti-1.jpg",
      url: "collections.html?category=kurtis"
    },
    {
      id: "kurta-sets",
      kicker: "New Collection",
      title: "Kurta Sets",
      desc: "Everyday elegance, elevated.",
      img: "assets/women-collections/card_1_kurta-sets.jpg",
      url: "collections.html?category=kurta-sets"
    },
    {
      id: "dresses",
      kicker: "New Collection",
      title: "Dresses & Sets",
      desc: "Modern silhouettes for every you.",
      img: "assets/women-collections/card_2_dresses.jpg",
      url: "dresses.html"
    },
    {
      id: "lehengas",
      kicker: "New Collection",
      title: "Lehengas",
      desc: "Royal silhouettes, timeless grace.",
      img: "assets/women-collections/card_3_lehengas.jpg",
      url: "collections.html?category=lehengas"
    },
    {
      id: "anarkalis",
      kicker: "New Collection",
      title: "Anarkali Sets",
      desc: "Voluminous flares & royal grace.",
      img: "assets/women-collections/card_4_anarkalis.jpg",
      url: "collections.html?category=kurta-sets"
    },
    {
      id: "dupattas",
      kicker: "Heirloom Weaves",
      title: "Dupattas & Stoles",
      desc: "Handwoven organza & metallic gossamer.",
      img: "/assets/pakistani-kurti-3.jpg",
      url: "collections.html?category=dupattas"
    },
    {
      id: "fabrics",
      kicker: "Atelier Curations",
      title: "Unstitched Fabrics",
      desc: "Pure Banarasi katan silks & brocades.",
      img: "assets/women-collections/card_6_fabrics.jpg",
      url: "collections.html?category=fabrics"
    },
    {
      id: "velvet",
      kicker: "Limited Edition",
      title: "Royal Velvet Edit",
      desc: "Opulent micro-velvet with antique tilla.",
      img: "/assets/pakistani-kurti-2.jpg",
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
  return firestore.fetchDoc(docName, 3500);
}

function saveDoc(docName, data) {
  return firestore.saveDoc(docName, data, 3000);
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
  const subDocPromises = [];
  for (let i = 0; i < payloadSlides.length; i++) {
    const s = payloadSlides[i];
    // If slide image is a large base64 data URL (> 50KB), store in dedicated document in parallel
    if (typeof s.img === 'string' && s.img.startsWith('data:image')) {
      const docKey = `atelier_slide_img_${i}`;
      subDocPromises.push(saveDoc(docKey, { img: s.img, updatedAt: new Date().toISOString() }));
      s.img = `firestore:${docKey}`;
    }
  }

  if (subDocPromises.length > 0) {
    await Promise.all(subDocPromises);
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

  const payloadCards = JSON.parse(JSON.stringify(cards));
  const subDocPromises = [];
  for (let i = 0; i < payloadCards.length; i++) {
    const c = payloadCards[i];
    if (typeof c.img === 'string' && c.img.startsWith('data:image')) {
      const docKey = `atelier_women_img_${i}`;
      subDocPromises.push(saveDoc(docKey, { img: c.img, updatedAt: new Date().toISOString() }));
      c.img = `firestore:${docKey}`;
    }
  }

  if (subDocPromises.length > 0) {
    await Promise.all(subDocPromises);
  }

  await saveDoc('atelier_women', payloadCards);
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
