# -*- coding: utf-8 -*-
"""
OCCULTIMGDB source registry.

Each entry describes one source work whose page/illustration images already live under
C:\\Dev\\EmblemPrintShop\\sources\\<dir>\\images. build_catalog.py reads this registry,
scans the image dir, and emits one catalog record per image.

tier:
  "illustration" -> the images ARE illustrations (emblem plates, woodcuts, engraved plates).
                    Included in the default build; shown in the main gallery.
  "page_scan"    -> raw book-page scans that mix illustrations with text/blank pages.
                    Included only with --all; flagged in the UI as "unfiltered pages" for curation.

Scholarly metadata here is intentionally conservative and web-verifiable. Per-IMAGE scholarly
prose (the 5k-word summaries) lives in data/overrides.json, keyed by catalog id, and is merged
over the generated record.
"""

import os as _os
EMBLEM_ROOT = r"C:\Dev\EmblemPrintShop\sources"
# Second image root: curated, by-text alchemical illustration scans.
ALCHEMY_BEU_ROOT = r"C:\Dev\AlchemyBeatEmUp\staging\raw_images"
# Third root: images sourced from the web into this project (public-domain only).
_PROJECT_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
LOCAL_SOURCED_ROOT = _os.path.join(_PROJECT_ROOT, "sources_web")
# A source sets "root": "BEU" | "LOCAL"; default is EMBLEM_ROOT.

# era: antiquity | medieval | renaissance | early_modern | modern
# tradition: alchemy | hermetic | rosicrucian | kabbalah | goetia_grimoire | astrology | theosophy | reception

SOURCES = [
    {
        "key": "atalanta_fugiens",
        "short_id": "AF",
        "title": "Atalanta Fugiens",
        "creator": "Michael Maier",
        "date": "1618",
        "century": 17,
        "place": "Oppenheim",
        "region": "German lands (HRE)",
        "language": "Latin",
        "era": "early_modern",
        "tradition": "alchemy",
        "tier": "illustration",
        "image_dir": r"claudiens\site\images\emblems",
        "provenance_url": "https://furnaceandfugue.org/atalanta-fugiens/",
        "rights": "Public domain. Images via furnaceandfugue.org / Science History Institute.",
        "motifs": ["emblem", "engraving", "alchemical opus", "atalanta", "fugue"],
        "blurb": "Maier's polymodal emblem book: 50 emblems plus a frontispiece, each fusing an "
                 "engraved plate, a Latin epigram, and a polyphonic fugue. The sequence encodes the "
                 "alchemical Great Work from prima materia to the Philosophers' Stone.",
    },
    {
        "key": "hypnerotomachia",
        "short_id": "HP",
        "title": "Hypnerotomachia Poliphili",
        "creator": "Francesco Colonna (attrib.)",
        "date": "1499",
        "century": 15,
        "place": "Venice",
        "region": "Republic of Venice",
        "language": "Vernacular Italian / Latin / Greek",
        "era": "renaissance",
        "tradition": "reception",
        "tier": "illustration",
        "image_dir": r"hypnerotomachia-polyphili\site\images\woodcuts_1499",
        "provenance_url": "https://archive.org/details/hypnerotomachiap00colo",
        "rights": "Public domain. 1499 Aldine edition via Internet Archive.",
        "motifs": ["woodcut", "incunabulum", "neoplatonic", "architecture", "triumph", "nymph"],
        "blurb": "The Aldine first edition — among the most lavishly illustrated incunabula, with "
                 "~172 woodcuts. Included as alchemical-reception context: its Hermetic, Neoplatonic, "
                 "and architectural imagery overlaps heavily with the emblem tradition.",
    },
    {
        "key": "rosarium",
        "short_id": "ROS",
        "title": "Rosarium Philosophorum",
        "creator": "Anonymous (pub. Cyriacus Jacobus)",
        "date": "1550",
        "century": 16,
        "place": "Frankfurt",
        "region": "German lands (HRE)",
        "language": "Latin",
        "era": "renaissance",
        "tradition": "alchemy",
        "tier": "illustration",
        "image_dir": r"rosarium\images",
        "provenance_url": "https://archive.org/details/rosarium-philosophorum-the-rosary-of-the-philosophers",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["woodcut", "coniunctio", "king and queen", "hermaphrodite", "stages of the work"],
        "blurb": "The most influential illustrated alchemical sequence of the Renaissance: ~20 woodcuts "
                 "tracing the chymical wedding of Sol and Luna through death, putrefaction, and rebirth. "
                 "Famously analysed by C. G. Jung in 'The Psychology of the Transference'.",
    },
    {
        "key": "splendor_solis",
        "short_id": "SS",
        "title": "Splendor Solis",
        "creator": "attrib. Salomon Trismosin",
        "date": "1532–1535 (MS); printed later",
        "century": 16,
        "place": "Germany",
        "region": "German lands (HRE)",
        "language": "German",
        "era": "renaissance",
        "tradition": "alchemy",
        "tier": "illustration",
        "image_dir": r"splendor_solis\images",
        "provenance_url": "https://archive.org/details/splendor-solis",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["illuminated manuscript", "flasks", "the work", "knight", "philosophers"],
        "blurb": "A sumptuously illuminated alchemical treatise of 22 allegorical plates set in painted "
                 "architectural borders — among the most beautiful of all alchemical manuscripts, "
                 "surviving in several richly coloured copies.",
    },
    {
        "key": "stolcius",
        "short_id": "VC",
        "title": "Viridarium Chymicum",
        "creator": "Daniel Stolcius",
        "date": "1624",
        "century": 17,
        "place": "Frankfurt",
        "region": "German lands (HRE)",
        "language": "Latin",
        "era": "early_modern",
        "tradition": "alchemy",
        "tier": "illustration",
        "image_dir": r"stolcius\images",
        "provenance_url": "https://archive.org/details/viridariumchymic00stol",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["engraving", "emblem anthology", "furnace", "apparatus", "philosophers"],
        "blurb": "Stolcius's 'Chymical Garden' — an anthology of 107 engraved emblems gathered from "
                 "Maier, Mylius, and other masters, each with an epigram. A visual encyclopaedia of the "
                 "alchemical emblem tradition.",
    },
    {
        "key": "mylius_plates",
        "short_id": "PR",
        "title": "Philosophia Reformata",
        "creator": "Johann Daniel Mylius",
        "date": "1622",
        "century": 17,
        "place": "Frankfurt",
        "region": "German lands (HRE)",
        "language": "Latin",
        "era": "early_modern",
        "tradition": "alchemy",
        "tier": "illustration",
        "image_dir": r"mylius_philosophia\plates",
        "provenance_url": "https://archive.org/details/philosophiarefor00myli",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["engraving", "emblem series", "twelve keys", "stages of the work"],
        "blurb": "Mylius's compendium, whose celebrated engraved emblem series (executed by Balthasar "
                 "Schwan) illustrates the stages of the opus; widely copied by later emblem-makers.",
    },
    {
        "key": "khunrath",
        "short_id": "AMP",
        "title": "Amphitheatrum Sapientiae Aeternae",
        "creator": "Heinrich Khunrath",
        "date": "1595 / 1609",
        "century": 16,
        "place": "Hamburg / Hanau",
        "region": "German lands (HRE)",
        "language": "Latin",
        "era": "renaissance",
        "tradition": "hermetic",
        "tier": "illustration",
        "image_dir": r"khunrath\images",
        "provenance_url": "https://archive.org/details/amphitheatrumsap00khun",
        "rights": "Public domain. BIU Santé / Internet Archive scan.",
        "motifs": ["circular engraving", "oratory and laboratory", "kabbalah", "christian theosophy"],
        "blurb": "Khunrath's 'Amphitheatre of Eternal Wisdom' — a Christian-theosophical-alchemical "
                 "work famous for its great circular engravings, including the 'Oratory-Laboratory' plate "
                 "fusing prayer and chemistry.",
    },
    {
        "key": "cramer",
        "short_id": "ES",
        "title": "Emblemata Sacra",
        "creator": "Daniel Cramer",
        "date": "1624",
        "century": 17,
        "place": "Frankfurt",
        "region": "German lands (HRE)",
        "language": "Latin / German",
        "era": "early_modern",
        "tradition": "rosicrucian",
        "tier": "illustration",
        "image_dir": r"cramer\images",
        "provenance_url": "https://archive.org/details/emblematasacraho00cram",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["emblem", "flaming heart", "rosicrucian", "devotional"],
        "blurb": "Cramer's devotional 'Sacred Emblems' — 50 flaming-heart emblems with strong "
                 "Rosicrucian resonance, widely reused in 17th-century esoteric print culture.",
    },
    {
        "key": "maier_arcana",
        "short_id": "AA",
        "title": "Arcana Arcanissima",
        "creator": "Michael Maier",
        "date": "1614",
        "century": 17,
        "place": "London",
        "region": "England",
        "language": "Latin",
        "era": "early_modern",
        "tradition": "hermetic",
        "tier": "page_scan",
        "image_dir": r"maier_arcana\images",
        "provenance_url": "https://archive.org/details/arcanaarcanissim00maie",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["mythology as alchemy", "egyptian", "hieroglyph"],
        "blurb": "Maier's reading of classical and Egyptian myth as veiled chymistry — a key text of "
                 "the 'mytho-alchemical' method.",
    },
    {
        "key": "maier_viatorium",
        "short_id": "VIA",
        "title": "Viatorium",
        "creator": "Michael Maier",
        "date": "1618",
        "century": 17,
        "place": "Oppenheim",
        "region": "German lands (HRE)",
        "language": "Latin",
        "era": "early_modern",
        "tradition": "alchemy",
        "tier": "page_scan",
        "image_dir": r"maier_viatorium\images",
        "provenance_url": "https://archive.org/details/viatorium",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["seven planets", "journey", "engraving"],
        "blurb": "Maier's 'Wayfarer' — a planetary-alchemical journey through the seven metals.",
    },
    {
        "key": "fludd",
        "short_id": "FL",
        "title": "Mosaicall Philosophy / Utriusque Cosmi",
        "creator": "Robert Fludd",
        "date": "1617–1659",
        "century": 17,
        "place": "Oppenheim / London",
        "region": "England / HRE",
        "language": "Latin / English",
        "era": "early_modern",
        "tradition": "hermetic",
        "tier": "page_scan",
        "image_dir": r"fludd\images",
        "provenance_url": "https://archive.org/details/mosaicallphiloso00flud",
        "rights": "Public domain. BnF / Internet Archive scan.",
        "motifs": ["cosmic diagram", "monochord", "macrocosm-microcosm", "rosicrucian"],
        "blurb": "Fludd's vast Hermetic cosmology, source of the iconic macrocosm-microcosm and divine-"
                 "monochord diagrams.",
    },
    {
        "key": "hall_manuscripts",
        "short_id": "HALL",
        "title": "Hall Collection Manuscripts",
        "creator": "various (Manly P. Hall collection)",
        "date": "various",
        "century": None,
        "place": "various",
        "region": "various",
        "language": "various",
        "era": "early_modern",
        "tradition": "hermetic",
        "tier": "page_scan",
        "image_dir": r"hall_manuscripts\images",
        "provenance_url": "https://archive.org/details/manlypalmerhall",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["grimoire", "diagram", "manuscript"],
        "blurb": "Scans from the Manly Palmer Hall collection of esoteric manuscripts and diagrams.",
    },
    {
        "key": "paul_marshall",
        "short_id": "DEE",
        "title": "Dee / Elizabethan Occult (Marshall coll.)",
        "creator": "various (incl. John Dee)",
        "date": "16th–17th c.",
        "century": 16,
        "place": "England",
        "region": "England",
        "language": "Latin / English",
        "era": "renaissance",
        "tradition": "hermetic",
        "tier": "page_scan",
        "image_dir": r"paul_marshall\images",
        "provenance_url": "[PLACEHOLDER: provenance URL needed]",
        "rights": "Public domain (verify per item).",
        "motifs": ["monas hieroglyphica", "enochian", "angelic", "sigil"],
        "blurb": "Elizabethan occult material including John Dee's Monas Hieroglyphica and Enochian "
                 "diagrams. [PLACEHOLDER: verify exact sources & rights per image].",
    },
    {
        "key": "obrist_medieval",
        "short_id": "MED",
        "title": "Medieval Alchemical Illustration (Obrist coll.)",
        "creator": "various (medieval manuscripts)",
        "date": "13th–15th c.",
        "century": 14,
        "place": "various (Latin West)",
        "region": "Latin West",
        "language": "Latin",
        "era": "medieval",
        "tradition": "alchemy",
        "tier": "page_scan",
        "image_dir": r"obrist_medieval\images",
        "provenance_url": "[PLACEHOLDER: provenance URL needed]",
        "rights": "Public domain (verify per item).",
        "motifs": ["ouroboros", "manuscript diagram", "aurora consurgens", "ramon llull"],
        "blurb": "Medieval alchemical manuscript illustrations — the earliest strata of the visual "
                 "tradition (e.g. Aurora Consurgens). [PLACEHOLDER: verify exact sources & rights].",
    },
    {
        "key": "mclean_second",
        "short_id": "MCL",
        "title": "Alchemical Imagery (McLean coll.)",
        "creator": "various",
        "date": "various",
        "century": None,
        "place": "various",
        "region": "various",
        "language": "various",
        "era": "early_modern",
        "tradition": "alchemy",
        "tier": "page_scan",
        "image_dir": r"mclean_second\images",
        "provenance_url": "https://www.alchemywebsite.com/",
        "rights": "[PLACEHOLDER: verify rights per item].",
        "motifs": ["emblem", "diagram", "miscellany"],
        "blurb": "A miscellany of alchemical imagery. [PLACEHOLDER: verify exact sources & rights].",
    },

    # ---- Web-sourced ANTIQUITY stratum (root = LOCAL): public-domain images downloaded into the repo.
    {
        "key": "antiquity_ouroboros", "short_id": "OUR", "title": "The Ouroboros — Earliest Witnesses",
        "creator": "various (Hellenistic–Byzantine)", "date": "1st c. CE – 1478 (copies)", "century": 1,
        "place": "Egypt / Byzantium", "region": "Eastern Mediterranean", "language": "Greek",
        "era": "antiquity", "tradition": "alchemy", "tier": "illustration", "root": "LOCAL",
        "image_dir": "antiquity",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Chrysopoeia_of_Cleopatra",
        "rights": "Public domain (PD Mark 1.0). Via Wikimedia Commons.",
        "motifs": ["ouroboros", "serpent", "dragon", "hen to pan", "unity", "antiquity"],
        "blurb": "The deepest stratum of the tradition — the self-devouring serpent, the oldest "
                 "alchemical sign, in its earliest surviving witnesses (the Chrysopoeia of Kleopatra and "
                 "the Byzantine copies that transmit it).",
    },
    {
        "key": "antiquity_apparatus", "short_id": "ZOS", "title": "Greek Alchemy — Apparatus & Diagrams",
        "creator": "Zosimos of Panopolis / Maria the Jewess (tradition)", "date": "3rd–4th c. CE (copies later)",
        "century": 3, "place": "Hellenistic Egypt / Byzantium", "region": "Eastern Mediterranean",
        "language": "Greek", "era": "antiquity", "tradition": "alchemy", "tier": "illustration", "root": "LOCAL",
        "image_dir": "apparatus",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Alchemical_apparatus",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["apparatus", "distillation", "alembic", "tribikos", "kerotakis", "furnace", "antiquity"],
        "blurb": "The instruments of the first alchemists — the stills, alembics, and furnaces described by "
                 "Zosimos of Panopolis and credited in part to Maria the Jewess, preserved through "
                 "Byzantine manuscript copies.",
    },
    {
        "key": "cosmology", "short_id": "COS", "title": "Cosmological Diagrams",
        "creator": "various (Fludd & others)", "date": "17th c.", "century": 17,
        "place": "Oppenheim / London", "region": "England / HRE", "language": "Latin",
        "era": "early_modern", "tradition": "hermetic", "tier": "illustration", "root": "LOCAL",
        "image_dir": "cosmology",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Robert_Fludd",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["cosmic diagram", "great chain of being", "macrocosm", "microcosm", "nature", "hermetic"],
        "blurb": "The great hermetic cosmological engravings — the chains, spheres, and monochords that "
                 "picture the whole structure of the cosmos as 'above, so below'.",
    },
    {
        "key": "figures", "short_id": "FIG", "title": "Portraits of the Adepts",
        "creator": "various", "date": "16th–17th c.", "century": 16,
        "place": "Europe", "region": "Europe", "language": "—",
        "era": "renaissance", "tradition": "hermetic", "tier": "illustration", "root": "LOCAL",
        "image_dir": "figures",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Occultists",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["portrait", "figure", "adept", "magus"],
        "blurb": "Faces of the tradition — portraits of the philosophers, magi, and adepts whose names "
                 "run through the works in this archive.",
    },
    {
        "key": "grimoire_plates", "short_id": "GRM", "title": "Grimoire & Goetia Plates",
        "creator": "various (Solomonic tradition)", "date": "17th c. (comp.); 1904 ed.", "century": 17,
        "place": "England", "region": "England", "language": "Latin / English",
        "era": "early_modern", "tradition": "goetia_grimoire", "tier": "illustration", "root": "LOCAL",
        "image_dir": "grimoire",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Key_of_Solomon",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["magic circle", "sigil", "solomon", "goetia", "ceremonial magic", "pentacle"],
        "blurb": "Plates from the ceremonial-magic tradition — protective circles, triangles of art, "
                 "and spirit seals from the Keys of Solomon.",
    },

    {
        "key": "tarot", "short_id": "TAR", "title": "Tarot — A Visual History",
        "creator": "various", "date": "15th c. – 1909", "century": 15,
        "place": "Italy / France / England", "region": "Europe", "language": "—",
        "era": "renaissance", "tradition": "divination", "tier": "illustration", "root": "LOCAL",
        "image_dir": "tarot",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Tarot",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["tarot", "trump", "divination", "cards", "allegory"],
        "blurb": "The trump cards of the tarot across five centuries — from the painted Visconti-Sforza "
                 "deck to the occult Rider-Waite-Smith — the visual backbone of Western cartomancy.",
    },
    {
        "key": "witchcraft", "short_id": "WCH", "title": "Witchcraft & the Sabbath",
        "creator": "various", "date": "16th–17th c.", "century": 16,
        "place": "German lands / Europe", "region": "Europe", "language": "—",
        "era": "renaissance", "tradition": "witchcraft", "tier": "illustration", "root": "LOCAL",
        "image_dir": "witchcraft",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Witchcraft_in_art",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["witch", "sabbath", "broom", "cauldron", "devil", "woodcut"],
        "blurb": "The early-modern image of the witch — Baldung Grien's sabbaths, the cauldron and the "
                 "night-flight — and its biblical antecedents.",
    },
    {
        "key": "kabbalah", "short_id": "KAB", "title": "Kabbalah — The Tree of Life",
        "creator": "various", "date": "16th–17th c.", "century": 16,
        "place": "Italy / German lands", "region": "Europe", "language": "Hebrew / Latin",
        "era": "renaissance", "tradition": "kabbalah", "tier": "illustration", "root": "LOCAL",
        "image_dir": "kabbalah",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Tree_of_life_(Kabbalah)",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["sephiroth", "tree of life", "divine names", "kabbalah", "diagram"],
        "blurb": "The Sephirotic Tree of Life and the divine-name diagrams of Jewish and Christian "
                 "Kabbalah — the architecture of the emanated cosmos.",
    },
    {
        "key": "astrology", "short_id": "AST", "title": "Astrology & the Stars",
        "creator": "various", "date": "15th–16th c.", "century": 15,
        "place": "German lands / Netherlands", "region": "Europe", "language": "—",
        "era": "renaissance", "tradition": "astrology", "tier": "illustration", "root": "LOCAL",
        "image_dir": "astrology",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Astrology",
        "rights": "Public domain. Via Wikimedia Commons / Rijksmuseum.",
        "motifs": ["zodiac", "planet", "saturn", "melancholy", "planetary children", "star"],
        "blurb": "The reading of celestial influence — the Children of the Planets, the Saturnine "
                 "melancholy of Dürer's masterpiece, and the geometry of the heavens.",
    },
    {
        "key": "enochian", "short_id": "ENO", "title": "John Dee & Enochian Magic",
        "creator": "John Dee", "date": "1564–1583", "century": 16,
        "place": "England", "region": "England", "language": "Latin / English",
        "era": "renaissance", "tradition": "hermetic", "tier": "illustration", "root": "LOCAL",
        "image_dir": "enochian",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:John_Dee",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["monas hieroglyphica", "sigil", "enochian", "angelic", "glyph"],
        "blurb": "The angelic and hieroglyphic magic of John Dee — the compressed cosmological glyph of "
                 "the Monas Hieroglyphica and the Enochian system.",
    },
    {
        "key": "rosicrucian_plates", "short_id": "GFR", "title": "Secret Symbols of the Rosicrucians",
        "creator": "anonymous (Altona, 1785–88)", "date": "1785", "century": 18,
        "place": "Altona", "region": "German lands", "language": "German",
        "era": "early_modern", "tradition": "rosicrucian", "tier": "illustration", "root": "LOCAL",
        "image_dir": "rosicrucian",
        "provenance_url": "https://archive.org/details/Geheime-Figuren-der-Rosenkreuzer_3-Hefte_Altona-1785-1788",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["rose cross", "emblem", "divine names", "creation", "kabbalah", "colour plate"],
        "blurb": "The great colour plates of the Geheime Figuren der Rosenkreuzer ('Secret Symbols of "
                 "the Rosicrucians') — the keystone visual document of the Rosicrucian tradition.",
    },
    {
        "key": "biblical_magic_legacy_DISABLED", "short_id": "BIBX", "title": "Magic in the Bible (legacy)",
        "creator": "various", "date": "16th c. onward", "century": 16,
        "place": "Europe", "region": "Europe", "language": "—",
        "era": "renaissance", "tradition": "reception", "tier": "illustration", "root": "LOCAL",
        "image_dir": "biblical",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Witch_of_Endor",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["witch of endor", "necromancy", "biblical", "magician", "vision"],
        "blurb": "Magic as told in scripture and painted across art history — the Witch of Endor, Simon "
                 "Magus, Moses and Pharaoh's magicians — the occult within the canonical image-world.",
    },
    {
        "key": "revival", "short_id": "REV", "title": "The Occult Revival",
        "creator": "various", "date": "1856–1901", "century": 19,
        "place": "France / England", "region": "Europe", "language": "—",
        "era": "modern", "tradition": "theosophy", "tier": "illustration", "root": "LOCAL",
        "image_dir": "revival",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Occultism",
        "rights": "Public domain. Via Wikimedia Commons.",
        "motifs": ["baphomet", "thought-form", "occult revival", "theosophy", "ritual magic"],
        "blurb": "The 19th-century occult revival — Éliphas Lévi's Baphomet and the Theosophists' "
                 "Thought-Forms — where the old tradition was reborn and made modern.",
    },
    {
        "key": "alchemy_ms", "short_id": "AMS", "title": "Medieval Alchemical Manuscripts",
        "creator": "various", "date": "14th–16th c.", "century": 15,
        "place": "Latin Europe", "region": "Europe", "language": "Latin / German",
        "era": "medieval", "tradition": "alchemy", "tier": "illustration", "root": "LOCAL",
        "image_dir": "alchemy_ms",
        "provenance_url": "https://commons.wikimedia.org/wiki/Category:Alchemical_manuscripts",
        "rights": "Public domain / CC BY (per item). Via Wikimedia Commons / Wellcome Collection.",
        "motifs": ["manuscript", "alchemy", "ouroboros", "coniunctio", "dragon", "vessel"],
        "blurb": "The picture-cycles of late-medieval alchemy catalogued by Barbara Obrist — the "
                 "Aurora consurgens, the Rosarium, the Buch der heiligen Dreifaltigkeit and the "
                 "Pretiosa margarita — where illustration first became a mode of alchemical thought.",
    },

    # ---- AlchemyBeatEmUp corpus (root = ALCHEMY_BEU_ROOT): curated, by-text illustration scans.
    #      Extends coverage into the MEDIEVAL stratum and adds key works not otherwise held.
    {
        "key": "aurora_consurgens", "short_id": "AUR", "title": "Aurora Consurgens",
        "creator": "Anonymous (pseudo-Thomas Aquinas)", "date": "c. 1420 (MS)", "century": 15,
        "place": "Zürich (Codex Rhenovacensis)", "region": "Latin West", "language": "Latin",
        "era": "medieval", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "aurora_consurgens",
        "provenance_url": "https://www.e-codices.unifr.ch/en/list/one/zbz/Ms-Rh-0172",
        "rights": "Public domain. Zentralbibliothek Zürich, Ms. Rh. 172 (e-codices).",
        "motifs": ["illuminated manuscript", "dragon", "coniunctio", "sun and moon", "medieval"],
        "blurb": "One of the earliest fully-illustrated alchemical manuscripts — a luminous, strange "
                 "cycle of paintings (dragons, eclipses, a winged figure crushing a smaller one) once "
                 "attributed to Aquinas; the deepest medieval root of the printed emblem tradition.",
    },
    {
        "key": "geber_summa", "short_id": "GEB", "title": "Summa Perfectionis (pseudo-Geber)",
        "creator": "pseudo-Geber (Paul of Taranto?)", "date": "late 13th c. (comp.)", "century": 13,
        "place": "Latin West", "region": "Latin West", "language": "Latin",
        "era": "medieval", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "geber_summa",
        "provenance_url": "https://archive.org/details/geber",
        "rights": "Public domain (verify edition per item).",
        "motifs": ["apparatus", "alembic", "furnace", "distillation", "medieval"],
        "blurb": "The 'Sum of Perfection', the most influential Latin alchemical text of the Middle "
                 "Ages — its apparatus and furnace woodcuts are foundational reference for the "
                 "medieval laboratory.",
    },
    {
        "key": "ripley_scrolls", "short_id": "RIP", "title": "Ripley Scroll",
        "creator": "George Ripley tradition", "date": "15th–16th c.", "century": 15,
        "place": "England", "region": "England", "language": "English / Latin",
        "era": "renaissance", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "ripley_scrolls",
        "provenance_url": "https://wellcomecollection.org/works?query=ripley%20scroll",
        "rights": "Public domain. Wellcome Collection / Huntington scans.",
        "motifs": ["scroll", "dragon", "toad", "alchemical tree", "serpents", "sun and moon"],
        "blurb": "The spectacular emblematic scrolls of the Ripley tradition — towering vertical "
                 "compositions of dragons, toads, serpents, fountains, and the alchemical tree. Among "
                 "the most visually arresting objects in the whole tradition.",
    },
    {
        "key": "lambsprinck", "short_id": "LAM", "title": "De Lapide Philosophico (Lambspring)",
        "creator": "'Lambspring' (Nicolas Barnaud, ed.)", "date": "1625", "century": 17,
        "place": "Frankfurt", "region": "German lands (HRE)", "language": "Latin",
        "era": "early_modern", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "lambsprinck",
        "provenance_url": "https://archive.org/details/musaeumhermeticu00maie",
        "rights": "Public domain. From the Musaeum Hermeticum.",
        "motifs": ["emblem", "two fish", "two birds", "dragon", "ouroboros", "stag and unicorn", "king and son"],
        "blurb": "The fifteen plates of 'Lambspring' from the Musaeum Hermeticum — two fish in a sea, "
                 "stag and unicorn in a forest, a king devouring his son — among the most beloved and "
                 "reproduced of all alchemical emblems.",
    },
    {
        "key": "mutus_liber", "short_id": "MUT", "title": "Mutus Liber (The Silent Book)",
        "creator": "'Altus' (Isaac Baulot?)", "date": "1677", "century": 17,
        "place": "La Rochelle", "region": "France", "language": "(wordless)",
        "era": "early_modern", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "mutus_liber",
        "provenance_url": "https://archive.org/details/mutusliber",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["wordless emblem", "dew collection", "angels", "ladder", "laboratory", "sun and moon"],
        "blurb": "The 'Silent Book' — an entirely wordless sequence of 15 plates teaching the Work by "
                 "image alone: gathering dew, the labours of a couple, angels and ladders. A unique, "
                 "purely visual grammar of alchemy.",
    },
    {
        "key": "symbola_aureae", "short_id": "SAM", "title": "Symbola Aureae Mensae",
        "creator": "Michael Maier", "date": "1617", "century": 17,
        "place": "Frankfurt", "region": "German lands (HRE)", "language": "Latin",
        "era": "early_modern", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "symbola_aureae_mensae",
        "provenance_url": "https://archive.org/details/symbolaaureaemen00maie",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["engraving", "twelve nations", "philosophers", "portrait", "emblem"],
        "blurb": "Maier's 'Symbols of the Golden Table of the Twelve Nations' — engraved emblems "
                 "pairing twelve great alchemists (Hermes, Maria, Geber, Lull, …) each with a symbolic scene.",
    },
    {
        "key": "agricola_metallica", "short_id": "DRM", "title": "De Re Metallica",
        "creator": "Georgius Agricola", "date": "1556", "century": 16,
        "place": "Basel", "region": "German lands (HRE)", "language": "Latin",
        "era": "renaissance", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "agricola_de_re_metallica",
        "provenance_url": "https://www.gutenberg.org/ebooks/38015",
        "rights": "Public domain.",
        "motifs": ["mining", "furnace", "machinery", "metallurgy", "woodcut", "laboratory"],
        "blurb": "Agricola's great illustrated treatise on mining and metallurgy — the gold standard "
                 "for authentic Renaissance furnaces, bellows, and ore-works; the practical substrate "
                 "beneath alchemical theory.",
    },
    {
        "key": "glauber_furni", "short_id": "GLA", "title": "Furni Novi Philosophici",
        "creator": "Johann Rudolph Glauber", "date": "1648", "century": 17,
        "place": "Amsterdam", "region": "Dutch Republic", "language": "German",
        "era": "early_modern", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "glauber_furni_novi",
        "provenance_url": "https://archive.org/details/furninoviphiloso00glau",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["furnace", "distillation", "apparatus", "chemistry", "engraving"],
        "blurb": "Glauber's 'New Philosophical Furnaces' — detailed engravings of distillation furnaces "
                 "and chemical apparatus from one of the founders of practical chemistry.",
    },
    {
        "key": "libavius_alchymia", "short_id": "LIB", "title": "Alchymia",
        "creator": "Andreas Libavius", "date": "1597", "century": 16,
        "place": "Frankfurt", "region": "German lands (HRE)", "language": "Latin",
        "era": "renaissance", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "libavius_alchymia",
        "provenance_url": "https://archive.org/details/alchymiaandreael00liba",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["apparatus", "laboratory plan", "vessels", "furnace", "engraving"],
        "blurb": "Often called the first chemistry textbook — Libavius's 'Alchymia' includes the famous "
                 "plan for an ideal alchemical laboratory ('Chemical House') and meticulous apparatus plates.",
    },
    {
        "key": "biringuccio_piro", "short_id": "PIR", "title": "De la Pirotechnia",
        "creator": "Vannoccio Biringuccio", "date": "1540", "century": 16,
        "place": "Venice", "region": "Republic of Venice", "language": "Italian",
        "era": "renaissance", "tradition": "alchemy", "tier": "illustration", "root": "BEU",
        "image_dir": "biringuccio_pirotechnia",
        "provenance_url": "https://archive.org/details/pirotechnia00biri",
        "rights": "Public domain. Internet Archive scan.",
        "motifs": ["metallurgy", "furnace", "casting", "bellows", "woodcut", "foundry"],
        "blurb": "The first printed work on metallurgy and pyrotechnics — furnaces, foundries, and "
                 "casting woodcuts that ground the alchemical imagination in real fire and metal.",
    },
]

# Mass-sourcing campaign works: registered via data/works_extra.json (one dict per work,
# same schema as a SOURCES entry). Appended here so build_catalog picks them up automatically.
import json as _json
_WORKS_EXTRA = _os.path.join(_PROJECT_ROOT, "data", "works_extra.json")
if _os.path.exists(_WORKS_EXTRA):
    try:
        with open(_WORKS_EXTRA, encoding="utf-8") as _fh:
            _extra = _json.load(_fh)
        _have = {s["key"] for s in SOURCES}
        for _w in _extra:
            if _w.get("key") and _w["key"] not in _have:
                SOURCES.append(_w)
                _have.add(_w["key"])
    except Exception as _e:  # never let a bad extra file break the catalog
        print(f"[config] WARNING: could not load works_extra.json: {_e}")

# Sources whose page scans are mostly text; we still register them but keep them out of the
# default fast build. Map key -> True is implicit via tier == "page_scan".
