# CATEGORY_AUDIT — copertura 2024

Audit delle collezioni JSON con record `XPHB`, `XDMG`, `XMM` confrontate con le categorie del prototipo. Le collezioni `fluff-*`, `foundry-*` e `bookData` sono state escluse perché duplicate, immagini o già lette dal renderer.

## Aggiunte in questo giro

| Categoria | Voci | Fonte |
|---|---:|---|
| Opzioni di classe | 58 | `optionalfeatures.json` |
| Lingue | 34 | `languages.json` |
| Divinità | 27 | `deities.json` |
| Abilità | 18 | `skills.json` |
| Maestria delle armi | 8 | `items-base.json` → `itemMastery` |
| Proprietà delle armi | 12 | `items-base.json` → `itemProperty` |
| Tesori (gemme/arte) | 11 | `loot.json` |
| Tipi di oggetto | 33 | `items-base.json` → `itemType` |
| Carte | 55 | `decks.json` |
| Gruppi leggendari | 23 | `bestiary/legendarygroups.json` |
| Armi e armature | +94 | `items-base.json` → `baseitem` |
| Oggetti magici (varianti + famiglie) | +57 | `magicvariants.json`, `items-base.json` → `itemEntry` |

## Categorie già presenti

Incantesimi 391 · Mostri 505 · Oggetti magici 641 · Equipaggiamento 218 · Classi 12 · Sottoclassi 48 · Talenti 77 · Background 16 · Specie 10 · Bastioni 35 · Glossario 225.

## Totale

**2.457 voci** in 20 categorie.

## Cosa resta fuori, e perché

- **Tabelle tesoro per fascia** (`loot.json` → `individual`/`hoard`, 8 record): non sono schede, sono tabelle di tiro. Sono già visibili nei capitoli del lettore.
- **`itemGroup`** (34): raggruppamenti merceologici, non voci singole; gli oggetti sono già nelle categorie.
- **`classFeature` / `subclassFeature`**: incorporati nel dettaglio di classi e sottoclassi, non duplicati come categoria.
- **`monsterFluff` / `spellFluff` / `itemFluff`**: descrizioni e immagini, non record di regole.
- **`foundry-*`**: conversione Foundry degli stessi record.
