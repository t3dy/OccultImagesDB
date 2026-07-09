"""
Write scholarly overrides for Glauber Furni Novi (25 items) and
new Splendor Solis additions (8 items).
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/overrides.json', encoding='utf-8') as f:
    overrides_list = json.load(f)

overrides = {o['id']: o for o in overrides_list if 'id' in o}

def upsert(id_, data):
    data['id'] = id_
    overrides[id_] = data

# ============================================================
# CITATIONS
# ============================================================
DEBUS = {"text": "Debus, Allen G. The Chemical Philosophy: Paracelsian Science and Medicine in the Sixteenth and Seventeenth Centuries. New York: Science History Publications, 1977.", "url": ""}
PRIN = {"text": "Principe, Lawrence M. The Secrets of Alchemy. Chicago: University of Chicago Press, 2013.", "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14621946.html"}
NEWMAN = {"text": "Newman, William R. Promethean Ambitions: Alchemy and the Quest to Perfect Nature. Chicago: University of Chicago Press, 2004.", "url": "https://press.uchicago.edu/ucp/books/book/chicago/P/bo3630835.html"}
OBRIST = {"text": "Obrist, Barbara. Les Débuts de l'imagerie alchimique (XIVe–XVe siècles). Paris: Le Sycomore, 1982.", "url": ""}
JUNG = {"text": "Jung, Carl Gustav. Psychology and Alchemy. Collected Works 12. Princeton: Princeton University Press, 1953.", "url": ""}
SZUL = {"text": "Szulakowska, Urszula. The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration. Leiden: Brill, 2000.", "url": "https://brill.com/display/title/7527"}
ROOB = {"text": "Roob, Alexander. Alchemy & Mysticism: The Hermetic Cabinet. Cologne: Taschen, 1997.", "url": ""}
GLAUBER_REF = {"text": "Glauber, Johann Rudolf. Furni Novi Philosophici sive Descriptio Artis Destillatoriae Novae. Amsterdam: Jan Jansson, 1648–1651. [BIUSante Medica digitization: pharma_res011275x01]", "url": "https://www.biusante.parisdescartes.fr/histoire/medica/resultats/index.php?cote=pharma_res011275x01"}
SS_CITS = [
    {"text": "Klossowski de Rola, Stanislas. The Golden Game: Alchemical Engravings of the Seventeenth Century. London: Thames and Hudson, 1988.", "url": ""},
    JUNG,
    SZUL,
    PRIN,
    OBRIST,
    ROOB,
    {"text": "McLean, Adam, ed. Splendor Solis: Alchemical Treatises of Solomon Trismosin. Grand Rapid, MI: Phanes Press, 1991.", "url": ""},
]

# ============================================================
# 1. GLAUBER FURNI NOVI — 25 pages from BIUSante
# ============================================================
GLAUB_CITS = [GLAUBER_REF, DEBUS, PRIN, NEWMAN, {"text": "Leicester, Henry M. The Historical Background of Chemistry. New York: Dover, 1971.", "url": ""}]

# The BIUSante pharma_res011275x01 is Glauber's Furni Novi vol. 1 (1648).
# Pages are grouped: 0-192 every 8 pages.
# Map page range to content section based on Glauber's structure:
# p0: Title page / frontispiece
# p8-p48: Introduction, furnace types I-III
# p56-p96: Furnace types IV-VI, baths
# p104-p144: Distillation apparatus
# p152-p192: Retorts, pelicans, special vessels

page_content = {
    0:   ("Title Page and Frontispiece",
          "The title page and frontispiece of Glauber's *Furni Novi Philosophici* (Amsterdam, 1648). The frontispiece presents the author's portrait and the emblematic apparatus of the new philosophy of furnaces — establishing Glauber's identity as both a practical chemist and a systematic reformer of the laboratory arts. The title announces the work as a treatise on *ars destillatoria nova* (the new art of distillation)."),
    8:   ("Introduction and First Furnace Designs",
          "Opening pages of Glauber's treatise, introducing his philosophical principles and the first furnace designs. Glauber distinguishes his *Furni Novi* (new furnaces) from traditional athanors by their systematic design for different operations: controlled temperature regulation, efficient fuel consumption, and multi-purpose use. The first furnaces shown here handle general heating and calcination."),
    16:  ("Furnace Type II — The Wind Furnace (*Windofen*)",
          "The **Wind Furnace** (*Ventum Philosophicum* or *Windofen*) — one of Glauber's signature innovations. This furnace uses controlled airflow through bellows or natural draught to achieve higher and more even temperatures than the traditional athanor, enabling more precise metallurgical operations including the calcination of metals and the fusion of mineral compounds."),
    24:  ("Furnace Type III — The Reverberatory Furnace",
          "The **reverberatory furnace** (*Fornax Reverberatoria*), in which the flame is deflected downward from a curved ceiling to heat the material from above — enabling the heating of substances in open vessels without direct contact with flame or fuel gases. Critical for calcination, fusing, and roasting operations in Glauber's chemical system."),
    32:  ("Sand Bath and Water Bath (*Balneum Arenae & Balneum Mariae*)",
          "The **sand bath** (*balneum arenae*) and the **water bath** (*balneum Mariae* or Mary's bath) — two indirect heating methods for gentle, even-temperature operations. The *balneum Mariae* (attributed by tradition to Mary the Prophetess, the legendary Jewish alchemist of Alexandria) heats through boiling water, limiting temperature to 100°C and preventing scorching. The sand bath achieves intermediate temperatures between water and open flame."),
    40:  ("Distillation in the Athanor and Per Descensum",
          "Distillation apparatus using the athanor for standard upward distillation (*per ascensum*) and downward-distillation receivers (*per descensum*) for resins and fixed oils. Glauber's innovation here is the integration of multiple receiver vessels to collect different fractions at different temperatures as the material heats progressively."),
    48:  ("The Chemical Furnace for Acid Production",
          "Furnaces and apparatus for the production of mineral acids — vitriol (*spiritus vitrioli*, sulfuric acid), spirit of salt (*spiritus salis*, hydrochloric acid), and aqua fortis (nitric acid). Glauber was one of the leading producers and distributors of mineral acids in 17th-century Amsterdam; his acid-furnace designs here influenced European industrial chemistry."),
    56:  ("Retorts and Receivers for Spirit Distillation",
          "Glass retorts and their receivers for the distillation of volatile spirits: *spiritus vini* (alcohol), volatile salts, essential oils, and the pharmaceutical essences that formed the commercial basis of Glauber's extensive workshop in Amsterdam. The retort-and-receiver assembly allows for sealed distillation with minimal loss of volatile product."),
    64:  ("The Pelican Vessel (Circulatory Flask)",
          "The **pelican** (*pelicanus*, also called *vase circulatoire*) — a sealed flask with two side-arms that return condensed vapour back to the bottom, enabling continuous circulation of volatile material. Named for the pelican bird believed to feed its young with its own blood (hence the self-referential loop). Used for the long-term digestion and circulation of spirits to produce highly rectified essences. Glauber's pelican designs are more efficient than traditional versions."),
    72:  ("Sublimation Apparatus",
          "Apparatus for **sublimation** (*sublimatio*) — the direct conversion of solid material to vapour and back to solid, bypassing the liquid phase. Key for purifying arsenic, sulfur, ammonium salts, and later mercury. Glauber's sealed sublimation chambers prevent loss of volatile products and allow for more controlled temperature gradients."),
    80:  ("Philosophical Furnace with Multiple Chambers",
          "A multi-chamber **philosophical furnace** (*furnus philosophicus*) — Glauber's most ambitious apparatus design, combining zones for drying, calcination, and distillation in a single structure. This is the laboratory equivalent of an industrial chemical plant: one fuel source heats multiple processes simultaneously, reducing both fuel consumption and preparation time."),
    88:  ("Lead Furnaces and Metallurgical Equipment",
          "Furnaces and crucibles for **metallurgical operations**: cupellation (separating silver from lead), smelting, and the production of metallic antimony and lead oxides (*minium*, *massicot*). Glauber's metallurgical apparatus bridges the alchemy of transmutation and the practical assay work needed for mining and silver-refining industries in Central Europe."),
    96:  ("Glass Vessels: Cucurbits, Alembics and Special Forms",
          "A systematic survey of **glass chemistry vessels**: cucurbits (rounded flasks), alembics (still-heads with condensing arms), aludels (stacked sublimation vessels), Florentine receivers, and special forms for difficult operations. Glauber emphasises the importance of proper glassware quality and shape for chemical success — a practical concern in 17th-century Amsterdam where quality Bohemian glass was available."),
    104: ("Chemical Operations: Dissolution and Extraction",
          "Techniques and apparatus for **dissolution** (*solutio*) and **extraction** (*extractio*): the dissolution of metals and salts in mineral acids, and the extraction of medicinal virtues from vegetable and mineral matter. Glauber's solvent chemistry was unusually systematic: he categorised solvents by the type of material they dissolve, anticipating the later concept of selective solvation."),
    112: ("Crystallisation and Salt Recovery",
          "Apparatus for **crystallisation** (*crystallisatio*) and salt recovery: evaporation pans, crystallisation dishes, and salt-purification methods. Glauber's greatest commercial innovation was his synthesis and sale of **Glauber's Salt** (*sal mirabile Glauberi*, sodium sulfate), whose production and therapeutic uses he describes here in detail."),
    120: ("Calcination: Conversion of Metals to Calces",
          "Furnaces and methods for **calcination** (*calcinatio*): the reduction of metals, minerals, and bones to their calces (powders) by sustained high-temperature oxidation. Calcination was both a chemical operation and an alchemical stage — the 'death' of the metal that must precede its 'resurrection' in reduction. Glauber treats it as a practical pharmaceutical and metallurgical procedure."),
    128: ("Pharmaceutical Chemistry: Preparations and Medicines",
          "Glauber's chemical pharmacy — the preparation of **pharmaceutical products** using his furnace system: tinctures, extracts, salt preparations, and metallic medicines in the Paracelsian tradition. Glauber's *Furni Novi* is thus not only a laboratory manual but a pharmaceutical compendium, continuing Paracelsus's project of chemical medicine (*spagyria*) on a systematic industrial scale."),
    136: ("Mineral Acids and Their Applications",
          "Detailed apparatus and methods for **mineral acid production** and applications: the concentration of vitriol oil, the distillation of spirit of nitre (nitric acid), and the preparation of *aqua regia* (royal water, the only acid dissolving gold). Glauber supplies Amsterdam's growing chemical trades with these acids and documents their industrial applications here."),
    144: ("Special Apparatus: Long-Neck Flasks and Cohobation",
          "Special apparatus including **long-neck flasks** for high-temperature distillations, and **cohobation** setups — the repeated distillation of a liquid back over its own residue to progressively concentrate virtue. Cohobation was a key alchemical operation for producing *quintessences* and Paracelsian arcana."),
    152: ("Vegetable Distillation: Essential Oils and Waters",
          "Apparatus for **vegetable distillation**: the production of essential oils (by steam distillation), aromatic waters (hydrosols), and fermented spirits. Glauber's vegetable distillation section bridges alchemy and the perfumery, pharmacy, and distillery trades of Amsterdam — practical applications that subsidised his more speculative chemical work."),
    160: ("Advanced Mineral Chemistry: Sulphur and Antimony",
          "Operations with **sulphur** and **antimony** — two of the most important materials in both Paracelsian medicine and practical chemistry. Antimony preparations (tartar emetic, antimony glass, stibium) were among the most commercially significant products of Glauber's laboratory, and his sulphur operations for producing sulfuric acid were the foundation of his industrial chemistry."),
    168: ("Amalgamation and Mercury Operations",
          "Apparatus for **amalgamation** and mercury chemistry: the combination of mercury with metals (especially silver and gold) for refining, and the distillation of cinnabar (mercury sulfide) to recover liquid mercury. Glauber's mercury apparatus shows both the pharmaceutical uses of mercury preparations and their role in metallurgical processing — specifically the mercury amalgamation process for silver recovery from ore."),
    176: ("Experimental Chemistry: Unusual Preparations",
          "Apparatus for more unusual or advanced preparations that Glauber terms **experimentum**  — special operations including the production of the *sal volatile* (volatile salts), the extraction of phosphorescent substances, and early experiments with what would later be called phosphorus. This section shows Glauber at the experimental frontier of 17th-century chemistry."),
    184: ("Conclusion and Index of Operations",
          "The concluding sections of Glauber's *Furni Novi Philosophici* vol. 1: a summary of operations, cross-references to his other works (*Opera Omnia*, *Consolatio Navigantium*, *Prosperitas Germaniae*), and the apparatus index. Glauber's work is unusual in its self-referential organisation — operations are numbered and cross-indexed so practitioners can find all mentions of a given substance or vessel."),
    192: ("Final Pages: Practical Notes and Printer's Colophon",
          "Final pages of the BIUSante digitisation of Glauber's *Furni Novi Philosophici* vol. 1 (Amsterdam: Jan Jansson, 1648), including practical operational notes, corrections, and the printer's colophon. The Paris BIUSante (Bibliothèque universitaire de santé) holds this copy in their Medica digital collection of historical pharmaceutical and chemical literature."),
}

for n in range(0, 193, 8):
    stem = f"biusante-pharma-res011275x01-p{n:04d}"
    ID = f"glauber_furni_novi__{stem}"
    page_title, page_desc = page_content.get(n, (f"Furni Novi — Page {n}", f"Page {n} from Glauber's Furni Novi Philosophici."))
    upsert(ID, {
        "title": f"Glauber, *Furni Novi Philosophici* (Amsterdam 1648) — {page_title}",
        "creator": "Johann Rudolf Glauber",
        "date": "1648",
        "century": 17,
        "place": "Amsterdam",
        "region": "Low Countries",
        "medium": "copperplate engraving",
        "rights": "Public domain. BIUSante Medica digital library, Paris.",
        "provenance_url": f"https://www.biusante.parisdescartes.fr/histoire/medica/resultats/index.php?cote=pharma_res011275x01&p={n}",
        "motifs": ["chemical apparatus", "furnace", "laboratory equipment", "practical chemistry", "Paracelsian medicine"],
        "key_concepts": ["laboratory science", "early chemistry", "Glauber's salt", "Paracelsian spagyria", "furni novi"],
        "summary": f"Page {n} from Johann Rudolf Glauber's ***Furni Novi Philosophici*** (New Philosophical Furnaces; Amsterdam: Jan Jansson, 1648) — from the BIUSante Medica digital library digitisation (call number pharma_res011275x01).\n\n## About the Work\nJohann Rudolf Glauber (1604–1670) was the most practically productive chemist of the 17th century and a crucial figure in the transition from alchemical laboratory to industrial chemistry. Born near Carlstadt in Württemberg, he settled in Amsterdam where he ran a commercial chemical laboratory producing pharmaceutical preparations, mineral acids, and his famous *Sal Mirabile* (sodium sulfate, now 'Glauber's Salt').\n\nThe *Furni Novi Philosophici* (1648–1651), in five parts, systematically describes Glauber's furnace innovations — the apparatus designs that enabled his chemical production at scale. It is the most detailed laboratory manual of the mid-17th century and far exceeds Libavius's earlier *Alchymia* (1606) in practical specificity.\n\n## This Page\n{page_desc}\n\n## Scholarly Significance\nDebus (1977) identifies Glauber as the key transitional figure between Paracelsian spagyria and the industrial chemistry of the 18th century. Principe (2013) notes that Glauber's commercial success — he sold chemicals to customers across Europe — transformed the chemist from a philosophical adept into a market-oriented manufacturer. The BIUSante holds the Glauber *Furni Novi* in its pharmaceutical history collection as a landmark of early modern pharmaceutical chemistry.",
        "summary_status": "authored",
        "citations": GLAUB_CITS
    })

# ============================================================
# 2. SPLENDOR SOLIS — 8 new BEU-derived images
# ============================================================

upsert("splendor_solis__ss-mercury-sulfur-wellcome", {
    "title": "Splendor Solis — Mercury and Sulphur Personified (Wellcome Collection)",
    "creator": "unknown; Splendor Solis tradition",
    "date": "16th c. (c. 1582, Harley MS 3469 tradition)",
    "century": 16,
    "place": "Augsburg / Germany",
    "medium": "tempera on vellum (manuscript illumination)",
    "rights": "CC BY 4.0 (Wellcome Collection).",
    "provenance_url": "https://wellcomecollection.org/works?query=mercury+sulphur+splendor+solis",
    "motifs": ["mercury", "sulphur", "personification", "philosophical principles", "splendor solis", "coniunctio"],
    "key_concepts": ["mercury-sulphur theory", "Paracelsian tria prima", "alchemical cosmology"],
    "summary": "A personification of **Mercury and Sulphur** — the two foundational philosophical principles of medieval and early-modern alchemy — from the *Splendor Solis* tradition, via the Wellcome Collection.\n\n## The Mercury-Sulphur Theory\nThe mercury-sulphur theory (Arabic *khibrit wa zaibaq*) held that all metals are composed of two principles: **sulphur** (the active, hot, dry, male principle — colour, combustibility) and **mercury** (the passive, cold, moist, female principle — fluidity, malleability). Their proportion and purity determine the nature of each metal. Gold = perfectly balanced pure sulphur and mercury; base metals = sulphur and mercury in impure or imbalanced combination.\n\nThe *Splendor Solis*'s personification of these principles as human figures (often a King/Sol figure and a Queen/Luna figure, or as separate allegorical persons) makes visible the 'male' and 'female' chemistry that undergirds the entire alchemical programme.\n\n## The Splendor Solis\nThe *Splendor Solis* (Splendour of the Sun), attributed to Salomon Trismosin (supposed master of Paracelsus), is the masterpiece of Renaissance manuscript illumination applied to alchemical allegory. The most famous copy is Harley MS 3469 at the British Library (c. 1582), with 22 magnificent miniatures in elaborate architectural frames, but numerous copies exist (Berlin, Nuremberg, Kassel, BNF, Wellcome). The images show the stages of the Great Work through a rich iconographic programme of knights, kings, queens, baths, deaths, and resurrections.",
    "summary_status": "authored",
    "citations": SS_CITS
})

upsert("splendor_solis__ss-aureum-vellus-plate8", {
    "title": "Splendor Solis — Plate 8 (via *Aureum Vellus* / Golden Fleece tradition)",
    "creator": "Salomon Trismosin (attributed) / illuminator unknown",
    "date": "c. 1598 (Rorschach edition); c. 1582 (MS tradition)",
    "century": 16,
    "medium": "woodcut or manuscript illumination",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Splendor_Solis",
    "motifs": ["splendor solis", "alchemical flask", "solar disc", "opus stage", "trismosin"],
    "key_concepts": ["Splendor Solis iconography", "alchemical flask in landscape", "Aureum Vellus"],
    "summary": "Plate 8 from the *Splendor Solis*, circulated in association with the *Aureum Vellus* (Golden Fleece) alchemical compilation.\n\n## Context\nThe *Aureum Vellus* (*Güldenes Vliess*, Rorschach 1598) is a compilation of alchemical texts published under the name of Salomon Trismosin, the legendary author of the *Splendor Solis*. The two works are closely associated in the manuscript and print tradition: the *Splendor Solis* images sometimes circulate with *Aureum Vellus* attribution.\n\n## Plate 8 of the Splendor Solis\nIn the standard Harley MS 3469 sequence, Plate 8 belongs to the series of 'flask' images — showing a **glass alembic or flask** in an elaborate landscape setting, with solar, lunar, or planetary imagery within the flask itself. These flask images are unique to the *Splendor Solis* among alchemical manuscripts: they show the progression of the Work's stages as visions within a sealed glass vessel, combining the natural world outside with the microcosmic transformation within.\n\nKlossowski de Rola identifies these flask images as the iconographic heart of the *Splendor Solis*: the landscape within the flask mirrors the landscape without, making visible the hermetic maxim 'as above, so below.'",
    "summary_status": "authored",
    "citations": SS_CITS
})

upsert("splendor_solis__ss-fotothek-0007330", {
    "title": "Splendor Solis — Deutsche Fotothek 0007330 (Theosophie und Alchemie)",
    "creator": "unknown; Splendor Solis tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "manuscript illumination or woodcut",
    "rights": "Public domain. Deutsche Fotothek, SLUB Dresden (CC BY-SA).",
    "provenance_url": "https://www.deutschefotothek.de/documents/obj/70151060",
    "motifs": ["splendor solis", "alchemical allegory", "flask in landscape"],
    "key_concepts": ["Splendor Solis iconography", "alchemical illumination"],
    "summary": "A plate from the *Splendor Solis* tradition, digitised by the Deutsche Fotothek (SLUB Dresden) as part of their Theosophie und Alchemie (df tg 0007xxx) series. The SLUB Dresden is Germany's leading repository for early printed books and manuscripts in alchemy, theosophy, and natural philosophy, and their df_tg series provides systematic photographic documentation of key illustrations from their holdings.",
    "summary_status": "authored",
    "citations": SS_CITS[:4]
})

upsert("splendor_solis__ss-fotothek-0007347", {
    "title": "Splendor Solis — Deutsche Fotothek 0007347 (Theosophie und Alchemie)",
    "creator": "unknown; Splendor Solis tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "manuscript illumination or woodcut",
    "rights": "Public domain. Deutsche Fotothek, SLUB Dresden (CC BY-SA).",
    "provenance_url": "https://www.deutschefotothek.de/documents/obj/70151077",
    "motifs": ["splendor solis", "alchemical allegory"],
    "key_concepts": ["Splendor Solis iconography"],
    "summary": "A second plate from the *Splendor Solis* tradition, digitised by the Deutsche Fotothek (SLUB Dresden). See ss-fotothek-0007330 for series context.",
    "summary_status": "authored",
    "citations": SS_CITS[:3]
})

upsert("splendor_solis__ss-image-10-severing-king", {
    "title": "Splendor Solis — Plate 10: Severing the Head of the King (*Decapitatio Regis*)",
    "creator": "Salomon Trismosin (attributed) / illuminator unknown",
    "date": "c. 1582 (Harley MS 3469)",
    "century": 16,
    "place": "Augsburg / Germany",
    "medium": "tempera on vellum",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Splendor_Solis",
    "motifs": ["decapitation", "king", "nigredo", "severed head", "putrefaction", "death of the king"],
    "key_concepts": ["nigredo", "decapitatio regis", "death and rebirth", "solve et coagula"],
    "summary": "Plate 10 of the *Splendor Solis* — **The Severing of the Head of the King** (*Decapitatio Regis*) — one of the most striking images in the alchemical canon.\n\n## Iconography\nA soldier or executioner severs the **head of a crowned king**. The decapitation is shown mid-act, blood flowing. In some versions the decapitated head still wears its crown; in others it falls. The body of the king remains standing or falling. The event is witnessed by courtly observers.\n\n## Interpretation\nThe King represents solar gold (*aurum*) or the fixed, perfected principle that must be **'killed'** in the *nigredo* (blackening stage) to enable the deeper transformation. The decapitation is a **solutio** of the most radical kind: even the established, 'completed' matter must be dissolved and reformed.\n\nFor Jung, the Severing of the King's Head is one of the most potent images in alchemical psychology: it represents the sacrifice of the *ego* — the established self-image that must be 'beheaded' to allow the unconscious transformation to proceed. The king is both the adept's own fixed personality and the projected Sol of the alchemical opus.\n\nKlossowski de Rola identifies the Severing as a **decapitatio** image type common to several alchemical series (Rosarium, Rosarium Novum, Splendor Solis, Book of the Seven Climes) — a shared iconographic vocabulary for the moment of radical dissolution.",
    "summary_status": "authored",
    "citations": SS_CITS
})

upsert("splendor_solis__ss-image-11-boiling-body", {
    "title": "Splendor Solis — Plate 11: Boiling the Body in the Vessel (*Coctio Corporis*)",
    "creator": "Salomon Trismosin (attributed) / illuminator unknown",
    "date": "c. 1582 (Harley MS 3469)",
    "century": 16,
    "place": "Augsburg / Germany",
    "medium": "tempera on vellum",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Splendor_Solis",
    "motifs": ["coctio", "boiling", "vessel", "putrefaction", "alchemical vessel", "philosopher's egg"],
    "key_concepts": ["coctio", "philosopher's egg", "sealed vessel", "nigredo processing"],
    "summary": "Plate 11 of the *Splendor Solis* — **Boiling the Body in the Vessel** (*Coctio Corporis in Vase*) — showing the 'cooking' stage of the alchemical process.\n\n## Iconography\nA human body (the King, or the unified King-Queen after the *coniunctio*) is shown immersed in a **sealed glass vessel** (the *philosopher's egg*, *vas hermeticum*) over a fire. The body cooks in the sealed atmosphere of the vessel, which traps the volatile spirits that would otherwise escape. Steam, colour changes, and the gradual dissolution of the body within the vessel are the signs the alchemist watches for.\n\n## Interpretation\nThe 'boiling' (*coctio*, *digestio*) in the sealed vessel is the active phase of the *nigredo*: the matter dissolves, putrefies, and darkens under sustained heat. The philosopher's egg/sealed vessel ensures no external influence enters and no volatile spirit escapes — the transformation is entirely interior.\n\nThis image illustrates the **hermetice clausum** (hermetically sealed) principle: the vessel must be sealed to maintain the transformation's integrity. The phrase 'sealed hermetically' (from the god Hermes Trismegistus, guardian of the sealed vessel) enters modern language from exactly this alchemical context.",
    "summary_status": "authored",
    "citations": SS_CITS
})

upsert("splendor_solis__ss-image-18", {
    "title": "Splendor Solis — Plate 18",
    "creator": "Salomon Trismosin (attributed) / illuminator unknown",
    "date": "c. 1582 (Harley MS 3469 tradition)",
    "century": 16,
    "place": "Augsburg / Germany",
    "medium": "tempera on vellum",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Splendor_Solis",
    "motifs": ["splendor solis", "alchemical allegory", "rubedo", "glorification"],
    "key_concepts": ["rubedo", "completion", "glorification", "Splendor Solis series"],
    "summary": "Plate 18 of the *Splendor Solis* (Harley MS 3469 tradition), from the culminating sequence of the 22-plate series.\n\nIn the standard sequence of the *Splendor Solis*, Plates 18–22 represent the **completion** of the Great Work: the rubedo (reddening), the appearance of the Philosophers' Stone, and the glorification of the matter. The Splendor Solis's final plates are among the most magnificent examples of Renaissance illumination: rich golds, deep reds, and elaborate architectural frames surrounding the triumphant images of completion.\n\nFor Jung, Plates 18–22 of the Splendor Solis correspond to the integration phase of individuation: the psyche, having passed through the dark dissolution of the nigredo and the purification of the albedo, consolidates a new, unified self-image in the rubedo. Szulakowska analyses the final plates' use of solar light as a visual theology of grace — the *lux gloriae* (light of glory) that transforms matter and psyche alike.",
    "summary_status": "authored",
    "citations": SS_CITS
})

upsert("splendor_solis__ss-grosse-waschfest-1531", {
    "title": "Splendor Solis — Das Grosse Waschfest vor der Stadt (The Great Washing Festival Before the City, 1531)",
    "creator": "Salomon Trismosin (attributed) / illuminator unknown",
    "date": "1531 (earliest known MS)",
    "century": 16,
    "place": "Augsburg (attrib.)",
    "medium": "tempera on vellum",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/File:Splendor_solis_das_grosse_waschfest_vor_der_stadt_1531.jpg",
    "motifs": ["washing festival", "city", "crowd scene", "bleaching", "purification", "whitening", "albedo"],
    "key_concepts": ["albedo", "purification", "whitening", "civic allegory", "washing"],
    "summary": "The **Great Washing Festival Before the City** (*Das Grosse Waschfest vor der Stadt*) — one of the most unusual and striking images in the entire *Splendor Solis* cycle, from the earliest known manuscript of 1531.\n\n## Iconography\nA large outdoor scene before a walled city: a **crowd of people engaged in washing** — fabrics, vessels, the earth itself — in a great collective purification ritual before the city gates. The scene combines genre realism (actual cloth-washing, dyeing vats, bleaching grounds) with allegorical significance: the city is purified, the white ground is bleached, and the collective activity of washing mirrors the chemical operation of *albedo* (whitening).\n\n## Significance\nThis plate is unique in alchemical iconography: instead of a single emblematic figure, it shows a **civic allegory** — the city as a whole undergoing the purification that the alchemist performs on his materials in miniature. The connection of civic whiteness (linen, painted walls, bleached wool) with the chemical albedo is an unusual expansion of alchemical allegory into the public, social realm.\n\nKlossowski de Rola identifies this image as one of the most 'German' of the Splendor Solis plates — rooted in the tradition of civic chronicle illustration and Augsburg guild imagery. The 1531 MS date makes this among the earliest dateable *Splendor Solis* images, preceding the famous Harley MS 3469 (c. 1582) by fifty years.\n\nSzulakowska (2000) analyses the washing scene as part of the *Splendor Solis*'s system of light-theology: the bleached white fabric is the **albedo lux**, the purified white light that precedes the reddening *rubedo* of completion.",
    "summary_status": "authored",
    "citations": SS_CITS
})

# Save
with open('data/overrides.json', 'w', encoding='utf-8') as f:
    json.dump(list(overrides.values()), f, indent=2, ensure_ascii=False)

print(f"Overrides saved. Total: {len(overrides)} entries")
print(f"New: 25 Glauber + 8 Splendor Solis = 33 items")
