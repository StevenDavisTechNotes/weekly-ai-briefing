import re
from pathlib import Path

HISTORY_FOLDER = Path("history")
STAGED_AUDIO_FOLDER = Path("staged_audio")
BRIEFING_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})-ai-outlook-briefing\.md")
# Each "## " heading starts a section that is voiced and emailed on its own.
SECTION_HEADING = re.compile(r"^(##[ \t].*)$", re.MULTILINE)
# Sections emailed as text only: for reference not worth hearing.
TEXT_ONLY_SECTIONS = {"source notes and attribution"}  # compared against the lowercased title

SENDER_EMAIL = "stevendavisma@gmail.com"
RECIPIENTS = [
    SENDER_EMAIL,
    "Recipient <recipient@example.com>",
]
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
IMAP_HOST = "imap.gmail.com"
# Gmail files the sent copy a moment after SMTP accepts the message.
SENT_COPY_ATTEMPTS = 10
SENT_COPY_DELAY_SECONDS = 2

# Kokoro model files are not in git; README.md says how to download them.
MODEL_PATH = Path("models/kokoro-v1.0.fp16.onnx")
VOICES_PATH = Path("models/voices-v1.0.bin")
VOICE = "af_heart"
TTS_CHUNK_CHARS = 3000
CHUNK_PAUSE_SECONDS = 0.4

# Gmail rejects messages over 25 MB; base64 inflates attachments by ~4/3 (plus
# line breaks), so the raw mp3 must stay comfortably below 18 MB.
MAX_MP3_BYTES = 17 * 1024 * 1024
MAX_BITRATE_KBPS = 48
MIN_BITRATE_KBPS = 8
