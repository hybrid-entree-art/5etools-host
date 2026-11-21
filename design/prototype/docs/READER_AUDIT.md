# READER_AUDIT — prototipo UX/UI 5E ATLAS

Data: 2026-11-21 · Autore: @prototype-builder · Solo audit, **nessuna modifica** a `index.html` o ai dati.

## Metodo e fonti
- Sorgente: `/opt/data/cache/scratch/atlas-ux-prototype/index.html` (53 KB), `data/books-2024.json`, `data/core-2024.json`.
- Server locale: `python3 -m http.server 8896`, URL `http://127.0.0.1:8896/index.html#reader`, viewport 390×844.
- Verifica dati: Python su 29 capitoli / 11 categorie; verifica DOM: browser headless, 0 errori `window.onerror` / `unhandledrejection`.
-comandi utili: `node check.mjs`, `node test-reader.mjs`, `node test-toc.mjs`.

## Cosa funziona (verificato)
- 29 capitoli (XPHB 12, XDMG 12, XMM 5); switch libro da UI → titoli e TOC corretti (`Indice · Manuale del Master`, 12 voci; XMM `1 / 5`).
- TOC: `#tocBtn` apre il dialog, click su voce → capitolo 8/12 (`Chapter 7: Spells`) e chiusura dialog.
- Stepper: `#readerArticle [data-reader-next]` / `[data-reader-prev]` → 8/12 → 9/12 → 8/12, titoli coerenti.
- Breadcrumb `#readerCrumbs`: `Home / Biblioteca / Manuale del Giocatore / <capitolo>`, con `aria-current`.
- XPHB ch7: 394/394 ref espandibili; primo `<details>` aperto con 5 statistiche e 1 paragrafo.
- XPHB ch7: 2 tabelle, 27 liste, 157 note; tabella con overflow orizzontale attivo (client 305px / scroll 340px).
- Capitolo senza sezioni (`Appendix B`, XPHB 10/12): `#readerSideLinks` mostra «Nessuna sezione», nessun errore.
- Performance: XPHB ch7 61 ms, XDMG ch7 177 ms (665 ref), XMM ch2 154 ms (587 ref). Nessun errore JS.

## Bug e priorità

### P1 — 1. Reference irrisolte: card non espandibili (281 casi)
- **Evidenza**: XPHB 2/12 → 20/20 card fallback; XPHB Glossary → 39/155; XDMG 7/12 → 81/665; XMM 2/5 → 82/587. Esempi: `Burning`, `Dehydration` (tag `hazard`).
- **Causa**: `blockHTML()`, ramo `if(!item)`: genera `<div class="ref-card">` invece di `<details>`. I dati hanno `b.cat === null` (281 ref), quindi la lookup `DATA.categories[b.cat].items[b.idx]` non parte.
- **Selettore**: `div.ref-card` (vs `details.ref-card`).
- **Fix consigliato**: risolvere per nome normalizzato su `Object.values(DATA.categories).flatMap(c=>c.items)` con fallback di ricerca; in alternativa rendere comunque `<details>` con summary «Riferimento non risolto» e link a `#spells?search=<nome>`, così l'utente ha un'azione.

### P1 — 2. Stato del lettore non persistente (nessun deep link)
- **Evidenza**: dopo TOC/stepper `location.hash` resta `#reader` (`history.replaceState(null,'','#reader')` in `renderReader()`). Reload, Back o link condiviso riportano sempre XPHB capitolo 1.
- **Selettori**: `renderReader()`, `history.replaceState`, `#readerArticle [data-reader-prev|next]`, `[data-toc-chapter]`.
- **Fix consigliato**: codificare libro+capitolo nell'hash (`#reader/XDMG/7`) o query (`?book=XDMG&ch=7`); leggere lo stato all'avvio e su `hashchange`/`popstate`; usare `pushState` per i cambi capitolo così Back torna al precedente.

### P1 — 3. Indice del capitolo troncato a 18 voci
- **Evidenza**: XPHB ch7 ha 56 `.book-section[id]` ma `#readerSideLinks` contiene solo 18 link (`CURRENT_SECTIONS.slice(0,18)`): 38 sezioni non raggiungibili dall'indice laterale.
- **Selettore**: `#readerSideLinks`, `.book-section[id]`, `CURRENT_SECTIONS.slice(0,18)`.
- **Fix consigliato**: elenco completo con contenitore scrollabile e header sticky, oppure accordion per gruppo; evitare il taglio silenzioso.

### P2 — 4. DOM molto pesante nei capitoli densi
- **Evidenza**: XPHB ch7 463 KB HTML / 394 `<details>`; XDMG ch7 553 KB / 665 ref; XMM ch2 690 KB / 587 ref. Tempi 61/177/154 ms solo per `innerHTML`, esclusi layout e pittura.
- **Selettore**: `#readerArticle .ref-card`, `blockHTML()` ramo `b.t==='ref'`.
- **Fix consigliato**: renderizzare i `<details>` con corpo vuoto e popolarlo al primo `toggle` (lazy); oppure virtualizzare la lista; precalculare `statsFor`/`sourceOf` una volta per categoria.

### P2 — 5. Ref con scheda vuota
- **Evidenza**: 107 voci nei manuali hanno `entries` assente → l'espansione mostra «Nessuna descrizione testuale.».
- **Selettore**: `.ref-body p` con testo «Nessuna descrizione testuale.», `paragraphs(item.entries)`.
- **Fix consigliato**: mostrare almeno statistiche, fonte e un link «Apri nel compendio»; il testo generico da solo non aggiunge contesto.

### P2 — 6. Target touch sotto soglia nell'indice
- **Evidenza**: a 390px `.toc-item` misura **29px** di altezza (minimo richiesto 44px). `#tocBtn` è 44px, ok.
- **Selettore**: `.toc-item` (`padding:11px 0`, font 14px, nessuna `min-height`).
- **Fix consigliato**: `min-height:44px; align-items:center` su `.toc-item` e sui suoi contenitori.

### P3 — 7. TOC non bottom-sheet; indice laterale non sticky su mobile
- **Evidenza**: `dialog#toc` a 390px è un modale centrato di 339px; `.reader-side` è in flusso normale (la regola sticky è solo dentro `@media (min-width:768px)`).
- **Selettori**: `dialog#toc`, `.toc-item`, `.reader-side`, `.reader-bar` (sticky top 72px, 66px misurati).
- **Fix consigliato**: ancorare `dialog#toc` a `bottom:0` con `border-radius:18px 18px 0 0`; rendere `.reader-side` sticky anche >0px o trasformarlo in drawer.

### P3 — 8. Sezioni senza nome non navigabili
- **Evidenza**: 7 blocchi `t==='section'` senza `name`: `blockHTML()` non assegna `id` e non emette heading, quindi non entrano in `CURRENT_SECTIONS`.
- **Selettore**: `.book-section` senza `id`, `if(b.name) CURRENT_SECTIONS.push(...)`.
- **Fix consigliato**: generare comunque un id (`sec-<book>-<index>-<n>`) e un heading con titolo derivato dal primo paragrafo, o renderizzare come gruppo senza sezione.

### P3 — 9. Tabelle leggibili ma header non ancorato
- **Evidenza**: `table{min-width:340px}` e `.table-wrap{overflow-x:auto}` funzionano;`<th>` ha sfondo `#e5d5b7` ma non è `sticky`, e non c'è indizio visivo che la tabella scorra.
- **Selettore**: `.table-wrap`, `table thead th`.
- **Fix consigliato**: `thead th{position:sticky;top:0;z-index:1;background:#e5d5b7}` e un gradiente/ombra sul bordo destro del wrapper.

### P3 — 10. Immagini remote senza fallback
- **Evidenza**: copertine `https://raw.githubusercontent.com/...` e background categorie `https://media.ruleholder.com/...` con `loading="lazy"` ma nessun `onerror`; in assenza di rete restano cassette vuote senza testo alternativo visibile.
- **Selettore**: `.book img`, `.cat[style*="--art"]`.
- **Fix consigliato**: asset locali in `assets/` con `onerror` che mostra iniziali/titolo.

## Sintesi gate
Nessun blocco funzionale: capitoli, TOC, stepper, tabelle, liste, note ed espansione ref funzionano senza errori JS. Prima della promozione: risolvere **P1-1** (281 card mute), **P1-2** (deep link) e **P1-3** (indice troncato). Le P2 sono ottimizzazioni di qualità/performance; le P3 rifiniture mobile.
