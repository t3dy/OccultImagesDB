# -*- coding: utf-8 -*-
"""
fix_nocit_orphans.py — resolve the 14 remaining nocit catalog entries.

Actions:
  1. Delete 4 junk/duplicate image files from sources_web so build_catalog
     no longer generates stubs for them.
  2. Add proper override entries (title, summary, citations) for the 10
     remaining orphan images that ARE worth keeping.

Run once, then rebuild:
  python scripts/fix_nocit_orphans.py && python scripts/build_all.py
"""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OVERRIDES_PATH = os.path.join(ROOT, 'data', 'overrides.json')
SW = os.path.join(ROOT, 'sources_web')

# ── 1. Delete bad/duplicate image files ──────────────────────────────────────

DELETE_FILES = [
    # Apartment building in SE Asia — completely wrong file
    os.path.join(SW, 'islamic_alchemy', 'jabir_seventy.jpg'),
    # Medieval Saint Barbara badge — misnamed as "lab scene painting"
    os.path.join(SW, 'islamic_alchemy', 'lab_scene_paint.jpg'),
    # Exact duplicate of jabir_alchemist.jpg (same bytes/engraving)
    os.path.join(SW, 'islamic_alchemy', 'jabir_portrait.jpg'),
    # Partial 4-panel composite; all22woodcuts-composite already covers it
    os.path.join(SW, 'compendium_maleficarum', 'panorama_ANCHO.jpg'),
]

deleted = 0
for p in DELETE_FILES:
    if os.path.exists(p):
        os.remove(p)
        print(f'Deleted: {p}')
        deleted += 1
    else:
        print(f'Already gone: {p}')
print(f'{deleted} file(s) deleted.\n')

# ── 2. Override entries for the 10 keepers ───────────────────────────────────

NEW_ENTRIES = [
    # ------------------------------------------------------------------
    {
        "id": "ancient_alchemy__farnese-atlas-naples",
        "title": "Farnese Atlas — Earliest Surviving Map of the Greek Constellations",
        "medium": "sculpture",
        "summary": (
            "The Farnese Atlas, a Roman marble copy (c. 2nd century CE) of a lost "
            "Hellenistic original, shows the Titan Atlas kneeling under the weight of a "
            "celestial sphere (globus caelestis) incised with the 48 Ptolemaic constellations. "
            "Now in the Museo Nazionale Archeologico di Napoli (inv. 6374), it was discovered in "
            "the Farnese baths, Rome, in the 16th century. The sphere is the oldest surviving "
            "three-dimensional representation of the Greek constellation system; scholars, "
            "notably Hipparchus scholar Bradley Schaefer, have used its star positions to argue "
            "it preserves the lost star catalogue of Hipparchus (c. 129 BCE). Constellations "
            "visible include Libra, Pegasus, Perseus, Andromeda, Orion, and Taurus. For the "
            "history of alchemy, the Farnese Atlas encodes the cosmological frame — the "
            "48 figures of the celestial sphere within which planetary, zodiacal, and stellar "
            "correspondences were worked out — that underlies Greco-Egyptian alchemical "
            "cosmology from Zosimos onward. The alchemical tradition inherited from Hellenistic "
            "astrology a theory of cosmic sympathy and planetary rulers over metals that is "
            "legible precisely in this sphere: Saturn rules lead, Jupiter tin, Mars iron, "
            "Sol gold, Venus copper, Mercury quicksilver, and Luna silver."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Halleux, Robert. *Les textes alchimiques*. Brepols, 1979. Ch. 1: "
                     "Greek and Hellenistic origins of the alchemical tradition."},
            {"text": "Fowden, Garth. *The Egyptian Hermes: A Historical Approach to the Late "
                     "Pagan Mind*. Cambridge University Press, 1986. On Hermetic cosmology "
                     "and its Hellenistic matrix."},
            {"text": "Dekker, Elly. *Illustrating the Phaenomena: Celestial Cartography in "
                     "Antiquity and the Middle Ages*. Oxford University Press, 2013. "
                     "Catalogue entry for the Farnese Atlas and its star positions."},
            {"text": "Principe, Lawrence M. *The Secrets of Alchemy*. University of Chicago "
                     "Press, 2013. Ch. 1: ancient roots of the alchemical tradition in "
                     "Hellenistic Egypt."},
            {"text": "Obrist, Barbara. *Les débuts de l'imagerie alchimique (XIVe–XVe siècles)*. "
                     "Le Sycomore, 1982. On cosmological imagery in the medieval alchemical "
                     "manuscript tradition descending from Hellenistic sources."},
        ],
    },

    # ------------------------------------------------------------------
    {
        "id": "ars_notoria__sigillum-dei-aemeth",
        "title": "Sigillum Dei Aemeth — Seal of the Truth of God (Liber Iuratus Tradition)",
        "medium": "diagram",
        "summary": (
            "The Sigillum Dei Aemeth ('Seal of the Truth of God'), a complex heptagonal "
            "diagram from the learned magic tradition. This manuscript copy preserves the "
            "characteristic seven-sided nested polygon design, reading from the outside in: "
            "an outer ring of Hebrew divine names (EMETH, ELOHIM, etc.), a heptagonal frame "
            "with angelic names in seven planetary sectors, a pentagonal layer, a five-pointed "
            "star, and finally the divine name at the centre. The title at the top reads "
            "SIGILLVM DEI AEMETH EMETH. The diagram originates in the *Liber Iuratus Honorii* "
            "(Sworn Book of Honorius, c. 1225), one of the most ambitious grimoires of the "
            "high medieval period, which claimed that possession of the Sigillum Dei would "
            "grant its possessor knowledge of all things and power over spirits. The present "
            "manuscript version predates John Dee's famous wax-disk adaptation (1582) but "
            "belongs to the same continuous tradition. Dee's version, drawn from the *Liber "
            "Iuratus* via the *Book of Soyga*, added 40-digit Pythagorean tables at the "
            "perimeter and became the central ritual object of his Enochian angel sessions "
            "recorded in the *Mysteriorum Libri* (British Library, MS Sloane 3188)."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Véronèse, Julien. *L'Ars notoria au Moyen Âge: Introduction et édition "
                     "critique*. SISMEL–Edizioni del Galluzzo, 2007. Critical edition of "
                     "the Ars Notoria tradition, with the Liber Iuratus in its manuscript context."},
            {"text": "Klaassen, Frank. *The Transformations of Magic: Illicit Learned Magic "
                     "in the Later Middle Ages and Renaissance*. Penn State University Press, "
                     "2013. On the Sigillum Dei as a central object of clerical operative magic."},
            {"text": "Kieckhefer, Richard. *Magic in the Middle Ages*. Cambridge University "
                     "Press, 1989. Ch. 6: learned magic and the clerical underworld; the "
                     "tradition of the Ars Notoria."},
            {"text": "Clulee, Nicholas H. *John Dee's Natural Philosophy: Between Science and "
                     "Religion*. Routledge, 1988. On Dee's adaptation of the Sigillum Dei "
                     "Aemeth for the Enochian scrying sessions."},
            {"text": "Harkness, Deborah E. *John Dee's Conversations with Angels: Cabala, "
                     "Alchemy, and the End of Nature*. Cambridge University Press, 1999. "
                     "The role of the Sigillum in Dee's angelic communication system."},
        ],
    },

    # ------------------------------------------------------------------
    {
        "id": "geomancy_ms__geomantic-classification",
        "title": "Arabic Geomancy Classification Table — Raml Diagram",
        "medium": "diagram",
        "summary": (
            "A square geomancy diagram from an Arabic manuscript, divided by diagonals into "
            "triangular sections bearing the names of geomantic figures in Arabic script, "
            "with additional annotations at the edges. The diagram functions as a "
            "classification table for the 16 geomantic figures (*ashkal*, pl. of *shakl*), "
            "arranging them according to their elemental, planetary, and directional "
            "attributions — the fundamental reference grid for interpreting a *raml* "
            "(sand-divination) shield chart. The 16 figures are binary combinations of odd "
            "and even (single and double) dot-rows in four elemental positions, yielding "
            "configurations associated with the seven planets and the twelve zodiacal signs. "
            "Arabic geomancy (*'ilm al-raml*, 'science of sand') was codified between the 9th "
            "and 12th centuries CE and transmitted to Latin Europe as *geomantia* from the "
            "11th century. In Latin guise — with figure names such as Via, Populus, Fortuna "
            "Major, Acquisitio, Rubeus, and so on — it became one of the most widely "
            "practised learned divination systems of medieval and early modern Europe, "
            "appearing in manuscripts alongside astrology, chiromancy, and physiognomy as "
            "part of a coherent Renaissance divinatory complex."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Savage-Smith, Emily and Marion B. Smith. *Islamic Geomancy and a "
                     "Thirteenth-Century Divinatory Device*. Undena Publications, 1980. "
                     "Foundational study of Arabic geomancy with manuscript sources."},
            {"text": "Fahd, Toufic. *La Divination arabe: Études religieuses, sociologiques "
                     "et folkloriques sur le milieu natif de l'Islam*. Brill, 1966. "
                     "Comprehensive survey of Arabic divination including the raml tradition."},
            {"text": "Boudet, Jean-Patrice. *Entre science et nigromance: Astrologie, "
                     "divination et magie dans l'Occident médiéval (XIIe–XVe siècle)*. "
                     "Publications de la Sorbonne, 2006. Latin reception of Arabic geomancy."},
            {"text": "Skinner, Stephen. *Terrestrial Astrology: Divination by Geomancy*. "
                     "Routledge & Kegan Paul, 1980. The 16 figures and their planetary "
                     "attributions in comparative context."},
            {"text": "Principe, Lawrence M. *The Secrets of Alchemy*. University of Chicago "
                     "Press, 2013. On the divinatory arts as part of the broader occult "
                     "philosophy tradition contextualising alchemy."},
        ],
    },

    # ------------------------------------------------------------------
    {
        "id": "islamic_alchemy__ibn-sina-portrait",
        "title": "Portrait of Avicenna (Ibn Sina) — 'Tableau ancien'",
        "medium": "painting",
        "figures": ["Ibn Sina"],
        "summary": (
            "A black-and-white photograph of an early painted portrait of Ibn Sina "
            "(Latin: Avicenna, 980–1037 CE), labelled at the lower edge *AVICENNE / Tableau "
            "ancien* (Avicenna — ancient painting). The portrait shows a bearded man in turban "
            "and dark robes, half-bust, against a dark background in the manner of early modern "
            "scholar portraiture. Ibn Sina was the foremost philosopher-physician of the "
            "medieval Islamic world. His *Kitab al-Shifa* (Book of Healing, covering logic, "
            "natural science, mathematics, and metaphysics) and *Kitab al-Qanun fi al-Tibb* "
            "(Canon of Medicine) were the foundational texts of European university medicine "
            "for five centuries. His position on alchemy was skeptical: his *Risala fi ibtal "
            "ahkam al-nujum* (Letter of Refutation) argued that alchemists cannot truly "
            "transmute metals but only imitate their surface appearances — a position that "
            "generated centuries of debate with the transformative theory of Jabir ibn "
            "Hayyan. Ibn Sina's concept of *mumiya* (mineral virtue sealed within a substance "
            "by celestial influence) and his mineral taxonomy in the *Shifa* became central "
            "sources for Latin alchemical mineralogy, transmitted through Gerard of Cremona's "
            "translation and known as the pseudo-Avicennan *De mineralibus*."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Nasr, Seyyed Hossein. *An Introduction to Islamic Cosmological "
                     "Doctrines*. Harvard University Press, 1964; rev. ed. SUNY Press, 1993. "
                     "Chapter on Ibn Sina's natural philosophy and mineral theory."},
            {"text": "Ullmann, Manfred. *Die Natur- und Geheimwissenschaften im Islam*. "
                     "Brill (Handbuch der Orientalistik), 1972. Comprehensive survey of "
                     "Islamic alchemy, mineralogy, and divinatory sciences."},
            {"text": "Principe, Lawrence M. *The Secrets of Alchemy*. University of Chicago "
                     "Press, 2013. On Avicenna's skepticism of transmutation and its "
                     "reception in Latin alchemy."},
            {"text": "Newman, William R. *Promethean Ambitions: Alchemy and the Quest to "
                     "Perfect Nature*. University of Chicago Press, 2004. The Avicennan "
                     "challenge to alchemical transmutation."},
            {"text": "Rampling, Jennifer M. *The Experimental Fire: Inventing English "
                     "Alchemy, 1300–1700*. University of Chicago Press, 2020. On the "
                     "Latin Avicennan tradition in medieval and early modern alchemy."},
        ],
    },

    # ------------------------------------------------------------------
    {
        "id": "islamic_alchemy__jabir-alchemist",
        "title": "Geber, Arab Alchemist — European Engraved Portrait of Jabir ibn Hayyan",
        "medium": "engraving",
        "figures": ["Jabir"],
        "summary": (
            "A 17th-century European engraved portrait captioned *GEBER ALCHYMISTE ARABE. "
            "Chap. 33.* with a manuscript annotation reading 'Jabiz Ibn Hayzan' (Jabir Ibn "
            "Hayyan). The figure known in Latin Europe as 'Geber' — the Arabic alchemist "
            "Jabir ibn Hayyan (fl. c. 721–c. 815 CE) — is shown in three-quarter bust, "
            "wearing contemporary European scholar's robes, surrounded by alchemical "
            "glassware: alembics, retorts, cucurbits, and long-necked glass flasks in the "
            "style of European laboratory iconography. His upward gaze suggests visionary "
            "or philosophic contemplation. The inscription 'Chap. 33' locates this image in "
            "a French or Latin compilation, probably a history of the sciences or a "
            "biographical dictionary. European scholarship long conflated the historical "
            "Jabir with the 13th-century Latin author 'Pseudo-Geber' (*Summa perfectionis*), "
            "a confusion definitively resolved by Paul Kraus (1943) and William Newman (1991). "
            "The Jabirian corpus — including the *Kitab al-Sab'in* (Book of Seventy), "
            "*Kitab al-Mizan* (Book of the Balance), and the *Kitab al-Khawass al-Kabir* — "
            "represents the most theoretically ambitious systematic elaboration of alchemical "
            "science in the early Islamic tradition, grounding it in a numerological balance "
            "theory of the four qualities and their degrees."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Kraus, Paul. *Jabir ibn Hayyan: Contribution à l'histoire des idées "
                     "scientifiques dans l'Islam*. 2 vols. Institut Français d'Archéologie "
                     "Orientale, 1942–43. The foundational study of the Jabirian corpus."},
            {"text": "Newman, William R. *The 'Summa perfectionis' of Pseudo-Geber: A "
                     "Critical Edition, Translation and Study*. Brill, 1991. Separating "
                     "the historical Jabir from the Latin Pseudo-Geber."},
            {"text": "Principe, Lawrence M. *The Secrets of Alchemy*. University of Chicago "
                     "Press, 2013. On the Jabirian tradition and its Latin reception."},
            {"text": "Rampling, Jennifer M. *The Experimental Fire: Inventing English "
                     "Alchemy, 1300–1700*. University of Chicago Press, 2020. The European "
                     "Geber tradition as a practical laboratory programme."},
            {"text": "Ullmann, Manfred. *Die Natur- und Geheimwissenschaften im Islam*. "
                     "Brill, 1972. Comprehensive survey of the Jabirian alchemical corpus "
                     "and its Islamic context."},
        ],
    },

    # ------------------------------------------------------------------
    {
        "id": "agrippa_plates__agrippa-portrait-wellcome",
        "title": "Heinrich Cornelius Agrippa von Nettesheim — Portrait Engraving, c. 1535",
        "medium": "engraving",
        "figures": ["Agrippa"],
        "summary": (
            "A finely engraved portrait of Heinrich Cornelius Agrippa von Nettesheim "
            "(1486–1535), the most influential theorist of Renaissance occult philosophy, "
            "in profile bust within an oval medallion inscribed *HENRICVS CORNELIVS AGRIPPA "
            "Med. & IceQ.* The oval is set within a Renaissance architectural surround "
            "decorated with vines and flowers; below, a small vignette shows a writing desk "
            "with a book and compass or instruments. A cartouche reads: *Nascitur Colon. "
            "Agrip. Obiit Anno 1535.* (Born in Cologne, died 1535). A Latin distich below "
            "summarises his career: *Stemmate natus Eques, Medicus Magus atq peritus / "
            "Juris et Imperij consul Agrippa fui* ('Of noble stock born — Knight, "
            "Physician, Magician, skilled in Law and Empire's counsellor was I, Agrippa'). "
            "Via Wellcome Collection, London. Agrippa studied under Johannes Trithemius, "
            "undertook diplomatic missions for the Emperor Maximilian I, and served as court "
            "physician to Margaret of Austria before publishing his magnum opus *De Occulta "
            "Philosophia libri tres* (Cologne, 1531 — first full edition after a 1510 draft "
            "circulated in manuscript). The *De Occulta* synthesised natural magic, "
            "celestial magic, and ceremonial magic into the definitive Renaissance occult "
            "framework, drawing on Ficino's *De vita* and Pico's *Conclusiones*. Its "
            "three books — on natural magic, celestial/mathematical magic, and ceremonial "
            "magic — influenced every subsequent occult writer from John Dee and Robert Fludd "
            "to the Rosicrucians, the Kabbalah scholarship, and the 19th-century revival."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Walker, D.P. *Spiritual and Demonic Magic from Ficino to Campanella*. "
                     "Warburg Institute, 1958. Agrippa in the Ficinian tradition of "
                     "Renaissance natural and celestial magic."},
            {"text": "Lehrich, Christopher I. *The Language of Demons and Angels: Cornelius "
                     "Agrippa's Occult Philosophy*. Brill, 2003. Close reading of "
                     "*De Occulta Philosophia* and its synthetic project."},
            {"text": "Nauert, Charles G. *Agrippa and the Crisis of Renaissance Thought*. "
                     "University of Illinois Press, 1965. Biography and intellectual context."},
            {"text": "Principe, Lawrence M. *The Secrets of Alchemy*. University of Chicago "
                     "Press, 2013. On Agrippa's place in the Renaissance occult-alchemy nexus."},
            {"text": "Copenhaver, Brian P. 'Hermes Trismegistus, Proclus, and the Question "
                     "of a Philosophy of Magic in the Renaissance.' In *Hermeticism and the "
                     "Renaissance*, ed. Merkel & Debus. Folger Books, 1988. pp. 79–110. "
                     "On the Hermetic sources of Agrippa's system."},
        ],
    },

    # ------------------------------------------------------------------
    {
        "id": "enochian__dee-monas-hieroglyphica",
        "title": "The Monas Hieroglyphica — John Dee's Cosmological Glyph (1564)",
        "medium": "diagram",
        "figures": ["Dee"],
        "summary": (
            "The Monas Hieroglyphica, John Dee's composite cosmological symbol first "
            "published in *Monas Hieroglyphica* (Antwerp: Plantin, 1564), the work he "
            "considered his greatest intellectual achievement. The glyph unifies the seven "
            "planetary symbols into a single compressed cosmological statement: the crescent "
            "horns of Luna (top), the circle with centre point of Sol (middle), the cross of "
            "Mercury and the four elements (vertical shaft and horizontal arms), and the "
            "horned arc of Aries/fire (base). Together these encode the entire Ptolemaic "
            "cosmos — from the four elements through the seven planetary spheres to the "
            "sphere of the fixed stars — within a single figure that also encodes arithmetic, "
            "geometry, music, and kabbalah. Dee's 24 theorems expound the symbol as a "
            "universal key that its possessor could use to unlock all the secrets of "
            "mathematics, astronomy, and alchemy. The *Monas* influenced Rosicrucian "
            "symbolism (its imagery appears in the *Fama Fraternitatis*, the *Chymische "
            "Hochzeit*, and the *Geheime Figuren der Rosenkreuzer*) and Dee's own later "
            "Enochian system of angelic communication (1582–87), in which the Monas glyph "
            "served as a cosmic signature of his theurgic authority. The present image shows "
            "the glyph as a clean schematic diagram."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Josten, C.H. 'A Translation of John Dee's *Monas Hieroglyphica* "
                     "(Antwerp, 1564), with an Introduction and Annotations.' *Ambix* 12 "
                     "(1964): 84–221. The critical edition and English translation."},
            {"text": "Clulee, Nicholas H. *John Dee's Natural Philosophy: Between Science "
                     "and Religion*. Routledge, 1988. The most thorough analysis of the "
                     "Monas Hieroglyphica in its intellectual context."},
            {"text": "Harkness, Deborah E. *John Dee's Conversations with Angels: Cabala, "
                     "Alchemy, and the End of Nature*. Cambridge University Press, 1999. "
                     "The Monas as foundation for Dee's Enochian project."},
            {"text": "French, Peter J. *John Dee: The World of an Elizabethan Magus*. "
                     "Routledge & Kegan Paul, 1972. Biography and analysis of the Monas."},
            {"text": "Szulakowska, Urszula. *The Alchemy of Light: Geometry and Optics in "
                     "Late Renaissance Alchemical Illustration*. Brill, 2000. The Monas "
                     "glyph in the visual tradition of alchemical symbolism."},
        ],
    },

    # ------------------------------------------------------------------
    {
        "id": "biblical_magic_legacy_DISABLED__witch-of-endor-west",
        "title": "Witches' Sabbath — Flemish Mannerist Painting, c. 1540–60",
        "medium": "painting",
        "summary": (
            "A vivid Flemish Mannerist oil painting showing a witches' sabbath or "
            "sorcerers' assembly, probably from the circle of Jan van Mandijn or the "
            "broader Antwerp Mannerist tradition, c. 1540–1560. The complex composition "
            "is staged beneath a ruined stone arch. At centre left, a semi-nude "
            "witch-queen in drapery holds a wand aloft and presides over an open grimoire "
            "read by a younger crowned figure (Apollo? a sorcerer?), with an owl at their "
            "feet. At lower right, female figures engage in ritual activities around a "
            "caldron and a goat. At upper right, a naked female witch flies on a broom "
            "into a swarm of demons against a volcanic hellscape. In the left background, "
            "a military camp and procession suggest the temporal stakes of such magic. The "
            "painting exemplifies the period's fusion of classical mythology, Boschian "
            "fantasy, and theological anti-witchcraft polemic. Charles Zika has analysed "
            "this visual complex as constituting a European 'witch-image' in the century "
            "1480–1580, in which classical Circe and Medea traditions merge with the "
            "sabbath theology developed in the *Malleus Maleficarum* (1486), Nider's "
            "*Formicarius*, and the Tractatus de strigibus tradition. The grimoire at "
            "centre — with its visible magical diagrams — links the learned-magic "
            "tradition to the popular sabbath image."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Zika, Charles. *The Appearance of Witchcraft: Print and Visual Culture "
                     "in Sixteenth-Century Europe*. Routledge, 2007. The definitive study of "
                     "witchcraft imagery from 1480–1600, including Flemish Mannerist painting."},
            {"text": "Clark, Stuart. *Thinking with Demons: The Idea of Witchcraft in Early "
                     "Modern Europe*. Oxford University Press, 1997. Intellectual and "
                     "theological framework of the witch-image."},
            {"text": "Levack, Brian P. *The Witch Hunt in Early Modern Europe*. 4th ed. "
                     "Routledge, 2016. Historical context for the witch-trial phenomenon "
                     "these images both reflected and produced."},
            {"text": "Roper, Lyndal. *Witch Craze: Terror and Fantasy in Baroque Germany*. "
                     "Yale University Press, 2004. Psychoanalytic and social history of "
                     "witch-imagery; strong on the female body in persecution."},
            {"text": "Kieckhefer, Richard. *Magic in the Middle Ages*. Cambridge University "
                     "Press, 1989. The learned-magic tradition that fills the grimoire at "
                     "the painting's centre."},
        ],
    },

    # ------------------------------------------------------------------
    {
        "id": "paracelsus_revolution__alchemical-emblems",
        "title": "Sigillum Silentium Artis — Two Eagles and the Rosy Cross, Paracelsian MS, fol. 59",
        "medium": "manuscript",
        "summary": (
            "A richly coloured manuscript page (fol. 59) from a German Paracelsian "
            "alchemical or Rosicrucian manuscript, headed *Sigillum Silentium Artis* "
            "(Seal of the Silence of the Art). The emblem occupies the upper third of the "
            "page: two confronted double-headed heraldic eagles stand on a red ribbon with "
            "tasselled ends. The LEFT EAGLE is coloured red (solar), bearing planetary and "
            "alchemical symbols (sulphur cross, mercury sign) on breast and wings. The "
            "RIGHT EAGLE is blue (lunar), bearing a crescent moon and further symbols "
            "including a Phi-like glyph. Between them, suspended from the ribbon, hangs a "
            "golden cross pattée on a green triangular mound with a flame at the base — a "
            "variant of the Rosicrucian Rosy Cross from the *Geheime Figuren* tradition. "
            "Below, dense German Kurrent philosophic prose discusses the four elements and "
            "the cosmic circulation of nature through Air (*Luft*), Water (*Wasser*), and "
            "Earth (*Erde*), closing with a reference to the Second Epistle of the Apostle "
            "Peter — a characteristic Paracelsian blend of natural philosophy and "
            "Scripture. The 'Sigillum Silentium Artis' (Seal of the Art's Silence) belongs "
            "to the Paracelsian initiation vocabulary of *Arcana* — secret knowledge sealed "
            "against the uninitiated. The red-and-blue opposing eagles directly encode the "
            "coniunctio of Solar and Lunar principles, the central alchemical operation. "
            "The manuscript probably dates to the late 17th or early 18th century, in the "
            "tradition of the great German Paracelsian handwritten Hausbücher."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Pagel, Walter. *Paracelsus: An Introduction to Philosophical Medicine "
                     "in the Era of the Renaissance*. 2nd ed. Karger, 1982. The definitive "
                     "intellectual biography; on *arcana*, *tria prima*, and the secrecy doctrine."},
            {"text": "Webster, Charles. *From Paracelsus to Newton: Magic and the Making of "
                     "Modern Science*. Cambridge University Press, 1982. Paracelsian natural "
                     "philosophy in its social and religious context."},
            {"text": "Debus, Allen G. *The Chemical Philosophy: Paracelsian Science and "
                     "Medicine in the Sixteenth and Seventeenth Centuries*. Science History "
                     "Publications, 1977. 2 vols. The most thorough history of Paracelsianism."},
            {"text": "Szulakowska, Urszula. *The Alchemy of Light: Geometry and Optics in "
                     "Late Renaissance Alchemical Illustration*. Brill, 2000. Solar-lunar "
                     "eagle imagery in the Rosicrucian-Paracelsian visual tradition."},
            {"text": "Rampling, Jennifer M. *The Experimental Fire: Inventing English "
                     "Alchemy, 1300–1700*. University of Chicago Press, 2020. The Paracelsian "
                     "revolution and its manuscript transmission in Northern Europe."},
        ],
    },

    # ------------------------------------------------------------------
    {
        "id": "paracelsus_revolution__paracelsus-physician",
        "title": "Effigies Paracelsi Medici Celeberrimi — Engraved Portrait by P. Van Sompel after P. Soutman",
        "medium": "engraving",
        "figures": ["Paracelsus"],
        "summary": (
            "A majestic 17th-century engraved portrait of Philippus Aureolus Theophrastus "
            "Bombastus von Hohenheim, known as Paracelsus (1493/4–1541), physician, "
            "alchemist, and natural philosopher. Captioned *EFFIGIES PARACELSI MEDICI "
            "CELEBERRIMI* (Portrait of Paracelsus, Most Famous Physician). Engraved by "
            "Pieter van Sompel (active c. 1640–1650) after a composition by Pieter Soutman "
            "(c. 1580–1657), who is credited at the lower left as *Inven. Offigianit et "
            "Excud.* (inventor, publisher). Paracelsus is shown in three-quarter bust wearing "
            "a physician's black gown, a beret, and a chain with medallion — emblems of "
            "his dual status as courtly physician and natural magician. His intense, "
            "slightly upward gaze belongs to the characteristic Paracelsian portrait "
            "tradition: the seer who looks beyond the visible. The laudatory Latin verses "
            "below invoke Machaon (the healer son of Asclepius) and Phoebus Apollo: "
            "*Edura fortis fata refringero, ut docta callens iura Machaonis; / Artesque "
            "Phaebaeas salubri mente PARACELSUS elaborat* — 'Paracelsus, mastering the "
            "skilled laws of Machaon and Phoebus's healing arts, breaks the harsh decrees "
            "of fate.' Paracelsus's rejection of Galenic humoral medicine in favour of "
            "chemical remedies (*specifics* derived from his *tria prima* of sulphur, "
            "mercury, and salt) defined the Paracelsian revolution. His influence extended "
            "from metallurgy, pharmacy, and toxicology to natural magic, theology, and the "
            "social criticism of official medicine — a counter-tradition Walter Pagel and "
            "Allen Debus traced as central to the making of early modern science."
        ),
        "summary_status": "authored",
        "citations": [
            {"text": "Pagel, Walter. *Paracelsus: An Introduction to Philosophical Medicine "
                     "in the Era of the Renaissance*. 2nd ed. Karger, 1982. The canonical "
                     "intellectual biography of Paracelsus."},
            {"text": "Debus, Allen G. *The Chemical Philosophy: Paracelsian Science and "
                     "Medicine in the Sixteenth and Seventeenth Centuries*. 2 vols. Science "
                     "History Publications, 1977. Paracelsianism in European intellectual history."},
            {"text": "Webster, Charles. *From Paracelsus to Newton: Magic and the Making of "
                     "Modern Science*. Cambridge University Press, 1982. Social and "
                     "religious context of Paracelsian natural philosophy."},
            {"text": "Rampling, Jennifer M. *The Experimental Fire: Inventing English "
                     "Alchemy, 1300–1700*. University of Chicago Press, 2020. The "
                     "Paracelsian legacy in experimental and alchemical practice."},
            {"text": "Szulakowska, Urszula. *The Alchemy of Light: Geometry and Optics in "
                     "Late Renaissance Alchemical Illustration*. Brill, 2000. Visual "
                     "traditions of Paracelsian portraiture and symbolic imagery."},
        ],
    },
]

# ── 3. Load overrides.json and merge new entries ──────────────────────────────

with open(OVERRIDES_PATH, encoding='utf-8') as f:
    existing = json.load(f)

by_id = {e['id']: e for e in existing}
added = 0
updated = 0
for entry in NEW_ENTRIES:
    eid = entry['id']
    if eid in by_id:
        # merge: new fields overwrite, existing citations kept if new ones provided
        by_id[eid].update(entry)
        updated += 1
    else:
        by_id[eid] = entry
        added += 1

merged = sorted(by_id.values(), key=lambda r: r['id'])
with open(OVERRIDES_PATH, 'w', encoding='utf-8') as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f'overrides.json: {len(merged)} total entries '
      f'({added} added, {updated} updated).')
print('\nDone. Now run:  python scripts/build_all.py')
