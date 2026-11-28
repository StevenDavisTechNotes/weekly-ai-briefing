---
description: Seed state/background.md once (research, then verification). Argument: the latest edition's date, YYYY-MM-DD.
---

Seed the briefing's background file as of $ARGUMENTS (if no date is given, use the date of the latest edition in
`editions/markdown_format/`). Follow `src/weekly_ai_briefing/prompts/background_seed/prompt.md` exactly, with
`<date>` set to that date: run part 1 in its own subagent, wait for its draft, then run part 2 in a second, fresh
subagent, so that verification is independent of the research.
