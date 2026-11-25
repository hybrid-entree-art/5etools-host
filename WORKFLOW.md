# Flusso di lavoro — 5E Atlas self-host

Repo: `hybrid-entree-art/5etools-host`. Branch reale: **`master`** (non `main`). Sito pubblico: `https://5etools-host.vercel.app/`. Questa è la guida operativa: `docs/VERCEL.md` contiene i dettagli dei comandi Vercel.

## 1. Cosa è Atlas (e cosa non è)

È un **clone statico self-host di 5e.tools** (versione `2.41.1` in `package.json`) con una **shell mobile Atlas** innestata sopra. Non è una riscrittura del sito:

- **Desktop** → 5e.tools nativo, senza modifiche di layout.
- **Mobile (≤767px)** → shell Atlas: navigazione bottom, dettagli a piena schermata, palette scura, tipografia e token propri.
- La root `/` serve `index.html` (core). Uno script inline in `index.html:12` fa `location.replace("atlas.html")` se `matchMedia("(max-width:767px)")` è vero. Su desktop la root resta il core. Il redirect è **client-side**: le risposte HTTP di `/` sono identiche per qualsiasi User-Agent.
- Non riscrivere parser, renderer, dati o pagine core per "sistematle": Atlas aggiunge, non sostituisce il motore.

## 2. Mappa del repo — file che contano

| Percorso | Ruolo |
|---|---|
| `index.html` | Home core 5e.tools + redirect mobile verso `atlas.html` |
| `atlas.html` | Home Atlas (solo shell, carica `js/atlas-nav.js`) |
| 54 file `*.html` | Pagine core; molte hanno la shell iniettata (CSS + `js/atlas-*.js`) |
| `css/atlas*.css` | 6 file: `atlas.css`, `atlas-nav.css`, `atlas-site.css`, `atlas-book.css`, `atlas-classes.css`, `atlas-bestiary.css` |
| `js/atlas-*.js` | 6 file: `atlas-nav.js`, `atlas-site.js`, `atlas-book.js`, `atlas-classes.js`, `atlas-bestiary.js`, `atlas-spells.js` |
| `js/render.js` | `Renderer.getMediaUrl()`: punto unico da cui passano le immagini del core |
| `js/atlas-nav.js` | Hook su `getMediaUrl` verso `IMG_CDN = https://cdn.jsdelivr.net/gh/5etools-mirror-3/5etools-img@main/`, nav mobile, Telegram |
| `sw-injector.js` | Stub intenzionale: service worker disabilitato, evita il 404 |
| `data/` | Dati 5e.tools: **non modificare a mano** |
| `vercel.json` | `framework: null`, `outputDirectory: "."`, `buildCommand: ""` |
| `.vercelignore` | Esclude `.git`, `node_modules`, `.DS_Store`, `*.log`, `Dockerfile` |
| `img/` | Vuota e in `.gitignore`: **nessuna cartella immagini da ~7 GB su Vercel** |
| `docs/VERCEL.md` | Comandi e procedure di deploy/alias |

Le immagini vengono da jsDelivr (`5etools-mirror-3/5etools-img`), non da `img/`: il core chiama `Renderer.getMediaUrl('img', …)` in `js/render.js` e `js/atlas-nav.js` riscrive quel risultato verso il CDN.

## 3. Flusso GitHub

Identità git configurata: `hybrid-entree-art <hybrid-entree-art@users.noreply.github.com>`. Remote `origin` → `https://github.com/hybrid-entree-art/5etools-host.git`.

```bash
git status --short
git fetch origin
git checkout master
git pull --ff-only origin master
git add -- path/to/file.css path/to/file.js     # mai `git add -A`
git diff --cached --check                       # obbligatorio prima del commit
git diff --cached --stat
git commit -m "descrizione breve"
git push origin master
```

Regole: un solo autore per file per evitare conflitti; niente commit di `.env*`, token o ID; push sempre su `origin master`.

## 4. Flusso Vercel (vedi `docs/VERCEL.md`)

Progetto Vercel `5etools-host` (team `hybrid-art`), CLI in `/opt/data/bin/vercel` (v65.17.0). **La Production del progetto è vecchia: conta l'alias**, non il deployment di default.

```bash
/opt/data/bin/vercel deploy -y --no-wait --archive=tgz
# attendere 10-15 secondi, poi verificare l'URL restituito
/opt/data/bin/vercel alias set <deployment-url> 5etools-host.vercel.app
curl -sI https://5etools-host.vercel.app/
```

Rollback = puntare l'alias a un deployment precedente (`vercel ls -n 20` per elencarli). Non usare `vercel --prod`: creerebbe un deployment della Production, che non è la sorgente del sito.

## 5. Test mobile/desktop e checklist pre-deploy

- Aprire `https://5etools-host.vercel.app/` a **390px**: deve finire su `atlas.html` con nav bottom. A **1440px**: deve restare il core 5e.tools.
- Verificare `curl -sI` su `/`, `atlas.html`, `book.html`: `200`, `x-vercel-cache: HIT`, HSTS presente.
- Provare almeno un deep link (`book.html#xphb` → capitolo "Introduction"), il back button e l'apertura di una scheda.
- Controllare in console errori JS e 404 di asset.
- Checklist: `git diff --cached --check` pulito; nessun segreto nel diff; `sw-injector.js` presente; immagini via CDN; nessun toggle lingua; inglese prima; target touch ≥48px; nessun cambiamento al layout desktop.

## 6. Convenzioni UI/token e cosa non toccare

- Tutti i token e le classi Atlas usano il prefisso `atlas-`: `.atlas-global-nav`, `.atlas-menu`, `body.atlas-site`, `.atlas-detail-open`. Breakpoint condiviso: `@media (max-width:767px)`.
- Mini App Telegram: `js/atlas-nav.js` carica `telegram-web-app.js` **solo** in ambiente Telegram; usa `tg.expand()`, `tg.BackButton`, `--tg-vh`. In browser normale è no-op.
- **Non toccare**: `data/`, i file core `js/parser.js`, `js/book*.js`, `js/render*.js`, `css/main.css`, `css/bootstrap.css`, le 54 pagine core se non serve innestare la shell, il comportamento desktop.
- L'autorizzazione dell'utente copre tutti i materiali usati: non escludere font/texture per motivi di licenza, ma valutarne peso e coerenza.

## 7. Problemi noti e troubleshooting

- **Home doppia**: `/` è core, `/atlas.html` è Atlas. Se su desktop appare Atlas, controllare lo script `matchMedia` in `index.html:12`.
- **`book.html#hash`**: i deep link validi funzionano; lo shell Atlas ("Indietro"/overlay) non si attiva su `book.html` perché `js/atlas-site.js` cerca `#contentwrapper`. Hash inesistenti possono richiamare `history.back()`.
- **404 asset**: se ricompaiono, verificare `sw-injector.js`, le immagini `img/**` (non presenti) e i percorsi jsDelivr.
- **`www.5etools-host.vercel.app`**: certificato non valido per quell'hostname. Usare solo la root senza `www`.
- **Cache**: `cache-control: public, max-age=0, must-revalidate`; aggiornamenti immediati ma riconvalida a ogni richiesta. `x-vercel-cache: HIT` è normale.
- **Build "building"**: vedere `docs/VERCEL.md`, sezione errori comuni.

## 8. Documentazione vs changelog

Questi due file descrivono **come si lavora** (procedure stabili). Il changelog descrive **cosa è cambiato** (date, commit, versioni). Aggiornare la documentazione quando cambia una procedura; scrivere nel changelog quando cambia il codice. Non usare la documentazione come cronologia.
