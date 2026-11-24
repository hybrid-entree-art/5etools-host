/* 5E ATLAS — single source for mobile navigation and section menu. */
(() => {
  const path = location.pathname.split('/').pop() || 'atlas.html';
  const infer = path === '' || path === 'atlas.html' || path === 'index.html'
    ? 'home'
    : path.replace(/\.html$/, '');
  const page = document.body.dataset.atlasPage || infer;
  const sectionPages = new Set(['home', 'spells', 'bestiary']);
  const active = sectionPages.has(page) ? page : 'menu';
  const items = [
    {key: 'home', href: 'atlas.html', label: 'Home', icon: '<path d="m4 11 8-7 8 7v9a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1z"/>'},
    {key: 'spells', href: 'spells.html', label: 'Incantesimi', icon: '<path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>'},
    {key: 'bestiary', href: 'bestiary.html', label: 'Mostri', icon: '<path d="M4 8c3-3 6-3 8 0 2-3 5-3 8 0v9c-3-2-6-2-8 0-2-2-5-2-8 0z"/>'},
    {key: 'menu', label: 'Menu', icon: '<path d="M4 7h16M4 12h16M4 17h16"/>', button: true},
  ];
  const sections = [
    ['Classi', 'classes.html', 'classes'],
    ['Oggetti', 'items.html', 'items'],
    ['Background', 'backgrounds.html', 'backgrounds'],
    ['Talenti', 'feats.html', 'feats'],
    ['Specie', 'races.html', 'races'],
    ['Glossario', 'variantrules.html', 'variantrules'],
    ['Cerca', 'search.html', 'search'],
    ['Libreria', 'books.html', 'books'],
  ];

  document.querySelectorAll('.atlas-bottom, .bottom').forEach((el) => el.remove());

  const nav = document.createElement('nav');
  nav.className = 'atlas-global-nav';
  nav.setAttribute('aria-label', 'Navigazione mobile');
  nav.innerHTML = items.map((item) => item.button
    ? `<button type="button" data-atlas-menu-open${item.key === active ? ' aria-current="page"' : ''}><svg viewBox="0 0 24 24" aria-hidden="true">${item.icon}</svg><span>${item.label}</span></button>`
    : `<a href="${item.href}"${item.key === active ? ' aria-current="page"' : ''}><svg viewBox="0 0 24 24" aria-hidden="true">${item.icon}</svg><span>${item.label}</span></a>`).join('');
  document.body.append(nav);

  const dialog = document.createElement('dialog');
  dialog.className = 'atlas-menu';
  dialog.id = 'atlasMenu';
  dialog.setAttribute('aria-labelledby', 'atlasMenuTitle');
  dialog.innerHTML = `
    <div class="atlas-menu-head">
      <b id="atlasMenuTitle">Menu</b>
      <button type="button" data-atlas-menu-close aria-label="Chiudi menu"><svg viewBox="0 0 24 24"><path d="m6 6 12 12M18 6 6 18"/></svg></button>
    </div>
    <div class="atlas-menu-list">
      ${sections.map(([label, href, key]) => `<a href="${href}"${key === page ? ' aria-current="page"' : ''}>${label}<span>${key === page ? 'Sei qui' : '→'}</span></a>`).join('')}
    </div>`;
  document.body.append(dialog);
  document.body.classList.add('atlas-nav-on');

  const openMenu = () => { if (!dialog.open) dialog.showModal(); };
  const closeMenu = () => { if (dialog.open) dialog.close(); };
  document.querySelectorAll('[data-atlas-menu-open]').forEach((btn) => btn.addEventListener('click', openMenu));
  document.querySelectorAll('[data-atlas-menu-close]').forEach((btn) => btn.addEventListener('click', closeMenu));
  dialog.addEventListener('click', (e) => { if (e.target === dialog) closeMenu(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });

  // Zero-cost image CDN: redirect 5e.tools img/ requests to public 5etools-img CDN.
  const IMG_CDN = 'https://cdn.jsdelivr.net/gh/5etools-mirror-3/5etools-img@main/';
  const hookRendererImages = () => {
    if (typeof Renderer === 'undefined' || !Renderer.prototype?.getMediaUrl || Renderer.prototype._atlasMediaHooked) return false;
    Renderer.prototype._atlasMediaHooked = true;
    const orig = Renderer.prototype.getMediaUrl;
    Renderer.prototype.getMediaUrl = function (mediaDir, path) {
      if (mediaDir === 'img' && path) {
        return IMG_CDN + String(path).replace(/^\/+/, '');
      }
      return orig.call(this, mediaDir, path);
    };
    return true;
  };
  if (!hookRendererImages()) {
    let tries = 0;
    const timer = setInterval(() => {
      if (hookRendererImages() || ++tries > 60) clearInterval(timer);
    }, 50);
  }

  // Telegram Mini App integration (safe no-op in standard browsers).
  const initTelegram = () => {
    const tg = window.Telegram?.WebApp;
    if (!tg) return;
    try {
      tg.ready();
      tg.expand();
      tg.setHeaderColor?.('#1a2028');
      tg.setBackgroundColor?.('#1a2028');
      const syncViewport = () => {
        if (tg.viewportStableHeight) {
          document.documentElement.style.setProperty('--tg-vh', `${tg.viewportStableHeight}px`);
        }
      };
      syncViewport();
      tg.onEvent?.('viewportChanged', syncViewport);

      const syncBack = () => {
        const hasOverlay = dialog.open
          || document.body.classList.contains('atlas-detail-open')
          || document.body.classList.contains('atlas-class-open')
          || document.body.classList.contains('atlas-toc-open');
        if (hasOverlay) tg.BackButton?.show();
        else tg.BackButton?.hide();
      };
      tg.BackButton?.onClick(() => {
        if (dialog.open) return closeMenu();
        if (document.body.classList.contains('atlas-toc-open')) {
          document.getElementById('atlasTocBtn')?.click();
          return;
        }
        if (document.body.classList.contains('atlas-class-open')) {
          document.getElementById('atlasClassBack')?.click();
          return;
        }
        if (document.body.classList.contains('atlas-detail-open')) {
          const back = document.querySelector('.atlas-appbar > a, .atlas-sitebar > a, #atlasSiteBack');
          back?.click();
          return;
        }
        history.back();
      });
      new MutationObserver(syncBack).observe(document.body, {attributes: true, attributeFilter: ['class']});
      new MutationObserver(syncBack).observe(dialog, {attributes: true, attributeFilter: ['open']});
      syncBack();
    } catch (_) {}
  };
  if (window.Telegram?.WebApp) {
    initTelegram();
  } else if (window.TelegramWebviewProxy || /tgWebApp/i.test(location.search + location.hash) || /Telegram/i.test(navigator.userAgent)) {
    const sc = document.createElement('script');
    sc.src = 'https://telegram.org/js/telegram-web-app.js';
    sc.async = true;
    sc.onload = initTelegram;
    document.head.appendChild(sc);
  }
})();
