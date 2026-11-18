import re

with open('Aleen website/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update <body> tag from is-loading to is-ready
text = text.replace('<body class="is-loading">', '<body class="is-ready">')

# 2. Add bulletproof hero visibility and stacking CSS
hero_bulletproof_css = """
/* ================= BULLETPROOF HERO VISIBILITY & STACKING ================= */
html, body {
  overflow-x: hidden !important;
  overflow-y: auto !important;
}

#hero {
  position: relative !important;
  height: 100vh !important;
  height: 100svh !important;
  background: #0f1d15 radial-gradient(circle at 65% 35%, rgba(20, 38, 28, 0.95) 0%, #0a140e 100%) !important;
  overflow: hidden !important;
  z-index: 1 !important;
}

.hero-static-bg {
  position: absolute !important;
  inset: 0 !important;
  background: #0f1d15 radial-gradient(circle at 65% 35%, rgba(20, 38, 28, 0.95) 0%, #0a140e 100%) !important;
  z-index: 0 !important;
  pointer-events: none !important;
}

.slide, .slide.is-active, .slide.s-women {
  position: absolute !important;
  inset: 0 !important;
  visibility: visible !important;
  display: block !important;
  z-index: 2 !important;
  opacity: 1 !important;
}

.slide .img-wrap, #heroModelWrap {
  position: absolute !important;
  inset: 0 !important;
  z-index: 2 !important;
  display: block !important;
  overflow: hidden !important;
}

.hero-model-layer {
  position: absolute !important;
  inset: 0 !important;
  opacity: 0 !important;
  visibility: hidden !important;
  transition: opacity 0.8s cubic-bezier(0.25, 1, 0.5, 1), transform 0.8s cubic-bezier(0.25, 1, 0.5, 1) !important;
  will-change: opacity, transform !important;
  z-index: 2 !important;
  pointer-events: none !important;
}

.hero-model-layer.active {
  opacity: 1 !important;
  visibility: visible !important;
  display: block !important;
  z-index: 3 !important;
  pointer-events: auto !important;
}

.hero-model-layer picture, .hero-model-layer img {
  position: absolute !important;
  inset: 0 !important;
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  object-position: 50% 25% !important;
  display: block !important;
}

.slide .veil {
  position: absolute !important;
  inset: 0 !important;
  z-index: 4 !important;
  background: linear-gradient(90deg, rgba(6, 14, 9, 0.72) 0%, rgba(6, 14, 9, 0.35) 45%, rgba(6, 14, 9, 0.12) 100%) !important;
  pointer-events: none !important;
  opacity: 1 !important;
}

.slide-content, .slide-content.in {
  position: absolute !important;
  top: 26.4vh !important;
  left: clamp(38px, 7vw, 110px) !important;
  padding-left: clamp(12px, 2.2vw, 36px) !important;
  max-width: clamp(480px, 46vw, 750px) !important;
  z-index: 10 !important;
  opacity: 1 !important;
  visibility: visible !important;
  display: block !important;
}

.slide-content .eyebrow,
.slide-content .headline,
.slide-content .tagline,
.slide-content .subcopy,
.slide-content .cta-row {
  opacity: 1 !important;
  visibility: visible !important;
  transform: none !important;
  display: block !important;
}

.slide-content .cta-row {
  display: flex !important;
  gap: 16px !important;
  align-items: center !important;
  flex-wrap: wrap !important;
  margin-top: clamp(20px, 3vh, 32px) !important;
}

.hero-hl-wrap {
  min-height: auto !important;
  display: block !important;
}

.headline.hl-women {
  font-family: var(--serif) !important;
  font-size: clamp(44px, 5.8vw, 88px) !important;
  color: #f7efdc !important;
  line-height: 1.08 !important;
  font-weight: 400 !important;
  text-shadow: 0 4px 20px rgba(0,0,0,0.6) !important;
}

.eyebrow .eb-text {
  font-size: clamp(10px, 0.8vw, 13px) !important;
  letter-spacing: 0.28em !important;
  text-transform: uppercase !important;
  color: var(--gold-light) !important;
  font-weight: 500 !important;
}

.tagline {
  font-family: var(--serif-i) !important;
  font-size: clamp(18px, 1.8vw, 26px) !important;
  color: rgba(247, 239, 220, 0.9) !important;
  font-style: italic !important;
  margin-top: 14px !important;
}
"""

if "BULLETPROOF HERO VISIBILITY" not in text:
    text = text.replace('</head>', f'<style>\n{hero_bulletproof_css}\n</style>\n</head>')
    print("✓ Added bulletproof hero CSS to head!")

# 3. Ensure applyFinalState is called on window load
immediate_ready_js = """
<script>
// Guarantee hero readiness immediately
(function() {
  document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('is-ready');
    document.body.classList.remove('is-loading');
    document.documentElement.style.overflow = '';
    const content = document.querySelector('.slide-content');
    if (content) content.classList.add('in');
    const firstLayer = document.querySelector('.hero-model-layer');
    if (firstLayer) firstLayer.classList.add('active');
  });
  window.addEventListener('load', function() {
    document.body.classList.add('is-ready');
    document.body.classList.remove('is-loading');
    document.documentElement.style.overflow = '';
  });
})();
</script>
"""

if "Guarantee hero readiness immediately" not in text:
    text = text.replace('</body>', f'{immediate_ready_js}\n</body>')
    print("✓ Added immediate hero readiness script!")

with open('Aleen website/index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("✦ Updated index.html successfully!")

