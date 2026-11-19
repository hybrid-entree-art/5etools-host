/* 5E ATLAS — Rimodella la home 5e.tools in stile Ruleholder, senza toccare i dati. */
(function () {
  var path = location.pathname.replace(/\/+$/, "");
  if (path && path !== "/index.html" && path !== "/") return;

  var ART = {
    "races.html": "cat-species", "classes.html": "cat-classes", "feats.html": "cat-feats",
    "backgrounds.html": "cat-backgrounds", "items.html": "cat-equipment", "spells.html": "cat-spells",
    "bestiary.html": "cat-monsters", "books.html": "cat-sources", "bastions.html": "cat-bastions",
    "glossary.html": "cat-glossary", "adventures.html": "cat-sources",
    "conditionsdiseases.html": "cat-glossary", "charcreationoptions.html": "cat-classes"
  };
  var BOOKS = [
    { id: "xphb", title: "Player's Handbook", meta: "2024 · core rules" },
    { id: "xdmg", title: "Dungeon Master's Guide", meta: "2024 · running the game" },
    { id: "xmm", title: "Monster Manual", meta: "2024 · bestiary" }
  ];

  function build() {
    var splits = [].slice.call(document.querySelectorAll(".home__split"));
    if (!splits.length || document.querySelector(".atlas-home")) return;

    var anchors = [];
    splits.forEach(function (split) {
      [].slice.call(split.querySelectorAll("a.home__btn-page")).forEach(function (a) {
        var href = a.getAttribute("href") || "";
        var label = a.querySelector(".home__lbl-page");
        anchors.push({ node: a, href: href, label: label ? label.textContent.trim() : a.textContent.trim() });
      });
    });

    var home = document.createElement("div");
    home.className = "atlas-home";
    home.innerHTML =
      '<section class="atlas-hero"><div class="atlas-hero-c">' +
      '<div class="atlas-kicker">Reference compendium · 2024 rules</div>' +
      '<h1>All the rules.<br>At your fingertips.</h1>' +
      '<p>Three core rulebooks and the full 5e.tools compendium. English source text, mobile-first.</p>' +
      '<a class="atlas-cta" href="spells.html">Search the compendium →</a>' +
      '</div></section>' +
      '<h2 class="atlas-sec">Sourcebooks · 29 chapters</h2><div class="atlas-books"></div>' +
      '<h2 class="atlas-sec">Compendium</h2><div class="atlas-grid"></div>';

    var books = home.querySelector(".atlas-books");
    BOOKS.forEach(function (b) {
      var a = document.createElement("a");
      a.className = "atlas-book";
      a.href = "books.html#" + b.id;
      a.innerHTML = '<img src="/art/cover-' + b.id + '.webp" alt="" loading="lazy"><span><strong>' + b.title + '</strong><small>' + b.meta + '</small></span>';
      books.appendChild(a);
    });

    var grid = home.querySelector(".atlas-grid");
    anchors.forEach(function (item) {
      var art = ART[item.href.replace(/^\.\//, "")] || "cat-sources";
      item.node.classList.add("atlas-card");
      item.node.style.setProperty("--card-art", "url('/art/" + art + "-bg.webp')");
      var lbl = item.node.querySelector(".home__lbl-page") || document.createElement("h4");
      lbl.className = "atlas-lbl";
      lbl.textContent = item.label;
      if (!item.node.contains(lbl)) item.node.appendChild(lbl);
      grid.appendChild(item.node);
    });

    var title = document.getElementById("page__title");
    if (title) title.innerHTML = '<span class="atlas-mark">20</span> 5E <span>ATLAS</span>';
    var sub = document.getElementById("page__subtitle");
    if (sub) sub.textContent = "5.5e reference built on 5e.tools";

    var container = document.querySelector(".container") || document.body;
    container.insertBefore(home, container.firstChild);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build);
  else build();
})();
