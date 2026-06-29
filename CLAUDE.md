# OCCULTIMGDB — Claude Code Project Instructions

**Project type:** Static website (HTML / CSS / vanilla JS, no build step).
**One-line:** A browsable, scholarly-cataloged archive of *whole* illustrations from the
alchemical & occult tradition (late antiquity → early modern, later extending to Victorian/modern),
optimized for **game developers and artists** sourcing public-domain visual assets.

Parent workspace rules: `C:\Dev\CLAUDE.md`. User profile: `C:\Dev\docs\CLAUDE_PROJECT_CONTEXT.md`.

---

## What this project IS

- A catalog of **complete illustrations** (a whole emblem plate, a whole woodcut, a whole portrait,
  a whole diagram) — e.g. "Atalanta Fugiens, Emblem XXI", "Ouroboros from Kleopatra's *Chrysopoeia*",
  "Solomonic magic circle from the *Goetia*", "Portrait of John Dee".
- Each entry carries scholarly, web-sourced metadata: title, source work, creator, date, place,
  iconographic description, alchemical/occult meaning, motifs/tags, provenance, and rights.
- A **5,000-word maximum** scholarly summary per image (usually far shorter). Where we lack
  verified info we leave explicit `[PLACEHOLDER: …]` markers for the user to source.

## What this project is NOT

- **NOT** atomic visual-element extraction. We do **whole images only** — no cutting the dragon out
  of the emblem, no cropping the sword from the knight. (That was EmblemPrintShop's job; it is
  explicitly out of scope here.)
- Not a build-tooling SPA. Keep it plain static files so it deploys to GitHub Pages / Netlify with
  zero build.

## Primary audience (optimize UX for this)

Game devs / artists sourcing assets → fast visual browse, filter by motif/era/source, clear
licensing, and a downloadable image per entry. Scholarly depth is present but secondary to browse speed.

---

## Architecture

```
OCCULTIMGDB/
  data/
    overrides.json      # AUTHORED per-image scholarship (encyclopedia prose + citations + tags) — edit this
    entities.json       # AUTHORED creators / traditions / motifs (the relational layer) — edit this
    catalog.json        # GENERATED denormalised per-image catalog (do not hand-edit; rebuild)
    works.json          # GENERATED source-work list
  db/
    occultimgdb.db      # CANONICAL SQLite database — compiled, normalised, queryable (see below)
  scripts/
    config.py                    # SOURCE REGISTRY: every source dir + its metadata (+ image roots)
    build_catalog.py             # scans source dirs, generates thumbs/cards, emits catalog.json
    import_local_scholarship.py  # folds local Claudiens/Theo discourse + citations into overrides.json
    import_motifs.py             # promotes the motif ontology into entities.json
    build_db.py                  # compiles catalog.json + entities.json -> db/occultimgdb.db
    build_all.py                 # runs the whole pipeline in order (use this)
  site/                 # the deployable static website (open site/index.html)
    index.html  item.html  entity.html  browse.html  history.html  about.html
    css/style.css   js/{app,item,entity}.js
    images/thumbs/  images/cards/   # GENERATED derivatives (not full-res originals)
  sources_web/          # public-domain images downloaded INTO the repo (root:"LOCAL")
```

### The database (db/occultimgdb.db)
The project's **dedicated, canonical catalog store** is a normalised SQLite database, **compiled** from
the authored JSON sources by `build_db.py`. Tables: `works`, `images`, `image_motifs`,
`image_citations`, `image_relations`, `image_concepts`, `creators`/`creator_works`/`creator_links`,
`traditions`/`tradition_links`, `motifs`/`motif_terms`/`motif_see_also`. It is the substrate for
querying, analytics, an encyclopedia export, or a future API.

**Authoring model (important):** scholarship/prose is authored in the **JSON sources** (`overrides.json`,
`entities.json`) — version-controllable, diffable, reviewable — and *compiled* into both `catalog.json`
(for the browser) and `occultimgdb.db` (canonical/queryable). Do **not** hand-edit the `.db` or
`catalog.json`; edit the sources and run `build_all.py`. This keeps the Deckard boundary clean:
deterministic compile, human/LLM judgement in the sources.

### Documenting academic info per entry (the encyclopedia)
Each `overrides.json` record should carry as much *sourced* scholarship as possible:
`summary` (use `## Iconography`, `## Significance`, `## Reading` sections), `citations` (list of
`{text, url?}` — the bibliography), `key_concepts` (indexable terms), `related_emblems`/relations,
and specific `motifs`. Mark gaps `[PLACEHOLDER: …]`; never invent a citation.

### Image strategy
Original full-res scans live in `C:\Dev\EmblemPrintShop\sources\<book>\images\` (≈3,700 public-domain
pages already downloaded — **do not re-download**). `build_catalog.py` reads those, and writes two
derivatives into `site/images/`:
- `thumbs/<id>.jpg` — ~400px, for the gallery grid.
- `cards/<id>.jpg`  — ~1400px, the on-site downloadable display image.
The full original path + provenance URL are recorded in `catalog.json` so the highest-res source is
always one click away.

### Rebuilding everything
```
python scripts/build_all.py            # full pipeline: imports -> catalog.json -> occultimgdb.db
python scripts/build_all.py --all      # also include the raw page-scan tier
python scripts/build_db.py --stats     # rebuild just the DB + print a stats summary
```
All steps are **idempotent** and preserve hand-authored content. `build_catalog.py --force`
regenerates image derivatives.

### Querying the database
```
sqlite3 db/occultimgdb.db "SELECT era, COUNT(*) FROM images GROUP BY era;"
# images depicting a motif across every work:
sqlite3 db/occultimgdb.db "SELECT i.title FROM images i JOIN image_motifs m ON m.image_id=i.id WHERE m.motif='ouroboros';"
```

---

## Conventions

- Eras (controlled vocab): `antiquity`, `medieval`, `renaissance`, `early_modern`, `modern`.
- Traditions: `alchemy`, `hermetic`, `rosicrucian`, `kabbalah`, `goetia_grimoire`, `astrology`,
  `theosophy`, `reception`.
- Every catalog entry MUST carry a `rights` string and, where known, a `provenance_url`.
- Scholarly prose follows the workspace voice guide (`C:\Dev\wiki\concept_scholarly_writing.md`):
  critical-reportorial, sourced, no purple filler. Mark unknowns as `[PLACEHOLDER: …]`.

## Working in this repo as an agent (read this first)

This project is built by AI coding agents. To stay token-efficient and avoid losing work:

**Read in layers — pull only the context the task needs.** Don't load everything up front.
1. `CONTEXT.md` — the 30-second orientation packet (what/why/state/entry-points). Start here.
2. `HANDOVER_CURRENT.md` — live state + next actions. Read before resuming.
3. `PROGRESS.md` — append-only history; skim the tail for what just happened.
4. `SCOPE.md` — only when scoping or deciding what's in/out.
5. Source: `scripts/config.py` (the registry) and `data/overrides.json` (the prose) are the two
   files you actually edit to grow the catalog. The site JS rarely needs changing.

**Never re-read what a derivative already summarizes.** `data/catalog.json` is generated — read
`config.py` + `overrides.json` instead. The 3,700 source scans live under
`C:\Dev\EmblemPrintShop\sources\` — never re-download, never copy wholesale into context; the importer
streams them. To inspect an image, open the one file, don't glob the directory.

**Persist every step as a file artifact.** Sessions can end at any time. After any meaningful unit of
work: append to `PROGRESS.md`, update `HANDOVER_CURRENT.md`'s "next actions", and (if catalog data
changed) re-run the importer so `catalog.json` reflects reality. A change that exists only in chat is
lost work.

**The importer is the seam (Deckard boundary).** Deterministic Python (`build_catalog.py`) owns
scanning, thumbnailing, and assembling records. LLM/human judgment owns only the prose + tags in
`overrides.json`. Keep that split: don't hand-edit `catalog.json`; add an override and rebuild.

**Memory / cross-session continuity.** This project's durable memory is these markdown files plus the
workspace wiki (`C:\Dev\wiki\project_occultimgdb.md`) and the auto-memory
(`...\memory\project_occultimgdb.md`). When state changes materially (new tier ingested, schema
change, deploy target chosen), update those pointers — they are how the *next* session reconstitutes
context cheaply.

**Idempotence & safety.** Prefer idempotent, resumable operations (the importer skips existing
derivatives). Large/long jobs (`--all`, full-res copy) should run in the background and log progress,
so a dropped session leaves a recoverable state, not a half-written catalog.

## Status

See `HANDOVER_CURRENT.md` for the live state and next actions.
