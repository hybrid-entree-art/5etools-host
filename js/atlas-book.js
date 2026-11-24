/* 5E ATLAS — reader chrome for the native 5e.tools book page. */
(() => {
  const body = document.body;
  const appbar = document.querySelector('.atlas-sitebar');
  const list = document.getElementById('listcontainer');
  if (!appbar || !list) return;
  body.classList.add('atlas-book');

  const title = appbar.querySelector('.atlas-sitebar-title');
  const toc = document.createElement('button');
  toc.type = 'button';
  toc.id = 'atlasTocBtn';
  toc.textContent = 'Indice';
  toc.setAttribute('aria-expanded', 'false');
  appbar.append(toc);

  const setTitle = () => {
    const parts = document.title.split(' - ');
    const chapter = parts[0] || 'Manuale';
    const book = parts[1] || '5e.tools core';
    if (title) title.innerHTML = `${chapter}<small>${book}</small>`;
  };
  const toggleToc = (force) => {
    const open = force ?? !body.classList.contains('atlas-toc-open');
    body.classList.toggle('atlas-toc-open', open);
    toc.setAttribute('aria-expanded', String(open));
    if (open) list.scrollTop = 0;
  };

  toc.addEventListener('click', () => toggleToc());
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') toggleToc(false);
  });
  list.addEventListener('click', (e) => {
    if (e.target instanceof Element && e.target.closest('a')) toggleToc(false);
  });
  new MutationObserver(setTitle).observe(document.querySelector('#pagecontent') || document.body, {childList: true, subtree: true});
  setInterval(setTitle, 1200);
  setTitle();
})();
