# Briefing state

This folder holds the mutable state of the weekly briefing: the reader's current mental model and the state
table it is measured against. Each phase prompt under `src/weekly_ai_briefing/prompts/` says which of these files
it reads and writes. Git history of this folder is the history of the model.

| File | Written by | Purpose |
|---|---|---|
| `current_model.md` | bootstrap, then phase C each week | The mental model: a small set of claims, each with what would show it wrong, plus a watching list |
| `state_table.md` | bootstrap, then phase C each week | About 12 to 15 state variables with direction and regime, and the definition of each |
| `runs/<date>/fact_sheet.md` | phase A | The week's facts, one entry per fact, with source and source type |
| `runs/<date>/research_drafts/D<n>.md` | phase A, API route only | Each dimension worker's draft, before the lead merges them |
| `runs/<date>/verification.md` | phase B | A verdict on every fact, from re-reading its source |
| `runs/<date>/change_log.md` | phase C | What changed in the model and table this week, and why |
| `runs/<date>/metrics.md`, `runs/<date>/phase_usage.json` | `weekly_ai_briefing.run_metrics`, after each phase | Counts of facts, verdicts and source types, and minutes and tokens per phase |
| `pronouncers.md` | `weekly_ai_briefing.pronouncer_lexicon`, after phase D | One IPA per name; phase D reads it so names sound the same every week |

Phase A also keeps a copy of each source it reads in `source_document_cache/<date>/` at the repository root. That
folder is not part of the state: git ignores it, and publishing deletes all but the two newest dates.

`<date>` is the publication date of the edition, in YYYY-MM-DD form. The briefing itself, written by phase D,
goes to `editions/markdown_format/<date>-ai-outlook-briefing.md` as before.

## `current_model.md` format

```markdown
# Current model

As of: YYYY-MM-DD

## Claims

### M-01 Three to eight word name

- Claim: one or two sentences stating what we believe and the mechanism behind it.
- Dimensions: the briefing dimensions it bears on.
- Introduced: YYYY-MM-DD. Last revised: YYYY-MM-DD.
- Confidence: firm or provisional.
- Why we believe it: two to four sentences of evidence, with sources named in words and dates.
- Would be wrong if: an observable outcome, stated to the specification standard below.
- Check each week: the named pages, releases or series where a reading of that test would appear, so research can
  open each one directly.

## Watching

- W-01 Name. First seen YYYY-MM-DD. What surprised us, and what evidence would promote it to a claim or drop it.

## Test calendar

| Due | Item | What settles then |
|---|---|---|
| YYYY-MM-DD | M-xx or W-xx Name | the reading that settles its test, promotion or drop |

## Retired this quarter

- Name. Retired YYYY-MM-DD. One sentence on why: refuted, absorbed into another claim, or churn that never
  changed how we reason.
```

The test calendar lists every dated claim test and every watching item with a dated promotion or drop rule,
soonest first, with the due date taken from the item's own text. A claim or item with no date is not listed.

Keep at most 12 claims and at most 8 watching items. Claim ids are never reused. Clear "Retired this quarter" at
each quarterly review.

## `state_table.md` format

```markdown
# State table

As of: YYYY-MM-DD

| Row | Latest shift | Major trend | Direction | Regime | Introduced | Takeaway |
|---|---|---|---|---|---|---|
| Short row name | what moved this week, or "none" | the trend over months, in a few words | accelerating, steady, decelerating or reversing | current level on the row's regime scale, or "n/a" | YYYY-MM-DD | one short sentence on what it means for the reader |

## Row definitions

### Short row name

- Measure: what is observed and where, precisely enough that two readers would agree on a reading.
- Regime scale: the ordered levels, each with written criteria, or "none" for a purely numeric row.
- Why it is in the table: the model claims it informs, by id.
- Last reading: the value or level, its date and its source.
```

Keep 12 to 15 rows that are as independent of one another as possible. Remove a row when it becomes too correlated
with another row or stops bearing on a briefing dimension, and record the removal in the change log.

## Specification standard

Any checkable statement in these files (a claim's "would be wrong if", a row's measure, a regime's criteria) is
stated precisely enough that a prediction-market site could settle it: named actors or instruments, a threshold,
a date, and a resolution source.

## Source types

Every fact carries one of these source types:

- primary: filings, company releases, official statistics, regulator or central-bank documents, papers and
  preprints read directly.
- wire or trade: wire services, and established general, financial or trade press.
- analyst: sell-side, rating-agency or research-firm notes, read directly or as quoted.
- secondhand: any of the above known only through another outlet, a digest, or social media.

Digests and newsletters are for finding stories. Cite the original article they point to, or mark the fact
secondhand.
