import sys
sys.stdout.reconfigure(encoding='utf-8')

from fpdf import FPDF, FontFace

FONT_R  = r'C:\Windows\Fonts\arial.ttf'
FONT_B  = r'C:\Windows\Fonts\arialbd.ttf'
FONT_I  = r'C:\Windows\Fonts\ariali.ttf'
FONT_BI = r'C:\Windows\Fonts\arialbi.ttf'

def fmt(n):
    parts = f'{n:.2f}'.split('.')
    s, r = parts[0], ''
    for i, c in enumerate(reversed(s)):
        if i > 0 and i % 3 == 0:
            r = ' ' + r
        r = c + r
    return r + ',' + parts[1]

# === ДАННЫЕ ИЗ КП 2 + 10% ===
items = [
    {'num': 1, 'name': 'Накладки держателей бутылок UNIBLOC MOD VACUUM 40/40/8',                                                  'qty': 82,  'price': round(3850   * 1.1, 2)},
    {'num': 2, 'name': 'Накладки держателей бутылок инспекционной машины MOD.VISION 24',                                          'qty': 98,  'price': round(3850   * 1.1, 2)},
    {'num': 3, 'name': 'Столы донной ориентации для этикетировочного автомата Z-ADHESIVE 96/8T',                                  'qty': 17,  'price': round(12000  * 1.1, 2)},
    {'num': 4, 'name': 'Полный комплект оснастки системы подачи колпачков укупорочного автомата',                                 'qty': 1,   'price': round(418000 * 1.1, 2)},
    {'num': 5, 'name': 'Оснастка на укупорочный автомат (звездочка входная, рассекатель, звездочка выходная, шнек, кольцевая направляющая)', 'qty': 1, 'price': round(385000 * 1.1, 2)},
]
for it in items:
    it['sum'] = round(it['qty'] * it['price'], 2)

total   = round(sum(it['sum'] for it in items), 2)
vat     = round(total * 0.22, 2)
with_vat = round(total + vat, 2)

# === PDF ===
class KP(FPDF):
    def footer(self):
        pass

pdf = KP('P', 'mm', 'A4')
pdf.add_font('A',  '',  FONT_R)
pdf.add_font('A',  'B', FONT_B)
pdf.add_font('A',  'I', FONT_I)
pdf.add_font('A',  'BI',FONT_BI)
pdf.add_page()
pdf.set_margins(20, 15, 15)
pdf.set_auto_page_break(True, margin=20)

LM = pdf.l_margin  # 20
EW = 175           # 210 - 20 - 15
C1 = 108           # левая колонка шапки
C2 = EW - C1       # 67

# ─────────── ШАПКА ─────────────────────────────────────────────
hy = pdf.get_y()
r1h = 23   # высота 1-й строки шапки
r2h = 9    # высота 2-й строки шапки

# Рамки
pdf.set_draw_color(0, 0, 0)
pdf.set_line_width(0.3)
pdf.rect(LM, hy, EW, r1h + r2h)                         # внешняя
pdf.line(LM, hy + r1h, LM + EW, hy + r1h)               # горизонталь
pdf.line(LM + C1, hy, LM + C1, hy + r1h + r2h)          # вертикаль

# Левая верхняя: логотип
pdf.set_xy(LM + 3, hy + 2)
pdf.set_font('A', 'B', 15)
pdf.set_text_color(0, 120, 0)
pdf.cell(C1 - 4, 8, 'TECHNSPRODUCT', border=0)

pdf.set_xy(LM + 3, hy + 11)
pdf.set_font('A', 'I', 7)
pdf.set_text_color(60, 60, 60)
pdf.multi_cell(
    C1 - 4, 3.5,
    'Импорт промышленной автоматики, электроники и з/ч к\n'
    'оборудованию. Изготовление по чертежам.\n'
    'Услуги аккредитованного агента по закупкам',
    border=0
)

# Правая верхняя: реквизиты
pdf.set_xy(LM + C1 + 3, hy + 3)
pdf.set_font('A', 'B', 11)
pdf.set_text_color(0, 0, 0)
pdf.multi_cell(C2 - 4, 6, 'ООО «Технопродукт»', border=0, align='R')

pdf.set_xy(LM + C1 + 3, hy + 12)
pdf.set_font('A', 'B', 9)
pdf.multi_cell(C2 - 4, 5, 'ИНН/КПП: 0275914810/027501001', border=0, align='R')

# Вторая строка шапки (серый фон)
pdf.set_fill_color(242, 242, 242)
pdf.rect(LM, hy + r1h, C1, r2h, 'F')
pdf.rect(LM + C1, hy + r1h, C2, r2h, 'F')
pdf.set_text_color(0, 0, 0)

pdf.set_xy(LM + 3, hy + r1h + 2)
pdf.set_font('A', '', 9)
pdf.cell(C1 - 4, 5, 'Исх. №250 от 25.05.2026', border=0, align='C')

pdf.set_xy(LM + C1 + 3, hy + r1h + 2)
pdf.set_font('A', 'BI', 10)
pdf.cell(C2 - 4, 5, 'Для: АО "БАШСПИРТ"', border=0, align='C')

# ─────────── ЗАГОЛОВОК ─────────────────────────────────────────
pdf.set_xy(LM, hy + r1h + r2h + 6)
pdf.set_font('A', 'B', 15)
pdf.set_text_color(0, 0, 0)
pdf.cell(EW, 9, 'Коммерческое предложение', border=0, align='C', ln=True)

pdf.ln(3)
pdf.set_font('A', '', 10)
pdf.multi_cell(
    EW, 5,
    'Выражаем свою признательность за интерес к нашей компании, '
    'и сообщаем о возможности поставки продукции по следующим ценам:',
    border=0, align='C'
)
pdf.ln(4)

# ─────────── ОСНОВНАЯ ТАБЛИЦА ──────────────────────────────────
# Ширины столбцов: №, Наименование, Кол-во, Цена, Сумма, Срок
CW = [10, 72, 15, 26, 26, 26]  # sum = 175

head_style = FontFace(emphasis='BOLD', fill_color=(217, 217, 217))
gray_row   = FontFace(fill_color=(249, 249, 249))

pdf.set_font('A', '', 9)

with pdf.table(
    width=EW,
    col_widths=CW,
    line_height=5,
    text_align=('CENTER', 'LEFT', 'CENTER', 'RIGHT', 'RIGHT', 'CENTER'),
    borders_layout='ALL',
) as table:

    # Заголовок
    row = table.row()
    for txt, style in zip(
        ['No.', 'Наименование', 'Кол-во', 'Цена, руб\nбез НДС', 'Сумма, руб\nбез НДС', 'Срок\nпоставки\n(дней)'],
        [head_style] * 6
    ):
        row.cell(txt, style=style)

    # Данные
    for it in items:
        row = table.row()
        row.cell(str(it['num']))
        row.cell(it['name'])
        row.cell(str(it['qty']))
        row.cell(fmt(it['price']))
        row.cell(fmt(it['sum']))
        row.cell('')

    # Итоги
    sum_style  = FontFace(emphasis='BOLD')
    sum_labels = ['Сумма без НДС', 'НДС 22%', 'Сумма с НДС 22%']
    sum_values = [fmt(total), fmt(vat), fmt(with_vat)]
    for label, value in zip(sum_labels, sum_values):
        row = table.row()
        row.cell(label, colspan=5, style=sum_style, align='RIGHT')
        row.cell(value, style=sum_style)

pdf.ln(5)

# ─────────── УСЛОВИЯ ───────────────────────────────────────────
pdf.set_font('A', '', 10)
for line in [
    'Цены указаны с учетом стоимости доставки.',
    'Условия оплаты: 50% предоплата, 50% по факту поставки',
    'Срок поставки: До 14 дней',
]:
    pdf.cell(EW, 5.5, line, ln=True)

pdf.ln(5)

# ─────────── ИСПОЛНИТЕЛЬ ───────────────────────────────────────
pdf.cell(EW, 5.5, 'Исполнитель: Салават Шигабутдинов  +7 960 384 00 16', ln=True)
pdf.cell(EW, 5.5, 'e-mail: sh.salavat@tehnoprod.ru', ln=True)
pdf.ln(8)

# ─────────── ДИРЕКТОР ──────────────────────────────────────────
pdf.cell(30, 5.5, 'Директор', border=0)
pdf.cell(85, 5.5, '', border=0)
pdf.cell(60, 5.5, 'Газизов Д.Р', border=0, ln=True)
pdf.ln(8)

# ─────────── ПОДВАЛ ────────────────────────────────────────────
pdf.set_font('A', 'B', 10)
pdf.cell(EW, 5.5, 'Оперативно обработаем ваши заявки', ln=True, align='C')
pdf.set_font('A', 'B', 11)
pdf.cell(EW, 6, 'эл.почта: sh.salavat@tehnoprod.ru', ln=True, align='C')
pdf.ln(4)

# ─────────── ПРЕИМУЩЕСТВА ──────────────────────────────────────
pdf.set_font('A', 'B', 8)
pdf.cell(EW, 4.5, 'Технопродукт', ln=True)
pdf.set_font('A', '', 8)
for adv in [
    'НАДЕЖНОСТЬ: более 5 лет на рынке, долгосрочные контракты с крупнейшими компаниями РФ',
    'ПЕРСОНАЛЬНОЕ ОБСЛУЖИВАНИЕ: закреплённый менеджер ведёт заявку от приёма до отгрузки',
    'СРОК ОТВЕТА 2-3 ДНЯ: налаженный опыт с зарубежными производителями и поставщиками',
    'ОПТИМАЛЬНЫЕ ЦЕНЫ: оптовые закупки позволяют сокращать издержки логистики и платежей',
]:
    pdf.cell(4, 4, '>', border=0)
    pdf.multi_cell(EW - 4, 4, adv, border=0)

# ─────────── СОХРАНЕНИЕ ────────────────────────────────────────
out = r'Хранилище/raw/02_Технопродукт/КП/КП_на_основе_КП2_цена_плюс_10.pdf'
pdf.output(out)

print(f'PDF сохранён: {out}')
print(f'Позиций: {len(items)}')
print(f'Сумма без НДС:  {fmt(total)} руб.')
print(f'НДС 22%:        {fmt(vat)} руб.')
print(f'Сумма с НДС:    {fmt(with_vat)} руб.')
