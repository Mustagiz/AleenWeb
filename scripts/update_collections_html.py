import re
from shared_header import HEADER_HTML, HEADER_CSS, HEADER_SCRIPT

with open('Aleen-react2/public/collections.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add HEADER_CSS inside <style>
# Insert HEADER_CSS right before </style>
html = html.replace('</style>', f'\n{HEADER_CSS}\n</style>')

# 2. Replace old <header class="atelier-nav">...</header> with HEADER_HTML
# Let's inspect what <header class="atelier-nav">...</header> contains
old_header_pattern = r'<header class="atelier-nav">.*?</header>'
html = re.sub(old_header_pattern, HEADER_HTML, html, flags=re.DOTALL)

# Also ensure top announcement has proper margin if needed
html = html.replace(
    '<aside class="atelier-announcement">',
    '<aside class="atelier-announcement" style="margin-top: var(--hdr-h-solid); position: relative; z-index: 90;">'
)

# 3. Remove .card-badge in renderGarments
html = html.replace(
    '<span class="card-badge">${item.badge}</span>',
    '<!-- badge suppressed -->'
)

# 4. In footer, add Atelier Manager Portal
footer_old = '<p class="footer-copy">'
footer_new = """
      <div class="f-atelier-portal-bar">
        <a href="/login" class="f-atelier-portal-link" title="Atelier Staff & Garment Management Console">
          <span class="spark" style="color: var(--gold);">✦</span>
          <span style="font-weight: 700; letter-spacing: 1.8px; color: #FFFFFF;">Atelier Manager Login</span>
          <span style="font-size: 11px; opacity: 0.85; color: var(--gold-light);">— Manage, Edit &amp; Update Garments</span>
        </a>
      </div>
      <p class="footer-copy">
"""
html = html.replace(footer_old, footer_new, 1)

# 5. Fix header button listeners that may not exist in new constant header
html = html.replace(
    'document.getElementById("wishlistHeaderBtn").addEventListener',
    'document.getElementById("wishlistHeaderBtn")?.addEventListener'
)
html = html.replace(
    'document.getElementById("bagHeaderBtn").addEventListener',
    'document.getElementById("bagHeaderBtn")?.addEventListener'
)

# 6. Append HEADER_SCRIPT right before </body>
html = html.replace('</body>', f'\n{HEADER_SCRIPT}\n</body>')

with open('Aleen-react2/public/collections.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("collections.html updated successfully!")
