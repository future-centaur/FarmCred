Smallholder Credit Scoring — Merged Master Parameter List 
Synthesized from four independently drafted lists. Organized into 9 categories. Each parameter shows a one-line definition, intended data source, and which raw list(s) it was merged from. ⚠️ marks a conflict/overlap the group needs to explicitly resolve.


0. Identity, Geolocation & KYC
Not scored — foundational fields that unlock other data sources (satellite, mobile money, etc.)

Parameter
Definition
Data Source
Full name & national ID
Legal identity verification
Self-report + ID document scan
Phone number (M-Pesa linked)
Enables mobile money data pull and disbursement
Self-report, verified via M-Pesa API
County / sub-county / ward
Administrative location, used for regional risk aggregation
Self-report / GPS reverse-geocode
GPS pin of farm
Exact plot location — auto-captured, not typed
Phone geolocation at onboarding


1. Production Capacity (Farm & Agronomic Profile)
Parameter
Definition
Data Source
Land size (acreage)
Total cultivated area
Self-report (dropdown bands), cross-checked via satellite plot delineation
Tenure status
Owned / leased / family land / allotment letter / title
Self-report (dropdown)
Primary & secondary crop(s)
What's grown, main and intercropped
Self-report
Years farming this plot / experience
Tenure and track record on this specific land
Self-report
Irrigated vs. rain-fed
Water source for the plot
Self-report, verified via satellite/imagery
Soil quality proxy
Indicator of agronomic ceiling on yield
Extension officer verification or soil-type geodata
Input package used
Certified seed vs. recycled; fertilizer type/quantity
Self-report, agrovet purchase records
Historical yield (volume)
Physical output in past seasons (kg/bags per acre)
Self-report, extension verification
Last-season revenue (KES)
Cash value of last season's output
Self-report, coop/buyer sales records
Seasons per year
Cropping frequency/intensity of the plot
Self-report
Production Capacity Index
Composite score combining the above — sets the ceiling on repayment capacity, not the willingness to repay
Derived/computed, not a raw field

⚠️ Conflict — Yield vs. Revenue: one list tracks historical yield (physical volume), another tracks last-season revenue (KES value). These are not interchangeable — yield can be strong while revenue is weak (poor prices/no buyer), which is exactly the gap Category 2 below is meant to catch. Keep both, don't collapse into one "production" number.


2. Market Linkage & Realized Revenue
Parameter
Definition
Data Source
Offtake/market linkage strength
Tiered score from "spot market only" to "signed offtake with reputable buyer"
Self-report + buyer/coop confirmation
Volume delivered to buyer, last 2–3 seasons
Actual quantity sold through the linkage, not just its existence
Cooperative/processor delivery records
Season-on-season delivery consistency
Did they deliver every cycle or only intermittently?
Cooperative/processor records
Acreage × county-average yield (fallback estimate)
Proxy for expected output where no delivery history exists
County agricultural statistics

⚠️ Conflict/refinement: one list treats market linkage as a simple categorical flag ("do you have a buyer?"), another treats it as a behavioral, volume-based metric ("how much did you actually deliver, how consistently?"). Recommend keeping the categorical version as an onboarding-stage question and the volume/consistency version as the scored metric once delivery history exists.


3. Cash-Flow / Financial Behavior (Digital Transaction Data)
Parameter
Definition
Data Source
Median monthly inflow (KES)
Central tendency of mobile money income over 6–12 months
M-Pesa statement (consent-based pull)
Coefficient of variation of monthly inflows
How irregular the farmer's income is — lower is better
M-Pesa statement
Months with inflow above a floor
Count of months clearing a minimum subsistence threshold
M-Pesa statement
Debt-service-ratio proxy
Proposed instalment ÷ median monthly inflow
Derived from M-Pesa + loan terms
Input-purchase timing consistency
Whether input purchases happen reliably before planting season
M-Pesa / agrovet transaction history
Digital wallet savings frequency
Frequency of savings deposits via mobile money
M-Pesa statement
Other/off-farm monthly income (amount)
Non-farm income the household receives
Self-report

⚠️ Conflict — two different "savings" signals: "digital wallet savings frequency" (behavioral, mobile-money-based) is not the same instrument as "SACCO savings balance" (see Category 5) — one is a personal wallet habit, the other is a formal cooperative account balance. Keep both; don't average them into one savings score.

⚠️ Conflict — granularity of off-farm income: one list wants a specific KES amount, another only wants a binary "has off-farm income y/n." Decide which resolution you can reliably collect — binary is easier to get truthfully, amount is more useful for DSR calculations.


4. Repayment & Credit History (Formal + Informal)
Parameter
Definition
Data Source
Existing loan exposure (balance/count)
Current outstanding debt across SACCO, bank, mobile lender
Self-report, CRB check
SACCO/coop input-credit repayment record
Performance history on formal cooperative credit
Cooperative/SACCO records
PAYGo asset finance repayment history
Repayment behavior on solar, water pump, cookstove financing — a strong, underused proxy for small regular payments under real constraints
PAYGo provider records
Agro-dealer / input-supplier trade credit repayment
Informal credit repayment with agrovets or input suppliers
Agrovet records, self-report
Chama/table-banking repayment history
Informal group loan repayment performance
Group records, self-report
CRB (credit reference bureau) report
Formal default/delinquency record — thin for this segment but checked for active defaults
CRB pull
Guarantor / group guarantee
Named individual or group willing to co-sign or vouch
Self-report + reference verification

⚠️ Conflict — exposure vs. performance: "existing loans, self-reported yes/no + amount" measures current debt stock (relevant to over-indebtedness/DSR); "repayment history" measures past behavior/performance (relevant to willingness-to-pay). Both lists sometimes use "existing loans" loosely to mean either — keep them as two explicitly separate parameters.

⚠️ CRB has two possible roles: as a scored input (weight ~20% in one list) and as a hard knockout gate ("active default on CRB") in another. Decide whether it's a point-scored factor, an eligibility gate, or both at different thresholds — using it in both places without a defined boundary will double-penalize borderline cases.


5. Social Collateral / Group-Based Signals
Parameter
Definition
Data Source
Group repayment performance
Track record within a chama, SACCO, or cooperative — repayment consistency, peer vetting
Group/cooperative records
SACCO/chama membership (name, member number, join date)
Formal registration and tenure in a group — a static fact, distinct from performance within it
Group records, self-report
SACCO savings balance
Current formal savings held with the cooperative
SACCO records
Reference contact
Cooperative official, agrovet, or chama chairperson who can vouch for the farmer
Self-report + phone verification
Group guarantee
Whether a group formally co-signs or backs the loan
Self-report, group confirmation

⚠️ Conflict: "membership exists / how long" is a different data point from "how well did they perform within that group" — one list captures only the former (join date, member number), another only the latter (repayment consistency, peer vetting). Both matter and should stay separate — a long-standing member with a poor group repayment record is a very different risk than a new member with no track record yet.


6. Climate & Agro-Environmental Risk
Used to size, time, and structure the loan (and determine if insurance is mandatory) — not to reject applicants outright, since rejecting on geography alone unfairly excludes entire regions.

Parameter
Definition
Data Source
Regional climate/weather exposure score
Rainfall reliability and drought/flood history for the plot's micro-region, historical basis
Satellite/weather data
NDVI anomaly vs. plot's own 5-year baseline
In-season vegetation health relative to that specific plot's own history
Satellite NDVI
Rainfall deficit, current season-to-date vs. ward long-run average
Real-time in-season rainfall shortfall signal
Satellite/weather data
Irrigation access
Whether the plot has irrigation as a risk mitigant
Self-report, satellite verification
Crop diversification count
Number of distinct crops/enterprises — monoculture carries more covariate risk
Self-report, satellite land-cover check

⚠️ Conflict/complementary distinction: the "regional climate exposure score" is a historical, location-based, ex-ante risk classification (used at underwriting to decide loan structure/insurance requirement); "NDVI anomaly vs. own baseline" and "in-season rainfall deficit" are real-time, plot-specific monitoring signals (useful for in-season early warning and restructuring, not just initial underwriting). Recommend keeping both — one feeds loan structuring at origination, the other feeds portfolio monitoring during the season.

⚠️ Irrigation access appears twice with different roles: once as a static farm-profile attribute (Category 1) and once as a climate-risk mitigant (Category 6). It's the same underlying fact — decide which category "owns" it, or explicitly note it's used in both a farm-profile view and a risk-scoring view.


7. Asset Base & Household Resilience
Buffer capacity if a season disappoints — keep this weight modest, since land/livestock registration in Kenya skews strongly male and over-weighting it introduces gender bias.

Parameter
Definition
Data Source
Livestock units owned
Asset and secondary income stream (e.g., dairy cattle)
Self-report, extension verification
Land tenure status
Also appears in Category 1 — see note below
Self-report
Off-farm income presence
Binary flag — also appears in Category 3 with amount detail
Self-report
Years farming current plot
Also appears in Category 1 as farm-profile field
Self-report

⚠️ Structural overlap, not a data conflict: tenure status, off-farm income, and years-on-plot are each listed once as a farm/financial profile field and once as a resilience-scoring input. They don't need separate values — but decide explicitly whether they're captured once and reused in two scoring modules, or whether the resilience module needs a re-verified snapshot at scoring time.


8. Loan Request Parameters
Deal-specific terms, not creditworthiness signals — but they interact with risk (e.g., input loans tied to a planting cycle repay differently than general cash loans).

Parameter
Definition
Data Source
Amount requested
Loan principal requested
Self-report
Purpose
Seeds, fertilizer, equipment, labor, general cash
Self-report
Expected harvest date
Agronomic timing of when cash is expected to arrive
Self-report, crop-calendar cross-check
Preferred repayment month
Borrower's stated preference for repayment timing
Self-report

⚠️ Conflict: "expected harvest date" (when income will actually exist) and "preferred repayment month" (what the borrower wants) are not guaranteed to match — a borrower may prefer to repay later than harvest, or a lender may want repayment scheduled right at harvest. Keep both distinct and reconcile at loan structuring, don't assume they're the same date.


9. Eligibility Gates / Knockouts
Non-scored. These sit outside the point system entirely — they're pass/fail conditions, not variables to trade off against a strong score elsewhere.

Failed identity verification
Active default on CRB (see also the CRB conflict flagged in Category 4)
Plot outside serviceable area
Crop outside financed value chains


Design Framework to Preserve
Two of the raw lists proposed genuinely useful — and compatible — organizing logics. Worth keeping both explicitly in the model documentation rather than losing them in the merge:

Structuring inputs vs. creditworthiness filter (from List 1): Production Capacity (Cat. 1) and Climate Risk (Cat. 6) tell you how much to lend, on what terms, and whether insurance is mandatory. Market Linkage, Cash Flow, Repayment History, and Social Collateral (Cats. 2–5) tell you whether repayment will happen once the harvest exists. Conflating the two — e.g., rejecting a disciplined, well-linked farmer purely for being in a drought-prone zone — overprices good borrowers or excludes viable ones.
Scored parameters vs. knockout gates (from List 4): most variables above should be binned into 3–5 bands and point-scored (robust to outliers, easy to explain to a credit committee/regulator); a short separate list (Category 9) should function as pass/fail eligibility gates, never traded off against score.

These are two different axes (what the parameter measures vs. how it's used in the decision), and both should probably show up in your scorecard documentation.


Gaps — Parameters Missing From the Combined List
Worth considering against known frameworks (CGAP smallholder scoring guidance, Apollo Agriculture's embedded-finance model, MkulimaScore360-style digital-footprint scoring):

Household size / dependency ratio — a standard CGAP-type resilience signal (repayment capacity relative to number of dependents); currently only individual-level income/assets are captured, not household burden.
Gender of primary decision-maker / household headship — CGAP research repeatedly finds this affects both access and repayment outcomes. Given the explicit caution already flagged about land/livestock registration skewing male (Category 7), this may be better tracked as a fairness/bias-monitoring variable rather than a scoring input, to check the model isn't systematically disadvantaging women farmers.
Post-harvest storage/loss behavior — none of the four lists capture this, yet it's the gap between "yield" and "realized revenue" (Category 1's ⚠️ conflict above) — losses between harvest and sale directly erode repayment capacity.
Crop/index insurance uptake — Apollo Agriculture bundles insurance with its input loans; whether a farmer already carries index insurance (e.g., via ACRE Africa) materially changes the climate-risk calculus in Category 6 and could reduce how conservatively you need to size/structure around weather risk.
Extension/advisory engagement — uptake of SMS agronomic advisory or training attendance is used by some digital scoring models as a proxy for farming diligence, distinct from the input-package and yield data already captured.
Distance/access to input suppliers and markets — logistics access affects both timely input use and the reliability of the market linkage; relevant to last-mile-focused models like Apollo's.
Digital literacy / phone type (smartphone vs. feature phone) — affects which data channels are even available (e.g., NDVI-linked apps, digital advisory), and thus which of the above parameters can realistically be collected for a given farmer.


Summary Recommendation
You have five categories of parameter (Production Capacity, Market Linkage, Cash-Flow/Financial Behavior, Repayment History, Climate Risk, Social Collateral) that all four lists converge on — that convergence is a good sign the core model is right. The main work left isn't adding more parameters; it's resolving the ⚠️ conflicts above (especially yield-vs-revenue, CRB's dual role, and the exposure-vs-performance distinction in repayment history) and deciding bin/weighting structure, which List 4's scorecard format is well-suited to.




Addendum: Conflict Resolutions, Kenya Regulatory Filter & Phased Data Collection Flow
Part A — Conflicts Resolved
#
Conflict
Resolution
1
Yield (volume) vs. revenue (KES)
Keep both, distinct fields. Yield = self-report/extension-verified at harvest. Revenue = buyer/coop sales record. The gap between them is diagnostic (post-harvest loss, weak pricing), not noise.
2
Market linkage: categorical flag vs. volume/consistency metric
Sequence them. Categorical flag ("spot market only" → "signed offtake") is collected once at onboarding as a cheap first pass. Volume/consistency becomes the scored metric once the farmer has ≥1 season of verifiable coop/processor delivery data. New applicants without history fall back to the categorical flag + acreage×county-yield estimate.
3
Digital wallet savings frequency vs. SACCO savings balance
Keep both, distinct instruments. One is mobile-money behavior (flow), the other a formal cooperative balance (stock). Don't average them into one "savings" number.
4
Off-farm income: binary vs. exact amount
Default to binary. Data-minimization principle under the DPA — collect the minimum needed for the purpose. Only prompt for an amount if the binary is "yes" and it's needed to refine a borderline DSR calculation, and even then it's self-reported and optional.
5
Existing loan exposure vs. repayment performance
Keep both, distinct. Exposure/balance = self-report (corroborated by CRB where consented). Performance = SACCO/PAYGo/agro-dealer records, collected with explicit consent from each source.
6
CRB as scored input and knockout gate
Demote to a bounded scored input, not an automatic knockout. Only weight negative CRB listings that are (a) above the regulatory KES 1,000 reporting threshold and (b) within a defined recency window (e.g. last 24 months). Reserve hard knockouts for identity fraud or active insolvency, not routine small-loan defaults — this also keeps you aligned with CBK's own reform direction on CRB use.
7
Regional climate score (historical/ex-ante) vs. NDVI anomaly & rainfall deficit (real-time/in-season)
Keep both, different jobs. Regional score feeds loan structuring at origination (size, term, mandatory insurance). NDVI/rainfall-deficit feeds post-disbursement portfolio monitoring and early-warning/restructuring — not the initial decision.
8
Irrigation access listed in two categories
Capture once, reference twice. It's a single farm-profile fact, reused by both the production-capacity view and the climate-risk view. Don't re-ask it.
9
Tenure status / off-farm income / years-on-plot appearing in both farm profile and resilience scoring
Same resolution as #8 — single source of truth captured at onboarding, referenced by whichever scoring module needs it.
10
Expected harvest date vs. preferred repayment month
Keep both, reconcile explicitly at structuring. Don't assume they match — use the harvest date to sanity-check the requested repayment date rather than treating one as redundant.
11
Group membership (existence/tenure) vs. group repayment performance
Keep both, different data sources. Membership facts at onboarding (self-report); performance pulled later with the cooperative's consent.
Part B — Kenya Data Privacy & Regulatory Filter
Legal basis: Data Protection Act 2019 (DPA), enforced by the Office of the Data Protection Commissioner (ODPC); Central Bank of Kenya (Digital Credit Providers) Regulations 2022; Credit Reference Bureau Regulations 2020; Article 31 of the Constitution (right to privacy).

Removed or restricted from the parameter list:

Phone contact list / contacts scraping — never in the design, but worth stating explicitly: the CBK Digital Credit Providers Regulations 2022 expressly prohibit a digital credit provider from accessing a customer's phone book or contacts list, and from making unauthorized or unsolicited calls or messages to a customer's phone contacts for debt collection. "Reference contact" and "guarantor" must be manually entered by the farmer (a name and number they choose to disclose) — never pulled from the device.
Marital status — excluded from the model entirely. It's explicitly named as a sensitive personal data category under the DPA; there's no lawful, proportionate reason to collect it for a farm credit score.
Names of spouse/children/parents ("family details") — excluded. If household size or dependency ratio is added (see gaps, previous message), collect only an aggregate count, never names — named family members are explicitly a sensitive personal data category.
Gender — retained only as an internal fairness-monitoring variable, explicitly excluded from the scoring model itself. This isn't a strict legal prohibition, but it materially reduces disparate-impact/discrimination exposure under Article 27 of the Constitution, especially since asset-based fields (land, livestock) are already flagged as skewing male.

Reclassified as "sensitive personal data" — needs explicit (not implied) consent + a Data Protection Impact Assessment (DPIA), not standard consent:

Land tenure status, land title/ownership, livestock/asset holdings — the DPA's sensitive-data category explicitly includes "property details." This applies across Categories 1 and 7 of the master list above (tenure status, asset base). Treat consent for these fields as its own granular step, not bundled into general onboarding consent.
GPS pin of the farm — not itself in the sensitive-data list, but as precise geolocation tied to identity it deserves the same purpose-limitation discipline: state explicitly it's used only to unlock satellite crop-health/rainfall data, and isn't shared beyond that purpose.

Process obligations that affect the build, not just the field list:

DPIA required before launch. Since this is large-scale automated profiling feeding a credit decision, a DPIA is required before processing begins, and the model design should be able to show it was done.
ODPC registration is mandatory for financial-services data controllers/processors regardless of size or revenue — this isn't optional at your stage.
Consent must be specific, granular, and purpose-stated per data category — not one blanket "I agree" checkbox. M-Pesa pulls, CRB checks, SACCO data-sharing, and satellite/GPS use should each get their own short consent moment, worded in plain language (and ideally in Swahili/local language too).
CRB checks need prior notice, and any negative listing considered must respect the KES 1,000 minimum reporting threshold — a CRB may not receive a report on negative credit information where the value of the subject matter is less than KES 1,000, so nothing below that should ever influence the score.
Storage limitation — don't retain full applicant data indefinitely, especially for people who never convert to a loan; define a deletion/anonymization schedule.
Cross-border transfer care — if any vendor (satellite/NDVI provider, cloud host, analytics tool) is outside Kenya, you need an adequacy basis, contractual safeguards, or consent for that specific transfer; some data categories may need to stay in-country if the Cabinet Secretary designates them for localization.
Part C — Phased Data Collection User Flow
Design principle: front-load only what's low-friction and self-benefiting (helps the farmer see their own eligibility); delay anything relational (naming other people) or negative-connotation (credit checks) until trust and momentum are already established; move anything satellite/passive to the background so the farmer never has to "hand over" it themselves.

Phase
Farmer-facing?
What's collected
Why now
Consent framing
0. Pre-qualification
Yes — 60 seconds
Phone number, rough location (ward), crop type, land-size band, loan purpose/amount range
Lets the farmer self-check eligibility before investing any real effort — filters out crop/geography knockouts immediately with almost no data given up
"Check if you're eligible" — no sensitive consent needed yet
1. Farm & Identity Registration
Yes — one-time, editable each season
Full name, national ID, GPS pin, land size, tenure status, primary/secondary crop, irrigation, years farming
Once they've passed pre-qualification, they're invested — this is the natural "create your profile" moment
Granular consent screens: one for identity/KYC, one for GPS ("this lets us check your crop's health by satellite so we can offer a fairer rate, not a generic one")
2. Financial Consent Layer
Yes — framed as unlocking a better rate
M-Pesa statement consent pull, existing loan disclosure (binary + rough amount), off-farm income (binary), SACCO/chama membership name
Positioned right before showing indicative loan terms — farmer sees the benefit (better limit/rate) of sharing this, rather than it feeling like a background check
Explicit OTP-based consent for M-Pesa; explained as "the more we can see your cash flow, the less we have to guess — and guessing costs you a higher rate"
3. Background Enrichment (invisible to farmer)
No — system-side
Satellite NDVI, regional rainfall/climate history, county-average yield, production capacity composite
Runs automatically the moment GPS + Phase-1 consent exist — the richest data, but the farmer never has to answer anything for it
One-time notice, not an active step: "As part of your application, we check public satellite and weather data for your area"
4. Market & Social Layer (optional, score-boosting)
Yes — explicitly optional
Offtake/buyer relationship detail, delivery volume history, reference contact (self-provided), group guarantee/vouching
Introduced after the farmer has an indicative offer, framed as "want a higher limit or lower rate? adding these can help" — this is the most relational data (it names other people), so it should never feel mandatory
"Optional — add this later if you'd like a higher limit"
5. Loan Request Specifics
Yes — at point of asking for money
Amount requested, purpose, expected harvest date, preferred repayment month
Naturally comes last — it's the actual ask, once everything else is in place
Standard loan-terms consent
6. Final Credit Check (last gate before approval)
Yes — brief notice, not upfront
CRB check
Deliberately placed last, with clear notice ("we're about to check your credit reference report") rather than upfront — doing it early reads as being judged before any relationship is established, and regulation requires notice before negative-information use anyway
"We're required to check this before final approval — here's what it means for you"
7. Post-disbursement Monitoring
No — system-side, disclosed upfront
In-season NDVI anomaly, delivery consistency, repayment behavior
Ongoing, powers early-warning and portfolio risk management, not a fresh ask of the farmer
Disclosed once at Phase 1 as part of the loan agreement, not re-consented every season unless materially new data types are added

Timing logic in one line: ask for self-benefiting, low-effort data first (Phases 0–1), ask for financial data once the farmer can see it improves their offer (Phase 2), pull passive/satellite data invisibly in the background (Phase 3), make relational/social data explicitly optional and incentivized rather than gating (Phase 4), and hold negative-connotation checks like CRB until the very last step with clear notice (Phase 6) — so the experience escalates in depth roughly in step with the farmer's own investment and trust in the process, and the two most privacy-sensitive moments (satellite/GPS and CRB) are each paired with a plain-language explanation of why, not just a consent checkbox.
Developer Insights
Self-reporting - user credibility - we don't want to rely on sensitive information. For some parameters, we plan to use human agents at the ground level, who will bypass the credibility check and prevent user-side bias
The System
This is an alternative agricultural credit scoring platform that replaces bureau-dependent underwriting with a fused, farm-level evidence base: mobile money transaction behavior, input-purchase and cooperative delivery records, satellite-derived crop health and climate exposure, land tenure and identity data, and formal or informal repayment history where it exists. It separates two distinct questions rather than blending them into one number — how much can this farm plausibly repay (production capacity, climate risk) versus will this person actually repay it (market linkage, cash flow, repayment history, social collateral) — and treats a small set of factors (identity fraud, active insolvency, out-of-area or unfinanced crops) as hard pass/fail gates that sit outside the score entirely rather than being traded off against it. It's used by lenders — banks, MFIs, agri-fintechs, impact investors — making the financing decision; loan officers and field agents who capture and verify ground-truth data the farmer's own devices can't; agronomists and cooperative managers who attest to farm-level claims; and the farmers themselves, who consent to each category of data sharing individually, see their own score and specific levers to improve it, and are never profiled on information (marital status, family names, contact-list scraping) that Kenyan data protection law puts off-limits or restricts to a fairness-monitoring role only. It connects outward to the data sources that make the score possible and inward to the systems that act on it — mobile network and mobile money rails, satellite/weather providers, national ID and land registries, cooperative and off-taker ledgers, the credit reference bureau, and the lender's own loan origination and core banking systems — closing the loop as disbursed loans generate the repayment data that refines the next score.
Primary User Journey
Pre-qualify (60 seconds, near-zero data) — Farmer checks basic eligibility with phone number, ward, crop, land-size band, and loan purpose — filtered against geography/crop knockouts before any real data changes hands.
Register farm & identity — Once invested, farmer (or field agent on their behalf) provides name, national ID, GPS pin, tenure, and crop details, with GPS explicitly framed as unlocking satellite crop-health checks rather than surveillance.
Consent into financial and background data — Farmer authorizes an M-Pesa pull and discloses existing loans/off-farm income binary, positioned as unlocking a better rate; satellite NDVI, rainfall, and county-yield data are pulled invisibly in the background the moment GPS consent exists.
Verify and enrich (optional layers) — Field agents or agronomists confirm sparse or unverifiable ground-truth claims; farmer can optionally add offtake/buyer history, delivery volumes, and a reference contact to raise their limit — always framed as optional, never gating.
Score, decide, and check credit last — The model surfaces a plain-language score and improvement path to the farmer and a risk breakdown to the lender; a CRB check runs as the final gate with explicit notice; the lender's decision and subsequent repayment performance feed back to refine future scoring.
External Systems Touched
jeremy
Mobile network operator / mobile money APIs (transaction history, SIM tenure, disbursement rails):Disbursement rails — BUILD REAL Daraja sandbox STK Push, live on stage with a real phone. Confirm the portal product subscription before debugging credentials. Make the callback handler idempotent on OriginatorConversationID.
Transaction history — FAKE THE DATA, REAL PARSING Generate synthetic M-Pesa statement PDFs in Safaricom's real layout (Receipt No., Completion Time, Details, Paid In, Withdrawn, Balance), password-protected with the persona's ID number. Define each persona's inflows explicitly — Grace steady, Peter spiky, Mary thin-file — and include the transaction mix (co-op paybill, agrovet payment pre-planting). parse_statement() calls Claude for real; assert extraction against your known ground truth.
SIM tenure — FAKE FULLY fixtures/sim.json: MSISDN → {sim_tenure_months, sim_swap_last_90d, msisdn_id_match}. Four cases, one with the swap flag firing. Behind SimProvider, @demo_latency(). Needs an MNO partnership — say so.

Satellite and remote-sensing providers (NDVI, land-cover, yield estimation):
PRE-CACHED REAL DATA — not fabricated Pull real Sentinel-2 NDVI for 3–5 actual Kenyan parcels the week before, via Copernicus or Digital Earth Africa. Pick one visibly healthy, one visibly stressed — green next to brown is your most legible visual.
Offline: cloud-mask via SCL band, erode boundary 10m, median NDVI per date, plus a cached 5-year baseline. Store as fixtures/ndvi/{parcel_id}.json.
MockVegetationProvider.get_series() computes anomaly_vs_baseline at read time, so the real adapter drops in unchanged. Add a fourth parcel returning insufficient_history, and a FORCE_NDVI_TIMEOUT flag — use it once to show the UNAVAILABLE bin firing instead of a null scored as zero.

Weather and climate data providers (rainfall, drought/flood indices):
In-season deficit — BUILD REAL Open-Meteo. No key, no signup, live in under an hour. get_season_deficit(lat, lon).
Historical climatology — CACHED (correct in production too) CHIRPS per demo ward: long-run seasonal mean, CV, drought frequency over 20 years. Static fixtures/climate_wards.json, loaded at boot. get_climate_profile(ward).
Two functions, two jobs — don't collapse them. Enforce in code that climate features sit outside the accept/reject allowlist: they size and structure the loan, never decline it.

National ID / KYC verification systems:
FAKE THE LOOKUP, REAL EXTRACTION fixtures/iprs.json: synthetic IDs → {iprs_match, name, dob, maisha_namba, status}. Four outcomes — clean, name mismatch, not found, deceased. Demo the mismatch; it shows your three-way compare working.
Generate ID card images from an HTML template, watermarked SPECIMEN. Never a real ID, never an image that could pass as genuine.
MockIprsVerifier.verify() behind IdentityVerifier, field-level match booleans in Youverify/Smile ID shape, @demo_latency(). Claude extraction is real; the three-way compare across typed / extracted / IPRS values is real. Store the result only — no selfie retention, even in demo code.
Blocked on institutional accreditation. Answer to "is this real?": production-shape adapter, fixture implementation, vendor swap is a config change.

jumba
Land registry or cadastral databases

Cooperative and off-taker/aggregator databases (delivery volumes, membership standing)

Agro-input supplier / distributor records (agrovet purchase history)

PAYGo asset finance providers (solar, water pump, cookstove repayment records)Jumba –Land registry / cadastral databases — dropping it. Ardhisasa has no third-party API, is live in 2 of 47 counties, costs KES 500 + 1–3 days per search, and most smallholders hold no title. Replacing with KIAMIS.
KIAMIS farmer registry lookup
Build mockKIAMISLookup(national_id) returning what the real registry actually holds: farmer_id, national_id, ward, parcel_geometry (GeoJSON), acreage, crops[], livestock_count, validation_status. Seed 5–6 synthetic farmers covering fully-validated, registered-but-unvalidated, not-found, and acreage-mismatch-vs-self-report.
Shape it as a REST resource so the eventual MoU integration (batch extract or scoped query endpoint) drops in behind the same function signature.
Fire it in Phase 3 background enrichment — invisible to the farmer, triggered the moment GPS + Phase 1 consent exist. The sequencing is real even though the registry isn't.
Tenure status stays self-report + field-agent attestation. Don't build an Ardhisasa path at all, not even a stub.
Cooperative and off-taker / aggregator databases
Co-op delivery ledger — mocked data, real schema, one genuinely real piece
Build mockDeliveryHistory(farmer_id, since_date) in the KTDA SAP extract shape: member_no, delivery_date, volume_kg, unit_rate, value_kes, cumulative_season_volume, input_loan_balance, input_loan_deductions[]. Generate 6 seasons per farmer so both delivery consistency and the yield-vs-revenue gap are computable.
Seed 4 profiles: consistent deliverer, intermittent, declining trend, and non-member returning coverage: "none" — the last one exists specifically to prove absence isn't scored as bad.
Real piece: the give-to-get capture tool can be a Kobo/ODK form — same stack Kevin is already standing up. A co-op clerk form recording deliveries per member is a genuine working integration and the actual production route for small co-ops, not a mock.
Trigger in Phase 4 as an async score uplift: return the initial offer first, then push a limit increase when the co-op record resolves. No co-op source can answer synchronously, so the honest sequencing story is the uplift event, not a spinner.
Agro-input supplier / distributor records
Derived from M-Pesa — real classifier, synthetic input
Do not stub an agrovet API. There isn't one to stub — iProcure went into administration in 2024 and the rest of the sector is paper and cash. The production route is derivation, so build the derivation.
Build the real Till/Paybill → agrodealer mapping table and fuzzy matcher, seeded from the AGMARK, KEPHIS and PCPB dealer registers. This code ships to production unchanged; only its input is synthetic.
Feed it synthetic M-Pesa lines in the actual Safaricom SMS format so the parser does genuine work. Output: agro_input_spend_kes, purchases[], days_before_planting against the county crop calendar.
SKU detail (certified vs recycled seed, fertilizer type) comes from a field-agent receipt photo — same Kobo/ODK form as Kevin's, one extra image field. Real capture, real pipeline.
PAYGo asset finance providers
Folds into Kevin's CRB mock — do not build separately
M-KOPA is CBK-licensed and reports full-file to the bureaus, so PAYGo tradelines arrive inside the CRB response. Ask Kevin to extend mockCRBCheck() to return tradelines[] with an account_type field, so asset-finance lines stay separable from mobile-lender lines instead of collapsing into one "has credit history" flag.
Add one threshold-edge fixture: positive PAYGo history plus a sub-KES 1,000 negative listing, to prove the scorer applies the threshold rule and doesn't penalise the farmer for it.
Only genuinely separate stub needed: mockAssetOwnership(farmer_id) → device_type, provider, purchase_date, payment_status. A SunCulture solar pump is direct evidence of irrigation access (Cat 1 + 6), and that is not in any CRB file.


Credit reference bureau (CRB) — supplementary signal, bounded by the KES 1,000 reporting threshold, not a default knockout
CRB check
Build a small local lookup table: 4-5 synthetic ID numbers mapped to pre-baked JSON responses (clean, delinquent, threshold-edge, fraud-flag).
Your app calls a mockCRBCheck(id_number) function with the same response shape Metropol's real API returns (score, delinquency_code, has_fraud, etc.) — so swapping in the real API later is a one-line change, not a rewrite.
In the UI, trigger it at the same point in the flow (final gate, after consent) so the sequencing story is real even if the data isn't.

Lending institution's loan origination system (LOS)
LOS / core banking
Build a stub service with 2-3 endpoints: createLoanApplication, recordDisbursement, recordRepayment — return realistic-looking IDs and statuses.
Have your scoring output actually call this stub so the hand-off is real, even though what's receiving it isn't a real bank system.
Keep the response schema close to what Mambu's API actually returns, so this is a placeholder for a real adapter, not throwaway code.

Core banking system (disbursement and repayment tracking)

Field data collection tools used by agents (photo/geo-tagged farm verification)
Field data collection (Kobo/ODK) , Real form + API pull into your pipeline — geo-tagged photo capture 
Payment gateway / mobile money disbursement rails
Real sandbox integration — STK push/B2C payout + transaction history pull 
One structural note worth flagging back to the group: since this touches large-scale automated profiling feeding a credit decision, the DPIA and ODPC registration are prerequisites to launch, not a later compliance step — worth locking into the build timeline now rather than after the user flow is finalized. For the mvp some of the sources we need we will fake but keep the shape they will arrive in during production


