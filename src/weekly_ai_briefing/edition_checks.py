"""Mechanical checks of a written edition against the phase D writing rules.

These cover the rules a script can check exactly: the `##` parts, the five signals, footnotes, URLs, the metadata
block and the length budget. The figures-per-sentence rule is checked only for figures written in digits, as a
heuristic, so its findings are worth a look rather than proof.

usage:
    uv run python -m weekly_ai_briefing.edition_checks editions/markdown_format/<date>-ai-outlook-briefing.md
"""

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

import yaml

from weekly_ai_briefing.bottom_matter import DELIMITER, REQUIRED_KEYS
from weekly_ai_briefing.config import BRIEFING_PATTERN, MARKDOWN_FOLDER
from weekly_ai_briefing.pronouncer_lexicon import mismatches, read_lexicon
from weekly_ai_briefing.pronouncers import drop_pronouncers

DIMENSIONS = (
    "AI Technology",
    "Quantum Computing",
    "Enterprise AI Adoption",
    "Physical AI & Industrial Automation",
    "Human and Machine Agency",
    "Economic Structural Change",
    "Institutional Financial Services",
)
REQUIRED_PARTS = (
    "Orientation: The Five Signals That Matter This Week",
    *DIMENSIONS,
    "Strategic Mental Model Shifts",
    "Source Notes and Attribution",
)
SOURCE_NOTES = "Source Notes and Attribution"
SIGNAL_CUES = ("First,", "Second,", "Third,", "Fourth,", "Fifth,")
MAX_BODY_WORDS = 10_000
MAX_FIGURES_PER_SENTENCE = 2
MAX_FIGURES_PER_BLOCK = 4

FOOTNOTE_REF = re.compile(r"\[\^(\d+)\](?!:)")
FOOTNOTE_DEF = re.compile(r"^\[\^(\d+)\]:", re.MULTILINE)
URL = re.compile(r"https?://\S+")
ISO_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
MONTH_DAY = re.compile(rf"\b(?:{MONTHS})\s+\d{{1,2}}(?:st|nd|rd|th)?\b|\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:{MONTHS})\b")
YEAR = re.compile(r"\b(?:19|20)\d{2}s?\b")
QUARTER = re.compile(r"\b(?:[1-4]Q\d{2}|Q[1-4](?:\s+\d{4})?)\b")
MATURITY = re.compile(r"\b\d+-(?:year|month)\b")  # a Treasury tenor such as "the 10-year" names a security
# A versioned name such as "GPT-6" or "Sonnet 4.5". A capital word and a whole number, as in "About 40 firms" or
# "Gemini 4", is left counted as a figure, since it cannot be told apart from a sentence opening.
VERSION = re.compile(r"\b[A-Z]\w*(?:-\d+(?:\.\d+)*|\s+\d+\.\d+)\b(?!\s*(?:%|percent))")
FIGURE = re.compile(r"\d+(?:[.,]\d+)*")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def parts(markdown: str) -> list[tuple[str, str]]:
    """The `##` parts in order, each as (title, text below the heading)."""
    pieces = re.split(r"^## (.+)$", markdown, flags=re.MULTILINE)
    return [(pieces[i].strip(), pieces[i + 1]) for i in range(1, len(pieces) - 1, 2)]


def split_metadata(markdown: str) -> tuple[str | None, str]:
    """The text of the closing `---` block (None when absent) and the markdown before it."""
    lines = markdown.rstrip().splitlines()
    if not lines or lines[-1].strip() != DELIMITER:
        return None, markdown
    opening = next((i for i in range(len(lines) - 2, -1, -1) if lines[i].strip() == DELIMITER), None)
    if opening is None:
        return None, markdown
    return "\n".join(lines[opening + 1:-1]), "\n".join(lines[:opening]) + "\n"


def check_parts(found: list[str]) -> list[str]:
    if found == list(REQUIRED_PARTS):
        return []
    missing = [title for title in REQUIRED_PARTS if title not in found]
    extra = [title for title in found if title not in REQUIRED_PARTS]
    problems = [f"missing ## part: {title}" for title in missing] + [f"unexpected ## part: {title}" for title in extra]
    return problems or ["## parts are out of order"]


def check_signals(orientation: str) -> list[str]:
    bullets = [line.strip()[2:] for line in orientation.splitlines() if re.match(r"\s*[-*] ", line)]
    if len(bullets) != len(SIGNAL_CUES):
        return [f"Orientation has {len(bullets)} bullets, not five"]
    return [
        f"Orientation bullet {number} does not open with {cue!r}"
        for number, (cue, bullet) in enumerate(zip(SIGNAL_CUES, bullets), start=1)
        if not bullet.startswith(cue)
    ]


def check_footnotes(body: str) -> list[str]:
    definitions = FOOTNOTE_DEF.findall(body)
    text = FOOTNOTE_DEF.sub("", body)
    first_use = list(dict.fromkeys(FOOTNOTE_REF.findall(text)))
    problems = [f"footnote [^{n}] is defined more than once" for n in sorted({d for d in definitions
                                                                              if definitions.count(d) > 1}, key=int)]
    problems += [f"footnote [^{n}] is used but not defined" for n in first_use if n not in definitions]
    problems += [f"footnote [^{n}] is defined but not used" for n in dict.fromkeys(definitions) if n not in first_use]
    expected = [str(n) for n in range(1, len(first_use) + 1)]
    if first_use != expected:
        problems.append("footnotes are not numbered 1, 2, 3... in order of first appearance")
    return problems


def check_urls(body: str) -> list[str]:
    lines = [line for line in body.splitlines() if URL.search(line) and not FOOTNOTE_DEF.match(line)]
    return [f"URL outside a footnote definition: {line.strip()[:80]}" for line in lines]


def check_metadata(metadata: str | None) -> list[str]:
    if metadata is None:
        return ["the edition does not end with a --- delimited metadata block"]
    try:
        data = yaml.safe_load(metadata)
    except yaml.YAMLError as error:
        return [f"metadata block is not valid YAML: {error}"]
    if not isinstance(data, dict):
        return ["metadata block is not a YAML mapping"]
    if list(data) != list(REQUIRED_KEYS):
        return [f"metadata keys are {list(data)}, not exactly {list(REQUIRED_KEYS)} in that order"]
    return []


def spoken_text(text: str) -> str:
    """Text as heard: no tables, headings or footnote definitions, pronouncers reduced to the bare name."""
    kept = [
        line for line in text.splitlines()
        if not line.lstrip().startswith(("|", "#")) and not FOOTNOTE_DEF.match(line)
    ]
    return drop_pronouncers("\n".join(kept))


def briefing_spoken_text(markdown: str) -> str:
    """The spoken text of every part before the Source Notes: the text the length budget counts."""
    _, body = split_metadata(markdown)
    return spoken_text("".join(text for title, text in parts(body) if title != SOURCE_NOTES))


def spoken_words(markdown: str) -> int:
    return len(briefing_spoken_text(markdown).split())


def check_length(spoken: str) -> list[str]:
    words = len(spoken.split())
    return [f"body is about {words:,} words, over the {MAX_BODY_WORDS:,}-word budget"] if words > MAX_BODY_WORDS else []


def figures(text: str) -> int:
    """Figures written in digits, leaving out dates, years, quarters, tenors, versioned names and footnotes."""
    for pattern in (FOOTNOTE_REF, ISO_DATE, MONTH_DAY, QUARTER, YEAR, MATURITY, VERSION):
        text = pattern.sub(" ", text)
    return len(FIGURE.findall(text))


def check_figures(spoken: str) -> list[str]:
    problems = []
    for block in re.split(r"\n\s*\n|\n(?=\s*[-*] )", spoken):
        block = block.strip()
        if not block:
            continue
        if figures(block) > MAX_FIGURES_PER_BLOCK:
            problems.append(f"more than {MAX_FIGURES_PER_BLOCK} figures in: {block[:80]}")
        problems += [
            f"more than {MAX_FIGURES_PER_SENTENCE} figures in sentence: {sentence[:80]}"
            for sentence in SENTENCE_END.split(block)
            if figures(sentence) > MAX_FIGURES_PER_SENTENCE
        ]
    return problems


def check_edition(markdown: str) -> list[str]:
    """Every rule problem found in the edition; an empty list means it passed."""
    metadata, body = split_metadata(markdown)
    found = parts(body)
    titles = [title for title, _ in found]
    problems = check_parts(titles)
    orientation = next((text for title, text in found if title == REQUIRED_PARTS[0]), None)
    if orientation is not None:
        problems += check_signals(orientation)
    problems += check_footnotes(body)
    problems += check_urls(body)
    problems += check_metadata(metadata)
    spoken = briefing_spoken_text(markdown)
    problems += check_length(spoken)
    problems += check_figures(spoken)
    return problems


def latest_edition() -> Path:
    editions = sorted(path for path in MARKDOWN_FOLDER.glob("*.md") if re.fullmatch(BRIEFING_PATTERN, path.name))
    if not editions:
        raise SystemExit(f"No editions in {MARKDOWN_FOLDER}")
    return editions[-1]


def main(argv: Sequence[str] | None = None) -> int:
    """Checks each edition file named on the command line; exits 1 when any rule check fails."""
    parser = argparse.ArgumentParser(description="Check edition markdown against the phase D writing rules.")
    parser.add_argument("paths", nargs="*", type=Path, help="edition markdown files")
    parser.add_argument("--latest", action="store_true", help="check the newest edition in editions/markdown_format")
    args = parser.parse_args(argv)
    paths = list(args.paths)
    if args.latest:
        paths.append(latest_edition())
    if not paths:
        parser.error("name edition files, or pass --latest")
    failed = False
    for path in paths:
        markdown = path.read_text(encoding="utf-8")
        problems = check_edition(markdown)
        problems += [f"{name} is written {used!r} but the pronouncer lexicon has {listed!r}"
                     for name, used, listed in mismatches(markdown, read_lexicon())]
        words = spoken_words(markdown)
        print(f"{path}: {'passed' if not problems else f'{len(problems)} problem(s)'}, about {words:,} spoken words")
        for problem in problems:
            print(f"  - {problem}")
        failed = failed or bool(problems)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
