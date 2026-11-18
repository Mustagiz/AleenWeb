import os
import re
from shared_header import HEADER_HTML, HEADER_CSS, HEADER_SCRIPT

OUT_DIR = os.path.abspath("Aleen website")
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Update collections.html for Aleen website
with open('Aleen-react2/public/collections.html', 'r', encoding='utf-8') as f:
    col_html = f.read()

# Replace any references to mahira.html with index.html
col_html = col_html.replace('mahira.html', 'index.html')
# Ensure no CRM links
col_html = col_html.replace('/login', 'admin.html')
# Replace any atelier-portal-bar with social lock button
col_html = re.sub(r'<div class="f-atelier-portal-bar".*?</div>', '', col_html, flags=re.DOTALL)

# In collections.html script, make it dynamically read from localStorage.getItem("aleen_master_catalog")
col_html = col_html.replace(
    'let currentCategory = "all";',
    '''// Read dynamic catalog from admin dashboard
    const savedCatalog = localStorage.getItem("aleen_master_catalog");
    if (savedCatalog) {
      try {
        const parsed = JSON.parse(savedCatalog);
        if (Array.isArray(parsed) && parsed.length > 0) {
          GARMENTS.length = 0;
          parsed.forEach(p => GARMENTS.push(p));
        }
      } catch(e) {
        console.warn("Using default garments:", e);
      }
    }
    let currentCategory = "all";'''
)

# Also add lock icon in footer of collections.html
footer_social_block = """
    <div style="display: flex; justify-content: center; gap: 14px; margin-top: 24px;">
      <button type="button" class="f-lock-btn" id="lockModalBtn" aria-label="Atelier Staff Management" title="Atelier Management Portal" style="width: 40px; height: 40px; border-radius: 50%; border: 1px solid rgba(201,163,95,0.4); background: rgba(20,37,27,0.5); color: #fff; cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.25s ease;">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
        </svg>
      </button>
    </div>
"""
col_html = col_html.replace('<p class="footer-copy">', f'{footer_social_block}\n<p class="footer-copy">')

# Add lock modal to collections.html
lock_modal_markup = """
<!-- ======================= ATELIER LOCK MODAL ======================= -->
<div class="atelier-lock-modal" id="atelierLockModal" aria-hidden="true" style="position: fixed; inset: 0; z-index: 10000; background: rgba(4, 9, 6, 0.88); backdrop-filter: blur(14px); display: flex; align-items: center; justify-content: center; padding: 20px; opacity: 0; pointer-events: none; transition: opacity 0.3s ease;">
  <div style="background: linear-gradient(135deg, #112318 0%, #07100a 100%); border: 1px solid rgba(201, 163, 95, 0.5); box-shadow: 0 24px 60px rgba(0,0,0,0.8); border-radius: 20px; max-width: 420px; width: 100%; padding: 34px 30px; text-align: center; position: relative;">
    <button id="lockCloseBtn" style="position: absolute; top: 16px; right: 16px; background: none; border: none; color: var(--cream); font-size: 22px; cursor: pointer;">&times;</button>
    <div style="width: 52px; height: 52px; margin: 0 auto 16px; border-radius: 50%; background: rgba(201, 163, 95, 0.15); border: 1px solid var(--gold); display: flex; align-items: center; justify-content: center; color: var(--gold-light);">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
    </div>
    <h3 style="font-family: var(--serif); font-size: 22px; font-weight: 500; color: var(--cream-hi); margin-bottom: 6px;">Atelier Management</h3>
    <p style="font-size: 13px; color: var(--cream); opacity: 0.8; margin-bottom: 22px;">Sign in to manage, edit, and update garments on your website catalog.</p>
    <form id="lockLoginForm">
      <input type="password" id="lockPassInput" placeholder="Enter Access Passcode" required style="width: 100%; padding: 12px 18px; background: rgba(4, 9, 6, 0.8); border: 1px solid rgba(201, 163, 95, 0.4); border-radius: 999px; color: #ffffff; font-size: 14px; text-align: center; outline: none; margin-bottom: 16px;">
      <button type="submit" style="width: 100%; padding: 12px 24px; background: var(--gold); color: #241A0C; border: 1px solid var(--gold-light); border-radius: 999px; font-size: 12px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; cursor: pointer;">✦ Enter Dashboard</button>
    </form>
    <p style="font-size: 11px; margin-top: 14px; opacity: 0.6;">Atelier Passcode: <code>aleen</code></p>
  </div>
</div>

<script>
(function() {
  const modal = document.getElementById('atelierLockModal');
  const openBtn = document.getElementById('lockModalBtn');
  const closeBtn = document.getElementById('lockCloseBtn');
  const form = document.getElementById('lockLoginForm');
  const passInput = document.getElementById('lockPassInput');

  if (openBtn && modal) {
    openBtn.addEventListener('click', () => {
      modal.style.opacity = '1';
      modal.style.pointerEvents = 'auto';
      if (passInput) passInput.focus();
    });
  }
  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => {
      modal.style.opacity = '0';
      modal.style.pointerEvents = 'none';
    });
  }
  if (modal) {
    modal.addEventListener('click', e => {
      if (e.target === modal) {
        modal.style.opacity = '0';
        modal.style.pointerEvents = 'none';
      }
    });
  }
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      window.location.href = 'admin.html';
    });
  }
})();
</script>
"""
col_html = col_html.replace('</body>', f'{lock_modal_markup}\n</body>')

with open(os.path.join(OUT_DIR, "collections.html"), "w", encoding="utf-8") as f:
    f.write(col_html)
print("Generated Aleen website/collections.html")

# 2. Generate the 7 Ethnic Pages in Aleen website
ETHNIC_PAGES = [
  ("sarees", "sarees.html", "The Royal Saree Treasury", "Six yards of sheer majesty — Banarasi Katan, Pen Kalamkari, and hand-embroidered organza drapes."),
  ("kurta-sets", "kurta-sets.html", "The Handcrafted Kurta Sets Edit", "Everyday elegance elevated with Marodi needlework, antique gota, and tissue organza trims."),
  ("anarkali", "anarkali.html", "The Regal Anarkali Suite", "Voluminous 32-kali flares, heirloom Chikankari, and silver mukaish accents woven for royal presence."),
  ("suits", "suits.html", "Bespoke Royal Suits", "Structured silhouettes with antique threadwork, regal lapels, and handloom churidars."),
  ("coord-sets", "coord-sets.html", "The Contemporary Co-ord Sets", "Modern fluid luxury — tunic and palazzo ensembles crafted in pure silks and artisanal prints."),
  ("lehengas", "lehengas.html", "The Bridal & Festive Lehenga Edit", "Heirloom bridal ensembles detailed with beaten zardozi, semi-precious stones, and dual dupattas."),
  ("dresses", "dresses.html", "The Dresses & Sets Collection", "Fusion couture gowns and tiered maxi dresses crafted for red-carpet affairs and festive galas.")
]

ETHNIC_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Aleen Clothing — {title}</title>
  <meta name="description" content="Explore {title} by Aleen Clothing. Consciously Curated luxury Indian couture.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600;700&family=Great+Vibes&display=swap" rel="stylesheet">
  <style>
    :root {{
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
      --ink-on-gold: #241a0c;
      --serif: 'Playfair Display', Georgia, 'Times New Roman', serif;
      --serif-i: 'Cormorant Garamond', Georgia, serif;
      --sans: 'Montserrat', 'Segoe UI', Arial, sans-serif;
      --ease: cubic-bezier(0.22, 0.61, 0.21, 1);
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      background-color: var(--void-0);
      color: #ffffff;
      font-family: var(--sans);
      font-size: 16px;
      line-height: 1.6;
      overflow-x: hidden;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    /* Announcement */
    .atelier-announcement {{
      background: linear-gradient(90deg, #112217, #1c3826, #112217);
      border-bottom: 1px solid rgba(201, 163, 95, 0.25);
      text-align: center;
      padding: 8px 16px;
      font-size: 11px;
      letter-spacing: 2px;
      text-transform: uppercase;
      font-weight: 500;
      color: var(--gold-light);
      position: relative;
      z-index: 90;
      margin-top: var(--hdr-h-solid);
    }}

    {header_css}

    /* Hero section */
    .hero-banner {{
      padding: clamp(48px, 6vh, 72px) 24px clamp(32px, 4vh, 48px);
      text-align: center;
      background: radial-gradient(circle at 50% 20%, rgba(29, 53, 39, 0.5) 0%, rgba(4, 9, 6, 0.98) 75%);
      border-bottom: 1px solid rgba(201, 163, 95, 0.18);
    }}
    .hero-eyebrow {{
      font-size: 11px;
      letter-spacing: 4px;
      text-transform: uppercase;
      color: var(--gold);
      font-weight: 600;
      margin-bottom: 12px;
    }}
    .hero-title {{
      font-family: var(--serif);
      font-size: clamp(32px, 4.5vw, 56px);
      font-weight: 400;
      color: var(--cream-hi);
      margin-bottom: 14px;
    }}
    .hero-sub {{
      font-family: var(--serif-i);
      font-size: clamp(16px, 1.6vw, 22px);
      font-style: italic;
      color: var(--cream);
      max-width: 680px;
      margin: 0 auto;
      opacity: 0.9;
    }}

    /* Sub-nav tabs */
    .ethnic-tabs {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 10px;
      padding: 24px 16px;
      background: rgba(11, 21, 14, 0.6);
      border-bottom: 1px solid rgba(201, 163, 95, 0.15);
    }}
    .ethnic-tab {{
      padding: 8px 18px;
      border-radius: 999px;
      border: 1px solid rgba(201, 163, 95, 0.3);
      color: var(--cream);
      text-decoration: none;
      font-size: 12px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      font-weight: 500;
      transition: all 0.25s ease;
    }}
    .ethnic-tab:hover, .ethnic-tab.active {{
      background: var(--gold);
      color: var(--ink-on-gold);
      border-color: var(--gold-light);
      box-shadow: 0 0 12px rgba(201, 163, 95, 0.3);
    }}

    /* Grid */
    .catalog-section {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 48px 28px 96px;
    }}
    .garments-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 36px 28px;
    }}

    .garment-card {{
      background: linear-gradient(180deg, rgba(20, 37, 27, 0.45) 0%, rgba(10, 18, 12, 0.85) 100%);
      border: 1px solid rgba(201, 163, 95, 0.3);
      border-radius: 200px 200px 18px 18px;
      padding: 12px 12px 20px;
      display: flex;
      flex-direction: column;
      transition: all 0.4s var(--ease);
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45);
    }}
    .garment-card:hover {{
      transform: translateY(-8px);
      border-color: rgba(201, 163, 95, 0.85);
      box-shadow: 0 24px 50px rgba(0, 0, 0, 0.65), 0 0 22px rgba(201, 163, 95, 0.22);
    }}

    .card-media {{
      position: relative;
      width: 100%;
      height: 380px;
      border-radius: 190px 190px 12px 12px;
      overflow: hidden;
      background: #040906;
    }}
    .card-media img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center top;
      transition: transform 0.8s var(--ease);
    }}
    .garment-card:hover .card-media img {{
      transform: scale(1.06);
    }}

    .card-info {{
      padding: 18px 8px 6px;
      display: flex;
      flex-direction: column;
      flex-grow: 1;
    }}
    .card-craft {{
      font-size: 10px;
      letter-spacing: 2px;
      text-transform: uppercase;
      color: var(--gold);
      font-weight: 600;
      margin-bottom: 6px;
    }}
    .card-title {{
      font-family: var(--serif);
      font-size: 19px;
      font-weight: 500;
      color: #ffffff;
      line-height: 1.25;
      margin-bottom: 8px;
    }}
    .card-fabric {{
      font-size: 12px;
      color: var(--cream);
      opacity: 0.8;
      margin-bottom: 12px;
      font-family: var(--serif-i);
      font-style: italic;
    }}
    .card-bottom-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-top: auto;
      padding-top: 14px;
      border-top: 1px solid rgba(201, 163, 95, 0.2);
    }}
    .card-price {{
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
    }}
    .card-cta-btn {{
      background: transparent;
      border: 1px solid rgba(201, 163, 95, 0.8);
      color: #ffffff !important;
      font-weight: 700;
      font-size: 10.5px;
      letter-spacing: 1.8px;
      text-transform: uppercase;
      padding: 8px 16px;
      border-radius: 999px;
      text-decoration: none;
      transition: all 0.25s ease;
    }}
    .card-cta-btn:hover {{
      background: var(--gold);
      color: var(--ink-on-gold) !important;
      box-shadow: 0 0 14px rgba(201, 163, 95, 0.35);
    }}

    /* Footer */
    .atelier-footer {{
      background: #060e09;
      border-top: 1px solid rgba(201, 163, 95, 0.2);
      padding: 48px 24px 32px;
      text-align: center;
    }}
    .footer-copy {{
      font-size: 11px;
      color: rgba(255, 255, 255, 0.45);
      letter-spacing: 1px;
      margin-top: 16px;
    }}
  </style>
</head>
<body>
  {header_html}

  <aside class="atelier-announcement">
    <span>✦ Aleen Haute Couture · Handcrafted Luxury Editions · Worldwide Atelier Shipping ✦</span>
  </aside>

  <section class="hero-banner">
    <p class="hero-eyebrow">Ethnic Haute Couture</p>
    <h1 class="hero-title">{title}</h1>
    <p class="hero-sub">"{sub}"</p>
  </section>

  <nav class="ethnic-tabs">
    <a href="sarees.html" class="ethnic-tab {act_sarees}">Sarees</a>
    <a href="kurta-sets.html" class="ethnic-tab {act_kurta_sets}">Kurta Sets</a>
    <a href="anarkali.html" class="ethnic-tab {act_anarkali}">Anarkali</a>
    <a href="suits.html" class="ethnic-tab {act_suits}">Suits</a>
    <a href="coord-sets.html" class="ethnic-tab {act_coord_sets}">Co-ord Sets</a>
    <a href="lehengas.html" class="ethnic-tab {act_lehengas}">Lehengas</a>
    <a href="dresses.html" class="ethnic-tab {act_dresses}">Dresses &amp; Sets</a>
  </nav>

  <main class="catalog-section">
    <div class="garments-grid" id="categoryGarmentsGrid">
      <!-- Injected live from localStorage/seed -->
    </div>
  </main>

  <footer class="atelier-footer">
    <div style="display: flex; justify-content: center; gap: 14px; margin-bottom: 18px;">
      <a href="index.html" class="btn btn-outline" style="border: 1px solid rgba(201,163,95,0.4); color: #fff; text-decoration: none; font-size: 11px; letter-spacing: 1.5px; padding: 8px 20px; border-radius: 999px; text-transform: uppercase;">← Return to Aleen Home</a>
      <a href="admin.html" title="Atelier Management Portal" style="width: 36px; height: 36px; border-radius: 50%; border: 1px solid rgba(201,163,95,0.4); background: rgba(20,37,27,0.5); color: #fff; display: flex; align-items: center; justify-content: center; text-decoration: none;">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
      </a>
    </div>
    <p class="footer-copy">© 2026 Aleen Clothing. Consciously Curated Luxury Garments. All Rights Reserved.</p>
  </footer>

  {header_script}

  <script>
  (function() {
    const CATEGORY = "{slug}";
    const grid = document.getElementById("categoryGarmentsGrid");

    const fallbackMap = {
      "sarees": [
        {{ title: "Chandramukhi Katan Silk Saree", price: 48500, craft: "Pure Zari & Meenakari", fabric: "Pure Banarasi Katan Silk", image: "https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5" }},
        {{ title: "Kalamkari Rooh Silk Saree", price: 34200, craft: "Pen Kalamkari & Vegetable Dyes", fabric: "Handspun Tussar Silk", image: "https://mahira2.netlify.app/assets/s2-room.jpg?v=4" }},
        {{ title: "Nirvana Organza Tissue Saree", price: 36000, craft: "Cutwork Gota Patti", fabric: "Pure Metallic Tissue Organza", image: "https://mahira2.netlify.app/assets/s7-story.jpg?v=4" }},
        {{ title: "Meenakari Jamdani Heritage Saree", price: 52000, craft: "Multi-hued Weft Inlay", fabric: "Fine Mulberry Silk", image: "https://mahira2.netlify.app/assets/s3-bg.jpg?v=1" }}
      ],
      "kurta-sets": [
        {{ title: "Gulmohar Chanderi Kurta Set", price: 26800, craft: "Marodi & Aari Needlework", fabric: "Tissue Chanderi with Silk Organza", image: "https://mahira2.netlify.app/assets/s3-kurta.jpg?v=5" }},
        {{ title: "Sitara Zari Handloom Kurta Set", price: 24500, craft: "Handloom Zari Booti", fabric: "Handspun Silk Chanderi", image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=1" }},
        {{ title: "Noor Tissue Brocade Kurta Set", price: 28900, craft: "Zari Jacquard & Mukaish", fabric: "Golden Tissue Silk", image: "https://mahira2.netlify.app/assets/s4-p1.jpg?v=2" }},
        {{ title: "Awadhi Shadow-work Kurta Set", price: 22000, craft: "Bakhiya Chikankari", fabric: "Pure Fine Georgette", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }}
      ],
      "anarkali": [
        {{ title: "Mumtaz 32-Kali Georgette Anarkali", price: 38500, craft: "32-Panel Chikankari & Mukaish", fabric: "Pure Viscose Georgette", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }},
        {{ title: "Noor Jahan Champagne Silk Anarkali", price: 42000, craft: "Pita Zari & Pearl Tassels", fabric: "Pure Tussar Silk", image: "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5" }},
        {{ title: "Amber Gilded Festive Anarkali", price: 34000, craft: "Gota Jaal & Dabka", fabric: "Tissue Crepe", image: "https://mahira2.netlify.app/assets/s5-p1.jpg?v=1" }},
        {{ title: "Pakeezah White Shadow Anarkali", price: 46000, craft: "Tepchi Chikankari & Pearls", fabric: "Opulent Handwoven Chanderi", image: "https://mahira2.netlify.app/assets/s3-bg.jpg?v=1" }}
      ],
      "suits": [
        {{ title: "Shahi Angrakha Velvet Suit", price: 32500, craft: "Zardozi Cord Work", fabric: "Micro Velvet & Brocade Pants", image: "https://mahira2.netlify.app/assets/women-clean.jpg?v=3" }},
        {{ title: "Zehra Silk Straight Suit Set", price: 25000, craft: "Dabka & Resham Borders", fabric: "Matka Silk with Zari Dupatta", image: "https://mahira2.netlify.app/assets/s2-room.jpg?v=4" }},
        {{ title: "Jahanara Peplum Kurti & Sharara", price: 29800, craft: "Gota Patti & Foil Inlay", fabric: "Pure Georgette", image: "https://mahira2.netlify.app/assets/s4-p1.jpg?v=2" }},
        {{ title: "Bageecha Brocade Formal Suit", price: 31000, craft: "Jacquard Weft & Pearl Trims", fabric: "Benarasi Tanchoi Brocade", image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=1" }}
      ],
      "coord-sets": [
        {{ title: "Roshni Draped Cape & Trousers", price: 23500, craft: "Hand-folded Micro Pleats", fabric: "Satin Silk with Georgette Cape", image: "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5" }},
        {{ title: "Zubeida Printed Silk Co-ord", price: 19800, craft: "Hand Block Print & Mirror Work", fabric: "Habotai Pure Silk", image: "https://mahira2.netlify.app/assets/s2-room.jpg?v=4" }},
        {{ title: "Tara Belted Kimono Co-ord", price: 21500, craft: "Zari Topstitching & Tassels", fabric: "Crepe de Chine", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }},
        {{ title: "Sultana Embroidered Vest & Pants", price: 27000, craft: "Gota Applique & Bullion Knots", fabric: "Raw Silk & Organza Overlay", image: "https://mahira2.netlify.app/assets/s5-p1.jpg?v=1" }}
      ],
      "lehengas": [
        {{ title: "Sheesh Mahal Bridal Lehenga", price: 135000, craft: "Zardozi & Dabka Resham", fabric: "Heritage Velvet & Tissue Silk", image: "https://mahira2.netlify.app/assets/women-clean.jpg?v=3" }},
        {{ title: "Vasant Garden Floral Lehenga", price: 92000, craft: "French Knot & Silk Floss", fabric: "Mulberry Organza & Crepe", image: "https://mahira2.netlify.app/assets/s3-bg.jpg?v=1" }},
        {{ title: "Darbari Meenakari Silk Lehenga", price: 118000, craft: "Real Zari Weft & Kundan Setting", fabric: "Pure Banarasi Brocade Silk", image: "https://mahira2.netlify.app/assets/s7-story.jpg?v=4" }},
        {{ title: "Chandni Raat Organza Lehenga", price: 78000, craft: "Silver Mukaish & Cutwork Scallops", fabric: "Metallic Tissue Organza", image: "https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5" }}
      ],
      "dresses": [
        {{ title: "Aura Champagne Flared Gown", price: 38900, craft: "Pita Work & Micro Pleating", fabric: "Raw Silk & Multilayered Tulle", image: "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5" }},
        {{ title: "Mehrunissa Draped Kaftan Set", price: 22400, craft: "Hand-rolled Zardozi Cords", fabric: "Italian Crepe de Chine", image: "https://mahira2.netlify.app/assets/s2-room.jpg?v=4" }},
        {{ title: "Chandini Tiered Maxi Gown", price: 27500, craft: "Badla Wire & Mirror Sequins", fabric: "Tissue Organza with Satin Slip", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }},
        {{ title: "Nazneen Asymmetric Cape Gown", price: 35000, craft: "Aari Needling & Cutdana", fabric: "Fine Mulberry Silk Georgette", image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=1" }}
      ]
    }};

    let items = fallbackMap[CATEGORY] || [];
    const stored = localStorage.getItem("aleen_master_catalog");
    if (stored) {{
      try {{
        const catalog = JSON.parse(stored);
        const filtered = catalog.filter(c => c.category === CATEGORY);
        if (filtered.length > 0) items = filtered;
      }} catch(e) {{}}
    }}

    grid.innerHTML = items.map(item => `
      <article class="garment-card">
        <div class="card-media">
          <img src="${{item.image}}" alt="${{item.title}}" loading="lazy" />
        </div>
        <div class="card-info">
          <span class="card-craft">${{item.craft || 'Artisanal'}}</span>
          <h2 class="card-title">${{item.title}}</h2>
          <p class="card-fabric">${{item.fabric || 'Pure Silk'}}</p>
          <div class="card-bottom-row">
            <span class="card-price">₹${{Number(item.price).toLocaleString('en-IN')}}</span>
            <a href="collections.html?category=${{CATEGORY}}" class="card-cta-btn">Examine Craft</a>
          </div>
        </div>
      </article>
    `).join('');
  }})();
  </script>
</body>
</html>
"""

for slug, filename, title, sub in ETHNIC_PAGES:
    html = ETHNIC_TEMPLATE.format(
        header_css=HEADER_CSS,
        header_html=HEADER_HTML,
        header_script=HEADER_SCRIPT,
        title=title,
        sub=sub,
        slug=slug,
        act_sarees="active" if slug == "sarees" else "",
        act_kurta_sets="active" if slug == "kurta-sets" else "",
        act_anarkali="active" if slug == "anarkali" else "",
        act_suits="active" if slug == "suits" else "",
        act_coord_sets="active" if slug == "coord-sets" else "",
        act_lehengas="active" if slug == "lehengas" else "",
        act_dresses="active" if slug == "dresses" else ""
    )
    with open(os.path.join(OUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated Aleen website/{filename}")
