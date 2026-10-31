import pytest

from weekly_ai_briefing import publish
from weekly_ai_briefing.email_briefing.briefing import Section

STEM = "2026-10-17-ai-outlook-briefing"
SECTIONS = [
    Section("Orientation", "# Title\n\nPreamble.\n\n## Orientation\n\nIntro."),
    Section("Source Notes and Attribution", "## Source Notes and Attribution\n\nSources."),
    Section("Outlook", "## Outlook\n\nLooking ahead."),
]


def asset_url(number: int) -> str:
    return publish.release_asset_url("ai-outlook-briefing-2026-10-17", f"{STEM}-{number:02d}.mp3")


def test_players_follow_section_numbers_and_skip_text_only_sections():
    page = publish.render_edition_page("2026-10-17", STEM, SECTIONS, has_audio=True)
    assert asset_url(1) in page
    assert asset_url(2) not in page  # text-only, but its number is still taken
    assert asset_url(3) in page


def test_player_sits_under_its_section_heading():
    page = publish.render_edition_page("2026-10-17", STEM, SECTIONS, has_audio=True)
    assert page.index("<h2>Orientation</h2>") < page.index(asset_url(1)) < page.index("Intro.")


def test_page_without_release_has_no_players():
    page = publish.render_edition_page("2026-10-17", STEM, SECTIONS, has_audio=False)
    assert "<audio" not in page
    assert "Looking ahead." in page


def test_leading_h1_is_replaced_by_the_page_title():
    page = publish.render_edition_page("2026-10-17", STEM, SECTIONS, has_audio=False)
    assert page.count("<h1>") == 1
    assert "Title" not in page.split("<h1>", 1)[1].split("</h1>", 1)[0]


def test_index_keeps_given_order_and_marks_audio_with_an_icon():
    editions = [
        publish.Edition("2026-10-17", STEM, True, "Week <A>", "First."),
        publish.Edition("2026-10-10", "2026-10-10-ai-outlook-briefing", False, "Week B", "Second."),
    ]
    index = publish.render_index(editions)
    assert index.index("2026-10-17") < index.index("2026-10-10")
    assert index.count('aria-label="Includes embedded audio"') == 1
    assert "(with embedded audio)" not in index
    assert "<th" not in index  # no column headings
    assert "Week &lt;A&gt;" in index


BOTTOM_MATTER = (
    "---\n"
    'title: "Costs: the real story"\n'
    "publication_date: 2026-10-17\n"
    "survey_begin_date: 2026-10-11\n"
    "survey_last_date: 2026-10-17\n"
    'summary: "Short summary."\n'
    "---\n"
)


@pytest.fixture
def site(tmp_path, monkeypatch):
    markdown = tmp_path / "markdown"
    markdown.mkdir()
    monkeypatch.setattr(publish, "MARKDOWN_FOLDER", markdown)
    monkeypatch.setattr(publish, "HTML_FOLDER", tmp_path / "html")
    monkeypatch.setattr(publish, "SITE_INDEX", tmp_path / "index.html")
    return tmp_path


def test_site_index_uses_bottom_matter_and_pages_omit_it(site):
    (site / "markdown" / f"{STEM}.md").write_text("## Orientation\n\nIntro.\n\n" + BOTTOM_MATTER, encoding="utf-8")
    publish.write_site(set())
    index = (site / "index.html").read_text(encoding="utf-8")
    assert "Costs: the real story" in index
    assert "Short summary." in index
    assert "survey_begin_date" not in (site / "html" / f"{STEM}.html").read_text(encoding="utf-8")


def test_site_refuses_a_briefing_without_bottom_matter(site):
    (site / "markdown" / f"{STEM}.md").write_text("## Orientation\n\nIntro.\n", encoding="utf-8")
    with pytest.raises(ValueError, match="no YAML bottom matter"):
        publish.write_site(set())


def test_site_refuses_a_publication_date_that_differs_from_the_file_name(site):
    text = BOTTOM_MATTER.replace("publication_date: 2026-10-17", "publication_date: 2026-10-18")
    (site / "markdown" / f"{STEM}.md").write_text("## Orientation\n\nIntro.\n\n" + text, encoding="utf-8")
    with pytest.raises(ValueError, match="does not match the file name date"):
        publish.write_site(set())
