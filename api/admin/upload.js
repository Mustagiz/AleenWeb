// POST /api/admin/upload — base64 image upload
// On Vercel: saves to /tmp (ephemeral) and returns a data URL fallback
const { getData } = require('../_data');
const fs = require('fs');
const path = require('path');

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
  if (!admin) { res.status(403).json({ error: 'Admin role required to upload images' }); return; }

  const { filename, data } = req.body || {};
  if (!data) { res.status(400).json({ error: 'Missing image data' }); return; }

  try {
    const matches = data.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
    let ext = '.jpg';
    let buffer;

    if (matches && matches.length === 3) {
      const mime = matches[1];
      if (mime.includes('png')) ext = '.png';
      else if (mime.includes('webp')) ext = '.webp';
      else if (mime.includes('svg')) ext = '.svg';
      buffer = Buffer.from(matches[2], 'base64');
    } else {
      buffer = Buffer.from(data, 'base64');
    }

    const safeBase = (filename || 'garment').replace(/[^a-zA-Z0-9_\-\.]/g, '_').replace(/\.[^/.]+$/, '');
    const targetFilename = `${Date.now()}_${safeBase}${ext}`;

    // Try writing to public uploads dir first (works locally)
    const uploadsDir = path.join(process.cwd(), 'assets', 'uploads');
    let fileUrl = data; // fallback: return the base64 data URL itself

    try {
      if (!fs.existsSync(uploadsDir)) fs.mkdirSync(uploadsDir, { recursive: true });
      const targetPath = path.join(uploadsDir, targetFilename);
      fs.writeFileSync(targetPath, buffer);
      fileUrl = `/assets/uploads/${targetFilename}`;
    } catch (writeErr) {
      // On Vercel, write to /tmp
      try {
        const tmpPath = path.join('/tmp', targetFilename);
        fs.writeFileSync(tmpPath, buffer);
        // Return data URL since /tmp is not publicly accessible
        fileUrl = data;
      } catch (tmpErr) {
        fileUrl = data; // Last resort: use inline base64
      }
    }

    res.status(200).json({
      success: true,
      url: fileUrl,
      filename: targetFilename
    });
  } catch (err) {
    console.error('Upload error:', err);
    res.status(500).json({ error: 'Failed to process uploaded image' });
  }
};
