# Brief per FigCraft — 5E ATLAS

Copia il testo qui sotto nel comando di progettazione/AI di FigCraft (o usalo come brief se generi i frame a mano).

---

Design a single, coherent interface for **5E ATLAS**, a D&D 2024 (5.5e) reference web app. Mobile-first at 390px, also desktop at 1440px. Do NOT mix two visual languages: take the *structure and reading experience* from Ruleholder, but create an original identity, not a clone.

## Identity
- Name: **5E ATLAS**. Mark: d20 outline with amber core.
- Palette: background `#0b0f14`, surfaces `#141a21` / `#1b232c`, text `#eef3f6` / `#b6c2cc`, primary accent amber `#f0a742`, secondary teal `#5fd0c0`, borders subtle `rgba(182,194,204,.16)`.
- Glow is allowed ONLY on accents, focus rings, active chips and hover states. Never behind body text. radius 14px.
- Typography: **Modesto Condensed** for big display and chapter titles, **Modesto** for section titles, **Mulish** for UI and metadata, **Lora** for long-form reading at 17px / 1.65. All fonts are self-hosted.

## Screens to produce
1. `01-home` — hero with curated fantasy art, short English copy, search pill, 3 core sourcebook cards (Player's Handbook 2024, Dungeon Master's Guide 2024, Monster Manual 2024), then a grid of 10–12 illustrated category cards (spells, monsters, magic items, equipment, classes, feats, backgrounds, species, bastions, glossary).
2. `02-catalog-spells` — one-column mobile list, rows at least 88px high with 56px thumbnail, search field, chip filters with 44px touch targets, "2024 core" active by default, count shown as e.g. "391 of 1,038 spells".
3. `03-detail-spell` — breadcrumb, title in Modesto, metadata shown once (no repetition), body in Lora, callouts and a table that fits 356px inside a 358px content area.
4. `04-reader-xphb` — single-article reader, bottom-sheet table of contents with 3 levels and an explicit "Close" control, a single previous/next stepper, readable tables, no static full index in the hamburger.
5. `05-mobile-home` — 390px version of the home with safe-area, no horizontal overflow.

## Rules
- English source text only. No Italian translation in this phase. Default ruleset is 2024, not 2014.
- Mobile-first: single column at 390px, touch targets 44px minimum, `:focus-visible` ring, safe-area insets.
- No duplicated metadata on detail pages. No phone frame mockup. No heavy textures.
- Illustrations as lightweight WebP, ideally under 100KB each.
- Components must be reusable: card, chip, callout, table, bottom sheet, stepper.

## Deliverables
Export the frames as PNG (and SVG where possible), keep the editable `.figcraft` source, and put everything in `design/` on branch `design/frames` of `hybrid-entree-art/5etools-host`. Add a short note listing frame names and any intentional deviation from this brief.
