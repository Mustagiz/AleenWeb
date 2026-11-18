import os
import json
import re

# 1. Load static SVG from mahira.html
with open('Aleen-react2/public/mahira.html', 'r', encoding='utf-8') as f:
    mahira = f.read()

m = re.search(r'window\.ALEEN_LOGO\s*=\s*(\{.*?\});', mahira, re.DOTALL)
if not m:
    raise Exception("ALEEN_LOGO not found in mahira.html")
D = json.loads(m.group(1))

EC = D['center']
ornaments = D['orn']['ne'] + D['orn']['nw'] + D['orn']['se'] + D['orn']['sw']

svg_parts = []
svg_parts.append('<svg id="brandLogo" viewBox="0 0 1600 1351" role="img" aria-label="Aleen Clothing">')
svg_parts.append('''<defs>
  <linearGradient id="lgGold" gradientUnits="userSpaceOnUse" x1="436.7" y1="105.6" x2="1165.3" y2="834.2">
    <stop offset="0%" stop-color="#8a6420"/>
    <stop offset="32%" stop-color="#c9a35f"/>
    <stop offset="50%" stop-color="#f0d48c"/>
    <stop offset="68%" stop-color="#c9a35f"/>
    <stop offset="100%" stop-color="#7c5a1d"/>
  </linearGradient>
  <linearGradient id="lgWmGold" gradientUnits="userSpaceOnUse" x1="0" y1="1000" x2="1600" y2="1180">
    <stop offset="0%" stop-color="#9a7226"/>
    <stop offset="30%" stop-color="#d9b269"/>
    <stop offset="50%" stop-color="#f2d896"/>
    <stop offset="70%" stop-color="#d9b269"/>
    <stop offset="100%" stop-color="#9a7226"/>
  </linearGradient>
  <linearGradient id="lgSelGold" gradientUnits="userSpaceOnUse" x1="280" y1="0" x2="1320" y2="0">
    <stop offset="0%" stop-color="#8a6420"/>
    <stop offset="45%" stop-color="#e7c87f"/>
    <stop offset="60%" stop-color="#f0d48c"/>
    <stop offset="100%" stop-color="#8a6420"/>
  </linearGradient>
</defs>''')

svg_parts.append('<g id="lgAll">')
svg_parts.append('<g id="lgEmblem">')
svg_parts.append(f'<circle id="lgRing" cx="{EC["x"]}" cy="{EC["y"]}" r="{D["ring"]["r"]}" fill="none" stroke="url(#lgGold)" stroke-width="{D["ring"]["w"] + 1}"/>')
svg_parts.append(f'<path id="lgMFill" d="{D["m"]["d"]}" fill="url(#lgGold)" fill-rule="evenodd"/>')

svg_parts.append('<g id="lgDia">')
for k in ['n', 's', 'e', 'w']:
    if k in D['diamonds']:
        svg_parts.append(f'<path d="{D["diamonds"][k]["d"]}" fill="url(#lgGold)" fill-rule="evenodd" class="lg-dia lg-dia-{k}"/>')
svg_parts.append('</g>')

svg_parts.append('<g id="lgOrn">')
for o in ornaments:
    svg_parts.append(f'<path d="{o["d"]}" fill="url(#lgGold)" fill-rule="evenodd" class="lg-orn"/>')
svg_parts.append('</g>')
svg_parts.append('</g>')

svg_parts.append('<g id="lgMah">')
for l in D['mahira']:
    svg_parts.append(f'<path d="{l["d"]}" fill="url(#lgWmGold)" fill-rule="evenodd" class="lg-mah"/>')
svg_parts.append('</g>')

svg_parts.append('''<g id="lgSel">
  <text x="801" y="1318" text-anchor="middle" fill="url(#lgSelGold)" class="lg-sel" style="font-family: 'Great Vibes', cursive, 'Playfair Display', serif; font-size: 155px; font-weight: 400; letter-spacing: 2px;">Consciously Curated</text>
  <rect x="40" y="1300" width="220" height="4" fill="url(#lgSelGold)" class="lg-line lg-line-0"/>
  <rect x="1340" y="1300" width="220" height="4" fill="url(#lgSelGold)" class="lg-line lg-line-1"/>
</g>''')

svg_parts.append('</g></svg>')

STATIC_BRAND_LOGO_SVG = ''.join(svg_parts)

HEADER_HTML = f"""
<!-- ======================= HEADER ======================= -->
<header id="header" class="is-solid">
  <button id="menuBtn" class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="mobileNav">
    <span></span><span></span>
  </button>

  <div class="nav-center">
    <nav class="nav-side nav-l" aria-label="Primary">
      <a href="mahira.html#top">Home</a>
      <a aria-expanded="false" aria-haspopup="true" data-mega="women" href="mahira.html#women-new">Women</a>
      <a aria-expanded="false" aria-haspopup="true" data-mega="kalakaari" href="mahira.html#kalakaari">Kalakaari</a>
    </nav>
    <span class="logo-space" aria-hidden="true"></span>
    <nav class="nav-side nav-r" aria-label="Collections">
      <a href="mahira.html#women-new">New Arrivals</a>
      <a href="mahira.html#best">Best Sellers</a>
      <a href="mahira.html#storyEd">Our Story</a>
    </nav>
  </div>

  <div class="brand-slot">
    <a class="brand" id="brand" href="mahira.html#top" aria-label="Aleen Clothing — home">
      {STATIC_BRAND_LOGO_SVG}
    </a>
  </div>

  <div class="nav-utils" style="display: none !important;"></div>

  <!-- mega menus -->
  <div class="mega" id="mega" aria-hidden="true">
    <div class="mega-sheet"></div>
    <div class="mega-inner"></div>
  </div>
</header>

<!-- ======================= MOBILE NAVIGATION ======================= -->
<div id="mobileNav" aria-hidden="true">
  <div class="mn-top">
    <button class="mn-back" id="mnBack" aria-label="Close menu">
      <svg viewBox="0 0 20 14" width="20" height="14" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 7H2M8 1 1.5 7 8 13"/></svg>
    </button>
    <p class="mn-title">Aleen Menu</p>
  </div>
  <div class="mn-body">
    <ul class="mn-list">
      <li><a href="mahira.html#top">Home</a></li>
      <li class="mn-group-title">Women's Ethnic</li>
      <li><a href="sarees.html" class="mn-sub">Sarees</a></li>
      <li><a href="kurta-sets.html" class="mn-sub">Kurta Sets</a></li>
      <li><a href="anarkali.html" class="mn-sub">Anarkali</a></li>
      <li><a href="suits.html" class="mn-sub">Suits</a></li>
      <li><a href="coord-sets.html" class="mn-sub">Co-ord Sets</a></li>
      <li><a href="lehengas.html" class="mn-sub">Lehengas</a></li>
      <li><a href="dresses.html" class="mn-sub">Dresses &amp; Sets</a></li>
      <li class="mn-group-title">Treasury</li>
      <li><a href="mahira.html#kalakaari">Kalakaari</a></li>
      <li><a href="collections.html">Collections Gallery</a></li>
      <li><a href="mahira.html#best">Best Sellers</a></li>
      <li><a href="mahira.html#storyEd">Our Story</a></li>
      <li><a href="/login" class="mn-atelier-login">✦ Atelier Manager Login</a></li>
    </ul>
  </div>
</div>
"""

HEADER_CSS = """
/* ============================================================
   CONSTANT HEADER STYLES — identical across all Aleen pages
   ============================================================ */
:root {
  --hdr-h: clamp(104px, 12vh, 132px);
  --hdr-h-solid: clamp(76px, 8.4vh, 92px);
  --logo-h: clamp(88px, 9.8vh, 112px);
  --logo-h-solid: clamp(58px, 6.2vh, 70px);
  --hdr-x: clamp(22px, 3.2vw, 64px);
  --nav-gap: clamp(26px, 2.8vw, 54px);
  --util-gap: clamp(10px, 1.15vw, 20px);
}

#header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  display: flex; align-items: center; justify-content: space-between;
  column-gap: clamp(16px, 2vw, 40px);
  height: var(--hdr-h-solid);
  padding: 0 var(--hdr-x);
  transition: height 0.5s var(--ease), background 0.5s var(--ease), box-shadow 0.5s var(--ease);
  background: rgba(11, 21, 14, 0.95);
  backdrop-filter: blur(16px) saturate(1.05);
  -webkit-backdrop-filter: blur(16px) saturate(1.05);
  box-shadow: 0 1px 0 rgba(201, 163, 95, 0.2);
}

.brand-slot {
  position: absolute; left: 50%; top: 50%;
  transform: translate(-50%, -50%);
  z-index: 2; line-height: 0;
  pointer-events: none;
}
.brand-slot .brand { pointer-events: auto; }
.nav-side { display: flex; align-items: center; gap: clamp(13px, 1.4vw, 28px); }
.nav-center { display: contents; }
.logo-space { display: none; }
#header { --logo-half: calc(var(--logo-h-solid) * 0.5925); }
.nav-l, .nav-r {
  position: absolute; top: 50%;
  transform: translateY(-50%);
  z-index: 1;
}
.nav-l { right: calc(50% + var(--logo-half) + var(--nav-gap)); }
.nav-r { left:  calc(50% + var(--logo-half) + var(--nav-gap)); }
.nav-utils { display: none !important; }

.brand { display: block; line-height: 0; }
#brandLogo {
  display: block;
  height: var(--logo-h-solid); width: auto;
}

.nav-side a {
  position: relative;
  display: block;
  padding: 10px 0;
  font-size: clamp(10px, 0.76vw, 13px);
  font-weight: 500;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(240, 232, 210, 0.96);
  white-space: nowrap;
  text-decoration: none;
  transition: color 0.3s ease;
}
.nav-side a::after {
  content: ""; position: absolute; left: 0; right: 0; bottom: 2px;
  height: 1px; background: var(--gold);
  transform: scaleX(0); transform-origin: left center;
  transition: transform 0.3s ease;
}
.nav-side a:hover, .nav-side a.is-open { color: var(--gold-light); }
.nav-side a:hover::after, .nav-side a.is-open::after { transform: scaleX(1); }

/* Mega Dropdown */
.mega {
  position: absolute; left: 0; right: 0; top: 100%;
  visibility: hidden; z-index: 99;
}
.mega.is-open { visibility: visible; }
.mega-sheet {
  position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(15, 27, 18, 0.985) 0%, rgba(11, 21, 14, 0.99) 100%);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-top: 1px solid rgba(201, 163, 95, 0.22);
  box-shadow: 0 30px 70px rgba(4, 10, 6, 0.5);
}
.mega-inner {
  position: relative;
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr)) clamp(210px, 17vw, 290px);
  gap: clamp(20px, 2.6vw, 54px);
  width: min(94vw, 1560px);
  margin: 0 auto;
  padding: clamp(30px, 3.4vh, 48px) 0 clamp(34px, 3.8vh, 54px);
}
.mega-inner.is-women {
  display: grid !important;
  grid-template-columns: minmax(260px, 340px) 1fr !important;
  gap: clamp(36px, 4.5vw, 80px) !important;
  align-items: center !important;
  width: min(94vw, 1500px) !important;
  padding: 36px 0 42px !important;
}
.mg-col { min-width: 0; }
.mg-col h4 {
  font-size: 11px; letter-spacing: 0.32em; text-transform: uppercase;
  font-weight: 600; color: #b89a62; margin-bottom: 12px;
}
.mg-col > i {
  display: block; width: 26px; height: 1px; background: rgba(201, 163, 95, 0.6);
  margin-bottom: 16px;
}
.mg-col a {
  position: relative; display: block; padding: 7px 0;
  font-size: 14.5px; letter-spacing: 0.035em;
  color: rgba(238, 230, 208, 0.96); text-decoration: none;
  transition: color 0.28s ease, transform 0.28s ease;
  width: fit-content;
}
.mg-col a:hover { color: var(--gold-light); transform: translateX(3px); }
.mg-promo {
  position: relative; overflow: hidden; border-radius: 12px;
  border: 1px solid rgba(184, 154, 98, 0.75);
  box-shadow: 0 16px 40px rgba(0,0,0,0.5);
  min-height: 280px; height: 290px;
  display: block; text-decoration: none;
}
.mg-promo img {
  position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
  object-position: center 30%; transition: transform 0.8s ease;
}
.mg-promo:hover img { transform: scale(1.04); }
.mg-promo span {
  position: absolute; inset: 0; z-index: 1;
  background: linear-gradient(180deg, rgba(8, 14, 9, 0.1) 30%, rgba(8, 14, 9, 0.88) 100%);
}
.mg-promo b {
  position: absolute; left: 6%; bottom: 24%; z-index: 2;
  font-family: var(--serif); font-size: clamp(20px, 1.8vw, 28px);
  color: var(--cream-hi); letter-spacing: 0.08em; text-transform: uppercase;
}
.mg-promo em {
  position: absolute; left: 6%; bottom: 12%; z-index: 2;
  font-family: var(--serif-i); font-style: italic; font-size: 15px;
  color: rgba(233, 224, 200, 0.96);
}

/* Mobile Nav Drawer */
.menu-btn {
  display: none; width: 44px; height: 44px;
  position: relative; z-index: 130; background: none; border: none; cursor: pointer;
}
.menu-btn span {
  position: absolute; left: 11px; width: 22px; height: 1.5px;
  background: var(--cream); transition: transform 0.3s, top 0.3s;
}
.menu-btn span:nth-child(1) { top: 18px; }
.menu-btn span:nth-child(2) { top: 26px; }
.menu-btn.is-active span:nth-child(1) { transform: rotate(45deg); top: 22px; }
.menu-btn.is-active span:nth-child(2) { transform: rotate(-45deg); top: 22px; }

#mobileNav {
  position: fixed; inset: 0; z-index: 95;
  background: rgba(4, 9, 6, 0.98);
  backdrop-filter: blur(20px);
  transform: translateX(-100%);
  transition: transform 0.4s var(--ease);
  display: flex; flex-direction: column;
}
#mobileNav.is-open { transform: translateX(0); }
.mn-top {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px 24px; border-bottom: 1px solid rgba(201, 163, 95, 0.2);
}
.mn-back {
  background: none; border: none; color: var(--gold); cursor: pointer; display: flex; align-items: center;
}
.mn-title { font-family: var(--serif); font-size: 16px; color: var(--gold-light); letter-spacing: 2px; }
.mn-body { flex: 1; overflow-y: auto; padding: 24px; }
.mn-list { list-style: none; margin: 0; padding: 0; }
.mn-list li { margin-bottom: 14px; }
.mn-list a {
  color: var(--cream); text-decoration: none; font-size: 16px; font-weight: 500;
  display: block; transition: color 0.2s;
}
.mn-list a:hover { color: var(--gold); }
.mn-group-title {
  color: var(--gold); font-size: 11px; letter-spacing: 2px; text-transform: uppercase;
  margin-top: 20px; margin-bottom: 8px; font-weight: 700;
}
.mn-sub { padding-left: 16px; font-size: 14px !important; color: rgba(255, 255, 255, 0.8) !important; }
.mn-atelier-login {
  color: var(--gold-spark) !important; font-weight: 700 !important;
  margin-top: 24px; padding: 12px 18px; border: 1px solid var(--gold); border-radius: 999px; text-align: center;
}

@media (max-width: 900px) {
  .menu-btn { display: block !important; }
  .nav-side { display: none !important; }
  .brand-slot { left: 50%; transform: translate(-50%, -50%); }
}

/* Badge Suppression Rule: Never display BESTSELLER or pill badges on any garment card */
.card-badge, .bestseller-badge {
  display: none !important;
  visibility: hidden !important;
  opacity: 0 !important;
}

/* Footer Atelier Manager Portal */
.f-atelier-portal-bar {
  text-align: center;
  padding: 24px 0 16px;
  border-top: 1px solid rgba(201, 163, 95, 0.2);
  margin-top: 32px;
}
.f-atelier-portal-link {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  color: #FFFFFF !important;
  background: rgba(20, 37, 27, 0.6);
  border: 1px solid rgba(201, 163, 95, 0.45);
  border-radius: 999px;
  padding: 10px 26px;
  font-size: 12px;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  text-decoration: none;
  transition: all 0.3s ease;
}
.f-atelier-portal-link:hover {
  background: var(--gold) !important;
  border-color: var(--gold-light) !important;
  box-shadow: 0 4px 20px rgba(201, 163, 95, 0.4) !important;
  transform: translateY(-2px);
}
.f-atelier-portal-link:hover span {
  color: #241A0C !important;
}
"""

HEADER_SCRIPT = """
<script>
(function() {
  const NAV_DATA = {
    women: {
      label: 'Women',
      href: 'mahira.html#women-new',
      promo: {
        img: 'https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2',
        title: 'The Women’s Edit',
        line: 'Elegance in every drape.'
      },
      groups: [
        {
          title: 'Ethnic',
          items: [
            { name: 'Sarees', url: 'sarees.html' },
            { name: 'Kurta Sets', url: 'kurta-sets.html' },
            { name: 'Anarkali', url: 'anarkali.html' },
            { name: 'Suits', url: 'suits.html' },
            { name: 'Co-ord Sets', url: 'coord-sets.html' },
            { name: 'Lehengas', url: 'lehengas.html' },
            { name: 'Dresses', url: 'dresses.html' }
          ]
        }
      ]
    },
    kalakaari: {
      label: 'Kalakaari',
      href: 'mahira.html#kalakaari',
      promo: {
        img: 'https://mahira2.netlify.app/assets/s2-card-kala.jpg?v=2',
        title: 'Kalakaari',
        line: 'Art that tells a story.'
      },
      groups: [
        {
          title: 'Sarees',
          items: [
            { name: 'Kalamkari Sarees', url: 'sarees.html' },
            { name: 'Printed Sarees', url: 'sarees.html' },
            { name: 'Handcrafted Sarees', url: 'sarees.html' }
          ]
        },
        {
          title: 'Dress Sets',
          items: [
            { name: 'Kalamkari Dress Sets', url: 'dresses.html' },
            { name: 'Kurta Sets', url: 'kurta-sets.html' },
            { name: 'Anarkali Sets', url: 'anarkali.html' }
          ]
        },
        {
          title: 'Fabric',
          items: [
            { name: 'Kalamkari Fabric', url: 'collections.html?category=unstitched' },
            { name: 'Printed Fabric', url: 'collections.html?category=unstitched' },
            { name: 'Handcrafted Fabric', url: 'collections.html?category=unstitched' }
          ]
        },
        {
          title: 'Dupattas',
          items: [
            { name: 'Kalamkari Dupattas', url: 'collections.html?category=dupattas' },
            { name: 'Printed Dupattas', url: 'collections.html?category=dupattas' },
            { name: 'Handcrafted Dupattas', url: 'collections.html?category=dupattas' }
          ]
        }
      ]
    }
  };

  const header = document.getElementById('header');
  const mega = document.getElementById('mega');
  const megaInner = mega ? mega.querySelector('.mega-inner') : null;
  const menuBtn = document.getElementById('menuBtn');
  const mobileNav = document.getElementById('mobileNav');
  const mnBack = document.getElementById('mnBack');
  let megaTimer = null;

  function renderMega(key) {
    if (!megaInner || !NAV_DATA[key]) return;
    const c = NAV_DATA[key];
    megaInner.innerHTML = '';
    megaInner.classList.toggle('is-women', key === 'women');

    c.groups.forEach(g => {
      const col = document.createElement('div');
      col.className = 'mg-col';
      const h4 = document.createElement('h4');
      h4.textContent = g.title;
      col.appendChild(h4);
      col.appendChild(document.createElement('i'));
      g.items.forEach(it => {
        const a = document.createElement('a');
        a.textContent = it.name;
        a.href = it.url;
        col.appendChild(a);
      });
      megaInner.appendChild(col);
    });

    const promo = document.createElement('a');
    promo.className = 'mg-promo';
    promo.href = c.href;
    promo.innerHTML = `<img src="${c.promo.img}" alt="" loading="lazy"><span></span><b>${c.promo.title}</b><em>${c.promo.line}</em>`;
    megaInner.appendChild(promo);
  }

  function openMega(key) {
    clearTimeout(megaTimer);
    if (!mega) return;
    renderMega(key);
    mega.classList.add('is-open');
    mega.setAttribute('aria-hidden', 'false');
    document.querySelectorAll('.nav-side a[data-mega]').forEach(a => {
      const on = a.getAttribute('data-mega') === key;
      a.classList.toggle('is-open', on);
    });
  }

  function closeMega() {
    if (!mega) return;
    mega.classList.remove('is-open');
    mega.setAttribute('aria-hidden', 'true');
    document.querySelectorAll('.nav-side a[data-mega]').forEach(a => {
      a.classList.remove('is-open');
    });
  }

  document.querySelectorAll('.nav-side a[data-mega]').forEach(a => {
    const key = a.getAttribute('data-mega');
    a.addEventListener('mouseenter', () => openMega(key));
    a.addEventListener('focus', () => openMega(key));
  });

  document.querySelectorAll('.nav-side a:not([data-mega])').forEach(a => {
    a.addEventListener('mouseenter', () => {
      megaTimer = setTimeout(closeMega, 80);
    });
  });

  if (header) {
    header.addEventListener('mouseleave', () => {
      megaTimer = setTimeout(closeMega, 150);
    });
  }
  if (mega) {
    mega.addEventListener('mouseenter', () => clearTimeout(megaTimer));
    mega.addEventListener('mouseleave', () => {
      megaTimer = setTimeout(closeMega, 150);
    });
  }

  // Mobile menu toggle
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener('click', () => {
      const open = mobileNav.classList.toggle('is-open');
      menuBtn.classList.toggle('is-active', open);
      document.body.style.overflow = open ? 'hidden' : '';
    });
  }
  if (mnBack && mobileNav) {
    mnBack.addEventListener('click', () => {
      mobileNav.classList.remove('is-open');
      if (menuBtn) menuBtn.classList.remove('is-active');
      document.body.style.overflow = '';
    });
  }
})();
</script>
"""

# Export definitions to file
with open('scripts/shared_header.py', 'w', encoding='utf-8') as f:
    f.write(f'''
HEADER_HTML = """{HEADER_HTML}"""
HEADER_CSS = """{HEADER_CSS}"""
HEADER_SCRIPT = """{HEADER_SCRIPT}"""
''')

print("shared_header.py generated successfully!")
