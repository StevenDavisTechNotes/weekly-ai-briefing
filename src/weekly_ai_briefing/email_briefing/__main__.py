#! python3
# usage: uv run python -m weekly_ai_briefing.email_briefing [--voice [--section N [N ...]]] [--email]
#
# Weekly order: --voice writes the mp3 files; weekly_ai_briefing.publish uploads them and builds the
# pages; push; then --email mails the link to the latest briefing's page (it refuses until the page is live).
# Email credentials come from the environment; see mailer.py.

import argparse
import urllib.error
import urllib.request

from weekly_ai_briefing.config import MARKDOWN_FOLDER, MP3_FOLDER

from .audio import generate_mp3
from .briefing import (
    Section,
    edition_name,
    edition_page_url,
    find_latest_briefing,
    is_text_only,
    mp3_filename,
    split_sections,
)
from .mailer import send_email


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Voice the latest weekly briefing and/or email the link to its page.")
    parser.add_argument(
        "--voice", action="store_true",
        help="write one mp3 per section to editions/mp3_format/ai-outlook-briefing-<date>/",
    )
    parser.add_argument(
        "--section", type=int, nargs="+", metavar="N", default=None,
        help="with --voice: 1-based section numbers to voice (default: all sections)",
    )
    parser.add_argument(
        "--email", action="store_true",
        help="email the link to the latest briefing's published page",
    )
    args = parser.parse_args(argv)
    if not (args.voice or args.email):
        parser.error("nothing to do; pass --voice and/or --email")
    if args.section is not None and not args.voice:
        parser.error("--section only applies with --voice")
    return args


def select_sections(requested: list[int] | None, count: int) -> set[int]:
    """Returns the 1-based section numbers to process, exiting if any is out of range."""
    selected = set(requested) if requested is not None else set(range(1, count + 1))
    invalid = sorted(n for n in selected if not 1 <= n <= count)
    if invalid:
        raise SystemExit(f"error: --section {invalid} out of range; the briefing has sections 1-{count}")
    return selected


def email_subject(date: str) -> str:
    return f"Weekly AI Briefing - {date}"


def email_body(date: str, page_url: str, sections: list[Section]) -> str:
    lines = [
        "Hi Steve,",
        "",
        f"This week's AI briefing (dated {date}) is ready to read and listen to:",
        page_url,
        "",
        "Sections:",
        *(f"{number}. {section.title}: {page_url}#section-{number}" for number, section in enumerate(sections, start=1)),
    ]
    return "\n".join(lines) + "\n"


def page_is_live(url: str) -> bool:
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return response.status == 200
    except urllib.error.URLError:  # includes HTTPError, e.g. 404 before GitHub Pages has built the page
        return False


def voice_sections(briefing_stem: str, date: str, sections: list[Section], selected: set[int]) -> None:
    edition_folder = MP3_FOLDER / edition_name(date)
    edition_folder.mkdir(parents=True, exist_ok=True)
    for number, section in enumerate(sections, start=1):
        if number not in selected:
            continue
        print(f"[{number}/{len(sections)}] {section.title}")
        if is_text_only(section):
            print("  Text-only section; nothing to generate")
            continue
        generate_mp3(section.markdown, edition_folder / mp3_filename(briefing_stem, number))


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    try:
        briefing_path, date = find_latest_briefing(MARKDOWN_FOLDER)
        sections = split_sections(briefing_path.read_text(encoding="utf-8"))
        print(f"Using {briefing_path}: {len(sections)} sections")
        if args.voice:
            voice_sections(briefing_path.stem, date, sections, select_sections(args.section, len(sections)))
        if args.email:
            page_url = edition_page_url(briefing_path.stem)
            if not page_is_live(page_url):
                raise SystemExit(
                    f"error: {page_url} is not live; run weekly_ai_briefing.publish, push, "
                    "wait for GitHub Pages to build, then retry"
                )
            send_email(subject=email_subject(date), body=email_body(date, page_url, sections))
    except KeyboardInterrupt:
        print("Interrupted")


if __name__ == "__main__":
    main()
