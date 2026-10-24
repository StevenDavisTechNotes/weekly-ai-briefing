from weekly_ai_briefing.convert_for_blogger import markdown_to_html


def test_footnote_references_link_to_their_definitions():
    rendered = markdown_to_html("Claim[^1][^2].\n\n[^1]: [One](https://a.example)\n[^2]: Two\n")
    assert '<sup><a href="#fn-1">[1]</a></sup><sup><a href="#fn-2">[2]</a></sup>' in rendered
    assert '<li id="fn-1">[1] <a href="https://a.example">One</a></li>' in rendered
    assert '<li id="fn-2">[2] Two</li>' in rendered


def test_footnote_definitions_end_the_preceding_paragraph():
    rendered = markdown_to_html("Text\n[^1]: Note\n")
    assert "<p>Text</p>" in rendered
    assert 'id="fn-1"' in rendered
