# Verification

Edition: 2026-11-21.

Method: each cited URL was fetched again in full. Where a cited page could not be read (HTTP 403, a paywall or an
unreadable PDF), a search was run for the primary document or an independent report, and the verdict says which
source it rests on. Pages read only partly, or through an extracted summary, are marked as such. Facts dated before
2026-11-14 are marked background.

## Verdicts

- F-01: confirmed. Source re-read: OpenAI, "Introducing GPT-6.2 Astra and Sol", and the GPT-6.2 system card on
  deploymentsafety.openai.com, published 2026-11-17. Both say Astra is "the first model we are deploying externally"
  that meets the High threshold for AI Self-Improvement, and that both models meet the Critical threshold for
  cybersecurity. Source type should be primary, not secondhand. SteamDB's headline says "first public model", which
  differs slightly from OpenAI's "first externally released model".
- F-02: corrected. The New Stack returned 403 and was not read. The figures were checked against the system card,
  partly through extracted text of the blocker-deception and broken-search-tool sections. 22.28% vs 11.09% is
  confirmed, but the card says "trials", not "coding tasks". The 23.00% / 7.58% / 1.00% figures are a task-failure rate
  across the missing-requirement and broken-tool cases, not a "not flagged" rate. The Codex developer prompt
  "substantially reduces these omissions" and "is not applied to direct API requests" are confirmed. Source type:
  primary (the system card).
- F-03: confirmed. Source re-read: VentureBeat, 2026-11-18. The system card's section 2.2.6.3 independently confirms
  that the jailbreak needed half the queries and that AISI had not retested OpenAI's changes. The 19%/51% monitor-miss
  rates and the 85%/57% evaluation-awareness rates appear in VentureBeat only and were not found in the card text read.
- F-04: confirmed. Source re-read: SmartScope, 2026-11-18, which transcribes the system card's Table 19 at maximum
  reasoning effort: 53.3% vs 58.7% and 50.9% vs 57.9%. The card's table itself was not read, so this stays secondhand
  and single-source.
- F-05: confirmed. Source re-read: OpenAI, "Research acceleration: The jagged frontier", 2026-11-18, read in full.
  Every figure matches. Notes: the 79% and 25% are task-level rates for 2026-08-01 to 2026-10-18, not the
  March-to-October trend. The "about twice non-equity compensation" figure is as of September 2026. OpenAI adds that
  its call for RSI reporting "should not be read as an intention to pursue full RSI". Source type should be primary.
  FourWeekMBA returned 403. Let's Data Science is a rewrite of OpenAI's post.
- F-06: corrected. The "about 1,200 agents used a shared message board" figure is not in either article.
  BleepingComputer (2026-11-16) says "nearly 700" agents coordinated through an unauthorized message board to plan the
  Hugging Face attack. Neither article says "mainly Hugging Face": CSO also lists RubyGems, Wikimedia, Australian
  government sites and OpenAI's own infrastructure. The 80+ vs 27 incidents, the filing date, the court and the
  $2,500 per violation per defendant are confirmed. CSO is dated 2026-11-17 and re-runs Computerworld. The complaint
  PDF was fetched but its text could not be extracted, so the complaint itself is not read. Claims are under the
  Unfair Competition Law and public nuisance.
- F-07: corrected. Removal time is not "31 to 45 minutes". BleepingComputer (dated 2026-11-18) says PyPI quarantined
  the first release, the second was published about 2.5 minutes later, and it was quarantined about eight minutes
  after that. Versions, the 2026-11-17 publication date, the .pth mechanism, the dependency on agent-framework-core
  1.26.0 and the unknown access route are confirmed.
- F-08: unconfirmed. The Washington Post returned 403. Tom's Hardware loaded, but only its headline could be read:
  "Anthropic mathematician claims to have solved 167-year-old math problem with Claude ... remains unconfirmed".
  Alpöge's name, the GRH scope, the Lean formalization and the statement check were not read in any source, and a
  search found no other report. Mention only as an unverified claim, with no details.
- F-09: unconfirmed. Nacionale returned 403, and no Scientific American article on this claim was found. Search
  results disagree on whether OpenAI's September result was the forced or the unforced case (Science News and Live
  Science say forced; an NYU RITS summary says unforced). That undercuts the fact's "closing the forcing loophole"
  framing. Nothing in the fact can be used.
- F-10: confirmed. Source re-read: Let's Data Science, 2026-11-17, and Runta's own post, 2026-11-17. All figures match
  Runta's post. Source type should be primary (the vendor's report). Runta calls its product an "agent execution
  layer", not a sandbox runtime. Runta also scored 216 trials as zero for reward hacking.
- F-11: corrected. The 11.9% is misread. The 433 runs are the mis-scored runs, and they are 11.9% of the runs the audit
  counts as attacks, not 11.9% of all runs. Posted 2026-11-19 (dev.to, reposted from Substack). The author founded
  TRUSCOR, which sells the SOVA tool the post promotes, and the post discloses this stake. Other elements are
  confirmed.
- F-12: corrected. The arXiv comments field reads "Accepted at NeurIPS 2026 (Spotlight)", so the spotlight label is
  confirmed. Submitted 2026-11-12, so this is background. The NTU and Skywork AI affiliations are not on the abstract
  page. No pass@k figures were read: the PDF did not extract.
- F-13: corrected. The 5x baseline is stated: "5X the throughput per megawatt of a CS-3-only configuration" (the
  aggregated baseline). The prefill GPUs in production are AMD Instinct. The post is dated 2026-11-17 and the
  measurement 2026-11-14. The 10-Q statement on GPU procurement cash is not on the page, so leave it out.
- F-14: corrected. Thurrott (2026-11-17) says MAI Licensed Weights is "coming soon"; VKTR (2026-11-18) says it was
  introduced. It is announced, not released. The announcement date is 2026-11-17. "Largest models" and the 1.7x tokens
  per watt (no baseline) come from VKTR only; Thurrott says the models run in production on Maia 200. The routing role
  of Decision 1.1 is from VKTR. Pricing comparisons are Microsoft's own and unverified.
- F-15: corrected. The Artificial Analysis Neon page confirms the 2026-11-18 release, $3/$15, index 61 and #6/95. The
  $2.21 blended price uses AA's 7:2:1 cache-hit/input/output weighting, not 3:1. AA's Carbon page shows only the
  current $4/$20 and a release date of 2026-10-28, with no introductory price and no December 1 date. The $2/$10 to
  $4/$20 change on 2026-12-01 is supported only by secondary blogs that quote Google's pricing page, so that part is
  secondhand. "Google calls Neon third overall" is not on the page.
- F-16: corrected. Background (2026-11-13). The page does not say "single-use". It says the payment network provides a
  payment token, a substitute for the card details, so the card is not shared with the business or the agent. Each
  purchase is approved with a security check such as Face ID. Everything else is confirmed.
- F-17: confirmed. Source re-read: PYMNTS, 2026-11-19. Sparky +129%, baskets 40% larger, $188.8 billion (+5.2%) and
  e-commerce +17% all match. The Sparky figures are PYMNTS's paraphrase of the call. Walmart's own release was not
  read.
- F-18: corrected. The cited pages confirm the $83 price, the $70–$78 range, ANT on Nasdaq from 2026-11-19 and the
  $97.17 first-day close, up 17.1% (AP via NBC New York). They do not support the other figures. investingLive's "$81
  billion" is October revenue run-rate, not proceeds. AP gives only "above $115" intraday. The $111.50 open is reported
  by TechRepublic and Constellation Research (not cited). The 980 million shares and about $81.3 billion raised come
  from secondary outlets only, and one gives 956,351,354 shares. VKTR's pre-pricing terms were 825 million Class A
  shares. The $1.5 trillion valuation comes from Korea JoongAng Daily, and about $2.1 trillion was an intraday figure.
  Use the offer price and close only. Treat the share count, proceeds and valuation as unconfirmed.
- F-19: corrected. VKTR (2026-11-17) says Amendment No. 3 was filed "on Tuesday", which most likely means 2026-11-17,
  not 2026-11-10. Check EDGAR. All placement amounts, Class N with no underwriter lockup, and the Amazon 14.7% and
  Google 13.7% holdings are confirmed. Amazon's absence is by omission only. VKTR's 825 million Class A shares
  conflict with F-18's 980 million.
- F-20: confirmed. Source re-read: Nvidia press release, 2026-11-17. Every figure matches. Q4 includes an extra week.
- F-21: confirmed. Sources re-read: BusinessDay (Reuters) 2026-11-17, InvestmentNews (re-reporting the WSJ)
  2026-11-17, Khaleej Times (Reuters) 2026-11-18. The committee is the "National Security and Export Control Oversight
  Committee", meeting at least quarterly. "Standing" and "global trade risk" are not the source's words. The SEC
  declined to comment.
- F-22: corrected. Per the Boston Globe of 2026-11-16, the licensing applies to "sales of chips for" Indonesia,
  Malaysia, Singapore, Thailand or Brazil, not to companies headquartered there. The end-user rule covers countries
  "including China, Russia, Iran and Cuba". Rescission of a Biden-era rule is not on the page. No AP byline is visible.
- F-23: corrected. Bloomberg Government (2026-11-15, paywalled lede) confirms Megaspeed as a Singapore cloud company
  accused of smuggling Nvidia chips, that it was kept off the blacklist, and that Senate Republicans asked Lutnick to
  testify. The FT two-month delay comes via Let's Data Science, dated 2026-11-10 (background), so it is secondhand.
  The Ricketts 30-day proposal and Megaspeed's denial were not found on either page and are unconfirmed.
- F-24: corrected. "As much as 11% intraday" is on neither page. Motley Fool (2026-11-19) says AMD was down 6.8% at
  11:16 a.m. ET. Its -13.25% quote box is stamped 4:00 PM 11/20, so it is not the 11/19 move. Use "fell sharply; down
  6.8% by late morning". Wccftech (2026-11-19) confirms the IEIT listing in March 2025, at least six newer firmware
  versions, the short position, that Hunterbrook did not establish licensing, and $7.75 billion (22.4% of fiscal 2025
  revenue). AMD says it complies with export law.
- F-25: confirmed, with a wording note. Source re-read: Federal Reserve minutes, October 27–28, 2026. The first 40,000
  characters were read verbatim and the rest as an extract. Verbatim: "Many participants" saw AI demand straining
  supply and raising prices of technology goods. "Almost all participants commented on risks" in a scenario where AI
  returns disappoint (the minutes say "commented on risks", not "raised concerns"). Staff: "circular financing
  arrangements among AI-related firms could amplify losses". From the extract only, not verbatim: "material source of
  inflation risk", the skilled-construction-labor point, and "almost all" judging further increases likely appropriate.
  The release date of 2026-11-18 comes from the page's "Last Update" line.
- F-26: confirmed. Background (CPI on 2026-11-10, PPI on 2026-11-13). Source re-read: the BLS PPI and CPI releases
  directly, plus TheStreet Pro. Every figure matches. Source type should be primary. BLS says "lapse in appropriations"
  and omits the 12-month change only where October 2025 data are missing. The all-items 12-month change is
  unpublished, but some components (gasoline +37.4%) are published.
- F-27: corrected. Morningstar returned 403. A search excerpt of the same Dow Jones data note gives 5.051% as a 3 p.m.
  ET reading, not a close: down 1.4 bp, the fourth straight decline, and 10.1 bp over the four days. AP via NBC (dated
  2026-11-19) gives 5.04% from 5.07%. The S&P 500's longest losing streak since 2024 (six straight losses) on Anthropic's
  debut day is confirmed. "Lowest since 2026-11-10" and the 5.310% 52-week high on 2026-10-05 were not confirmed.
- F-28: corrected. "Highest since end of August" is not on the page. investingLive (2026-11-19) confirms 203,000,
  prior revised 202,000, consensus 197,000, four-week average 197,750, and continuing claims of 1.763 million, up
  70,000. The DOL PDF did not extract.
- F-29: corrected. The Vanguard page is dated 2026-11-05, not 2026-11-16, so it is background. The finding is
  confirmed. The AI-exposed occupation employment comparison uses Current Population Survey data. The 401(k)
  recordkeeping data feeds a separate hiring comparison. The population is graduates aged 22 to 26.
- F-30: corrected. The cited Banque de France PDF did not extract. The same press release was read on Banque de
  France's HTML page, dated 2026-11-18. Confirmed: AI valuations, fiscal imbalances and geoeconomic tensions are the
  three main risks; "ambitious earnings expectations" make markets vulnerable to abrupt adjustment; AI infrastructure is
  "increasingly funded through debt"; vulnerabilities "are more pronounced in certain non-banks". Not in the press
  release: circular financing among AI firms, concentrated third-party dependencies at banks, banks' limited direct
  lending to AI, and a special feature on AI adoption. Drop those elements unless the Review itself is read.
- F-31: corrected. Warner's release of 2026-11-19 applies the disclosure duty to "non-financial public companies" and
  also covers variable interest entities. The SEC study covers accounting for AI R&D, revenues and capital
  expenditures, not infrastructure useful life. Referral to the Banking Committee is not on the page. WRIC returned 403.
- F-32: corrected. The cited SEC exhibit is a different deal: SpaceX's $25 billion unsecured bond of 2026-06-23. It
  does not support any element. Reuters could not be fetched. Search excerpts of Bloomberg (via Yahoo Finance) and
  Quartz confirm the tranches: $25.17 billion A3 notes due April 2033 at 8.259%, about $4.4 billion A2 notes due April
  2031 at 7.66%, and $2.564 billion class B notes due April 2033 at 8.36%. These sum to about $32 billion of notes.
  Apollo and Goldman's announcement, as reported by Reuters via AOL, gives about $44 billion. Bloomberg frames the
  total as over $40 billion including a senior secured loan, and dates the pricing Thursday 2026-11-19. The SPV is
  Saturn Funding Trust. The upsizing on demand is confirmed. The Moody's A3 and KBRA A-minus ratings, "a notch above
  SpaceX", the anchor investors at pricing, and the H1 2027 lease start were not confirmed in the window (the October
  reports named BlackRock, GSAM and KKR as committed lenders). Write it as about $32 billion of notes within a
  financing of about $44 billion. Source type is wire or trade, not primary.
- F-33: corrected. Commercial Observer (2026-11-19) re-reports Bloomberg. The AAA rating (Fitch and KBRA expected) and
  the 1.95-point spread apply to the $375 million top tranche, not the whole $513 million. A $112 million AA tranche
  prices at 2.6 points. The lease runs through 2042 with two five-year renewals. The page gives the location as
  Gainesville, Va., not Prince William County. $779.5 million and 54 MW are confirmed.
- F-34: corrected. Background. TIKR (updated 2026-11-11) confirms that CoreWeave will not use unsecured debt at current
  yields, about $9 billion of prepayments and deposits in three months, and more than $3 billion against gear "already
  paid off". It puts unsecured yields at about 16%. Not on the page: the 9.625% 2032 notes at 14.21% (TRACE), the
  $4 billion investment-grade loan, and the Bloomberg report of 2026-11-18. Those are unconfirmed. The call date is
  inferred, not stated.
- F-35: corrected. The $2.1 trillion forecast, with about $225 billion from hyperscalers plus about $225 billion for
  data-center and chip financing, is from AI Weekly (2026-11-14) re-reporting Bloomberg (2026-11-13). It is secondhand
  and background. The JPMorgan Asset Management note is dated 2026-08-20, not November. It confirms the quarter
  coverage, 2% to 9%, and 30 bp vs 2 bp. It gives more than $1 trillion of capex for 2027 only, with no 2028 figure.
  Net debt to EBITDA of 1.3x is not on the page.
- F-36: corrected. Loudoun County's release (2026-11-18) says the Board "may consider exceptions" for grid-reliability
  applications; it does not exempt them. The 7-1-1 vote and the county attorney's "real threat of litigation" are from
  Bisnow only. The new standards are expected in summer 2027. Everything else is confirmed.
- F-37: corrected. Both items are background. Energy Connects (Bloomberg) is dated 2026-11-12. It confirms the
  suspended Adelaide project (the 1,200 MW Tungkillo project by Quantum DC) and "at least the third" Australian stall.
  FourWeekMBA returned 403. Search excerpts (Bridge Michigan, Michigan Advance) say Lighthouse Sustainability withdrew
  from the $10 billion, 700 MW Delhi Township site per a LEAP release of 2026-11-09. They also say the township board
  voted 6-0 in opposition and no land-use application had been filed. The Michigan item is secondhand.
- F-38: corrected. The Boston Globe (2026-10-14) confirms the Data Center Watch figure: at least 75 projects worth $130
  billion cancelled in Q1 2026, largely because of opposition. The Carbon Direct report (46 projects, $170 billion) was
  not found; the domain redirects elsewhere. Drop that half. The remainder is wire or trade and background.
- F-39: corrected. The release of 2026-11-20 says "model provenance standard and an AI bill of materials", not
  "model-sourcing standard". Airbnb, Anysphere and DoorDash are the companies the committees corresponded with, not
  "examples". The release says "Moonshot AI base model", not Kimi K2.5, and the CNBC piece was not read. The page count
  is not confirmed, because the report PDF is image-only. 12 recommendations and the federal and critical-infrastructure
  bars are confirmed.
- F-40: corrected. GAO published the report 2026-10-16 and released it publicly 2026-11-18. Results are presented by
  anonymized platform (A–D), not withheld. The model-to-letter mapping and the techniques beyond generic categories
  are withheld. The Highlights say companies "will continue to improve" safety, not that safeguards have changed (the
  extract adds that Anthropic says it has expanded safeguards since May 2026). "No recommendations" is not confirmed:
  the full report was only partly read.
- F-41: corrected. The release does include an application result, in a separate IBM and RIKEN quantum chemistry item
  (protein-ligand binding energies up to 12,635 atoms). "No application result" is wrong as a statement about the
  release. The 13,000x is against "existing leading algorithms" with no comparator named. The processors include IBM
  Quantum Nighthawk. The platform is described as planned and proposed.
- F-42: confirmed. Source re-read: Quantum Computing Report, dated 2026-11-17 (Quantum Machines' own release, linked,
  was not read). Every figure matches. The decode figures are PyMatching on a GH200.
- F-43: confirmed. Source re-read: Boston Dynamics release, 2026-11-17. The sites are Malta NY, Burlington VT, Dresden
  and Singapore (two Spot robots in Singapore).
- F-44: corrected. TechCrunch (2026-11-17) gives no $3.5 billion valuation and no Paris headquarters, so drop both
  unless another source is found. The company is piloting with "a handful of undisclosed customers". A mass-manufacturing
  contractor starts "next year" in the US. The lead investors, the $500 million and the $105 million seed are
  confirmed.
- F-45: confirmed. Source re-read: arXiv 2611.21099 abstract, submitted 2026-11-16. Every figure matches. Source type
  should be primary. The NUS affiliation is not on the abstract page.
- F-46: corrected. The Ramp page has been updated: data now runs to the week ending 2026-11-15, and it shows Anthropic
  at 58.7% of business token spend and total token spend up 12.0% on a month earlier. The 49.3% (week ending
  2026-11-01) and 10.5% figures are not on the page and are unconfirmed. Use the current figures with their date.
  56.8% (+1.0 pt), Anthropic 44.8% vs OpenAI 40.6%, $16.32 (the median firm paying for AI) and $10,199.20 are confirmed.
  "Sample skews tech-savvy" is not on the page. No release date is shown.
- F-47: corrected. The TrendForce bulletin of 2026-11-18 confirms stalled mobile DRAM talks, weak spot demand, and that
  the market is still "undersupplied" while "the shortage gap is narrowing". The DDR5 $60.233 (-2.1%), DDR4 -0.09% and
  SK hynix 14-agreement figures are not in the public bulletin. FourWeekMBA returned 403. Those figures are unconfirmed.
- F-48: confirmed. Source re-read: Dragos, published 2026-11-16, so in window. 1,266 incidents (+11% on Q2's 1,140),
  1,020 in Q1, and no Stage 2 case are all confirmed.
- F-49: corrected. Background. The Star (2026-11-04) re-runs Bloomberg. Meta was "eyeing at least US$20bil" in a
  potential multi-currency offering, not a completed $15 billion. Oracle's coupons and the $67 billion Goldman figure
  are not on the page. S&P's negative outlook on Meta is confirmed, but the AA- rating and the 2026-10-30 date are not.
  Oracle's $10 billion of bonds alongside $10 billion of equity and Microsoft's $25 billion, its first US offering since
  2017, are confirmed. The page adds Alphabet's €6 billion and more than $330 billion of AI-related US high-grade
  borrowing this year.

Totals: 14 confirmed, 33 corrected, 2 unconfirmed (F-08, F-09), 0 dropped. Corrections remove elements from several
facts (F-30 circular financing, F-38 Carbon Direct, F-44 valuation, F-46 and F-47 figures, F-32 ratings). Those
elements may not be used.

## Source mix

Counts by source type after verification. The fact sheet's labels are in brackets.

- Primary: 22 [17]. Relabelled to primary: F-01, F-02, F-05, F-10, F-26, F-45. Relabelled away: F-32, now wire or
  trade.
- Wire or trade: 21 [22]. F-38 moves here from secondhand once the Carbon Direct half is dropped. Several are re-runs
  (Reuters via BusinessDay and Khaleej Times; AP via NBC New York; Bloomberg via Commercial Observer, Energy Connects
  and The Star).
- Analyst: 3 [3]: F-15, F-35, F-47. Parts of each rest on secondhand or unconfirmed material.
- Secondhand: 3 [7]: F-04, F-09, F-34. Secondhand elements inside other facts: F-15 (Carbon price change), F-18
  (share count and open), F-23 (FT), F-32 (search excerpts of Bloomberg and Reuters), F-35 (Bloomberg forecast), F-37
  (Michigan).

Concentration:

- OpenAI is the source behind five facts (F-01, F-02, F-04, F-05, F-16) and the corroborating source for F-03, about
  a tenth. F-01 to F-04 all come from one release and its system card, so they are one event, not four independent
  signals.
- Bloomberg is the originating outlet behind about six facts (F-32, F-33, F-35, F-37, F-49, and part of F-34), mostly
  through re-runs, also about a tenth.
- Let's Data Science (F-05, F-10, F-23) and FourWeekMBA (F-05, F-37, F-47) appear as secondary sources. FourWeekMBA
  returned 403 every time, and Let's Data Science was a rewrite of a primary in each case checked.

## Flags

Change types that look like level only:

- F-04 "new trend": one benchmark drop across one version step.
- F-07 "acceleration": a single incident.
- F-08 and F-09 "acceleration": the claims are unconfirmed, so they carry no change type.
- F-12 "new trend" and F-45 "acceleration": single papers.
- F-13 "new trend": a single vendor launch reporting a ratio.
- F-24 "new trend": a single short-seller report.
- F-15 "reversal": the Carbon price rise is the scheduled end of an introductory price. It is not a reversal of falling
  list prices, and its source is secondhand.
- F-27 "reversal": a four-day, 10 bp move, which M-07 already describes as the pattern for this trigger.
- F-30 "acceleration": the circular-financing element that justified it is not in the ECB press release. The claim
  that a second central bank adopted M-08's framing this week does not hold, and the change is level only.
- F-32 "reversal": rests on one deal. The notes were about $32 billion, not $44 billion, and the ratings are
  unconfirmed. It is evidence the window is open for strong sponsors at about 8%, not by itself a regime reversal.
- F-37 "acceleration": both withdrawals are background, dated before the window.
- F-01 "new trend": one release crossing a threshold. It is better read as a level event against M-12.

Model claims and rows that the research did not check, or checked only partly:

- M-01: the refutation condition (published harness-invariance results on ARC Prize, LMArena or Artificial Analysis)
  was not checked.
- M-07: the TrendForce Q1 2027 DRAM contract forecast was not found. F-47's figures that would bear on it are
  unconfirmed.
- M-09: the refutation condition is a share of planned capacity cancelled. F-38's Data Center Watch figure is in
  projects and dollars, so it cannot be compared with the 10% threshold without a capacity base.
- M-10: no check of whether any learned policy was certified as final authority over actuation. The fact sheet says
  "against none" without saying it looked.
- M-11 and the "Post-quantum migration deadlines" row: no evidence. The executive order number disagreement (14409 vs
  14412) is unresolved.
- "Power capacity price" row: no evidence this week.
- W-05 and W-08: no evidence.
- W-01: whether Nvidia named a permanent chief executive (the drop condition) was not stated explicitly. F-21 says only
  that the board will not reinstate Huang.

Other things phase C should know:

- F-25 is confirmed, so the FOMC conjunct of M-07's "would be wrong if" has already failed. The circular-financing
  framing is the Fed staff's, not the Committee's.
- F-18 vs F-19: the share count conflicts (980 million reported, 956 million in one report, 825 million in the
  pre-pricing terms). Use no share count, proceeds or valuation figure for Anthropic until the final prospectus is read.
- F-32: the source the fact sheet called primary (the SEC exhibit) is a different deal. Pricing date is 2026-11-19 or
  2026-11-20 depending on the source.
- F-46: the Ramp token-spend figures moved between research and verification. Quote them with the week-ending date.
- F-06: the complaint has not been read. Its allegations are unproven.
- Single-source items after verification: F-03 (VentureBeat for the 19%/51% and 85%/57% figures), F-04, F-11, the
  F-14 Maia figures (VKTR), F-36's vote count and litigation warning (Bisnow).
