# SLICE 1 — Yield and revenue stay separate

**status:** card_accepted

**Claim:** CL1 — Yield and realized revenue stay separate fields. The gap between volume and KES is a signal, not noise to be averaged. A file with strong yield and weak buyer revenue must produce a different limit from the same yield with matching revenue.

**In scope:** One season on a farmer's file. Yield (kg or bags per acre) and realized revenue (KES from a buyer or cooperative sales record) are stored as separate facts. The limit moves when realized revenue moves and yield is held constant. The gap between volume and KES stays on the file. Two files settle it: the same strong yield, one with weak buyer revenue and one with matching revenue.

**Deferred:**

| What | What brings it back |
|---|---|
| Score bands and weights (C8) | A credit-policy sheet. Until then the two files only have to produce different limits. |
| Post-harvest loss as its own field (C2) | A loss record separate from the sales receipt, and a decision that it changes the limit. |
| A computed production-capacity ceiling (A7) | A policy rule for how physical output caps the limit while yield and realized revenue stay separate. |
| Attested yield, and a live buyer or cooperative sales pull | An extension attestation or a sales record that is actually connected. This slice reads both facts already on the file. |
| A file with yield and no sales record | A policy rule for the limit when realized revenue is absent. Both settling files have revenue. |
| Market-linkage category, delivery history, and the acreage × county-yield fallback | CL2 is the slice. |
| Climate, term, and insurance on this limit | CL5 is the slice. |

**Permanently excluded:**

| What | Reason |
|---|---|
| One combined production number in place of yield and realized revenue | The gap between volume and KES is the signal (B1). |
| Declining an applicant for climate, drought geography, NDVI, or rainfall deficit | Those facts size, term, insure, or monitor. They are not an accept or decline (D6). |
| Land-registry title search | No usable third-party path for most smallholders. This slice does not use tenure (D16). |
| Sex or gender as a scoring input | Sensitive personal data, and asset fields already skew male (D4). |

**Falsified if:** The strong-yield weak-revenue file and the strong-yield matching-revenue file produce the same limit, or the limit is taken from one combined production number.

**Done when:** Those two files produce different limits, and each file still shows yield and realized revenue as separate fields.

**Secondary claims touched:** CL2, because yield is stored and its no-history fallback estimates output from acreage times county yield. CL5, because climate also structures the loan. This slice settles neither.
