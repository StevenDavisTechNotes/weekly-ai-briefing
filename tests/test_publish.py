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


def test_index_keeps_given_order_and_marks_audio():
    editions = [
        publish.Edition("2026-10-17", STEM, has_audio=True),
        publish.Edition("2026-10-10", "2026-10-10-ai-outlook-briefing", has_audio=False),
    ]
    index = publish.render_index(editions)
    assert index.index("2026-10-17") < index.index("2026-10-10")
    assert index.count("(with embedded audio)") == 1
