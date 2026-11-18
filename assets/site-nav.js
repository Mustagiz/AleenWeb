/* Aleen Clothing — responsive header navigation.
 *
 * The storefront header carries a centred mark with a pair of inline links.
 * Below 1200px those links are hidden, so this module adds the hamburger and a
 * single shared drawer. Every page loads this file instead of pasting its own
 * drawer markup; any stale #mobileNav block is removed on the way in.
 */
(function () {
  'use strict';

  var DESKTOP = 1200;

  var PRIMARY = [
    { label: 'Home', href: '/' },
    { label: 'Garments', href: '/collections' },
    { label: 'Our Story', href: '/our-story' },
    { label: 'Contact Us', href: '/contact-us' }
  ];

  var SHOP = [
    { label: 'Sarees', href: '/collections?category=sarees' },
    { label: 'Kurta Sets', href: '/collections?category=kurta-sets' },
    { label: 'Lehengas', href: '/collections?category=lehengas' },
    { label: 'Dresses', href: '/dresses' },
    { label: 'All Garments', href: '/collections' },
    { label: 'Atelier Console', href: '/admin' }
  ];

  function currentPath() {
    var p = window.location.pathname.replace(/index\.html$/, '');
    return p === '' ? '/' : p;
  }

  function normalize(path) {
    return path.replace(/\.html$/, '').replace(/\/$/, '');
  }

  // Only the most specific match is marked: on /collections?category=sarees
  // that is "Sarees", not the three broader /collections links beside it.
  function currentHref() {
    var here = normalize(currentPath());
    var search = window.location.search;
    var best = null;
    var bestQuery = -1;

    PRIMARY.concat(SHOP).forEach(function (item) {
      if (normalize(item.href.split('?')[0]) !== here) return;
      var query = item.href.indexOf('?') === -1 ? '' : item.href.slice(item.href.indexOf('?'));
      if (query && query !== search) return;
      if (query.length > bestQuery) {
        best = item.href;
        bestQuery = query.length;
      }
    });

    return best;
  }

  function linkHTML(item, index, activeHref) {
    var active = item.href === activeHref ? ' aria-current="page"' : '';
    var numeral = index === null ? '' : '<span class="sd-idx">' + String(index + 1).padStart(2, '0') + '</span>';
    return '<a href="' + item.href + '"' + active + '>' +
      '<span>' + item.label + '</span>' + numeral +
      '</a>';
  }

  function buildDrawer() {
    var drawer = document.createElement('div');
    drawer.className = 'site-drawer';
    drawer.id = 'siteNav';
    drawer.setAttribute('aria-hidden', 'true');

    var activeHref = currentHref();
    var rail = PRIMARY.map(function (item, i) { return linkHTML(item, i, activeHref); }).join('');
    var shop = SHOP.map(function (item) { return linkHTML(item, null, activeHref); }).join('');

    drawer.innerHTML =
      '<div class="sd-top">' +
        '<span class="sd-eyebrow">Aleen &middot; Menu</span>' +
        '<button class="sd-close" type="button" aria-label="Close menu">' +
          '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 4l12 12M16 4L4 16"/></svg>' +
        '</button>' +
      '</div>' +
      '<div class="sd-body">' +
        '<nav class="sd-nav" aria-label="Primary">' + rail + '</nav>' +
        '<p class="sd-label">Shop by silhouette</p>' +
        '<div class="sd-grid">' + shop + '</div>' +
        '<div class="sd-foot">' +
          '<a class="sd-cta" href="/collections">Explore the Collections</a>' +
          '<p class="sd-meta">Handcrafted in Lucknow</p>' +
        '</div>' +
      '</div>';

    return drawer;
  }

  function init() {
    if (document.getElementById('siteNav')) return;

    var header = document.getElementById('header') || document.querySelector('header.site-header');
    if (!header) return;

    // Remove the stale drawer copies left over from earlier builds.
    Array.prototype.forEach.call(document.querySelectorAll('#mobileNav, .mobile-nav'), function (n) {
      if (n.parentNode) n.parentNode.removeChild(n);
    });

    var toggle = document.createElement('button');
    toggle.className = 'nav-toggle';
    toggle.id = 'navToggle';
    toggle.type = 'button';
    toggle.setAttribute('aria-label', 'Open menu');
    toggle.setAttribute('aria-controls', 'siteNav');
    toggle.setAttribute('aria-expanded', 'false');
    toggle.innerHTML = '<span></span><span></span>';
    header.insertBefore(toggle, header.firstChild);

    // Sits directly after the header in the DOM (it is position: fixed, so this
    // is only about reading order) — Tab from the toggle walks into the sheet.
    var drawer = buildDrawer();
    header.parentNode.insertBefore(drawer, header.nextSibling);

    var lastFocus = null;

    function open() {
      lastFocus = document.activeElement;
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Close menu');
      document.documentElement.classList.add('nav-open');
      var close = drawer.querySelector('.sd-close');
      if (close) close.focus({ preventScroll: true });
    }

    function close(restoreFocus) {
      if (!drawer.classList.contains('is-open')) return;
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Open menu');
      document.documentElement.classList.remove('nav-open');
      if (restoreFocus) {
        // Pointer-opened sheets leave focus on <body>; hand it back to the
        // toggle so the next Tab continues from the header.
        var target = lastFocus && lastFocus !== document.body ? lastFocus : toggle;
        if (target && target.focus) target.focus({ preventScroll: true });
      }
    }

    toggle.addEventListener('click', function () {
      if (drawer.classList.contains('is-open')) close(true);
      else open();
    });

    drawer.addEventListener('click', function (event) {
      if (event.target.closest && event.target.closest('a')) {
        close(false);
        return;
      }
      if (event.target.closest && event.target.closest('.sd-close')) close(true);
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' || event.key === 'Esc') {
        close(true);
        return;
      }
      if (event.key !== 'Tab' || !drawer.classList.contains('is-open')) return;

      var focusable = drawer.querySelectorAll('a[href], button:not([disabled])');
      if (!focusable.length) return;
      var first = focusable[0];
      var last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });

    // Leaving the drawer breakpoint — by resize or by rotating a tablet —
    // always drops the sheet and releases the scroll lock.
    var desktopQuery = window.matchMedia('(min-width: ' + DESKTOP + 'px)');
    function onBreakpoint(event) {
      if (event.matches) close(false);
    }
    if (desktopQuery.addEventListener) desktopQuery.addEventListener('change', onBreakpoint);
    else if (desktopQuery.addListener) desktopQuery.addListener(onBreakpoint);

    var resizeTimer;
    window.addEventListener('resize', function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        if (window.innerWidth >= DESKTOP) close(false);
      }, 120);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
