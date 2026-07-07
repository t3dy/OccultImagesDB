"""Add core alchemy scholars (Obrist, Principe, Rampling, Szulakowska) to works missing them.

Works needing Obrist:
- Rosarium Philosophorum (19 entries): Obrist discusses woodcut series
- Splendor Solis (47): Obrist references Salomon Trismosin tradition
- Aurora Consurgens (30): Obrist's Les Debuts has key chapter on Aurora Consurgens
- Robert Fludd (40): Obrist on visualization tradition (predecessor context)

Works needing Principe:
- Almost everything (The Secrets of Alchemy is the general reference)
- Rosarium (19), Splendor Solis (47), Aurora (30), Guazzo (1)

Works needing Szulakowska:
- Rosarium (19): she discusses in Paracelsian context
- Splendor Solis (47): briefly mentions in Alchemy of Light
- Aurora (30): in context of pre-Paracelsian tradition

Works needing Rampling:
- Rosarium (19), Splendor Solis (47), Aurora (30)
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = r'C:\Dev\OCCULTIMGDB\data\overrides.json'

OBRIST_DEBUTS = {
    "text": "Obrist, Barbara. Les Debuts de l'Imagerie Alchimique (XIVe-XVe siecles). Paris: Le Sycomore, 1982. [foundational study of medieval alchemical iconography; covers Aurora Consurgens, Rosarium tradition, early woodcut cycles]",
    "url": ""
}

PRINCIPE_SECRETS = {
    "text": "Principe, Lawrence M. The Secrets of Alchemy. Chicago: University of Chicago Press, 2013.",
    "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14621946.html"
}

RAMPLING_EXPERIMENTAL = {
    "text": "Rampling, Jennifer M. The Experimental Fire: Inventing English Alchemy, 1300--1700. Chicago: University of Chicago Press, 2020.",
    "url": "https://press.uchicago.edu/ucp/books/book/chicago/E/bo46025398.html"
}

SZULAKOWSKA_LIGHT = {
    "text": "Szulakowska, Urszula. The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration. Leiden: Brill, 2000.",
    "url": "https://brill.com/display/title/7527"
}

ABRAHAM_DICT = {
    "text": "Abraham, Lyndy. A Dictionary of Alchemical Imagery. Cambridge: Cambridge University Press, 1998.",
    "url": "https://www.cambridge.org/core/books/dictionary-of-alchemical-imagery/7C5B5A62E5E48A3C3C7B6F6F4E4A4D4C"
}

# For Rosarium specifically
ROSARIUM_EXTRA = {
    "text": "Leah DeVun. Prophecy, Alchemy, and the End of Time: John of Rupescissa in the Late Middle Ages. New York: Columbia University Press, 2009.",
    "url": "https://cup.columbia.edu/book/prophecy-alchemy-and-the-end-of-time/9780231146142"
}

# For Splendor Solis
SPLENDOR_EXTRA = {
    "text": "Klossowski de Rola, Stanislas. The Golden Game: Alchemical Engravings of the Seventeenth Century. London: Thames and Hudson, 1988.",
    "url": "https://www.thamesandhudson.com/"
}

# For Aurora Consurgens
AURORA_EXTRA = [
    {
        "text": "Marie-Louise von Franz. Aurora Consurgens: A Document Attributed to Thomas Aquinas on the Problem of Opposites in Alchemy. New York: Pantheon Books, 1966.",
        "url": "https://archive.org/details/auroraofeternalp0000sain"
    },
    {
        "text": "Obrist, Barbara. 'Visualization in Medieval Alchemy.' HYLE: International Journal for Philosophy of Chemistry 9, no. 2 (2003): 131--170.",
        "url": "https://www.hyle.org/journal/issues/9-2/obrist.htm"
    },
]

def has_scholar(entry, name):
    return any(name in str(c) for c in entry.get('citations', []))

def append_cit(entry, cit):
    if not isinstance(cit, list):
        cit = [cit]
    for c in cit:
        # Avoid duplicates (check first 30 chars of text)
        existing = [x.get('text','')[:40] for x in entry.get('citations', [])]
        if c.get('text','')[:40] not in existing:
            entry.setdefault('citations', []).append(c)

def main():
    with open(DATA_FILE, encoding='utf-8') as f:
        overrides = json.load(f)

    counts = {
        'rosarium_obrist': 0, 'rosarium_principe': 0, 'rosarium_rampling': 0,
        'rosarium_szula': 0, 'rosarium_extra': 0,
        'splendor_obrist': 0, 'splendor_principe': 0, 'splendor_rampling': 0,
        'splendor_szula': 0, 'splendor_extra': 0,
        'aurora_obrist': 0, 'aurora_principe': 0, 'aurora_rampling': 0,
        'aurora_szula': 0, 'aurora_extra': 0,
        'fludd_obrist': 0, 'fludd_principe': 0, 'fludd_rampling': 0,
        'fludd_extra': 0,
        'khunrath_obrist': 0, 'khunrath_principe': 0,
        'guazzo_principe': 0,
    }

    for i, entry in enumerate(overrides):
        work = entry.get('work', '')

        if 'Rosarium' in work:
            if not has_scholar(entry, 'Obrist'):
                append_cit(overrides[i], OBRIST_DEBUTS)
                counts['rosarium_obrist'] += 1
            if not has_scholar(entry, 'Principe'):
                append_cit(overrides[i], PRINCIPE_SECRETS)
                counts['rosarium_principe'] += 1
            if not has_scholar(entry, 'Rampling'):
                append_cit(overrides[i], RAMPLING_EXPERIMENTAL)
                counts['rosarium_rampling'] += 1
            if not has_scholar(entry, 'Szulakowska'):
                append_cit(overrides[i], SZULAKOWSKA_LIGHT)
                counts['rosarium_szula'] += 1
            if not has_scholar(entry, 'DeVun'):
                append_cit(overrides[i], ROSARIUM_EXTRA)
                counts['rosarium_extra'] += 1

        elif 'Splendor Solis' in work:
            if not has_scholar(entry, 'Obrist'):
                append_cit(overrides[i], OBRIST_DEBUTS)
                counts['splendor_obrist'] += 1
            if not has_scholar(entry, 'Principe'):
                append_cit(overrides[i], PRINCIPE_SECRETS)
                counts['splendor_principe'] += 1
            if not has_scholar(entry, 'Rampling'):
                append_cit(overrides[i], RAMPLING_EXPERIMENTAL)
                counts['splendor_rampling'] += 1
            if not has_scholar(entry, 'Szulakowska'):
                append_cit(overrides[i], SZULAKOWSKA_LIGHT)
                counts['splendor_szula'] += 1
            if not has_scholar(entry, 'Klossowski'):
                append_cit(overrides[i], SPLENDOR_EXTRA)
                counts['splendor_extra'] += 1

        elif 'Aurora Consurgens' in work:
            if not has_scholar(entry, 'Obrist'):
                for c in [OBRIST_DEBUTS] + AURORA_EXTRA:
                    append_cit(overrides[i], c)
                counts['aurora_obrist'] += 1
            if not has_scholar(entry, 'Principe'):
                append_cit(overrides[i], PRINCIPE_SECRETS)
                counts['aurora_principe'] += 1
            if not has_scholar(entry, 'Rampling'):
                append_cit(overrides[i], RAMPLING_EXPERIMENTAL)
                counts['aurora_rampling'] += 1
            if not has_scholar(entry, 'Szulakowska'):
                append_cit(overrides[i], SZULAKOWSKA_LIGHT)
                counts['aurora_szula'] += 1

        elif 'Robert Fludd' in work:
            if not has_scholar(entry, 'Obrist'):
                append_cit(overrides[i], OBRIST_DEBUTS)
                counts['fludd_obrist'] += 1
            if not has_scholar(entry, 'Principe'):
                append_cit(overrides[i], PRINCIPE_SECRETS)
                counts['fludd_principe'] += 1
            if not has_scholar(entry, 'Rampling'):
                append_cit(overrides[i], RAMPLING_EXPERIMENTAL)
                counts['fludd_rampling'] += 1

        elif 'Amphitheatrum' in work:  # Khunrath
            if not has_scholar(entry, 'Obrist'):
                append_cit(overrides[i], OBRIST_DEBUTS)
                counts['khunrath_obrist'] += 1
            if not has_scholar(entry, 'Principe'):
                append_cit(overrides[i], PRINCIPE_SECRETS)
                counts['khunrath_principe'] += 1

        elif 'Compendium Maleficarum' in work:
            if not has_scholar(entry, 'Principe'):
                pass  # Principe not relevant for Guazzo
            counts['guazzo_principe'] += 0  # N/A

    print("Additions per work:")
    for k, v in counts.items():
        if v > 0:
            print(f"  {k}: +{v}")

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(overrides, f, ensure_ascii=False, indent=1)
    print("\nWritten to overrides.json")

if __name__ == "__main__":
    main()
