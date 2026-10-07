# Idea pool so far (status: FINALIST / COMPONENT / WEAK / KILLED). All facts about datasets/competitors are UNVERIFIED.
FINALISTS
- Coercion Shield: detect a payment being controlled by a scammer on a call. (a) Puppeteer: sequence model over send-flow interaction timing, trained on 30-50 students doing self-directed vs coached (scam script dictated by a phone partner) sends, on-device; (b) kill-chain listener: Bangla speech -> scam-stage classifier (hook, authority, urgency, ask) + HMM/CRF; (c) voice-clone guard: anti-spoofing + speaker verification. Action: friction, guardian veto, or reversible window. Risks: role-play is not real coercion; Android can't record calls; evaluate on held-out people.
- Khata Lens: photograph a paper credit book (khata/baki); read Bangla handwriting (digits, names, dates); match names to phone contacts; send upay payment requests; rank overdue. Digit data possibly NumtaDB. Competitors TallyKhata/Hishabee may need typing.
- Dialect voice wallet: feature-phone voice call; dialect speech (Sylheti, Chittagonian, Noakhali) -> intent/slots -> read-back confirmation + keypad PIN; fine-tune Whisper on Bangla plus DIU students' dialect recordings.
- Confusion detector: learn from interaction events when first-time/older users are struggling; simplify UI; aggregate to rank problem screens. Data: students + parents on a clickable prototype.
- Scam Census: collect real scam SMS/screenshots/numbers (consented, redacted); cluster into campaigns, track drift; weekly radar + blocklist.
- Name Confirm: match intended recipient name vs masked registered name across Bangla/English spellings; must beat fuzzy-string baseline; may already exist.
- Agent Bounty Guardian: bounties for agents who stop confirmed scam cash-outs; model ranks which cash-outs to question.
- Fraud Arena: attacker agent adapts against the detector in a simulator; robustness-vs-rounds curve (circular; claim robustness only).
- Chanda Trust: fraud-checked community fundraising; text patterns, stolen-photo reuse via embeddings, recipient mismatch.
- Transaction foundation model: small transformer pretrained on a public bank transaction dataset (e.g. PKDD'99 Czech), surprise scores, expected-vs-actual explanations, life-event detection.
- Ledger-grounded Banglish complaint resolver: extract amounts/times/partial numbers from Banglish; rank candidate ledger transactions; flag contradictions; must beat an LLM function-calling baseline or it dies.
- Scam sparring partner: adaptive AI scam practice (voice/chat in Bangla) with leak detection and per-tactic knowledge tracing.
- Payment-proof forensics: detect forged payment screenshots for F-commerce sellers; works on any provider's screenshots.
- Competitor pain miner: aspect + switching-intent model on public Banglish app reviews.
COMPONENTS: Guardian Tap (trusted-contact veto), Regret Window (risk-scaled reversible hold on first-time-recipient sends).
WEAK / CONDITIONAL: Float Radar (agent liquidity; circular), Remittance Envelopes, Silence Engine (needs a public uplift dataset like Criteo/Hillstrom), salary-day cash-out reducer, cash-drawer vision (agents' cash photo, YOLO notes), shop-snapshot profiling (SKU-110K), bazaar-aware budgeting (public price data; weak upay link), Vouch Graph (mule-farming risk).
KILLED: Digital Samity (deposit-taking regulation), Rain-Day Payout, Peak Shaver, Flood Corridor, Bulk Buy Circles, merchant cash-flow passport, generic churn predictor, generic chatbot, honeypot wallets, voice soundbox, cash tax meter, Wrong-Send Guard.

UPDATES FROM DATA INVENTORY (verified today)
- Dialect voice wallet is stronger: Ben-10 (BengaliAI, 78h, 10 Bangladeshi dialects, CC0, public train data, closed test set held by BengaliAI) gives person-level held-out evaluation for free.
- Transaction foundation model: PKDD'99 is UNVERIFIED/unreachable; it needs another real pretraining dataset or it is demoted.
- dunnhumby and PaySim are synthetic: baselines only, never training evidence (they fail the strict test, rule 2).
- FLEURS Bengali is Indian Bengali (bn_in) only, so it is a weak fit.
- Common Voice is now behind Mozilla Data Collective, so there is extra access friction.
- Google Play scraping is ToS-flagged; use sparingly.
- WorldPop has a no-surveillance/responsible-use clause.
- Unreachable and dropped: DAM, TCB, PKDD'99, IndicVoices, Ekush, CMATERdb, SKU-110K, SROIE, MIDV-500, FakeAVCeleb.
- Strongest data combinations found: Ben-10 + self-collected dialects; scam census + SentNoB; khata pages + NumtaDB digits; WFP prices + Open-Meteo; SLR37 TTS + real scam scripts (training-only synthetic).
