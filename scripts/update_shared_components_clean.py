import os
import re

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, "..", "Aleen website"))

def get_header_logo_svg():
    logo_path = os.path.join(SCRIPTS_DIR, "header_logo.svg")
    with open(logo_path, "r", encoding="utf-8") as f:
        return f.read().strip()

LOGO_SVG = get_header_logo_svg()

# 1. CLEAN GLOBAL_HEADER_HTML (strictly ends at </header>)
CLEAN_HEADER_HTML = f"""<!-- ======================= GLOBAL HEADER ======================= -->
<header id="header">
  <button id="menuBtn" class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="mobileNav">
    <span></span><span></span>
  </button>

  <div class="nav-center">
    <nav class="nav-side nav-l" aria-label="Primary">
      <a href="index.html#top">Home</a>
      <a aria-expanded="false" aria-haspopup="true" data-mega="women" href="collections.html">Women</a>
    </nav>
    <span class="logo-space" aria-hidden="true"></span>
    <nav class="nav-side nav-r" aria-label="Collections">
      <a href="collections.html">New Arrivals</a>
      <a href="our-story.html">Our Story</a>
    </nav>
  </div>

  <div class="brand-slot">
    <a class="brand" id="brand" href="index.html" aria-label="Aleen Clothing — home">
      {LOGO_SVG}
    </a>
  </div>

  <div class="nav-utils" style="display: none !important;"></div>

  <!-- mega menus -->
  <div class="mega" id="mega" aria-hidden="true">
    <div class="mega-sheet"></div>
    <div class="mega-inner"></div>
  </div>
</header>
"""

# 2. CLEAN GLOBAL_FOOTER_HTML with centered brand alignment and button lock
FOOT_LOGO_SVG = LOGO_SVG.replace('id="brandLogo"', 'class="aleen-crest-svg foot-brand-logo"')
FOOT_LOGO_SVG = FOOT_LOGO_SVG.replace('id="lgGold"', 'id="fgGoldMaster"')
FOOT_LOGO_SVG = FOOT_LOGO_SVG.replace('url(#lgGold)', 'url(#fgGoldMaster)')
FOOT_LOGO_SVG = FOOT_LOGO_SVG.replace('id="lgWmGold"', 'id="fgWmGoldMaster"')
FOOT_LOGO_SVG = FOOT_LOGO_SVG.replace('url(#lgWmGold)', 'url(#fgWmGoldMaster)')
FOOT_LOGO_SVG = FOOT_LOGO_SVG.replace('id="lgSelGold"', 'id="fgSelGoldMaster"')
FOOT_LOGO_SVG = FOOT_LOGO_SVG.replace('url(#lgSelGold)', 'url(#fgSelGoldMaster)')

CLEAN_FOOTER_HTML = f"""<!-- ======================= GLOBAL FOOTER ======================= -->
<footer id="footer">
  <img class="f-leaves" src="https://mahira2.netlify.app/assets/f-leaves.jpg?v=3" alt="" loading="lazy" decoding="async">
  <img class="f-arch" src="https://mahira2.netlify.app/assets/f-arch.jpg?v=3" alt="" loading="lazy" decoding="async">
  
  <div class="f-statement">
    <svg class="lotus" viewBox="0 0 40 32" aria-hidden="true"><path d="M20 4c2.5 4 2.5 9 0 13-2.5-4-2.5-9 0-13zM12 8c4 2.5 6.5 7 6.5 11.5C14 18 11 13.5 12 8zM28 8c1 5.5-2 10-6.5 11.5 0-4.5 2.5-9 6.5-11.5zM5 14c4.5.7 8.5 3.8 10.5 8C11 22 7 19 5 14zM35 14c-2 5-6 8-10.5 8 2-4.2 6-7.3 10.5-8z"/></svg>
    <p class="f-st-line f-st-line2">A Feeling</p>
    <i class="f-st-rule"></i>
    <p class="f-st-copy">Rooted in tradition. Woven for tomorrow.<br>Thank you for being a part of our story.</p>
  </div>

  <div class="f-main">
    <div class="f-brand">
      <a href="index.html" class="f-logo-link" aria-label="Aleen Clothing Home">
        {FOOT_LOGO_SVG}
      </a>
      <p class="f-about">Thoughtfully curated sarees, kurtas and timeless pieces &mdash; bringing India&rsquo;s finest craftsmanship to your everyday.</p>
    </div>

    <nav class="f-col" aria-label="Shop Aleen">
      <h4>Shop</h4><i></i>
      <a href="collections.html">New Arrivals</a>
      <a href="sarees.html">Sarees</a>
      <a href="kurta-sets.html">Kurta Sets</a>
      <a href="index.html#kalakaari">Kalakaari</a>
      <a href="collections.html">Best Sellers</a>
      <a href="collections.html">All Collections</a>
    </nav>

    <nav class="f-col" aria-label="About Aleen">
      <h4>About</h4><i></i>
      <a href="our-story.html">Our Story</a>
      <a href="the-complete-journey.html">The Complete Journey</a>
      <a href="craftsmanship.html">Craftsmanship</a>
      <a href="sustainability.html">Sustainability</a>
      <a href="journal.html">Journal</a>
      <a href="care-guide.html">Care Guide</a>
      <a href="contact-us.html">Contact Us</a>
    </nav>

    <div class="f-news">
      <h4>Stay In Touch</h4><i></i>
      <p>Be the first to know about new collections, exclusive offers and stories from our artisans.</p>
      <form id="newsForm" novalidate>
        <div class="f-field">
          <input type="email" id="newsEmail" placeholder="Your email address" autocomplete="email" required>
          <button type="submit" aria-label="Subscribe"><svg viewBox="0 0 16 12"><path d="M0 6h12M9 2l4 4-4 4"/></svg></button>
        </div>
        <label class="f-agree"><input type="checkbox"><span></span>I agree to receive updates from Aleen Clothing.</label>
      </form>
      <p class="f-thanks" id="newsThanks" style="display:none; color: var(--gold-light); font-size: 13px; margin-top: 10px;">Thank you. Welcome to the story.</p>
      
      <div class="f-social">
        <a href="https://instagram.com" target="_blank" rel="noopener" aria-label="Instagram"><svg viewBox="0 0 24 24"><rect x="3.5" y="3.5" width="17" height="17" rx="4.5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="0.8" fill="currentColor" stroke="none"/></svg></a>
        <a href="https://facebook.com" target="_blank" rel="noopener" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M14.8 4.5h-2.1a3.4 3.4 0 0 0-3.4 3.4v2.6H7v3h2.3v6h3.1v-6h2.4l.5-3h-2.9V8.2c0-.5.4-.9.9-.9h2z"/></svg></a>
        <a href="https://youtube.com" target="_blank" rel="noopener" aria-label="YouTube"><svg viewBox="0 0 24 24"><rect x="3" y="6.5" width="18" height="11" rx="3"/><path d="m10.2 9.5 4.6 2.5-4.6 2.5z"/></svg></a>
        <a href="https://whatsapp.com" target="_blank" rel="noopener" aria-label="WhatsApp"><svg viewBox="0 0 24 24"><path d="M12 4.2a7.8 7.8 0 0 0-6.7 11.8L4.1 20l4.1-1.1A7.8 7.8 0 1 0 12 4.2z"/><path d="M9.2 9.4c.2-.6.8-.7 1.2-.3l.8 1c.3.3.2.8-.1 1.1l-.5.5c.6 1.2 1.5 2.1 2.7 2.7l.5-.5c.3-.3.8-.4 1.1-.1l1 .8c.4.4.3 1-.3 1.2-3.2 1.6-8-3.2-6.4-6.4z"/></svg></a>
        
        <button type="button" class="f-lock-btn" id="lockModalBtn" aria-label="Atelier Staff Management" title="Atelier Management Portal">
          <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </button>
      </div>
    </div>
  </div>

  <i class="f-orna"></i>
  
  <div class="f-bottom">
    <p>&copy; 2026 Aleen Clothing. All rights reserved.</p>
    <nav aria-label="Legal">
      <a href="privacy.html">Privacy Policy</a><i>|</i>
      <a href="terms.html">Terms &amp; Conditions</a><i>|</i>
      <a href="sitemap.html">Sitemap</a><i>|</i>
      <span class="f-region">India <svg viewBox="0 0 10 6"><path d="m1 1 4 4 4-4"/></svg></span>
    </nav>
    <button id="backTop" aria-label="Back to top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
      <svg viewBox="0 0 12 8"><path d="m1 7 5-5 5 5"/></svg>
      <span>Back to top</span>
    </button>
  </div>
</footer>

<!-- ======================= ATELIER LOCK MODAL ======================= -->
<div class="atelier-lock-modal" id="atelierLockModal" aria-hidden="true" style="display:none;">
  <div class="lock-modal-dialog">
    <button id="lockCloseBtn" class="lock-modal-close" aria-label="Close modal">&times;</button>
    <div class="lock-icon-wrap">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
      </svg>
    </div>
    <p class="lock-eyebrow">Atelier Portal</p>
    <h3 class="lock-title">Staff Authentication</h3>
    <p class="lock-sub">Enter the Atelier passcode to access the garment curation and inventory management console.</p>
    <form id="lockLoginForm" autocomplete="off">
      <input type="password" id="lockPassInput" placeholder="Enter Access Passcode" required class="lock-input" autocomplete="current-password">
      <div id="lockErrorMsg" style="display:none; color: #ff6b6b; font-size: 12.5px; margin-top: 8px; font-family: var(--sans);">Invalid passcode. Please try again.</div>
      <button type="submit" class="lock-btn">✦ Enter Dashboard</button>
    </form>
    <p class="lock-hint">Default Passcode: <code>aleen</code></p>
  </div>
</div>
"""

# 3. GLOBAL_COMPONENTS_CSS with transparent header, realigned brand, and HIDDEN mobile nav
CLEAN_COMPONENTS_CSS = """/* ================= GLOBAL HEADER & FOOTER LUXURY CSS ================= */
:root {
  --void-0: #040906;
  --void-1: #0d1c13;
  --green-deep: #0f1d15;
  --green: #14251b;
  --green-soft: #1d3527;
  --gold-deep: #8a6420;
  --gold: #c9a35f;
  --gold-light: #eccf8b;
  --gold-spark: #f9ecc4;
  --champagne: #d9c08a;
  --cream: #efe4c8;
  --cream-hi: #f7efdc;
  --cream-dim: rgba(238, 228, 205, 0.62);
  --serif: 'Playfair Display', Georgia, serif;
  --serif-i: 'Cormorant Garamond', Georgia, serif;
  --sans: 'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --ease: cubic-bezier(0.22, 0.61, 0.21, 1);
  --ease-io: cubic-bezier(0.77, 0, 0.18, 1);
}

/* Header Transparent by default, luxury blur on scroll */
#header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 clamp(22px, 3.2vw, 64px);
  height: clamp(76px, 8.4vh, 92px);
  background: transparent !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  border-bottom: 1px solid transparent !important;
  box-shadow: none !important;
  transition: background 0.35s ease, backdrop-filter 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
}

#header.is-solid, #header.scrolled {
  background: rgba(4, 9, 6, 0.92) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border-bottom: 1px solid rgba(201, 163, 95, 0.22) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45) !important;
}

.nav-center {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.nav-side {
  display: flex;
  align-items: center;
  gap: clamp(24px, 2.5vw, 48px);
}
.nav-side a {
  font-family: var(--sans);
  font-size: clamp(10.5px, 0.72vw, 12px);
  font-weight: 500;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: #ffffff !important;
  text-decoration: none;
  transition: color 0.3s ease;
}
.nav-side a:hover {
  color: var(--gold-spark) !important;
}

.brand-slot {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: auto;
}
.brand {
  display: inline-block;
  line-height: 0;
  text-decoration: none;
}
.brand svg, #brandLogo {
  height: clamp(68px, 7.2vh, 84px) !important;
  width: auto !important;
  display: block;
}
.logo-space {
  width: clamp(140px, 14vw, 220px);
}

.menu-btn {
  display: none;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
}
.menu-btn span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--gold-light);
  margin: 5px 0;
  transition: 0.3s;
}

/* Mega Menus */
.mega {
  position: fixed;
  top: clamp(76px, 8.4vh, 92px);
  left: 0;
  right: 0;
  z-index: 999;
  display: none;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}
.mega.is-open {
  display: block;
  opacity: 1;
  pointer-events: auto;
}
.mega-sheet {
  position: absolute;
  inset: 0;
  background: rgba(4, 9, 6, 0.97);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border-bottom: 1px solid rgba(201, 163, 95, 0.25);
}
.mega-inner {
  position: relative;
  max-width: 1380px;
  margin: 0 auto;
  padding: 44px 48px;
  display: grid;
  grid-template-columns: 3.2fr 1.8fr;
  gap: 56px;
}
.mega-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 36px;
}
.mega-group h4 {
  font-family: var(--sans);
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold-light);
  margin-bottom: 18px;
  font-weight: 600;
}
.mega-group a {
  display: block;
  font-family: var(--sans);
  font-size: 13.5px;
  color: rgba(233, 224, 200, 0.82);
  text-decoration: none;
  padding: 7px 0;
  transition: all 0.25s ease;
}
.mega-group a:hover {
  color: #ffffff;
  padding-left: 6px;
}
.mega-promo {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(201, 163, 95, 0.3);
  aspect-ratio: 16/10;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
}
.mega-promo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}
.mega-promo:hover img {
  transform: scale(1.04);
}
.mega-promo-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(0deg, rgba(4, 9, 6, 0.9) 0%, rgba(4, 9, 6, 0.2) 60%, transparent 100%);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 24px;
}
.mega-promo-title {
  font-family: var(--serif);
  font-size: 20px;
  color: #ffffff;
  margin-bottom: 4px;
}
.mega-promo-sub {
  font-size: 12px;
  color: var(--gold-light);
  letter-spacing: 0.1em;
}

/* Mobile Nav Drawer strictly hidden unless triggered on small mobile */
.mobile-nav, #mobileNav {
  display: none !important;
  position: fixed;
  inset: 0;
  z-index: 99999;
  background: rgba(4, 9, 6, 0.98);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}
.mobile-nav.is-open, #mobileNav.is-open {
  display: block !important;
}
@media (min-width: 901px) {
  .mobile-nav, #mobileNav {
    display: none !important;
  }
}

/* ======================= GLOBAL FOOTER STYLES ======================= */
#footer {
  position: relative;
  z-index: 50;
  background: #040906 !important;
  color: #ffffff;
  padding: clamp(60px, 8vh, 100px) clamp(24px, 4vw, 72px) 36px;
  border-top: 1px solid rgba(201, 163, 95, 0.22);
  overflow: hidden;
}
.f-leaves, .f-arch {
  position: absolute;
  pointer-events: none;
  opacity: 0.12;
}
.f-leaves { top: 0; right: 0; width: 420px; height: auto; }
.f-arch { bottom: 0; left: 0; width: 380px; height: auto; }

.f-statement {
  position: relative;
  text-align: center;
  max-width: 720px;
  margin: 0 auto clamp(48px, 6vh, 72px);
}
.f-statement .lotus {
  width: 32px;
  height: 26px;
  fill: var(--gold);
  margin-bottom: 14px;
}
.f-st-line2 {
  font-family: var(--serif-i);
  font-size: clamp(26px, 3.2vw, 42px);
  font-style: italic;
  color: var(--gold-light);
  margin-bottom: 12px;
}
.f-st-rule {
  display: block;
  width: 48px;
  height: 1px;
  background: var(--gold);
  margin: 0 auto 16px;
  opacity: 0.6;
}
.f-st-copy {
  font-size: 14px;
  line-height: 1.8;
  color: rgba(233, 224, 200, 0.85);
}

.f-main {
  position: relative;
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2.2fr 1fr 1.2fr 1.8fr;
  gap: clamp(28px, 3.5vw, 64px);
  align-items: start;
}

/* Brand column centered and balanced */
.f-brand {
  position: relative;
  margin-top: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 330px;
  margin: 0 auto;
}
.f-logo-link {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  margin-bottom: 16px;
  width: 100%;
}
.f-logo-link svg, .foot-brand-logo {
  height: clamp(92px, 9.2vw, 122px) !important;
  width: auto !important;
  display: block !important;
  margin: 0 auto !important;
}
.f-about {
  font-family: var(--sans);
  font-size: clamp(13px, 0.9vw, 14px);
  line-height: 1.8;
  color: rgba(233, 224, 200, 0.88);
  max-width: 300px;
  margin: 0 auto;
  text-align: center;
}

/* Nav Columns */
.f-col h4, .f-news h4 {
  font-family: var(--sans);
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold-light);
  margin-bottom: 18px;
  font-weight: 600;
}
.f-col a {
  display: block;
  font-family: var(--sans);
  font-size: 13.5px;
  color: rgba(233, 224, 200, 0.82);
  text-decoration: none;
  padding: 6px 0;
  transition: color 0.25s ease, padding-left 0.25s ease;
}
.f-col a:hover {
  color: #ffffff;
  padding-left: 5px;
}

/* Newsletter */
.f-news p {
  font-size: 13px;
  line-height: 1.7;
  color: rgba(233, 224, 200, 0.8);
  margin-bottom: 16px;
}
.f-field {
  display: flex;
  align-items: center;
  background: rgba(20, 37, 27, 0.6);
  border: 1px solid rgba(201, 163, 95, 0.35);
  border-radius: 999px;
  padding: 4px 6px 4px 18px;
  margin-bottom: 12px;
}
.f-field input {
  background: transparent;
  border: none;
  outline: none;
  color: #ffffff;
  font-size: 13px;
  font-family: var(--sans);
  width: 100%;
}
.f-field button {
  background: var(--gold);
  border: none;
  border-radius: 50%;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #040906;
  transition: transform 0.2s ease, background 0.2s ease;
}
.f-field button:hover {
  background: var(--gold-spark);
  transform: scale(1.06);
}
.f-agree {
  font-size: 11.5px;
  color: rgba(233, 224, 200, 0.65);
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

/* Social & Lock Icon */
.f-social {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 22px;
}
.f-social a, .f-lock-btn {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid rgba(201, 163, 95, 0.35);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-light);
  text-decoration: none;
  background: transparent;
  cursor: pointer;
  padding: 0;
  transition: all 0.25s ease;
}
.f-social a svg, .f-lock-btn svg {
  width: 15px;
  height: 15px;
  stroke: currentColor;
  stroke-width: 1.8;
  fill: none;
}
.f-social a:hover, .f-lock-btn:hover {
  background: rgba(201, 163, 95, 0.2);
  border-color: var(--gold);
  color: var(--gold-spark);
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(201, 163, 95, 0.35);
}

.f-orna {
  display: block;
  max-width: 1400px;
  height: 1px;
  background: rgba(201, 163, 95, 0.2);
  margin: 48px auto 28px;
}

.f-bottom {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: rgba(233, 224, 200, 0.65);
  flex-wrap: wrap;
  gap: 16px;
}
.f-bottom nav {
  display: flex;
  align-items: center;
  gap: 14px;
}
.f-bottom nav a {
  color: rgba(233, 224, 200, 0.7);
  text-decoration: none;
  transition: color 0.2s ease;
}
.f-bottom nav a:hover {
  color: var(--gold-spark);
}
.f-bottom button {
  background: transparent;
  border: 1px solid rgba(201, 163, 95, 0.3);
  color: var(--gold-light);
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 11px;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s ease;
}
.f-bottom button svg {
  width: 10px;
  height: 7px;
  stroke: currentColor;
  stroke-width: 2;
  fill: none;
}
.f-bottom button:hover {
  background: rgba(201, 163, 95, 0.15);
  color: #ffffff;
}

/* Atelier Lock Modal Styles */
.atelier-lock-modal {
  position: fixed;
  inset: 0;
  z-index: 100000;
  background: rgba(4, 9, 6, 0.88);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}
.atelier-lock-modal.is-open {
  opacity: 1 !important;
  pointer-events: auto !important;
}
.lock-modal-dialog {
  background: linear-gradient(145deg, rgba(20, 37, 27, 0.98), rgba(9, 19, 13, 0.98));
  border: 1px solid rgba(201, 163, 95, 0.35);
  border-radius: 18px;
  padding: 40px 36px;
  max-width: 440px;
  width: 100%;
  text-align: center;
  position: relative;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.8), 0 0 35px rgba(201, 163, 95, 0.15);
}
.lock-modal-close {
  position: absolute;
  top: 16px;
  right: 18px;
  background: transparent;
  border: none;
  color: rgba(233, 224, 200, 0.7);
  font-size: 26px;
  cursor: pointer;
  line-height: 1;
}
.lock-modal-close:hover {
  color: #ffffff;
}
.lock-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: 1px solid var(--gold);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-light);
  margin-bottom: 16px;
  background: rgba(201, 163, 95, 0.1);
}
.lock-eyebrow {
  font-size: 11px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--gold-light);
  margin-bottom: 6px;
}
.lock-title {
  font-family: var(--serif);
  font-size: 22px;
  color: #ffffff;
  margin-bottom: 8px;
}
.lock-sub {
  font-size: 13px;
  color: rgba(233, 224, 200, 0.8);
  line-height: 1.6;
  margin-bottom: 24px;
}
.lock-input {
  width: 100%;
  padding: 13px 18px;
  background: rgba(4, 9, 6, 0.8);
  border: 1px solid rgba(201, 163, 95, 0.35);
  border-radius: 8px;
  color: #ffffff;
  font-size: 15px;
  text-align: center;
  margin-bottom: 16px;
  outline: none;
}
.lock-input:focus {
  border-color: var(--gold-light);
  box-shadow: 0 0 14px rgba(201, 163, 95, 0.3);
}
.lock-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, var(--gold) 0%, var(--gold-deep) 100%);
  color: #040906;
  border: none;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.2s ease;
}
.lock-btn:hover {
  background: linear-gradient(135deg, var(--gold-spark) 0%, var(--gold) 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(201, 163, 95, 0.45);
}
.lock-hint {
  font-size: 11.5px;
  color: rgba(201, 163, 95, 0.6);
  margin-top: 16px;
}
.lock-hint code {
  color: var(--gold-light);
  background: rgba(201, 163, 95, 0.12);
  padding: 2px 6px;
  border-radius: 4px;
}

@media (max-width: 1024px) {
  .f-main { grid-template-columns: 1fr 1fr; gap: 40px; }
  .brand-slot { display: none; }
  .menu-btn { display: block; }
}
@media (max-width: 640px) {
  .f-main { grid-template-columns: 1fr; gap: 36px; }
}
"""

# 4. GLOBAL_HEADER_FOOTER_JS
CLEAN_HEADER_FOOTER_JS = """<!-- ================= GLOBAL SCRIPT: MEGA MENUS & ATELIER LOCK ================= -->
<script>
(function() {
  // Mega Menu Data
  const NAV_DATA = {
    women: {
      label: 'Women',
      promo: {
        img: 'https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2',
        title: 'The Women’s Edit',
        line: 'Elegance in every drape.',
        url: 'collections.html'
      },
      groups: [
        {
          title: 'Ethnic Haute Couture',
          items: [
            { name: 'Sarees', url: 'sarees.html' },
            { name: 'Kurta Sets', url: 'kurta-sets.html' },
            { name: 'Anarkali Sets', url: 'anarkali.html' },
            { name: 'Suits', url: 'suits.html' },
            { name: 'Co-ord Sets', url: 'coord-sets.html' },
            { name: 'Lehengas', url: 'lehengas.html' },
            { name: 'Dresses & Sets', url: 'dresses.html' }
          ]
        },
        {
          title: 'Curated Heritage',
          items: [
            { name: 'Kalakaari Artistry', url: 'index.html#kalakaari' },
            { name: 'Banarasi Brocades', url: 'sarees.html' },
            { name: 'Zardozi Masterpieces', url: 'craftsmanship.html' },
            { name: 'Pure Silk Unstitched', url: 'collections.html' }
          ]
        },
        {
          title: 'The Atelier',
          items: [
            { name: 'All Garments Catalog', url: 'collections.html' },
            { name: 'New Arrivals', url: 'collections.html' },
            { name: 'Craftsmanship Story', url: 'craftsmanship.html' },
            { name: 'Atelier Portal Login', url: 'admin.html' }
          ]
        }
      ]
    }
  };

  const header = document.getElementById('header');
  const mega = document.getElementById('mega');
  const megaInner = mega ? mega.querySelector('.mega-inner') : null;

  // Header scroll transition: Transparent over hero, luxury glass blur when scrolled
  function updateHeaderTransparency() {
    if (!header) return;
    if (window.scrollY > 40) {
      header.classList.add('is-solid');
    } else {
      header.classList.remove('is-solid');
    }
  }
  window.addEventListener('scroll', updateHeaderTransparency, { passive: true });
  updateHeaderTransparency();

  // Mega Menu Hover
  if (header && mega && megaInner) {
    const womenTrigger = header.querySelector('a[data-mega="women"]');

    function buildMegaMenu(key) {
      const data = NAV_DATA[key];
      if (!data) return;

      let groupsHtml = '<div class="mega-grid">';
      data.groups.forEach(g => {
        groupsHtml += `<div class="mega-group"><h4>${g.title}</h4>`;
        g.items.forEach(it => {
          groupsHtml += `<a href="${it.url}">${it.name}</a>`;
        });
        groupsHtml += '</div>';
      });
      groupsHtml += '</div>';

      const promoHtml = `
        <a href="${data.promo.url}" class="mega-promo">
          <img src="${data.promo.img}" alt="${data.promo.title}" loading="lazy">
          <div class="mega-promo-overlay">
            <h4 class="mega-promo-title">${data.promo.title}</h4>
            <p class="mega-promo-sub">${data.promo.line}</p>
          </div>
        </a>
      `;

      megaInner.innerHTML = groupsHtml + promoHtml;
    }

    if (womenTrigger) {
      womenTrigger.addEventListener('mouseenter', () => {
        buildMegaMenu('women');
        mega.classList.add('is-open');
        mega.setAttribute('aria-hidden', 'false');
      });
    }

    header.addEventListener('mouseleave', (e) => {
      if (!e.relatedTarget || !mega.contains(e.relatedTarget)) {
        mega.classList.remove('is-open');
        mega.setAttribute('aria-hidden', 'true');
      }
    });

    mega.addEventListener('mouseleave', () => {
      mega.classList.remove('is-open');
      mega.setAttribute('aria-hidden', 'true');
    });
  }

  // Newsletter
  const newsForm = document.getElementById('newsForm');
  const newsThanks = document.getElementById('newsThanks');
  if (newsForm && newsThanks) {
    newsForm.addEventListener('submit', (e) => {
      e.preventDefault();
      newsForm.style.display = 'none';
      newsThanks.style.display = 'block';
    });
  }

  // Reliable Atelier Lock Modal Logic
  const lockModal = document.getElementById('atelierLockModal');
  const lockOpenBtn = document.getElementById('lockModalBtn');
  const lockCloseBtn = document.getElementById('lockCloseBtn');
  const lockForm = document.getElementById('lockLoginForm');
  const lockPassInput = document.getElementById('lockPassInput');
  const lockErrorMsg = document.getElementById('lockErrorMsg');

  function openLockModal() {
    if (!lockModal) return;
    lockModal.classList.add('is-open');
    lockModal.style.display = 'flex';
    lockModal.style.opacity = '1';
    lockModal.style.pointerEvents = 'auto';
    if (lockErrorMsg) lockErrorMsg.style.display = 'none';
    if (lockPassInput) {
      lockPassInput.value = '';
      setTimeout(() => lockPassInput.focus(), 100);
    }
  }

  function closeLockModal() {
    if (!lockModal) return;
    lockModal.classList.remove('is-open');
    lockModal.style.opacity = '0';
    lockModal.style.pointerEvents = 'none';
    setTimeout(() => { lockModal.style.display = 'none'; }, 200);
  }

  if (lockOpenBtn) {
    lockOpenBtn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      openLockModal();
    });
  }

  if (lockCloseBtn) {
    lockCloseBtn.addEventListener('click', function(e) {
      e.preventDefault();
      closeLockModal();
    });
  }

  if (lockModal) {
    lockModal.addEventListener('click', function(e) {
      if (e.target === lockModal) {
        closeLockModal();
      }
    });
  }

  if (lockForm) {
    lockForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const entered = lockPassInput ? lockPassInput.value.trim() : '';
      const masterPass = localStorage.getItem('aleen_admin_password') || 'aleen';
      
      let userList = [];
      try {
        userList = JSON.parse(localStorage.getItem('aleen_users')) || [];
      } catch(err) { userList = []; }
      
      const foundUser = userList.find(u => u.password && u.password === entered);

      if (entered === masterPass || entered === 'aleen' || foundUser) {
        sessionStorage.setItem('aleen_admin_logged', 'true');
        const role = foundUser ? foundUser.role : 'Super Admin';
        const username = foundUser ? foundUser.username : 'Admin';
        sessionStorage.setItem('aleen_current_user', JSON.stringify({ username, role }));
        window.location.href = 'admin.html';
      } else {
        if (lockErrorMsg) {
          lockErrorMsg.style.display = 'block';
          lockErrorMsg.textContent = 'Invalid passcode. Please try again.';
        }
        if (lockPassInput) {
          lockPassInput.select();
          lockPassInput.focus();
        }
      }
    });
  }
})();
</script>
"""

def update_shared_components_file():
    target = os.path.join(SCRIPTS_DIR, "shared_components.py")
    content = f'''"""Shared Header, Footer, CSS, and Scripts for Aleen Website."""

GLOBAL_HEADER_HTML = """{CLEAN_HEADER_HTML}"""

GLOBAL_FOOTER_HTML = """{CLEAN_FOOTER_HTML}"""

GLOBAL_COMPONENTS_CSS = """{CLEAN_COMPONENTS_CSS}"""

GLOBAL_HEADER_FOOTER_JS = """{CLEAN_HEADER_FOOTER_JS}"""
'''
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ scripts/shared_components.py updated cleanly.")

if __name__ == "__main__":
    update_shared_components_file()

