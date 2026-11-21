# 5E ATLAS — prototipo UX/UI

Prototipo unico e cliccabile con **tutto il contenuto 2024 dei tre manuali base** (XPHB, XDMG, XMM) e con i libri reali nel lettore. Non è il sito di produzione: serve a validare gerarchia, densità e comportamento mobile prima di toccare `main`.

- **Preview:** https://atlas-ux-prototype-q58hyn3fx-hybrid-art.vercel.app/
- **Mobile:** 390 px, poi desktop 1440 px.
- **Dataset compendio:** `data/core-2024.json`, 2.076 voci, 1,3 MB.
- **Dataset lettore:** `data/books-2024.json`, capitoli e riferimenti espandibili ai contenuti del compendio.
- **Categorie:** Incantesimi 391 · Mostri 505 · Oggetti magici 634 · Equipaggiamento 123 · Classi 12 · Sottoclassi 48 · Talenti 77 · Background 16 · Specie 10 · Bastioni 35 · Glossario 225.
- **Navigazione:** Home e Biblioteca. Il lettore si apre scegliendo uno dei tre manuali, non da una voce di menu separata.
- **Lettore:** capitoli reali da `book-xphb`, `book-xdmg`, `book-xmm`; indice del manuale; riferimenti espandibili per incantesimi, classi, background, talenti, oggetti, mostri e glossario. Deep link `#reader/XPHB/8`.
- **Dettaglio:** fonte mostrata una sola volta; metadati e testo pulito dai tag di 5e.tools.
- **Direzione:** guscio scuro ATLAS, pergamena solo nel contenuto di lettura e nella scheda.
- **Font:** Modesto, Modesto Condensed, Mulish, Lora in `fonts/`.

## Rigenerare i dataset

I generatori leggono il checkout self-hosted di 5e.tools durante lo sviluppo:

```bash
python3 scripts/build-core-data.py
python3 scripts/build-books-data.py
```

I file `data/core-2024.json` e `data/books-2024.json` sono già inclusi: per la preview non serve né il clone né rigenerarli.

Aprire `index.html` da un server statico (il fetch dei JSON non funziona da `file://`).
