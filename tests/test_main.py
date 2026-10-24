import pytest

from weekly_ai_briefing.email_briefing import __main__ as cli
from weekly_ai_briefing.email_briefing.briefing import Section

BRIEFING = "## Orientation\n\nIntro.\n\n## Source Notes and Attribution\n\nSources.\n"
PAGE_URL = cli.edition_page_url("2026-10-17-ai-outlook-briefing")


def test_parse_args_requires_an_action(capsys):
    with pytest.raises(SystemExit):
        cli.parse_args([])
    assert "nothing to do" in capsys.readouterr().err


def test_parse_args_section_needs_voice(capsys):
    with pytest.raises(SystemExit):
        cli.parse_args(["--email", "--section", "1"])
    assert "--section only applies with --voice" in capsys.readouterr().err


def test_parse_args_options():
    args = cli.parse_args(["--voice", "--section", "1", "3"])
    assert (args.voice, args.email, args.section) == (True, False, [1, 3])


def test_select_sections_defaults_to_all():
    assert cli.select_sections(None, 3) == {1, 2, 3}


def test_select_sections_rejects_out_of_range():
    with pytest.raises(SystemExit, match="out of range"):
        cli.select_sections([1, 4], 3)


def test_email_body_links_the_page_and_each_section():
    sections = [Section("Quantum Computing", "## Quantum Computing\n"), Section("Outlook", "## Outlook\n")]
    body = cli.email_body("2026-10-17", "https://example.org/p.html", sections)
    assert "dated 2026-10-17" in body
    assert "1. Quantum Computing: https://example.org/p.html#section-1" in body
    assert "2. Outlook: https://example.org/p.html#section-2" in body


@pytest.fixture
def run_env(tmp_path, monkeypatch):
    history = tmp_path / "history"
    history.mkdir()
    (history / "2026-10-17-ai-outlook-briefing.md").write_text(BRIEFING, encoding="utf-8")
    monkeypatch.setattr(cli, "MARKDOWN_FOLDER", history)
    monkeypatch.setattr(cli, "MP3_FOLDER", tmp_path / "staged")
    generated, emails = [], []
    monkeypatch.setattr(cli, "generate_mp3", lambda md, path: generated.append(f"{path.parent.name}/{path.name}"))
    monkeypatch.setattr(cli, "send_email", lambda **kw: emails.append(kw))
    monkeypatch.setattr(cli, "page_is_live", lambda url: True)
    return generated, emails


def test_voice_writes_mp3s_for_voiced_sections_only(run_env):
    generated, emails = run_env
    cli.main(["--voice"])
    assert generated == ["ai-outlook-briefing-2026-10-17/2026-10-17-ai-outlook-briefing-01.mp3"]
    assert emails == []


def test_voice_section_filter(run_env):
    generated, _ = run_env
    cli.main(["--voice", "--section", "2"])
    assert generated == []


def test_email_sends_one_link_message_when_page_is_live(run_env):
    generated, emails = run_env
    cli.main(["--email"])
    assert generated == []
    (email,) = emails
    assert email["subject"] == "Weekly AI Briefing - 2026-10-17"
    assert PAGE_URL in email["body"]
    assert set(email) == {"subject", "body"}


def test_email_refuses_until_page_is_live(run_env, monkeypatch):
    _, emails = run_env
    monkeypatch.setattr(cli, "page_is_live", lambda url: False)
    with pytest.raises(SystemExit, match="not live"):
        cli.main(["--email"])
    assert emails == []
