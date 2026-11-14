// /api/catalog.js
// GET  → public catalog list
// POST → admin save catalog (requires auth)
const { getData, saveData } = require('./_data');

function verifyAdmin(req) {
  const auth = req.headers['authorization'] || '';
  const token = auth.replace('Bearer ', '');
  if (!token) return null;
  try {
    const decoded = Buffer.from(token, 'base64').toString('utf8');
    const [username, role] = decoded.split(':');
    const data = getData();
    return data.users.find(u => u.username === username && u.role === role) || null;
  } catch (e) { return null; }
}

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') { res.status(200).end(); return; }

  const data = getData();

  if (req.method === 'GET') {
    res.status(200).json({ catalog: data.catalog || [] });
    return;
  }

  if (req.method === 'POST') {
    if (!verifyAdmin(req)) { res.status(403).json({ error: 'Admin role required' }); return; }
    const { catalog } = req.body || {};
    if (!Array.isArray(catalog)) { res.status(400).json({ error: 'catalog must be an array' }); return; }
    data.catalog = catalog;
    saveData(data);
    res.status(200).json({ success: true, message: 'Catalog updated!', count: catalog.length });
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
