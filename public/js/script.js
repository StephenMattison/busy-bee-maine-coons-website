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
})();
