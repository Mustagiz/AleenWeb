// /api/social-links.js
// GET  → public social links & email
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
    res.status(200).json({ success: true, socialLinks: data.socialLinks || {} });
    return;
  }

  if (req.method === 'POST') {
    const admin = await verifyAdmin(req);
    if (!admin) { res.status(403).json({ error: 'Admin role required' }); return; }
    const { socialLinks } = req.body || {};
    if (!socialLinks || typeof socialLinks !== 'object') {
      res.status(400).json({ error: 'socialLinks object is required' });
      return;
    }
    data.socialLinks = {
      instagram: socialLinks.instagram || 'https://instagram.com',
      facebook: socialLinks.facebook || 'https://facebook.com',
      youtube: socialLinks.youtube || 'https://youtube.com',
      whatsapp: socialLinks.whatsapp || '+91 98765 43210',
      whatsappMsg: socialLinks.whatsappMsg || 'Hello Aleen Atelier, I would like to connect with a private stylist for bespoke curation.',
      email: socialLinks.email || 'Contact@aleen.com'
    };
    await saveData(data);
    res.status(200).json({ success: true, socialLinks: data.socialLinks });
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
