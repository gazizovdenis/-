#!/usr/bin/env bash
# Конвертирует HTML-презентацию в PDF (16:9 = 13.333" × 7.5") через Chrome headless.
# Использование: ./html_to_pdf.sh <absolute_path_to_html> [output_pdf_path]

set -e

HTML="$1"
PDF="${2:-${HTML%.html}.pdf}"

if [ -z "$HTML" ] || [ ! -f "$HTML" ]; then
  echo "Ошибка: HTML-файл не найден: $HTML" >&2
  exit 1
fi

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
if [ ! -x "$CHROME" ]; then
  # fallback варианты
  for alt in \
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"; do
    if [ -x "$alt" ]; then CHROME="$alt"; break; fi
  done
fi

if [ ! -x "$CHROME" ]; then
  echo "Не найден Chrome/Chromium для headless-печати. Установи Google Chrome или сохрани PDF вручную: открой HTML и Cmd+P → Save as PDF (размер 13.333×7.5 in)." >&2
  exit 2
fi

# file:// URL c корректным экранированием пробелов
URL="file://$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$HTML")"

"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-pdf-header-footer \
  --hide-scrollbars \
  --virtual-time-budget=10000 \
  --print-to-pdf="$PDF" \
  --print-to-pdf-no-header \
  "$URL" 2>/dev/null

if [ -f "$PDF" ]; then
  echo "OK: $PDF"
else
  echo "Ошибка генерации PDF" >&2
  exit 3
fi
