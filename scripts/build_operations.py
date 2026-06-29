# -*- coding: utf-8 -*-
"""Build data/operations.json — the Twelve Alchemical Processes (Ripley's Twelve Gates),
each gathering whole illustrations from across the archive that depict that operation.

Matching is motif/title-driven (precise terms tuned to the real catalog vocabulary), so the
same operation pulls emblems, woodcuts, manuscript miniatures and engravings from many sources.
Regenerable: edit OPERATIONS below and re-run, then commit data/operations.json."""
import json, io, os

HERE = os.path.dirname(__file__)
ROOT = os.path.dirname(HERE)
CAT = os.path.join(ROOT, "data", "catalog.json")
OUT = os.path.join(ROOT, "data", "operations.json")

# Each op: tight `motifs` (matched against the image motif list, lowercased substring),
# `title_terms` (strong words that qualify on their own in the title), and prose.
OPERATIONS = [
  {"key":"calcination","n":1,"name":"Calcination","latin":"Calcinatio","stage":"nigredo",
   "tagline":"The matter burned to ash.",
   "blurb":"The first gate: the raw body is given to the fire — dried, scorched, reduced to a black "
           "ash so the volatile spirit can later be freed. Its creatures are the furnace, the "
           "salamander unburnt in the flame, and the green lion that devours the sun.",
   "motifs":["calcination","green lion","salamander","bellows","furnace fire","incineration"],
   "title_terms":["calcination","calcinatio","green lion","salamander"]},
  {"key":"dissolution","n":2,"name":"Dissolution","latin":"Solutio","stage":"nigredo→albedo",
   "tagline":"The ash drowned in the philosophical water.",
   "blurb":"The second gate: what fire hardened, water now dissolves. The body is returned to its "
           "first moisture — the bath, the falling dew, the flood and the drowning king — so that "
           "form may melt back into prime matter.",
   "motifs":["dissolution","solution","bath","dew","ablution","drowning","flood","mercurial water","immersion"],
   "title_terms":["dissolution","solutio","bath","the drowning","dew"]},
  {"key":"separation","n":3,"name":"Separation","latin":"Separatio","stage":"albedo",
   "tagline":"The subtle divided from the gross.",
   "blurb":"The third gate: the dissolved matter is parted — pure from impure, soul from body, the "
           "fixed from the volatile. Its sign is the sword that divides, the eagle that rises from "
           "the toad, the two that were one made two again.",
   "motifs":["separation","fixed and volatile","sword axe","division","toad"],
   "title_terms":["separation","separatio","fixed and volatile"]},
  {"key":"conjunction","n":4,"name":"Conjunction","latin":"Coniunctio","stage":"albedo",
   "tagline":"The chymical wedding of Sol and Luna.",
   "blurb":"The fourth gate, and the heart of the Work: the purified opposites are married. Sun weds "
           "Moon, King weds Queen, male weds female, and from their embrace comes the Rebis — the "
           "two-headed hermaphrodite in whom the contraries are reconciled.",
   "motifs":["coniunctio","conjunction","king and queen","marriage","hermaphrodite","rebis","sol and luna","sun and moon","coupling","embrace"],
   "title_terms":["conjunction","coniunctio","wedding","marriage","king and queen","hermaphrodite","rebis"]},
  {"key":"putrefaction","n":5,"name":"Putrefaction","latin":"Putrefactio","stage":"nigredo",
   "tagline":"The black death in the sealed grave.",
   "blurb":"The fifth gate: the wedded pair die together and rot in the closed vessel. This is the "
           "nigredo, the blackest night of the Work — the corpse in the tomb, the raven's head, the "
           "toad swollen with poison — without which nothing is reborn.",
   "motifs":["putrefaction","nigredo","death","raven","crow","skull","corpse","tomb","grave","toad","decay"],
   "title_terms":["putrefaction","putrefactio","nigredo","death","the tomb","raven"]},
  {"key":"congelation","n":6,"name":"Congelation","latin":"Congelatio","stage":"albedo",
   "tagline":"The white spirit fixed into a body.",
   "blurb":"The sixth gate: the freed spirit is coagulated again into a white, fixed body — the "
           "albedo, the silver dawn after the black night. The dove descends, the swan whitens, the "
           "scattered is gathered and made to stand.",
   "motifs":["congelation","coagulation","albedo","fixation","white dove","white swan","whitening","crystallization"],
   "title_terms":["congelation","congelatio","coagulation","albedo","whitening"]},
  {"key":"cibation","n":7,"name":"Cibation","latin":"Cibatio","stage":"albedo",
   "tagline":"The infant stone fed and nursed.",
   "blurb":"The seventh gate: the young stone is fed by degrees with its milk and meat — new draughts "
           "of mercurial water and earth — as a nurse feeds a child or the pelican her brood with her "
           "own blood. It is tended until it can bear the fire.",
   "motifs":["cibation","nourishment","pelican","nursing","feeding","milk","nurse"],
   "title_terms":["cibation","cibatio","pelican","nursing","nourishment"]},
  {"key":"sublimation","n":8,"name":"Sublimation","latin":"Sublimatio","stage":"albedo",
   "tagline":"The volatile raised on white wings.",
   "blurb":"The eighth gate: the spirit is lifted up — vapour climbing the glass, the bird of Hermes "
           "ascending and descending, the eagle bearing the body aloft. What was heavy and below is "
           "made subtle and above, then made to fall again, purified.",
   "motifs":["sublimation","ascent","bird of hermes","eagle","dove","vapour","wings","distillation"],
   "title_terms":["sublimation","sublimatio","ascent","bird of hermes"]},
  {"key":"fermentation","n":9,"name":"Fermentation","latin":"Fermentatio","stage":"citrinitas",
   "tagline":"The peacock's tail and the leaven of gold.",
   "blurb":"The ninth gate: a ferment of pure gold is added to quicken the stone, as leaven raises "
           "bread. The matter bursts into the iridescent cauda pavonis — the peacock's tail — every "
           "colour flashing across the glass before it settles toward gold.",
   "motifs":["fermentation","cauda pavonis","peacock","leaven","ferment","all colours"],
   "title_terms":["fermentation","fermentatio","peacock","cauda pavonis"]},
  {"key":"exaltation","n":10,"name":"Exaltation","latin":"Exaltatio","stage":"rubedo",
   "tagline":"The stone lifted to its highest virtue.",
   "blurb":"The tenth gate: the stone is exalted — raised in dignity and power, refined to a higher "
           "nature. It is the ascent of the mountain, the crowning, the glorified body that has put "
           "off corruption and shines.",
   "motifs":["exaltation","glorification","ascension","mountain","crowning","crown","glory"],
   "title_terms":["exaltation","exaltatio","glorification","ascension"]},
  {"key":"multiplication","n":11,"name":"Multiplication","latin":"Multiplicatio","stage":"rubedo",
   "tagline":"The stone's power increased a thousandfold.",
   "blurb":"The eleventh gate: the perfected stone is multiplied — each turn of the wheel increasing "
           "its quantity and its virtue, as one seed yields a harvest. The tree of the philosophers "
           "fruits; a little tinges much, and then far more.",
   "motifs":["multiplication","increase","tree","harvest","sowing","fruit","seed"],
   "title_terms":["multiplication","multiplicatio","the tree","harvest"]},
  {"key":"projection","n":12,"name":"Projection","latin":"Proiectio","stage":"rubedo",
   "tagline":"The red stone cast upon base metal — and gold.",
   "blurb":"The twelfth and final gate: the red stone, the perfected Elixir, is cast upon molten base "
           "metal and transmutes it to gold. The rubedo is complete — the King returns crowned in "
           "red, the phoenix rises, the Great Work is accomplished.",
   "motifs":["projection","rubedo","elixir","philosophers stone","transmutation","phoenix","red king","tincture"],
   "title_terms":["projection","proiectio","rubedo","transmutation","the elixir","red king"]},
]

# visually-rich works that make strong overview covers (colored miniatures / full-plate emblems)
PICTORIAL = {"splendor_solis","aurora_consurgens","atalanta_fugiens","valentine_twelve_keys","stolcius",
             "mylius_plates","lambsprinck","alchemy_visionary","alchemy_emblems_more","magical_creatures"}
FAMOUS = {"atalanta_fugiens","splendor_solis","rosarium","mylius_philosophia","stolcius",
          "valentine_twelve_keys","aurora_consurgens","mutus_liber","lambsprinck","alchemy_visionary",
          "alchemy_emblems_more","pretiosa_margarita","geber_summa","symbola_aureae"}

def img_match(it, op):
    # the Twelve Processes are an alchemical scheme — keep cross-tradition noise (a Tarot Death
    # card, a Holy-Spirit dove) out by scoping to alchemy imagery.
    if it.get("tradition") != "alchemy":
        return False
    mots = [m.lower() for m in (it.get("motifs") or [])]
    motblob = " ".join(mots)
    for t in op["motifs"]:
        if t in motblob:
            return True
    title = (it.get("title") or "").lower()
    for t in op["title_terms"]:
        if t in title:
            return True
    return False

def op_primary(it, op):
    """True if the image carries the operation's defining motif/name — used to pick good covers."""
    blob = " ".join([m.lower() for m in (it.get("motifs") or [])]) + " " + (it.get("title") or "").lower()
    return op["key"] in blob or op["latin"].lower() in blob or op["motifs"][0] in blob

def main():
    cat = json.load(io.open(CAT, encoding="utf-8"))
    items = [i for i in cat["items"] if i.get("tier") != "page_scan"]
    works = {w["key"]: w for w in cat["works"]}
    ops_out = []
    for op in OPERATIONS:
        matched = [i for i in items if img_match(i, op)]
        # cover: prefer an image that NAMES this operation, from a visually-rich pictorial source
        # (colored miniatures / full-plate emblems) over small text-page woodcuts.
        def coverscore(i):
            return (1 if op_primary(i, op) else 0,
                    2 if i["work_key"] in PICTORIAL else (1 if i["work_key"] in FAMOUS else 0),
                    1 if i.get("medium") in ("manuscript", "engraving", "woodcut") else 0)
        cover = max(matched, key=coverscore)["id"] if matched else None
        srcs = sorted({i["work_key"] for i in matched})
        ERA_ORDER = {"antiquity":0,"medieval":1,"renaissance":2,"early_modern":3,"modern":4}
        matched.sort(key=lambda i: (ERA_ORDER.get(i.get("era"),9), i.get("work_key",""), i.get("seq") or 0))
        ops_out.append({k: op[k] for k in ("key","n","name","latin","stage","tagline","blurb")} | {
            "cover": cover, "count": len(matched), "n_sources": len(srcs),
            "image_ids": [i["id"] for i in matched]})
        sample = ", ".join((works.get(i["work_key"], {}).get("title", i["work_key"]))
                           for i in matched[:1])
        print(f"{op['n']:2}. {op['name']:14} {len(matched):4} imgs · {len(srcs):2} sources  cover={cover}")
    json.dump({"title": "The Twelve Processes of the Great Work",
               "intro": "The alchemists divided the making of the Stone into a sequence of operations — "
                        "Ripley's twelve gates, from Calcination to Projection. Each gate below gathers "
                        "illustrations from across the archive that depict the same operation, so you can "
                        "see how Splendor Solis, the Rosarium, Maier, and a dozen other sources each "
                        "imagined calcination, conjunction, or the final projection.",
               "operations": ops_out},
              io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nwrote {OUT} — {len(ops_out)} operations")

if __name__ == "__main__":
    main()
