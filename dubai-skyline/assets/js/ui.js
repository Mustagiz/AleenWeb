/* UI layer — deliberately independent of Three.js so the page is
   visible and interactive while the 3D scene is still initialising. */

const body = document.body;
const isTouch = window.matchMedia('(hover: none), (pointer: coarse)').matches;
body.classList.add('is-loaded');

const nav = document.querySelector('.nav');
const railLinks = [...document.querySelectorAll('.rail a')];
const sections = [...document.querySelectorAll('[data-chapter]')];

function onScrollUI() {
  const y = window.scrollY;
  if (nav) nav.classList.toggle('is-solid', y > 40);

  const max = document.documentElement.scrollHeight - window.innerHeight;
  const p = max > 0 ? y / max : 0;
  const line = document.querySelector('.rail-progress span');
  if (line) line.style.transform = `scaleY(${p})`;

  let active = 0;
  sections.forEach((s, i) => {
    const rect = s.getBoundingClientRect();
    if (rect.top <= window.innerHeight * 0.45) active = i;
  });
  railLinks.forEach((a, i) => a.classList.toggle('is-active', i === active));
}
window.addEventListener('scroll', onScrollUI, { passive: true });
onScrollUI();

/* Instant depth on the static hero: the poster is a real 3D render, so a
   tiny pointer parallax makes it feel dimensional before WebGL is ready. */
const poster = document.querySelector('.fallback img');
if (poster && !isTouch) {
  window.addEventListener('pointermove', (e) => {
    if (document.body.classList.contains('is-scene-ready')) return;
    const x = (e.clientX / window.innerWidth - 0.5) * -18;
    const y = (e.clientY / window.innerHeight - 0.5) * -10;
    poster.style.setProperty('--px', `${x.toFixed(1)}px`);
    poster.style.setProperty('--py', `${y.toFixed(1)}px`);
  }, { passive: true });
}

/* cursor */
if (!isTouch) {
  const dot = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');
  if (dot && ring) {
    let mx = window.innerWidth / 2;
    let my = window.innerHeight / 2;
    let rx = mx;
    let ry = my;
    window.addEventListener('pointermove', (e) => {
      mx = e.clientX;
      my = e.clientY;
      dot.style.transform = `translate3d(${mx}px, ${my}px, 0)`;
    }, { passive: true });

    const loop = () => {
      rx += (mx - rx) * 0.18;
      ry += (my - ry) * 0.18;
      ring.style.transform = `translate3d(${rx}px, ${ry}px, 0)`;
      requestAnimationFrame(loop);
    };
    loop();

    document.querySelectorAll('a, button, .card, input, select, textarea').forEach((el) => {
      el.addEventListener('mouseenter', () => body.classList.add('cursor-grow'));
      el.addEventListener('mouseleave', () => body.classList.remove('cursor-grow'));
    });
  }
}

/* mobile menu */
const toggle = document.querySelector('.nav-toggle');
if (toggle) {
  toggle.addEventListener('click', () => {
    const open = body.classList.toggle('nav-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  document.querySelectorAll('.nav-links a').forEach((a) =>
    a.addEventListener('click', () => {
      body.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
    })
  );
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && body.classList.contains('nav-open')) {
      body.classList.remove('nav-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });
}

/* optional live 3D: the poster is the instant hero, WebGL is opt-in */
const launch3D = document.getElementById('launch-3d');
if (launch3D) {
  launch3D.addEventListener('click', () => {
    launch3D.disabled = true;
    launch3D.textContent = 'Preparing live 3D…';
    import('./main.js').catch((err) => {
      launch3D.textContent = 'Live 3D unavailable';
      console.error(err);
    });
  });
}

/* form */
const form = document.getElementById('enquiry');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const note = form.querySelector('.form-note');
    if (note) {
      note.textContent = 'Received. A private advisor will contact you within one business day.';
      note.classList.add('is-visible');
    }
    form.reset();
  });
}

/* reveal-on-scroll */
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        io.unobserve(entry.target);
      }
    });
  },
  { rootMargin: '-8% 0px -6% 0px' }
);
document.querySelectorAll('.reveal').forEach((el) => {
  const rect = el.getBoundingClientRect();
  if (rect.top < window.innerHeight * 0.92 && rect.bottom > 0) {
    /* Above-the-fold content must never wait for an observer callback:
       it is visible even while the 3D scene is still booting. */
    el.classList.add('in-view');
  } else {
    el.classList.add('reveal-pending');
    io.observe(el);
  }
});
