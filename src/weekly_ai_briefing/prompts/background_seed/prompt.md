# Background seeding: the backstory the model rests on

Run once to create the first `state/background.md`, in two parts, each in its own fresh conversation, so that the
check in part 2 is independent of the research in part 1. Rerun only to rebuild the file from scratch; phase C
maintains it each week.

`<date>` is the date of the latest edition, the date this file is seeded as of.

## What the file is for

The weekly research looks at seven days. Some developments only make sense against a story that began before that
window, or before the first edition: the Hopper licensing deadlock and the neocloud credit it squeezed is one
example, which reached the briefing only as fragments. `state/background.md` holds those stories, so that research
can recognize a new fact as the next step of an old story and writing can remind the listener of it in a sentence.

It is not a history of AI. A story goes back only as far as it takes to explain a mechanism the model uses today,
and no further.

## Which stories qualify

A story qualifies only when all three hold:

1. It is still running: it has a live consequence within the briefing's four-year horizon.
2. A current claim, state-table row or watching item rests on it.
3. It began before the research window of the edition it would first be needed in, or before the first edition.

Early machine-learning research, the history of a company or a technology, and settled events do not qualify unless
a current claim rests on them. Keep at most 12 stories, preferring those that more claims and rows rest on.

## Part 1: research

Read first:

- `src/weekly_ai_briefing/prompts/shared/reader_and_dimensions.md`
- `state/README.md`, for the background format, the source types and the specification standard
- `state/current_model.md` and `state/state_table.md`
- Any extra story files under `editions/extra_*/`, if present: unverified leads only, never sources

Write: `state/runs/<date>/background_draft.md`, in the background format, plus a final `## Seeding notes` section.

Steps:

1. For each claim, row and watching item, ask what earlier story it rests on that a reader new to the briefing
   would not know. List the candidates, merging those that are one story.
2. Apply the qualification test, and keep at most 12.
3. For each story, research three to six milestones, each a dated event with a primary source where one exists,
   read in full. Prefer the first official act (a rule, filing, release or statistic) over commentary. Follow the
   evidence rules of `src/weekly_ai_briefing/prompts/A_research/prompt.md`, including its rules for inferring what
   private credit does not disclose.
4. Write where each story stands as of `<date>`, and what observable outcome would end it.
5. In the seeding notes, list the candidates you did not keep, each with one line on why, and every source you could
   not read.

## Part 2: verification

Start a fresh conversation. Do not reuse the research conversation.

Read first:

- `src/weekly_ai_briefing/prompts/shared/reader_and_dimensions.md`
- `state/README.md`
- `state/current_model.md` and `state/state_table.md`
- `state/runs/<date>/background_draft.md`

Write: `state/background.md`, and `state/runs/<date>/background_verification.md`.

For every milestone, open its source again and read it in full, as in
`src/weekly_ai_briefing/prompts/B_verification/prompt.md`. Keep a milestone that the source supports, correcting it
where needed; remove one whose source cannot be read or does not support it. Remove a story left with fewer than
two milestones, or that fails the qualification test. Record each milestone's verdict, and each removal with its
reason, in the verification file, then write `state/background.md` with "As of" set to `<date>`.
