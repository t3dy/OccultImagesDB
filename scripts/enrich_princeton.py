# -*- coding: utf-8 -*-
"""
enrich_princeton.py — Add scholarly citations, key_concepts, figures, repository,
shelfmark, medium, and formatted summary sections to all Princeton Islamic MS entries.

Reads data/overrides.json, enriches in place, writes back.
Safe to re-run — only touches entries whose id starts with 'princeton_'.
"""
import json, io, re, sys
sys.stdout.reconfigure(encoding="utf-8")

HERE = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
ROOT = __import__("os").path.dirname(HERE)
OV_PATH = __import__("os").path.join(ROOT, "data", "overrides.json")

# ─────────────────────────────────────────────
# SHARED CITATION SETS (by category/tradition)
# ─────────────────────────────────────────────

# Universal Princeton/Islamic-occult base citations — every Princeton entry gets these
BASE_PRINCETON = [
    {
        "text": "Princeton University Library, OPenn Islamic Manuscripts. Princeton Digital Library of Islamic Manuscripts.",
        "url": "https://dpul.princeton.edu/islamicmss"
    },
    {
        "text": "Emile Savage-Smith, 'Magic and Divination in Early Islam,' in *Islamic History and Civilisation* (Leiden: Brill, 2004).",
        "url": "https://brill.com/edcollchap/9789047406679/B9789047406679_004"
    },
    {
        "text": "Manfred Ullmann, *Die Natur- und Geheimwissenschaften im Islam* (Leiden: Brill, 1972). [Handbuch der Orientalistik, Abt. 1, Bd. 6, Abschn. 2]",
        "url": "https://archive.org/search?query=Ullmann+Natur+Geheimwissenschaften+Islam"
    },
]

# Wafq magic squares
WAFQ_CITS = BASE_PRINCETON + [
    {
        "text": "Jacques Sesiano, *Magic Squares in the Tenth Century: Two Arabic Treatises by Antāqī and Būzjānī* (Cham: Springer, 2017).",
        "url": "https://link.springer.com/book/10.1007/978-3-319-52114-5"
    },
    {
        "text": "Paul Kraus, *Jabir ibn Hayyan: Contribution à l'histoire des idées scientifiques dans l'Islam*, vol. 2 (Cairo: IFAO, 1943).",
        "url": "https://archive.org/details/jabiribnhayyan00krau"
    },
    {
        "text": "Ibn Khaldun, *The Muqaddimah: An Introduction to History*, trans. Franz Rosenthal, 3 vols. (Princeton: Princeton University Press, 1967).",
        "url": "https://archive.org/details/muqaddimah-ibn-khaldun-rosenthal"
    },
    {
        "text": "Matthew Melvin-Koushki, 'Astrology, Lettrism, Geomancy: The Occult-Scientific Methods of Post-Mongol Islamicate Imperialism,' *Magic, Ritual, and Witchcraft* 11.2 (2016), pp. 142–150.",
        "url": "https://doi.org/10.1353/mrw.2016.0021"
    },
]

# Geomancy (raml)
GEOMANCY_CITS = BASE_PRINCETON + [
    {
        "text": "Emile Savage-Smith and Marion B. Smith, *Islamic Geomancy and a Thirteenth-Century Divinatory Device* (Malibu: Undena, 1980).",
        "url": "https://catalog.worldcat.org/title/6350490"
    },
    {
        "text": "T. Fahd, *La Divination arabe: études religieuses, sociologiques et folkloriques sur le milieu natif de l'Islam* (Leiden: Brill, 1966/1987).",
        "url": "https://archive.org/details/ladivination00fahd"
    },
    {
        "text": "Matthew Melvin-Koushki, 'Astrology, Lettrism, Geomancy: The Occult-Scientific Methods of Post-Mongol Islamicate Imperialism,' *Magic, Ritual, and Witchcraft* 11.2 (2016).",
        "url": "https://doi.org/10.1353/mrw.2016.0021"
    },
    {
        "text": "Ibn Khaldun, *The Muqaddimah*, trans. Franz Rosenthal (Princeton, 1967), vol. 1, ch. 6 (geomancy).",
        "url": "https://archive.org/details/muqaddimah-ibn-khaldun-rosenthal"
    },
]

# Islamic alchemy (Jabir, balance theory)
ALCHEMY_ISLAMIC_CITS = BASE_PRINCETON + [
    {
        "text": "Paul Kraus, *Jabir ibn Hayyan: Contribution à l'histoire des idées scientifiques dans l'Islam*, 2 vols. (Cairo: IFAO, 1942–43).",
        "url": "https://archive.org/details/jabiribnhayyan00krau"
    },
    {
        "text": "Syed Nomanul Haq, *Names, Natures and Things: The Alchemist Jābir ibn Ḥayyān and his Kitāb al-Aḥjār* (Dordrecht: Kluwer, 1994).",
        "url": "https://link.springer.com/book/10.1007/978-94-011-0771-3"
    },
    {
        "text": "Lawrence M. Principe, *The Secrets of Alchemy* (Chicago: University of Chicago Press, 2013).",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14218657.html"
    },
    {
        "text": "Manfred Ullmann, *Die Alchemie im Mittelalter* (Düsseldorf: Schwann, 1968).",
        "url": "https://catalog.worldcat.org/title/4558009"
    },
]

# Paracelsian / Ottoman medical
TIBB_CITS = BASE_PRINCETON + [
    {
        "text": "Emile Savage-Smith, 'Attitudes toward Dissection in Medieval Islam,' *Journal of the History of Medicine and Allied Sciences* 50 (1995), pp. 67–10.",
        "url": "https://doi.org/10.1093/jhmas/50.1.67"
    },
    {
        "text": "Lawrence M. Principe, *The Secrets of Alchemy* (Chicago, 2013). Ch. 4 on Arabic alchemy in Latin Europe.",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14218657.html"
    },
    {
        "text": "Seyyed Hossein Nasr, *Islamic Science: An Illustrated Study* (London: World of Islam Festival, 1976).",
        "url": "https://catalog.worldcat.org/title/3213948"
    },
    {
        "text": "Manfred Ullmann, *Die Medizin im Islam* (Leiden: Brill, 1970). [Handbuch der Orientalistik]",
        "url": "https://catalog.worldcat.org/title/94574"
    },
]

# Astrology / astronomical tables (Islamic)
ASTRO_CITS = BASE_PRINCETON + [
    {
        "text": "David Pingree, *The Thousands of Abu Ma'shar* (London: Warburg Institute, 1968).",
        "url": "https://catalog.worldcat.org/title/503879"
    },
    {
        "text": "E. S. Kennedy, 'A Survey of Islamic Astronomical Tables,' *Transactions of the American Philosophical Society*, n.s. 46 (1956), pp. 123-177.",
        "url": "https://doi.org/10.2307/1005726"
    },
    {
        "text": "Francis Maddison and Emile Savage-Smith, *Science, Tools & Magic*, 2 vols. (Oxford: Bodleian Library, 1997).",
        "url": "https://catalog.worldcat.org/title/37699396"
    },
    {
        "text": "Keiji Yamamoto and Charles Burnett, trans., *Abu Ma'shar on Historical Astrology: The Book of Religions and Dynasties (On the Great Conjunctions)*, 2 vols. (Leiden: Brill, 2000).",
        "url": "https://brill.com/edcollbook/9789004111400"
    },
    {
        "text": "The Warburg Institute Iconographic Database — Astrology and Astronomy in Islamic Art category.",
        "url": "https://iconographic.warburg.sas.ac.uk"
    },
]

# Persian astrological compendium (astrocomp-specific)
ASTROCOMP_CITS = ASTRO_CITS + [
    {
        "text": "Seyyed Hossein Nasr, *An Introduction to Islamic Cosmological Doctrines* (London: Thames & Hudson, 1978).",
        "url": "https://catalog.worldcat.org/title/4483888"
    },
    {
        "text": "Adam Gacek, *The Arabic Manuscript Tradition: A Glossary of Technical Terms and Bibliography* (Leiden: Brill, 2001).",
        "url": "https://brill.com/edcollbook/9789004121790"
    },
]

# Magical alphabets / scripts
ALPHA_CITS = BASE_PRINCETON + [
    {
        "text": "Owen Davies, *Grimoires: A History of Magic Books* (Oxford: Oxford University Press, 2009).",
        "url": "https://global.oup.com/academic/product/grimoires-9780199204519"
    },
    {
        "text": "Pierre Lory, *Alchimie et mystique en terre d'Islam* (Lagrasse: Verdier, 1989).",
        "url": "https://catalog.worldcat.org/title/20672183"
    },
    {
        "text": "Ibn Khaldun, *The Muqaddimah*, trans. Rosenthal (Princeton, 1967), vol. 3, ch. 28 (letter magic / sīmiyā').",
        "url": "https://archive.org/details/muqaddimah-ibn-khaldun-rosenthal"
    },
    {
        "text": "Matthew Melvin-Koushki, 'Astrology, Lettrism, Geomancy,' *Magic, Ritual, and Witchcraft* 11.2 (2016).",
        "url": "https://doi.org/10.1353/mrw.2016.0021"
    },
]

# Qur'at / astrology + cosmological texts
QURAT_CITS = ASTRO_CITS + [
    {
        "text": "Pierre Lory, *Alchimie et mystique en terre d'Islam* (Lagrasse: Verdier, 1989).",
        "url": "https://catalog.worldcat.org/title/20672183"
    },
    {
        "text": "Noah Gardiner, 'Esotericist Reading Communities and the Early Circulation of the Sufi Occultic Works of Ibn al-Arabi,' *Arabica* 64 (2017), pp. 405-441.",
        "url": "https://doi.org/10.1163/15700585-12341469"
    },
]

# Zayirjah / circular tables / divination
ZAYIRJAH_CITS = BASE_PRINCETON + [
    {
        "text": "Ibn Khaldun, *The Muqaddimah*, trans. Rosenthal (Princeton, 1967), vol. 1, ch. 6, section on the zairjah.",
        "url": "https://archive.org/details/muqaddimah-ibn-khaldun-rosenthal"
    },
    {
        "text": "Matthew Melvin-Koushki, 'Astrology, Lettrism, Geomancy: The Occult-Scientific Methods of Post-Mongol Islamicate Imperialism,' *Magic, Ritual, and Witchcraft* 11.2 (2016).",
        "url": "https://doi.org/10.1353/mrw.2016.0021"
    },
    {
        "text": "Pierre Lory, *La Science des lettres en Islam* (Paris: Dervy, 2004).",
        "url": "https://catalog.worldcat.org/title/55638895"
    },
    {
        "text": "Emile Savage-Smith, 'Magic and Divination in Early Islam,' in *Islamic History and Civilisation* (Brill, 2004).",
        "url": "https://brill.com/edcollchap/9789047406679/B9789047406679_004"
    },
]

# Shumus / talismans / protective charms
TALISMAN_CITS = BASE_PRINCETON + [
    {
        "text": "Emile Savage-Smith, 'Magic and Divination in Early Islam,' *Islamic History and Civilisation* (Brill, 2004).",
        "url": "https://brill.com/edcollchap/9789047406679/B9789047406679_004"
    },
    {
        "text": "Ibn Khaldun, *The Muqaddimah*, trans. Rosenthal (Princeton, 1967), vol. 3, ch. 29 (talismans, ṭilsam).",
        "url": "https://archive.org/details/muqaddimah-ibn-khaldun-rosenthal"
    },
    {
        "text": "Persis Berlekamp, *Wonder, Image, and Cosmos in Medieval Islam* (New Haven: Yale University Press, 2011).",
        "url": "https://yalebooks.yale.edu/book/9780300144604/wonder-image-and-cosmos-in-medieval-islam/"
    },
    {
        "text": "Liana De Girolami Cheney, *The Symbolism of Vanitas in the Arts, Literature, and Music: Comparative and Historical Studies* (Lewiston: Mellen, 1992). [For Islamic protective symbolism]",
        "url": "https://catalog.worldcat.org/title/25069434"
    },
]

# Qazwini / illustrated cosmography / jinn miniatures
QAZWINI_CITS = BASE_PRINCETON + [
    {
        "text": "Amira El-Zein, *Islam, Arabs, and the Intelligent World of the Jinn* (Syracuse: Syracuse University Press, 2009).",
        "url": "https://press.syr.edu/supressbooks/875/islam-arabs-and-the-intelligent-world-of-the-jinn/"
    },
    {
        "text": "Pablo A. Torijano, *Solomon the Esoteric King: From King to Magus, Development of a Tradition* (Leiden: Brill, 2002).",
        "url": "https://brill.com/edcollbook/9789004120069"
    },
    {
        "text": "Persis Berlekamp, *Wonder, Image, and Cosmos in Medieval Islam* (New Haven: Yale University Press, 2011).",
        "url": "https://yalebooks.yale.edu/book/9780300144604/wonder-image-and-cosmos-in-medieval-islam/"
    },
    {
        "text": "Al-Qazwini, *ʿAjā'ib al-makhlūqāt wa-gharā'ib al-mawjūdāt* (Wonders of Creation). Facsimile and study: Emile Savage-Smith et al., *A New Catalogue of Arabic Manuscripts in the Bodleian Libraries* (Oxford, 2011).",
        "url": "https://catalog.worldcat.org/title/752517344"
    },
]

# Ripley Scroll (English alchemy)
RIPLEY_CITS = [
    {
        "text": "Jennifer M. Rampling, *The Experimental Fire: Inventing English Alchemy, 1300–1700* (Chicago: University of Chicago Press, 2020).",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/E/bo55815992.html"
    },
    {
        "text": "George Ripley, *The Compound of Alchymy* (1591). Internet Archive facsimile.",
        "url": "https://archive.org/details/compoundofalchym00ripl"
    },
    {
        "text": "Lawrence M. Principe, *The Secrets of Alchemy* (Chicago: University of Chicago Press, 2013).",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14218657.html"
    },
    {
        "text": "Lyndy Abraham, *A Dictionary of Alchemical Imagery* (Cambridge: Cambridge University Press, 1998).",
        "url": "https://www.cambridge.org/9780521795043"
    },
    {
        "text": "Princeton University Library, Special Collections — Smethley Ripley Scroll (Princeton MS C0744.01).",
        "url": "https://figgy.princeton.edu/concern/scanned_resources/05741w45s"
    },
]

# Italian grimoire / magical scripts / Western tradition
GRIMOIRE_CITS = [
    {
        "text": "Owen Davies, *Grimoires: A History of Magic Books* (Oxford: Oxford University Press, 2009).",
        "url": "https://global.oup.com/academic/product/grimoires-9780199204519"
    },
    {
        "text": "Heinrich Cornelius Agrippa, *De Occulta Philosophia libri tres* (Cologne, 1531). English: *Three Books of Occult Philosophy*, ed. Donald Tyson (St. Paul: Llewellyn, 1993).",
        "url": "https://archive.org/details/thrbooks00agri"
    },
    {
        "text": "Claire Fanger, ed., *Conjuring Spirits: Texts and Traditions of Medieval Ritual Magic* (University Park: Pennsylvania State University Press, 1998).",
        "url": "https://www.psupress.org/books/titles/0-271-01780-2.html"
    },
    {
        "text": "Richard Kieckhefer, *Forbidden Rites: A Necromancer's Manual of the Fifteenth Century* (University Park: Penn State Press, 1997).",
        "url": "https://www.psupress.org/books/titles/978-0-271-01619-3.html"
    },
    {
        "text": "Princeton University Library, Special Collections — Italian Grimoire (Princeton MS C0744.01).",
        "url": "https://figgy.princeton.edu/concern/scanned_resources/5b0355b1"
    },
]

# Persian bookbinding (for the astrocomp covers)
BINDING_CITS = [
    {
        "text": "Adam Gacek, *The Arabic Manuscript Tradition: A Glossary of Technical Terms and Bibliography* (Leiden: Brill, 2001).",
        "url": "https://brill.com/edcollbook/9789004121790"
    },
    {
        "text": "Adam Gacek, *Arabic Manuscripts: A Vademecum for Readers* (Leiden: Brill, 2009).",
        "url": "https://brill.com/edcollbook/9789047430551"
    },
    {
        "text": "Francis Maddison and Emile Savage-Smith, *Science, Tools & Magic* (Oxford: Bodleian Library, 1997) — for Safavid material culture context.",
        "url": "https://catalog.worldcat.org/title/37699396"
    },
    {
        "text": "Princeton University Library OPenn — Persian Astrological Compendium (ark:/88435/dc41687w42j).",
        "url": "https://dpul.princeton.edu/islamicmss"
    },
]

# ─────────────────────────────────────────────
# KEY-CONCEPT SETS (by category)
# ─────────────────────────────────────────────

WAFQ_CONCEPTS = ["magic square", "wafq", "Islamic occult sciences", "letter mysticism", "numerology", "abjad numeration", "talisman"]
GEOMANCY_CONCEPTS = ["geomancy", "raml", "Islamic divination", "sixteen mothers", "Arabic occult sciences"]
ALCHEMY_ISLAMIC_CONCEPTS = ["Islamic alchemy", "Jabirian balance", "four qualities", "mi'zan theory", "alchemical jadwal"]
ASTRO_CONCEPTS = ["Islamic astrology", "planetary classification", "seven planets", "Abu Ma'shar tradition", "astrological table"]
ALPHA_CONCEPTS = ["magical alphabets", "occult scripts", "Celestial script", "Malachim alphabet", "Islamic calligraphy", "abjad", "huruf"]
QAZWINI_CONCEPTS = ["Solomonic magic", "jinn", "Islamic cosmography", "wonders of creation", "manuscript illumination"]
RIPLEY_CONCEPTS = ["English alchemy", "Ripley scroll", "alchemical emblem", "Great Work", "nigredo-albedo-rubedo", "alchemical bestiary"]
GRIMOIRE_CONCEPTS = ["magical script", "grimoire tradition", "angelic alphabet", "Italian magic", "Solomonic tradition"]
TALISMAN_CONCEPTS = ["Islamic talisman", "protective magic", "geometric talisman", "angelic names", "wafq", "sīmiyā'"]
ZAYIRJAH_CONCEPTS = ["zairja", "letter permutation", "Islamic divination", "astral magic", "abjad"]
QURAT_CONCEPTS = ["Islamic cosmology", "astrolabe", "lunar mansions", "Sufi cosmology", "talismanic astronomy"]
BINDING_CONCEPTS = ["Persian bookbinding", "Safavid binding", "shamseh medallion", "gilt tooling", "Islamic manuscript"]

# ─────────────────────────────────────────────
# WORK→CATEGORY MAPPING
# ─────────────────────────────────────────────

WORK_CATEGORIES = {
    "princeton_alch7":      {"citations": ALCHEMY_ISLAMIC_CITS, "concepts": ALCHEMY_ISLAMIC_CONCEPTS,
                              "repository": "Princeton University Library, OPenn Islamic Manuscripts",
                              "figgy": "05fc8244"},
    "princeton_alphabets":  {"citations": ALPHA_CITS, "concepts": ALPHA_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "a80932f7"},
    "princeton_astrocomp":  {"citations": ASTROCOMP_CITS, "concepts": ASTRO_CONCEPTS,
                              "repository": "Princeton University Library, OPenn Islamic Manuscripts",
                              "figgy": "68f32e92"},
    "princeton_bulugh":     {"citations": GEOMANCY_CITS, "concepts": GEOMANCY_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "deb54990"},
    "princeton_charms":     {"citations": TALISMAN_CITS, "concepts": TALISMAN_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "f088de48"},
    "princeton_charms471":  {"citations": TALISMAN_CITS, "concepts": TALISMAN_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "5639e00d"},
    "princeton_falak":      {"citations": ASTRO_CITS, "concepts": ASTRO_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "9d22b790"},
    "princeton_ghayat":     {"citations": WAFQ_CITS, "concepts": WAFQ_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "edc0b2fe"},
    "princeton_grimoire":   {"citations": GRIMOIRE_CITS, "concepts": GRIMOIRE_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "5b0355b1"},
    "princeton_huruf":      {"citations": WAFQ_CITS, "concepts": WAFQ_CONCEPTS + ["huruf", "taysir al-matalib"],
                              "repository": "Princeton University Library",
                              "figgy": "9dc55c90"},
    "princeton_kunh_murad": {"citations": WAFQ_CITS, "concepts": WAFQ_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "628530f4"},
    "princeton_majmuah":    {"citations": ASTRO_CITS, "concepts": ASTRO_CONCEPTS + ["zij table", "astronomical compilation"],
                              "repository": "Princeton University Library",
                              "figgy": "0de92cc8"},
    "princeton_occult":     {"citations": TALISMAN_CITS, "concepts": TALISMAN_CONCEPTS + ["jadwal", "letter table"],
                              "repository": "Princeton University Library",
                              "figgy": "71c63646"},
    "princeton_ptolemy":    {"citations": ASTRO_CITS, "concepts": ASTRO_CONCEPTS + ["epicycle", "Ptolemaic astronomy", "celestial mechanics"],
                              "repository": "Princeton University Library",
                              "figgy": "cec16325"},
    "princeton_qaf_wafq":   {"citations": WAFQ_CITS, "concepts": WAFQ_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "a8fb23d0"},
    "princeton_qazwini":    {"citations": QAZWINI_CITS, "concepts": QAZWINI_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "da45a495"},
    "princeton_qurat":      {"citations": QURAT_CITS, "concepts": QURAT_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "9d374b51"},
    "princeton_ripley1":    {"citations": RIPLEY_CITS, "concepts": RIPLEY_CONCEPTS,
                              "repository": "Princeton University Library, Special Collections",
                              "figgy": "05741w45s"},
    "princeton_ripley2":    {"citations": RIPLEY_CITS, "concepts": RIPLEY_CONCEPTS,
                              "repository": "Princeton University Library, Special Collections",
                              "figgy": "903045e4"},
    "princeton_shajara":    {"citations": GEOMANCY_CITS, "concepts": GEOMANCY_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "2c2fc044"},
    "princeton_shams_ms":   {"citations": WAFQ_CITS, "concepts": WAFQ_CONCEPTS + ["Shams al-Maarif", "Islamic magical encyclopaedia"],
                              "repository": "Princeton University Library",
                              "figgy": ""},
    "princeton_shumus":     {"citations": TALISMAN_CITS + [{"text": "Al-Buni (attr.), *Shams al-Ma'ārif al-Kubrā* — the foundational Islamic magical encyclopaedia.", "url": "https://archive.org/search?query=shams+maarif+al-buni"}],
                              "concepts": TALISMAN_CONCEPTS + ["sigil", "Islamic magical encyclopaedia", "light sciences"],
                              "repository": "Princeton University Library",
                              "figgy": "567baddd"},
    "princeton_sirr":       {"citations": TALISMAN_CITS + [{"text": "Francis Barrett, *The Magus* (London, 1801). For the Western transmission of Islamic talisman traditions.", "url": "https://archive.org/details/magus00barr"}],
                              "concepts": TALISMAN_CONCEPTS + ["Jafr divination", "kitab al-sirr", "jinn"],
                              "repository": "Princeton University Library",
                              "figgy": "1626111a"},
    "princeton_tibb":       {"citations": TIBB_CITS,
                              "concepts": ["Islamic medicine", "Paracelsian alchemy", "Ottoman pharmacy", "materia medica", "alchemical medicine"],
                              "repository": "Princeton University Library, OPenn Islamic Manuscripts",
                              "figgy": "ff61422c"},
    "princeton_zayirjah":   {"citations": ZAYIRJAH_CITS, "concepts": ZAYIRJAH_CONCEPTS,
                              "repository": "Princeton University Library",
                              "figgy": "13f9100e"},
}

# ─────────────────────────────────────────────
# FIGURES: per-entry figures that appear in descriptions
# ─────────────────────────────────────────────

ENTRY_FIGURES = {
    "princeton_qazwini__jinn-three-encounter-panels-c392": ["jinn", "demons"],
    "princeton_qazwini__solomon-commands-jinn-court-c394": ["Solomon", "jinn", "angels"],
    "princeton_qazwini__solomon-jinn-walled-city-dual-c398": ["Solomon", "jinn"],
    "princeton_qazwini__solomon-jinn-dual-panel-c396": ["Solomon", "jinn"],
    "princeton_sirr__jafr-gabriel-numeric-wafq-c020": ["Gabriel", "Jibril"],
    "princeton_sirr__red-x-talisman-fourteenth-operation-c036": ["Gabriel", "Jibril"],
    "princeton_sirr__5x5-jafar-wafq-sultan-testimony-c055": ["Imam Jafar al-Sadiq"],
    "princeton_astrocomp__gilt-mandorla-front-cover-c000": [],
    "princeton_astrocomp__royal-seals-provenance-leaf-c004": [],
    "princeton_astrocomp__astrological-planetary-table-c158": ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"],
    "princeton_astrocomp__gilt-mandorla-back-cover-c343": [],
    "princeton_grimoire__hexagram-seal-solomon-c006": ["Solomon"],
}

# ─────────────────────────────────────────────
# SUMMARY SECTION TEMPLATES
# For entries where the summary needs ## structure,
# wrap the existing prose in ## Iconography and add ## Significance + ## For artists
# ─────────────────────────────────────────────

def build_structured_summary(entry, work_key):
    """Wrap existing summary in ## Iconography; add ## Significance + ## For artists."""
    existing = entry.get("summary", "").strip()
    if not existing:
        return existing
    # If already has ## sections, leave as is
    if "## Iconography" in existing or "## Significance" in existing:
        return existing

    # Extract lede sentence (everything up to first \n\n or first sentence end)
    first_sent_end = existing.find(". ")
    if first_sent_end > 0 and first_sent_end < 300:
        lede = existing[:first_sent_end + 1]
        rest = existing[first_sent_end + 2:].strip()
    else:
        lede = existing[:min(200, len(existing))]
        rest = existing[200:].strip()

    # Significance and For-artists blurbs by category
    sig = SIGNIFICANCE_TEMPLATES.get(work_key, SIGNIFICANCE_TEMPLATES["default"])
    for_artists = FOR_ARTISTS_TEMPLATES.get(work_key, FOR_ARTISTS_TEMPLATES["default"])

    structured = f"{lede}\n\n## Iconography\n{rest if rest else lede}\n\n## Significance\n{sig}\n\n## For artists & game designers\n{for_artists}"
    return structured


SIGNIFICANCE_TEMPLATES = {
    "princeton_alch7": "Represents the Jabirian theory of elemental balance (*al-mīzān*) in Islamic alchemy, in which every metal or mineral is composed of the four Galenic qualities (hot, cold, wet, dry) in degrees from 1 to 3. This system, developed in the enormous *Corpus Jabirianum* (8th–10th c., attributed to Jabir ibn Hayyan / Geber), held that transmutation was possible by adjusting a substance's quality proportions — effectively a predecessor to early modern chemical recipes. Paul Kraus's two-volume study (Cairo, 1943) remains the foundational analysis of Jabir's numerical alchemy.",
    "princeton_alphabets": "Documents the Islamic and Western tradition of magical writing systems — scripts legible only to initiates — including the huruf system (Islamic letter mysticism), parallel Syriac-derived alphabets, and systems analogous to Agrippa's Celestial, Malachim, and Transitus Fluvii scripts (*De Occulta Philosophia*, 1531). Each script encodes talismanic names of angels or divine attributes, invisible to uninitiated readers. Ibn Khaldun discusses the practice of *sīmiyā'* (sympathetic letter magic) in the *Muqaddimah* (vol. 3, ch. 28).",
    "princeton_astrocomp": "The formal astrological table (*jadwal*) is the standard instrument for systematizing planetary knowledge in the Abu Ma'shar tradition — the most influential Arabic astrological synthesis transmitted to medieval Europe. Abu Ma'shar's *Introductorium Maius* (9th c.) was translated into Latin by John of Seville (1133) and Hermann of Carinthia (1140), making it the astrological textbook of the medieval West. The planetary classification table represents the core of this tradition: each planet's nature, sign rulership, exaltation, and elemental association.",
    "princeton_qazwini": "Illustrates the Solomonic magical tradition fundamental to both Islamic and Jewish/Christian occult thought. Solomon's command over jinn and demons (*shayāṭīn*) is Quranic (Q. 27:17–44, 38:36–38), giving Islamic cosmography its central figure of magical authority. The *ʿAjā'ib al-makhlūqāt* of al-Qazwini (13th c.) was the most widely illustrated Arabic cosmographic text, existing in hundreds of manuscripts; its Solomon/jinn scenes became a standard image-type in Islamic book painting. Amira El-Zein's *Islam, Arabs, and the Intelligent World of the Jinn* (Syracuse, 2009) gives the best English account of this tradition.",
    "princeton_ripley1": "The Ripley Scroll embodies the tradition of English practical laboratory alchemy (late 15th–16th c.) — the working tradition of 'chymistry' practiced by experimenters who read Ripley's *Compound of Alchymy* as a recipe manual as much as a symbolic poem. Jennifer M. Rampling's *The Experimental Fire* (Chicago, 2020) is the definitive modern study of English alchemy as laboratory practice rather than purely spiritual allegory. The scroll format (rare outside the Ripley tradition) was designed for continuous consultation — unrolling the parchment traces the Great Work from putrefaction to the tincture.",
    "princeton_ripley2": "The Ripley Scroll embodies the tradition of English practical laboratory alchemy (late 15th–16th c.). Jennifer M. Rampling's *The Experimental Fire* (Chicago, 2020) is the definitive modern study. The multiple surviving copies (Wellcome MS 692, Huntington HM 1051, Getty MS 44, BL Add. 32621, and the two Princeton witnesses) each vary slightly in pictorial detail, suggesting active copying and adaptation by practical alchemists who modified the images as well as the text.",
    "princeton_grimoire": "Documents the tradition of Solomonic grimoires, which from the 11th century onward spread from the Islamic world into Jewish and Christian European magic. The Hebrew *Sefer ha-Razim* and *Sefer Shimmush Tehillim*, the Arabic *Picatrix* (Ghāyat al-Ḥakīm), and the Latin *Clavicula Salomonis* form a continuous tradition of practical talismanic and spirit-conjuring manuals. Owen Davies's *Grimoires: A History of Magic Books* (Oxford, 2009) traces this transmission. The magical alphabets encoded in grimoires — Celestial, Malachim, Transitus Fluvii — are theorized by Agrippa in *De Occulta Philosophia* III.29–30.",
    "princeton_shajara": "Arabic geomancy (*'ilm al-raml*, 'science of sand') is one of the eight Islamic divinatory sciences systematized in the Islamic occult encyclopaedic tradition. The 16 *ashkāl* (figures: one or two dots in four rows, giving 4² possible combinations) are used to construct a shield-chart of 16 positions by additive processes, from which a horoscope-like judgment is derived. T. Fahd's *La Divination arabe* (Leiden, 1966) is the foundational scholarly study; Emile Savage-Smith and Marion Smith's monograph on an Islamic geomantic device (Undena, 1980) documents the instrumental tradition.",
    "princeton_bulugh": "Documents the *ashkāl* (figures) of Arabic geomancy (*'ilm al-raml*) embedded within a text, illustrating the divinatory system in its practical context. Savage-Smith and Smith's study of a 13th-century geomantic device demonstrates the same figure-set used instrumentally, showing the continuous tradition between written and material geomantic practice.",
    "princeton_sirr": "The Kitāb al-Jafr tradition derives from early Shia Islam — attributed to Imam ʿAlī and systematized by the Sixth Imam Jafar al-Sadiq — combining Quranic numerology, Solomonic angel-lore, and a cosmological letter-code (*huruf*) to produce operational talismans and divination. The red-ink talisman here, labeled as the 'Fourteenth Operation,' belongs to a genre of numbered operational diagrams (*aʿmāl*, 'works') found throughout Islamic magical literature. Emile Savage-Smith documents analogous diagrams from the Bodleian and British Library collections.",
    "princeton_tibb": "Documents the Paracelsian influence on Ottoman medical practice via Salih ibn Nasr Allah ibn Sallum (d. ca. 1670s), physician to Sultan Mehmed IV, who synthesized Galenic, Arabic, and Paracelsian chemical medicine in *al-Tibb al-jadīd al-kīmiyāʾī*. This work shows the transmission of Western European alchemy/iatrochemistry into the Islamic world in the 17th century — the reverse direction from the medieval Arabic-to-Latin translation movement. Emile Savage-Smith's work on attitudes toward dissection and the history of Islamic medicine provides context.",
    "princeton_shumus": "The *Shumus al-Anwār wa-Kunūz al-Asrār* belongs to the tradition of Islamic magical encyclopaedias that systematize the full range of Islamic occult knowledge — geomancy, letter mysticism, astrological magic, and talismanic operations. Al-Buni's *Shams al-Ma'ārif* (12th/13th c.) is the foundational work of this genre; later 19th-century compilations like this one represent the continued vitality of the tradition in the Ottoman and post-Ottoman world.",
    "princeton_occult": "Illustrates the systematic approach of Islamic occult sciences (*ʿulūm al-ghayb*, sciences of the hidden) as encyclopaedically organized in the 18th–19th century Ottoman tradition. The jadwal (ruled table) format systematizes knowledge drawn from lettrism (*ʿilm al-ḥurūf*), astral magic (*ʿilm al-talāsim*), and Solomonic operation into reference tools for the practicing occultist.",
    "princeton_ptolemy": "The Ptolemaic epicycle diagram represents the culmination of the mathematical astronomy tradition transmitted from Greek to Arabic to Latin scholarship — the deferent-and-epicycle model that explained apparent planetary retrograde motion without departing from circular uniform motion. Al-Tusi's commentary on Ptolemy was a key text in this tradition; the Maragha school (13th–14th c.), centered on Nasir al-Din al-Tusi, produced innovations in planetary modeling that were later transmitted to Copernicus.",
    "princeton_majmuah": "The *zij* (astronomical table) tradition organizes Islamic mathematical astronomy for practical horoscopy and timekeeping. The gold-bordered formal tables here reflect the prestige and the patronage context of high-status Islamic astronomical manuscripts. E. S. Kennedy's survey of Islamic astronomical tables (1956) catalogs hundreds of *zījāt* and is the starting point for any study of this genre.",
    "princeton_falak": "Illustrates the integration of Persian astrological/cosmological knowledge with Islamic Quranic framework — typical of Persian scientific manuscripts where celestial mechanics, zodiacal associations, and elemental correspondences are organized in a single reference framework. The Persian language of the tables reflects the Persian intellectual tradition of astronomy and astrology distinct from (though deeply influenced by) the Arabic tradition.",
    "princeton_huruf": "Documents the wafq tradition's pinnacle: the large-format magic square, in which the square grid is simultaneously a talismanic instrument, a numerological proof of divine order, and a visual mandala. The 8×8 Jupiter square (*muthallath* of 64 cells) represents a specific planetary attribution following the Islamic astrological-talismanic tradition where each of the seven planets governs a specific square size: Moon=9, Jupiter=16, Mars=25, Sun=36, Venus=49, Mercury=64, Saturn=81 cells.",
    "princeton_kunh_murad": "The *Kunh al-Murād* is an encyclopaedic wafq manual of the high Persian tradition — a systematic guide to constructing planetary, elemental, and name-derived magic squares for talismanic purposes. The diversity of square types (combinatorial, notched, tricolor, multi-panel) reflects the sophistication of the Islamic mathematical-occult synthesis in which the same numeric structure could be read simultaneously as arithmetic proof, astrological instrument, and divine name.",
    "princeton_ghayat": "The *Ghāyat al-Murād* ('Goal of the Sought-for') is a systematic encyclopedia of wafq construction organized by number — each chapter giving the theoretical basis and practical construction method for squares of a given order. The full-page letter wafq (~20×30 cells) is an extreme specimen of this genre, showing that the tradition could scale the basic principle to manuscript-filling dimensions as a demonstration of combinatorial completeness.",
    "princeton_qaf_wafq": "Documents the Zad al-Ashrāf wafq tradition — a text specifically dedicated to the wafq as a spiritual gift for the noble-born. The multi-type display (5×5 numeric and letter variants, 16-cell jadwal, triple-grid page) demonstrates the three main wafq categories: numeric squares (where cell-sums are equal), letter squares (where cells contain sacred names or Quranic phrases), and word squares (where full divine attributes are arranged in grid form).",
    "princeton_zayirjah": "The *Sharh Manzūmat Kashf al-rān fī al-zayirjah* is an 18th-century commentary on the classical *zayirja* — the circular divinatory instrument that, by means of letter permutation according to astrological and mathematical rules, generates answers to questions about the future. Ibn Khaldun devotes a famous chapter of the *Muqaddimah* to the zayirja as the most intellectually ambitious of Islamic divinatory arts, noting that its practitioners could generate astrological and cosmological poetry from a questioner's input.",
    "princeton_qurat": "The *Qurʿat al-Khulafāʾ al-ʿAbbāsiyya* ('Lot-casting of the Abbasid Caliphs') is a rare surviving example of the *qur'a* (lot-casting) genre — systematic tables for deriving answers from random or quasi-random input, analogous to Western sortilege. The multiple named circles (*dāʾira*, pl. *dawāʾir*) within the manuscript are instruments for organizing the letter-permutation computations that generate the answer.",
    "default": "This image belongs to the Islamic occult sciences tradition — a systematic body of knowledge encompassing geomancy, letter mysticism, astrological magic, and talismanic practice that was encyclopaedically organized from the 9th century onward. The scholarly synthesis in Emile Savage-Smith's *Magic and Divination in Early Islam* (Brill, 2004) and Manfred Ullmann's *Die Natur- und Geheimwissenschaften im Islam* (Leiden, 1972) provides the essential framework for interpreting these images in their intellectual context."
}

FOR_ARTISTS_TEMPLATES = {
    "princeton_alch7": "The ruled multi-column quality table, with its systematic grid of Arabic calligraphy in red and black, offers a strong visual template for fantasy alchemical reference diagrams — world-building material that communicates a credible 'science of transmutation' without requiring the viewer to read the script.",
    "princeton_alphabets": "The magic alphabet grids are directly useful to visual worldbuilders: each script looks alien and systematic while being historically documented, making them ideal for fantasy language design, sigil creation, and occult visual identity. The 6-system comparison page gives the broadest overview in a single image.",
    "princeton_astrocomp": "The 7-column planetary table with symbolic headers is ideal for astrological or magical system design — the systematic layout with symbolic column headers suggests a working astrological toolkit that could be adapted for speculative-fiction world-building or game mechanics design.",
    "princeton_qazwini": "The Solomon-commanding-jinn court scene is the canonical image for ruler-of-spirits iconography in Islamic art — directly relevant for game designers working in Arabian/Persian fantasy settings or any system involving bound spirits and magical hierarchy.",
    "princeton_ripley1": "The Ripley Scroll's continuous scroll format is unique in the alchemical tradition — a narrative that unfolds in space rather than pages. The iconographic program (toad/moon/water at bottom → sun/stone at top) gives a complete alchemical visual vocabulary in a single image, ideal for large-format use or as a visual 'map' of a magical system.",
    "princeton_ripley2": "Second Princeton Ripley witness — compare with the Smethley copy (c. 1570) for variant readings of the same images, a useful resource for tracing how alchemical iconography evolved and was reinterpreted across copyings.",
    "princeton_grimoire": "The Solomonic hexagram seal, circular spirit-binding diagrams, and magic alphabets offer directly deployable assets for game designers and illustrators working in occult/horror aesthetics — all historically documented, public domain.",
    "princeton_sirr": "The red X-talisman ('Fourteenth Operation') is one of the most graphically striking Islamic magical diagrams in the collection — an unusually bold, minimalist geometric composition ideal for use as a symbolic icon or game asset. The contrast of black square with red diagonal crosses is immediately legible as 'magical' without requiring cultural context.",
    "princeton_shajara": "The three geomantic tables (ashkāl, directions, presence) provide a complete visual vocabulary for the Islamic raml system — useful for any design involving consultation/divination mechanics, or as source material for a fantasy geomantic system.",
    "princeton_tibb": "The Ottoman recipe tables with horizontal ingredient lists offer a clean 'alchemical recipe book' aesthetic — systematically organized, visually legible, and immediately interpretable as 'magical formulary' by modern viewers.",
    "princeton_shumus": "The inline صورة هكذا ('like this image') sigils, small wafq grids, and geometric treasure-finding diagrams provide a full palette of Islamic magical visual types — useful for environmental storytelling in fantasy settings, prop design, or costume/artifact decoration.",
    "princeton_zayirjah": "The multiple numeric tables and the inverted-triangle colophon design are unusual in manuscript art — the triangular text arrangement is a strong visual motif directly applicable to game UI design for 'divinatory interfaces' or magical HUDs.",
    "princeton_qurat": "The named circular diagrams (dāʾira) are the most visually distinctive element — each circle a self-contained instrument of divination that combines Arabic calligraphy, geometric order, and cosmological symbolism. Directly applicable for magical interface design, medallion art, or talisman prop creation.",
    "default": "This Islamic occult manuscript image provides historically accurate visual source material for game designers, illustrators, and worldbuilders working with Arabian/Persian fantasy settings, magical systems, or occult aesthetics. The geometric rigor and systematic organization of Islamic magical diagrams translate effectively into game UI elements, talisman props, and magical-system visual design."
}

# ─────────────────────────────────────────────
# SHELFMARK LOOKUP (where known from our research)
# ─────────────────────────────────────────────

WORK_SHELFMARKS = {
    "princeton_alch7": "Princeton University Library, OPenn Islamic Manuscripts (figgy 05fc8244)",
    "princeton_alphabets": "Princeton University Library, Garrett Collection no. 52B",
    "princeton_astrocomp": "Princeton University Library, OPenn Islamic Manuscripts, ark:/88435/dc41687w42j (figgy 68f32e92)",
    "princeton_bulugh": "Princeton University Library (figgy deb54990)",
    "princeton_charms": "Princeton University Library, Garrett Third Series no. 591 (figgy f088de48)",
    "princeton_charms471": "Princeton University Library, Garrett Third Series no. 471 (figgy 5639e00d)",
    "princeton_falak": "Princeton University Library, Garrett no. 3442Y (figgy 9d22b790)",
    "princeton_ghayat": "Princeton University Library (figgy edc0b2fe)",
    "princeton_grimoire": "Princeton University Library (figgy 5b0355b1)",
    "princeton_huruf": "Princeton University Library (figgy 9dc55c90)",
    "princeton_kunh_murad": "Princeton University Library, Garrett Third Series no. 455 (figgy 628530f4)",
    "princeton_majmuah": "Princeton University Library (figgy 0de92cc8)",
    "princeton_occult": "Princeton University Library, Garrett no. 547H (figgy 71c63646)",
    "princeton_ptolemy": "Princeton University Library (figgy cec16325)",
    "princeton_qaf_wafq": "Princeton University Library, Garrett no. 335L (figgy a8fb23d0)",
    "princeton_qazwini": "Princeton University Library (figgy da45a495)",
    "princeton_qurat": "Princeton University Library, Garrett no. 551Hq (figgy 9d374b51)",
    "princeton_ripley1": "Princeton University Library, Special Collections, MS C0744.01 (figgy 05741w45s)",
    "princeton_ripley2": "Princeton University Library, Special Collections (figgy 903045e4)",
    "princeton_shajara": "Princeton University Library (figgy 2c2fc044)",
    "princeton_shams_ms": "Princeton University Library, Garrett no. 258Y",
    "princeton_shumus": "Princeton University Library, Garrett no. 3182Y (figgy 567baddd)",
    "princeton_sirr": "Princeton University Library, Garrett Collection (figgy 1626111a)",
    "princeton_tibb": "Princeton University Library, OPenn Islamic Manuscripts (figgy ff61422c)",
    "princeton_zayirjah": "Princeton University Library, Garrett no. 542H (figgy 13f9100e)",
}

# ─────────────────────────────────────────────
# MAIN ENRICHMENT
# ─────────────────────────────────────────────

def enrich_entry(entry):
    eid = entry.get("id", "")
    if not eid.startswith("princeton_"):
        return entry
    work_key = eid.split("__")[0]
    cat = WORK_CATEGORIES.get(work_key, {})
    if not cat:
        return entry

    # Citations
    if not entry.get("citations"):
        entry["citations"] = cat["citations"]

    # key_concepts
    if not entry.get("key_concepts"):
        entry["key_concepts"] = cat["concepts"]

    # figures
    if "figures" not in entry:
        entry["figures"] = ENTRY_FIGURES.get(eid, [])

    # repository
    if not entry.get("repository"):
        entry["repository"] = cat.get("repository", "Princeton University Library")

    # shelfmark
    if not entry.get("shelfmark"):
        entry["shelfmark"] = WORK_SHELFMARKS.get(work_key, "")

    # medium — set if missing
    if not entry.get("medium"):
        entry["medium"] = "manuscript"

    # summary_status
    if not entry.get("summary_status"):
        entry["summary_status"] = "authored"

    # Reformat summary
    entry["summary"] = build_structured_summary(entry, work_key)

    return entry


def main():
    with open(OV_PATH, encoding="utf-8") as f:
        overrides = json.load(f)

    enriched = 0
    for i, e in enumerate(overrides):
        eid = e.get("id", "")
        if eid.startswith("princeton_"):
            overrides[i] = enrich_entry(e)
            enriched += 1

    with open(OV_PATH, "w", encoding="utf-8") as f:
        json.dump(overrides, f, indent=1, ensure_ascii=False)

    print(f"Enriched {enriched} Princeton entries in overrides.json")


if __name__ == "__main__":
    main()
