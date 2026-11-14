// /api/carousel.js
// GET             → public slides
// POST            → admin replace all slides
// PUT             → admin update single slide by index
// DELETE          → admin remove slide by index
const { getData, saveData } = require('./_data');

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
    return data.users.find(u => u.username === username && u.role === role) || null;
  } catch (e) { return null; }
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') { res.status(200).end(); return; }

  const data = await getData();

  if (req.method === 'GET') {
    res.status(200).json({ slides: data.carouselSlides || [] });
    return;
  }

  const admin = await verifyAdmin(req);
  if (!admin) { res.status(403).json({ error: 'Admin role required' }); return; }

  if (req.method === 'POST') {
    const { slides } = req.body || {};
    if (!Array.isArray(slides)) { res.status(400).json({ error: 'slides must be an array' }); return; }
    data.carouselSlides = slides;
    await saveData(data);
    res.status(200).json({ success: true, message: 'Carousel updated!', slides: data.carouselSlides });
    return;
  }

  if (req.method === 'PUT') {
    const { index, slide } = req.body || {};
    if (index === undefined || !slide) { res.status(400).json({ error: 'index and slide required' }); return; }
    if (!data.carouselSlides) data.carouselSlides = [];
    data.carouselSlides[index] = slide;
    await saveData(data);
    res.status(200).json({ success: true, slides: data.carouselSlides });
    return;
  }

  if (req.method === 'DELETE') {
    const { index } = req.body || {};
    if (index === undefined) { res.status(400).json({ error: 'index required' }); return; }
    if (data.carouselSlides) { data.carouselSlides.splice(index, 1); await saveData(data); }
    res.status(200).json({ success: true, slides: data.carouselSlides || [] });
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
