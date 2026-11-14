// /api/admin/account.js
// Handles: users (GET/POST/DELETE) + password change (PUT)
const { getData, saveData } = require('../_data');

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
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  if (req.method === 'OPTIONS') { res.status(200).end(); return; }

  const admin = verifyAdmin(req);
  if (!admin) { res.status(403).json({ error: 'Admin role required' }); return; }

  const data = getData();

  // GET → list users
  if (req.method === 'GET') {
    const safeUsers = data.users.map(u => ({ username: u.username, role: u.role, createdAt: u.createdAt }));
    res.status(200).json({ users: safeUsers });
    return;
  }

  // POST → create user
  if (req.method === 'POST') {
    const { username, role, password } = req.body || {};
    if (!username || !password) { res.status(400).json({ error: 'Username and password required' }); return; }
    data.users.push({
      username: username.trim(), role: role || 'Staff', password: password.trim(),
      createdAt: new Date().toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    });
    saveData(data);
    res.status(200).json({ success: true, message: `User '${username}' created.` });
    return;
  }

  // PUT → change password
  if (req.method === 'PUT') {
    const { currentPassword, newPassword } = req.body || {};
    if (!currentPassword || !newPassword) { res.status(400).json({ error: 'currentPassword and newPassword required' }); return; }
    const user = data.users.find(u => u.username === admin.username);
    if (!user || user.password !== currentPassword.trim()) { res.status(401).json({ error: 'Current password is incorrect' }); return; }
    user.password = newPassword.trim();
    saveData(data);
    res.status(200).json({ success: true, message: 'Password updated.' });
    return;
  }

  // DELETE → remove user
  if (req.method === 'DELETE') {
    const { username } = req.body || {};
    if (!username) { res.status(400).json({ error: 'Username required' }); return; }
    data.users = data.users.filter(u => u.username !== username);
    saveData(data);
    res.status(200).json({ success: true, message: `User '${username}' deleted.` });
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
