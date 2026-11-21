# Briefing prompts

Each week's briefing is produced in four phases, each in a fresh conversation. Files carry the work from one phase
to the next; the mutable state lives in `state/` at the repository root (see `state/README.md`).

| Phase | Prompt | Reads | Writes |
|---|---|---|---|
| A, research | `A_research/prompt.md` | current model, state table | `state/runs/<date>/fact_sheet.md` |
| B, verification | `B_verification/prompt.md` | current model, fact sheet | `state/runs/<date>/verification.md` |
| C, model update | `C_model_update/prompt.md` | current model, state table, fact sheet, verification | `state/runs/<date>/change_log.md`, revised `state/current_model.md` and `state/state_table.md` |
| D, writing | `D_writing/prompt.md` | revised model and table, change log, fact sheet, verification | `editions/markdown_format/<date>-ai-outlook-briefing.md` |

Every phase also reads `shared/reader_and_dimensions.md`. `<date>` is the edition's publication date.

## Weekly run

Run the phases in order, each in a new conversation, so that verification in particular is independent of the
research it checks. Between C and D, optionally read `state/runs/<date>/change_log.md` and edit the model, the
table or the five-signal ranking before the briefing is written.

Any harness that can read and write the repository's files works. Give it the phase prompt and the date; the prompt
lists the files to read and write. Two ready-made ways:

- Claude Code: `/briefing-A-research <date>`, then `/briefing-B-verification <date>`, `/briefing-C-model-update
  <date>` and `/briefing-D-writing <date>`, each in a new session (commands in `.claude/commands/`).
- The Claude API, without an agent harness: `uv run python -m weekly_ai_briefing.generate_briefing_text` runs all
  four phases for today's date, each as a separate request, and writes the output files. Pass phase letters and
  `--date` to run part of it, for example `A B C` to stop before writing for review, then `D`.

When the edition is written, commit `state/` and the new edition, then publish as before (`scripts/publish_text.ps1`).

## Other prompts

- `bootstrap/prompt.md`: run once to build the first current model and state table from the past editions.
