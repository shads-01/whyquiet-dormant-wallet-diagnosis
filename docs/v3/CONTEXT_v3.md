# CONTEXT v3 — AI Hackathon 2026 (DIU CPC × upay)

> Replaces `CONTEXT.md` and `CONTEXT_v2.md`. Earlier-round docs are historical only.
> Source of truth for this file: `AI_Hackathon_2026_DIU_CPC_x_upay_Student_Guideline_Official_docx.pdf` (repo root) unless marked otherwise.

---

## 0. STOP — one unresolved conflict

**Track 01 (Trust & Risk Intelligence) is officially a fraud/scam/account-takeover/mule track.** The official PDF lists as challenge directions: real-time transaction risk scoring, behavioral anomaly detection, **account takeover intelligence**, **money-mule and suspicious-network discovery**, agent risk intelligence, **scam intelligence**.

**But our own banned list says: fraud, scam, account takeover, mule are banned.**

These cannot both stand. Track 01 is 1 of 7 tracks and is arguably the best-documented one in the brief.

- **Decision needed before ideation proceeds:** is Track 01 off-limits for us, or was "banned" about a *framing* (e.g. don't build a bare classifier dashboard) rather than the topic?
- Everything below assumes **Tracks 02–07 are safe** and Treats Track 01 as **conditionally available**.

---

## 1. Situation

| Fact | Value | Source |
| --- | --- | --- |
| Format | T+0 → T+72h initial dev, then pre-evaluation, then on-site day with assigned new requirements, then 90-min final eval | rules §3, §8 |
| **Time remaining** | **~24 hours of the 72h initial development window** | user |
| Team | Max 3 members, single-member permitted | hackathon rules §2 |
| Teams competing | First 100 registered teams; 25 extra slots opened 16 Sep 2026 | hackathon page, announcements |
| Registration | Closed 19 Sep 2026, entry fee ৳750 | hackathon page |
| Prize pool (this track) | ৳130,000 across 6 teams (50k/30k/20k/15k/10k/5k) | hackathon page |
| Prize pool (festival) | ৳335,000 | aidevfest.top |
| Venue | Daffodil International University, Daffodil Smart City, Savar, Dhaka | aidevfest.top |
| upay's role | **Title Partner** of AI Dev Fest 2026 | aidevfest.top |
| Organizer | DIU Computer & Programming Club (DIU-CPC), Dept. of CSE, DIU | aidevfest.top |

**Correction to earlier assumptions:** this is not a single 48h sprint. It is 72h of initial development, then a second on-site phase where judges hand out *new requirements* we must integrate, then a 90-minute final evaluation. Final ranking = marks from **both** evaluations.

**Implication:** build modular and demo-able. A monolith cannot absorb a requirement drop on the final day.

---

## 2. Rubric (official, page 11)

| Criterion | Weight | "What good looks like" (verbatim) |
| --- | --- | --- |
| Problem relevance | 20% | Solves a real and meaningful customer/business problem |
| AI/ML depth | 20% | AI is material to the solution and technically credible |
| Business/customer impact | 20% | Clear, measurable value and plausible economics |
| Prototype quality | 15% | Working end-to-end experience, not only slides |
| Innovation | 10% | Distinctive insight or differentiated product idea |
| Scalability & integration | 10% | Believable path toward real systems and future data |
| Responsible AI & security | 5% | Privacy, explainability, fairness, and safety considered |

Shape: **60 points in relevance + AI depth + business impact.** A beautiful prototype with thin ML loses.

Note the official column name is **"Problem relevance"**, not just "relevance".

---

## 3. Tracks (official, pages 3–7)

| # | Track | Direction |
| --- | --- | --- |
| 01 | Trust & Risk Intelligence | fraud/scam/ATO/mule/agent risk — **see conflict in §0** |
| 02 | Customer Intelligence | Customer 360, churn, segmentation, next-best-action, CLV, personalized service recs |
| 03 | **Customer Innovation & Financial Independence** (flagship) | financial health coach, savings planner, spending companion, cash-flow forecasting, goal copilot, inclusive assistant, financial literacy personalizer, responsible credit readiness |
| 04 | Growth & Campaign Intelligence | next-best-offer, campaign response, **uplift modeling**, budget optimizer, lifecycle orchestration, offer fatigue, experiment intelligence |
| 05 | Merchant & Agent Intelligence | merchant demand forecasting, merchant growth/churn, benchmarking, **agent liquidity forecasting**, location intelligence |
| 06 | Operations & Service Intelligence | dispute investigation, support copilot, complaint intelligence, workflow automation |
| 07 | Open Innovation | "Any responsible AI solution for an MFS challenge" |

### Track 03 — the flagship, worth extra attention

Explicitly framed as the **differentiated** track. Big question: *"How might an MFS platform help customers become more financially confident and independent — not merely more active users?"*

The doc names worked example experiences, which are effectively free product specs:
- "I need to save ৳30,000 in six months" → target plan + feasible monthly contribution + trade-offs
- "Why do I always run short before month-end?" → recurring cash-flow pattern, weeks with largest outflows
- "How can I reduce cash-outs?" → where digital alternatives could replace repetitive cash withdrawal
- "I don't understand these transactions" → simple categories, plain-language insights

Guardrail the doc states explicitly: **empower the customer. Avoid manipulative recommendations, hidden fees, or designs encouraging unnecessary spending.**

### Track 04 — the sharpest ML signal

> "A mature project should distinguish correlation from incremental impact. *'This customer will transact' is weaker than 'this customer is likely to transact because of the offer.'*"

Uplift modeling / causal reasoning is called out by name. Most teams will do response prediction and miss this.

---

## 4. Data rule (official, §11) — confirmed

- Synthetic, public, or self-generated data only. **Production upay data is not required and not provided.**
- Make it realistic enough to reproduce meaningful patterns, but clearly synthetic.
- Inject known patterns for testing: normal behavior, anomalies, seasonal effects, campaign response, churn.
- **Document every synthetic assumption.**
- **Never use real personally identifiable information.**
- **Keep a clean test set not used to train.**

Sanctioned synthetic domains: customers + basic behavioral attributes; transactions + types; merchants + categories; agents + activity; devices, locations, timestamps, channels; campaigns/offers/treatment-control labels; cases, complaints, operational events.

Post-hackathon controlled validation is a *possibility*, explicitly "not a promise of access or deployment".

**Do not impose any data rule stricter than this.** Data availability is not grounds to drop an idea.

---

## 5. What is explicitly *not* rewarded (official §1)

> "The objective is **not** to produce a generic chatbot, a dashboard, or a model accuracy score."

Banned-by-official (confirmed): generic chatbot, generic dashboard, accuracy-score-as-the-product.

Also banned, self-imposed by us this round: phishing, spoofing, deepfake, AML, OCR of paper documents, Bangla ASR as the main idea, generic churn dashboard.

---

## 6. Architecture expectations (official §12)

Explicit judge-visible expectations:

- Separate **data preparation** from **model inference** where possible.
- Keep **business rules distinct** from ML predictions.
- Make model outputs **traceable and explainable**.
- Design APIs so the prototype could later connect to a real backend.
- **Do not put sensitive decision logic entirely inside a free-form LLM prompt.**

Suggested stack (reference, not required): Python/Pandas/PostgreSQL · scikit-learn/XGBoost/LightGBM/PyTorch · LLM+RAG · FastAPI/Node · React/Next.js · logs/metrics/dashboards.

## 7. Responsible AI minimums (official §14)

| Principle | Minimum expectation |
| --- | --- |
| Privacy | synthetic/public/self-generated only |
| Explainability | show main reasons behind important predictions |
| Fairness | check behaviour differs across relevant groups |
| Security | consider adversarial manipulation, prompt injection, data leakage, access control |
| Human oversight | high-impact actions allow human review |
| Transparency | separate predictions, assumptions, generated explanations |
| No harmful automation | do not autonomously approve/deny consequential financial decisions |

## 8. Product-readiness checklist (official §13)

A project is a *product candidate* only if: problem is frequent or economically meaningful · AI beats a simple deterministic rule · there is a clear action after the prediction · benefit is measurable · model is validatable with future real data · privacy/fairness/explainability/security addressable · integrates into a real digital-service workflow.

**"AI adds value beyond a simple deterministic rule"** is the line most weak ideas cross badly.

## 9. Mandatory submission artifacts (rules §5–§7)

- **Public GitHub repo**, continuous commit history across *both* phases. A single final upload fails.
- **README.md** with all of: project overview · features · tech stack · requirements · install/setup · env vars (placeholders, no secrets) · run & build commands · **live deployment URL** · testing instructions.
- **Video demo** — how it works, features, AI components, real-life impact.
- **Project report** — problem, idea, solution, key features, AI approach, real-life impact.
- Live deployment must be reachable by judges.

**The video and README are deliverables, not afterthoughts.** Budget time for them.

---

## 10. upay — who the customer actually is

upay (উপায়) is the digital financial services / mobile financial service (MFS) brand of **UCB Fintech Company Limited**, a subsidiary of **United Commercial Bank PLC**. Licensed by Bangladesh Bank, launched early 2021, replacing UCB's earlier "Ucash" MFS brand.

| Fact | Source |
| --- | --- |
| Agent-based payments; deposit/withdraw, transfers, bill pay | https://platform.tracxn.com/a/d/company/59a99b4fe4b0414cfd07a974/upay |
| Services: Cash In, Cash Out, Send Money, Make Payment, Add Money, Pay Bill | https://www.upaybd.com/ |
| Merchant QR + online payments; also dialable via `*268#` | https://www.upaybd.com/products/make-payment |
| App: Bangla + English, USSD fallback, add money from any bank or card, all-operator recharge, wallet showing inflow provenance (salary / disbursement / remittance), ticket booking | https://play.google.com/store/apps/details?id=bd.com.upay.customer |
| Bill payments include traffic fines, Indian visa fee, Titas prepaid gas | https://today.thefinancialexpress.com.bd/trade-market/upay-offers-lowest-cash-out-fees-highest-client-security-1628439154 |
| **130,000+ upay agents**; card loadable at any agent | https://www.ucb.com.bd/banking/retail-banking/upay-ucb-card |
| Agents and merchants "covering all 64 districts" | https://www.upaybd.com/ |
| UCB Agent Banking: 64 districts & 273 upazilas | https://www.ucb.com.bd/banking/agent-banking/business-network |
| UCB parent bank: 236 branches | https://www.ucb.com.bd/banking/retail-banking/upay-ucb-card |
| Real-time remittance from Malaysia (FELDA Mobile) into upay wallet | https://www.ucb.com.bd/news-and-events/press-release/ucb-and-incentive-remit-launched-real-time-remittance-service-in-bangladesh |
| NRB Bank tie-up: Micro DPS, remittance, credit card bill pay | https://www.tbsnews.net/economy/corporates/upay-nrb-bank-partner-expand-digital-financial-services-1494556 |
| **Education/campus push**: Daffodil Group MoU for digital payment acceptance across the education ecosystem | https://www.ucb.com.bd/news-and-events/press-release/upay-and-daffodil-group-sign-strategic-partnership-mou-to-advance-digital-payments |
| **UCSI University**: QR merchant payments campus-wide, tuition fees, scholarships, **RFID smart student ID** | https://www.ucb.com.bd/news-and-events/press-release/upay-and-ucsi-university-bangladesh-sign-agreement-to-build-a-cashless-smart-campus |
| 24/7 hotline 16268; customer service + complaints channels exist | https://www.upaybd.com/ |
| ~324 employees; Dhaka; founded 2021 | https://platform.tracxn.com/a/d/company/59a99b4fe4b0414cfd07a974/upay |

### Angles this surface

- **Agent network is the operational backbone** (130,000+ agents). Agent liquidity and agent performance are Track 05 territory and map to a real, physical, staffed operation.
- **Campus/education is an active, dated strategy line** — and DIU, the hackathon host, sits inside that same group. A campus-financial-life angle has unusually high relevance credibility.
- **Remittance inflow** is a documented, structurally important flow.
- **Bill pay and recharge** are high-frequency, low-value, repetitive — the automation candidates Track 06 asks for.
- **App supports Bangla and English** and USSD — a real accessibility constraint, not a hypothetical one.

---

## 11. Evidence discipline

- **Every external claim needs a URL.**
- No URL → mark **UNVERIFIED**.
- Never invent numbers. No fabricated market sizes, user counts, or benchmark results.
- Technical judges will probe. One unsourceable figure discredits every other claim in the deck.

---

## 12. Working agreement for the remaining 24h

1. **Resolve §0 before anything else.** It determines the track.
2. Pick **one** idea. Three people × 24h cannot hedge.
3. Prefer ideas where the business number is a **rate, ratio, or count** a business judge can hold in their head.
4. Prefer **one strong model story** over a broad pipeline. AI/ML depth is 20% and must be *material*, not decorative.
5. Must clear the §8 line: AI beating a simple deterministic rule.
6. Design so the on-site requirement drop is absorbable — separate data prep from inference, business rules from model output (§6).
7. Reserve explicit time for: README, live deploy, demo video, project report (§9).
8. Keep Git history continuous from now on. Judges read it.