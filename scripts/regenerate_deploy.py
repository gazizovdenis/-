import re, os

src = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт\index.html"
dst = r"C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Сайт_Netlify\index.html"

with open(src, 'r', encoding='utf-8') as f:
    html = f.read()

before = html.count('src="')
print(f"Total src= before: {before}")

# Replace local image paths: src="PATH.ext" -> src="images/PATH.webp"
# (skip https:// and already-prefixed images/)
html = re.sub(
    r'src="(?!https?://)(?!images/)([^"]+)\.(png|jpg|jpeg)"',
    r'src="images/\1.webp"',
    html,
    flags=re.IGNORECASE
)

after_local = html.count('src="images/')
print(f"Local paths converted: {after_local}")

# Add loading=lazy to img tags that don't already have it
html = re.sub(r'<img (?!loading)', '<img loading="lazy" ', html)

with open(dst, 'w', encoding='utf-8') as f:
    f.write(html)

# Verify
sample = re.findall(r'src="images/[^"]+"', html)[:3]
for s in sample:
    print(' ', s[:80])

print("Done.")
