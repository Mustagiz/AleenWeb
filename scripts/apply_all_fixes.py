import os
import re
from shared_components import GLOBAL_HEADER_HTML, GLOBAL_FOOTER_HTML, GLOBAL_COMPONENTS_CSS, GLOBAL_HEADER_FOOTER_JS

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Aleen website"))

# 1. Update index.html
def fix_index_html():
    index_path = os.path.join(SITE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        c = f.read()

    # 1.1 Remove Picture 1: k-corner in Kalakaari section
    c = re.sub(r'<p class="k-corner k-corner-l"[\s\S]*?</p>', '', c)
    c = re.sub(r'<p class="k-corner k-corner-r"[\s\S]*?</p>', '', c)

    # 1.2 Remove Picture 2: b-rail in Best Sellers section
    c = re.sub(r'<aside class="b-rail b-rail-l"[\s\S]*?</aside>', '', c)
    c = re.sub(r'<aside class="b-rail b-rail-r"[\s\S]*?</aside>', '', c)

    # 1.3 Fix Picture 3: remove b-badge from b-c2 and fix styling
    c = re.sub(r'<span class="b-badge">[\s\S]*?</span>\s*</i>\s*</span>', '', c)
    c = re.sub(r'<span class="b-badge">[\s\S]*?</span>', '', c)

    # 1.4 Update Header in index.html (remove Kalakaari and Best Sellers)
    c = re.sub(r'<header id="header"[\s\S]*?</header>', GLOBAL_HEADER_HTML, c)

    # 1.5 Update Footer in index.html (with Privacy Policy, Terms, Sitemap links)
    c = re.sub(r'<footer id="footer"[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, c)
    if 'id="atelierLockModal"' not in c:
        c = c.replace("</body>", f"{GLOBAL_FOOTER_HTML}\n</body>")

    # 1.6 Fix Picture 4: remove empty part / giant dead space from #women-new
    # Also add styles for Picture 1, 2, 3 fixes
    custom_overrides = """
/* ================= USER REQUESTED REFINEMENTS ================= */
/* Picture 4: Remove empty void above New Collections For Women */
#women-new {
  padding-top: clamp(24px, 3vh, 44px) !important;
  padding-bottom: clamp(50px, 7vh, 80px) !important;
}
#women-new .sec-head {
  margin-top: 10px !important;
  margin-bottom: clamp(30px, 4.5vh, 60px) !important;
}
#women-new .rail {
  top: 18% !important;
}

/* Picture 1: Ensure k-corner is removed */
.k-corner, .k-corner-l, .k-corner-r {
  display: none !important;
}

/* Picture 2: Ensure b-rail is removed */
.b-rail, .b-rail-l, .b-rail-r {
  display: none !important;
}

/* Picture 3: Refine Best Sellers card 02 (clean contrast, no milky wash, no awkward badge) */
.b-badge {
  display: none !important;
}
.b-veil {
  position: absolute !important;
  inset: 0 !important;
  background: linear-gradient(104deg, rgba(8, 16, 10, 0.78) 0%, rgba(8, 16, 10, 0.38) 32%, transparent 60%) !important;
}
.b-txt .b-no {
  color: var(--gold-light) !important;
}
.b-txt .b-no::after {
  background: var(--gold) !important;
}
.b-txt h3 {
  color: #f7efdc !important;
  text-shadow: 0 2px 8px rgba(0,0,0,0.5) !important;
}
.b-txt p {
  color: rgba(239, 228, 200, 0.92) !important;
  text-shadow: 0 1px 4px rgba(0,0,0,0.5) !important;
}
.b-shop span {
  color: var(--gold-spark) !important;
}
.b-go svg {
  stroke: var(--gold-spark) !important;
}
"""
    if "/* ================= USER REQUESTED REFINEMENTS ================= */" not in c:
        c = c.replace("</style>", f"{custom_overrides}\n</style>")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("✦ index.html updated with all fixes for Picture 1, 2, 3, 4, header & footer!")

# 2. Update collections.html
def fix_collections_html():
    col_path = os.path.join(SITE_DIR, "collections.html")
    with open(col_path, "r", encoding="utf-8") as f:
        c = f.read()

    # Update Header & Footer
    c = re.sub(r'<header id="header"[\s\S]*?</header>', GLOBAL_HEADER_HTML, c)
    c = re.sub(r'<footer id="footer"[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, c)

    with open(col_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("✦ collections.html updated with new header and footer.")

# 3. Update admin.html
def fix_admin_html():
    admin_path = os.path.join(SITE_DIR, "admin.html")
    with open(admin_path, "r", encoding="utf-8") as f:
        c = f.read()

    c = re.sub(r'<header id="header"[\s\S]*?</header>', GLOBAL_HEADER_HTML, c)
    c = re.sub(r'<footer id="footer"[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, c)

    with open(admin_path, "w", encoding="utf-8") as f:
        f.write(c)
    print("✦ admin.html updated with new header and footer.")

# 4. Update all other HTML pages in the site
def fix_all_other_pages():
    all_files = [f for f in os.listdir(SITE_DIR) if f.endswith(".html") and f not in ["index.html", "collections.html", "admin.html"]]
    for filename in all_files:
        filepath = os.path.join(SITE_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            c = f.read()

        c = re.sub(r'<header id="header"[\s\S]*?</header>', GLOBAL_HEADER_HTML, c)
        c = re.sub(r'<footer id="footer"[\s\S]*?</footer>', GLOBAL_FOOTER_HTML, c)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"✦ {filename} updated with standardized header and footer.")

if __name__ == "__main__":
    fix_index_html()
    fix_collections_html()
    fix_admin_html()
    fix_all_other_pages()
    print("✦ All pages successfully updated across Aleen website!")

