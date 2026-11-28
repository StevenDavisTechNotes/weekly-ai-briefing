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
research it checks. The phases run end to end with no pause for review. The change log, fact sheet and verification
file stay in `state/runs/<date>/` for the reader to inspect afterwards.

Any harness that can read and write the repository's files works. Give it the phase prompt and the date; the prompt
lists the files to read and write. Two ready-made ways:

- Claude Code: `/briefing-A-research <date>`, then `/briefing-B-verification <date>`, `/briefing-C-model-update
  <date>` and `/briefing-D-writing <date>`, each in a new session (commands in `.claude/commands/`).
- The Claude API, without an agent harness: `uv run python -m weekly_ai_briefing.generate_briefing_text` runs all
  four phases for today's date, each as a separate request, and writes the output files. Pass phase letters and
  `--date` to run part of it, for example `D` alone to rewrite the briefing from existing phase outputs.
  Phase A runs as seven dimension workers in parallel and then a lead that merges their drafts into the fact
  sheet; the drafts are kept in `state/runs/<date>/research_drafts/`, so a rerun after a failed merge reuses them.
  Pass `--single-research` to run phase A as one request instead.
  Every page phase A fetches is copied to `source_document_cache/<date>/`, which git ignores. After each phase it
  records minutes and tokens and rewrites `state/runs/<date>/metrics.md`; after phase D it adds the edition's new
  names to `state/pronouncers.md`. `uv run python -m weekly_ai_briefing.run_metrics --history` lists past runs.
  After phase D it checks the edition against the writing rules a script can check (parts, signals, footnotes,
  URLs, metadata keys, length, figures written in digits) and prints anything to fix by hand.

When the edition is written, commit `state/` and the new edition, then publish as before (`scripts/publish_text.ps1`). Publishing
first runs the test suite and the edition rule check (`edition_checks --latest`) and stops if either fails; it
ends by deleting all but the two newest date folders in `source_document_cache/`.

## Other prompts

- `bootstrap/prompt.md`: run once to build the first current model and state table from the past editions.
- `prompt_one_big.md`: a single, self-contained prompt for the comparison briefings other models write
  (`editions/<model>_version/`). It has the same reader, dimensions, sourcing and writing rules as the phases but no
  state files: run it in the same conversation as that model's earlier editions, which carry the mental model
  forward. When `shared/reader_and_dimensions.md` or the writing rules in `D_writing/prompt.md` change, update it to
  match.
