/* ===========================================
   Busy Bee Maine Coons — Cart (localStorage)
   Stores reservations and shop products.
   =========================================== */
(function () {
  'use strict';

  const STORAGE_KEY = 'bbmc_cart_v1';

  function read() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || []; }
    catch { return []; }
  }
  function write(cart) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    updateBadge();
  }
  function updateBadge() {
    const count = read().reduce((n, item) => n + (item.qty || 1), 0);
    document.querySelectorAll('.cart-badge').forEach((el) => { el.textContent = String(count); });
  }

  function add(item) {
    const cart = read();
    const existing = cart.find((c) => c.id === item.id);
    if (existing) {
      existing.qty = (existing.qty || 1) + (item.qty || 1);
    } else {
      cart.push(Object.assign({ qty: 1 }, item));
    }
    write(cart);
    if (typeof window.showToast === 'function') {
      window.showToast(item.name + ' added to cart');
    }
  }

  function remove(id) {
    const cart = read().filter((c) => c.id !== id);
    write(cart);
    if (typeof renderCartPage === 'function') renderCartPage();
  }

  function clear() {
    write([]);
    if (typeof renderCartPage === 'function') renderCartPage();
  }

  // Public API
  window.BBMCCart = { read, add, remove, clear, update: write, updateBadge };

  // Wire up any [data-add-cart] buttons
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-add-cart]');
    if (!btn) return;
    add({
      id: btn.dataset.id || btn.dataset.addCart,
      name: btn.dataset.name || btn.textContent.trim(),
      price: parseFloat(btn.dataset.price) || 0,
      type: btn.dataset.type || 'product',
    });
  });

  // ---- Cart page rendering ----
  const cartList = document.getElementById('cart-list');
  function renderCartPage() {
    if (!cartList) return;
    const cart = read();
    if (!cart.length) {
      cartList.innerHTML = '<p class="lead text-center" style="padding:2rem 0;">Your cart is empty. <a href="kittens.html">Browse available kittens</a> or <a href="shop.html">shop our store</a>.</p>';
      const totalEl = document.getElementById('cart-total');
      if (totalEl) totalEl.textContent = '$0.00';
      return;
    }
    let total = 0;
    cartList.innerHTML = cart.map((item) => {
      const lineTotal = (item.price || 0) * (item.qty || 1);
      total += lineTotal;
      return (
        '<div class="cart-row" style="display:grid;grid-template-columns:1fr auto auto auto;gap:1rem;align-items:center;padding:1rem 0;border-bottom:1px solid var(--gray-200);">' +
          '<div><strong style="color:var(--primary);">' + escapeHtml(item.name) + '</strong>' +
            '<div style="font-size:.8125rem;color:var(--text-muted);">' + escapeHtml(item.type || '') + '</div>' +
          '</div>' +
          '<div>$' + (item.price || 0).toFixed(2) + '</div>' +
          '<div>Qty: ' + (item.qty || 1) + '</div>' +
          '<button class="btn btn-outline" style="padding:.4rem .75rem;" data-remove="' + escapeHtml(item.id) + '" aria-label="Remove ' + escapeHtml(item.name) + '">Remove</button>' +
        '</div>'
      );
    }).join('');
    const totalEl = document.getElementById('cart-total');
    if (totalEl) totalEl.textContent = '$' + total.toFixed(2);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  }

  if (cartList) {
    renderCartPage();
    cartList.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-remove]');
      if (btn) remove(btn.dataset.remove);
    });
    const clearBtn = document.getElementById('cart-clear');
    if (clearBtn) clearBtn.addEventListener('click', clear);
  }

  updateBadge();
})();
