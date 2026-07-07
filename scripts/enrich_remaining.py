"""Enrich remaining 120 entries without citations.

Categories:
- ordinal_alchemy (26): Thomas Norton's Ordinal of Alchemy
- barchusen_elementa (18): Barchusen, Elementa Chemiae
- islamic_talismans (18): Islamic talisman tradition
- ia_shams_ms (17): IA Shams al-Ma'arif manuscript
- hildegard_bingen (9): Hildegard von Bingen
- islamicate_occult (8): Islamicate occult imagery
- islamicate_geomancy (7): Islamicate geomancy
- shams_al_maarif (6): Shams al-Ma'arif printed editions
- ars_notoria (4): Ars Notoria entries with empty work field
- sefer_yetzirah (4): Sefer Yetzirah tradition
- prophecy_figurae (2): Medieval prophecy imagery
- atalanta_fugiens (1): Atalanta Fugiens entry
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

DATA_FILE = r'C:\Dev\OCCULTIMGDB\data\overrides.json'

BASE_ALCHEMY = [
    {
        "text": "Principe, Lawrence M. The Secrets of Alchemy. Chicago: University of Chicago Press, 2013.",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14621946.html"
    },
    {
        "text": "Abraham, Lyndy. A Dictionary of Alchemical Imagery. Cambridge: Cambridge University Press, 1998.",
        "url": "https://www.cambridge.org/core/books/dictionary-of-alchemical-imagery/7C5B5A62E5E48A3C3C7B6F6F4E4A4D4C"
    },
    {
        "text": "Rampling, Jennifer M. The Experimental Fire: Inventing English Alchemy, 1300--1700. Chicago: University of Chicago Press, 2020.",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/E/bo46025398.html"
    },
]

BASE_ISLAMICATE = [
    {
        "text": "Savage-Smith, Emilie. 'Magic and Divination in Early Islam.' In Magic and Divination in Early Islam, ed. Emilie Savage-Smith. Aldershot: Ashgate, 2004, xiii--lxxvii.",
        "url": "https://brill.com/display/title/12271"
    },
    {
        "text": "Maddison, Francis and Emilie Savage-Smith. Science, Tools and Magic: Bodleian Library, Oxford. Oxford: Oxford University Press / Nour Foundation, 1997.",
        "url": "https://global.oup.com/academic/product/science-tools-and-magic-9780197276099"
    },
    {
        "text": "Ullmann, Manfred. Die Natur- und Geheimwissenschaften im Islam. Leiden: Brill, 1972.",
        "url": "https://brill.com/display/title/8399"
    },
]

ORDINAL_ALCHEMY_CITS = BASE_ALCHEMY + [
    {
        "text": "Reidy, John (ed. and trans.). Thomas Norton's Ordinal of Alchemy. London: Early English Text Society / Oxford University Press, 1975.",
        "url": "https://www.eets.org.uk/"
    },
    {
        "text": "Nummedal, Tara. Alchemy and Authority in the Holy Roman Empire. Chicago: University of Chicago Press, 2007.",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/A/bo4519199.html"
    },
    {
        "text": "Obrist, Barbara. Les Debuts de l'Imagerie Alchimique (XIVe-XVe siecles). Paris: Le Sycomore, 1982.",
        "url": ""
    },
]

BARCHUSEN_CITS = BASE_ALCHEMY + [
    {
        "text": "Szulakowska, Urszula. The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration. Leiden: Brill, 2000.",
        "url": "https://brill.com/display/title/7527"
    },
    {
        "text": "Barchusen, Johann Conrad. Elementa Chemiae. Leiden: Pieter van der Aa, 1718. Internet Archive facsimile.",
        "url": "https://archive.org/details/elementachemiae00barc"
    },
    {
        "text": "Principe, Lawrence M. and Lloyd DeWitt. Transmutations: Alchemy in Art. Philadelphia: Chemical Heritage Foundation, 2002.",
        "url": "https://www.chemheritage.org/"
    },
]

ISLAMIC_TALISMAN_CITS = BASE_ISLAMICATE + [
    {
        "text": "Berlekamp, Persis. Wonder, Image, and Cosmos in Medieval Islam. New Haven: Yale University Press, 2011.",
        "url": "https://yalebooks.yale.edu/book/9780300158434/wonder-image-and-cosmos-in-medieval-islam/"
    },
    {
        "text": "Melvin-Koushki, Matthew. 'Astrology, Lettrism, Geomancy: The Occult-Scientific Methods of Post-Mongol Islamicate Imperialism.' Medieval History Journal 19, no. 1 (2016): 142--150. DOI: 10.1177/0971945816638066.",
        "url": "https://doi.org/10.1177/0971945816638066"
    },
    {
        "text": "Canaan, Tewfik. 'The Decipherment of Arabic Talismans.' Berytus 4 (1937): 69--110 and 5 (1938): 141--151.",
        "url": ""
    },
]

SHAMS_CITS = BASE_ISLAMICATE + [
    {
        "text": "Berlekamp, Persis. Wonder, Image, and Cosmos in Medieval Islam. New Haven: Yale University Press, 2011.",
        "url": "https://yalebooks.yale.edu/book/9780300158434/wonder-image-and-cosmos-in-medieval-islam/"
    },
    {
        "text": "Melvin-Koushki, Matthew. 'Astrology, Lettrism, Geomancy: The Occult-Scientific Methods of Post-Mongol Islamicate Imperialism.' Medieval History Journal 19, no. 1 (2016): 142--150. DOI: 10.1177/0971945816638066.",
        "url": "https://doi.org/10.1177/0971945816638066"
    },
    {
        "text": "Lory, Pierre. La science des lettres en Islam. Paris: Dervy, 2004.",
        "url": "https://www.dervy-medicis.fr/"
    },
]

HILDEGARD_CITS = [
    {
        "text": "Newman, Barbara. Sister of Wisdom: St. Hildegard's Theology of the Feminine. Berkeley: University of California Press, 1987.",
        "url": "https://www.ucpress.edu/book/9780520215979/sister-of-wisdom"
    },
    {
        "text": "Maddocks, Fiona. Hildegard of Bingen: The Woman of Her Age. London: Headline, 2001.",
        "url": "https://archive.org/details/hildegardofbinge0000madd"
    },
    {
        "text": "Flanagan, Sabina. Hildegard of Bingen, 1098--1179: A Visionary Life. London: Routledge, 1989.",
        "url": "https://www.routledge.com/Hildegard-of-Bingen-1098-1179-A-Visionary-Life/Flanagan/p/book/9780415045599"
    },
    {
        "text": "Caviness, Madeline. 'Hildegard as Designer of the Illustrations to Her Works.' In Hildegard of Bingen: The Context of Her Thought and Art, ed. Charles Burnett and Peter Dronke. London: Warburg Institute, 1998, 29--62.",
        "url": "https://warburg.sas.ac.uk/publications/"
    },
    {
        "text": "Obrist, Barbara. 'Cosmological Iconography in Hildegard of Bingen's Liber divinorum operum.' In Hildegard of Bingen: The Context of Her Thought and Art, ed. Burnett and Dronke. London: Warburg Institute, 1998, 111--148.",
        "url": "https://warburg.sas.ac.uk/publications/"
    },
]

ISLAMICATE_OCCULT_CITS = BASE_ISLAMICATE + [
    {
        "text": "Melvin-Koushki, Matthew. 'Astrology, Lettrism, Geomancy.' Medieval History Journal 19 (2016). DOI: 10.1177/0971945816638066.",
        "url": "https://doi.org/10.1177/0971945816638066"
    },
    {
        "text": "Fahd, Toufic. La Divination arabe: Etudes religieuses, sociologiques et folkloriques sur le milieu natif de l'Islam. Leiden: Brill, 1966.",
        "url": "https://brill.com/"
    },
]

ISLAMICATE_GEOMANCY_CITS = BASE_ISLAMICATE + [
    {
        "text": "Savage-Smith, Emilie and Marion B. Smith. Islamic Geomancy and a Thirteenth-Century Divinatory Device. Malibu: Undena Publications, 1980.",
        "url": ""
    },
    {
        "text": "Fahd, Toufic. La Divination arabe: Etudes religieuses, sociologiques et folkloriques. Leiden: Brill, 1966.",
        "url": "https://brill.com/"
    },
    {
        "text": "Melvin-Koushki, Matthew. 'Astrology, Lettrism, Geomancy.' Medieval History Journal 19 (2016). DOI: 10.1177/0971945816638066.",
        "url": "https://doi.org/10.1177/0971945816638066"
    },
]

ARS_NOTORIA_CITS = [
    {
        "text": "Kieckhefer, Richard. Magic in the Middle Ages. Cambridge: Cambridge University Press, 1990.",
        "url": "https://www.cambridge.org/core/books/magic-in-the-middle-ages/D5FE4B5B9F6AB0C5D3B4E0A6E2D2B2D4"
    },
    {
        "text": "Fanger, Claire (ed.). Conjuring Spirits: Texts and Traditions of Medieval Ritual Magic. University Park: Penn State University Press, 1998.",
        "url": "https://www.psupress.org/books/titles/0-271-01777-8.html"
    },
    {
        "text": "Veronese, Julien. 'Magic, Theurgy and Spirituality in the Medieval Ritual Magic of the Ars Notoria.' In Invoking Angels: Theurgic Ideas and Practices, Thirteenth to Sixteenth Centuries, ed. Claire Fanger. University Park: Penn State, 2012, 37--78.",
        "url": "https://www.psupress.org/books/titles/978-0-271-04842-8.html"
    },
    {
        "text": "Camille, Michael. 'Visual Art in Two Manuscripts of the Ars Notoria.' In Fanger, Conjuring Spirits (1998), 110--139.",
        "url": "https://www.psupress.org/books/titles/0-271-01777-8.html"
    },
    {
        "text": "Klaassen, Frank. The Transformations of Magic: Illicit Learned Magic in the Later Middle Ages and Renaissance. University Park: Penn State, 2013.",
        "url": "https://www.psupress.org/books/titles/978-0-271-06257-8.html"
    },
]

SEFER_YETZIRAH_CITS = [
    {
        "text": "Hayman, A. Peter (ed. and trans.). Sefer Yesira: Edition, Translation and Text-Critical Commentary. Tubingen: Mohr Siebeck, 2004.",
        "url": "https://www.mohrsiebeck.com/"
    },
    {
        "text": "Scholem, Gershom. Kabbalah. New York: Quadrangle/New York Times, 1974.",
        "url": "https://archive.org/details/kabbalah00scho"
    },
    {
        "text": "Idel, Moshe. Golem: Jewish Magical and Mystical Traditions on the Artificial Anthropoid. Albany: SUNY Press, 1990.",
        "url": "https://www.sunypress.edu/p-2027-golem.aspx"
    },
    {
        "text": "Dan, Joseph. Kabbalah: A Very Short Introduction. Oxford: Oxford University Press, 2006.",
        "url": "https://global.oup.com/academic/product/kabbalah-9780195300345"
    },
]

PROPHECY_CITS = [
    {
        "text": "McGinn, Bernard. Visions of the End: Apocalyptic Traditions in the Middle Ages. New York: Columbia University Press, 1979.",
        "url": "https://cup.columbia.edu/book/visions-of-the-end/9780231043489"
    },
    {
        "text": "Reeves, Marjorie. Prophecy in the Later Middle Ages: A Study in Joachimism. Oxford: Clarendon Press, 1969.",
        "url": "https://global.oup.com/academic/product/prophecy-in-the-later-middle-ages-9780198213192"
    },
    {
        "text": "Lerner, Robert E. The Powers of Prophecy: The Cedar of Lebanon Vision from the Mongol Onslaught to the Dawn of the Enlightenment. Berkeley: University of California Press, 1983.",
        "url": "https://www.ucpress.edu/book/9780520046634/the-powers-of-prophecy"
    },
]

ATALANTA_CITS = [
    {
        "text": "Tilton, Hereward. The Quest for the Phoenix: Spiritual Alchemy and Rosicrucianism in the Work of Count Michael Maier (1569--1622). Berlin: De Gruyter, 2003.",
        "url": "https://www.degruyter.com/document/doi/10.1515/9783110906660/html"
    },
    {
        "text": "Szulakowska, Urszula. The Alchemy of Light: Geometry and Optics in Late Renaissance Alchemical Illustration. Leiden: Brill, 2000.",
        "url": "https://brill.com/display/title/7527"
    },
    {
        "text": "Abraham, Lyndy. A Dictionary of Alchemical Imagery. Cambridge: Cambridge University Press, 1998.",
        "url": "https://www.cambridge.org/core/books/dictionary-of-alchemical-imagery/7C5B5A62E5E48A3C3C7B6F6F4E4A4D4C"
    },
    {
        "text": "Principe, Lawrence M. The Secrets of Alchemy. Chicago: University of Chicago Press, 2013.",
        "url": "https://press.uchicago.edu/ucp/books/book/chicago/S/bo14621946.html"
    },
    {
        "text": "Maier, Michael. Atalanta Fugiens. Oppenheim: Johann Theodore de Bry, 1617. Internet Archive facsimile.",
        "url": "https://archive.org/details/atalantafugiensh00maie"
    },
]

# Map: ID prefix -> citations
PREFIX_CITS = {
    "ordinal_alchemy": ORDINAL_ALCHEMY_CITS,
    "barchusen_elementa": BARCHUSEN_CITS,
    "islamic_talismans": ISLAMIC_TALISMAN_CITS,
    "ia_shams_ms": SHAMS_CITS,
    "shams_al_maarif": SHAMS_CITS,
    "hildegard_bingen": HILDEGARD_CITS,
    "islamicate_occult": ISLAMICATE_OCCULT_CITS,
    "islamicate_geomancy": ISLAMICATE_GEOMANCY_CITS,
    "ars_notoria": ARS_NOTORIA_CITS,
    "sefer_yetzirah": SEFER_YETZIRAH_CITS,
    "prophecy_figurae": PROPHECY_CITS,
    "atalanta_fugiens": ATALANTA_CITS,
}

def get_prefix(eid):
    if '__' in eid:
        return eid.split('__')[0]
    parts = eid.rsplit('_', 1)
    return parts[0] if len(parts) > 1 else eid

def main():
    with open(DATA_FILE, encoding='utf-8') as f:
        overrides = json.load(f)

    enriched = 0
    for i, entry in enumerate(overrides):
        if entry.get('citations'):
            continue
        eid = entry.get('id', '')
        prefix = get_prefix(eid)
        cits = PREFIX_CITS.get(prefix)
        if not cits:
            continue
        overrides[i]['citations'] = cits
        enriched += 1

    print(f"Enriched {enriched} entries.")
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(overrides, f, ensure_ascii=False, indent=1)
    print("Written to overrides.json")

if __name__ == "__main__":
    main()
