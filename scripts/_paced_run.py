# temp paced runner: one job at a time with sleeps to respect Commons 429
import json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
jobs = json.load(open(os.path.join(HERE, "jobs_alchemy_emblems_more.json"), encoding="utf-8"))
tmp = os.path.join(HERE, "_one.json")
delay = 18
for i, job in enumerate(jobs):
    json.dump([job], open(tmp, "w", encoding="utf-8"))
    for attempt in range(4):
        r = subprocess.run([sys.executable, os.path.join(HERE, "fetch_commons.py"), tmp],
                           capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        print(out.strip().encode("ascii", "replace").decode("ascii"), flush=True)
        if "429" not in out:
            break
        wait = 30 * (attempt + 1)
        print(f"   [429 backoff {wait}s]", flush=True)
        time.sleep(wait)
    time.sleep(delay)
os.remove(tmp)
print("PACED DONE", flush=True)
