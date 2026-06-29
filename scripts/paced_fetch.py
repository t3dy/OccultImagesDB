# -*- coding: utf-8 -*-
"""Paced wrapper: run fetch_commons one job at a time with a delay to respect 429 limits."""
import json, sys, time, subprocess, os, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
jobs = json.load(open(sys.argv[1], encoding="utf-8"))
delay = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
for i, job in enumerate(jobs):
    tf = os.path.join(tempfile.gettempdir(), f"_pj_{i}.json")
    json.dump([job], open(tf, "w", encoding="utf-8"))
    r = subprocess.run([sys.executable, os.path.join(HERE, "fetch_commons.py"), tf],
                       capture_output=True, text=True, encoding="utf-8")
    print((r.stdout or "").strip())
    if r.stderr and "429" in r.stderr:
        print("[stderr429]")
    os.remove(tf)
    if i < len(jobs) - 1:
        time.sleep(delay)
