import functools
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import onnxruntime
from kokoro_onnx import Kokoro

from weekly_ai_briefing.config import (
    CHUNK_PAUSE_SECONDS,
    MAX_BITRATE_KBPS,
    MAX_MP3_BYTES,
    MIN_BITRATE_KBPS,
    MODEL_PATH,
    TTS_CHUNK_CHARS,
    VOICE,
    VOICES_PATH,
)
from .speech import markdown_to_speech_text, split_chunks


@functools.cache
def load_kokoro() -> Kokoro:
    for path in (MODEL_PATH, VOICES_PATH):
        if not path.exists():
            raise FileNotFoundError(f"{path} is missing; see 'Kokoro model files' in README.md")
    onnxruntime.set_default_logger_severity(3)  # the fp16 model warns once per graph node
    return Kokoro(str(MODEL_PATH), str(VOICES_PATH))


def synthesize(chunks: list[str]) -> tuple[np.ndarray, int]:
    """Returns (mono float32 samples, sample rate) for all chunks, in order."""
    kokoro = load_kokoro()
    parts: list[np.ndarray] = []
    rate = 0
    for number, chunk in enumerate(chunks, start=1):
        print(f"  chunk {number}/{len(chunks)}")
        samples, rate = kokoro.create(chunk, voice=VOICE, lang="en-us")
        parts += [samples, np.zeros(int(rate * CHUNK_PAUSE_SECONDS), dtype=np.float32)]
    return np.concatenate(parts), rate


def choose_bitrate_kbps(seconds: float) -> int:
    """Returns the highest bitrate, capped at MAX_BITRATE_KBPS, that keeps the audio under MAX_MP3_BYTES."""
    return min(MAX_BITRATE_KBPS, max(MIN_BITRATE_KBPS, int(MAX_MP3_BYTES * 8 / seconds / 1000)))


def encode_mp3(samples: np.ndarray, rate: int, mp3_path: Path) -> None:
    """Encodes samples as a mono CBR mp3, lowering the bitrate if needed to fit MAX_MP3_BYTES."""
    seconds = len(samples) / rate
    kbps = choose_bitrate_kbps(seconds)
    if kbps < MAX_BITRATE_KBPS:
        print(f"  {seconds / 60:.0f} minutes of audio; encoding at {kbps} kbps to fit email limits")
    pcm = (np.clip(samples, -1.0, 1.0) * 32767).astype("<i2").tobytes()  # cSpell: ignore tobytes
    subprocess.run(
        [
            imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
            "-f", "s16le", "-ar", str(rate),
            "-ac", "1", "-i", "pipe:0",
            "-codec:a",
            "libmp3lame",   # cSpell: ignore libmp
            "-b:a",
            f"{kbps}k",
            str(mp3_path),
        ],
        input=pcm,
        check=True,
    )
    if mp3_path.stat().st_size > MAX_MP3_BYTES:
        raise RuntimeError(
            f"MP3 is still {mp3_path.stat().st_size / 1e6:.1f} MB at {kbps} kbps; too large to email")


def generate_mp3(markdown: str, mp3_path: Path) -> None:
    speech = markdown_to_speech_text(markdown)
    chunks = split_chunks(speech, TTS_CHUNK_CHARS)
    print(f"Generating audio: {len(speech):,} chars in {len(chunks)} chunks...")
    samples, rate = synthesize(chunks)
    encode_mp3(samples, rate, mp3_path)
    print(f"Saved {mp3_path} ({mp3_path.stat().st_size / 1e6:.1f} MB)")
