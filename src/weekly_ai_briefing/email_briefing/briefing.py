import re
from pathlib import Path
from typing import NamedTuple

from weekly_ai_briefing.config import BRIEFING_PATTERN, SECTION_HEADING

BRIEFING_FILENAME = re.compile(BRIEFING_PATTERN)
SECTION_HEADING_LINE = re.compile(SECTION_HEADING, re.MULTILINE)


class Section(NamedTuple):
    title: str
    markdown: str


def find_latest_briefing(history_dir: Path) -> tuple[Path, str]:
    """Returns (path, date string) of the newest YYYY-MM-DD-ai-outlook-briefing.md."""
    candidates = [
        (match.group(1), path)
        for path in history_dir.iterdir()
        if (match := BRIEFING_FILENAME.fullmatch(path.name))
    ]
    if not candidates:
        raise FileNotFoundError(f"No YYYY-MM-DD-ai-outlook-briefing.md files in {history_dir}")
    date, path = max(candidates)  # ISO dates sort lexicographically
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
