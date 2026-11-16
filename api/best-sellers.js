// /api/best-sellers.js
// GET  → public best sellers
// POST → admin update (requires auth)
const { getData, saveData } = require('./_data');
const { verifyAdmin } = require('./_auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') { res.status(200).end(); return; }

  const data = await getData();

  if (req.method === 'GET') {
    res.status(200).json({ success: true, bestSellers: data.bestSellers || [] });
    return;
  }

  if (req.method === 'POST') {
    const admin = await verifyAdmin(req);
    if (!admin) { res.status(403).json({ error: 'Admin role required' }); return; }
    const { bestSellers } = req.body || {};
    if (!Array.isArray(bestSellers) || bestSellers.length === 0) {
      res.status(400).json({ error: 'bestSellers array is required' });
      return;
    }
    data.bestSellers = bestSellers.slice(0, 4).map((item, idx) => ({
      no: item.no || `0${idx + 1}`,
      title: item.title || 'Haute Couture',
      subtitle: item.subtitle || 'Everyday elegance, redefined.',
      image: item.image || 'assets/s5-p1.jpg?v=1',
      url: item.url || '/collections'
    }));
    await saveData(data);
    res.status(200).json({ success: true, bestSellers: data.bestSellers });
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
