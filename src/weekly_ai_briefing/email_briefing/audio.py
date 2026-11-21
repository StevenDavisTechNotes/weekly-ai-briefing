import functools
import subprocess
from pathlib import Path

import imageio_ffmpeg
import numpy as np
import onnxruntime
from kokoro_onnx import Kokoro

from weekly_ai_briefing.config import (
    CHUNK_PAUSE_SECONDS,
    MODEL_PATH,
    MP3_BITRATE_KBPS,
    TTS_CHUNK_CHARS,
    VOICE,
    VOICES_PATH,
)
from weekly_ai_briefing.pronouncers import pronunciations, to_phonemes, usable_pronunciations

from .speech import markdown_to_speech_text, split_chunks


@functools.cache
def load_kokoro() -> Kokoro:
    for path in (MODEL_PATH, VOICES_PATH):
        if not path.exists():
            raise FileNotFoundError(f"{path} is missing; see 'Kokoro model files' in README.md")
    onnxruntime.set_default_logger_severity(3)  # the fp16 model warns once per graph node
    return Kokoro(str(MODEL_PATH), str(VOICES_PATH))


def synthesize(chunks: list[str], pronounced: dict[str, str]) -> tuple[np.ndarray, int]:
    """Returns (mono float32 samples, sample rate) for all chunks, in order.

    Each name in pronounced is spoken by its IPA instead of the engine's guess.
    """
    kokoro = load_kokoro()
    usable = usable_pronunciations(pronounced, kokoro.tokenizer.vocab)
    parts: list[np.ndarray] = []
    rate = 0
    for number, chunk in enumerate(chunks, start=1):
        print(f"  chunk {number}/{len(chunks)}")
        phonemes = to_phonemes(chunk, usable, lambda text: kokoro.tokenizer.phonemize(text, "en-us"))
        samples, rate = kokoro.create(phonemes, voice=VOICE, lang="en-us", is_phonemes=True)
        parts += [samples, np.zeros(int(rate * CHUNK_PAUSE_SECONDS), dtype=np.float32)]
    return np.concatenate(parts), rate


def encode_mp3(samples: np.ndarray, rate: int, mp3_path: Path) -> None:
    """Encodes samples as a mono CBR mp3 at MP3_BITRATE_KBPS."""
    pcm = (np.clip(samples, -1.0, 1.0) * 32767).astype("<i2").tobytes()  # cSpell: ignore tobytes
    subprocess.run(
        [
            imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
            "-f", "s16le", "-ar", str(rate),
            "-ac", "1", "-i", "pipe:0",
            "-codec:a",
            "libmp3lame",   # cSpell: ignore libmp
            "-b:a",
            f"{MP3_BITRATE_KBPS}k",
            str(mp3_path),
        ],
        input=pcm,
        check=True,
    )


def generate_mp3(markdown: str, mp3_path: Path, pronounced: dict[str, str] | None = None) -> None:
    """Voices markdown into mp3_path.

    pronounced maps names to IPA, usually from the whole edition, so that a name marked
    in an earlier section is said the same way here; the markdown's own pronouncers are
    added to it.
    """
    pronounced = {**pronunciations(markdown), **(pronounced or {})}
    speech = markdown_to_speech_text(markdown)
    chunks = split_chunks(speech, TTS_CHUNK_CHARS)
    print(f"Generating audio: {len(speech):,} chars in {len(chunks)} chunks...")
    samples, rate = synthesize(chunks, pronounced)
    encode_mp3(samples, rate, mp3_path)
    print(f"Saved {mp3_path} ({mp3_path.stat().st_size / 1e6:.1f} MB)")
