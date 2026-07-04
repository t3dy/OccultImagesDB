# -*- coding: utf-8 -*-
"""
fetch_batch_direct.py — Download images from an overrides batch file using direct Commons URLs.

For each entry in the batch that has a `commons_file` field, looks up the direct image URL
via the Commons API and downloads it to sources_web/<work_key>/<slug>.ext
Also writes a .prov.json sidecar.

TIF files are automatically converted to JPEG (build_catalog only accepts .jpg/.png/.webp).

Usage:
  python scripts/fetch_batch_direct.py data/overrides_batch_XXXX.json [--force]
"""
import io, json, os, re, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WEB = os.path.join(ROOT, "sources_web")
API = "https://commons.wikimedia.org/w/api.php"
UA = "OCCULTIMGDB/1.0 (educational catalog; ted.hand@gmail.com)"


def api_get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def lookup_commons_url(commons_file):
    title = commons_file if commons_file.startswith("File:") else "File:" + commons_file
    data = api_get({
        "action": "query", "format": "json", "titles": title,
        "prop": "imageinfo", "iiprop": "url|extmetadata",
    })
    pages = (data.get("query") or {}).get("pages", {})
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        url = ii.get("url")
        meta = ii.get("extmetadata") or {}
        lic = (meta.get("LicenseShortName") or {}).get("value", "")
        artist = (meta.get("Artist") or {}).get("value", "")
        return url, lic, artist
    return None, None, None


def slugify(s):
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s


def ext_from_url(url):
    path = url.split("?")[0]
    if path.lower().endswith(".png"):
        return ".png"
    elif path.lower().endswith(".tif") or path.lower().endswith(".tiff"):
        return ".jpg"  # will convert via urllib (tiff not useful)
    return ".jpg"


def download(url, dest_path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    # If source is a TIFF and dest is .jpg, convert via PIL
    url_lower = url.split("?")[0].lower()
    if (url_lower.endswith(".tif") or url_lower.endswith(".tiff")) and dest_path.lower().endswith(".jpg"):
        try:
            from PIL import Image
            Image.MAX_IMAGE_PIXELS = None
            img = Image.open(io.BytesIO(data))
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            img.save(dest_path, "JPEG", quality=90)
            return len(data)
        except Exception as conv_err:
            print(f"[tif->jpg conversion failed: {conv_err}, saving raw]", end=" ")
    with open(dest_path, "wb") as f:
        f.write(data)
    return len(data)


def main():
    force = "--force" in sys.argv
    batch_path = next((a for a in sys.argv[1:] if not a.startswith("--")), None)
    if not batch_path:
        print("Usage: python scripts/fetch_batch_direct.py data/overrides_batch_XXX.json [--force]")
        sys.exit(1)

    batch = json.load(open(batch_path, encoding="utf-8"))
    work_key = batch.get("_work", {}).get("key", "unknown")
    entries = batch.get("entries", [])

    dest_dir = os.path.join(WEB, work_key)
    os.makedirs(dest_dir, exist_ok=True)

    ok = skipped = failed = 0
    for entry in entries:
        commons_file = entry.get("commons_file")
        if not commons_file:
            print(f"  SKIP (no commons_file): {entry.get('id')}")
            skipped += 1
            continue

        eid = entry["id"]
        slug = eid.split("__", 1)[-1] if "__" in eid else slugify(commons_file)

        # Determine extension from commons_file name
        cf_lower = commons_file.lower()
        ext = ".png" if cf_lower.endswith(".png") else ".jpg"
        dest_file = os.path.join(dest_dir, slug + ext)
        prov_file = dest_file + ".prov.json"

        if os.path.exists(dest_file) and not force:
            print(f"  EXISTS: {slug + ext}")
            skipped += 1
            continue

        print(f"  Fetching {commons_file} -> {slug + ext} ...", end=" ", flush=True)
        try:
            url, lic, artist = lookup_commons_url(commons_file)
            if not url:
                print("NOT FOUND on Commons")
                failed += 1
                continue
            size = download(url, dest_file)
            prov = {
                "source_url": entry.get("source_url", f"https://commons.wikimedia.org/wiki/{commons_file.replace(' ', '_')}"),
                "provenance_url": entry.get("provenance_url", entry.get("source_url", "")),
                "rights": entry.get("rights") or lic or "Public Domain",
                "artist": artist or "",
                "commons_file": commons_file,
            }
            with open(prov_file, "w", encoding="utf-8") as f:
                json.dump(prov, f, ensure_ascii=False, indent=2)
            print(f"OK ({size // 1024}KB)")
            ok += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"ERROR: {e}")
            failed += 1

    print(f"\nDone: {ok} downloaded, {skipped} skipped, {failed} failed")


if __name__ == "__main__":
    main()
