# OCCULTIMGDB — Authoring Style Guide (cards & essays)

How to write a catalog entry. The data model is in [`ONTOLOGY.md`](ONTOLOGY.md); the machine-readable
field spec agents follow is `scripts/AGENT_SOURCING_SPEC.md`. Author in `data/overrides.json`
(keyed by `id`); never hand-edit `catalog.json` / the `.db`.

## Two surfaces, one record

Each image is presented two ways, both generated from the same entry:

### 1. The card (grid view — `site/js/common.js` `masonryCard` + `briefDesc`)
What the browsing user scans. It shows, automatically:
- the **image** (image-forward),
- **title**,
- **creator · date** (in gold),
- a **brief description** = the markdown-stripped first sentence(s) of `summary`, clamped to ~3 lines.

➡️ **Authoring rule:** the **first sentence of `summary` must stand alone as a caption** — a single,
concrete, jargon-light clause that says what the thing *is*. It is the card blurb; write it for a reader
who knows nothing. (e.g. "The hexagram Seal of Solomon as drawn in the *Lemegeton*, worn by the conjurer
to command the seventy-two spirits.") Don't open with "This image…".

### 2. The essay page (detail view — `site/js/item.js`)
The full scholarly record. Renders, in order: the 1200px image + download/source buttons · title ·
creator·work·date line · **motif tags** · **Depicted figures** · the **facts table** · the **essay** ·
the **scholarly apparatus** · "more from this work".

## The `summary` essay — structure

Markdown. Lede sentence (the card blurb), then these `##` sections (≤ ~400 words total):

```
<Lede sentence — the standalone caption.>

## Iconography
What is *literally depicted* — figures, objects, gestures, inscriptions, colours, layout. Concrete and
visual. This is what a viewer sees before interpretation.

## Significance
The esoteric/historical meaning: the doctrine, the text it illustrates, its place in the tradition, named
scholarship. Link motifs/traditions inline with [[motif:ouroboros|the ouroboros]] where natural.

## For artists & game designers
One practical note — how the image could be used (an emblem, a mechanic, a mood, an asset). This is the
project's audience hook; keep it short and usable.
```

**Hard rules**
- **Never invent** facts, shelfmarks, dates, attributions, or scholarship. Unsure → stay general and
  accurate, or mark `[PLACEHOLDER: …]` (renders visibly as "needs:" so gaps are honest, not hidden).
- **Date to the surviving artwork**, not the lost original. Reception images (a Baroque Witch of Endor)
  are dated and `era`-tagged to the painting; the ancient subject lives in the prose + `figures`.
- Italicise Latin/Greek and work-titles (`*Atalanta Fugiens*`). Keep manuscript shelfmarks verbatim.
- Record **real licences** in `rights` (a lot of museum scans are CC BY / CC BY-SA, not PD) with the
  institution — never relabel a CC-BY image as public domain.

## The facts table — fields to fill (metadata for relational browsing)

Every entry should carry, beyond the prose:

| Field | Rule |
|---|---|
| `medium` | one value from the 18-term vocabulary (ONTOLOGY) — what it physically *is* |
| `figures` | every named person/deity/being **depicted** (≠ the creator). `[]` if purely diagrammatic |
| `repository` | holding institution, from the `.prov.json` (`[PLACEHOLDER: …]` if only an uploader is known) |
| `shelfmark` | MS/accession ref if applicable; `""` for printed books |
| `motifs` | 6–10 specific lowercase iconographic tags (the fine-grained index) |
| `key_concepts` | 4–6 indexable abstract concepts |
| `citations` | ≥1 real source + the Commons/provenance URL |
| `iconclass` | optional — only if you confidently know the code |

### `motifs` vs `figures` vs `key_concepts` (don't conflate)
- **`motifs`** = *things in the picture*, lowercase, iconographic: `ouroboros`, `magic circle`, `cauldron`,
  `magic square`, `woodcut`. The visual index.
- **`figures`** = *named beings depicted*, Title Case: `Saturn`, `Hermes Trismegistus`, `Lilith`. The
  who/what-is-pictured index.
- **`key_concepts`** = *ideas the image is about*, the abstractions: `coniunctio`, `Christian Cabala`,
  `the music of the spheres`. The intellectual index.

## Checklist before you commit an entry
1. First sentence works as a standalone card caption.
2. `## Iconography` describes only what's visible; `## Significance` carries the interpretation.
3. `medium`, `figures`, `repository` filled; `rights` records the real licence + institution.
4. No invented facts; placeholders where genuinely unknown.
5. `id` = `<work_key>__<slug>` matches the image filename (the importer slugifies `_`→`-`).
6. Run `python scripts/build_all.py`; confirm it renders (card + item page) with no console errors.
