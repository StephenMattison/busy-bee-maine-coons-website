// Story modal: opens hidden articles in an overlay when a card link is clicked.
(function () {
  var ARTICLE_IDS = ['first-30-days', 'hcm-explained', 'ethical-breeders', 'size-and-growth', 'polydactyl-maine-coons', 'best-cat-tree'];
  var modal = document.getElementById('story-modal');
  var content = document.getElementById('story-modal-content');
  var library = document.getElementById('story-articles');
  if (!modal || !content || !library) return;
  var lastFocused = null;

  function openArticle(id, updateHash) {
    var src = library.querySelector('#' + CSS.escape(id) + ' .article');
    if (!src) return false;
    content.innerHTML = '';
    content.appendChild(src.cloneNode(true));
    lastFocused = document.activeElement;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    var closeBtn = modal.querySelector('.story-modal-close');
    if (closeBtn) closeBtn.focus();
    var panel = modal.querySelector('.story-modal-panel');
    if (panel) panel.scrollTop = 0;
    if (updateHash) history.pushState({ storyId: id }, '', '#' + id);
    return true;
  }

  function closeModal(updateHash) {
    if (modal.hidden) return;
    modal.hidden = true;
    document.body.style.overflow = '';
    content.innerHTML = '';
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
    if (updateHash && location.hash) history.pushState('', '', location.pathname + location.search);
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute('href').slice(1);
    if (ARTICLE_IDS.indexOf(id) === -1) return;
    if (openArticle(id, true)) e.preventDefault();
  });

  modal.addEventListener('click', function (e) {
    if (e.target.closest('[data-close-modal]')) closeModal(true);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !modal.hidden) closeModal(true);
  });
  window.addEventListener('popstate', function () {
    var id = location.hash.slice(1);
    if (id && ARTICLE_IDS.indexOf(id) !== -1) openArticle(id, false);
    else closeModal(false);
  });

  if (location.hash) {
    var hashId = location.hash.slice(1);
    if (ARTICLE_IDS.indexOf(hashId) !== -1) openArticle(hashId, false);
  }
})();
