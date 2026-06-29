# RESEARCH_PLAN.md — Toward "Everything Occult"

*A strategy for systematically discovering, sourcing, and cataloging every extant image relevant to
Western esotericism — from antiquity to the modern revival — across local research materials and the
open web. Companion to `SOURCINGIMAGES.md` (what's been sourced) and the `coming_soon` topics/collections.*

Status: **planning artifact.** Last updated 2026-06-27.

---

## 0. Reality check — where we actually stand

We hold **~904 images across 23 works, ~95% alchemy.** Measured against the ambition, the gaps are
near-total. Candid answers to the questions that prompted this plan:

| Do we have… | Status |
|---|---|
| Apuleius's *Golden Ass* / Isis-mysteries imagery (late antiquity + reception) | **No — 0 images** |
| The complete corpus of early alchemical imagery per **Obrist** | **No** — we hold an unlabeled `obrist_medieval` page-dump, never mapped to her catalogue |
| Every early-printed woodcut/pamphlet of **ceremonial magic & witchcraft** | **No — almost 0** (one Solomonic circle) |
| Every **Rosicrucian** image | **Partial** — Cramer's emblems + Fludd's Great Chain; missing the *Geheime Figuren*, the manifestos, etc. |
| **Biblical magic** scenes across art history (Witch of Endor, Simon Magus, Moses vs the magicians, the Magi) | **No — 0 images** |
| **Tarot, astrology cycles, Gnostic gems, witch-trial prints, Theosophical thought-forms, Masonic emblems…** | **No** |

Realistically, "everything occult" is on the order of **tens of thousands** of images — perhaps
50–100× the current corpus. That is reachable only with a **repeatable, LLM-driven discovery pipeline**,
not ad-hoc sourcing. This document defines that pipeline and, first, the *map of the territory* — because
the hardest part of "everything" is knowing what you haven't thought of.

---

## 1. The universe of occult imagery — what "everything" contains

Three orthogonal axes. An image is located by **(subject domain) × (period) × (medium/object type)**.
Coverage should be tracked as a matrix across all three. The blind spots are mostly whole rows we
haven't begun.

### 1A. Subject domains (✓ = some coverage · ◐ = seed only · ✗ = none yet)

**Alchemy ✓** — emblem books, the colour stages, coniunctio, apparatus, the Ripley scrolls, the
Mutus Liber, the alchemical bestiary (phoenix, pelican, salamander, green lion, basilisk).

**Hermeticism ◐** — the *Tabula Smaragdina*, cosmic-correspondence diagrams, the Hieroglyphica
tradition (Horapollo), Egyptian-revival imagery, Kircher's *Oedipus Aegyptiacus*.

**Kabbalah / Christian Cabala ✗** — Sephirotic trees, the *Portae Lucis* frontispiece, divine-name
charts, gematria diagrams, the *Zohar*, Lurianic diagrams, Kircher's tree.

**Astrology ✗** — zodiac cycles, the **"Children of the Planets"** series, the astrological/zodiac
man (Books of Hours), planetary deities & their chariots, almanacs, volvelles, the Dendera zodiac,
astrological treatises (Sibly, Leo).

**Ceremonial / ritual magic & grimoires ◐** — Solomonic circles & pentacles, the *Heptameron*, the
*Ars Notoria* notae, the *Sworn Book of Honorius*, the *Black Pullet*, Olympic-spirit seals.

**Goetia / demonology ◐** — the 72 seals (we have the data via GoetiaRevEng), demon portraits
(*Dictionnaire Infernal*, Collin de Plancy), the goetic circle/triangle, infernal hierarchies.

**Witchcraft ✗** — Baldung Grien's witches, the *Malleus*/*Compendium Maleficarum* woodcuts, sabbath
scenes (de Lancre), witch-trial pamphlets (*Newes from Scotland*), the witch's flight, familiars.

**Divination ✗** — tarot (Visconti-Sforza → Marseille → Etteilla → Golden Dawn → Waite-Smith → Thoth),
geomancy figures, chiromancy/palmistry charts, physiognomy & metoposcopy, scrying, the I Ching reception.

**Talismans, amulets & magical gems ✗** — **Gnostic/Abraxas gems** (antiquity!), magical papyri (PGM)
drawings, *defixiones* (curse tablets), Hebrew amulets, planetary talismans, magic squares (Agrippa's kameas).

**Angelology & visionary ✗** — angelic hierarchies, Enochian tables & the Sigillum Dei Aemeth (Dee),
apocalyptic figurae (Joachim of Fiore), Hildegard of Bingen's *Scivias*, Beatus Apocalypse, the Ophite diagram.

**Rosicrucian ◐** — the *Fama*/*Confessio*, the *Geheime Figuren der Rosenkreuzer* (the great colour
plates), the Temple of the Rosy Cross, the Chymical Wedding.

**Theosophy / Boehmenism ✗** — Boehme & Gichtel's theosophical-man diagrams, the *Aurora*, Law's
illustrations; later: Blavatsky, **Besant & Leadbeater's *Thought-Forms* (1901)**, *Man Visible and Invisible*.

**Spiritualism & the occult revival (Victorian–modern) ✗** — spirit photography, séance/ectoplasm
imagery, Éliphas Lévi's **Baphomet**, the Golden Dawn (tattvas, the Tree, ritual diagrams), Crowley/Harris
**Thoth**, Austin Osman Spare's automatic drawings & sigils, **Hilma af Klint**, Jung's *Red Book*.

**Freemasonry & fraternal esoterica ✗** — tracing boards, aprons, the all-seeing eye, Masonic emblem
charts, Odd Fellows / Rosicrucian-order regalia.

**Neoplatonism & cosmology ◐** — the scale of being, the celestial spheres, the *anima mundi*, Fludd's
& Kircher's universes, sacred-geometry diagrams, mandalas.

**Natural magic & the marvellous ✗** — della Porta's *Magia Naturalis*, the doctrine of signatures,
wonder/monster broadsides, the mandrake, herbals with occult virtues (*Hortus Sanitatis*).

**Mysticism & the bible-occult ✗** — the Witch of Endor, Simon Magus, the Magi/astrologers, Moses vs
Pharaoh's magicians, the Brazen Serpent, the Whore of Babylon, Solomon & the demons — across **every era
of art history** (Byzantine, Romanesque, Gothic, Renaissance, Baroque, Romantic).

### 1B. Periods (the chronological completeness test)
- **Antiquity** ◐ (ouroboros, Zosimos) — *missing:* Gnostic gems, PGM, Mithraic, zodiacs, Orphic, the
  Isis/Apuleius reception.
- **Medieval** ◐ (Aurora Consurgens, Geber) — *missing:* the Obrist corpus in full, Hildegard, Beatus,
  Ars Notoria, astrological MSS, kabbalistic diagrams, Joachimist figurae.
- **Renaissance / early modern** ✓ (emblem books) — *missing:* witchcraft prints, tarot, Dürer's
  *Melencolia I*, Dee, della Porta, Kircher, the Rosicrucian plates.
- **Enlightenment (18th c.)** ✗ — Freemasonry, Sibly, alchemical & masonic revival, the *Geheime Figuren*.
- **Victorian / 19th c.** ✗ — the occult revival, Lévi, the Golden Dawn, Theosophy, spiritualism, Waite-Smith.
- **Modern / 20th c.** ✗ — Crowley/Thoth, Spare, af Klint, Jung — *(scope/rights: much is in copyright; see §6).*

### 1C. Media & object types (we currently catalog only book illustrations)
Books & manuscripts ✓ · single-leaf **prints / woodcuts / engravings / broadsides** ◐ · **paintings**
✗ · **magical gems, amulets, talismans, ritual objects** ✗ · **tarot & playing cards** ✗ · **textiles
/ regalia (Masonic aprons, banners)** ✗ · **architecture & monuments** ✗ · **maps & cosmological charts**
◐ · **scientific instruments (astrolabes, volvelles)** ✗.

---

## 2. Blind spots — things likely not yet considered

1. **Iconclass & Warburg classification.** There is a *standard* iconographic notation (Iconclass) with
   dedicated codes for magic, astrology, witchcraft, divination, and biblical-magic scenes. Enumerating
   by Iconclass code (and the Warburg Institute's Iconographic Database) is the single most powerful path
   to *completeness* — it turns "find everything" into "walk a finite classification tree." *(Codes to be
   filled in from the research agent — see §4B.)*
2. **Reception, not just origins.** Apuleius is the archetype: no ancient illustration survives, but the
   *Isis* iconography and the illustrated *editions* (Renaissance woodcuts onward) are abundant. Many
   "antique" subjects exist only through later art — we need a **reception model** (an image entry can be
   "a later depiction of an ancient subject," dated to the artwork, tagged to the subject).
3. **The bible as an occult image-source.** Magic scenes in canonical religious art (Endor, Simon Magus,
   the Magi, Moses' contest) span every period and museum — a huge, well-digitized, public-domain seam.
4. **Objects beyond the page.** Gems, talismans, tarot decks, Masonic regalia, instruments — held by
   museums (the Met, the BM, the Warburg) with open-access photography. We've only mined *books*.
5. **Scholarly image-compendia as ready-made "wanted lists."** Obrist, Roob (*Alchemy & Mysticism*),
   Klossowski de Rola (*The Golden Game*), Hall (*Secret Teachings*), Yates — each is a curated index of
   specific plates with provenance. Harvesting their figure-lists *is* a coverage spec.
6. **The anti-occult image stream.** Inquisition manuals, Protestant anti-papal prints, witch-trial
   propaganda, debunking literature (Scot's *Discoverie*) — part of the field's visual record.
7. **Non-book scholarship in our own DBs.** RenMagDB / MedievalMagicDB / PicoDB name hundreds of texts,
   manuscripts, and figures with shelfmarks we have never turned into image-sourcing targets.
8. **Provenance & rights as first-class data** for "everything" — pre-1929/PD-vs-CC-vs-in-copyright must
   be tracked per item, because the modern strata (Crowley, af Klint, Jung) are largely restricted.
9. **Cross-cultural sources of Western esotericism** — Islamic alchemy/talismanic (Jabir, the *Picatrix*
   origin), Hebrew kabbalistic MSS, Hellenistic-Egyptian — *in scope as sources*; fully non-Western
   esoterica (Chinese/Indian alchemy, Mesoamerican divination) is a **scope dial** (§6).
10. **Deduplication across editions/copies.** The same emblem recurs in many books/editions; we need an
    "image vs. witness" model so we catalog the *image* once and list its witnesses.

---

## 3. The discovery methodology — five engines

Each engine is a repeatable, LLM-drivable loop that feeds a shared **discovery queue** (`data/wanted.json`,
§5). Engines run in parallel; everything converges on: *propose → verify provenance & rights → source →
author → dedup → catalog.*

### Engine 1 — Compendium harvest (highest yield first)
Take a scholarly image-compendium (start: **Obrist**; then Roob, Klossowski, Hall) and extract its
**complete figure/plate list** into the queue — each with title, the work/MS it's from, holding
institution, and (if given) shelfmark. The compendium's table of plates becomes a coverage checklist.
*LLM task:* "From this plate-list / these footnotes, emit one queue row per distinct image with
{title, source_work, shelfmark, holding_institution, subject_tags}."

### Engine 2 — Iconclass / Warburg systematic enumeration
Walk the Iconclass codes for magic/astrology/witchcraft/divination/biblical-magic (§4B) and the Warburg
Iconographic Database categories. For each node, query the linked open-access collections and enumerate
matching works. This guarantees breadth no keyword search achieves.

### Engine 3 — Repository / IIIF crawl
For each open-access repository (§4A), run subject queries ("alchemy", "nigredo", "witchcraft",
"talisman", "Rosicrucian", "zodiac man", "Simon Magus"…) against its search/IIIF API; collect manifests;
queue candidates with their stable image URLs + rights. Many expose **IIIF** so we can pull
specific pages at high resolution deterministically.

### Engine 4 — Local-materials mining
Map our existing `obrist_medieval` dump to Obrist's catalogue; extract every manuscript/plate named in
RenMagDB/MedievalMagicDB/PicoDB/HermeticDB (shelfmarks, figures, primary sources) into the queue; OCR
local scholarly PDFs for plate-lists. *(Leads from the research agent — §4C.)*

### Engine 5 — Reception / edition tracing
For subjects with no surviving original image (Apuleius, Orpheus, the PGM), trace the **illustrated
editions and the iconographic afterlife**: find the canonical depictions, date them to the artwork, tag
them to the ancient subject. Produces the antiquity-by-reception layer.

### The convergence loop (applies to every engine)
1. **Propose** → queue row (status `proposed`).
2. **Verify** → confirm it's a real, locatable image; resolve the best PD/open source; record rights.
   (status `verified` / `rights_blocked`).
3. **Source** → download via the proven pipeline (Wikimedia `Special:FilePath`, IIIF image API, IA).
4. **Author** → full encyclopedia record (Iconography / Significance / bibliography), per `CLAUDE.md`.
5. **Dedup** → match against existing images; if a known image, add as a *witness*, don't duplicate.
6. **Catalog** → `overrides.json` + rebuild; the queue row closes (`cataloged`).

---

## 4. Source & classification directory

> Concrete endpoints, access methods, and Iconclass codes are being compiled by a research agent and
> will be filled into this section (§4A repositories, §4B Iconclass codes, §4C local leads). Placeholder
> headings below so the structure is stable.

### 4A. Open-access & IIIF repositories (verified 2026-06)

| Repo | Access method | Esoteric strength | License flag |
|---|---|---|---|
| **The Met** (`collectionapi.metmuseum.org/public/collection/v1/`) | REST/JSON, **no key**, 80 req/s; bulk CSV | prints/drawings, emblem & alchemical book illustration, biblical-magic paintings | **CC0** (OA items) |
| **Rijksmuseum** (`data.rijksmuseum.nl`) | **IIIF + OAI-PMH** (old API-key REST deprecated 2026) | huge print collection; emblem/alchemical/astrological prints, biblical-magic | **CC0** |
| **Wikimedia Commons** (`commons.wikimedia.org/w/api.php`) | Action API (`list=categorymembers`, `prop=imageinfo`); see `fetch_commons.py` | curated `Category:Alchemy/Astrology/Witchcraft…`; fastest pre-cropped sets | per-file (PD/CC0/CC-BY-SA) |
| **Internet Archive** (`archive.org/developers`) | metadata API, **scrape API**, direct `/download/`, OCR | largest free trove of out-of-copyright occult books; mirrors offline BL scans | ⚠ mixed (some controlled-lending) |
| **Wellcome Collection** (`api.wellcomecollection.org/catalogue/v2`) | Catalogue API (no key) + **IIIF Image & Presentation** | world-class medical-magic/alchemy/occult MSS; Ripley scrolls | mostly PD/CC-BY; ⚠ per-item |
| **BnF Gallica** (`gallica.bnf.fr/iiif/…/manifest.json`) | **IIIF v1.1 + Presentation v2**; SRU; OAI | deep medieval/early-modern alchemical MSS, French grimoires | PD; ⚠ commercial reuse fee |
| **e-codices** (`e-codices.unifr.ch/…/iiif/…`) | **full IIIF 2.0** | Swiss medieval alchemical/astrological codices (Aurora Consurgens) | ⚠ CC-BY-**NC** |
| **Digital Bodleian** (`digital.bodleian.ox.ac.uk`) | IIIF v2/v3 + Data API | **Ashmole** alchemical/astrological/magical MSS | ⚠ much CC-BY-NC |
| **Getty** (`data.getty.edu`) | IIIF + Linked Art + **SPARQL**; 160k+ Open Content | GRI prints; **Alchemy Special Collection** (Manly P. Hall) | **CC0** Open Content |
| **Library of Congress** (`loc.gov/apis`) | JSON API + IIIF | astrology/almanac prints, emblem books | PD; ⚠ per-item |
| **British Library** | IIIF (degraded) | world-class Harley/Sloane/Royal alchemy+astrology MSS | ⚠ **post-2023 ransomware: APIs partly offline** — use Commons/IA mirrors |

**Specialist esoterica:** **Warburg Iconographic Database** (`iconographic.warburg.sas.ac.uk`, ~106k images, top category "MAGIC AND SCIENCE", free) · **Ritman / Embassy of the Free Mind** (`embassyofthefreemind.com`, largest hermetic/Rosicrucian collection; ⚠ anti-scraping) · **alchemywebsite.com** (Adam McLean, 5,000+ images — best as a *finding aid*; ⚠ he claims copyright on compilations → cite originals from IA/Commons) · **Princeton Index of Medieval Art** (`theindex.princeton.edu`, **free since 2023**) · **Campbell Bonner Magical Gems DB** (`cbd.mfab.hu`, antique Gnostic/Abraxas gems) · **SDBM** (`sdbm.library.upenn.edu`, MS provenance tracking).

**Frictionless first targets:** Met + Rijksmuseum (CC0, no key) → Commons categories → IA scrape API → IIIF (Wellcome/Gallica/e-codices/Bodleian). Tooling: `scripts/fetch_commons.py` already implements the Commons path with license capture.

### 4B. Iconclass codes for systematic enumeration (verified against `iconclass.org/<code>.json`)

Browse `https://iconclass.org/<NOTATION>`; enumerate a branch via the JSON API (returns label + children)
or `https://iconclass.org/api/search?q=<term>`. (Note: magic is **13**, not 11K as one might guess.)

| Subject | Code | Notes |
|---|---|---|
| Magic / occultism (general) | **`13`** | `13A` spirits/ghosts · `13C` magic signs & objects · `13D` enchantment · `13F` microcosmos~macrocosmos |
| Witchcraft / sorcery | **`13B`** | `13B1` witch · `13B3` **witches' sabbath** (`13B33` devil-worship, `13B34` pact) · `13B4` witches at work (`13B41` cauldron, `13B43` raising storms, `13B45` raising the dead) · `13B6` witch-hunt |
| Astrology | **`14`** | `14A` astrologer at work · `14B` horoscope · `14C` astrological signs |
| Zodiac | **`23O`** | `23O5` zodiacal man; individual signs `23O11`…`23O43` |
| Planets / planet-children | **`24C`** | **`24C21` Planetenkinder** · `24C22` + zodiac · `24C3` seven planets as metals |
| Alchemy | **`49E39`** | `49E391` alchemist at work · `49E392` symbols · `49E393` equipment · `49E394` substances · `49E395` processes |
| Divination / necromancy | **`13E`** | `13E41` necromancy (`13E411` necromancer) · `13E7` diviner/soothsayer |
| Devil & demons | **`11K`** | `11K1` human-shaped · `11K2` animal-form · `11K5` devil-worship |
| Witch of Endor | **`71H31`** | Saul & the witch (1 Sam 28); `71H3152` ghost of Samuel appears |
| Fall of Simon Magus | **`73F215365`** | person-key `11I72(SIMON MAGUS)` |
| Adoration of the Magi | **`73B57`** | the Magi as star-following astrologers |
| Moses/Aaron vs Pharaoh's magicians | **`71E11641`** | rods→snakes; `71E114231` rod→serpent miracle |

*(URL-encode `( ) ` and spaces when fetching key-codes as JSON.)* Engine 2 walks these branches against §4A repositories.

### 4C. Local leads (verified on disk)

- **`obrist_medieval/` = Barbara Obrist's two books as page-scans.** 319 JPGs: `obrist_debuts_*` (305 pp.,
  *Les débuts de l'imagerie alchimique*, 1982) + `obrist_visualization_*` (14 pp., *Visualization in Medieval
  Alchemy*). **No machine-readable MS metadata** — the shelfmarks (Buch der heiligen Dreifaltigkeit, Aurora
  Consurgens/Zürich Rh. 172, Pretiosa Margarita Novella…) are in Obrist's captions *inside the page-images*.
  → **Action: OCR the page-scans to recover her plate-list + shelfmarks** (Engine 1+4).
- **`EmeraldTablet/db/emerald_tablet.db`** has the **best provenance schema** —
  `manuscripts(manuscript_id, shelfmark, repository, city, date_year, image_folder)` — but the table is
  **empty**. → Adopt this schema as OCCULTIMGDB's image-provenance model and populate it from Engine 1/4.
- **`MedievalMagicDB`** `bibliography(author,title,year,pdf_path)` + `texts(text_type∈{GRIMOIRE,…},pdf_path)`
  → a local PDF corpus (Kieckhefer; Page & Rider) to mine for plate-lists. **`renmagic.db`** `documents.path`
  names the **Charles Zika witchcraft visual-culture corpus** on disk. Neither has shelfmark/image columns.
- **Local iconography PDFs to harvest (Engine 1):** Urszula **Szulakowska** (3 books on alchemical
  *illustration*, in `Claudiens/`) · Charles **Zika** (witchcraft visual culture, in `renaissance magic/Zika/`)
  · Frances **Yates** (Bruno/Hermetic) · the two **Obrist** PDFs. *(Already-extracted Fludd plates exist at
  `EmblemPrintShop/assets/extracted_all/fludd_mosaicall_p*`.)*
- **To acquire** (densest plate-indexes, not on disk): **Roob** *Alchemy & Mysticism*; **Klossowski de Rola**
  *The Golden Game* (533 engravings); **Manly P. Hall** *Secret Teachings* (PD — on IA).

### 4D. Compendia to harvest (Engine 1 backlog)
- Barbara **Obrist**, *Les débuts de l'imagerie alchimique (XIVe–XVe siècles)* — the foundational catalogue
  of early alchemical imagery. **Top priority.**
- Alexander **Roob**, *Alchemy & Mysticism* (Taschen) — ~700 images, broad survey, full provenance.
- Stanislas **Klossowski de Rola**, *The Golden Game* & *Alchemy: The Secret Art* — engraved-emblem corpus.
- Manly P. **Hall**, *The Secret Teachings of All Ages* — a wide esoteric image-survey (we hold `hall_manuscripts`).
- Adam **McLean**, alchemywebsite.com galleries & his published catalogues.
- Frances **Yates**, *Giordano Bruno…*, *The Art of Memory*, *The Rosicrucian Enlightenment* — for the
  magical-memory and Rosicrucian image sets.

---

## 5. The machine-actionable layer — `data/wanted.json`

A discovery queue that turns this plan into pipeline-consumable work. Engines append rows; the
convergence loop advances `status`. Proposed schema:

```json
{
  "id": "apuleius_isis_initiation",
  "title": "The Initiation of Lucius into the Mysteries of Isis",
  "subject": "apuleius_golden_ass",         // the subject/topic
  "topic": "hermeticism",                    // maps to topics.json
  "period": "antiquity",                      // by SUBJECT
  "via": "reception",                         // direct | reception | edition
  "why": "The Isis-mysteries climax of the Golden Ass; the antique mystery-cult image-source.",
  "candidate_sources": [
    {"where": "Wikimedia Commons / The Met", "note": "later illustrated editions; Isis iconography"}
  ],
  "rights": "unknown",                         // pd | cc | in_copyright | unknown
  "status": "proposed",                        // proposed|verified|rights_blocked|sourced|cataloged
  "engine": "reception",
  "added": "2026-06-27"
}
```

A seed queue (`data/wanted.json`) is created alongside this plan with first targets across all the gaps
(Apuleius/Isis, the Obrist corpus, witchcraft woodcuts, the *Geheime Figuren*, biblical-magic scenes,
Gnostic gems, tarot, Children of the Planets, the Sephirotic tree, Dee's Monas/Sigillum, Lévi's Baphomet,
*Thought-Forms*). `build_db.py` can ingest it into a `wanted` table so coverage/gap reporting is queryable.

---

## 6. Scope dials — decisions that define "everything" (for the user to set)

These genuinely change the size and shape of the corpus. Recommended defaults in **bold**:

1. **Geographic/cultural scope:** *Western esotericism + its direct sources (Hellenistic-Egyptian,
   Islamic alchemy, Hebrew Kabbalah)* **[recommended]** · vs. global occult (adds Chinese/Indian alchemy,
   Mesoamerican divination, African systems — very large).
2. **Period cutoff / copyright:** *Everything public-domain (pre-~1929), plus PD/open-access modern*
   **[recommended]** · vs. include in-copyright modern (Crowley/Harris Thoth, af Klint, Jung) under
   fair-use/thumbnail terms (rights risk).
3. **Object types:** *Books + prints + paintings + objects (gems, tarot, regalia, instruments)*
   **[recommended]** · vs. printed/MS illustration only (tighter, what we do now).
4. **Reception depth:** *Include the iconographic afterlife of subjects with no surviving original*
   **[recommended]** · vs. only contemporaneous images.
5. **The "image vs. witness" model:** adopt it (catalog each image once, list its editions/copies as
   witnesses) **[recommended]** · vs. one row per scanned page (simpler, more duplication).

---

## 7. Prioritized roadmap

**Phase A — wire the machinery (now):** create `data/wanted.json` + the `wanted` DB table + gap report;
adopt the reception model and the rights field in the schema.

**Phase B — highest-yield harvests:** (1) Map & complete the **Obrist** alchemical corpus from `obrist_medieval`
+ the holding libraries. (2) Harvest **Roob** & **Klossowski** plate-lists. (3) The **Geheime Figuren**
Rosicrucian plates (PD, iconic). (4) **Witchcraft** woodcuts (Baldung, *Compendium Maleficarum*). These
turn four `coming_soon` collections live fast.

**Phase C — systematic breadth:** Iconclass/Warburg enumeration (Engine 2) + IIIF crawls (Engine 3)
across astrology (Children of the Planets, zodiac man), divination (tarot history), Kabbalah (Sephirotic
trees), antiquity (Gnostic gems, PGM), and **biblical-magic scenes** across art history.

**Phase D — the modern strata (rights permitting):** Theosophy (*Thought-Forms*), the occult revival
(Lévi, Golden Dawn), spiritualism, and PD-clearable modern works.

**Phase E — objects & reception:** museum open-access for gems, talismans, tarot decks, Masonic regalia,
instruments; the Apuleius/Isis reception layer.

Each phase: run the relevant engine → queue → convergence loop → author full records → rebuild → update
`SOURCINGIMAGES.md`, this plan's status, and the `coming_soon` flags as collections go live.

---

## 8. Direct answers to the questions that started this

- **Apuleius's Golden Ass from late antiquity?** No surviving ancient images exist; we have none of the
  *reception* either. → Engine 5 (reception), Phase E. Source the Isis-mysteries iconography and
  illustrated editions.
- **The complete Obrist alchemical catalogue?** No. We have an unmapped page-dump. → Engine 1 + 4,
  Phase B, **top priority** — it is the closest thing to a finite spec for early alchemical imagery.
- **Every early-printed ceremonial-magic / witchcraft woodcut & pamphlet?** No (≈1). → Engine 1 + 3,
  Phase B/C.
- **Every Rosicrucian image?** Partial. → the *Geheime Figuren* is the keystone gap, Phase B.
- **Every biblical magic scene across art history?** None. → Iconclass enumeration (Engine 2) + museum
  open-access (Engine 3), Phase C — likely one of the largest, best-digitized seams.

The throughline: we don't get to "everything" by sourcing harder. We get there by (a) **mapping the
territory** (§1–2), (b) **harvesting the scholarship that already indexed it** (Engine 1), and (c)
**walking the standard iconographic classifications** (Engine 2) — then letting the convergence loop grind.
