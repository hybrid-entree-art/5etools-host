# Vercel — deploy, alias, verifica

Progetto: `5etools-host` (team `hybrid-art`). CLI: `/opt/data/bin/vercel`, versione verificata **65.17.0** (`/opt/data/bin/vercel --version`). Link stabile: **`https://5etools-host.vercel.app`**.

**Nessun token, password o ID segreto deve comparire in questo file né nei comandi condivisi.** La CLI è già autenticata nell'ambiente: non incollare credenziali.

## Comandi usati (verificati)

| Comando | Effetto | Stato verifica |
|---|---|---|
| `/opt/data/bin/vercel --version` | versione CLI | eseguito → 65.17.0 |
| `/opt/data/bin/vercel deploy -y --no-wait --archive=tgz` | crea deployment preview, non attende il completamento | flag verificati con `vercel deploy --help`; **deploy non eseguito** in questa sessione (sola documentazione) |
| `/opt/data/bin/vercel alias set <deployment-url> 5etools-host.vercel.app` | punta l'alias stabile al deployment | sintassi verificata con `vercel alias --help`; esecuzione non effettuata |
| `/opt/data/bin/vercel alias ls --json` | elenca alias | verificato con `vercel alias ls --help`; esecuzione non effettuata |
| `/opt/data/bin/vercel ls -n 20` | elenca deployment recenti | verificato con `vercel ls --help` |
| `/opt/data/bin/vercel inspect <deployment> --logs` | log di build/diagnosi | verificato con `vercel inspect --help` |
| `curl -sI https://5etools-host.vercel.app/` | header HTTP di verifica | eseguito → 200, HSTS, `x-vercel-cache: HIT` |
| `git diff --cached --check` | controlla errori nel diff in staging | eseguito in repo |

## Deploy preview

```bash
cd /opt/data/5etools-host
git status --short
git diff --cached --check
/opt/data/bin/vercel deploy -y --no-wait --archive=tgz
```

- `-y` salta le prompt; `--no-wait` restituisce subito l'URL del deployment; `--archive=tgz` comprime il payload (evita di caricare l'albero completo).
- `vercel.json` ha `buildCommand: ""`, `outputDirectory: "."`, `framework: null`: non c'è una build da attendere, solo l'upload dei file statici.
- L'URL restituito è un deployment **preview**. Non è ancora pubblico sotto l'alias.

## Verifica prima di puntare l'alias

Attendere **10–15 secondi** dopo il deploy, poi:

```bash
curl -sI <deployment-url>/
curl -sI <deployment-url>/atlas.html
curl -s <deployment-url>/index.html | grep -o 'matchMedia([^)]*)' | head -1
```

Controllare: `HTTP/2 200`, `content-type: text/html`, `x-vercel-cache: HIT` (o `MISS` al primo accesso), HSTS, e che `index.html` contenga ancora il redirect mobile `matchMedia("(max-width:767px)") → location.replace("atlas.html")`.

Verifica del sito live:

```bash
curl -sI https://5etools-host.vercel.app/
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' http://5etools-host.vercel.app/
```

Atteso: `200` su HTTPS e `308` → HTTPS su HTTP. `www.5etools-host.vercel.app` **non** è un alias valido (errore TLS hostname mismatch): usare solo la root.

## Alias

```bash
/opt/data/bin/vercel alias set <deployment-url> 5etools-host.vercel.app
/opt/data/bin/vercel alias ls --json
curl -sI https://5etools-host.vercel.app/ | grep -iE 'HTTP/|etag|cache-control'
```

L'alias è la **fonte di verità**: la Production del progetto è vecchia e non va usata come riferimento. Non usare `vercel deploy --prod`: creerebbe un deployment nella Production, non collegato all'alias.

La propagazione può richiedere qualche secondo: se `curl` mostra ancora vecchi `etag`/`content-length`, ripetere dopo 10–15s.

## Rollback e deploy vecchi

Non esiste un comando di rollback verificato in questa sessione. La procedura è **ripuntare l'alias** a un deployment precedente:

```bash
/opt/data/bin/vercel ls -n 20                 # trovare l'URL del deployment buono
/opt/data/bin/vercel alias set <vecchio-deployment-url> 5etools-host.vercel.app
curl -sI https://5etools-host.vercel.app/
```

I deployment preview restano disponibili finché non scadono secondo la ritenzione del piano: `vercel ls -n 20` è il modo per trovarli. `vercel inspect <url>` mostra i dettagli di uno specifico deployment.

## Limiti e costi (Hobby)

- Piano **Hobby**: bandwidth mensile limitata (ordine di ~100 GB/mese) e ritenzione dei deployment limitata. Verificare sempre i valori correnti nella dashboard Vercel: i limiti possono cambiare.
- **Niente `img/` da ~7 GB**: la cartella è vuota e in `.gitignore`. Le immagini vengono da jsDelivr `5etools-mirror-3/5etools-img@main/` tramite `js/render.js` (`getMediaUrl`) e l’hook in `js/atlas-nav.js`. Non committare immagini locali.
- `.vercelignore` esclude `.git`, `node_modules`, `.DS_Store`, `*.log`, `Dockerfile`, `docker-compose.yml`.
- Nessun build step: il costo è soprattutto bandwidth, non compute.

## Errori comuni

- **Build resta "building"**: con `--no-wait` è normale vedere lo stato iniziale. Controllare con `vercel inspect <url> --wait --timeout 3m` e, se serve, `vercel inspect <url> --logs`. Se il deployment non completa, riprovare con un nuovo `vercel deploy -y --no-wait --archive=tgz`; **non** puntare l'alias a un deployment mai passato a `READY`.
- **404 su `sw-injector.js`**: il file è uno stub (`/* 5E Atlas: service worker disabled… */`) e deve restare presente: rimuoverlo fa comparire l'errore in console su tutte le pagine.
- **404 immagini**: verificare che il percorso usi l'CDN jsDelivr e il branch `@main`; non cercare file in `img/`.
- **Home sbagliata**: su mobile `/` deve portare ad `atlas.html`; su desktop deve restare il core. Il redirect è in `index.html:12`.
- **Alias non aggiornato**: ripetere `curl -sI` dopo 10–15s e controllare `vercel alias ls --json`.
- **`www.` non risolve**: usare `https://5etools-host.vercel.app/`.
- **Cache**: `cache-control: public, max-age=0, must-revalidate` è voluto: aggiornamenti immediati, ma ogni richiesta riconvalida. `x-vercel-cache: HIT` è il cache edge, non browser.

Tutti i comandi Vercel che richiedono auth sono riportati per completezza ma **non sono stati eseguiti** durante la stesura di questo documento.
