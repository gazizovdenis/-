"""Конвертация markdown в PDF через fpdf2."""
import re
import sys
from pathlib import Path
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", size=8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"{self.page_no()}", align="C")


def parse_and_render(pdf: PDF, md_text: str):
    lines = md_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        # Горизонтальная линия
        if re.match(r"^-{3,}$", line.strip()):
            pdf.set_draw_color(180, 180, 180)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, pdf.get_y() + 2, pdf.w - pdf.r_margin, pdf.get_y() + 2)
            pdf.ln(6)
            i += 1
            continue

        # Таблица
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[-| :]+\|$", lines[i]):
                    cells = [c.strip() for c in lines[i].strip("|").split("|")]
                    rows.append(cells)
                i += 1
            if rows:
                render_table(pdf, rows)
            pdf.ln(4)
            continue

        # Заголовки
        if line.startswith("# "):
            pdf.set_font("DejaVuB", size=16)
            pdf.set_text_color(20, 20, 20)
            pdf.multi_cell(0, 8, line[2:].strip())
            pdf.set_draw_color(50, 50, 50)
            pdf.set_line_width(0.5)
            pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
            pdf.ln(6)
        elif line.startswith("## "):
            pdf.set_font("DejaVuB", size=13)
            pdf.set_text_color(30, 30, 30)
            pdf.ln(3)
            pdf.multi_cell(0, 7, line[3:].strip())
            pdf.set_draw_color(180, 180, 180)
            pdf.set_line_width(0.3)
            pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
            pdf.ln(4)
        elif line.startswith("### "):
            pdf.set_font("DejaVuB", size=11)
            pdf.set_text_color(60, 60, 60)
            pdf.ln(2)
            pdf.multi_cell(0, 6, line[4:].strip())
            pdf.ln(2)
        # Список
        elif re.match(r"^[-*] ", line):
            text = line[2:].strip()
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
            pdf.set_font("DejaVu", size=10)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(pdf.l_margin + 4)
            pdf.multi_cell(0, 5.5, f"• {text}", new_x="LMARGIN")
            pdf.ln(1)
        # Пустая строка
        elif line.strip() == "":
            pdf.ln(2)
        # Курсив (мета-строка источника)
        elif line.startswith("*") and line.endswith("*"):
            pdf.set_font("DejaVuI", size=8)
            pdf.set_text_color(140, 140, 140)
            pdf.multi_cell(0, 5, line.strip("*").strip())
            pdf.ln(1)
        # Обычный текст
        else:
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", line)
            pdf.set_font("DejaVu", size=10)
            pdf.set_text_color(30, 30, 30)
            pdf.multi_cell(0, 5.5, text)
            pdf.ln(1)

        i += 1


def render_table(pdf: PDF, rows: list[list[str]]):
    col_count = max(len(r) for r in rows)
    usable_w = pdf.w - pdf.l_margin - pdf.r_margin

    # Ширины колонок
    col_widths = [usable_w / col_count] * col_count
    if col_count == 4:
        col_widths = [8, 60, 40, 30]
        total = sum(col_widths)
        col_widths = [w / total * usable_w for w in col_widths]

    for ri, row in enumerate(rows):
        is_header = ri == 0
        if is_header:
            pdf.set_fill_color(230, 230, 230)
            pdf.set_font("DejaVuB", size=9)
        else:
            pdf.set_fill_color(250, 250, 250) if ri % 2 == 0 else pdf.set_fill_color(255, 255, 255)
            pdf.set_font("DejaVu", size=9)

        pdf.set_text_color(20, 20, 20)
        pdf.set_draw_color(180, 180, 180)

        # Высота строки по максимуму содержимого
        row_h = 5.5
        x0, y0 = pdf.get_x(), pdf.get_y()

        for ci, cell in enumerate(row[:col_count]):
            text = re.sub(r"\*\*(.+?)\*\*", r"\1", cell.strip())
            w = col_widths[ci]
            pdf.set_xy(x0 + sum(col_widths[:ci]), y0)
            pdf.multi_cell(w, row_h, text, border=1, fill=True, new_x="RIGHT", new_y="TOP")

        # Сдвигаем Y вниз на высоту строки
        pdf.set_xy(pdf.l_margin, y0 + row_h)


def main():
    if len(sys.argv) < 2:
        print("Использование: python md_to_pdf.py <file.md>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    pdf_path = md_path.with_suffix(".pdf")
    md_text = md_path.read_text(encoding="utf-8")

    pdf = PDF(format="A4")
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=15)

    # Шрифт с поддержкой кириллицы (системный Arial)
    fonts = Path("C:/Windows/Fonts")
    pdf.add_font("DejaVu", style="", fname=str(fonts / "arial.ttf"))
    pdf.add_font("DejaVuB", style="", fname=str(fonts / "arialbd.ttf"))
    pdf.add_font("DejaVuI", style="", fname=str(fonts / "ariali.ttf"))

    pdf.add_page()
    parse_and_render(pdf, md_text)

    pdf.output(str(pdf_path))
    print(f"PDF создан: {pdf_path}")


if __name__ == "__main__":
    main()
