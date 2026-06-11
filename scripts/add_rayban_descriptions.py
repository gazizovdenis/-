html_path = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт\index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ===== 1. CSS =====
css_anchor = '        .model-group::after { content: \'\'; flex: 1; height: 1px; background: #f4f4f4; }'
css_new = '\n        .model-desc { grid-column: 1 / -1; padding: 0 2px 20px; color: #999; font-size: 13px; line-height: 1.65; max-width: 560px; }'

if '.model-desc' not in html:
    html = html.replace(css_anchor, css_anchor + css_new)
    print("CSS added")

# Mobile override
mobile_anchor = '            .brand-section { padding: 36px 0 12px; }'
mobile_new = '\n            .model-desc { font-size: 12px; padding-bottom: 14px; }'
if mobile_anchor in html and '.model-desc { font-size: 12px' not in html:
    html = html.replace(mobile_anchor, mobile_anchor + mobile_new)
    print("CSS mobile added")

# ===== 2. Описания =====
DESCRIPTIONS = {
    'rb-aviator': (
        'Классика с 1937 года — созданы для лётчиков ВВС США. '
        'Тонкая металлическая оправа, каплевидные линзы. '
        'Подходят для овального, квадратного и сердцевидного лица.'
    ),
    'rb-wayfarer': (
        'Самые культовые очки в истории — с 1952 года. '
        'Трапециевидная ацетатная оправа, которую носили от Одри Хепберн до Боба Дилана. '
        'Универсальны для большинства форм лица.'
    ),
    'rb-reverse': (
        'Авторская технология Ray-Ban: линзы выступают вперёд за оправу, создавая объёмный 3D-эффект. '
        'Три формы — Aviator, Caravan и Round. '
        'Металлические оправы ручной сборки.'
    ),
    'rb-new-wayfarer': (
        'Обновлённый Wayfarer с более мягкими линиями и меньшим углом наклона. '
        'Легче сидит на лице и подходит большему числу форм лица, чем классика.'
    ),
    'rb-mega-wayfarer': (
        'Увеличенная версия Wayfarer с широкими линзами и насыщенным ацетатом. '
        'Современная интерпретация иконы — для тех, кто выбирает заметный образ.'
    ),
    'rb-round-metal': (
        'Круглые металлические оправы в стиле 60-х. '
        'Тонкий профиль и изящная посадка. '
        'Хорошо балансируют квадратные и прямоугольные черты лица.'
    ),
    'rb-drifter': (
        'Клубная форма с комбинированной оправой: металлический обод и ацетатные дужки. '
        'Плоские широкие линзы, геометричный силуэт.'
    ),
}

for group_id, text in DESCRIPTIONS.items():
    anchor = f'<div class="model-group" id="{group_id}"><span>'
    desc_block = f'\n<div class="model-desc">{text}</div>'

    # Find end of this model-group line and insert desc after it
    idx = html.find(anchor)
    if idx == -1:
        print(f"NOT FOUND: {group_id}")
        continue

    # Find end of this line (closing </div>)
    end = html.index('\n', idx)
    if 'model-desc' in html[end:end+40]:
        print(f"SKIP (already exists): {group_id}")
        continue

    html = html[:end] + desc_block + html[end:]
    print(f"Added: {group_id}")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("\nDone. Saved.")
