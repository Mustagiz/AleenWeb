import os

# Complete Pre-Rendered Mega Menu HTML
MEGA_PRE_RENDERED_HTML = """  <!-- mega menus -->
  <div class="mega" id="mega" aria-hidden="true">
    <div class="mega-sheet"></div>
    <div class="mega-inner">
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
    </div>
  </div>"""

sc_path = os.path.join(os.path.dirname(__file__), "shared_components.py")
with open(sc_path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace mega menus block in GLOBAL_HEADER_HTML
old_mega_block_start = "  <!-- mega menus -->\n  <div class=\"mega\" id=\"mega\" aria-hidden=\"true\">"
old_mega_block_end = "  </div>\n</header>"

pos1 = text.find(old_mega_block_start)
pos2 = text.find(old_mega_block_end, pos1)

if pos1 != -1 and pos2 != -1:
    text = text[:pos1] + MEGA_PRE_RENDERED_HTML + "\n</header>" + text[pos2 + len(old_mega_block_end):]
    print("✓ Injected pre-rendered mega dropdown in shared_components.py")

with open(sc_path, "w", encoding="utf-8") as f:
    f.write(text)

print("✦ Saved shared_components.py!")

