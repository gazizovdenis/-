# -*- coding: utf-8 -*-
from faster_whisper import WhisperModel
import os

BASE = r'C:\Users\Denis\Desktop\Система\Хранилище\raw\08_Личное\Выводы дня\ChatExport_2026-05-26\voice_messages'
OUT = r'C:\Users\Denis\Desktop\Система\Хранилище\raw\08_Личное\Выводы дня\2026-05-26_выводы-дня_transcript.md'

files = [
    ('2026-05-17', 'audio_1@17-05-2026_22-40-37.ogg'),
    ('2026-05-18', 'audio_2@18-05-2026_23-10-10.ogg'),
    ('2026-05-24', 'audio_3@24-05-2026_20-28-16.ogg'),
    ('2026-05-25', 'audio_4@25-05-2026_22-23-32.ogg'),
]

print('Загружаю модель medium...', flush=True)
model = WhisperModel('medium', device='cpu', compute_type='int8')

result_blocks = []

for date, fname in files:
    path = os.path.join(BASE, fname)
    print(f'\nТранскрибирую {date} ({fname})...', flush=True)
    segments, info = model.transcribe(path, language='ru', beam_size=5)
    print(f'Длительность: {info.duration/60:.1f} мин', flush=True)

    lines = []
    for seg in segments:
        h = int(seg.start) // 3600
        m = (int(seg.start) % 3600) // 60
        s = int(seg.start) % 60
        line = f'[{h}:{m:02d}:{s:02d}] {seg.text.strip()}'
        lines.append(line)
        print(line, flush=True)

    result_blocks.append((date, info.duration, lines))

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('# Выводы дня — транскрипты\n\n')
    for date, duration, lines in result_blocks:
        f.write(f'## {date}\n\n')
        f.write(f'**Длительность:** {duration/60:.1f} мин\n\n')
        for line in lines:
            f.write(line + '\n')
        f.write('\n---\n\n')

print(f'\nDONE → {OUT}', flush=True)
