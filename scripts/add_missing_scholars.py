"""Add remaining scholar citations to Mylius, Viridarium, and Ripley entries."""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = r'C:\Dev\OCCULTIMGDB\data\overrides.json'

OBRIST = {
    "text": "Obrist, Barbara. Les Debuts de l'Imagerie Alchimique (XIVe-XVe siecles). Paris: Le Sycomore, 1982.",
    "url": ""
}
PRINCIPE = {
    "text": "Principe, Lawrence M. The Secrets of Alchemy. Chicago: University of Chicago Press, 2013.",
    "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14621946.html"
}
RAMPLING = {
    "text": "Rampling, Jennifer M. The Experimental Fire: Inventing English Alchemy, 1300--1700. Chicago: University of Chicago Press, 2020.",
    "url": "https://press.uchicago.edu/ucp/books/book/chicago/E/bo46025398.html"
}
SZULAKOWSKA = {
    "text": "Szulakowska, Urszula. The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration. Leiden: Brill, 2000.",
    "url": "https://brill.com/display/title/7527"
}

def has(entry, name):
    return any(name in str(c) for c in entry.get('citations', []))

def add(entry, cit):
    existing = [x.get('text','')[:40] for x in entry.get('citations', [])]
    if cit.get('text','')[:40] not in existing:
        entry.setdefault('citations', []).append(cit)

with open(DATA_FILE, encoding='utf-8') as f:
    overrides = json.load(f)

counts = {}
for i, entry in enumerate(overrides):
    work = entry.get('work', '')
    w = None
    if 'Philosophia Reformata' in work:
        w = 'mylius'
        if not has(entry, 'Principe'): add(overrides[i], PRINCIPE); counts[w+'_principe'] = counts.get(w+'_principe',0)+1
        if not has(entry, 'Obrist'): add(overrides[i], OBRIST); counts[w+'_obrist'] = counts.get(w+'_obrist',0)+1
    elif 'Viridarium' in work:
        w = 'viridarium'
        if not has(entry, 'Principe'): add(overrides[i], PRINCIPE); counts[w+'_principe'] = counts.get(w+'_principe',0)+1
        if not has(entry, 'Obrist'): add(overrides[i], OBRIST); counts[w+'_obrist'] = counts.get(w+'_obrist',0)+1
    elif 'Ripley' in work:
        w = 'ripley'
        if not has(entry, 'Principe'): add(overrides[i], PRINCIPE); counts[w+'_principe'] = counts.get(w+'_principe',0)+1
        if not has(entry, 'Obrist'): add(overrides[i], OBRIST); counts[w+'_obrist'] = counts.get(w+'_obrist',0)+1
        if not has(entry, 'Szulakowska'): add(overrides[i], SZULAKOWSKA); counts[w+'_szula'] = counts.get(w+'_szula',0)+1

print("Additions:")
for k, v in sorted(counts.items()):
    print(f"  {k}: +{v}")

with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(overrides, f, ensure_ascii=False, indent=1)
print("Saved.")
