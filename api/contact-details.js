// /api/contact-details.js
// GET  → public contact details
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
    res.status(200).json({ success: true, contactDetails: data.contactDetails || {} });
    return;
  }

  if (req.method === 'POST') {
    const admin = await verifyAdmin(req);
    if (!admin) { res.status(403).json({ error: 'Admin role required' }); return; }
    const { contactDetails } = req.body || {};
    if (!contactDetails || typeof contactDetails !== 'object') {
      res.status(400).json({ error: 'contactDetails object is required' });
      return;
    }
    data.contactDetails = {
      boutiqueBadge: contactDetails.boutiqueBadge || 'Pune Flagship Boutique',
      boutiqueTitle: contactDetails.boutiqueTitle || 'Aleen Clothing Atelier',
      addressLine1: contactDetails.addressLine1 || 'Moti Building, Jaan Mohammad Street,',
      addressLine2: contactDetails.addressLine2 || 'Beside Parag wedding Mall, Babajaan Chawk,',
      addressLine3: contactDetails.addressLine3 || 'Pune Maharashtra 411001',
      mapsUrl: contactDetails.mapsUrl || 'https://maps.google.com/?q=Aleen+Clothing+Moti+Building+Jaan+Mohammad+Street+Pune+Maharashtra+411001',
      emailBadge: contactDetails.emailBadge || 'Electronic Mail',
      email: contactDetails.email || 'Contact@aleen.com',
      emailSubtext: contactDetails.emailSubtext || 'Our client liaison desk responds to all inquiries within 4 business hours.',
      conciergeBadge: contactDetails.conciergeBadge || 'Direct Concierge & WhatsApp',
      phone: contactDetails.phone || '+91 98765 43210',
      hours: contactDetails.hours || 'Mon – Sat, 10:00 AM – 7:30 PM IST',
      whatsappMsg: contactDetails.whatsappMsg || 'Hello Aleen Atelier, I would like to inquire about your couture creations.'
    };
    await saveData(data);
    res.status(200).json({ success: true, contactDetails: data.contactDetails });
    return;
  }

  res.status(405).json({ error: 'Method not allowed' });
};
