from weekly_ai_briefing.convert_for_blogger import inline_html, markdown_to_html
from weekly_ai_briefing.email_briefing.speech import markdown_to_speech_text
from weekly_ai_briefing.pronouncers import (
    possessive,
    pronunciations,
    to_phonemes,
    usable_pronunciations,
)

TEXT = "Shares of {Rigetti|ɹɪdʒˈɛti} rose, and {Ilya Sutskever|/ˈɪljə sʊtskˈɛvɚ/} spoke."


def fake_phonemize(text: str) -> str:
    """Upper-cases text, so tests can tell guessed words from given IPA."""
    return text.strip().upper()


def test_pronunciations_maps_names_to_ipa_without_slashes():
    assert pronunciations(TEXT) == {"Rigetti": "ɹɪdʒˈɛti", "Ilya Sutskever": "ˈɪljə sʊtskˈɛvɚ"}


def test_the_first_pronouncer_for_a_name_wins():
    assert pronunciations("{A|æ} then {A|eɪ}") == {"A": "æ"}


def test_readers_see_the_bare_name():
    assert inline_html("**{Rigetti|ɹɪdʒˈɛti}**") == "<strong>Rigetti</strong>"
    assert markdown_to_html(f"- {TEXT}\n\n{TEXT}") == (
        "<ul><li>Shares of Rigetti rose, and Ilya Sutskever spoke.</li></ul>\n"
        "<p>Shares of Rigetti rose, and Ilya Sutskever spoke.</p>"
    )


def test_speech_text_keeps_only_the_name():
    assert markdown_to_speech_text(TEXT) == "Shares of Rigetti rose, and Ilya Sutskever spoke."


def test_to_phonemes_says_every_mention_by_its_ipa():
    phonemes = to_phonemes("Rigetti rose; Rigetti, again. Rigettiville too.", {"Rigetti": "ɹɪdʒˈɛti"}, fake_phonemize)
    assert phonemes == "ɹɪdʒˈɛti ROSE; ɹɪdʒˈɛti, AGAIN. RIGETTIVILLE TOO."


def test_to_phonemes_prefers_the_longest_name_and_handles_possessives():
    pronounced = {"Ilya Sutskever": "ˈɪljə sʊtskˈɛvɚ", "Sutskever": "sʊtskˈɛvɚ"}
    assert to_phonemes("Ilya Sutskever's lab and Sutskever", pronounced, fake_phonemize) == (
        "ˈɪljə sʊtskˈɛvɚz LAB AND sʊtskˈɛvɚ"
    )


def test_to_phonemes_without_pronunciations_is_the_plain_guess():
    assert to_phonemes("Plain text.", {}, fake_phonemize) == "PLAIN TEXT."


def test_possessive_follows_the_final_sound():
    assert possessive("dʒˈɑːbz") == "dʒˈɑːbzɪz"
    assert possessive("hˈɑːk") == "hˈɑːks"
    assert possessive("hwˈɑːŋ") == "hwˈɑːŋz"


def test_usable_pronunciations_fixes_g_and_skips_unknown_symbols(capsys):
    vocabulary = set("ɡæʃ")
    assert usable_pronunciations({"Gash": "gæʃ", "Bad": "bæd"}, vocabulary) == {"Gash": "ɡæʃ"}
    assert "'Bad' has unknown symbols 'bd'" in capsys.readouterr().out
