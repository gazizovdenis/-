import re

html_path = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт\index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

def format_price(val):
    s = str(val)
    if len(s) > 3:
        return s[:-3] + ' ' + s[-3:]
    return s

def new_price_str(match):
    raw = match.group(1).replace(' ', '')
    old = int(raw)
    new = round(old * 0.7 / 100) * 100
    return format_price(new) + ' ₽'

price_pattern = re.compile(r'от (\d[\d ]+) ₽')
count = len(price_pattern.findall(html))
print(f"Found {count} price entries")

html = price_pattern.sub(new_price_str, html)

# Verify no "от" remains before prices
remaining = len(re.findall(r'от \d', html))
print(f"Remaining 'от N' patterns: {remaining}")

# Update data-price attributes with new thresholds (low<35K, mid 35-70K, high>70K)
def reprice_attr(match):
    card = match.group(0)
    price_m = re.search(r'(\d[\d ]+) ₽', card)
    if price_m:
        val = int(price_m.group(1).replace(' ', ''))
        tier = 'low' if val < 35000 else ('mid' if val <= 70000 else 'high')
        card = re.sub(r'data-price="[^"]*"', f'data-price="{tier}"', card, count=1)
    return card

html = re.sub(r'<a data-gender="[^"]*"[^>]+class="card">.*?</a>', reprice_attr, html, flags=re.DOTALL)

# Update filter button labels
html = html.replace('>до 50К<', '>до 35К<')
html = html.replace('>50–70К<', '>35–70К<')
html = html.replace('>50–100К<', '>35–70К<')
html = html.replace('>100К+<', '>70К+<')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved.")
