// /api/mega-banner.js
// GET  → public banner
// POST → admin update (requires auth)
const { getData, saveData } = require('./_data');

async function verifyAdmin(req) {
  const auth = req.headers['authorization'] || '';
  const token = auth.replace('Bearer ', '');
  if (!token) return null;
  try {
    const decoded = Buffer.from(token, 'base64').toString('utf8');
    const [username, role] = decoded.split(':');
    const data = await getData();
    return data.users.find(u => u.username === username && u.role === role) || null;
  } catch (e) { return null; }
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') { res.status(200).end(); return; }

  const data = await getData();

  if (req.method === 'GET') {
    res.status(200).json({ banner: data.megaMenuBanner });
    return;
  }

  if (req.method === 'POST') {
    const admin = await verifyAdmin(req);
    if (!admin) { res.status(403).json({ error: 'Admin role required' }); return; }
    const banner = req.body || {};
    if (!banner.img) { res.status(400).json({ error: 'Valid banner with img URL required' }); return; }
    data.megaMenuBanner = banner;
    await saveData(data);
    res.status(200).json({ success: true, banner: data.megaMenuBanner });
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
