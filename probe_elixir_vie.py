"""Find correct Commons filename for Elixir de vie (Dict Infernal)."""
import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

titles = [
    'Elixir_de_vie.png',
    'Elixir_de_vie.jpg',
    'Elixir de vie.jpg',
    'Dictionnaire_infernal_elixir_de_vie.jpg',
    'P._Christian_-_Histoire_de_la_magie_-_elixir.jpg',
    'Collin_de_Plancy_Dictionnaire_Infernal_Elixir_de_vie.jpg',
]

print("Checking Commons filenames for Elixir de vie...")
for t in titles:
    t_enc = t.replace(' ', '_')
    url = f'https://commons.wikimedia.org/w/api.php?action=query&titles=File:{urllib.request.quote(t_enc)}&prop=imageinfo&iiprop=url|size&format=json'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'OCCULTIMGDB/1.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.load(r)
        pages = d['query']['pages']
        for pid, pg in pages.items():
            if pg.get('missing') is not None:
                print(f'  MISSING: {t_enc}')
            else:
                ii = pg.get('imageinfo', [{}])[0]
                sz = ii.get('size', 0)
                w, h = ii.get('width', 0), ii.get('height', 0)
                u = ii.get('url', '?')
                print(f'  FOUND: {t_enc} ({w}x{h}, {sz//1024}KB)')
                print(f'    URL: {u[:80]}')
    except Exception as e:
        print(f'  ERROR {t_enc}: {e}')

# Also try Commons search API
print('\nSearching Commons for "elixir de vie" in category:')
search_url = 'https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch=elixir+de+vie+dictionnaire+infernal&srnamespace=6&srlimit=10&format=json'
try:
    req = urllib.request.Request(search_url, headers={'User-Agent': 'OCCULTIMGDB/1.0'})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.load(r)
    for res in d['query']['search']:
        print(f'  {res["title"]}')
except Exception as e:
    print(f'  Search error: {e}')
