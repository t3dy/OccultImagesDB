# Agent Sourcing Spec — OCCULTIMGDB mass-sourcing campaign

You are ONE domain agent in a parallel campaign to source public-domain occult images and author full
encyclopedia entries. You own exactly one domain (given in your task). Work only in your assigned
subdir and your own batch file — never touch `scripts/config.py`, `data/overrides.json`, or another
agent's files. Project root: `C:\Dev\OCCULTIMGDB`.

## Your pipeline (do all of it)

### 1. Generate targets
Brainstorm 20–35 SPECIFIC, real, public-domain images in your domain that are likely to exist on
**Wikimedia Commons** (museum open-access — Met, British Museum, Rijksmuseum, Wellcome, Getty, BnF,
Walters — plus standard art-history canon). Prefer *named* objects/works/manuscripts with known
repositories. Span the full date-range of your domain. Include physical objects (sculpture, gems,
bowls, mosaics, architecture, amulets, instruments), not only book illustrations, where relevant.

### 2. Source them (iterate!)
Write a jobs file `scripts/jobs_<WORKKEY>.json` — a JSON list of:
`{"query": "...", "out": "<WORKKEY>/<short_stem>.jpg", "prefer": "<substring to prefer in title>"}`
- `out` is relative to `sources_web/`. Use simple stems: lowercase, words separated by `_`, no spaces.
- Run: `python scripts/fetch_commons.py scripts/jobs_<WORKKEY>.json` (from project root, via Bash).
- It downloads the best-resolution PD match + a `.prov.json` sidecar, prints `[ok]`/`[FAIL]` per job.
- **Iterate**: for every `[FAIL]`, rewrite the query (different name, artist, museum, language —
  e.g. German/Latin/French terms) and re-run with a fresh jobs file. Do at least 2–3 retry rounds.
  Aim for 12+ successful downloads; more is better. Tokens are no object — be thorough.
- Some results are flagged `[CHECK-RIGHTS]` (CC BY etc.) — keep them, but record the real license.

### 3. Author full encyclopedia entries
For EACH successfully downloaded image (verify the file exists in `sources_web/<WORKKEY>/`), read its
`.prov.json` for accurate license + source_url + dimensions, then author one entry. Compute the id as:
`<WORKKEY>__<stem>` where `<stem>` is the filename without extension, with every run of
non-alphanumeric chars replaced by a single `-`, lowercased. (e.g. `bes_amulet.jpg` →
`<WORKKEY>__bes-amulet`.)

Entry schema (match EXACTLY; this is merged into the catalog):
```json
{
 "id": "<WORKKEY>__<stem>",
 "title": "Human-readable title (artwork/object name)",
 "work": "<the work title from your _work block>",
 "creator": "artist or 'Anonymous' / culture",
 "date": "date of the ARTWORK/object (not the lost original)",
 "place": "place of origin",
 "era": "antiquity | medieval | renaissance | early_modern | modern",
 "tradition": "alchemy|hermetic|rosicrucian|kabbalah|goetia_grimoire|astrology|theosophy|reception|witchcraft|divination",
 "motifs": ["6-10 specific lowercase motif tags"],
 "medium": "<ONE of: manuscript | woodcut | engraving | etching | drawing | painting | fresco | mosaic | sculpture | relief | gem | amulet | metalwork | ceramic | textile | print | diagram | photograph>",
 "figures": ["named people / deities / personified beings DEPICTED in the image (e.g. Hermes Trismegistus, Saturn, Lilith, Solomon) — [] if none / purely diagrammatic"],
 "repository": "holding institution, e.g. 'Österreichische Nationalbibliothek, Vienna' or 'British Museum' ([PLACEHOLDER: …] if unknown)",
 "shelfmark": "manuscript/accession ref if applicable, e.g. 'cod. 2372, fol. 35r' (omit or '' if a printed book / not applicable)",
 "iconclass": ["optional Iconclass notation code(s) if you confidently know one, e.g. '49E39'; [] if unsure"],
 "rights": "Public domain. Via Wikimedia Commons. (or the real CC BY + institution)",
 "provenance_url": "the source_url from the .prov.json",
 "summary": "Lede sentence.\n\n## Iconography\n<what is literally depicted>\n\n## Significance\n<historical/esoteric meaning, named scholarship, [[motif:x|links]] welcome>\n\n## For artists & game designers\n<one practical note>",
 "citations": [{"text":"Author, *Title* (year)."},{"text":"Wikimedia Commons","url":"<source_url>"}],
 "key_concepts": ["4-6 indexable concepts"],
 "summary_status": "authored"
}
```
Rules: ≤ ~400 words per summary. NEVER invent facts, shelfmarks, or scholarship — if unsure, stay
general and accurate. Date the entry to the surviving artwork. Use `[PLACEHOLDER: …]` only if truly
unknown. Keep Latin/Greek titles italicized. **`medium`, `figures`, `repository` are REQUIRED** (they
power the new relational facets); `shelfmark`/`iconclass` are best-effort. Derive `medium`/`repository`
from the `.prov.json` (commons_title / artist / source) and the object itself — do not guess wildly.

### 4. Write your batch file
Write everything to `data/overrides_batch_<WORKKEY>.json` as:
```json
{
 "_work": {
   "key":"<WORKKEY>","short_id":"<3-4 CAPS>","title":"<Work/collection title>",
   "creator":"various","date":"<range>","century":<int>,"place":"<place>","region":"<region>",
   "language":"<lang>","era":"<dominant era>","tradition":"<dominant tradition>","tier":"illustration",
   "root":"LOCAL","image_dir":"<WORKKEY>",
   "provenance_url":"<a Commons category URL>","rights":"Public domain / CC BY (per item). Via Wikimedia Commons.",
   "motifs":["5-6 domain motifs"],
   "blurb":"<1-2 sentence description of this collection>"
 },
 "entries": [ <one entry object per downloaded image> ]
}
```
`region` ∈ {Europe, England, France, Italy, German lands, Eastern Mediterranean, Egypt, Near East,
Mediterranean, Global}. `tier` always "illustration".

### 5. Return a terse manifest (your final message = data, not prose)
Report: WORKKEY, # images downloaded, # entries authored, any notable rights flags, and any domain
sub-topics you could NOT source (so the orchestrator can queue them). Do not summarize for a human.
