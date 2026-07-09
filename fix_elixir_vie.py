"""Fix Elixir de vie provenance_url and optionally download a better copy."""
import urllib.request, json, sys, os, shutil
sys.stdout.reconfigure(encoding='utf-8')

CORRECT_FILENAME = 'Ill_dict_infernal_p0250-234_elixir_de_vie.jpg'

# Get correct image info from Commons
url = f'https://commons.wikimedia.org/w/api.php?action=query&titles=File:{urllib.request.quote(CORRECT_FILENAME)}&prop=imageinfo&iiprop=url|size|thumburl&iiurlwidth=1200&format=json'
req = urllib.request.Request(url, headers={'User-Agent': 'OCCULTIMGDB/1.0'})
with urllib.request.urlopen(req, timeout=15) as r:
    d = json.load(r)

pages = d['query']['pages']
for pid, pg in pages.items():
    if pg.get('missing') is not None:
        print(f'ERROR: File not found on Commons: {CORRECT_FILENAME}')
        sys.exit(1)
    ii = pg['imageinfo'][0]
    full_url = ii['url']
    thumb_url = ii.get('thumburl', full_url)
    w, h = ii.get('width', 0), ii.get('height', 0)
    sz = ii.get('size', 0)
    print(f'Commons file: {CORRECT_FILENAME}')
    print(f'  Full: {w}x{h}, {sz//1024}KB')
    print(f'  URL: {full_url[:80]}')
    print(f'  Thumb URL: {thumb_url[:80]}')

# Check current file
current = r'sources_web\dict_infernal\elixir_vie.jpg'
cur_sz = os.path.getsize(current) if os.path.exists(current) else 0
print(f'\nCurrent file: {cur_sz//1024}KB')

# Download if current is smaller than available
download_url = thumb_url if sz > 300000 else full_url
print(f'\nDownloading from: {download_url[:80]}')
try:
    req2 = urllib.request.Request(download_url, headers={'User-Agent': 'OCCULTIMGDB/1.0'})
    with urllib.request.urlopen(req2, timeout=30) as r2:
        data = r2.read()
    # Save to temp then replace if bigger
    tmp = current + '.new'
    with open(tmp, 'wb') as f:
        f.write(data)
    new_sz = os.path.getsize(tmp)
    print(f'Downloaded: {new_sz//1024}KB')
    if new_sz > cur_sz:
        os.replace(tmp, current)
        print('Replaced with larger version')
    else:
        os.remove(tmp)
        print('Kept existing (same or larger)')
except Exception as e:
    print(f'Download error: {e}')

# Fix the override provenance_url
with open('data/overrides.json', encoding='utf-8') as f:
    overrides = json.load(f)

correct_prov = f'https://commons.wikimedia.org/wiki/File:{CORRECT_FILENAME}'
changed = 0
for o in overrides:
    if o.get('id') == 'dict_infernal__elixir-vie':
        old = o.get('provenance_url', '')
        o['provenance_url'] = correct_prov
        print(f'\nFixed provenance_url:')
        print(f'  Old: {old}')
        print(f'  New: {correct_prov}')
        changed += 1

if changed:
    with open('data/overrides.json', 'w', encoding='utf-8') as f:
        json.dump(overrides, f, indent=2, ensure_ascii=False)
    print('Saved overrides.json')
else:
    print('No override found to fix')
