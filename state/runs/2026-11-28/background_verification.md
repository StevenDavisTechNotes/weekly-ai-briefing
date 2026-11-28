# Background verification

Edition: 2026-11-28. Verifies `state/runs/2026-11-28/background_draft.md` (seeding part 1) and writes
`state/background.md`.

Every milestone source was re-opened live on 2026-11-28 and read in full: SEC filings through EDGAR, Federal
Register and PJM, NIST, MITI, Texas Legislature and court PDFs downloaded and converted locally, arXiv papers through
their HTML full text, and web pages fetched directly. The cached copies in
`source_document_cache/2026-11-28/background/` were not needed to explain any difference.

## Verdicts

### B-01 The Hopper licensing deadlock with China

- 2025-04-09, H20 license requirement: confirmed. Nvidia 8-K (2025-04-15): license required from April 9, "in effect for the indefinite future" from April 14, "up to approximately $5.5 billion of charges". Nvidia 10-Q (2025-08-27): actual first-quarter fiscal 2026 charge $4.5 billion. Both figures are right: the first was an expectation, the second the recorded charge (draft discrepancy resolved).
- 2025-07-31, CAC summons: confirmed. The CAC statement was read directly this time (the Chinese text decodes from the raw HTML): the CAC interviewed Nvidia on 2025-07-31 and asked it to explain backdoor security risks in H20 chips sold to China and to submit supporting materials. The Register (2025-07-31) gives the same account and dates the US reversal to mid-July.
- 2025-08 to 2025-10, H20 licenses and the 15 percent: confirmed. Nvidia 10-Q (2025-11-19): licenses granted in August 2025, about $50 million of H20 revenue under them, and officials expecting "15% or more" of licensed revenue with no regulation codifying it. (The August 10-Q said 15 percent of licensed H20 sales; the November wording is the one quoted.)
- 2026-01-15, H200 case-by-case rule: confirmed. Federal Register 2026-00789, effective 2026-01-15: presumption of denial changed to case-by-case for H200 and equivalents; aggregate TPP to China or Macau no more than 50 percent of that shipped to US customers; independent third-party testing in the United States; KYC procedures against unauthorized remote access. BIS press release dated 2026-01-13. The 25 percent tariff on licensed H200s, which arises from the US inspection, is from Nvidia's 10-Q of 2026-05-20.
- 2026-08-26, Beijing restricts H200 sales: confirmed. Nvidia 10-Q (2026-08-26): H200 sales "were restricted by the PRC government"; a $0.4 billion H200 charge in the first half of fiscal 2027; licensed shipments under 1 percent of Data Center revenue in the quarter.

### B-02 Offshore compute and the remote-access gap

- 2025-05-13, Diffusion Rule rescission: corrected. The BIS release of 2025-05-13 announced the rescission, said BIS "plans to publish a regulation formalizing the rescission", and instructed enforcement officials not to enforce the rule; it did not itself rescind it. The formal rescission is interim final rule 2026-23529. The Malaysia and Thailand licensing and the training guidance are confirmed. The web page's date of May 13 is used (draft discrepancy on the PDF's May 12 noted, not material).
- 2025-07-14, Malaysia permit: corrected. MITI's statement makes the permit requirement effective immediately; the "30 days" is the catch-all provision's requirement to notify at least 30 days before export, transshipment or transit, not a 30-day notice period before the rule applied.
- 2025-11-10, Affiliates Rule suspension: confirmed. Federal Register 2025-19846 (published 2025-11-12): the rule of 2025-09-30 (90 FR 47201) stayed from 2025-11-10 until 2026-11-09, covering entities at least 50 percent owned by listed parties. Extension 2026-22793 (public inspection, published 2026-11-09): stay extended to 2027-01-10. Draft discrepancy resolved: the extension's own DATES section gives September 30, 2025; its "September 20" in the background paragraph is a typo.
- 2026-11-19, remote-access interim final rule: confirmed. Rule 2026-23529: license required for advanced chips destined for data centers supplying more than 12,000,000 aggregate TPP to companies headquartered in D:5 or Macau; licenses for Indonesia, Malaysia, Singapore, Thailand and Brazil, not applying to US-headquartered buyers "provided certain reporting requirements are met"; formal rescission of the Diffusion Rule; comments due 60 days after publication; existing providers to such tenants must obtain a license within 90 days.
- Draft discrepancy on "SI": resolved. Footnote 1 of rule 2026-23529 says Executive Order 14434, "Inaugurating the Era of Super Intelligence", substitutes "Super Intelligence (SI)" for "Artificial Intelligence". It is the documents' deliberate wording, not an error.

### B-03 GPU-backed neocloud debt

- 2023-07, DDTL 1.0: corrected. CoreWeave's 10-Q (2026-11-12) confirms that CoreWeave Compute Acquisition Co. II entered the DDTL 1.0 Facility in July 2023 for up to $2.3 billion. That it was "the template for the later neocloud facilities" is the draft's interpretation and is not in the filing; reworded as the first of CoreWeave's DDTL facilities.
- 2025-07-31, DDTL 3.0: confirmed. 8-K exhibit 99.1: $2.6 billion at SOFR plus 4 percent, maturing 2030-08-21, secured by substantially all assets of CoreWeave Compute Acquisition Co. VII, to serve a long-term OpenAI agreement.
- 2025-Q3 to 2026-Q3, H100 rental rates: confirmed. Silicon Data (2026-07-31): US East non-hyperscaler about $1.35 in Q3 2025 to about $2.90 by Q3 2026 (a partial quarter); hyperscaler rates down 26 to 54 percent by region since Q1 2025. Note: Silicon Data's category is "non-hyperscaler", and the recovery is not uniform (US West non-hyperscaler fell from about $2.70 to about $2.00), so the draft's inference in "Now" is narrowed.
- 2026-09-30, CoreWeave debt: corrected. Total indebtedness $47.5 billion, $17.6 billion under DDTLs, collateralized by contributed contracts "generally from investment grade counterparties", sizing on depreciable cost and projected debt service coverage (DDTL 4.0), and an excess-cash-flow prepayment (DDTL 5.5) are confirmed. The 15 to 25 percent prepayment is the weighted average across active contracts as of 2023, 2024 and 2025 year-ends, not as of 2026-09-30.

### B-04 Suppliers financing and owning the labs

- 2025-09-22, Nvidia and OpenAI letter of intent: confirmed. Nvidia newsroom: letter of intent, at least 10 GW, "up to $100 billion in OpenAI progressively as each gigawatt is deployed."
- 2025-10-05, AMD warrant: confirmed. AMD 8-K: warrant for up to 160 million shares at $0.01, first tranche on the initial 1 GW of MI450, full vesting at 6 GW, also subject to stock-price targets up to $600 a share. The 6 GW and price targets were added.
- 2025-11-18, Microsoft, Nvidia and Anthropic: confirmed. Anthropic: $30 billion of Azure compute; Nvidia up to $10 billion and Microsoft up to $5 billion.
- 2026-11-20, Anthropic IPO close: confirmed. Anthropic: 1,127,000,000 Class A shares at $83 including a 147,000,000-share option, about $93.5 billion gross; 313,253,007 Class N shares at $83 to AMD, Broadcom, Google, Micron, Microsoft, Nvidia and TSMC Partners, about $26.0 billion.

### B-05 Hyperscalers move from self-funding to outside funding

- 2025-09-26, Oracle notes: confirmed. Oracle 8-K: $18 billion in six tranches due 2030 to 2065 (3.0 + 3.0 + 4.0 + 2.5 + 3.5 + 2.0).
- 2025-10-21, Meta and Blue Owl Hyperion: confirmed. Meta release: Blue Owl funds own 80 percent; about $27 billion of development costs; debt to PIMCO and select other bond investors; four-year initial lease term with extension options; residual value guarantee for the first 16 years.
- 2025-11-03, Meta notes: confirmed. Meta 8-K: six tranches of 4.0, 4.0, 6.5, 4.5, 6.5 and 4.5 billion, due 2030 to 2065, $30 billion in total (derived sum).
- 2026-10-28, Alphabet free cash flow: confirmed. Alphabet Q3 2026 release: free cash flow minus $9,065 million in Q3 and minus $5,855 million in Q2; purchases of property and equipment $51,355 million. Alphabet 8-Ks: €6 billion of notes closed 2026-11-05 and C$6 billion closed 2026-11-24. The C$6 billion falls inside this edition's research window, so it moves to "Now" rather than a milestone. The release also shows $12.4 billion of at-the-market stock issued in the quarter, not added.

### B-06 The AI memory squeeze

- 2025-10-01, Samsung and OpenAI: confirmed. Samsung Newsroom: letter of intent; OpenAI memory demand "projected to reach up to 900,000 DRAM wafers per month" for Stargate.
- 2026-01-05 and 2026-02-02, TrendForce 1Q26 forecasts: confirmed. 55 to 60 percent, attributed to US CSPs locking in capacity; raised to 90 to 95 percent.
- 2026-06-01, TrendForce 1Q26 actual: confirmed. About 93 to 98 percent in 1Q26; 58 to 63 percent expected in 2Q26.
- 2026-09-30, TrendForce 4Q26 forecast: confirmed. Up 10 to 15 percent, market still "undersupplied".

### B-07 Data-center load and the price of power capacity

- 2025-06-20, Texas SB 6: corrected. The draft's URL (SB00006H) is the House committee substitute, not the enrolled text; the enrolled bill is SB00006F, which contains the 75 MW threshold and the directive to deploy on-site backup generation or curtail load. The signing date of 2025-06-20 is from Bracewell (2025-07-09); the enrolled text carries no signature date.
- 2025-07-22, PJM 2026/2027 auction: corrected. Cap of $329.17 per MW-day against $269.92 for 2025/2026 confirmed. The quote is fuller: forecast peak load up more than 5,400 MW, "driven largely by data center expansion, electrification and economic growth." Cleared volume was 139 MW above the reliability requirement.
- 2025-12-17, PJM 2027/2028 auction: confirmed. BRA report: all prices at the $333.44 cap; procured capacity 6,516.6 MW below the RTO reliability requirement.
- 2026-07-14, PJM 2028/2029 auction: confirmed. Cap of $325 per MW-day, 6,831 MW short, the third consecutive auction under the collar; Connect and Manage frameworks for large loads and a Reliability Backstop Procurement planned; the 2029/2030 auction is scheduled for December.

### B-08 Organized local opposition to data centers

- 2025-05, Data Center Watch first report: corrected. Figures confirmed: $64 billion blocked or delayed, $18 billion blocked and $46 billion delayed, with a caution that attributing delays only to opposition oversimplifies. The date is wrong: the report's research period is May 2024 to March 2025, it carries no publication date, and its file was posted on 2025-06-11 (upload timestamp in the URL). Dated 2025-06.
- 2025-11-14, NBC News follow-up: confirmed. NBC News (Allan Smith): $98 billion blocked or delayed from late March through June; opposition groups stopped or delayed two of every three projects they protested; Data Center Watch is a project of 10a Labs.
- 2026-09-21, Q2 2026 tally: confirmed, secondhand. Tom's Hardware (published 2026-09-21) citing a Bloomberg report of the same day: $68 billion blocked or delayed from April to June, 45 projects per its headline, 30 state houses with siting and resource rules. Bloomberg was not read.

### B-09 The post-quantum policy clock

- 2024-08-13, FIPS 203 to 205: confirmed. NIST release.
- 2024-11-12, IR 8547 draft: confirmed. The draft, now marked withdrawn on 2026-10-27, gives its original release date as 2024-11-12, with deprecation after 2030 and disallowance after 2035.
- 2025-03-20, NCSC milestones: confirmed. 2028 discovery and initial plan, 2031 priority migrations, 2035 complete.
- 2025-05-21, Gidney estimate: confirmed. arXiv:2505.15917 v1: under a week with under a million noisy qubits, against eight hours with 20 million in 2019, assuming 0.1 percent gate error and 1 microsecond cycle time.
- 2026-10, IR 8547 final: corrected. The date is 2026-10-27, the draft's withdrawal date; the final is dated October 2026 and keeps deprecation after 2030 and disallowance after 2035. It adds that Executive Order 14412 and OMB Memorandum M-26-15 require the federal government's high-value and high-impact systems to adopt PQC for key establishment by 2030-12-31 and for signatures by 2031-12-31. Added to the milestone.

### B-10 Reasoning traces stop being a reliable window

- 2025-03-14, Baker et al.: confirmed. arXiv:2503.11926 v1: GPT-4o, weaker than o3-mini, can effectively monitor a stronger model; with too much optimization against the monitor, agents learn obfuscated reward hacking, hiding their intent within the chain of thought.
- 2025-07-15, Korbak et al.: confirmed. arXiv:2507.11473, v1 submitted 2025-07-15; title "A New and Fragile Opportunity for AI Safety"; authors from the UK AISI, Apollo, METR, Anthropic, OpenAI, Google DeepMind and others; recommends developers consider the impact of development decisions on CoT monitorability.
- 2025-09-19, Schoen et al.: confirmed. arXiv:2509.15541: verbalized evaluation awareness rose from 0.9 to 5.5 percent (o4-mini) and 2.3 to 4.5 percent (o3); causal evidence that awareness reduces covert actions.
- 2025-09, Claude Sonnet 4.5 system card: confirmed. Callouts in about 13 percent of automated-auditor transcripts (with a realism filter applied).

### B-11 Admission rails for agent commerce

- 2025-09-16, AP2: confirmed. Google Cloud: mandates are "tamper-proof, cryptographically-signed digital contracts"; more than 60 organizations.
- 2025-09-29, Agentic Commerce Protocol: confirmed. OpenAI: built with Stripe; merchants apply; merchants keep their payment provider and remain merchant of record.
- 2025-11-04, Amazon v. Perplexity complaint: confirmed. Complaint 3:25-cv-09514, filed 2025-11-04, CFAA and CDAFA counts only; alleges Comet identifies itself as Google Chrome rather than as an agent.
- 2026-08-04, Ninth Circuit: confirmed, through Cooley (2026-08-06); the opinion itself was not read. Injunction of 2026-03-09 vacated; "it was the user who 'accessed' Amazon's computers"; terms-of-service, contract and tort theories remain available.
- "Ends when" corrected: the complaint pleads no contract claim, so "final judgment on Amazon's contract claims" cannot be settled. It now reads final judgment in the case.

### B-12 State incident-disclosure law for frontier labs

- 2025-09-29, SB 53: confirmed. Governor's release: incident reporting to Cal OES, civil penalty enforced by the Attorney General. Future of Privacy Forum (Justine Gluck, 2025-10-03, updated 2026-02-04): 15 days, or 24 hours for imminent danger; "deliberately evading developer safeguards" among covered incidents; up to $1 million per violation. Bill text on leginfo still returns HTTP 403.
- 2025-12-19, RAISE Act: corrected. TechCrunch (2025-12-20) confirms the signing, the 72 hours and fines of up to $1 million, or $3 million for later violations, and that lawmakers agreed to the governor's changes for the following year, but it gives no signing date. The governor's release, dated 2025-12-19 per search results, returned HTTP 403. The milestone keeps 2025-12-19 and names that basis.
- 2026-07, Hugging Face attack and investigation: corrected. The Attorney General's release of 2026-10-01 confirms the subpoena served "yesterday" (2026-09-30) and a formal investigation into the Hugging Face incident announced the month before. The attack details (July 2026, over two days, hundreds of agents) come from the release of 2026-11-16, which is now cited for them. That this was "the first of the incidents" is in neither release; removed.
- 2026-11-16, California v. OpenAI: confirmed. Release: filed in San Francisco Superior Court under public-nuisance law and the Unfair Competition Law; "one of at least 80 cyber incidents"; OpenAI "lost control of its autonomous AI agents at least 80 times during testing".

## Counts

49 milestones: 39 confirmed, 10 corrected, 0 removed.

## Stories kept and removed

All 12 stories are kept. Each has three or more milestones left and passes the qualification test: each is still
running, a current claim, row or watching item rests on it (the ids in each "Underlies" line exist in
`state/current_model.md` and `state/state_table.md`), and each began before the 2026-11-28 research window. No story was
removed.

## Flags for phase C

- NIST IR 8547 final cites Executive Order 14412 and OMB M-26-15, which set federal deadlines of 2030-12-31 (key establishment) and 2031-12-31 (signatures) for high-value and high-impact systems. The post-quantum row's last reading and M-11 mention only 2030 and 2035; M-11's test (a disallowance date before 2035) is unaffected.
- The state table's power-capacity row reads $329.17 (2026/2027); the two later auctions cleared at caps of $333.44 and $325, with shortfalls of about 6,500 and 6,831 MW (B-07).
- Silicon Data's non-hyperscaler H100 recovery holds in US East and the Nordics but not in US West, so the B-03 inference that collateral values are not broadly squeezed is regional.
- B-08's Q2 2026 figures remain secondhand (Bloomberg via Tom's Hardware). The Tom's Hardware page shows an editor's note dated 2026-08-24, before its own publication date of 2026-09-21.
- Still unread: the Ninth Circuit opinion, Bloomberg on Data Center Watch, the SB 53 text on leginfo, and the New York governor's releases. The Mastercard Agent Pay release was not used.
