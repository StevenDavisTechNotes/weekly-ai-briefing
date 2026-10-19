import re

# A pipe table: header row, delimiter row (|---|:--:|), then any rows with a pipe.
MARKDOWN_TABLE = re.compile(
    r"^.*\|.*\n"
    r"(?=[-:| \t]*\|)[-:| \t]*-[-:| \t]*(?:\n|$)"
    r"(?:.*\|.*(?:\n|$))*",
    re.MULTILINE,
)


def markdown_to_speech_text(markdown: str) -> str:
    """Strips markdown syntax so the TTS engine doesn't read it aloud."""
    text = re.sub(r"`{3}.*?`{3}", "", markdown, flags=re.DOTALL)
    text = MARKDOWN_TABLE.sub("", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)  # images
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links -> label
    text = re.sub(r"\[\^[^\]]+\]", "", text)  # footnote references like [^1]
    text = re.sub(r"https?://\S+", "", text)  # bare URLs
    text = re.sub(r"^\s*-{3,}\s*$", "", text, flags=re.MULTILINE)  # rules
    # Headings: drop the hashes, end with a period so the voice pauses.
    text = re.sub(
        r"^#{1,6}\s*(.+?)\s*#*\s*$",
        lambda m: m.group(1).rstrip(".:") + ".",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", text, flags=re.MULTILINE)  # bullets
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)  # quotes
    text = re.sub(r"(\*\*|__|\*|_|`)", "", text)  # emphasis / inline code
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def split_chunks(text: str, max_chars: int) -> list[str]:  # noqa: C901
    """Splits on paragraph (then sentence) boundaries into pieces <= max_chars."""
    pieces: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if len(paragraph) <= max_chars:
            pieces.append(paragraph)
            continue
        current = ""
        for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
            while len(sentence) > max_chars:  # pathological: no punctuation
                if current:
                    pieces.append(current)
                    current = ""
                pieces.append(sentence[:max_chars])
                sentence = sentence[max_chars:]
            if current and len(current) + 1 + len(sentence) > max_chars:
                pieces.append(current)
                current = sentence
            else:
                current = f"{current} {sentence}".strip()
        if current:
            pieces.append(current)

    # Merge small neighbors so we don't make hundreds of tiny requests.
    chunks: list[str] = []
    for piece in pieces:
        if chunks and len(chunks[-1]) + 2 + len(piece) <= max_chars:
            chunks[-1] += "\n\n" + piece
        else:
            chunks.append(piece)
    return chunks
