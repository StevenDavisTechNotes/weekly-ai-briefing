from pathlib import Path

import pytest

from weekly_ai_briefing import generate_briefing_text as g

DATE = "2026-11-21"
BOTTOM_MATTER = (
    "---\n"
    'title: "T"\n'
    f"publication_date: {DATE}\n"
    "survey_begin_date: 2026-11-14\n"
    "survey_last_date: 2026-11-20\n"
    'summary: "S"\n'
    "---\n"
)


def test_parse_output_files_extracts_each_block():
    reply = (
        "=== BEGIN state/a.md ===\n# A\n\ntext\n=== END state/a.md ===\n\n"
        "=== BEGIN state/b.md ===\n# B\n=== END state/b.md ===\n"
    )
    assert g.parse_output_files(reply, ["state/a.md", "state/b.md"]) == {
        "state/a.md": "# A\n\ntext\n",
        "state/b.md": "# B\n",
    }


def test_parse_output_files_rejects_missing_and_unexpected_paths():
    reply = "=== BEGIN state/other.md ===\nx\n=== END state/other.md ===\n"
    with pytest.raises(ValueError, match="missing state/a.md; unexpected state/other.md"):
        g.parse_output_files(reply, ["state/a.md"])


def test_parse_args_defaults_to_all_phases_in_order():
    args = g.parse_args([])
    assert args.phases == ["A", "B", "C", "D"]


def test_parse_args_sorts_phases_and_checks_the_date():
    assert g.parse_args(["D", "B", "--date", DATE]).phases == ["B", "D"]
    with pytest.raises(SystemExit):
        g.parse_args(["--date", "21 November"])


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """A minimal repository layout in tmp_path, used as the working directory."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(g, "REPO_ROOT", tmp_path)
    shared = tmp_path / "prompts" / "shared.md"
    shared.parent.mkdir(parents=True)
    shared.write_text("# Shared\n", encoding="utf-8")
    monkeypatch.setattr(g, "SHARED_PROMPT", shared)
    run = tmp_path / "state" / "runs" / DATE
    run.mkdir(parents=True)
    for path in ("state/current_model.md", "state/state_table.md"):
        (tmp_path / path).write_text(f"# {path}\n", encoding="utf-8")
    for name in ("change_log.md", "fact_sheet.md", "verification.md"):
        (run / name).write_text(f"# {name}\n", encoding="utf-8")
    return tmp_path


def test_build_request_inlines_inputs_and_names_outputs(repo: Path):
    request = g.build_request(g.PHASES["D"], DATE)
    assert f"- editions/markdown_format/{DATE}-ai-outlook-briefing.md" in request
    assert "=== BEGIN prompts/shared.md ===\n# Shared\n=== END prompts/shared.md ===" in request
    assert f"=== BEGIN state/runs/{DATE}/verification.md ===" in request


def test_build_request_stops_when_an_input_is_missing(repo: Path):
    (repo / "state" / "runs" / DATE / "verification.md").unlink()
    with pytest.raises(SystemExit, match=f"missing input files: state/runs/{DATE}/verification.md"):
        g.build_request(g.PHASES["D"], DATE)


def test_run_phase_writes_the_edition(repo: Path, monkeypatch: pytest.MonkeyPatch):
    name = f"editions/markdown_format/{DATE}-ai-outlook-briefing.md"
    reply = f"=== BEGIN {name} ===\n## Orientation\n\nIntro.\n\n{BOTTOM_MATTER}=== END {name} ===\n"
    monkeypatch.setattr(g, "send", lambda client, system, messages, tools: reply)
    g.run_phase(None, "D", DATE)  # ty: ignore[invalid-argument-type]
    written = (repo / name).read_text(encoding="utf-8")
    assert written.startswith("## Orientation\n\nIntro.\n")
    assert f"publication_date: {DATE}" in written


def test_run_phase_saves_the_reply_when_files_are_missing(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(g, "send", lambda client, system, messages, tools: "no files here")
    with pytest.raises(SystemExit, match="phase_D_reply.md"):
        g.run_phase(None, "D", DATE)  # ty: ignore[invalid-argument-type]
    assert (repo / "state" / "runs" / DATE / "phase_D_reply.md").read_text(encoding="utf-8") == "no files here"


def test_build_request_adds_other_model_briefings_only_when_present(repo: Path):
    (repo / "state" / "README.md").write_text("# readme\n", encoding="utf-8")
    names = [f"editions/gemini_version/{DATE}-gemini.md", f"editions/muse_version/{DATE}-muse.md"]
    assert "_version/" not in g.build_request(g.PHASES["A"], DATE)
    for name in [*names, "editions/muse_version/2026-11-14-muse.md"]:
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text("# Other\n", encoding="utf-8")
    request = g.build_request(g.PHASES["A"], DATE)
    for name in names:
        assert f"=== BEGIN {name} ===\n# Other\n=== END {name} ===" in request
    assert "2026-11-14-muse.md" not in request
