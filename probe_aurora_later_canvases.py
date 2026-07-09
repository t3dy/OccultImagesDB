"""
Check Aurora Consurgens ZBZ canvases beyond f.36r.
We have f.1r through f.36r in the catalog — check what comes after.
"""
import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

MANIFEST = 'https://www.e-codices.unifr.ch/metadata/iiif/zbz-Ms-Rh-0172/manifest.json'
BASE_LORIS = 'https://www.e-codices.unifr.ch/loris/zbz/zbz-Ms-Rh-0172'

req = urllib.request.Request(MANIFEST, headers={'User-Agent': 'OCCULTIMGDB/1.0'})
with urllib.request.urlopen(req, timeout=20) as r:
    d = json.load(r)

canvases = d['sequences'][0]['canvases']
print(f'Total: {len(canvases)} canvases')

# We have f.1r to f.36r (roughly canvases 3-73 based on labels)
# Let's print canvases from index 70 onward to see what's after folio 36
print('\nCanvases after f.36r (index 70+):')
for i, c in enumerate(canvases[70:130], start=70):
    label = c.get('label', f'canvas_{i}')
    imgs = c.get('images', [])
    res = imgs[0].get('resource', {}) if imgs else {}
    svc = res.get('service', {})
    if isinstance(svc, list): svc = svc[0] if svc else {}
    base = svc.get('@id', '')
    fn = base.split('/')[-1] if base else '?'
    print(f'  [{i:3d}] {label:15s} | {fn}')

print('\nLast 10 canvases:')
for i, c in enumerate(canvases[-10:], start=len(canvases)-10):
    label = c.get('label', f'canvas_{i}')
    print(f'  [{i:3d}] {label}')
