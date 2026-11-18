// /api/_auth.js
// Cryptographically signed HMAC-SHA256 server-side authentication
// Strictly rejects static/unverified tokens (offline_admin, admin_session)

const crypto = require('crypto');

// Passwords that shipped in the source, are public in the git history, and must
// never authenticate again — even if they are still sitting in atelier_data.json
// or in Firestore. The server replaces them with ATELIER_ADMIN_PASSWORD on sync.
const LEAKED_PASSWORDS = new Set(['aleen', 'Aleen@Atelier2026!']);

// Signing key must come from the environment. There is deliberately no default:
// a committed fallback would let anyone forge admin tokens.
const AUTH_SECRET = process.env.ATELIER_AUTH_SECRET;

function requireAuthSecret() {
  if (!AUTH_SECRET) {
    throw new Error(
      'ATELIER_AUTH_SECRET is not set. Add it to .env (see .env.example) or to the Vercel environment variables.'
    );
  }
  return AUTH_SECRET;
}

function signToken(user, ttlMs = 24 * 60 * 60 * 1000) {
  const payload = {
    username: (user && user.username) || 'admin',
    role: (user && user.role) || 'admin',
    iat: Date.now(),
    exp: Date.now() + ttlMs
  };
  const payloadStr = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const signature = crypto.createHmac('sha256', requireAuthSecret()).update(payloadStr).digest('base64url');
  return `${payloadStr}.${signature}`;
}

function verifyToken(token) {
  if (!token || typeof token !== 'string') return null;
  // Strictly reject static fallback tokens
  if (token === 'offline_admin' || token === 'admin_session' || token === 'aleen') {
    return null;
  }

  if (!AUTH_SECRET) return null;

  const parts = token.split('.');
  if (parts.length !== 2) return null;

  const [payloadStr, signature] = parts;
  if (!payloadStr || !signature) return null;

  try {
    const expectedSig = crypto.createHmac('sha256', AUTH_SECRET).update(payloadStr).digest('base64url');
    const sigBuf = Buffer.from(signature);
    const expBuf = Buffer.from(expectedSig);

    if (sigBuf.length !== expBuf.length || !crypto.timingSafeEqual(sigBuf, expBuf)) {
      return null;
    }

    const payload = JSON.parse(Buffer.from(payloadStr, 'base64url').toString('utf8'));
    if (!payload || typeof payload.exp !== 'number' || payload.exp < Date.now()) {
      return null;
    }

    if (payload.role !== 'admin' && payload.role !== 'Super Admin') {
      return false; // Valid token but insufficient role
    }

    return payload;
  } catch (err) {
    return null;
  }
}

function verifyAdmin(req) {
  if (!req || !req.headers) return null;
  const authHeader = req.headers['authorization'] || '';
  const token = authHeader.replace(/^Bearer\s+/i, '').trim();
  return verifyToken(token);
}

module.exports = {
  AUTH_SECRET,
  LEAKED_PASSWORDS,
  signToken,
  verifyToken,
  verifyAdmin
};
