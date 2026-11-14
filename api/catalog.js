// /api/catalog.js
// Dedicated catalog handler synchronized with Firestore (settings/atelier_catalog)
// GET  → public catalog list
// POST → admin save catalog (requires auth)
const { getData, getCatalog, saveCatalog } = require('./_data');

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
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');

  if (req.method === 'OPTIONS') { res.status(200).end(); return; }

  if (req.method === 'GET') {
    try {
      const catalog = await getCatalog();
      res.status(200).json({ success: true, catalog });
    } catch (err) {
      console.error('Error fetching catalog:', err);
      res.status(500).json({ error: 'Failed to fetch catalog' });
    }
    return;
  }

  const admin = await verifyAdmin(req);
  if (!admin) { res.status(403).json({ error: 'Admin role required' }); return; }

  if (req.method === 'POST') {
    const { catalog } = req.body || {};
    if (!Array.isArray(catalog)) { res.status(400).json({ error: 'catalog must be an array' }); return; }
    try {
      await saveCatalog(catalog);
      res.status(200).json({ success: true, message: 'Catalog updated!', count: catalog.length });
    } catch (err) {
      console.error('Error saving catalog:', err);
      res.status(500).json({ error: 'Failed to save catalog' });
    }
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
