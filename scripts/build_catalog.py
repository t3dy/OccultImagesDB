# -*- coding: utf-8 -*-
"""
build_catalog.py — scan registered source image dirs, generate web derivatives, emit catalog.json.

Usage:
    python scripts/build_catalog.py            # curated illustration tier only (fast)
    python scripts/build_catalog.py --all      # include raw page-scan sources too
    python scripts/build_catalog.py --force     # regenerate thumbnails/cards even if present
    python scripts/build_catalog.py --limit 20  # cap images per source (for quick test runs)

Idempotent: skips derivatives that already exist unless --force.
Per-image scholarly prose in data/overrides.json (keyed by id) is merged over generated records.
"""
import argparse
import json
import os
import re
import sys

from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE_IMG = os.path.join(ROOT, "site", "images")
THUMB_DIR = os.path.join(SITE_IMG, "thumbs")
CARD_DIR = os.path.join(SITE_IMG, "cards")
DATA_DIR = os.path.join(ROOT, "data")

sys.path.insert(0, HERE)
import config  # noqa: E402

THUMB_MAX = (400, 600)
CARD_MAX = (1200, 1700)  # 1200px long edge keeps the published site under the Pages 1GB cap
IMG_EXTS = (".jpg", ".jpeg", ".png", ".webp")

ROMAN = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
         "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
         "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX",
         "XXXI", "XXXII", "XXXIII", "XXXIV", "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL",
         "XLI", "XLII", "XLIII", "XLIV", "XLV", "XLVI", "XLVII", "XLVIII", "XLIX", "L"]


def roman(n):
    return ROMAN[n] if 0 < n < len(ROMAN) else str(n)


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "x"


def last_number(name):
    nums = re.findall(r"(\d+)", name)
    return int(nums[-1]) if nums else None


def make_title(src, stem, seq):
    """Human-readable title from source + filename sequence."""
    t = src["title"]
    emblem_books = {"atalanta_fugiens", "stolcius", "mylius_plates", "cramer"}
    if seq is None:
        return t
    if src["key"] == "atalanta_fugiens":
        if seq == 0 or "frontis" in stem.lower():
            return f"{t} — Frontispiece"
        return f"{t} — Emblem {roman(seq)}"
    if src["key"] in emblem_books:
        return f"{t} — Emblem {seq}"
    if src["key"] == "rosarium":
        return f"{t} — Woodcut (p. {seq})"
    return f"{t} — Plate {seq}"


def load_provenance(image_dir):
    """Return {basename: {rights, source_url, ...}} from a sibling provenance.json if present."""
    out = {}
    pj = os.path.join(image_dir, "provenance.json")
    if not os.path.isfile(pj):
        return out
    try:
        with open(pj, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return out
    if isinstance(data, list):
        for rec in data:
            ip = rec.get("image_path") or rec.get("path")
            if ip:
                out[os.path.basename(ip)] = {
                    "rights": rec.get("rights"),
                    "provenance_url": rec.get("ia_url") or rec.get("source_url"),
                    "source_name": rec.get("source_name"),
                }
    return out


def gen_derivative(src_path, dst_path, max_size, force):
    if os.path.exists(dst_path) and not force:
        return True
    try:
        with Image.open(src_path) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            im.thumbnail(max_size, Image.LANCZOS)
            im.save(dst_path, "JPEG", quality=82, optimize=True)
        return True
    except Exception as e:
        print(f"  ! failed {os.path.basename(src_path)}: {e}")
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="include page_scan tier")
    ap.add_argument("--force", action="store_true", help="regenerate existing derivatives")
    ap.add_argument("--limit", type=int, default=0, help="max images per source (0 = no cap)")
    args = ap.parse_args()

    os.makedirs(THUMB_DIR, exist_ok=True)
    os.makedirs(CARD_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    overrides = {}
    op = os.path.join(DATA_DIR, "overrides.json")
    if os.path.isfile(op):
        try:
            with open(op, "r", encoding="utf-8") as f:
                overrides = {r["id"]: r for r in json.load(f)}
            print(f"Loaded {len(overrides)} override record(s).")
        except Exception as e:
            print(f"! overrides.json unreadable: {e}")

    records = []
    works = []
    for src in config.SOURCES:
        if src["tier"] == "page_scan" and not args.all:
            continue
        roots = {"BEU": config.ALCHEMY_BEU_ROOT, "LOCAL": config.LOCAL_SOURCED_ROOT}
        root = roots.get(src.get("root"), config.EMBLEM_ROOT)
        image_dir = os.path.join(root, src["image_dir"])
        if not os.path.isdir(image_dir):
            print(f"[skip] {src['key']}: dir not found -> {image_dir}")
            continue
        prov = load_provenance(image_dir)
        files = sorted(f for f in os.listdir(image_dir)
                       if f.lower().endswith(IMG_EXTS))
        if args.limit:
            files = files[:args.limit]
        print(f"[{src['key']}] {len(files)} images  ({src['tier']})")
        count = 0
        for fn in files:
            stem, _ = os.path.splitext(fn)
            seq = last_number(stem)
            cid = f"{src['key']}__{slugify(stem)}"
            src_path = os.path.join(image_dir, fn)
            thumb_path = os.path.join(THUMB_DIR, cid + ".jpg")
            card_path = os.path.join(CARD_DIR, cid + ".jpg")
            if not gen_derivative(src_path, card_path, CARD_MAX, args.force):
                continue
            gen_derivative(src_path, thumb_path, THUMB_MAX, args.force)
            pinfo = prov.get(fn, {})
            rec = {
                "id": cid,
                "title": make_title(src, stem, seq),
                "work": src["title"],
                "work_key": src["key"],
                "short_id": src["short_id"],
                "creator": src["creator"],
                "date": src["date"],
                "century": src["century"],
                "place": src["place"],
                "region": src["region"],
                "language": src["language"],
                "era": src["era"],
                "tradition": src["tradition"],
                "tier": src["tier"],
                "seq": seq,
                "motifs": list(src["motifs"]),
                "rights": pinfo.get("rights") or src["rights"],
                "provenance_url": pinfo.get("provenance_url") or src["provenance_url"],
                "source_file": src_path,
                "thumb": f"images/thumbs/{cid}.jpg",
                "card": f"images/cards/{cid}.jpg",
                "summary": "[PLACEHOLDER: scholarly summary needed — see overrides.json]",
                "summary_status": "placeholder",
            }
            if cid in overrides:
                ov = {k: v for k, v in overrides[cid].items() if v not in (None, "")}
                rec.update(ov)
                if ov.get("summary"):
                    rec["summary_status"] = "authored"
            records.append(rec)
            count += 1
        works.append({
            "key": src["key"], "title": src["title"], "creator": src["creator"],
            "date": src["date"], "era": src["era"], "tradition": src["tradition"],
            "tier": src["tier"], "place": src["place"], "language": src["language"],
            "provenance_url": src["provenance_url"], "rights": src["rights"],
            "blurb": src["blurb"], "count": count,
        })
        print(f"   -> {count} cataloged")

    era_rank = {"antiquity": 0, "medieval": 1, "renaissance": 2, "early_modern": 3, "modern": 4}
    records.sort(key=lambda r: (era_rank.get(r["era"], 9), r["work"], r["seq"] or 0))

    # work_key -> creator-entity key, read from data/entities.json (for relational linking)
    creators_index = {}
    ep = os.path.join(DATA_DIR, "entities.json")
    if os.path.isfile(ep):
        try:
            with open(ep, "r", encoding="utf-8") as f:
                ent = json.load(f)
            for c in ent.get("creators", []):
                for wk in c.get("works", []):
                    creators_index[wk] = c["key"]
        except Exception as e:
            print(f"! entities.json unreadable: {e}")

    catalog = {
        "generated_records": len(records),
        "works": works,
        "creators_index": creators_index,
        "items": records,
    }
    with open(os.path.join(DATA_DIR, "catalog.json"), "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=1)
    with open(os.path.join(DATA_DIR, "works.json"), "w", encoding="utf-8") as f:
        json.dump(works, f, ensure_ascii=False, indent=2)
    authored = sum(1 for r in records if r.get("summary_status") == "authored")
    print(f"\nDONE: {len(records)} items across {len(works)} works "
          f"({authored} with authored summaries, {len(records)-authored} placeholders).")
    print(f"Wrote {os.path.join(DATA_DIR, 'catalog.json')}")


if __name__ == "__main__":
    main()
