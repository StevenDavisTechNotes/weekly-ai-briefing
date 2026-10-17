#! python3
# usage: uv run python -m src.weekly_ai_briefing.convert_for_blogger history/YYYY-MM-DD-ai-outlook-briefing.md
#
# Writes blog_posts/<same stem>.xml: a Blogger import file (an Atom feed holding
# one post) that Blogger accepts under Settings > Manage blog > Import content.

import argparse
import html
import re
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path

BLOG_POSTS_FOLDER = Path("blog_posts")
BRIEFING_DATE = re.compile(r"(\d{4}-\d{2}-\d{2})")
AUTHOR = "Steven Davis"
LABEL = "Weekly AI Briefing"

ATOM_NS = "http://www.w3.org/2005/Atom"
KIND_SCHEME = "http://schemas.google.com/g/2005#kind"
KIND_POST = "http://schemas.google.com/blogger/2008/kind#post"
LABEL_SCHEME = "http://www.blogger.com/atom/ns#"

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
RULE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
BULLET = re.compile(r"^\s*[-*+]\s+(.*)$")
NUMBERED = re.compile(r"^\s*\d+[.)]\s+(.*)$")
TABLE_DELIMITER = re.compile(r"^\s*\|?\s*:?-+:?\s*(?:\|\s*:?-+:?\s*)*\|?\s*$")


def inline_html(text: str) -> str:
    """Escapes text and renders inline code, links, bold and italics."""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)\s]+)\)",
        lambda m: f'<a href="{m.group(2).replace('"', "&quot;")}">{m.group(1)}</a>',
        text,
    )
    text = re.sub(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1", r"<strong>\2</strong>", text)
    return re.sub(r"(?<![*\w])\*(?=\S)(.+?)(?<=\S)\*(?![*\w])", r"<em>\1</em>", text)


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_html(lines: list[str]) -> str:
    """Renders a pipe table: header row, delimiter row, body rows."""
    header = "".join(f"<th>{inline_html(cell)}</th>" for cell in table_cells(lines[0]))
    rows = [
        "<tr>" + "".join(f"<td>{inline_html(cell)}</td>" for cell in table_cells(line)) + "</tr>" for line in lines[2:]
    ]
    return f'<table border="1"><thead><tr>{header}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


def is_table_start(lines: list[str], index: int) -> bool:
    return "|" in lines[index] and index + 1 < len(lines) and bool(TABLE_DELIMITER.match(lines[index + 1]))


def take_while(lines: list[str], index: int, pattern: re.Pattern[str]) -> tuple[list[str], int]:
    """Collects the captured text of consecutive lines matching pattern."""
    items: list[str] = []
    while index < len(lines) and (match := pattern.match(lines[index])):
        items.append(match.group(1))
        index += 1
    return items, index


def take_paragraph(lines: list[str], index: int) -> tuple[str, int]:
    """Joins lines up to the next blank line or block-level element."""
    parts: list[str] = []
    while index < len(lines) and lines[index].strip() and not starts_block(lines, index):
        parts.append(lines[index].strip())
        index += 1
    return " ".join(parts), index


def starts_block(lines: list[str], index: int) -> bool:
    line = lines[index]
    return any(p.match(line) for p in (HEADING, RULE, BULLET, NUMBERED)) or is_table_start(lines, index)


def markdown_to_html(markdown: str) -> str:
    """Converts the subset of markdown the briefings use into HTML blocks."""
    lines = markdown.splitlines()
    blocks: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
        elif heading := HEADING.match(line):
            level = len(heading.group(1))
            blocks.append(f"<h{level}>{inline_html(heading.group(2))}</h{level}>")
            index += 1
        elif RULE.match(line):
            blocks.append("<hr />")
            index += 1
        elif is_table_start(lines, index):
            end = index + 2
            while end < len(lines) and "|" in lines[end] and lines[end].strip():
                end += 1
            blocks.append(table_html(lines[index:end]))
            index = end
        elif BULLET.match(line) or NUMBERED.match(line):
            tag, pattern = ("ul", BULLET) if BULLET.match(line) else ("ol", NUMBERED)
            items, index = take_while(lines, index, pattern)
            blocks.append(f"<{tag}>" + "".join(f"<li>{inline_html(item)}</li>" for item in items) + f"</{tag}>")
        else:
            paragraph, index = take_paragraph(lines, index)
            blocks.append(f"<p>{inline_html(paragraph)}</p>")
    return "\n".join(blocks)


def split_title(markdown: str, fallback: str) -> tuple[str, str]:
    """Pulls a leading '# ' heading out to serve as the post title."""
    match = re.match(r"\s*#\s+(.+?)\s*#*\s*(?:\n|$)", markdown)
    if not match:
        return fallback, markdown
    title, body_start = match.group(1).strip(), match.end()
    return title, markdown[body_start:]


def post_timestamp(source: Path) -> str:
    """Uses the briefing date in the file name, else the file's modified time."""
    if match := BRIEFING_DATE.search(source.stem):
        moment = datetime.fromisoformat(match.group(1)).replace(hour=12, tzinfo=UTC)
    else:
        moment = datetime.fromtimestamp(source.stat().st_mtime, tz=UTC)
    return moment.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def build_feed(title: str, body_html: str, timestamp: str, post_id: str) -> ET.ElementTree[ET.Element]:
    ET.register_namespace("", ATOM_NS)

    def child(parent: ET.Element, tag: str, text: str | None = None, **attributes: str) -> ET.Element:
        element = ET.SubElement(parent, f"{{{ATOM_NS}}}{tag}", attributes)
        element.text = text
        return element

    feed = ET.Element(f"{{{ATOM_NS}}}feed")
    child(feed, "id", "tag:blogger.com,1999:blog-0")
    child(feed, "updated", timestamp)
    child(feed, "title", LABEL, type="text")
    child(feed, "generator", "Blogger", uri="http://www.blogger.com", version="7.00")

    entry = child(feed, "entry")
    child(entry, "id", f"tag:blogger.com,1999:blog-0.post-{post_id}")
    child(entry, "published", timestamp)
    child(entry, "updated", timestamp)
    child(entry, "category", scheme=KIND_SCHEME, term=KIND_POST)
    child(entry, "category", scheme=LABEL_SCHEME, term=LABEL)
    child(entry, "title", title, type="text")
    child(entry, "content", body_html, type="html")
    author = child(entry, "author")
    child(author, "name", AUTHOR)
    ET.indent(feed)
    return ET.ElementTree(feed)


def convert(source: Path, output_dir: Path = BLOG_POSTS_FOLDER) -> Path:
    """Writes output_dir/<source stem>.xml and returns its path."""
    markdown = source.read_text(encoding="utf-8")
    title, body = split_title(markdown, fallback=source.stem)
    timestamp = post_timestamp(source)
    post_id = re.sub(r"\D", "", timestamp)[:14]
    feed = build_feed(title, markdown_to_html(body), timestamp, post_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{source.stem}.xml"
    feed.write(output_path, encoding="utf-8", xml_declaration=True)
    return output_path


def main() -> None:
    try:
        parser = argparse.ArgumentParser(description="Convert a briefing .md file to a Blogger import .xml file.")
        parser.add_argument("source", type=Path, help="path to a .md file in the history folder")
        args = parser.parse_args()
        print(f"Wrote {convert(args.source)}")
    except KeyboardInterrupt:
        print("Interrupted")


if __name__ == "__main__":
    main()
