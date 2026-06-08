import os
import sys
from pathlib import Path
from PIL import Image

images_dir = Path(r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт_Netlify\images")
converted = 0
failed = 0
skipped = 0

for f in images_dir.rglob("*"):
    if f.suffix.lower() not in (".png", ".jpg", ".jpeg"):
        continue
    webp_path = f.with_suffix(".webp")
    if webp_path.exists():
        skipped += 1
        continue
    try:
        img = Image.open(f)
        if img.mode in ("RGBA", "LA"):
            img.save(webp_path, "WEBP", quality=85, method=6)
        else:
            img = img.convert("RGB")
            img.save(webp_path, "WEBP", quality=85, method=6)
        converted += 1
        if converted % 100 == 0:
            print(f"Converted {converted}...", flush=True)
    except Exception as e:
        print(f"FAIL: {f.name} — {e}", flush=True)
        failed += 1

print(f"Done: {converted} converted, {skipped} skipped, {failed} failed")
