# -*- coding: utf-8 -*-
"""
Универсальный транскрибатор аудио.

Использование:
  python transcribe.py <audio1.m4a> [audio2.m4a ...] [--out-dir DIR] [--engine local|openai] [--model small|medium|large] [--openai-key sk-...]

Примеры:
  # Вариант 1 — локально, быстро (small + beam=1):
  python transcribe.py встреча.m4a

  # Вариант 2 — через OpenAI API:
  python transcribe.py встреча.m4a --engine openai --openai-key sk-...

  # Несколько файлов в папку:
  python transcribe.py *.m4a --out-dir C:\\папка\\с\\транскриптами
"""

import argparse
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def timestamp(seconds: float) -> str:
    h = int(seconds) // 3600
    m = (int(seconds) % 3600) // 60
    s = int(seconds) % 60
    return f'[{h}:{m:02d}:{s:02d}]'


def transcribe_local(audio_path: Path, model_name: str) -> list[dict]:
    from faster_whisper import WhisperModel
    print(f'  Загружаю модель {model_name}...', flush=True)
    model = WhisperModel(model_name, device='cpu', compute_type='int8')
    print(f'  Транскрибирую...', flush=True)
    segments, info = model.transcribe(str(audio_path), language='ru', beam_size=1)
    print(f'  Длительность: {info.duration/60:.1f} мин', flush=True)
    result = []
    for seg in segments:
        line = f'{timestamp(seg.start)} {seg.text.strip()}'
        result.append({'ts': seg.start, 'text': line})
        print(line, flush=True)
    return result, info.duration


def transcribe_openai(audio_path: Path, api_key: str) -> list[dict]:
    from openai import OpenAI
    import json

    client = OpenAI(api_key=api_key)
    print(f'  Отправляю в OpenAI Whisper API...', flush=True)

    with open(audio_path, 'rb') as f:
        response = client.audio.transcriptions.create(
            model='whisper-1',
            file=f,
            language='ru',
            response_format='verbose_json',
            timestamp_granularities=['segment'],
        )

    duration = response.duration
    print(f'  Длительность: {duration/60:.1f} мин', flush=True)
    result = []
    for seg in response.segments:
        line = f'{timestamp(seg.start)} {seg.text.strip()}'
        result.append({'ts': seg.start, 'text': line})
        print(line, flush=True)
    return result, duration


def save_transcript(segments, duration: float, audio_path: Path, out_path: Path):
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(f'# {audio_path.stem}\n\n')
        f.write(f'**Длительность:** {duration/60:.1f} мин\n\n')
        f.write('---\n\n')
        for seg in segments:
            f.write(seg['text'] + '\n')
    print(f'  Сохранено: {out_path}', flush=True)


def main():
    parser = argparse.ArgumentParser(description='Транскрибация аудио')
    parser.add_argument('files', nargs='+', help='Аудиофайлы (.m4a, .mp3, .wav, ...)')
    parser.add_argument('--out-dir', help='Папка для транскриптов (по умолчанию — рядом с аудио)')
    parser.add_argument('--engine', choices=['local', 'openai'], default='local',
                        help='local = faster-whisper (по умолчанию), openai = OpenAI API')
    parser.add_argument('--model', default='small',
                        help='Модель для local: tiny/base/small/medium/large (по умолчанию: small)')
    parser.add_argument('--openai-key', help='OpenAI API ключ (или переменная OPENAI_API_KEY)')
    args = parser.parse_args()

    openai_key = args.openai_key or os.environ.get('OPENAI_API_KEY')
    if args.engine == 'openai' and not openai_key:
        print('Ошибка: нужен OpenAI API ключ (--openai-key или $OPENAI_API_KEY)', file=sys.stderr)
        sys.exit(1)

    # Загружаем локальную модель один раз для всех файлов
    local_model = None
    if args.engine == 'local':
        from faster_whisper import WhisperModel
        print(f'Загружаю модель {args.model}...', flush=True)
        local_model = WhisperModel(args.model, device='cpu', compute_type='int8')

    for file_str in args.files:
        audio_path = Path(file_str)
        if not audio_path.exists():
            print(f'[SKIP] Файл не найден: {audio_path}', flush=True)
            continue

        out_dir = Path(args.out_dir) if args.out_dir else audio_path.parent
        out_path = out_dir / (audio_path.stem + '_transcript.md')

        if out_path.exists():
            print(f'[SKIP] {audio_path.name} — транскрипт уже есть', flush=True)
            continue

        print(f'\n=== {audio_path.name} ===', flush=True)

        if args.engine == 'local':
            from faster_whisper import WhisperModel

            def _transcribe(path):
                segs, info = local_model.transcribe(str(path), language='ru', beam_size=1)
                result = []
                for seg in segs:
                    line = f'{timestamp(seg.start)} {seg.text.strip()}'
                    result.append({'ts': seg.start, 'text': line})
                    print(line, flush=True)
                return result, info.duration

            segments, duration = _transcribe(audio_path)
        else:
            segments, duration = transcribe_openai(audio_path, openai_key)

        save_transcript(segments, duration, audio_path, out_path)

    print('\nВсё готово!', flush=True)


if __name__ == '__main__':
    main()
