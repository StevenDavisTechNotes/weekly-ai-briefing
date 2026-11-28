# Phase B: Verification

Start a fresh conversation for this phase. Do not reuse the research conversation: the point of this phase is an
independent check by a reader who did not find the facts.

Read first:

- `src/weekly_ai_briefing/prompts/shared/reader_and_dimensions.md`
- `state/README.md`, for the source types
- `state/current_model.md`
- `state/runs/<date>/fact_sheet.md`

Write: `state/runs/<date>/verification.md`.

## What to do

For every fact in the fact sheet:

1. Open the cited source and read it again, in full rather than through search excerpts. Do not judge from memory
   or from the fact sheet's wording.
   If you can run local commands and a PDF, Word or other document will not read in full through web fetch,
   download it into its own new folder and convert it locally, with `uv run markitdown <file>` or with pypdf (both are
   in this repository's environment). Keep any script you write in a separate folder.
   For an arXiv paper, read the full text at `arxiv.org/html/<id>` when it exists, otherwise the PDF, not just the
   abstract page.
2. Check that the source says what the fact says, including every figure, unit and date.
   If it does not, and the fact's "Read" field names a cached copy in `source_document_cache/<date>/`, read that
   copy too, and say in the verdict whether the page changed after research read it or research misread it.
   Always judge from the live source first; the copy only explains a difference.
3. Check that the source type is right. A fact known only through a digest, a re-report or social media is
   secondhand, whatever outlet it names.
4. Where a figure matters to the model, look for a second, independent source or the primary document.
5. Give one verdict:
   - confirmed: the source supports the fact as written.
   - corrected: the source supports a corrected version; give the correction.
   - unconfirmed: the source could not be read, or it does not clearly support the fact. The fact may be
     mentioned only with that caveat and its figures may not be used.
   - dropped: the source contradicts the fact, or the fact is noise under the research rules.

Then check the fact sheet as a whole:

- Source mix: count facts by source type, and name any single source that supplies more than about a tenth of
  them.
- Change types: flag any fact labelled as a new trend, acceleration or reversal that is really level only.
- Model check: flag any claim or row in the current model that the research did not check.

## Verification file format

```markdown
# Verification

Edition: YYYY-MM-DD.

## Verdicts

- F-01: confirmed. Source re-read: outlet, date. Note, if any.
- F-02: corrected. Figure is X, not Y, per outlet, date.
- F-03: unconfirmed. Source could not be read; only a digest carried it.
- F-04: dropped. Reason.

## Source mix

Counts by source type, and any source above about a tenth of facts.

## Flags

Mislabelled change types, unchecked model claims or rows, and anything else phase C should know.
```

Do not add new facts, write analysis, or edit the fact sheet.
