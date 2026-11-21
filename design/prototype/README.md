# 5E ATLAS — prototipo UX/UI

Prototipo unico e cliccabile con **tutto il contenuto 2024 dei tre manuali base** (XPHB, XDMG, XMM). Non è il sito di produzione: serve a validare gerarchia, densità e comportamento mobile prima di toccare `main`.

- **Preview:** https://atlas-ux-prototype-qjnc4dr7p-hybrid-art.vercel.app/
- **Mobile:** 390 px, poi desktop 1440 px.
- **Dataset:** `data/core-2024.json`, 1.916 voci, 1,3 MB.
- **Categorie:** Incantesimi 391 · Mostri 505 · Oggetti magici 584 · Equipaggiamento 123 · Classi 12 · Sottoclassi 48 · Talenti 77 · Background 16 · Specie 10 · Bastioni 35 · Glossario 115.
- **Ricerca:** su nome, scuola, tipo, rarità, classe, categoria e testo.
- **Filtri:** pannello contestuale per categoria (livello/scuola, tipo/taglia, rarità/tipo, ecc.) con pillole rimovibili e azzeramento.
- **Dettaglio:** scheda dinamica per ogni voce, con metadati e testo pulito dai tag di 5e.tools.
- **Direzione:** guscio scuro ATLAS, pergamena solo nel contenuto di lettura e nella scheda.
- **Font:** Modesto, Modesto Condensed, Mulish, Lora in `fonts/`.

## Rigenerare il dataset

Il generatore legge il checkout self-hosted di 5e.tools:

```bash
python3 scripts/build-core-data.py
```

Per impostazione predefinita cerca `../../5etools-host/data` rispetto al prototipo. Il file `data/core-2024.json` è già incluso e non serve rigenerarlo per aprire la preview.

Aprire `index.html` da un server statico (il fetch del JSON non funziona da `file://`).
