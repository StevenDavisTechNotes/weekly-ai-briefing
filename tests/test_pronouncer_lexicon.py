from pathlib import Path

from weekly_ai_briefing.pronouncer_lexicon import Entry, mismatches, read_lexicon, update_lexicon, write_lexicon


def test_update_adds_new_names_and_never_changes_existing_ones(tmp_path: Path):
    lexicon = tmp_path / "pronouncers.md"
    write_lexicon({"Rigetti": Entry("ɹɪdʒˈɛti", "2026-10-24")}, lexicon)
    edition = tmp_path / "2026-11-28-ai-outlook-briefing.md"
    edition.write_text("{Rigetti|ɹɪɡˈɛti} met {Pachocki|pəhˈɑːtski} and {Pachocki|other}.\n", encoding="utf-8")
    assert update_lexicon(edition, lexicon) == ["Pachocki"]
    assert read_lexicon(lexicon) == {
        "Pachocki": Entry("pəhˈɑːtski", "2026-11-28"),
        "Rigetti": Entry("ɹɪdʒˈɛti", "2026-10-24"),
    }
    assert update_lexicon(edition, lexicon) == []


def test_mismatches_name_where_an_edition_departs_from_the_lexicon():
    lexicon = {"Rigetti": Entry("ɹɪdʒˈɛti", "2026-10-24")}
    assert mismatches("{Rigetti|ɹɪɡˈɛti} and {Qwen|tʃwˈɛn}", lexicon) == [("Rigetti", "ɹɪɡˈɛti", "ɹɪdʒˈɛti")]


def test_a_missing_lexicon_reads_as_empty(tmp_path: Path):
    assert read_lexicon(tmp_path / "none.md") == {}
