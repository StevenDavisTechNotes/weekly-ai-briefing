# Phase D: Writing

Start a fresh conversation for this phase.

Read first:

- `src/weekly_ai_briefing/prompts/shared/reader_and_dimensions.md`
- `state/current_model.md` and `state/state_table.md`, as revised by phase C this week
- `state/runs/<date>/change_log.md`
- `state/runs/<date>/fact_sheet.md`
- `state/runs/<date>/verification.md`

Write: `editions/markdown_format/<date>-ai-outlook-briefing.md`.

The analysis is done. This phase turns it into a briefing for listening. Do not research, and do not change the
model, the table or the ranking of the five signals. Use only facts whose verdict is confirmed or corrected, with
corrections applied. An unconfirmed fact may be mentioned only with its caveat, and never with its figures.

## Length

Aim for about 5,000 to 6,000 words for the body, excluding the Source Notes and the metadata block. This is a
budget, not a target: a quiet week should be shorter. A dimension with nothing that moved the model or the table
gets one or two sentences saying so, not a recap of its baseline.

## Briefing structure

- Orientation: The Five Signals That Matter This Week
- Dimensions
  - AI Technology
  - Quantum Computing
  - Enterprise AI Adoption
  - Physical AI & Industrial Automation
  - Societal Adoption
  - Economic Structural Change
  - Institutional Financial Services
- Strategic Mental Model Shifts
- Source Notes and Attribution
- Edition metadata: one YAML block between `---` lines at the very end (not a `##` part), as described below

Start each of these parts with a level-2 heading (`##`) using exactly the title shown, with the seven dimensions
as seven separate parts. Use `###` or lower for everything inside a part; never use `##` for anything else. Each
`##` part becomes its own email and audio file.

## Continuity for listeners

The reader listens over several hours, one part at a time. A brief reminder of a related story from an earlier
part, or of the model claim a finding bears on, helps them keep the thread; one or two sentences is enough. Refer
to model claims by name, never by id.

## Core content and formatting rules

- Format: Professional executive briefing format optimized for text-to-speech listening. Present findings via
  structured narrative paragraphs and clear bulleted breakdowns, and put detailed data in markdown tables as
  described below. Omit conversational podcast filler, greetings, and timestamps.
- Numbers: Use few numbers, and only verified ones. Prefer relative scale that explains behavior, such as "about
  four times larger" or "the lowest on record", over precise figures. Use no more than 2 numbers in any sentence
  and no more than 4 in any paragraph or bullet. A number here means any figure: a percentage, amount, count, rate,
  ratio, price, or growth figure, including a figure written out in words. Dates and footnote references do not
  count. Do not say "Version X runs at 1.1 while version Y runs at 2.0." as this does not translate well to audio
  playback.
- Markdown tables: Use a table when several related figures would otherwise crowd the text. Tables are skipped in
  audio playback, so give each a one-line introduction that says what it shows, and make sure the surrounding text
  states the finding in words. Put only figures from primary sources, or from two independent sources, in a
  table. Keep tables simple: a header row, short cell text, units in the header, and footnote references in a
  final source column or after the cell they support.
- Source strength in the text: When a fact rests on a secondhand source, a single source, or a company's own
  claim, say so in words in the sentence, such as "according to the company" or "in a report that could not be
  confirmed".
- Citations: Never put identifiers, arXiv numbers, URLs or other reference strings in the running text, because
  they do not work in audio playback. Name the source in words instead (for example "a paper by Bürger and
  colleagues") and mark the claim with a numbered footnote reference such as `[^1]` immediately after the sentence
  it supports. Number references in order of first appearance across the whole briefing, and reuse a number when
  citing the same source again. Define every reference once, in the "Source Notes and Attribution" part, using the
  form `[^1]: [Anchor Text](URL)` or, when there is no URL, `[^1]: citation text`. For an arXiv paper, use the
  paper title and identifier as the definition text, with the arXiv link as the URL.
- Findings: For each finding with changes, give a summary followed by a First-Derivative Forward Extrapolation
  ("So-What?" analysis) as a separate paragraph, not a heading, that opens with a spoken cue such as
  "Extrapolating forward," so listeners hear where the forecast begins. Say which model claim or table row the
  finding bears on, and whether it is a new trend, an acceleration, a deceleration or a reversal.

## Orientation: The Five Signals That Matter This Week

- Open with one sentence explaining that these are the week's five developments that most changed, or most
  tested, the mental model.
- Then give exactly five bullets, introduced as "First,", "Second,", and so on, in the order the change log
  ranks them.
- Each bullet is one paragraph of three to five sentences: what happened, with its date, and what it changes or
  tests in the model. Keep figures to the one or two that carry the point.
- These bullets preview the dimension sections, which expand on them; do not add separate "So-What?" analysis
  here.

## Strategic Mental Model Shifts

Write this part from the change log, in this order:

- `### What changed in the model`: the revised, new and retired claims, each with what reality showed and why the
  old version no longer fits. If nothing changed, say so in one or two sentences; that is a valid week.
- `### What continued`: the claims that held or strengthened, briefly. This subsection and the reminders in it may
  take at most half of this part.
- `### Watching`: newly added or promoted watching items, one sentence each.
- `### The state table`: a spoken walk-through of the rows that moved this week, saying for each what moved, in
  which direction, and whether its regime changed, followed by the full state table copied from
  `state/state_table.md` (the summary table only, not the row definitions). Rows that did not move are not
  discussed; the table shows them. Say dates and levels in words suited to audio.

## Source Notes and Attribution

- Open with one line stating the date window of the principal sources consulted.
- List the sources as bullets grouped by topic. Within each bullet, name the outlet or author, what it covered, its
  date, and its source type (primary, wire or trade, analyst, or secondhand); mark older items as "for
  background". Cite arXiv papers by identifier. Do not include bare URLs.
- Follow with a "Discrepancies and limits noted during research" list, drawn from the fact sheet's research limits
  and the verification file: corrected figures, unconfirmed and single-source claims, sources that could not be
  read, and expected developments looked for and not found.
- Then give the footnote definitions for every `[^n]` reference used in the briefing, one per line, in numeric
  order. Every reference in the text must have a definition and every definition must be referenced. These
  definitions are the only place URLs may appear.
- Finish with an attribution to the model that generated the briefing.

## Edition metadata block

- After the attribution, end the response with the metadata block: a line holding only `---`, the YAML, and a final
  line holding only `---`. Do not wrap it in a code fence, write nothing after the closing `---`, and use no other
  YAML block in the response.
- Write the title and summary last, after reviewing the whole briefing.
- The block holds exactly these five keys, in this order:
  - title: a double-quoted headline of 5 to 15 words naming the edition's dominant theme.
  - publication_date: today's date, unquoted, in YYYY-MM-DD form.
  - survey_begin_date: the first day of the research window, unquoted, in YYYY-MM-DD form.
  - survey_last_date: the last day of the research window, unquoted, in YYYY-MM-DD form.
  - summary: a double-quoted summary of 20 to 35 words covering the edition's most significant developments,
    written as plain prose without footnote references, URLs, or markdown.
- Escape any double quote inside a value with a backslash.
