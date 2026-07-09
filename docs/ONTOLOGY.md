# OCCULTIMGDB — Data Ontology & Relational Model

The catalog is a graph: every **image** is the hub, linked outward to the dimensions you can browse by.
This document is the single source of truth for the fields, the controlled vocabularies, and how each
dimension surfaces in the website. Authoring conventions live in [`STYLE_GUIDE.md`](STYLE_GUIDE.md).

## The entities

| Entity | Source file | Key |
|---|---|---|
| **Image** (the catalog unit) | generated `data/catalog.json` (from `overrides.json` + image files) | `id` = `<work_key>__<slug>` |
| **Work** (a book / collection / corpus) | `scripts/config.py` + `data/works_extra.json` | `work_key` |
| **Creator / figure-as-maker** | `data/entities.json` → `creators[]` | `key` |
| **Tradition** | `entities.json` → `traditions[]` (controlled, see below) | slug |
| **Motif** | `entities.json` → `motifs[]` + free per-image tags | term |
| **Topic** (esoteric-historiography domain) | `data/topics.json` | `key` |
| **Collection** (curated journey) | `data/collections.json` | `key` |

Everything compiles to **`db/occultimgdb.db`** (SQLite) via `scripts/build_all.py` — never hand-edit the
`.db` or `catalog.json`.

## Image fields (the per-image record)

**Required, generated from the source registry:** `id`, `title`, `work` / `work_key`, `short_id`,
`creator`, `date`, `century`, `place`, `region`, `language`, `era`, `tradition`, `tier`, `seq`,
`rights`, `provenance_url`, `source_file`, `thumb`, `card`.

**Authored in `overrides.json` (the scholarship):**

| Field | Type | Purpose / browsing |
|---|---|---|
| `summary` | markdown | the essay (## Iconography / ## Significance / ## For artists) — see style guide |
| `motifs` | string[] | fine-grained iconographic tags → **Motif facet** + search |
| `medium` | enum (1) | material form → **Medium tab & facet** |
| `figures` | string[] | named people/deities/beings **depicted** (≠ creator) → **Figure-depicted facet** |
| `repository` | string | holding institution → shown on item page; provenance |
| `shelfmark` | string | MS/accession ref (e.g. `cod. 2372, fol. 35r`) → item page |
| `iconclass` | string[] | optional Iconclass notation → future systematic browsing |
| `citations` | {text,url}[] | bibliography → "Sources & further reading" |
| `key_concepts` | string[] | indexable concepts → links to faceted search |
| `summary_status` | `authored` \| `placeholder` | quality state |

## Controlled vocabularies

> **Values are exact slugs** — lowercase, underscored, no spaces or spelling variants. A single stray
> space silently forges a *phantom* facet bucket (e.g. `"early modern"` split 77 images off into a
> sixth era that the Timeline then rendered as real). Author the canonical value verbatim; don't invent
> near-variants. Lint after any authoring wave:
> `sqlite3 db/occultimgdb.db "SELECT DISTINCT era FROM images;"` (and likewise `tradition`, `medium`,
> `tier`) must return **only** the values listed here — anything else is a typo to fix at the source.

- **`era`** (chronology, 5): `antiquity` · `medieval` · `renaissance` · `early_modern` · `modern`.
  Date the image to the **surviving artwork/object**, not the lost original (a 1597 Witch of Endor is
  `early_modern`, even though the subject is biblical). Note the underscore: `early_modern`, never
  `early modern`.
- **`tier`** (eligibility outcome, 2): `illustration` — a whole illustration; the default browse — vs
  `page_scan` — book-furniture (bindings, text/title/index pages, blanks, annotation sketches) demoted
  out of the homepage/entity/gallery-default and revealed only by the gallery's "show scans" toggle.
  The [style guide](STYLE_GUIDE.md) Step-0 gate decides which; `page_scan` is how a not-quite-junk page
  is kept without polluting the artist-facing browse.
- **`tradition`** (the esoteric current, ~12): `alchemy` · `hermetic` · `rosicrucian` · `kabbalah` ·
  `goetia_grimoire` · `astrology` · `theosophy` · `reception` · `witchcraft` · `divination`. (`reception`
  = an occult/biblical/classical subject pictured by a later, non-esoteric artist.)
- **`medium`** (material form, 18): `manuscript` · `woodcut` · `engraving` · `etching` · `drawing` ·
  `painting` · `fresco` · `mosaic` · `sculpture` · `relief` · `gem` · `amulet` · `metalwork` · `ceramic` ·
  `textile` · `print` · `diagram` · `photograph`. Authored entries set it directly; older/placeholder
  items get an inferred value (`infer_medium()` in `build_catalog.py`) so the facet covers the archive.
- **`region`** (macro-geography): resolved from `place`/`region` free-text by `REGIONS` in
  `site/js/common.js` (Mediterranean & Near East · Italy · German Lands & Central Europe · England & the
  Low Countries · the Latin West & Beyond).
- **`figures`**: an open vocabulary of proper nouns DEPICTED (Hermes Trismegistus, Saturn, Lilith,
  Solomon, the Ouroboros-as-character …). Use the canonical English name; keep consistent spelling so the
  facet groups correctly.

## The relational browsing map (image → dimension → site surface)

| Dimension | Field(s) | Where you browse it |
|---|---|---|
| Chronology | `era`, `date` | **Timeline** tab · **Eras** tab · era pages |
| Geography | `region`/`place` | **Regions** tab · region pages |
| Esoteric domain | `tradition`, motifs, work | **Topics** tab (57 topics via `match{traditions,work_keys,motif_terms,ids}`) |
| **Material form** | `medium` | **Medium** tab · gallery **Medium** facet · item-page link |
| Maker | `creator`/`work_key` | **Figures** tab (creators) · creator pages |
| **Subject depicted** | `figures` | gallery **Figure-depicted** facet · item-page "Depicted:" links |
| Iconography | `motifs` | gallery **Motif** facet · item-page motif tags · search |
| Curation | curated `match` | **Collections** tab |
| Source corpus | `work_key` | gallery **Source-work** facet · work pages |
| Full text | all prose | global search (Explore + gallery) |

## How to extend

- **Add images:** author entries in `overrides.json` per the style guide → `build_all.py`.
- **Add a controlled value** (e.g. a new `tradition` or `medium`): add it to the vocab in this doc, to
  `MEDIA`/the tradition list, and the facet picks it up automatically (counts are data-driven).
- **Add a browsing dimension:** add the field to the entry schema (`AGENT_SOURCING_SPEC.md`), pass it
  through `build_catalog.py` + `build_db.py`, then add a facet (gallery `app.js`) and/or an Explore tab.
