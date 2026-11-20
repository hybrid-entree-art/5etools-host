# Piano UX mobile — 5e.tools self-host

## Cosa prendere dai riferimenti

| Riferimento | Pattern osservato | Come applicarlo qui |
| --- | --- | --- |
| [Ruleholder — home](https://ruleholder.com/) e [biblioteca](https://ruleholder.com/sourcebooks) | Ricerca e categorie raggiungibili dalla home; biblioteca distinta con copertine e filtri per tipo di pubblicazione. | Mettere ricerca, Regole e Biblioteca prima delle utility. Mostrare i tre manuali base in evidenza, con un accesso diretto alla biblioteca completa. Niente feed, commenti o logo copiati. |
| [Ruleholder — incantesimi](https://ruleholder.com/spells) | Liste raggruppate per livello; ogni riga mostra scuola, lancio, gittata e fonte. | Riga mobile compatta, senza ripetere dettagli. I filtri restano del motore 5e.tools; la priorità visiva va ai più utili. |
| [D&D Beyond — Basic Rules](https://www.dndbeyond.com/sources/dnd/br-2024) | Indice per pubblico e argomento; collegamenti puntuali al glossario. | Indice del singolo manuale distinto dal menu generale. Preservare i collegamenti profondi e la leggibilità delle tabelle. |
| [Archives of Nethys — Spells](https://2e.aonprd.com/Spells.aspx) | Collegamenti diretti a sottoinsiemi filtrati del catalogo, come tradizioni e rituali. | Per i filtri frequenti usare scorciatoie alle viste filtrate quando supportate da 5e.tools; non copiare tassonomie Pathfinder né introdurre un secondo motore. |

## Ordine di lavoro

1. **Lettore per primo.** Percorso iniziale: apertura di un manuale → capitolo → indice flottante → altro capitolo. Usare il renderer nativo di `book.html`; un solo passo precedente/successivo, tabella larga scorrevole nel proprio contenitore, indice con chiusura esplicita. Provare PHB 2024, un secondo manuale e un libro legacy.
2. **Un catalogo completo: incantesimi.** Lista, ricerca, filtri, scheda, ritorno alla lista senza perdere lo stato. Priorità alle regole 2024, non eliminare le altre fonti. Nessun metadato ripetuto nella scheda. Riutilizzare il codice già operativo di 5e.tools.
3. **Home e biblioteca.** Riutilizzare gli stessi componenti, non aggiungere una home davanti alla vecchia navigazione. Illustrazioni ad acquerello su copertine e categorie; prosa e tabelle su superfici pulite. Il resto del compendio adotta i componenti solo dopo i primi flussi verificati.
4. **Lingua dopo grafica e mobile.** Testi italiani forniti dall'utente associati all'ID originale; inglese mantenuto per testi mancanti e nuove uscite. Alias IT/EN verso la stessa scheda. Nessuna modifica linguistica in questa fase.

## Protezioni e criteri prima del deploy

- `python3 scripts/check_ux_baseline.py` verifica che ogni libro indicizzato abbia un payload non vuoto, che i tre manuali base siano presenti e che gli ingressi nativi esistano. In una PR solo UX, `git diff origin/main...HEAD -- data/` deve essere vuoto: preserva il corpus anche se qualcuno rimuovesse un libro sia dall'indice sia dal file.
- In browser a 390 e 1440 px: aprire biblioteca, capitolo e scheda da URL diretto; verificare navigazione, filtri, ritorno e tabelle. Nessuno scroll orizzontale della pagina, comandi mobili principali con area utile da almeno 44 px, focus visibile e contenuti leggibili anche a immagini non caricate.
- Non promuovere un restyling se i menu sono solo nascosti per far posto a una seconda interfaccia o se un link nativo cambia destinazione senza compatibilità.

## Baseline verificata

- Self-host pulito: in browser la home originale e la biblioteca caricano; `book.html#xphb,1` apre *Playing the Game* e `spells.html#fireball_xphb` apre *Fireball*. Questi sono test di apertura, non una certificazione mobile.
- Repository: 68 libri indicizzati con contenuti non vuoti. Il numero è una misura della base corrente, non un limite ai contenuti futuri.
