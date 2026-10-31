#! python3
# usage: uv run python -m weekly_ai_briefing.publish [--date YYYY-MM-DD] [--no-upload]
#
# Uploads an edition's mp3 files as assets of a GitHub release (tag: see
# edition_name), then regenerates the GitHub Pages site: index.html plus one
# page per edition in editions/html_format/. The pages play the mp3s straight
# from the release assets. Commit and push index.html and editions/html_format/
# afterwards to publish. Needs the GitHub CLI (gh), logged in.

import argparse
import html
import shutil
import subprocess
from typing import NamedTuple

from weekly_ai_briefing.config import GITHUB_REPO, HTML_FOLDER, MARKDOWN_FOLDER, MP3_FOLDER, POST_TITLE, SITE_INDEX
from weekly_ai_briefing.convert_for_blogger import markdown_to_html, strip_heading
from weekly_ai_briefing.email_briefing.briefing import (
    Section,
    edition_name,
    is_text_only,
    list_briefings,
    mp3_filename,
    split_sections,
)
from weekly_ai_briefing.bottom_matter import split_bottom_matter
from weekly_ai_briefing.html_rendering import render_template


class Edition(NamedTuple):
    date: str
    briefing_stem: str
    has_audio: bool
    title: str
    summary: str


def page_title(date: str) -> str:
    return f"{POST_TITLE} - {date}"


def release_asset_url(tag: str, filename: str) -> str:
    return f"https://github.com/{GITHUB_REPO}/releases/download/{tag}/{filename}"


def audio_player(url: str) -> str:
    # preload="none": opening a page must not download the whole edition on a phone.
    return f'<audio controls preload="none"><source type="audio/mpeg" src="{html.escape(url)}"></audio>'


def insert_after_heading(rendered: str, extra: str) -> str:
    """Places extra after the first level-2 heading, or first when there is none."""
    end = rendered.find("</h2>")
    if end == -1:
        return f"{extra}\n{rendered}"
    end += len("</h2>")
    return f"{rendered[:end]}\n{extra}{rendered[end:]}"


def render_edition_page(date: str, briefing_stem: str, sections: list[Section], has_audio: bool) -> str:
    """Renders one briefing, with a player under each voiced section's heading when has_audio."""
    tag = edition_name(date)
    parts = []
    for number, section in enumerate(sections, start=1):
        markdown = strip_heading(section.markdown) if number == 1 else section.markdown  # the page has its own title
        rendered = markdown_to_html(markdown)
        if has_audio and not is_text_only(section):
            url = release_asset_url(tag, mp3_filename(briefing_stem, number))
            rendered = insert_after_heading(rendered, audio_player(url))
        parts.append((number, rendered))
    return render_template("github_hosted_edition.html.j2", title=page_title(date), sections=parts)


def render_index(editions: list[Edition]) -> str:
    """Renders the editions in the order given: date, title with summary, and icons, with no column headings."""
    return render_template(
        "github_hosted_index.html.j2", title=POST_TITLE, html_folder=HTML_FOLDER.as_posix(), editions=editions
    )


def write_site(release_tags: set[str]) -> list[Edition]:
    """Writes the page of every briefing in MARKDOWN_FOLDER and the index; audio where a release exists."""
    HTML_FOLDER.mkdir(parents=True, exist_ok=True)
    editions = []
    for date, path in list_briefings(MARKDOWN_FOLDER):
        bottom_matter, body = split_bottom_matter(path.read_text(encoding="utf-8"))
        if bottom_matter is None:
            raise ValueError(
                f"{path} has no YAML bottom matter"
                " (title, publication_date, survey_begin_date, survey_last_date, summary)"
            )
        if bottom_matter.publication_date.isoformat() != date:
            raise ValueError(
                f"{path}: publication_date {bottom_matter.publication_date} does not match the file name date {date}"
            )
        edition = Edition(
            date, path.stem, edition_name(date) in release_tags, bottom_matter.title, bottom_matter.summary
        )
        sections = split_sections(body)
        page = render_edition_page(date, path.stem, sections, edition.has_audio)
        (HTML_FOLDER / f"{path.stem}.html").write_text(page, encoding="utf-8")
        editions.append(edition)
    SITE_INDEX.write_text(render_index(editions), encoding="utf-8")
    return editions


def gh(*args: str) -> str:
    executable = shutil.which("gh")
    if executable is None:
        raise RuntimeError("GitHub CLI not found; install it (winget install GitHub.cli) and run 'gh auth login'")
    # gh's own error messages go straight to the terminal.
    return subprocess.run([executable, *args], check=True, stdout=subprocess.PIPE, text=True).stdout


def release_tags() -> set[str]:
    output = gh("release", "list", "--repo", GITHUB_REPO, "--limit", "1000", "--json", "tagName", "--jq", ".[].tagName")
    return set(output.split())


def upload_release(date: str, existing_tags: set[str]) -> str:
    """Attaches the edition's mp3 files to its release, creating the release if needed. Returns the tag."""
    tag = edition_name(date)
    folder = MP3_FOLDER / tag
    mp3_paths = [str(path) for path in sorted(folder.glob("*.mp3"))]
    if not mp3_paths:
        raise FileNotFoundError(f"No mp3 files in {folder}; run 'python -m weekly_ai_briefing.email_briefing' first")
    if tag in existing_tags:
        gh("release", "upload", tag, *mp3_paths, "--clobber", "--repo", GITHUB_REPO)
    else:
        gh(
            "release", "create", tag, *mp3_paths, "--repo", GITHUB_REPO,
            "--title", page_title(date), "--notes", f"Audio for the {date} briefing.",
        )
    return tag


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload an edition's audio to a GitHub release and rebuild the site.")
    parser.add_argument("--date", metavar="YYYY-MM-DD", default=None, help="edition to upload (default: the latest)")
    parser.add_argument(
        "--upload", action=argparse.BooleanOptionalAction, default=True,
        help="upload the edition's mp3 files to its release; --no-upload only rebuilds the site",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    try:
        dates = [date for date, _ in list_briefings(MARKDOWN_FOLDER)]
        if not dates:
            raise SystemExit(f"error: no briefings in {MARKDOWN_FOLDER}")
        date = args.date or dates[0]
        if date not in dates:
            raise SystemExit(f"error: no briefing dated {date} in {MARKDOWN_FOLDER}")
        tags = release_tags()
        if args.upload:
            tags.add(upload_release(date, tags))
            print(f"Uploaded {date} audio to release {edition_name(date)}")
        editions = write_site(tags)
        print(f"Wrote {SITE_INDEX} and {len(editions)} pages in {HTML_FOLDER}")
        print(f"Next: git add {SITE_INDEX} {HTML_FOLDER.as_posix()}; git commit; git push")
    except KeyboardInterrupt:
        print("Interrupted")
    except ValueError as error:
        raise SystemExit(f"error: {error}") from error


if __name__ == "__main__":
    main()
