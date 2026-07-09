"""
Probe ZBZ Rh. 172 (Aurora Consurgens) manifest.
We already have 18 items (aurora-1r, aurora-3r, ...).
Check if there are additional illuminated pages we're missing.
"""
import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

MANIFEST = 'https://www.e-codices.unifr.ch/metadata/iiif/zbz-Ms-Rh-0172/manifest.json'

req = urllib.request.Request(MANIFEST, headers={'User-Agent': 'OCCULTIMGDB/1.0'})
with urllib.request.urlopen(req, timeout=20) as r:
    d = json.load(r)

seqs = d.get('sequences', [])
canvases = seqs[0].get('canvases', []) if seqs else []
print(f'Total canvases: {len(canvases)}')

# Check what IDs we already have in catalog
import os; sys.path.insert(0, 'scripts')
existing_stems = set()
try:
    catalog = json.load(open('data/catalog.json', encoding='utf-8'))
    for item in catalog['items']:
        if item.get('work_key') == 'aurora_consurgens_zbz':
            # stem is after __ in id
            stem = item['id'].split('__', 1)[1] if '__' in item['id'] else item['id']
            existing_stems.add(stem)
    print(f'Already in catalog: {len(existing_stems)} items')
    print(f'  {sorted(existing_stems)[:8]}...')
except Exception as e:
    print(f'Catalog check error: {e}')

# Print all canvases with their labels
print(f'\nAll canvases:')
for i, canvas in enumerate(canvases):
    label = canvas.get('label', f'canvas_{i}')
    # Get first image URL
    images = canvas.get('images', [])
    if images:
        res = images[0].get('resource', {})
        img_url = res.get('@id', '?')
        # Get thumbnail service
        svc = res.get('service', {})
        if isinstance(svc, list): svc = svc[0] if svc else {}
        base = svc.get('@id', '')
        width = res.get('width', 0)
        height = res.get('height', 0)
        print(f'  [{i:3d}] {label} | {width}x{height}')
        if i < 3:
            print(f'         thumb: {base}/full/200,/0/default.jpg' if base else f'         url: {img_url[:60]}')
