"""The pronouncer lexicon, state/pronouncers.md: one IPA for each name, reused every week so the audio stays consistent.

Phase D reads the lexicon and uses its IPA for any name in it. After an edition is written, update_lexicon adds the
names the edition introduced, so the lexicon grows by a deterministic step rather than by a model rewriting it.

usage:
    uv run python -m weekly_ai_briefing.pronouncer_lexicon editions/markdown_format/<date>-ai-outlook-briefing.md
"""

import argparse
import re
from collections.abc import Sequence
from pathlib import Path
from typing import NamedTuple

from weekly_ai_briefing.config import BRIEFING_PATTERN, PRONOUNCER_LEXICON
from weekly_ai_briefing.pronouncers import pronunciations

HEADER = """# Pronouncer lexicon

The IPA the briefing uses for names a speech engine is likely to get wrong. Phase D uses an entry's IPA exactly for
any name listed here and writes new IPA only for names that are not. After each edition is written,
`uv run python -m weekly_ai_briefing.pronouncer_lexicon <edition>` adds the names it introduced. To correct an
entry, edit its IPA here; later editions follow it.

| Name | IPA | First used |
|---|---|---|
"""
ROW = re.compile(r"^\| (?P<name>[^|]+?) \| (?P<ipa>[^|]+?) \| (?P<first>[^|]*?) \|$", re.MULTILINE)


class Entry(NamedTuple):
    ipa: str
    first_used: str


def read_lexicon(path: Path = PRONOUNCER_LEXICON) -> dict[str, Entry]:
    if not path.is_file():
        return {}
    return {
        match["name"]: Entry(match["ipa"], match["first"])
        for match in ROW.finditer(path.read_text(encoding="utf-8"))
        if match["name"] != "Name" and not match["name"].startswith("---")
    }


def write_lexicon(lexicon: dict[str, Entry], path: Path = PRONOUNCER_LEXICON) -> None:
    rows = "".join(f"| {name} | {entry.ipa} | {entry.first_used} |\n"
                   for name, entry in sorted(lexicon.items(), key=lambda item: item[0].casefold()))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(HEADER + rows, encoding="utf-8")


def edition_date(path: Path) -> str:
    match = re.fullmatch(BRIEFING_PATTERN, path.name)
    return match[1] if match else ""


def mismatches(markdown: str, lexicon: dict[str, Entry]) -> list[tuple[str, str, str]]:
    """Each (name, IPA in the edition, IPA in the lexicon) where the edition departs from the lexicon."""
    return [(name, ipa, lexicon[name].ipa) for name, ipa in pronunciations(markdown).items()
            if name in lexicon and lexicon[name].ipa != ipa]


def update_lexicon(edition: Path, path: Path = PRONOUNCER_LEXICON) -> list[str]:
    """Adds the edition's new names to the lexicon and returns them; existing entries are never changed."""
    lexicon = read_lexicon(path)
    found = pronunciations(edition.read_text(encoding="utf-8"))
    added = [name for name in found if name not in lexicon]
    for name in added:
        lexicon[name] = Entry(found[name], edition_date(edition))
    if added or not path.is_file():
        write_lexicon(lexicon, path)
    return added


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Add the names an edition introduced to the pronouncer lexicon.")
    parser.add_argument("editions", nargs="+", type=Path, help="edition markdown files, oldest first")
    args = parser.parse_args(argv)
    lexicon = read_lexicon()
    for edition in args.editions:
        for name, used, listed in mismatches(edition.read_text(encoding="utf-8"), lexicon):
            print(f"{edition.name}: {name} is written {used!r} but the lexicon has {listed!r}; the lexicon is kept")
        added = update_lexicon(edition)
        lexicon = read_lexicon()
        print(f"{edition.name}: added {len(added)} name(s)" + (f": {', '.join(added)}" if added else ""))


if __name__ == "__main__":
    main()
