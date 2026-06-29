# -*- coding: utf-8 -*-
"""
build_db.py — compile the canonical SQLite database for OCCULTIMGDB.

The database `db/occultimgdb.db` is the project's dedicated, queryable catalog store. It is COMPILED
(idempotently, full rebuild) from the authored sources that already drive the site:
  - data/catalog.json   (denormalised per-image records: works + images + motifs + citations + relations)
  - data/entities.json  (creators, traditions, motifs — the relational/encyclopedia layer)

Why compile rather than hand-edit the DB: prose & scholarship live in version-controlled JSON
(easy to diff, review, and author); the DB is the normalised, indexed, query-friendly canonical view
and the substrate for analytics, an encyclopedia export, or a future API. (Deckard boundary:
deterministic compile; human/LLM judgement stays in the JSON sources.)

Run order:  build_catalog.py  ->  build_db.py
Then query:  python scripts/build_db.py --stats
"""
import argparse
import json
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
DB_DIR = os.path.join(ROOT, "db")
DB_PATH = os.path.join(DB_DIR, "occultimgdb.db")

SCHEMA = """
DROP TABLE IF EXISTS works;
DROP TABLE IF EXISTS images;
DROP TABLE IF EXISTS image_motifs;
DROP TABLE IF EXISTS image_citations;
DROP TABLE IF EXISTS image_relations;
DROP TABLE IF EXISTS image_concepts;
DROP TABLE IF EXISTS creators;
DROP TABLE IF EXISTS creator_works;
DROP TABLE IF EXISTS creator_links;
DROP TABLE IF EXISTS traditions;
DROP TABLE IF EXISTS tradition_links;
DROP TABLE IF EXISTS motifs;
DROP TABLE IF EXISTS motif_terms;
DROP TABLE IF EXISTS motif_see_also;

CREATE TABLE works (
  work_key TEXT PRIMARY KEY, title TEXT, creator TEXT, date TEXT, era TEXT, tradition TEXT,
  tier TEXT, place TEXT, language TEXT, provenance_url TEXT, rights TEXT, blurb TEXT, image_count INTEGER
);
CREATE TABLE images (
  id TEXT PRIMARY KEY, work_key TEXT, seq INTEGER, title TEXT, creator TEXT, date TEXT, century INTEGER,
  place TEXT, region TEXT, language TEXT, era TEXT, tradition TEXT, tier TEXT,
  summary TEXT, summary_status TEXT, source_origin TEXT,
  rights TEXT, provenance_url TEXT, source_file TEXT, thumb TEXT, card TEXT,
  FOREIGN KEY(work_key) REFERENCES works(work_key)
);
CREATE TABLE image_motifs   (image_id TEXT, motif TEXT, FOREIGN KEY(image_id) REFERENCES images(id));
CREATE TABLE image_citations(image_id TEXT, ord INTEGER, text TEXT, url TEXT, FOREIGN KEY(image_id) REFERENCES images(id));
CREATE TABLE image_relations(image_id TEXT, related_id TEXT, kind TEXT, FOREIGN KEY(image_id) REFERENCES images(id));
CREATE TABLE image_concepts (image_id TEXT, concept TEXT, FOREIGN KEY(image_id) REFERENCES images(id));

CREATE TABLE creators (key TEXT PRIMARY KEY, name TEXT, dates TEXT, role TEXT, blurb TEXT, summary TEXT);
CREATE TABLE creator_works (creator_key TEXT, work_key TEXT);
CREATE TABLE creator_links (creator_key TEXT, label TEXT, url TEXT);
CREATE TABLE traditions (key TEXT PRIMARY KEY, name TEXT, blurb TEXT, summary TEXT);
CREATE TABLE tradition_links (tradition_key TEXT, label TEXT, url TEXT);
CREATE TABLE motifs (key TEXT PRIMARY KEY, name TEXT, blurb TEXT, summary TEXT, source TEXT);
CREATE TABLE motif_terms (motif_key TEXT, term TEXT);
CREATE TABLE motif_see_also (motif_key TEXT, other_key TEXT);

DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS topic_subthemes;
DROP TABLE IF EXISTS topic_figures;
DROP TABLE IF EXISTS collections;
DROP TABLE IF EXISTS collection_figures;
CREATE TABLE topics (key TEXT PRIMARY KEY, name TEXT, status TEXT, blurb TEXT, summary TEXT, match_json TEXT, needs TEXT);
CREATE TABLE topic_subthemes (topic_key TEXT, subtheme TEXT);
CREATE TABLE topic_figures (topic_key TEXT, figure_key TEXT);
CREATE TABLE collections (key TEXT PRIMARY KEY, title TEXT, status TEXT, framing TEXT, cover TEXT, match_json TEXT, needs TEXT);
CREATE TABLE collection_figures (collection_key TEXT, figure_key TEXT);

DROP TABLE IF EXISTS wanted;
CREATE TABLE wanted (id TEXT PRIMARY KEY, title TEXT, subject TEXT, topic TEXT, period TEXT, via TEXT,
  why TEXT, rights TEXT, status TEXT, engine TEXT, candidate_sources TEXT);

CREATE INDEX idx_images_work ON images(work_key);
CREATE INDEX idx_images_era ON images(era);
CREATE INDEX idx_images_tradition ON images(tradition);
CREATE INDEX idx_image_motifs ON image_motifs(motif);
"""


def load(name):
    with open(os.path.join(DATA, name), "r", encoding="utf-8") as f:
        return json.load(f)


def build():
    os.makedirs(DB_DIR, exist_ok=True)
    catalog = load("catalog.json")
    entities = load("entities.json")
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA)
    cur = con.cursor()

    for w in catalog.get("works", []):
        cur.execute("INSERT OR REPLACE INTO works VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            w.get("key"), w.get("title"), w.get("creator"), w.get("date"), w.get("era"),
            w.get("tradition"), w.get("tier"), w.get("place"), w.get("language"),
            w.get("provenance_url"), w.get("rights"), w.get("blurb"), w.get("count")))

    for it in catalog.get("items", []):
        cur.execute("""INSERT OR REPLACE INTO images VALUES
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            it.get("id"), it.get("work_key"), it.get("seq"), it.get("title"), it.get("creator"),
            it.get("date"), it.get("century"), it.get("place"), it.get("region"), it.get("language"),
            it.get("era"), it.get("tradition"), it.get("tier"), it.get("summary"),
            it.get("summary_status"), it.get("source"), it.get("rights"), it.get("provenance_url"),
            it.get("source_file"), it.get("thumb"), it.get("card")))
        for m in it.get("motifs", []) or []:
            cur.execute("INSERT INTO image_motifs VALUES (?,?)", (it["id"], m))
        for i, c in enumerate(it.get("citations", []) or []):
            cur.execute("INSERT INTO image_citations VALUES (?,?,?,?)", (it["id"], i, c.get("text"), c.get("url")))
        for n in it.get("related_emblems", []) or []:
            rid = f"atalanta_fugiens__emblem-{int(n):02d}"
            cur.execute("INSERT INTO image_relations VALUES (?,?,?)", (it["id"], rid, "related_emblem"))
        for k in it.get("key_concepts", []) or []:
            cur.execute("INSERT INTO image_concepts VALUES (?,?)", (it["id"], k))

    for c in entities.get("creators", []):
        cur.execute("INSERT OR REPLACE INTO creators VALUES (?,?,?,?,?,?)", (
            c["key"], c.get("name"), c.get("dates"), c.get("role"), c.get("blurb"), c.get("summary")))
        for wk in c.get("works", []) or []:
            cur.execute("INSERT INTO creator_works VALUES (?,?)", (c["key"], wk))
        for l in c.get("links", []) or []:
            cur.execute("INSERT INTO creator_links VALUES (?,?,?)", (c["key"], l.get("label"), l.get("url")))

    for t in entities.get("traditions", []):
        cur.execute("INSERT OR REPLACE INTO traditions VALUES (?,?,?,?)", (
            t["key"], t.get("name"), t.get("blurb"), t.get("summary")))
        for l in t.get("links", []) or []:
            cur.execute("INSERT INTO tradition_links VALUES (?,?,?)", (t["key"], l.get("label"), l.get("url")))

    for m in entities.get("motifs", []):
        cur.execute("INSERT OR REPLACE INTO motifs VALUES (?,?,?,?,?)", (
            m["key"], m.get("name"), m.get("blurb"), m.get("summary"), m.get("source")))
        for term in (m.get("match") or [m["key"]]):
            cur.execute("INSERT INTO motif_terms VALUES (?,?)", (m["key"], term))
        for o in m.get("see_also", []) or []:
            cur.execute("INSERT INTO motif_see_also VALUES (?,?)", (m["key"], o))

    # topics + collections (the esoteric-historiography taxonomy)
    try:
        topics = load("topics.json").get("topics", [])
    except Exception:
        topics = []
    for t in topics:
        cur.execute("INSERT OR REPLACE INTO topics VALUES (?,?,?,?,?,?,?)", (
            t["key"], t.get("name"), t.get("status"), t.get("blurb"), t.get("summary"),
            json.dumps(t.get("match", {})), t.get("needs")))
        for s in t.get("subthemes", []) or []:
            cur.execute("INSERT INTO topic_subthemes VALUES (?,?)", (t["key"], s))
        for fk in t.get("figures", []) or []:
            cur.execute("INSERT INTO topic_figures VALUES (?,?)", (t["key"], fk))
    try:
        collections = load("collections.json").get("collections", [])
    except Exception:
        collections = []
    for c in collections:
        cur.execute("INSERT OR REPLACE INTO collections VALUES (?,?,?,?,?,?,?)", (
            c["key"], c.get("title"), c.get("status"), c.get("framing"), c.get("cover"),
            json.dumps(c.get("match", {})), c.get("needs")))
        for fk in c.get("figures", []) or []:
            cur.execute("INSERT INTO collection_figures VALUES (?,?)", (c["key"], fk))

    # discovery queue
    try:
        wanted = load("wanted.json").get("wanted", [])
    except Exception:
        wanted = []
    for w in wanted:
        cur.execute("INSERT OR REPLACE INTO wanted VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
            w["id"], w.get("title"), w.get("subject"), w.get("topic"), w.get("period"), w.get("via"),
            w.get("why"), w.get("rights"), w.get("status"), w.get("engine"),
            json.dumps(w.get("candidate_sources", []))))

    con.commit()
    return con


def stats(con):
    cur = con.cursor()
    def n(q): return cur.execute(q).fetchone()[0]
    authored = n("SELECT COUNT(*) FROM images WHERE summary_status='authored'")
    print("OCCULTIMGDB database:", DB_PATH)
    print(f"  works ............ {n('SELECT COUNT(*) FROM works')}")
    print(f"  images ........... {n('SELECT COUNT(*) FROM images')}")
    print(f"  authored ......... {authored}")
    print(f"  motif tags ....... {n('SELECT COUNT(*) FROM image_motifs')}  ({n('SELECT COUNT(DISTINCT motif) FROM image_motifs')} distinct)")
    print(f"  citations ........ {n('SELECT COUNT(*) FROM image_citations')}")
    print(f"  relations ........ {n('SELECT COUNT(*) FROM image_relations')}")
    print(f"  concepts ......... {n('SELECT COUNT(*) FROM image_concepts')}")
    print(f"  creators ......... {n('SELECT COUNT(*) FROM creators')}")
    print(f"  traditions ....... {n('SELECT COUNT(*) FROM traditions')}")
    print(f"  motifs (enc.) .... {n('SELECT COUNT(*) FROM motifs')}")
    topics_live = n("SELECT COUNT(*) FROM topics WHERE status='live'")
    coll_live = n("SELECT COUNT(*) FROM collections WHERE status='live'")
    print(f"  topics ........... {n('SELECT COUNT(*) FROM topics')}  ({topics_live} live)")
    print(f"  collections ...... {n('SELECT COUNT(*) FROM collections')}  ({coll_live} live)")
    print(f"  wanted (queue) ... {n('SELECT COUNT(*) FROM wanted')} discovery targets")
    print("  images per era:")
    for era, c in cur.execute("SELECT era, COUNT(*) FROM images GROUP BY era ORDER BY COUNT(*) DESC"):
        print(f"     {era:14s} {c}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stats", action="store_true", help="print stats after building")
    args = ap.parse_args()
    con = build()
    print(f"Built {DB_PATH}")
    if args.stats:
        stats(con)
    con.close()


if __name__ == "__main__":
    main()
