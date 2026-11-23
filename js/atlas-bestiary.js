/* 5E ATLAS — mobile behaviour for the 5e.tools spells screen.
   The core list renderer and URLs stay untouched. */
(() => {
  const body = document.body;
  const content = document.getElementById('contentwrapper');
  if (!content) return;

  const openDetail = () => {
    body.classList.add('atlas-detail-open');
    content.scrollTop = 0;
  };

  const closeDetail = () => {
    body.classList.remove('atlas-detail-open');
    if (location.hash) {
      history.replaceState(null, '', location.pathname + location.search);
    }
    const list = document.getElementById('listcontainer');
    if (list) list.scrollIntoView({block: 'start'});
  };

  document.getElementById('atlasDetailBack')?.addEventListener('click', closeDetail);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && body.classList.contains('atlas-detail-open')) closeDetail();
  });

  // A list row is an anchor handled by 5e.tools; let the core update the hash,
  // then reveal the native detail table as a full-screen panel on phones.
  document.addEventListener('click', (e) => {
    const row = e.target.closest('#list a');
    if (!row) return;
    setTimeout(openDetail, 80);
  });



  // 5e.tools renders ability scores as three dense groups of 4 columns.
  // Rebuild that native table as six readable cards on phones, moving the
  // original dice spans so their inline roll handlers keep working.
  const ABILITY_NAMES = {Str: 'FOR', Dex: 'DES', Con: 'COS', Int: 'INT', Wis: 'SAG', Cha: 'CAR'};
  const ABILITY_TITLES = {Str: 'Forza', Dex: 'Destrezza', Con: 'Costituzione', Int: 'Intelligenza', Wis: 'Saggezza', Cha: 'Carisma'};
  const upgradeAbilityTable = () => {
    if (!window.matchMedia('(max-width: 767px)').matches) return;
    const abv = document.querySelector('#pagecontent .ve-stats-tbl-ability-scores__lbl-abv');
    const table = abv?.closest('table');
    if (!table || table.dataset.atlasAbility === '1') return;
    table.dataset.atlasAbility = '1';
    const dataRows = [...table.querySelectorAll('tbody tr')].filter(tr => tr.querySelector('.ve-stats-tbl-ability-scores__lbl-abv')?.innerText.trim());
    const grid = document.createElement('div');
    grid.className = 'atlas-ability-grid';
    dataRows.forEach((tr) => {
      const cells = [...tr.children];
      cells.forEach((cell, i) => {
        if (!cell.classList.contains('ve-stats-tbl-ability-scores__lbl-abv') || !cell.innerText.trim()) return;
        const score = cells[i + 1];
        const mod = cells[i + 2];
        const save = cells[i + 3];
        if (!score || !mod || !save) return;
        const key = cell.innerText.trim();
        const card = document.createElement('div');
        card.className = 'atlas-ability-card';
        const fullName = ABILITY_TITLES[key] || key;
        card.title = fullName;
        const label = document.createElement('span');
        label.className = 'atlas-ability-abv';
        label.textContent = ABILITY_NAMES[key] || key.toUpperCase();
        const scoreEl = document.createElement('b');
        scoreEl.className = 'atlas-ability-score';
        scoreEl.textContent = score.innerText.trim();
        const lineMod = document.createElement('small');
        lineMod.className = 'atlas-ability-line';
        lineMod.innerHTML = '<em>Mod</em>';
        const modVal = mod.querySelector('.ve-roller') || mod.firstElementChild || mod;
        if (modVal) { modVal.remove(); lineMod.append(modVal); }
        const lineSave = document.createElement('small');
        lineSave.className = 'atlas-ability-line';
        lineSave.innerHTML = '<em>TS</em>';
        const saveVal = save.querySelector('.ve-roller') || save.firstElementChild || save;
        if (saveVal) { saveVal.remove(); lineSave.append(saveVal); }
        card.setAttribute('aria-label', `${fullName}: punteggio ${scoreEl.textContent}, modificatore ${modVal?.textContent || ''}, tiro salvezza ${saveVal?.textContent || ''}`);
        if ((modVal?.textContent || '').trim().startsWith('-')) lineMod.classList.add('is-negative');
        if ((saveVal?.textContent || '').trim().startsWith('-')) lineSave.classList.add('is-negative');
        card.append(label, scoreEl, lineMod, lineSave);
        grid.append(card);
      });
    });
    if (grid.children.length === 6) table.replaceWith(grid);
  };
  setTimeout(upgradeAbilityTable, 500);
  setTimeout(upgradeAbilityTable, 1200);
  new MutationObserver(upgradeAbilityTable).observe(document.body, {childList: true, subtree: true});

  // Deep links from search/book pages should land on the sheet, not on the list.
  if (window.__atlasInitialHash && window.__atlasInitialHash.length > 1) {
    const openInitial = () => {
      if (document.querySelector('#pagecontent h1')) openDetail();
      else setTimeout(openInitial, 150);
    };
    setTimeout(openInitial, 250);
  }

  // The core filter summary is a desktop chip-wall. On phones the same
  // filters live behind the native dialog; hide the wall, keep the state.
  const hideCoreChrome = () => {
    ['#filtertools', '.ve-fltr__mini-view', '.ve-lst__wrp-search-visible'].forEach((sel) => {
      document.querySelectorAll(sel).forEach((el) => {
        if (el.style.getPropertyValue('display') !== 'none') el.style.setProperty('display', 'none', 'important');
      });
    });
    if (window.matchMedia('(max-width: 767px)').matches) {
      const listWrap = document.getElementById('listcontainer');
      if (listWrap) {
        listWrap.style.setProperty('width', '100%', 'important');
        listWrap.style.setProperty('flex', '1 1 auto', 'important');
        listWrap.style.setProperty('padding', '0 16px', 'important');
        listWrap.style.setProperty('margin', '0', 'important');
        listWrap.style.setProperty('box-sizing', 'border-box', 'important');
      }
      const wrapper = document.querySelector('.view-col-wrapper');
      if (wrapper) {
        wrapper.style.setProperty('width', '100%', 'important');
        wrapper.style.setProperty('max-width', 'none', 'important');
        wrapper.style.setProperty('padding', '0', 'important');
        wrapper.style.setProperty('margin', '0', 'important');
      }
      const list = document.getElementById('list');
      if (list) list.style.setProperty('width', '100%', 'important');
    }
    const diceFab = document.querySelector('.rollbox-min');
    if (diceFab) {
      diceFab.setAttribute('aria-label', 'Apri tira-dadi');
      diceFab.setAttribute('title', 'Apri tira-dadi');
    }
    const search = document.getElementById('lst__search');
    if (search && !search.placeholder) {
      search.placeholder = 'Cerca mostri…';
      search.setAttribute('aria-label', 'Cerca mostri');
    }
  };
  hideCoreChrome();
  setTimeout(hideCoreChrome, 400);
  setTimeout(hideCoreChrome, 1200);
  new MutationObserver(hideCoreChrome).observe(document.body, {childList: true, subtree: true});

  // The core filter button is hidden on mobile; the redesigned top bar
  // opens the same native filter dialog instead of duplicating filter state.
  document.getElementById('atlasFilterBtn')?.addEventListener('click', () => {
    const nativeFilter = [...document.querySelectorAll('#filter-search-group > button')]
      .find((btn) => btn.textContent.trim() === 'Filter');
    nativeFilter?.click();
  });
})();
