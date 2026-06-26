---
name: diarize-setup
description: "Настройка диаризации аудио по голосам — скрипт, skill, инструменты"
metadata: 
  node_type: memory
  type: project
  originSessionId: 109e517e-fa00-4290-923e-dcf959de79c6
---

Диаризация настроена через pyannote.audio (speaker-diarization-3.1).

**Скрипт:** `c:\Users\Denis\Desktop\Система\scripts\diarize.py`
**Skill:** `skills/diarize-media/SKILL.md`

**Запуск:**
```
python "c:\Users\Denis\Desktop\Система\scripts\diarize.py" "<путь_к_аудио>" --token <hf_token> --speakers N
```

**Зависимости:** pyannote.audio, soundfile, ffmpeg (для m4a → wav конвертации)

**HuggingFace:** Условия для pyannote/speaker-diarization-3.1 приняты (2026-05-18).
**Токен:** HuggingFace token сохранён локально в переменной окружения HF_TOKEN (не коммитить)

**Результат:** `_diarized.md` рядом с транскриптом. Метки SPEAKER_00/01/... нужно вручную заменить на имена.

**Why:** whisperx несовместим с Python 3.14, поэтому используем pyannote напрямую.
**How to apply:** При запросах "разделить по голосам" / "диаризация" — использовать этот скрипт.
