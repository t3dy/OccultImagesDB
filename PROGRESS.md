# OCCULTIMGDB — Running Progress Log

Append-only. Newest at bottom. This file is the durable record of what was done, so work is never
lost if a session ends mid-task. Each entry: date · phase · what shipped · where the artifact lives.

---

## [2026-06-27] Phase 0 — V1 site (prior session)
- Project scaffolded at `C:\Dev\OCCULTIMGDB\`. Static HTML/CSS/JS, no build step.
- `scripts/config.py` (source registry) + `scripts/build_catalog.py` (idempotent Pillow importer).
- Catalog built: **687 curated illustrations** across 8 works → `data/catalog.json`, thumbs + 1400px cards.
- Site: gallery (era/tradition/work/motif facets, motif search, sort, masonry), detail pages, about.
- **12 flagship Atalanta Fugiens** scholarly entries authored → `data/overrides.json`.
- Docs: `CLAUDE.md`, `SCOPE.md`, `HANDOVER_CURRENT.md`, `README.md`.
- Wiki: `wiki/project_occultimgdb.md` + index/log updated. Memory: `project_occultimgdb.md`.
- Verified via DOM eval (screenshots time out in this preview env — renderer quirk, not a bug).

## [2026-06-27] Phase 1 — autonomous build-out (in progress)
- Goal refined: a *search engine through the whole history of every extant occult image*, scholarly,
  sourced, relationally hyperlinked. Use local DBs/PDFs + web. Bake context-engineering into system files.
- Launched background survey of local scholarly DBs/PDFs/metadata for catalog fuel.

### 1a. Context-engineering baked into system files
- `CLAUDE.md` — added "Working in this repo as an agent" (layered context reads, persist-every-step,
  Deckard seam, idempotence, cross-session memory pointers).
- New `CONTEXT.md` — 30-second orientation packet (token-efficient entry point).

### 1b. Relational hyperlinking layer (the "search engine through the whole history" vision) — DONE
- `data/entities.json` — hand-authored: 7 creators, 6 traditions, 6 motifs, with `[[type:key]]`
  cross-links + "learn more" external scholarly links. Durable.
- `site/entity.html` + `js/entity.js` — generic profile renderer for creator/work/tradition/motif/era;
  resolves `[[…]]` links, shows related entities + that node's images.
- `site/browse.html` — "Themes & Figures" directory (era/tradition/figure/motif/work tiles).
- `site/history.html` — chronological timeline walk (eras → work nodes → thumbnails).
- Importer now emits `creators_index` (work→creator). `item.html` facts link work/creator/era/tradition
  into the graph. Nav (Themes/History) added across pages.
- Verified via DOM: Maier profile resolves cross-links + 51 imgs; browse 29 tiles; history 8 nodes/64 thumbs; no console errors.

### 1c. Local-source survey result (see SOURCINGIMAGES.md for full detail)
- Found `C:\Dev\AlchemyBeatEmUp\staging\raw_images\` — ~262 illustration scans organized BY TEXT,
  incl. Aurora Consurgens (30, medieval), Geber Summa (25), Mutus Liber (11), Ripley Scrolls (16),
  Lambsprinck (20, ouroboros), Agricola De Re Metallica (14, furnaces), Biringuccio, Glauber, Libavius,
  Symbola Aureae Mensae (34). Extends corpus into medieval + new early-modern works.
- Found rich per-image scholarly metadata: `Claudiens/site/data.json` (50 Atalanta emblems w/ discourse +
  nigredo/albedo/rubedo stage + sources), `TheosophicalAlchemyDB` Maier metadata (De Jong cites),
  `EmblemPrintShop/data/motifs.json` (200+ motif ontology). SQLite DBs (renmagic 155MB, pico 93MB,
  emerald 6.7MB, medieval_magic) available for deep context (lower priority).
### 1d. Corpus expansion + scholarship import — DONE
- `scripts/config.py` — added 2nd image root (`ALCHEMY_BEU_ROOT`) + 10 new "illustration" works from
  `AlchemyBeatEmUp` (Aurora Consurgens, Geber, Ripley, Lambspring, Mutus Liber, Symbola Aureae, Agricola,
  Glauber, Libavius, Biringuccio). Importer resolves per-source `root`.
- `scripts/import_local_scholarship.py` — folds `Claudiens/site/data.json` discourse + `EmblemPrintShop/
  data/emblems.json` motif catalog into `overrides.json`. Preserves hand-authored (source!=import).
- `data/entities.json` — added creators (pseudo-Geber, George Ripley, Agricola); linked Symbola to Maier.
- **Catalog now: 898 images · 18 works · 3 eras (medieval 55 / renaissance 389 / early-modern 454) ·
  51 authored summaries (full Atalanta set).** Medieval stratum now present.
- `SOURCINGIMAGES.md` written (requested deliverable): what's sourced, local material mined vs untapped,
  prioritized next-images plan, where-to-source reference, next-5-actions.
- Verified: history timeline shows Medieval→Renaissance→Early-modern (18 nodes); imported emblems carry
  discourse + motif tags; furnace search hits 236.
- NOTE: imported Claudiens discourse occasionally has minor source-text artifacts (e.g. "the the me");
  each imported record carries a `[PLACEHOLDER: cross-check de Jong]` flag for human review.

### 1e. Motif ontology → relational motif pages — DONE
- `scripts/import_motifs.py` promotes 14 motifs from `EmblemPrintShop/data/motifs.json` (sourced
  iconographic descriptions + alchemical valence + planetary) into `data/entities.json` motif profiles,
  preserving the 6 hand-authored ones. Now **20 motif pages** (king, queen, lion, serpent, sun, moon,
  tree, bird, vessel, star, fountain, peacock, angel, sword + the 6 hand). Each has a `match` alias list.
- `entity.js`: motif image-matching honours the `match` field; link-resolver made block-aware so
  `## headings` render in entity summaries.
- Coverage varies by per-image tagging (sun 59, vessel 39, tree 31, bird 21 strong; king/lion/serpent
  sparse — flagged in SOURCINGIMAGES.md as the per-image-tagging gap). Pages render gracefully at 0.

### 1f. Scholarly citations + related-emblem links — DONE
- `import_local_scholarship.py` enrichment pass adds (additive, safe for hand-authored): **De Jong page
  citations** + **related-emblem cross-links** + **key-concepts** (from `TheosophicalAlchemyDB`, emblems
  1–20) + a per-emblem **Furnace & Fugue** digital-edition link for all 50. 50 records enriched.
- `item.js` renders a "scholarly apparatus" block: Key concepts (→ search), Related emblems (→ item
  cross-links), Sources & further reading (citations + external links). `style.css` styled.
- Verified: emblem-01 shows De Jong pp.58–63, F&F link to emblem1.html, related emblems 2/5/33/34,
  key concepts. No console errors.

### 1g. Antiquity stratum — web-sourced (the headline gap) — DONE
- Added a 3rd image root (`LOCAL_SOURCED_ROOT` → `sources_web/`) for public-domain web downloads.
- Downloaded (curl via Wikimedia `Special:FilePath`, PD Mark 1.0): the **Chrysopoeia of Kleopatra
  ouroboros** (MS Marciana gr. Z. 299) and the **1478 Theodoros Pelekanos coloured ouroboros**
  (Cod. Paris. gr. 2327) → `sources_web/antiquity/`.
- Registered the "The Ouroboros — Earliest Witnesses" collection (era=antiquity); authored both images
  with true titles/creators/provenance + scholarship in `overrides.json`.
- **The timeline now spans all four eras: Antiquity → Medieval → Renaissance → Early modern.** The
  user's headline example ("the first image of the ouroboros") is the literal first node. Web-sourcing
  pipeline proven end-to-end (download → register → author → build → render with provenance link).

### 1h. Figures + grimoire stratum — web-sourced — DONE
- Web-sourced (PD, Wikimedia): the **Ashmolean Portrait of John Dee** → `sources_web/figures/`, and
  the **Magic Circle & Triangle of King Solomon (Goetia)** → `sources_web/grimoire/`. Registered as
  "Portraits of the Adepts" + "Grimoire & Goetia Plates" collections; authored both.
- Added **John Dee** creator entity (his page surfaces the portrait; cross-links to alchemy + kabbalah).
  The `goetia_grimoire` tradition page now has a real plate.
- **All FIVE of the user's named example types are now in the archive:** Atalanta emblems · Portrait of
  John Dee · Solomonic magic circle · Chrysopoeia ouroboros · (+ the wider corpus).
- Caught & fixed an id-slug bug (overrides used `_`, importer slugifies to `-`); both merged after fix.

## State checkpoint (end of Phase 1)
**902 images · 21 works · 4 eras (antiquity→early-modern) · 55 authored summaries · 50 with De Jong/F&F
citations + related-emblem links · 20 motif pages · 14 creator + 6 tradition pages · full relational
entity/browse/history layer · web-sourcing pipeline proven (3 image roots).** All artifacts on disk;
site verified via DOM, no console errors.
Remaining phases queued in `SOURCINGIMAGES.md` §6 + `HANDOVER_CURRENT.md` (more antiquity + grimoire
plates, Splendor/Rosarium plate authoring, per-image motif tagging, page-scan curation, deploy).

## [2026-06-27] Phase 2 — dedicated database + per-period sourcing

### 2a. Canonical SQLite database — DONE
- `scripts/build_db.py` compiles `db/occultimgdb.db` from `catalog.json` + `entities.json`. Normalised
  schema (16 tables): `works`, `images`, `image_motifs`, `image_citations`, `image_relations`,
  `image_concepts`, `creators`/`creator_works`/`creator_links`, `traditions`/`tradition_links`,
  `motifs`/`motif_terms`/`motif_see_also`, indexed. Canonical, queryable store. `--stats` prints summary.
- Authoring model documented in `CLAUDE.md`: prose authored in JSON sources → compiled to catalog.json
  (browser) + occultimgdb.db (canonical). Do not hand-edit the DB.
- `scripts/build_all.py` wrapper runs the whole pipeline (imports → catalog → db) in order.
- Verified: cross-work motif joins, citation/concept counts, per-era rollups all query correctly.

### 2b. Per-period image sourcing + deep academic entries — DONE (ongoing)
- Web-sourced (PD, Wikimedia): **Zosimos distillation apparatus** (antiquity → `sources_web/apparatus/`)
  and **Fludd's *Integrae Naturae* Great Chain of Being** (early-modern → `sources_web/cosmology/`).
- Added **Robert Fludd** creator entity. New works: "Greek Alchemy — Apparatus & Diagrams",
  "Cosmological Diagrams".
- Both authored as full encyclopedia entries: multi-section summaries (Iconography / Significance /
  Reading) + **bibliographic citations** (Berthelot, Taylor, Godwin, primary sources) + key-concepts +
  specific motifs. This is the "document as much academic info as we can" model in practice.
- **Now: 904 images · 23 works · 4 eras · 57 authored · 76 citations · 12 creators.** Antiquity era now 2.

### State checkpoint (end of Phase 2)
DB-backed catalog (`db/occultimgdb.db`) + 904 images/23 works/4 eras + 57 deep academic entries + the
relational site. All compiled via `build_all.py`.

## [2026-06-27] Phase 3 — Explore frontend (tabbed database viewer)

### 3a. Esoteric-historiography taxonomy (mined from the user's DBs) — DONE
- Background agent mined RenMagDB/HermeticDB/MedievalMagicDB/PicoDB/TheosophicalAlchemyDB/GoetiaRevEng →
  11 topic domains, region/period vocabularies, key figures, 12 curated-collection ideas.
- `data/topics.json` — 11 topics (alchemy, hermeticism, ceremonial/goetia, rosicrucian = live;
  kabbalah, natural magic, astrology, neoplatonism, enochian, witchcraft, divination = coming_soon with
  `needs` sourcing notes). Each has match-rules + subthemes + figures + links.
- `data/collections.json` — 12 curated collections (6 live: Atalanta opus, Ouroboros-across-time,
  Coniunctio, Laboratory-revealed, Hermetic-cosmos, the Rebis; 6 coming_soon: Goetic hierarchy, Chymical
  Wedding, Kabbalah, Neoplatonic cosmos, Medieval grimoires, Witch trials — each with a `needs` roadmap).

### 3b. Tabbed Explore homepage + lightbox — DONE
- Per user decisions: **Explore is the new homepage** (`index.html`); old faceted gallery moved to
  `gallery.html`. **Forward-looking taxonomy** (empties shown "coming soon"). **Image-forward masonry**.
  **Lightbox + zoom/pan** as the headline convenience.
- `js/common.js` (shared): constants, `imageMatches`, region mapping, image-forward `renderMasonry`,
  and the **Lightbox** (wheel-zoom, drag-pan, dbl-click, arrows/esc/±, prev-next, "open full record").
- `index.html` + `js/explore.js`: 7 tabs — Timeline (chrono era-bands) · Eras · Regions · Topics ·
  Figures · Collections · All-images — plus global search. Category cards with covers + counts +
  coming-soon badges.
- Extended `entity.js`/`entity.html` to render `type=topic|region|collection` profiles (with the
  masonry+lightbox) and load topics/collections. Nav updated across all pages (Explore/Gallery/Themes/
  History/About).
- `build_db.py` now ingests topics + collections (5 new tables). DB: 11 topics (4 live), 12 collections
  (6 live).
- Verified via DOM: 904-image timeline, all 7 tabs, lightbox opens 1400px image, topic/collection/region
  entity pages, coming-soon roadmap notes, faceted gallery preserved. No console errors.

## [2026-06-27] Phase 4 — research plan for "everything occult"

### 4a. RESEARCH_PLAN.md — DONE (toolkit section pending agent)
- Candid coverage reality-check (~904 imgs, ~95% alchemy; near-zero on the user's named gaps).
- The "universe of occult imagery" mapped on 3 axes: subject domains (alchemy→spiritualism→Masonic→
  biblical-magic), periods (antiquity→modern), media/objects (books→gems→tarot→regalia→instruments).
- Blind spots surfaced: Iconclass/Warburg classification, reception-vs-origin (Apuleius), the bible as
  occult image-source, objects beyond the page, compendia-as-wanted-lists, the image-vs-witness model,
  rights as first-class data, our own DBs' unmined shelfmarks.
- 5 discovery ENGINES (compendium-harvest · Iconclass/Warburg enumeration · IIIF/repository crawl ·
  local-materials mining · reception tracing) + a convergence loop (propose→verify→source→author→dedup→
  catalog). Scope dials for the user. Prioritized roadmap (Obrist + Geheime Figuren + witchcraft first).
- Launched a background research agent to populate §4 (repositories, Iconclass codes, local leads).

### 4b. data/wanted.json — discovery queue (machine-actionable) — DONE
- 33 seed targets across every gap & period (Apuleius/Isis, Obrist corpus, Geheime Figuren, witchcraft
  woodcuts, Goetia 72 seals, biblical-magic scenes, Gnostic gems, PGM, tarot history, Children of the
  Planets, zodiac man, Sephirotic trees, Dee's Monas/Sigillum, Dürer Melencolia, Lévi Baphomet, Thought-
  Forms…). Schema: {id,title,subject,topic,period,via,why,candidate_sources,rights,status,engine}.
- `build_db.py` ingests it → `wanted` table (DB now 22 tables). Gap report is queryable
  (`SELECT topic,COUNT(*) FROM wanted GROUP BY topic`). Engines append rows; convergence loop advances status.

### 4c. RESEARCH_PLAN §4 toolkit — COMPLETE
- Research agent's findings folded into §4: §4A repositories (Met/Rijksmuseum CC0 no-key, Wikimedia,
  IA, Wellcome/Gallica/e-codices/Bodleian IIIF, Getty, Warburg, Ritman, Princeton Index, Campbell Bonner
  gems) · §4B verified Iconclass codes (13/13B/14/24C21/49E39/71H31/73F215365…) · §4C local leads
  (obrist_medieval = Obrist's 2 books as page-scans → OCR for shelfmarks; EmeraldTablet's empty
  `manuscripts(shelfmark,repository,image_folder)` schema to adopt; Szulakowska/Zika/Yates PDFs to harvest).

## [2026-06-27] Phase 5 — populate DB + website (Engine 3 in action)

### 5a. Reusable Commons sourcing tool — DONE
- `scripts/fetch_commons.py` — queries the Wikimedia Commons API, picks the best-quality PD original,
  downloads it + writes a `.prov.json` sidecar (license/artist/source URL). Jobs in `fetch_jobs*.json`.
  This is Engine 3 operationalised.

### 5b. 14 new entries across the gaps — DONE
- Sourced (all PD, mostly hi-res) + authored full encyclopedia entries (Iconography/Significance +
  bibliography + key-concepts per template): **Lévi's Baphomet · Besant/Leadbeater Thought-Forms ·
  Dürer's Melencolia I · Children of the Planets (Mars) · the Sephirotic Tree · RWS Magician & High
  Priestess · a Visconti-Sforza trump · Baldung's Witches' Sabbath · van Oostsanen's Witch of Endor ·
  Dee's Monas Hieroglyphica · a Geheime Figuren plate · Fludd's Divine Monochord · Astaroth (Dict. Infernal).**
- 8 new works registered (tarot, witchcraft, kabbalah, astrology, enochian, rosicrucian_plates,
  biblical_magic, revival) + 2 added to existing (cosmology, grimoire_plates).
- Flipped topics live: kabbalah, astrology, witchcraft, divination, enochian (now **9 of 11 live**).
  Flipped collections live + added Tarot collection (now **10 of 13 live**). 13 queue items → cataloged.
- **Catalog now: 918 images · 31 works · 5 ERAS (antiquity→modern) · 71 authored entries · 10 traditions**
  (alchemy/reception/hermetic/rosicrucian/divination/goetia/astrology/kabbalah/theosophy/witchcraft).
- Verified: new item pages render full apparatus (1382px image, sections, citations, relational links);
  modern era live on the timeline; Topics tab shows 9 live; search hits baphomet/tarot/witch/sephiroth.
  No console errors. Coverage is no longer ~95% alchemy — the occult breadth has genuinely begun.
