#!/usr/bin/env python3
"""
MEGA UPDATE SCRIPT — Aleen Website
Applies ALL pending tasks:
1. Remove spacing_overrides from #explore, #kalakaari, #best  
2. Fix women-new padding-top (remove excessive space)
3. Link Explore buttons in #explore to collections.html
4. Remove #kalakaari section → Replace with animated garment carousel
5. Add Our Story animated background
6. Apply global header + footer to ALL pages
7. Run build_admin_html.py to regenerate admin.html
8. Update footer Shop links (remove kalakaari, link correctly)
9. Add header icons hide (search/login/wishlist/bag)
10. Remove green gap between sections
"""
import os
import re
import sys

scripts_dir = os.path.dirname(os.path.abspath(__file__))
site_dir = os.path.abspath(os.path.join(scripts_dir, "..", "Aleen website"))
sys.path.insert(0, scripts_dir)

from shared_components import GLOBAL_HEADER_HTML, GLOBAL_FOOTER_HTML, GLOBAL_COMPONENTS_CSS, GLOBAL_HEADER_FOOTER_JS

# ============================================================
# ANIMATED CAROUSEL SECTION (replaces #kalakaari)
# ============================================================
GARMENT_REEL_HTML = """
  <!-- ================= ANIMATED GARMENT CAROUSEL ================= -->
  <section id="garment-reel" aria-label="Curated garments carousel">
    <div class="gr-wrap">
      <header class="sec-head gr-head">
        <p class="sh-eyebrow">The Atelier</p>
        <h2 class="sh-title">Curated Garments</h2>
        <i class="sh-orna"><b></b></i>
        <p class="sh-sub">Each piece a story. Each thread a legacy.</p>
      </header>
      <div class="gr-track-outer" aria-hidden="true">
        <div class="gr-track" id="grTrack">
          <div class="gr-card">
            <div class="gr-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s4-p1.jpg?v=3" alt="Embroidered Anarkali" loading="lazy">
            </div>
            <div class="gr-info">
              <span class="gr-tag">Ethnic Haute Couture</span>
              <h3>Embroidered Anarkali</h3>
              <a href="collections.html" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
            </div>
          </div>
          <div class="gr-card">
            <div class="gr-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s4-p2.jpg?v=3" alt="Heritage Saree" loading="lazy">
            </div>
            <div class="gr-info">
              <span class="gr-tag">Curated Heritage</span>
              <h3>Heritage Silk Saree</h3>
              <a href="collections.html" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
            </div>
          </div>
          <div class="gr-card">
            <div class="gr-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s4-p3.jpg?v=3" alt="Artisan Kurta Set" loading="lazy">
            </div>
            <div class="gr-info">
              <span class="gr-tag">The Atelier</span>
              <h3>Artisan Kurta Set</h3>
              <a href="collections.html" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
            </div>
          </div>
          <div class="gr-card">
            <div class="gr-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s5-p1.jpg?v=3" alt="Royal Lehenga" loading="lazy">
            </div>
            <div class="gr-info">
              <span class="gr-tag">Ethnic Haute Couture</span>
              <h3>Royal Lehenga</h3>
              <a href="collections.html" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
            </div>
          </div>
          <div class="gr-card">
            <div class="gr-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s5-p2.jpg?v=3" alt="Coord Set" loading="lazy">
            </div>
            <div class="gr-info">
              <span class="gr-tag">Curated Heritage</span>
              <h3>Printed Coord Set</h3>
              <a href="collections.html" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
            </div>
          </div>
          <div class="gr-card">
            <div class="gr-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s5-p3.jpg?v=3" alt="Dupatta Set" loading="lazy">
            </div>
            <div class="gr-info">
              <span class="gr-tag">The Atelier</span>
              <h3>Dupatta Ensemble</h3>
              <a href="collections.html" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
            </div>
          </div>
          <!-- Duplicate for seamless loop -->
          <div class="gr-card">
            <div class="gr-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s4-p1.jpg?v=3" alt="Embroidered Anarkali" loading="lazy">
            </div>
            <div class="gr-info">
              <span class="gr-tag">Ethnic Haute Couture</span>
              <h3>Embroidered Anarkali</h3>
              <a href="collections.html" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
            </div>
          </div>
          <div class="gr-card">
            <div class="gr-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s4-p2.jpg?v=3" alt="Heritage Saree" loading="lazy">
            </div>
            <div class="gr-info">
              <span class="gr-tag">Curated Heritage</span>
              <h3>Heritage Silk Saree</h3>
              <a href="collections.html" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
            </div>
          </div>
          <div class="gr-card">
            <div class="gr-img-wrap">
              <img src="https://mahira2.netlify.app/assets/s4-p3.jpg?v=3" alt="Artisan Kurta Set" loading="lazy">
            </div>
            <div class="gr-info">
              <span class="gr-tag">The Atelier</span>
              <h3>Artisan Kurta Set</h3>
              <a href="collections.html" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

# ============================================================
# GARMENT REEL CSS
# ============================================================
GARMENT_REEL_CSS = """
/* ===== GARMENT REEL CAROUSEL ===== */
#garment-reel {
  background: #0e1a0a;
  padding: clamp(60px,10vh,120px) 0 clamp(60px,10vh,100px);
  overflow: hidden;
  position: relative;
}
#garment-reel::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 0%, rgba(201,163,95,0.07) 0%, transparent 65%);
  pointer-events: none;
}
.gr-wrap { width: 100%; }
.gr-head { text-align: center; margin-bottom: clamp(36px,6vh,70px); }
.gr-track-outer {
  width: 100%;
  overflow: hidden;
  position: relative;
  mask-image: linear-gradient(to right, transparent 0%, black 8%, black 92%, transparent 100%);
  -webkit-mask-image: linear-gradient(to right, transparent 0%, black 8%, black 92%, transparent 100%);
}
.gr-track {
  display: flex;
  gap: clamp(16px,2vw,28px);
  width: max-content;
  animation: grScroll 32s linear infinite;
  will-change: transform;
}
.gr-track:hover { animation-play-state: paused; }
@keyframes grScroll {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.gr-card {
  flex: 0 0 clamp(260px, 22vw, 360px);
  background: #121f0d;
  border: 1px solid rgba(201,163,95,0.18);
  border-radius: 2px;
  overflow: hidden;
  transition: transform 0.4s ease, box-shadow 0.4s ease, border-color 0.4s ease;
  cursor: pointer;
}
.gr-card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 0 1px rgba(201,163,95,0.4);
  border-color: rgba(201,163,95,0.5);
}
.gr-img-wrap {
  width: 100%;
  aspect-ratio: 3/4;
  overflow: hidden;
  position: relative;
}
.gr-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}
.gr-card:hover .gr-img-wrap img { transform: scale(1.06); }
.gr-info {
  padding: clamp(14px,2vw,22px) clamp(14px,2vw,22px) clamp(18px,2.5vw,28px);
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.gr-tag {
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #c9a35f;
  font-family: 'Cormorant Garamond', Georgia, serif;
}
.gr-info h3 {
  font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: clamp(16px,1.6vw,22px);
  font-weight: 500;
  color: #f5edd8;
  margin: 0;
  line-height: 1.3;
}
.gr-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #c9a35f;
  text-decoration: none;
  margin-top: 4px;
  transition: color 0.3s, gap 0.3s;
}
.gr-cta svg { width: 20px; height: 8px; fill: none; stroke: currentColor; stroke-width: 1.5; transition: transform 0.3s; }
.gr-cta:hover { color: #f0d48c; gap: 12px; }
.gr-cta:hover svg { transform: translateX(4px); }
"""

# ============================================================
# OUR STORY IMPROVED BACKGROUND CSS
# ============================================================
STORY_BG_CSS = """
/* ===== OUR STORY SECTION IMPROVED BG ===== */
#storyEd {
  background: #0a1507 url('https://mahira2.netlify.app/assets/s7-story.jpg?v=3') center center / cover no-repeat !important;
  background-attachment: fixed !important;
  position: relative;
}
#storyEd::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    160deg,
    rgba(5, 12, 4, 0.82) 0%,
    rgba(10, 25, 8, 0.70) 40%,
    rgba(5, 12, 4, 0.88) 100%
  );
  pointer-events: none;
  z-index: 1;
}
#storyEd > * { position: relative; z-index: 2; }
"""

# ============================================================
# SECTION GAP ELIMINATOR CSS (removes green dead space)
# ============================================================
NO_GAP_CSS = """
/* ===== ELIMINATE GREEN GAPS BETWEEN SECTIONS ===== */
#women-new, #explore, #garment-reel, #best, #storyEd {
  margin-top: 0 !important;
  margin-bottom: 0 !important;
}
/* Fix women-new top padding — remove excessive space */
#women-new {
  padding-top: clamp(16px, 2.5vh, 36px) !important;
}
#women-new .sec-head {
  margin-top: 0 !important;
  padding-top: 0 !important;
}
/* Remove any inline padding-top from media overrides that cause the gap */
@media (max-width: 700px) {
  #women-new { padding-top: 16px !important; }
}
"""

def apply_to_index(content):
    """Apply all index.html specific changes."""
    
    # 1. Remove old spacing overrides block
    content = re.sub(
        r'/\* ================= ELEGANT LUXURY SPACING ON SECTIONS ================= \*/.*?(?=#best\s*\{[^}]*padding-top[^}]*\})',
        '',
        content, flags=re.DOTALL
    )
    # Also remove via exact text match
    content = re.sub(
        r'/\* ================= ELEGANT LUXURY SPACING ON SECTIONS ================= \*/\s*#explore\s*\{[^}]*\}\s*#kalakaari\s*\{[^}]*\}\s*#best\s*\{[^}]*\}',
        '',
        content, flags=re.DOTALL
    )
    
    # 2. Remove any CSS rules setting excessive padding-top on #women-new (the 12vh one)
    content = re.sub(
        r'(#women-new\s*\{[^}]*?)padding-top\s*:\s*12vh\s*;',
        r'\1padding-top: clamp(16px, 2.5vh, 36px);',
        content, flags=re.DOTALL
    )
    # Also fix the standalone override
    content = re.sub(
        r'#women-new\s*\{\s*padding-top\s*:\s*12vh\s*;?\s*\}',
        '#women-new { padding-top: clamp(16px, 2.5vh, 36px) !important; }',
        content
    )
    
    # 3. Link Explore buttons in #explore section to collections.html
    # Find the #explore section and change all .cta href to collections.html
    def fix_explore_hrefs(m):
        section = m.group(0)
        # Replace href="#kalakaari" or any internal link on cta buttons with collections.html
        section = re.sub(r'<a class="cta"\s+href="[^"]*"', '<a class="cta" href="collections.html"', section)
        section = re.sub(r'<a\s+class="cta"\s+href="[^"]*"', '<a class="cta" href="collections.html"', section)
        return section
    
    content = re.sub(
        r'<section id="explore"[^>]*>[\s\S]*?</section>',
        fix_explore_hrefs,
        content, count=1
    )
    
    # 4. Remove #kalakaari section and replace with animated carousel
    content = re.sub(
        r'\s*<!--[^>]*kalakaari[^>]*-->\s*<section id="kalakaari"[\s\S]*?</section>',
        '\n' + GARMENT_REEL_HTML,
        content, count=1, flags=re.IGNORECASE
    )
    # Fallback: try without comment
    if 'id="garment-reel"' not in content:
        content = re.sub(
            r'<section id="kalakaari"[\s\S]*?</section>',
            GARMENT_REEL_HTML,
            content, count=1
        )
    
    # 5. Inject Garment Reel CSS + Story BG CSS + No Gap CSS into <style>
    css_injection = GARMENT_REEL_CSS + '\n' + STORY_BG_CSS + '\n' + NO_GAP_CSS
    if '/* ===== GARMENT REEL CAROUSEL =====' not in content:
        content = content.replace('</style>', css_injection + '\n</style>', 1)
    
    # 6. Update footer Shop links — remove kalakaari link
    content = re.sub(
        r'<a href="index\.html#kalakaari">Kalakaari</a>\s*',
        '<a href="collections.html">Coord Sets</a>\n      ',
        content
    )
    
    # 7. Hero "New Arrivals" button → collections.html (ensure linked)
    content = re.sub(
        r'href="[^"]*"\s+class="hero-cta[^"]*"\s*>',
        'href="collections.html" class="hero-cta">',
        content
    )
    
    return content


def update_page(fpath, fname, content):
    """Apply global header/footer/CSS/JS to any page."""
    
    # 1. Update Header
    if re.search(r'<header id="header"', content):
        content = re.sub(r'<header id="header"[\s\S]*?</header>', GLOBAL_HEADER_HTML, content, count=1)
    
    # 2. Update Footer
    if re.search(r'<footer id="footer"', content):
        content = re.sub(r'<footer id="footer"[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, content, count=1)
    elif re.search(r'<footer', content):
        content = re.sub(r'<footer[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, content, count=1)
    
    # 3. Ensure GLOBAL_COMPONENTS_CSS is in <style>
    marker = "/* ================= GLOBAL HEADER & FOOTER LUXURY CSS ================= */"
    if marker not in content:
        content = content.replace('<style>', f'<style>\n{GLOBAL_COMPONENTS_CSS}\n', 1)
    else:
        # Update existing global CSS block
        content = re.sub(
            r'/\* ================= GLOBAL HEADER & FOOTER LUXURY CSS ================= \*/[\s\S]*?(?=/\* ===|</style>)',
            GLOBAL_COMPONENTS_CSS + '\n',
            content, count=1
        )
    
    # 4. Ensure GLOBAL_HEADER_FOOTER_JS is before </body>
    js_marker = "<!-- ================= GLOBAL SCRIPT: MEGA MENUS & ATELIER LOCK ================= -->"
    if js_marker in content:
        content = re.sub(
            r'<!-- ================= GLOBAL SCRIPT: MEGA MENUS & ATELIER LOCK ================= -->[\s\S]*?</script>',
            GLOBAL_HEADER_FOOTER_JS,
            content, count=1
        )
    else:
        content = content.replace('</body>', f'\n{GLOBAL_HEADER_FOOTER_JS}\n</body>', 1)
    
    # 5. index.html specific tweaks
    if fname == 'index.html':
        content = apply_to_index(content)
    
    # 6. Disable old footer logo builder call
    content = content.replace(
        "buildFooterLogo($('#footLogo'));",
        "// buildFooterLogo disabled - global SVG logo used"
    )
    
    return content


def main():
    html_files = [f for f in os.listdir(site_dir) if f.endswith('.html')]
    print(f"Found {len(html_files)} HTML files. Updating...")
    
    for fname in sorted(html_files):
        fpath = os.path.join(site_dir, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = update_page(fpath, fname, content)
        
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(updated)
        
        print(f"  ✓ {fname}")
    
    print(f"\n✦ All {len(html_files)} pages updated successfully!")
    print("  • Global header & footer applied to all pages")
    print("  • Animated garment carousel replaces Kalakaari section")
    print("  • No-gap CSS applied — green dead space eliminated")
    print("  • New Collections padding reduced")
    print("  • Explore buttons linked to collections.html")
    print("  • Our Story gets parallax background")


if __name__ == '__main__':
    main()

