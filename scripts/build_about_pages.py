import os
from shared_components import GLOBAL_HEADER_HTML, GLOBAL_FOOTER_HTML, GLOBAL_COMPONENTS_CSS, GLOBAL_HEADER_FOOTER_JS

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Aleen website"))

COMMON_PAGE_STYLES = f"""
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
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

    .editorial-hero {{
      position: relative;
      min-height: 52vh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 140px 24px 60px;
      background: radial-gradient(circle at 50% 30%, #15271c 0%, #060e08 85%);
      border-bottom: 1px solid rgba(201, 163, 95, 0.25);
    }}
    .hero-kicker {{
      font-family: var(--sans);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 4px;
      text-transform: uppercase;
      color: var(--gold-light);
      margin-bottom: 14px;
      display: block;
    }}
    .hero-title {{
      font-family: var(--serif);
      font-size: clamp(34px, 5.2vw, 62px);
      font-weight: 400;
      color: var(--cream-hi);
      line-height: 1.15;
      margin-bottom: 18px;
    }}
    .hero-subtitle {{
      font-family: var(--serif-i);
      font-size: clamp(18px, 2vw, 24px);
      color: var(--cream);
      max-width: 680px;
      margin: 0 auto;
      line-height: 1.5;
      opacity: 0.9;
    }}

    .page-container {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 80px 24px 100px;
    }}

    .section-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 60px;
      align-items: center;
      margin-bottom: 80px;
    }}
    .section-grid.reverse {{
      direction: rtl;
    }}
    .section-grid.reverse > * {{
      direction: ltr;
    }}
    .img-frame {{
      position: relative;
      border-radius: 200px 200px 16px 16px;
      overflow: hidden;
      border: 1px solid rgba(201, 163, 95, 0.4);
      box-shadow: 0 20px 50px rgba(0,0,0,0.6);
      height: 480px;
    }}
    .img-frame img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .content-block h3 {{
      font-family: var(--serif);
      font-size: clamp(26px, 2.6vw, 36px);
      color: var(--cream-hi);
      margin-bottom: 20px;
      line-height: 1.3;
    }}
    .content-block p {{
      font-size: 15px;
      line-height: 1.85;
      color: rgba(239, 228, 200, 0.85);
      margin-bottom: 20px;
    }}
    .card-cluster {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 30px;
      margin-top: 50px;
    }}
    .luxury-card {{
      background: linear-gradient(180deg, rgba(20, 37, 27, 0.5) 0%, rgba(8, 16, 11, 0.85) 100%);
      border: 1px solid rgba(201, 163, 95, 0.3);
      border-radius: 16px;
      padding: 34px 28px;
      transition: transform 0.3s ease, border-color 0.3s ease;
    }}
    .luxury-card:hover {{
      transform: translateY(-6px);
      border-color: var(--gold);
    }}
    .luxury-card h4 {{
      font-family: var(--serif);
      font-size: 20px;
      color: var(--gold-spark);
      margin-bottom: 12px;
    }}
    .luxury-card p {{
      font-size: 14px;
      line-height: 1.7;
      color: rgba(239, 228, 200, 0.8);
    }}

    .action-cta-box {{
      text-align: center;
      padding: 60px 30px;
      background: radial-gradient(circle at 50% 50%, #15291e 0%, #07100b 100%);
      border: 1px solid rgba(201, 163, 95, 0.35);
      border-radius: 24px;
      margin-top: 60px;
    }}
    .action-cta-box h3 {{
      font-family: var(--serif);
      font-size: 32px;
      color: var(--cream-hi);
      margin-bottom: 12px;
    }}
    .action-cta-box p {{
      font-size: 15px;
      color: var(--cream);
      margin-bottom: 28px;
    }}
    .btn-gold {{
      display: inline-block;
      padding: 14px 34px;
      background: var(--gold);
      color: #241A0C;
      text-decoration: none;
      font-family: var(--sans);
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      border-radius: 999px;
      border: 1px solid var(--gold-light);
      transition: all 0.3s ease;
    }}
    .btn-gold:hover {{
      background: var(--gold-spark);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(201, 163, 95, 0.4);
    }}

    @media (max-width: 900px) {{
      .section-grid, .section-grid.reverse {{
        grid-template-columns: 1fr;
        direction: ltr;
        gap: 40px;
      }}
      .img-frame {{
        height: 360px;
      }}
    }}
  </style>
"""

PAGES = [
    {
        "filename": "our-story.html",
        "title": "Our Story — Aleen Clothing | Tradition Meets Tomorrow",
        "kicker": "The Atelier Chronicle",
        "heading": "Tradition Lives Beautifully",
        "sub": "A slow fashion sanctuary celebrating India's artisanal lineage with a contemporary editorial soul.",
        "content": """
        <div class="section-grid">
          <div class="img-frame">
            <img src="https://mahira2.netlify.app/assets/s7-story.jpg?v=4" alt="Aleen Heritage Weaver Model" />
          </div>
          <div class="content-block">
            <span class="hero-kicker">Genesis</span>
            <h3>Rooted in Reverence for Timeless Drape</h3>
            <p>Aleen Clothing was born out of a desire to protect and elevate the magnificent handloom traditions of India. In an age dominated by transient trends and synthetic fabrications, we anchor our craft in slow, conscious couture.</p>
            <p>Every piece in our atelier is a symphony between the master weavers of Varanasi, Chanderi, and Bengal, and contemporary silhouettes designed for the discerning global patron. When you wear Aleen, you wear centuries of quiet luxury.</p>
          </div>
        </div>

        <div class="card-cluster">
          <div class="luxury-card">
            <h4>Authentic Looms</h4>
            <p>We work exclusively with certified artisanal clusters, ensuring every yard of silk and organza is loomed with genuine gold and silver zari.</p>
          </div>
          <div class="luxury-card">
            <h4>Consciously Curated</h4>
            <p>Small-batch releases that respect the artisan's pace. We produce in limited quantities to eliminate waste and uphold craftsmanship.</p>
          </div>
          <div class="luxury-card">
            <h4>Empowering Lineage</h4>
            <p>Direct patronage ensures that ancient weaving families receive sustainable livelihood, training, and rightful generational honor.</p>
          </div>
        </div>

        <div class="action-cta-box">
          <h3>Explore the Pieces Shaped by This Journey</h3>
          <p>Discover our handpicked sarees, majestic kurta sets, and bespoke anarkalis.</p>
          <a href="collections.html" class="btn-gold">Explore All Collections &rarr;</a>
        </div>
        """
    },
    {
        "filename": "the-complete-journey.html",
        "title": "The Complete Journey — From Seed to Silhouette | Aleen Clothing",
        "kicker": "Step by Step",
        "heading": "The Complete Journey",
        "sub": "Trace the artisanal lifecycle of every garment — from ethical mulberry cocoons to the master cutter's table.",
        "content": """
        <div class="section-grid reverse">
          <div class="img-frame">
            <img src="https://mahira2.netlify.app/assets/s4-room.jpg?v=1" alt="Artisan Weaving Table" />
          </div>
          <div class="content-block">
            <span class="hero-kicker">Phase 01 &middot; Ethical Silk Harvest</span>
            <h3>Pure Mulberries & Natural Fiber</h3>
            <p>Our journey begins in sustainable sericulture farms where mulberry silkworms yield the softest raw silk filaments. No harsh bleaching or plastic resins are ever applied to our pure threads.</p>
            <p>Once reeled, the raw silk travels directly to our dyeing vats where master colorists blend turmeric, pomegranate rinds, and madder root for natural, lightfast pigmentation.</p>
          </div>
        </div>

        <div class="section-grid">
          <div class="img-frame">
            <img src="https://mahira2.netlify.app/assets/s5-room.jpg?v=1" alt="Intricate Handloom Weaving" />
          </div>
          <div class="content-block">
            <span class="hero-kicker">Phase 02 &middot; 400 Hours of Loom Time</span>
            <h3>The Rhythms of Handloom Heritage</h3>
            <p>A single Aleen bridal saree or Jamdani kurta requires between 180 to 400 hours on a wooden pit loom. Two master weavers collaborate in tandem — one synchronizing the pedals while the other hand-inserts delicate gold bootis.</p>
            <p>No high-speed automation can replicate the nuanced drape, textured drape-memory, and emotional warmth of handwoven pure silk.</p>
          </div>
        </div>

        <div class="card-cluster">
          <div class="luxury-card">
            <h4>01. Reeling</h4>
            <p>Hand-harvested filaments spun into multi-ply warp and weft silk.</p>
          </div>
          <div class="luxury-card">
            <h4>02. Dyeing</h4>
            <p>Vat-dyed with low-impact botanical and mineral hues.</p>
          </div>
          <div class="luxury-card">
            <h4>03. Weaving</h4>
            <p>Traditional wooden Jacquard & pit loom orchestrations.</p>
          </div>
          <div class="luxury-card">
            <h4>04. Atelier Finish</h4>
            <p>Hand-hemming, bespoke lining, and inspection by our master tailor.</p>
          </div>
        </div>

        <div class="action-cta-box">
          <h3>Witness Craft in Motion</h3>
          <p>Book a bespoke showroom consultation to touch and drape our latest pieces.</p>
          <a href="contact-us.html" class="btn-gold">Book Atelier Consultation &rarr;</a>
        </div>
        """
    },
    {
        "filename": "contact-us.html",
        "title": "Contact Us — Aleen Haute Atelier Concierge",
        "kicker": "Private Appointments & Inquiries",
        "heading": "Atelier Concierge",
        "sub": "We invite you to connect with our stylists, reserve private fittings, or request bespoke garment tailoring.",
        "content": """
        <div class="section-grid">
          <div class="content-block">
            <span class="hero-kicker">Direct Assistance</span>
            <h3>Let Us Curate Your Ensemble</h3>
            <p>Whether you require customized bridal fittings, advice on textile provenance, or express global delivery for upcoming festivities, our dedicated concierges are at your service.</p>
            
            <div style="margin: 28px 0; border-top: 1px solid rgba(201, 163, 95, 0.3); padding-top: 20px;">
              <p style="margin-bottom: 8px; color: var(--gold-light); font-weight: 600;">✦ Atelier Flagship</p>
              <p style="font-size: 14px; color: rgba(239, 228, 200, 0.85); margin-bottom: 16px;">The Aleen Atelier &middot; Heritage Design District &middot; New Delhi &middot; India</p>

              <p style="margin-bottom: 8px; color: var(--gold-light); font-weight: 600;">✦ Direct Concierge Line</p>
              <p style="font-size: 14px; color: rgba(239, 228, 200, 0.85); margin-bottom: 16px;">+91 98765 43210 &middot; Mon &ndash; Sat, 10:00 AM &ndash; 7:30 PM IST</p>

              <p style="margin-bottom: 8px; color: var(--gold-light); font-weight: 600;">✦ Electronic Mail</p>
              <p style="font-size: 14px; color: rgba(239, 228, 200, 0.85);">concierge@aleenclothing.com</p>
            </div>
          </div>

          <div class="luxury-card" style="padding: 40px 32px;">
            <h4 style="font-size: 24px; color: var(--cream-hi); margin-bottom: 6px;">Send Atelier Inquiry</h4>
            <p style="margin-bottom: 24px; font-size: 13.5px;">Our stylist will respond within 4 hours.</p>

            <form onsubmit="event.preventDefault(); document.getElementById('contactSent').style.display='block'; this.style.display='none';">
              <div style="margin-bottom: 16px;">
                <input type="text" placeholder="Your Full Name *" required style="width: 100%; padding: 13px 18px; background: rgba(4, 9, 6, 0.7); border: 1px solid rgba(201, 163, 95, 0.4); border-radius: 8px; color: #fff; font-family: var(--sans); font-size: 13px; outline: none;">
              </div>
              <div style="margin-bottom: 16px;">
                <input type="email" placeholder="Your Email Address *" required style="width: 100%; padding: 13px 18px; background: rgba(4, 9, 6, 0.7); border: 1px solid rgba(201, 163, 95, 0.4); border-radius: 8px; color: #fff; font-family: var(--sans); font-size: 13px; outline: none;">
              </div>
              <div style="margin-bottom: 16px;">
                <select style="width: 100%; padding: 13px 18px; background: rgba(4, 9, 6, 0.9); border: 1px solid rgba(201, 163, 95, 0.4); border-radius: 8px; color: var(--cream); font-family: var(--sans); font-size: 13px; outline: none;">
                  <option>Bespoke Bridal Consultation</option>
                  <option>Garment Sizing & Tailoring Inquiry</option>
                  <option>Order & Worldwide Shipping Assistance</option>
                  <option>Media & Editorial Collaboration</option>
                </select>
              </div>
              <div style="margin-bottom: 20px;">
                <textarea rows="4" placeholder="Your Message or Styling Requirements..." required style="width: 100%; padding: 13px 18px; background: rgba(4, 9, 6, 0.7); border: 1px solid rgba(201, 163, 95, 0.4); border-radius: 8px; color: #fff; font-family: var(--sans); font-size: 13px; outline: none;"></textarea>
              </div>
              <button type="submit" class="btn-gold" style="width: 100%; cursor: pointer;">Send Message &rarr;</button>
            </form>

            <div id="contactSent" style="display: none; text-align: center; padding: 24px 0;">
              <p style="font-family: var(--serif); font-size: 20px; color: var(--gold-light); margin-bottom: 8px;">Message Received with Honor</p>
              <p style="font-size: 13.5px; color: var(--cream);">Our senior stylist has received your request and will connect with you promptly.</p>
            </div>
          </div>
        </div>
        """
    }
]

for p in PAGES:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <title>{p['title']}</title>
{COMMON_PAGE_STYLES}
</head>
<body>
{GLOBAL_HEADER_HTML}

<main id="main">
  <section class="editorial-hero">
    <div>
      <span class="hero-kicker">{p['kicker']}</span>
      <h1 class="hero-title">{p['heading']}</h1>
      <p class="hero-subtitle">"{p['sub']}"</p>
    </div>
  </section>

  <div class="page-container">
    {p['content']}
  </div>
</main>

{GLOBAL_FOOTER_HTML}
{GLOBAL_HEADER_FOOTER_JS}
</body>
</html>
"""
    dest = os.path.join(SITE_DIR, p["filename"])
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✦ Created {p['filename']}")

print("✦ All 7 ABOUT pages generated successfully!")

