# -*- coding: utf-8 -*-
"""
import_local_scholarship.py — fold LOCAL scholarly metadata into data/overrides.json.

Sources (read-only, on this machine):
  - C:\\Dev\\Claudiens\\site\\data.json          per-emblem scholarly discourse + alchemical stage + sources
  - C:\\Dev\\EmblemPrintShop\\data\\emblems.json  per-emblem object_catalog -> motif tags

Behaviour:
  - Generates an override record for each Atalanta Fugiens emblem (id atalanta_fugiens__emblem-NN).
  - PRESERVES hand-authored overrides: a record is only (re)written if it is absent OR already carries
    "source":"claudiens_import". Records with no "source" field are treated as hand-authored and kept.
  - Idempotent: re-running refreshes only the imported records.

Run, then rebuild:  python scripts/import_local_scholarship.py && python scripts/build_catalog.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OVERRIDES = os.path.join(ROOT, "data", "overrides.json")
CLAUDIENS = r"C:\Dev\Claudiens\site\data.json"
EMBLEMS = r"C:\Dev\EmblemPrintShop\data\emblems.json"
THEO = r"C:\Dev\TheosophicalAlchemyDB\data\maier_atalanta_fugiens_emblems_metadata.json"

BASE_MOTIFS = ["emblem", "engraving", "atalanta fugiens"]


def load_json(p, default=None):
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"! could not read {p}: {e}")
        return default


def pretty_source(code):
    s = re.sub(r"^AUTH[_\s]*", "", str(code)).replace("_", " ").strip()
    return s.title() if s else None


def motifs_for(num, emblems_by_num):
    rec = emblems_by_num.get(num)
    tags = []
    if rec:
        for o in rec.get("object_catalog", []) or []:
            mid = (o.get("motif_id") or o.get("label") or "").strip().lower().replace("_", " ")
            if mid and mid not in tags:
                tags.append(mid)
    out = list(BASE_MOTIFS)
    for t in tags:
        if t not in out:
            out.append(t)
    return out


def compose_summary(entry, emblems_by_num, num):
    motto = (entry.get("motto") or "").strip()
    discourse = (entry.get("discourse") or "").strip()
    stage = (entry.get("stage") or "").strip()
    sources = [pretty_source(s) for s in (entry.get("sources") or [])]
    sources = [s for s in sources if s]
    erec = emblems_by_num.get(num, {})
    latin = (erec.get("latin_motto") or "").strip()

    parts = []
    if motto:
        head = f"Motto: *{motto}*"
        if latin and latin.lower() not in motto.lower():
            head = f"Motto: *{latin}* — *{motto}*"
        parts.append(head)
    if discourse:
        parts.append("## Reading\n" + discourse)
    tail = []
    if stage:
        tail.append(f"Alchemical phase: **{stage.title()}**.")
    if sources:
        tail.append("Maier's acknowledged sources here include " + ", ".join(sources) + ".")
    if tail:
        parts.append("## In the Work\n" + " ".join(tail))
    parts.append("[PLACEHOLDER: cross-check against H. M. E. de Jong's source commentary and add a "
                 "note on the distinct visual elements present for asset use.]")
    return "\n\n".join(parts)


def roman_label(entry, num):
    roman = entry.get("roman") or str(num)
    label = (entry.get("label") or "").strip()
    if num == 0:
        return f"Atalanta Fugiens — Frontispiece: {label}" if label else "Atalanta Fugiens — Frontispiece"
    return f"Atalanta Fugiens — Emblem {roman}: {label}" if label else f"Atalanta Fugiens — Emblem {roman}"


def main():
    existing = load_json(OVERRIDES, []) or []
    by_id = {r["id"]: r for r in existing}
    hand = {i for i, r in by_id.items() if r.get("source") != "claudiens_import"}

    cl = load_json(CLAUDIENS, {}) or {}
    entries = cl.get("entries", cl if isinstance(cl, list) else [])
    em = load_json(EMBLEMS, []) or []
    emblems_by_num = {}
    for r in em:
        n = r.get("number")
        if n is not None:
            emblems_by_num[int(n)] = r

    added = updated = preserved = 0
    for entry in entries:
        num = entry.get("number")
        if num is None:
            continue
        num = int(num)
        cid = f"atalanta_fugiens__emblem-{num:02d}"
        if cid in hand:
            preserved += 1
            continue
        rec = {
            "id": cid,
            "title": roman_label(entry, num),
            "motifs": motifs_for(num, emblems_by_num),
            "summary": compose_summary(entry, emblems_by_num, num),
            "summary_status": "authored",
            "source": "claudiens_import",
        }
        if cid in by_id:
            updated += 1
        else:
            added += 1
        by_id[cid] = rec

    # --- enrichment pass: scholarly citations + related-emblem links + key concepts.
    #     Additive only (never touches summary/title/motifs) — safe for hand-authored records too.
    theo_raw = load_json(THEO, []) or []
    if isinstance(theo_raw, dict):
        # find the first value that's a list of emblem dicts
        theo = next((v for v in theo_raw.values() if isinstance(v, list)), [])
    else:
        theo = theo_raw
    theo_by_num = {int(t["emblem_number"]): t for t in theo
                   if isinstance(t, dict) and t.get("emblem_number") is not None}
    enriched = 0
    for num in range(0, 51):
        cid = f"atalanta_fugiens__emblem-{num:02d}"
        rec = by_id.get(cid)
        if not rec:
            continue
        citations = []
        t = theo_by_num.get(num)
        if t and t.get("de_jong_pages"):
            citations.append({"text": "H. M. E. de Jong, *Atalanta Fugiens: Sources of an Alchemical "
                                      f"Book of Emblems* (Brill, 1969), pp. {t['de_jong_pages']}."})
        if num >= 1:
            citations.append({"text": f"Furnace and Fugue — digital edition, Emblem {num}",
                              "url": f"https://furnaceandfugue.org/atalanta-fugiens/emblem{num}.html"})
        if citations:
            rec["citations"] = citations
        if t and t.get("related_emblems"):
            rec["related_emblems"] = [int(n) for n in t["related_emblems"]]
        if t and t.get("key_concepts"):
            rec["key_concepts"] = t["key_concepts"]
        if t or num >= 1:
            enriched += 1

    merged = sorted(by_id.values(), key=lambda r: r["id"])
    with open(OVERRIDES, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
    print(f"overrides.json: {len(merged)} records "
          f"(+{added} new imported, {updated} refreshed, {preserved} hand-authored preserved); "
          f"{enriched} enriched with citations/related-emblems.")


if __name__ == "__main__":
    main()
