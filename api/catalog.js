// /api/catalog.js
// Dedicated catalog handler synchronized with Firestore (settings/atelier_catalog)
// GET  → public catalog list
// POST → admin save catalog (requires auth)
const { getData, getCatalog, saveCatalog } = require('./_data');
const { verifyAdmin } = require('./_auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');

  if (req.method === 'OPTIONS') { res.status(200).end(); return; }

  if (req.method === 'GET' || req.method === 'HEAD') {
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
    const list = (req.body && (req.body.catalog || req.body.garments)) || (Array.isArray(req.body) ? req.body : null);
    if (!Array.isArray(list)) { res.status(400).json({ error: 'catalog must be an array' }); return; }
    try {
      await saveCatalog(list);
      res.status(200).json({ success: true, message: 'Catalog updated!', count: list.length, garments: list, catalog: list });
    } catch (err) {
      console.error('Error saving catalog:', err);
      res.status(500).json({ error: 'Failed to save catalog' });
    }
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
