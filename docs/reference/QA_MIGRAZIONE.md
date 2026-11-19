# QA — migrazione ATLAS (5E ATLAS)

Data: 2026-11-19 · Ruolo: @critique-reviewer · Branch: `main` (solo verifica; nessuna modifica a `.tsx`/`.css`)

## Metodo e stato del server

- Server richiesto `http://127.0.0.1:3000`: attivo (`next-server v16.4.6`, avviato 12:51:14), HTTP 200 su tutte le route. **Serve però un build precedente ai commit `b6a0abb` (12:51:51) e `178a61f` (12:54:16)**: non applica il default "2024 core" ora presente in HEAD.
- Per verificare anche HEAD ho eseguito `npm run build` (12:57, PASS) e avviato un secondo server non invasivo su **porta 3001** (`npm run start -- -p 3001`), senza fermare quello su 3000.
- Browser Chrome driver: viewport **390×844** e **1440×900**, cache-buster `?v=…` su ogni navigazione, 4 pagine (`/spells`, `/classes`, `/books/xphb`, `/books/xphb?ch=2`) su entrambe le porte.
- Errori JS intercettati prima dell'hydration (`Page.addScriptToEvaluateOnNewDocument` → `window.__qaErrs`), russo via `/[\u0400-\u04FF]/` su `innerText`, overflow via `documentElement.scrollWidth` vs `innerWidth`.

## Risultati

| Verifica | :3000 (build vecchio) | :3001 (HEAD) | Esito |
|---|---|---|---|
| Errori JS / console | `[]` su 4 pagine × 2 viewport | `[]` | PASS |
| Testo russo | 0 match | 0 match | PASS |
| Overflow orizzontale | 390px: `scrollWidth=390`/`iw=390`; 1440px: 1425/1440 (scrollbar) | identico | PASS |
| **Conteggio spells (default)** | **1,038 of 1,038** (lede "1,038 … including 391") | **391 of 1,038 spells · 2024 core** | FAIL su :3000, PASS su HEAD |
| **Conteggio classes (default)** | **43 of 43** | **12 of 43 classes · 2024 core** | FAIL su :3000, PASS su HEAD |
| Ricerca `fireball` | 4 risultati (2 solo attivando a mano "2024 core") | **2 risultati · 2024 core**, 2 card corrette (`Delayed Blast Fireball`, `Fireball`) | PASS su HEAD |
| Stepper lettore | click `Next`: `?ch=1` → `?ch=2`, `.chap-title` `Introduction: Welcome to Adventure` → `Chapter 1: Playing the Game` | idem | PASS |
| TOC bottom sheet | `<summary class="atlas-sheet__btn">Contents · 12 chapters</summary>` in `<details>`; `.atlas-sheet__panel` `position:fixed`; open/close verificato (`details.open` true→false) | idem | PASS (nota D3) |
| Font Modesto / Mulish | reader: `modesto.woff2`, `modesto-condensed-bold.woff2`, `mulish-400-800-latin.woff2`, `lora.woff2` HTTP 200, `document.fonts.check = true/true`; catalogo: solo `space-grotesk.woff2` | idem | PARZIALE (D2) |
| Tabelle | 13 tabelle su `?ch=2`, tutte in `div.table-wrap` con `overflow-x:auto` (390px: `sw=460 > cw`), pagina non overflow | idem | PASS |
| `npm run build` | — | `✓ Compiled successfully in 720ms`, TS `3.4s`, 23/23 pagine, 0 errori | **PASS** |

## Difetti

### D1 — P1 · Griglia catalogo non segue il filtro (chiavi React duplicate)

- **Evidenza (ripromossa anche su HEAD)**: disattivando il filtro default "2024 core" (vista *all sources*) e cercando `fireball`, il contatore dice **"4 of 1,038 spells · all sources"** ma la griglia mostra **23 card** (Acid Splash, Aid, Alarm … Fireball) invece di 4. Attivando "2024 core" tutto è corretto (2 contatore / 2 card), perché lì le chiavi non collidono.
- **Causa**: `src/app/components/catalog-data.ts:173` → `id: slug(spell.name)` senza source né suffisso di dedup. Corpus `src/data/spells/*.json`: **1.038 spell, 651 nomi unici, 387 nomi duplicati** (Acid Splash, Aid, Alarm, Fireball, Antimagic Field…). Chiavi duplicate → riconciliazione React lascia card obsolete nel DOM. `loadClasses` gestisce correttamente il caso (righe 235-240: prefisso source + suffisso), infatti `/classes` mostra 12/12 card.
- **Effetto**: risultati non pertinenti accanto a un contatore corretto; nessun errore console nella build di produzione.
- **Fix suggerito** (non applicato): allineare `loadSpells` a `loadClasses`: `let id = slug(spell.name); if (!CORE_2024.has(source)) id = source.toLowerCase()+'-'+id;` più suffisso progressivo per collisioni residue, mantenendo id stabili tra build.

### D2 — P2 · Build servito su :3000 non aggiornato

- Server avviato 12:51:14, commit del default "2024 core" alle 12:54:16: su :3000 i conteggi appaiono 1.038/43 invece dei richiesti 391/12. Su :3001 (HEAD) sono corretti. Non è un difetto del codice sorgente, ma della distribuzione: **riavviare `next start` dopo il build** prima della promozione.

### D3 — P2 · Font brand non usati nelle pagine catalogo

- Su `/spells` e `/classes` viene richiesto solo `space-grotesk.woff2`; `document.fonts.check('16px ModestoLocal')` = false. Sul reader Modesto/Mulish sono `loaded` (HTTP 200, file presenti in `public/art/fonts/`).
- Causa: `src/app/components/catalog.css` usa solo `var(--ui)`; Modesto/Mulish sono referenziati in `atlas.css` (`.book-title`, `.reader-*`, `.chap-title`) e `books/books.css`. Se la typography di sistema deve essere globale, aggiungere l'uso anche al catalogo.

### D4 — P2 · TOC sheet senza semantica di dialog

- Il pannello fixed è `<details>/<summary>`: `role="dialog"` assente, nessun `aria-modal`, focus non intrappolato. Fix suggerito: aggiungere ruoli dialog + Escape/focus trap, oppure accettare e documentare il pattern `<details>`.

## Nota metodologica (non difetto)

Il prefisso `🐴` visto in `document.title` in alcune navigazioni driverate **non è presente** nell'HTML servito (`curl -s … | grep -oE '<title>[^<]*</title>'` → `<title>Spells · 5E ATLAS</title>`) né nei sorgenti/chunk build: artefatto della sessione browser, escluso dai difetti. Una seconda sessione browser isolata non riusciva a caricare le pagine, quindi le misure provengono dalla sessione funzionante, con HTTP verificato a parte via `curl`.

## Gate

Build **PASS**; QA su HEAD: 1 difetto P1 (D1) + 3 P2. Il server richiesto su :3000 è **stale** (D2): per la verifica ufficiale usare il build HEAD. Consigliato **no-promuovi finché D1 non è corretto**; decisione finale a Hermes.
