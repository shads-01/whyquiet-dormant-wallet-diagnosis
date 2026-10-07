# Data inventory for a Bangladeshi MFS AI project (40+ sources)

Built by opening each source page (webfetch) on 2026-10-02. Status: VERIFIED = page opened and facts below read from it; UNVERIFIED = not opened or page partially unreadable; facts from memory stay UNVERIFIED. Dropped sources at the bottom.

## A. Public datasets

### A1. Bangla speech and dialects

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Ben-10 (BengaliAI regional speech) | https://huggingface.co/datasets/bengaliAI/Ben-10 + github.com/BengaliAI/reg-speech-aacl | 78h annotated Bengali STT, 10 regional dialects; public train 13.4k rows; CLOSED test set scored by maintainers (WER only) | audio+text | bn (10 dialects) | 15,036 rows / 8.52 GB | CC0-1.0 | Direct HF download; test set only via eval-request issue | AACL 2025 paper, Kaggle Ben-10 competition, regional ASR leaderboard | Built for ASR research, never aimed at MFS payments/fraud | Low (researchers, consented) | 1-2 | VERIFIED |
| OpenSLR SLR53 Bengali ASR | https://www.openslr.org/53/ | ~196K utterances Bengali ASR training set | audio+text | bn | 196K utterances | OpenSLR-hosted, per-resource licence page (not read) | Direct wget (max 5 connections) | ASR research | Generic Bengali ASR, no MFS/dialect focus | Low | 2 | VERIFIED (index only) |
| OpenSLR SLR37 Bengali TTS | https://www.openslr.org/37/ | Multi-speaker high-quality TTS for bn-BD AND bn-IN | audio+text | bn | TTS-scale | per-resource licence page (not read) | Direct wget | TTS synthesis | TTS corpora unused for scam-call simulation or voice UX in MFS | Low | 2 | VERIFIED (index only) |
| Google FLEURS bn_in | https://huggingface.co/datasets/google/fleurs | Read speech, 102 languages; Bengali subset present is **bn_in (Indian Bengali), NOT bn_bd** | audio+text | bn-IN | ~4.3k rows bn_in | CC-BY-4.0 | Direct download / streaming | Multilingual ASR benchmark | Indian Bengali accent, not Bangladeshi speech | Low | 1 | VERIFIED |
| Common Voice bn | https://commonvoice.mozilla.org/bn (data via https://datacollective.mozillafoundation.org) | Crowdsourced Bengali read speech | audio+text | bn | bn config existed on CV17 | CC0 (historically); **since Oct 2025 datasets moved exclusively to Mozilla Data Collective** | Data Collective account | ASR fine-tuning (BengaliAI has a commonvoice-bangla repo) | Read speech, no spontaneous/payment language | Low | 2-3 | VERIFIED (change note read; bn size UNVERIFIED) |

### A2. Bangla handwriting, digits and OCR

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NumtaDB | https://bengali.ai/datasets/ + https://www.kaggle.com/BengaliAI/numta | Bengali handwritten digits, multiple styles/augmentations | image | bn digits | ~85k images (UNVERIFIED) | MIT on tutorial repo; DB licence not stated on fetched page | Kaggle/HF download | Digit recognition research | Nobody applied it to khata/baki credit-book reading | Low | 1 | VERIFIED (repo; size UNVERIFIED) |
| Bengali.AI graphemePrepare / bengaliai-cv19 | https://github.com/BengaliAI/graphemePrepare + Kaggle bengaliai-cv19 | Handwritten Bengali graphemes, ground truth + extraction (CV19 Kaggle ~200k) | image | bn | ~200k (Kaggle) | MIT (repo); Kaggle competition terms | Kaggle account | CV19 grapheme classification competition | Grapheme recognition never applied to MFS documents | Low | 1-2 | VERIFIED (org page) |
| BADLAD | https://github.com/BengaliAI/BADLAD | Bengali Document Layout Analysis Dataset | image/layout | bn | UNVERIFIED | repo (licence not read) | GitHub | Layout analysis | Document layout never used for MFS statements/receipts | Low | 1 | VERIFIED (org page) |
| BaNLAD | https://github.com/BengaliAI/BaNLAD | Bengali NLP dataset (layout/annotation family) | text/image | bn | UNVERIFIED | MIT | GitHub | Bengali NLP research | Generic Bengali NLP, no MFS application | Low | 1 | VERIFIED (org page) |
| bbocr | https://github.com/BengaliAI/bbocr | Bangla OCR tooling (Python, BSD-3-Clause) | code+model | bn | UNVERIFIED | BSD-3-Clause | GitHub | Bangla OCR | OCR tooling never wired into MFS workflows | Low | 1 | VERIFIED (org page) |

### A3. Bangla/Banglish text, sentiment, NER

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SentNoB | https://huggingface.co/datasets/khondoker/SentNoB | Social-media user comments sentiment (pos/neg/neutral), expert-labelled | text | bn | 10K-100K | CC-BY-ND-4.0 (no derivatives) | Direct download | Findings of EMNLP 2021 (islam2021sentnob) | Social-media sentiment never applied to MFS complaints/support | Low-medium (public comments) | 1 | VERIFIED |
| NC-SentNoB | https://huggingface.co/datasets/ktoufiquee/NC-SentNoB | Multilabel noise categories (local/regional words etc.) in noisy Bangla, 4 native annotators, Fleiss Kappa 0.69 | text | bn | 10K-100K | CC-BY-SA-4.0 | Direct download | W-NUT/EACL 2024 noise-reduction paper | Regional-word taxonomies unused for Banglish support tooling | Low-medium | 1 | VERIFIED |
| BanFakeNews-2.0 | https://huggingface.co/datasets/hrshihab/BanFakeNews-2.0 | Bengali fake-news text classification | text | bn | 10K-100K | Apache-2.0 | Direct download | Fake-news research | Never applied to scam SMS/payment fraud messages | Low-medium | 1 | VERIFIED |
| BLUGE-bengali-ner | https://huggingface.co/datasets/nahid-hub/BLUGE-bengali-ner | NER (person/org/location/object, IOB) part of the 7-task BLUGE benchmark + B-CORE pretraining corpus | text | bn | 10K-100K | CC-BY-4.0 | Direct download | BLUGE benchmark (2026) | NER unused for recipient-name / ledger entity matching in MFS | Low | 1 | VERIFIED |
| TyDi QA | https://ai.google.com/research/tydiqa | QA across 11 typologically diverse languages incl. Bengali | text | bn + 10 | ~200k pairs (UNVERIFIED) | per-page licence (content truncated on fetch) | Direct download | QA benchmark | QA never applied to MFS FAQ/help flows | Low | 1 | VERIFIED (partial) |

### A4. App-store reviews and complaints

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Google Play reviews via google-play-scraper | https://github.com/JoMingyu/google-play-scraper (pip install google-play-scraper) | Reviews, ratings, versions, replies for any Play app (bKash/Nagad/Rocket/Upay) | text | bn/en | 200/page, paginated | MIT (tool); **Google Play ToS prohibits scraping - flag: hackathon risk, use sparingly/attribute** | None (tool works today) | Widely used for app analytics | Bangladesh MFS reviews in Banglish unmined | Medium (public usernames - redact) | 1 | VERIFIED |
| App Store customer reviews RSS | https://itunes.apple.com/{country}/rss/customerreviews/page=1/id={app-id}/sortby=mostrecent/json | Official Apple RSS feed of app reviews | text | bn/en | 500/app/page | Apple public feed | None (format from memory) | Common review-mining practice | Bangladeshi MFS iOS reviews unmined | Medium | 1 | UNVERIFIED (format from memory) |
| Bangladesh Bank Customer Complaints CMS | https://cmsform.bb.org.bd/apps/f?p=107 (linked from https://www.bb.org.bd) | BB's complaint submission portal for banks/FIs | form/portal | bn/en | UNVERIFIED | Government portal; no bulk data published | Form-based; data request via BB | Consumer complaint routing | Aggregate complaint themes never published as data | Medium | 1 (form) / UNVERIFIED for data | VERIFIED (portal exists; data access UNVERIFIED) |

### A5. Bangladeshi food/commodity prices

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| WFP/HDX Bangladesh Food Prices | https://data.humdata.org/dataset/wfp-food-prices-for-bangladesh | Retail prices (rice, fish, sugar etc.), ~3000 markets, sources include DAM and FAO GIEWS; weekly/monthly, back to 1900 | tabular | en | 4.3 MB CSV | CC BY-IGO | Direct CSV download | WFP VAM Economic Explorer | MFS food-price forecasting/budgeting never built on it | Low | <1 | VERIFIED |
| WFP VAM Economic Explorer (BD) | https://dataviz.vam.wfp.org/asia-and-the-pacific/bangladesh/overview | Interactive view of the same WFP price data | tabular/viz | en | same source | CC BY-IGO | Public | WFP dashboards | Same - unused for MFS | Low | <1 | VERIFIED (link) |
| FAO GIEWS food prices | https://www.fao.org/giews/ (root; specific BD page 404 on fetch) | Global food price monitoring incl. Bangladesh | tabular | en | UNVERIFIED | FAO terms | UNVERIFIED | Food-security monitoring | Unused for MFS | Low | 1 | UNVERIFIED |

Note: DAM (dam.gov.bd) and TCB (tcb.gov.bd) both failed to load today (transport errors) - dropped. Their data flows into the WFP CSV instead.

### A6. Weather and flood data

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Open-Meteo Historical Weather API | https://open-meteo.com/en/docs/historical-weather-api | Hourly weather 1940-present (ERA5 25km / ERA5-Land 11km / IFS 9km), rainfall, soil, gusts | tabular/API | en | per-request | Free for non-commercial; API key for commercial | None (no key for non-commercial) | Research/industry | Never joined to MFS transaction behaviour | Low | <1 | VERIFIED |
| BMD (Bangladesh Meteorological Department) | http://www.bmd.gov.bd | Forecasts, warnings (heavy rain, kalbaishakhi, heat), climate normals, agromet archive, AWS | web/API | bn/en | normal tables public; raw data via paid portal | Public norms; **raw data purchase via dataportal.bmd.gov.bd (paid)** | Paid portal for raw data; norms free | National forecasting | Local weather never joined to MFS behaviour | Low | 1 (norms) | VERIFIED |
| FFWC (Flood Forecasting & Warning Centre, BWDB) | http://www.ffwc.gov.bd | River levels, flood forecasts | web | bn/en | UNVERIFIED | Government site | UNVERIFIED | National flood warning | Flood exposure never joined to MFS behaviour | Low | 1 | VERIFIED (title only; contents UNVERIFIED) |

### A7. Geospatial

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| OSM Bangladesh (Geofabrik) | https://download.geofabrik.de/asia/bangladesh.html | Full OSM extract: roads, shops, markets, ATMs, banks (amenity tags), hourly updates | geospatial | en/bn names | 339 MB .osm.pbf | ODbL 1.0 | Direct download | Mapping/GIS | Market/agent/ATM density never modelled against MFS behaviour | Low | 1-2 | VERIFIED |
| WorldPop | https://www.worldpop.org/ (+ https://wopr.worldpop.org/) | High-res population distribution, age/sex, poverty/literacy indicators; REST API | geospatial | en | country rasters | Open; **explicit clause: must not be used to surveil or harm individuals/vulnerable groups** | Direct/API | Health/development planning | Population density never joined to MFS access gaps | Medium (responsible-use clause) | 1 | VERIFIED |
| HDX Bangladesh group | https://data.humdata.org/group/bgd | Hub of Bangladesh humanitarian datasets (flood, population, prices) | mixed | en | mixed | per-dataset | Direct | Humanitarian response | Hub unused by MFS projects | Low | 1 | UNVERIFIED (hub; linked from VERIFIED pages) |

### A8. Household and financial-inclusion surveys

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Global Findex 2025 | https://www.worldbank.org/en/publication/globalfindex (download-data tab) | Demand-side financial inclusion: accounts, savings, borrowing, digital payments, mobile money; Bangladesh featured | tabular | en | country-level CSV/microdata | World Bank open data | Direct download | Financial-inclusion research | Never used as the demand-side frame for a BD MFS prototype | Low | 1 | VERIFIED |
| Bangladesh Bank statistics | https://www.bb.org.bd (Remittances: /en/index.php/econdata/wageremitance; Payment Systems reports; platform-wise stats) | Wage-earner remittance inflow (PDF), payment platform stats, half-yearly BPSR, policy rates, FX | tabular/PDF | bn/en | monthly PDFs | Public government data | Direct PDF; some need data-portal form | Regulator publications | Remittance/payment aggregate trends never used as training signal | Low | 1-2 | VERIFIED |
| BBS HIES (Household Income & Expenditure) | https://bbs.portal.gov.bd (not opened) | National household income/expenditure microdata | tabular | en/bn | UNVERIFIED | UNVERIFIED (request form expected) | Request form | Poverty statistics | Not opened today; inclusion/expenditure microdata unused for MFS | Medium (household data) | UNVERIFIED | UNVERIFIED |

### A9. Public fraud/transaction/graph/uplift/tabular finance

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IEEE-CIS Fraud Detection | https://www.kaggle.com/c/ieee-fraud-detection | Card transaction fraud labels, anonymised Vesta features | tabular | en | large | Kaggle competition terms (non-commercial) | Kaggle account | Fraud-detection benchmark | Card fraud, not MFS send-flow; anonymised | Low (anonymised) | 2 | VERIFIED (page) |
| UCI Default of Credit Card Clients | https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients | 30,000 Taiwan credit clients, 23 features, default labels | tabular | en | 5.3 MB | CC BY 4.0 | Direct/ucimlrepo | Default-prediction benchmark (Yeh & Lien 2009) | Credit default, not MFS | Low | <1 | VERIFIED |
| PaySim | https://www.kaggle.com/datasets/ealaxi/paysim1 | **SYNTHETIC** mobile money transactions (Kaggle title: "Synthetic Financial Datasets For Fraud Detection") | tabular | en | 6.3M rows | Kaggle | Direct | Mobile-money fraud papers | **Fails strict-ideation rule 2: synthetic - model learns only injected patterns** | Low | <1 | VERIFIED (synthetic) |
| Elliptic Data Set | https://www.kaggle.com/datasets/ellipticco/elliptic-data-set | Bitcoin transaction graph, licit/illicit labels, 200k nodes | graph | en | ~1 GB | Kaggle/CC (UNVERIFIED) | Kaggle account | Graph anti-money-laundering research | Crypto AML, not MFS; graph baseline only | Low | 2 | VERIFIED (page) |
| dunnhumby The Complete Journey / Carbo-Loading | https://www.dunnhumby.com/source-files/ | 2,500 households, 2y transactions + marketing contact history; "representation" of real data | tabular | en | 4.3 GB / samples | dunnhumby Source Files terms (academic use encouraged) | Direct download (registration implied) | Retail marketing research | US grocery retail; **"representation of real" - treat as synthetic-derived, fails rule 2 unless the licence states real data** | Low | 2-3 | VERIFIED |
| Criteo uplift dataset | https://ailab.criteo.com/ressources/ (dataset page not confirmed on fetch) | Advertising uplift (treatment/control conversions) | tabular | en | ~45M rows | per-page (UNVERIFIED) | Direct (UNVERIFIED) | Uplift modelling research | Ads uplift, not MFS campaigns; only public uplift option found | Low | 2 | UNVERIFIED |

Dropped: PKDD'99 Czech bank (http://lisp.vse.cz/pkdd99/Challenge/berka.htm) - server unreachable today (transport error). IDEA_POOL.md cites it; treat that citation as UNVERIFIED until an open mirror is found.

### A10. Images

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BADLAD (cross-list from A2) | https://github.com/BengaliAI/BADLAD | Bengali document layout (statements, forms) | image | bn | UNVERIFIED | repo | GitHub | Layout analysis | Never applied to MFS statements/receipts | Low | 1 | VERIFIED (org page) |
| NumtaDB (cross-list from A2) | https://bengali.ai/datasets/ | Handwritten digits | image | bn | ~85k | MIT repo | Kaggle/HF | Digit recognition | Never applied to khata reading | Low | 1 | VERIFIED |
| (self-collected) shop + receipt photos, payment-proof screenshots | n/a | Collectable with consent (see B) | image | bn/en | n/a | own | own | none | Nothing public covers Bangladeshi F-commerce payment proofs | Medium (consent needed) | 2-4 | n/a |

Dropped (could not open): SKU-110K (TrickyGo/DenseDet not fetched), SROIE (ICDAR RRC portal), MIDV-500 (arXiv/GitHub page not opened), Ekush (GitHub URL 404; could not locate), CMATERdb (not opened).

### A11. Audio (voice spoofing, speaker ID)

| Name | URL | Contains | Modality | Language | Size | Licence/terms | Access friction | Known uses | Why unused in MFS | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ASVspoof 5 | https://www.asvspoof.org/ (download: /database) | Spoofed/deepfake speech attacks, anti-spoofing eval data (2019/2021/2025 editions) | audio | en/multilingual | large | research registration | Login/registration on asvspoof.org | Anti-spoofing challenge | Never applied to Bangla voice-clone fraud (scam calls) | Low | 2-3 | VERIFIED |
| VoxCeleb 1/2 | https://www.robots.ox.ac.uk/~vgg/data/voxceleb/ | 7,000+ speakers, 1M+ utterances, 2000+ hours in-the-wild speech; speaker verification | audio/video | en | 2000+ hours | Academic; **form-gated download** (privacy notice published) | Request form + password | VoxSRC challenges | Speaker-verification baselines never applied to Bangla/MFS | Medium (celebrity speech; privacy notice) | 2-3 | VERIFIED |
| (self-collected) scam call re-enactments + dialect voices | n/a | Collectable with consent (see B) | audio | bn/dialects | n/a | own | own | none | Nothing public contains Bangla scam-call speech | High (consent, redaction mandatory) | 4-6 | n/a |

Dropped: FakeAVCeleb (not opened); IndicVoices (both URL variants 404).

## B. Collectable by 3 students in under 8 hours with consent

| Name | Contains | Consent/redaction | Privacy risk | Hours | Status |
|---|---|---|---|---|---|
| Dialect voice recordings (DIU classmates) | Sylheti/Chittagonian/Noakhali read + spontaneous speech, per-speaker labels | Written consent, per-person held-out split | Medium | 2-4 | n/a (self) |
| Handwritten khata pages | Family and campus-shop credit books, photographed | Shopkeeper consent, blur names | Low | 2-3 | n/a |
| Real scam SMS/screenshots/call stories | Own phones + relatives, consented, phone numbers redacted | Consent, redact numbers/names | Medium | 2-3 | n/a |
| Interaction logs on clickable prototype | Friends/parents using a mock send flow (timings, taps, hesitation) | Consent, no accounts touched | Low | 2-4 | n/a |
| Shop and receipt photos | Campus shops, F-commerce sellers' payment proofs | Consent | Low | 2-3 | n/a |
| Surveys/interviews | Agents, shopkeepers, parents (Money-Test style questions) | Consent | Low | 3-4 | n/a |
| Utility bill photos (DESCO/DPDC/WASA) | Bill formats, account-number layout (redacted) | Consent, redact account numbers | Low | 1-2 | n/a |

## C. Unusual

| Name | URL | Contains | Modality | Privacy risk | Hours | Status |
|---|---|---|---|---|---|---|
| Bangladesh Bank ICT Security Advisories & circulars | https://www.bb.org.bd (mediaroom/circular; saw PSD-2 Bangla QR dispute-resolution circular, Sep 2026) | Regulator texts on fraud patterns, disputes, MFS rules | text/PDF | Low | 1-2 | VERIFIED (site) |
| News archives on scams (Daily Star / Prothom Alo) | https://www.thedailystar.net / https://www.prothomalo.com (not opened) | Scam and fraud reporting, dates and patterns | text | Low (no personal data use) | 2-3 | UNVERIFIED; check each paper's scraping ToS before crawling |
| Wikipedia pageviews (bKash/Nagad/scam pages) | https://dumps.wikimedia.org/other/pageviews/ (not opened) | Hourly pageview counts, public API | tabular | Low | 1 | UNVERIFIED |
| Google Trends Bangladesh | https://trends.google.com (JS app; not fetchable directly) | Search interest on scam/payment queries | tabular | Low | 1-2 | UNVERIFIED |
| BTRC telecom statistics | http://www.btrc.gov.bd (not opened) | Subscriber/market data | tabular | Low | 1 | UNVERIFIED |
| Festival/holiday calendars | Bangladesh government gazette (not opened) | Eid, Puja, Pohela Boishakh dates - spending-day effects | tabular | Low | 1 | UNVERIFIED |

## Dropped (could not open or failed privacy rules)

- DAM (dam.gov.bd) - transport error; data available inside the WFP CSV
- TCB (tcb.gov.bd) - transport error
- PKDD'99 Czech bank dataset - transport error (IDEA_POOL citation now UNVERIFIED)
- IndicVoices (ai4bharat.iitm.ac.in) - 404 on both URL variants
- Ekush - could not locate a live page (GitHub 404)
- SKU-110K, SROIE, MIDV-500, CMATERdb, FakeAVCeleb - not opened within this pass
- Google Play reviews raw scraping at scale - kept as a flagged option (Play ToS risk), not dropped

## Ranking: top 20 by obtainability x uniqueness x signal for money-related decisions

1. Ben-10 (BengaliAI) - direct CC0 download, 10 real Bangladeshi dialects, closed test set maintained for us
2. Real scam SMS/screenshots/call stories (self-collected) - nothing public exists; max uniqueness
3. Dialect voice recordings (self-collected) - real held-out people, complements Ben-10
4. Interaction logs on clickable prototype (self-collected) - the only data that captures user *struggle* in the send flow
5. Handwritten khata pages (self-collected) - the artefact no public dataset covers
6. NumtaDB - easiest image dataset, direct digits
7. Bangladesh Bank payment/remittance statistics - official money signal, monthly PDFs
8. WFP/HDX food prices BD - 4.3MB CSV, weekly, sub-national markets
9. Global Findex 2025 - demand-side inclusion frame, direct download
10. google-play-scraper reviews (bKash/Nagad/Upay) - Banglish complaint text, ToS-flagged
11. Open-Meteo historical API - free, no key, joins to any behaviour data
12. OSM Bangladesh - markets/ATM/agent density for merchant ideas
13. SentNoB - labelled Bangla sentiment, direct
14. SLR53 Bengali ASR - 196K utterances, direct wget
15. UCI Default of Credit Card Clients - CC BY, clean default-prediction baseline
16. IEEE-CIS Fraud Detection - fraud benchmark, Kaggle terms
17. ASVspoof 5 - anti-spoofing eval data, registration friction
18. FLEURS bn_in - free ASR but Indian Bengali (weaker fit)
19. BLUGE-bengali-ner - new 2026 benchmark, direct
20. WorldPop - population density, free, responsible-use clause

## Combination notes (dataset + dataset that is new)

- Ben-10 + self-collected dialect recordings: base dialect ASR, then test on OUR held-out people - real person-level evaluation.
- Scam SMS census + SentNoB / BanFakeNews: scam-message classifier seeded by labelled public text, tested on real collected scam messages.
- Khata pages + NumtaDB digits: digit OCR pretraining, then fine-tune on real khata handwriting (Numta digits alone are not khata pages).
- WFP prices + Open-Meteo: weather/price elasticity - public-only, joinable in an afternoon.
- Play reviews + Findex: switching-intent model grounded in inclusion demographics.
- SLR37 TTS + self-collected scam call scripts: generate synthetic scam-call audio for detector TRAINING only; test set must stay real (strict-ideation rule 2).
- Bangladesh Bank platform stats + Findex: adoption-gap analysis (who has accounts vs who transacts).
- ASVspoof 5 + self-collected dialect voices: spoofing detector for non-standard accents - public spoof data is English-centric.
