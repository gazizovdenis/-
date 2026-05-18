"""
Диаризация аудио: разделение по спикерам + наложение на транскрипт Whisper.

Использование:
  python diarize.py <audio_file> [--transcript <transcript.md>] [--token <hf_token>] [--speakers N]

Результат сохраняется рядом с транскриптом (или аудио) с суффиксом _diarized.md
"""

import argparse
import os
import re
import sys
from pathlib import Path


def load_transcript_segments(transcript_path: str) -> list[dict]:
    """Парсит таймкоды из markdown-транскрипта faster-whisper."""
    segments = []
    pattern = re.compile(r"\[(\d+):(\d+):(\d+)\]\s*(.*)")
    with open(transcript_path, encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                h, mn, s, text = m.groups()
                start = int(h) * 3600 + int(mn) * 60 + int(s)
                segments.append({"start": float(start), "text": text.strip()})
    # Добавляем end как start следующего сегмента
    for i in range(len(segments) - 1):
        segments[i]["end"] = segments[i + 1]["start"]
    if segments:
        segments[-1]["end"] = segments[-1]["start"] + 5.0
    return segments


def assign_speakers(diarization, segments: list[dict]) -> list[dict]:
    """Сопоставляет каждый сегмент транскрипта со спикером по максимальному перекрытию."""
    from pyannote.core import Segment

    result = []
    for seg in segments:
        window = Segment(seg["start"], seg["end"])
        overlap: dict[str, float] = {}
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            inter = window & turn
            if inter:
                overlap[speaker] = overlap.get(speaker, 0) + inter.duration
        if overlap:
            best = max(overlap, key=overlap.__getitem__)
        else:
            best = "UNKNOWN"
        result.append({**seg, "speaker": best})
    return result


def format_markdown(segments: list[dict], audio_path: str) -> str:
    lines = [
        f"# Диаризация: {Path(audio_path).name}",
        "",
        "Спикеры разделены автоматически (pyannote.audio).",
        "Имена заменить вручную: SPEAKER_00 → Денис, SPEAKER_01 → Анатолий, ...",
        "",
    ]
    current_speaker = None
    for seg in segments:
        spk = seg["speaker"]
        if spk != current_speaker:
            if current_speaker is not None:
                lines.append("")
            lines.append(f"**{spk}**")
            current_speaker = spk
        h = int(seg["start"]) // 3600
        m = (int(seg["start"]) % 3600) // 60
        s = int(seg["start"]) % 60
        lines.append(f"[{h}:{m:02d}:{s:02d}] {seg['text']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("audio", help="Путь к аудиофайлу")
    parser.add_argument("--transcript", help="Путь к .md транскрипту (необязательно)")
    parser.add_argument("--token", help="HuggingFace токен")
    parser.add_argument("--speakers", type=int, default=None, help="Ожидаемое число спикеров")
    args = parser.parse_args()

    hf_token = args.token or os.environ.get("HF_TOKEN")
    if not hf_token:
        print("Ошибка: нужен HuggingFace токен (--token или $HF_TOKEN)", file=sys.stderr)
        sys.exit(1)

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"Файл не найден: {audio_path}", file=sys.stderr)
        sys.exit(1)

    # Определяем путь к транскрипту
    transcript_path = args.transcript
    if not transcript_path:
        candidate = audio_path.with_name(audio_path.stem + "_transcript.md")
        if candidate.exists():
            transcript_path = str(candidate)

    print(f"Загружаю модель диаризации...")
    from pyannote.audio import Pipeline
    import torch
    import soundfile as sf

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        token=hf_token,
    )

    # Если формат не поддерживается soundfile (m4a, aac и т.д.) — конвертируем в wav
    suffix = audio_path.suffix.lower()
    if suffix not in (".wav", ".flac", ".mp3", ".ogg"):
        import subprocess
        import tempfile
        tmp_wav = Path(tempfile.mktemp(suffix=".wav"))
        print(f"Конвертирую {suffix} → wav через ffmpeg...")
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(audio_path), "-ac", "1", "-ar", "16000", str(tmp_wav)],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        read_path = tmp_wav
    else:
        read_path = audio_path
        tmp_wav = None

    print(f"Загружаю аудио через soundfile...")
    waveform_np, sample_rate = sf.read(str(read_path), always_2d=True, dtype="float32")
    # soundfile → (frames, channels), pyannote ждёт (channels, frames)
    waveform = torch.tensor(waveform_np.T)
    audio_input = {"waveform": waveform, "sample_rate": sample_rate}

    if tmp_wav and tmp_wav.exists():
        tmp_wav.unlink()

    print(f"Диаризирую...")
    kwargs = {}
    if args.speakers:
        kwargs["num_speakers"] = args.speakers
    diarization = pipeline(audio_input, **kwargs)

    if transcript_path and Path(transcript_path).exists():
        print(f"Накладываю на транскрипт: {transcript_path}")
        segments = load_transcript_segments(transcript_path)
        segments = assign_speakers(diarization, segments)
        output_md = format_markdown(segments, str(audio_path))
        out_path = Path(transcript_path).with_name(
            Path(transcript_path).stem.replace("_transcript", "") + "_diarized.md"
        )
    else:
        # Нет транскрипта — просто сохраняем временны́е метки спикеров
        lines = [f"# Диаризация: {audio_path.name}", ""]
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            h = int(turn.start) // 3600
            m = (int(turn.start) % 3600) // 60
            s = int(turn.start) % 60
            lines.append(f"[{h}:{m:02d}:{s:02d}] **{speaker}** ({turn.duration:.1f}s)")
        output_md = "\n".join(lines)
        out_path = audio_path.with_name(audio_path.stem + "_diarized.md")

    out_path.write_text(output_md, encoding="utf-8")
    print(f"Готово: {out_path}")


if __name__ == "__main__":
    main()
