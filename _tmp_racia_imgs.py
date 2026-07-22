import sys, io, zipfile, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

src = r"c:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Конвеер новинок\Товары из Китая 13.05 (1).xlsx"
out = r"c:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Конвеер новинок\_images_temp2\xl\media"

# Find which sheet "рация" is (index) and get its drawing relationships
with zipfile.ZipFile(src) as z:
    # Find the sheet index for рация
    wb_xml = z.read("xl/workbook.xml").decode("utf-8")
    # Find sheet names and their r:id
    import re
    sheets = re.findall(r'<sheet[^>]+name="([^"]+)"[^>]+r:id="([^"]+)"', wb_xml)
    print("Листы:", [(i, n, rid) for i, (n, rid) in enumerate(sheets)])

    # Find рация sheet index
    racia_idx = None
    for i, (name, rid) in enumerate(sheets):
        if name == "рация":
            racia_idx = i + 1  # 1-based
            racia_rid = rid
            print(f"\nРация - индекс: {racia_idx}, rid: {racia_rid}")
            break

    if racia_idx:
        # Get the sheet file name from relationships
        rels_xml = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
        sheet_files = re.findall(r'Id="([^"]+)"[^>]+Target="([^"]+)"', rels_xml)
        racia_file = None
        for rel_id, target in sheet_files:
            if rel_id == racia_rid:
                racia_file = "xl/" + target
                print(f"Файл листа: {racia_file}")
                break

        if racia_file:
            # Get drawings for this sheet
            sheet_base = racia_file.replace("xl/", "").replace(".xml", "")
            sheet_dir = "/".join(racia_file.split("/")[:-1])
            sheet_name_only = racia_file.split("/")[-1].replace(".xml", "")
            rels_path = f"xl/worksheets/_rels/{sheet_name_only}.xml.rels"
            print(f"Ищем rels: {rels_path}")

            if rels_path in z.namelist():
                rels = z.read(rels_path).decode("utf-8")
                print("Sheet rels:", rels[:2000])
                drawings = re.findall(r'Target="\.\./(drawings/[^"]+)"', rels)
                print("Drawings:", drawings)

                for drawing in drawings:
                    drawing_path = "xl/" + drawing
                    if drawing_path in z.namelist():
                        drawing_xml = z.read(drawing_path).decode("utf-8")
                        # Find image references
                        img_refs = re.findall(r'r:embed="([^"]+)"', drawing_xml)
                        print("Image refs in drawing:", img_refs)

                        # Get the drawing rels
                        drawing_dir = "/".join(drawing_path.split("/")[:-1])
                        drawing_name = drawing_path.split("/")[-1]
                        drawing_rels = f"{drawing_dir}/_rels/{drawing_name}.rels"
                        if drawing_rels in z.namelist():
                            drels = z.read(drawing_rels).decode("utf-8")
                            img_files = re.findall(r'Target="\.\./(media/[^"]+)"', drels)
                            print("Actual image files:", img_files)
            else:
                print(f"Rels file not found: {rels_path}")
                # list all namelist entries with рация context
                matches = [n for n in z.namelist() if "worksheets" in n and "rels" in n]
                print("Available rels:", matches[-5:])
