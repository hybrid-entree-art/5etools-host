# CATALOG UI SPEC — 5E ATLAS (mobile-first)

Stato: **solo specifica**. Nessun file CSS/TSX modificato. Fonti lette:
`IDENTITY.md`, `src/app/atlas.css`, `src/app/page.tsx`, `src/app/books/[id]/page.tsx`.
Coerente con il lettore ATLAS esistente (`atlas.css:65-88`) e con la palette
slate/ambra/teal di `IDENTITY.md:9-23`.

## 1. Token da usare

Usare **solo** i token già definiti in `atlas.css:8-14`; non introdurre nuovi esadecimali.
Derivazioni ammesse con `color-mix(in srgb, …)` sui token esistenti.

| Token | Valore | Uso nei cataloghi |
|---|---|---|
| `--bg` | `#0b0f14` | fondo pagina, testo su pill ambra |
| `--surface` | `#141a21` | card di lista/dettaglio |
| `--surface2` | `#1b232c` | header tabella, chip attiva, inset |
| `--line` | `rgba(182,194,204,.16)` | bordi card, separatori, righe tabella |
| `--ink` | `#eef3f6` | titoli e testo primario |
| `--ink2` | `#b6c2cc` | meta, sottotitoli, celle secondarie |
| `--ink3` | `#8a9aa8` | contatori, kicker, testo inattivo |
| `--accent` | `#f0a742` | ambra: badge, link, pill attiva, focus |
| `--accent2` | `#5fd0c0` | teal: **solo** secondo accento (inset, tag tipo) |
| `--glow` | `rgba(240,167,66,.20)` | alone, solo su accenti (§7) |
| `--radius` | `14px` | card; `--r-sm:8px` per badge/pill |
| `--gutter` | `clamp(16px,4vw,32px)` | 16px a 390px |
| `--touch` | `44px` | altezza minima di ogni target |

Token derivati consigliati (da aggiungere in futuro, non ora):
`--cat-row-min:88px`, `--cat-thumb:56px`, `--cat-badge-bg:color-mix(in srgb,var(--accent) 14%,var(--surface))`.

## 2. Gerarchia tipografica (Modesto / ModestoCondensed / Mulish / Lora)

Font già self-hosted in `atlas.css:4-7`; mantenere Space Grotesk per la UI globale
(brand, hero, barra — `atlas.css:1,12`) e usare i quattro font del lettore così:

| Font | Ruolo | Dove | Misura mobile (390px) |
|---|---|---|---|
| **ModestoLocal** | display serif "di libro" | titolo libro, `h2.sec-title`, `h4` inset, titoli sezione dettaglio | 28–36px / 1.12, `700` |
| **ModestoCondLocal** | titoli compressi | `chap-title`, intestazioni di colonna catalogo, numeri di livello/CR | 22–28px / 1.12, `700` |
| **MulishLocal** | UI di lettura e dati | meta, TOC, badge, caption tabella, `dt`, `dd` brevi, filtri | 14–16px, `500/600/700` |
| **LoraLocal** (`--book`) | corpo di lettura | paragrafi lunghi, descrizioni entità | **17px / 1.65**, `400` |

Regola: **Modesto = titolo, Mulish = dato, Lora = prosa**. Non usare Modesto per il
corpo e non usare Lora per label/UI. Nessun testo sotto 16px tranne kicker
uppercase non essenziali (che restano 16px per coerenza con il lettore).

## 3. Card di lista (catalogo)

A 390px: **una colonna, riga intera** — non la griglia a 2 colonne di
`atlas.css:61-62`. Struttura:

```
<a class="cat-row" href="#/entity/{cat}/{i}">     /* display:grid; min-height:88px;
                                                    grid-template-columns:56px 1fr auto */
  <img class="cat-row__thumb" loading="lazy" alt="">   /* WebP 56px, aria-hidden */
  <span class="cat-row__body">
    <span class="cat-row__title">Name</span>            /* Modesto 18px/1.2, --ink */
    <span class="cat-row__meta">Level 3 · Evocation</span> /* Mulish 15px, --ink2 */
  </span>
  <span class="cat-badge">Spell</span>                  /* Mulish 700, 13→16px,
                                                          --accent su --cat-badge-bg */
</a>
```

- Bordo `1px solid var(--line)`, `border-radius:var(--radius)`, `background:var(--surface)`,
  padding `12px var(--gutter)`; gap 12px; separatore tra righe con `var(--line)`.
- Tutta la riga è il target (≥44px; in pratica 88px). Nessun pulsante annidato.
- Stati: `:hover` → `border-color:var(--accent)` + glow controllato (§7);
  `:active` → `background:var(--surface2)`; `:focus-visible` → §6.
- 391/503/584 voci: usare `content-visibility:auto` e `contain-intrinsic-size:88px`
  sulle righe fuori schermo; `loading="lazy"` sulle thumb. Nessuna virtualizzazione
  a mano necessaria a 390px.
- Variante senza immagine: `grid-template-columns:1fr auto`, stessa altezza minima.

## 4. Card di dettaglio (entità)

```
<article class="entity">
  <header class="entity__head">          /* sticky sotto la barra: top:64px */
    <a class="back" href="#/catalog/{cat}">← Back</a>   /* target 44px */
    <h1 class="entity__title">Acid Splash</h1>          /* Modesto 32px/1.1 */
    <p class="entity__meta">Evocation · Cantrip</p>     /* Mulish 15px, --ink2 */
    <span class="cat-badge cat-badge--teal">Spell</span> /* --accent2, mai dominante */
  </header>
  <figure class="entity__art">…webp lazy…<figcaption>Mulish 15px --ink3</figcaption></figure>
  <dl class="entity__stats">             /* grid 2 col a 390px; dt Mulish 14/--ink3,
                                            dd ModestoCond 18/--ink */
    <dt>Casting Time</dt><dd>1 action</dd> …
  </dl>
  <section class="entity__body">          /* Lora 17/1.65 --ink, misura max 68ch */
    <h2 class="sec-title">Description</h2>  /* Modesto 24px --accent */
    <p>…</p>
    <aside class="inset"><h4>…</h4>…</aside> /* teal --accent2, bordo sinistro 3px */
    <div class="table-wrap"><table>…</table></div>
    <a class="rh-ref-pill">…</a>            /* riferimenti inline come pill */
  </section>
</article>
```

- Ordine su telefono: titolo → badge/meta → stats → prosa → tabelle → riferimenti.
- `dl` a 2 colonne con `gap:12px`; ogni coppia ha sfondo `var(--surface)` e bordo
  `var(--line)`. Niente griglie a 3+ colonne sotto 768px.
- Il teal `--accent2` compare al massimo in un badge e negli `inset`: mai come
  sfondo di pagina o titolo principale.

## 5. Tabelle mobile-first

Eredita `.table-wrap` / `.reader-body table` (`atlas.css:83-88`) senza stravolgerli:

- `.table-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%}`;
  a 390px con `--gutter:16px` lo spazio utile è `358px`: impostare
  `table{width:100%;min-width:356px}` così **non c'è scroll orizzontale a 390px**.
  Sotto 356px (320px) lo scroll resta come fallback.
- `th,td{padding:10px 12px;font:500 15px/1.45 'MulishLocal',var(--ui);
  text-align:left;vertical-align:top}` — 15px per le celle, 16px minimo per il
  testo libero (evita lo zoom automatico di iOS sugli input).
- `th{background:var(--surface2);color:var(--ink)}`;
  `tbody tr:nth-child(even){background:color-mix(in srgb,var(--ink) 3%,transparent)}`.
- `caption{font:700 16px 'ModestoLocal',var(--book);color:var(--accent);text-align:left}`.
- Pattern per tabelle a molte colonne (statistiche mostro): trasformare in
  **schede impilate** con `td::before{content:attr(data-label)}` (richiede
  `data-label` nel renderer, futuro intervento TSX — non in questa fase).
- Nessun glow su celle o righe: il contrasto resta strutturale, non luminoso.

## 6. Focus ring e target touch

- Mantenere **identico** `atlas.css:20`:
  `:focus-visible{outline:2px solid var(--accent);outline-offset:2px;
   box-shadow:0 0 0 4px var(--glow)}`.
  Non usare `outline:none` altrove; il ring va esteso a `.cat-row`, `.cat-badge` quando
  interattivo, `.back`, chip filtro, stepper e icone TOC.
- Ogni elemento interattivo: `min-height:var(--touch);min-width:var(--touch)`.
- **Da correggere** (segnalato, non modificato): `.book .go` è `26×26px`
  (`atlas.css:47-48`) → renderizzarlo `pointer-events:none` o portarlo a 44px;
  `.search input` è `15px` (`atlas.css:37`) → 16px; `.reader-toc summary` è già
  `min-height:var(--touch)` (`atlas.css:71`) → da replicare nelle righe catalogo.

## 7. Uso del glow (controllato)

Il glow resta, ma **solo sugli accenti**:

| Ammesso | Non ammesso |
|---|---|
| `:focus-visible` (ring 4px) | corpo del testo, paragrafi Lora |
| chip/pill attive e stepper | celle di tabella, `dt/dd` |
| hover/focus di card e `.mark` | sfondi di pagina, `.hero` |
| barra di progresso lettore | testo `--ink2/--ink3` |
| badge ambra | badge teal (usa bordo, non alone) |

Usare sempre `var(--glow)` (mai rgba scritti a mano); limite `box-shadow:0 0 22px`
per le card, `0 0 0 4px` per il focus. Rispettare `prefers-reduced-motion`
(`atlas.css:64`): niente animazioni dell'alone, solo cambio istantaneo.

## 8. Contrasto verificato (calcolato, non stimato)

Rapporti WCAG su `--bg #0b0f14`, `--surface #141a21`, `--surface2 #1b232c`:

| Testo | su bg | su surface | su surface2 |
|---|---|---|---|
| `--ink` | 17.19 | 15.66 | 14.20 |
| `--ink2` | 10.60 | 9.65 | 8.75 |
| `--ink3` | 6.65 | 6.06 | 5.49 |
| `--accent` | 9.44 | 8.60 | 7.79 |
| `--accent2` | 10.31 | 9.40 | 8.52 |

Tutti ≥4.5 (AA testo normale). Su pill ambra usare **`--bg`** (9.44), mai `--ink`
(1.82 → fallisce). `--line` resta solo decorativo.

## 9. Cinque regole chiave

1. **Una colonna a 390px**: righe catalogo full-width da 88px, non griglie a 2 colonne.
2. **Gerarchia netta**: Modesto = titoli, ModestoCond = titoli compressi/dati,
   Mulish = UI e metadati, Lora = prosa a 17px/1.65; Space Grotesk resta alla UI globale.
3. **Glow solo sugli accenti** (`var(--glow)`), mai su testo o tabelle; focus ring
   `outline 2px --accent` + `box-shadow 0 0 0 4px --glow` identico al lettore.
4. **44px minimo** su ogni target, con `.book .go` (26px) e input 15px da correggere;
   input a 16px per evitare lo zoom iOS.
5. **Tabelle leggibili senza scroll a 390px**: `min-width:356px` in 358px utili,
   header `--surface2`, righe alternate, caption Modesto ambra; stacking solo sotto 356px.
