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
    monkeypatch.setattr(g, "send", lambda client, system, messages, tools, **_: reply)
    g.run_phase(client=None, letter="D", date=DATE)  # ty: ignore[invalid-argument-type]
    written = (repo / name).read_text(encoding="utf-8")
    assert written.startswith("## Orientation\n\nIntro.\n")
    assert f"publication_date: {DATE}" in written


def test_run_phase_saves_the_reply_when_files_are_missing(repo: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(g, "send", lambda client, system, messages, tools, **_: "no files here")
    with pytest.raises(SystemExit, match="phase_D_reply.md"):
        g.run_phase(client=None, letter="D", date=DATE)  # ty: ignore[invalid-argument-type]
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


def test_phase_d_gets_only_the_orientation_and_metadata_of_the_previous_edition(repo: Path):
    folder = repo / "editions" / "markdown_format"
    folder.mkdir(parents=True)
    previous = f"## Orientation: Signals\n\nLast week's signals.\n\n## AI Technology\n\nBody text.\n\n{BOTTOM_MATTER}"
    (folder / "2026-11-14-ai-outlook-briefing.md").write_text("## Orientation: Old\n\nOlder.\n", encoding="utf-8")
    (folder / "2026-11-20-ai-outlook-briefing.md").write_text(previous, encoding="utf-8")
    (folder / f"{DATE}-ai-outlook-briefing.md").write_text("## Orientation: This week\n", encoding="utf-8")
    request = g.build_request(g.PHASES["D"], DATE)
    label = (
        "editions/markdown_format/2026-11-20-ai-outlook-briefing.md"
        " (excerpt: the Orientation part and the metadata block only)"
    )
    assert f"=== BEGIN {label} ===\n## Orientation: Signals\nLast week's signals.\n\n---\ntitle:" in request
    assert "Body text." not in request
    assert "Older." not in request
    assert "This week" not in request


def test_phase_d_runs_without_a_previous_edition(repo: Path):
    assert "excerpt:" not in g.build_request(g.PHASES["D"], DATE)


def test_phase_a_runs_seven_dimension_workers_then_a_merging_lead(repo: Path, monkeypatch: pytest.MonkeyPatch):
    (repo / "state" / "README.md").write_text("# readme\n", encoding="utf-8")
    name = f"state/runs/{DATE}/fact_sheet.md"
    requests: list[str] = []

    def fake_send(client, system, messages, tools, **_):
        content = messages[0]["content"]
        requests.append(content)
        if "You are the lead" in content:
            return f"=== BEGIN {name} ===\n# Fact sheet\n=== END {name} ===\n"
        return "draft for " + content.split("research worker for dimension ")[1].split(",")[0]

    monkeypatch.setattr(g, "send", fake_send)
    g.run_phase(client=None, letter="A", date=DATE)  # ty: ignore[invalid-argument-type]
    workers, lead = requests[:-1], requests[-1]
    assert len(workers) == 7 and all("Write no BEGIN or END lines" in request for request in workers)
    assert "draft for 3" in lead and "draft for 7" in lead
    assert (repo / name).read_text(encoding="utf-8") == "# Fact sheet\n"
    assert (repo / "state" / "runs" / DATE / "research_drafts" / "D3.md").read_text(encoding="utf-8") == "draft for 3\n"

    requests.clear()
    g.run_phase(client=None, letter="A", date=DATE)  # ty: ignore[invalid-argument-type]
    assert len(requests) == 1  # the saved drafts are reused; only the lead runs again


def test_single_research_sends_one_request(repo: Path, monkeypatch: pytest.MonkeyPatch):
    (repo / "state" / "README.md").write_text("# readme\n", encoding="utf-8")
    name = f"state/runs/{DATE}/fact_sheet.md"
    requests: list[str] = []
    monkeypatch.setattr(g, "send", lambda client, system, messages, tools, **_: requests.append(messages[0]["content"])
                        or f"=== BEGIN {name} ===\n# Fact sheet\n=== END {name} ===\n")
    g.run_phase(client=None, letter="A", date=DATE, parallel_research=False)  # ty: ignore[invalid-argument-type]
    assert len(requests) == 1 and "You are the lead" not in requests[0]
    assert g.parse_args(["A", "--single-research"]).single_research


def test_phase_c_saves_its_starting_point_and_reruns_from_it(repo: Path, monkeypatch: pytest.MonkeyPatch):
    (repo / "state" / "README.md").write_text("# readme\n", encoding="utf-8")
    model, table = repo / "state" / "current_model.md", repo / "state" / "state_table.md"
    model.write_text("# Model before\n", encoding="utf-8")
    outputs = [f"state/runs/{DATE}/change_log.md", "state/current_model.md", "state/state_table.md",
               "state/background.md"]
    reply = "".join(f"=== BEGIN {name} ===\n# Revised {name}\n=== END {name} ===\n" for name in outputs)
    requests: list[str] = []
    monkeypatch.setattr(g, "send", lambda client, system, messages, tools, **_: requests.append(
        messages[0]["content"]) or reply)

    g.run_phase(client=None, letter="C", date=DATE)  # ty: ignore[invalid-argument-type]
    assert model.read_text(encoding="utf-8") == "# Revised state/current_model.md\n"
    run = repo / "state" / "runs" / DATE
    assert (run / "current_model_before.md").read_text(encoding="utf-8") == "# Model before\n"
    assert (run / "state_table_before.md").is_file()

    g.run_phase(client=None, letter="C", date=DATE)  # ty: ignore[invalid-argument-type]
    assert "=== BEGIN state/current_model.md ===\n# Model before\n" in requests[1]
    assert (run / "current_model_before.md").read_text(encoding="utf-8") == "# Model before\n"
    assert table.read_text(encoding="utf-8") == "# Revised state/state_table.md\n"
