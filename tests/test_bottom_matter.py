import datetime
from typing import Any

import pytest

from weekly_ai_briefing.bottom_matter import (
    BottomMatter,
    format_bottom_matter,
    split_bottom_matter,
)

BOTTOM_MATTER = BottomMatter(
    title='Costs: the "real" story',
    publication_date=datetime.date(2026, 10, 24),
    survey_begin_date=datetime.date(2026, 10, 17),
    survey_last_date=datetime.date(2026, 10, 23),
    summary="Plain summary.",
)

YAML_KEYS = (
    'title: "T"\n'
    "publication_date: 2026-10-24\n"
    "survey_begin_date: 2026-10-17\n"
    "survey_last_date: 2026-10-23\n"
    'summary: "S"\n'
)


def test_markdown_without_bottom_matter_is_returned_unchanged() -> None:
    assert split_bottom_matter("# Title\n\nBody\n") == (None, "# Title\n\nBody\n")


def test_formatted_bottom_matter_round_trips_with_awkward_text() -> None:
    assert split_bottom_matter("# Title\n\n" + format_bottom_matter(BOTTOM_MATTER)) == (BOTTOM_MATTER, "# Title\n")


def test_bottom_matter_is_removed_from_the_body() -> None:
    bottom_matter, body = split_bottom_matter(f"## A\n\nText.\n\n---\n{YAML_KEYS}---\n")
    assert bottom_matter is not None
    assert bottom_matter.publication_date == datetime.date(2026, 10, 24)
    assert body == "## A\n\nText.\n"


def test_horizontal_rules_in_the_body_are_kept() -> None:
    bottom_matter, body = split_bottom_matter(f"## A\n\n---\n\n## B\n\n---\n\n{YAML_KEYS}\n---\n\n")
    assert bottom_matter is not None
    assert body == "## A\n\n---\n\n## B\n"


def test_windows_line_endings_are_accepted() -> None:
    markdown = f"## A\n\n---\n{YAML_KEYS}---\n".replace("\n", "\r\n")
    bottom_matter, body = split_bottom_matter(markdown)
    assert bottom_matter is not None
    assert body == "## A\n"


def test_a_trailing_horizontal_rule_is_not_bottom_matter() -> None:
    markdown = "## A\n\n---\n\nJust prose.\n\n---\n"
    assert split_bottom_matter(markdown) == (None, markdown)


def test_a_leading_block_is_no_longer_read() -> None:
    markdown = f"---\n{YAML_KEYS}---\n\n## A\n\nText.\n"
    assert split_bottom_matter(markdown) == (None, markdown)


def test_missing_key_is_named() -> None:
    block = YAML_KEYS.replace('summary: "S"\n', "")
    with pytest.raises(ValueError, match="missing summary"):
        split_bottom_matter(f"## A\n\n---\n{block}---\n")


def test_survey_window_must_not_be_reversed() -> None:
    block = YAML_KEYS.replace("survey_begin_date: 2026-10-17", "survey_begin_date: 2026-10-24")
    with pytest.raises(ValueError, match="after survey_last_date"):
        split_bottom_matter(f"## A\n\n---\n{block}---\n")


def test_indicator_ledger_round_trips() -> None:
    indicator: dict[str, Any] = {
        "id": "I-2026-10-24-01",
        "name": 'Ledger: "quoted"',
        "opened": datetime.date(2026, 10, 24),
        "prior": 0.25,
        "history": [{"date": datetime.date(2026, 10, 24), "event": "opened"}],
    }
    bottom_matter = BOTTOM_MATTER._replace(indicators=(indicator,))
    assert split_bottom_matter("# Title\n\n" + format_bottom_matter(bottom_matter)) == (bottom_matter, "# Title\n")


def test_indicators_must_be_a_list_of_mappings() -> None:
    block = YAML_KEYS + "indicators: open\n"
    with pytest.raises(ValueError, match="indicators must be a list of mappings"):
        split_bottom_matter(f"## A\n\n---\n{block}---\n")
