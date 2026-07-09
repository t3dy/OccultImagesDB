"""
Copy and prepare BEU uncovered images into sources_web/ directories.

Targets:
1. khunrath_amphi/ — 4 Amphitheatrum circular plates + 2 Fotothek + 1 general
2. rosarium_supplement/ — legitimate historical Rosarium plates
3. libavius_alchymia/ — 6 lab illustration pages (p0025-p0150)

All are resized to max 1500px long edge and saved as JPG.
"""
import os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("PIL not available; will use shutil.copy for PNG files")

BEU = r"C:\Dev\AlchemyBeatEmUp\staging\raw_images"
LOCAL = r"C:\Dev\OCCULTIMGDB\sources_web"
MAX_PX = 1500

def resize_save(src, dst, max_px=MAX_PX):
    """Resize image to max_px long edge and save as JPEG."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not HAS_PIL:
        shutil.copy2(src, dst)
        print(f"  Copied (no PIL): {os.path.basename(dst)}")
        return
    try:
        img = Image.open(src).convert("RGB")
        w, h = img.size
        if max(w, h) > max_px:
            scale = max_px / max(w, h)
            img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
        img.save(dst, "JPEG", quality=92, optimize=True)
        size_kb = os.path.getsize(dst) // 1024
        print(f"  {os.path.basename(src)} -> {os.path.basename(dst)} ({size_kb}KB)")
    except Exception as e:
        print(f"  ERROR {os.path.basename(src)}: {e}")

# ============================================================
# 1. Khunrath Amphitheatrum circular plates
# ============================================================
print("=== khunrath_amphi: 4 circular plates + 2 Fotothek + 1 general ===")
kh_src = os.path.join(BEU, "khunrath_amphitheatrum")
kh_dst = os.path.join(LOCAL, "khunrath_amphi")

kh_files = [
    ("Amphitheatrum_sapientiae_aeternae_1__a9663043.png", "amphitheatrum_plate_1.jpg"),
    ("Amphitheatrum_sapientiae_aeternae_2__7074747e.png", "amphitheatrum_plate_2.jpg"),
    ("Amphitheatrum_sapientiae_aeternae_3__bf2fa8d9.png", "amphitheatrum_plate_3.jpg"),
    ("Amphitheatrum_sapientiae_aeternae_4__5faa64e8.png", "amphitheatrum_plate_4.jpg"),
    ("Fotothek_df_tg_0008212_Theosophie___Alchemie___Medizin__33fcf40a.jpg", "fotothek_0008212.jpg"),
    ("Fotothek_df_tg_0008213_Theosophie___Alchemie___Medizin__78d840f9.jpg", "fotothek_0008213.jpg"),
    ("Khunrath__5f5c8055.jpg", "khunrath_general.jpg"),
    # Note: Paulus_van_der_Doort will go to alchemist_laboratory separately
]

for src_fn, dst_fn in kh_files:
    src = os.path.join(kh_src, src_fn)
    dst = os.path.join(kh_dst, dst_fn)
    if os.path.exists(src):
        resize_save(src, dst)
    else:
        print(f"  MISSING: {src_fn}")

# ============================================================
# 2. Van der Doort laboratory painting -> sources_web/alchemist_laboratory/
# ============================================================
print("\n=== alchemist_laboratory: van der Doort painting ===")
al_dst = os.path.join(LOCAL, "alchemist_laboratory")
vdd_src = os.path.join(kh_src, "Paulus_van_der_Doort_-_The_laboratory_of_the_alchemist__2f6ff019.jpg")
vdd_dst = os.path.join(al_dst, "van_der_doort_laboratory.jpg")
if os.path.exists(vdd_src):
    resize_save(vdd_src, vdd_dst)
else:
    print(f"  MISSING: {vdd_src}")

# ============================================================
# 3. Rosarium supplement (legitimate historical images only)
# ============================================================
print("\n=== rosarium_supplement: legitimate Rosarium plates ===")
ros_src = os.path.join(BEU, "rosarium_philosophorum")
ros_dst = os.path.join(LOCAL, "rosarium_supplement")

PLACEHOLDER_SIZE = 500455  # Google Books placeholder

ros_files = [
    # Filename (BEU), target name, include?
    ("Androgynous_Rebis__bba6b24a.jpg", "rebis_androgynous.jpg"),
    ("Der_grüne_Löwe__der_Sol_verschlingt__9efaa2e2.jpg", "green_lion_devouring_sun.jpg"),
    ("Fig.3__3a0b4233.jpg", "fig_03_fountain.jpg"),
    ("Fig._10__2a6f2f7e.jpg", "fig_10_birth.jpg"),
    ("Fig.17__2f8bb196.jpg", "fig_17_fermentation.jpg"),
    ("Fig.19__f1452ca2.jpg", "fig_19_soul_return.jpg"),
    ("Fig.20__1c1127de.jpg", "fig_20_resurrection.jpg"),
    ("Fixatio__85d43a48.png", "fixation.jpg"),
    ("Fotothek_df_tg_0007012_Theosophie___Alchemie__bda735cd.jpg", "fotothek_0007012.jpg"),
    ("Fotothek_df_tg_0007013_Theosophie___Alchemie__02273b77.jpg", "fotothek_0007013.jpg"),
    ("Fotothek_df_tg_0007014_Theosophie___Alchemie__7b698d00.jpg", "fotothek_0007014.jpg"),
    ("Fotothek_df_tg_0007015_Theosophie___Alchemie__31c30b70.jpg", "fotothek_0007015.jpg"),
    ("Lion_devouring_the_sun__c129237c.jpg", "lion_devouring_sun_large.jpg"),
    ("Lion_Sun_Moon__6ee155b0.jpg", "lion_sun_moon.jpg"),
    ("Marriage_Sol_Moon_-_Rosarium_Philosophorum_Griemiller02__e6d8224b.jpg", "griemiller_sol_luna_02.jpg"),
    ("Marriage_Sun_Moon_-_Rosarium_Philosophorum_Griemiller__0725e909.jpg", "griemiller_sol_luna_01.jpg"),
    ("Rosarium_11_fermentatio__82834baa.jpg", "rosarium_11_fermentatio.jpg"),
    # SKIP: New_skin* (album art), Green_lion_consuming_sun (smaller version), Roi_et_Reine (34KB), Turba_phil, Winged_Sun
]

for src_fn, dst_fn in ros_files:
    src = os.path.join(ros_src, src_fn)
    if not os.path.exists(src):
        print(f"  MISSING: {src_fn}")
        continue
    sz = os.path.getsize(src)
    if sz == PLACEHOLDER_SIZE:
        print(f"  SKIP (placeholder): {src_fn}")
        continue
    dst = os.path.join(ros_dst, dst_fn)
    resize_save(src, dst)

# ============================================================
# 4. Libavius Alchymia (only pages with real illustrations)
# ============================================================
print("\n=== libavius_alchymia: 6 illustration pages ===")
lib_src = os.path.join(BEU, "libavius_alchymia")
lib_dst = os.path.join(LOCAL, "libavius_alchymia")

for n in [25, 50, 75, 100, 125, 150]:
    src_fn = f"bub_gb_0WfRikJt9yQC__p{n:04d}.jpg"
    src = os.path.join(lib_src, src_fn)
    dst_fn = f"libavius_p{n:04d}.jpg"
    dst = os.path.join(lib_dst, dst_fn)
    if not os.path.exists(src):
        print(f"  MISSING: {src_fn}")
        continue
    sz = os.path.getsize(src)
    if sz == PLACEHOLDER_SIZE:
        print(f"  SKIP (placeholder): {src_fn}")
        continue
    resize_save(src, dst)

print("\nDone.")
