import sys, io, zipfile, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

path = r"c:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Конвеер новинок\Товары из Китая 29.06.xlsx"
out = r"c:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Конвеер новинок\_images_temp2"
os.makedirs(out, exist_ok=True)

targets = ["кухонный набор", "измельчитель"]

with zipfile.ZipFile(path) as z:
    wb_xml = z.read("xl/workbook.xml").decode("utf-8")
    sheets = re.findall(r'<sheet[^>]+name="([^"]+)"[^>]+r:id="([^"]+)"', wb_xml)
    rels_xml = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    sheet_files = re.findall(r'Id="([^"]+)"[^>]+Target="([^"]+)"', rels_xml)

    for t_name in targets:
        print(f"\n=== {t_name} ===")
        for i, (name, rid) in enumerate(sheets):
            if name == t_name:
                # get sheet file
                sheet_file = None
                for rel_id, target in sheet_files:
                    if rel_id == rid:
                        sheet_file = "xl/" + target
                        break
                sheet_name_only = sheet_file.split("/")[-1].replace(".xml","")
                rels_path = f"xl/worksheets/_rels/{sheet_name_only}.xml.rels"
                if rels_path in z.namelist():
                    rels = z.read(rels_path).decode("utf-8")
                    drawings = re.findall(r'Target="\.\./(drawings/[^"]+)"', rels)
                    for drawing in drawings:
                        dp = "xl/" + drawing
                        draw_name = dp.split("/")[-1]
                        draw_dir = "/".join(dp.split("/")[:-1])
                        drels_path = f"{draw_dir}/_rels/{draw_name}.rels"
                        if drels_path in z.namelist():
                            drels = z.read(drels_path).decode("utf-8")
                            img_files = re.findall(r'Target="\.\./(media/[^"]+)"', drels)
                            print("Изображения:", img_files)
                            for img in img_files:
                                full = "xl/" + img
                                if full in z.namelist():
                                    z.extract(full, out)
                                    print(f"  OK: {full}")
                break
