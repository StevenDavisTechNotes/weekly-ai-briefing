# Briefing prompts

Each week's briefing is produced in four phases, each in a fresh conversation in the Claude app or Claude Code.
Files carry the work from one phase to the next; the mutable state lives in `state/` at the repository root (see
`state/README.md`).

| Phase | Prompt | Reads | Writes |
|---|---|---|---|
| A, research | `A_research/prompt.md` | current model, state table | `state/runs/<date>/fact_sheet.md` |
| B, verification | `B_verification/prompt.md` | current model, fact sheet | `state/runs/<date>/verification.md` |
| C, model update | `C_model_update/prompt.md` | current model, state table, fact sheet, verification | `state/runs/<date>/change_log.md`, revised `state/current_model.md` and `state/state_table.md` |
| D, writing | `D_writing/prompt.md` | revised model and table, change log, fact sheet, verification | `editions/markdown_format/<date>-ai-outlook-briefing.md` |

Every phase also reads `shared/reader_and_dimensions.md`. `<date>` is the edition's publication date.

## Weekly run

1. Start a new conversation and run phase A. In Claude Code: `/briefing-A-research 2026-11-21`. In the Claude
   app: attach the phase prompt and the files it lists, and give the date.
2. Start a new conversation and run phase B (`/briefing-B-verification <date>`). Keep it separate from phase A so
   the check is independent.
3. Start a new conversation and run phase C (`/briefing-C-model-update <date>`).
4. Optional review: read `state/runs/<date>/change_log.md` and edit the model, the table or the five-signal
   ranking before writing.
5. Start a new conversation and run phase D (`/briefing-D-writing <date>`).
6. Commit `state/` and the new edition, then publish as before (`scripts/publish_text.ps1`).

## Other prompts

- `bootstrap/prompt.md`: run once to build the first current model and state table from the past editions.
- `prompt_one_big.md` and `prompt_context.md`: the earlier single-prompt process, used by
  `generate_briefing_text.py`. Kept for reference until the phased process has run for a few weeks.
