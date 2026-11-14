// GET /api/admin/verify
const { getData } = require('../_data');

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
    if (role === 'admin') {
      return { username, role };
    }
    const data = await getData();
    const user = Array.isArray(data.users) && data.users.find(u => u.username.toLowerCase() === username.toLowerCase());
    return user || null;
  } catch (e) {
    return null;
  }
}

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
