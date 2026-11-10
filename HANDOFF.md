# HANDOFF — Farmcred

**Maintained by:** the agent, rewritten when a claim is banked.
**Read by:** the next slice, before ranking. This is the single picture of what the system currently is.
**Corrected by:** the human, only where it has missed a commitment or a connection the agent does not hold.

---

**Last updated:** 2026-11-10 · **Last slice banked:** none · **Unaccounted count at last verification:** none yet
**in_flight:** slice 1 — Yield and revenue stay separate

## Built

What exists and works, one line each. Name the slice that built it.

| What | Slice | Where in the repo |
|---|---|---|

## Deferred

Everything excluded by decision and expected back. **Each needs the condition that returns it.** A row deferred twice with no later slice claiming it is abandonment wearing a deferral label — Verification surfaces those, and the human rules on them.

| What | Deferred since slice | What brings it back | Times deferred |
|---|---|---|---|

## Permanently excluded

Never to be built, with the reason (regulatory, ethical, architectural). Kept here so a later slice cannot quietly pick it up as a feature.

| What | Reason |
|---|---|
| Reading the phone book or contacts, at scoring or in collection | CBK Digital Credit Providers Regulations 2022, reg 20, bans that access in debt collection. The product rule is wider: never read it. A reference is typed by the farmer. |
| Marital status | Sensitive personal data under the Data Protection Act. No proportionate purpose on this file. |
| Names of a spouse, children, or parents | Sensitive personal data. A later household-size count, if adopted, is an aggregate only. |
| Sex or gender as a scoring input | Sensitive personal data, and asset fields already skew male. Fairness storage is still an open question, not a score weight. |
| Land-registry title search (Ardhisasa) | No usable third-party path for most smallholders. Tenure is self-report plus field attestation. |
| Declining an applicant for climate, drought geography, NDVI, or rainfall deficit | Those facts size, term, insure, or monitor. They are not an accept/decline. |
| One combined production number in place of yield and revenue | The gap between volume and KES is the signal. |
| One combined savings number across wallet frequency and SACCO balance | They are different instruments. |
| An automatic knockout for a routine credit-reference default | Points only, and only above KES 1,000 inside a window still to be set. Gates are identity fraud, active insolvency, area, and crop. |

## Claims supported

Banked claims. The regression pass checks new work against these — breaking one blocks banking regardless of how clean the conservation table is.

| Claim id | Statement | Banked at slice |
|---|---|---|

## Questions still stubbed

Open manifest questions the build was told to stub rather than invent. Each stays here until a slice takes a claim that settles it, or it is deliberately left open.

| Question id | What is stubbed | What would settle it |
|---|---|---|
| C1 | Household size or dependency ratio | Credit policy: does an aggregate count change limit or price? |
| C2 | Post-harvest loss as its own field | A loss record separate from the sales receipt, and whether it changes the limit. |
| C3 | Insurance already held | A named product and the structuring rule it changes. |
| C4 | Extension or advisory engagement | A real source, and evidence it predicts repayment beyond inputs and yield. |
| C5 | Distance to suppliers and markets | A definition computable from the plot pin, and the decision it is allowed to change. |
| C6 | Phone type and digital literacy | A shorter path for feature phones, or a decision that phone type only routes the journey. |
| C7 | Credit-reference recency window | A length from credit policy or from CBK. |
| C8 | Score bands and weights | A credit-policy sheet. |
| C9 | Serviceable area and financed crops | The lender’s list. |
| C10 | Storing sex for fairness monitoring | A DPA s.45 ground accepted in the DPIA, or a decision not to store it. |
| C11 | ODPC registration regardless of revenue | The Commissioner’s threshold notice for this industry. |
| C12 | Whether the 2020 credit-reference regulations survive appeal | The Court of Appeal’s final decision, or a replacement instrument. |
| C13 | Who may pull a bureau report | The operator’s licence or a written agency agreement. |
| C14 | The meaning of active insolvency | A map onto bureau codes or a court status. |
| C15 | Retention when no loan is booked | A written schedule. |
| C16 | Which fields may leave Kenya | A vendor-country list with a safeguard or specific consent for each. |

---

## Agent notes

**Resolution ledger:** before any exploratory debugging, search `C:\Users\user\OneDrive\Desktop\BFG\Centaur-vault\Auxiliary stocks\ledger\entries\` for the error signature. After resolving an error, write one new entry file there. Never edit an existing entry.

**Slice concurrency:** one slice in flight at a time. Read `in_flight`. If it names a slice this chat did not start, stop. `none` means no slice is held.
