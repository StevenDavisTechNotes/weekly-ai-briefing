#! python3
"""Runs the four briefing phases (research, verification, model update, writing) through the Claude API.

This is one way to run the phased process described in prompts/README.md; any harness that can read and write the
repository's files works too. Each phase is a separate request with no shared conversation, matching the "fresh
conversation" rule in the phase prompts. The files a phase reads are sent inline, and the phase returns the files it
writes between BEGIN and END marker lines, which this script writes to disk.

usage:
    uv run python -m weekly_ai_briefing.generate_briefing_text                  # all phases, today's date
    uv run python -m weekly_ai_briefing.generate_briefing_text D --date 2026-11-21
"""

import argparse
import datetime
import re
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

import httpx2
from anthropic import Anthropic, APIConnectionError, APIStatusError
from anthropic.types import Message, MessageParam, ThinkingConfigAdaptiveParam, ToolUnionParam

from weekly_ai_briefing.bottom_matter import format_bottom_matter, split_bottom_matter
from weekly_ai_briefing.config import (
    EDITIONS_FOLDER,
    EFFORT,
    MARKDOWN_FOLDER,
    MAX_CONTINUATIONS,
    MAX_TOKENS,
    MODEL,
    PROMPT_FOLDER,
    REPO_ROOT,
    RESEARCH_TOOLS,
    STATE_FOLDER,
    STREAM_RETRIES,
    STREAM_RETRY_BASE_SECONDS,
    TRANSIENT_ERROR_TYPES,
    VERIFICATION_TOOLS,
)

SHARED_PROMPT = PROMPT_FOLDER / "shared" / "reader_and_dimensions.md"
STATE_README = STATE_FOLDER / "README.md"
CURRENT_MODEL = STATE_FOLDER / "current_model.md"
STATE_TABLE = STATE_FOLDER / "state_table.md"

FILE_BLOCK = re.compile(r"^=== BEGIN (?P<path>\S+) ===\n(?P<body>.*?)^=== END (?P=path) ===$", re.MULTILINE | re.DOTALL)


def run_folder(date: str) -> Path:
    return STATE_FOLDER / "runs" / date


def edition_path(date: str) -> Path:
    return MARKDOWN_FOLDER / f"{date}-ai-outlook-briefing.md"


def other_model_briefings(date: str) -> list[Path]:
    """Other models' briefings for the same week, editions/<model>_version/<date>-<model>.md.

    Phase A uses them only as a coverage check.
    """
    return sorted(EDITIONS_FOLDER.glob(f"*_version/{date}-*.md"))


@dataclass(frozen=True)
class Phase:
    name: str
    prompt: Path
    inputs: Callable[[str], list[Path]]
    outputs: Callable[[str], list[Path]]
    tools: list[ToolUnionParam]
    optional_inputs: Callable[[str], list[Path]] = field(default=lambda date: [])

    def present_inputs(self, date: str) -> list[Path]:
        """The required inputs, then whichever optional inputs exist."""
        return self.inputs(date) + [path for path in self.optional_inputs(date) if path.is_file()]


PHASES: dict[str, Phase] = {
    "A": Phase(
        name="research",
        prompt=PROMPT_FOLDER / "A_research" / "prompt.md",
        inputs=lambda date: [SHARED_PROMPT, STATE_README, CURRENT_MODEL, STATE_TABLE],
        outputs=lambda date: [run_folder(date) / "fact_sheet.md"],
        tools=RESEARCH_TOOLS,
        optional_inputs=other_model_briefings,
    ),
    "B": Phase(
        name="verification",
        prompt=PROMPT_FOLDER / "B_verification" / "prompt.md",
        inputs=lambda date: [SHARED_PROMPT, STATE_README, CURRENT_MODEL, run_folder(date) / "fact_sheet.md"],
        outputs=lambda date: [run_folder(date) / "verification.md"],
        tools=VERIFICATION_TOOLS,
    ),
    "C": Phase(
        name="model update",
        prompt=PROMPT_FOLDER / "C_model_update" / "prompt.md",
        inputs=lambda date: [
            SHARED_PROMPT,
            STATE_README,
            CURRENT_MODEL,
            STATE_TABLE,
            run_folder(date) / "fact_sheet.md",
            run_folder(date) / "verification.md",
        ],
        outputs=lambda date: [run_folder(date) / "change_log.md", CURRENT_MODEL, STATE_TABLE],
        tools=[],
    ),
    "D": Phase(
        name="writing",
        prompt=PROMPT_FOLDER / "D_writing" / "prompt.md",
        inputs=lambda date: [
            SHARED_PROMPT,
            CURRENT_MODEL,
            STATE_TABLE,
            run_folder(date) / "change_log.md",
            run_folder(date) / "fact_sheet.md",
            run_folder(date) / "verification.md",
        ],
        outputs=lambda date: [edition_path(date)],
        tools=[],
    ),
}


def relative(path: Path) -> str:
    """The path as the prompts name it: relative to the repository root, with forward slashes."""
    return path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()


def build_request(phase: Phase, date: str) -> str:
    """The user message for one phase: the date, the output protocol, and every input file inline."""
    missing = [relative(path) for path in phase.inputs(date) if not path.is_file()]
    if missing:
        raise SystemExit(f"Phase {phase.name} cannot start; missing input files: {', '.join(missing)}")
    outputs = "\n".join(f"- {relative(path)}" for path in phase.outputs(date))
    files = "\n\n".join(
        f"=== BEGIN {relative(path)} ===\n{path.read_text(encoding='utf-8').rstrip()}\n=== END {relative(path)} ==="
        for path in phase.present_inputs(date)
    )
    return (
        f"Today's date is {date}, so <date> in the prompt is {date}.\n\n"
        "You are running through the API without file access. The files the prompt tells you to read are included "
        "below, each between a BEGIN and an END line naming its path. Return each file the prompt tells you to "
        "write, complete, in the same form: a line `=== BEGIN <path> ===`, the file's content, and a line "
        "`=== END <path> ===`. Write nothing outside those blocks. The files to return are:\n\n"
        f"{outputs}\n\n{files}\n"
    )


def parse_output_files(response: str, expected: Sequence[str]) -> dict[str, str]:
    """Extracts the BEGIN/END file blocks from a phase's reply, insisting on exactly the expected paths."""
    files = {match["path"]: match["body"].rstrip() + "\n" for match in FILE_BLOCK.finditer(response)}
    missing = [path for path in expected if path not in files]
    extra = [path for path in files if path not in expected]
    if missing or extra:
        problems = [f"missing {', '.join(missing)}"] if missing else []
        problems += [f"unexpected {', '.join(extra)}"] if extra else []
        raise ValueError(f"reply did not return the expected files: {'; '.join(problems)}")
    return files


def normalize_edition(text: str) -> str:
    """Re-emits the edition's YAML bottom matter in canonical form, or warns and keeps the text as written."""
    try:
        bottom_matter, body = split_bottom_matter(text)
    except ValueError as error:
        bottom_matter, problem = None, str(error)
    else:
        problem = "the briefing does not end with a --- delimited YAML block"
    if bottom_matter is None:
        print(f"Warning: {problem}; saved as written, fix the bottom matter by hand before publishing")
        return text
    return f"{body}\n{format_bottom_matter(bottom_matter)}"


def is_transient(error: Exception) -> bool:
    if isinstance(error, (APIConnectionError, httpx2.TransportError)):
        return True
    if not isinstance(error, APIStatusError):
        return False
    if error.status_code == 429 or error.status_code >= 500:
        return True
    # An error event mid-stream arrives on an HTTP 200 response, so only
    # the error type in the body says whether it is worth retrying.
    body = error.body
    if isinstance(body, dict) and isinstance(body.get("error"), dict):
        return body["error"].get("type") in TRANSIENT_ERROR_TYPES
    return False


def stream_message(
        client: Anthropic,
        system_prompt: str,
        messages: list[MessageParam],
        tools: list[ToolUnionParam],
) -> Message:
    """Streams one request, retrying transient failures with backoff."""
    for attempt in range(STREAM_RETRIES + 1):
        try:
            with client.messages.stream(
                max_tokens=MAX_TOKENS,
                messages=messages,
                model=MODEL,
                output_config={"effort": EFFORT},
                system=system_prompt,
                thinking=ThinkingConfigAdaptiveParam(
                    type="adaptive",
                    display="omitted",
                ),
                tools=tools,
            ) as stream:
                return stream.get_final_message()
        except (APIConnectionError, APIStatusError, httpx2.TransportError) as error:
            if not is_transient(error) or attempt == STREAM_RETRIES:
                raise
            delay = STREAM_RETRY_BASE_SECONDS * 2 ** attempt
            print(f"Transient API error ({error}); retrying in {delay}s...")
            time.sleep(delay)
    raise AssertionError("unreachable")


def send(
        client: Anthropic,
        system_prompt: str,
        messages: list[MessageParam],
        tools: list[ToolUnionParam],
) -> str:
    """Sends the conversation and returns the assistant's complete text reply.

    Resumes server-side tool turns (`pause_turn`) and continues truncated
    output (`max_tokens`). `messages` is not modified.
    """
    messages = messages.copy()
    text_parts: list[str] = []

    for _ in range(MAX_CONTINUATIONS + 1):
        response = stream_message(client, system_prompt, messages, tools)

        text = "".join(
            b.text
            for b in response.content
            if b.type == "text"
        )

        if response.stop_reason == "end_turn":
            text_parts.append(text)
            return "".join(text_parts)

        if response.stop_reason == "pause_turn":
            # Server tool loop hit its iteration limit; resend the assistant
            # turn as-is (including tool blocks) so the model resumes.
            text_parts.append(text)
            messages.append({"role": "assistant", "content": response.content})
        elif response.stop_reason == "max_tokens":
            text_parts.append(text)
            messages.append({"role": "assistant", "content": text})
            messages.append({
                "role": "user",
                "content": "Continue exactly where you left off. "
                           "Do not repeat anything already written.",
            })
        else:
            raise RuntimeError(
                f"Unexpected stop_reason {response.stop_reason!r}; "
                f"partial output: {''.join(text_parts + [text])[-500:]!r}"
            )

    raise RuntimeError(
        f"Response still incomplete after {MAX_CONTINUATIONS} continuations")


def run_phase(
        *,
        client: Anthropic,
        letter: str,
        date: str,
) -> None:
    phase = PHASES[letter]
    request = build_request(phase, date)
    print(f"Phase {letter} ({phase.name})...")
    reply = send(
        client,
        phase.prompt.read_text(encoding="utf-8"),
        [{"role": "user", "content": request}],
        phase.tools,
    )

    run_folder(date).mkdir(parents=True, exist_ok=True)
    expected = {relative(path): path for path in phase.outputs(date)}
    try:
        files = parse_output_files(reply, list(expected))
    except ValueError as error:
        raw = run_folder(date) / f"phase_{letter}_reply.md"
        raw.write_text(reply, encoding="utf-8")
        raise SystemExit(f"Phase {letter}: {error}. The full reply is saved in {raw}") from error

    for name, text in files.items():
        path = expected[name]
        if path == edition_path(date):
            text = normalize_edition(text)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print(f"  wrote {name}")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run briefing phases through the Claude API.")
    parser.add_argument(
        "phases",
        nargs="*",
        choices=list(PHASES),
        default=list(PHASES),
        help="phases to run, in order (default: A B C D)",
    )
    parser.add_argument(
        "--date",
        default=datetime.date.today().isoformat(),
        type=lambda value: datetime.date.fromisoformat(value).isoformat(),
        help="edition publication date, YYYY-MM-DD (default: today)",
    )
    args = parser.parse_args(argv)
    args.phases = sorted(set(args.phases))
    return args


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(argv)
    client = Anthropic()
    try:
        for letter in args.phases:
            run_phase(
                client=client,
                letter=letter,
                date=args.date,
            )
    except KeyboardInterrupt:
        print("Interrupted")


if __name__ == "__main__":
    main()
