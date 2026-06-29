# -*- coding: utf-8 -*-
"""
fetch_iiif.py — fetch full-resolution images from IIIF repositories that aren't on Wikimedia Commons
(Gallica/BnF, e-codices, NLI, Wellcome, museum IIIF). Use for targets the Commons pipeline can't reach.

Jobs file: a list of entries, each one of:
  {"image_url": "https://.../full/full/0/native.jpg", "out": "subdir/file.jpg", "rights": "...", "source": "..."}
  {"gallica_ark": "12148/bpt6k8584280", "vue": 953, "out": "subdir/file.jpg", "rights":"Public domain. BnF/Gallica."}
     -> https://gallica.bnf.fr/iiif/ark:/{ark}/f{vue}/full/full/0/native.jpg
  {"iiif_id": "https://.../iiif/imageid", "region":"full", "size":"full", "out":"..."}
     -> {iiif_id}/{region}/{size}/0/default.jpg

Writes the image + a .prov.json sidecar (rights/source must be supplied — IIIF carries no license inline).
Usage:  python scripts/fetch_iiif.py jobs.json [--force]
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WEB = os.path.join(ROOT, "sources_web")
UA = "OCCULTIMGDB/1.0 (educational catalog; ted.hand@gmail.com)"


def url_for(job):
    if job.get("image_url"):
        return job["image_url"]
    if job.get("gallica_ark"):
        return f"https://gallica.bnf.fr/iiif/ark:/{job['gallica_ark']}/f{job['vue']}/full/full/0/native.jpg"
    if job.get("iiif_id"):
        return f"{job['iiif_id'].rstrip('/')}/{job.get('region','full')}/{job.get('size','full')}/0/default.jpg"
    raise ValueError("job needs image_url, gallica_ark, or iiif_id")


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://gallica.bnf.fr/"})
    with urllib.request.urlopen(req, timeout=180) as r, open(dest, "wb") as f:
        f.write(r.read())


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    jobs = json.load(open(args[0], encoding="utf-8"))
    try:
        from PIL import Image
    except Exception:
        Image = None
    ok = skip = fail = 0
    for job in jobs:
        out = os.path.join(WEB, job["out"])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if os.path.exists(out) and not force:
            print(f"[skip] {job['out']}"); skip += 1; continue
        try:
            url = url_for(job)
            download(url, out)
            dims = ""
            if Image:
                with Image.open(out) as im:
                    dims = f"{im.size[0]}x{im.size[1]}"
            prov = {"source_url": job.get("source", url), "original_url": url,
                    "license": job.get("rights", "[verify rights]"), "via": "IIIF"}
            json.dump(prov, open(out + ".prov.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print(f"[ok] {job['out']:42s} {dims:>11s}  {url[:60]}")
            ok += 1
        except Exception as e:
            print(f"[FAIL] {job['out']}: {e}"); fail += 1
    print(f"\n{ok} downloaded, {skip} skipped, {fail} failed.")


if __name__ == "__main__":
    main()
