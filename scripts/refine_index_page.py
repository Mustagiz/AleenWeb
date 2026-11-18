import re

with open('Aleen website/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove the misplaced noscript tags around the secondary style block
pos_ns = text.find('<noscript>\n  <style>')
if pos_ns != -1:
    pos_ns_end = text.find('</style>\n</noscript>', pos_ns)
    if pos_ns_end != -1:
        text = text[:pos_ns] + '<style>' + text[pos_ns + len('<noscript>\n  <style>'):pos_ns_end] + '</style>' + text[pos_ns_end + len('</style>\n</noscript>'):]
        print("✓ Unwrapped noscript from style tag!")
    else:
        # fallback regex
        text = text.replace('<noscript>\n  <style>', '<style>').replace('</style>\n</noscript>', '</style>')
        print("✓ Fallback unwrapped noscript from style tag!")
else:
    text = text.replace('<noscript>', '<!-- noscript removed -->').replace('</noscript>', '<!-- /noscript removed -->')
    print("✓ Replaced noscript tags!")

# 2. Add high-priority CSS overrides in head
hero_and_layout_css = """
/* ================= HERO MULTI-MODEL SCROLL CROSSFADE & LAYOUT FIXES ================= */
#hero {
  position: relative !important;
  background: #0f1d15 !important;
  overflow: hidden !important;
}
.hero-static-bg {
  position: absolute !important;
  inset: 0 !important;
  background: #0f1d15 radial-gradient(circle at 65% 35%, rgba(20, 38, 28, 0.95) 0%, #0a140e 100%) !important;
  z-index: 1 !important;
  pointer-events: none !important;
}
#hero .img-wrap {
  position: absolute !important;
  inset: 0 !important;
  z-index: 2 !important;
}
.hero-model-layer {
  position: absolute !important;
  inset: 0 !important;
  opacity: 0 !important;
  transform: scale(1.04) !important;
  transition: opacity 0.8s cubic-bezier(0.25, 1, 0.5, 1), transform 0.8s cubic-bezier(0.25, 1, 0.5, 1) !important;
  will-change: opacity, transform !important;
  pointer-events: none !important;
}
.hero-model-layer.active {
  opacity: 1 !important;
  transform: scale(1) !important;
  pointer-events: auto !important;
}
.hero-model-layer img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  object-position: 50% 25% !important;
}

/* Picture 1 Fix: Left breathing room and padding in Hero section */
.slide-content {
  left: clamp(38px, 7vw, 110px) !important;
  padding-left: clamp(12px, 2.2vw, 36px) !important;
}

/* Picture 4 Fix: Completely remove top empty gap above New Collections For Women */
#women-new {
  margin-top: 0 !important;
  padding-top: 20px !important;
  padding-bottom: clamp(40px, 6vh, 70px) !important;
  isolation: isolate !important;
}
#women-new::before {
  display: none !important;
}
#women-new .rail {
  top: 20px !important;
}
#women-new .sec-head {
  margin-top: 0 !important;
  padding-top: 0 !important;
  margin-bottom: clamp(16px, 2.4vh, 28px) !important;
}

/* Clean section gap elimination */
#women-new, #explore, #garment-reel, #best, #storyEd {
  margin-top: 0 !important;
  margin-bottom: 0 !important;
}

/* Luxurious atmospheric background for Our Story */
#storyEd {
  background: radial-gradient(circle at 75% 30%, rgba(201, 163, 95, 0.16) 0%, transparent 60%),
              linear-gradient(175deg, rgba(8, 18, 12, 0.84) 0%, rgba(12, 25, 16, 0.94) 100%),
              url('https://mahira2.netlify.app/assets/s2-room.jpg?v=3') center/cover no-repeat fixed !important;
  position: relative !important;
}
#storyEd::before {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  background: radial-gradient(circle at 50% 50%, rgba(20, 36, 24, 0.5) 0%, rgba(8, 16, 10, 0.85) 100%) !important;
  pointer-events: none !important;
  z-index: 1 !important;
}
#storyEd > * {
  position: relative !important;
  z-index: 2 !important;
}
"""

if "HERO MULTI-MODEL SCROLL CROSSFADE" not in text:
    text = text.replace('</head>', f'<style>\n{hero_and_layout_css}\n</style>\n</head>')
    print("✓ Injected Hero & layout CSS into head!")

# 3. Update Hero HTML to include multi-model layers & New Arrivals button
old_hero_model_regex = r'<div class="slide s-women is-active" data-index="0">.*?<div class="slide-content">'
new_hero_model_html = """<div class="hero-static-bg" aria-hidden="true"></div>
    <div class="slide s-women is-active" data-index="0">
      <div class="img-wrap" id="heroModelWrap">
        <!-- Model 1 (Initial / Top of Page) -->
        <div class="hero-model-layer model-layer-1 active" data-model="1">
          <picture>
            <source media="(max-width: 700px)" srcset="https://mahira2.netlify.app/assets/women-mobile.jpg?v=3">
            <img src="https://mahira2.netlify.app/assets/women-clean.jpg?v=3" alt="Awadh champagne saree model" decoding="async">
          </picture>
        </div>
        <!-- Model 2 (Crossfade on scroll phase 1) -->
        <div class="hero-model-layer model-layer-2" data-model="2">
          <picture>
            <img src="https://mahira2.netlify.app/assets/s4-p1.jpg?v=3" alt="Royal haute couture embroidered model" decoding="async">
          </picture>
        </div>
        <!-- Model 3 (Crossfade on scroll phase 2) -->
        <div class="hero-model-layer model-layer-3" data-model="3">
          <picture>
            <img src="https://mahira2.netlify.app/assets/s5-p1.jpg?v=3" alt="Heritage Awadh artisanal attire model" decoding="async">
          </picture>
        </div>
      </div>
      <div class="veil"></div>
      <div class="slide-content">"""

text = re.sub(r'<div class="slide s-women is-active" data-index="0">\s*<div class="img-wrap">.*?</div>\s*<div class="veil"></div>\s*<div class="slide-content">',
              new_hero_model_html, text, flags=re.DOTALL)
print("✓ Updated Hero HTML with multi-model layers!")

# Update CTA row in Hero to have both Explore Collections and New Arrivals
old_cta_row = r'<div class="cta-row">\s*<a class="btn btn-primary" href="collections.html"><span class="fill"></span><span class="lbl">Explore&nbsp;Collections</span>.*?</a>\s*</div>'
new_cta_row = """<div class="cta-row" style="display: flex; gap: 16px; flex-wrap: wrap;">
          <a class="btn btn-primary" href="collections.html"><span class="fill"></span><span class="lbl">Explore&nbsp;Collections</span><span class="arrow"><svg viewBox="0 0 28 10"><path d="M0 5h24M20 1l5 4-5 4"/></svg></span></a>
          <a class="btn btn-primary" href="collections.html?filter=new" style="border: 1px solid rgba(201, 163, 95, 0.45); background: rgba(15, 29, 21, 0.6);"><span class="fill"></span><span class="lbl">New&nbsp;Arrivals</span><span class="arrow"><svg viewBox="0 0 28 10"><path d="M0 5h24M20 1l5 4-5 4"/></svg></span></a>
        </div>"""
text = re.sub(old_cta_row, new_cta_row, text, flags=re.DOTALL)
print("✓ Updated Hero CTA row with New Arrivals button!")

# 4. Inject script before </body> for scroll-based model transition & carousel loader
scroll_and_carousel_js = """
<script>
// Header Scroll Model Animation & Dynamic Carousel Loader
(function() {
  // 1. Model crossfade on scroll while keeping background rock-steady
  const modelLayers = document.querySelectorAll('.hero-model-layer');
  if (modelLayers.length > 0) {
    let currentIdx = 0;
    function handleScrollModel() {
      const scrollY = window.pageYOffset || document.documentElement.scrollTop;
      let targetIdx = 0;
      if (scrollY > 300) {
        targetIdx = 2; // Model 3
      } else if (scrollY > 90) {
        targetIdx = 1; // Model 2
      } else {
        targetIdx = 0; // Model 1
      }

      if (targetIdx !== currentIdx) {
        currentIdx = targetIdx;
        modelLayers.forEach((layer, idx) => {
          if (idx === currentIdx) {
            layer.classList.add('active');
          } else {
            layer.classList.remove('active');
          }
        });
      }
    }
    window.addEventListener('scroll', handleScrollModel, { passive: true });
    handleScrollModel();
  }

  // 2. Dynamic Curated Carousel Loader (sync with Admin customizations)
  const track = document.getElementById('grTrack');
  if (track) {
    const savedSlides = localStorage.getItem('aleen_carousel_slides');
    if (savedSlides) {
      try {
        const slides = JSON.parse(savedSlides);
        if (Array.isArray(slides) && slides.length > 0) {
          track.innerHTML = '';
          slides.forEach(slide => {
            const card = document.createElement('div');
            card.className = 'gr-card';
            card.innerHTML = `
              <div class="gr-img-wrap">
                <img src="${slide.img}" alt="${slide.title || 'Curated Garment'}" loading="lazy">
              </div>
              <div class="gr-info">
                <span class="gr-tag">${slide.tag || 'Haute Couture'}</span>
                <h3>${slide.title || 'Atelier Masterpiece'}</h3>
                <a href="${slide.link || 'collections.html'}" class="gr-cta">Examine Craft <svg viewBox="0 0 28 10"><path d="M0 5h22M18 1l5 4-5 4"/></svg></a>
              </div>
            `;
            track.appendChild(card);
          });
        }
      } catch(e) {
        console.warn('Custom slides error:', e);
      }
    }
  }
})();
</script>
"""

if "Header Scroll Model Animation & Dynamic Carousel Loader" not in text:
    text = text.replace('</body>', f'{scroll_and_carousel_js}\n</body>')
    print("✓ Injected scroll model & carousel loader script!")

with open('Aleen website/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✦ Completed index.html refinements!")

