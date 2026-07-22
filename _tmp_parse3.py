import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

path = r"C:\Users\Denis\.claude\projects\c--Users-Denis-Desktop--------\1fe30397-edde-49bd-b3f9-87fa47acc811\tool-results\mcp-claude_ai_Google_Drive-read_file_content-1781502855064.txt"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

content = data["fileContent"]
lines = content.split("\n")

# Find all product rows: they have a category + product name + pricing data
# Pattern: line has a category (like "Швабры") AND naименование AND pricing
current_niche = None
products = []
for i, line in enumerate(lines):
    if "| :-:" in line or line.strip() == "":
        continue
    cells = [c.strip() for c in line.split("|") if c.strip()]
    if not cells:
        continue
    # Niche line: contains "/"
    if len(cells) > 5 and "/" in cells[0] and "₽" not in cells[0] and "http" not in cells[0]:
        current_niche = cells[0]
    # Product line: second cell is category, third is name, then pricing numbers
    # Check if it has a price value (contains "₽" or just numbers in cols 3-5)
    elif len(cells) >= 5 and current_niche:
        # Skip header rows
        if "себестоимость" in cells[0].lower() or "наименование" in cells[0].lower() or "Название" in cells[0]:
            continue
        # Try to identify product row: cells[1] or cells[2] looks like a product name
        cat = cells[0] if len(cells) > 0 else ""
        name = cells[1] if len(cells) > 1 else ""
        price_cn = cells[2] if len(cells) > 2 else ""
        price_msk = cells[3] if len(cells) > 3 else ""
        retail = cells[4] if len(cells) > 4 else ""
        commission = cells[5] if len(cells) > 5 else ""
        logistics = cells[6] if len(cells) > 6 else ""
        profit = cells[10] if len(cells) > 10 else ""
        profit_pct = cells[11] if len(cells) > 11 else ""

        # Filter: if profit looks like a number
        if any(c.isdigit() for c in profit) or any(c.isdigit() for c in retail):
            products.append({
                "niche": current_niche,
                "cat": cat,
                "name": name[:60],
                "price_cn": price_cn[:20],
                "price_msk": price_msk[:15],
                "retail": retail[:15],
                "commission": commission[:10],
                "logistics": logistics[:10],
                "profit": profit[:15],
                "profit_pct": profit_pct[:10],
                "line": i
            })

print("=== Все найденные товары ===")
for p in products:
    print(f"L{p['line']}: [{p['niche'][:50]}]")
    print(f"  Товар: {p['cat']} / {p['name']}")
    print(f"  Китай: {p['price_cn']} | МСК: {p['price_msk']} | Розница: {p['retail']} | Прибыль: {p['profit']} ({p['profit_pct']}%)")
    print()
