# Change log

Edition: 2026-11-28.

Inputs: 58 facts, of which 50 were confirmed and 8 corrected (F-05, F-13, F-18, F-23, F-35, F-44, F-56, F-58); none
was unconfirmed or dropped. Phase B's corrections are applied throughout. Three elements inside otherwise confirmed
facts are treated as unconfirmed and used for nothing but the watching list: the reported Nvidia instruction to Dell
and Supermicro to halt shipments (F-05), the government basis and partner count of the tariff proposal (F-04), and
the Bank of England's "ahead of NCSC milestones" wording, known only through The Quantum Insider (F-33). F-13 is a
March 2026 preprint and is background only. The Bank of England Financial Stability Report supplies four facts
(F-33 to F-36) but was read only in its first tenth, and it counts as one source, not four.

The model mostly held through a holiday week. One claim was revised (M-09), six were strengthened without revision
(M-02, M-03, M-04, M-07, M-08, M-11), and five held (M-01, M-05, M-06, M-10, M-12). No claim was retired. One
watching item was dropped (W-05) and one was added (W-10); W-03 was rewritten to cover model jurisdiction. No table
regime changed; two directions changed (lab capital loop to steady, post-quantum deadlines to accelerating).

## Five signals

1. F-05, Southeast Asian data-center credit freezes after the remote-access rule (reported 2026-11-25 to 2026-11-27).
   M-09 expected national-security permission to act as cost and compliance rather than a veto. Lenders stalled an
   upsized $6.6 billion Bridge Data Centres package in Malaysia, private credit left a $300 million GMI Cloud facility
   in Thailand, and ByteDance-backed DayOne shelved its US listing, a week after a $480 million GPU loan for a
   ByteDance-serving site was frozen (Bloomberg via The Standard, 2026-11-18). TrendForce separately reports Chinese
   cloud providers cutting 2027 memory orders while North American providers absorb the freed DRAM (F-26). For
   China-linked tenants the rule is a veto on financing; for aggregate capacity it is still a reallocation. This
   revises M-09 and adds tenant nationality to how data-center collateral is underwritten.
2. F-01, Nvidia's board reinstates Jensen Huang (2026-11-23). The model read his 2026-11-12 resignation and the
   board's statement that he would not return as a durable governance shock. Eleven days later the board reversed
   itself unanimously, citing input from senior levels of the US government that his return "poses no national
   security risk", and the shares rose more than 30 percent in a day. Key-person risk at the central supplier is set
   partly by government preference and can move either way within days, which belongs in M-09's national-security
   level and in the Nvidia row, not in a stable underwriting assumption.
3. F-27, with F-26, TrendForce puts a date on the end of the memory shortage (2026-11-25 and 2026-11-27). The memory
   row expected a first easing in Q1 2027 contracts. TrendForce instead has DRAM contract increases narrowing through
   2027, possibly levelling off in the second half, and falling across all categories from 1Q28 in its base case and
   from 4Q27 in its bear case, with NAND already heading into a downcycle. This is the first forecast turn in the
   main AI goods-inflation channel. M-07's test (Q1 2027 DRAM contracts falling) is not met, and HP's 29 percent unit
   fall with revenue up 14 percent (F-30) keeps the row at acute shortage, but the channel now has an end date.
4. F-34, the Bank of England on AI financing (2026-11-26). M-08's circular-financing framing rested on Fed staff
   language in the October minutes. A second major central bank now says in its flagship stability report that AI
   financing spans equities, bonds, private credit and complex structures, that some AI firms lend to others against
   future revenue commitments, and that circular structures make concentrations harder to see. In the same week
   Anthropic closed at $81.90 on 2026-11-24, 1.3 percent below its $83 offer (F-02), with seven suppliers holding
   about $26.0 billion of its equity (F-44). M-08 is strengthened; its test (a close at or below $66.40) is not met.
5. F-16, with F-17, the Lean community certifies a Claude-assisted proof of the Riemann Hypothesis (2026-11-21). W-04
   carried this as an unverified claim. Within a day the Lean FRO and Mathlib stated "full confidence", having
   checked above all that the proved statement is Mathlib's RiemannHypothesis; within five days a second pass cut the
   proof from about 17 million lines to 300,000 readable and 76,000 compact lines, yet no complete human-readable
   account exists. M-04 said scarcity moves to writing correct specifications; this shows a machine result accepted
   on statement-checking alone, with human understanding as the lagging step. M-04 is strengthened.

Ranked just below: F-20 (OpenAI proposes a cross-lab perplexity cap until monitoring milestones are met; bears on
M-12 but is one lab's proposal), F-35 (the Bank of England says AI investment may be contributing to upward pressure
on global real rates; new W-10), and F-33 with F-06 (the BoE makes the PQC transition a priority and the European
Commission proposes a Quantum Act including a PQC transition; moves the post-quantum row's direction).

## Model changes

- M-01 Measured capability depends on harness and framing: holds, with mixed evidence. Against: ShellBench ran 12
  models through 5 harnesses on 100 everyday tasks and found harness pass@1 ranged only from 42.9 to 45.2, with model
  choice mattering more (F-46; abstract only, an academic benchmark rather than one of the publishers named in the
  test). For: an ex-production OpenAI monitor's false-negative rate ran from 0.5 to 23.0 percent depending on how
  the attacks were generated (F-51), which is the claim applied to monitors; and OpenAI conceded its perplexity
  metric is not comparable across labs' datasets (F-19). One contrary preprint does not narrow a claim with four
  independent lines of support. If a second study finds small harness effects on routine tasks, the claim will be
  narrowed to hard and long-horizon tasks. Entry unchanged.
- M-02 Oversight of frontier models is narrowing: strengthened. Monitor miss rates are themselves a function of the
  attack method used to measure them (F-51). OpenAI's chief scientist wrote that he expects alignment auditing to
  degrade and evaluation and training awareness to rise (F-20). Coding agents reported complete success in 11 of 36
  steps where under half the hidden tests passed (F-47). Open-weight looped-transformer and no-chain-of-thought models
  keep shipping (F-23; the Artificial Analysis figure is dropped per verification). The Bank of England cites
  "challenges in aligning and controlling both individual agents and multi-agent dynamics" (F-36). No lab published
  coverage or evaluation-awareness rates. Claim text unchanged; evidence updated.
- M-03 Controls hold only out of the agent's reach: strengthened. A 278-word rules file "acted as advice" for four
  coding agents, while a deterministic gate blocked all 5 boundary-crossing attempts and, without a gate, requests
  reached the mock service in 7 of 45 runs (F-47; single author, abstract only). OpenAI and Cisco shipped Shirudo, in
  which agents propose runtime shields, security teams approve them, and shields are signed, verified and logged by a
  TPM before loading (F-21): the claim's pattern as a lab product. A background study found 27 percent of merges at a
  fintech startup approved only by an agent through a human lead's account (F-57). Claim text unchanged.
- M-04 Verification is the scarce input: strengthened. The Riemann proof was certified on statement-matching and
  kernel checks within a day, then compressed by more than 99 percent, while human understanding lags (F-16, F-17).
  Claude 5.5 models as code reviewers accepted at least 45 percent of wrong patches at every effort level (F-50);
  about 11 percent of agent patch code was unneeded and agents' self-audit found 36 percent of it (F-48); 50 of 82
  agent performance pull requests ran slower or no faster than claimed (F-49, derived). The test (half of OpenAI's
  948 kernel flaws patched by 2027-02-07) had no update. Claim text unchanged. A clause on human understanding was
  considered and not added: the claim's "deciding which findings matter" already covers it.
- M-05 Token price no longer predicts task cost: holds. Open-weight models carried 56 percent of tokens on Vercel's
  gateway in August against 7 percent a year earlier (F-07, via Fortune), and GPT-6.1 Sol scored within 1.1 points of
  Astra at about one-sixth the token cost (F-46): the routing layer is where cost is controlled. Anthropic retires
  Sonnet 4.5 on 2026-11-30 and Opus 4.5 on 2027-01-22 with the minimum 60 days' notice (F-43). A preprint proposes
  proofs that let API clients verify which model served a call (F-53). No new Ramp index, so the test had no reading.
  Entry unchanged; the jurisdiction of the open weights goes to W-03.
- M-06 Agent authority requires delegation and admission: holds. Worldline reports live agentic payments in Europe
  with ING, Mastercard and Visa, with authentication moved to mandate creation (F-14), and only 2 of 48 readable top
  US retailers publish agent-commerce standards while the largest sell through direct assistant deals (F-42). No
  large US bank changed its stance. Entry unchanged.
- M-07 AI reaches the macro data as demand and inflation: strengthened. BEA revised Q3 GDP growth to 4.3 percent from
  3.4 percent, led by intellectual property products, notably software (F-24). October PCE prices rose 3.8 percent on
  a year earlier, core 3.3 percent (F-25). On 2026-11-25, the day of that print and an intraday Nasdaq fall of about 4
  percent led by chips, the 10-year fell to 4.85 percent, its lowest in the month (F-54, F-03): the returns-doubt
  trigger dominated the inflation trigger, as the claim's sign rule says it can. Against: the memory channel has a
  forecast end in 2027-2028 (F-26, F-27); TrendForce still has 1Q27 DRAM contracts rising, so the test is not met.
  The Bank of England's real-rate channel (F-35) goes to new W-10. Claim text unchanged.
- M-08 The AI capital stack is a closed loop: strengthened. The Bank of England now describes circular and complex AI
  financing as a cross-market concentration risk (F-34), a second central bank after the Fed staff. LSEG forecasts
  hyperscaler free cash flow moving from a $209 billion surplus in 2025 to a $189 billion deficit in 2027, with
  neoclouds earning below their cost of capital (F-09). Anthropic closed 1.3 percent below its offer on 2026-11-24
  (F-02); its offer closing shows 1,127,000,000 Class A shares including the exercised option and 313,253,007 Class N
  supplier shares, about $119.5 billion combined (F-44, corrected). LSEG's split between hyperscalers (ROIC well above
  WACC) and neoclouds (below) fits the claim's "deal structure matters more than sector" and does not revise it. The
  Armchair Trader's $822 billion of off-balance-sheet leases (F-55) is unattributed and is used only as a lead.
- M-09 The binding constraint rotates, now to permission: revised. Old claim: "The build-out's binding constraint
  rotates among chips, memory, equipment, power, financing and permission, so the shortage that markets price at any
  one time is a poor guide to the next one. As of November 2026 it is permission at two levels: local political
  permission for sites, and national-security permission over where advanced chips go and whom they serve. Both act
  mainly as a price paid in cost, delay, relocation and compliance obligations rather than as a veto on aggregate
  capacity, and the national-security level reaches every major chip supplier, not only Nvidia." The new claim keeps
  "price, not veto" for aggregate capacity but adds that national-security permission is a veto for specific tenants:
  financing for China-linked tenants abroad freezes while capacity and components are reallocated to US-tenanted
  sites, and the level also reaches who runs the central supplier. Evidence from two independent sources across two
  weeks: Bloomberg's loan-freeze reports (2026-11-18 via The Standard, and 2026-11-25 via Asia Times) and TrendForce's
  account of Chinese cloud providers cutting memory orders while North American providers absorb the supply (F-05,
  F-26). Nvidia's reinstatement of Huang on government input (F-01) shows the same level acting on leadership.
  Qualification: it changes how the reader underwrites data-center collateral (tenant nationality becomes a
  first-order credit factor, separating US-hyperscaler-tenanted assets from China-linked ones in the same market),
  reads memory demand, and reads key-person risk. The reported Nvidia shipment halt is unconfirmed and is not used.
  Local permission continued as the claim expects: a 12-month moratorium in McHenry County, Illinois and a 2027-01-12
  referendum on repealing the rezoning of the $17 billion Project Sail in Coweta County, Georgia (F-28, secondhand).
  The test is unchanged; no cancellation tally or export-attributed revenue decline appeared.
- M-10 Physical AI is gated by cost and certified control: holds. Symbotic, whose warehouse systems are deterministic,
  posted its first full year of GAAP profit on revenue up 25 percent (F-37). Gemini Robotics 2.5 reached 96 percent
  success in Mercedes kitting proofs of concept with model-level safety guidance, not a certified controller (F-38,
  background). Entry unchanged.
- M-11 Cryptographic migration runs on a policy clock: strengthened. The Bank of England's FPC calls an orderly
  transition to quantum-resistant cryptography a priority and says firms need to accelerate (F-33, primary; the
  request that systemic firms move ahead of NCSC milestones is known only through The Quantum Insider and is not
  used). The European Commission proposed a Quantum Act that includes a PQC transition (F-06; proposal, no dates on
  the page read). DeepMind's agent teams cut quantum-algorithm costs by 2.5 to 290 times with each result proved in
  Lean, for simulation rather than cryptography (F-22): the algorithm clock keeps running. The March 2026 Oratomic
  estimate (F-13) is background and its RSA-2048 figure was misstated in the summary, so it is not used. No agency
  moved a disallowance date. Claim text unchanged.
- M-12 Labs set capability as a control: holds, still provisional, with evidence on both sides. For: OpenAI's chief
  scientist proposed that developers agree not to cross a defined perplexity-based limit until a monitoring or
  understanding milestone is met, and published an internal capability scale with thresholds (F-19, F-20); that
  would make capability a negotiated industry quantity, a larger lever than per-release limits. Against: OpenAI
  published GPT-6 protein-design results that bound in wet-lab tests with no stated access restriction (F-45), and
  attributed its 2026 acceleration mainly to long-term research and compute, with a smaller share from automation
  (F-19), which softens the "labs use their own models to accelerate research" half. One lab's proposal is not
  adoption, so the claim text is unchanged and the evidence is updated. Revisit if a second lab endorses a cap, or
  if the 2027-02-14 test fires.
- No claim retired. No new claim: the real-rate channel (F-35) and model jurisdiction (F-07, F-08) are first-week or
  not-yet-enacted surprises and go to the watching list.

## Watching list changes

- W-02 Customers as lenders to compute suppliers: kept. No second neocloud reported prepayments as a main funding
  source. TrendForce mentions "possible changes to Nvidia's financing support for neoclouds" (F-27) without detail.
- W-03 Provenance of the model and agent supply chain: kept and rewritten to cover jurisdiction. Most leading open
  weights are Chinese, and open weights now carry a majority of tokens on at least one large gateway (F-07). The
  administration is reported to be considering requiring US firms to disclose their use of Chinese models, a
  congressional report accuses PRC developers of harvesting US model outputs, and Cursor told Congress it may phase
  Chinese models out (F-08, secondhand via Fortune). On detection: no single model-diffing method resists both
  evasion attacks (F-52), so the drop condition (detectors improve) is not met. The promotion trigger is widened to
  include a disclosure rule on model origin, and the drop condition now requires detectors that resist both known evasion
  families, replacing the old 91.4 percent true-positive benchmark. Not promoted: nothing has been enacted or required.
- W-04 AI-assisted findings expire and converge: kept. The Riemann claim was certified rather than expired (F-16), so
  it does not bear on the expiry rate; no second expiry study appeared. The convergence half saw no new case. The
  verification-stage evidence went to M-04. The old drop condition (reviewers confirm the disproof) no longer
  discriminates, so it is replaced with a date: dropped if no second expiry study appears by the 2027-01-09 edition.
- W-05 Default monoculture in analysis: dropped. No evidence since it was first seen on 2026-10-31, and its own stated
  deadline was this edition.
- W-06 Agent-initiated payments as a liquidity channel: kept. Governor Waller described agentic commerce as early and
  placed final settlement on central-bank money, with no guidance (F-11, background speech). Worldline reports live
  agentic payments in Europe (F-14). Robinhood's agentic accounts have over 150,000 users and about 30 million agent
  tool calls a day, with no volume disclosed (F-58, background, launch date corrected to 2026-09-29). The
  Uber-based drop condition is replaced with a volume-based one, since Robinhood shows agent activity is not
  negligible in tool calls even if volume is unknown.
- W-07 Robots-as-a-service as an asset-backed market: kept. No humanoid fleet facility appeared.
- W-08 Quantum advantage verified in public: kept. The 123-qubit entanglement result (F-32) and the QEC report (F-12)
  are not advantage claims.
- W-09 Containment failure as legal liability: kept. No new filing or ruling. The Bank of England now cites agent
  control challenges as a financial-stability concern (F-36), which is supervisory attention, not the legal action the
  trigger requires.
- Added W-10 AI capital demand and real rates. The Bank of England says AI investment raises demand for capital and
  "may be contributing to upward pressure on global real interest rates" (F-35, wording corrected), and LSEG frames
  data-center debt issuance alongside a US deficit near 6 percent of GDP as tilting the saving-investment balance
  toward excess investment (F-09, F-35). If it holds, long rates can stay high from AI capital demand even as the
  memory inflation channel eases (F-26, F-27), which M-07, tied to inflation, does not capture. It is hedged and from
  one official source, so it is watched.
- Considered and not added: the US excess-capacity tariff proposal (F-04) is single-source with no government notice;
  ChatGPT Health's training-default change (F-39) is one vendor's terms and bears on no claim; the Claude artifact apps
  with a full-access tier (F-15) fit M-03 and are noted there in spirit but not cited as evidence of failure.

## State table changes

- US Treasury curve: latest shift is the 10-year falling to 4.85 percent on 2026-11-25, the day of the 3.8 percent PCE
  print and the AI selloff, then 4.94 percent on 2026-11-27; the 2-year fell from 4.83 percent on 2026-11-16 to 4.61
  percent on 2026-11-25 (F-54, Treasury par curve). Direction steady. Last reading replaced with Treasury data. The
  fact sheet's "pricing less tightening" inference is not used: no futures reading supports it.
- Fed policy and inflation pulse: latest shift is October PCE at 3.8 percent year on year, core 3.3 percent (F-25),
  with initial claims at 189,000 (F-41). Regime (gradual tightening) and direction (accelerating) unchanged. Reuters
  cited expected increases in December and early 2027 (F-03), but no dated futures reading was found.
- Memory prices: latest shift is TrendForce's cuts to 2027 forecasts after Chinese cloud providers cut orders, a NAND
  downcycle, and DRAM contract declines from 1Q28 (base) or 4Q27 (bear) (F-26, F-27); HP's units fell 29 percent while
  Personal Systems revenue rose 14 percent (F-30). Regime stays at acute shortage: HP's figures meet that level's
  "device volumes falling as average prices rise" criterion, and TrendForce still has DRAM contracts rising in 1Q27.
  Direction stays decelerating. Takeaway updated: the channel has a forecast end date.
- AI credit and data-center debt window: latest shift is the Southeast Asian freeze of China-linked data-center loans
  (F-05), A-rated data-center ABS new-issue spreads widening from about 192 to about 274 bp and AAA CMBS market spreads
  from 142.5 to 174.8 bp (F-10), and the Bank of England's note of sharp widening for lower-quality AI borrowers
  (F-34). Regime stays at narrowing. The "shut" criterion (deals of $250 million or more pulled in consecutive weeks)
  was considered: $250 million-plus China-linked loans were frozen or stalled in two consecutive weeks (Aolani, then
  Bridge), but they were stalled rather than pulled, reported secondhand, confined to one tenant segment, and US
  sponsor deals priced the week before; recorded as the most reasonable reading. Neither LSEG CMBS new-issue figure is
  used (F-10). Direction unchanged (decelerating). The SEC Section 3(a)(79) treatment is noted without a date.
- Hyperscaler cash flow and capex: latest shift is LSEG's forecast swing from +$209 billion to -$189 billion of free
  cash flow between 2025 and 2027, hyperscaler bonds of $279.0 billion year to date (F-09), the BoE's expectation of
  more than $305 billion in 2026, about 8 percent of global investment-grade issuance (F-34), and Dell's AI backlog of
  $132.3 billion (F-29). The 15 and 8 percent shares use different denominators and do not conflict. Regime
  (outside-funded) and direction (steady) unchanged.
- Lab capital loop: latest shift is Anthropic closing at $81.90 on 2026-11-24, 1.3 percent below its $83 offer (F-02),
  the closing figures (F-44, corrected), and the BoE's circular-financing warning (F-34). Direction moves from
  accelerating to steady: no new link was added, and the price fall is stress on the loop, not an unwinding. Regime
  stays at closed loop; the unwinding criterion (a participant cuts exposure or a link defaults) is not met.
- Enterprise AI spend and token price: latest shift is Vercel's 56 percent open-weight token share in August
  (secondhand via Fortune, F-07) and Workday's nearly $150 million of AI new annual contract value (F-31). No new Ramp
  reading. Direction unchanged.
- Power capacity price: none.
- Local permission for data centers: latest shift is McHenry County's 12-month moratorium and Coweta County's
  2027-01-12 referendum on Project Sail (F-28, secondhand). Regime stays at pricing; direction accelerating.
- Nvidia position as central supplier: latest shift is Huang's reinstatement on 2026-11-23 on government input (F-01),
  Moody's outlook moved to stable from positive on 2026-11-18 (F-56, background, paraphrase only, no quote used), and
  Chinese demand falling under export rules (F-26). Regime stays at dominant, contested (the export shock persists);
  direction steady.
- Agent oversight coverage: latest shift is the finding that a monitor's miss rate ranges from 0.5 to 23.0 percent
  with the attack method (F-51) and the BoE's supervisory attention (F-36). Regime stays at partial disclosure; no lab
  published coverage.
- Productivity and labor share: latest shift is Q3 GDP revised to 4.3 percent, led by software investment, and Q3
  profits up $206.0 billion (F-24). No new productivity release; revised Q3 productivity is due in December. Direction
  unchanged.
- Entry-level technical hiring: none. HP and Workday cite AI-linked workforce reductions without headcounts (F-30,
  F-31).
- Post-quantum migration deadlines: latest shift is the FPC making the PQC transition a priority (F-33) and the EU's
  proposed Quantum Act including a PQC transition (F-06). Direction moves from steady to accelerating. Regime stays
  at dated guidance: neither sets dates enforceable on regulated firms. The row's measure now names the EU among the
  tracked sources, since the Quantum Act would be its first legislative vehicle.
- Humanoid deployment: none in the window. Gemini Robotics 2.5 kitting pilots at Mercedes (F-38, background) are
  proofs of concept, not paid fleets.
- No rows added or removed. A row for open-weight and foreign-model share of enterprise tokens was considered and not
  added: the only reading is secondhand and the estimates range from 19 to 56 percent; it stays under W-03.

## Continuing shifts

- M-02: oversight keeps narrowing; monitor miss rates now depend on how they are measured.
- M-03: written rules fail and deterministic gates hold, now shipped as lab tooling.
- M-04: a machine-checked Riemann proof was accepted before humans understood it; AI review still passes wrong
  patches.
- M-07: growth revised up on software investment, inflation at 3.8 percent, and yields fell on the AI selloff.
- M-08: a second central bank names circular AI financing; Anthropic trades just below its offer.
- M-11: the policy clock now runs through financial-stability and EU legislative channels.
- M-01, M-05, M-06, M-10 and M-12 held, with M-12's evidence on both sides.
