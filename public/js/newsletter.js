/* ====================================================
   Busy Bee Maine Coons — Newsletter signup
   Posts to /api/subscribe (Cloudflare Pages Function)
   ==================================================== */
(function () {
  'use strict';

  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  document.querySelectorAll('.nl-form').forEach((form) => {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const successEl = form.parentElement.querySelector('.nl-success');
      const errorEl   = form.parentElement.querySelector('.nl-error');
      if (successEl) successEl.textContent = '';
      if (errorEl) errorEl.textContent = '';

      const input = form.querySelector('input[type="email"]');
      const email = (input?.value || '').trim();
      if (!EMAIL_RE.test(email)) {
        if (errorEl) errorEl.textContent = 'Please enter a valid email address.';
        return;
      }

      const btn = form.querySelector('button[type="submit"]');
      const original = btn ? btn.textContent : '';
      if (btn) { btn.disabled = true; btn.textContent = 'Subscribing…'; }

      try {
        const res = await fetch('/api/subscribe', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email }),
        });
        if (!res.ok) throw new Error('subscribe_failed');
        if (successEl) successEl.textContent = 'Welcome to the hive — check your inbox for your 10% off code.';
        form.reset();
      } catch {
        if (errorEl) errorEl.textContent = 'Something went wrong. Please try again in a moment.';
      } finally {
        if (btn) { btn.disabled = false; btn.textContent = original; }
      }
    });
  });
})();
