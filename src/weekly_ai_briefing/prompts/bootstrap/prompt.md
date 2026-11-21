# Bootstrap: infer the current model from past editions

Run once, in a fresh conversation, to create the first `state/current_model.md` and `state/state_table.md`. Rerun
only to rebuild the state from scratch.

Read first:

- `src/weekly_ai_briefing/prompts/shared/reader_and_dimensions.md`
- `state/README.md`, for the file formats, the specification standard and the source types
- `src/weekly_ai_briefing/prompts/C_model_update/prompt.md`, for the principles the weekly model update follows
- Every edition in `editions/markdown_format/`, in date order, in full, including the YAML indicator ledger at the
  end of each

Write:

- `state/current_model.md`
- `state/state_table.md`
- `state/runs/<date>/bootstrap_notes.md`, where `<date>` is the publication date of the latest edition

Do not research on the web. The editions are the only input: the task is to infer the terminal state of the
mental model that their narrative built, as of the latest edition.

## How to infer the model

The editions record a sequence of "mental model shifts", each revising the last. Many of those shifts did not
qualify as fundamental: some were the next feature in a product lineage, some were reversed a week later, and some
restated an earlier shift in new words. Read the sequence as a historian would, and keep what survived.

- Apply the qualification test from the phase C prompt. A claim belongs in the model only if it changes how the
  reader reasons across more than one dimension or decision, or explains observations an older model could not.
  "Benchmark scores depend heavily on the harness" is an example that qualifies. A sequence such as "which lab is
  best", then "thinking models", then "tiered models", then "version identity" is an example of lineage that does
  not, unless a durable principle sits underneath it; if one does, state the principle.
- Prefer the latest form of a claim that was sharpened over several weeks, and merge claims that say the same
  thing.
- Mark a claim firm when several editions supported it with independent evidence, and provisional when it rests on
  one or two weeks.
- Keep at most 12 claims, covering the seven dimensions in proportion to what the editions actually established.
  A dimension with no durable claim gets none.
- Put recent surprises that have not yet shown persistence on the watching list, at most 8.
- Write each claim's "would be wrong if" to the specification standard. The open indicators in the latest ledger
  are useful raw material, but do not carry the ledger over.

## How to build the state table

- Choose 12 to 15 rows that are as independent of one another as possible and that the model's claims depend on.
  Examples the reader suggested: Nvidia's share of the AI accelerator market; the
  sovereign yield curve at two to five informative tenors (such as the US Treasury 2-, 10- and 30-year yields, with
  euro, UK or Asian sovereign curves where they help the exposition); the effectiveness of anti-data-center activism. Use them if the editions support them, and
  choose others where the editions point to a better variable.
- For each row, write the measure, a regime scale with written criteria for each level where the row is
  qualitative, and the claims it informs. An example of a regime scale, for memory makers' capacity: aggressive
  growth, deliberate growth, organic growth, deliberate contraction, defensive contraction.
- Fill latest shift, major trend, direction, regime and last reading from the editions. Every figure in "last
  reading" must be stated as reported in a named edition, with the source that edition cited, and marked "not
  re-verified". Use fewer figures rather than uncertain ones.
- Set "Introduced" to the edition in which the editions first tracked the topic.
- Consider every dimension and subdimension in the shared reader file, including those added after the editions
  were written (such as issuers' business models, agent ecosystems, trust and the information ecosystem, and
  healthcare). Give one a row or a watching item only where the editions contain evidence for it; otherwise list it
  in the notes as a gap for the first weekly run to fill.

## Bootstrap notes

In `bootstrap_notes.md`, for the reader's review:

- For each claim: the editions it draws on, and the earlier shifts it replaces or merges.
- The shifts from the editions that you did not keep, each with one sentence on why: reversed, churn, absorbed, or
  too little evidence.
- For each table row: why it was chosen, and which other rows it is most correlated with.
- Any figure you could not state confidently, and anything the reader should check before the first weekly run.
