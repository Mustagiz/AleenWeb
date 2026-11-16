// GET /api/admin/verify
const { getData } = require('../_data');
const { verifyAdmin } = require('../_auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') { res.status(200).end(); return; }

  const admin = await verifyAdmin(req);
  if (!admin) {
    res.status(401).json({ error: 'Unauthorized' });
    return;
  }
  res.status(200).json({ valid: true, role: admin.role, username: admin.username });
};
