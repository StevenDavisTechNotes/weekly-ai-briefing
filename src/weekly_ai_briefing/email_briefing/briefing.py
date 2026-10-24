import re
from pathlib import Path
from typing import NamedTuple

from weekly_ai_briefing.config import (
    BRIEFING_PATTERN,
    EDITION_PREFIX,
    HTML_FOLDER,
    SECTION_HEADING,
    SITE_URL,
    TEXT_ONLY_SECTIONS,
)

BRIEFING_FILENAME = re.compile(BRIEFING_PATTERN)
SECTION_HEADING_LINE = re.compile(SECTION_HEADING, re.MULTILINE)


class Section(NamedTuple):
    title: str
    markdown: str


def is_text_only(section: Section) -> bool:
    """Text-only sections have no mp3; the page shows only their text."""
    return section.title.lower() in TEXT_ONLY_SECTIONS


def edition_name(date: str) -> str:
    """Names an edition's mp3 folder and its GitHub release tag."""
    return f"{EDITION_PREFIX}{date}"


def mp3_filename(briefing_stem: str, number: int) -> str:
    """Names the mp3 of the 1-based section number of a briefing."""
    return f"{briefing_stem}-{number:02d}.mp3"


def edition_page_url(briefing_stem: str) -> str:
    """Returns the public URL of a briefing's page (see publish.py)."""
    return f"{SITE_URL}{HTML_FOLDER.as_posix()}/{briefing_stem}.html"


def list_briefings(folder: Path) -> list[tuple[str, Path]]:
    """Returns (date string, path) of every YYYY-MM-DD-ai-outlook-briefing.md, newest first."""
    found = [
        (match.group(1), path)
        for path in folder.iterdir()
        if (match := BRIEFING_FILENAME.fullmatch(path.name))
    ]
    return sorted(found, reverse=True)  # ISO dates sort lexicographically


def find_latest_briefing(history_dir: Path) -> tuple[Path, str]:
    """Returns (path, date string) of the newest YYYY-MM-DD-ai-outlook-briefing.md."""
    briefings = list_briefings(history_dir)
    if not briefings:
        raise FileNotFoundError(f"No YYYY-MM-DD-ai-outlook-briefing.md files in {history_dir}")
    date, path = briefings[0]
    return path, date


def split_sections(markdown: str) -> list[Section]:
    """Splits a briefing on its '##' headings; any preamble joins the first section."""
    parts = SECTION_HEADING_LINE.split(markdown)
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
