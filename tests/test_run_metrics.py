from pathlib import Path

import pytest

from weekly_ai_briefing import run_metrics as r

DATE = "2026-11-28"
FACT_SHEET = """# Fact sheet

## Facts

### F-01 [Financial Services] One

- Source type: primary.
- Read: full document.
- Change type: reversal.

### F-02 [Quantum] Two

- Source type: secondhand (digest).
- Read: excerpt only; paywalled.
- Change type: level only.
"""
VERIFICATION = """# Verification

## Verdicts

- F-01: confirmed. Re-read.
- F-02: corrected. Date was wrong.

## Flags

- F-02: the label is wrong.
"""


@pytest.fixture
def run(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(r, "STATE_FOLDER", tmp_path / "state")
    monkeypatch.setattr(r, "MARKDOWN_FOLDER", tmp_path / "editions")
    folder = tmp_path / "state" / "runs" / DATE
    folder.mkdir(parents=True)
    (folder / "fact_sheet.md").write_text(FACT_SHEET, encoding="utf-8")
    (folder / "verification.md").write_text(VERIFICATION, encoding="utf-8")
    return folder


def test_metrics_count_the_run_files(run: Path):
    m = r.metrics(DATE)
    assert m["facts"] == 2 and m["full_reads"] == 1
    assert m["dimensions"] == {"Financial Services": 1, "Quantum": 1}
    assert m["verdicts"] == {"confirmed": 1, "corrected": 1}
    assert m["source_types"] == {"primary": 1, "secondhand": 1}
    assert m["change_types"] == {"reversal": 1, "level only": 1}
    assert m["spoken_words"] is None


def test_usage_adds_up_and_lands_in_the_metrics_file(run: Path):
    r.record_usage(DATE, "A", minutes=10, tokens=1000, requests=7)
    r.record_usage(DATE, "A", minutes=2.5, tokens=500, requests=1)
    assert r.load_usage(DATE) == {"A": {"minutes": 12.5, "tokens": 1500, "requests": 8}}
    text = r.write_metrics(DATE).read_text(encoding="utf-8")
    assert "- Verdicts: confirmed 1, corrected 1, " not in text
    assert "- Verdicts: confirmed 1, corrected 1." in text
    assert "| A | 12 | 1,500 | 8 |" in text


def test_history_has_a_line_per_run(run: Path):
    assert f"| {DATE} | 2 | 1 | 1 | 0 | 0 |  | 0 |" in r.history()
