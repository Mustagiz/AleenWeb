#!/usr/bin/env python3
"""
Generate all 7 Ethnic Haute Couture pages with Global Header & Footer:
- Sarees (sarees.html)
- Kurta Sets (kurta-sets.html)
- Anarkali Sets (anarkali.html)
- Royal Suits (suits.html)
- Co-ord Sets (coord-sets.html)
- Lehengas (lehengas.html)
- Dresses & Sets (dresses.html)
"""

import os
import sys

scripts_dir = os.path.dirname(os.path.abspath(__file__))
site_dir = os.path.abspath(os.path.join(scripts_dir, "..", "Aleen website"))
sys.path.insert(0, scripts_dir)

from shared_components import GLOBAL_HEADER_HTML, GLOBAL_FOOTER_HTML, GLOBAL_COMPONENTS_CSS, GLOBAL_HEADER_FOOTER_JS

ETHNIC_PAGES = [
  ("sarees", "sarees.html", "The Royal Saree Treasury", "Six yards of sheer majesty — Banarasi Katan, Pen Kalamkari, and hand-embroidered organza drapes."),
  ("kurta-sets", "kurta-sets.html", "The Handcrafted Kurta Sets Edit", "Everyday elegance elevated with Marodi needlework, antique gota, and tissue organza trims."),
  ("anarkali", "anarkali.html", "The Regal Anarkali Suite", "Voluminous 32-kali flares, heirloom Chikankari, and silver mukaish accents woven for royal presence."),
  ("suits", "suits.html", "Bespoke Royal Suits", "Structured silhouettes with antique threadwork, regal lapels, and handloom churidars."),
  ("coord-sets", "coord-sets.html", "The Contemporary Co-ord Sets", "Modern fluid luxury — tunic and palazzo ensembles crafted in pure silks and artisanal prints."),
  ("lehengas", "lehengas.html", "The Bridal & Festive Lehenga Edit", "Heirloom bridal ensembles detailed with beaten zardozi, semi-precious stones, and dual dupattas."),
  ("dresses", "dresses.html", "The Dresses & Sets Collection", "Fusion couture gowns and tiered maxi dresses crafted for red-carpet affairs and festive galas.")
]

for slug, filename, title, sub in ETHNIC_PAGES:
    act_s = "active" if slug == "sarees" else ""
    act_k = "active" if slug == "kurta-sets" else ""
    act_a = "active" if slug == "anarkali" else ""
    act_st = "active" if slug == "suits" else ""
    act_c = "active" if slug == "coord-sets" else ""
    act_l = "active" if slug == "lehengas" else ""
    act_d = "active" if slug == "dresses" else ""

    html = f"""<!DOCTYPE html>
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
    {GLOBAL_COMPONENTS_CSS}

    body {{
      background: var(--void-0);
      color: #ffffff;
      font-family: var(--sans);
      margin: 0;
      padding: 0;
      overflow-x: hidden;
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }}

    .ethnic-hero {{
      position: relative;
      min-height: 48vh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: clamp(100px, 12vh, 130px) 24px 40px;
      background: radial-gradient(ellipse at 50% 30%, rgba(20, 38, 26, 0.95), rgba(4, 9, 6, 0.98));
      border-bottom: 1px solid rgba(201, 163, 95, 0.25);
    }}
    .hero-content {{
      max-width: 840px;
      margin: 0 auto;
    }}
    .hero-eyebrow {{
      font-family: var(--serif-i);
      font-size: 13px;
      letter-spacing: 3.5px;
      text-transform: uppercase;
      color: var(--gold-light);
      margin-bottom: 12px;
      display: block;
    }}
    .hero-title {{
      font-family: var(--serif);
      font-size: clamp(32px, 4.2vw, 54px);
      font-weight: 500;
      color: #ffffff;
      margin: 0 0 16px 0;
      line-height: 1.18;
    }}
    .hero-sub {{
      font-family: var(--serif-i);
      font-style: italic;
      font-size: clamp(16px, 1.6vw, 21px);
      color: var(--cream);
      max-width: 680px;
      margin: 0 auto;
      line-height: 1.6;
    }}

    .ethnic-tabs {{
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 10px;
      padding: 20px 16px;
      background: rgba(11, 21, 14, 0.6);
      border-bottom: 1px solid rgba(201, 163, 95, 0.15);
    }}
    .ethnic-tab {{
      padding: 8px 18px;
      border-radius: 999px;
      border: 1px solid rgba(201, 163, 95, 0.3);
      color: var(--cream);
      text-decoration: none;
      font-size: 11.5px;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      font-weight: 500;
      transition: all 0.25s ease;
    }}
    .ethnic-tab:hover, .ethnic-tab.active {{
      background: var(--gold);
      color: #040906;
      border-color: var(--gold-light);
      box-shadow: 0 0 12px rgba(201, 163, 95, 0.3);
    }}

    .catalog-section {{
      max-width: 1440px;
      margin: 0 auto;
      padding: 48px clamp(20px, 3.5vw, 60px) 96px;
    }}
    .garments-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 36px 28px;
    }}
    @media (max-width: 1200px) {{
      .garments-grid {{ grid-template-columns: repeat(3, 1fr); }}
    }}
    @media (max-width: 860px) {{
      .garments-grid {{ grid-template-columns: repeat(2, 1fr); gap: 20px 16px; }}
    }}
    @media (max-width: 540px) {{
      .garments-grid {{ grid-template-columns: 1fr; }}
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
      color: #040906 !important;
      box-shadow: 0 0 14px rgba(201, 163, 95, 0.35);
    }}
  </style>
</head>
<body>

{GLOBAL_HEADER_HTML}

<header class="ethnic-hero">
  <div class="hero-content">
    <span class="hero-eyebrow">Ethnic Haute Couture</span>
    <h1 class="hero-title">{title}</h1>
    <p class="hero-sub">"{sub}"</p>
  </div>
</header>

<nav class="ethnic-tabs" aria-label="Haute Couture Categories">
  <a href="sarees.html" class="ethnic-tab {act_s}">Sarees</a>
  <a href="kurta-sets.html" class="ethnic-tab {act_k}">Kurta Sets</a>
  <a href="anarkali.html" class="ethnic-tab {act_a}">Anarkali Sets</a>
  <a href="suits.html" class="ethnic-tab {act_st}">Royal Suits</a>
  <a href="coord-sets.html" class="ethnic-tab {act_c}">Co-ord Sets</a>
  <a href="lehengas.html" class="ethnic-tab {act_l}">Lehengas</a>
  <a href="dresses.html" class="ethnic-tab {act_d}">Dresses &amp; Sets</a>
  <a href="collections.html" class="ethnic-tab">All Collections</a>
</nav>

<main class="catalog-section">
  <div class="garments-grid" id="garmentsGrid">
    <!-- Populated via JavaScript from Master Catalog -->
  </div>
</main>

{GLOBAL_FOOTER_HTML}

{GLOBAL_HEADER_FOOTER_JS}

<script>
(function() {{
  const CATEGORY = "{slug}";
  const grid = document.getElementById("garmentsGrid");
  if (!grid) return;

  const fallbackMap = {{
    "sarees": [
      {{ title: "Chandramukhi Katan Silk Saree", price: 48500, craft: "Pure Zari & Meenakari", fabric: "Pure Banarasi Katan Silk", image: "https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5" }},
      {{ title: "Kalamkari Rooh Silk Saree", price: 34200, craft: "Pen Kalamkari & Vegetable Dyes", fabric: "Handspun Tussar Silk", image: "https://mahira2.netlify.app/assets/s4-p2.jpg?v=3" }},
      {{ title: "Nirvana Organza Tissue Saree", price: 29500, craft: "Scalloped Cutwork & Mukaish", fabric: "Metallic Tissue Organza", image: "https://mahira2.netlify.app/assets/s5-p3.jpg?v=3" }},
      {{ title: "Zari Vanya Tussar Drape", price: 38000, craft: "Kadwa Zari Weave", fabric: "Wild Vanya Silk", image: "https://mahira2.netlify.app/assets/s5-p1.jpg?v=3" }}
    ],
    "kurta-sets": [
      {{ title: "Gulmohar Chanderi Kurta Set", price: 26800, craft: "Marodi & Aari Needlework", fabric: "Tissue Chanderi with Silk Organza", image: "https://mahira2.netlify.app/assets/s3-kurta.jpg?v=5" }},
      {{ title: "Mumtaz Anarkali Kurta Set", price: 28500, craft: "Gota Patti & Foil Inlay", fabric: "Pure Georgette with Chiffon", image: "https://mahira2.netlify.app/assets/s4-p1.jpg?v=3" }},
      {{ title: "Sitara Silk Straight Kurta", price: 22000, craft: "Dabka & French Knots", fabric: "Raw Mulberry Silk", image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=3" }},
      {{ title: "Meera Velvet Winter Kurta Set", price: 31500, craft: "Tilla Needlework & Cutwork", fabric: "Silk Velvet with Organza Veil", image: "https://mahira2.netlify.app/assets/s4-p3.jpg?v=3" }}
    ],
    "anarkali": [
      {{ title: "Zeenat Royal Anarkali Ensemble", price: 42000, craft: "32-Kali Mukaish & Chikankari", fabric: "Mulberry Georgette & Malmal", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }},
      {{ title: "Bagh-e-Fiza Tiered Anarkali", price: 36000, craft: "Heirloom Tilla Needlework", fabric: "Pure Chanderi Silk", image: "https://mahira2.netlify.app/assets/s5-p4.jpg?v=1" }},
      {{ title: "Mehr Angrakha Kali Suit", price: 39500, craft: "Zari Cord Work & Sequins", fabric: "Fine Organza Tissue", image: "https://mahira2.netlify.app/assets/s3-bg.jpg?v=1" }},
      {{ title: "Noor Mahal Velvet Anarkali", price: 46000, craft: "Embossed Zardozi Borders", fabric: "Silk Micro Velvet", image: "https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2" }}
    ],
    "suits": [
      {{ title: "Shahi Angrakha Velvet Suit", price: 32500, craft: "Zardozi Cord Work", fabric: "Micro Velvet & Brocade Pants", image: "https://mahira2.netlify.app/assets/women-clean.jpg?v=3" }},
      {{ title: "Zehra Silk Straight Suit Set", price: 25000, craft: "Dabka & Resham Borders", fabric: "Matka Silk with Zari Dupatta", image: "https://mahira2.netlify.app/assets/s2-room.jpg?v=4" }},
      {{ title: "Jahanara Peplum Kurti & Sharara", price: 29800, craft: "Gota Patti & Foil Inlay", fabric: "Pure Georgette", image: "https://mahira2.netlify.app/assets/s4-p1.jpg?v=3" }},
      {{ title: "Bageecha Brocade Formal Suit", price: 31000, craft: "Jacquard Weft & Pearl Trims", fabric: "Benarasi Tanchoi Brocade", image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=3" }}
    ],
    "coord-sets": [
      {{ title: "Roshni Draped Cape & Trousers", price: 23500, craft: "Hand-folded Micro Pleats", fabric: "Satin Silk with Georgette Cape", image: "https://mahira2.netlify.app/assets/s4-p3.jpg?v=3" }},
      {{ title: "Zubeida Printed Silk Co-ord", price: 19800, craft: "Hand Block Print & Mirror Work", fabric: "Habotai Pure Silk", image: "https://mahira2.netlify.app/assets/s2-room.jpg?v=4" }},
      {{ title: "Tara Belted Kimono Co-ord", price: 21500, craft: "Zari Topstitching & Tassels", fabric: "Crepe de Chine", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }},
      {{ title: "Sultana Embroidered Vest & Pants", price: 27000, craft: "Gota Applique & Bullion Knots", fabric: "Raw Silk & Organza Overlay", image: "https://mahira2.netlify.app/assets/s5-p1.jpg?v=3" }}
    ],
    "lehengas": [
      {{ title: "Sheesh Mahal Bridal Lehenga", price: 135000, craft: "Zardozi & Dabka Resham", fabric: "Heritage Velvet & Tissue Silk", image: "https://mahira2.netlify.app/assets/women-clean.jpg?v=3" }},
      {{ title: "Vasant Garden Floral Lehenga", price: 92000, craft: "French Knot & Silk Floss", fabric: "Mulberry Organza & Crepe", image: "https://mahira2.netlify.app/assets/s5-p1.jpg?v=3" }},
      {{ title: "Darbari Meenakari Silk Lehenga", price: 118000, craft: "Real Zari Weft & Kundan Setting", fabric: "Pure Banarasi Brocade Silk", image: "https://mahira2.netlify.app/assets/s7-story.jpg?v=4" }},
      {{ title: "Chandni Raat Organza Lehenga", price: 78000, craft: "Silver Mukaish & Cutwork Scallops", fabric: "Metallic Tissue Organza", image: "https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5" }}
    ],
    "dresses": [
      {{ title: "Aura Champagne Flared Gown", price: 38900, craft: "Pita Work & Micro Pleating", fabric: "Raw Silk & Multilayered Tulle", image: "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5" }},
      {{ title: "Mehrunissa Draped Kaftan Set", price: 22400, craft: "Hand-rolled Zardozi Cords", fabric: "Italian Crepe de Chine", image: "https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2" }},
      {{ title: "Chandini Tiered Maxi Gown", price: 27500, craft: "Badla Wire & Mirror Sequins", fabric: "Tissue Organza with Satin Slip", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }},
      {{ title: "Nazneen Asymmetric Cape Gown", price: 35000, craft: "Aari Needling & Cutdana", fabric: "Fine Mulberry Silk Georgette", image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=3" }}
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

  grid.innerHTML = items.map(function(item) {{
    return '<article class="garment-card">' +
      '<div class="card-media">' +
        '<img src="' + item.image + '" alt="' + item.title + '" loading="lazy" />' +
      '</div>' +
      '<div class="card-info">' +
        '<span class="card-craft">' + (item.craft || "Artisanal") + '</span>' +
        '<h2 class="card-title">' + item.title + '</h2>' +
        '<p class="card-fabric">' + (item.fabric || "Pure Silk") + '</p>' +
        '<div class="card-bottom-row">' +
          '<span class="card-price">₹' + Number(item.price).toLocaleString("en-IN") + '</span>' +
          '<a href="collections.html?category=' + CATEGORY + '" class="card-cta-btn">Examine Craft</a>' +
        '</div>' +
      '</div>' +
    '</article>';
  }}).join('');
}})();
</script>

</body>
</html>
"""
    fpath = os.path.join(site_dir, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Generated {filename} with Global Header & Footer")

print("✦ All 7 Ethnic pages generated successfully!")
      {{ title: "Kalamkari Rooh Silk Saree", price: 34200, craft: "Pen Kalamkari & Vegetable Dyes", fabric: "Handspun Tussar Silk", image: "https://mahira2.netlify.app/assets/s4-p2.jpg?v=3" }},
      {{ title: "Nirvana Organza Tissue Saree", price: 29500, craft: "Scalloped Cutwork & Mukaish", fabric: "Metallic Tissue Organza", image: "https://mahira2.netlify.app/assets/s5-p3.jpg?v=3" }},
      {{ title: "Zari Vanya Tussar Drape", price: 38000, craft: "Kadwa Zari Weave", fabric: "Wild Vanya Silk", image: "https://mahira2.netlify.app/assets/s5-p1.jpg?v=3" }}
    ],
    "kurta-sets": [
      {{ title: "Gulmohar Chanderi Kurta Set", price: 26800, craft: "Marodi & Aari Needlework", fabric: "Tissue Chanderi with Silk Organza", image: "https://mahira2.netlify.app/assets/s3-kurta.jpg?v=5" }},
      {{ title: "Mumtaz Anarkali Kurta Set", price: 28500, craft: "Gota Patti & Foil Inlay", fabric: "Pure Georgette with Chiffon", image: "https://mahira2.netlify.app/assets/s4-p1.jpg?v=3" }},
      {{ title: "Sitara Silk Straight Kurta", price: 22000, craft: "Dabka & French Knots", fabric: "Raw Mulberry Silk", image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=3" }},
      {{ title: "Meera Velvet Winter Kurta Set", price: 31500, craft: "Tilla Needlework & Cutwork", fabric: "Silk Velvet with Organza Veil", image: "https://mahira2.netlify.app/assets/s4-p3.jpg?v=3" }}
    ],
    "anarkali": [
      {{ title: "Zeenat Royal Anarkali Ensemble", price: 42000, craft: "32-Kali Mukaish & Chikankari", fabric: "Mulberry Georgette & Malmal", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }},
      {{ title: "Bagh-e-Fiza Tiered Anarkali", price: 36000, craft: "Heirloom Tilla Needlework", fabric: "Pure Chanderi Silk", image: "https://mahira2.netlify.app/assets/s5-p4.jpg?v=1" }},
      {{ title: "Mehr Angrakha Kali Suit", price: 39500, craft: "Zari Cord Work & Sequins", fabric: "Fine Organza Tissue", image: "https://mahira2.netlify.app/assets/s3-bg.jpg?v=1" }},
      {{ title: "Noor Mahal Velvet Anarkali", price: 46000, craft: "Embossed Zardozi Borders", fabric: "Silk Micro Velvet", image: "https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2" }}
    ],
    "suits": [
      {{ title: "Shahi Angrakha Velvet Suit", price: 32500, craft: "Zardozi Cord Work", fabric: "Micro Velvet & Brocade Pants", image: "https://mahira2.netlify.app/assets/women-clean.jpg?v=3" }},
      {{ title: "Zehra Silk Straight Suit Set", price: 25000, craft: "Dabka & Resham Borders", fabric: "Matka Silk with Zari Dupatta", image: "https://mahira2.netlify.app/assets/s2-room.jpg?v=4" }},
      {{ title: "Jahanara Peplum Kurti & Sharara", price: 29800, craft: "Gota Patti & Foil Inlay", fabric: "Pure Georgette", image: "https://mahira2.netlify.app/assets/s4-p1.jpg?v=3" }},
      {{ title: "Bageecha Brocade Formal Suit", price: 31000, craft: "Jacquard Weft & Pearl Trims", fabric: "Benarasi Tanchoi Brocade", image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=3" }}
    ],
    "coord-sets": [
      {{ title: "Roshni Draped Cape & Trousers", price: 23500, craft: "Hand-folded Micro Pleats", fabric: "Satin Silk with Georgette Cape", image: "https://mahira2.netlify.app/assets/s4-p3.jpg?v=3" }},
      {{ title: "Zubeida Printed Silk Co-ord", price: 19800, craft: "Hand Block Print & Mirror Work", fabric: "Habotai Pure Silk", image: "https://mahira2.netlify.app/assets/s2-room.jpg?v=4" }},
      {{ title: "Tara Belted Kimono Co-ord", price: 21500, craft: "Zari Topstitching & Tassels", fabric: "Crepe de Chine", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }},
      {{ title: "Sultana Embroidered Vest & Pants", price: 27000, craft: "Gota Applique & Bullion Knots", fabric: "Raw Silk & Organza Overlay", image: "https://mahira2.netlify.app/assets/s5-p1.jpg?v=3" }}
    ],
    "lehengas": [
      {{ title: "Sheesh Mahal Bridal Lehenga", price: 135000, craft: "Zardozi & Dabka Resham", fabric: "Heritage Velvet & Tissue Silk", image: "https://mahira2.netlify.app/assets/women-clean.jpg?v=3" }},
      {{ title: "Vasant Garden Floral Lehenga", price: 92000, craft: "French Knot & Silk Floss", fabric: "Mulberry Organza & Crepe", image: "https://mahira2.netlify.app/assets/s5-p1.jpg?v=3" }},
      {{ title: "Darbari Meenakari Silk Lehenga", price: 118000, craft: "Real Zari Weft & Kundan Setting", fabric: "Pure Banarasi Brocade Silk", image: "https://mahira2.netlify.app/assets/s7-story.jpg?v=4" }},
      {{ title: "Chandni Raat Organza Lehenga", price: 78000, craft: "Silver Mukaish & Cutwork Scallops", fabric: "Metallic Tissue Organza", image: "https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5" }}
    ],
    "dresses": [
      {{ title: "Aura Champagne Flared Gown", price: 38900, craft: "Pita Work & Micro Pleating", fabric: "Raw Silk & Multilayered Tulle", image: "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5" }},
      {{ title: "Mehrunissa Draped Kaftan Set", price: 22400, craft: "Hand-rolled Zardozi Cords", fabric: "Italian Crepe de Chine", image: "https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2" }},
      {{ title: "Chandini Tiered Maxi Gown", price: 27500, craft: "Badla Wire & Mirror Sequins", fabric: "Tissue Organza with Satin Slip", image: "https://mahira2.netlify.app/assets/s4-room.jpg?v=1" }},
      {{ title: "Nazneen Asymmetric Cape Gown", price: 35000, craft: "Aari Needling & Cutdana", fabric: "Fine Mulberry Silk Georgette", image: "https://mahira2.netlify.app/assets/s5-p2.jpg?v=3" }}
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

  grid.innerHTML = items.map(function(item) {{
    return '<article class="garment-card">' +
      '<div class="card-media">' +
        '<img src="' + item.image + '" alt="' + item.title + '" loading="lazy" />' +
      '</div>' +
      '<div class="card-info">' +
        '<span class="card-craft">' + (item.craft || "Artisanal") + '</span>' +
        '<h2 class="card-title">' + item.title + '</h2>' +
        '<p class="card-fabric">' + (item.fabric || "Pure Silk") + '</p>' +
        '<div class="card-bottom-row">' +
          '<span class="card-price">₹' + Number(item.price).toLocaleString("en-IN") + '</span>' +
          '<a href="collections.html?category=' + CATEGORY + '" class="card-cta-btn">Examine Craft</a>' +
        '</div>' +
      '</div>' +
    '</article>';
  }}).join('');
}})();
</script>

</body>
</html>
"""
    fpath = os.path.join(site_dir, filename)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Generated {filename} with Global Header & Footer")

print("✦ All 7 Ethnic pages generated successfully!")
