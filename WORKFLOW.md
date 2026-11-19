# Flusso di collaborazione ATLAS

Repo: `hybrid-entree-art/5etools-host`. È l'unica sorgente del progetto.

## Rami
- `main` — codice pronto da distribuire. Deploy Vercel via CLI (`vercel deploy --archive=tgz`).
- `design/frames` — esportazioni FigCraft dell'utente (PNG/SVG/.figcraft). Non tocca il codice.

## Come collaboriamo
1. L'utente disegna in FigCraft ed esporta i frame in `design/` sul ramo `design/frames`, poi scrive in chat quali frame sono pronti.
2. Io faccio `git fetch` + checkout del ramo, leggo i frame e implemento in `atlas.css` / `atlas.js` sul ramo `main`.
3. Verifico in browser a 390px e 1440px, poi pusho su `main` e distribuisco la preview.
4. Se serve una correzione, l'utente aggiorna il frame e ripete dal punto 1.

## Regole
- Nessun CSS che nasconde un'interfaccia per metterne sopra un'altra: si riscrive un solo set di componenti.
- I dati restano nel clone 5e.tools; `data/` non si modifica a mano.
- Le immagini usate sono quelle leggere generate da `scripts/curate_assets.py`.
- Un solo autore per file per evitare conflitti.

## Stato
- Home ATLAS attiva (`atlas.css` + `atlas.js`) su self-host 5e.tools.
- Tutti i 68 libri presenti.
- Nessun accesso live a FigCraft da questa sessione: GitHub è il canale di scambio.
