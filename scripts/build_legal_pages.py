import os
from shared_components import GLOBAL_HEADER_HTML, GLOBAL_FOOTER_HTML, GLOBAL_COMPONENTS_CSS, GLOBAL_HEADER_FOOTER_JS

SITE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Aleen website"))

PAGE_STYLES = f"""
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

    .legal-hero {{
      position: relative;
      min-height: 40vh;
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 140px 24px 50px;
      background: radial-gradient(circle at 50% 30%, #15271c 0%, #060e08 85%);
      border-bottom: 1px solid rgba(201, 163, 95, 0.25);
    }}
    .legal-kicker {{
      font-family: var(--sans);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 4px;
      text-transform: uppercase;
      color: var(--gold-light);
      margin-bottom: 12px;
      display: block;
    }}
    .legal-title {{
      font-family: var(--serif);
      font-size: clamp(32px, 4.5vw, 54px);
      font-weight: 400;
      color: var(--cream-hi);
      line-height: 1.2;
      margin-bottom: 14px;
    }}
    .legal-subtitle {{
      font-family: var(--serif-i);
      font-size: clamp(16px, 1.8vw, 22px);
      color: var(--cream);
      max-width: 640px;
      margin: 0 auto;
      line-height: 1.5;
      opacity: 0.85;
    }}

    .legal-container {{
      max-width: 960px;
      margin: 0 auto;
      padding: 70px 24px 100px;
    }}
    .legal-card {{
      background: linear-gradient(180deg, rgba(20, 37, 27, 0.45) 0%, rgba(8, 16, 11, 0.85) 100%);
      border: 1px solid rgba(201, 163, 95, 0.3);
      border-radius: 20px;
      padding: clamp(30px, 4.5vw, 56px);
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
    }}
    .legal-section {{
      margin-bottom: 36px;
    }}
    .legal-section:last-child {{
      margin-bottom: 0;
    }}
    .legal-section h3 {{
      font-family: var(--serif);
      font-size: 22px;
      color: var(--gold-spark);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .legal-section h3::before {{
      content: '✦';
      font-size: 14px;
      color: var(--gold);
    }}
    .legal-section p, .legal-section li {{
      font-size: 14.5px;
      line-height: 1.8;
      color: rgba(239, 228, 200, 0.82);
    }}
    .legal-section ul {{
      padding-left: 20px;
      margin: 12px 0;
    }}
    .legal-section li {{
      margin-bottom: 8px;
    }}

    /* Sitemap Grid */
    .sitemap-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 32px;
    }}
    .sitemap-col h4 {{
      font-family: var(--serif);
      font-size: 20px;
      color: var(--gold-light);
      margin-bottom: 16px;
      padding-bottom: 8px;
      border-bottom: 1px solid rgba(201, 163, 95, 0.3);
    }}
    .sitemap-col a {{
      display: block;
      color: rgba(239, 228, 200, 0.85);
      text-decoration: none;
      font-size: 14px;
      padding: 7px 0;
      transition: color 0.2s ease, transform 0.2s ease;
    }}
    .sitemap-col a:hover {{
      color: var(--gold-spark);
      transform: translateX(4px);
    }}
  </style>
"""

LEGAL_PAGES = [
    {
        "filename": "privacy.html",
        "title": "Privacy Policy — Aleen Clothing",
        "kicker": "Atelier Governance",
        "heading": "Privacy Policy",
        "sub": "Our solemn commitment to protecting the sanctity of your private patron data.",
        "content": """
        <div class="legal-card">
          <div class="legal-section">
            <p>Last Updated: November 2026</p>
            <p>At Aleen Clothing, we honor your privacy as fiercely as we revere our artisanal heritage. This Privacy Policy delineates how we collect, safeguard, and conscientiously utilize your information when you browse our boutique website, consult our atelier, or acquire handcrafted couture.</p>
          </div>

          <div class="legal-section">
            <h3>Information Entrusted to Us</h3>
            <p>When you interact with Aleen Clothing, we may collect the following details:</p>
            <ul>
              <li><strong>Contact Particulars:</strong> Name, shipping address, bespoke delivery instructions, electronic mail, and mobile contact.</li>
              <li><strong>Atelier Sizing & Drape Measurements:</strong> Custom blouse, anarkali, or bridal drape measurements shared during private tailor consultations.</li>
              <li><strong>Transaction Records:</strong> Billing summaries and acquisition histories (all financial payment processing is handled through PCI-DSS certified encrypted gateways; no raw card data is ever retained on our servers).</li>
            </ul>
          </div>

          <div class="legal-section">
            <h3>Purpose of Data Curation</h3>
            <p>Your details are curated solely for:</p>
            <ul>
              <li>Fulfilling bespoke tailoring, hand-hemming, and insured boutique dispatch.</li>
              <li>Transmitting order dispatches and private invitations to exclusive collection previews (only with your explicit consent).</li>
              <li>Providing dedicated lifetime repair and restoration concierge services for your garments.</li>
            </ul>
          </div>

          <div class="legal-section">
            <h3>Non-Disclosure Guarantee</h3>
            <p>Aleen Clothing will never trade, license, or monetize your private patron records. Data is accessed solely by our internal atelier managers, logistics couriers, and master tailors strictly for fulfilling your couture requirements.</p>
          </div>

          <div class="legal-section">
            <h3>Your Prerogatives & Contact</h3>
            <p>You may at any time request inspection, modification, or complete erasure of your patron records by contacting our Data Privacy Officer at <code>privacy@aleenclothing.com</code>.</p>
          </div>
        </div>
        """
    },
    {
        "filename": "terms.html",
        "title": "Terms & Conditions — Aleen Clothing",
        "kicker": "Boutique Agreement",
        "heading": "Terms & Conditions",
        "sub": "The terms of patronage governing bespoke orders, handloom variations, and atelier acquisitions.",
        "content": """
        <div class="legal-card">
          <div class="legal-section">
            <p>Last Updated: November 2026</p>
            <p>Welcome to Aleen Clothing. By accessing our website, reserving private fittings, or acquiring atelier creations, you enter into mutual accord with these Terms & Conditions.</p>
          </div>

          <div class="legal-section">
            <h3>Artisanal Handcraft Nuances</h3>
            <p>Every Aleen garment is woven on traditional wooden pit looms or hand-embroidered by master zardozi craftspeople. Natural variations in weft slubs, handloom selvedges, and botanical dye tonal depths are inherent hallmarks of authentic slow craft rather than defects.</p>
          </div>

          <div class="legal-section">
            <h3>Bespoke Orders & Tailoring</h3>
            <ul>
              <li>Custom measurements provided during private atelier consultations are crafted with up to 2 inches of internal luxury seam allowances for future adjustments.</li>
              <li>Because bespoke garments are individually dyed and loomed for a specific patron, cancellations cannot be processed once loom warping commences (typically 48 hours post-consultation).</li>
            </ul>
          </div>

          <div class="legal-section">
            <h3>Insured Worldwide Dispatch</h3>
            <p>Every Aleen parcel is dispatched in sealed, tamper-evident museum-grade packaging under transit insurance. Patrons receive live tracking and concierge notifications upon courier pickup.</p>
          </div>

          <div class="legal-section">
            <h3>Exchange & Atelier Store Credit</h3>
            <p>Standard collection pieces in unworn, unaltered condition with original wax seals intact may be exchanged within 14 days of delivery. Due to individual hygiene and bespoke sizing, custom-tailored drapes and cut fabrics are eligible for complimentary alterations rather than cash returns.</p>
          </div>

          <div class="legal-section">
            <h3>Intellectual Property & Heritage Protection</h3>
            <p>All designs, silhouette patterns, editorial imagery, and brand emblems displayed on this platform are proprietary to Aleen Clothing. Reproduction or unauthorized digital appropriation is strictly prohibited.</p>
          </div>
        </div>
        """
    },
    {
        "filename": "sitemap.html",
        "title": "Sitemap — Aleen Clothing Architecture",
        "kicker": "Website Directory",
        "heading": "Atelier Sitemap",
        "sub": "A complete architectural index of our collections, editorial stories, and patron services.",
        "content": """
        <div class="legal-card">
          <div class="sitemap-grid">
            <div class="sitemap-col">
              <h4>Boutique Collections</h4>
              <a href="index.html">✦ Home Page</a>
              <a href="collections.html">✦ The Haute Garments Gallery</a>
              <a href="collections.html?category=sarees">✦ Sarees Collection</a>
              <a href="collections.html?category=kurta-sets">✦ Kurta Sets</a>
              <a href="collections.html?category=lehengas">✦ Royal Lehengas</a>
              <a href="collections.html?category=dresses">✦ Contemporary Dresses &amp; Sets</a>
              <a href="collections.html?category=dupattas">✦ Kalamkari Dupattas</a>
              <a href="collections.html?category=unstitched">✦ Handloom Unstitched Silks</a>
            </div>

            <div class="sitemap-col">
              <h4>Ethnic Categories</h4>
              <a href="sarees.html">✦ Sarees Haute Edit</a>
              <a href="kurta-sets.html">✦ Kurta Sets Atelier</a>
              <a href="anarkali.html">✦ Royal Anarkali Drapes</a>
              <a href="suits.html">✦ Bespoke Suits</a>
              <a href="coord-sets.html">✦ Artisan Co-ord Sets</a>
              <a href="lehengas.html">✦ Bridal Lehengas</a>
              <a href="dresses.html">✦ Flared Gowns &amp; Dresses</a>
            </div>

            <div class="sitemap-col">
              <h4>Editorial &amp; Heritage</h4>
              <a href="our-story.html">✦ Our Story</a>
              <a href="the-complete-journey.html">✦ The Complete Journey</a>
              <a href="craftsmanship.html">✦ Craftsmanship &amp; Artistry</a>
              <a href="sustainability.html">✦ Sustainability &amp; Ethical Weaving</a>
              <a href="journal.html">✦ The Aleen Journal</a>
              <a href="care-guide.html">✦ Atelier Care Guide</a>
              <a href="contact-us.html">✦ Contact Us &amp; Concierge</a>
            </div>

            <div class="sitemap-col">
              <h4>Governance &amp; Portal</h4>
              <a href="privacy.html">✦ Privacy Policy</a>
              <a href="terms.html">✦ Terms &amp; Conditions</a>
              <a href="sitemap.html">✦ Sitemap Directory</a>
              <a href="admin.html">✦ Atelier Management Console</a>
            </div>
          </div>
        </div>
        """
    }
]

for p in LEGAL_PAGES:
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <title>{p['title']}</title>
{PAGE_STYLES}
</head>
<body>
{GLOBAL_HEADER_HTML}

<main id="main">
  <section class="legal-hero">
    <div>
      <span class="legal-kicker">{p['kicker']}</span>
      <h1 class="legal-title">{p['heading']}</h1>
      <p class="legal-subtitle">"{p['sub']}"</p>
    </div>
  </section>

  <div class="legal-container">
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
    print(f"✦ Generated {p['filename']}")

print("✦ All 3 legal pages generated successfully!")

