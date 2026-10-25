import datetime

import pytest

from weekly_ai_briefing.front_matter import (
    FrontMatter,
    extract_yaml_block,
    format_front_matter,
    split_front_matter,
)

FRONT_MATTER = FrontMatter(
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


def test_markdown_without_front_matter_is_returned_unchanged():
    assert split_front_matter("# Title\n\nBody\n") == (None, "# Title\n\nBody\n")


def test_formatted_front_matter_round_trips_with_awkward_text():
    assert split_front_matter(format_front_matter(FRONT_MATTER) + "\n# Title\n") == (FRONT_MATTER, "# Title\n")


def test_extract_yaml_block_removes_the_block_from_the_body():
    briefing = f"## A\n\nText.\n\n```yaml\n{YAML_KEYS}```\n"
    front_matter, body = extract_yaml_block(briefing)
    assert front_matter.publication_date == datetime.date(2026, 10, 24)
    assert body == "## A\n\nText.\n"


def test_extract_yaml_block_requires_a_block():
    with pytest.raises(ValueError, match="no ```yaml block"):
        extract_yaml_block("## A\n")


def test_missing_key_is_named():
    block = YAML_KEYS.replace('summary: "S"\n', "")
    with pytest.raises(ValueError, match="missing summary"):
        extract_yaml_block(f"## A\n\n```yaml\n{block}```\n")


def test_survey_window_must_not_be_reversed():
    block = YAML_KEYS.replace("survey_begin_date: 2026-10-17", "survey_begin_date: 2026-10-24")
    with pytest.raises(ValueError, match="after survey_last_date"):
        extract_yaml_block(f"## A\n\n```yaml\n{block}```\n")


def test_indicator_ledger_round_trips():
    indicator = {
        "id": "I-2026-10-24-01",
        "name": 'Ledger: "quoted"',
        "opened": datetime.date(2026, 10, 24),
        "prior": 0.25,
        "history": [{"date": datetime.date(2026, 10, 24), "event": "opened"}],
    }
    front_matter = FRONT_MATTER._replace(indicators=(indicator,))
    assert split_front_matter(format_front_matter(front_matter) + "\n# Title\n") == (front_matter, "# Title\n")


def test_extract_yaml_block_keeps_the_indicator_ledger():
    block = YAML_KEYS + "indicators:\n- id: I-2026-10-24-01\n  deadline: 2027-01-24\n"
    front_matter, _ = extract_yaml_block(f"## A\n\n```yaml\n{block}```\n")
    assert front_matter.indicators == ({"id": "I-2026-10-24-01", "deadline": datetime.date(2027, 1, 24)},)


def test_indicators_must_be_a_list_of_mappings():
    block = YAML_KEYS + "indicators: open\n"
    with pytest.raises(ValueError, match="indicators must be a list of mappings"):
        extract_yaml_block(f"## A\n\n```yaml\n{block}```\n")
