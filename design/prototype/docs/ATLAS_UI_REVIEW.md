# 5E ATLAS — UI/UX review ( Atlas prototype )

**Ambito:** review visiva e strutturale del prototipo `atlas-ux-prototype-gvnc8nu0l-hybrid-art.vercel.app`, sorgente `/opt/data/cache/scratch/atlas-ux-prototype/index.html` (788 righe). Nessuna modifica al codice: solo questo documento.

**Metodo:** Playwright (`node_modules/playwright`, browser in `/opt/data/cache/scratch/pw-browsers`), viewport 390×844 e 1440×900, route `#home`, lettore XPHB, capitolo 7 (Spells), dettaglio `Acid Splash`. Script: `/opt/data/profiles/ui-designer/cache/scratch/atlas_audit.cjs`. Screenshot: `/opt/data/profiles/ui-designer/cache/scratch/atlas-review-*.png`.

---

## Verifiche positive (da non rompere)

| Verifica | 390 | 1440 |
|---|---|---|
| Overflow orizzontale | 0 px | 0 px |
| Bottom nav / padding body | `grid` / 90 px | `none` / 0 px |
| Contrasto guscio (`--muted`, `--faint`, `--eyebrow` su `--bg`) | 11.80 / 7.90 / 9.44 : 1 | identici |
| Fonte nella scheda dettaglio | 1 × `XPHB · 2024` | 1 × |
| Errori JS (`pageerror`) | 0 | 0 |
| Barra capitolo / progresso | `Capitolo 1 di 12`, 8.33 % | identico |
| Indice | 12 voci, apre/chiude con Escape | 12 voci |

Il glow è già usato con coerenza (search, bottoni primari, barra progresso, hover card): **non va ritoccato**.

---

## Problemi ordinati per impatto

### P0 — La media query desktop contiene tutti gli stili del lettore e delle ref card

`index.html:213` apre `@media(min-width:760px){` e la `}` che lo chiude è alla riga **256**. Dentro quel blocco finiscono `.book-eyebrow`, `.book-section`, `.book-note`, `.book-list`, `.ref-card`, `.ref-stats`, `.ref-body`, `.reader-pager`, `.toc-item` (righe 228-255). Su mobile quindi **394 ref card del capitolo 7 sono senza stile**.

Evidenza (`atlas_audit.cjs`, capitolo 7):

| Proprietà | 390 px | 1440 px |
|---|---|---|
| `.ref-card` border / bg | `0px` / `rgba(0,0,0,0)` | `1px` / `rgba(255,255,255,.28)` |
| `.ref-card summary` padding | `0px` | `11px 12px` |
| `.ref-card summary` marker | `disclosure-closed` (triangolo nativo) | `none` |
| altezza `summary` | 23 px | 47 px |
| `.book-note` border-left | `0px` | `3px` |
| `.reader-pager` border-top | `0px` | `1px` |

Conseguenze testuali verificate: `firstRef` = `Acid SplashIncantesimi · XPHB` a 390 (nessun separatore, era `Acid Splash\nIncantesimi · XPHB` a 1440) e `REFOPEN` = `LivelloTrucchetto`, `Tempo di lancio1 azione`, `Gittata60 piedi` — label e valore si saldano perché `.ref-stats span{display:block}` non si applica.

**Fix:** spostare la `}` che chiude il media query dalla riga **256 alla riga 227**. Tutto il blocco 228-255 diventa base CSS, invariato su desktop. Se si preferisce esplicitare:

```css
/* base, FUORI da @media(min-width:760px) */
.ref-card{border:1px solid var(--paper-line);border-radius:10px;background:rgba(255,255,255,.28);margin:8px 0;overflow:hidden}
.ref-card summary{cursor:pointer;padding:11px 12px;display:flex;align-items:baseline;justify-content:space-between;gap:10px;list-style:none}
.ref-card summary::-webkit-details-marker{display:none}
.ref-card summary b{font:700 16px var(--book);color:var(--paper-ink)}
.ref-card summary span{font:600 11px var(--ui);color:#7a5b3a;text-align:right}
.ref-body{padding:0 12px 12px;border-top:1px solid var(--paper-line)}
.ref-stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;margin:10px 0}
.ref-stats span{display:block;font:600 9px var(--ui);text-transform:uppercase;letter-spacing:.07em;color:#7a5b3a}
.reader-pager{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:18px;border-top:1px solid var(--paper-line);padding-top:14px}
.book-note{border-left:3px solid #b8863b;background:rgba(201,178,138,.18);padding:10px 14px;margin:14px 0;border-radius:0 8px 8px 0}
```

---

### P0 — Voci dell'indice sotto il target touch

`dialog#toc` misura 354×427 px a 390. Le voci `.toc-item` (**index.html:252**, dentro il media query) misurano **29 px a 390** e **41 px a 1440**, entrambe sotto i 44 px. Nessuna voce ha `aria-current`: `active: 0` in entrambe le viewport — il capitolo corrente non è segnalato nell'indice.

```css
/* base, non nel media query */
.toc-item{min-height:44px;padding:11px 0}
.toc-item[aria-current="true"]{color:var(--amber);background:rgba(240,167,66,.10)}
.toc-item[aria-current="true"] span{color:var(--amber)}
```

Nota: il selettore `[aria-current]` richiede l'aggiunta dell'attributo in `renderTOC()` (riga 717, template dei pulsanti); è l'unico punto che non si risolve con CSS solo.

---

### P1 — Titolo della scheda dettaglio ripetuto tre volte

`DETAIL` a entrambe le viewport: `headings: ["Acid Splash","Acid Splash"]`, più il breadcrumb (`Home / Incantesimi / Acid Splash`). La fonte invece è correttamente **una sola volta** (`sourceNodes: 1`). Anche "Scheda 2024" (`#detailSubtitle`) e il pill `XPHB · 2024` comunicano la stessa informazione.

Mantenere l'h1 per l'accessibilità ma nasconderlo visivamente; eliminare il subtitle:

```css
#view-detail .page-head h1{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
#view-detail .page-head p{display:none}
#view-detail .spell-card{margin-top:0}
```

Risultato: nome una volta nel breadcrumb + una volta come h2 della scheda; edizione solo nel pill.

---

### P1 — Contrasto insufficiente nelle etichette dei metadati

Calcolo diretto dei colori del sorgente su `--paper` (`#f3e9d2`):

| Selettore | Colore | Ratio | Esito |
|---|---|---|---|
| `.stat span` (`:161`) | `#8a6a45` | **4.11 : 1** | **fallisce AA** (testo 10 px) |
| `.ref-stats span` | `#7a5b3a` | 5.14 : 1 | ok |
| `.prose` / `.paper` | `#2a2118` | 13.09 : 1 | ok |
| `.spell-card .source` | `#7a4a12` | 6.18 : 1 | ok |

```css
.stat span{color:#7a5b3a}   /* 5.14:1, passa AA */
```

Le lamentele visive sul pill "source" non sono confermate dal calcolo: 6.18:1, ok.

---

### P1 — Densità: 394 ref card in un solo capitolo

`READERCH7` a 390 e 1440: `refCards: 394`. Anche dopo il fix P0, una pagina con 394 `<details>` è pesante da scorrere e da tenere in memoria su un telefono. Consigliato limite progressivo su mobile:

```css
@media(max-width:759px){
  #readerArticle .ref-card:nth-of-type(n+13){display:none}
  #readerArticle.refs-expanded .ref-card{display:block}
}
```

Richiede un pulsante "Mostra tutte le schede (394)" che aggiunga `.refs-expanded`: **non applicare il solo CSS**, altrimenti si nasconde contenuto senza recupero.

---

### P1 — Inglese prima: la UI è ancora in italiano

Rilevato in `DETAIL` e `READERDOM`: `Home / Biblioteca / Incantesimi`, `Scheda 2024`, `LIVELLO`, `Tempo di lancio`, `Gittata`, `Capitolo 1 di 12 · Introduction: Welcome to Adventure`, e ref card `Acid SplashIncantesimi · XPHB`. La descrizione è in inglese: **lingua mista nella stessa scheda**. Il vincolo condiviso è inglese prima, senza switcher lingua. È una questione di contenuto (non di identità visiva): va risolta nei template di `renderDetail()`/`renderReader()`, non con CSS.

---

### P2 — Breadcrumb del lettore: 4 livelli che mangiano spazio

`index.html:727` produce `Home / Biblioteca / <manuale> / <capitolo>`. A 390 la `.reader-bar` inizia a y=146 px (top bar 64 px + ~82 px di breadcrumb), prima ancora della lettura. Su mobile servono solo gli ultimi due livelli:

```css
@media(max-width:759px){
  #readerCrumbs{flex-wrap:nowrap;overflow:hidden;white-space:nowrap;min-width:0}
  #readerCrumbs a,#readerCrumbs .sep{display:none}
  #readerCrumbs span[aria-current="page"]::before{content:"/";margin:0 7px;color:var(--faint)}
}
```

---

### P2 — Alcuni target restano sotto 44 px

Da sorgente: `.cat-tab` **42 px** (:93), `.filter-option` **40 px** (:132), `.pill` **32 px** (:127). `.btn`, `.chip`, `.bottom button` (64 px), `.icon-btn` sono già a posto.

```css
.cat-tab,.filter-option,.pill{min-height:44px}
```

---

### P2 — Hero mobile troppo alta, prima card lontano dal fold

A 390: `.hero-card` 358×330, prima `.book` a y=488, prima `.cat` a y=1000. L'h1 passa da 34 px (390) a 58 px (1440): la scala è corretta, ma l'altezza fissa 330 px ruba spazio ai manuali.

```css
@media(max-width:759px){.hero-card{min-height:270px}}
```

Non toccare `.hero h1`: la scala `clamp(34px,6.4vw,58px)` è coerente.

---

### P3 — Regole morte e dipendenze esterne

- `.toc-fab{display:none}` è definito due volte (`:193` e `:255`) e **nessuna regola lo mostra**: il pulsante indice funziona tramite `#tocBtn` nella reader bar. Rimuovere la regola morta o collegarla.
- `.hero-card` usa un URL `raw.githubusercontent.com` (:54) e le copertine dei tre manuali sono remote: senza rete l'hero perde l'artwork. Non è un difetto di gerarchia, ma va segnalato per l'export/affidabilità.

---

## Cosa NON cambiare

- Identità dark + pergamena, palette amber/teal, font Modesto/Mulish/Lora: funzionano e sono coerenti tra 390 e 1440.
- Effetti glow: già dosati e distribuiti con criterio (focus ring, search, primari, progresso, hover).
- Struttura a 3 manuali + 11 categorie in home e navigazione del lettore da copertina: gerarchia corretta.
- Nessun commit e nessuna modifica a `index.html` in questa review.
