# Flusso di collaborazione — 5e.tools self-host

[`hybrid-entree-art/5etools-host`](https://github.com/hybrid-entree-art/5etools-host) è il repository applicativo. `main` conserva il self-host funzionante, senza il vecchio tema ibrido.

- **Design:** `design/frames` conserva [brief, base SVG e file FigCraft](https://github.com/hybrid-entree-art/5etools-host/tree/design/frames/design). È un canale di scambio, non un prerequisito per audit e lavoro tecnico. Non va fuso in `main`: contiene anche una vecchia base applicativa.
- **Implementazione:** un ramo e una PR per ciascun flusso, con [piano e criteri UX](docs/UX-PLAN.md). Intervenire sulle pagine native: niente progetto parallelo, niente navigazione duplicata. Preservare `data/`, URL e funzioni originali.
- **Verifica:** eseguire `python3 scripts/check_ux_baseline.py`, controllare il diff dei dati e provare il flusso a 390 e 1440 px prima di promuovere. Le preview, quando servono, si distribuiscono via Vercel CLI con `--archive=tgz`; il push su GitHub non le pubblica automaticamente.
