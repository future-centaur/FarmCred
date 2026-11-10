# Domain model — Kenyan smallholder agricultural credit

**Date:** 2026-11-10  
**Tier:** 1 (consequential: a credit decision under Kenya’s data-protection and credit-reference rules)  
**Boundary:** which facts about a farmer’s production, sales, cash, and repayment a lender must get right; which facts only size and structure the loan; which facts are pass/fail gates.  
**Not in this domain:** land-title search, running a cooperative or SACCO, designing an insurance product, giving agronomic advice, using sex as a score, and keeping the lender’s own books.

The checkable list is `MANIFEST.md`. This file holds the vocabulary’s states and the order of the decision. `RESEARCH.md` is a synthesis source. Where a row below cites an Act or a regulation, that instrument wins if the synthesis is looser.

## Sources

| source | authority for | recency |
|---|---|---|
| Data Protection Act, 2019 (Kenya Law, revised to 2022-12-31) | Sensitive personal data, consent, minimisation, retention, cross-border transfer, DPIA, registration duty | In force. Registration thresholds are a separate Commissioner instrument (manifest C11). |
| The Banking (Credit Reference Bureau) Regulations, Legal Notice 55 of 2020 | What customer information may be shared, the KES 1,000 bar on submitting negative information, third-party consent before furnisstart the loophing information to a bureau | High Court nullified them in 2023. Court of Appeal in *CBK v Bogongo*, KECA 101 (2024), suspended that nullification pending Civil Appeal E782 of 2023. Treated as in force until that appeal ends (manifest C12). |
| Central Bank of Kenya (Digital Credit Providers) Regulations, 2022, Legal Notice 46 | Submission ban at KES 1,000, thirty-day notice before a provider submits negative information, debt-collection ban on phone books, collection limited to what appraisal and collection need | In force. Applies to a digital credit provider. Whether this operator is one is manifest C13. |
| `RESEARCH.md` | Parameter meanings, the eleven conflict resolutions, the phased journey, which evidence is creditworthiness and which is structuring | Synthesis of four lists plus a regulatory and build addendum. Not fieldwork by the person who confirmed the boundary. |

Stopped when further official pages repeated these rules rather than adding a new obligation inside the boundary.

## What the decision is

Two questions, kept apart.

Production capacity and climate exposure answer how much to lend, on what term, and whether insurance is mandatory. Market linkage, mobile-money cash flow, repayment performance, and social collateral answer whether repayment happens once the harvest cash exists. Eligibility gates sit outside both and are not traded for a high score.

A bureau credit score is an input from a credit reference bureau. It is not the name of this decision.

## States

**Application**

1. Pre-qualified. Phone, ward, crop, land-size band, purpose, and amount range only. Area and crop gates can stop it here.
2. Farm and identity registered. Name, national identity, plot pin, tenure, crops, irrigation, years on the plot. Tenure has its own consent.
3. Financial consent given. Mobile-money statement, exposure disclosed, off-farm income as yes/no, cooperative or chama name.
4. Enrichment attached. Climate exposure, NDVI where the series exists, county yield. Invisible to the farmer. Missing series stays missing.
5. Indicative offer. Structuring from production capacity and climate, creditworthiness from whatever financial evidence exists.
6. Optional uplift. Delivery records, offtake detail, a typed reference, a group guarantee. Refusal leaves the indicative offer standing.
7. Loan requested. Amount, purpose, expected harvest date, preferred repayment month, reconciled at structuring.
8. Bureau check, last, with notice.
9. Decided. Gates first, then points, then size and term and insurance.
10. Disbursed, then in-season monitoring by NDVI anomaly and rainfall deficit. Monitoring does not reopen the original decline question.

**Identity.** Verified when the name given, the document, and the registry agree. Failed identity verification is a gate. The four demo outcomes in the research (clean, mismatch, not found, deceased) are a fixture contract for the build, not a sourced list of registry codes.

**Cooperative evidence.** Either a delivery history exists and can be scored, or it does not. “Does not” is neutral.

**Remote sensing.** A series with enough history, a series too short to compare with a baseline, or unavailable. The last two are not a zero score.

**Loan, once booked.** Originated, then monitored. An in-season deficit can trigger restructuring. It is not a second underwriting decline.

## Rules that bind every state

- Decline does not come from climate exposure, NDVI, or rainfall deficit. Being outside the lender’s serviceable area can still stop an application. That is coverage, not weather.
- Yield and realized revenue are both on the file. One does not fill in for the other.
- Exposure and repayment performance are both on the file.
- Wallet savings frequency and SACCO balance are both on the file and are not averaged.
- Group membership and group repayment performance are both on the file.
- Expected harvest date and preferred repayment month are both on the file and are reconciled when the loan is structured.
- Irrigation, tenure, off-farm income, and years on the plot are each captured once.
- Off-farm income is yes/no unless a borderline debt-service ratio needs an optional amount.
- Market linkage starts as a category. Volume and consistency replace it as the scored metric only after a verifiable delivery season. Before that, the fallback is the category plus acreage times county-average yield.
- A routine credit-reference listing is scored only above KES 1,000 and only inside a recency window that is not yet chosen. It is not a gate. Identity fraud and active insolvency are gates. What “active insolvency” denotes is still open.
- Phone books are never read. Marital status and named family members are never collected. Sex is not a scoring input.
- Reference contacts and guarantors are people the farmer chooses to name.
- Each of identity, GPS, mobile money, cooperative data, and the bureau has its own consent moment.
- Property details (tenure, livestock, ownership) have their own express consent.
- GPS is for satellite and weather on this application.
- The impact assessment comes before live scoring, on the assumption that this profiling meets the Act’s high-risk test.
- No Ardhisasa path. Tenure is the farmer’s statement plus field attestation.
- Agro-input purchases are inferred from mobile-money counterparties and, where a photo exists, a receipt. Statement lines do not identify certified seed versus recycled seed by themselves.

## Edge cases the research treats as normal

- Strong yield, weak revenue. The farmer grew it and did not get paid. That is the case the two fields exist to see.
- No cooperative membership. Common. Scored as absence of that evidence.
- A positive PAYGo history beside a sub-1,000 negative listing. The listing does not count. The PAYGo history can.
- A long chama membership with a poor group record. Membership will not rescue performance.
- A preferred repayment month that is not the harvest month. Legitimate. Structuring says so explicitly.
- Satellite series missing because of cloud or a short history. The factor is unavailable. The rest of the file still decides.
- Untitled land. The usual smallholder case. The file does not wait for a title search.

## Open questions

Carried in manifest section C. They include the six parameters the merged list noticed and did not adopt: household size, post-harvest loss as its own field, insurance already held, extension engagement, distance to market, and phone type. Also carried: the bureau recency length, score bands, the serviceable area and the crop list, fairness storage of sex, ODPC registration thresholds, the credit-reference appeal, who may pull a bureau report, the meaning of active insolvency, retention periods, and cross-border vendors.

## Fidelity

Entities above are the research’s terms, with Act terms where the Act defines them (sensitive personal data, consent, negative information, credit score). Rules are tied to a named source or sit in manifest section E. The open-question list is non-empty. No practitioner has read this list back. KIAMIS field names, the high-risk characterization, and the lawful path to a bureau report are assumptions, not observations.
