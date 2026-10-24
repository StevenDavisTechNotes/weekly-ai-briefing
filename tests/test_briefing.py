import pytest

from weekly_ai_briefing.email_briefing.briefing import Section, find_latest_briefing, list_briefings, split_sections


def test_find_latest_briefing_picks_newest_matching_file(tmp_path):
    for name in (
        "2026-10-10-ai-outlook-briefing.md",
        "2026-10-17-ai-outlook-briefing.md",
        "notes.md",
        "2026-10-18-other.md",
    ):
        (tmp_path / name).write_text("x")
    path, date = find_latest_briefing(tmp_path)
    assert (path.name, date) == ("2026-10-17-ai-outlook-briefing.md", "2026-10-17")


def test_find_latest_briefing_without_candidates_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        find_latest_briefing(tmp_path)


def test_list_briefings_is_newest_first_and_skips_other_files(tmp_path):
    for name in ("2026-10-03-ai-outlook-briefing.md", "2026-10-17-ai-outlook-briefing.md", "notes.md"):
        (tmp_path / name).write_text("x")
    assert [date for date, _ in list_briefings(tmp_path)] == ["2026-10-17", "2026-10-03"]


def test_split_sections_titles_and_bodies():
    sections = split_sections("## One\n\nA\n\n## Two\n\nB\n")
    assert sections == [Section("One", "## One\n\nA\n\n"), Section("Two", "## Two\n\nB\n")]


def test_split_sections_joins_preamble_to_first_section():
    sections = split_sections("# Title\n\n## One\n\nA\n\n## Two\n\nB")
    assert sections[0].markdown.startswith("# Title")
    assert sections[0].title == "One"
    assert not sections[1].markdown.startswith("# Title")


def test_split_sections_ignores_deeper_headings():
    sections = split_sections("## One\n\n### Sub\n\nA")
    assert [s.title for s in sections] == ["One"]


def test_split_sections_without_headings_raises():
    with pytest.raises(ValueError):
        split_sections("no headings here")
