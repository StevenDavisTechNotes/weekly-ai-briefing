from weekly_ai_briefing.email_briefing.speech import markdown_to_speech_text, split_chunks


def test_headings_become_sentences():
    assert markdown_to_speech_text("## Quantum Computing:\n\nBody.") == "Quantum Computing.\nBody."


def test_footnote_references_are_removed():
    assert markdown_to_speech_text("Faster caches[^1]. More[^lab] here.") == "Faster caches. More here."


def test_links_keep_label_and_bare_urls_go():
    text = "See [the docs](https://example.com/x) or https://example.com/y now."
    assert markdown_to_speech_text(text) == "See the docs or now."


def test_footnote_definition_url_is_dropped():
    assert "example.com" not in markdown_to_speech_text("[^1]: [Title](https://example.com/a)")


def test_emphasis_bullets_quotes_and_rules_are_stripped():
    text = "- **Bold** and *italic*\n\n---\n\n> quoted\n\n1. numbered"
    assert markdown_to_speech_text(text) == "Bold and italic\nquoted\nnumbered"


def test_tables_and_code_blocks_are_skipped():
    text = "Before.\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n```\ncode\n```\n\nAfter."
    assert markdown_to_speech_text(text) == "Before.\n\nAfter."


def test_images_are_removed():
    assert markdown_to_speech_text("Hi ![alt](pic.png) there") == "Hi there"


def test_split_chunks_keeps_short_text_whole():
    assert split_chunks("One.\n\nTwo.", 100) == ["One.\n\nTwo."]


def test_split_chunks_splits_long_paragraph_on_sentences():
    assert split_chunks("Aaaa. Bbbb. Cccc.", 10) == ["Aaaa.", "Bbbb.", "Cccc."]


def test_split_chunks_respects_limit_without_punctuation():
    assert split_chunks("x" * 25, 10) == ["x" * 10, "x" * 10, "x" * 5]


def test_split_chunks_merges_small_paragraphs_up_to_limit():
    # cSpell: disable
    assert split_chunks("aaaa\n\nbbbb\n\ncccc", 10) == ["aaaa\n\nbbbb", "cccc"]
    # cSpell: enable


def test_split_chunks_empty_text():
    assert split_chunks("  \n\n ", 10) == []
