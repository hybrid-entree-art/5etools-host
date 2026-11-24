/* 5E ATLAS — class list/detail flow on top of the native classes renderer. */
(() => {
  const body = document.body;
  const list = document.getElementById('listcontainer');
  const panel = document.getElementById('classtable');
  if (!list || !panel) return;
  body.classList.add('atlas-classes');

  const title = document.querySelector('.atlas-sitebar-title');
  const appbarBack = document.querySelector('.atlas-sitebar > a');
  const originalTitle = title?.innerHTML || 'Classi<small>5e.tools core</small>';

  const back = document.createElement('button');
  back.type = 'button';
  back.id = 'atlasClassBack';
  back.textContent = 'Indietro';
  const ensureBack = () => {
    if (!document.getElementById('atlasClassBack')) panel.prepend(back);
    if (!back.isConnected) panel.prepend(back);
  };
  ensureBack();

  const translateHeaders = () => {
    const map = {Level: 'Livello', 'Proficiency Bonus': 'Bonus competenza', Features: 'Privilegi', 'Spell Slots per Spell Level': 'Slot incantesimo per livello', 'Cantrips': 'Trucchetti', 'Prepared Spells': 'Incantesimi preparati'};
    document.querySelectorAll('#classtable .ve-cls-tbl th').forEach((th) => {
      const text = th.textContent.trim();
      if (map[text]) th.textContent = map[text];
    });
  };
  setTimeout(translateHeaders, 900);
  new MutationObserver(translateHeaders).observe(panel, {childList: true});

  const openClass = (row) => {
    const name = row.querySelector('span.ve-bold')?.innerText.trim();
    body.classList.add('atlas-class-open');
    if (title && name) title.innerHTML = `${name}<small>classe</small>`;
    window.scrollTo({top: 0, behavior: 'instant'});
    ensureBack();
  };
  const closeClass = () => {
    body.classList.remove('atlas-class-open');
    if (title) title.innerHTML = originalTitle;
    list.scrollIntoView({block: 'start'});
  };

  document.addEventListener('click', (e) => {
    const target = e.target instanceof Element ? e.target : null;
    const row = target?.closest('#list .ve-lst__row');
    if (row) setTimeout(() => openClass(row), 120);
  }, true);
  back.addEventListener('click', closeClass);
  appbarBack?.addEventListener('click', (e) => {
    if (body.classList.contains('atlas-class-open')) { e.preventDefault(); closeClass(); }
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && body.classList.contains('atlas-class-open')) closeClass();
  });
  new MutationObserver(ensureBack).observe(panel, {childList: true});
})();
