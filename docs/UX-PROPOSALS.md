# Proposte di interfaccia UX — 5E ATLAS

Vincolo comune: **un solo sistema**, sui dati e sulle URL native di 5e.tools. Le proposte cambiano gerarchia e densità, non moltiplicano le navigazioni. La lingua resta fuori.

## Proposta A — Reference Desk (consigliata per l'uso al tavolo)

La home è un banco di consultazione: ricerca grande, tre manuali base, categorie subito sotto. Il catalogo è una lista densa a una colonna su mobile, con filtri a chip e conteggio sempre visibile. La scheda mostra metadati una volta e testo subito dopo. Il lettore ha un solo comando `Contents` flottante e un solo pager a fine capitolo.

- **Mobile:** header 56 px con marchio, ricerca e menu; home con search field a tutta larghezza; righe catalogo 72–88 px; filtri in riga orizzontale scorrevole; niente thumbnail obbligatoria.
- **Desktop:** colonna centrale 720–860 px, filtri a sinistra, indice del lettore a destra; la home resta a una colonna larga, non a dashboard.
- **Forza:** trovare una regola in pochi secondi, anche durante una sessione.
- **Rischio:** meno invitante per chi vuole sfogliare; richiede disciplina nel non aggiungere decorazione.

## Proposta B — Library Shelf (per lettura e scoperta)

La home è una biblioteca: copertine grandi dei tre manuali, poi scaffali per edizione, ambientazione e tipo. Il catalogo usa copertine e titoli come unità; il lettore è un articolo lungo con tipografia generosa e indice laterale su desktop.

- **Mobile:** home a due colonne di copertine; catalogo con card 2:3 e titolo sotto; lettore con prosa 18/30 e `Contents` in basso.
- **Desktop:** griglia a 3–4 colonne per la biblioteca; lettore a due colonne (testo + indice sticky).
- **Forza:** dà valore a copertine e manuali, rende la biblioteca memorabile.
- **Rischio:** più scroll e meno efficienza nella ricerca; le copertine possono dominare sui contenuti.

## Proposta C — Atlas Index (per esplorazione e apprendimento)

La home è un atlante di categorie illustrate, con breadcrumb persistente e ricerca globale. Le schede si collegano tra loro (classe → incantesimi → oggetti) e il lettore usa sezioni numerate con note marginali.

- **Mobile:** griglia di tile 2 colonne; breadcrumb sticky; schede con “Correlati” in fondo.
- **Desktop:** indice laterale sempre visibile, contenuto centrale, correlati a destra.
- **Forza:** aiuta a capire le relazioni tra regole, ottimo per chi impara.
- **Rischio:** più complesso da costruire e da mantenere; può sembrare un wiki.

## Confronto

| Criterio | A — Reference Desk | B — Library Shelf | C — Atlas Index |
|---|---|---|---|
| Ricerca al tavolo | Ottima | Media | Buona |
| Lettura lunga | Buona | Ottima | Media |
| Scoperta | Media | Ottima | Ottima |
| Mobilità | Ottima | Buona | Media |
| Complessità | Bassa | Media | Alta |
| Rischio di doppia UI | Basso | Basso | Medio |

## Raccomandazione

**A come struttura principale, con la tipografia e le copertine di B.** Non due interfacce: un solo guscio, due densità. La modalità `Reference` è il default; la modalità `Reading` si attiva quando si apre un manuale e cambia solo misura del testo, larghezza e presenza dell'indice laterale. Stessi componenti, stessi colori, stessa navigazione.

## Primo taglio da prototipare

1. `Reader / Reading` a 390 px — PHB 2024, capitolo “Playing the Game”.
2. `Reader / Contents` — pannello aperto, focus, Escape, ritorno al comando.
3. `Spells / Results` — ricerca `Fireball`, filtro 2024, ritorno dalla scheda.
4. `Spell / Detail` — Fireball: livello 3, Evocation, 1 action, 150 ft.
5. `Home` e `Library` — solo dopo che i primi tre flussi sono approvati.

## Pattern dagli esempi app

Gli esempi mostrano un compendio mobile ben riconoscibile: lista scura, ricerca subito sotto l'header, card con nome e fonte, tag colorati per le meccaniche, dettaglio con titolo italiano e originale inglese, metadati a icone, cerchi delle caratteristiche e chip delle classi. Sono pattern utili, ma vanno corretti nei punti in cui l'app li ripete o li comprime.

| Prendere | Correggere |
|---|---|
| Ricerca sempre visibile e filtro nell'header. | Icona filtro a imbuto, non tre linee ambigue; etichetta della tab completa, mai troncata. |
| Tag colorati per concentrazione, rituale, componenti materiali. | Colore più testo o icona, mai solo colore; niente tag duplicati nella stessa scheda. |
| Titolo italiano con originale inglese in corsivo sotto. | Non ripetere il titolo nell'header e nel corpo: l'header mostra il titolo solo dopo lo scroll. |
| Metadati a icone: tempo, gittata, durata, componenti. | Una sola griglia, allineata; niente concentrazione scritta due volte. |
| Card mostro/oggetto con immagine, nome, CR/rarità e fonte. | Due colonne solo per i cataloghi visivi; per gli incantesimi righe più dense. Immagini con fondo coerente, non bianco su dark. |
| Cerchi delle caratteristiche e chip delle classi. | Chip leggibili come pulsanti; lore lunga collassabile o con indice interno. |
| Bottom navigation per le sezioni principali. | Per 5E ATLAS: Home, Library, Compendium, Search, Menu. Non Spells/Monsters/Sheet come app character-centric. |
| Dettaglio con immagine, dati, descrizione, correlati. | Separatori e respiro; prezzi e note secondarie in stile coerente, non tutti in corsivo. |

**Applicazione alla proposta A:** lista incantesimi a righe con tag; mostri e oggetti a griglia 2 colonne; dettaglio con header contestuale, metadati una volta, immagine con fondo scuro, classi come chip. **Proposta B:** la stessa scheda può usare copertine e immagini più grandi, ma non cambiare la struttura dei dati. **Proposta C:** i correlati e le lore collassabili sono il punto di partenza.

## Cosa non fare


- Non nascondere il chrome di 5e.tools con CSS per metterne sopra un altro.
- Non duplicare il menu globale dentro l'indice del libro.
- Non usare immagini dietro tabelle o paragrafi.
- Non introdurre una seconda ricerca o un secondo modello dati.
- Non congelare la palette prima di aver provato i flussi: prima gerarchia e orientamento, poi stile.
