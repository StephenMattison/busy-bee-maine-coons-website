/* ====================================================
   Busy Bee Maine Coons — Newsletter + exit-intent
   Posts to /api/subscribe (Cloudflare Pages Function)
   ==================================================== */
(function () {
  'use strict';

  var ENDPOINT = '/api/subscribe';
  var STORAGE_KEY = 'busybee_nl';
  var EXIT_STORAGE = 'busybee_nl_exit_shown';
  var EXIT_DELAY = 4000;
  var MOBILE_SCROLL_DELAY = 25000;
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function getState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
    catch (e) { return {}; }
  }

  function saveState(data) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(data)); }
    catch (e) { /* silent */ }
  }

  function handleSubmit(form) {
    var input = form.querySelector('input[type="email"]');
    var btn = form.querySelector('button[type="submit"], .nl-btn');
    var wrap = form.closest('.nl-inner, .nl-popup, .nl-section') || form.parentElement;
    var successEl = wrap ? wrap.querySelector('.nl-success') : null;
    var errorEl = wrap ? wrap.querySelector('.nl-error') : null;
    var email = (input && input.value || '').trim().toLowerCase();
    var source = form.getAttribute('data-nl-source') || 'inline';

    if (successEl) { successEl.textContent = ''; successEl.classList.remove('show'); }
    if (errorEl) { errorEl.textContent = ''; errorEl.classList.remove('show'); }

    if (!EMAIL_RE.test(email)) {
      if (errorEl) {
        errorEl.textContent = 'Please enter a valid email address.';
        errorEl.classList.add('show');
      }
      if (input) input.focus();
      return;
    }

    var original = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = 'Joining…'; }
    if (input) input.disabled = true;

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email,
        list: 'Busy_Bee_Hive',
        source: source,
        path: location.pathname,
      }),
    })
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        }).catch(function () {
          return { ok: res.ok, data: {} };
        });
      })
      .then(function (result) {
        if (!result.ok) {
          var msg = (result.data && (result.data.error || result.data.message)) ||
            'Something went wrong. Please try again in a moment.';
          if (errorEl) {
            errorEl.textContent = msg;
            errorEl.classList.add('show');
          }
          return;
        }
        saveState({ subscribed: true, email: email, ts: Date.now() });
        form.style.display = 'none';
        if (successEl) {
          successEl.textContent = 'Welcome to the Hive! Check your inbox for early litter alerts and your shop welcome offer.';
          successEl.classList.add('show');
        }
        if (source === 'exit') {
          setTimeout(closePopup, 2200);
        }
      })
      .catch(function () {
        if (errorEl) {
          errorEl.textContent = 'Connection issue. Check your internet and try again.';
          errorEl.classList.add('show');
        }
      })
      .finally(function () {
        if (btn) { btn.disabled = false; btn.textContent = original || 'Join free'; }
        if (input) input.disabled = false;
      });
  }

  /* ── Exit-intent popup ── */
  var popupEl = null;
  var exitEnabled = false;

  function openPopup() {
    if (!popupEl) return;
    if (getState().subscribed) return;
    try {
      if (sessionStorage.getItem(EXIT_STORAGE)) return;
      sessionStorage.setItem(EXIT_STORAGE, '1');
    } catch (e) { /* silent */ }

    popupEl.hidden = false;
    popupEl.setAttribute('aria-hidden', 'false');
    requestAnimationFrame(function () {
      popupEl.classList.add('active');
    });
    document.body.classList.add('nl-popup-open');
    var closeBtn = popupEl.querySelector('.nl-popup-close');
    if (closeBtn) closeBtn.focus();
  }

  function closePopup() {
    if (!popupEl) return;
    popupEl.classList.remove('active');
    document.body.classList.remove('nl-popup-open');
    popupEl.setAttribute('aria-hidden', 'true');
    setTimeout(function () {
      if (!popupEl.classList.contains('active')) popupEl.hidden = true;
    }, 280);
  }

  function pathBlocksPopup() {
    var p = (location.pathname || '').replace(/\/+$/, '') || '/';
    return p === '/cart' || p === '/account' || /\/cart\.html$|\/account\.html$/.test(p);
  }

  function initExitIntent() {
    popupEl = document.getElementById('nl-popup-overlay');
    if (!popupEl || pathBlocksPopup()) return;
    if (getState().subscribed) return;
    try {
      if (sessionStorage.getItem(EXIT_STORAGE)) return;
    } catch (e) { /* silent */ }

    setTimeout(function () { exitEnabled = true; }, EXIT_DELAY);

    document.addEventListener('mouseout', function (e) {
      if (!exitEnabled) return;
      if (e.clientY <= 0 && !e.relatedTarget) {
        exitEnabled = false;
        openPopup();
      }
    });

    // Mobile / tablet: after time on page + meaningful scroll, offer once
    var scrolledDeep = false;
    window.addEventListener('scroll', function () {
      if (window.scrollY > window.innerHeight * 0.45) scrolledDeep = true;
    }, { passive: true });

    setTimeout(function () {
      if (!exitEnabled || getState().subscribed) return;
      if (window.matchMedia('(max-width: 900px)').matches && scrolledDeep) {
        exitEnabled = false;
        openPopup();
      }
    }, MOBILE_SCROLL_DELAY);

    var closeBtn = popupEl.querySelector('.nl-popup-close');
    if (closeBtn) closeBtn.addEventListener('click', closePopup);
    popupEl.addEventListener('click', function (e) {
      if (e.target === popupEl) closePopup();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && popupEl.classList.contains('active')) closePopup();
    });
  }

  function init() {
    var state = getState();
    document.querySelectorAll('.nl-form').forEach(function (form) {
      if (state.subscribed) {
        form.style.display = 'none';
        var wrap = form.closest('.nl-inner, .nl-popup, .nl-section') || form.parentElement;
        var successEl = wrap && wrap.querySelector('.nl-success');
        if (successEl) {
          successEl.textContent = 'You\'re already in the Hive — watch your inbox for litter alerts and care tips.';
          successEl.classList.add('show');
        }
      }
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        handleSubmit(form);
      });
    });
    initExitIntent();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
