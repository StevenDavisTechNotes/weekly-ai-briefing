#! python3
# usage: uv run python -m src.weekly_ai_briefing.email_briefing [--section N [N ...]] [--no-send-email]
#
# Environment:
#   GMAIL_USER          optional; sending account (default: the recipient address)
#   GMAIL_APP_PASSWORD  required;
#        a Google app password for the sending account
#        see https://myaccount.google.com/apppasswords

import argparse
import functools
import imaplib
import os
import re
import smtplib
import subprocess
import time
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path
from typing import NamedTuple

import imageio_ffmpeg
import numpy as np
import onnxruntime
from kokoro_onnx import Kokoro

HISTORY_FOLDER = Path("history")
STAGED_AUDIO_FOLDER = Path("staged_audio")
BRIEFING_PATTERN = re.compile(r"(\d{4}-\d{2}-\d{2})-ai-outlook-briefing\.md")
# Each "## " heading starts a section that is voiced and emailed on its own.
SECTION_HEADING = re.compile(r"^(##[ \t].*)$", re.MULTILINE)
# Sections emailed as text only: for reference not worth hearing.
TEXT_ONLY_SECTIONS = {"Source Notes and Attribution"}
# A pipe table: header row, delimiter row (|---|:--:|), then any rows with a pipe.
MARKDOWN_TABLE = re.compile(
    r"^.*\|.*\n"
    r"(?=[-:| \t]*\|)[-:| \t]*-[-:| \t]*(?:\n|$)"
    r"(?:.*\|.*(?:\n|$))*",
    re.MULTILINE,
)
RECIPIENT = "stevendavisma@gmail.com"
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


def find_latest_briefing(history_dir: Path) -> tuple[Path, str]:
    """Returns (path, date string) of the newest YYYY-MM-DD-ai-outlook-briefing.md."""
    candidates = [
        (match.group(1), path)
        for path in history_dir.iterdir()
        if (match := BRIEFING_PATTERN.fullmatch(path.name))
    ]
    if not candidates:
        raise FileNotFoundError(f"No YYYY-MM-DD-ai-outlook-briefing.md files in {history_dir}")
    date, path = max(candidates)  # ISO dates sort lexicographically
    return path, date


def markdown_to_speech_text(markdown: str) -> str:
    """Strips markdown syntax so the TTS engine doesn't read it aloud."""
    text = re.sub(r"`{3}.*?`{3}", "", markdown, flags=re.DOTALL)
    text = MARKDOWN_TABLE.sub("", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)  # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> label
    text = re.sub(r"https?://\S+", "", text)  # bare URLs
    text = re.sub(r"^\s*-{3,}\s*$", "", text, flags=re.MULTILINE)  # rules
    # Headings: drop the hashes, end with a period so the voice pauses.
    text = re.sub(
        r"^#{1,6}\s*(.+?)\s*#*\s*$",
        lambda m: m.group(1).rstrip(".:") + ".",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", text, flags=re.MULTILINE)  # bullets
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)  # quotes
    text = re.sub(r"(\*\*|__|\*|_|`)", "", text)  # emphasis / inline code
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def split_chunks(text: str, max_chars: int) -> list[str]:  # noqa: C901
    """Splits on paragraph (then sentence) boundaries into pieces <= max_chars."""
    pieces: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if len(paragraph) <= max_chars:
            pieces.append(paragraph)
            continue
        current = ""
        for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
            while len(sentence) > max_chars:  # pathological: no punctuation
                if current:
                    pieces.append(current)
                    current = ""
                pieces.append(sentence[:max_chars])
                sentence = sentence[max_chars:]
            if current and len(current) + 1 + len(sentence) > max_chars:
                pieces.append(current)
                current = sentence
            else:
                current = f"{current} {sentence}".strip()
        if current:
            pieces.append(current)

    # Merge small neighbours so we don't make hundreds of tiny requests.
    chunks: list[str] = []
    for piece in pieces:
        if chunks and len(chunks[-1]) + 2 + len(piece) <= max_chars:
            chunks[-1] += "\n\n" + piece
        else:
            chunks.append(piece)
    return chunks


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


def encode_mp3(samples: np.ndarray, rate: int, mp3_path: Path) -> None:
    """Encodes samples as a mono CBR mp3, lowering the bitrate if needed to fit MAX_MP3_BYTES."""
    seconds = len(samples) / rate
    kbps = min(MAX_BITRATE_KBPS, max(MIN_BITRATE_KBPS, int(MAX_MP3_BYTES * 8 / seconds / 1000)))
    if kbps < MAX_BITRATE_KBPS:
        print(f"  {seconds / 60:.0f} minutes of audio; encoding at {kbps} kbps to fit email limits")
    pcm = (np.clip(samples, -1.0, 1.0) * 32767).astype("<i2").tobytes()
    subprocess.run(
        [
            imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
            "-f", "s16le", "-ar", str(rate), "-ac", "1", "-i", "pipe:0",
            "-codec:a", "libmp3lame", "-b:a", f"{kbps}k",
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


class Section(NamedTuple):
    title: str
    markdown: str


def split_sections(markdown: str) -> list[Section]:
    """Splits a briefing on its '##' headings; any preamble joins the first section."""
    parts = SECTION_HEADING.split(markdown)
    preamble, rest = parts[0], parts[1:]
    if not rest:
        raise ValueError("Briefing has no '##' section headings")
    sections = [
        Section(title=heading.lstrip("#").strip(), markdown=heading + body)
        for heading, body in zip(rest[0::2], rest[1::2])
    ]
    first = sections[0]
    sections[0] = first._replace(markdown=preamble + first.markdown)
    return sections


def find_special_folder(imap: imaplib.IMAP4_SSL, attribute: str) -> str:
    r"""Returns the quoted name of the mailbox flagged with attribute, e.g. \Sent.

    Gmail's folder names are localized ("[Gmail]/Sent Mail", "[Google Mail]/...")
    but the special-use attributes are not.
    """
    _, lines = imap.list()
    for line in lines:
        if not isinstance(line, bytes):
            continue
        flags = line.split(b")", 1)[0].split()
        if attribute.encode() in flags:
            name = line.decode().rsplit(' "/" ', 1)[1]
            return name if name.startswith('"') else f'"{name}"'
    raise RuntimeError(f"No {attribute} mailbox found")


def delete_sent_copy(sender: str, password: str, message_id: str) -> None:
    """Permanently deletes the copy Gmail saved in the sender's Sent folder."""
    with imaplib.IMAP4_SSL(IMAP_HOST) as imap:
        imap.login(sender, password)
        sent_folder = find_special_folder(imap, r"\Sent")
        trash_folder = find_special_folder(imap, r"\Trash")

        imap.select(sent_folder)
        for _ in range(SENT_COPY_ATTEMPTS):
            _, data = imap.uid("SEARCH", "HEADER", "Message-ID", message_id)
            uids = data[0]
            if isinstance(uids, bytes) and uids:
                break
            time.sleep(SENT_COPY_DELAY_SECONDS)
            imap.noop()
        else:
            print(f"  Sent copy of {message_id} not found; leaving it")
            return
        # In Gmail, expunging from Sent only removes the label; the message must
        # go through Trash to actually be deleted.
        imap.uid("MOVE", uids.decode().replace(" ", ","), trash_folder)

        imap.select(trash_folder)
        _, data = imap.uid("SEARCH", "HEADER", "Message-ID", message_id)
        uids = data[0]
        if isinstance(uids, bytes) and uids:
            imap.uid("STORE", uids.decode().replace(" ", ","), "+FLAGS", r"(\Deleted)")
            imap.expunge()
    print("  Deleted the sent copy")


def send_email(subject: str, body: str, mp3_path: Path | None) -> None:
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        raise RuntimeError("Set GMAIL_APP_PASSWORD to a Google app password")
    sender = os.environ.get("GMAIL_USER", RECIPIENT)

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = RECIPIENT
    message["Message-ID"] = message_id = make_msgid(domain=sender.split("@")[-1])
    message.set_content(body)
    if mp3_path is not None:
        message.add_attachment(
            mp3_path.read_bytes(),
            maintype="audio",
            subtype="mpeg",
            filename=mp3_path.name,
        )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)
    print(f"Emailed {mp3_path.name if mp3_path else subject} to {RECIPIENT}")

    # Mailing yourself stores one message labelled both Inbox and Sent, so
    # there is no second copy to delete (deleting it would empty the Inbox too).
    if sender.lower() != RECIPIENT.lower():
        delete_sent_copy(sender, password, message_id)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Voice the latest weekly briefing and email it section by section.")
    parser.add_argument(
        "--section", type=int, nargs="+", metavar="N", default=None,
        help="1-based section numbers to process (default: all sections)",
    )
    parser.add_argument(
        "--send-email", action=argparse.BooleanOptionalAction, default=True,
        help="email each section; --no-send-email only writes the mp3 files to staged_audio/",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        briefing_path, date = find_latest_briefing(HISTORY_FOLDER)
        sections = split_sections(briefing_path.read_text(encoding="utf-8"))
        print(f"Using {briefing_path}: {len(sections)} sections")
        selected = set(args.section) if args.section is not None else set(range(1, len(sections) + 1))
        invalid = sorted(n for n in selected if not 1 <= n <= len(sections))
        if invalid:
            raise SystemExit(f"error: --section {invalid} out of range; the briefing has sections 1-{len(sections)}")
        STAGED_AUDIO_FOLDER.mkdir(exist_ok=True)
        for number, section in enumerate(sections, start=1):
            if number not in selected:
                continue
            print(f"[{number}/{len(sections)}] {section.title}")
            if section.title.lower() in TEXT_ONLY_SECTIONS:
                if not args.send_email:
                    print("  Text-only section; nothing to generate")
                    continue
                send_email(
                    subject=f"Weekly AI Briefing - {date} - {section.title}",
                    body=(
                        f"Hi Steve,\n\n"
                        f"This is section {number} of {len(sections)} of this "
                        f"week's AI briefing (dated {date}): {section.title}. "
                        "It has no audio version.\n\n"
                        + section.markdown
                    ),
                    mp3_path=None,
                )
                continue
            mp3_path = STAGED_AUDIO_FOLDER / f"{briefing_path.stem}-{number:02d}.mp3"
            generate_mp3(section.markdown, mp3_path)
            if not args.send_email:
                continue
            send_email(
                subject=f"Weekly AI Briefing - {date} - {section.title}",
                body=(
                    f"Hi Steve,\n\n"
                    f"This is section {number} of {len(sections)} of this "
                    f"week's AI briefing (dated {date}): {section.title}. "
                    "The audio version is attached as an MP3.\n"
                ),
                mp3_path=mp3_path,
            )
    except KeyboardInterrupt:
        print("Interrupted")


if __name__ == "__main__":
    main()
