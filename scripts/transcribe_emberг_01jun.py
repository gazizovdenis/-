# -*- coding: utf-8 -*-
audio = r'C:\Users\Denis\Desktop\Система\Хранилище\raw\02_Технопродукт\Встречи\01.06.26 Эмберг.m4a'
out_path = r'C:\Users\Denis\Desktop\Система\Хранилище\raw\02_Технопродукт\Встречи\2026-06-01_Эмберг_transcript.md'

print('Загружаю модель medium...', flush=True)
from faster_whisper import WhisperModel
model = WhisperModel('medium', device='cpu', compute_type='int8')
print('Транскрибирую...', flush=True)

segments, info = model.transcribe(audio, language='ru', beam_size=5)
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
    f.write('# Созвон с Эмбергом — 01.06.2026\n\n')
    f.write(f'**Длительность:** {info.duration/60:.1f} мин\n\n')
    f.write('---\n\n')
    for line in lines:
        f.write(line + '\n')

print('DONE', flush=True)
