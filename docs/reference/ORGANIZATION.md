# Organizzazione ATLAS — decisione unica

## Sorgente di verità
- **Dati**: `/opt/data/5etools-host/data/` (clone 5e.tools). Nessun dato scritto a mano nel progetto ATLAS. **Tutti i 68 libri vengono conservati**, non solo i tre manuali base.
- **Asset**: `public/art/` nel progetto ATLAS, generati da `scripts/curate_assets.py` da fonti autorizzate.
- **Font**: `public/art/fonts/`, generati da font self-hosted di Ruleholder.

## Progetto applicativo
- Path attuale: `/opt/data/ruleholder-clone` (verrà rinominato in `atlas` dopo la migrazione).
- Design: `IDENTITY.md` + `src/app/atlas.css`.
- Pagine: solo route ATLAS. `src/app/(clone)/` è **solo riferimento storico**, da cancellare alla fine.

## Regole di lavoro
1. Ogni pagina nuova legge i dati tramite `src/data/`, popolato esclusivamente da `scripts/sync_data.py` che copia da `/opt/data/5etools-host/data/`.
2. Nessun conteggio hardcoded: sempre calcolato dai JSON.
3. Nessun numero "di memoria" (391/503/584 sono derivati, non costanti).
4. Ogni pagina nuova passa da: build → browser 390px → QA di @critique-reviewer.
5. Un bot per insieme di file, mai due sullo stesso file.

## Stato
- Fatti: home, `/spells`, `/classes`, `/books/*`.
- Da fare: `/monsters`, `/magic-items`, `/equipment`, `/feats`, `/backgrounds`, `/species`, `/bastions`, `/glossary`, `/sourcebooks`.
- Fine: cancellazione di `(clone)/`, rename cartella, deploy finale.
