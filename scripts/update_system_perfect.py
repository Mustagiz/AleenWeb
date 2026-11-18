import os
import re

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Aleen website"))

# Read the full header logo SVG from scripts/header_logo.svg
with open(os.path.join(os.path.dirname(__file__), "header_logo.svg"), "r") as f:
    full_header_logo_svg = f.read().strip()

# Create a clean version of this exact SVG for the footer by ensuring gradient IDs are unique to avoid collision
footer_logo_svg = full_header_logo_svg
footer_logo_svg = re.sub(r'id="brandLogo"', 'class="aleen-crest-svg foot-brand-logo"', footer_logo_svg)
footer_logo_svg = footer_logo_svg.replace('id="lgGold"', 'id="fgGoldMaster"')
footer_logo_svg = footer_logo_svg.replace('url(#lgGold)', 'url(#fgGoldMaster)')
footer_logo_svg = footer_logo_svg.replace('id="lgWmGold"', 'id="fgWmGoldMaster"')
footer_logo_svg = footer_logo_svg.replace('url(#lgWmGold)', 'url(#fgWmGoldMaster)')
footer_logo_svg = footer_logo_svg.replace('id="lgSelGold"', 'id="fgSelGoldMaster"')
footer_logo_svg = footer_logo_svg.replace('url(#lgSelGold)', 'url(#fgSelGoldMaster)')

# Standard Header HTML (Home & Women on Left; New Arrivals & Our Story on Right)
GLOBAL_HEADER_HTML = """<!-- ======================= GLOBAL HEADER ======================= -->
<header id="header" class="is-solid">
  <button id="menuBtn" class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="mobileNav">
    <span></span><span></span>
  </button>

  <div class="nav-center">
    <nav class="nav-side nav-l" aria-label="Primary">
      <a href="index.html#top">Home</a>
      <a aria-expanded="false" aria-haspopup="true" data-mega="women" href="index.html#women-new">Women</a>
    </nav>
    <span class="logo-space" aria-hidden="true"></span>
    <nav class="nav-side nav-r" aria-label="Collections">
      <a href="index.html#women-new">New Arrivals</a>
      <a href="our-story.html">Our Story</a>
    </nav>
  </div>

  <div class="brand-slot">
    <a class="brand" id="brand" href="index.html" aria-label="Aleen Clothing — home">
      """ + full_header_logo_svg + """
    </a>
  </div>

  <div class="nav-utils" style="display: none !important;"></div>

  <!-- mega menus -->
  <div class="mega" id="mega" aria-hidden="true">
    <div class="mega-sheet"></div>
    <div class="mega-inner"></div>
  </div>
</header>

<!-- Mobile Navigation Drawer -->
<div class="mobile-nav" id="mobileNav" aria-hidden="true">
  <div class="mn-panel">
    <div class="mn-head">
      <span class="mn-title">Aleen Menu</span>
      <button class="mn-close" id="mnBack" aria-label="Close menu">&times;</button>
    </div>
    <nav class="mn-links">
      <a href="index.html">Home</a>
      <a href="collections.html">All Garments</a>
      <a href="sarees.html">Sarees</a>
      <a href="kurta-sets.html">Kurta Sets</a>
      <a href="anarkali.html">Anarkali</a>
      <a href="suits.html">Suits</a>
      <a href="coord-sets.html">Co-ord Sets</a>
      <a href="lehengas.html">Lehengas</a>
      <a href="dresses.html">Dresses</a>
      <a href="our-story.html">Our Story</a>
      <a href="craftsmanship.html">Craftsmanship</a>
      <a href="admin.html">Atelier Console</a>
    </nav>
  </div>
</div>
"""

# Standard Footer HTML with the exact header logo in footer, clean baseline alignment, and reliable lock modal
GLOBAL_FOOTER_HTML = """<!-- ======================= GLOBAL FOOTER ======================= -->
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
        """ + footer_logo_svg + """
      </a>
      <p class="f-about">Thoughtfully curated sarees, kurtas and timeless pieces &mdash; bringing India&rsquo;s finest craftsmanship to your everyday.</p>
      <p class="f-script">Tradition <span>Lives Beautifully</span></p>
      <i class="f-script-rule"></i>
    </div>

    <nav class="f-col" aria-label="Shop Collections">
      <h4>Shop</h4><i></i>
      <a href="index.html#women-new">New Arrivals</a>
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
        
        <a href="admin.html" class="f-lock-btn" id="lockModalBtn" aria-label="Atelier Staff Management" title="Atelier Management Portal">
          <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </a>
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
    <button id="backTop" aria-label="Back to top" onclick="window.scrollTo({top: 0, behavior: 'smooth'});">
      <span class="bt-circle"><svg viewBox="0 0 12 14"><path d="M6 13V2M2 6l4-4 4 4"/></svg></span>
      <span class="bt-label">Back To Top</span>
    </button>
  </div>
</footer>

<!-- ======================= ATELIER LOCK MODAL ======================= -->
<div class="atelier-lock-modal" id="atelierLockModal" aria-hidden="true">
  <div class="lock-modal-dialog">
    <button id="lockCloseBtn" class="lock-modal-close" aria-label="Close modal">&times;</button>
    <div class="lock-icon-wrap">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
    </div>
    <h3 class="lock-modal-heading">Atelier Management</h3>
    <p class="lock-modal-desc">Sign in to manage, edit, and update garments on your website catalog.</p>
    <form id="lockLoginForm">
      <input type="password" id="lockPassInput" placeholder="Enter Access Passcode" required class="lock-input">
      <button type="submit" class="lock-btn">✦ Enter Dashboard</button>
    </form>
    <p class="lock-hint">Atelier Passcode: <code>aleen</code></p>
  </div>
</div>
"""

GLOBAL_COMPONENTS_CSS = """
/* ================= GLOBAL HEADER & FOOTER LUXURY CSS ================= */
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
  --serif: 'Playfair Display', Georgia, 'Times New Roman', serif;
  --serif-i: 'Cormorant Garamond', Georgia, serif;
  --sans: 'Montserrat', 'Segoe UI', Arial, sans-serif;
  --ease: cubic-bezier(0.22, 0.61, 0.21, 1);
}

/* Header Styles */
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
  background: rgba(4, 9, 6, 0.94);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(201, 163, 95, 0.28);
  transition: all 0.3s ease;
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
  font-size: 11.5px;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #f7efdc;
  text-decoration: none;
  position: relative;
  transition: color 0.25s ease;
}
.nav-side a:hover, .nav-side a.is-open {
  color: var(--gold-light);
}
.nav-side a::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 1px;
  background: var(--gold);
  transition: width 0.3s ease;
}
.nav-side a:hover::after, .nav-side a.is-open::after {
  width: 100%;
}
.logo-space {
  width: clamp(170px, 16vw, 240px);
  flex-shrink: 0;
}

.brand-slot {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  pointer-events: auto;
}
.brand {
  display: block;
  text-decoration: none;
}
.brand svg, .aleen-crest-svg {
  height: clamp(62px, 7vh, 80px);
  width: auto;
  display: block;
}

.menu-btn {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
}
.menu-btn span {
  display: block;
  width: 22px;
  height: 1.5px;
  background: var(--cream);
  margin: 5px 0;
  transition: 0.3s;
}

/* Mega Menu */
.mega {
  position: fixed;
  top: clamp(76px, 8.4vh, 92px);
  left: 0;
  right: 0;
  pointer-events: none;
  opacity: 0;
  transform: translateY(-8px);
  transition: opacity 0.28s var(--ease), transform 0.28s var(--ease);
  z-index: 999;
}
.mega.is-open {
  pointer-events: auto;
  opacity: 1;
  transform: translateY(0);
}
.mega-sheet {
  position: absolute;
  inset: 0;
  background: #f3ebdd;
  background-image: radial-gradient(circle at 10% 20%, rgba(201, 163, 95, 0.15), transparent 45%);
  box-shadow: 0 30px 60px rgba(0, 0, 0, 0.45);
  border-bottom: 1px solid rgba(184, 154, 98, 0.4);
}
.mega-inner {
  position: relative;
  max-width: 1280px;
  margin: 0 auto;
  padding: 40px clamp(24px, 4vw, 60px);
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)) 340px;
  gap: 36px;
  color: #17261b;
}
.mega-col h5 {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: #7c6132;
  margin-bottom: 16px;
  padding-bottom: 6px;
  border-bottom: 1px solid rgba(184, 154, 98, 0.3);
}
.mega-col a {
  display: block;
  font-size: 13.5px;
  color: #17261b;
  text-decoration: none;
  padding: 6px 0;
  transition: color 0.2s ease, transform 0.2s ease;
}
.mega-col a:hover {
  color: #9a7226;
  transform: translateX(4px);
}
.mega-promo {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  height: 220px;
  box-shadow: 0 10px 24px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 20px;
  text-decoration: none;
}
.mega-promo img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.mega-promo::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 30%, rgba(4, 9, 6, 0.85) 100%);
}
.mega-promo-text {
  position: relative;
  z-index: 2;
  color: #fff;
}
.mega-promo-title {
  font-family: var(--serif);
  font-size: 18px;
  color: var(--cream-hi);
  margin-bottom: 4px;
}
.mega-promo-line {
  font-size: 12px;
  color: var(--gold-spark);
}

/* Global Footer Styles with Perfect Alignment */
#footer {
  position: relative;
  background: linear-gradient(180deg, #09150d 0%, #040906 100%);
  color: #f7efdc;
  padding: clamp(60px, 8vh, 90px) clamp(22px, 4vw, 70px) 36px;
  border-top: 1px solid rgba(201, 163, 95, 0.35);
  overflow: hidden;
  z-index: 10;
}
.f-leaves, .f-arch {
  position: absolute;
  pointer-events: none;
  opacity: 0.15;
  mix-blend-mode: luminosity;
}
.f-leaves { top: 0; right: 0; width: 380px; }
.f-arch { bottom: 0; left: 0; width: 420px; }

.f-statement {
  text-align: center;
  max-width: 650px;
  margin: 0 auto clamp(36px, 5vh, 60px);
  position: relative;
  z-index: 2;
}
.f-statement .lotus {
  width: 32px;
  height: 26px;
  fill: var(--gold);
  margin: 0 auto 12px;
  display: block;
}
.f-st-line2 {
  font-family: var(--sans);
  font-size: 12px;
  letter-spacing: 4px;
  text-transform: uppercase;
  color: var(--gold-light);
  margin-bottom: 10px;
}
.f-st-rule {
  display: block;
  width: 44px;
  height: 1px;
  background: var(--gold);
  margin: 0 auto 14px;
  opacity: 0.6;
}
.f-st-copy {
  font-family: var(--serif-i);
  font-size: clamp(17px, 1.4vw, 21px);
  color: var(--cream);
  line-height: 1.6;
}

.f-main {
  position: relative;
  z-index: 2;
  max-width: 1360px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 2.2fr 1fr 1.2fr 1.8fr;
  gap: clamp(28px, 3.5vw, 64px);
  align-items: start;
}

/* Brand column aligned at top with Shop/About */
.f-brand {
  position: relative;
  margin-top: -6px;
}
.f-logo-link {
  display: inline-block;
  text-decoration: none;
  margin-bottom: 16px;
}
.f-logo-link svg, .foot-brand-logo {
  height: clamp(85px, 8.5vw, 115px) !important;
  width: auto !important;
  display: block !important;
}
.f-about {
  font-size: clamp(13px, 0.9vw, 14.5px);
  line-height: 1.8;
  color: rgba(233, 224, 200, 0.88);
  max-width: 380px;
  margin-bottom: 18px;
}
.f-script {
  font-family: 'Great Vibes', var(--serif-i), cursive;
  font-size: clamp(24px, 2vw, 32px);
  line-height: 1.2;
  color: var(--gold-light);
}
.f-script span {
  display: block;
  padding-left: 1.2em;
}
.f-script-rule {
  display: block;
  width: 100px;
  height: 1px;
  background: linear-gradient(90deg, rgba(201,163,95,.8), transparent);
  margin-top: 12px;
}

/* Navigation Columns */
.f-col h4, .f-news h4 {
  font-family: var(--sans);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2.6px;
  text-transform: uppercase;
  color: var(--gold-light);
  margin-bottom: 8px;
  line-height: 1;
}
.f-col i, .f-news i {
  display: block;
  width: 24px;
  height: 1px;
  background: var(--gold);
  margin-bottom: 18px;
  opacity: 0.7;
}
.f-col a {
  display: block;
  font-size: 13.5px;
  color: rgba(247, 239, 220, 0.82);
  text-decoration: none;
  margin-bottom: 10px;
  transition: color 0.2s ease, transform 0.2s ease;
}
.f-col a:hover {
  color: var(--gold-spark);
  transform: translateX(3px);
}

.f-news p {
  font-size: 13.5px;
  line-height: 1.7;
  color: rgba(233, 224, 200, 0.85);
  margin-bottom: 16px;
}
.f-field {
  display: flex;
  position: relative;
  margin-bottom: 12px;
}
.f-field input {
  width: 100%;
  background: rgba(4, 9, 6, 0.65);
  border: 1px solid rgba(201, 163, 95, 0.4);
  border-radius: 999px;
  padding: 12px 50px 12px 18px;
  font-family: var(--sans);
  font-size: 13px;
  color: #fff;
  outline: none;
  transition: border-color 0.25s ease;
}
.f-field input:focus {
  border-color: var(--gold-light);
}
.f-field button {
  position: absolute;
  right: 5px;
  top: 5px;
  bottom: 5px;
  width: 36px;
  background: var(--gold);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.25s ease, transform 0.2s ease;
}
.f-field button:hover {
  background: var(--gold-spark);
  transform: scale(1.05);
}
.f-field button svg {
  width: 14px;
  height: 10px;
  stroke: #241a0c;
  stroke-width: 2;
  fill: none;
}
.f-agree {
  display: flex;
  align-items: center;
  font-size: 11.5px;
  color: rgba(233, 224, 200, 0.7);
  gap: 8px;
  cursor: pointer;
}
.f-agree input {
  accent-color: var(--gold);
}

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
  background: rgba(201, 163, 95, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-light);
  text-decoration: none;
  transition: all 0.25s ease;
  cursor: pointer;
}
.f-social a:hover, .f-lock-btn:hover {
  background: var(--gold);
  color: #241a0c;
  border-color: var(--gold-spark);
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(201, 163, 95, 0.3);
}
.f-social a svg, .f-lock-btn svg {
  width: 16px;
  height: 16px;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
}

.f-orna {
  display: block;
  width: 100%;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(201, 163, 95, 0.3), transparent);
  margin: clamp(36px, 5vh, 50px) 0 24px;
}

.f-bottom {
  max-width: 1360px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12.5px;
  color: rgba(233, 224, 200, 0.65);
}
.f-bottom nav {
  display: flex;
  align-items: center;
  gap: 12px;
}
.f-bottom nav a {
  color: inherit;
  text-decoration: none;
  transition: color 0.2s ease;
}
.f-bottom nav a:hover {
  color: var(--gold-light);
}
.f-bottom nav i {
  color: rgba(201, 163, 95, 0.3);
}
.f-region {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--gold-light);
}
.f-region svg {
  width: 8px;
  height: 5px;
  stroke: currentColor;
  stroke-width: 1.5;
  fill: none;
}
#backTop {
  background: none;
  border: none;
  color: var(--gold-light);
  font-family: var(--sans);
  font-size: 11.5px;
  font-weight: 600;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: color 0.25s ease;
}
#backTop:hover {
  color: var(--gold-spark);
}
.bt-circle {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 1px solid rgba(201, 163, 95, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s ease;
}
#backTop:hover .bt-circle {
  background: var(--gold);
  border-color: var(--gold-spark);
}
#backTop:hover .bt-circle svg {
  stroke: #241a0c;
}
.bt-circle svg {
  width: 10px;
  height: 12px;
  stroke: var(--gold-light);
  stroke-width: 2;
  fill: none;
}

/* Atelier Lock Modal Styles */
.atelier-lock-modal {
  position: fixed !important;
  inset: 0 !important;
  z-index: 100000 !important;
  background: rgba(4, 9, 6, 0.88) !important;
  backdrop-filter: blur(14px) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 20px !important;
  opacity: 0 !important;
  pointer-events: none !important;
  transition: opacity 0.3s ease !important;
}
.atelier-lock-modal.is-open {
  opacity: 1 !important;
  pointer-events: auto !important;
}
.lock-modal-dialog {
  background: linear-gradient(135deg, #112318 0%, #07100a 100%);
  border: 1px solid rgba(201, 163, 95, 0.5);
  box-shadow: 0 24px 60px rgba(0,0,0,0.85);
  border-radius: 20px;
  max-width: 420px;
  width: 100%;
  padding: 34px 30px;
  text-align: center;
  position: relative;
}
.lock-modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  background: none;
  border: none;
  color: var(--cream);
  font-size: 24px;
  cursor: pointer;
}
.lock-icon-wrap {
  width: 52px;
  height: 52px;
  margin: 0 auto 16px;
  border-radius: 50%;
  background: rgba(201, 163, 95, 0.15);
  border: 1px solid var(--gold);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-light);
}
.lock-modal-heading {
  font-family: var(--serif);
  font-size: 22px;
  font-weight: 500;
  color: var(--cream-hi);
  margin-bottom: 6px;
}
.lock-modal-desc {
  font-size: 13px;
  color: var(--cream);
  opacity: 0.8;
  margin-bottom: 22px;
  line-height: 1.5;
}
.lock-input {
  width: 100%;
  padding: 12px 18px;
  background: rgba(4, 9, 6, 0.8);
  border: 1px solid rgba(201, 163, 95, 0.4);
  border-radius: 999px;
  color: #ffffff;
  font-size: 14px;
  text-align: center;
  outline: none;
  margin-bottom: 16px;
}
.lock-input:focus {
  border-color: var(--gold-light);
}
.lock-btn {
  width: 100%;
  padding: 12px 24px;
  background: var(--gold);
  color: #241A0C;
  border: 1px solid var(--gold-light);
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.25s ease;
}
.lock-btn:hover {
  background: var(--gold-spark);
  transform: translateY(-2px);
}
.lock-hint {
  font-size: 11px;
  margin-top: 14px;
  opacity: 0.6;
  color: var(--cream);
}

@media (max-width: 1024px) {
  .f-main {
    grid-template-columns: 1fr 1fr;
    gap: 40px;
  }
  .f-brand, .f-news {
    grid-column: span 2;
  }
}
@media (max-width: 768px) {
  .nav-center { display: none; }
  .menu-btn { display: block; }
  .f-main {
    grid-template-columns: 1fr;
  }
  .f-brand, .f-news {
    grid-column: span 1;
  }
  .f-bottom {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
}
"""

GLOBAL_HEADER_FOOTER_JS = """
<!-- ================= GLOBAL SCRIPT: MEGA MENUS & ATELIER LOCK ================= -->
<script>
(function() {
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
            { name: 'Anarkali', url: 'anarkali.html' },
            { name: 'Suits', url: 'suits.html' },
            { name: 'Co-ord Sets', url: 'coord-sets.html' },
            { name: 'Lehengas', url: 'lehengas.html' },
            { name: 'Dresses', url: 'dresses.html' }
          ]
        }
      ]
    }
  };

  const header = document.getElementById('header');
  const mega = document.getElementById('mega');
  const menuBtn = document.getElementById('menuBtn');
  const mobileNav = document.getElementById('mobileNav');
  const mnBack = document.getElementById('mnBack');
  let megaTimer = null;

  function renderMega(key) {
    if (!mega) return;
    const data = NAV_DATA[key];
    if (!data) return;
    const inner = mega.querySelector('.mega-inner');
    if (!inner) return;

    let html = '';
    data.groups.forEach(group => {
      html += '<div class="mega-col">';
      html += '<h5>' + group.title + '</h5>';
      group.items.forEach(it => {
        html += '<a href="' + it.url + '">' + it.name + '</a>';
      });
      html += '</div>';
    });

    if (data.promo) {
      html += '<a href="' + data.promo.url + '" class="mega-promo">';
      html += '<img src="' + data.promo.img + '" alt="' + data.promo.title + '" loading="lazy" />';
      html += '<div class="mega-promo-text">';
      html += '<h4 class="mega-promo-title">' + data.promo.title + '</h4>';
      html += '<p class="mega-promo-line">' + data.promo.line + '</p>';
      html += '</div></a>';
    }

    inner.innerHTML = html;
  }

  function openMega(key) {
    clearTimeout(megaTimer);
    if (!mega) return;
    renderMega(key);
    mega.classList.add('is-open');
    mega.setAttribute('aria-hidden', 'false');
    document.querySelectorAll('.nav-side a[data-mega]').forEach(a => {
      a.classList.toggle('is-open', a.getAttribute('data-mega') === key);
    });
  }

  function closeMega() {
    if (!mega) return;
    mega.classList.remove('is-open');
    mega.setAttribute('aria-hidden', 'true');
    document.querySelectorAll('.nav-side a[data-mega]').forEach(a => {
      a.classList.remove('is-open');
    });
  }

  document.querySelectorAll('.nav-side a[data-mega]').forEach(a => {
    const key = a.getAttribute('data-mega');
    a.addEventListener('mouseenter', () => openMega(key));
    a.addEventListener('focus', () => openMega(key));
  });

  document.querySelectorAll('.nav-side a:not([data-mega])').forEach(a => {
    a.addEventListener('mouseenter', () => {
      megaTimer = setTimeout(closeMega, 80);
    });
  });

  if (header) {
    header.addEventListener('mouseleave', () => {
      megaTimer = setTimeout(closeMega, 160);
    });
  }
  if (mega) {
    mega.addEventListener('mouseenter', () => clearTimeout(megaTimer));
    mega.addEventListener('mouseleave', () => {
      megaTimer = setTimeout(closeMega, 160);
    });
  }

  // Mobile menu toggle
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener('click', () => {
      const open = mobileNav.classList.toggle('is-open');
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }
  if (mnBack && mobileNav) {
    mnBack.addEventListener('click', () => {
      mobileNav.classList.remove('is-open');
      document.body.style.overflow = '';
    });
  }

  // Newsletter submission
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

  if (lockOpenBtn && lockModal) {
    lockOpenBtn.addEventListener('click', function(e) {
      e.preventDefault();
      lockModal.classList.add('is-open');
      lockModal.style.opacity = '1';
      lockModal.style.pointerEvents = 'auto';
      if (lockPassInput) {
        lockPassInput.value = '';
        setTimeout(() => lockPassInput.focus(), 80);
      }
    });
  }

  if (lockCloseBtn && lockModal) {
    lockCloseBtn.addEventListener('click', function(e) {
      e.preventDefault();
      lockModal.classList.remove('is-open');
      lockModal.style.opacity = '0';
      lockModal.style.pointerEvents = 'none';
    });
  }

  if (lockModal) {
    lockModal.addEventListener('click', function(e) {
      if (e.target === lockModal) {
        lockModal.classList.remove('is-open');
        lockModal.style.opacity = '0';
        lockModal.style.pointerEvents = 'none';
      }
    });
  }

  if (lockForm) {
    lockForm.addEventListener('submit', function(e) {
      e.preventDefault();
      window.location.href = 'admin.html';
    });
  }
})();
</script>
"""

# Write to shared_components.py for persistence
with open(os.path.join(os.path.dirname(__file__), "shared_components.py"), "w", encoding="utf-8") as f:
    f.write(f'''GLOBAL_HEADER_HTML = """{GLOBAL_HEADER_HTML}"""
GLOBAL_FOOTER_HTML = """{GLOBAL_FOOTER_HTML}"""
GLOBAL_COMPONENTS_CSS = """{GLOBAL_COMPONENTS_CSS}"""
GLOBAL_HEADER_FOOTER_JS = """{GLOBAL_HEADER_FOOTER_JS}"""
''')

print("✦ shared_components.py updated with exact header logo in footer and reliable lock modal.")

