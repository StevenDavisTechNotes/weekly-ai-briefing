from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from anthropic.types import ToolUnionParam

# --- Editions on disk ---
EDITIONS_FOLDER = Path("editions")
MARKDOWN_FOLDER = EDITIONS_FOLDER / "markdown_format"
MP3_FOLDER = EDITIONS_FOLDER / "mp3_format"
BLOGGER_FOLDER = EDITIONS_FOLDER / "blogger_format"
HTML_FOLDER = EDITIONS_FOLDER / "html_format"
PROMPT_FOLDER = Path(__file__).resolve().parent / "prompts"
BRIEFING_PATTERN = r"(\d{4}-\d{2}-\d{2})-ai-outlook-briefing\.md"
STATEMENT_OF_INTENT = "statement_of_intent.md"
EDITION_PREFIX = "ai-outlook-briefing-"  # an edition's mp3 folder and GitHub release tag: <prefix><date>

# --- Briefing generation (generate_briefing_text.py) ---
MODEL = "claude-opus-5-5"
EFFORT = "medium"
MAX_TOKENS: int = 128000
HISTORY_LOOKBACK: int = 2
MAX_CONTINUATIONS: int = 10  # per request: pause_turn resumes + max_tokens continues
# The whole briefing is one long streamed call, so a dropped connection or an
# overloaded API would otherwise discard all the research done so far.
STREAM_RETRIES: int = 4
STREAM_RETRY_BASE_SECONDS: int = 30
TRANSIENT_ERROR_TYPES = {"overloaded_error", "api_error", "rate_limit_error"}

# The briefing is about the preceding week, so the model must be able to search.
TOOLS: list[ToolUnionParam] = [
    {"type": "web_search_20260318", "name": "web_search"},
]

# --- Blogger export (convert_for_blogger.py) ---
AUTHOR = "Steven Davis"
LABEL = "Weekly AI Briefing"
POST_TITLE = "AI Off-Consensus: The Entropy Brief"
STATEMENT_TITLE = "Statement of Intent"

# --- GitHub publishing (publish.py) ---
GITHUB_REPO = "StevenDavisTechNotes/weekly-ai-briefing"
SITE_INDEX = Path("index.html")  # GitHub Pages serves the repository root
SITE_URL = "https://stevendavistechnotes.github.io/weekly-ai-briefing/"

# --- Email briefing ---
# Each "## " heading starts a section that is voiced and linked on its own.
SECTION_HEADING = r"^(##[ \t].*)$"  # compiled with re.MULTILINE
# Sections shown as text only: for reference not worth hearing.
TEXT_ONLY_SECTIONS = {"source notes and attribution"}  # compared against the lowercased title

SENDER_EMAIL = "stevendavisma@gmail.com"
RECIPIENTS = [SENDER_EMAIL]
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
