import base64
from pathlib import Path

import pytest
from anthropic.types import (
    Base64PDFSource,
    DocumentBlock,
    PlainTextSource,
    TextBlock,
    WebFetchBlock,
    WebFetchToolResultBlock,
    WebFetchToolResultErrorBlock,
)

from weekly_ai_briefing import source_cache as c

DATE = "2026-11-28"


@pytest.fixture
def cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    folder = tmp_path / "source_document_cache"
    monkeypatch.setattr(c, "SOURCE_CACHE_FOLDER", folder)
    return folder


def fetched(url: str, source: PlainTextSource | Base64PDFSource) -> WebFetchToolResultBlock:
    return WebFetchToolResultBlock(
        type="web_fetch_tool_result",
        tool_use_id="t1",
        content=WebFetchBlock(type="web_fetch_result", url=url, retrieved_at="2026-11-24T10:00:00Z",
                              content=DocumentBlock(type="document", source=source)),
    )


def test_file_stem_is_readable_and_unique():
    stem = c.file_stem("https://www.bankofengland.co.uk/financial-stability-report/2026/november-2026")
    assert stem.startswith("bankofengland-co-uk-financial-stability-report-2026-november-2026-")
    assert stem != c.file_stem("https://www.bankofengland.co.uk/financial-stability-report/2026/may-2026")


def test_save_fetch_results_keeps_text_and_pdfs_and_skips_the_rest(cache: Path):
    text = PlainTextSource(type="text", media_type="text/plain", data="Page text.")
    pdf = Base64PDFSource(type="base64", media_type="application/pdf", data=base64.b64encode(b"%PDF-1").decode())
    error = WebFetchToolResultBlock(
        type="web_fetch_tool_result", tool_use_id="t2",
        content=WebFetchToolResultErrorBlock(type="web_fetch_tool_result_error", error_code="url_not_accessible"),
    )
    saved = c.save_fetch_results(DATE, [
        TextBlock(type="text", text="hi"),
        fetched("https://example.com/a", text),
        fetched("https://example.com/b.pdf", pdf),
        error,
    ])
    assert [path.suffix for path in saved] == [".md", ".pdf"]
    assert saved[0].read_text(encoding="utf-8") == (
        "URL: https://example.com/a\nFetched: 2026-11-24T10:00:00Z\n\nPage text."
    )
    assert saved[1].read_bytes() == b"%PDF-1"
    assert saved[0].parent == cache / DATE


def test_prune_keeps_the_newest_dates_and_other_files(cache: Path):
    for name in ("2026-11-14", "2026-11-21", "2026-11-28", "notes"):
        (cache / name).mkdir(parents=True)
    removed = c.prune(keep=2)
    assert [path.name for path in removed] == ["2026-11-14"]
    assert sorted(path.name for path in cache.iterdir()) == ["2026-11-21", "2026-11-28", "notes"]


def test_prune_without_a_cache_does_nothing(cache: Path):
    assert c.prune() == []
