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
