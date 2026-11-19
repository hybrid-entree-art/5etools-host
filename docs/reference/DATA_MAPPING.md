# DATA MAPPING — 5e.tools JSON → 5E ATLAS catalogs

Scope: read-only analysis of `/opt/data/5etools-host/data/` for the ATLAS migration.
No `.tsx`/`.css` and no `src/app/(clone)/` file was modified. Counts below come from
actual `json.load()` + array lengths, not from filenames or estimates.

## 1. Correction to the source paths in the brief

Several filenames in the brief do **not exist** in this 5e.tools snapshot. The real
layout is:

| Brief name | Real path | Why |
|---|---|---|
| `spells.json` | `data/spells/spells-*.json` (19 files) | split by source |
| `bestiary.json` | `data/bestiary/bestiary-*.json` (114 files) | split by source; 98 more `fluff-bestiary-*.json` are enrichment |
| `equipment.json` | `data/items.json` → `item[]` filtered by `rarity === "none"` | mundane and magic gear share one array |
| `classes.json` | `data/class/class-*.json` (23 files) | one file per class |
| `species.json` | `data/races.json` (`race[]`, `subrace[]`) | "races" in 5e.tools |
| `glossary.json` | `data/book/book-{xphb,xdmg,egw}.json` sections + `data/conditionsdiseases.json` | glossary is embedded in book data |

Reproduce: `cd /opt/data/5etools-host/data && python3 -c "import json,glob; ..."`.

## 2. Verified record counts

| Catalog | Real source | Records | Unique (`name`+`source`) | Notes |
|---|---|---:|---:|---|
| Spells | `spells/spells-*.json` → `spell[]` | **1038** | 1038 | 19 source files |
| Monsters | `bestiary/bestiary-*.json` → `monster[]` | **4683** | 4683 | 114 source files |
| Items (all) | `items.json` → `item[]` | **2607** | 2607 | includes 127 `itemGroup[]` headers — skip, not entries |
| Equipment (mundane) | `items.json` → `item[]` where `rarity === "none"` | **787** | 787 | e.g. Abacus: `type:G`, `rarity:none` |
| Magic items | complement of the above | **1820** | 1820 | includes 51 unrated variants/artifacts (`Ashbringer (True State)`, `Cloak of Billowing`, …) |
| Classes | `class/class-*.json` → `class[]` | **43** | 43 | 23 files; 2014 + 2024 + UA + homebrew (e.g. Fighter appears 2×, Druid 3×) |
| Subclasses | `class/class-*.json` → `subclass[]` | **367** | 367 | separate catalog from classes |
| Feats | `feats.json` → `feat[]` | **317** | 317 | |
| Backgrounds | `backgrounds.json` → `background[]` | **175** | 175 | |
| Species | `races.json` → `race[]` | **177** | 177 | |
| Subspecies | `races.json` → `subrace[]` | **98** | 92 | 6 duplicate `name`+`source` pairs — dedupe before import |
| Bastions (facilities) | `bastions.json` → `facility[]` | **70** | 70 | |
| Glossary — rules | `book/book-xphb.json` → `Rules Definitions`, named entries | **155** | — | 159 array items incl. 1 intro string and section prose |
| Glossary — lore | `book/book-xdmg.json` → `Appendix A: Lore Glossary` | **74** | — | 75 array items = 74 named sections + 1 intro string |
| Glossary — EGW | `book/book-egw.json` → `Glossary` | **105** | — | plain strings beginning `{@b …}` |
| Conditions / diseases / statuses | `conditionsdiseases.json` | **64** | — | `condition:30`, `disease:29`, `status:5` — good seed for glossary cards |
| Books | `books.json` → `book[]` | **68** | 68 | matches 68 `book/book-*.json` files; chapters in `bookData[0].data[]` |

Item split check: `rarity:"none"` = 787; `rarity` present = 2556; `wondrous:true` = 993
(992 of them also carry rarity); no `rarity` = 51. `787 + 1820 = 2607`.

## 3. Fields to use (per catalog)

All records carry `name` and `source`; `page` is the print reference. Source codes are
short (`PHB`, `XPHB`, `XDMG`, `MM`, `TCE`, `EGW`, `XGE`, …). Description = first readable
element of `entries[]`; never concatenate the whole array for a card.

| Catalog | Name | Source | Type / taxonomy | Short description |
|---|---|---|---|---|
| Spells | `name` | `source` | `level` (0–9) + `school` | `entries[0]` (flatten tags) |
| Monsters | `name` | `source` | `type.type` (string or `{type,tags}`), `size`, `cr`, `alignment` | `entries[0]` when present; else `trait[0].entries[0]` or generated `"{cr} {size} {type}"` — `entries` missing on most records |
| Items / equipment | `name` | `source` | `type` (5e.tools codes: `G`,`M`,`HA`,`SC`,`WD|XPHB`,…), `rarity`, `wondrous` | `entries[0]`, fall back to `value`/`weight` for gear without prose |
| Classes | `name` | `source` | `hd`, `classFeatures[]`, `subclassTitle` | `classFeatures[0].name` or first `entries` string |
| Subclasses | `name` | `source` | parent class from filename (`class-<name>.json`) | first `entries` string |
| Feats | `name` | `source` | `category`, `ability`, `prerequisite` | `entries[0]` |
| Backgrounds | `name` | `source` | `ability` | `entries[0]` (26 records lack `entries`) |
| Species / subspecies | `name` | `source` | `size`, `ability`; subspecies inherit parent from `races.json` | `entries[0]` |
| Bastions | `name` | `source` | `level`, `prerequisite` | `entries[0]` (all 70 have it) |
| Glossary | `name` (section name) | book id from filename | book section / condition kind | first string in `entries[]` |
| Books | `name` | `source`/`id` | `group`, `published`, `author` | `contents[]` count as chapter metadata |

Field coverage (counts of records containing the field): spells 1038/1038 have
`level`, `school`, `entries`, `time`, `range`, `components`, `duration`; monsters only
4562/4683 have `page`, 3785 have `type`, 3495 have `cr`, 2940 have `trait`, 3576
have `action`; items 2556 have `rarity`, 2216 have `entries`, 1580 have `type`;
feats 317/317 have `entries`, 236 have `prerequisite`; backgrounds 149/175 have
`entries`; races 156/177 and subraces 90/98 have `entries`.

## 4. Slug convention for routes

Existing Ruleholder hrefs in `src/fragments/*.ts` use
`/{catalog}/{kebab-slug}` with a lowercase source prefix for non-core content:
`/spells/acid-splash`, `/feats/alert`, `/backgrounds/entertainer`,
`/classes/efa-artificer`, `/bastions/au-soup-kitchen`,
`/magic-items/rhw-brute-spirit`, `/sourcebooks/phb`.

Adopt the same shape:

```
/{catalog}/{slugify(name, source)}
slugify = lowercase(name).replace(/['’]/g,'').replace(/[^a-z0-9]+/g,'-')
          .replace(/^-|-$/g,'')
if source not in {PHB, XPHB, XDMG, XMM, MM}: prefix `${source.toLowerCase()}-`
if collision: append `-${source.toLowerCase()}` (and then `-2`, `-3` …)
```

Catalog segments: `spells`, `monsters`, `items`, `equipment`, `magic-items`,
`classes`, `subclasses`, `feats`, `backgrounds`, `species`, `bastions`, `glossary`,
`sourcebooks`. Route map mirrors `src/fragments/` names where they exist.

Collision risks to handle explicitly: 6 duplicate subspecies; 43 classes with
repeated names across sources (prefer `XPHB` for 2024, then `PHB` for 2014, hide UA
behind a source filter); 695 items with `reprintedAs` and 787 monsters with
`reprintedAs` — index the canonical record, keep reprints as aliases.

## 5. `{@…}` tag cleanup

5e.tools markup uses 29+ tag types. Counts observed in the main arrays (spells/monsters/items/classes/feats/backgrounds/races/bastions):

| Tag | Occurrences | Suggested handling |
|---|---:|---|
| `{@spell X}` | 14,435 | internal link `/spells/…` |
| `{@damage X}` | 11,429 | styled damage chip, text kept |
| `{@hit}` (6,093) + `{@h}` (5,667) | 11,760 | plain text/attack chip |
| `{@condition X}` | 7,342 | internal link `/glossary/…` |
| `{@dc X}` | 6,077 | plain text |
| `{@atk X}` (4,501) / `{@atkr X}` (1,146) | 5,647 | plain text / attack chip |
| `{@variantrule X}` | 4,629 | expand or link; do not leave raw |
| `{@item X}` | 3,057 | internal link `/items/…` |
| `{@dice X}` | 2,162 | plain text (keep notation) |
| `{@skill X}` | 1,882 | plain text / filter chip |
| `{@creature X}` | 1,301 | internal link `/monsters/…` |
| `{@action X}` | 1,078 | plain text |
| `{@book X}` (335) / `{@b X}` (230) | 565 | citation pill |
| `{@filter X}` | 528 | metadata only; strip from prose |
| `{@status X}` (495) / `{@sense X}` (645) / `{@quickref X}` (282) | 1,422 | plain text / glossary link |
| `{@table X}` (250) / `{@card X}` (118) / `{@scaledamage X}` (148) / `{@reward X}` (30) | 546 | strip wrapper or render as chip; keep inner text |

Rules: (1) parse with `/\{@([^}\s]+)([^}]*)\}/g`; (2) resolve cross-references via the
slug function above; (3) drop formatting-only wrappers but preserve their text;
(4) never render a raw `{@…}` token in ATLAS UI; (5) flag unresolved references for a
QA report instead of failing the build. Highest-density arrays: monsters 60,226 tags
over 4,683 records, items 8,333 over 2,607, spells 3,346 over 1,038.

## 6. Migration caveats

- 2014 and 2024 material coexist (`PHB` vs `XPHB`, `DMG` vs `XDMG`, `MM` vs `XMM`).
  ATLAS is 2024-first: default `source = XPHB/XDMG/XMM`, keep 2014 as secondary.
- `fluff-*.json` files (98 in `bestiary/`, 10 in `spells/`, plus `fluff-items.json` etc.)
  are enrichment for images/descriptions, not catalog records; merge by `name`+`source`.
- `generated/gendata-spell-source-lookup.json`, `gendata-subclass-lookup.json` and
  `generated/gendata-tag-redirects.json` are useful join tables for the slug resolver.
- Do not import `itemGroup[]` (127 headers) as entities.

**Deliverable status:** this file is the only artifact created. No source code changed.
