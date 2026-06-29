# SOURCINGIMAGES.md — Where the images come from, and where to go next

*How OCCULTIMGDB's image corpus has been assembled so far, what local material is still untapped,
and a prioritized plan for the images to source next. Companion to `SCOPE.md` (§8 has the short TODO).*

Last updated: 2026-06-27.

---

## 0. The principle

Every image in this archive is a **whole illustration** from a real, identifiable source, carrying a
**provenance link** and a **rights statement**. We never invent images and never re-download what we
already hold. Sourcing proceeds in three modes, in priority order:

1. **Reuse what's already on disk** under `C:\Dev` (thousands of public-domain scans already gathered
   across sibling projects). Cheapest, fastest, already rights-checked.
2. **Mine local scholarly databases & PDFs** for the *metadata* that turns a bare scan into a
   catalogued, searchable, scholarly record.
3. **Source from the open web** (public-domain digitisations) for what the machine doesn't yet hold —
   chiefly the antiquity and grimoire strata.

---

## 1. What is sourced and IN the catalog now

### 1a. From `C:\Dev\EmblemPrintShop\sources\` (already downloaded; read in place)
The original V1 spine — 8 works, **687 images**, curated "illustration" tier:

| Work | Creator | Date | Images | Era |
|---|---|---|---|---|
| Atalanta Fugiens | Michael Maier | 1618 | 51 | early modern |
| Hypnerotomachia Poliphili | Francesco Colonna | 1499 | 162 | renaissance |
| Rosarium Philosophorum | anon. | 1550 | 19 | renaissance |
| Splendor Solis | attr. Trismosin | 1532–35 | 46 | renaissance |
| Viridarium Chymicum | Daniel Stolcius | 1624 | 108 | early modern |
| Philosophia Reformata (plates) | J. D. Mylius | 1622 | 134 | early modern |
| Amphitheatrum Sapientiae | Heinrich Khunrath | 1595/1609 | 92 | renaissance |
| Emblemata Sacra | Daniel Cramer | 1624 | 75 | early modern |

### 1b. From `C:\Dev\AlchemyBeatEmUp\staging\raw_images\` (newly ingested this session)
Discovered by the local-source survey — illustration scans **organized by text**, which extends the
archive back into the **medieval stratum** and adds major works. **10 works, ~211 images:**

| Work | Creator | Date | Images | Era | Why it matters |
|---|---|---|---|---|---|
| Aurora Consurgens | pseudo-Aquinas | c.1420 | 30 | **medieval** | earliest illustrated alchemical MS |
| Summa Perfectionis | pseudo-Geber | 13th c. | 25 | **medieval** | foundational apparatus/furnace woodcuts |
| Ripley Scroll | Ripley tradition | 15–16th c. | 16 | renaissance | the great emblematic scrolls |
| Lambspring | (Musaeum Hermeticum) | 1625 | 19 | early modern | beloved emblems; an ouroboros |
| Mutus Liber | 'Altus' | 1677 | 8 | early modern | the wordless picture-book of alchemy |
| Symbola Aureae Mensae | Michael Maier | 1617 | 34 | early modern | 12 alchemists + symbolic scenes |
| De Re Metallica | Georgius Agricola | 1556 | 10 | renaissance | authentic furnaces & foundries |
| Furni Novi Philosophici | J. R. Glauber | 1648 | 25 | early modern | distillation apparatus |
| Alchymia | Andreas Libavius | 1597 | 24 | renaissance | the "ideal laboratory" plan |
| De la Pirotechnia | Biringuccio | 1540 | 20 | renaissance | first printed metallurgy |

*(Deliberately skipped here to avoid duplication: this corpus also held rosarium / splendor_solis /
khunrath copies, which are already covered by §1a.)*

**Combined catalog after this session: ~18 works, ~900 images.** Rebuild with
`python scripts/build_catalog.py` (idempotent).

---

## 2. Local SCHOLARSHIP mined for metadata (turns scans into records)

The survey of `C:\Dev` found rich scholarly metadata. Used so far:

- **`C:\Dev\Claudiens\site\data.json`** — 51 Atalanta emblems, each with a ~1,000-char scholarly
  *discourse*, the alchemical *stage* (nigredo/albedo/rubedo), and *source authorities*. **Imported**
  via `scripts/import_local_scholarship.py` → authored summaries for the 39 Atalanta emblems not
  hand-written (the 12 flagship hand-authored entries are preserved).
- **`C:\Dev\EmblemPrintShop\data\emblems.json`** — per-emblem `object_catalog` (detected motifs).
  **Imported** as motif tags so Atalanta emblems are searchable by what they depict.

### Mined-but-not-yet-used (high-value next imports)
- **`C:\Dev\EmblemPrintShop\data\motifs.json`** — a 200+ entry motif **ontology** (iconographic
  meaning + alchemical valence + planetary association per motif). *Next: promote into
  `data/entities.json` motif profiles so every motif page has sourced scholarship.*
- **`C:\Dev\TheosophicalAlchemyDB\data\maier_atalanta_fugiens_emblems_metadata.json`** — **De Jong
  page citations**, key concepts, related-emblem links (emblems 1–20). *Next: add citations + "related
  emblems" cross-links to Atalanta records.*
- **`C:\Dev\TheosophicalAlchemyDB\data\prototype_data.json`** — 40+ alchemist biographies (dates,
  works, scholars). *Next: seed more creator entities (Paracelsus, Agrippa, Andreae, Fludd…).*
- **`C:\Dev\Claudiens\site\visual-data.json`** — index of 300+ images across *many* works (Agricola,
  Aurora, Lambsprinck, Libavius, Mutus Liber, Ripley, Rosarium, Splendor Solis, Symbola) with tags and
  source URLs. *Next: use its tags to enrich the §1b works, and its URLs as provenance.*
- **SQLite knowledge bases** — `renaissance magic\db\renmagic.db` (155 MB), `PicoDB\db\pico.db`
  (93 MB), `EmeraldTablet\db\emerald_tablet.db` (6.7 MB), `MedievalMagicDB\db\medieval_magic.db`.
  Deep context for tradition/figure essays. *Next: query for figure bios + "where to learn more" links.*
- **`C:\Dev\GoetiaRevEng\demon_metadata.json`** — the 72 Goetia spirits with rank/appearance, plus
  seal images under `GoetiaRevEng\docs\precedents\`. *Next: a grimoire/Goetia work (see §4).*

---

## 3. Web sourcing done so far

- Verified flagship Atalanta iconography (mottos, subjects) via Wikipedia, furnaceandfugue.org,
  mjdorian.com, and De Jong references — used to author the 12 hand-written emblem entries.
- Compiled external **"Learn more" links** per creator/tradition/motif in `data/entities.json`
  (Internet Archive editions, SEP, British Library, e-codices, furnaceandfugue).

We have *not* yet pulled new image *files* from the web — everything catalogued so far was already on
disk. The web is the route for the strata in §4.

---

## 4. NEXT images to source — prioritized

> Legend: 🟢 already on disk somewhere under C:\Dev (just needs ingesting) · 🌐 source from the web ·
> 📄 needs a scholarly summary written.

### Priority 1 — the ANTIQUITY stratum (the project's headline gap) 🌐
> **STARTED (2026-06-27):** web-sourced two public-domain ouroboros witnesses into
> `sources_web/antiquity/` — the **Chrysopoeia of Kleopatra** ouroboros (MS Marciana gr. Z. 299) and
> the **1478 Theodoros Pelekanos** coloured ouroboros (Cod. Paris. gr. 2327), both authored. The
> timeline now opens with Antiquity. The pipeline (curl via Wikimedia `Special:FilePath` → register
> under `root:"LOCAL"` → author override → rebuild) is proven; repeat it for the targets below.

The vision begins "with the first image of the ouroboros." First two now in; remaining targets:
- **Ouroboros of Kleopatra**, from the *Chrysopoeia of Kleopatra* — ✅ done (locus classicus). Source:
  **Codex Marcianus graecus 299**, Biblioteca Marciana, Venice. Look for digitisations via the
  Marciana, Wikimedia Commons ("Chrysopoeia of Cleopatra"), or facsimiles in Berthelot's
  *Collection des anciens alchimistes grecs* (public domain).
- **Zosimos of Panopolis** apparatus / the "Visions" — via Berthelot, and MS illustrations.
- **Early furnace & still diagrams** (Hellenistic/Byzantine alchemical MSS).
- *Caveat:* genuine antiquity images are scarce and often survive only via later Byzantine copies —
  be explicit in the catalog about "earliest surviving witness" vs "original."

### Priority 2 — GRIMOIRE & ceremonial magic 🟢🌐
- **The 72 Goetia seals** — 🟢 partly local: `C:\Dev\GoetiaRevEng\` (metadata + precedent seal images;
  cf. workspace `wiki/goetia_sigil_analysis.md`). Ingest as a "Grimoire & Goetia" work; 🌐 supplement
  with the *Goetia of Dr Rudd* (BL Sloane/Harley) and Mathers/Crowley 1904 plates (public domain).
- **Solomonic magic circles & pentacles** — *Key of Solomon* (Mathers, 1889, public domain;
  BL Sloane MSS). 🌐
- **Sigillum Dei Aemeth** and **Enochian tables** of John Dee. 🌐 (BL Sloane 3188/3189.)
- **Theban alphabet** (Honorius / Agrippa). 🌐

### Priority 3 — PORTRAITS of the figures 🌐
Faces for the creator pages (currently text-only):
- **John Dee** (Ashmolean portrait), **Paracelsus** (Hirschvogel/Quentin Massys school),
  **Cornelius Agrippa**, **Michael Maier** (the *Symbola* frontispiece portrait — 🟢 may be in our
  symbola_aureae scans), **Robert Fludd**, **Heinrich Khunrath**. Wikimedia Commons has public-domain
  versions of most.

### Priority 4 — DEEPEN works already held 🟢📄
- **Splendor Solis**: identify and richly summarise the canonical **22 plates** (the knight, the
  drowning king, the peacock vessel, the sun-child) — currently generic. 🟢 images on disk; 📄 needs prose.
- **Rosarium Philosophorum**: map our 19 woodcuts to the canonical **20 stages** and author each. 📄
- **Khunrath**: identify the great circular plates (Oratory-Laboratory, the cosmic rose) among the 92
  page-scans and feature them. 🟢📄
- **Ripley Scroll / Mutus Liber / Lambspring**: author per-plate readings (well-documented). 📄

### Priority 5 — the PAGE-SCAN tier (curation, not new sourcing) 🟢
`build_catalog.py --all` exposes ~3,000 more on-disk images (Fludd 311, Hall 254, Marshall/Dee 265,
Obrist medieval 320, …). These mix illustration with text pages. *Next: an illustration-vs-text pass*
(reuse EmblemPrintShop's junk-filter approach, or a quick vision classifier) so only the plates surface.

### Priority 6 — later eras (post-V1)
Victorian/modern occult revival: **Mathers/Golden Dawn**, **A. E. Waite / Pamela Colman Smith tarot**
(1909, now public domain), **Crowley/Harris Thoth** (check rights), **Eliphas Lévi's Baphomet**,
**Manly P. Hall's *Secret Teachings*** plates (🟢 `hall_manuscripts` already on disk).

---

## 5. Where to source public-domain occult images (reference)

| Source | Good for | Notes |
|---|---|---|
| **Internet Archive** | printed books (Maier, Fludd, Khunrath, Musaeum Hermeticum) | full PDFs; our main well |
| **Wellcome Collection** | alchemy & magic MSS, Ripley scrolls | CC0/PD, IIIF, high-res |
| **e-codices (Switzerland)** | illuminated MSS (Aurora Consurgens) | IIIF manifests |
| **BnF Gallica** | French/European MSS & prints | PD; high-res |
| **British Library** | Sloane/Harley/Royal grimoires, Dee | check item rights |
| **Wikimedia Commons** | portraits, single famous plates, ouroboros | verify the underlying source |
| **Science History Institute** | Atalanta Fugiens, chemistry prints | PD, excellent metadata |
| **Getty / The Met (Open Access)** | prints & drawings | CC0 |
| **furnaceandfugue.org** | Atalanta scholarship + per-emblem pages | scholarly apparatus |

Rights rule of thumb: the *artwork* is PD by age; record the *scan's* institutional rights per item,
and prefer CC0 / no-known-copyright sources for anything a game dev might ship commercially.

---

## 6. Concrete next 5 actions

1. **Ingest the Goetia seals** from `C:\Dev\GoetiaRevEng\` as a new "Grimoire & Goetia" work + add a
   `goetia_grimoire` tradition page already stubbed in `entities.json`. (🟢 local, fast.)
2. **Source the Chrysopoeia ouroboros** from Wikimedia/Marciana/Berthelot → first antiquity entry. (🌐)
3. **Promote `EmblemPrintShop/data/motifs.json`** into `entities.json` motif profiles (sourced
   iconography for every motif page). (🟢 local.)
4. **Author the 22 Splendor Solis plates** and the 20 Rosarium stages from De Jong / standard
   literature. (🟢 images on disk; 📄 prose.)
5. **Add De Jong citations + related-emblem links** to Atalanta records from the
   TheosophicalAlchemyDB metadata. (🟢 local.)

Each is a self-contained, resumable unit; complete one, append to `PROGRESS.md`, rebuild, repeat.
