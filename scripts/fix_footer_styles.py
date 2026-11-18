import os, re

# Perfect Luxury Footer Form & Social CSS
CLEAN_FOOTER_FORM_CSS = """
/* ================= STANDARDIZED LUXURY FOOTER FORM & ICONS ================= */
#footer .f-news {
  position: relative !important;
}

#footer .f-field {
  position: relative !important;
  display: flex !important;
  align-items: center !important;
  width: 100% !important;
  max-width: 380px !important;
  height: 48px !important;
  background: rgba(12, 24, 16, 0.75) !important;
  border: 1px solid rgba(201, 163, 95, 0.4) !important;
  border-radius: 999px !important;
  padding: 0 5px 0 20px !important;
  margin-bottom: 14px !important;
  box-sizing: border-box !important;
  transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}

#footer .f-field:focus-within {
  border-color: var(--gold) !important;
  box-shadow: 0 0 16px rgba(201, 163, 95, 0.25) !important;
}

#footer .f-field input {
  flex: 1 !important;
  width: auto !important;
  height: 100% !important;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
  border-radius: 0 !important;
  padding: 0 10px 0 0 !important;
  margin: 0 !important;
  color: #ffffff !important;
  font-family: var(--sans) !important;
  font-size: 13.5px !important;
  letter-spacing: 0.02em !important;
  box-sizing: border-box !important;
}

#footer .f-field input::placeholder {
  color: rgba(233, 224, 200, 0.5) !important;
  opacity: 1 !important;
}

#footer .f-field button {
  position: static !important;
  transform: none !important;
  flex-shrink: 0 !important;
  width: 38px !important;
  height: 38px !important;
  min-width: 38px !important;
  min-height: 38px !important;
  max-width: 38px !important;
  max-height: 38px !important;
  border-radius: 50% !important;
  border: none !important;
  background: linear-gradient(135deg, #e4be77 0%, #c9a35f 100%) !important;
  color: #0c1810 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  padding: 0 !important;
  margin: 0 !important;
  transition: transform 0.22s ease, background 0.22s ease, box-shadow 0.22s ease !important;
}

#footer .f-field button:hover {
  transform: scale(1.06) !important;
  background: #f7dfa3 !important;
  box-shadow: 0 4px 14px rgba(201, 163, 95, 0.45) !important;
}

#footer .f-field button svg {
  width: 15px !important;
  height: 11px !important;
  stroke: #0c1810 !important;
  stroke-width: 2 !important;
  fill: none !important;
}

/* Identical 40px Circles for All 5 Icons (Instagram, Facebook, YouTube, WhatsApp, Lock) */
#footer .f-social {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
  margin-top: 22px !important;
}

#footer .f-social a,
#footer .f-social .f-lock-btn,
#footer #lockModalBtn {
  width: 40px !important;
  height: 40px !important;
  min-width: 40px !important;
  min-height: 40px !important;
  max-width: 40px !important;
  max-height: 40px !important;
  border-radius: 50% !important;
  border: 1px solid rgba(201, 163, 95, 0.35) !important;
  background: rgba(20, 37, 27, 0.5) !important;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 0 !important;
  margin: 0 !important;
  color: var(--gold-light) !important;
  box-sizing: border-box !important;
  text-decoration: none !important;
  cursor: pointer !important;
  transition: all 0.25s ease !important;
}

#footer .f-social a svg,
#footer .f-social .f-lock-btn svg,
#footer #lockModalBtn svg {
  width: 16px !important;
  height: 16px !important;
  stroke: currentColor !important;
  stroke-width: 1.8 !important;
  fill: none !important;
}

#footer .f-social a:hover,
#footer .f-social .f-lock-btn:hover,
#footer #lockModalBtn:hover {
  background: rgba(201, 163, 95, 0.22) !important;
  border-color: var(--gold) !important;
  color: #ffffff !important;
  transform: translateY(-2px) !important;
  box-shadow: 0 4px 14px rgba(201, 163, 95, 0.35) !important;
}
"""

# 1. Update shared_components.py
sc_path = os.path.join(os.path.dirname(__file__), "shared_components.py")
with open(sc_path, "r", encoding="utf-8") as f:
    sc = f.read()

# Append to GLOBAL_HEADER_FOOTER_CSS in shared_components.py
if "STANDARDIZED LUXURY FOOTER FORM & ICONS" not in sc:
    pos_css_end = sc.find('"""\n\nGLOBAL_HEADER_HTML')
    if pos_css_end != -1:
        sc = sc[:pos_css_end] + "\n" + CLEAN_FOOTER_FORM_CSS + "\n" + sc[pos_css_end:]
        with open(sc_path, "w", encoding="utf-8") as f:
            f.write(sc)
        print("✓ Injected clean footer CSS into shared_components.py")

# 2. Update index.html
with open('Aleen website/index.html', 'r', encoding='utf-8') as f:
    idx = f.read()

if "STANDARDIZED LUXURY FOOTER FORM & ICONS" not in idx:
    idx = idx.replace('</head>', f'<style>\n{CLEAN_FOOTER_FORM_CSS}\n</style>\n</head>')
    with open('Aleen website/index.html', 'w', encoding='utf-8') as f:
        f.write(idx)
    print("✓ Injected clean footer CSS into index.html")

# 3. Rebuild all secondary pages to ensure footer consistency across all 20 pages
os.system("python3 scripts/rebuild_collections_page.py")
os.system("python3 scripts/build_admin_html.py")
os.system("python3 scripts/generate_ethnic_for_website.py")
os.system("python3 scripts/build_about_pages.py")
os.system("python3 scripts/build_legal_pages.py")
print("✦ Re-synced all pages with clean footer form and social circles!")

