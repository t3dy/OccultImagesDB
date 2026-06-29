# OCCULTIMGDB — Current State

**Last updated:** 2026-06-27
**🌐 DEPLOYED LIVE: https://t3dy.github.io/OccultImagesDB/** — repo is git-tracked and pushed to
`github.com/t3dy/OccultImagesDB`; GitHub Pages serves the repo root (root `index.html` redirects to
`/site/`). Redeploy = commit + `git push origin main` (Pages rebuilds automatically in ~1–2 min).

**Status:** V9 (2026-06-29) — **2,768 catalogued · 2,452 curated illustrations (316 text-pages/junk hidden
as `tier:page_scan`) · 121 works · 57 topics · ZERO placeholders (every illustration has a curatorial
essay).** This session: (a) **Hellmouth** medieval gallery added; (b) sourcing — Apuleius/Isis, Symbolist
occult, Asian cosmology, Art of Memory, Christian theosophy, wish-list fills (Behenian star-seals, Splendor
Solis plates, Sola-Busca, Joachim); (c) **full documentation audit** — authored essays for ALL placeholder
emblem-books (Splendor Solis, Mylius, Stolcius, Hypnerotomachia, Khunrath, Cramer, Aurora, Symbola, Geber,
Biringuccio, Rosarium, Mutus Liber, Ripley, Lambspring, Agricola) in a witchcraft-museum curatorial voice,
with TRIAGE: text/index/binding pages and Google-Books "page-not-available" junk demoted to `tier:page_scan`
(hidden from homepage + entity + gallery-default; the gallery's "show scans" toggle still reveals them);
(d) **figures** facet backfilled 50→688 (infer_figures from title in build_catalog); (e) **two-level emblem
viewer** — gallery.html + app.js `groupBy` toggle "View: individual emblems | emblem books" (?view=books);
(f) alchemy **coverage audit** vs C:\Dev\Claudiens (atalanta.db), C:\Dev\ALCHEMYTIMELINEMAP, C:\Dev\
TheosophicalAlchemyDB — comprehensive, every illustrated emblem-cycle held. **GOTCHA:** doc agents that
fan-out into sub-agents blow the session limit — run ONE agent per work. **Cleanup candidate:** `glauber_furni`
+ `libavius_alchymia` are text-only scans (all demoted; libavius has 18 broken Google-Books cards) — consider
deleting outright. Earlier V7 notes below.

**Status:** V7 — **deployed; 2,470 images · 108 works · 56 topics ALL LIVE · 1,566 authored entries.** Many
sourcing waves added (each = 6 parallel agents): St Cyprian, mesmerism, occult botany, Fortune & Fate,
Enochian/Dee, the alchemist's lab; Bosch/Bruegel, Paracelsian elementals, lot-books, astrological medicine,
secret societies, the undead; prophecy figurae (Joachim/Vaticinia/Nostradamus), the Temple as cosmos
(Villalpando), Kircher's universal knowledge, the music of the spheres, cosmic machines (astronomical clocks),
Byzantine/Jewish amulets. **Gotcha fixed:** museum masters can be >100MB (over GitHub's limit) — `fetch_commons.py`
now auto-caps downloads to a 3500px long edge (`cap_size()`), and a one-time pass downsized 69 existing
oversized originals (~2GB saved). `fetch_iiif.py` exists for non-Commons IIIF but **Gallica is Cloudflare-IP-blocked**
(Boderie diagram + Ilanot scrolls remain queued for a user browser session).

**V8 — ONTOLOGY + LIBRARY SOURCING (2026-06-28).** ~2,601 images / 114 works / 57 topics. **Enriched
metadata model** (see `docs/ONTOLOGY.md` + `docs/STYLE_GUIDE.md`): every entry now carries `medium`
(18-term vocab), `figures` (named beings depicted ≠ creator), `repository`, `shelfmark`, optional
`iconclass`. Wired through `build_catalog.py` (`infer_medium()` backfills medium → 100% coverage) +
`build_db.py` (new columns + `image_figures` table). **Front-end:** new **Medium** Explore tab; gallery
**Medium** + **Figure-depicted** facets; item page shows Medium/Repository/Shelfmark + a "Depicted:" line.
**Bug fixed:** motif/key-concept tag links now point at `gallery.html` (were `index.html`, which ignored the
params — they were dead). Explore honors `?q=`. The 5 newest domain-works: fludd_works (40), neoplatonism,
renaissance_magic_deep, islamicate_deep, lettrism.
- **Browser/IIIF sourcing** (for items not on Commons): `scripts/fetch_iiif.py` + a connected Chrome browser
  (Chrome MCP). PROVEN on the **Heidelberg open IIIF library** (`digi.ub.uni-heidelberg.de/diglit/iiif/cpgNNN/manifest`)
  → sourced the *Heidelberger Schicksalsbuch* (cpg832, work `heidelberg_mss`). **RIGHTS CAVEAT:** open libraries
  are reachable (BSB `digitale-sammlungen.de`, Heidelberg) — unlike Cloudflare-blocked Gallica — BUT most
  digitisations are **NC-restricted** (BSB = `NoC-NC`) and unfit for our free-assets catalog. **Heidelberg is
  true Public Domain Mark** → usable. Rule: browser-source ONLY PD/CC0/CC-BY IIIF, record the real rights.

**REPO MANAGEMENT (important):** the published GitHub Pages tree must stay under **1 GB**.
- `sources_web/` (high-res originals, ~3.5GB) is **gitignored / local-only** — re-sourceable from each item's
  provenance URL; the site never needs it (it serves the 1200px `site/images/cards` + `data/`). Keep it on
  disk for `build_catalog`; do NOT re-add to git.
- Cards are **1200px** (`CARD_MAX` in `build_catalog.py`); `site/images` ≈ 717MB. When it nears ~900MB,
  lower `CARD_MAX` again and re-derive, OR move images off-repo. `fetch_commons.py` auto-caps source
  downloads to 3500px (`cap_size()`).
- **History was squashed to a single commit** (2026-06-28) to reclaim ~3.5GB of large-blob bloat. The remote
  `.size` may still report ~5GB until GitHub's background GC reclaims the orphaned objects (can take hours/
  days; harmless — Pages publishes the ~740MB current tree). Local `.git` was `git gc`'d.

**Prior (V6):** 2,143 images · 90 works · 40 topics · 1,239 authored entries. Cards
show a **brief description** (markdown-stripped summary lede) under each image — `briefDesc()` in
`site/js/common.js`, always-visible `.mcard-cap` (was hover-only). Recent works added: the 72 Goetia seals,
tarot (historic + decks), astrological figures/decans, hermetic Egypt, sacred geometry, Mesoamerican codices,
emblemata, Ripa's Iconologia, theosophy, the esoteric bestiary, portents/Book-of-Miracles, physiognomy,
Renaissance hieroglyphs, the Voynich & ciphers, African divination, Christian apotropaic charms, talismanic
astrology (kameas/lunar mansions), celestial portents. **Gallica is Cloudflare-hard-blocked** (CAPTCHA/IP
block — can't be bypassed) so the **Boderie 1578 three-worlds diagram** and the off-Commons **Ilanot scrolls**
remain queued in `wanted.json` with exact source leads (need an un-flagged browser session, not this pipeline). Latest sourcing: the **72 Goetia seals**
(work `goetia_seals`, 47 + composite, via fetch_svg/fetch_commons), plus a gap-fill wave — `tarot_historic`,
`astrological_figures` (decans, Children of the Planets), `hermetic_egypt` (Mensa Isiaca, Kircher, Roman
obelisks), `sacred_geometry` (Vitruvian man, Platonic solids, Kepler), `mesoamerican_divination` (Codex
Borgia/Dresden), `emblemata` (Alciato/Ripa/frontispieces). New tools: `scripts/fetch_svg.py` (rasterizes
SVG-only Commons sigils/diagrams via svglib+reportlab) and `scripts/fetch_iiif.py` (Gallica/e-codices/NLI
IIIF — note Gallica 403-blocks bots, needs browser-session cookies). Still queued in `wanted.json` (genuinely
off-Commons): the **Boderie 1578 three-worlds/32-paths diagram** (Gallica ark:/12148/bpt6k8584280 — bot-blocked)
and the **Ilan/Ilanot tree scrolls** (NLI/Braginsky).

**Prior (V5):** Latest pass (user-requested deep-dive on
the Solomonic/grimoire + Kabbalah seams): 8 new works — solomonic_tradition, magical_characters (PGM
charaktêres + magical alphabets), grimoire_spirits, magicians_at_work, tree_of_life, sefer_yetzirah,
christian_cabala, seals_sigils. **ceremonial-goetia topic 77→176 imgs, kabbalah 39→104.** New tool
`scripts/fetch_svg.py` rasterizes SVG-only Commons files (planetary seals, Pentagrammaton, Goetia sigils)
via svglib+reportlab — use for any vector sigil/diagram fetch_commons skips. User-named gaps queued in
`wanted.json`: the Boderie 1578 three-worlds/32-paths diagram (Crofton Black Pico cover; PD on Gallica
ark:/12148/bpt6k8584280, locate folio via IIIF), the Ilan/Ilanot tree scrolls (NLI/Braginsky, not on
Commons), the full 72 Goetia seals + Venus/Moon planetary seals (SVG on Commons → fetch_svg.py). Coverage is no longer alchemy-heavy: 32 new domain-works added in 5
parallel agent waves (+621 images, all authored) — the ancient world (Greco-Egyptian magic, magical &
Gnostic gems, incantation bowls, Egyptian funerary magic, ancient zodiac & Mithraic cosmology, mystery
cults), medieval (astrology, grimoires, cosmological diagrams, sacred architecture, Jewish mysticism),
renaissance/early-modern (learned magic, demonology, witch prints, Rosicrucian/Hermetic, divination,
magical OBJECTS, celestial cartography, biblical & classical reception), and global/cross-tradition
(Islamicate, Norse/Germanic, Gnostic-Hermetic, Freemasonry, spiritualism, Asian esoterica) plus the
visionary/apocalyptic/macabre/folk/occult-revival/visionary-alchemy seams. Obrist research + full French
translations live at `E:\pdf\Obrist\` (outside the repo).

**Campaign mechanics (reusable):** `scripts/AGENT_SOURCING_SPEC.md` = the per-agent brief;
`scripts/fetch_commons.py` = Wikimedia sourcing tool; each agent wrote `data/overrides_batch_<key>.json`
+ a `_work` block; `scripts/merge_batches.py` folds batches → `data/works_extra.json` (config.py
auto-loads it) + `data/overrides.json` with id/orphan validation. To add more: spawn agents per the spec,
then `merge_batches.py` → `build_all.py`. Canonical **SQLite database** `db/occultimgdb.db` (now 1,543
images, 1,715 citations, 26 topics; `wanted` queue 43)
compiled via `scripts/build_all.py`. Coverage is no longer alchemy-only: now spans alchemy, hermeticism,
Kabbalah, ceremonial/goetic magic, astrology, witchcraft, divination (tarot), Rosicrucian, Enochian,
theosophy, and biblical-magic. Tabbed **Explore** homepage + faceted gallery + detail pages with
scholarly apparatus + relational entity/topic/collection/region pages + history timeline + lightbox.
New sourcing tool: `scripts/fetch_commons.py` (Wikimedia API → best PD original + license sidecar).

## Build (one command)
`python scripts/build_all.py` → imports → `data/catalog.json` → `db/occultimgdb.db` (`--stats` for a
summary). `--all` adds the page-scan tier. Query: `sqlite3 db/occultimgdb.db "…"`.

## Frontend (V3 — tabbed Explore viewer)
- **`index.html` = Explore homepage** (`js/explore.js` + `js/common.js`): 7 tabs — Timeline · Eras ·
  Regions · Topics · Figures · Collections · All-images — image-forward masonry, global search, and a
  **lightbox with zoom/pan** (wheel/±/dbl-click zoom, drag pan, arrows/esc, prev-next).
- **`gallery.html`** = the faceted gallery (former homepage; era/tradition/work/motif filters, deep-links).
- **`entity.html`** renders profiles for creator/work/tradition/motif/era **+ topic/region/collection**.
- Taxonomy data (edit these to grow categories): `data/topics.json` (11 domains, live/coming_soon),
  `data/collections.json` (12 curated, with `needs` roadmap for coming_soon ones). Both compiled into the DB.
- `data/topics.json`/`collections.json` define category membership via `match: {work_keys, traditions,
  motif_terms, ids}`. To make a coming_soon collection live: source its images, add them, set status:"live".

## What works right now

- **Catalog build:** `python scripts/build_catalog.py` scans 18 works across two image roots
  (`EmblemPrintShop\sources\` + `AlchemyBeatEmUp\staging\raw_images\`), generates
  `site/images/thumbs/` + `cards/`, and writes `data/catalog.json` + `works.json`. Idempotent.
  `--all` adds the page-scan tier; `--force` regenerates derivatives.
- **Scholarship import:** `python scripts/import_local_scholarship.py` folds local Claudiens discourse
  + EmblemPrintShop motif catalog into `data/overrides.json` (preserves hand-authored records).
- **Site** (`site/`, served via the `occultimgdb` launch config → `/site/index.html`):
  - `index.html` — faceted gallery (era/tradition/work/motif), motif-aware search, sort, masonry.
  - `item.html` — detail: 1400px image, download, facts table linked into the relational graph,
    scholarly essay, related images.
  - `entity.html` — profile pages for creator / work / tradition / motif / era, with `[[…]]`
    cross-links, related entities, and external "learn more" links.
  - `browse.html` — "Themes & Figures" directory. `history.html` — chronological timeline walk.
- **Data model:** `data/entities.json` (10 creators, 6 traditions, 6 motifs) is the relational layer;
  `data/overrides.json` (51 records) is per-image scholarship; both merge into generated `catalog.json`.

## Verified (DOM eval; screenshots time out in this preview env — renderer quirk, not a bug)
Gallery 898 items + facets; search by motif (dragon/wolf/ouroboros/furnace…); detail pages render
authored summaries + relational links; entity pages resolve cross-links + list images; browse 29+ tiles;
history shows Medieval/Renaissance/Early-modern with 18 work nodes. No console errors.

## Done since V2 base
- ✅ Promoted motif ontology → 20 relational motif pages (`scripts/import_motifs.py`).
- ✅ Added De Jong citations + related-emblem links + key-concepts + Furnace&Fugue links to Atalanta
  records (`import_local_scholarship.py` enrichment pass; rendered as item-page scholarly apparatus).

- ✅ Seeded the **antiquity stratum**: web-sourced the Chrysopoeia + Pelekanos ouroboros (PD) →
  `sources_web/antiquity/`; timeline now spans all four eras. (3rd image root `LOCAL` added.)

## Next actions (priority order — see SOURCINGIMAGES.md §6 for detail)
1. **Expand antiquity/grimoire** via the proven web pipeline: Zosimos apparatus, more ouroboros
   witnesses; Solomonic circles, Goetia plates as whole pages — NOT the extracted
   sigil crops in `GoetiaRevEng`, which violate the whole-image rule) → fills `goetia_grimoire` tradition.
3. **Author Splendor Solis (22 plates) + Rosarium (20 stages)** per-plate summaries.
4. **Improve per-image motif tagging** beyond Atalanta (king/lion/serpent motif pages are sparse) — a
   vision-tagging pass over the non-Atalanta works would light up the motif search.
5. Curate the page-scan tier (`--all`): illustration-vs-text pass over Fludd/Hall/Obrist/Marshall.

## Research / sourcing pipeline (the path to "everything occult")
- **`RESEARCH_PLAN.md`** — the strategy: the universe-of-occult-imagery map, blind spots, 5 discovery
  engines, scope dials, prioritized roadmap. §4 (repositories, Iconclass codes, local leads) populated
  from a research agent.
- **`data/wanted.json`** — the discovery queue (33 seed targets; schema in the file). Engines append rows;
  advance `status` proposed→verified→sourced→cataloged. Compiled into the DB `wanted` table.
- Gap report: `sqlite3 db/occultimgdb.db "SELECT topic,COUNT(*) FROM wanted GROUP BY topic;"`
- Next highest-yield: map `obrist_medieval` to Obrist's catalogue; source the *Geheime Figuren*; the
  Goetia 72 seals; witchcraft woodcuts — each turns a `coming_soon` collection live.

## Known issues
- Imported Claudiens discourse has occasional source-text artifacts (e.g. "the the me"); every imported
  record carries a `[PLACEHOLDER: cross-check de Jong]` flag for human review.
- `python -m http.server` caches JS; after editing `site/js/*`, navigate to a fresh URL (cache-bust query)
  rather than `reload()`.

## File map
`CONTEXT.md` (orientation) · `CLAUDE.md` (architecture + agent rules) · `SCOPE.md` · `SOURCINGIMAGES.md` ·
`PROGRESS.md` (history) · `scripts/config.py` (registry) · `scripts/build_catalog.py` ·
`scripts/import_local_scholarship.py` · `data/{entities,overrides,catalog,works}.json` · `site/`.
