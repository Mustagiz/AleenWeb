import os, re

# 1. Update scripts/shared_components.py
sc_path = os.path.join(os.path.dirname(__file__), "shared_components.py")
with open(sc_path, "r", encoding="utf-8") as f:
    sc_text = f.read()

new_mega_css = """/* Mega Menus — Atelier Luxury Deep Emerald Glass */
.mega {
  position: fixed !important;
  top: clamp(76px, 8.4vh, 92px) !important;
  left: 0 !important;
  right: 0 !important;
  z-index: 9999 !important;
  display: block !important;
  opacity: 0 !important;
  visibility: hidden !important;
  transform: translateY(-8px) !important;
  transition: opacity 0.3s cubic-bezier(0.22, 0.61, 0.21, 1), transform 0.3s cubic-bezier(0.22, 0.61, 0.21, 1), visibility 0.3s !important;
  pointer-events: none !important;
}
.mega.is-open {
  opacity: 1 !important;
  visibility: visible !important;
  transform: translateY(0) !important;
  pointer-events: auto !important;
}
.mega-sheet {
  position: absolute !important;
  inset: 0 !important;
  background: rgba(8, 17, 12, 0.97) !important;
  backdrop-filter: blur(28px) !important;
  -webkit-backdrop-filter: blur(28px) !important;
  border-top: 1px solid rgba(201, 163, 95, 0.25) !important;
  border-bottom: 1px solid rgba(201, 163, 95, 0.35) !important;
  box-shadow: 0 35px 80px rgba(0, 0, 0, 0.85), 0 0 50px rgba(201, 163, 95, 0.08) !important;
}
.mega-inner {
  position: relative !important;
  z-index: 2 !important;
  max-width: 1360px !important;
  margin: 0 auto !important;
  padding: clamp(28px, 3.6vh, 44px) clamp(24px, 3.2vw, 48px) !important;
  display: block !important;
}
.mega-layout {
  display: grid !important;
  grid-template-columns: 3.1fr 2.4fr !important;
  gap: clamp(32px, 3.5vw, 56px) !important;
  align-items: start !important;
}
.mega-grid {
  display: grid !important;
  grid-template-columns: repeat(3, 1fr) !important;
  gap: clamp(24px, 2.5vw, 36px) !important;
}
.mega-group h4 {
  font-family: var(--sans) !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  letter-spacing: 0.24em !important;
  text-transform: uppercase !important;
  color: var(--gold-light) !important;
  margin: 0 0 6px 0 !important;
}
.mega-group-line {
  display: block !important;
  width: 28px !important;
  height: 1px !important;
  background: linear-gradient(90deg, var(--gold) 0%, transparent 100%) !important;
  margin-bottom: 14px !important;
}
.mega-group a {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  font-family: var(--sans) !important;
  font-size: 13.5px !important;
  color: rgba(245, 237, 216, 0.82) !important;
  text-decoration: none !important;
  padding: 6.5px 0 !important;
  transition: all 0.22s ease !important;
}
.mega-group a .mega-arr {
  width: 11px !important;
  height: 11px !important;
  stroke: var(--gold) !important;
  fill: none !important;
  stroke-width: 2 !important;
  opacity: 0 !important;
  transform: translateX(-4px) !important;
  transition: all 0.22s ease !important;
}
.mega-group a:hover {
  color: #ffffff !important;
  transform: translateX(4px) !important;
}
.mega-group a:hover .mega-arr {
  opacity: 1 !important;
  transform: translateX(0) !important;
}

/* Two Featured Promo Cards Side-by-Side */
.mega-promos-grid {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 18px !important;
}
.mega-promo-card {
  display: flex !important;
  flex-direction: column !important;
  text-decoration: none !important;
  border-radius: 8px !important;
  overflow: hidden !important;
  border: 1px solid rgba(201, 163, 95, 0.28) !important;
  background: rgba(15, 29, 21, 0.6) !important;
  transition: all 0.35s ease !important;
}
.mega-promo-card:hover {
  transform: translateY(-4px) !important;
  border-color: rgba(201, 163, 95, 0.6) !important;
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6), 0 0 20px rgba(201, 163, 95, 0.15) !important;
}
.mega-promo-img-wrap {
  position: relative !important;
  width: 100% !important;
  aspect-ratio: 4/3 !important;
  overflow: hidden !important;
}
.mega-promo-img-wrap img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  transition: transform 0.6s ease !important;
}
.mega-promo-card:hover .mega-promo-img-wrap img {
  transform: scale(1.06) !important;
}
.mega-promo-badge {
  position: absolute !important;
  top: 12px !important;
  left: 12px !important;
  background: rgba(10, 20, 14, 0.85) !important;
  backdrop-filter: blur(8px) !important;
  border: 1px solid rgba(201, 163, 95, 0.45) !important;
  color: var(--gold-light) !important;
  font-size: 9.5px !important;
  letter-spacing: 0.18em !important;
  text-transform: uppercase !important;
  padding: 4px 10px !important;
  border-radius: 2px !important;
}
.mega-promo-copy {
  padding: 14px 16px 16px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 4px !important;
}
.mega-promo-copy h5 {
  font-family: var(--serif) !important;
  font-size: 17px !important;
  color: #f7efdc !important;
  margin: 0 !important;
  font-weight: 500 !important;
}
.mega-promo-copy p {
  font-size: 12px !important;
  color: var(--gold-light) !important;
  margin: 0 !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 6px !important;
  transition: gap 0.22s ease !important;
}
.mega-promo-copy p svg {
  width: 16px !important;
  height: 8px !important;
  fill: none !important;
  stroke: currentColor !important;
  stroke-width: 1.5 !important;
  transition: transform 0.22s ease !important;
}
.mega-promo-card:hover .mega-promo-copy p {
  color: var(--gold-spark) !important;
  gap: 10px !important;
}
.mega-promo-card:hover .mega-promo-copy p svg {
  transform: translateX(4px) !important;
}
"""

# Replace old mega css in shared_components.py
pos1 = sc_text.find("/* Mega Menus */")
pos2 = sc_text.find("/* Mobile Nav Drawer", pos1)
if pos1 != -1 and pos2 != -1:
    sc_text = sc_text[:pos1] + new_mega_css + "\n\n" + sc_text[pos2:]
    print("✓ Replaced Mega CSS in shared_components.py")

# Replace NAV_DATA and buildMegaMenu in shared_components.py
new_nav_and_builder = """  const NAV_DATA = {
    women: {
      label: 'Women',
      promos: [
        {
          img: 'https://mahira2.netlify.app/assets/s2-card-women.jpg?v=2',
          badge: 'CURATED DRAPES',
          title: 'The Women’s Edit',
          line: 'Elegance in every drape',
          url: 'collections.html'
        },
        {
          img: 'https://mahira2.netlify.app/assets/s4-p1.jpg?v=3',
          badge: 'NEW SEASON',
          title: 'Royal Awadh Couture',
          line: 'Centuries of artistry',
          url: 'collections.html?filter=new'
        }
      ],
      groups: [
        {
          title: 'Ethnic Haute Couture',
          items: [
            { name: 'Sarees', url: 'sarees.html' },
            { name: 'Kurta Sets', url: 'kurta-sets.html' },
            { name: 'Anarkali Sets', url: 'anarkali.html' },
            { name: 'Royal Suits', url: 'suits.html' },
            { name: 'Co-ord Sets', url: 'coord-sets.html' },
            { name: 'Heritage Lehengas', url: 'lehengas.html' },
            { name: 'Dresses & Gowns', url: 'dresses.html' }
          ]
        },
        {
          title: 'Curated Heritage',
          items: [
            { name: 'Banarasi Brocades', url: 'sarees.html' },
            { name: 'Zardozi Masterpieces', url: 'craftsmanship.html' },
            { name: 'Pure Handloom Silks', url: 'collections.html' },
            { name: 'Awadh Needlecraft', url: 'collections.html' },
            { name: 'Artisanal Dupattas', url: 'collections.html' }
          ]
        },
        {
          title: 'The Atelier',
          items: [
            { name: 'All Collections Catalog', url: 'collections.html' },
            { name: 'New Arrivals 2026', url: 'collections.html?filter=new' },
            { name: 'Craftsmanship Story', url: 'craftsmanship.html' },
            { name: 'Our Sustainability', url: 'sustainability.html' },
            { name: 'Staff Atelier Portal', url: 'admin.html' }
          ]
        }
      ]
    }
  };

  const header = document.getElementById('header');
  const mega = document.getElementById('mega');
  const megaInner = mega ? mega.querySelector('.mega-inner') : null;

  // Header scroll transition: Transparent over hero, luxury glass blur when scrolled
  function updateHeaderTransparency() {
    if (!header) return;
    if (window.scrollY > 40) {
      header.classList.add('is-solid');
    } else {
      header.classList.remove('is-solid');
    }
  }
  window.addEventListener('scroll', updateHeaderTransparency, { passive: true });
  updateHeaderTransparency();

  // Robust Mega Menu Hover
  if (header && mega && megaInner) {
    const womenTrigger = header.querySelector('a[data-mega="women"]');

    function buildMegaMenu(key) {
      const data = NAV_DATA[key];
      if (!data) return;

      let groupsHtml = '<div class="mega-grid">';
      data.groups.forEach(g => {
        groupsHtml += `<div class="mega-group">
          <h4>${g.title}</h4>
          <span class="mega-group-line"></span>`;
        g.items.forEach(it => {
          groupsHtml += `<a href="${it.url}"><span>${it.name}</span><svg class="mega-arr" viewBox="0 0 16 16"><path d="M6 3l5 5-5 5"/></svg></a>`;
        });
        groupsHtml += '</div>';
      });
      groupsHtml += '</div>';

      let promosHtml = '<div class="mega-promos-grid">';
      data.promos.forEach(p => {
        promosHtml += `
          <a href="${p.url}" class="mega-promo-card">
            <div class="mega-promo-img-wrap">
              <img src="${p.img}" alt="${p.title}" loading="lazy">
              <span class="mega-promo-badge">${p.badge}</span>
            </div>
            <div class="mega-promo-copy">
              <h5>${p.title}</h5>
              <p>${p.line} <svg viewBox="0 0 24 10"><path d="M0 5h20M16 1l4 4-4 4"/></svg></p>
            </div>
          </a>
        `;
      });
      promosHtml += '</div>';

      megaInner.innerHTML = `<div class="mega-layout">${groupsHtml}${promosHtml}</div>`;
    }

    if (womenTrigger) {
      womenTrigger.addEventListener('mouseenter', () => {
        buildMegaMenu('women');
        mega.classList.add('is-open');
        mega.setAttribute('aria-hidden', 'false');
      });
    }

    header.addEventListener('mouseleave', (e) => {
      if (!e.relatedTarget || !mega.contains(e.relatedTarget)) {
        mega.classList.remove('is-open');
        mega.setAttribute('aria-hidden', 'true');
      }
    });

    mega.addEventListener('mouseleave', () => {
      mega.classList.remove('is-open');
      mega.setAttribute('aria-hidden', 'true');
    });
  }
"""

pos_nd = sc_text.find("  const NAV_DATA = {")
pos_nd_end = sc_text.find("  // Newsletter", pos_nd)
if pos_nd != -1 and pos_nd_end != -1:
    sc_text = sc_text[:pos_nd] + new_nav_and_builder + "\n" + sc_text[pos_nd_end:]
    print("✓ Replaced NAV_DATA and buildMegaMenu in shared_components.py")

with open(sc_path, "w", encoding="utf-8") as f:
    f.write(sc_text)

print("✦ Saved updated shared_components.py!")

