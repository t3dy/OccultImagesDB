"""Add Szulakowska citations to Fludd, Mylius/Philosophia Reformata, and Viridarium Chymicum entries.

Szulakowska's key scholarship:
1. The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration (Brill, 2000)
   - Focuses on Fludd's optics, Paracelsian alchemy, mathematical cosmology in Fludd/Khunrath
2. The Sacrificial Body and the Day of Doom (Brill, 2006)
   - Eschatological alchemy in Paracelsian and Rosicrucian imagery
3. 'The Alchemical Engravings of Matthieu Merian' in Alchemy and the Alchemists in Literature
   - Mylius's Philosophia Reformata (Merian engravings) analysis
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = r'C:\Dev\OCCULTIMGDB\data\overrides.json'

SZULAKOWSKA_ALCHEMY_OF_LIGHT = {
    "text": "Szulakowska, Urszula. The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration. Leiden: Brill, 2000.",
    "url": "https://brill.com/display/title/7527"
}

SZULAKOWSKA_SACRIFICIAL = {
    "text": "Szulakowska, Urszula. The Sacrificial Body and the Day of Doom: Alchemy and Apocalyptic Discourse in the Protestant Reformation. Leiden: Brill, 2006.",
    "url": "https://brill.com/display/title/12547"
}

# Work titles to match
FLUDD_MATCH = "Robert Fludd"
MYLIUS_MATCH = "Philosophia Reformata"
VIRIDARIUM_MATCH = "Viridarium"

def already_has_szulakowska(entry):
    return any('Szulakowska' in str(c) for c in entry.get('citations', []))

def main():
    with open(DATA_FILE, encoding='utf-8') as f:
        overrides = json.load(f)

    fludd_added = 0
    mylius_added = 0
    viridarium_added = 0

    for i, entry in enumerate(overrides):
        work = entry.get('work', '')
        if already_has_szulakowska(entry):
            continue

        if FLUDD_MATCH in work:
            overrides[i].setdefault('citations', []).append(SZULAKOWSKA_ALCHEMY_OF_LIGHT)
            overrides[i]['citations'].append(SZULAKOWSKA_SACRIFICIAL)
            fludd_added += 1
        elif MYLIUS_MATCH in work:
            overrides[i].setdefault('citations', []).append(SZULAKOWSKA_ALCHEMY_OF_LIGHT)
            mylius_added += 1
        elif VIRIDARIUM_MATCH in work:
            overrides[i].setdefault('citations', []).append(SZULAKOWSKA_ALCHEMY_OF_LIGHT)
            viridarium_added += 1

    print(f"Fludd entries updated: {fludd_added}")
    print(f"Mylius/Philosophia Reformata entries updated: {mylius_added}")
    print(f"Viridarium Chymicum entries updated: {viridarium_added}")
    total = fludd_added + mylius_added + viridarium_added
    print(f"Total updated: {total}")

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(overrides, f, ensure_ascii=False, indent=1)
    print("Written to overrides.json")

if __name__ == "__main__":
    main()
