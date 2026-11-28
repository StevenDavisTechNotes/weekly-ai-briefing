# Phase C: Model update

Start a fresh conversation for this phase.

Read first:

- `src/weekly_ai_briefing/prompts/shared/reader_and_dimensions.md`
- `state/README.md`, for the file formats and the specification standard
- `state/current_model.md`
- `state/state_table.md`
- `state/background.md`
- `state/runs/<date>/fact_sheet.md`
- `state/runs/<date>/verification.md`

Write:

- `state/runs/<date>/change_log.md`
- `state/current_model.md`, revised in place
- `state/state_table.md`, revised in place
- `state/background.md`, revised in place

## Starting point

This phase revises the model in place, so a second run must not apply this week's changes on top of the first.
Before reading the model, look for `state/runs/<date>/current_model_before.md`,
`state/runs/<date>/state_table_before.md` and `state/runs/<date>/background_before.md`:

- If they exist, this is a rerun. Read them in place of `state/current_model.md`, `state/state_table.md` and
  `state/background.md`, and ignore what those files now hold.
- If they do not, this is the first run. If you can write files, first copy each of the three state files to
  its `_before.md` name in `state/runs/<date>/`, unchanged, then revise from the copies.

Either way, write the revised files to `state/current_model.md`, `state/state_table.md` and
`state/background.md`.

Use only facts whose verdict is confirmed or corrected, with corrections applied. Unconfirmed facts may inform the
watching list but never a claim, a table reading or a figure.

Do not stop for the reader's review or approval after this phase; phase D follows without a pause. Still make the
change log readable on its own, since the reader may read it afterwards.

## Principles

- Inertia first. The model is meant to be stable. Most weeks, most claims hold; say so and move on. A week with no
  change to the model is a valid outcome.
- Rank by surprise times consequence, not by size. A loud development that changes nothing in the model is noise.
  A quiet one that shows a claim is wrong is signal.
- Second derivative. What matters most is a change in a trend: a new trend, an acceleration, a deceleration or a
  reversal. A level that continues an expected trend updates the table's latest shift but not the model.
- Persistence. A first-week surprise goes to the watching list. Promote it to a claim, or let it revise a claim,
  only when a second week of evidence or two independent sources support it.
- Qualification. A change to a claim, or a new claim, must change how the reader reasons across more than one
  dimension or decision, or explain earlier observations the old model could not. The next feature in a product
  lineage (which vendor leads, model tiers, version numbering) does not qualify by itself. "Benchmark scores
  depend heavily on the harness" is an example that qualified: it changed how every later benchmark is read.
- Modest complexity. Prefer revising or merging a claim to adding one. Keep at most 12 claims, 8 watching items
  and 15 table rows.

## Steps

0. Read the test calendar in `current_model.md`. Settle every entry due on or before this edition's date: a claim
   whose test was met is refuted (revise or retire it); a claim whose deadline passed with the test unmet is
   strengthened, and gets a new test with a later date; a watching item at its deadline is promoted or dropped.
   No entry may stay on the calendar past its date.
1. For each claim, decide: holds, strengthened, weakened, revised, or retired. Retire a claim that was refuted, that
   another claim absorbed, or that turned out to be churn.
2. For each watching item, decide: promote, keep, or drop. Drop items that saw no evidence for four weeks.
3. Add new watching items for this week's qualifying surprises.
4. For each table row, update latest shift, major trend, direction, regime and last reading from verified facts.
   Change a regime only when the row's written criteria for the new level are met. Add or remove rows only for
   the reasons in `state/README.md`.
5. Read the fact sheet's linked chains. A chain whose facts are verified may support a watching item or a claim
   revision; it counts as independent support only where its facts come from independent sources. A reading of
   an opaque market, such as private credit, may be inferred from verified market signals; mark it "inferred
   from" in the row's last reading and name the signals.
6. Maintain `state/background.md` to its format and qualification rule in `state/README.md`. Add a story when a
   verified fact turns out to be the next step of an earlier story the file lacks, with milestones from verified
   facts or from sources you name; update a story's "Now" line when this week moved it; retire a story that
   ended or that no claim, row or watching item rests on any longer. Record each change in the change log.
7. Rank this week's verified facts by surprise times consequence and pick the five that matter most for the
   Orientation. Prefer facts that moved the model or the table.

## Change log format

```markdown
# Change log

Edition: YYYY-MM-DD.

## Five signals

1. F-xx, with one sentence on why it ranks here: what was expected, what happened, what it changes.
(five entries, most significant first)

## Model changes

- M-xx Name: holds, strengthened, weakened, revised, or retired. One to three sentences on why, citing fact ids.
  For a revision, quote the old claim.
- New claim M-xx Name: the qualification reason, citing fact ids.

## Watching list changes

- Promoted, kept, dropped or added, with the reason.

## State table changes

- Row: the change and the fact ids behind it. Rows added or removed, with the reason.

## Tests coming due

Each calendar entry due within four weeks of this edition, with its date and whether this week's facts moved it.

## Background changes

- B-xx Name: added, updated or retired, with the reason and fact ids, or "none".

## Continuing shifts

The claims that continued or strengthened without revision, in one line each.
```

Then write the revised `current_model.md` and `state_table.md`, setting "As of" to this edition's date and keeping
the formats in `state/README.md`. Whenever you add a claim or change its "would be wrong if", update its "check
each week" line to name where a reading of the new test would appear. Keep the test calendar in step with every
change: add, re-date or remove entries, and keep it sorted soonest first.
