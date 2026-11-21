"""Pronouncers: names the briefing writes as {Name|IPA}.

They exist only for the audio, which speaks the IPA in place of the speech engine's
guess at every mention of the name in the edition, not only the marked one. Every
other rendering shows the bare name.
"""

import re
from collections.abc import Callable, Container

PRONOUNCER = re.compile(r"\{([^{}|\n]+)\|([^{}|\n]+)\}")

# Possessive endings after a name: "Rigetti's".
POSSESSIVE = r"(?:['’]s\b)?"
VOICELESS_ENDINGS = tuple("ptkfθ")
SIBILANT_ENDINGS = ("s", "z", "ʃ", "ʒ", "tʃ", "dʒ", "ʧ", "ʤ")
PUNCTUATION = tuple(",.;:!?)…—")


def pronunciations(markdown: str) -> dict[str, str]:
    """Maps each name that has a pronouncer to its IPA; a name's first pronouncer wins."""
    found: dict[str, str] = {}
    for match in PRONOUNCER.finditer(markdown):
        found.setdefault(match.group(1).strip(), match.group(2).strip().strip("/[]").strip())
    return found


def drop_pronouncers(text: str) -> str:
    """Rewrites each pronouncer as the bare name."""
    return PRONOUNCER.sub(lambda m: m.group(1).strip(), text)


def usable_pronunciations(pronounced: dict[str, str], vocabulary: Container[str]) -> dict[str, str]:
    """The pronunciations the speech engine can say, warning about the rest.

    An ASCII g becomes the IPA ɡ, which is the symbol the engine knows.
    """
    usable: dict[str, str] = {}
    for name, ipa in pronounced.items():
        ipa = ipa.replace("g", "ɡ")
        unknown = sorted({symbol for symbol in ipa if symbol not in vocabulary})
        if unknown:
            print(f"  warning: pronouncer for {name!r} has unknown symbols {''.join(unknown)!r}; using the engine's guess")
        else:
            usable[name] = ipa
    return usable


def possessive(ipa: str) -> str:
    """The IPA of the name's possessive: "s" after a voiceless sound, "ɪz" after a sibilant, else "z"."""
    stripped = ipa.rstrip("ˈˌː ")
    if stripped.endswith(SIBILANT_ENDINGS):
        return ipa + "ɪz"
    return ipa + ("s" if stripped.endswith(VOICELESS_ENDINGS) else "z")


def to_phonemes(text: str, pronounced: dict[str, str], phonemize: Callable[[str], str]) -> str:
    """Phonemizes text, saying each name in pronounced by its IPA instead of phonemize's guess."""
    if not pronounced:
        return phonemize(text)
    names = "|".join(re.escape(name) for name in sorted(pronounced, key=len, reverse=True))
    mention = re.compile(rf"(?<!\w)({names})(?!\w)({POSSESSIVE})")
    def guess(segment: str) -> str:
        return phonemize(segment) if segment.strip() else ""

    pieces: list[str] = []
    start = 0
    for match in mention.finditer(text):
        pieces.append(guess(text[start : match.start()]))
        ipa = pronounced[match.group(1)]
        pieces.append(possessive(ipa) if match.group(2) else ipa)
        start = match.end()
    pieces.append(guess(text[start:]))
    phonemes = ""
    for piece in filter(None, (piece.strip() for piece in pieces)):
        separator = "" if not phonemes or piece.startswith(PUNCTUATION) else " "
        phonemes += separator + piece
    return phonemes
