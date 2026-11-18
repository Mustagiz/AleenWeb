// /api/_ratelimit.js
// Fixed-window attempt limiter for credential endpoints.
//
// State is per process: the Node server keeps one map, and on serverless each
// isolate keeps its own. That still costs a scripted attacker many connections
// per guess attempt instead of letting them hammer a single account freely.

function createLimiter({ max = 8, windowMs = 15 * 60 * 1000, blockMs = 15 * 60 * 1000 } = {}) {
  const hits = new Map();

  function prune(now) {
    if (hits.size < 1000) return;
    for (const [key, entry] of hits) {
      if (now >= entry.resetAt) hits.delete(key);
    }
  }

  return {
    check(key, now = Date.now()) {
      const entry = hits.get(key);
      if (!entry) return { allowed: true, retryAfter: 0 };
      if (now >= entry.resetAt) {
        hits.delete(key);
        return { allowed: true, retryAfter: 0 };
      }
      if (entry.count < max) return { allowed: true, retryAfter: 0 };
      return { allowed: false, retryAfter: Math.ceil((entry.resetAt - now) / 1000) };
    },

    fail(key, now = Date.now()) {
      prune(now);
      const entry = hits.get(key);
      if (!entry || now >= entry.resetAt) {
        hits.set(key, { count: 1, resetAt: now + windowMs });
        return;
      }
      entry.count += 1;
      if (entry.count >= max) entry.resetAt = now + blockMs;
    },

    reset(key) {
      hits.delete(key);
    }
  };
}

// Vercel and other proxies set x-forwarded-for; behind them this is the client
// address. Without a proxy the header is client-controlled, so the socket
// address is used instead.
function clientIp(req) {
  const forwarded = String((req && req.headers && req.headers['x-forwarded-for']) || '')
    .split(',')[0]
    .trim();
  if (forwarded) return forwarded;
  const socket = req && (req.socket || req.connection);
  return (socket && socket.remoteAddress) || 'unknown';
}

module.exports = { createLimiter, clientIp };
