'use strict';
(() => {
  const header = document.querySelector('.header');
  const toggle = document.querySelector('.nav-toggle');
  const navigation = document.querySelector('#navigation');
  toggle.hidden = false;
  header.classList.add('nav-ready');
  const mobileLayout = matchMedia('(max-width: 900px)');
  const backdrop = document.querySelector('.nav-backdrop');
  const main = document.querySelector('main');
  const brand = header.querySelector('.wordmark');
  let navigationOverflow = '';
  function setNavigation(open, restoreFocus = false) {
    const wasOpen = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Закрыть меню' : 'Открыть меню');
    navigation.classList.toggle('is-open', open);
    backdrop.hidden = !open;
    if (open && !wasOpen) {
      navigationOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
    } else if (!open && wasOpen) document.body.style.overflow = navigationOverflow;
    main.inert = open;
    document.querySelector('.back-to-top').inert = open;
    brand.inert = open;
    if (restoreFocus) toggle.focus();
  }
  function closeNavigation(restoreFocus) {
    setNavigation(false, restoreFocus);
  }
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    setNavigation(open);
  });
  navigation.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link) return;
    const mobileOpen = toggle.getAttribute('aria-expanded') === 'true';
    closeNavigation(false);
    if (mobileOpen) {
      const href = link.getAttribute('href');
      const target = href.startsWith('#') ? document.getElementById(href.slice(1)) : null;
      if (target) { target.tabIndex = -1; target.focus({preventScroll:true}); }
    }
  });
  document.addEventListener('keydown', event => {
    if (toggle.getAttribute('aria-expanded') !== 'true') return;
    if (event.key === 'Escape') closeNavigation(true);
    if (event.key === 'Tab') {
      const controls = [toggle, ...navigation.querySelectorAll('a')];
      if (event.shiftKey && document.activeElement === controls[0]) { event.preventDefault(); controls[controls.length-1].focus(); }
      else if (!event.shiftKey && document.activeElement === controls[controls.length-1]) { event.preventDefault(); toggle.focus(); }
    }
  });
  document.addEventListener('click', event => { if (!header.contains(event.target)) closeNavigation(false); });
  mobileLayout.addEventListener('change', () => closeNavigation(false));

  const cards = Array.from(document.querySelectorAll('.dish'));
  const groups = Array.from(document.querySelectorAll('.menu-group'));
  const filters = Array.from(document.querySelectorAll('[data-filter]'));
  const status = document.querySelector('#menu-status');
  const viewTitle = document.querySelector('#menu-view-title');
  let category = 'all';
  const expandedCategories = new Set();
  document.querySelector('.menu-tools').hidden = false;
  const categoryLabels = {'Салаты':'салаты','Роллы':'роллы','Супы':'супы','Холодные закуски':'холодные закуски','Бургер':'бургеры','Горячие блюда':'горячие блюда','Горячие закуски':'горячие закуски','Десерты':'десерты'};
  function filterMenu() {
    let count = 0;
    groups.forEach(group => {
      const name = group.dataset.menuCategory;
      const groupCards = Array.from(group.querySelectorAll('.dish'));
      const selected = category === 'all' || category === name;
      const limit = expandedCategories.has(name) ? groupCards.length : 4;
      groupCards.forEach((card,index) => { card.hidden = !selected || index >= limit; });
      const visibleCount = selected ? Math.min(limit,groupCards.length) : 0;
      count += visibleCount;
      group.hidden = !selected;
      group.classList.toggle('single-dish', visibleCount === 1);
      group.dataset.visibleCount = String(visibleCount);
      group.querySelector('.menu-group-title').hidden = category !== 'all';
      const more = group.querySelector('.menu-more');
      more.hidden = !selected || groupCards.length <= 4;
      more.setAttribute('aria-expanded', String(expandedCategories.has(name)));
      more.textContent = expandedCategories.has(name) ? 'Показать меньше' : `Посмотреть все ${categoryLabels[name] || name.toLocaleLowerCase('ru')} (${groupCards.length})`;
    });
    viewTitle.textContent = category === 'all' ? 'Все блюда' : category;
    const total = category === 'all' ? cards.length : cards.filter(card => card.dataset.category === category).length;
    status.textContent = count < total ? `${count} из ${total}` : `Позиций: ${count}`;
  }
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
    filterMenu();
  }));
  groups.forEach(group => group.querySelector('.menu-more').addEventListener('click', () => {
    const firstNewCard = group.querySelector('.dish[hidden]');
    const name = group.dataset.menuCategory;
    const collapsing = expandedCategories.has(name);
    if (collapsing) expandedCategories.delete(name);
    else expandedCategories.add(name);
    filterMenu();
    if (collapsing) group.querySelector('.menu-more').focus();
    if (!collapsing && firstNewCard) {
      const title = firstNewCard.querySelector('h4');
      title.tabIndex = -1;
      title.focus({preventScroll:true});
    }
  }));
  filterMenu();

  const backToTop = document.querySelector('.back-to-top');
  function updateBackToTop() { backToTop.hidden = window.scrollY < 400; }
  window.addEventListener('scroll', updateBackToTop, {passive:true});
  backToTop.addEventListener('click', () => {
    const home = document.querySelector('#home');
    home.tabIndex = -1;
    home.focus({preventScroll:true});
  });
  updateBackToTop();

  const gallery = Array.from(document.querySelectorAll('[data-gallery]'));
  const dialog = document.querySelector('.lightbox');
  const image = document.querySelector('#gallery-image');
  const counter = document.querySelector('#gallery-counter');
  const close = document.querySelector('#close-gallery');
  let current = 0;
  let opener = null;
  let savedOverflow = '';
  function showPhoto(index) {
    current = (index + gallery.length) % gallery.length;
    const photo = gallery[current];
    image.src = photo.getAttribute('href');
    image.alt = photo.dataset.caption;
    counter.textContent = `${current + 1} / ${gallery.length}`;
  }
  if (typeof dialog.showModal === 'function') {
    gallery.forEach((link, index) => link.addEventListener('click', event => {
      event.preventDefault();
      opener = link;
      showPhoto(index);
      savedOverflow = document.body.style.overflow;
      document.body.style.overflow = 'hidden';
      dialog.showModal();
      close.focus();
    }));
    close.addEventListener('click', () => dialog.close());
    document.querySelector('#previous-photo').addEventListener('click', () => showPhoto(current - 1));
    document.querySelector('#next-photo').addEventListener('click', () => showPhoto(current + 1));
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const box = dialog.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
    });
    dialog.addEventListener('keydown', event => {
      if (event.key === 'ArrowRight') { event.preventDefault(); showPhoto(current + 1); }
      if (event.key === 'ArrowLeft') { event.preventDefault(); showPhoto(current - 1); }
      if (event.key === 'Tab') {
        const focusable = Array.from(dialog.querySelectorAll('button'));
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
    });
    let touchStart = null;
    image.addEventListener('touchstart', event => {
      if (event.touches.length === 1) touchStart = {x:event.touches[0].clientX,y:event.touches[0].clientY};
    }, {passive:true});
    image.addEventListener('touchend', event => {
      if (!touchStart || !event.changedTouches.length) return;
      const deltaX = event.changedTouches[0].clientX - touchStart.x;
      const deltaY = event.changedTouches[0].clientY - touchStart.y;
      if (Math.abs(deltaX) > 45 && Math.abs(deltaX) > Math.abs(deltaY)) showPhoto(current + (deltaX < 0 ? 1 : -1));
      touchStart = null;
    }, {passive:true});
    dialog.addEventListener('close', () => {
      document.body.style.overflow = savedOverflow;
      if (opener) opener.focus({preventScroll:true});
    });
  }
})();
