# -*- coding: utf-8 -*-
"""
import_motifs.py — promote the local motif ONTOLOGY into data/entities.json motif profiles.

Source (read-only): C:\\Dev\\EmblemPrintShop\\data\\motifs.json  (79-entry iconographic ontology with
per-motif description + alchemical_valence + planetary).

Behaviour:
  - For each motif in WHITELIST, build an entities.json motif record (sourced summary, match aliases,
    see_also cross-links).
  - PRESERVES hand-authored motifs: never overwrites a key already present that lacks
    "source":"ontology_import". Hand-authored motifs (ouroboros, green-lion, coniunctio, rebis,
    furnace, dragon) are kept as-is.
  - Idempotent.

Run:  python scripts/import_motifs.py   (entity/browse pages read entities.json directly; no rebuild needed)
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ENTITIES = os.path.join(ROOT, "data", "entities.json")
MOTIFS = r"C:\Dev\EmblemPrintShop\data\motifs.json"

# key -> {aliases (extra catalog motif strings that count), see_also (other motif keys)}
WHITELIST = {
    "king":        {"aliases": ["king", "rex"], "see_also": ["queen", "coniunctio", "lion"]},
    "queen":       {"aliases": ["queen"], "see_also": ["king", "coniunctio", "moon"]},
    "lion":        {"aliases": ["lion"], "see_also": ["green-lion", "sun"]},
    "serpent":     {"aliases": ["serpent", "snake"], "see_also": ["ouroboros", "dragon"]},
    "sun":         {"aliases": ["sun", "sun and moon", "solar"], "see_also": ["moon", "king", "lion"]},
    "moon":        {"aliases": ["moon", "sun and moon"], "see_also": ["sun", "queen"]},
    "tree":        {"aliases": ["tree", "alchemical tree"], "see_also": ["coniunctio"]},
    "bird":        {"aliases": ["bird", "eagle", "two birds"], "see_also": ["furnace"]},
    "vessel":      {"aliases": ["vessel", "flask", "alembic", "retort", "philosophical egg", "egg"], "see_also": ["furnace"]},
    "star":        {"aliases": ["star", "zodiac"], "see_also": ["sun", "moon"]},
    "fountain":    {"aliases": ["fountain", "spring", "bath"], "see_also": ["moon"]},
    "peacock":     {"aliases": ["peacock", "feathers"], "see_also": ["coniunctio"]},
    "angel":       {"aliases": ["angel", "angels"], "see_also": []},
    "sword":       {"aliases": ["sword"], "see_also": ["egg"]},
    "toad":        {"aliases": ["toad"], "see_also": ["dragon"]},
    "salamander":  {"aliases": ["salamander", "fire creature"], "see_also": ["furnace"]},
}


def first_sentence(s):
    s = (s or "").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    return (m.group(1) if m else s)[:160]


def main():
    ent = json.load(open(ENTITIES, encoding="utf-8"))
    onto = json.load(open(MOTIFS, encoding="utf-8"))
    onto = onto if isinstance(onto, list) else onto.get("motifs", [])
    by = {}
    for m in onto:
        k = (m.get("id") or m.get("label", "")).strip().lower()
        by[k] = m

    motifs = ent.get("motifs", [])
    existing = {m["key"]: m for m in motifs}
    hand = {k for k, m in existing.items() if m.get("source") != "ontology_import"}

    added = refreshed = 0
    for key, cfg in WHITELIST.items():
        if key in hand:
            continue
        src = by.get(key)
        if not src:
            print(f"  ! ontology has no '{key}', skipping")
            continue
        desc = src.get("description") or src.get("appearance") or ""
        val = src.get("alchemical_valence") or []
        planetary = src.get("planetary")
        summary = desc.strip()
        if val:
            summary += "\n\n## Alchemical valence\n" + ", ".join(v.replace("_", " ") for v in val) + "."
        if planetary and planetary != "None":
            summary += f"\n\nPlanetary association: *{planetary}*."
        rec = {
            "key": key,
            "name": src.get("label") or key.title(),
            "blurb": first_sentence(desc),
            "summary": summary,
            "match": sorted(set([key] + cfg["aliases"])),
            "see_also": cfg["see_also"],
            "links": [],
            "source": "ontology_import",
        }
        if key in existing:
            refreshed += 1
        else:
            added += 1
        existing[key] = rec

    # preserve order: hand-authored first (original order), then imported alpha
    hand_list = [m for m in motifs if m.get("source") != "ontology_import"]
    hand_keys = {m["key"] for m in hand_list}
    imported = sorted((m for k, m in existing.items() if k not in hand_keys), key=lambda m: m["key"])
    ent["motifs"] = hand_list + imported
    json.dump(ent, open(ENTITIES, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"entities.json motifs: {len(ent['motifs'])} total (+{added} new, {refreshed} refreshed, "
          f"{len(hand_list)} hand-authored preserved).")


if __name__ == "__main__":
    main()
