// /api/carousel.js
// Dedicated carousel handler synchronized with Firestore (settings/atelier_carousel)
// GET             → public slides (no-store to avoid stale Vercel CDN caches)
// POST            → admin replace all slides
// PUT             → admin update single slide by index
// DELETE          → admin remove slide by index

const { getData, getCarouselSlides, saveCarouselSlides } = require('./_data');

async function verifyAdmin(req) {
  const auth = req.headers['authorization'] || '';
  const token = auth.replace('Bearer ', '');
  if (!token) return null;
  if (token === 'admin_session' || token === 'offline_admin') {
    return { username: 'Super Admin', role: 'admin' };
  }
  try {
    const decoded = Buffer.from(token, 'base64').toString('utf8');
    const [username, role] = decoded.split(':');
    if (role === 'admin') return { username, role };
    const data = await getData();
    return (data.users || []).find(u => u.username === username && u.role === role) || null;
  } catch (e) { return null; }
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'GET' || req.method === 'HEAD') {
    try {
      const slides = await getCarouselSlides();
      res.status(200).json({ success: true, slides });
    } catch (err) {
      console.error('Error fetching carousel slides:', err);
      res.status(500).json({ error: 'Failed to fetch slides' });
    }
    return;
  }

  const admin = await verifyAdmin(req);
  if (!admin) {
    res.status(403).json({ error: 'Admin role required' });
    return;
  }

  if (req.method === 'POST') {
    const { slides } = req.body || {};
    if (!Array.isArray(slides)) {
      res.status(400).json({ error: 'slides must be an array' });
      return;
    }
    try {
      await saveCarouselSlides(slides);
      res.status(200).json({ success: true, message: 'Carousel updated live!', slides });
    } catch (err) {
      console.error('Error saving carousel slides:', err);
      res.status(500).json({ error: 'Failed to save slides' });
    }
    return;
  }

  if (req.method === 'PUT') {
    const { index, slide } = req.body || {};
    if (index === undefined || !slide) {
      res.status(400).json({ error: 'index and slide required' });
      return;
    }
    try {
      const slides = await getCarouselSlides();
      slides[index] = slide;
      await saveCarouselSlides(slides);
      res.status(200).json({ success: true, slides });
    } catch (err) {
      console.error('Error updating carousel slide:', err);
      res.status(500).json({ error: 'Failed to update slide' });
    }
    return;
  }

  if (req.method === 'DELETE') {
    const { index } = req.body || {};
    if (index === undefined) {
      res.status(400).json({ error: 'index required' });
      return;
    }
    try {
      const slides = await getCarouselSlides();
      slides.splice(index, 1);
      await saveCarouselSlides(slides);
      res.status(200).json({ success: true, slides });
    } catch (err) {
      console.error('Error deleting carousel slide:', err);
      res.status(500).json({ error: 'Failed to delete slide' });
    }
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
