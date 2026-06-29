# -*- coding: utf-8 -*-
"""
fetch_svg.py — companion to fetch_commons.py for SVG-only Wikimedia files (sigils, seals, diagrams
that Commons stores as vector and fetch_commons skips). Searches Commons for an image/svg+xml match,
downloads the SVG, and rasterizes it to a high-res PNG via svglib+reportlab. Writes a .prov.json sidecar.

Jobs file: a list of {"query": "...", "out": "subdir/file.png", "prefer": "optional title substring"}.
`out` should end in .png (it's the rasterized result), relative to sources_web/.

Usage:  python scripts/fetch_svg.py jobs.json [--force] [--width 1400]
"""
import json, os, sys, urllib.parse, urllib.request, re

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


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def search_svg(query, prefer=None):
    data = api_get({
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": query, "gsrnamespace": "6", "gsrlimit": "15",
        "prop": "imageinfo", "iiprop": "url|size|mime|extmetadata",
    })
    pages = (data.get("query", {}) or {}).get("pages", {})
    out = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("mime", "") != "image/svg+xml":
            continue
        meta = ii.get("extmetadata", {}) or {}
        lic = (meta.get("LicenseShortName", {}) or {}).get("value", "")
        usage = (meta.get("UsageTerms", {}) or {}).get("value", "")
        artist = (meta.get("Artist", {}) or {}).get("value", "")
        is_pd = any(h in (lic + " " + usage).lower() for h in PD_HINTS)
        out.append({"title": p.get("title"), "url": ii.get("url"), "license": lic or usage,
                    "artist": strip_html(artist), "desc": ii.get("descriptionurl"), "is_pd": is_pd})

    def score(c):
        pref = 1 if (prefer and prefer.lower() in (c["title"] or "").lower()) else 0
        return (pref, 1 if c["is_pd"] else 0)
    out.sort(key=score, reverse=True)
    return out


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())


def rasterize(svg_path, png_path, target_w):
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM
    drawing = svg2rlg(svg_path)
    if drawing is None:
        raise RuntimeError("svg2rlg returned None")
    if drawing.width and drawing.width > 0:
        scale = max(1.0, target_w / float(drawing.width))
        drawing.scale(scale, scale)
        drawing.width *= scale
        drawing.height *= scale
    renderPM.drawToFile(drawing, png_path, fmt="PNG", bg=0xFFFFFF)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    width = 1400
    if "--width" in sys.argv:
        width = int(sys.argv[sys.argv.index("--width") + 1])
    jobs = json.load(open(args[0], encoding="utf-8"))
    ok = skip = fail = 0
    for job in jobs:
        out = os.path.join(WEB, job["out"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if os.path.exists(out) and not force:
            print(f"[skip] {job['out']}"); skip += 1; continue
        try:
            cands = search_svg(job["query"], job.get("prefer"))
            if not cands:
                print(f"[FAIL] no svg for: {job['query']}"); fail += 1; continue
            c = cands[0]
            tmp = out + ".svg"
            download(c["url"], tmp)
            rasterize(tmp, out, width)
            os.remove(tmp)
            prov = {"query": job["query"], "commons_title": c["title"], "source_url": c["desc"],
                    "original_url": c["url"], "license": c["license"], "artist": c["artist"],
                    "is_pd": c["is_pd"], "format": "svg->png"}
            json.dump(prov, open(out + ".prov.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            flag = "" if c["is_pd"] else "  [CHECK-RIGHTS]"
            print(f"[ok] {job['out']:40s} {c['title'][5:50]} [{c['license']}]{flag}".encode("ascii", "replace").decode())
            ok += 1
        except Exception as e:
            print(f"[FAIL] {job['out']}: {e}"); fail += 1
    print(f"\n{ok} rasterized, {skip} skipped, {fail} failed.")


if __name__ == "__main__":
    main()
