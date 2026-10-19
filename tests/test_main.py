import pytest

from weekly_ai_briefing.email_briefing import __main__ as cli
from weekly_ai_briefing.email_briefing.briefing import Section

BRIEFING = "## Orientation\n\nIntro.\n\n## Source Notes and Attribution\n\nSources.\n"


def test_parse_args_defaults():
    args = cli.parse_args([])
    assert args.section is None
    assert args.send_email is True


def test_parse_args_options():
    args = cli.parse_args(["--section", "1", "3", "--no-send-email"])
    assert args.section == [1, 3]
    assert args.send_email is False


def test_select_sections_defaults_to_all():
    assert cli.select_sections(None, 3) == {1, 2, 3}


def test_select_sections_rejects_out_of_range():
    with pytest.raises(SystemExit, match="out of range"):
        cli.select_sections([1, 4], 3)


def test_email_subject_and_bodies():
    section = Section("Quantum Computing", "## Quantum Computing\n\nText")
    assert cli.email_subject("2026-10-17", section) == "Weekly AI Briefing - 2026-10-17 - Quantum Computing"
    audio = cli.email_body("2026-10-17", 2, 7, section, has_audio=True)
    assert "section 2 of 7" in audio and "attached as an MP3" in audio
    text = cli.email_body("2026-10-17", 7, 7, section, has_audio=False)
    assert "no audio version" in text and text.endswith("Text")


@pytest.fixture
def run_env(tmp_path, monkeypatch):
    history = tmp_path / "history"
    history.mkdir()
    (history / "2026-10-17-ai-outlook-briefing.md").write_text(BRIEFING, encoding="utf-8")
    monkeypatch.setattr(cli, "HISTORY_FOLDER", history)
    monkeypatch.setattr(cli, "STAGED_AUDIO_FOLDER", tmp_path / "staged")
    generated, emails = [], []
    monkeypatch.setattr(cli, "generate_mp3", lambda md, path: generated.append(path.name))
    monkeypatch.setattr(cli, "send_email", lambda **kw: emails.append(kw))
    return generated, emails


def test_main_voices_and_emails_each_section(run_env):
    generated, emails = run_env
    cli.main([])
    assert generated == ["2026-10-17-ai-outlook-briefing-01.mp3"]
    assert [e["mp3_path"] is not None for e in emails] == [True, False]
    assert "Sources." in emails[1]["body"]


def test_main_without_email_only_generates_audio(run_env):
    generated, emails = run_env
    cli.main(["--no-send-email"])
    assert generated == ["2026-10-17-ai-outlook-briefing-01.mp3"]
    assert emails == []


def test_main_section_filter(run_env):
    generated, emails = run_env
    cli.main(["--section", "2"])
    assert generated == []
    assert len(emails) == 1 and emails[0]["mp3_path"] is None
