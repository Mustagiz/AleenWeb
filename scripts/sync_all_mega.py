import os, re
from shared_components import GLOBAL_HEADER_HTML

# 1. Update index.html
with open('Aleen website/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace header in index.html with GLOBAL_HEADER_HTML
header_start = text.find('<!-- ======================= GLOBAL HEADER ======================= -->\n<header id="header">')
if header_start == -1:
    header_start = text.find('<header id="header">')

header_end = text.find('</header>', header_start) + len('</header>')

if header_start != -1 and header_end != -1:
    text = text[:header_start] + GLOBAL_HEADER_HTML + text[header_end:]
    print("✓ Replaced header in index.html with pre-rendered luxury mega dropdown!")

with open('Aleen website/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Re-sync secondary pages
os.system("python3 scripts/rebuild_collections_page.py")
os.system("python3 scripts/build_admin_html.py")
os.system("python3 scripts/generate_ethnic_for_website.py")
os.system("python3 scripts/build_about_pages.py")
os.system("python3 scripts/build_legal_pages.py")
print("✦ All pages re-synced successfully!")

