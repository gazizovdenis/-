"""
Find duplicate glasses images between two folders by visual similarity.
Uses perceptual hash on the full image AND on cropped text regions (top/bottom)
where article numbers are typically placed.
"""
import os
import sys
import json
from PIL import Image
import numpy as np

FOLDER1 = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Фото с очками\Исходники Гульшат"
FOLDER2 = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Фото с очками\Исходники Гульшат 2"

HASH_SIZE = 16  # 16x16 = 256-bit hash
TEXT_CROP_RATIO = 0.18  # top/bottom 18% of image for text crop
FULL_THRESHOLD = 15    # max hamming distance for full-image match
TEXT_THRESHOLD = 8     # max hamming distance for text-region match


def phash(img, size=HASH_SIZE):
    """Perceptual hash: resize, grayscale, DCT-like via mean comparison."""
    img = img.convert("L").resize((size * 4, size * 4), Image.LANCZOS)
    arr = np.array(img, dtype=float)
    # Simple block average instead of full DCT
    block = arr.reshape(size, 4, size, 4).mean(axis=(1, 3))
    avg = block.mean()
    bits = (block >= avg).flatten()
    return bits


def hamming(a, b):
    return int(np.sum(a != b))


def crop_text_zones(img):
    """Return top strip, bottom strip, and full image as PIL Images."""
    w, h = img.size
    top_h = int(h * TEXT_CROP_RATIO)
    bot_h = int(h * TEXT_CROP_RATIO)
    top = img.crop((0, 0, w, top_h))
    bot = img.crop((0, h - bot_h, w, h))
    return top, bot


def load_folder(folder):
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    result = {}
    for fname in sorted(os.listdir(folder)):
        if os.path.splitext(fname)[1].lower() not in exts:
            continue
        path = os.path.join(folder, fname)
        try:
            img = Image.open(path)
            img.load()
            top, bot = crop_text_zones(img)
            result[fname] = {
                "full": phash(img),
                "top": phash(top),
                "bot": phash(bot),
            }
        except Exception as e:
            print(f"  [skip] {fname}: {e}", file=sys.stderr)
    return result


print("Loading folder 1...", flush=True)
data1 = load_folder(FOLDER1)
print(f"  {len(data1)} images loaded")

print("Loading folder 2...", flush=True)
data2 = load_folder(FOLDER2)
print(f"  {len(data2)} images loaded")

print("Comparing...", flush=True)

groups = []  # list of {f1, f2, full_dist, text_dist, reason}
seen_pairs = set()

for f1, h1 in data1.items():
    for f2, h2 in data2.items():
        pair = (f1, f2)
        if pair in seen_pairs:
            continue

        full_d = hamming(h1["full"], h2["full"])
        top_d = hamming(h1["top"], h2["top"])
        bot_d = hamming(h1["bot"], h2["bot"])
        text_d = min(top_d, bot_d)

        match_full = full_d <= FULL_THRESHOLD
        match_text = text_d <= TEXT_THRESHOLD

        if match_full or match_text:
            seen_pairs.add(pair)
            reason_parts = []
            if match_full:
                reason_parts.append(f"full_hash_dist={full_d}")
            if match_text:
                zone = "top" if top_d <= bot_d else "bottom"
                reason_parts.append(f"text_{zone}_dist={text_d}")
            groups.append({
                "f1": f1,
                "f2": f2,
                "full_dist": full_d,
                "text_dist": text_d,
                "reason": ", ".join(reason_parts),
            })

# Sort by similarity (lower = more similar)
groups.sort(key=lambda x: x["full_dist"])

print(f"\n=== RESULTS: {len(groups)} potential duplicate pairs ===\n")
for i, g in enumerate(groups, 1):
    print(f"Пара {i}:")
    print(f"  Папка 1: {g['f1']}")
    print(f"  Папка 2: {g['f2']}")
    print(f"  Причина: {g['reason']}")
    print()

# Also dump JSON for further processing
out_path = os.path.join(os.path.dirname(__file__), "dup_glasses_result.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(groups, f, ensure_ascii=False, indent=2)
print(f"JSON saved to: {out_path}")
