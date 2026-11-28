"""Run metrics: one small file per edition, so research quality and cost can be followed week to week.

Counts come from the run's own files: facts per dimension, change types, source types and full-document reads from
the fact sheet; verdicts from the verification; spoken words from the edition. Minutes and tokens per phase come from
state/runs/<date>/phase_usage.json, which the API script writes, or which `--phase` adds to by hand for a run in an
agent harness.

usage:
    uv run python -m weekly_ai_briefing.run_metrics 2026-11-28                            # write metrics.md
    uv run python -m weekly_ai_briefing.run_metrics 2026-11-28 --phase A --minutes 108 --tokens 396139
    uv run python -m weekly_ai_briefing.run_metrics --history                             # one line per run
"""

import argparse
import json
import re
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from weekly_ai_briefing.config import MARKDOWN_FOLDER, STATE_FOLDER
from weekly_ai_briefing.edition_checks import spoken_words

DIMENSION_TAGS = (
    "AI Technology",
    "Quantum",
    "Enterprise",
    "Physical AI",
    "Human and Machine Agency",
    "Economic",
    "Financial Services",
)
VERDICTS = ("confirmed", "corrected", "unconfirmed", "dropped")
CHANGE_TYPES = ("new trend", "acceleration", "deceleration", "reversal", "level only")
SOURCE_TYPES = ("primary", "wire or trade", "analyst", "secondhand")

FACT = re.compile(r"^### F-\d+(?: \[(?P<tag>[^\]]+)\])?", re.MULTILINE)
VERDICT = re.compile(rf"^- F-\d+: (?P<verdict>{'|'.join(VERDICTS)})\b", re.MULTILINE)


def runs_folder() -> Path:
    return STATE_FOLDER / "runs"


def usage_path(date: str) -> Path:
    return runs_folder() / date / "phase_usage.json"


def load_usage(date: str) -> dict[str, dict[str, float]]:
    path = usage_path(date)
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def record_usage(date: str, phase: str, minutes: float | None = None, tokens: int | None = None,
                 requests: int | None = None) -> None:
    """Adds one phase's minutes, tokens and requests to the run's usage file, adding to any earlier figures."""
    usage = load_usage(date)
    entry = usage.setdefault(phase, {})
    for key, value in (("minutes", minutes), ("tokens", tokens), ("requests", requests)):
        if value is not None:
            entry[key] = round(entry.get(key, 0) + value, 1)
    path = usage_path(date)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(usage, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def field_values(fact_sheet: str, name: str) -> list[str]:
    return [value.strip().lower() for value in re.findall(rf"^- {name}: (.*)$", fact_sheet, re.MULTILINE)]


def first_match(value: str, options: Sequence[str]) -> str:
    return next((option for option in options if value.startswith(option)), "other")


def dimension_of(tag: str) -> str:
    return next((name for name in DIMENSION_TAGS if tag.lower().startswith(name.lower())), tag)


def metrics(date: str) -> dict[str, Any]:
    run = runs_folder() / date
    fact_sheet = (run / "fact_sheet.md").read_text(encoding="utf-8") if (run / "fact_sheet.md").is_file() else ""
    verification = (run / "verification.md").read_text(encoding="utf-8") if (run / "verification.md").is_file() \
        else ""
    edition = MARKDOWN_FOLDER / f"{date}-ai-outlook-briefing.md"
    tags = [match["tag"] or "untagged" for match in FACT.finditer(fact_sheet)]
    reads = field_values(fact_sheet, "Read")
    return {
        "facts": len(tags),
        "dimensions": Counter(dimension_of(tag) for tag in tags),
        "verdicts": Counter(match["verdict"] for match in VERDICT.finditer(verification)),
        "change_types": Counter(first_match(value, CHANGE_TYPES) for value in field_values(fact_sheet, "Change type")),
        "source_types": Counter(first_match(value, SOURCE_TYPES) for value in field_values(fact_sheet, "Source type")),
        "full_reads": sum(1 for value in reads if value.startswith("full")),
        "spoken_words": spoken_words(edition.read_text(encoding="utf-8")) if edition.is_file() else None,
        "usage": load_usage(date),
    }


def counts(counter: Counter[str], order: Sequence[str]) -> str:
    keys = [key for key in order if key in counter] + sorted(key for key in counter if key not in order)
    return ", ".join(f"{key} {counter[key]}" for key in keys) or "none"


def format_metrics(date: str, m: dict[str, Any]) -> str:
    lines = [
        "# Run metrics",
        "",
        f"Edition: {date}.",
        "",
        f"- Facts: {m['facts']}, of which {m['full_reads']} read in full.",
        f"- By dimension: {counts(m['dimensions'], DIMENSION_TAGS)}.",
        f"- Verdicts: {counts(m['verdicts'], VERDICTS)}.",
        f"- Change types: {counts(m['change_types'], CHANGE_TYPES)}.",
        f"- Source types: {counts(m['source_types'], SOURCE_TYPES)}.",
        f"- Spoken words in the edition: {m['spoken_words']:,}." if m["spoken_words"] is not None
        else "- Spoken words in the edition: not written yet.",
    ]
    if m["usage"]:
        lines += ["", "| Phase | Minutes | Tokens | Requests |", "|---|---|---|---|"]
        for phase, entry in sorted(m["usage"].items()):
            cells = [f"{entry[key]:,.0f}" if key in entry else "" for key in ("minutes", "tokens", "requests")]
            lines.append(f"| {phase} | {' | '.join(cells)} |")
    return "\n".join(lines) + "\n"


def write_metrics(date: str) -> Path:
    path = runs_folder() / date / "metrics.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(format_metrics(date, metrics(date)), encoding="utf-8")
    return path


def history() -> str:
    """One line per run with a fact sheet, oldest first."""
    rows = ["| Edition | Facts | Confirmed | Corrected | Unconfirmed | Dropped | Words | Minutes |",
            "|---|---|---|---|---|---|---|---|"]
    for run in sorted(path for path in runs_folder().iterdir() if (path / "fact_sheet.md").is_file()):
        m = metrics(run.name)
        minutes = sum(entry.get("minutes", 0) for entry in m["usage"].values())
        words = f"{m['spoken_words']:,}" if m["spoken_words"] is not None else ""
        verdicts = " | ".join(str(m["verdicts"][verdict]) for verdict in VERDICTS)
        rows.append(f"| {run.name} | {m['facts']} | {verdicts} | {words} | {minutes:,.0f} |")
    return "\n".join(rows) + "\n"


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Write or show briefing run metrics.")
    parser.add_argument("date", nargs="?", help="edition date, YYYY-MM-DD")
    parser.add_argument("--phase", choices=list("ABCD"), help="record usage for this phase instead")
    parser.add_argument("--minutes", type=float)
    parser.add_argument("--tokens", type=int)
    parser.add_argument("--history", action="store_true", help="print one line per run")
    args = parser.parse_args(argv)
    if args.history:
        print(history(), end="")
        return
    if args.date is None:
        parser.error("give an edition date, or --history")
    if args.phase:
        record_usage(args.date, args.phase, args.minutes, args.tokens)
    print(f"wrote {write_metrics(args.date)}")


if __name__ == "__main__":
    main()
