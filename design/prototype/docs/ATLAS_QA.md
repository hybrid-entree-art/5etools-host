# QA — prototipo 5E ATLAS (UX/UI)

Data: 2026-11-21 · Ruolo: @critique-reviewer · Solo verifica: **nessuna modifica** a `index.html`, `data/`, script, nessun commit.

## Metodo

- Preview: `https://atlas-ux-prototype-gvnc8nu0l-hybrid-art.vercel.app/` (HTTP 200). Sorgente: `/opt/data/cache/scratch/atlas-ux-prototype/`.
- La copia locale di `index.html` è identica al preview eccetto il tag `<script async … feedback.js>` iniettabile da Vercel (verificato con `diff -u`): 53.646 B locali vs 53.809 B remoti.
- Viewport: **390×844** e **1440×900** su copia locale servita via `python3 -m http.server 8898`; cross-check funzionale sul preview remote (394 reference in Chapter 7, 0 errori console).
- Errori JS catturati prima dell'hydration (`Page.addScriptToEvaluateOnNewDocument`). Selettori usati: `.book[data-book]`, `.top-nav`/`.bottom`, `#detailBody .spell-card .source`, `#detailSubtitle`, `#readerArticle details.ref-card`, `#readerSideLinks a`, `.table-wrap`.

## Esito verifiche

| # | Verifica | Esito | Prova |
|---|---|---|---|
| 1 | Fonte una sola volta nella scheda incantesimo/mostro | **PASS** | `#detailBody .spell-card` → `XPHB · 2024` **1×** per *Acid Splash*; `XDMG · 2024` **1×** per *Avatar of Death*. `#detailSubtitle` = `Trucchetto · Evocazione` / `Media Non morto · GS —` (senza fonte). Conta sull'intero `#view-detail`: 1. |
| 2 | Nessuna voce Compendio / Lettore nella navigazione | **PASS** | `nav a, nav button` → `Home`, `Biblioteca`, `Menu` (e `Home`, `Biblioteca` nella bottom bar); regex `/compendio|lettore/i` sul testo di `nav` → `false`. |
| 3 | Tre libri della home → lettore corretto | **PASS** | Click su `.book[data-book="XPHB"]` → eyebrow `Manuale del Giocatore · 2024`, h1 `Introduction: Welcome to Adventure`; `XDMG` → `Manuale del Master · 2024` / `Chapter 1: The Basics`; `XMM` → `Manuale dei Mostri · 2024` / `How to Use a Monster`. Breadcrumb coerente. |
| 4 | PHB Chapter 7: Spells | **PASS** | 394 `details.ref-card` = **391 `Incantesimi` + 3 `Glossario`**; primo ref espanso con `summary.click()` → `open=true`, `.ref-body` mostra statistiche e testo. |
| 5 | Contenuti PHB Ch.3–6 | **PASS** | Ch.3 `12 Classi + 48 Sottoclassi` (60); Ch.4 `16 Background + 10 Specie` (26); Ch.5 `77 Talenti`; Ch.6 `123 Equipaggiamento`. |
| 6 | XDMG Ch.7 / XMM A–Z | **PASS** | XDMG Chapter 7: Treasure → **584 `Oggetti magici`**; XMM `Monsters A to Z` → **505 `Mostri`**. |
| 7 | Nessun overflow orizzontale | **FAIL a 390px** | 1440px: `clientWidth=1425`, `scrollWidth=1425` ovunque. A 390px: XPHB Ch.3 `scrollWidth=637` (client 390), XPHB Ch.6 `scrollWidth=613` (client 390); `visualViewport.width=390` ma `innerWidth` si espande. Dettagli in P1-1. |

Console: `window.__qaErrs = []` su home, catalogo, dettaglio e lettore, sia locale che preview. Tabelle: 16 `.table-wrap` in Ch.6 con `overflow-x:auto`, `clientWidth=320`, scroll interno fino a 605px — **non** causano overflow di pagina.

## Problemi

### P0
Nessuno.

### P1-1 — Overflow orizzontale su XPHB Chapter 3 e Chapter 6 a 390px

- **Selettori**: `aside.reader-side` (`index.html:370-372`), figli `#readerSideLinks a` (generati da `renderReader()`, `index.html:714`), regola `.reader-side a{display:block;…}` chiusa dentro `@media(min-width:760px)` (`index.html:208-222`).
- **Riproduzione**:
  1. Apri il prototipo a 390×844 (preview o `http://127.0.0.1:8898/index.html`).
  2. Tocca `.book[data-book="XPHB"]` dalla home.
  3. Apri l'indice e scegli `Chapter 3: Character Classes` (`[data-toc-chapter="3"]`).
  4. Verifica: `document.documentElement.clientWidth = 390`, `scrollWidth = 637`, `innerWidth = 637`, `visualViewport.width = 390`; i link `Rogue` (right 430), `Sorcerer` (487), `Warlock` (545), `Wizard` (596), `Indice completo · Sottoclassi` (637) escono dal viewport.
  5. Ripeti con `[data-toc-chapter="6"]` (Chapter 6: Equipment): `scrollWidth = 613`; link overflow `Loading` (435), `Range` (480), `Reach` (524), `Thrown` (577), `Two-Handed` (613).
- **Causa**: sotto i 760px non esiste una regola per `#readerSideLinks a`, quindi le `<a>` restano `inline` e si susseguono in orizzontale dentro `.reader` (`grid-template-columns:1fr`, `index.html:173`).
- **Fix suggerito**: spostare `.reader-side a{display:block;padding:7px 0;border-bottom:1px solid var(--line);…}` fuori dal media query (o aggiungere una regola mobile equivalente), e impostare `.reader-side{min-width:0;overflow-wrap:anywhere}`.
- **Impatto**: viola il requisito 7; l'utente può panning orizzontale solo in questi due capitoli. A 1440px non si verifica.

### P2-1 — Indice laterale troncato a 18 sezioni

- **Selettore**: `#readerSideLinks a`, `index.html:714` (`.slice(0,18)`). In Chapter 7: Spells ci sono **56** `.book-section[id]` ma solo **18** link nell'indice (ultimo: `Somatic (S)`).
- **Mitigazione presente**: il dialogo TOC completo (`#tocList`) resta disponibile. Non bloccante; valutare "Mostra tutte le sezioni" o uno scroll interno.

### P2-2 — Artefatto ambientale (escluso dai difetti)

Il titolo `🐴 5E ATLAS — prototipo UX/UI` comparso in alcune sessioni browser **non è presente** in `index.html` (grep: 0 occorrenze) né nell'HTML servito dal preview (`curl … | grep -oE '<title>[^<]*</title>'`). È un artefatto della sessione driver, non del prototipo: non è conteggiato come difetto.

## Gate

6 verifiche su 7 PASS. Il fallback è una sola regressione P1 (overflow a 390px in due capitoli del PHB): **no-promuovi finché P1-1 non è corretto** e poi ripetere la verifica 7 a 390×844.
