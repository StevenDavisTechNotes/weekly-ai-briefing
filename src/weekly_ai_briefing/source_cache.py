"""Short-lived copies of the sources phase A reads, in source_document_cache/<date>/, which git ignores.

Verification reads a copy only to explain a difference between a fact and its live source. Publishing deletes all
but the newest SOURCE_CACHE_KEEP date folders.

usage:
    uv run python -m weekly_ai_briefing.source_cache --prune
"""

import argparse
import base64
import hashlib
import re
import shutil
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

from weekly_ai_briefing.config import SOURCE_CACHE_FOLDER, SOURCE_CACHE_KEEP

DATE_FOLDER = re.compile(r"\d{4}-\d{2}-\d{2}")


def cache_folder(date: str) -> Path:
    return SOURCE_CACHE_FOLDER / date


def file_stem(url: str) -> str:
    """A readable, unique file name for a URL: its host and path as a slug, plus a short hash."""
    slug = re.sub(r"[^A-Za-z0-9]+", "-", re.sub(r"^https?://(www\.)?", "", url)).strip("-")[:80]
    return f"{slug}-{hashlib.sha256(url.encode()).hexdigest()[:8]}"


def save_fetch_results(date: str, content: Iterable[Any]) -> list[Path]:
    """Saves the page text, or PDF, of each successful web_fetch result among a response's content blocks."""
    saved = []
    for block in content:
        if getattr(block, "type", None) != "web_fetch_tool_result":
            continue
        result = block.content
        if getattr(result, "type", None) != "web_fetch_result":
            continue  # a fetch error; nothing was read
        source = result.content.source
        folder = cache_folder(date)
        folder.mkdir(parents=True, exist_ok=True)
        stem = file_stem(result.url)
        if source.type == "base64":
            path = folder / f"{stem}.pdf"
            path.write_bytes(base64.b64decode(source.data))
        else:
            path = folder / f"{stem}.md"
            header = f"URL: {result.url}\nFetched: {result.retrieved_at or 'unknown'}\n\n"
            path.write_text(header + source.data, encoding="utf-8")
        saved.append(path)
    return saved


def prune(keep: int = SOURCE_CACHE_KEEP) -> list[Path]:
    """Deletes every date folder but the newest `keep`; anything else in the cache folder is left alone."""
    if not SOURCE_CACHE_FOLDER.is_dir():
        return []
    dated = sorted(path for path in SOURCE_CACHE_FOLDER.iterdir()
                   if path.is_dir() and DATE_FOLDER.fullmatch(path.name))
    doomed = dated[:-keep] if keep > 0 else dated
    for path in doomed:
        shutil.rmtree(path)
    return doomed


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Manage the short-lived cache of sources phase A read.")
    parser.add_argument("--prune", action="store_true", required=True,
                        help=f"delete all but the newest {SOURCE_CACHE_KEEP} date folders")
    parser.add_argument("--keep", type=int, default=SOURCE_CACHE_KEEP, help="date folders to keep")
    args = parser.parse_args(argv)
    removed = prune(args.keep)
    print(f"Removed {len(removed)} source cache folder(s)" + (f": {', '.join(p.name for p in removed)}" if removed
                                                             else ""))


if __name__ == "__main__":
    main()
