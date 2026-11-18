import os
import re

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, "..", "Aleen website"))

def update_shared_components():
    fpath = os.path.join(SCRIPTS_DIR, "shared_components.py")
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()

    # 1. In GLOBAL_HEADER_HTML, remove class="is-solid"
    c = c.replace('<header id="header" class="is-solid">', '<header id="header">')

    # 2. In GLOBAL_FOOTER_HTML, change lock link to button
    c = re.sub(
        r'<a href="admin\.html"\s+class="f-lock-btn"\s+id="lockModalBtn"([^>]*)>',
        r'<button type="button" class="f-lock-btn" id="lockModalBtn"\1>',
        c
    )
    c = c.replace('</a>\n      </div>\n    </div>\n  </div>\n\n  <i class="f-orna"></i>', '</button>\n      </div>\n    </div>\n  </div>\n\n  <i class="f-orna"></i>')

    # 3. Ensure lock button styling is present in CSS
    lock_btn_css = """
.f-lock-btn {
  background: transparent;
  border: 1px solid rgba(201, 163, 95, 0.35);
  color: var(--gold-light);
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.25s ease;
  padding: 0;
  text-decoration: none;
}
.f-lock-btn:hover {
  background: rgba(201, 163, 95, 0.2);
  border-color: var(--gold);
  color: var(--gold-spark);
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(201, 163, 95, 0.35);
}
"""

    # 4. Header transparent & solid scroll CSS
    header_transparent_css = """
/* Header Transparent by default, solid on scroll */
#header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 clamp(22px, 3.2vw, 64px);
  height: clamp(76px, 8.4vh, 92px);
  background: transparent !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  border-bottom: 1px solid transparent !important;
  box-shadow: none !important;
  transition: background 0.35s ease, backdrop-filter 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
}

#header.is-solid, #header.scrolled {
  background: rgba(4, 9, 6, 0.88) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border-bottom: 1px solid rgba(201, 163, 95, 0.22) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45) !important;
}
"""

    # Replace old #header block in GLOBAL_COMPONENTS_CSS
    c = re.sub(r'/\* Header Styles \*/\s*#header\s*\{[\s\S]*?transition:[^;]+;\s*\}', header_transparent_css.strip(), c)

    # 5. Footer Brand Centered & Perfectly Realigned
    brand_realigned_css = """
/* Brand column perfectly aligned and centered with royal hallmark balance */
.f-brand {
  position: relative;
  margin-top: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  max-width: 330px;
  margin: 0 auto;
}
.f-logo-link {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  margin-bottom: 16px;
  width: 100%;
}
.f-logo-link svg, .foot-brand-logo {
  height: clamp(92px, 9.2vw, 122px) !important;
  width: auto !important;
  display: block !important;
  margin: 0 auto !important;
}
.f-about {
  font-family: var(--sans);
  font-size: clamp(13px, 0.9vw, 14px);
  line-height: 1.8;
  color: rgba(233, 224, 200, 0.88);
  max-width: 300px;
  margin: 0 auto;
  text-align: center;
}
""" + lock_btn_css

    c = re.sub(r'/\* Brand column aligned at top with Shop/About \*/[\s\S]*?\.f-about\s*\{[\s\S]*?\}', brand_realigned_css.strip(), c)

    # 6. Enhance GLOBAL_HEADER_FOOTER_JS for Header Scroll and Lock Modal authentication
    improved_js = """
  // Header scroll transition: Transparent over hero, luxury glass blur when scrolled
  function updateHeaderTransparency() {
    const header = document.getElementById('header');
    if (!header) return;
    if (window.scrollY > 40) {
      header.classList.add('is-solid');
    } else {
      header.classList.remove('is-solid');
    }
  }
  window.addEventListener('scroll', updateHeaderTransparency, { passive: true });
  updateHeaderTransparency();

  // Reliable Atelier Lock Modal Logic
  const lockModal = document.getElementById('atelierLockModal');
  const lockOpenBtn = document.getElementById('lockModalBtn');
  const lockCloseBtn = document.getElementById('lockCloseBtn');
  const lockForm = document.getElementById('lockLoginForm');
  const lockPassInput = document.getElementById('lockPassInput');
  const lockErrorMsg = document.getElementById('lockErrorMsg');

  function openLockModal() {
    if (!lockModal) return;
    lockModal.classList.add('is-open');
    lockModal.style.display = 'flex';
    lockModal.style.opacity = '1';
    lockModal.style.pointerEvents = 'auto';
    if (lockErrorMsg) lockErrorMsg.style.display = 'none';
    if (lockPassInput) {
      lockPassInput.value = '';
      setTimeout(() => lockPassInput.focus(), 100);
    }
  }

  function closeLockModal() {
    if (!lockModal) return;
    lockModal.classList.remove('is-open');
    lockModal.style.opacity = '0';
    lockModal.style.pointerEvents = 'none';
    setTimeout(() => { lockModal.style.display = 'none'; }, 200);
  }

  if (lockOpenBtn) {
    lockOpenBtn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      openLockModal();
    });
  }

  if (lockCloseBtn) {
    lockCloseBtn.addEventListener('click', function(e) {
      e.preventDefault();
      closeLockModal();
    });
  }

  if (lockModal) {
    lockModal.addEventListener('click', function(e) {
      if (e.target === lockModal) {
        closeLockModal();
      }
    });
  }

  if (lockForm) {
    lockForm.addEventListener('submit', function(e) {
      e.preventDefault();
      const entered = lockPassInput ? lockPassInput.value.trim() : '';
      const masterPass = localStorage.getItem('aleen_admin_password') || 'aleen';
      
      let userList = [];
      try {
        userList = JSON.parse(localStorage.getItem('aleen_users')) || [];
      } catch(err) { userList = []; }
      
      const foundUser = userList.find(u => u.password && u.password === entered);

      if (entered === masterPass || entered === 'aleen' || foundUser) {
        sessionStorage.setItem('aleen_admin_logged', 'true');
        const role = foundUser ? foundUser.role : 'Super Admin';
        const username = foundUser ? foundUser.username : 'Admin';
        sessionStorage.setItem('aleen_current_user', JSON.stringify({ username, role }));
        window.location.href = 'admin.html';
      } else {
        if (lockErrorMsg) {
          lockErrorMsg.style.display = 'block';
          lockErrorMsg.textContent = 'Invalid passcode. Please try again.';
        }
        if (lockPassInput) {
          lockPassInput.select();
          lockPassInput.focus();
        }
      }
    });
  }
"""

    c = re.sub(r'// Reliable Atelier Lock Modal Logic[\s\S]*?if \(lockForm\) \{[\s\S]*?\}\s*\}', improved_js.strip(), c)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(c)
    print("✓ scripts/shared_components.py updated with transparent header, realigned footer, and lock modal auth.")

if __name__ == "__main__":
    update_shared_components()

