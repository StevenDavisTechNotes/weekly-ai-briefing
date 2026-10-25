"""YAML front matter of an edition: title, dates, summary and the indicator ledger.

Writers emit format_front_matter(fm) + "\n" + body; split_front_matter undoes that.
"""

import datetime
import json
import re
from typing import NamedTuple

import yaml


class FrontMatter(NamedTuple):
    title: str
    publication_date: datetime.date
    survey_begin_date: datetime.date
    survey_last_date: datetime.date
    summary: str
    indicators: tuple[dict, ...] = ()


FRONT_MATTER_BLOCK = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
YAML_FENCE = re.compile(r"^```ya?ml[ \t]*\n(.*?)\n```[ \t]*$", re.MULTILINE | re.DOTALL)

REQUIRED_KEYS = ("title", "publication_date", "survey_begin_date", "survey_last_date", "summary")


def _text(data: dict, key: str) -> str:
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"front matter {key} must be non-empty text")
    return value.strip()


def _date(data: dict, key: str) -> datetime.date:
    value = data[key]
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value)
        except ValueError:
            pass
    raise ValueError(f"front matter {key} must be a YYYY-MM-DD date")


def _indicators(data: dict) -> tuple[dict, ...]:
    value = data.get("indicators")
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError("front matter indicators must be a list of mappings")
    return tuple(value)


def parse_front_matter(yaml_text: str) -> FrontMatter:
    try:
        data = yaml.safe_load(yaml_text)
    except yaml.YAMLError as error:
        raise ValueError(f"front matter is not valid YAML: {error}") from error
    if not isinstance(data, dict):
        raise ValueError("front matter is not a YAML mapping")
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        raise ValueError(f"front matter is missing {', '.join(missing)}")
    title = _text(data, "title")
    summary = _text(data, "summary")
    publication_date = _date(data, "publication_date")
    survey_begin_date = _date(data, "survey_begin_date")
    survey_last_date = _date(data, "survey_last_date")
    if survey_begin_date > survey_last_date:
        raise ValueError("front matter survey_begin_date is after survey_last_date")
    return FrontMatter(
        title, publication_date, survey_begin_date, survey_last_date, summary, _indicators(data)
    )


def format_front_matter(front_matter: FrontMatter) -> str:
    # JSON strings are valid YAML double-quoted scalars; they keep colons and quotes safe.
    ledger = (
        yaml.safe_dump({"indicators": list(front_matter.indicators)}, sort_keys=False, allow_unicode=True, width=4096)
        if front_matter.indicators
        else ""
    )
    return (
        "---\n"
        f"title: {json.dumps(front_matter.title, ensure_ascii=False)}\n"
        f"publication_date: {front_matter.publication_date.isoformat()}\n"
        f"survey_begin_date: {front_matter.survey_begin_date.isoformat()}\n"
        f"survey_last_date: {front_matter.survey_last_date.isoformat()}\n"
        f"summary: {json.dumps(front_matter.summary, ensure_ascii=False)}\n" + ledger + "---\n"
    )


def split_front_matter(markdown: str) -> tuple[FrontMatter | None, str]:
    """Returns the leading front matter (None when absent) and the rest of the markdown."""
    match = FRONT_MATTER_BLOCK.match(markdown)
    if match is None:
        return None, markdown
    return parse_front_matter(match.group(1)), markdown[match.end() :].lstrip("\n")


def extract_yaml_block(briefing: str) -> tuple[FrontMatter, str]:
    """Takes the last fenced yaml block out of a generated briefing; returns it parsed and the remaining text."""
    matches = list(YAML_FENCE.finditer(briefing))
    if not matches:
        raise ValueError("the briefing has no ```yaml block")
    match = matches[-1]
    front_matter = parse_front_matter(match.group(1))
    body = (briefing[: match.start()] + briefing[match.end() :]).rstrip() + "\n"
    return front_matter, body
