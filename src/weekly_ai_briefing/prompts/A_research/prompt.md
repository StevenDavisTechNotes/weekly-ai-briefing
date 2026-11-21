# Phase A: Research

Start a fresh conversation for this phase.

Read first:

- `src/weekly_ai_briefing/prompts/shared/reader_and_dimensions.md`
- `state/README.md`, for the file formats and source types
- `state/current_model.md`
- `state/state_table.md`
- `editions/gemini_version/<date>-gemini.md`, if it exists: a briefing another model wrote for the same week

Write: `state/runs/<date>/fact_sheet.md`, where `<date>` is today's date (the publication date).

## Research window

Research the seven days before today. If run on 2026-10-24, the window is 2026-10-17 through 2026-10-23. Older
items may be used only as background and are marked as such.

## What to look for

Research has two jobs, and both matter.

1. Test the model. For every claim in `current_model.md` and every row in `state_table.md`, look for this week's
   evidence for and against it. Look hardest for evidence against: the model improves where reality shows its
   fault lines. Record "no material evidence" for a claim or row when you looked and found nothing.
2. Find surprises. Search each of the seven dimensions for developments that the current model did not expect.
   A surprise matters when it is unexpected and would change how the reader reasons or decides, not when it is
   loud. Corporate deal noise, routine partnerships, generic fundraising rounds and consensus rehash are not
   surprises.

Also check each item on the watching list, since a second week of evidence can promote it.

If the other model's briefing for this week exists, use it only as a coverage check. List each development it
reports that your search missed, then find the primary source for it and record it as a fact, or leave it out if no
source confirms it. Never cite that briefing, and do not adopt its analysis.

For every fact, classify the change it shows:

- new trend: something the model does not yet describe.
- acceleration or deceleration: an existing trend speeding up or slowing down.
- reversal: an existing trend changing direction.
- level only: the trend continues as expected; worth at most a line.

## Sources

- Prefer primary sources. Read the filing, the release, the statistical table or the paper itself when you can,
  including lab research blogs and new papers for the AI Technology dimension.
- Use digests and newsletters only to find stories; cite the article or document they point to.
- For what AI is doing to issuers' business models, search the week's SEC filings, earnings-call transcripts and
  shareholder letters directly; these primary disclosures carry measured effects that press coverage often skips.
- Aim for a mix of source types, and let no single source supply more than about a tenth of the facts.
- Record a number only with its exact value, unit, date and the source that states it. Never compute a number
  and present it as reported; if you derive one, mark it "derived" and show the arithmetic.
- Note when a source could not be read, when a claim rests on one source only, and when sources disagree.

## Fact sheet format

```markdown
# Fact sheet

Edition: YYYY-MM-DD. Window: YYYY-MM-DD to YYYY-MM-DD.

## Facts

### F-01 Short label

- Fact: one or two sentences stating what happened, with its date.
- Figures: each number with unit and date, or "none".
- Source: outlet or author, title, date, and URL.
- Source type: primary, wire or trade, analyst, or secondhand.
- Bears on: model claim ids, state-table rows, watching items, or "new".
- Change type: new trend, acceleration, deceleration, reversal, or level only.
- Expected vs. happened: one sentence on what the model would have predicted and how this differs.
- Consequence: one sentence on what it would change for the reader if it holds.

## Model check

One line per claim and per row: the fact ids for and against, or "no material evidence".

## Research limits

Sources that could not be read, single-source claims, disagreements between sources, and expected developments
looked for and not found.
```

Number facts F-01, F-02 and so on in the order found. Aim for 40 to 80 facts; completeness on the model check
matters more than volume. Do not write analysis or prose for the briefing in this phase.
