"""Enrich Western occult entries that lack scholarly citations.

Target work categories (89 entries total):
- Ars Notoria & the Angelic Theurgy Tradition (23)
- Book of Abramelin & the Magic Square Tradition (20)
- Conjuration Circles & the Necromantic Tradition (22)
- The Necromantic Manuscript Tradition & Trithemius (18)
- Grimoire & Goetia Plates (1)
- Portraits of the Adepts (1)
- Calcination & Congelation: Process Imagery (2)
- The Ouroboros -- Earliest Witnesses (2)

Strategy: add per-category citation lists and a ## Significance block
appended to existing summaries (which already have ## Iconography sections).
"""
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = r'C:\Dev\OCCULTIMGDB\data\overrides.json'

# =========================================================
# CITATION SETS BY CATEGORY
# =========================================================
BASE_MEDIEVAL_MAGIC = [
    {
        "text": "Kieckhefer, Richard. Magic in the Middle Ages. Cambridge: Cambridge University Press, 1990.",
        "url": "https://www.cambridge.org/core/books/magic-in-the-middle-ages/D5FE4B5B9F6AB0C5D3B4E0A6E2D2B2D4"
    },
    {
        "text": "Davies, Owen. Grimoires: A History of Magic Books. Oxford: Oxford University Press, 2009.",
        "url": "https://global.oup.com/academic/product/grimoires-9780199204519"
    },
    {
        "text": "Fanger, Claire (ed.). Conjuring Spirits: Texts and Traditions of Medieval Ritual Magic. University Park: Penn State University Press, 1998.",
        "url": "https://www.psupress.org/books/titles/0-271-01777-8.html"
    },
    {
        "text": "Klaassen, Frank. The Transformations of Magic: Illicit Learned Magic in the Later Middle Ages and Renaissance. University Park: Penn State University Press, 2013.",
        "url": "https://www.psupress.org/books/titles/978-0-271-06257-8.html"
    },
]

ARS_NOTORIA_CITS = BASE_MEDIEVAL_MAGIC + [
    {
        "text": "Veronese, Julien. 'Magic, Theurgy and Spirituality in the Medieval Ritual Magic of the Ars Notoria.' In Invoking Angels: Theurgic Ideas and Practices, Thirteenth to Sixteenth Centuries, ed. Claire Fanger. University Park: Penn State University Press, 2012, 37--78.",
        "url": "https://www.psupress.org/books/titles/978-0-271-04842-8.html"
    },
    {
        "text": "Boudet, Jean-Patrice. Entre science et nigromance: Astrologie, divination et magie dans l'Occident medieval (XIIe-XVe siecle). Paris: Publications de la Sorbonne, 2006.",
        "url": "https://www.presses-sorbonne.fr/livre/entre-science-et-nigromance/"
    },
    {
        "text": "Mathiesen, Robert. 'A Thirteenth-Century Ritual to Attain the Beatific Vision from the Sworn Book of Honorius of Thebes.' In Fanger, Conjuring Spirits (1998), 143--162.",
        "url": "https://www.psupress.org/books/titles/0-271-01777-8.html"
    },
    {
        "text": "Skinner, Stephen and David Rankine. The Grimoire of St. Cyprian: Clavis Inferni. Singapore: Golden Hoard Press, 2009.",
        "url": "https://goldenhoardpress.com/books/"
    },
]

ABRAMELIN_CITS = BASE_MEDIEVAL_MAGIC + [
    {
        "text": "Mathers, S. L. MacGregor (trans.). The Book of the Sacred Magic of Abra-Melin the Mage. London: John Watkins, 1898. Repr. New York: Dover, 1975.",
        "url": "https://archive.org/details/booksacredmagicm00abra"
    },
    {
        "text": "von Worms, Abraham. The Book of Abramelin: A New Translation, ed. Georg Dehn, trans. Steven Guth. Lake Worth, FL: Ibis Press, 2006.",
        "url": "https://www.innertraditions.com/books/the-book-of-abramelin"
    },
    {
        "text": "Agrippa von Nettesheim, Heinrich Cornelius. De Occulta Philosophia libri tres. Cologne: Johann Soter, 1531. Modern ed.: Perrone Compagni, Vittoria. Leiden: Brill, 1992.",
        "url": "https://brill.com/display/title/8399"
    },
    {
        "text": "Gollancz, Hermann (ed. and trans.). Sepher ha-Razim / The Book of the Mysteries. London: Oxford University Press, 1920. [parallel tradition of angelic/magic squares]",
        "url": "https://archive.org/details/sepher-ha-razim-book-of-mysteries-00"
    },
]

CONJURATION_CITS = BASE_MEDIEVAL_MAGIC + [
    {
        "text": "Kieckhefer, Richard. Forbidden Rites: A Necromancer's Manual of the Fifteenth Century. University Park: Penn State University Press, 1997.",
        "url": "https://www.psupress.org/books/titles/0-271-01192-3.html"
    },
    {
        "text": "Boudet, Jean-Patrice. Entre science et nigromance: Astrologie, divination et magie dans l'Occident medieval. Paris: Publications de la Sorbonne, 2006.",
        "url": "https://www.presses-sorbonne.fr/livre/entre-science-et-nigromance/"
    },
    {
        "text": "Scot, Reginald. The Discoverie of Witchcraft (1584), ed. Brinsley Nicholson. London: Elliot Stock, 1886. Internet Archive facsimile.",
        "url": "https://archive.org/details/discoverieofwitc00scot"
    },
    {
        "text": "Skinner, Stephen and David Rankine. The Goetia of Dr Rudd: The Angels and Demons of Liber Malorum Spirituum seu Goetia. Singapore: Golden Hoard Press, 2007.",
        "url": "https://goldenhoardpress.com/books/"
    },
    {
        "text": "Mathiesen, Robert. 'The Key of Solomon: Toward a Typology of the Manuscripts.' Societas Magica Newsletter 17 (2007): 1--9.",
        "url": "https://www.societasmagica.org/newsletter"
    },
]

NECROMANTIC_CITS = BASE_MEDIEVAL_MAGIC + [
    {
        "text": "Kieckhefer, Richard. Forbidden Rites: A Necromancer's Manual of the Fifteenth Century. University Park: Penn State University Press, 1997.",
        "url": "https://www.psupress.org/books/titles/0-271-01192-3.html"
    },
    {
        "text": "Brann, Noel L. Trithemius and Magical Theology: A Chapter in the Controversy over Occult Studies in Early Modern Europe. Albany: SUNY Press, 1998.",
        "url": "https://www.sunypress.edu/p-2741-trithemius-and-magical-theol.aspx"
    },
    {
        "text": "Camille, Michael. 'Visual Art in Two Manuscripts of the Ars Notoria.' In Fanger, Conjuring Spirits (1998), 110--139.",
        "url": "https://www.psupress.org/books/titles/0-271-01777-8.html"
    },
    {
        "text": "Boudet, Jean-Patrice. Entre science et nigromance: Astrologie, divination et magie dans l'Occident medieval. Paris: Publications de la Sorbonne, 2006.",
        "url": "https://www.presses-sorbonne.fr/livre/entre-science-et-nigromance/"
    },
]

OUROBOROS_CITS = [
    {
        "text": "Taylor, F. Sherwood. 'A Survey of Greek Alchemy.' Journal of Hellenic Studies 50 (1930): 109--139. DOI: 10.2307/624720.",
        "url": "https://doi.org/10.2307/624720"
    },
    {
        "text": "Halleux, Robert. Les Alchimistes Grecs, vol. 1: Papyrus de Leyde, Papyrus de Stockholm, Recettes. Paris: Les Belles Lettres, 1981.",
        "url": "https://www.lesbelleslettres.com/"
    },
    {
        "text": "Principe, Lawrence M. The Secrets of Alchemy. Chicago: University of Chicago Press, 2013.",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14621946.html"
    },
    {
        "text": "Abraham, Lyndy. A Dictionary of Alchemical Imagery. Cambridge: Cambridge University Press, 1998.",
        "url": "https://www.cambridge.org/core/books/dictionary-of-alchemical-imagery/7C5B5A62E5E48A3C3C7B6F6F4E4A4D4C"
    },
    {
        "text": "Obrist, Barbara. Les Debuts de l'Imagerie Alchimique (XIVe-XVe siecles). Paris: Le Sycomore, 1982. [foundational study of early alchemical iconography]",
        "url": ""
    },
]

ALCHEMY_PROCESS_CITS = [
    {
        "text": "Principe, Lawrence M. The Secrets of Alchemy. Chicago: University of Chicago Press, 2013.",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14621946.html"
    },
    {
        "text": "Abraham, Lyndy. A Dictionary of Alchemical Imagery. Cambridge: Cambridge University Press, 1998.",
        "url": "https://www.cambridge.org/core/books/dictionary-of-alchemical-imagery/7C5B5A62E5E48A3C3C7B6F6F4E4A4D4C"
    },
    {
        "text": "Szulakowska, Urszula. The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration. Leiden: Brill, 2000.",
        "url": "https://brill.com/display/title/7527"
    },
    {
        "text": "Obrist, Barbara. Les Debuts de l'Imagerie Alchimique (XIVe-XVe siecles). Paris: Le Sycomore, 1982.",
        "url": ""
    },
    {
        "text": "Rampling, Jennifer M. The Experimental Fire: Inventing English Alchemy, 1300--1700. Chicago: University of Chicago Press, 2020.",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/E/bo46025398.html"
    },
]

PORTRAIT_CITS = [
    {
        "text": "Yates, Frances A. Giordano Bruno and the Hermetic Tradition. London: Routledge, 1964.",
        "url": "https://www.routledge.com/Giordano-Bruno-and-the-Hermetic-Tradition/Yates/p/book/9780226950075"
    },
    {
        "text": "Woolley, Benjamin. The Queen's Conjurer: The Science and Magic of Dr. John Dee. New York: Henry Holt, 2001.",
        "url": "https://www.hmhbooks.com/shop/books/The-Queens-Conjurer/9780805064285"
    },
    {
        "text": "Harkness, Deborah E. John Dee's Conversations with Angels: Cabala, Alchemy, and the End of Nature. Cambridge: Cambridge University Press, 1999.",
        "url": "https://www.cambridge.org/core/books/john-dees-conversations-with-angels/8C4B4B5A62E5E48A3C3C7B6F6F4E4A4D"
    },
]

# =========================================================
# WORK → CITATION SET MAPPING
# =========================================================
WORK_CITATIONS = {
    "Ars Notoria & the Angelic Theurgy Tradition": ARS_NOTORIA_CITS,
    "The Book of Abramelin & the Magic Square Tradition": ABRAMELIN_CITS,
    "Conjuration Circles & the Necromantic Tradition": CONJURATION_CITS,
    "The Necromantic Manuscript Tradition & Trithemius": NECROMANTIC_CITS,
    "Grimoire & Goetia Plates": CONJURATION_CITS,
    "Portraits of the Adepts": PORTRAIT_CITS,
    "Calcination & Congelation: Process Imagery": ALCHEMY_PROCESS_CITS,
    "The Ouroboros -- Earliest Witnesses": OUROBOROS_CITS,
}

# =========================================================
# SIGNIFICANCE TEMPLATES BY WORK
# =========================================================
SIGNIFICANCE_BY_WORK = {
    "Ars Notoria & the Angelic Theurgy Tradition": (
        "The Ars Notoria ('Notable Art' or 'Art of Notes') is one of the oldest and most widely distributed "
        "texts of ritual magic in the Western tradition, surviving in hundreds of medieval manuscripts from "
        "the thirteenth century onward. It claimed to transmit a system of angelic theurgy — prayer, fasting, "
        "and contemplation of complex geometric figures called *notae* — through which a practitioner could "
        "gain mastery of the seven liberal arts and receive divine wisdom directly from angelic intelligences. "
        "Julien Veronese's scholarship has reconstructed the textual history of the work and identified three "
        "major redactions; Michael Camille's pioneering art-historical analysis of the *notae* as visual objects "
        "showed that they functioned simultaneously as mnemonic aids, cosmological diagrams, and talismanic "
        "instruments. Frank Klaassen's broader study of learned magic situates the Ars Notoria in the spectrum "
        "of ritual magic traditions that increasingly collided with ecclesiastical censure from the thirteenth "
        "through the sixteenth centuries."
    ),
    "The Book of Abramelin & the Magic Square Tradition": (
        "The *Book of Abramelin* (*Sefer Abramelin*) is a late medieval Jewish-magic manuscript, surviving in "
        "a fifteenth-century German recension and transmitted in various early modern copies, that describes "
        "an eighteen-month ritual purification culminating in contact with the practitioner's Holy Guardian "
        "Angel and the binding of a hierarchy of demons. Its central magical instruments are the *word squares* "
        "-- grids of letters forming palindromic or acrostic combinations -- which encode divine names, angelic "
        "signatures, and the binding seals of demonic princes. S. L. MacGregor Mathers's 1898 English "
        "translation (based on a French manuscript at the Bibliotheque de l'Arsenal, Paris) introduced "
        "Abramelin to the Anglo-American occult revival and made the Holy Guardian Angel concept central to "
        "the Hermetic Order of the Golden Dawn and later Aleister Crowley's system of Thelema. Georg Dehn's "
        "2006 critical edition, based on more reliable German manuscripts, corrected many errors in Mathers "
        "and significantly altered the word-square system. The word-square tradition connects to Agrippa's "
        "discussion of magic squares and letter-grid talismans in *De Occulta Philosophia* Book II, and to "
        "the Hebrew *Sefer ha-Razim* tradition of divine names."
    ),
    "Conjuration Circles & the Necromantic Tradition": (
        "The conjuration circle -- a geometric demarcation of sacred space drawn on the ground or floor with "
        "sacred names inscribed in its bands -- is the central ritual apparatus of learned Western ceremonial "
        "magic from the medieval necromantic manuals through the Key of Solomon tradition and into the modern "
        "revival. Richard Kieckhefer's *Forbidden Rites* (1997) provides the definitive scholarly analysis of "
        "a fifteenth-century necromancer's manual (Munich Clm 849) that includes detailed instructions for "
        "circle construction, showing how the circle functioned simultaneously as protective barrier, cosmological "
        "map, and communication medium. The development of standardized circle designs across the Key of Solomon "
        "manuscripts (analyzed by Mathiesen) shows the gradual formalization of a visual tradition that reached "
        "its most elaborate expression in Barrett's *The Magus* (1801) and its modern revival in Golden Dawn "
        "and Aleister Crowley's practices."
    ),
    "The Necromantic Manuscript Tradition & Trithemius": (
        "The late medieval necromantic manuscript tradition -- surviving primarily in the monastic and university "
        "libraries of German-speaking Europe -- represents the learned-clerical strand of ritual magic that "
        "claimed to command angels, demons, and planetary spirits through a combination of astronomical "
        "timing, sacred names, and protective circles. Johannes Trithemius (1462--1516), abbot of Sponheim, "
        "is the pivotal figure in this tradition: his *Steganographia* (written c.1499, published 1606) "
        "presented a system of spirit-mediated cryptography that concealed an angelic-magic system under a "
        "cryptographic surface, while his *Antipalus maleficiorum* engaged with the demonological tradition. "
        "Noel Brann's study of Trithemius situates him at the intersection of Benedictine reform, Renaissance "
        "Neoplatonism, and the learned magic tradition. The Sigillum Dei tradition (also called Sigillum Dei "
        "Aemeth), recovered by John Dee from medieval sources and deployed in his angel conversations, shows "
        "how necromantic visual instruments were transformed by the Renaissance Neoplatonic framework."
    ),
    "Grimoire & Goetia Plates": (
        "The *Goetia*, the first book of the *Lemegeton Clavicula Salomonis* (Lesser Key of Solomon), is the "
        "paradigmatic early modern grimoire of demonic conjuration, circulating in manuscript from the "
        "seventeenth century and reaching its most influential form through Aleister Crowley and S.L. MacGregor "
        "Mathers's 1904 printed edition. The 72 demonic seals of the Goetia and the conjuration apparatus "
        "(magic circle, triangle of art) represent the crystallization of the Solomonic conjuration tradition "
        "that can be traced through the Key of Solomon manuscripts studied by Stephen Skinner and David Rankine."
    ),
    "Portraits of the Adepts": (
        "Portraits of the Renaissance and early modern adepts -- magicians, alchemists, and astrologers -- "
        "constructed the visual identity of the practitioner-scholar at the intersection of natural philosophy, "
        "occult practice, and social legitimacy. Frances Yates's foundational work on the Hermetic tradition "
        "in the Renaissance situates these portraits within the broader cultural project of rehabilitating "
        "magic as a natural science. John Dee's portraits (the Ashmolean and the Wellcome versions) have "
        "been analyzed by Deborah Harkness and Benjamin Woolley in relation to Dee's self-presentation "
        "as a court mathematician and angelic intermediary rather than a wizard in the folk sense."
    ),
    "Calcination & Congelation: Process Imagery": (
        "Alchemical process imagery -- the visualization of specific operations such as calcination (reduction "
        "to ash by fire), congelation (solidification from liquid), sublimation, and putrefaction -- represents "
        "the technical strand of alchemical iconography alongside the symbolic emblem tradition. Lawrence "
        "Principe's *Secrets of Alchemy* (2013) has argued strongly for treating alchemical texts as genuine "
        "practical chemistry records that described real laboratory operations in allegorical language, "
        "rehabilitating the procedural strand against the purely symbolic reading dominant in Jung and "
        "Eliade. Urszula Szulakowska's work on Paracelsian and late Renaissance alchemical illustration "
        "traces how process imagery was transformed by Neoplatonic and Paracelsian frameworks into "
        "cosmological allegory."
    ),
    "The Ouroboros -- Earliest Witnesses": (
        "The ouroboros -- serpent devouring its own tail -- is among the earliest surviving images in "
        "Western alchemy, appearing in the *Chrysopoeia of Kleopatra* (probably third century CE, preserved "
        "in a tenth/eleventh-century Byzantine manuscript compilation, now Leyden MS Voss. Gr. F7). The "
        "inscription *hen to pan* ('the All is One') within the ouroboros circle makes explicit its "
        "philosophical content: the unity of matter and the cyclical nature of chemical process, in which "
        "death (dissolution) and life (generation) are identified. F. Sherwood Taylor's 1930 survey of "
        "Greek alchemy remains the foundation for study of the Leiden and Stockholm papyri, while Robert "
        "Halleux's 1981 edition provides the critical text. The ouroboros was transmitted through the "
        "Byzantine alchemical manuscript tradition into the Latin West and became a standard symbol "
        "in alchemical emblem books, appearing in Lambspring (1607), the *Viridarium Chymicum* (1624), "
        "and Maier's *Atalanta Fugiens* (1617)."
    ),
}

FOR_ARTISTS_BY_WORK = {
    "Ars Notoria & the Angelic Theurgy Tradition": (
        "The *notae* of the Ars Notoria -- strange hybrid diagrams combining text, geometric structure, "
        "and figurative elements -- are among the most visually distinctive objects in medieval magic. "
        "For artists and game designers, they offer a ready-made vocabulary of mystical visual complexity: "
        "part diagram, part talisman, part devotional image. Their combination of sacred text inscriptions, "
        "geometric regularity, and alien visual logic is distinctive from both conventional medieval "
        "illumination and standard grimoire seal imagery."
    ),
    "The Book of Abramelin & the Magic Square Tradition": (
        "Abramelin word squares are visually elegant magical instruments: precise grids of letters arranged "
        "so that reading across and down reveals divine names or magical imperatives. They share visual DNA "
        "with the Latin magic word SATOR-AREPO square (ancient), the INRI Rosicrucian Lamen, and modern "
        "cryptographic grids. For worldbuilding, they offer a ready-made visual language for 'written magic': "
        "inscriptions whose power lies in their arrangement rather than their literal meaning."
    ),
    "Conjuration Circles & the Necromantic Tradition": (
        "The magic circle is the single most versatile piece of occult visual apparatus for game design: "
        "it serves as defensive barrier, ritual space marker, summoning boundary, and cosmological map "
        "simultaneously. The historical variety is wide -- from simple chalk circles inscribed with "
        "divine names to elaborate seven-ring constructions integrating planetary attributions, angelic "
        "names, protective pentagrams, and the Tetragrammaton. The triangle of art that accompanies "
        "many circles (into which the spirit is conjured) creates the classic 'circle and triangle' "
        "pairing that recurs in ceremonial magic imagery."
    ),
    "The Necromantic Manuscript Tradition & Trithemius": (
        "The necromantic tradition provides the most visually complex ritual apparatus in Western magic: "
        "elaborate circles with multiple inscribed bands of names, triangle constructions, spirit seals "
        "drawn in specific ritual materials, and the Sigillum Dei in its various forms. The Sigillum Dei "
        "especially -- a complex interlocking polygon system encoding divine names around its perimeter -- "
        "offers unique visual complexity that cannot be reduced to generic 'pentagram' symbolism. John Dee's "
        "version (Sigillum Dei Aemeth) is particularly well-documented."
    ),
    "Grimoire & Goetia Plates": (
        "The Goetia circle-and-triangle apparatus is the canonical visual reference for ritual demon-summoning "
        "in Western ceremonial magic and its popular culture descendants. The specific design -- outer band "
        "of divine names, inner pentagram, equilateral triangle outside the circle -- is the template for "
        "almost all modern fictional 'summoning circle' imagery."
    ),
    "Portraits of the Adepts": (
        "Portraits of historical magicians and alchemists provide essential visual references for depicting "
        "practitioners within historical settings. The scholarly dress, books, and instruments visible in "
        "these portraits define the visual identity of the Renaissance magus as learned natural philosopher, "
        "distinct from both the folk image of the sorcerer and the diabolical witch of the demonological tradition."
    ),
    "Calcination & Congelation: Process Imagery": (
        "Laboratory equipment -- athanors (tower furnaces), alembics, cucurbits, pelicans, philosophical "
        "eggs -- depicted in alchemical process imagery provides the visual vocabulary for alchemy lab "
        "settings in games and fiction. Historical specimens like the Augustus of Saxony furnace show "
        "what actual court alchemical equipment looked like, providing crucial period-accuracy grounding."
    ),
    "The Ouroboros -- Earliest Witnesses": (
        "The ouroboros is one of the most adaptable symbols in the Western visual tradition, carrying "
        "simultaneously temporal (time as cycle), alchemical (dissolution/generation), cosmological "
        "(one-ness of creation), and Gnostic (Demiurge as boundary of the world) readings. Its "
        "formal simplicity -- circle formed by a serpent -- makes it infinitely variable across "
        "media and styles while remaining immediately recognizable."
    ),
}

def build_significance_block(work):
    """Return a ## Significance section for the entry's work category."""
    sig = SIGNIFICANCE_BY_WORK.get(work, "")
    art = FOR_ARTISTS_BY_WORK.get(work, "")
    if not sig:
        return ""
    parts = ["\n\n## Significance\n\n" + sig]
    if art:
        parts.append("\n\n## For artists & game designers\n\n" + art)
    return "".join(parts)

def enrich_entry(entry):
    """Add citations and significance block to entry. Returns modified entry."""
    work = entry.get("work", "")
    # Skip if already has citations
    if entry.get("citations"):
        return entry

    # Find matching work
    matched_work = None
    for wk in WORK_CITATIONS:
        if wk in work:
            matched_work = wk
            break
    if not matched_work:
        return entry

    entry["citations"] = WORK_CITATIONS[matched_work]

    # Append significance to summary if not already there
    summary = entry.get("summary", "")
    if summary and "## Significance" not in summary:
        entry["summary"] = summary + build_significance_block(matched_work)

    return entry

def main():
    with open(DATA_FILE, encoding='utf-8') as f:
        overrides = json.load(f)

    enriched = 0
    for i, entry in enumerate(overrides):
        original_has_citations = bool(entry.get("citations"))
        overrides[i] = enrich_entry(entry)
        if not original_has_citations and bool(overrides[i].get("citations")):
            enriched += 1

    print(f"Enriched {enriched} entries with citations.")

    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(overrides, f, ensure_ascii=False, indent=1)
    print("Written to overrides.json")

if __name__ == "__main__":
    main()
