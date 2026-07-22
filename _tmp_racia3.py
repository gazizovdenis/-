import sys, io, zipfile, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
import openpyxl

wb = openpyxl.load_workbook(
    r"c:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Конвеер новинок\Товары из Китая 13.05 (1).xlsx",
    read_only=True, data_only=True
)

ws = wb["рация"]
print("=== ЛИСТ: рация ===")
for row in ws.iter_rows(values_only=True):
    if any(c is not None for c in row):
        clean = [str(c)[:120] if c is not None else "" for c in row[:20]]
        non_empty = [c for c in clean if c.strip()]
        if non_empty:
            print(" | ".join(non_empty))

# Also extract images
print("\n\n=== ИЗОБРАЖЕНИЯ ===")
src = r"c:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Конвеер новинок\Товары из Китая 13.05 (1).xlsx"
out = r"c:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Конвеер новинок\_images_temp2"
os.makedirs(out, exist_ok=True)
with zipfile.ZipFile(src) as z:
    imgs = [f for f in z.namelist() if 'media' in f.lower()]
    print(f"Всего изображений в файле: {len(imgs)}")
    for img in imgs[-10:]:  # last 10 (likely from рация sheet)
        name = os.path.basename(img)
        z.extract(img, out)
        print(f"  {img}")
