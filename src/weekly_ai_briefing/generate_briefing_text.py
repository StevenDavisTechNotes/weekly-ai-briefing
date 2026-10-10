#! python3
# usage: pythom -m src.weekly_ai_briefing.main

import datetime
from pathlib import Path

from anthropic import Anthropic
from anthropic.types import MessageParam, ThinkingConfigAdaptiveParam, ToolUnionParam

HISTORY_FOLDER = Path("history")
PROMPT_FOLDER = Path(__file__).resolve().parent / "prompts"
MODEL = "claude-opus-5-5"
EFFORT = "medium"
MAX_TOKENS: int = 128000
HISTORY_LOOKBACK: int = 2
SECTION_COUNT: int = 6
MAX_CONTINUATIONS: int = 10  # per request: pause_turn resumes + max_tokens continues

# The briefing is about the preceding week, so the model must be able to search.
TOOLS: list[ToolUnionParam] = [
    {"type": "web_search_20260318", "name": "web_search"},
]


def load_recent_reports(
        reports_dir: Path,
        limit: int
) -> list[str]:
    """Loads the N most recent weekly reports from disk."""
    if not reports_dir.is_dir():
        return []

    files = sorted(reports_dir.glob("*.md"), reverse=True)  # Newest first

    return [
        f"--- START OF {f.name} ---\n"
        + f.read_text(encoding='utf-8')
        + "--- END ---"
        for f in files[:limit]
    ]


def send(
        client: Anthropic,
        system_prompt: str,
        messages: list[MessageParam],
        tools: list[ToolUnionParam] | None = None,
) -> str:
    """Sends the conversation and returns the assistant's complete text reply.

    Resumes server-side tool turns (`pause_turn`) and continues truncated
    output (`max_tokens`). `messages` is not modified.
    """
    messages = messages.copy()
    text_parts: list[str] = []

    for _ in range(MAX_CONTINUATIONS + 1):
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
            tools=tools if tools else [],
        ) as stream:
            response = stream.get_final_message()

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


def generate_weekly_report() -> None:
    client = Anthropic()
    today = datetime.date.today().isoformat()

    system_prompt = (
        PROMPT_FOLDER / "prompt_system.md").read_text(encoding="utf-8")
    context_prompt = (
        (PROMPT_FOLDER / "prompt_context.md")
        .read_text(encoding="utf-8")
        .replace(
            "::past_reports_context::",
            "\n\n".join(
                load_recent_reports(
                    reports_dir=HISTORY_FOLDER,
                    limit=HISTORY_LOOKBACK,
                )
            )
        )
    )

    # One conversation: the system prompt promises sections arrive as separate
    # messages, and later sections build on earlier ones.
    messages: list[MessageParam] = [
        {
            "role": "user",
            "content": f"Today's date is {today}.\n\n{context_prompt}",
        }
    ]

    ack = send(client, system_prompt, messages)
    if ack.strip().strip('."').lower() != "ready":
        raise RuntimeError(
            f"Expected 'Ready.' acknowledgement, got: {ack[:200]!r}"
        )
    messages.append({"role": "assistant", "content": ack})

    sections: list[str] = []
    for section_no in range(1, SECTION_COUNT + 1):
        print(f"Generating section {section_no}/{SECTION_COUNT}...")
        message_prompt = (
            (PROMPT_FOLDER / f"prompt_{section_no}.md")
            .read_text(encoding="utf-8")
        )
        messages.append({"role": "user", "content": message_prompt})
        section_text = send(client, system_prompt, messages, tools=TOOLS)
        # Keep only the text (not search results) in history for later sections.
        messages.append({"role": "assistant", "content": section_text})
        sections.append(section_text)

    report = (
        f"Coverage week ending on {today}\n"
        + "\n".join(
            f"\nSection {i_section}:\n{section_text}"
            for i_section, section_text in enumerate(sections, start=1)
        )
    )

    HISTORY_FOLDER.mkdir(exist_ok=True)
    output_path = HISTORY_FOLDER / f"briefing-{today}.md"
    output_path.write_text(report, encoding="utf-8")

    print(f"Report successfully generated and saved to {output_path}")


def main() -> None:
    generate_weekly_report()


if __name__ == "__main__":
    main()
