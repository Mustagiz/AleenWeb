// POST /api/auth/login
const { getData } = require('../_data');
const { signToken } = require('../_auth');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { passcode, username, password } = req.body || {};
  const pass = (passcode || password || '').trim();
  const user = (username || 'admin').trim();

  if (!pass) {
    res.status(400).json({ error: 'Passcode is required' });
    return;
  }

  if (pass === 'aleen') {
    res.status(401).json({ error: 'Default passcode has been revoked. Access denied.' });
    return;
  }

  const data = await getData();

  let matchedUser = null;
  const masterPass = process.env.ATELIER_ADMIN_PASSWORD || data.masterPassword || 'Aleen@Atelier2026!';
  if (pass === masterPass) {
    matchedUser = { username: 'Super Admin', role: 'admin' };
  } else if (Array.isArray(data.users)) {
    const found = data.users.find(u => u.username.toLowerCase() === user.toLowerCase() && u.password === pass);
    if (found) {
      matchedUser = { username: found.username, role: found.role };
    }
  }

  if (!matchedUser) {
    res.status(401).json({ error: 'Invalid passcode. Access denied.' });
    return;
  }

  const token = signToken(matchedUser);
  res.status(200).json({
    success: true,
    token,
    user: matchedUser,
    role: matchedUser.role,
    username: matchedUser.username,
    message: `Welcome, ${matchedUser.username}!`
  });
};
