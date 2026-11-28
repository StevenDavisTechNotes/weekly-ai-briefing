# Manual Trigger Prompt

Paste everything below the line into the Claude app, in a session that can read and write files in the
`weekly_ai_briefing` repository folder and browse the web.

---

Generate this week's AI Off-Consensus briefing edition, end to end and without stopping.

Today's date is the edition date, `<date>`, in YYYY-MM-DD form. The repository root is the `weekly_ai_briefing`
folder; all paths below are relative to it.

## Process

The briefing is produced in four phases, run in order. Each phase has a prompt file; read it and follow it exactly,
reading every file it lists, with `<date>` set to the edition date.

| Phase | Prompt | Writes |
| --- | --- | --- |
| A, research | `src/weekly_ai_briefing/prompts/A_research/prompt.md` | `state/runs/<date>/fact_sheet.md` |
| B, verification | `src/weekly_ai_briefing/prompts/B_verification/prompt.md` | `state/runs/<date>/verification.md` |
| C, model update | `src/weekly_ai_briefing/prompts/C_model_update/prompt.md` | `state/runs/<date>/change_log.md`, revised `state/current_model.md` and `state/state_table.md` |
| D, writing | `src/weekly_ai_briefing/prompts/D_writing/prompt.md` | `editions/markdown_format/<date>-ai-outlook-briefing.md` |

Every phase also reads `src/weekly_ai_briefing/prompts/shared/reader_and_dimensions.md`. Each phase's prompt says
"start a fresh conversation". If you can run each phase in its own subagent or fresh context, do so, passing it only
the phase prompt and the date, so that verification is independent of the research it checks. If you cannot, run the
phases one after another here, and in phase B re-open every source rather than relying on what you remember of phase A.

## Rules for the whole run

- Run autonomously from start to finish. Do not pause to ask me to check, confirm or approve anything between phases
  or at the end, and do not ask questions. If something is ambiguous or a source cannot be read, make the most
  reasonable choice, record it in the place the phase prompt provides (research limits, verification flags, the
  change log, or the Source Notes), and keep going.
- Do not skip a phase or merge phases. Each phase must write its output file before the next begins.
- Do not edit the prompt files. Write only the files named above.
- Do not commit, push or publish. Only the markdown edition and the files under `state/` are produced.
- The final edition must meet the length, structure, citation, number and metadata-block rules in
  `D_writing/prompt.md`. Before finishing, check the edition file against them: the seven dimensions and other
  required `##` parts, five signals, footnotes all defined and all used, no URLs in running text, and the closing
  YAML block with exactly its five keys.

## When finished

Reply with a short report only: the path of the edition file, its approximate word count, the number of facts
found and how many were confirmed, corrected, unconfirmed and dropped, and whether the mental model changed. Mention
anything that could not be done.
