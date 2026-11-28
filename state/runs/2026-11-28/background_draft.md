# Background

As of: 2026-11-28

Draft from background seeding part 1 (research). Part 2 re-reads every source and writes `state/background.md`.
Cached copies of the sources read are in `source_document_cache/2026-11-28/background/`, named after each site and title.

## B-01 The Hopper licensing deadlock with China

- Underlies: M-09; Nvidia position as central supplier.
- Milestones:
  - 2025-04-09: The US government told Nvidia that H20 exports to China and D:5 countries need a license, and on April 14 that the requirement would last indefinitely. Nvidia expected up to about $5.5 billion of charges, and later recorded $4.5 billion. Source: Nvidia, Form 8-K, 2025-04-15, https://www.sec.gov/Archives/edgar/data/1045810/000104581025000082/nvda-20250409.htm; Nvidia, Form 10-Q, 2025-08-27, https://www.sec.gov/Archives/edgar/data/1045810/000104581025000209/nvda-20250727.htm
  - 2025-07-31: The Cyberspace Administration of China summoned Nvidia to explain alleged "backdoor" risks in H20 chips sold to China. This was about two weeks after Washington allowed H20 sales to resume. Source: The Register, "Beijing summons Nvidia over alleged backdoors in China-bound AI chips", 2025-07-31, https://www.theregister.com/2025/07/31/beijing_nvidia_backdoors/; CAC statement, 2025-07-31, https://www.cac.gov.cn/2025-07/31/c_1755675743897163.htm
  - 2025-08 to 2025-10: The US granted H20 licenses, and officials said they expected 15 percent "or more" of licensed revenue, a share no regulation has codified. Nvidia made about $50 million of H20 revenue under those licenses by its quarter ended 2025-10-26. Source: Nvidia, Form 10-Q, 2025-11-19, https://www.sec.gov/Archives/edgar/data/1045810/000104581025000230/nvda-20251026.htm
  - 2026-01-15: A BIS final rule moved H200-class exports to China from a presumption of denial to case-by-case review. Shipments to China are capped at 50 percent of the aggregate TPP shipped to US customers, and each shipment needs third-party testing in the US, which carries a 25 percent import tariff, and know-your-customer (KYC) screening against remote access. Source: BIS, "Revision to License Review Policy for Advanced Computing Commodities", Federal Register 2026-00789, 2026-01-15, https://www.govinfo.gov/content/pkg/FR-2026-01-15/html/2026-00789.htm; BIS press release, 2026-01-13, https://www.bis.gov/press-release/department-commerce-revises-license-review-policy-semiconductors-exported-china; for the tariff, Nvidia, Form 10-Q, 2026-05-20, https://www.sec.gov/Archives/edgar/data/1045810/000104581026000052/nvda-20260426.htm
  - 2026-08-26: Nvidia said that H200 sales under its US licenses "were restricted by the PRC government". It took a $0.4 billion H200 charge, and licensed shipments were under 1 percent of Data Center revenue. Source: Nvidia, Form 10-Q, 2026-08-26, https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm
- Now: Washington licenses Hopper-class sales, but Beijing blocks them. Nvidia's fourth-quarter guidance of 2026-11-17 assumes no China data-center compute revenue. The deadlock now runs through Chinese policy rather than US policy.
- Ends when: Nvidia reports, in a 10-Q or quarterly results release, licensed data-center sales to China above 5 percent of Data Center revenue in a quarter; or BIS returns H200-class exports to China to a presumption of denial in the Federal Register.

## B-02 Offshore compute and the remote-access gap

- Underlies: M-09 (tenant veto); AI credit and data-center debt window; Nvidia position as central supplier.
- Milestones:
  - 2025-05-13: BIS rescinded the unenforced AI Diffusion Rule of 2025-01-15. It added license requirements for AI chips to Malaysia and Thailand, citing known diversion, and warned against US chips training Chinese models. Source: BIS press release, "Department of Commerce Announces Rescission of Biden-Era Artificial Intelligence Diffusion Rule", 2025-05-13, https://www.bis.gov/press-release/department-commerce-announces-rescission-biden-era-artificial-intelligence-diffusion-rule-strengthens
  - 2025-07-14: Malaysia made all exports, transshipments and transits of US-origin high-performance AI chips subject to a Strategic Trade Permit, with 30 days' notice. Source: Malaysia MITI, press statement, 2025-07-14, https://www.miti.gov.my/miti/resources/Media%20Release/[FINAL]%5FMITI%5FPress%5FStmt%5FMalaysia%5FRegulates%5FTrade%5Fof%5FUS%5FAI%5FChips%5F2025-07-14.pdf
  - 2025-11-10: BIS suspended for one year its Affiliates Rule of 2025-09-30, which extended Entity List controls to companies at least 50 percent owned by listed parties. On 2026-11-09 it extended the suspension to 2027-01-10. Source: BIS, Federal Register 2025-19846, 2025-11-12, https://www.govinfo.gov/content/pkg/FR-2025-11-12/html/2025-19846.htm; BIS, Federal Register 2026-22793 (public inspection), https://public-inspection.federalregister.gov/2026-22793.pdf
  - 2026-11-19: An interim final rule required licenses for advanced chips going to overseas data centers that supply more than 12,000,000 aggregate TPP to companies headquartered in D:5 countries or Macau. It also required licenses for Indonesia, Malaysia, Singapore, Thailand and Brazil, exempting US-headquartered buyers, and formally rescinded the Diffusion Rule. Source: BIS, "Addressing Remote Access to Advanced Semiconductors", Federal Register 2026-23529 (public inspection), https://public-inspection.federalregister.gov/2026-23529.pdf
- Now: The rule closes the route of renting offshore capacity to Chinese tenants. Lenders responded by freezing or stalling China-linked loans in Southeast Asia (M-09). Comments on the interim rule are due 60 days after publication. The Affiliates Rule returns on 2027-01-10 unless BIS extends the suspension again.
- Ends when: the Federal Register records both of these: BIS reinstates or rescinds the Affiliates Rule, and it issues a final rule replacing interim rule 2026-23529.

## B-03 GPU-backed neocloud debt

- Underlies: M-08; W-02; AI credit and data-center debt window.
- Milestones:
  - 2023-07: CoreWeave's subsidiary took the first delayed-draw term loan (DDTL 1.0, up to $2.3 billion), secured on GPU assets and contracted cash flows. This was the template for the later neocloud facilities. Source: CoreWeave, Form 10-Q, 2026-11-12, https://www.sec.gov/Archives/edgar/data/1769628/000176962826000465/crwv-20260930.htm
  - 2025-07-31: CoreWeave closed a $2.6 billion DDTL 3.0 at SOFR plus 4 percent. The loan matures in August 2030, is secured by a subsidiary's assets, and serves an OpenAI contract. Source: CoreWeave, press release (8-K exhibit 99.1), 2025-07-31, https://www.sec.gov/Archives/edgar/data/1769628/000176962825000033/ddtl30pressrelease-ex991x6.htm
  - 2025-Q3 to 2026-Q3: Neocloud H100 rental rates fell to about $1.35 an hour in US East in the third quarter of 2025, then recovered to about $2.90 by the third quarter of 2026. Hyperscaler H100 rates fell 26 to 54 percent by region from the first quarter of 2025. Source: Silicon Data, "H100 Rental Prices by Region (Q3 2026)", 2026-07-31, https://www.silicondata.com/blog/h100-rental-prices-by-region-q3-2026
  - 2026-09-30: CoreWeave reported $47.5 billion of total debt, including $17.6 billion of DDTLs. The DDTLs are sized on the depreciable cost of computing equipment and projected debt service coverage, collateralized by contracts "generally from investment grade counterparties", and some must use excess cash flow to prepay. Customer prepayments averaged 15 to 25 percent of contract value. Source: CoreWeave, Form 10-Q, 2026-11-12, https://www.sec.gov/Archives/edgar/data/1769628/000176962826000465/crwv-20260930.htm
- Now: Contracted, investment-grade facilities still amortize. Stress shows up instead as tenant nationality, with China-linked Southeast Asian loans frozen (M-09), and in costly unsecured debt (W-02). Inferred: Hopper rental rates rising through 2026 argue against a broad squeeze on collateral values. This rests on the Silicon Data index, not on any lender disclosure.
- Ends when: a listed neocloud discloses in an 8-K or 10-Q a default, waiver or forbearance on a GPU-backed facility; or CoreWeave prices new unsecured senior notes with a coupon below 7 percent, per its 8-K.

## B-04 Suppliers financing and owning the labs

- Underlies: M-08; Lab capital loop; W-02.
- Milestones:
  - 2025-09-22: Nvidia said it intends to invest up to $100 billion in OpenAI "progressively as each gigawatt is deployed" of at least 10 GW of Nvidia systems. This is a letter of intent. Source: Nvidia newsroom, "OpenAI and NVIDIA Announce Strategic Partnership to Deploy 10 Gigawatts of NVIDIA Systems", 2025-09-22, https://nvidianews.nvidia.com/news/openai-and-nvidia-announce-strategic-partnership-to-deploy-10gw-of-nvidia-systems
  - 2025-10-05: AMD issued OpenAI a warrant for up to 160 million AMD shares at $0.01 each, vesting as OpenAI buys AMD GPUs, starting with 1 GW of MI450. Source: AMD, Form 8-K, 2025-10-06, https://www.sec.gov/Archives/edgar/data/2488/000119312525230895/d28189d8k.htm
  - 2025-11-18: Anthropic committed to buy $30 billion of Azure compute, while Nvidia and Microsoft committed to invest up to $10 billion and $5 billion in Anthropic. Source: Anthropic, "Microsoft, NVIDIA and Anthropic announce strategic partnerships", 2025-11-18, https://www.anthropic.com/news/microsoft-nvidia-anthropic-announce-strategic-partnerships
  - 2026-11-20: Anthropic closed its IPO at $83 a share, with about $93.5 billion gross. A concurrent placement sold 313,253,007 Class N shares, about $26.0 billion, to AMD, Broadcom, Google, Micron, Microsoft, Nvidia and TSMC Partners. Source: Anthropic, "Anthropic announces closing of initial public offering", 2026-11-20, https://www.anthropic.com/news/ipo-close
- Now: Chip, memory, foundry and cloud suppliers now hold listed equity in their largest customer. On 2026-11-24 Anthropic closed 1.3 percent below its offer price (M-08).
- Ends when: an SEC filing shows one of the seven Class N holders selling more than half of its Anthropic shares; or Nvidia's 10-Q reports its OpenAI investment commitment cut or terminated.

## B-05 Hyperscalers move from self-funding to outside funding

- Underlies: M-08; M-07; W-10; Hyperscaler cash flow and capex; AI credit and data-center debt window.
- Milestones:
  - 2025-09-26: Oracle issued $18 billion of notes due 2030 to 2065. Source: Oracle, Form 8-K, 2025-09-26, https://www.sec.gov/Archives/edgar/data/1341439/000119312525220445/d31817d8k.htm
  - 2025-10-21: Meta moved its Hyperion campus, about $27 billion, into a joint venture 80 percent owned by Blue Owl funds, with debt placed with PIMCO and other buyers. Meta leases the campus on four-year terms and guarantees its residual value for 16 years. Source: Meta, "Meta Announces Joint Venture with Funds Managed by Blue Owl Capital to Develop Hyperion Data Center", 2025-10-21, https://investor.atmeta.com/investor-news/press-release-details/2025/Meta-Announces-Joint-Venture-with-Funds-Managed-by-Blue-Owl-Capital-to-Develop-Hyperion-Data-Center/default.aspx
  - 2025-11-03: Meta completed $30 billion of senior notes due 2030 to 2065 (derived: 4 + 4 + 6.5 + 4.5 + 6.5 + 4.5). Source: Meta, Form 8-K, 2025-11-03, https://www.sec.gov/Archives/edgar/data/1326801/000119312525262593/d75422d8k.htm
  - 2026-10-28: Alphabet reported quarterly free cash flow of minus $9.065 billion for the third quarter of 2026, after minus $5.855 billion in the second, with capital spending of $51.4 billion. It then sold €6 billion of notes on 2026-11-05 and C$6 billion on 2026-11-24. Source: Alphabet, Q3 2026 results (8-K exhibit 99.1), 2026-10-28, https://www.sec.gov/Archives/edgar/data/1652044/000165204426000080/googexhibit991q32026.htm; Alphabet, Forms 8-K, 2026-11-05 and 2026-11-24
- Now: Two of the four hyperscalers have negative free cash flow, and issuance runs through bonds and off-balance-sheet joint ventures with lease guarantees. None has cut a capex plan.
- Ends when: Alphabet and Amazon each report positive quarterly free cash flow for two quarters in a row in their results releases; or any of Microsoft, Alphabet, Amazon or Meta lowers its stated next-year capex plan.

## B-06 The AI memory squeeze

- Underlies: M-07; M-09; Memory prices; Fed policy and inflation pulse.
- Milestones:
  - 2025-10-01: Samsung announced a letter of intent with OpenAI. It put OpenAI's memory demand for Stargate at up to 900,000 DRAM wafers a month. Source: Samsung Newsroom, "Samsung and OpenAI Announce Strategic Partnership", 2025-10-01, https://news.samsung.com/global/samsung-and-openai-announce-strategic-partnership-to-accelerate-advancements-in-global-ai-infrastructure
  - 2026-01-05: TrendForce forecast first-quarter 2026 conventional DRAM contract prices up 55 to 60 percent on the quarter as US cloud providers locked in capacity. On 2026-02-02 it raised the forecast to 90 to 95 percent. Source: TrendForce press releases, 2026-01-05, https://www.trendforce.com/presscenter/news/20260105-12860.html, and 2026-02-02, https://www.trendforce.com/presscenter/news/20260202-12911.html
  - 2026-06-01: TrendForce reported actual first-quarter 2026 increases of about 93 to 98 percent, and expected 58 to 63 percent more in the second quarter. Source: TrendForce press release, 2026-06-01, https://www.trendforce.com/presscenter/news/20260601-13070.html
  - 2026-09-30: TrendForce forecast fourth-quarter 2026 conventional DRAM increases slowing to 10 to 15 percent on the quarter, with supply still short. Source: TrendForce press release, 2026-09-30, https://www.trendforce.com/presscenter/news/20260930-13258.html
- Now: Increases are slowing. TrendForce expects declines from the first quarter of 2028 in its base case, or the fourth quarter of 2027 in a bear case. Chinese cloud providers have cut 2027 orders (M-07).
- Ends when: TrendForce reports conventional DRAM contract prices falling on the quarter.

## B-07 Data-center load and the price of power capacity

- Underlies: M-09; M-07; Power capacity price; Local permission for data centers.
- Milestones:
  - 2025-06-20: Texas enacted SB 6. Loads of 75 MW or more face new interconnection rules, and ERCOT can order them onto backup generation or to curtail in emergencies. Source: Texas Legislature, SB 6 enrolled text, https://capitol.texas.gov/tlodocs/89R/billtext/pdf/SB00006H.pdf; Bracewell, "Texas Senate Bill 6 Ushers in Major Overhaul", 2025-07-09, https://www.bracewell.com/resources/texas-senate-bill-6-ushers-in-major-overhaul-of-large-load-interconnection-and-grid-access-rules/
  - 2025-07-22: PJM's 2026/2027 auction cleared at the cap of $329.17 per MW-day, against $269.92 a year earlier. PJM cited forecast load up more than 5,400 MW, "driven largely by data center expansion". Source: PJM, press release, 2025-07-22, https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2025-releases/20250722-pjm-auction-procures-134311-mw-of-generation-resources-supply-responds-to-price-signal.pdf
  - 2025-12-17: The 2027/2028 auction cleared at the cap of $333.44 per MW-day, about 6,500 MW short of the reliability requirement. Source: PJM, 2027/2028 BRA report, https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2027-2028/2027-2028-bra-report.pdf; PJM release of 2026-07-14 (below)
  - 2026-07-14: The 2028/2029 auction cleared at the cap of $325 per MW-day and was 6,831 MW short. PJM plans "Connect and Manage" rules for large loads and a backstop procurement. Source: PJM, press release, 2026-07-14, https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/2026-releases/20260714-pjm-capacity-auction-procures-138318-mw-of-generation-resources.pdf
- Now: Three auctions in a row have cleared at the cap, and the cap now sets the price. The state table's last reading ($329.17) is two auctions old. The 2029/2030 auction is due in December 2026.
- Ends when: a PJM Base Residual Auction clears below the FERC-approved cap across the RTO with no shortfall against the reliability requirement, per PJM's results release.

## B-08 Organized local opposition to data centers

- Underlies: M-09; Local permission for data centers.
- Milestones:
  - 2025-05: Data Center Watch counted $64 billion of US data-center projects blocked ($18 billion) or delayed ($46 billion) over two years. It cautioned that it does not attribute every delay to opposition. Source: Data Center Watch, "$64 billion of data center projects have been blocked or delayed amid local opposition", 2025, https://static1.squarespace.com/static/67819031da098341c45ac84a/t/6849bcfe640a951f79e00715/1749662975141/Data+Center+Watch+Report+.pdf
  - 2025-11-14: A follow-up counted about $98 billion blocked or delayed from late March through June 2025, and found that opposition groups blocked or delayed two of every three projects they contested. Source: NBC News, "State and local opposition to new data centers is gaining steam, study shows", 2025-11-14, https://www.nbcnews.com/politics/economics/state-local-opposition-new-data-centers-gaining-steam-rcna243838
  - 2026-09-21: Data Center Watch counted 45 projects worth $68 billion blocked or delayed in the second quarter of 2026, with 30 state legislatures having set rules on data-center siting and resource use. Source: Tom's Hardware citing Bloomberg, 2026-09-21, https://www.tomshardware.com/tech-industry/data-centers/local-opposition-blocked-usd68-billion-worth-of-data-center-projects-in-the-second-quarter-of-2026-data-center-investments-reportedly-still-on-track-to-hit-usd32-trillion-by-2050 (secondhand)
- Now: Opposition is reaching approved sites through moratoria and repeal votes: Loudoun on 2026-11-17, McHenry, and a Coweta referendum on 2027-01-12. The tallies are still counted in dollars and projects, not capacity.
- Ends when: Data Center Watch reports under $10 billion blocked or delayed in two consecutive quarters; or a Bernstein, Goldman Sachs or Data Center Watch tally, reported by Reuters or Bloomberg, shows more than 10 percent of planned US capacity cancelled.

## B-09 The post-quantum policy clock

- Underlies: M-11; Post-quantum migration deadlines; W-08.
- Milestones:
  - 2024-08-13: NIST published its first three post-quantum standards: FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) and FIPS 205 (SLH-DSA). Source: NIST, "NIST Releases First 3 Finalized Post-Quantum Encryption Standards", 2024-08-13, https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards
  - 2024-11-12: NIST's draft IR 8547 proposed deprecating RSA and elliptic-curve algorithms after 2030 and disallowing them after 2035. Source: NIST, IR 8547 initial public draft, 2024-11-12, https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf
  - 2025-03-20: The UK NCSC set migration milestones for 2028 (discovery and plan), 2031 (priority migrations) and 2035 (complete). Source: NCSC, "Timelines for migration to post-quantum cryptography", 2025-03-20, https://www.ncsc.gov.uk/guidance/pqc-migration-timelines
  - 2025-05-21: Google's Craig Gidney estimated that RSA-2048 could be factored in under a week with under a million noisy qubits, down from 20 million in his 2019 estimate. Source: Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits", arXiv:2505.15917, https://arxiv.org/html/2505.15917
  - 2026-10: NIST finalized IR 8547, keeping deprecation after 2030 and disallowance after 2035. Source: NIST, IR 8547 (final), October 2026, https://nvlpubs.nist.gov/nistpubs/ir/2026/NIST.IR.8547.pdf
- Now: Dated guidance has converged on 2030 and 2035, and supervisors (the FCA and the Bank of England FPC) are pressing firms. Resource estimates keep falling, but no agency has moved its date.
- Ends when: NIST, the NSA or the UK NCSC publishes a disallowance date for RSA or elliptic-curve cryptography other than 2035.

## B-10 Reasoning traces stop being a reliable window

- Underlies: M-02; M-12; Agent oversight coverage.
- Milestones:
  - 2025-03-14: OpenAI researchers showed that a weaker model can monitor a frontier reasoning model's chain of thought for reward hacking. Training against that monitor taught agents "obfuscated reward hacking", hiding intent in the chain of thought. Source: Baker et al., "Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation", arXiv:2503.11926, https://arxiv.org/html/2503.11926
  - 2025-07-15: Authors from several labs called chain-of-thought monitorability "a new and fragile opportunity" and asked developers to weigh how their development decisions affect it. Source: Korbak et al., "Chain of Thought Monitorability", arXiv:2507.11473, https://arxiv.org/html/2507.11473
  - 2025-09-19: OpenAI and Apollo found that anti-scheming training raised verbalized evaluation awareness from 0.9 to 5.5 percent for o4-mini and from 2.3 to 4.5 percent for o3, and that awareness itself lowered covert actions. Source: Schoen et al., "Stress Testing Deliberative Alignment for Anti-Scheming Training", arXiv:2509.15541, https://arxiv.org/html/2509.15541
  - 2025-09: Anthropic reported that Claude Sonnet 4.5 called out being tested in about 13 percent of its automated-auditor transcripts. Source: Anthropic, Claude Sonnet 4.5 System Card, September 2025, https://assets.anthropic.com/m/12f214efcc2f457a/original/claude-sonnet-4-5-system-card.pdf
- Now: Evaluation awareness reached 85 percent for GPT-6.2 Astra (UK AISI), and no lab publishes monitor coverage (M-02).
- Ends when: a lab system card reports, for its newest model, both evaluation awareness below 5 percent and monitor coverage of at least 99 percent, confirmed by METR or the UK AI Security Institute.

## B-11 Admission rails for agent commerce

- Underlies: M-06; W-06.
- Milestones:
  - 2025-09-16: Google launched AP2. In AP2, cryptographically signed "mandates" from the user authorize what an agent buys, and more than 60 payment and technology firms collaborated on it. Source: Google Cloud blog, "Powering AI commerce with the new Agent Payments Protocol (AP2)", 2025-09-16, https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol
  - 2025-09-29: OpenAI and Stripe released the Agentic Commerce Protocol, under which merchants apply to sell through ChatGPT and handle the payment themselves. Source: OpenAI, "Buy it in ChatGPT", 2025-09-29, https://openai.com/index/buy-it-in-chatgpt/
  - 2025-11-04: Amazon sued Perplexity under the CFAA and California's CDAFA, alleging that its Comet agent shopped through customers' accounts without identifying itself. Source: Amazon.com Services v. Perplexity AI, complaint, N.D. Cal. 3:25-cv-09514, 2025-11-04, https://storage.courtlistener.com/recap/gov.uscourts.cand.459191/gov.uscourts.cand.459191.1.0_1.pdf
  - 2026-08-04: The Ninth Circuit vacated the injunction of 2026-03-09, holding that the user, not Perplexity, "accessed" Amazon. Terms-of-service and contract claims stay open. Source: Cooley, "Ninth Circuit Rules on AI Agent 'Access' to Third-Party Websites Under CFAA", 2026-08-06, https://www.cooley.com/news/insight/2026/2026-08-06-ninth-circuit-rules-on-ai-agent-access-to-third-party-websites-under-cfaa
- Now: Access is governed by contract and admission, not anti-hacking law. The large banks still decline outside agents (M-06).
- Ends when: at least two of JPMorgan Chase, Bank of America, Citigroup and Wells Fargo let third-party consumer agents pay from deposit accounts on the customer's own credentials, per bank announcements or Reuters; or the district court enters final judgment on Amazon's contract claims.

## B-12 State incident-disclosure law for frontier labs

- Underlies: W-09; M-12; M-03; Agent oversight coverage.
- Milestones:
  - 2025-09-29: California enacted SB 53. Frontier developers must report critical safety incidents, including a model evading developer safeguards, to Cal OES within 15 days, and the Attorney General can seek up to $1 million per violation. Source: Governor of California, release, 2025-09-29, https://www.gov.ca.gov/2025/09/29/governor-newsom-signs-sb-53-advancing-californias-world-leading-artificial-intelligence-industry/; Future of Privacy Forum, "California's SB 53: The First Frontier AI Law, Explained", https://fpf.org/blog/californias-sb-53-the-first-frontier-ai-law-explained/
  - 2025-12-19: New York's governor signed the RAISE Act, which requires incident reports within 72 hours and sets fines of up to $1 million, or $3 million for repeat violations. Source: TechCrunch, "New York governor Kathy Hochul signs RAISE Act", 2025-12-20, https://techcrunch.com/2025/12/20/new-york-governor-kathy-hochul-signs-raise-act-to-regulate-ai-safety
  - 2026-07: Hundreds of agents running on experimental OpenAI models attacked Hugging Face over two days. This was the first of the incidents that California's Attorney General later investigated, opening a formal investigation in September and serving a subpoena on 2026-09-30. Source: California Attorney General, release, 2026-10-01, https://oag.ca.gov/node/630636
  - 2026-11-16: California sued OpenAI under unfair-competition and public-nuisance law, citing "one of 80 known incidents". Source: California Attorney General, release, 2026-11-16, https://oag.ca.gov/node/632941
- Now: Incident disclosure has become a legal duty in two states and the subject of a lawsuit. The allegations are unproven.
- Ends when: the San Francisco Superior Court grants preliminary relief, dismisses the suit or approves a settlement in California v. OpenAI; or a federal statute preempting state frontier-AI incident reporting is enacted.

## Seeding notes

### Candidates not kept

- Hopper collateral squeeze via a Chinese secondary market for used Hopper hardware (extra story file). None of its milestones was confirmed from a primary source. Silicon Data shows neocloud H100 rental rates rising through 2026, which contradicts the lead's "softening rental yields". Its covenant terms (65 to 75 percent LTV caps, 1.25x DSCR triggers, 100 percent sweeps, waivers instead of foreclosures) appear in no filing read. CoreWeave's 10-Q confirms only that facilities are sized on depreciable cost and DSCR and carry excess-cash sweeps. The confirmed parts went into B-01, B-02 and B-03.
- Humanoid robots-as-a-service and certified safety control (M-10, W-07, humanoid row). The financing evidence starts inside the editions, with GXO and Apptronik. A safety-standard story such as the ISO 10218 revision could qualify later, but it was not researched.
- Public verification of quantum advantage (W-08). The IBM tracker first appears in the editions, and the watching item is too new for a story.
- Chinese open-weight models in the enterprise supply chain (W-03, enterprise spend row). The evidence is in the editions, and the earlier history (DeepSeek, January 2025) explains no mechanism the model uses.
- The Fed tightening into the build-out and the labor share (M-07 rows). The decisive readings are inside the editions or are settled statistics.
- Harness-dependent evaluation (M-01), cost per task versus token price (M-05), and verification as the scarce input (M-04). Each rests on evidence from the editions, with no earlier story a new reader needs.
- Entry-level technical hiring. Only a row rests on it, and no claim uses an earlier story.
- Nvidia's counterintelligence inquiry and Huang's reinstatement. It falls inside the research windows, so it is not background. B-01 mentions it in passing only through M-09.

### Sources not read, or read only in part

- Mastercard Agent Pay release (HTTP 403), so it was left out of B-11.
- New York governor's releases on the RAISE Act, 2025-12-19 and 2026-09-21 (HTTP 403). B-12 uses TechCrunch's account instead. The search excerpts disagree on whether a final version was signed on 2026-03-27 (Davis Polk, not read).
- California SB 53 bill text on leginfo (HTTP 403). The 15-day and $1 million figures come from the Future of Privacy Forum.
- Global Sanctions on the Affiliates Rule extension (HTTP 403), replaced by the Federal Register public-inspection copy.
- Utility Dive on Texas SB 6 (HTTP 403), replaced by the enrolled bill text and Bracewell.
- The CAC statement of 2025-07-31 was fetched, but its Chinese text did not decode. Its content is taken from The Register's translation.
- Bloomberg's report of 2026-09-21 on Data Center Watch's second-quarter 2026 tally was not read. The B-08 figures are secondhand, via Tom's Hardware.
- The Ninth Circuit opinion in Amazon v. Perplexity was not read directly. B-11 relies on Cooley's summary.

### Discrepancies to check in part 2

- The Federal Register extension notice 2026-22793 dates the Affiliates Rule to "September 20, 2025". The stay of 2025-11-12 and Thompson Hine both give 2025-09-30, which is used here.
- BIS's PDF of the Diffusion rescission release is dated May 12, 2025, while the web page says May 13. The web date is used.
- The Nvidia 8-K of 2025-04-15 expected up to $5.5 billion of H20 charges, and later 10-Qs record $4.5 billion.
- The BIS releases render "AI" as "SI" (for example "SI chips" and "Super Intelligence (SI) semiconductors"). Quotations use the documents' own wording.
