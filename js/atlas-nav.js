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
  const groups = [
    ['Giocatore', [
      ['Classi', 'classes.html', 'classes'],
      ['Incantesimi', 'spells.html', 'spells'],
      ['Specie', 'races.html', 'races'],
      ['Background', 'backgrounds.html', 'backgrounds'],
      ['Talenti', 'feats.html', 'feats'],
      ['Oggetti', 'items.html', 'items'],
      ['Privilegi opzionali', 'optionalfeatures.html', 'optionalfeatures'],
      ['Creazione PG', 'charcreationoptions.html', 'charcreationoptions'],
      ['Psionica', 'psionics.html', 'psionics'],
    ]],
    ['Regole e Manuali', [
      ['Biblioteca', 'books.html', 'books'],
      ['Avventure', 'adventures.html', 'adventures'],
      ['Glossario', 'variantrules.html', 'variantrules'],
      ['Riferimento rapido', 'quickreference.html', 'quickreference'],
      ['Azioni', 'actions.html', 'actions'],
      ['Condizioni e malattie', 'conditionsdiseases.html', 'conditionsdiseases'],
      ['Lingue', 'languages.html', 'languages'],
      ['Divinità', 'deities.html', 'deities'],
    ]],
    ['Dungeon Master', [
      ['Mostri', 'bestiary.html', 'bestiary'],
      ['Trappole e pericoli', 'trapshazards.html', 'trapshazards'],
      ['Culti e doni', 'cultsboons.html', 'cultsboons'],
      ['Bastioni', 'bastions.html', 'bastions'],
      ['Ricompense', 'rewards.html', 'rewards'],
      ['Oggetti di scena', 'objects.html', 'objects'],
      ['Veicoli', 'vehicles.html', 'vehicles'],
      ['Tabelle', 'tables.html', 'tables'],
      ['Mazzi', 'decks.html', 'decks'],
    ]],
    ['Strumenti', [
      ['Cerca ovunque', 'search.html', 'search'],
      ['Schermo DM', 'dmscreen.html', 'dmscreen'],
      ['Generatore incontri', 'encountergen.html', 'encountergen'],
      ['Generatore tesori', 'lootgen.html', 'lootgen'],
      ['Calcolatore GS', 'crcalculator.html', 'crcalculator'],
      ['Generatore nomi', 'names.html', 'names'],
      ['Mappe', 'maps.html', 'maps'],
    ]],
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
      ${groups.map(([gTitle, links]) => `<div class="atlas-menu-group"><h3>${gTitle}</h3><div class="atlas-menu-grid">${links.map(([label, href, key]) => `<a href="${href}"${key === page ? ' aria-current="page"' : ''}>${label}<span>${key === page ? 'Sei qui' : '→'}</span></a>`).join('')}</div></div>`).join('')}
    </div>`;
  document.body.append(dialog);
  document.body.classList.add('atlas-nav-on');

  const openMenu = () => { if (!dialog.open) dialog.showModal(); };
  const closeMenu = () => { if (dialog.open) dialog.close(); };
  document.querySelectorAll('[data-atlas-menu-open]').forEach((btn) => btn.addEventListener('click', openMenu));
  document.querySelectorAll('[data-atlas-menu-close]').forEach((btn) => btn.addEventListener('click', closeMenu));
  dialog.addEventListener('click', (e) => { if (e.target === dialog) closeMenu(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });



  // Native dice roller polish: Italian placeholder + accessible close control.
  const polishRollbox = () => {
    const box = document.querySelector('.rollbox');
    if (!box) return;
    const ipt = box.querySelector('.ipt-roll');
    if (ipt) {
      ipt.placeholder = 'Es. 8d6+6 oppure /help';
      ipt.setAttribute('aria-label', 'Tiro di dado');
    }
    const close = box.querySelector('.glyphicon-remove');
    if (close) {
      close.setAttribute('role', 'button');
      close.setAttribute('tabindex', '0');
      close.setAttribute('aria-label', 'Chiudi tira-dadi');
      if (!close.dataset.atlasCloseBound) {
        close.dataset.atlasCloseBound = '1';
        close.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') close.click(); });
      }
    }
    // Inline overrides beat the native !important rules regardless of CSS order/layers.
    const set = (el, props) => { if (el) Object.entries(props).forEach(([k, v]) => el.style.setProperty(k, v, 'important')); };
    set(box, {position: 'fixed', right: '14px', left: 'auto', bottom: 'calc(82px + env(safe-area-inset-bottom))', width: 'min(340px, calc(100vw - 28px))', 'max-height': 'calc(100dvh - 180px)', height: 'auto', padding: '0', border: '1px solid rgba(185,196,206,.2)', 'border-radius': '16px', background: '#1a2028', color: '#d8e2ea', 'box-shadow': '0 18px 50px rgba(6,9,12,.65)', 'z-index': '140', overflow: 'hidden'});
    set(box.querySelector('.head-roll'), {display: 'flex', 'align-items': 'center', 'justify-content': 'space-between', 'min-height': '48px', padding: '0 8px 0 14px', background: '#222a34', color: '#d8e2ea', 'border-bottom': '1px solid rgba(185,196,206,.16)'});
    set(box.querySelector('.hdr-roll'), {font: '700 20px/1 AtlasCond,Georgia,serif', color: '#d8e2ea', 'letter-spacing': '.02em'});
    set(box.querySelector('.glyphicon-remove'), {display: 'grid', 'place-items': 'center', width: '48px', height: '48px', color: '#b5c1cb', 'font-size': '16px', cursor: 'pointer'});
    set(box.querySelector('.out-roll'), {'min-height': '96px', 'max-height': 'calc(100dvh - 300px)', 'overflow-y': 'auto', padding: '12px 14px', background: '#1a2028', color: '#d8e2ea', font: '14px/1.55 AtlasBody,system-ui,sans-serif'});
    if (ipt) set(ipt, {display: 'block', width: 'calc(100% - 28px)', 'min-height': '48px', margin: '10px 14px 14px', padding: '0 12px', border: '1px solid rgba(185,196,206,.22)', 'border-radius': '12px', background: '#222a34', color: '#d8e2ea', font: '15px AtlasBody,system-ui,sans-serif'});
  };
  document.addEventListener('click', (e) => {
    const target = e.target instanceof Element ? e.target : null;
    if (target?.closest('.rollbox-min')) {
      [0, 80, 300, 700].forEach((ms) => setTimeout(polishRollbox, ms));
    }
  });

  // Separate the dice roller from scroll-to-top; add an in-app bug report.
  if (!document.querySelector('.atlas-fab')) {
    const fab = document.createElement('div');
    fab.className = 'atlas-fab';
    fab.innerHTML = `
      <button type="button" class="atlas-fab-top" aria-label="Torna in cima" title="Torna in cima"><svg viewBox="0 0 24 24"><path d="m5 14 7-7 7 7"/></svg></button>
      <button type="button" class="atlas-fab-bug" aria-label="Segnala un problema" title="Segnala un problema"><svg viewBox="0 0 24 24"><path d="M9 6a3 3 0 0 1 6 0"/><path d="M6 13a6 6 0 0 1 12 0v2a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4z"/><path d="M3 10h3M18 10h3M3 17h3M18 17h3M12 13v6"/></svg></button>`;
    document.body.append(fab);

    const topBtn = fab.querySelector('.atlas-fab-top');
    const syncTop = () => topBtn.classList.toggle('is-visible', window.scrollY > 240);
    syncTop();
    window.addEventListener('scroll', syncTop, {passive: true});
    topBtn.addEventListener('click', () => window.scrollTo({top: 0, behavior: 'smooth'}));

    const dlg = document.createElement('dialog');
    dlg.className = 'atlas-bug-dialog';
    dlg.id = 'atlasBugDialog';
    dlg.setAttribute('aria-labelledby', 'atlasBugTitle');
    dlg.innerHTML = `
      <div class="atlas-bug-head">
        <b id="atlasBugTitle">Segnala un problema</b>
        <button type="button" data-atlas-bug-close aria-label="Chiudi segnalazione"><svg viewBox="0 0 24 24"><path d="m6 6 12 12M18 6 6 18"/></svg></button>
      </div>
      <div class="atlas-bug-body">
        <p>Descrivi cosa non funziona. La segnalazione include pagina, viewport e browser; niente dati personali.</p>
        <label for="atlasBugText">Cosa è successo?</label>
        <textarea id="atlasBugText" placeholder="Es. nella scheda del Barbaro i tab sottoclasse non rispondono al tocco…"></textarea>
        <div class="atlas-bug-actions">
          <button type="button" data-atlas-bug-copy>Copia</button>
          <button type="button" class="is-primary" data-atlas-bug-send>Apri issue GitHub</button>
        </div>
        <div class="atlas-bug-status" role="status" aria-live="polite"></div>
      </div>`;
    document.body.append(dlg);

    const text = dlg.querySelector('#atlasBugText');
    const status = dlg.querySelector('.atlas-bug-status');
    const openBug = () => {
      status.textContent = '';
      if (!dlg.open) dlg.showModal();
      setTimeout(() => text.focus(), 80);
    };
    const closeBug = () => { if (dlg.open) dlg.close(); };
    const report = () => `[Atlas] ${text.value.trim() || '(nessuna descrizione)'}\n\nPagina: ${location.pathname}${location.search}${location.hash}\nViewport: ${innerWidth}x${innerHeight}\nUA: ${navigator.userAgent}`;

    fab.querySelector('.atlas-fab-bug').addEventListener('click', openBug);
    dlg.querySelector('[data-atlas-bug-close]').addEventListener('click', closeBug);
    dlg.addEventListener('click', (e) => { if (e.target === dlg) closeBug(); });

    dlg.querySelector('[data-atlas-bug-copy]').addEventListener('click', async () => {
      const body = report();
      try {
        await navigator.clipboard.writeText(body);
        status.textContent = 'Segnalazione copiata negli appunti.';
      } catch (_) {
        const ta = document.createElement('textarea');
        ta.value = body;
        document.body.append(ta);
        ta.select();
        document.execCommand('copy');
        ta.remove();
        status.textContent = 'Segnalazione copiata.';
      }
    });

    dlg.querySelector('[data-atlas-bug-send]').addEventListener('click', () => {
      const title = encodeURIComponent('[Atlas] ' + (text.value.trim().slice(0, 80) || 'Problema UI'));
      const body = encodeURIComponent(report());
      window.open(`https://github.com/hybrid-entree-art/5etools-host/issues/new?title=${title}&body=${body}`, '_blank', 'noopener');
      status.textContent = 'Issue aperta su GitHub: allega lo screenshot se puoi.';
    });
  }

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
