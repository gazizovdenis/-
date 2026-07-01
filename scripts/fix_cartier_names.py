import re

html_path = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт\index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ===== ISSUE 1: CTO (letter O) → CT0 (digit) in display text =====
# Safe: src paths use "CTO 468 S" (space before S), display uses "CTO 468S" (no space)

display_fixes = [
    ('CTO 468S',    'CT0468S'),
    ('CTO%20468S',  'CT0468S'),
    ('CTO 888S',    'CT0888S'),
    ('CTO%20888S',  'CT0888S'),
    ('CTO 889S',    'CT0889S'),
    ('CTO%20889S',  'CT0889S'),
    ('CTO 897S',    'CT0897S'),
    ('CTO%20897S',  'CT0897S'),
]

for old, new in display_fixes:
    count = html.count(old)
    html = html.replace(old, new)
    print(f"[1] {old!r:30} -> {new!r:15} ({count}x)")

# ===== ISSUE 2: Duplicate "Transparent Brown/Gold" in CT0711SA and CT0712SA =====
# Rename SUNGLASSES versions → "Transparent Brown/Gold/Brown"
# Anchor: unique img src for each sunglasses card

# CT0711SA sunglasses: src="Очки 3/CTO 711 SA (1)/1 (1).png"
fixes_711 = [
    # alt text (unique: Солнцезащитные + CT0711SA in same string)
    (
        'alt="Cartier CT0711SA Transparent Brown/Gold · Солнцезащитные"',
        'alt="Cartier CT0711SA Transparent Brown/Gold/Brown · Солнцезащитные"',
    ),
    # overlay p (unique: CT0711SA + Солнцезащитные)
    (
        '<h3>CT0711SA</h3><p>Transparent Brown/Gold · Солнцезащитные</p>',
        '<h3>CT0711SA</h3><p>Transparent Brown/Gold/Brown · Солнцезащитные</p>',
    ),
    # href: anchor via href + next img src on same card (consecutive lines)
    (
        'text=Хочу%20заказать%20Cartier%20CT0711SA%20Transparent%20Brown/Gold" target="_blank" class="card">\n<img loading="lazy" src="Очки 3/CTO 711 SA (1)/1 (1).png"',
        'text=Хочу%20заказать%20Cartier%20CT0711SA%20Transparent%20Brown/Gold/Brown" target="_blank" class="card">\n<img loading="lazy" src="Очки 3/CTO 711 SA (1)/1 (1).png"',
    ),
]

for old, new in fixes_711:
    count = html.count(old)
    html = html.replace(old, new)
    print(f"[2-711] ({count}x): ...{old[-40:]!r}")

# card-footer sub for CT0711SA sunglasses via regex (src→sub within same card)
pattern_711 = r'(src="Очки 3/CTO 711 SA \(1\)/1 \(1\)\.png".*?<div class="sub">)Transparent Brown/Gold(</div>)'
new_val, n = re.subn(pattern_711, r'\1Transparent Brown/Gold/Brown\2', html, flags=re.DOTALL)
html = new_val
print(f"[2-711-sub] regex sub: {n}x")

# CT0712SA sunglasses: src="Очки 3/CTO 712 SA (1)/1 (5).png"
fixes_712 = [
    (
        'alt="Cartier CT0712SA Transparent Brown/Gold · Солнцезащитные"',
        'alt="Cartier CT0712SA Transparent Brown/Gold/Brown · Солнцезащитные"',
    ),
    (
        '<h3>CT0712SA</h3><p>Transparent Brown/Gold · Солнцезащитные</p>',
        '<h3>CT0712SA</h3><p>Transparent Brown/Gold/Brown · Солнцезащитные</p>',
    ),
    (
        'text=Хочу%20заказать%20Cartier%20CT0712SA%20Transparent%20Brown/Gold" target="_blank" class="card">\n<img loading="lazy" src="Очки 3/CTO 712 SA (1)/1 (5).png"',
        'text=Хочу%20заказать%20Cartier%20CT0712SA%20Transparent%20Brown/Gold/Brown" target="_blank" class="card">\n<img loading="lazy" src="Очки 3/CTO 712 SA (1)/1 (5).png"',
    ),
]

for old, new in fixes_712:
    count = html.count(old)
    html = html.replace(old, new)
    print(f"[2-712] ({count}x): ...{old[-40:]!r}")

pattern_712 = r'(src="Очки 3/CTO 712 SA \(1\)/1 \(5\)\.png".*?<div class="sub">)Transparent Brown/Gold(</div>)'
new_val, n = re.subn(pattern_712, r'\1Transparent Brown/Gold/Brown\2', html, flags=re.DOTALL)
html = new_val
print(f"[2-712-sub] regex sub: {n}x")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("\nDone. Saved to index.html")
