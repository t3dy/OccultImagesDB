# -*- coding: utf-8 -*-
"""
merge_batches.py — fold mass-sourcing batch files into the canonical sources.

Reads every data/overrides_batch_*.json ({"_work": {...}, "entries": [...]}):
  - collects each _work into data/works_extra.json   (dedup by key; config.py auto-loads it)
  - merges each entry into data/overrides.json        (dedup by id; batch wins on conflict)

Validates: every entry id starts with its work key; every entry has a matching image file on disk
under sources_web/<work_key>/ (warns on orphans); reports duplicate ids across batches.
Idempotent — safe to re-run after each wave.
"""
import json, io, os, re, glob, sys
sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
WEB = os.path.join(ROOT, "sources_web")
IMG_EXTS = (".jpg", ".jpeg", ".png", ".gif", ".webp")


def slugify(s):
    return re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()


def img_ids_for(work_key):
    """The catalog ids build_catalog will generate for files in sources_web/<work_key>/."""
    d = os.path.join(WEB, work_key)
    if not os.path.isdir(d):
        return set()
    ids = set()
    for f in os.listdir(d):
        if f.lower().endswith(IMG_EXTS):
            ids.add(f"{work_key}__{slugify(os.path.splitext(f)[0])}")
    return ids


def main():
    works_extra_path = os.path.join(DATA, "works_extra.json")
    overrides_path = os.path.join(DATA, "overrides.json")

    works = []
    if os.path.exists(works_extra_path):
        works = json.load(io.open(works_extra_path, encoding="utf-8"))
    works_by_key = {w["key"]: w for w in works}

    overrides = json.load(io.open(overrides_path, encoding="utf-8"))
    ov_by_id = {o["id"]: o for o in overrides}

    batches = sorted(glob.glob(os.path.join(DATA, "overrides_batch_*.json")))
    seen_ids, dup_ids, orphan_entries, added_entries, added_works = set(), [], [], 0, 0

    for bf in batches:
        try:
            b = json.load(io.open(bf, encoding="utf-8"))
        except Exception as e:
            print(f"  [SKIP] {os.path.basename(bf)}: bad JSON ({e})")
            continue
        w = b.get("_work")
        if w and w.get("key"):
            if w["key"] not in works_by_key:
                works.append(w); works_by_key[w["key"]] = w; added_works += 1
            else:
                works_by_key[w["key"]].update(w)
        wk = w["key"] if w else None
        valid_img_ids = img_ids_for(wk) if wk else set()
        for e in b.get("entries", []):
            eid = e.get("id")
            if not eid:
                continue
            if eid in seen_ids:
                dup_ids.append(eid)
            seen_ids.add(eid)
            if wk and not eid.startswith(wk + "__"):
                print(f"  [WARN] id {eid} does not match work key {wk}")
            if valid_img_ids and eid not in valid_img_ids:
                orphan_entries.append(eid)
            if eid not in ov_by_id:
                overrides.append(e); ov_by_id[eid] = e; added_entries += 1
            else:
                # replace in place
                overrides[overrides.index(ov_by_id[eid])] = e
                ov_by_id[eid] = e

    json.dump(works, io.open(works_extra_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    json.dump(overrides, io.open(overrides_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    print(f"batches merged: {len(batches)}")
    print(f"works_extra.json: {len(works)} works (+{added_works} new)")
    print(f"overrides.json:   {len(overrides)} entries (+{added_entries} new)")
    if dup_ids:
        print(f"  DUPLICATE ids across batches ({len(dup_ids)}): {dup_ids[:10]}")
    if orphan_entries:
        print(f"  ORPHAN entries (no image on disk) ({len(orphan_entries)}): {orphan_entries[:10]}")
    if not dup_ids and not orphan_entries:
        print("  validation: clean (no dups, no orphans)")


if __name__ == "__main__":
    main()
