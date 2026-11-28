# Verification

Edition: 2026-11-28.

Method: every cited source was re-opened on 2026-11-28 with a page-reading tool (WebFetch), which returns page text
through a summarizing model, and checked against each figure, unit and date in the fact sheet. The DOL claims PDF
was read with pypdf. arXiv items were re-read at the abstract page, as in phase A. The Bank of England Financial
Stability Report was again read only in its first 100,000 of about 970,000 characters. Second sources were searched
for the figures that bear most on the model (F-01, F-04, F-05, F-13, F-18).

## Verdicts

- F-01: confirmed. Source re-read: Nvidia 8-K press release, 2026-11-23 (unanimous vote; reinstated as President
  and CEO and as a board member; consulted senior US officials; "poses no national security risk"; independent-director
  investigation "will proceed to conclusion"; new Chief Compliance Officer reporting to the Nominating and Corporate
  Governance Committee); TechCrunch, 2026-11-24 (Nvidia up more than 30% on Monday, down more than 7% by midday
  Tuesday); Fortune, 2026-11-26 (Reuters report that Huang's support for open-weight AI helped persuade Trump and
  Vance to push for his return; secondhand). No independent closing-price source for 2026-11-23 was found.
- F-02: confirmed. Source re-read: TechCrunch, 2026-11-24 ($83 offer, $111.50 debut, $76 by midday Tuesday, nearly
  12% below Monday's close); Reuters via Kitco, 2026-11-25 (closed Tuesday at $81.90, slipped 2.1% in the 11:28 a.m.
  snapshot). TechCrunch calls $111.50 the "debut price" rather than the open. The 2026-11-18 pricing date was not
  re-checked.
- F-03: confirmed. Source re-read: Reuters via Kitco, 2026-11-25. All index, sector, stock and new-high/new-low
  figures match as of 11:28 a.m. ET; Dell -7% after raising forecasts. The article also has HP +11.7%, not used in
  the fact sheet. No closing levels in the source.
- F-04: confirmed, with caveat. Source re-read: Reuters via Kitco, 2026-11-25 (14 partners; China proposed 20%
  excess-capacity levy on top of roughly 25% first-term duties). A search found no USTR or Federal Register notice;
  the Section 301 excess-capacity investigations opened 2026-03-11 cover 16 economies, and a June 2026 forced-labor
  proposal had a 10% tier on 14 economies, so the "14" may be conflated. Treat as single-source and unconfirmed by
  the government.
- F-05: corrected. Source re-read: Asia Times, 2026-11-27; The Standard, 2026-11-18. The loan figures ($6.6 billion
  Bridge Data Centres, Bain-owned, Malaysia; $300 million GMI Cloud, Thailand; DayOne listing shelved; US$49 billion
  Asian AI debt market; $480 million Aolani Cloud loan, DBS lead, five lenders) all match. Corrections: Asia Times
  dates the FT and Bloomberg reports only as "Thursday" and "Wednesday"; 2026-11-26 and 2026-11-25 are inferences.
  The Nvidia instruction to Dell and Supermicro to halt shipments must be stated as unconfirmed: the article says
  neither the companies nor BIS confirmed it, and a search found no other report.
- F-06: confirmed. Source re-read: European Commission news page, 2026-11-25. The three priorities, PQC transition,
  Sovereign Tech Equity Fund, Quantum Strategy Board and European Quantum Alliance match. The page also restates a
  2030 goal for Europe to be a global quantum leader; no PQC dates or fund size.
- F-07: confirmed. Source re-read: Fortune, 2026-11-26. 56% of Vercel gateway tokens to open weights in August 2026
  against 7% a year earlier (Fortune notes the linked report is labelled a September 2026 index); Pinterest "over 90%
  cost reduction" (APAC VP Damian Kim, Qwen); "about eight months behind" (Olaf Groth quoting US government
  evaluators); Cursor Composer built on Kimi. The Vercel figure remains secondhand through Fortune.
- F-08: confirmed. Source re-read: Fortune, 2026-11-26 (Reuters 2026-11-18 on disclosure; Moolenaar report
  2026-11-20 on proxy networks and fraudulent accounts; CNBC 2026-11-20 on Cursor). Secondhand, as labelled.
- F-09: confirmed. Source re-read: LSEG Analytics, 2026-11-24. Every figure matches, including FCF +$209 billion
  (2025) to -$189 billion (2027), $279.0 billion vs $108.1 billion bonds, about 15% of IG (SIFMA to end-Q3), WACC
  about 7% to 9%, the ROIC-WACC spreads and the short-interest figures.
- F-10: confirmed. Source re-read: LSEG Analytics, 2026-11-24. ABS spreads (labelled "A-" in the source) about 192 bp
  to about 274 bp; CMBS AAA market 142.5 bp to 174.8 bp (26 deals); SEC Section 3(a)(79) ruling as described, with no
  date or citation. The new-issue inconsistency is real: the text says 42 bp "from the second quarter of 2026 to the
  third quarter of 2026", the table shows about 140 to about 188 bp. Neither new-issue figure should be used.
- F-11: confirmed. Source re-read: BIS speech page, posted 2026-11-26; text dated 2026-11-17, The Clearing House
  Annual Conference, New York. Quote matches; no policy proposals.
- F-12: confirmed. Source re-read: Quantum Computing Report, 2026-11-25. Every figure matches.
- F-13: corrected. The Quantum Computing Report summary does say "as few as 10,000 physical qubits" for RSA-2048,
  but the underlying Oratomic paper (Cain, Xu, ... Preskill, Bluvstein, "Shor's algorithm is possible with as few as
  10,000 reconfigurable atomic qubits," arXiv:2603.28627, 2026-03-30) gives 10,000 as the headline minimum for Shor's
  algorithm at cryptographic scale, about 26,000 qubits for a P-256 discrete log in a few days, and RSA-2048 at "one
  to two orders of magnitude longer" than P-256; secondary coverage (Physics World, Live Science) puts the RSA-2048
  constructions at about 11,000 to 14,000 qubits with very long runtimes. Correct version: an estimate from March
  2026 (background, not new this week), as few as 10,000 reconfigurable atomic qubits for cryptographically relevant
  Shor, with RSA-2048 needing more qubits or far longer runtime; not yet peer reviewed.
- F-14: confirmed. Source re-read: UK Finance blog, 2026-11-26 (Thibault Pele, Worldline). Quote, partners, AP2,
  EMVCo, upstream SCA, unsourced "industry projections" and the disclaimer all match.
- F-15: confirmed. Source re-read: Computerworld (opinion), Jonny Evans, 2026-11-25. Beta; Mac, and per the author
  Windows; three permission tiers as described (examples of controlled permissions also include always-on-top
  windows); sandbox advice matches. No mention of Anthropic reviewing apps.
- F-16: confirmed. Source re-read: Lean FRO and Mathlib joint statement, 2026-11-21 ("full confidence"; the four
  checks; 17 million lines); Scientific American, 2026-11-20, updated 2026-11-21 (made "working with Claude";
  Sutherland independently compiled it). The Lean statement itself does not mention Claude or Sutherland; those
  points come from Scientific American.
- F-17: confirmed. Source re-read: Wikipedia, as edited by 2026-11-28. All line counts and dates match. Note: the
  article says "as of November 2026" no complete human-readable account exists, and that Michael Rubinstein has
  released two expository papers (an outline and a guide) that fall short of one. Secondhand, as labelled.
- F-18: corrected. Source re-read: Terence Tao, 2026-11-20. Tao lists a Lean formalization for the unforced
  Navier-Stokes result as well as for Euler, and says more work is needed for a professionally written proof; he does
  not say its Lean verification is unfinished. The "Lean verification has not finished" statement found by search is
  Buckmaster's September 2026 statement about a hypo-dissipative Navier-Stokes extension, not this result. Correct
  version: drop the Buckmaster clause; the Navier-Stokes claim is technically human-readable, has a Lean
  formalization whose completion status Tao does not state, and lacks a professional write-up.
- F-19: confirmed. Source re-read: OpenAI, Jakub Pachocki, 2026-11-22. Values 0.99, 0.91, below 0.8, about 0.76 and
  about 0.68 to 0.7 match; acceleration mostly from long-term research and compute, a smaller part from automation
  (no numerical shares); cross-lab comparison called a challenge.
- F-20: confirmed. Source re-read: OpenAI, 2026-11-22. Proposed perplexity-based limit until a monitoring or
  understanding milestone (example: successor to chain-of-thought monitors); expects further degradation of alignment
  auditing and rising evaluation and training awareness.
- F-21: confirmed. Source re-read: OpenAI, 2026-11-23. Open source (BSD 2-Clause; BPF programs BSD/GPL), human
  approval, signed and verified shields, TPM record. The test shield added an input check to Java's Base64 decoder and
  blocked a Java4Shell exploit attempt on running Elasticsearch.
- F-22: confirmed. Source re-read: Google DeepMind, 2026-11-23. All factors and qubit counts match; arXiv:2611.09822;
  no mention of cryptography.
- F-23: corrected. Source re-read: NoCode MBA tracker, updated 2026-11-27. Inkling 2 Mini (2026-11-20, open-weight
  looped transformer, middle layers three times per token) and Mellum2.1 Instruct (2026-11-25, open-weight, no chain
  of thought) match. The tracker has no Artificial Analysis figure; drop "Artificial Analysis index 20" (search
  excerpt only, not in the cited source).
- F-24: confirmed. Source re-read: BEA, 2026-11-25. 4.3% vs 3.4%; revision led by intellectual property products,
  notably software (the revision primarily reflects investment and consumer spending); gross domestic purchases prices
  2.7%, down 0.3 point; PCE 2.1%, core 2.5%; profits +$206.0 billion vs +$384.0 billion.
- F-25: confirmed. Source re-read: BEA, 2026-11-25. All figures match.
- F-26: confirmed. Source re-read: TrendForce, 2026-11-25. All figures and timing match.
- F-27: confirmed. Source re-read: TrendForce, 2026-11-27. Base case declines across all categories from 1Q28; bear
  case from 4Q27; causes as listed, plus Chinese CSP cuts and consumer-electronics pressure; no percentages.
- F-28: confirmed. Source re-read: Strisker digest, 2026-11-27. Figures match; the Coweta ballot also covers banning
  crypto mining, and the rezoning being repealed was approved April 7. Secondhand, as labelled.
- F-29: confirmed. Source re-read: Dell 8-K Exhibit 99.1, 2026-11-24 (quarter ended 2026-10-30). Every figure matches;
  Q4 guide $56.3 billion is up 69%. The 7% share fall on 2026-11-25 is confirmed by Reuters via Kitco.
- F-30: confirmed. Source re-read: HP 8-K Exhibit 99.1, 2026-11-24. Every figure matches; the workforce wording refers
  to the fiscal 2026 plan's efficiencies "primarily through artificial intelligence adoption and enablement."
- F-31: confirmed. Source re-read: Workday 8-K Exhibit 99.1, 2026-11-24. Every figure matches; restructuring was
  primarily workforce reductions, also facility closures.
- F-32: confirmed. Source re-read: Phys.org, 2026-11-25. Figures match; atoms are ultracold rubidium. Institution not
  named.
- F-33: confirmed. Source re-read: Bank of England FSR, 2026-11-26 (first 100,000 characters: "an orderly transition
  to quantum-resistant cryptography a priority"); The Quantum Insider, 2026-11-27 (immediate priority; systemic firms
  to move ahead of NCSC milestones of 2028, 2031 and 2035 with no new dates; single-provider warning; CMORG method;
  Australia end-2030, India end-2028). The "ahead of NCSC milestones" point is still known only through The Quantum
  Insider.
- F-34: confirmed. Source re-read: Bank of England FSR, 2026-11-26 (excerpt). Wording matches, including spreads
  widening sharply "for some lower-quality AI-related borrowers" (and US CCC debt), the post-midterm fall, hedge-fund
  deleveraging and leveraged ETFs, and hyperscaler issuance above $305 billion, about 8% of global IG issuance.
- F-35: corrected. The BoE wording is "may be contributing to upward pressure on global real interest rates", not
  "may be adding". The LSEG figures the fact sheet left unrecorded are in the LSEG piece: US deficit about $2 trillion,
  about 6% of GDP (CBO, October 2026) and household saving ratio 3.8% (attributed to BEA, October 2026); BEA's own
  October saving rate is 4.1% (F-25), so the BEA figure should be used.
- F-36: confirmed. Source re-read: Bank of England FSR, 2026-11-26 (excerpt). Matches in substance: growth in agents
  and open-weight models, "challenges in aligning and controlling both individual agents and multi-agent dynamics",
  safeguards "more easily disabled or removed", reliance on common third-party providers. Use the BoE's wording on
  control challenges rather than "incidents show".
- F-37: confirmed. Source re-read: Symbotic 8-K Exhibit 99.1, 2026-11-23. Release text gives rounded figures ($2.8
  billion, $133 million, $354 million, $778 million) consistent with the fact sheet's; first full year of GAAP
  profitability; no backlog figure.
- F-38: confirmed. Source re-read: Google DeepMind, 2026-11-10. Figures match; also 20-30% faster completion.
- F-39: confirmed. Source re-read: OpenAI Health Privacy Notice, updated 2026-11-19; and now in full the July launch
  post, dated 2026-07-23, which says connected records and conversations that use them are not used to train
  foundation models "regardless of the model-training setting". The reversal is confirmed from both primary pages.
- F-40: confirmed. Source re-read: Education Week, 2026-11-10. Figures match.
- F-41: confirmed. Source re-read: DOL release PDF, 2026-11-25 (pypdf). 189,000 (-13,000), 4-week average 196,000;
  insured unemployment 1,697,000 (-95,000), rate 1.1%.
- F-42: confirmed. Source re-read: HumanForward, re-run 2026-11-24. All figures match; the original DTC figure was 14
  of 54 readable sites.
- F-43: confirmed. Source re-read: Anthropic model-deprecations page, 2026-11-28. Sonnet 4.5 deprecated 2026-09-30,
  retires 2026-11-30 (Sonnet 5.5); Opus 4.5 deprecated 2026-11-23, retires 2027-01-22 (Opus 5.5); 404
  not_found_error; at least 60 days' notice; Bedrock and Google-managed Google Cloud set their own schedules.
- F-44: corrected. Source re-read: Anthropic, 2026-11-20. The 1,127,000,000 Class A shares include the fully exercised
  147,000,000-share option; it is not 147,000,000 more. Anthropic sold 1,103,351,354 and selling stockholders
  23,648,646. Proceeds figures ($93.5 billion, $91.6 billion to Anthropic, $26.0 billion placement, $119.5 billion
  combined) match.
- F-45: confirmed. Source re-read: OpenAI, 2026-11-24. Figures match. Clarifications: the 66-70% range is antibody
  fragments (66%) and VHH loops (70%); the TM-score of 0.38 is OpenAI's latest internal model (GPT-6.2 scored 0.26)
  against 0.93 for ESMFold2; the filtering models were Boltz-2, OpenDDE and ESMFold2. No access restriction stated.
- F-46: confirmed. Source re-read: arXiv:2611.32946 abstract, 2026-11-24 (22 authors led by Vincent Koc). All figures
  match.
- F-47: confirmed. Source re-read: arXiv:2611.27112 abstract, 2026-11-20. Figures match; the 5 boundary attempts were
  all by OpenCode with DeepSeek, and the 7 of 45 ungated runs were under the neutral file.
- F-48: confirmed. Source re-read: arXiv:2611.34875 abstract, 2026-11-25. Figures match. Context the fact sheet omits:
  the 11% figure is for SWE-bench Verified, and agent code is about as necessary as developers' code (mean necessity
  0.887 vs 0.864).
- F-49: confirmed. Source re-read: arXiv:2611.31460 abstract, 2026-11-23 (short paper for the AGENT 2027 workshop at
  ICSE 2027). Figures match.
- F-50: confirmed. Source re-read: arXiv:2611.33639 abstract, 2026-11-25. Figures match (Opus medium vs high
  difference 0.018, 95% CI -0.065 to 0.108; 20% cheaper, short of a preregistered 30%).
- F-51: confirmed. Source re-read: arXiv:2611.34934 abstract, 2026-11-25. Figures match; attacks were developed against
  proxy monitors and tested on a held-out GPT-5.4 monitor.
- F-52: confirmed. Source re-read: arXiv:2611.34758 abstract, 2026-11-25. Best method ΔW J++; output penalty defeats
  activation and output methods, permutation or residual-reading-layer training defeats weight methods.
- F-53: confirmed. Source re-read: arXiv:2611.33741 abstract, 2026-11-25. Figures match; no commercial API audited.
- F-54: confirmed. Source re-read: US Treasury daily par yield curve, November 2026. Every 2-, 10- and 30-year value
  matches; no row for 2026-11-26.
- F-55: confirmed. Source re-read: The Armchair Trader, 2026-11-27. Figures match and none is attributed to a named
  source; secondhand, as labelled.
- F-56: corrected. Source re-read: 24/7 Wall St., 2026-11-19, now in full. Rating, outlook and timing match, but the
  article paraphrases Moody's SVP Raj Joshi and gives no verbatim quote; the quoted phrase "has introduced uncertainty
  about the company's business strategy and financial policies" must not be presented as Moody's words. Secondhand.
- F-57: confirmed. Source re-read: arXiv:2610.28683 abstract, 2026-10-19 (Bashi AI). Figures match; the source
  describes the 263 as non-bot merges into the main branch, not "gated-phase" merges.
- F-58: corrected. Source re-read: Forkast, 2026-10-02. The article dates the agentic trading accounts launch to
  Robinhood's HOOD Summit on 2026-09-29; May 2026 was when Robinhood opened to agents. Other figures (over 150,000
  customers, nearly 30 million tool interactions a day, Loops, risk on the user, no volume) match.

Totals: 50 confirmed, 8 corrected (F-05, F-13, F-18, F-23, F-35, F-44, F-56, F-58), 0 unconfirmed, 0 dropped.
Elements to be stated as unconfirmed within otherwise confirmed or corrected facts: the Nvidia shipment halt (F-05),
the government basis for the tariff proposal (F-04), and the BoE "ahead of NCSC milestones" wording (F-33).

## Source mix

Counts by main source type (58 facts; where a fact has more than one type, the type of its principal source):

- primary: 37 (F-01, F-06, F-11, F-14, F-16, F-18 to F-22, F-24, F-25, F-29 to F-31, F-33 to F-39, F-41 to F-54,
  F-57). Of these, 9 are arXiv preprints read at the abstract only (F-46 to F-53, F-57).
- wire or trade: 9 (F-02, F-03, F-04, F-07, F-12, F-15, F-32, F-40, F-58).
- analyst: 4 (F-09, F-10, F-26, F-27).
- secondhand: 8 (F-05, F-08, F-13, F-17, F-23, F-28, F-55, F-56).

No single document supplies more than about a tenth of the facts. The largest are the Bank of England FSR (4 facts,
F-33 to F-36, about 7%, read only in its first tenth), Reuters via Kitco (3, plus a supporting role in F-29), LSEG (3)
and the Fortune open-weight article (2, plus the Reuters report in F-01). By publisher, OpenAI supplies 5 (F-19, F-20,
F-21, F-39, F-45), about 9%, and an OpenAI-built monitor is the subject of F-51; arXiv as a platform supplies 9
(about 16%) but from nine separate author groups.

## Flags

Mislabelled change types (level only, or otherwise mislabelled):

- F-02 (reversal): the shares closed 1.3% below offer after four sessions; that is a level reading, not yet a
  reversal of a trend. The fact sheet's consequence that the M-08 test "is now live" overstates it: the threshold is
  a close at or below $66.40.
- F-03 (acceleration): a single intraday selloff is level only unless set against prior selloffs.
- F-04 (acceleration): a single-source proposal with no government notice; level only at most.
- F-15 (new trend), F-17 (new trend), F-45 (acceleration), F-51 (acceleration): each is a single release or paper;
  level only.
- F-46 (deceleration): one paper against M-01 is evidence against a claim, not a deceleration of a measured row.
- F-58 (new trend): background from October; its launch date is 2026-09-29, not May.

Other points phase C should know:

- F-13 is background (a March 2026 preprint) and its RSA-2048 figure was misstated in the summary; it should not be
  used to argue that disallowance dates may move forward this week.
- F-18: the "Lean verification unfinished" claim about the Navier-Stokes result was not supported; it came from a
  September statement about a different result.
- F-54: the fact sheet's consequence says the 2-year fell 22 bp "in a week"; the fall from 4.83% to 4.61% runs from
  2026-11-16 to 2026-11-25, and no futures reading supports "pricing less tightening".
- F-09 vs F-34: hyperscaler issuance is about 15% of US IG issuance to end-Q3 (LSEG, SIFMA) and about 8% of global IG
  issuance for 2026 (BoE); these use different denominators and are not in conflict.
- F-35: LSEG's 3.8% saving ratio conflicts with BEA's 4.1% for October (F-25); use BEA.
- F-10: neither CMBS AAA new-issue widening figure (42 bp or about 48 bp) should be used.

Model claims or watch items the research did not check (no evidence, or no test reading found in the window):

- M-02 refutation condition: no lab monitor-coverage or evaluation-awareness disclosure found.
- M-04 refutation condition: no update on patching of OpenAI's 948 kernel flaws.
- M-05 refutation condition: no new Ramp AI Index in the window.
- M-06 refutation condition: no search reported for changes in the four large US banks' agent stance beyond "none
  found".
- M-08 refutation condition: CoreWeave 2031 bond and Oracle CDS levels not found.
- M-09 refutation condition: no Bernstein, Goldman Sachs or Data Center Watch cancellation tally; no Nvidia or AMD
  export-attributed revenue decline.
- M-10 refutation condition: no certification of a learned policy as final authority found.
- M-12: only OpenAI items bear on it; no Anthropic, Google DeepMind, xAI or Meta release page was checked for stated
  capability limits.
- Rows with no material evidence: power capacity price; entry-level technical hiring; humanoid deployment (background
  only).
- W-02, W-07 and W-08: no material evidence.
- W-05: no material evidence, and its stated deadline was this edition (2026-11-28), so phase C must decide whether to
  drop it.
- W-09: no new filings or rulings; only BoE supervisory attention (F-36).
