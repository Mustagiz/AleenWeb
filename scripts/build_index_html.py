import re
import os

with open('Aleen-react2/public/mahira.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update title and meta
html = html.replace('<title>Aleen Clothing — Tradition Meets Tomorrow</title>', '<title>Aleen Clothing — Consciously Curated</title>')
html = html.replace('<title>Mahira Select — Tradition Meets Tomorrow</title>', '<title>Aleen Clothing — Consciously Curated</title>')

# 2. Fix dead space in Kalakaari (Picture 1)
# Remove .x-bridge
html = re.sub(r'<div class="x-bridge" aria-hidden="true"></div>', '', html)
dead_space_css = """
/* Remove green dead space above Kalakaari */
.x-bridge { display: none !important; height: 0 !important; margin: 0 !important; }
#kalakaari { padding-top: 0 !important; margin-top: 0 !important; }
#kalakaari .k-stage::before { display: none !important; }
.k-head { top: 2.2% !important; }
@media (max-width: 767px) {
  .k-stage { padding-top: 4vh !important; }
}

/* Social Lock Button */
.f-lock-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1px solid rgba(201, 163, 95, 0.45);
  background: rgba(20, 37, 27, 0.5);
  color: #ffffff;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}
.f-lock-btn:hover {
  background: var(--gold);
  color: #241A0C;
  border-color: var(--gold-light);
  box-shadow: 0 0 16px rgba(201, 163, 95, 0.45);
  transform: translateY(-2px);
}

/* Atelier Lock Login Modal */
.atelier-lock-modal {
  position: fixed;
  inset: 0;
  z-index: 10000;
  background: rgba(4, 9, 6, 0.88);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}
.atelier-lock-modal.is-open {
  opacity: 1;
  pointer-events: auto;
}
.lock-dialog {
  background: linear-gradient(135deg, #112318 0%, #07100a 100%);
  border: 1px solid rgba(201, 163, 95, 0.5);
  box-shadow: 0 24px 60px rgba(0,0,0,0.8), 0 0 30px rgba(201, 163, 95, 0.2);
  border-radius: 20px;
  max-width: 440px;
  width: 100%;
  padding: 36px 32px 32px;
  text-align: center;
  position: relative;
  transform: scale(0.95);
  transition: transform 0.3s ease;
}
.atelier-lock-modal.is-open .lock-dialog {
  transform: scale(1);
}
.lock-icon-crest {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  border-radius: 50%;
  background: rgba(201, 163, 95, 0.15);
  border: 1px solid var(--gold);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--gold-light);
}
.lock-dialog h3 {
  font-family: var(--serif);
  font-size: 24px;
  font-weight: 500;
  color: var(--cream-hi);
  margin-bottom: 8px;
  letter-spacing: 1px;
}
.lock-dialog p {
  font-size: 13px;
  color: var(--cream);
  opacity: 0.8;
  line-height: 1.5;
  margin-bottom: 24px;
}
.lock-form input {
  width: 100%;
  padding: 12px 18px;
  background: rgba(4, 9, 6, 0.8);
  border: 1px solid rgba(201, 163, 95, 0.4);
  border-radius: 999px;
  color: #ffffff;
  font-size: 14px;
  letter-spacing: 2px;
  text-align: center;
  outline: none;
  margin-bottom: 16px;
  transition: all 0.25s ease;
}
.lock-form input:focus {
  border-color: var(--gold);
  box-shadow: 0 0 14px rgba(201, 163, 95, 0.3);
}
.lock-submit-btn {
  width: 100%;
  padding: 12px 24px;
  background: var(--gold);
  color: #241A0C;
  border: 1px solid var(--gold-light);
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s ease;
}
.lock-submit-btn:hover {
  background: var(--gold-spark);
  box-shadow: 0 4px 20px rgba(201, 163, 95, 0.5);
}
.lock-close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: none;
  border: none;
  color: var(--cream);
  font-size: 20px;
  cursor: pointer;
  opacity: 0.7;
}
.lock-close-btn:hover { opacity: 1; color: var(--gold); }
"""
html = html.replace('</style>', f'\n{dead_space_css}\n</style>')

# 3. Remove "Explore All Kalakaari" button from Kalakaari
html = re.sub(
    r'<div class="k-all">\s*<a class="cta" href="#">.*?Explore All Kalakaari.*?</a>\s*</div>',
    '',
    html,
    flags=re.DOTALL
)

# 4. Remove section in Picture 4 (b-all, b-corner-l, b-corner-r)
pic4_pattern = r'<div class="b-all">\s*<a class="cta" href="#">.*?Shop Best Sellers.*?</a>\s*</div>\s*<p class="b-corner b-corner-l".*?</p>\s*<p class="b-corner b-corner-r".*?</p>'
html = re.sub(pic4_pattern, '', html, flags=re.DOTALL)

# Also ensure Best Sellers cards link to collections.html
html = html.replace('<a class="cta" href="#">', '<a class="cta" href="collections.html">')

# 5. Remove the Atelier Login bar from the footer
html = re.sub(r'<div class="f-atelier-portal-bar".*?</div>\s*</div>', '</div>', html, flags=re.DOTALL)
# Also remove any standalone f-atelier-portal-bar
html = re.sub(r'<div class="f-atelier-portal-bar".*?</div>', '', html, flags=re.DOTALL)

# 6. Remove Pinterest icon and add Lock icon at the end of .f-social
pinterest_pattern = r'<a href="#" aria-label="Pinterest">.*?</a>'
html = re.sub(pinterest_pattern, '', html, flags=re.DOTALL)

lock_btn_html = """
        <button type="button" class="f-lock-btn" id="lockModalBtn" aria-label="Atelier Staff Management" title="Atelier Management Portal">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
            <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
          </svg>
        </button>
"""
# Insert lock_btn_html inside .f-social right before its closing </div>
html = re.sub(r'(<div class="f-social">.*?)(</div>)', r'\1' + lock_btn_html + r'\2', html, flags=re.DOTALL)

# 7. Add Lock Login Modal right before </body>
lock_modal_markup = """
<!-- ======================= ATELIER LOCK MODAL ======================= -->
<div class="atelier-lock-modal" id="atelierLockModal" aria-hidden="true">
  <div class="lock-dialog">
    <button class="lock-close-btn" id="lockCloseBtn" aria-label="Close dialog">&times;</button>
    <div class="lock-icon-crest">
      <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
        <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
      </svg>
    </div>
    <h3>Atelier Management</h3>
    <p>Sign in to manage, edit, add, or update garments on your live website catalog.</p>
    <form class="lock-form" id="lockLoginForm">
      <input type="password" id="lockPassInput" placeholder="Enter Access Passcode" required autocomplete="current-password" autofocus>
      <button type="submit" class="lock-submit-btn">✦ Enter Dashboard</button>
    </form>
    <p style="font-size: 11px; margin-top: 14px; opacity: 0.6; letter-spacing: 0.5px;">Atelier Passcode: <code>aleen</code></p>
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
    openBtn.addEventListener('click', (e) => {
      e.preventDefault();
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      if (passInput) passInput.focus();
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
    });
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
      }
    });
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      sessionStorage.setItem('aleen_admin_auth', 'true');
      window.location.href = 'admin.html';
    });
  }
})();
</script>
"""
html = html.replace('</body>', f'{lock_modal_markup}\n</body>')

# 8. Update all URLs in index.html:
# - Change 'mahira.html' to 'index.html'
html = html.replace('mahira.html', 'index.html')
# - Ensure no CRM redirects exist
html = html.replace('/login', 'admin.html')
html = html.replace('href="#best"', 'href="collections.html"')

dest_path = os.path.join("Aleen website", "index.html")
with open(dest_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Generated Aleen website/index.html successfully!")
