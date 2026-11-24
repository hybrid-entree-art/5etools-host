/* 5E ATLAS — shared mobile shell for the remaining native 5e.tools pages. */
(() => {
  const body = document.body;
  const page = body.dataset.atlasPage || (location.pathname.split('/').pop() || 'index.html').replace(/\.html$/, '');
  const titles = {
    actions: 'Azioni', backgrounds: 'Background', bastions: 'Bastioni', book: 'Manuale',
    books: 'Biblioteca', charcreationoptions: 'Creazione personaggio', classes: 'Classi',
    conditionsdiseases: 'Condizioni e malattie', cultsboons: 'Culti e doni', decks: 'Mazzi',
    deities: 'Divinità', encountergen: 'Generatore di incontri', feats: 'Talenti',
    homecrafts: 'Artigianato', items: 'Oggetti', languages: 'Lingue', names: 'Nomi',
    objects: 'Oggetti', optionalfeatures: 'Privilegi opzionali', psionics: 'Psionica',
    races: 'Specie', recipes: 'Ricette', rewards: 'Ricompense', tables: 'Tabelle',
    trapshazards: 'Trappole e pericoli', variantrules: 'Glossario', vehicles: 'Veicoli',
    adventures: 'Avventure', adventure: 'Avventura', search: 'Cerca', dmscreen: 'Schermo DM',
    lootgen: 'Tesori', statgen: 'Caratteristiche', crcalculator: 'Calcolatore GS',
    maps: 'Mappe', lifegen: 'Storia personaggio', quickreference: 'Riferimento rapido',
    converter: 'Convertitore', changelog: 'Novità', blocklist: 'Esclusioni',
    makebrew: 'Crea homebrew', makecards: 'Crea carte', managebrew: 'Gestisci homebrew',
    manageprerelease: 'Gestisci prerelease', plutonium: 'Plutonium', 'privacy-policy': 'Privacy',
  };
  const title = body.dataset.atlasTitle || titles[page] || document.title.replace(' - 5etools', '');
  body.classList.add('atlas-site');

  const appbar = document.createElement('header');
  appbar.className = 'atlas-sitebar';
  appbar.innerHTML = `
    <a href="atlas.html" aria-label="Torna alla home 5E Atlas"><svg viewBox="0 0 24 24"><path d="m15 18-6-6 6-6"/></svg></a>
    <div class="atlas-sitebar-title">${title}<small>5e.tools core</small></div>
    <button type="button" class="atlas-site-filter" id="atlasSiteFilter" hidden>Filtri</button>`;
  body.prepend(appbar);
  const appbarBack = appbar.querySelector('a');
  const appbarTitle = appbar.querySelector('.atlas-sitebar-title');
  const sectionTitle = appbarTitle?.innerHTML || '';

  const getNativeFilter = () => [...document.querySelectorAll('#filter-search-group > button, #filtertools button')]
    .find((btn) => btn.textContent.trim().toLowerCase() === 'filter');
  const filterBtn = document.getElementById('atlasSiteFilter');
  const syncFilterButton = () => {
    if (filterBtn) filterBtn.hidden = !getNativeFilter();
  };
  if (filterBtn) {
    syncFilterButton();
    setTimeout(syncFilterButton, 600);
    setTimeout(syncFilterButton, 1500);
    filterBtn.addEventListener('click', () => getNativeFilter()?.click());
    new MutationObserver(syncFilterButton).observe(document.body, {childList: true, subtree: true});
  }

  const content = document.getElementById('contentwrapper');
  if (content) {
    const back = document.createElement('button');
    back.type = 'button';
    back.id = 'atlasSiteBack';
    back.textContent = 'Indietro';
    content.prepend(back);

    const open = () => {
      body.classList.add('atlas-detail-open');
      content.scrollTop = 0;
      const name = document.querySelector('#pagecontent h1')?.innerText.trim();
      if (appbarTitle && name) appbarTitle.innerHTML = `${name}<small>${title}</small>`;
    };
    const close = () => {
      body.classList.remove('atlas-detail-open');
      if (appbarTitle) appbarTitle.innerHTML = sectionTitle;
      if (location.hash) history.replaceState(null, '', location.pathname + location.search);
      document.getElementById('listcontainer')?.scrollIntoView({block: 'start'});
    };
    back.addEventListener('click', close);
    appbarBack?.addEventListener('click', (e) => {
      if (body.classList.contains('atlas-detail-open')) { e.preventDefault(); close(); }
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && body.classList.contains('atlas-detail-open')) close();
    });
    document.addEventListener('click', (e) => {
      const target = e.target instanceof Element ? e.target : null;
      const row = target?.closest('#listcontainer a[href^="#"], #listcontainer .ve-lst__row, #list-mundane .ve-lst__row, #list-magic .ve-lst__row');
      if (row) setTimeout(open, 140);
    }, true);
    if (window.__atlasSiteInitialHash && window.__atlasSiteInitialHash.length > 1) {
      const openInitial = () => {
        if (document.querySelector('#pagecontent h1')) open();
        else setTimeout(openInitial, 150);
      };
      setTimeout(openInitial, 300);
    }
  }

  const diceFab = document.querySelector('.rollbox-min');
  if (diceFab) {
    diceFab.setAttribute('aria-label', 'Apri tira-dadi');
    diceFab.setAttribute('title', 'Apri tira-dadi');
  }
  const search = document.getElementById('lst__search') || document.getElementById('search');
  if (search) {
    if (page === 'books') search.placeholder = 'Cerca manuale…';
    else if (page === 'adventures') search.placeholder = 'Cerca avventura…';
    else if (!search.placeholder) search.placeholder = 'Cerca nel compendio…';
    search.setAttribute('aria-label', search.placeholder);
  }
  const siteSearch = document.querySelector('.pg-search__ipt, input.search');
  if (siteSearch && page === 'search') {
    siteSearch.placeholder = 'Cerca incantesimo, mostro, classe, regola…';
  }
})();
