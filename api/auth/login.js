// POST /api/auth/login
const { getData } = require('../_data');

module.exports = (req, res) => {
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

  const { username, password } = req.body || {};
  if (!username || !password) {
    res.status(400).json({ error: 'Username and password required' });
    return;
  }

  const data = getData();
  const user = data.users.find(
    u => u.username === username.trim() && u.password === password.trim()
  );

  if (!user) {
    res.status(401).json({ error: 'Invalid credentials' });
    return;
  }

  // Simple token (username:role encoded)
  const token = Buffer.from(`${user.username}:${user.role}:${Date.now()}`).toString('base64');
  res.status(200).json({
    success: true,
    token,
    role: user.role,
    username: user.username,
    message: `Welcome, ${user.username}!`
  });
};
