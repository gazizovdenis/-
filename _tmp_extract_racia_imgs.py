import sys, io, zipfile, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

src = r"c:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Конвеер новинок\Товары из Китая 13.05 (1).xlsx"
out = r"c:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Конвеер новинок\_images_temp2"
os.makedirs(out, exist_ok=True)

target_imgs = ["xl/media/image155.png", "xl/media/image156.png", "xl/media/image159.png", "xl/media/image166.png"]
with zipfile.ZipFile(src) as z:
    for img in target_imgs:
        if img in z.namelist():
            z.extract(img, out)
            print(f"Extracted: {img}")
        else:
            print(f"NOT FOUND: {img}")
