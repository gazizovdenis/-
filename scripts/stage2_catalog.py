import re

html_path = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт\index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

CARD_RE = re.compile(r'<a\s+data-gender="[^"]*"[^>]+class="card">.*?</a>', re.DOTALL)

# ======================================================
# PART 1: Хиты — first card per brand
# ======================================================
BRANDS = [
    'Ray-Ban', 'Gucci', 'Chanel', 'Prada', 'Cartier', 'Saint Laurent',
    'Miu Miu', 'Dior', 'Tom Ford', 'Tiffany', 'Bvlgari', 'Balenciaga',
    'Louis Vuitton', 'Fendi', 'Burberry', 'Giorgio Armani', 'Gentle Monster', 'Celine',
]

hits = []
for brand in BRANDS:
    for m in CARD_RE.finditer(html):
        card = m.group(0)
        bt = re.search(r'class="brand-tag">([^<]+)<', card)
        if bt:
            cb = bt.group(1).strip().replace('&amp;', '&')
            if cb == brand or cb.startswith(brand):
                hits.append(card)
                break

print(f"Hits: {len(hits)} cards")
for c in hits:
    bt = re.search(r'class="brand-tag">([^<]+)<', c)
    h3 = re.search(r'<h3>([^<]+)</h3>', c)
    print(f"  {bt.group(1) if bt else '?'}: {h3.group(1) if h3 else '?'}")

hits_html = '<div class="brand-section" id="hits"><span>Хиты</span></div>\n'
hits_html += '\n'.join(hits) + '\n'

# ======================================================
# PART 2: Ray-Ban — regroup by form
# ======================================================
rb_start  = html.index('<div class="brand-section" id="ray-ban">')
gc_start  = html.index('<div class="brand-section" id="gucci">')
rb_block  = html[rb_start:gc_start]

FORM_MAP = [
    (['RB3025', 'RB3026'],              'Aviator'),
    (['RB2140'],                         'Wayfarer'),
    (['RB2132'],                         'New Wayfarer'),
    (['RB0840S'],                        'Mega Wayfarer'),
    (['RB3447'],                         'Round Metal'),
    (['RB4432'],                         'Drifter'),
    (['RBR'],                            'Reverse'),
]

def form_of(card):
    h3 = re.search(r'<h3>([^<]+)</h3>', card)
    model = h3.group(1) if h3 else ''
    for keys, form in FORM_MAP:
        for k in keys:
            if k in model:
                return form
    return 'Другие'

groups, order = {}, []
for m in CARD_RE.finditer(rb_block):
    card = m.group(0)
    f = form_of(card)
    if f not in groups:
        groups[f] = []
        order.append(f)
    groups[f].append(card)

print(f"\nRay-Ban groups:")
for f in order:
    print(f"  {f}: {len(groups[f])} cards")

new_rb = '<div class="brand-section" id="ray-ban"><span>Ray-Ban</span></div>\n'
for f in order:
    fid = 'rb-' + f.lower().replace(' ', '-')
    new_rb += f'<div class="model-group" id="{fid}"><span>{f}</span></div>\n'
    new_rb += '\n'.join(groups[f]) + '\n'

# ======================================================
# Apply changes
# ======================================================
# Replace Ray-Ban block (without Gucci+)
html = html[:rb_start] + new_rb + html[gc_start:]

# Insert Хиты before Ray-Ban
rb_pos = html.index('<div class="brand-section" id="ray-ban">')
html = html[:rb_pos] + hits_html + '\n' + html[rb_pos:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("\nDone.")
