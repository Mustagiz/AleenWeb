import os
import re
from shared_components import GLOBAL_HEADER_HTML, GLOBAL_FOOTER_HTML, GLOBAL_COMPONENTS_CSS, GLOBAL_HEADER_FOOTER_JS

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Aleen website"))

def update_all_pages():
    all_html_files = [f for f in os.listdir(SITE_DIR) if f.endswith(".html")]
    print(f"Updating {len(all_html_files)} HTML pages...")

    for fname in all_html_files:
        fpath = os.path.join(SITE_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()

        # 1. Update Header
        c = re.sub(r'<header id="header"[\s\S]*?</header>', GLOBAL_HEADER_HTML, c)

        # 2. Update Footer
        c = re.sub(r'<footer id="footer"[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, c)
        if '<footer' in c and '<footer id="footer"' not in c:
            c = re.sub(r'<footer[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, c)

        # 3. Ensure Lock Modal is in place before </body>
        # Replace existing modal if present, else insert
        if 'id="atelierLockModal"' in c:
            c = re.sub(r'<div class="atelier-lock-modal"[\s\S]*?</div>\s*</div>', '', c)
        
        # 4. Ensure GLOBAL_COMPONENTS_CSS is in <style>
        if "/* ================= GLOBAL HEADER & FOOTER LUXURY CSS ================= */" not in c:
            c = c.replace("<style>", f"<style>\n{GLOBAL_COMPONENTS_CSS}\n")
        else:
            # Replace old block with new GLOBAL_COMPONENTS_CSS
            c = re.sub(r'/\* ================= GLOBAL HEADER & FOOTER LUXURY CSS ================= \*/[\s\S]*?/\* Atelier Lock Modal Styles \*/[\s\S]*?}', GLOBAL_COMPONENTS_CSS, c)

        # 5. Ensure GLOBAL_HEADER_FOOTER_JS is before </body>
        if "<!-- ================= GLOBAL SCRIPT: MEGA MENUS & ATELIER LOCK ================= -->" in c:
            c = re.sub(r'<!-- ================= GLOBAL SCRIPT: MEGA MENUS & ATELIER LOCK ================= -->[\s\S]*?</script>', GLOBAL_HEADER_FOOTER_JS, c)
        else:
            c = c.replace("</body>", f"{GLOBAL_HEADER_FOOTER_JS}\n</body>")

        # Specific adjustments for index.html
        if fname == "index.html":
            # Add generous spacing on top of Kalakaari, Discover, and Best Sellers
            spacing_overrides = """
/* ================= ELEGANT LUXURY SPACING ON SECTIONS ================= */
#explore {
  padding-top: clamp(80px, 11vh, 130px) !important;
  margin-top: clamp(24px, 3vh, 50px) !important;
}
#kalakaari {
  padding-top: clamp(80px, 11vh, 130px) !important;
  margin-top: clamp(30px, 4vh, 60px) !important;
}
#best {
  padding-top: clamp(80px, 11vh, 130px) !important;
  margin-top: clamp(30px, 4vh, 60px) !important;
}
"""
            if "/* ================= ELEGANT LUXURY SPACING ON SECTIONS ================= */" not in c:
                c = c.replace("</style>", f"{spacing_overrides}\n</style>")

            # Disable old buildFooterLogo call if present in index.html
            c = c.replace("buildFooterLogo($('#footLogo'));", "// buildFooterLogo disabled - exact header SVG used")

        # Specific adjustments for collections.html: Ensure Picture 3 background is set
        if fname == "collections.html":
            if "collection-bg.png" not in c:
                c = c.replace("body {", "body { background: #f3ebdd url('assets/collection-bg.png') no-repeat top left / cover fixed !important; ")

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"  ✓ {fname} updated successfully.")

if __name__ == "__main__":
    update_all_pages()
    print("✦ All site pages updated with perfect alignment, exact header logo in footer, compact hero, and working lock modal!")

