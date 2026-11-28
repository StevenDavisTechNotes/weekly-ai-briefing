from weekly_ai_briefing.edition_checks import REQUIRED_PARTS, check_edition, figures

METADATA = (
    "---\n"
    'title: "T"\n'
    "publication_date: 2026-11-28\n"
    "survey_begin_date: 2026-11-21\n"
    "survey_last_date: 2026-11-27\n"
    'summary: "S"\n'
    "---\n"
)
SIGNALS = "One sentence.\n\n" + "\n".join(
    f"- {cue} a signal[^1]." for cue in ("First,", "Second,", "Third,", "Fourth,", "Fifth,")
)


def edition(orientation: str = SIGNALS, notes: str = "[^1]: [Source](https://example.com)",
            metadata: str = METADATA, extra: str = "") -> str:
    sections = [f"## {REQUIRED_PARTS[0]}\n\n{orientation}\n"]
    sections += [f"## {title}\n\nNothing moved.{extra if title == 'AI Technology' else ''}\n"
                 for title in REQUIRED_PARTS[1:-1]]
    sections.append(f"## {REQUIRED_PARTS[-1]}\n\n{notes}\n")
    return "\n".join(sections) + "\n" + metadata


def test_a_well_formed_edition_passes():
    assert check_edition(edition()) == []


def test_missing_and_renamed_parts_are_reported():
    text = edition().replace("## Quantum Computing", "## Quantum")
    assert check_edition(text) == ["missing ## part: Quantum Computing", "unexpected ## part: Quantum"]


def test_the_orientation_needs_five_cued_bullets():
    problems = check_edition(edition(orientation=SIGNALS.replace("- Fifth, a signal[^1].", "")))
    assert problems == ["Orientation has 4 bullets, not five"]
    problems = check_edition(edition(orientation=SIGNALS.replace("Third,", "Next,")))
    assert problems == ["Orientation bullet 3 does not open with 'Third,'"]


def test_footnotes_must_be_defined_used_and_in_order():
    problems = check_edition(edition(extra=" See this[^3].", notes="[^1]: a\n[^2]: b"))
    assert "footnote [^3] is used but not defined" in problems
    assert "footnote [^2] is defined but not used" in problems
    assert "footnotes are not numbered 1, 2, 3... in order of first appearance" in problems


def test_urls_belong_only_in_footnote_definitions():
    problems = check_edition(edition(extra=" Read https://example.com/x."))
    assert problems == ["URL outside a footnote definition: Nothing moved. Read https://example.com/x."]


def test_the_metadata_block_has_exactly_five_keys():
    assert check_edition(edition(metadata="")) == ["the edition does not end with a --- delimited metadata block"]
    extra_key = METADATA.replace("---\n", "---\nindicators: []\n", 1)
    assert check_edition(edition(metadata=extra_key))[0].startswith("metadata keys are")


def test_the_body_may_not_run_over_budget():
    problems = check_edition(edition(extra=" word" * 10_001))
    assert len(problems) == 1
    assert problems[0].startswith("body is about 10,0") and problems[0].endswith("over the 10,000-word budget")


def test_figures_leave_out_dates_tenors_names_and_footnotes():
    assert figures("On November 25, 2026, Claude Sonnet 4.5 and GPT-6 saw the 10-year at 4.85 percent[^12].") == 1
    assert figures("Revenue rose 14% while units fell 29% and prices rose 3.8%.") == 3


def test_too_many_figures_in_a_sentence_or_paragraph_are_reported():
    problems = check_edition(edition(extra=" Units fell 29%, revenue rose 14% and margin 3.8%. Then 1, 2."))
    assert any(problem.startswith("more than 2 figures in sentence: Units fell") for problem in problems)
    assert any(problem.startswith("more than 4 figures in: Nothing moved.") for problem in problems)


def test_the_command_line_reports_and_sets_the_exit_code(tmp_path, capsys):
    from weekly_ai_briefing.edition_checks import main

    good, bad = tmp_path / "good.md", tmp_path / "bad.md"
    good.write_text(edition(), encoding="utf-8")
    bad.write_text(edition(metadata=""), encoding="utf-8")
    assert main([str(good)]) == 0
    assert "passed" in capsys.readouterr().out
    assert main([str(good), str(bad)]) == 1
    assert "the edition does not end with a --- delimited metadata block" in capsys.readouterr().out


def test_latest_checks_the_newest_edition(tmp_path, monkeypatch, capsys):
    from weekly_ai_briefing import edition_checks

    monkeypatch.setattr(edition_checks, "MARKDOWN_FOLDER", tmp_path)
    (tmp_path / "2026-11-21-ai-outlook-briefing.md").write_text(edition(metadata=""), encoding="utf-8")
    (tmp_path / "2026-11-28-ai-outlook-briefing.md").write_text(edition(), encoding="utf-8")
    (tmp_path / "statement_of_intent.md").write_text("# Intent\n", encoding="utf-8")
    assert edition_checks.main(["--latest"]) == 0
    assert "2026-11-28-ai-outlook-briefing.md: passed" in capsys.readouterr().out
