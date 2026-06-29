# -*- coding: utf-8 -*-
"""
build_all.py — one command to (re)build the whole project from the authored sources.

Pipeline:
  1. import_local_scholarship.py   (fold local Claudiens/Theo discourse into overrides.json)
  2. import_motifs.py              (promote motif ontology into entities.json)
  3. build_catalog.py [args]       (scan images -> derivatives -> data/catalog.json + works.json)
  4. build_db.py --stats           (compile the canonical SQLite db/occultimgdb.db)

Pass-through args go to build_catalog.py, e.g.:  python scripts/build_all.py --all
The import_* steps are idempotent and preserve hand-authored content, so this is safe to re-run.
"""
import subprocess
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def run(script, *args):
    print(f"\n=== {script} {' '.join(args)} ===")
    r = subprocess.run([PY, os.path.join(HERE, script), *args])
    if r.returncode != 0:
        print(f"!! {script} failed (exit {r.returncode})")
        sys.exit(r.returncode)


if __name__ == "__main__":
    passthru = sys.argv[1:]
    run("import_local_scholarship.py")
    run("import_motifs.py")
    run("build_catalog.py", *passthru)
    run("build_operations.py")  # regen the Twelve Processes gates from the fresh catalog
    run("build_db.py", "--stats")
    print("\nAll done. Open site/index.html (served from project root) and query db/occultimgdb.db.")
