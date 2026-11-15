// /api/women-collections.js
// Dedicated handler for Women's Collection cards (S03 arched panels)
// Synchronized with Firestore (settings/atelier_women)

const { getData, getWomenCollections, saveWomenCollections } = require('./_data');

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
      const collections = await getWomenCollections();
      res.status(200).json({ success: true, collections });
    } catch (err) {
      console.error('Error fetching women collections:', err);
      res.status(500).json({ error: 'Failed to fetch women collections' });
    }
    return;
  }

  const admin = await verifyAdmin(req);
  if (!admin) {
    res.status(403).json({ error: 'Admin role required' });
    return;
  }

  if (req.method === 'POST') {
    const { collections } = req.body || {};
    if (!Array.isArray(collections) || collections.length < 2) {
      res.status(400).json({ error: 'collections must be an array with at least 2 items' });
      return;
    }
    try {
      await saveWomenCollections(collections);
      res.status(200).json({ success: true, message: 'Women collections updated!', collections });
    } catch (err) {
      console.error('Error saving women collections:', err);
      res.status(500).json({ error: 'Failed to save women collections' });
    }
    return;
  }

  if (req.method === 'PUT') {
    const { index, card } = req.body || {};
    if (index === undefined || !card) {
      res.status(400).json({ error: 'index and card required' });
      return;
    }
    try {
      const collections = await getWomenCollections();
      collections[index] = card;
      await saveWomenCollections(collections);
      res.status(200).json({ success: true, collections });
    } catch (err) {
      console.error('Error updating women collection card:', err);
      res.status(500).json({ error: 'Failed to update card' });
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
      const collections = await getWomenCollections();
      collections.splice(index, 1);
      await saveWomenCollections(collections);
      res.status(200).json({ success: true, collections });
    } catch (err) {
      console.error('Error deleting women collection card:', err);
      res.status(500).json({ error: 'Failed to delete card' });
    }
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
