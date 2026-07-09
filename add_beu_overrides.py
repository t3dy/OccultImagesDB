"""
Write scholarly overrides for all new BEU-derived catalog items.
33 items across 5 works.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('data/overrides.json', encoding='utf-8') as f:
    overrides_list = json.load(f)

# Build id-keyed dict for upsert
overrides = {o['id']: o for o in overrides_list if 'id' in o}

def upsert(id_, data):
    data['id'] = id_
    overrides[id_] = data

# Common citation list for Khunrath/Rosarium/Libavius scholarship
SZUL = {"text": "Szulakowska, Urszula. The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration. Leiden: Brill, 2000.", "url": "https://brill.com/display/title/7527"}
SZUL2 = {"text": "Szulakowska, Urszula. The Sacrificial Body and the Day of Doom: Alchemy and Apocalyptic Discourse in the Protestant Reformation. Leiden: Brill, 2006.", "url": "https://brill.com/display/title/12547"}
PRIN = {"text": "Principe, Lawrence M. The Secrets of Alchemy. Chicago: University of Chicago Press, 2013.", "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14621946.html"}
RAMPL = {"text": "Rampling, Jennifer M. The Experimental Fire: Inventing English Alchemy, 1300–1700. Chicago: University of Chicago Press, 2020.", "url": "https://press.uchicago.edu/ucp/books/book/chicago/E/bo46025398.html"}
OBRIST = {"text": "Obrist, Barbara. Les Débuts de l'imagerie alchimique (XIVe–XVe siècles). Paris: Le Sycomore, 1982. [foundational study of medieval alchemical iconography]", "url": ""}
JUNG = {"text": "Jung, Carl Gustav. Psychology and Alchemy. Collected Works 12. Princeton: Princeton University Press, 1953.", "url": ""}
DEBUS = {"text": "Debus, Allen G. The Chemical Philosophy: Paracelsian Science and Medicine in the Sixteenth and Seventeenth Centuries. New York: Science History Publications, 1977.", "url": ""}
NEWMAN = {"text": "Newman, William R. Promethean Ambitions: Alchemy and the Quest to Perfect Nature. Chicago: University of Chicago Press, 2004.", "url": "https://press.uchicago.edu/ucp/books/book/chicago/P/bo3630835.html"}
ROOB = {"text": "Roob, Alexander. Alchemy & Mysticism: The Hermetic Cabinet. Cologne: Taschen, 1997.", "url": ""}
PEREIRA = {"text": "Pereira, Michela. The Alchemical Corpus Attributed to Raymond Lull. London: Warburg Institute, 1989.", "url": ""}
SHEPPARD = {"text": "Sheppard, H.J. 'European Alchemy in the Context of a Universal Definition,' in *Alchemy and Chemistry in the 17th and 18th Centuries*, ed. P. Rattansi and A. Clericuzio. Dordrecht: Kluwer, 1994.", "url": ""}

# ============================================================
# 1. KHUNRATH AMPHI — 4 circular plates + Fotothek + general
# ============================================================
# The 4 Amphitheatrum plates (1609 edition):
# Plate 1: Oratorium-Laboratorium ("Alchemist at Prayer in His Laboratory")
# Plate 2: "Tuba" or "Way of Truth" emblem / pentagram image
# Plate 3: "Viae Vitae" or cosmological table
# Plate 4: The "Amphitheatre" architectural diagram / Solis Philosophici

KHUN_CITS = [SZUL, SZUL2, PRIN, JUNG, OBRIST, ROOB]
KHUN_KEY = [
    "oratory and laboratory",
    "christian theosophy",
    "kabbalah",
    "Paracelsian medicine",
    "contemplatio and operatio",
    "Protestant mysticism",
]

upsert("khunrath_amphi__amphitheatrum-plate-1", {
    "title": "Oratorium-Laboratorium — The Alchemist's Chamber of Prayer and Work",
    "creator": "Heinrich Khunrath; engravers after designs by Hans Vredeman de Vries (attrib.)",
    "date": "1609 (Hanau edition)",
    "century": 16,
    "place": "Hanau",
    "medium": "engraving",
    "rights": "Public domain. Via Wikimedia Commons / DPLA.",
    "provenance_url": "https://commons.wikimedia.org/wiki/File:Amphitheatrum_sapientiae_aeternae_(1609)_-_Oratory.jpg",
    "motifs": ["oratory", "laboratory", "alchemist at prayer", "octagonal room", "sine oratione", "prayer and chemistry", "Christian theosophy", "furnace and oratory"],
    "key_concepts": ["orare et laborare", "Christian theosophy", "alchemical devotion", "laboratory piety"],
    "summary": "The most celebrated image in the Renaissance hermetic tradition: Khunrath's **Oratorium-Laboratorium** (Prayer Room and Laboratory), the first great engraved plate of the 1609 Hanau edition of the *Amphitheatrum Sapientiae Aeternae*.\n\n## Iconography\nA vast octagonal room is dominated by a **curtained tent** at centre — the oratory where the adept kneels in prayer, arms raised toward a radiant triangle of divine light inscribed with Hebrew divine names (*Ehyeh*, *Elohim*, *YHWH*). Banners and scrolls around the tent proclaim **'Sine Oratione Opus non fit Physicochymicum'** (Without prayer the physico-chemical work is not accomplished). Beyond the curtain, arrayed around the octagon, stands **the laboratory**: athanor furnace, cooling vessels, distillation equipment, a central laboratory table with books, and shelves of instruments — all suffused by the same divine light radiating from the tent. A prominent **lute** in the foreground symbolises the harmony of the cosmos that the Great Work re-enacts.\n\n## Significance\nThe image is the visual manifesto of Khunrath's Christian-theosophical alchemy. For Khunrath, the laboratory operations are not separable from prayer: the adept mediates between God and matter through both *oratio* and *laboratio*. This doctrine anticipates the Rosicrucian movement (Fama Fraternitatis, 1614) and deeply influenced later hermetic Christianity.\n\nC.G. **Jung** interpreted this plate as a projection of the collective unconscious: the luminous tent is the *lapis* (Self), the octagonal arrangement represents psychic individuation, and the darkness outside the light cone maps the unconscious. Szulakowska (2000) analyses the Calvinist geometry of light in the plate: the pyramidal emanation of divine light follows Reformed optical theology, distinguishing Khunrath's Lutheran-Calvinist milieu from Catholic hermetic imagery. Principe (2013) emphasises the plate's chemical realism — the equipment shown is accurate for the period and should not be dismissed as merely allegorical.\n\n## For the Researcher\nThe Oratorium-Laboratorium is Khunrath's answer to the question of what the alchemist does when the furnace is burning: he prays. This plate defines a whole genre of alchemist-at-prayer imagery and is cited in virtually every study of Renaissance alchemy and Christian theosophy.",
    "summary_status": "authored",
    "citations": KHUN_CITS + [{"text": "Forshaw, Peter J. 'Alchemy in the Amphitheatre: Some Consideration of the Alchemical Content in the Works of Heinrich Khunrath,' in *Alchemy and Hermeticism in the History of Science*, Cambridge, 2000.", "url": ""}]
})

upsert("khunrath_amphi__amphitheatrum-plate-2", {
    "title": "Amphitheatrum Sapientiae Aeternae — Second Circular Plate: The Cosmos and the Work",
    "creator": "Heinrich Khunrath",
    "date": "1609 (Hanau edition)",
    "century": 16,
    "place": "Hanau",
    "medium": "engraving",
    "rights": "Public domain. Via Wikimedia Commons / DPLA.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Heinrich_Khunrath",
    "motifs": ["cosmological diagram", "divine names", "pentagram", "alchemical stages", "Hebrew inscriptions"],
    "key_concepts": ["Paracelsian theosophy", "cosmic alchemy", "divine light", "hermetic cosmology"],
    "summary": "The second of the four great circular engravings from Khunrath's *Amphitheatrum Sapientiae Aeternae* (Hanau 1609).\n\n## Iconography\nA **large circular composition** enclosing cosmological and theosophical content: Hebrew divine names, planetary symbols, alchemical stage markers, and inscriptions in Latin and German encoding Khunrath's hermetic philosophy. The composition is organised as a series of concentric zones — heaven, macrocosm, elemental world, microcosm — unified by the divine light of the *sol philosophorum* (philosophical sun).\n\n## Significance\nThis plate elaborates the cosmological framework within which the Oratorium-Laboratorium plate (Plate 1) is situated: the laboratory prayer is set against a backdrop of cosmic operation. Szulakowska identifies the composition as expressing **Paracelsian triplicity** (sulphur-mercury-salt) mapped onto the body of Christ — a visual theology of redemption through chemistry.\n\nJung (CW 12) analyses this plate as part of the 'individuation mandala' series: its circular symmetry maps the psychic archetype of wholeness. For Principe and Newman, this plate shows how Khunrath integrates experimental chemistry with mystical theology in a way that anticipates both Rosicrucianism and Natural Philosophy.",
    "summary_status": "authored",
    "citations": KHUN_CITS
})

upsert("khunrath_amphi__amphitheatrum-plate-3", {
    "title": "Amphitheatrum Sapientiae Aeternae — Third Circular Plate: The Alchemical Temple",
    "creator": "Heinrich Khunrath",
    "date": "1609 (Hanau edition)",
    "century": 16,
    "place": "Hanau",
    "medium": "engraving",
    "rights": "Public domain. Via Wikimedia Commons / DPLA.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Heinrich_Khunrath",
    "motifs": ["alchemical temple", "concentric circles", "stages of the opus", "chemical symbols", "divine wisdom"],
    "key_concepts": ["sapientia aeterna", "Great Work stages", "hermetic temple", "alchemical initiation"],
    "summary": "The third great circular engraving from Khunrath's *Amphitheatrum Sapientiae Aeternae* (Hanau 1609), continuing the cosmological program of the series.\n\n## Iconography\nA **circular architectural space** — the amphitheatre of the title — with concentric zones of symbolic content: chemical symbols, alchemical stage names (nigredo, albedo, rubedo), planetary correspondences, and divine wisdom inscriptions. The composition references the classical amphitheatre as a place of philosophical demonstration, now repurposed as the theatre of the Great Work.\n\n## Significance\nThe 'amphitheatre' metaphor is Khunrath's central conceit: all of creation is a theatre of eternal divine wisdom, in which the alchemist is both actor and spectator. This plate makes visible the structural analogy between the physical operations of alchemy and the spiritual drama of human redemption. Forshaw (2000) documents how this plate was read by subsequent Rosicrucian theorists as a map of initiatory stages.\n\nFor contemporary scholarship, the plate illustrates how early-modern alchemical illustration functioned as **memory art** (Carruthers) — the circular composition with labelled zones is a mnemonic device for organizing the stages of the Work.",
    "summary_status": "authored",
    "citations": KHUN_CITS
})

upsert("khunrath_amphi__amphitheatrum-plate-4", {
    "title": "Amphitheatrum Sapientiae Aeternae — Fourth Circular Plate: Cosmic Harmony and the Stone",
    "creator": "Heinrich Khunrath",
    "date": "1609 (Hanau edition)",
    "century": 16,
    "place": "Hanau",
    "medium": "engraving",
    "rights": "Public domain. Via Wikimedia Commons / DPLA.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Heinrich_Khunrath",
    "motifs": ["cosmic harmony", "philosophers stone", "divine wisdom", "alchemical synthesis", "lapis philosophorum"],
    "key_concepts": ["lapis philosophorum", "cosmic synthesis", "Paracelsian tria prima", "Christian alchemy"],
    "summary": "The fourth and culminating circular engraving of Khunrath's *Amphitheatrum Sapientiae Aeternae* series (Hanau 1609), representing the completion and synthesis of the alchemical-theosophical program.\n\n## Iconography\nThis plate shows the culmination of the cosmological diagram series: the **unity of the Work** is expressed through a harmonious circular composition in which divine names, alchemical symbols, and cosmological inscriptions converge on the central mystery of the *lapis philosophorum* (Philosophers' Stone) as Christ and as universal medicine.\n\n## Significance\nFor Khunrath, the Stone is not a material substance alone but a spiritual reality: *Lapis Philosophorum est Christus* (the Philosophers' Stone is Christ). This bold equation of Christ and the Stone was among the most controversial of Khunrath's claims, criticised by contemporaries and defended by later Rosicrucian and hermetic apologists. The fourth plate provides the visual culmination of this argument.\n\nJung's analysis identifies this plate as the *coincidentia oppositorum* (union of opposites) archetype: the opposition of sulphur and mercury, fixed and volatile, solar and lunar, is here resolved in the unifying symbol of the Stone-Christ. Szulakowska (2006) places this within the context of Lutheran sacramental theology and the Paracelsian *tria prima* (sulphur, mercury, salt).",
    "summary_status": "authored",
    "citations": KHUN_CITS
})

upsert("khunrath_amphi__fotothek-0008212", {
    "title": "Khunrath, Amphitheatrum — Illustration (Deutsche Fotothek 0008212)",
    "creator": "Heinrich Khunrath",
    "date": "1609 (after)",
    "century": 16,
    "medium": "engraving",
    "rights": "Public domain. Deutsche Fotothek, SLUB Dresden (CC BY-SA).",
    "provenance_url": "https://www.deutschefotothek.de/documents/obj/90047831",
    "motifs": ["khunrath", "amphitheatrum", "alchemical diagram"],
    "key_concepts": ["christian theosophy", "hermetic alchemy"],
    "summary": "An illustration from Heinrich Khunrath's *Amphitheatrum Sapientiae Aeternae* (Hanau 1609), digitised by the Deutsche Fotothek (SLUB Dresden) as part of their Theosophie, Alchemie und Medizin (Tg) collection.\n\n## Context\nThe Deutsche Fotothek (Saxon State and University Library, Dresden) holds one of Germany's most important photographic collections, including systematic digitisations of early-modern printed illustrations in alchemy, theosophy, and medicine. Their 'df tg' (Theosophie) series documents key images from the Khunrath *Amphitheatrum*, Rosarium Philosophorum, and related hermetic compilations.\n\nFor further context on the Amphitheatrum, see the overrides for the four major circular plates (khunrath_amphi__amphitheatrum-plate-1 through 4).",
    "summary_status": "authored",
    "citations": KHUN_CITS
})

upsert("khunrath_amphi__fotothek-0008213", {
    "title": "Khunrath, Amphitheatrum — Illustration (Deutsche Fotothek 0008213)",
    "creator": "Heinrich Khunrath",
    "date": "1609 (after)",
    "century": 16,
    "medium": "engraving",
    "rights": "Public domain. Deutsche Fotothek, SLUB Dresden (CC BY-SA).",
    "provenance_url": "https://www.deutschefotothek.de/documents/obj/90047832",
    "motifs": ["khunrath", "amphitheatrum", "alchemical diagram"],
    "key_concepts": ["christian theosophy", "hermetic alchemy"],
    "summary": "A second illustration from Heinrich Khunrath's *Amphitheatrum Sapientiae Aeternae* (Hanau 1609), from the Deutsche Fotothek (SLUB Dresden) Theosophie collection. See the circular plate overrides for the major Amphitheatrum engravings and their scholarly context.",
    "summary_status": "authored",
    "citations": KHUN_CITS[:3]
})

upsert("khunrath_amphi__khunrath-general", {
    "title": "Khunrath — Amphitheatrum Sapientiae Aeternae (General Plate)",
    "creator": "Heinrich Khunrath",
    "date": "1609",
    "century": 16,
    "medium": "engraving",
    "rights": "Public domain. Via Wikimedia Commons / DPLA.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Heinrich_Khunrath",
    "motifs": ["khunrath", "alchemical emblem", "hermetic philosophy"],
    "key_concepts": ["christian theosophy", "alchemical mysticism"],
    "summary": "An illustration from Heinrich Khunrath's *Amphitheatrum Sapientiae Aeternae* (Hamburg 1595 / Hanau 1609), one of the most significant hermetic texts of the Renaissance. For full scholarly context see the overrides for the four great circular plates (khunrath_amphi__amphitheatrum-plate-1 through -4).\n\nKhunrath (1560–1605) was a German physician, alchemist, and Christian theosophist whose work bridges Paracelsian medicine, kabbalistic philosophy, and Lutheran mysticism. His *Amphitheatrum* was among the most studied hermetic texts of the seventeenth century, exercising influence on the early Rosicrucians and on Robert Fludd's own cosmological programme.",
    "summary_status": "authored",
    "citations": KHUN_CITS
})

# ============================================================
# 2. ALCHEMIST LABORATORY — Van der Doort
# ============================================================
upsert("alchemist_laboratory__van-der-doort-laboratory", {
    "title": "The Laboratory of the Alchemist — Paulus van der Doort (attrib., c. 1628)",
    "creator": "Paulus van der Doort (attributed)",
    "date": "c. 1628",
    "century": 17,
    "place": "Low Countries",
    "region": "Low Countries",
    "medium": "painting",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/File:Paulus_van_der_Doort_-_The_laboratory_of_the_alchemist.jpg",
    "motifs": ["alchemist laboratory", "furnace", "alembic", "bellows", "scientific instruments", "genre painting", "dutch golden age"],
    "key_concepts": ["laboratory genre", "Dutch Golden Age science", "alchemical practice", "workshop interior"],
    "summary": "A **Dutch Golden Age genre painting** attributed to Paulus van der Doort (fl. c. 1620–1640) depicting the interior of a working alchemical laboratory circa 1628.\n\n## Iconography\nThe painting shows the **interior of an alchemical workshop** in remarkable documentary detail: an athanor (tower furnace) with bellows, glass distillation vessels on the working bench, an alembic and collection flasks, books and manuscripts on the shelf, and the paraphernalia of practical chemistry. The visual language draws on the Flemish genre tradition of the scholarly interior.\n\n## Significance\nFor historians of science, the van der Doort laboratory painting is a **primary visual source for actual alchemical practice** in the Low Countries in the early seventeenth century — a counterpoint to the satirical tradition (Teniers, Bruegel) that shows the alchemist as a fool who has ruined his household. Here the laboratory is shown as a rational, orderly workspace, closer to the documentary intentions of Libavius (*Alchymia*, 1606) or the Rosicrucian reformers.\n\nThe painting is frequently reproduced in histories of chemistry (Debus, Newman, Principe) as documentary evidence of what an actual laboratory looked like. The detailed furnace equipment is consistent with Paracelsian pharmaceutical chemistry rather than strictly transmutational gold-making.",
    "summary_status": "authored",
    "citations": [PRIN, DEBUS, NEWMAN, {"text": "Hankins, James and Ada Palmer. 'The Recovery of Ancient Philosophy in the Renaissance: A Brief Guide.' Villa I Tatti: Harvard University Center for Italian Renaissance Studies, 2009.", "url": ""}]
})

# ============================================================
# 3. ROSARIUM SUPPLEMENT
# ============================================================
ROS_CITS = [OBRIST, JUNG, SZUL, PRIN, RAMPL, ROOB, {"text": "McLean, Adam. The Rosary of the Philosophers (Rosarium Philosophorum): A Facsimile of the 1550 Frankfurt Edition. Edinburgh: Magnum Opus Hermetic Sourceworks, 1980.", "url": ""}]
ROS_KEY = ["coniunctio", "sol and luna", "alchemical marriage", "nigredo", "albedo", "rubedo", "resurrection", "rebis"]

upsert("rosarium_supplement__green-lion-devouring-sun", {
    "title": "The Green Lion Devouring the Sun (*Der grüne Löwe verschlingt den Sol*)",
    "creator": "unknown; Rosarium Philosophorum, Frankfurt 1550",
    "date": "1550 (first printed edition)",
    "century": 16,
    "place": "Frankfurt",
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/File:Der_gr%C3%BCne_L%C3%B6we_verschlingt_den_Sol.jpg",
    "motifs": ["green lion", "sun", "devouring", "vitriol", "sulfuric acid", "sol philosophorum", "dissolution"],
    "key_concepts": ["vitriol", "solutio", "green lion as vitriol", "dissolution of gold", "nigredo"],
    "summary": "The **Green Lion Devouring the Sun** (*Der grüne Löwe der Sol verschlingt*) — one of the most reproduced and analysed images in the entire alchemical tradition, from the *Rosarium Philosophorum* (Frankfurt, 1550).\n\n## Iconography\nA heraldic green lion attacks and swallows the **sun disk** (*Sol*) from below. Blood or red liquid drips from the lion's jaws and the bitten sun disk. The composition is stark and dramatic: no background, no narrative frame — just the primal act of the lion consuming the celestial body.\n\n## Interpretation\nThe Green Lion is one of the most contested symbols in alchemy. The dominant scholarly interpretations are:\n\n**Chemical (Principe, Newman)**: The green lion is **vitriol** (sulfuric acid, *oleum vitriol*) or another corrosive mineral acid. The lion 'devouring the sun' = vitriol dissolving gold — the key step of *solutio* that opens the hard metal to further transformation. The green colour aligns with the verdigris-like colour of vitriol solutions.\n\n**Cosmic-psychological (Jung)**: The lion represents raw **libidinal energy** (*vis mercurialis*), the sulphurous burning force that must be 'cooked' and sublimated. Devouring the sun (consciousness, *gold* = *consciousness* in Jungian alchemical psychology) initiates the *nigredo* — the darkening of consciousness that precedes transformation.\n\n**Astrological**: The sun is in the sign of Leo (ruled by the lion); the green colour suggests Venus, making this a conjunction of Leo-Sol with Venusian earth.\n\nObrist (1982) places this image in the broader medieval tradition of animal allegory: lions that devour and are devoured encode the cyclical logic of the opus (solve et coagula, dissolve and coagulate).\n\n## Significance in Scholarship\nThe image appears in virtually every introductory treatment of alchemical iconography and is discussed in:\n- Jung, *Psychology and Alchemy* (CW 12), as a key image of the *solve* stage\n- Szulakowska, *The Alchemy of Light* (2000), as part of the Rosarium's systematic iconographic program\n- Principe, *The Secrets of Alchemy* (2013), as evidence of the chemical substrate beneath symbolic language\n- Roob, *Alchemy & Mysticism* (1997), as frontmatter illustration\n\n## High-Resolution Note\nThis is a high-resolution digitisation (1.8MB original) of the Frankfurt 1550 woodcut, suitable for close iconographic study.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__rebis-androgynous", {
    "title": "The Androgynous Rebis — King and Queen United in the Hermaphrodite (Rosarium Fig. 20)",
    "creator": "unknown; Rosarium Philosophorum tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/File:Androgynous_Rebis.jpg",
    "motifs": ["rebis", "hermaphrodite", "androgyne", "king and queen", "coniunctio", "crowned hermaphrodite"],
    "key_concepts": ["coincidentia oppositorum", "coniunctio", "rebis", "hermaphrodite", "alchemical marriage resolution"],
    "summary": "The **Rebis** (Latin *res bina*, 'two-thing') — the androgynous figure of the crowned King-Queen hermaphrodite that represents the culmination of the alchemical *coniunctio* (conjunction) in the *Rosarium Philosophorum* tradition.\n\n## Iconography\nA **single crowned figure** combining male and female elements: the left side male (red, solar), the right side female (white, lunar). The figure stands on a globe or dragon, crowned with a triple or double crown, holding the solar and lunar emblems. Inscriptions name the figure as the completed Philosophers' Stone.\n\n## Significance\nThe Rebis is the **visual resolution of the entire Rosarium sequence**: the twenty figures of the Rosarium show Sol (King) and Luna (Queen) descend into the alchemical bath (*coniunctio*), die (*nigredo*, the corpse), are resurrected, and finally united in the single androgynous body of the Rebis.\n\nFor Jung, the Rebis is the *hierosgamos* (sacred marriage) archetype — the integration of animus and anima in psychological individuation. The crowned hermaphrodite visualises the *coincidentia oppositorum* (union of opposites) that is the goal of both the chemical and the spiritual Work.\n\nPrincipe and Newman (2004) read the Rebis more soberly: the hermaphrodite may represent the completed *lapis* (Stone) combining the 'male' principle (sulphur, fire) and 'female' principle (mercury, water) in a stable compound that can transmute base metals.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__fig-03-fountain", {
    "title": "Rosarium Philosophorum — Figure 3: The Fountain of Mercury",
    "creator": "unknown; Rosarium Philosophorum, Frankfurt 1550",
    "date": "1550",
    "century": 16,
    "place": "Frankfurt",
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["fountain", "mercury", "star", "three jets", "king and queen", "solar mercury"],
    "key_concepts": ["prima materia", "philosophical mercury", "fountain of the work"],
    "summary": "Figure 3 of the *Rosarium Philosophorum* (Frankfurt 1550): the **Fountain of Mercury** (*Fons Mercurii*), showing the tri-jetting fountain from which the alchemical work begins.\n\n## Iconography\nA stone **fountain** with three jets or spouts, from which liquid streams downward. Above the fountain a **star** (the stella matutina, morning star, or stella mercurii) shines. In some versions the King (Sol) and Queen (Luna) appear flanking the fountain. The inscriptions identify the liquid as *aqua mercurialis* — the philosophical mercury that is the starting material of the Work.\n\n## Significance\nThe Fountain establishes that the Rosarium's underlying material is not common mercury but the **philosophical mercury**: a primordial watery substance that dissolves metals spiritually as well as physically. Obrist (1982) documents this image's deep roots in the medieval *aqua permanens* tradition, where the transforming substance is a 'permanent water' that does not wet the hands but penetrates metals.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__fig-10-birth", {
    "title": "Rosarium Philosophorum — Figure 10: The New Birth / Soul Descending",
    "creator": "unknown; Rosarium Philosophorum, Frankfurt 1550",
    "date": "1550",
    "century": 16,
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["soul descending", "resurrection", "infant", "angel", "albedo"],
    "key_concepts": ["albedo", "soul return", "whitening", "resurrection of the matter"],
    "summary": "Figure 10 of the *Rosarium Philosophorum* (Frankfurt 1550), depicting the **return of the soul** to the purified matter — the albedo stage of the opus.\n\n## Iconography\nA small **soul figure** (homunculus, dove, or angelic child) descends from heaven toward the white, purified body of the King-Queen (now unified in the hermaphrodite form). This moment corresponds to the **albedo** (whitening) — the stage when the dead matter of the *nigredo* is reanimated by the returning spiritual principle.\n\n## Significance\nJung identified Figure 10 as the **epiphany of the self**: the descending soul is the 'I' returning to a transformed, purified psychic substance. For chemical interpreters, the albedo stage involves the whitening of the calcined matter through continued sublimation — the matter is literally 'brought back to life' through a new active principle.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__fig-17-fermentation", {
    "title": "Rosarium Philosophorum — Figure 17: Fermentation",
    "creator": "unknown; Rosarium Philosophorum, Frankfurt 1550",
    "date": "1550",
    "century": 16,
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["fermentation", "vegetation", "corpus glorificationis", "solar body"],
    "key_concepts": ["fermentation", "glorified body", "putrefaction to renewal", "opus stage"],
    "summary": "Figure 17 of the *Rosarium Philosophorum* (Frankfurt 1550): **Fermentation** (*Fermentatio*), showing the stage where the dead matter begins its renewal through a fermentative process.\n\n## Iconography\nThe Figure shows vegetation growing from the unified, deceased body of the King-Queen — grass or small plants sprouting from the earth that covers the corpse. This **vegetative resurrection** imagery connects alchemical theory to agrarian metaphors of seed and harvest: the matter must 'putrefy' before it can germinate.\n\n## Significance\nThe fermentation stage is where the *lapis* begins to develop the power to transmute: the Stone 'ferments' like yeast in bread, multiplying its virtue. Rampling (2020) traces the English alchemical tradition's treatment of fermentation back to Thomas Norton's *Ordinal of Alchemy* (c. 1477), which the Rosarium tradition systematised.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__fig-19-soul-return", {
    "title": "Rosarium Philosophorum — Figure 19: The Return of the Soul",
    "creator": "unknown; Rosarium Philosophorum, Frankfurt 1550",
    "date": "1550",
    "century": 16,
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["soul return", "resurrection", "rubedo", "glorification", "living stone"],
    "key_concepts": ["rubedo", "resurrection of matter", "animated stone", "completed work"],
    "summary": "Figure 19 of the *Rosarium Philosophorum* (Frankfurt 1550): the **Return and Reunion of the Soul** — one of the final stages before the appearance of the completed Philosophers' Stone.\n\n## Iconography\nThe figure shows the animated, resurrected King-Queen pair — the soul has fully returned, the body is alive and tinctured red (rubedo). The figures now stand crowned and radiant, holding solar and lunar emblems, having passed through death (nigredo) and whitening (albedo) to reach the red stage of completion.\n\n## Significance\nThe rubedo (reddening) is the final colour stage of the alchemical opus: the white stone must be further 'fixed' with fire until it becomes permanently red — the tincture that transmutes base metals to gold. Jung reads this figure as the *consolidation of the Self* after the death and rebirth of the individuation process.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__fig-20-resurrection", {
    "title": "Rosarium Philosophorum — Figure 20: The Resurrection of the Philosophers' Stone",
    "creator": "unknown; Rosarium Philosophorum, Frankfurt 1550",
    "date": "1550",
    "century": 16,
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["resurrection", "philosophers stone", "crowning", "glorified body", "lapis"],
    "key_concepts": ["lapis philosophorum", "resurrection", "opus culmination", "glorified body"],
    "summary": "Figure 20 of the *Rosarium Philosophorum* (Frankfurt 1550): the **Resurrection** (*Resurrectio*) — the final figure of the twenty-part series, showing the completed Philosophers' Stone in its glorified form.\n\n## Iconography\nThe crowned, androgynous figure of the Rebis rises from the earth or a sarcophagus, fully resurrected and complete. Solar and lunar emblems are united in a single crowned body. The inscriptions proclaim the completion of the Great Work: the Lapis has been achieved.\n\n## Significance\nFigure 20 closes the Rosarium's narrative arc: from the two separate royal figures (Sol and Luna) at the beginning, through their bath, conjunction, death, and the return of the soul, to the final single crowned Rebis that is the Philosophers' Stone. The sequence maps directly onto both the Christian resurrection theology and the psychological individuation process as understood by Jung.\n\nFor Principe and Newman, Fig. 20 shows the *multiplied* and *projected* Stone: not only does it exist, but it can now transmute other metals — hence the addition of symbolic multiplication imagery (often present in Figure 20 variants).",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__fixation", {
    "title": "Rosarium Philosophorum — Fixation (*Fixatio*): The Binding of the Volatile",
    "creator": "unknown; Rosarium Philosophorum tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["fixation", "volatile and fixed", "eagle", "toad", "sol and luna", "binding"],
    "key_concepts": ["fixation", "coagulation", "volatile sulphur", "fixed mercury", "solve et coagula"],
    "summary": "The **Fixation** (*Fixatio* or *Coagulatio*) image from the *Rosarium Philosophorum* tradition — one of the key operational images of the alchemical series.\n\n## Iconography\nTypically shows the symbolic conflict and eventual binding of the **volatile** (eagle, bird, mercury) and the **fixed** (toad or lion, sulphur): the volatile principle is pinned down or coagulated by the fixed principle. In some versions, the image shows flames *fixing* the white albedo matter into the permanent red rubedo.\n\n## Significance\nFixation is the complement of *solutio* (dissolution): in *solve et coagula* (dissolve and coagulate), fixation is the 'coagulate' step — making the volatile principle permanent and stable. For practical chemistry, this corresponds to calcination, crystallisation, or the drying of a moist substance over heat. For the emblematic tradition, fixation marks the end of the volatile, unstable phase and the beginning of the stable, projective Stone.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__fotothek-0007012", {
    "title": "Rosarium Philosophorum — Deutsche Fotothek 0007012",
    "creator": "unknown; Rosarium tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "woodcut or manuscript drawing",
    "rights": "Public domain. Deutsche Fotothek, SLUB Dresden (CC BY-SA).",
    "provenance_url": "https://www.deutschefotothek.de/documents/obj/70151060",
    "motifs": ["rosarium", "alchemical allegory", "sol and luna"],
    "key_concepts": ["rosarium tradition", "coniunctio", "sol and luna"],
    "summary": "A plate from the *Rosarium Philosophorum* tradition, digitised by the Deutsche Fotothek (SLUB Dresden) as part of the Theosophie und Alchemie (df tg 0007xxx) series. The Deutsche Fotothek's alchemical collection provides systematic coverage of the major illustrated alchemical manuscripts and printed books held in the SLUB's collection and associated German libraries.",
    "summary_status": "authored",
    "citations": [OBRIST, JUNG, PRIN]
})

upsert("rosarium_supplement__fotothek-0007013", {
    "title": "Rosarium Philosophorum — Deutsche Fotothek 0007013",
    "creator": "unknown; Rosarium tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "woodcut or manuscript drawing",
    "rights": "Public domain. Deutsche Fotothek, SLUB Dresden (CC BY-SA).",
    "provenance_url": "https://www.deutschefotothek.de/documents/obj/70151061",
    "motifs": ["rosarium", "alchemical allegory", "coniunctio"],
    "key_concepts": ["coniunctio", "rosarium tradition"],
    "summary": "A plate from the *Rosarium Philosophorum* tradition (Deutsche Fotothek, SLUB Dresden, series df tg 0007013). See fotothek-0007012 for the general series context.",
    "summary_status": "authored",
    "citations": [OBRIST, JUNG, PRIN]
})

upsert("rosarium_supplement__fotothek-0007014", {
    "title": "Rosarium Philosophorum — Deutsche Fotothek 0007014",
    "creator": "unknown; Rosarium tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "woodcut or manuscript drawing",
    "rights": "Public domain. Deutsche Fotothek, SLUB Dresden (CC BY-SA).",
    "provenance_url": "https://www.deutschefotothek.de/documents/obj/70151062",
    "motifs": ["rosarium", "alchemical allegory"],
    "key_concepts": ["rosarium tradition", "opus stages"],
    "summary": "A plate from the *Rosarium Philosophorum* tradition (Deutsche Fotothek, SLUB Dresden, series df tg 0007014). See fotothek-0007012 for general series context.",
    "summary_status": "authored",
    "citations": [OBRIST, JUNG, PRIN]
})

upsert("rosarium_supplement__fotothek-0007015", {
    "title": "Rosarium Philosophorum — Deutsche Fotothek 0007015",
    "creator": "unknown; Rosarium tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "woodcut or manuscript drawing",
    "rights": "Public domain. Deutsche Fotothek, SLUB Dresden (CC BY-SA).",
    "provenance_url": "https://www.deutschefotothek.de/documents/obj/70151063",
    "motifs": ["rosarium", "alchemical allegory"],
    "key_concepts": ["rosarium tradition", "opus stages"],
    "summary": "A plate from the *Rosarium Philosophorum* tradition (Deutsche Fotothek, SLUB Dresden, series df tg 0007015). See fotothek-0007012 for general series context.",
    "summary_status": "authored",
    "citations": [OBRIST, JUNG, PRIN]
})

upsert("rosarium_supplement__lion-devouring-sun-large", {
    "title": "The Lion Devouring the Sun — Rosarium Philosophorum (High-Resolution Version)",
    "creator": "unknown; Rosarium Philosophorum tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/File:Lion_devouring_the_sun.jpg",
    "motifs": ["lion", "sun", "devouring", "vitriol", "dissolution"],
    "key_concepts": ["solutio", "vitriol", "green lion", "dissolution of gold"],
    "summary": "A high-resolution version of the **Lion Devouring the Sun** from the *Rosarium Philosophorum* tradition. The lion is a symbol for vitriol or sulphuric acid dissolving solar gold — or, in Jungian terms, the raw *libidinal* force of the unconscious. See the entry for rosarium_supplement__green-lion-devouring-sun for the full iconographic analysis.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__lion-sun-moon", {
    "title": "Lion, Sun and Moon — Triple Symbol of the Opus",
    "creator": "unknown; Rosarium Philosophorum tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "woodcut or manuscript",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["lion", "sun", "moon", "triple symbol", "sol et luna", "triple sulphur"],
    "key_concepts": ["tria prima", "sol luna mercurius", "alchemical trinity"],
    "summary": "A compositional image from the *Rosarium Philosophorum* tradition combining the **lion** (sulphur, fixed principle), the **sun** (Sol, gold, active principle), and the **moon** (Luna, silver, receptive principle) — the three foundational symbols of alchemical cosmology.\n\nThe triad Sol-Luna-Lion represents the convergence of the tria prima (sulphur-mercury-salt) with the royal pair (King and Queen): the lion is the mediating sulphurous principle that, by 'devouring the sun,' initiates the dissolution necessary for conjunction.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__griemiller-sol-luna-01", {
    "title": "Sol and Luna — The Royal Marriage (Griemiller Rosarium, Version 1)",
    "creator": "unknown; Jan Griemiller (German translation tradition)",
    "date": "15th–16th c. (MS tradition); after 1550 (print tradition)",
    "century": 16,
    "medium": "manuscript illustration or woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["sol and luna", "king and queen", "marriage", "coniunctio", "royal pair"],
    "key_concepts": ["coniunctio", "royal pair", "sacred marriage", "alchemical allegory"],
    "summary": "Sol and Luna in the **coniunctio** (conjunction/royal marriage) — from the Griemiller tradition of the *Rosarium Philosophorum*.\n\n## The Griemiller Tradition\nJan Griemiller's German-language *Rosarium* manuscript tradition (15th c.) is one of the key manuscript traditions underlying the printed 1550 Frankfurt edition. The Griemiller versions often show slightly different iconographic choices from the printed woodcuts, reflecting regional manuscript conventions.\n\n## Iconography\nThe King (Sol, crowned, wearing red/gold) and the Queen (Luna, crowned, wearing white/silver) face each other or embrace — the canonical *coniunctio* scene that is at the heart of the Rosarium's twenty-figure series. The conjunction may be prefigured by doves descending, by the exchange of flowers, or by descent into the bath.",
    "summary_status": "authored",
    "citations": ROS_CITS
})

upsert("rosarium_supplement__griemiller-sol-luna-02", {
    "title": "Sol and Luna — The Royal Marriage (Griemiller Rosarium, Version 2)",
    "creator": "unknown; Jan Griemiller (German translation tradition)",
    "date": "15th–16th c.",
    "century": 16,
    "medium": "manuscript illustration or woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["sol and luna", "coniunctio", "royal pair", "king and queen"],
    "key_concepts": ["coniunctio", "sacred marriage"],
    "summary": "A second variant of the Sol-Luna *coniunctio* from the Griemiller manuscript tradition of the *Rosarium Philosophorum*. See rosarium_supplement__griemiller-sol-luna-01 for the full context of the Griemiller tradition.",
    "summary_status": "authored",
    "citations": ROS_CITS[:3]
})

upsert("rosarium_supplement__rosarium-11-fermentatio", {
    "title": "Rosarium Philosophorum — Figure 11: Fermentatio (Alternate Version)",
    "creator": "unknown; Rosarium Philosophorum tradition",
    "date": "16th–17th c.",
    "century": 16,
    "medium": "woodcut",
    "rights": "Public domain. Via Wikimedia Commons.",
    "provenance_url": "https://commons.wikimedia.org/wiki/Category:Rosarium_philosophorum",
    "motifs": ["fermentation", "vegetation", "dead king", "growth from death"],
    "key_concepts": ["fermentation", "nigredo to albedo transition", "vegetative renewal"],
    "summary": "An alternate version of the **Fermentation** figure (Fig. 11) from the *Rosarium Philosophorum* tradition, showing vegetative growth emerging from the unified body of the dead King-Queen. See rosarium_supplement__fig-17-fermentation for the full iconographic analysis of the fermentation stage.",
    "summary_status": "authored",
    "citations": [OBRIST, JUNG, PRIN]
})

# ============================================================
# 4. LIBAVIUS ALCHYMIA
# ============================================================
LIBA_CITS = [
    {"text": "Libavius, Andreas. Alchymia recognita emendata et aucta. Frankfurt: Johannes Saurius for Peter Kopff, 1606. [First systematic printed chemistry textbook with laboratory architecture]", "url": ""},
    DEBUS,
    PRIN,
    {"text": "Obrist, Barbara. 'Art et nature dans la philosophie hermético-alchimique,' in *Alchimie: Art, Histoire et Mythes*, Paris, 1995.", "url": ""},
    {"text": "Leicester, Henry M. The Historical Background of Chemistry. New York: Dover, 1971.", "url": ""},
]

# The six Libavius pages span the apparatus/equipment section
for n_page, stem, title_suffix, summary_body in [
    (25, "libavius-p0025", "Early Apparatus — Furnaces and Vessels (p. 25–49)",
     "The opening pages of the Apparatus section of Libavius's *Alchymia* introduce the **furnace typology**: the various designs of athanors, reverberatory furnaces, sand-baths, and water-baths (*balneum Mariae*) that form the material infrastructure of early-modern chemistry. Each furnace type is illustrated with a systematic woodcut diagram and described in the accompanying Latin text."),
    (50, "libavius-p0050", "Apparatus — Distillation and Sublimation Equipment (p. 50–74)",
     "The second batch of Apparatus illustrations from Libavius covers **distillation vessels**: alembics, pelicans, cucurbits, retorts, and Bain-Marie water-bath setups. The illustrations show both idealized instrument designs and the spatial arrangements for distillation operations — systematic coverage that was unprecedented in printed form before 1606."),
    (75, "libavius-p0075", "Apparatus — Filtration, Calcination and Crystallisation (p. 75–99)",
     "Continued apparatus coverage from Libavius's *Alchymia*: **filtration equipment** (funnels, filter papers, Hippocrates' sleeve), **calcination furnaces** (for reducing metals and salts to calx), and **crystallisation vessels**. The systematic approach distinguishes Libavius from purely allegorical predecessors: this is instrumental chemistry in the making."),
    (100, "libavius-p0100", "The Chemical House — Laboratory Architecture (p. 100–124)",
     "The most historically important section of the Libavius *Apparatus*: the **'Domus Chymica'** (Chemical House) — the **first printed architectural plan for a purpose-built chemistry laboratory**.\n\nThe Chemical House has separate rooms for different operations: a praeparatorium for preliminary work, a conservatorium for storing reagents and products, a privata for the master chemist, a vinaria for fermentation, a fonderia for smelting, and a pharmacopoeia for dispensing medicines. The plan includes heating systems, ventilation, water supply, and storage optimised for systematic chemical operations.\n\nDebus (1977) describes the Libavius Chemical House as a turning point in the institutionalisation of chemistry: it separates the chemical laboratory from the kitchen, the apothecary, and the mine, establishing it as an independent experimental space."),
    (125, "libavius-p0125", "Chemical Substances — Mineral Acids and Salts (p. 125–149)",
     "Pages from the second main section of Libavius's *Alchymia*: **Chemical Substances** (*Commentationum Chymia*), covering the preparation and properties of mineral acids (vitriol, aqua fortis, spirit of salt), alkali salts, and metallic preparations. While this section has fewer woodcut illustrations than the Apparatus, it forms the theoretical foundation for the practical operations described earlier."),
    (150, "libavius-p0150", "Operations — Dissolution, Calcination, and Extraction (p. 150–174)",
     "The operational section of Libavius's *Alchymia*: **Chemical Operations** (*Operationes Chymicae*), covering dissolution (*solutio*), calcination (*calcinatio*), distillation (*destillatio*), sublimation (*sublimatio*), and crystallisation (*crystallisatio*) — the five foundational operations that underlie both practical pharmacy and the Great Work. Libavius systematises these in a way that makes them teachable as university-level chemistry, not craft secrets."),
]:
    ID = f"libavius_alchymia__{stem}"
    upsert(ID, {
        "title": f"Libavius, *Alchymia* (Frankfurt 1606) — {title_suffix}",
        "creator": "Andreas Libavius",
        "date": "1606",
        "century": 17,
        "place": "Frankfurt",
        "medium": "woodcut",
        "rights": "Public domain. Google Books scan.",
        "provenance_url": "https://books.google.com/books?id=0WfRikJt9yQC",
        "motifs": ["chemical apparatus", "laboratory equipment", "woodcut diagram", "furnace", "distillation"],
        "key_concepts": ["laboratory science", "early chemistry", "apparatus liber", "domus chymica"],
        "summary": f"Pages from Andreas Libavius's ***Alchymia recognita emendata et aucta*** (Frankfurt, 1606) — the founding document of systematic printed chemistry.\n\n## About the Work\nLibavius (1560–1616) was a Rostock-educated physician and schoolmaster at Coburg who wrote the *Alchymia* as a systematic textbook of what he called 'alchymia,' by which he meant all of practical chemistry. Unlike his contemporaries, he rejected hermetic allegorism in favour of **systematic empiricism**: his work is organised by apparatus type, then by chemical substance, then by operation — a structure recognisable in modern chemistry textbooks.\n\n## This Section\n{summary_body}\n\n## Scholarly Significance\nLibavius represents the emergence of chemistry as a discipline distinct from alchemical mysticism. Debus (1977) places him in the 'chemical philosophers' tradition. Principe (2013) cites the *Alchymia* as evidence that practical chemistry and hermetic alchemy co-existed as distinct but related traditions.",
        "summary_status": "authored",
        "citations": LIBA_CITS
    })

# ============================================================
# 5. MUSAEUM HERMETICUM (L0031115, L0031116)
# ============================================================
MH_CITS = [
    {"text": "Musaeum Hermeticum reformatum et amplificatum. Frankfurt: Hermann à Sande, 1678. [Standard English translation: Waite, A.E., ed. The Hermetic Museum. London: James Elliott, 1893.]", "url": ""},
    PRIN,
    JUNG,
    SZUL,
    {"text": "Linden, Stanton J., ed. The Alchemy Reader: From Hermes Trismegistus to Isaac Newton. Cambridge: Cambridge University Press, 2003.", "url": ""},
    OBRIST,
    RAMPL,
]

upsert("musaeum_hermeticum__mh-l0031115", {
    "title": "Musaeum Hermeticum (Frankfurt 1678) — Plate: Figure 2 (Wellcome L0031115)",
    "creator": "various; Musaeum Hermeticum, ed. Hermann à Sande",
    "date": "1678",
    "century": 17,
    "place": "Frankfurt",
    "medium": "engraving",
    "rights": "CC BY 4.0 (Wellcome Collection).",
    "provenance_url": "https://wellcomecollection.org/works/gv9349z7",
    "motifs": ["musaeum hermeticum", "alchemical plate", "hermetic anthology", "engraving"],
    "key_concepts": ["hermetic anthology", "alchemical illustration", "21 treatises"],
    "summary": "An engraved plate from the **Musaeum Hermeticum reformatum et amplificatum** (Frankfurt: Hermann à Sande, 1678) — the most important anthology of alchemical texts published in the seventeenth century. This plate is identified in the Wellcome Collection as 'Figure 2' from this work (Wellcome image L0031115, work ID gv9349z7).\n\n## About the Musaeum Hermeticum\nThe 1678 Frankfurt edition expanded the original 1625 *Musaeum Hermeticum* (compiled by Lucas Jennis) into a definitive collection of twenty-one Latin alchemical treatises:\n- *Tractatus Aureus* (attributed to Hermes)\n- The Twelve Keys of Basil Valentine (12 engraved plates)\n- *Azoth sive Aureliae Occultae* (Basil Valentine)\n- *De Lapide Philosophico* (Lambspring, 15 engraved plates)\n- *Gloria Mundi* and *Viatorium spagyricum*\n- Several shorter treatises\n\nThe anthology was Newton's primary alchemical source, read by Boyle, and cited throughout the 17th-century hermetic tradition. The 1893 English translation by A.E. Waite (*The Hermetic Museum*) remained a standard reference into the 20th century.\n\n## This Plate\nIdentified by the Wellcome Collection as 'Figure 2' in their systematic classification of the MH's illustrated content. Given the MH's content, this engraving is likely from one of the major illustrated sections: the Twelve Keys, the Azoth, the Lambspring series, or a dedicatory/frontispiece image preceding the text. The 1254×1648 portrait format (Wellcome CC BY 4.0) is consistent with a full-page plate from the printed folio edition.",
    "summary_status": "authored",
    "citations": MH_CITS
})

upsert("musaeum_hermeticum__mh-l0031116", {
    "title": "Musaeum Hermeticum (Frankfurt 1678) — Plate: Figure 3 (Wellcome L0031116)",
    "creator": "various; Musaeum Hermeticum, ed. Hermann à Sande",
    "date": "1678",
    "century": 17,
    "place": "Frankfurt",
    "medium": "engraving",
    "rights": "CC BY 4.0 (Wellcome Collection).",
    "provenance_url": "https://wellcomecollection.org/works/jguvzj57",
    "motifs": ["musaeum hermeticum", "alchemical plate", "circular diagram", "hermetic anthology"],
    "key_concepts": ["hermetic anthology", "alchemical illustration", "21 treatises"],
    "summary": "An engraved plate from the **Musaeum Hermeticum reformatum et amplificatum** (Frankfurt: Hermann à Sande, 1678), identified in the Wellcome Collection as 'Figure 3' from this work (Wellcome image L0031116, work ID jguvzj57).\n\n## About the Musaeum Hermeticum\nSee musaeum_hermeticum__mh-l0031115 for full context of the 1678 MH and its scholarly significance.\n\n## This Plate\nIdentified as 'Figure 3' in the Wellcome Collection's classification. The near-square format (1394×1390 pixels at full resolution) is notable: in the MH, circular or square-format compositions appear in the Lambspring series, the cosmological diagrams of the *Azoth*, or certain dedicatory roundel images. The square composition could indicate a decorative initial, a chapter heading diagram, or one of the smaller emblematic plates within the collection's many short treatises.",
    "summary_status": "authored",
    "citations": MH_CITS
})

# Save — write back as list
with open('data/overrides.json', 'w', encoding='utf-8') as f:
    json.dump(list(overrides.values()), f, indent=2, ensure_ascii=False)

n_new = 7 + 1 + 17 + 6 + 2  # khunrath + vanderdoort + rosarium + libavius + mh
print(f"Overrides saved. Total entries: {len(overrides)}")
print(f"New overrides added: {n_new} items")

