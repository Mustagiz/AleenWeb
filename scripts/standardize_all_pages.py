import os
import re
from shared_components import GLOBAL_HEADER_HTML, GLOBAL_FOOTER_HTML, GLOBAL_COMPONENTS_CSS, GLOBAL_HEADER_FOOTER_JS, ALEEN_LOGO_SVG

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Aleen website"))

# 1. Update admin.html
def update_admin():
    admin_path = os.path.join(SITE_DIR, "admin.html")
    with open(admin_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Ensure GLOBAL_COMPONENTS_CSS is in <style>
    if "/* ================= GLOBAL HEADER & FOOTER LUXURY CSS ================= */" not in content:
        content = content.replace("<style>", f"<style>\n{GLOBAL_COMPONENTS_CSS}\n")

    # Replace <nav class="admin-nav">...</nav> with GLOBAL_HEADER_HTML + Admin Sub-Bar
    sub_bar = """
<div style="margin-top: clamp(76px, 8.4vh, 92px); background: linear-gradient(90deg, #0e1c13 0%, #172c1e 50%, #0e1c13 100%); border-bottom: 1px solid rgba(201, 163, 95, 0.35); padding: 14px clamp(20px, 3.5vw, 48px); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px; position: relative; z-index: 50;">
  <div style="display: flex; align-items: center; gap: 12px;">
    <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #4ade80; box-shadow: 0 0 10px #4ade80;"></span>
    <span style="font-size: 11.5px; letter-spacing: 2.2px; text-transform: uppercase; color: var(--gold-light); font-weight: 700;">Atelier Live Management Dashboard</span>
    <span style="font-size: 12px; color: var(--cream); opacity: 0.6;">&middot; Single-page e-commerce management console</span>
  </div>
  <div style="display: flex; align-items: center; gap: 12px;">
    <a href="collections.html" target="_blank" class="btn btn-outline" style="padding: 7px 18px; font-size: 11px;">Preview Collections &rarr;</a>
    <button id="addGarmentBtn" class="btn btn-gold" style="padding: 7px 18px; font-size: 11px;">+ Add New Garment</button>
    <button id="resetBtn" class="btn btn-outline" style="padding: 7px 18px; font-size: 11px;">Reset Catalog</button>
  </div>
</div>
"""
    # Replace existing <nav class="admin-nav">...</nav>
    content = re.sub(r'<nav class="admin-nav">[\s\S]*?</nav>', GLOBAL_HEADER_HTML + sub_bar, content)

    # Check footer in admin.html
    # If there's an existing footer, replace it; else append before </body>
    if "<footer" in content:
        content = re.sub(r'<footer[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, content)
    else:
        content = re.sub(r'(<div class="toast-popup"[\s\S]*?</div>)', r'\1\n' + GLOBAL_FOOTER_HTML, content)

    # Ensure GLOBAL_HEADER_FOOTER_JS is present
    if "/* ================= GLOBAL SCRIPT: MEGA MENUS & ATELIER LOCK ================= */" not in content:
        content = content.replace("</body>", f"{GLOBAL_HEADER_FOOTER_JS}\n</body>")

    with open(admin_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✦ admin.html standardized with constant header and footer.")

# 2. Update index.html
def update_index():
    index_path = os.path.join(SITE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace <footer id="footer">...</footer>
    if '<footer id="footer">' in content or '<footer id="footer"' in content:
        content = re.sub(r'<footer id="footer"[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, content)
    
    # Ensure footer modal is present
    if 'id="atelierLockModal"' not in content:
        content = content.replace("</body>", f"{GLOBAL_FOOTER_HTML}\n</body>")

    # Add or update footer CSS in index.html to guarantee 4-column layout and logo positioning
    footer_override_css = """
/* Global Footer Standardized Override */
#footer .f-main {
  display: grid !important;
  grid-template-columns: 2fr 1fr 1.2fr 1.8fr !important;
  gap: clamp(28px, 3.4vw, 64px) !important;
  align-items: start !important;
}
#footer .f-brand {
  position: relative !important;
  margin-top: -6px !important;
}
#footer .f-logo-link svg, #footer .aleen-crest-svg {
  height: clamp(90px, 9.5vw, 130px) !important;
  width: auto !important;
  display: block !important;
}
"""
    if "/* Global Footer Standardized Override */" not in content:
        content = content.replace("</style>", f"{footer_override_css}\n</style>")

    # Ensure JS handler for lock modal and mega menus
    if 'id="lockLoginForm"' not in content:
        content = content.replace("</body>", f"{GLOBAL_HEADER_FOOTER_JS}\n</body>")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✦ index.html standardized with constant global footer.")

# 3. Update the 7 ethnic pages:
ETHNIC_PAGES = [
    "sarees.html",
    "kurta-sets.html",
    "anarkali.html",
    "suits.html",
    "coord-sets.html",
    "lehengas.html",
    "dresses.html"
]

def update_ethnic_pages():
    for page_name in ETHNIC_PAGES:
        page_path = os.path.join(SITE_DIR, page_name)
        if not os.path.exists(page_path):
            continue
        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Update <style> with GLOBAL_COMPONENTS_CSS if needed
        if "/* Global Footer Standardized Override */" not in content:
            override_css = f"\n{GLOBAL_COMPONENTS_CSS}\n"
            content = content.replace("</style>", f"{override_css}\n</style>")

        # Standardize header
        if '<header id="header"' in content:
            content = re.sub(r'<header id="header"[\s\S]*?</header>', GLOBAL_HEADER_HTML, content)
            # Remove any duplicate mobile-nav if following
            content = re.sub(r'<div class="mobile-nav"[\s\S]*?</div>\s*</div>', '', content)

        # Standardize footer
        if '<footer' in content:
            content = re.sub(r'<footer[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, content)

        # Standardize JS
        if 'id="lockLoginForm"' not in content:
            content = content.replace("</body>", f"{GLOBAL_HEADER_FOOTER_JS}\n</body>")

        with open(page_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✦ {page_name} standardized.")

if __name__ == "__main__":
    update_admin()
    update_index()
    update_ethnic_pages()
    print("✦ All site pages standardized with constant global header & footer!")

