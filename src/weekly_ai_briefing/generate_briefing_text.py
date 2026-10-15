#! python3
# usage: uv run python -m src.weekly_ai_briefing.generate_briefing_text

import datetime
import time
from pathlib import Path

import httpx2
from anthropic import Anthropic, APIConnectionError, APIStatusError
from anthropic.types import Message, MessageParam, ThinkingConfigAdaptiveParam, ToolUnionParam

HISTORY_FOLDER = Path("history")
PROMPT_FOLDER = Path(__file__).resolve().parent / "prompts"
MODEL = "claude-opus-5-5"
EFFORT = "medium"
MAX_TOKENS: int = 128000
HISTORY_LOOKBACK: int = 2
MAX_CONTINUATIONS: int = 10  # per request: pause_turn resumes + max_tokens continues
# The whole briefing is one long streamed call, so a dropped connection or an
# overloaded API would otherwise discard all the research done so far.
STREAM_RETRIES: int = 4
STREAM_RETRY_BASE_SECONDS: int = 30

# The briefing is about the preceding week, so the model must be able to search.
TOOLS: list[ToolUnionParam] = [
    {"type": "web_search_20260318", "name": "web_search"},
]


def load_recent_reports(
        reports_dir: Path,
        limit: int,
        exclude_name: str,
) -> list[str]:
    """Loads the N most recent weekly reports from disk, skipping exclude_name.

    exclude_name is the file about to be written, so a same-day rerun does
    not treat its own earlier draft as a previous week's report.
    """
    if not reports_dir.is_dir():
        return []

    files = sorted(  # Newest first
        (f for f in reports_dir.glob("*.md") if f.name != exclude_name),
        reverse=True,
    )

    return [
        f"--- START OF {f.name} ---\n"
        + f.read_text(encoding='utf-8')
        + "--- END ---"
        for f in files[:limit]
    ]


TRANSIENT_ERROR_TYPES = {"overloaded_error", "api_error", "rate_limit_error"}


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
                tools=TOOLS,
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
) -> str:
    """Sends the conversation and returns the assistant's complete text reply.

    Resumes server-side tool turns (`pause_turn`) and continues truncated
    output (`max_tokens`). `messages` is not modified.
    """
    messages = messages.copy()
    text_parts: list[str] = []

    for _ in range(MAX_CONTINUATIONS + 1):
        response = stream_message(client, system_prompt, messages)

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
    output_path = HISTORY_FOLDER / f"briefing-{today}.md"

    system_prompt = (
        PROMPT_FOLDER / "prompt_one_big.md").read_text(encoding="utf-8")
    context_prompt = (
        (PROMPT_FOLDER / "prompt_context.md")
        .read_text(encoding="utf-8")
        .replace(
            "::past_reports_context::",
            "\n\n".join(
                load_recent_reports(
                    reports_dir=HISTORY_FOLDER,
                    limit=HISTORY_LOOKBACK,
                    exclude_name=output_path.name,
                )
            )
        )
    )

    # Single pass: the whole briefing is written in one response, so the
    # 15,000-word target applies to the briefing as a whole.
    messages: list[MessageParam] = [
        {
            "role": "user",
            "content": f"Today's date is {today}.\n\n{context_prompt}",
        }
    ]

    print("Generating briefing...")
    briefing = send(client, system_prompt, messages)

    report = f"Coverage week ending on {today}\n\n{briefing}"

    HISTORY_FOLDER.mkdir(exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(f"Report successfully generated and saved to {output_path}")


def main() -> None:
    generate_weekly_report()


if __name__ == "__main__":
    main()
