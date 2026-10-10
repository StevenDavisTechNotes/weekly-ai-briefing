#! python3
# usage:
#   $env:GMAIL_APP_PASSWORD="YourValue"
#   python -m src.weekly_ai_briefing.email_briefing
#
# Environment:
#   GMAIL_USER          optional; sending account (default: the recipient address)
#   GMAIL_APP_PASSWORD  required;
#        a Google app password for the sending account
#        see https://myaccount.google.com/apppasswords

import asyncio
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

import edge_tts
import imageio_ffmpeg

HISTORY_FOLDER = Path("history")
BRIEFING_PATTERN = re.compile(r"briefing-(\d{4}-\d{2}-\d{2})\.md")
# Each "## " heading starts a section that is voiced and emailed on its own.
SECTION_HEADING = re.compile(r"^(##[ \t].*)$", re.MULTILINE)
RECIPIENT = "stevendavisma@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
IMAP_HOST = "imap.gmail.com"
# Gmail files the sent copy a moment after SMTP accepts the message.
SENT_COPY_ATTEMPTS = 10
SENT_COPY_DELAY_SECONDS = 2

VOICE = "en-US-JennyNeural"
TTS_CHUNK_CHARS = 3000
TTS_CONCURRENCY = 4
TTS_RETRIES = 4
# edge-tts default output format: audio-24khz-48kbitrate-mono-mp3 (CBR).
TTS_SOURCE_BYTES_PER_SECOND = 48_000 // 8

# Gmail rejects messages over 25 MB; base64 inflates attachments by ~4/3 (plus
# line breaks), so the raw mp3 must stay comfortably below 18 MB.
MAX_MP3_BYTES = 17 * 1024 * 1024
MIN_BITRATE_KBPS = 8


def find_latest_briefing(history_dir: Path) -> tuple[Path, str]:
    """Returns (path, date string) of the newest briefing-YYYY-MM-DD.md."""
    candidates = [
        (match.group(1), path)
        for path in history_dir.iterdir()
        if (match := BRIEFING_PATTERN.fullmatch(path.name))
    ]
    if not candidates:
        raise FileNotFoundError(f"No briefing-YYYY-MM-DD.md files in {history_dir}")
    date, path = max(candidates)  # ISO dates sort lexicographically
    return path, date


def markdown_to_speech_text(markdown: str) -> str:
    """Strips markdown syntax so the TTS engine doesn't read it aloud."""
    text = re.sub(r"`{3}.*?`{3}", "", markdown, flags=re.DOTALL)
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


async def synthesize_chunk(chunk: str, semaphore: asyncio.Semaphore) -> bytes:
    async with semaphore:
        for attempt in range(1, TTS_RETRIES + 1):
            try:
                audio = bytearray()
                async for message in edge_tts.Communicate(chunk, VOICE).stream():
                    if message["type"] == "audio":
                        audio += message["data"]
                if not audio:
                    raise RuntimeError("TTS returned no audio")
                return bytes(audio)
            except Exception as exc:
                if attempt == TTS_RETRIES:
                    raise
                print(f"  TTS retry {attempt}/{TTS_RETRIES - 1} after: {exc!r}")
                await asyncio.sleep(2 * attempt)
    raise AssertionError("unreachable")


async def synthesize(chunks: list[str]) -> bytes:
    semaphore = asyncio.Semaphore(TTS_CONCURRENCY)
    tasks = [asyncio.create_task(synthesize_chunk(c, semaphore)) for c in chunks]
    try:
        parts = await asyncio.gather(*tasks)
    except BaseException:
        for task in tasks:
            task.cancel()
        raise
    return b"".join(parts)  # same-format CBR mp3 streams concatenate cleanly


def shrink_to_fit(mp3_path: Path, source_bytes: int) -> None:
    """Re-encodes mp3_path at a lower bitrate if it would exceed MAX_MP3_BYTES."""
    if source_bytes <= MAX_MP3_BYTES:
        return
    seconds = source_bytes / TTS_SOURCE_BYTES_PER_SECOND
    kbps = max(
        MIN_BITRATE_KBPS,
        int(MAX_MP3_BYTES * 8 / seconds / 1000),
    )
    print(f"MP3 is {source_bytes / 1e6:.1f} MB; re-encoding at {kbps} kbps to fit email limits...")
    smaller = mp3_path.with_suffix(".small.mp3")
    subprocess.run(
        [
            imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error",
            "-i", str(mp3_path),
            "-ac", "1", "-ar", "16000",  # speech; 16 kHz is valid for MPEG-2 low bitrates
            "-codec:a", "libmp3lame", "-b:a", f"{kbps}k",
            str(smaller),
        ],
        check=True,
    )
    smaller.replace(mp3_path)
    if mp3_path.stat().st_size > MAX_MP3_BYTES:
        raise RuntimeError(
            f"MP3 is still {mp3_path.stat().st_size / 1e6:.1f} MB at {kbps} kbps; too large to email")


def generate_mp3(markdown: str, mp3_path: Path) -> None:
    speech = markdown_to_speech_text(markdown)
    chunks = split_chunks(speech, TTS_CHUNK_CHARS)
    print(f"Generating audio: {len(speech):,} chars in {len(chunks)} chunks...")
    audio = asyncio.run(synthesize(chunks))
    mp3_path.write_bytes(audio)
    shrink_to_fit(mp3_path, len(audio))
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


def send_email(subject: str, body: str, mp3_path: Path) -> None:
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
    message.add_attachment(
        mp3_path.read_bytes(),
        maintype="audio",
        subtype="mpeg",
        filename=mp3_path.name,
    )

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)
    print(f"Emailed {mp3_path.name} to {RECIPIENT}")

    # Mailing yourself stores one message labelled both Inbox and Sent, so
    # there is no second copy to delete (deleting it would empty the Inbox too).
    if sender.lower() != RECIPIENT.lower():
        delete_sent_copy(sender, password, message_id)


def main() -> None:
    briefing_path, date = find_latest_briefing(HISTORY_FOLDER)
    sections = split_sections(briefing_path.read_text(encoding="utf-8"))
    print(f"Using {briefing_path}: {len(sections)} sections")
    for number, section in enumerate(sections, start=1):
        print(f"[{number}/{len(sections)}] {section.title}")
        mp3_path = briefing_path.with_name(f"{briefing_path.stem}-{number:02d}.mp3")
        generate_mp3(section.markdown, mp3_path)
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


if __name__ == "__main__":
    main()
