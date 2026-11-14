// POST /api/admin/password — change master password
const { getData, saveData } = require('../_data');

function verifyAdmin(req) {
  const auth = req.headers['authorization'] || '';
  const token = auth.replace('Bearer ', '');
  if (!token) return null;
  try {
    const decoded = Buffer.from(token, 'base64').toString('utf8');
    const [username, role] = decoded.split(':');
    const data = getData();
    const user = data.users.find(u => u.username === username && u.role === role);
    return user || null;
  } catch (e) { return null; }
}

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') { res.status(200).end(); return; }
  if (req.method !== 'POST') { res.status(405).json({ error: 'Method not allowed' }); return; }

  const admin = verifyAdmin(req);
  if (!admin) { res.status(403).json({ error: 'Admin role required' }); return; }

  const { currentPassword, newPassword } = req.body || {};
  if (!currentPassword || !newPassword) {
    res.status(400).json({ error: 'currentPassword and newPassword required' });
    return;
  }

  const data = getData();
  const user = data.users.find(u => u.username === admin.username);
  if (!user || user.password !== currentPassword.trim()) {
    res.status(401).json({ error: 'Current password is incorrect' });
    return;
  }

  user.password = newPassword.trim();
  saveData(data);
  res.status(200).json({ success: true, message: 'Password updated successfully.' });
};
