# 5E ATLAS — brief per FigCraft

Importa `BASE-FIGCRAFT.svg` in FigCraft come punto di partenza: contiene un lettore mobile a 390 px e una tavola di palette e componenti. Salva una copia `.figcraft` sul ramo `design/frames`. Non è un tema pronto per il sito: i frame si modificano e approvano prima di portarli sul self-host.

## Prompt

> Progetta un'unica interfaccia per il self-host 5e.tools. Prendi da Ruleholder il modo di passare da home a catalogo e manuale, non il suo logo; non sovrapporre una home nuova alla navigazione originale di 5e.tools. I contenuti e le funzionalità esistenti restano disponibili.
>
> Parti dal frame del lettore e dalla palette allegata. Esplora un trattamento **ad acquerello** per illustrazioni, copertine e separatori, lasciando pulita l'area di lettura. Slate, ambra e teal sono una proposta modificabile; tieni il glow solo su pochi accenti e sul focus. Prova Modesto/Modesto Condensed per i titoli, Mulish per l'interfaccia e Lora per il testo lungo: verificane la leggibilità insieme al layout, non trattarli come vincoli se non funzionano.
>
> Disegna a 390 px partendo da lettore, home, catalogo e scheda di dettaglio. Riusa la stessa navigazione e gli stessi componenti. Nel lettore: articolo unico, indice flottante separato dal menu generale, chiusura esplicita dell'indice e un solo controllo precedente/successivo. Le tabelle non devono allargare la pagina: se una tabella è larga, si scorre solo dentro la tabella. Tocchi da almeno 44 px, focus visibile, supporto alle safe area e nessun dato duplicato nelle schede. Nella home metti in evidenza i tre manuali base, ma lascia raggiungibile tutta la biblioteca. Dopo aver trovato la direzione mobile, adatta la stessa interfaccia a 1440 px.
>
> Usa qualche stringa reale per verificare la gerarchia, anche con titoli lunghi. Non tradurre e non fare selettori di lingua in questa fase. Consegna il file editabile `.figcraft` e un PNG per schermata in `design/` sul ramo `design/frames`; segnala le decisioni che vuoi trasferire al sito.

## Lingua — dopo l'approvazione grafica e mobile

L'inglese originale rimane intatto. I testi italiani forniti dall'utente vengono associati allo stesso ID e mostrati dove disponibili; un nuovo libro o una voce non tradotta rimangono leggibili in inglese. La ricerca indicizza il nome inglese, il nome italiano e gli alias disponibili; entrambe le lingue aprono la stessa scheda, senza duplicare il risultato. La lingua dell'interfaccia resta una decisione separata. Non implementare questa fase nel prototipo.
