"""Try to resolve the e-codices ZBZ Rh. 172 (Aurora Consurgens) URL pattern."""
import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

# e-codices serves IIIF manifests. Known patterns:
# - ZBZ = Zentralbibliothek Zürich
# - Rh. 172 = Rheinau MS 172
# The shelfmark format for ZBZ on e-codices is usually: zbz-XXXX or ZBZ-Ms-XXXX

candidates = [
    # e-codices manifest URL patterns for ZBZ
    'https://www.e-codices.unifr.ch/metadata/iiif/zbz-Ms-Rh-0172/manifest.json',
    'https://www.e-codices.unifr.ch/metadata/iiif/zbz-Rh-172/manifest.json',
    'https://www.e-codices.unifr.ch/metadata/iiif/zbz-Rh-0172/manifest.json',
    'https://www.e-codices.unifr.ch/metadata/iiif/zbz-Ms-Rh172/manifest.json',
    'https://www.e-codices.unifr.ch/metadata/iiif/zbz-Ms-Rheinau-172/manifest.json',
    # Also try the newer e-codices URL format
    'https://e-codices.ch/metadata/iiif/zbz-Ms-Rh-0172/manifest.json',
    'https://e-codices.ch/metadata/iiif/zbz-Rh-0172/manifest.json',
]

for url in candidates:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'OCCULTIMGDB/1.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            status = r.status
            d = json.load(r)
            label = d.get('label', '?')
            seqs = d.get('sequences', [{}])
            n = len(seqs[0].get('canvases', []) if seqs else [])
            print(f'FOUND: {url}')
            print(f'  label={label}, {n} canvases')
    except urllib.error.HTTPError as e:
        print(f'HTTP {e.code}: {url}')
    except Exception as e:
        print(f'ERROR: {url}: {type(e).__name__}: {e}')

# Try the ZBZ direct catalog
print('\nTrying ZBZ direct API...')
zbz_url = 'https://www.zb.uzh.ch/de/suche?q=Rh+172&field=q'
print(f'Manual check needed at: {zbz_url}')
