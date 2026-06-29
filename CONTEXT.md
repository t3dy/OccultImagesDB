# CONTEXT.md — 30-second orientation packet

> Token-efficient entry point. Read this first; descend into the linked files only as the task needs.
> (Layered-retrieval principle: cheap summary here → richer detail on demand.)

**What:** OCCULTIMGDB / "Occult Image DB" — a static website that is a *search engine through the
whole history of occult & alchemical imagery*. Every entry is a **whole illustration** (emblem,
woodcut, diagram, portrait), scholarly-catalogued, downloadable, and **relationally hyperlinked**
(image ↔ work ↔ creator ↔ tradition ↔ motif ↔ era).

**Why:** Google image search is a nightmare for this material. We give artists, game designers, and
researchers a sourced, navigable map of the tradition with clear provenance and "where to learn more."

**Hard constraints:**
- Whole images only — **no** atomic element extraction (that's EmblemPrintShop's job, not ours).
- Plain static HTML/CSS/vanilla JS — **no build step**.
- ≤5,000 words scholarly summary per image; mark unknowns `[PLACEHOLDER: …]`, never invent.

**State (see HANDOVER_CURRENT.md for live detail):** V1 = 687 curated illustrations, 8 works, 12
authored scholarly entries; ~3,000 more page-scan images registered behind `--all`. Antiquity/grimoire
stratum named but not yet sourced (see `SOURCINGIMAGES.md`).

**The files you edit to grow the catalog:**
- `scripts/config.py` — source registry (add a book/collection + its image root here).
- `data/overrides.json` — per-image encyclopedia scholarship: `summary` (## Iconography / ## Significance),
  `citations` (bibliography), `key_concepts`, `motifs`. Merged by `id` (use hyphens — importer slugifies).
- `data/entities.json` — creators / traditions / motifs (the relational layer).
Then run `python scripts/build_all.py` → rebuilds `data/catalog.json` (browser) **and**
`db/occultimgdb.db` (the canonical, queryable SQLite store). Never hand-edit the `.db` or `catalog.json`.

**Map:**
| File | Purpose |
|---|---|
| `CONTEXT.md` | this packet |
| `CLAUDE.md` | architecture + agent working rules |
| `SCOPE.md` | vision, corpus, roadmap, human-sourcing TODO |
| `SOURCINGIMAGES.md` | what's been sourced + next images to pursue |
| `HANDOVER_CURRENT.md` | live state + next actions |
| `PROGRESS.md` | append-only history |
| `scripts/` | `config.py` registry · `build_all.py` (run this) · `build_catalog.py` · `build_db.py` · `import_*` |
| `data/` | edit: `overrides.json` · `entities.json` · `topics.json` · `collections.json` — generated: `catalog.json`/`works.json` |
| `db/` | `occultimgdb.db` — canonical normalised SQLite store (compiled; query, don't edit) |
| `sources_web/` | public-domain images downloaded into the repo (`root:"LOCAL"`) |
| `site/` | `index.html` = **Explore** (tabbed: timeline/era/region/topic/figure/collection) · `gallery.html` = faceted gallery · `item.html` detail · `entity.html` profiles · `js/common.js` (lightbox+masonry) |

**Run:** `python -m http.server 5179 -d C:/Dev/OCCULTIMGDB` → `http://localhost:5179/site/index.html`
