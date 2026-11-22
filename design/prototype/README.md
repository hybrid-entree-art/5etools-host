# 5E ATLAS — prototipo UX/UI

Prototipo unico e cliccabile con **tutto il contenuto 2024 dei tre manuali base** (XPHB, XDMG, XMM) e con i libri reali nel lettore. Non è il sito di produzione: serve a validare gerarchia, densità e comportamento mobile prima di toccare `main`.

- **Preview:** https://atlas-ux-prototype-34eubedz8-hybrid-art.vercel.app/
- **Mobile:** 390 px, poi desktop 1440 px.
- **Dataset compendio:** `data/core-2024.json`, 2.434 voci in 20 categorie, 1,6 MB.
- **Dataset lettore:** `data/books-2024.json`, capitoli e riferimenti espandibili ai contenuti del compendio.
- **Categorie:** Incantesimi 391 · Mostri 505 · Oggetti magici 641 · Equipaggiamento 218 · Classi 12 · Sottoclassi 48 · Talenti 77 · Background 16 · Specie 10 · Bastioni 35 · Opzioni di classe 58 · Lingue 34 · Divinità 27 · Abilità 18 · Maestria 8 · Proprietà 12 · Tesori 11 · Tipi di oggetto 33 · Carte 55 · Glossario 225.
- **Navigazione:** Home e Biblioteca. Il lettore si apre scegliendo uno dei tre manuali, non da una voce di menu separata.
- **Lettore:** capitoli reali da `book-xphb`, `book-xdmg`, `book-xmm`; indice del manuale; riferimenti espandibili per incantesimi, classi, background, talenti, oggetti, mostri e glossario. Deep link `#reader/XPHB/8`.
- **Incantesimi:** lista con scuola colorata, tempo/gittata/durata e fonte; scheda con scuola, tiro salvezza, danno, attacco, classi e fonte in basso.
- **Navigazione:** tasto Indietro nell’header e nel menu per non uscire dal prototipo.
- **Mostri:** scheda divisa in Tratti, Azioni, Azioni bonus, Reazioni e Azioni leggendarie; nomi in grassetto; informazioni leggendarie incorporate, niente categoria separata.
- **Specie e classi:** lista con card orizzontali e arte a destra; dettaglio con hero image e feature di classe in accordion, come Ruleholder.
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
