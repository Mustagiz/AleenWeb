import os, re

# 1. Update index.html
with open('Aleen website/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Add the luxury mega dropdown CSS into head
luxury_mega_css = """
/* ================= ATELIER LUXURY MEGA DROPDOWN (PERFECT CONTRAST & BALANCE) ================= */
.mega {
  position: fixed !important;
  top: clamp(76px, 8.4vh, 92px) !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 9999 !important;
  display: block !important;
  opacity: 0 !important;
  visibility: hidden !important;
  transform: translateY(-8px) !important;
  transition: opacity 0.28s cubic-bezier(0.22, 0.61, 0.21, 1), transform 0.28s cubic-bezier(0.22, 0.61, 0.21, 1), visibility 0.28s !important;
  pointer-events: none !important;
}

.mega.is-open {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translateY(0) !important;
  pointer-events: auto !important;
}

.mega-sheet {
  position: absolute !important;
  inset: 0 !important;
  background: rgba(8, 17, 12, 0.97) !important;
  backdrop-filter: blur(28px) !important;
  -webkit-backdrop-filter: blur(28px) !important;
  border-top: 1px solid rgba(201, 163, 95, 0.28) !important;
  border-bottom: 1px solid rgba(201, 163, 95, 0.35) !important;
  box-shadow: 0 35px 80px rgba(0, 0, 0, 0.85), 0 0 50px rgba(201, 163, 95, 0.08) !important;
}

.mega-sheet::after {
  display: none !important;
}

.mega-inner {
  position: relative !important;
  z-index: 2 !important;
  max-width: 1360px !important;
  width: 92vw !important;
  margin: 0 auto !important;
  padding: clamp(28px, 3.6vh, 44px) clamp(20px, 2.5vw, 40px) !important;
  display: block !important;
}

.mega-layout {
  display: grid !important;
  grid-template-columns: 3.1fr 2.4fr !important;
  gap: clamp(32px, 3.5vw, 56px) !important;
  align-items: start !important;
}

.mega-grid {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
  gap: clamp(22px, 2.4vw, 36px) !important;
}

.mega-group h4 {
  font-family: var(--sans) !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  letter-spacing: 0.24em !important;
  text-transform: uppercase !important;
  color: var(--gold-light) !important;
  margin: 0 0 6px 0 !important;
  opacity: 1 !important;
}

.mega-group-line {
  display: block !important;
  width: 28px !important;
  height: 1px !important;
  background: linear-gradient(90deg, var(--gold) 0%, transparent 100%) !important;
  margin-bottom: 14px !important;
}

.mega-group a {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  font-family: var(--sans) !important;
  font-size: 13.5px !important;
  color: rgba(245, 237, 216, 0.82) !important;
  text-decoration: none !important;
  padding: 6.5px 0 !important;
  transition: all 0.22s ease !important;
}

.mega-group a .mega-arr {
  width: 11px !important;
  height: 11px !important;
  stroke: var(--gold) !important;
  fill: none !important;
  stroke-width: 2 !important;
  opacity: 0 !important;
  transform: translateX(-4px) !important;
  transition: all 0.22s ease !important;
}

.mega-group a:hover {
  color: #ffffff !important;
  transform: translateX(4px) !important;
}

.mega-group a:hover .mega-arr {
  opacity: 1 !important;
  transform: translateX(0) !important;
}

/* Two Featured Promo Cards Side-by-Side */
.mega-promos-grid {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 18px !important;
}

.mega-promo-card {
  display: flex !important;
  flex-direction: column !important;
  text-decoration: none !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid rgba(201, 163, 95, 0.28) !important;
  background: rgba(15, 29, 21, 0.6) !important;
  transition: all 0.35s ease !important;
}

.mega-promo-card:hover {
  transform: translateY(-4px) !important;
  border-color: rgba(201, 163, 95, 0.6) !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6), 0 0 20px rgba(201, 163, 95, 0.15) !important;
}

.mega-promo-img-wrap {
  position: relative !important;
  width: 100% !important;
  aspect-ratio: 4/3 !important;
  overflow: hidden !important;
}

.mega-promo-img-wrap img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  transition: transform 0.6s ease !important;
}

.mega-promo-card:hover .mega-promo-img-wrap img {
  transform: scale(1.06) !important;
}

.mega-promo-badge {
  position: absolute !important;
  top: 12px !important;
  left: 12px !important;
  background: rgba(10, 20, 14, 0.85) !important;
  backdrop-filter: blur(8px) !important;
  border: 1px solid rgba(201, 163, 95, 0.45) !important;
  color: var(--gold-light) !important;
  font-size: 9.5px !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  padding: 4px 10px !important;
  border-radius: 2px !important;
}

.mega-promo-copy {
  padding: 14px 16px 16px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 4px !important;
}

.mega-promo-copy h5 {
  font-family: var(--serif) !important;
  font-size: 17px !important;
  color: #f7efdc !important;
  margin: 0 !important;
  font-weight: 500 !important;
}

.mega-promo-copy p {
  font-size: 12px !important;
  color: var(--gold-light) !important;
  margin: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  transition: gap 0.22s ease !important;
}

.mega-promo-copy p svg {
  width: 16px !important;
  height: 8px !important;
  fill: none !important;
  stroke: currentColor !important;
  stroke-width: 1.5 !important;
  transition: transform 0.22s ease !important;
}

.mega-promo-card:hover .mega-promo-copy p {
  color: var(--gold-spark) !important;
  gap: 10px !important;
}

.mega-promo-card:hover .mega-promo-copy p svg {
  transform: translateX(4px) !important;
}
"""

if "ATELIER LUXURY MEGA DROPDOWN" not in text:
    text = text.replace('</head>', f'<style>\n{luxury_mega_css}\n</style>\n</head>')

# Replace the old renderMega function in index.html
old_render_mega_regex = r'function renderMega\(key\)\s*\{.*?function openMega\(key\)'
new_render_mega = """function renderMega(key) {
    if (!megaInner) return;
    megaInner.classList.remove('is-women');
    megaInner.innerHTML = `
      <div class="mega-layout">
        <div class="mega-grid">
          <div class="mega-group">
            <h4>Ethnic Haute Couture</h4>
            <span class="mega-group-line"></span>
            <a href="sarees.html"><span>Sarees</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="kurta-sets.html"><span>Kurta Sets</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="anarkali.html"><span>Anarkali Sets</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="suits.html"><span>Royal Suits</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="coord-sets.html"><span>Co-ord Sets</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="lehengas.html"><span>Heritage Lehengas</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="dresses.html"><span>Dresses &amp; Gowns</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
          </div>
          <div class="mega-group">
            <h4>Curated Heritage</h4>
            <span class="mega-group-line"></span>
            <a href="sarees.html"><span>Banarasi Brocades</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="craftsmanship.html"><span>Zardozi Masterpieces</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="collections.html"><span>Pure Handloom Silks</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="collections.html"><span>Awadh Needlecraft</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="collections.html"><span>Artisanal Dupattas</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
          </div>
          <div class="mega-group">
            <h4>The Atelier</h4>
            <span class="mega-group-line"></span>
            <a href="collections.html"><span>All Collections Catalog</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="collections.html?filter=new"><span>New Arrivals 2026</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="craftsmanship.html"><span>Craftsmanship Story</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="sustainability.html"><span>Our Sustainability</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
            <a href="admin.html"><span>Staff Atelier Portal</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>
          </div>
        </div>
        <div class="mega-promos-grid">
          <a href="collections.html" class="mega-promo-card">
            <div class="mega-promo-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2" alt="The Women's Edit" loading="lazy">
              <span class="mega-promo-badge">CURATED DRAPES</span>
            </div>
            <div class="mega-promo-copy">
              <h5>The Women’s Edit</h5>
              <p>Elegance in every drape <svg viewBox="0 0 24 10"><path d="M0 5h20M16 1l4 4-4 4"/></svg></p>
            </div>
          </a>
          <a href="collections.html?filter=new" class="mega-promo-card">
            <div class="mega-promo-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s4-p1.jpg?v=3" alt="Royal Awadh Couture" loading="lazy">
              <span class="mega-promo-badge">NEW SEASON</span>
            </div>
            <div class="mega-promo-copy">
              <h5>Royal Awadh Couture</h5>
              <p>Centuries of artistry <svg viewBox="0 0 24 10"><path d="M0 5h20M16 1l4 4-4 4"/></svg></p>
            </div>
          </a>
        </div>
      </div>
    `;
  }

  function openMega(key)"""

text = re.sub(old_render_mega_regex, new_render_mega, text, flags=re.DOTALL)

with open('Aleen website/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✦ Updated index.html mega menu logic and styling!")

