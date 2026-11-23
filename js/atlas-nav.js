/* 5E ATLAS — single source for the mobile bottom navigation. */
(() => {
  const path = location.pathname.split('/').pop() || 'atlas.html';
  const infer = path === '' || path === 'atlas.html' || path === 'index.html'
    ? 'home'
    : path.replace(/\.html$/, '');
  const page = document.body.dataset.atlasPage || infer;
  const items = [
    {key: 'home', href: 'atlas.html', label: 'Home', icon: '<path d="m4 11 8-7 8 7v9a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1z"/>'},
    {key: 'spells', href: 'spells.html', label: 'Incantesimi', icon: '<path d="m12 3 1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/>'},
    {key: 'bestiary', href: 'bestiary.html', label: 'Mostri', icon: '<path d="M4 8c3-3 6-3 8 0 2-3 5-3 8 0v9c-3-2-6-2-8 0-2-2-5-2-8 0z"/>'},
    {key: 'classes', href: 'classes.html', label: 'Classi', icon: '<path d="M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z"/><path d="M9 12h6M12 9v6"/>'},
    {key: 'items', href: 'items.html', label: 'Oggetti', icon: '<path d="M4 8h16v11a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1z"/><path d="M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M4 13h16"/>'},
    {key: 'search', href: 'search.html', label: 'Cerca', icon: '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>'},
  ];

  document.querySelectorAll('.atlas-bottom, .bottom').forEach((el) => el.remove());

  const nav = document.createElement('nav');
  nav.className = 'atlas-global-nav';
  nav.setAttribute('aria-label', 'Navigazione mobile');
  nav.innerHTML = items.map((item) => `
    <a href="${item.href}"${item.key === page ? ' aria-current="page"' : ''}>
      <svg viewBox="0 0 24 24" aria-hidden="true">${item.icon}</svg>
      <span>${item.label}</span>
    </a>`).join('');
  document.body.append(nav);
  document.body.classList.add('atlas-nav-on');
})();
