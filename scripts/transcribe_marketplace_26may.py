# -*- coding: utf-8 -*-
import sys
from faster_whisper import WhisperModel
from pathlib import Path

BASE_DIR = Path(r'C:\Users\Denis\Desktop\Система\Хранилище\raw\01_Маркетплейс\Встречи')

FILES = [
    ('26.05.2026 встреча 1.m4a', '2026-05-26_встреча-маркетплейс-1'),
    ('26.05.2026 встреча 2.m4a', '2026-05-26_встреча-маркетплейс-2'),
    ('26.05.2026 встреча 3.m4a', '2026-05-26_встреча-маркетплейс-3'),
    ('26.05.2026 встреча 4.m4a', '2026-05-26_встреча-маркетплейс-4'),
]

print('Загружаю модель medium...', flush=True)
model = WhisperModel('medium', device='cpu', compute_type='int8')

for audio_name, slug in FILES:
    audio_path = BASE_DIR / audio_name
    out_path = BASE_DIR / f'{slug}_transcript.md'

    if out_path.exists():
        print(f'[SKIP] {slug} — уже есть', flush=True)
        continue

    print(f'\n=== {audio_name} ===', flush=True)
    segments, info = model.transcribe(str(audio_path), language='ru', beam_size=5)
    print(f'Длительность: {info.duration/60:.1f} мин', flush=True)

    lines = []
    for seg in segments:
        h = int(seg.start) // 3600
        m = (int(seg.start) % 3600) // 60
        s = int(seg.start) % 60
        line = f'[{h}:{m:02d}:{s:02d}] {seg.text.strip()}'
        lines.append(line)
        print(line, flush=True)

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f'# {audio_name.replace(".m4a","")}\n\n')
        f.write(f'**Длительность:** {info.duration/60:.1f} мин\n\n')
        f.write('---\n\n')
        for line in lines:
            f.write(line + '\n')

    print(f'Сохранено: {out_path}', flush=True)

print('\nВсё готово!', flush=True)
