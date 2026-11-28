# Phase A: Research

Start a fresh conversation for this phase.

Read first:

- `src/weekly_ai_briefing/prompts/shared/reader_and_dimensions.md`
- `state/README.md`, for the file formats and source types
- `state/current_model.md`
- `state/state_table.md`
- `state/background.md`, if it exists: the earlier stories the model rests on
- `editions/<model>_version/<date>-<model>.md` for each model that has one this week, such as
  `editions/gemini_version/<date>-gemini.md` or `editions/muse_version/<date>-muse.md`: briefings other models wrote
  for the same week. They are comparative and not authoritative.

Write: `state/runs/<date>/fact_sheet.md`, where `<date>` is today's date (the publication date).

## Research window

Research the seven days before today. If run on 2026-10-24, the window is 2026-10-17 through 2026-10-23. Older
items may be used only as background and are marked as such.

Some weeks are quiet: the weeks of US Thanksgiving and from Christmas to New Year, and other weeks with major
market holidays or few scheduled releases. Expect fewer facts in those weeks, and do not pad toward the usual target.
Say in the research limits that the week was quiet and why.

## What to look for

Research has two jobs, and both matter.

1. Test the model. For every claim in `current_model.md` and every row in `state_table.md`, look for this week's
   evidence for and against it. Look hardest for evidence against: the model improves where reality shows its
   fault lines. Record "no material evidence" for a claim or row when you looked and found nothing.
   Open every source in each claim's "check each week" line and each row's measure directly, rather than relying
   on search to surface them, and say in the model check whether it showed a reading of the test.
2. Find surprises. Search each of the seven dimensions for developments that the current model did not expect.
   A surprise matters when it is unexpected and would change how the reader reasons or decides, not when it is
   loud. Corporate deal noise, routine partnerships, generic fundraising rounds and consensus rehash are not
   surprises.

Also check each item on the watching list, since a second week of evidence can promote it.

Read each story in `state/background.md` as a lead: when a development this week is the next step of one, say so
in the fact's "Bears on" field with the story's id, such as B-01. When a fact connects to an earlier story that
the file does not hold, say so in the research limits, so that phase C can consider adding it.

Look hardest at the entries in the test calendar of `current_model.md` that fall due within four weeks: open
every source in their "check each week" lines, and record a reading or "no material evidence" for each.

### Inferring what is not disclosed

Some markets the model depends on are opaque by design, chiefly the private credit behind AI infrastructure:
GPU-backed loans, data-center SPVs, neocloud facilities and the funds that hold them. Their covenant breaches,
waivers and marks are rarely disclosed, so a week with no reports is not evidence that nothing happened. Each week,
look for the published market signals that price them, and record each as an ordinary fact with its figures and
source:

- GPU rental-price indices and secondary prices for used accelerators, by generation.
- Spreads, new-issue terms and rating actions on public data-center and GPU asset-backed securities and CMBS, and
  rating-agency surveillance reports on them.
- Business development company filings: non-accruals, amendments, marks and payment-in-kind income on loans to
  AI infrastructure and data-center borrowers, and the BDCs' share prices against net asset value.
- Public neocloud and data-center operator filings: covenant amendments or waivers in 8-Ks and 10-Qs, liquidity,
  and the terms of new facilities.
- Disclosures by listed alternative asset managers and banks on AI infrastructure lending, back leverage and
  significant risk transfers.
- Secondary-market prices for private-credit fund interests.

When such a fact bears on the undisclosed market, fill its "Inference" field with what it suggests and why. An
inference is never written as a reported fact, rests only on the figures the fact records, and names its signal.

### Connecting across dimensions

A development can be invisible within each dimension and plain across them: an export rule (Economic Structural
Change) freezes financing for some data centers (Institutional Financial Services), which removes a resale market
that a chip's collateral value assumed (Enterprise AI Adoption). After the facts are gathered, look for chains of
facts from different dimensions that share one mechanism, actor or asset, and record each in the fact sheet's
"Linked chains" section. Then search once more for the link a chain is missing, and add what you find as a fact.

If other models' briefings for this week exist, use them only as a coverage check. List each development they
report that your search missed, then find the primary source for it and record it as a fact, or leave it out if no
source confirms it. Treat their figures, dates and characterizations as unverified leads, since they may be wrong.
Never cite those briefings, and do not adopt their analysis.

For every fact, classify the change it shows:

- new trend: something the model does not yet describe.
- acceleration or deceleration: an existing trend speeding up or slowing down.
- reversal: an existing trend changing direction.
- level only: the trend continues as expected; worth at most a line.

Before writing the fact sheet, check every label other than level only against the claim or row it bears on, and
relabel it level only unless one of these holds:

- new trend: no claim, row or watching item describes it. Example: the first lender to freeze loans because of who
  a data center's tenant is, when no claim covers financing by tenant.
- acceleration or deceleration: the rate has changed, not just the level, measured against the row's last reading
  or the claim's evidence. Example: a monthly price rise that doubles the previous month's rise.
- reversal: the direction has changed. Example: a price the state table shows rising that now falls.

A fact that merely adds another instance, a higher level or a larger amount on the same course is level only.
Likewise, do not call a refutation test "met" or "live" unless the fact meets that test's stated threshold.

## Sources

- Prefer primary sources. Read the filing, the release, the statistical table or the paper itself when you can,
  including lab research blogs and new papers for the AI Technology dimension.
- Read documents in full, not through search excerpts. Fetch and read the full text of every primary document a
  fact rests on, and of any article whose figures you record; excerpts lose the context, caveats and exact figures
  that the later phases need. Use excerpts only to find documents. When a document cannot be fetched, say so in
  the fact's "Read" field.
- Use digests and newsletters only to find stories; cite the article or document they point to.
- For what AI is doing to issuers' business models, search the week's SEC filings, earnings-call transcripts and
  shareholder letters directly; these primary disclosures carry measured effects that press coverage often skips.
- Aim for a mix of source types, and let no single source supply more than about a tenth of the facts.
- Record a number only with its exact value, unit, date and the source that states it. Never compute a number
  and present it as reported; if you derive one, mark it "derived" and show the arithmetic.
- Note when a source could not be read, when a claim rests on one source only, and when sources disagree.
- If you can run local commands and a PDF, Word or other document will not read in full through web fetch,
  download it into `source_document_cache/<date>/` and convert it locally, with `uv run markitdown <file>` or
  with pypdf (both are in this repository's environment). Keep any script you write in a separate folder.
- For an arXiv paper, read the full text, not the abstract page: the HTML version at `arxiv.org/html/<id>` when
  it exists, otherwise the PDF. Mark the fact "excerpt only" if you could read only the abstract.
- If you can write local files, keep a copy of every source a fact rests on, as you read it, in
  `source_document_cache/<date>/`: one markdown file per source, named from the site and a few words of the title,
  that starts with the URL and the time you fetched it, followed by the text you read. Verification uses the copy
  to tell a page that changed after you read it from a misreading. The folder is not committed and is deleted
  after the edition is published, so it is never a source to cite.

## Fact sheet format

```markdown
# Fact sheet

Edition: YYYY-MM-DD. Window: YYYY-MM-DD to YYYY-MM-DD.

## Facts

### F-01 [Dimension] Short label

- Fact: one or two sentences stating what happened, with its date.
- Figures: each number with unit and date, or "none".
- Source: outlet or author, title, date, and URL.
- Source type: primary, wire or trade, analyst, or secondhand.
- Read: full document, or excerpt only, with the reason the full document could not be read; the time fetched;
  and the cached copy's file name, when there is one.
- Bears on: model claim ids, state-table rows, watching items, or "new".
- Change type: new trend, acceleration, deceleration, reversal, or level only.
- Expected vs. happened: one sentence on what the model would have predicted and how this differs.
- Consequence: one sentence on what it would change for the reader if it holds.
- Inference: for a market signal read as evidence about an undisclosed market, one sentence on what it suggests
  and why, marked "inferred"; otherwise "none".

## Model check

One line per claim and per row: the fact ids for and against, or "no material evidence".

## Linked chains

- F-xx, F-yy, F-zz: the shared mechanism, actor or asset in one sentence, and the missing link that would confirm
  the chain, or "none found".

## Research limits

Sources that could not be read, single-source claims, disagreements between sources, dimensions that stopped short
of their floor, and expected developments looked for and not found.
```

In the heading, `[Dimension]` is one of `[AI Technology]`, `[Quantum]`, `[Enterprise]`, `[Physical AI]`,
`[Human and Machine Agency]`, `[Economic]` or `[Financial Services]`, for the dimension the fact mainly serves.

Number facts F-01, F-02 and so on in the order found. Aim for 75 to 100 facts, with at least 8 in each of the seven
dimensions, so that the extra search goes to the thin dimensions rather than the busy ones. Do not reach a number
with filler: a dimension that cannot reach its floor without routine deals, level-only updates or consensus rehash
stops short, and the research limits say so. Completeness on the model check matters more than volume. Do not write analysis or prose for the briefing in this phase.

## Splitting the work by dimension

If you can hand work to parallel workers, such as subagents, split the research by dimension: one worker for each
of the seven dimensions, all running at once, and you as the lead.

- Give each worker this prompt, the date, the files listed above except other models' briefings, and its
  dimension. Each worker researches only its own dimension, and tests the claims, rows and watching items that
  bear on it (by a claim's "Dimensions" field, or by the claims a row informs). An item that bears on several
  dimensions is tested by each of them; the lead merges the results.
- A worker returns, in its reply, its facts in the fact sheet format, numbered D<n>-01, D<n>-02 and so on, where
  `<n>` is its dimension's number; a model-check line for each item it tested; and its research limits. It writes no
  file.
- The lead then merges the drafts into the one fact sheet: removes duplicate facts, keeping the one with the
  better source; renumbers them F-01, F-02 and so on; combines the model-check lines so that every claim, row and
  watching item has one line; and combines the research limits. The lead runs the coverage check against other
  models' briefings itself, on the merged facts, and runs the change-type check on every merged fact. The lead
  also looks for linked chains across the workers' dimensions, since no single worker can see them.

If you cannot hand work to parallel workers, do the research yourself, one dimension after another.
