import os
import sys
from shared_header import HEADER_HTML, HEADER_CSS, HEADER_SCRIPT

PAGES = [
  {
    "slug": "sarees",
    "filename": "sarees.html",
    "title": "The Royal Saree Treasury",
    "eyebrow": "Ethnic Haute Couture",
    "sub": "Six yards of sheer majesty — Banarasi Katan, Pen Kalamkari, and hand-embroidered organza drapes.",
    "items": [
      {
        "title": "Chandramukhi Katan Silk Saree",
        "price": "₹48,500",
        "craft": "Pure Zari & Meenakari",
        "fabric": "Pure Banarasi Katan Silk",
        "image": "https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5",
        "desc": "Handwoven in the royal lofts of Varanasi over 140 artisan hours. Features real gold-dipped silver zari motifs across the pleated drape with opulent pallu styling."
      },
      {
        "title": "Kalamkari Rooh Silk Saree",
        "price": "₹34,200",
        "craft": "Pen Kalamkari & Vegetable Dyes",
        "fabric": "Handspun Tussar Silk",
        "image": "https://mahira2.netlify.app/assets/s2-room.jpg?v=4",
        "desc": "Entirely hand-painted with organic milk and plant dyes using bamboo pens. Depicts mystical forest motifs bordered in antique zari weave."
      },
      {
        "title": "Nirvana Organza Tissue Saree",
        "price": "₹36,000",
        "craft": "Cutwork Gota Patti",
        "fabric": "Pure Metallic Tissue Organza",
        "image": "https://mahira2.netlify.app/assets/s7-story.jpg?v=4",
        "desc": "Weightless drape reflecting amber candle glow. Features scalloped border embroidery with copper leafing and mirror accents."
      },
      {
        "title": "Meenakari Jamdani Heritage Saree",
        "price": "₹52,000",
        "craft": "Multi-hued Weft Inlay",
        "fabric": "Fine Mulberry Silk",
        "image": "https://mahira2.netlify.app/assets/s3-bg.jpg?v=1",
        "desc": "Intricate floral bootis inlaid by hand shuttle across a translucent silk body, finished with antique gold resham selvage."
      }
    ]
  },
  {
    "slug": "kurta-sets",
    "filename": "kurta-sets.html",
    "title": "The Handcrafted Kurta Sets Edit",
    "eyebrow": "Ethnic Haute Couture",
    "sub": "Everyday elegance elevated with Marodi needlework, antique gota, and tissue organza trims.",
    "items": [
      {
        "title": "Gulmohar Chanderi Kurta Set",
        "price": "₹26,800",
        "craft": "Marodi & Aari Needlework",
        "fabric": "Tissue Chanderi with Organza",
        "image": "https://mahira2.netlify.app/assets/s3-kurta.jpg?v=5",
        "desc": "Delicate dusty rose organza adorned with fine metallic badla and antique marodi needlecraft. Paired with straight-cut brocade trousers and scalloped veil."
      },
      {
        "title": "Sitara Zari Handloom Kurta Set",
        "price": "₹24,500",
        "craft": "Handloom Zari Booti",
        "fabric": "Handspun Silk Chanderi",
        "image": "https://mahira2.netlify.app/assets/s5-p2.jpg?v=1",
        "desc": "Gently illuminated with hand-tucked sequins and delicate zari florets. Tailored for all-day comfort and royal festive presence."
      },
      {
        "title": "Noor Tissue Brocade Kurta Set",
        "price": "₹28,900",
        "craft": "Zari Jacquard & Mukaish",
        "fabric": "Golden Tissue Silk",
        "image": "https://mahira2.netlify.app/assets/s4-p1.jpg?v=2",
        "desc": "Cut from liquid gold tissue silk woven on traditional looms, edged with hand-knotted pearl drops."
      },
      {
        "title": "Awadhi Shadow-work Kurta Set",
        "price": "₹22,000",
        "craft": "Bakhiya Chikankari",
        "fabric": "Pure Fine Georgette",
        "image": "https://mahira2.netlify.app/assets/s4-room.jpg?v=1",
        "desc": "Refined tonal embroidery executed with surgical precision on lightweight muslin-georgette, paired with scalloped palazzos."
      }
    ]
  },
  {
    "slug": "anarkali",
    "filename": "anarkali.html",
    "title": "The Regal Anarkali Suite",
    "eyebrow": "Ethnic Haute Couture",
    "sub": "Voluminous 32-kali flares, heirloom Chikankari, and silver mukaish accents woven for royal presence.",
    "items": [
      {
        "title": "Mumtaz 32-Kali Georgette Anarkali",
        "price": "₹38,500",
        "craft": "32-Panel Chikankari & Mukaish",
        "fabric": "Pure Viscose Georgette",
        "image": "https://mahira2.netlify.app/assets/s4-room.jpg?v=1",
        "desc": "A breathtaking 32-panel silhouette featuring hand-tucked silver mukaish and exquisite shadow needlework that sways majestically."
      },
      {
        "title": "Noor Jahan Champagne Silk Anarkali",
        "price": "₹42,000",
        "craft": "Pita Zari & Pearl Tassels",
        "fabric": "Pure Tussar Silk",
        "image": "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5",
        "desc": "Rich champagne silk structured with a corseted yoke and flowing flared kalis, paired with a hand-painted organza veil."
      },
      {
        "title": "Amber Gilded Festive Anarkali",
        "price": "₹34,000",
        "craft": "Gota Jaal & Dabka",
        "fabric": "Tissue Crepe",
        "image": "https://mahira2.netlify.app/assets/s5-p1.jpg?v=1",
        "desc": "Radiant amber tones accented with chevron gota borders and hand-beaded bullion flowers."
      },
      {
        "title": "Pakeezah White Shadow Anarkali",
        "price": "₹46,000",
        "craft": "Tepchi Chikankari & Pearls",
        "fabric": "Opulent Handwoven Chanderi",
        "image": "https://mahira2.netlify.app/assets/s3-bg.jpg?v=1",
        "desc": "Ivory dreamscape worked by master craftswomen over three months, paired with crushed tissue churidar and pearl drops."
      }
    ]
  },
  {
    "slug": "suits",
    "filename": "suits.html",
    "title": "Bespoke Royal Suits",
    "eyebrow": "Ethnic Haute Couture",
    "sub": "Structured silhouettes with antique threadwork, regal lapels, and handloom churidars.",
    "items": [
      {
        "title": "Shahi Angrakha Velvet Suit",
        "price": "₹32,500",
        "craft": "Zardozi Cord Work",
        "fabric": "Micro Velvet & Brocade Pants",
        "image": "https://mahira2.netlify.app/assets/women-clean.jpg?v=3",
        "desc": "Diagonal cross-over angrakha jacket enriched with antique gold cord work and real kundan buttons."
      },
      {
        "title": "Zehra Silk Straight Suit Set",
        "price": "₹25,000",
        "craft": "Dabka & Resham Borders",
        "fabric": "Matka Silk with Zari Dupatta",
        "image": "https://mahira2.netlify.app/assets/s2-room.jpg?v=4",
        "desc": "Clean-lined elegance in deep emerald green, framed by gold resham embroidery and cigarette trousers."
      },
      {
        "title": "Jahanara Peplum Kurti & Sharara",
        "price": "₹29,800",
        "craft": "Gota Patti & Foil Inlay",
        "fabric": "Pure Georgette",
        "image": "https://mahira2.netlify.app/assets/s4-p1.jpg?v=2",
        "desc": "Short flared peplum kurti paired with an opulent tiered sharara, radiating festive grace."
      },
      {
        "title": "Bageecha Brocade Formal Suit",
        "price": "₹31,000",
        "craft": "Jacquard Weft & Pearl Trims",
        "fabric": "Benarasi Tanchoi Brocade",
        "image": "https://mahira2.netlify.app/assets/s5-p2.jpg?v=1",
        "desc": "Lustrous all-over tanchoi weave with woven floral jaal and delicate pearl fringe detailing."
      }
    ]
  },
  {
    "slug": "coord-sets",
    "filename": "coord-sets.html",
    "title": "The Contemporary Co-ord Sets",
    "eyebrow": "Ethnic Haute Couture",
    "sub": "Modern fluid luxury — tunic and palazzo ensembles crafted in pure silks and artisanal prints.",
    "items": [
      {
        "title": "Roshni Draped Cape & Trousers",
        "price": "₹23,500",
        "craft": "Hand-folded Micro Pleats",
        "fabric": "Satin Silk with Georgette Cape",
        "image": "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5",
        "desc": "An effortless two-piece modern drape with a sweeping asymmetric cape and tailored silk trousers."
      },
      {
        "title": "Zubeida Printed Silk Co-ord",
        "price": "₹19,800",
        "craft": "Hand Block Print & Mirror Work",
        "fabric": "Habotai Pure Silk",
        "image": "https://mahira2.netlify.app/assets/s2-room.jpg?v=4",
        "desc": "Botanical hand-block motifs stamped with walnut and indigo vegetable dyes, finished with delicate mirror borders."
      },
      {
        "title": "Tara Belted Kimono Co-ord",
        "price": "₹21,500",
        "craft": "Zari Topstitching & Tassels",
        "fabric": "Crepe de Chine",
        "image": "https://mahira2.netlify.app/assets/s4-room.jpg?v=1",
        "desc": "Wrap-around tunic featuring hand-braided zari cords and coordinated flared culottes."
      },
      {
        "title": "Sultana Embroidered Vest & Pants",
        "price": "₹27,000",
        "craft": "Gota Applique & Bullion Knots",
        "fabric": "Raw Silk & Organza Overlay",
        "image": "https://mahira2.netlify.app/assets/s5-p1.jpg?v=1",
        "desc": "Architectural longline sleeveless vest worn over structured silk trousers with golden button accents."
      }
    ]
  },
  {
    "slug": "lehengas",
    "filename": "lehengas.html",
    "title": "The Bridal & Festive Lehenga Edit",
    "eyebrow": "Ethnic Haute Couture",
    "sub": "Heirloom bridal ensembles detailed with beaten zardozi, semi-precious stones, and dual dupattas.",
    "items": [
      {
        "title": "Sheesh Mahal Bridal Lehenga",
        "price": "₹1,35,000",
        "craft": "Zardozi & Dabka Resham",
        "fabric": "Heritage Velvet & Tissue Silk",
        "image": "https://mahira2.netlify.app/assets/women-clean.jpg?v=3",
        "desc": "Inspired by the mirrored halls of Amber Fort. Encased in genuine semi-precious bead embroidery, beaten metallic cord, and a dual tissue veil."
      },
      {
        "title": "Vasant Garden Floral Lehenga",
        "price": "₹92,000",
        "craft": "French Knot & Silk Floss",
        "fabric": "Mulberry Organza & Crepe",
        "image": "https://mahira2.netlify.app/assets/s3-bg.jpg?v=1",
        "desc": "A springtime dream composed of thousand-petal floral tapestries rendered in ombré pastel threads, crowned by an embroidered sweetheart bustier."
      },
      {
        "title": "Darbari Meenakari Silk Lehenga",
        "price": "₹1,18,000",
        "craft": "Real Zari Weft & Kundan Setting",
        "fabric": "Pure Banarasi Brocade Silk",
        "image": "https://mahira2.netlify.app/assets/s7-story.jpg?v=4",
        "desc": "Hand-loomed brocade skirt lined with antique silk can-can and accompanied by a zardozi velvet blouse."
      },
      {
        "title": "Chandni Raat Organza Lehenga",
        "price": "₹78,000",
        "craft": "Silver Mukaish & Cutwork Scallops",
        "fabric": "Metallic Tissue Organza",
        "image": "https://mahira2.netlify.app/assets/s3-sarees.jpg?v=5",
        "desc": "Gleaming like moonlight on water. Cascading sheer panels lined with metallic tissue and finished with teardrop pearls."
      }
    ]
  },
  {
    "slug": "dresses",
    "filename": "dresses.html",
    "title": "The Dresses & Sets Collection",
    "eyebrow": "Ethnic Haute Couture",
    "sub": "Fusion couture gowns and tiered maxi dresses crafted for red-carpet affairs and festive galas.",
    "items": [
      {
        "title": "Aura Champagne Flared Gown",
        "price": "₹38,900",
        "craft": "Pita Work & Micro Pleating",
        "fabric": "Raw Silk & Multilayered Tulle",
        "image": "https://mahira2.netlify.app/assets/s3-dresses.jpg?v=5",
        "desc": "Contemporary architectural drape meeting traditional hand-embroidery. A 32-meter flare cut structured for gala celebrations."
      },
      {
        "title": "Mehrunissa Draped Kaftan Set",
        "price": "₹22,400",
        "craft": "Hand-rolled Zardozi Cords",
        "fabric": "Italian Crepe de Chine",
        "image": "https://mahira2.netlify.app/assets/s2-room.jpg?v=4",
        "desc": "Effortless luxury designed for intimate soirees. Relaxed silhouette cinched with an ornate hand-beaded bullion belt."
      },
      {
        "title": "Chandini Tiered Maxi Gown",
        "price": "₹27,500",
        "craft": "Badla Wire & Mirror Sequins",
        "fabric": "Tissue Organza with Satin Slip",
        "image": "https://mahira2.netlify.app/assets/s4-room.jpg?v=1",
        "desc": "Three-tiered cascade of shimmering tissue organza that moves effortlessly with every step."
      },
      {
        "title": "Nazneen Asymmetric Cape Gown",
        "price": "₹35,000",
        "craft": "Aari Needling & Cutdana",
        "fabric": "Fine Mulberry Silk Georgette",
        "image": "https://mahira2.netlify.app/assets/s5-p2.jpg?v=1",
        "desc": "Floor-length column gown styled with an attached sheer embroidered shoulder cape and crystal embellishments."
      }
    ]
  }
]

TEMPLATE = """<!DOCTYPE html>
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
    <p class="hero-eyebrow">{eyebrow}</p>
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
    <div class="garments-grid">
      {cards_html}
    </div>
  </main>

  <footer class="atelier-footer">
    <div class="f-atelier-portal-bar">
      <a href="/login" class="f-atelier-portal-link" title="Atelier Staff & Garment Management Console">
        <span class="spark" style="color: var(--gold);">✦</span>
        <span style="font-weight: 700; letter-spacing: 1.8px; color: #FFFFFF;">Atelier Manager Login</span>
        <span style="font-size: 11px; opacity: 0.85; color: var(--gold-light);">— Manage, Edit &amp; Update Garments</span>
      </a>
    </div>
    <p class="footer-copy">© 2026 Aleen Clothing. Consciously Curated Luxury Garments. All Rights Reserved.</p>
  </footer>

  {header_script}
</body>
</html>
"""

def generate():
  out_dir = os.path.abspath("Aleen-react2/public")
  for page in PAGES:
    slug = page["slug"]
    cards_html = ""
    for item in page["items"]:
      # Note: No .card-badge or "BESTSELLER" in cards as requested
      cards_html += f"""
        <article class="garment-card">
          <div class="card-media">
            <img src="{item['image']}" alt="{item['title']}" loading="lazy" />
          </div>
          <div class="card-info">
            <span class="card-craft">{item['craft']}</span>
            <h2 class="card-title">{item['title']}</h2>
            <p class="card-fabric">{item['fabric']}</p>
            <div class="card-bottom-row">
              <span class="card-price">{item['price']}</span>
              <a href="collections.html?category={slug}" class="card-cta-btn">Examine Craft</a>
            </div>
          </div>
        </article>
      """
    
    html = TEMPLATE.format(
      header_css=HEADER_CSS,
      header_html=HEADER_HTML,
      header_script=HEADER_SCRIPT,
      title=page["title"],
      eyebrow=page["eyebrow"],
      sub=page["sub"],
      cards_html=cards_html,
      act_sarees="active" if slug == "sarees" else "",
      act_kurta_sets="active" if slug == "kurta-sets" else "",
      act_anarkali="active" if slug == "anarkali" else "",
      act_suits="active" if slug == "suits" else "",
      act_coord_sets="active" if slug == "coord-sets" else "",
      act_lehengas="active" if slug == "lehengas" else "",
      act_dresses="active" if slug == "dresses" else ""
    )
    
    filepath = os.path.join(out_dir, page["filename"])
    with open(filepath, "w", encoding="utf-8") as f:
      f.write(html)
    print(f"Generated {filepath}")

if __name__ == "__main__":
  generate()
