import re

html_path = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт\index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ===== 1. CSS — добавить .card-specs после .card-footer .sub =====
css_after = '        .card-footer .sub { font-size: 11px; color: #aaa; margin-top: 3px; }'
css_insert = '\n        .card-specs { font-size: 10px; color: #bbb; margin: 2px 0 4px; letter-spacing: 0.2px; }'

if '.card-specs' not in html:
    html = html.replace(css_after, css_after + css_insert)
    print("CSS desktop added")

# mobile override
mobile_after = '            .card-footer .sub { font-size: 9px; }'
mobile_insert = '\n            .card-specs { font-size: 8px; }'
if mobile_after in html and '.card-specs { font-size: 8px' not in html:
    html = html.replace(mobile_after, mobile_after + mobile_insert)
    print("CSS mobile added")

# ===== 2. Specs map =====
SPECS = {
    'RB3025 Aviator':           'Металл · 58 мм',
    'RB3026 Aviator Large':     'Металл · 62 мм',
    'RB2140 Wayfarer':          'Ацетат · 50–54 мм',
    'RBR0101S Aviator Reverse': 'Металл · Перевёрнутые линзы',
    'RBR0102S Caravan Reverse': 'Металл · Перевёрнутые линзы',
    'RBR0103S Round Reverse':   'Металл · Перевёрнутые линзы',
    'RBR0501S Reverse':         'Ацетат · Перевёрнутые линзы',
    'RBR0502S Reverse':         'Ацетат · Перевёрнутые линзы',
    'RB2132 New Wayfarer':      'Ацетат · 52–55 мм',
    'RB0840S Mega Wayfarer':    'Ацетат · 51 мм',
    'RB3447 Round Metal':       'Металл · 47–50 мм',
    'RB4432 Drifter':           'Металл + Ацетат · 52 мм',
}

total = 0
for model, specs in SPECS.items():
    old = f'<div class="brand-tag">Ray-Ban</div><h3>{model}</h3><div class="sub">'
    new = f'<div class="brand-tag">Ray-Ban</div><h3>{model}</h3><div class="card-specs">{specs}</div><div class="sub">'
    count = html.count(old)
    if count:
        html = html.replace(old, new)
        total += count
        print(f"  {model}: {count}x")
    else:
        print(f"  NOT FOUND: {model}")

print(f"\nTotal cards updated: {total}")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved.")
