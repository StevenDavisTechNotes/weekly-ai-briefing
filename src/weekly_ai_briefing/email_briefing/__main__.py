#! python3
# usage: uv run python -m weekly_ai_briefing.email_briefing [--section N [N ...]] [--no-send-email]
# Email credentials come from the environment; see mailer.py.

import argparse

from weekly_ai_briefing.config import MARKDOWN_FOLDER, MP3_FOLDER

from .audio import generate_mp3
from .briefing import Section, edition_name, find_latest_briefing, is_text_only, mp3_filename, split_sections
from .mailer import send_email


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Voice the latest weekly briefing and email it section by section.")
    parser.add_argument(
        "--section", type=int, nargs="+", metavar="N", default=None,
        help="1-based section numbers to process (default: all sections)",
    )
    parser.add_argument(
        "--send-email", action=argparse.BooleanOptionalAction, default=True,
        help="email each section; --no-send-email only writes the mp3 files to editions/mp3_format/ai-outlook-briefing-<date>/",
    )
    return parser.parse_args(argv)


def select_sections(requested: list[int] | None, count: int) -> set[int]:
    """Returns the 1-based section numbers to process, exiting if any is out of range."""
    selected = set(requested) if requested is not None else set(range(1, count + 1))
    invalid = sorted(n for n in selected if not 1 <= n <= count)
    if invalid:
        raise SystemExit(f"error: --section {invalid} out of range; the briefing has sections 1-{count}")
    return selected


def email_subject(date: str, section: Section) -> str:
    return f"Weekly AI Briefing - {date} - {section.title}"


def email_body(date: str, number: int, count: int, section: Section, has_audio: bool) -> str:
    intro = (
        f"Hi Steve,\n\n"
        f"This is section {number} of {count} of this "
        f"week's AI briefing (dated {date}): {section.title}. "
    )
    if has_audio:
        return intro + "The audio version is attached as an MP3.\n"
    return intro + "It has no audio version.\n\n" + section.markdown


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    try:
        briefing_path, date = find_latest_briefing(MARKDOWN_FOLDER)
        sections = split_sections(briefing_path.read_text(encoding="utf-8"))
        print(f"Using {briefing_path}: {len(sections)} sections")
        selected = select_sections(args.section, len(sections))
        edition_folder = MP3_FOLDER / edition_name(date)
        edition_folder.mkdir(parents=True, exist_ok=True)
        for number, section in enumerate(sections, start=1):
            if number not in selected:
                continue
            print(f"[{number}/{len(sections)}] {section.title}")
            mp3_path = None
            if is_text_only(section):
                if not args.send_email:
                    print("  Text-only section; nothing to generate")
                    continue
            else:
                mp3_path = edition_folder / mp3_filename(briefing_path.stem, number)
                generate_mp3(section.markdown, mp3_path)
                if not args.send_email:
                    continue
            send_email(
                subject=email_subject(date, section),
                body=email_body(date, number, len(sections), section, has_audio=mp3_path is not None),
                mp3_path=mp3_path,
            )
    except KeyboardInterrupt:
        print("Interrupted")


if __name__ == "__main__":
    main()
