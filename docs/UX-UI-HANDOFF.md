# 5E ATLAS — specifica UX/UI per Figma e harness AI

**Decisione proposta:** una biblioteca di gioco, non una landing promozionale. Due compiti principali: trovare una regola durante la sessione e leggere un manuale con calma. Stesso progetto, stessi dati, un solo sistema di navigazione. Questo documento è la bozza da provare, non una decisione grafica già approvata.

## 1. Struttura e navigazione

- **Navigazione globale:** `Home`, `Library`, `Compendium`; `Search` raggiungibile da tutte le pagine. Su mobile, header compatto con marchio/Home, ricerca e menu; su desktop le destinazioni sono visibili nello stesso header. Le utility esistenti restano raggiungibili dal menu, non rubano spazio ai flussi principali. Niente seconda barra globale.
- **Navigazione di contesto:** `Back to results` ripristina ricerca, filtri e posizione nella lista. Se si arriva da un link diretto, il link esplicito torna al catalogo o alla biblioteca: non mandare l’utente fuori dal sito. Home, ritorno e indice sono azioni distinte.
- **Lettore:** l’indice riguarda solo il libro aperto. Su mobile il pulsante flottante `Contents` resta raggiungibile anche scorrendo; su desktop la stessa struttura può stare in una colonna laterale. Un solo blocco `Previous chapter / Next chapter` a fine capitolo, non una seconda barra persistente. Il menu globale non contiene l’indice.

| Percorso | Comportamento da disegnare e provare |
| --- | --- |
| Home → Library → PHB → capitolo | Metti ricerca e accessi a biblioteca/cataloghi nella prima schermata; copertine in evidenza non escludono gli altri libri. La biblioteca mostra titolo, anno editoriale e tipo, e distingue le edizioni senza bloccare il legacy. |
| Home → Spells → ricerca → Fireball | La lista mobile è a una colonna. Ogni riga mostra titolo, livello/scuola e fonte; tempo di lancio e gittata solo se restano leggibili. Niente thumbnail obbligatoria negli elenchi densi. Il filtro `2024 Core` è un punto di partenza proposto, sempre visibile e rimovibile; `All sources` non elimina la ricerca corrente. |
| Risultati → scheda → Back to results | Titolo e fonte, poi una sola griglia di metadati, poi testo. Mostrare il risultato del ritorno, non solo il pulsante. Dati prova da 5e.tools: Fireball (XPHB), livello 3, Evocation, 1 action, 150 ft. |
| Lettore → Contents → scelta sezione | Evidenzia il capitolo corrente con testo e stile; profondità progressiva, non tutte le voci espanse. Chiusura senza selezione: conserva posizione e restituisce il focus al comando. Scelta: aggiorna il deep link nativo, chiude il pannello e porta focus al titolo di destinazione. |

**Stati da includere:** lista iniziale, filtri attivi, nessun risultato con `Clear filters`, dettaglio da link diretto, indice chiuso/aperto, tabella larga, titolo lungo e copertina assente. Niente traduzioni o selettore lingua in questa fase.

## 2. Direzione visuale: inchiostro e acquerello

- **Immagine:** macchie di colore e carta visibili nelle copertine, nelle aperture e nelle categorie; una sola illustrazione dominante quando serve. Il lettore parte dal titolo e dal testo: l’arte non è un prerequisito e non sta dietro paragrafi o tabelle.
- **Colori di partenza:** `canvas #0B0F14`, `surface #141A21`, `raised #1B232C`, `text #EEF3F6`, `muted #B6C2CC`, `accent #F0A742`, `secondary #5FD0C0`. Usare testo scuro su fondo ambra; il teal distingue i link anche con sottolineatura in prosa. Glow solo sul focus o su un accento selezionato; niente effetti permanenti su ogni card. La palette è editabile, non il requisito di contrasto.
- **Tipografia:** Modesto/Modesto Condensed per titoli e copertine; Mulish per UI e dati; Lora per la prosa. Proposta mobile: titolo capitolo 32/36, sezione 24/30, prosa 17/28, UI 16/22, metadati 14/20. Se il font non è disponibile nel file design, dichiarare il fallback, non convertire tutti i testi in tracciati.
- **Spaziatura:** scala 4/8/12/16/24/32; margine mobile 16, tap target principale almeno 44 px. Su desktop, allarga biblioteca e catalogo ma tieni la prosa intorno a 65–75 caratteri per riga; non far diventare le colonne delle tabelle una scusa per allargare tutta la pagina.
- **Componenti Figma:** `App header`, `Search field`, `Filter chip`, `Catalog row`, `Book cover`, `Metadata`, `Callout`, `Table`, `Contents dialog`, `Chapter pager`. Usa Auto Layout, variabili semantiche e varianti default/hover/focus/active/disabled dove pertinenti. Stati selezionati riconoscibili senza colore; focus visibile; niente testo essenziale incorporato nelle immagini.

## 3. Riferimenti da guardare, non da copiare

| Riferimento | Da osservare | Da lasciare fuori |
| --- | --- | --- |
| [Ruleholder — biblioteca](https://ruleholder.com/sourcebooks) | Copertina e titolo come unità, filtri per tipo di pubblicazione. | Logo, feed, chrome del sito. |
| [Ruleholder — incantesimi](https://ruleholder.com/spells) | Gerarchia delle righe per livello e fonte; dati riconoscibili prima di aprire la scheda. | Griglia illustrata dentro un catalogo che deve essere consultato velocemente. |
| [D&D Beyond — Basic Rules](https://www.dndbeyond.com/sources/dnd/br-2024) | Indice per argomenti, titoli chiari e sezioni del glossario linkabili. | Menu e banner commerciali. |
| [Archives of Nethys — Spells](https://2e.aonprd.com/Spells.aspx) | Scorciatoie ai sottoinsiemi e filtri utili nella consultazione. | Tassonomie Pathfinder o un secondo motore di ricerca. |
| [WAI — Modal Dialog](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) | Focus dentro il pannello, fondo inattivo, Escape, chiusura esplicita e ritorno del focus. | Dichiarare `aria-modal` senza comportamenti reali. |

## 4. Come lavoriamo: Figma → GitHub → harness

1. **Figma a 390 px:** partire da `Reader / Reading`, `Reader / Contents`, `Spells / Results`, `Spell / Detail`. Poi `Home` e `Library`. Aggiungere due adattamenti a 1440 px (Reader e Results); non duplicare a mano i componenti. Collegare i due flussi cliccabili. Annotare le decisioni ancora aperte, senza infilare stili alternativi nello stesso frame.
2. **Review di tre compiti:** trovare Fireball, tornare alla lista senza perdere il filtro, aprire una sezione del manuale e scorrere una tabella larga. Ripetere con tastiera nella fase browser. In Figma si giudicano gerarchia e orientamento, non si certifica l’accessibilità del codice.
3. **Scambio:** link al frame Figma con accessi scelti dall’utente; su GitHub tenere export condivisibili, token e note di decisione. Un frame approvato con nome stabile è il riferimento visivo. Questa specifica resta il riferimento per stati e comportamenti; se l’AI propone una deviazione, la annota prima di adottarla.
4. **Implementazione e QA:** una PR per flusso, partendo dal lettore nativo su `book.html`; poi `spells.html`, home e biblioteca. Nessun overlay per nascondere la vecchia UI, niente nuovo progetto o modifica a `data/`. Prova browser a 320, 390, 768 e 1440 px e confronto con frame/versione approvati: deep link, cronologia, focus, safe area, niente overflow pagina, scroll locale della tabella. Nessun deploy finché il flusso non passa.

### Prompt da passare al harness quando il frame è approvato

> Leggi questa specifica e il frame approvato indicato nella PR. Lavora solo sul primo flusso: lettore nativo su `book.html`. Preserva fonti, URL/hash, renderer e funzioni originali. Usa un solo sistema di componenti; non aggiungere una UI sopra la vecchia. Implementa il frame `Reader / Reading` e `Reader / Contents`, compresi focus, chiusura e tabella larga. Non lavorare su home, lingua o altri cataloghi. Testa a 320/390/768/1440 px con PHB 2024, un secondo manuale e un libro legacy. Riporta i frame usati, i file cambiati, gli esiti dei test, gli screenshot e le divergenze. Non distribuire né unire la PR automaticamente.
