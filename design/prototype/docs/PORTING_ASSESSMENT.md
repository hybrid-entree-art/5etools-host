# PORTING ASSESSMENT — Atlas dentro 5e.tools vs Atlas standalone

Analisi in sola lettura. Nessun repository, file sorgente o file del prototipo è stato
modificato; unico artefatto creato: questo memo.

## Domanda

Conviene portare le schermate del prototipo Atlas dentro il clone self-hosted di
5e.tools (`/opt/data/5etools-host`), oppure mantenere Atlas come frontend standalone
che consuma dataset generati?

## Evidenze ispezionate

### 5e.tools self-hosted

| Aspetto | Misura verificata | Comando / fonte |
|---|---|---|
| Pagine HTML | **56** file `.html` alla radice, ognuna con propri `<link>`/`<script>` | `find . -maxdepth 1 -name '*.html' | wc -l` |
| JavaScript | **225** file in `js/` (547 `.js` totali nel repo); `render.js` = 18.488 righe / 630 KB, `listpage.js` = 2.856 righe / 90 KB | `wc -l js/render.js js/listpage.js` |
| CSS/SCSS | **32** CSS compilati (**548 KB** totali; `main.css` 187 KB minificato, `fontawesome.css` 160 KB, `bootstrap.css` 49 KB) + **29** SCSS / ~19.701 righe sorgente | `du -ch css/*.css`, `cat scss/*.scss | wc -l` |
| Temi | `js/styleswitch.js` gestisce **5** temi (`auto`, `day`, `night`, `nightAlt`, `nightClean`) con classi globali `ve-night-mode*` e 3 chiavi `localStorage` | `head -50 js/styleswitch.js` |
| Routing | hash-based in `js/navigation.js`, `js/listpage.js`, `js/render.js`, `js/hist.js`, ecc. — non è una SPA con router proprio | `grep -rl "location.hash" js/*.js` |
| Dipendenze | librerie vendored in `lib/` (elasticlunr, localforage, lzma, ace, peerjs, dom-to-image…), Bootstrap + FontAwesome; build con Node **>=24**, sass, esbuild, workbox (service worker), handlebars, jest | `package.json`, `ls lib/` |
| Dati | **119 MB**, **543** file JSON in `data/` | `du -sh data/`, `find data -name '*.json' | wc -l` |

### Prototipo Atlas

| Aspetto | Misura verificata |
|---|---|
| Struttura | **un solo** `index.html` di 53 KB: `<style>` inline alle righe 7-255, `<script>` inline alle righe 406-786. Nessun framework, nessuna dipendenza npm reale (`package.json` è uno stub). |
| Dati | 2 dataset generati e già inclusi: `data/core-2024.json` 1,32 MB (1.916 voci) + `data/books-2024.json` 1,42 MB = **2,74 MB totali**. |
| Routing | hash proprio (`#spells`, `#reader`, `history.replaceState`), `fetch()` dei due JSON, `<dialog>` per filtri/TOC/menu, bottom-sheet TOC. |
| Font | 5 `.woff2` self-hosted (~164 KB) in `fonts/`. |
| Generazione | `scripts/build-core-data.py` e `build-books-data.py` leggono il checkout locale `../../5etools-host/data` **solo in sviluppo**; il README dichiara esplicitamente che per la preview il clone non serve. |
| Deploy | preview Vercel statica, già online. |

## Rischi concreti del porting

1. **Il tentativo è già fallito una volta, con evidenza nel git.** Il commit
   `2604243 "[ATLAS] Tema scuro ambra/teal sul self-host 5e.tools"` ha modificato
   **56 file HTML** per aggiungere un `<link rel="stylesheet" href="/atlas-theme.css">`
   (52 righe di CSS) sopra Bootstrap+`main.css`. Il risultato è stato annullato da
   `d57d707 "[RESET] Rimosso tema ibrido: self-host 5e.tools pulito"`, che ha rimosso
   `atlas.css` (68 righe), `atlas.js` (76 righe), font e arte. Il commit intermedio
   `139b37d` aveva ricostruito una home "in stile Ruleholder" sempre dentro il clone.
   Il problema non era il gusto ma l'_architettura_: due set di componenti sovrapposti.
2. **Divieto esplicito nel processo.** `WORKFLOW.md`: «Nessun CSS che nasconde
   un'interfaccia per metterne sopra un'altra: si riscrive un solo set di componenti.»
   Un porting "a strati" è quindi fuori regola per costruzione; resta solo la riscrittura
   integrale dei componenti 5e.tools.
3. **Superficie di riscrittura enorme.** Per avere parità visuale Atlas dentro 5e.tools
   andrebbero riscritti 56 template HTML, 32 CSS (548 KB), 19.701 righe SCSS e i
   renderer (`render.js` 18.488 righe, più `js/render-*.js`), mantenendo 5 temi,
   service worker, filtri per catalogo (`js/filter-*.js`) e le dipendenze vendored.
   Ogni aggiornamento upstream di 5e.tools (v2.41.1) può confliggere con le modifiche.
4. **Conflitto con i vincoli prodotto.** 5e.tools è Inglese+ Russo con selettore tema;
   Atlas richiede inglese prima, **nessuno switcher lingua**, glow selettivo e
   miniature mobile-first. I global styles `ve-*` e le classi tema entrano in conflitto
   con i token ATLAS (`--bg`, `--accent`, `--glow`).
5. **Costo di distribuzione.** Portare il clone in produzione significa servire 119 MB
   di JSON,Node >=24 per il build, sass/workbox e un service worker da rigenerare: un
   deployment molto più pesante e fragile di 2,74 MB di JSON statici.
6. **Regressione funzionale.** Il clone copre 56 pagine e decine di tool (initiative
   tracker, convertitore, DM screen, generatore incontri); toccarne il CSS globale
   rischia di rompere funzioni estranee al percorso Atlas senza che sia necessario.

## Parti riusabili (senza portare l'interfaccia)

- **I dati, non il frontend**: `data/*.json` di 5e.tools come *sorgente* degli
  generatori (`scripts/build-core-data.py`, `build-books-data.py`), già funzionanti.
- **La semantica dei tag `{@…}` e dei riferimenti**: il parser/cleanup dei dataset
  generati (14.435 `{@spell}`, 11.429 `{@damage}`, 7.342 `{@condition}`) è già
  implementato lato generatori; va mantenuto e testato, non riscritto in 5e.tools.
- **Gli ID e le convenzioni dei libro/capitoli** (`book-xphb`, `book-xdmg`, `book-xmm`)
  e le lookup generate (`gendata-*-lookup.json`) per risolvere slug e cross-link.
- **Asset curati**: copertine e arte categorie già selezionate (WebP leggere) e i 5
  font self-hosted: riusabili così come sono nel frontend standalone.
- **Le idee di UX dell'upstream** (ricerca globale, filtri per fonte, navigazione per
  hash) come ispirazione, non come codice da innestare.

## Stima dello sforzo

| Opzione | Sforzo | Note |
|---|---|---|
| Overlay CSS sopra 5e.tools | 2-3 giorni-uomo | ** già tentato e revertito**; qualità insufficiente, vieta il WORKFLOW.md — da scartare |
| Porting vero (riscrittura componenti dentro 5e.tools) | **40-80 giorni-uomo** (8-16 settimane) | 56 HTML + 548 KB CSS + 18,5k righe renderer + 5 temi + SW; più manutenzione continua sugli update upstream |
| Standalone (consolidare il prototipo esistente) | **10-20 giorni-uomo** (2-4 settimane) | refinements su dataset/generator, parità route e deep link, localizzazione immagini remote, QA 320/390/1440 e WCAG, export/deploy |

La stima standalone presume che il prototipo resti un file statico e che i generatori
restino l'unico ponte verso 5e.tools.

## Raccomandazione finale

**Standalone. Non portare le schermate Atlas dentro il clone 5e.tools.**

Motivazione in una frase: il porting obbligherebbe a riscrivere l'intera interfaccia
upstream (56 pagine, 548 KB di CSS, 18,5k righe di renderer) per poi ottenere un
prodotto identico a quello che il prototipo già realizza con 2,74 MB di dati generati,
ed è esattamente il percorso che ha già prodotto l'incidente dei temi mischiati.

Il clone 5e.tools resta uno **strumento di sviluppo** (sorgente dei dati e dei generatori),
non una dipendenza runtime né la base del sito pubblico.

## Implicazione: "dati solo su GitHub, niente clone locale in produzione"

- La sorgente autorevole resta il repository GitHub (`5etools-mirror-3/5etools-src` /
  il fork self-hosted), usato **offline** dai generatori per produrre i due dataset.
- In produzione viaggiano solo artefatti statici versionati: `core-2024.json`,
  `books-2024.json`, font e WebP curate. Nessun `node`, nessun `sass`, nessun service
  worker, nessun checkout da 119 MB sul server: riduzione di circa **43×** del peso
  dei dati distribuiti (119 MB → 2,74 MB).
- I generatori possono girare in CI o in locale e fare commit dei dataset aggiornati;
  il frontend non fa fetch verso 5e.tools e non dipende da servizi terzi per i dati.
- Da correggere prima della promozione: il prototipo referenzia ancora immagini remote
  (`media.ruleholder.com`, `raw.githubusercontent.com/5etools-mirror-3/...`). Vanno
  convertite in WebP locali per rispettare davvero il principio "solo GitHub, zero
  dipendenze esterne a runtime".
- Il vincolo "nessuno switcher lingua" è già rispettato nel prototipo (`<html lang="it">`
  è un dettaglio del mockup: il contenuto resta inglese-first); il tema Atlas non
  deve ereditare `styleswitch.js` né le classi `ve-night-mode*`.
