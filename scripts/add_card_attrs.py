import re

html_path = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт\index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Women-oriented brands; everything else = unisex
WOMEN_BRANDS = {'Chanel', 'Miu Miu', 'Tiffany', 'Dior', 'Fendi',
                'Louis Vuitton', 'Balenciaga', 'Bvlgari', 'Celine'}

def get_gender(brand):
    return 'women' if brand in WOMEN_BRANDS else 'unisex'

def get_type(card_html):
    return 'optical' if 'Оправа' in card_html else 'sunglasses'

def get_price(card_html):
    m = re.search(r'от\s+([\d\s ]+)\s*₽', card_html)
    if m:
        val = int(re.sub(r'[\s ]', '', m.group(1)))
        if val < 50000:
            return 'low'
        elif val <= 100000:
            return 'mid'
        else:
            return 'high'
    return 'low'

count = 0

def process_card(m):
    global count
    card = m.group(0)
    if 'data-gender' in card:
        return card

    brand_m = re.search(r'class="brand-tag">([^<]+)<', card)
    brand = brand_m.group(1).strip() if brand_m else ''

    gender = get_gender(brand)
    type_ = get_type(card)
    price = get_price(card)

    card = re.sub(
        r'(<a\s+)(href="[^"]*"\s+target="_blank"\s+class="card")',
        rf'\1data-gender="{gender}" data-type="{type_}" data-price="{price}" \2',
        card, count=1
    )
    count += 1
    return card

html = re.sub(
    r'<a\s+href="[^"]*"\s+target="_blank"\s+class="card">.*?</a>',
    process_card,
    html,
    flags=re.DOTALL
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done: {count} cards tagged")
