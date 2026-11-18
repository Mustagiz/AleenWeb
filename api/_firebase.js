// /api/_firebase.js
// Authenticated Firestore access for the Aleen atelier backend.
//
// Primary mode: Google service account (OAuth2 JWT-bearer flow). A service account
// is authorised at the IAM layer, so it bypasses Firestore security rules entirely.
// That is what allows /firestore.rules to deny all public access.
//
// Legacy fallback: if no service account is configured but FIREBASE_API_KEY is set,
// requests fall back to the old "?key=" REST call. That mode only works while the
// rules remain open, so it exists purely so a deploy does not break mid-migration.
// Delete FIREBASE_API_KEY once the service account is live.
//
// No third-party dependencies: the JWT assertion is signed with Node's built-in crypto.

const crypto = require('crypto');
const https = require('https');
const fs = require('fs');

const PROJECT_ID = process.env.FIREBASE_PROJECT_ID || 'aleen-a5c32';
const SCOPE = 'https://www.googleapis.com/auth/datastore';
const DEFAULT_TOKEN_URI = 'https://oauth2.googleapis.com/token';
const DOCS_BASE = `https://firestore.googleapis.com/v1/projects/${PROJECT_ID}/databases/(default)/documents/settings`;

let credentials = null;
let credentialsLoaded = false;
let cachedToken = null;
let cachedTokenExpiry = 0;

function parseCredentials(raw) {
  const attempt = (text) => {
    const parsed = JSON.parse(text);
    return parsed && parsed.client_email && parsed.private_key ? parsed : null;
  };
  try {
    return attempt(raw);
  } catch (e) {
    // Private keys pasted into env vars often arrive with literal "\n" sequences.
    try {
      return attempt(raw.replace(/\\n/g, '\n'));
    } catch (e2) {
      return null;
    }
  }
}

function loadCredentials() {
  if (credentialsLoaded) return credentials;
  credentialsLoaded = true;

  try {
    const inlineBase64 = process.env.FIREBASE_SERVICE_ACCOUNT_BASE64;
    const inlineJson = process.env.FIREBASE_SERVICE_ACCOUNT;
    const keyFile = process.env.GOOGLE_APPLICATION_CREDENTIALS;

    if (inlineBase64) {
      credentials = parseCredentials(Buffer.from(inlineBase64, 'base64').toString('utf8'));
    }
    if (!credentials && inlineJson) {
      credentials = parseCredentials(inlineJson);
    }
    if (!credentials && keyFile) {
      credentials = parseCredentials(fs.readFileSync(keyFile, 'utf8'));
    }
  } catch (e) {
    console.error('[firestore] failed to load service account credentials:', e.message);
    credentials = null;
  }
  return credentials;
}

function isConfigured() {
  return Boolean(loadCredentials());
}

// True when we are running on the legacy public-API-key path (rules must be open).
function isLegacyKeyMode() {
  return !isConfigured() && Boolean(process.env.FIREBASE_API_KEY);
}

function base64url(value) {
  return Buffer.from(value).toString('base64url');
}

function buildAssertion(creds) {
  const now = Math.floor(Date.now() / 1000);
  const header = base64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' }));
  const claims = base64url(JSON.stringify({
    iss: creds.client_email,
    scope: SCOPE,
    aud: creds.token_uri || DEFAULT_TOKEN_URI,
    iat: now,
    exp: now + 3600
  }));
  const signer = crypto.createSign('RSA-SHA256');
  signer.update(`${header}.${claims}`);
  const signature = signer.sign(creds.private_key, 'base64url');
  return `${header}.${claims}.${signature}`;
}

function postForm(url, body, timeoutMs) {
  return new Promise((resolve) => {
    const req = https.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': Buffer.byteLength(body)
      },
      timeout: timeoutMs
    }, (res) => {
      let text = '';
      res.on('data', (chunk) => { text += chunk; });
      res.on('end', () => resolve({ status: res.statusCode, body: text }));
    });
    req.on('timeout', () => { req.destroy(); resolve({ status: 0, body: '' }); });
    req.on('error', () => resolve({ status: 0, body: '' }));
    req.write(body);
    req.end();
  });
}

/** Resolves to a bearer token, or null when no service account is available. */
async function getAccessToken() {
  if (cachedToken && Date.now() < cachedTokenExpiry - 60000) return cachedToken;

  const creds = loadCredentials();
  if (!creds) return null;

  let assertion;
  try {
    assertion = buildAssertion(creds);
  } catch (e) {
    console.error('[firestore] could not sign service account assertion:', e.message);
    return null;
  }

  const body =
    `grant_type=${encodeURIComponent('urn:ietf:params:oauth:grant-type:jwt-bearer')}` +
    `&assertion=${encodeURIComponent(assertion)}`;

  const res = await postForm(creds.token_uri || DEFAULT_TOKEN_URI, body, 6000);
  if (res.status !== 200) {
    console.error('[firestore] token exchange failed:', res.status, String(res.body).slice(0, 300));
    return null;
  }

  try {
    const parsed = JSON.parse(res.body);
    if (!parsed.access_token) return null;
    cachedToken = parsed.access_token;
    cachedTokenExpiry = Date.now() + (parsed.expires_in || 3600) * 1000;
    return cachedToken;
  } catch (e) {
    return null;
  }
}

/** Builds the auth material for a Firestore REST call, or null if neither mode is available. */
async function authFor() {
  const token = await getAccessToken();
  if (token) return { headers: { Authorization: `Bearer ${token}` }, suffix: '' };

  const legacyKey = process.env.FIREBASE_API_KEY;
  if (legacyKey) {
    return { headers: {}, suffix: `?key=${encodeURIComponent(legacyKey)}` };
  }
  return null;
}

function docUrl(docName, suffix) {
  return `${DOCS_BASE}/${encodeURIComponent(docName)}${suffix}`;
}

/** Resolves to the stored JSON payload for a settings document, or null. */
async function fetchDoc(docName, timeoutMs = 4000) {
  const auth = await authFor();
  if (!auth) return null;

  return new Promise((resolve) => {
    const req = https.get(docUrl(docName, auth.suffix), { headers: auth.headers, timeout: timeoutMs }, (res) => {
      let text = '';
      res.on('data', (chunk) => { text += chunk; });
      res.on('end', () => {
        if (res.statusCode !== 200) {
          if (res.statusCode !== 404) {
            console.warn(`[firestore] fetchDoc(${docName}) returned ${res.statusCode}`);
          }
          resolve(null);
          return;
        }
        try {
          const doc = JSON.parse(text);
          const raw = doc.fields && doc.fields.jsonPayload && doc.fields.jsonPayload.stringValue;
          resolve(raw ? JSON.parse(raw) : null);
        } catch (e) {
          resolve(null);
        }
      });
    });
    req.on('timeout', () => { req.destroy(); resolve(null); });
    req.on('error', () => resolve(null));
  });
}

/** Writes a settings document. Resolves true when Firestore accepted the write. */
async function saveDoc(docName, data, timeoutMs = 4000) {
  const auth = await authFor();
  if (!auth) return false;

  const payload = JSON.stringify({
    fields: {
      jsonPayload: { stringValue: JSON.stringify(data) },
      updatedAt: { stringValue: new Date().toISOString() }
    }
  });

  return new Promise((resolve) => {
    const target = new URL(docUrl(docName, auth.suffix));
    const headers = Object.assign({}, auth.headers, {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(payload)
    });

    const req = https.request(target, { method: 'PATCH', headers, timeout: timeoutMs }, (res) => {
      let text = '';
      res.on('data', (chunk) => { text += chunk; });
      res.on('end', () => {
        if (res.statusCode !== 200) {
          console.warn(`[firestore] saveDoc(${docName}) returned ${res.statusCode}: ${String(text).slice(0, 200)}`);
          resolve(false);
          return;
        }
        resolve(true);
      });
    });
    req.on('timeout', () => { req.destroy(); resolve(false); });
    req.on('error', () => resolve(false));
    req.write(payload);
    req.end();
  });
}

/**
 * Startup diagnostic: confirms which credential mode is active and that a real
 * round-trip to Firestore succeeds. Useful right after the rules are closed.
 */
async function checkConnection() {
  const mode = isConfigured() ? 'service-account' : (isLegacyKeyMode() ? 'legacy-api-key' : 'none');
  if (mode === 'none') return { ok: false, mode, reason: 'no credentials configured' };

  const payload = await fetchDoc('atelier_data');
  return {
    ok: payload !== null,
    mode,
    reason: payload !== null ? 'read succeeded' : 'read failed (rules or permissions)'
  };
}

module.exports = {
  isConfigured,
  isLegacyKeyMode,
  getAccessToken,
  fetchDoc,
  saveDoc,
  checkConnection
};
