/* =====================================================
   Busy Bee Maine Coons — Main JS
   Mobile menu, fade-on-scroll, scroll-to-top, toasts,
   FAQ enhancements, kitten filtering.
   ===================================================== */
(function () {
  'use strict';

  /* ---------- MOBILE MENU ---------- */
  const mobileToggle = document.getElementById('mobile-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', function () {
      const isOpen = mobileMenu.classList.toggle('open');
      mobileToggle.setAttribute('aria-expanded', String(isOpen));
      mobileToggle.innerHTML = isOpen
        ? '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M18 6L6 18M6 6l12 12"/></svg>'
        : '<svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 12h18M3 6h18M3 18h18"/></svg>';
    });
  }

  /* ---------- TOAST ---------- */
  const toastEl = document.getElementById('toast');
  let toastTimer;
  function showToast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove('show'), 3000);
  }
  window.showToast = showToast;

  /* ---------- SCROLL-TO-TOP ---------- */
  const scrollBtn = document.getElementById('scroll-top');
  if (scrollBtn) {
    window.addEventListener('scroll', () => {
      scrollBtn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
    scrollBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ---------- FADE-IN ON SCROLL ---------- */
  const faders = document.querySelectorAll('.fade-on-scroll');
  if (faders.length && 'IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('fade-in');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    faders.forEach((el) => obs.observe(el));
  } else {
    faders.forEach((el) => el.classList.add('fade-in'));
  }

  /* ---------- KITTEN/PRODUCT FILTERING ---------- */
  const filters = document.querySelectorAll('[data-filter]');
  const sortSelect = document.getElementById('sort-select');
  const grid = document.querySelector('[data-filterable-grid]');

  function applyFilters() {
    if (!grid) return;
    const cards = Array.from(grid.querySelectorAll('[data-card]'));
    const activeFilters = {};
    filters.forEach((sel) => {
      const v = sel.value;
      if (v && v !== 'all') activeFilters[sel.dataset.filter] = v;
    });
    let visible = 0;
    cards.forEach((card) => {
      const match = Object.entries(activeFilters).every(([k, v]) => (card.dataset[k] || '').toLowerCase() === v.toLowerCase());
      card.style.display = match ? '' : 'none';
      if (match) visible += 1;
    });
    const counter = document.getElementById('result-count');
    if (counter) counter.textContent = visible + ' result' + (visible !== 1 ? 's' : '');
  }

  filters.forEach((sel) => sel.addEventListener('change', applyFilters));
  if (filters.length) applyFilters();

  if (sortSelect && grid) {
    sortSelect.addEventListener('change', () => {
      const cards = Array.from(grid.querySelectorAll('[data-card]'));
      const mode = sortSelect.value;
      cards.sort((a, b) => {
        const pa = parseFloat(a.dataset.price) || 0;
        const pb = parseFloat(b.dataset.price) || 0;
        const aa = parseFloat(a.dataset.age) || 0;
        const ab = parseFloat(b.dataset.age) || 0;
        if (mode === 'price-asc') return pa - pb;
        if (mode === 'price-desc') return pb - pa;
        if (mode === 'age-asc')   return aa - ab;
        if (mode === 'age-desc')  return ab - aa;
        return 0;
      });
      cards.forEach((c) => grid.appendChild(c));
    });
  }

  /* ---------- FORM (CONTACT / RESERVE) DEMO ---------- */
  document.querySelectorAll('form[data-demo-form]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const success = form.querySelector('.form-success-msg');
      if (success) {
        success.classList.add('show');
        form.reset();
        setTimeout(() => success.classList.remove('show'), 6000);
      } else {
        showToast('Thanks — we\u2019ll be in touch shortly.');
        form.reset();
      }
    });
  });

  /* ---------- SET CURRENT NAV LINK ---------- */
  const path = window.location.pathname.replace(/\/+$/, '') || '/';
  document.querySelectorAll('.nav-links a, .mobile-menu a').forEach((a) => {
    const href = a.getAttribute('href') || '';
    const norm = href.replace(/\.html$/, '').replace(/^\//, '/');
    const cur = path.replace(/\.html$/, '');
    if ((cur === '/' && (href === 'index.html' || href === '/' || href === './')) ||
        (cur !== '/' && (norm === cur || norm === cur + '/' || ('/' + href.replace(/\.html$/, '')) === cur))) {
      a.setAttribute('aria-current', 'page');
    }
  });

  /* ---------- GOOGLE REVIEW SYSTEM (SITE-GUIDE §0) ---------- */
  const cfg = window.BUSYBEE || {};
  const reviewUrl =
    cfg.googleReviewUrl ||
    'https://www.google.com/search?q=Busy+Bee+Maine+Coons+cooncatcentral.com+reviews';
  const reviewQr =
    cfg.googleReviewQr ||
    '/images/review/google-review-qr.png' +
      (cfg.assetVersion ? '?v=' + cfg.assetVersion : '');
  const reviewFab = document.getElementById('review-fab');
  const reviewDialog = document.getElementById('review-dialog');
  const reviewClose = document.getElementById('review-dialog-close');
  let lastFocus = null;

  function track(eventName, payload) {
    try {
      if (window.dataLayer && typeof window.dataLayer.push === 'function') {
        window.dataLayer.push(Object.assign({ event: eventName }, payload || {}));
      }
    } catch (err) { /* analytics optional */ }
  }

  function openReview(source) {
    if (!reviewDialog) return;
    lastFocus = document.activeElement;
    reviewDialog.hidden = false;
    document.body.classList.add('dialog-open');
    track('review_cta_open', { source: source || 'fab' });
    const closeBtn = reviewClose || reviewDialog.querySelector('button');
    if (closeBtn) closeBtn.focus();
  }

  function closeReview() {
    if (!reviewDialog) return;
    reviewDialog.hidden = true;
    document.body.classList.remove('dialog-open');
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  if (reviewFab) {
    reviewFab.addEventListener('click', function () {
      openReview('floating');
    });
  }

  document.querySelectorAll('[data-open-review]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      openReview(el.getAttribute('data-open-review') || 'inline');
    });
  });

  if (reviewClose) {
    reviewClose.addEventListener('click', closeReview);
  }

  if (reviewDialog) {
    reviewDialog.addEventListener('click', function (e) {
      if (e.target === reviewDialog) closeReview();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !reviewDialog.hidden) closeReview();
    });
  }

  document.querySelectorAll('[data-review-link]').forEach(function (el) {
    el.setAttribute('href', reviewUrl);
    el.addEventListener('click', function () {
      track('review_link_click', {
        source: el.getAttribute('data-review-link') || 'unknown',
      });
    });
  });

  document.querySelectorAll('img[data-review-qr]').forEach(function (img) {
    img.setAttribute('src', reviewQr);
  });
})();
