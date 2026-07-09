"""Check new works are in SOURCES after works_extra loading."""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, 'scripts')
import config

target_keys = ['khunrath_amphi', 'rosarium_supplement', 'libavius_alchymia', 'musaeum_hermeticum', 'alchemist_laboratory']
print("Checking new works in SOURCES:")
for k in target_keys:
    src = next((s for s in config.SOURCES if s['key'] == k), None)
    if src:
        root = src.get('root', 'EMBLEM')
        img_dir = src.get('image_dir', '')
        roots = {"BEU": config.ALCHEMY_BEU_ROOT, "LOCAL": config.LOCAL_SOURCED_ROOT}
        base = roots.get(root, config.EMBLEM_ROOT)
        full_dir = os.path.join(base, img_dir)
        files = [f for f in os.listdir(full_dir) if f.lower().endswith(('.jpg','.jpeg','.png','.webp'))] if os.path.exists(full_dir) else []
        print(f"  {k}: OK (root={root}, {len(files)} images at {full_dir})")
    else:
        print(f"  {k}: NOT FOUND in SOURCES")
