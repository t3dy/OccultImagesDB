# OCCULTIMGDB — Project Scope

*A scholarly-cataloged archive of whole illustrations from the alchemical & occult tradition,
built for artists, game designers, and researchers sourcing public-domain visual assets.*

Status: **V1 shipped** (browsable site, 687 curated illustrations, 12 authored scholarly entries).
See `HANDOVER_CURRENT.md` for the live build state.

---

## 1. Vision

A single, beautiful, fast place to find and understand the *images* of Western esotericism —
the dragon devouring its tail, the king devoured by the wolf, the squared circle of the Stone,
the ouroboros of Kleopatra, John Dee's Monas — each presented as a **complete illustration**,
catalogued with sourced scholarship, and offered as a downloadable public-domain asset.

It is **not** a cropping tool. We catalog whole images as they appear in their sources. (Atomic
element extraction was the EmblemPrintShop experiment and is explicitly out of scope here.)

## 2. Audience & the UX bet

Primary: **game developers, illustrators, concept artists, worldbuilders.** They think in
*motifs* ("I need a dragon / a furnace / a magic circle / a grim king"), not in bibliography.
So the product optimises for:

- **Visual browse first** — a dense, fast image grid.
- **Search/filter by what is *in* the image** — motif tags (dragon, wolf, toad, ouroboros, furnace…),
  not just author/date.
- **One-click download** + an unambiguous rights statement + a link to the source institution.
- Scholarly depth is present and excellent, but it sits one layer down, on the detail page.

Secondary: scholars and the esoterically curious, served by the per-image essays and provenance.

## 3. In scope / out of scope

| In scope | Out of scope |
|---|---|
| Whole illustrations from printed & manuscript esoterica | Cutting images into atomic elements |
| Alchemy, Hermetica, Rosicrucian, Kabbalah, grimoire/Goetia, astrology, theosophy | Modern copyrighted occult art (without clearance) |
| Late antiquity → early modern (V1), Victorian/modern (later) | A build-tooling SPA / heavy framework |
| Sourced scholarly metadata, ≤5,000 words per image | Original esoteric *claims*; we report cited scholarship |

## 4. Content corpus

### Shipped in V1 — curated "illustration" tier (687 images, 8 works)
| Work | Creator | Date | Images |
|---|---|---|---|
| Atalanta Fugiens | Michael Maier | 1618 | 51 |
| Hypnerotomachia Poliphili | Francesco Colonna | 1499 | 162 |
| Rosarium Philosophorum | anon. | 1550 | 19 |
| Splendor Solis | attr. Trismosin | 1532–35 | 46 |
| Viridarium Chymicum | Daniel Stolcius | 1624 | 108 |
| Philosophia Reformata (plates) | J. D. Mylius | 1622 | 134 |
| Amphitheatrum Sapientiae | Heinrich Khunrath | 1595/1609 | 92 |
| Emblemata Sacra | Daniel Cramer | 1624 | 75 |

All images are public-domain scans **already downloaded** under
`C:\Dev\EmblemPrintShop\sources\` — the importer reads them in place; nothing is re-downloaded.

### Registered, available with `--all` — "page-scan" tier (needs curation)
Fludd *Mosaicall Philosophy* (311), Khunrath, Maier *Arcana*/*Viatorium*, Hall manuscripts (254),
Marshall/Dee Elizabethan occult (265), Obrist medieval (320), McLean (57). These are raw book-page
scans mixing illustration with text; they need an illustration-vs-text pass before they hit the
main gallery. ≈3,700 total images exist across all tiers.

### Not yet sourced — the **antiquity & grimoire** stratum (the user's explicit wishlist)
These are named but **not yet in the corpus** — see the sourcing TODO (§8):
the ouroboros of **Kleopatra's *Chrysopoeia***, early **furnace/still diagrams**, the **Theban
alphabet**, **Solomonic magic circles** & the 72 **Goetia seals**, portraits (**John Dee**, Paracelsus,
Agrippa), **Aurora Consurgens** miniatures, the **Mutus Liber**, **Ripley Scroll**.

## 5. Tech & architecture

Plain **static HTML/CSS/vanilla JS** — no build step, deploys to GitHub Pages/Netlify as-is.
A small Python importer (`scripts/build_catalog.py`, idempotent) scans the source registry
(`scripts/config.py`), generates `thumbs/` (≈400px) and `cards/` (≈1400px) derivatives, and emits
`data/catalog.json`. Hand-authored scholarship lives in `data/overrides.json`, merged by id.
Full architecture in `CLAUDE.md`.

## 6. Data model (per image)

`id · title · work · creator · date · century · place · region · language · era · tradition ·
tier · seq · motifs[] · rights · provenance_url · source_file · thumb · card · summary ·
summary_status`. Controlled vocab for `era` and `tradition` is in `CLAUDE.md`.

## 7. Features

**Now:** faceted gallery (era / tradition / source work / motif), live text search across title +
motifs + summary, sort (chronological / by work / A–Z), incremental-render masonry grid,
per-image detail page (1400px viewer, download, facts table, motif tags, scholarly essay,
"more from this work"), deep-linkable filters, About/method/licensing page.

**Roadmap:** authored summaries for all flagship images → ingest & curate the page-scan tier →
add the antiquity/grimoire stratum → lightbox/zoom → "download pack" by motif → optional
contributor workflow → Victorian/modern revival imagery.

## 8. Sourcing TODO — what **you** need to provide (the placeholders)

The site marks every un-authored image with a "needs text" badge and every detail page with a
`[needs: …]` marker. Concretely, the human-sourcing queue is:

1. **Antiquity images** — find public-domain scans of: Kleopatra *Chrysopoeia* ouroboros (Codex
   Marcianus gr. 299), Zosimos apparatus diagrams, early furnace/alembic illustrations. *(image needed)*
2. **Grimoire & ceremonial** — Solomonic circles, Goetia seals (the 72 sigils already analysed in
   `C:\Dev\wiki\goetia_sigil_analysis.md` — wire those in), Theban alphabet plates. *(image needed)*
3. **Portraits** — John Dee, Paracelsus, Agrippa, Maier, Fludd, Khunrath. *(image needed)*
4. **Provenance gaps** — Marshall (Dee), Obrist (medieval), McLean collections lack per-item source
   URLs and rights confirmation. *(provenance needed)*
5. **Scholarly summaries** — 675 of 687 V1 images still carry placeholder summaries. Priority:
   Rosarium stages, Splendor Solis 22 plates, Khunrath's great circular engravings, Stolcius emblems.
   *(explanation needed)*
6. **Page-scan curation** — mark which Fludd/Hall/Mylius page scans are illustrations vs text.

## 9. Licensing posture

Underlying artworks are centuries old → public domain. Digital scans carry the holding library's
rights statement (recorded per item). For commercial/game use the user remains responsible for
confirming the per-item statement and source-institution terms. The About page states this plainly.

## 10. Open questions for the user

- **Deployment target?** (GitHub Pages vs Netlify vs custom domain.) Affects nothing structural.
- **Full-res downloads:** ship the 1400px "card" as the download (current), or also copy the
  original full-res scans into the repo (adds ~3–5 GB)?
- **Page-scan tier:** auto-include with a "pages" toggle (current behaviour) or keep hidden until
  hand-curated?
- **Scope creep guard:** confirm we stop at early-modern for V1 and treat Victorian/modern as a
  later, separate ingest.
