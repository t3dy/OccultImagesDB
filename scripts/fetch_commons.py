# -*- coding: utf-8 -*-
"""
fetch_commons.py — Engine 3 sourcing tool. Query the Wikimedia Commons API for the best-quality
public-domain image matching each job, download the original, validate, and record provenance.

Jobs file (default scripts/fetch_jobs.json): a list of
  {"query": "...", "out": "subdir/file.jpg", "prefer": "optional substring to prefer in the title"}
`out` is relative to sources_web/. Writes the image + a sibling <file>.prov.json with license/artist/
source URL. Idempotent (skips existing unless --force).

Usage:  python scripts/fetch_commons.py [jobs.json] [--force]
"""
import json
import os
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WEB = os.path.join(ROOT, "sources_web")
API = "https://commons.wikimedia.org/w/api.php"
UA = "OCCULTIMGDB/1.0 (educational catalog; ted.hand@gmail.com)"
PD_HINTS = ("public domain", "pd-", "cc0", "cc-zero", "no known copyright", "pd-art", "pd-old")


def api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def search(query, prefer=None):
    """Return list of candidate dicts {title,url,width,height,mime,license,artist,desc} sorted best-first."""
    data = api_get({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrnamespace": "6", "gsrlimit": "12",
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
    })
    pages = (data.get("query", {}) or {}).get("pages", {})
    out = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        mime = ii.get("mime", "")
        if mime not in ("image/jpeg", "image/png", "image/tiff"):
            continue
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        usage = (meta.get("UsageTerms", {}) or {}).get("value", "")
        artist = (meta.get("Artist", {}) or {}).get("value", "")
        licblob = (lic + " " + usage).lower()
        is_pd = any(h in licblob for h in PD_HINTS)
        out.append({
            "title": p.get("title"), "url": ii.get("url"), "width": ii.get("width", 0),
            "height": ii.get("height", 0), "mime": mime, "license": lic or usage,
            "artist": strip_html(artist), "desc": ii.get("descriptionurl"),
            "is_pd": is_pd, "rank": p.get("index", 99),
        })
    def score(c):
        pref = 1 if (prefer and prefer.lower() in (c["title"] or "").lower()) else 0
        return (pref, 1 if c["is_pd"] else 0, c["width"])
    out.sort(key=score, reverse=True)
    return out


def strip_html(s):
    import re
    return re.sub(r"<[^>]+>", "", s or "").strip()


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    jobs_path = args[0] if args else os.path.join(HERE, "fetch_jobs.json")
    jobs = json.load(open(jobs_path, encoding="utf-8"))
    try:
        from PIL import Image
        Image.MAX_IMAGE_PIXELS = None  # museum masters are huge; don't trip the decompression-bomb guard
    except Exception:
        Image = None

    def cap_size(path, max_edge=3500, max_bytes=20 * 1024 * 1024):
        """Downsize over-large originals so the repo stays under GitHub's 100MB file limit."""
        if not Image:
            return
        try:
            if os.path.getsize(path) < max_bytes:
                return
            with Image.open(path) as im:
                w, h = im.size
                if max(w, h) <= max_edge and os.path.getsize(path) < 25 * 1024 * 1024:
                    return
                s = min(1.0, max_edge / float(max(w, h)))
                im = im.convert("RGB").resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
                im.save(path, "JPEG", quality=88, optimize=True)
        except Exception:
            pass
    ok = skip = fail = 0
    for job in jobs:
        out = os.path.join(WEB, job["out"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if os.path.exists(out) and not force:
            print(f"[skip] {job['out']} (exists)"); skip += 1; continue
        try:
            cands = search(job["query"], job.get("prefer"))
            if not cands:
                print(f"[FAIL] no image for: {job['query']}"); fail += 1; continue
            c = cands[0]
            download(c["url"], out)
            # Commons holds many high-value plates (Maier, Valentine's Keys, Crowning of Nature) ONLY as
            # TIFF; the web can't display them and they'd sit as TIFF-bytes-in-a-.jpg. Transcode to JPEG.
            if Image and c["mime"] == "image/tiff":
                try:
                    with Image.open(out) as im:
                        w, h = im.size
                        s = min(1.0, 3500 / float(max(w, h)))
                        if s < 1.0:
                            im = im.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
                        im.convert("RGB").save(out, "JPEG", quality=88, optimize=True)
                except Exception as e:
                    print(f"[FAIL] {job['out']}: TIFF decode {e}"); fail += 1; os.remove(out); continue
            cap_size(out)
            dims = ""
            if Image:
                with Image.open(out) as im:
                    dims = f"{im.size[0]}x{im.size[1]}"
            prov = {"query": job["query"], "commons_title": c["title"], "source_url": c["desc"],
                    "original_url": c["url"], "license": c["license"], "artist": c["artist"],
                    "width": c["width"], "height": c["height"], "is_pd": c["is_pd"]}
            json.dump(prov, open(out + ".prov.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            flag = "" if c["is_pd"] else "  [CHECK-RIGHTS]"
            line = f"[ok] {job['out']:42s} {dims:>11s}  {c['title'][5:48]}  [{c['license']}]{flag}"
            print(line.encode("ascii", "replace").decode("ascii"))
            ok += 1
        except Exception as e:
            print(f"[FAIL] {job['out']}: {e}"); fail += 1
    print(f"\n{ok} downloaded, {skip} skipped, {fail} failed.")


if __name__ == "__main__":
    main()
