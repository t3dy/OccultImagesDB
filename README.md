# OCCULTIMGDB — The Occult Image Database

### 🔮 **Live site → https://t3dy.github.io/OccultImagesDB/site/index.html**

A browsable, scholarly-cataloged archive of **whole illustrations** from the occult, alchemical, and
esoteric tradition — emblems, woodcuts, engravings, cosmological diagrams, sigils, tarot, and portraits
from late antiquity through the modern occult revival. Every image is sourced from the public domain,
documented to encyclopedia depth, and **relationally hyperlinked**: image ↔ work ↔ creator ↔ tradition ↔
topic ↔ motif ↔ era.

Built as a **Digital Humanities resource** for artists, game designers, and researchers who need a sourced,
navigable map of the visual tradition — with clear provenance and a path to "where to learn more."

> The dragon devouring its tail, the king devoured by the wolf, the squared circle of the Stone, the
> witches' sabbath, the Tree of Life, Dürer's *Melencolia* — each catalogued as a complete image, with
> sourced scholarship and a downloadable public-domain scan.

---

## Why this exists

**Google Image Search is a nightmare and worse than useless for this material.** Search "ouroboros" or
"alchemical emblem" and you get a wall of Etsy listings, AI slop, Pinterest dead-ends, watermarked stock,
and pop-occult merchandise — with no provenance, no date, no source institution, no scholarship, and no way
to tell a 1617 engraving from a 2023 tattoo flash. The actual historical images are scattered across museum
IIIF servers, library digitizations, and Wikimedia Commons under inconsistent metadata, findable only if you
already know the exact title and artist.

This project is the corrective: a curated, **relationally browsable** catalog where every entry is a real
historical artwork, dated and provenanced, with a scholarly write-up and a verified public-domain source —
and where you discover images *by their place in the tradition* (by era, region, esoteric topic, figure, or
curated theme) rather than by guessing keywords into a black box.

---

## What's in it (current corpus)

| | |
|---|---|
| **918** catalogued images | every one with a scholarly summary |
| **31** works/collections | from Greek alchemical apparatus to *Thought-Forms* |
| **5** eras | Antiquity · Medieval · Renaissance · Early-modern · Modern |
| **10** traditions | alchemy · hermeticism · astrology · divination · kabbalah · goetia/grimoire · rosicrucianism · theosophy · witchcraft · classical reception |
| **16** creators | Maier, Fludd, Dürer, Dee, Lévi, Khunrath, Zosimos … |
| **11** topic domains · **13** curated collections | esoteric-historiography taxonomy mined from the maintainer's research databases |

Each entry carries: a sectioned essay (**Iconography** / **Significance** / **Reading**), a **bibliography**
of citations, indexable **key concepts**, **related entries**, and searchable **motifs** — all compiled into
a queryable database.

---

## How you browse it (UI / UX goals)

The homepage is **Explore** — a tabbed entry into the whole archive, seven ways in:

- **⏳ Timeline** — all images in chronological era-bands, antiquity → modern.
- **🜔 Eras** & **🌍 Regions** — cover-card grids into period and geographic pages.
- **📜 Topics** — the eleven esoteric-historiography domains (alchemy, hermeticism, witchcraft …), with
  forward-looking "coming soon" domains marked where the scholarship is mapped but images are still being sourced.
- **👤 Figures** — the creators and adepts.
- **✦ Collections** — curated thematic journeys (*The Great Work in Sequence*, *The Ouroboros Across Time*,
  *The Red King & White Queen*, *The Goetic Hierarchy* …).
- **▦ All images** — the full image-forward masonry with global search.

The interaction model targets the **modern comforts of a real image resource**:

- **Image-forward masonry** grid — the artwork leads, metadata appears on hover.
- **Lightbox with zoom & pan** — mouse-wheel / `±` / double-click to zoom, drag to pan, arrow-keys and `Esc`
  to navigate, loading a high-resolution (1400px) display image, with one click through to the full record.
- **Relational hyperlinking everywhere** — every creator, tradition, topic, motif, and era is a link, so you
  can wander the tradition laterally instead of dead-ending on a single result.
- **Faceted gallery** (preserved at `/site/gallery.html`) — filter by era / tradition / work for power users.
- **No accounts, no tracking, no JS framework, instant loads** — it's static files.

---

## Tech stack

Deliberately minimal and durable — a Digital Humanities resource should outlive its framework.

- **Frontend:** plain static **HTML / CSS / vanilla JavaScript** — *no build step, no framework, no
  dependencies*. The site is just files; it loads its data with `fetch()` and renders client-side.
- **Data authoring:** version-controlled **JSON** sources (`overrides.json` scholarship, `entities.json`
  relations, `topics.json` / `collections.json` taxonomy) — prose stays diffable and reviewable in git.
- **Build / pipeline:** **Python + Pillow** compiles the JSON sources into ① `catalog.json` (the browser feed,
  with generated thumbnail + card images) and ② `occultimgdb.db`, a normalized **SQLite** store.
- **Canonical store:** **SQLite** — ~21 normalized, indexed tables (`works`, `images`, `image_citations`,
  `image_relations`, `image_concepts`, `image_motifs`, `creators`, `traditions`, `topics`, `collections`,
  `wanted` …). Genuinely queryable: *"every image depicting an ouroboros across all works,"* *"entries ranked
  by citation count,"* per-era and topic-vs-have gap rollups.
- **Image sourcing:** a reusable **Wikimedia Commons / IIIF** fetch tool (`scripts/fetch_commons.py`) that
  queries the API, selects the highest-resolution public-domain original, downloads it, and writes a
  license/provenance sidecar.
- **Hosting:** **GitHub Pages** (static; serves the repo root so `/site` and `/data` are both reachable).

One command rebuilds everything: `python scripts/build_all.py`.

---

## Methodology — how the catalog is grown

The goal is coverage of *the whole history of occult imagery*, pursued by a repeatable, LLM-drivable
discovery pipeline rather than ad-hoc searching. The full plan is in [`RESEARCH_PLAN.md`](RESEARCH_PLAN.md);
in brief, five **discovery engines** feed one queue:

1. **Compendium harvest** — parse scholarly indexes (Obrist, Roob's *Alchemy & Mysticism*, Klossowski de
   Rola's *Golden Game*) into provenanced target lists. A scholar's plate-index *is* a coverage spec.
2. **Iconclass / Warburg enumeration** — walk the standard iconographic classification's codes for magic,
   witchcraft, astrology, divination, and biblical-magic scenes, turning "find everything" into "traverse a
   finite tree."
3. **Repository / IIIF crawl** — systematic sourcing from open-access museum and library APIs (Met & Rijksmuseum
   CC0, Wellcome, Gallica, e-codices …).
4. **Local-materials mining** — extract targets, shelfmarks, and plate-lists from the maintainer's own
   research PDFs and databases.
5. **Reception / edition tracing** — catalog a *subject* (e.g. the Isis mysteries of Apuleius's *Golden Ass*)
   through its later surviving depictions, dated to the artwork.

Every candidate runs a convergence loop: **propose → verify rights & provenance → source the best image →
author a full encyclopedia entry → de-duplicate → catalog.** Coverage gaps are tracked as first-class data in
a `wanted` table, so "what we don't have yet" is itself queryable.

**Authoring principles:** whole images only (no atomic element extraction); ≤5,000-word scholarly summary per
image; unknowns are marked `[PLACEHOLDER: …]`, **never invented**; rights are recorded per item.

---

## Quick start

```bash
# Serve the static site (no dependencies to run it)
python -m http.server 5179 -d .
#   → open http://localhost:5179/site/index.html

# Rebuild the catalog + database after editing data/ sources
python scripts/build_all.py     # → data/catalog.json + db/occultimgdb.db
```

Building/sourcing needs **Python + Pillow**. Running the site needs only a static file server.

## Repository map

| Path | Purpose |
|---|---|
| `site/` | the static website — `index.html` (Explore), `gallery.html` (faceted), `item.html` (detail), `entity.html` (profiles), `js/` (lightbox + masonry) |
| `data/` | **edit:** `overrides.json` · `entities.json` · `topics.json` · `collections.json` — **generated:** `catalog.json` · `works.json` |
| `db/` | `occultimgdb.db` — the canonical normalized SQLite store (compiled; query it, don't hand-edit) |
| `scripts/` | `build_all.py` (run this) · `build_catalog.py` · `build_db.py` · `fetch_commons.py` (image sourcing) |
| `sources_web/` | public-domain originals downloaded into the repo |
| `RESEARCH_PLAN.md` | the discovery methodology, engines, Iconclass codes, and coverage roadmap |
| `SCOPE.md` · `SOURCINGIMAGES.md` · `PROGRESS.md` | vision/corpus · sourcing log · append-only history |

## Rights

Underlying artworks are **public domain**. Digital scans carry the source institution's rights statement,
recorded per item; the catalog links back to each image's provenance URL. Confirm the per-item statement
before commercial use. Modern-era figures (e.g. Crowley, af Klint, Jung) are largely still in copyright and
are catalogued accordingly.

---

*A Digital Humanities project. Scholarship authored in version-controlled JSON, compiled to a queryable
database and a static site. Built with [Claude Code](https://claude.com/claude-code).*
