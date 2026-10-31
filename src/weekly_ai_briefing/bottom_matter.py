"""YAML bottom matter of an edition: title, dates, summary and the indicator ledger.

The block ends the markdown, between a line holding only --- and a final line holding only ---.
Writers emit body + "\n" + format_bottom_matter(bm); split_bottom_matter undoes that.
"""

import datetime
import json
from typing import Any, NamedTuple

import yaml


class BottomMatter(NamedTuple):
    title: str
    publication_date: datetime.date
    survey_begin_date: datetime.date
    survey_last_date: datetime.date
    summary: str
    indicators: tuple[dict[str, Any], ...] = ()


DELIMITER = "---"
REQUIRED_KEYS = ("title", "publication_date", "survey_begin_date", "survey_last_date", "summary")


def _text(data: dict[str, Any], key: str) -> str:
    value = data[key]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"bottom matter {key} must be non-empty text")
    return value.strip()


def _date(data: dict[str, Any], key: str) -> datetime.date:
    value = data[key]
    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value)
        except ValueError:
            pass
    raise ValueError(f"bottom matter {key} must be a YYYY-MM-DD date")


def _indicators(data: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    value = data.get("indicators")
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError("bottom matter indicators must be a list of mappings")
    return tuple(value)


def _load(yaml_text: str) -> Any:
    try:
        return yaml.safe_load(yaml_text)
    except yaml.YAMLError as error:
        raise ValueError(f"bottom matter is not valid YAML: {error}") from error


def _from_mapping(data: dict[str, Any]) -> BottomMatter:
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        raise ValueError(f"bottom matter is missing {', '.join(missing)}")
    title = _text(data, "title")
    summary = _text(data, "summary")
    publication_date = _date(data, "publication_date")
    survey_begin_date = _date(data, "survey_begin_date")
    survey_last_date = _date(data, "survey_last_date")
    if survey_begin_date > survey_last_date:
        raise ValueError("bottom matter survey_begin_date is after survey_last_date")
    return BottomMatter(title, publication_date, survey_begin_date, survey_last_date, summary, _indicators(data))


def parse_bottom_matter(yaml_text: str) -> BottomMatter:
    data = _load(yaml_text)
    if not isinstance(data, dict):
        raise ValueError("bottom matter is not a YAML mapping")
    return _from_mapping(data)


def format_bottom_matter(bottom_matter: BottomMatter) -> str:
    # JSON strings are valid YAML double-quoted scalars; they keep colons and quotes safe.
    ledger = (
        yaml.safe_dump({"indicators": list(bottom_matter.indicators)}, sort_keys=False, allow_unicode=True, width=4096)
        if bottom_matter.indicators
        else ""
    )
    return (
        f"{DELIMITER}\n"
        f"title: {json.dumps(bottom_matter.title, ensure_ascii=False)}\n"
        f"publication_date: {bottom_matter.publication_date.isoformat()}\n"
        f"survey_begin_date: {bottom_matter.survey_begin_date.isoformat()}\n"
        f"survey_last_date: {bottom_matter.survey_last_date.isoformat()}\n"
        f"summary: {json.dumps(bottom_matter.summary, ensure_ascii=False)}\n" + ledger + f"{DELIMITER}\n"
    )


def split_bottom_matter(markdown: str) -> tuple[BottomMatter | None, str]:
    """Returns the trailing bottom matter (None when absent) and the markdown before it.

    The block runs from the last two lines holding only ---. A markdown body may use --- as a
    horizontal rule, so a closing --- whose block is not a YAML mapping counts as no bottom matter.
    """
    lines = markdown.rstrip().splitlines()
    if not lines or lines[-1].strip() != DELIMITER:
        return None, markdown
    opening = next((i for i in range(len(lines) - 2, -1, -1) if lines[i].strip() == DELIMITER), None)
    if opening is None:
        return None, markdown
    data = _load("\n".join(lines[opening + 1:-1]))
    if not isinstance(data, dict):
        return None, markdown
    body = "\n".join(lines[:opening]).rstrip()
    return _from_mapping(data), body + "\n" if body else ""
