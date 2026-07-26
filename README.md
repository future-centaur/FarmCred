# FarmCred -- Smallholder Farmer Credit Scoring (Kenya Pilot)

Alternative agricultural credit-scoring platform for Kenyan smallholder farmers. A
rules-based scorecard (not yet a trained ML model -- no historical repayment-outcome
data exists yet) that fuses mobile-money behaviour, cooperative delivery records,
satellite-derived climate exposure, land/identity registry data, and bureau history,
behind a single swappable connector interface per data source.

See `PRD_Smallholder_Credit_Scoring.docx` for the full product requirements.

## Structure

- `credit_scoring_pipeline/` -- Python backend: config, connectors, scoring engine, FastAPI service, SQLite persistence.
- `frontend/` -- React + Vite single-page app implementing the phased consent flow.

## Running the backend

From the repo root:

```bash
pip install -e ".[dev]"
uvicorn api.main:app --reload --app-dir credit_scoring_pipeline --port 8000
```

This serves the API at `http://localhost:8000` and creates `farmcred.db` (SQLite) in
whatever directory you ran the command from.

Or the CLI demo (no HTTP layer, no persistence -- just prints scores for the shipped
demo profiles straight from the scoring engine):

```bash
python credit_scoring_pipeline/run_pipeline.py
```

Run the test suite with:

```bash
pytest
```

## Running the frontend

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173. The Vite dev server proxies `/v1` and `/health` calls
to `http://localhost:8000`, so the backend must be running first.

## Walking through the app

Fill in the Pre-Qualify form with a serviceable county/crop (e.g. county `kericho`,
crop `tea`) to proceed. Every farmer registered through the live app gets a freshly
generated, internally-consistent set of mock connector data (seeded on their farmer ID)
-- so scores and gate outcomes will vary run to run, exactly as they would against a
real, varied farmer population. Registering with a non-serviceable crop/county (e.g.
`macadamia`) is rejected at Pre-Qualify before anything else runs.

## Connector modes

Every external data source runs in `mock` mode by default (see
`credit_scoring_pipeline/config.py`). Flip one source to `live` with
`CONNECTOR_MODE_<SOURCE>=live` once a `LiveXConnector` is registered --
gates, bands, and the composite calculation require no other code change.

## Demo farmers (CLI only)

`credit_scoring_pipeline/data/mock_farmers.py` ships seven curated profiles used by
`run_pipeline.py` and the test suite to illustrate specific scoring scenarios:

- `F001` -- clean file (Strong)
- `F002` -- thin file, no CRB/co-op record (resolves to the neutral band, not the floor)
- `F003` -- high risk, mitigated by owned irrigation
- `F004`-`F007` -- one eligibility-gate trip each (unfinanced crop, out of area, active insolvency, failed KYC)

These fixed IDs aren't reachable through the live web app (farmer IDs there are
server-generated on registration) -- they exist to give the CLI demo and automated
tests a stable, hand-verifiable story per PRD s9.

## Known MVP limitations

- **Synthetic data is in-memory.** A farmer registered through the live app gets a
  synthetic connector profile generated once, at registration, and held in a
  process-local dict -- restarting the backend before scoring a given farmer will
  lose that synthetic linkage (the curated `F001`-`F007` profiles are unaffected,
  since they're hardcoded). Fine for a single demo session; would need to move to
  persisted/seeded fixtures for anything longer-lived.
- **No async job queue.** Phase 3's "background enrichment" and Phase 4's "async
  co-op uplift push notification" both run synchronously inline with the triggering
  request rather than on a real task queue -- the frontend still presents them as a
  brief loading state / a later revisit, per the PRD's UX, but there's no actual
  background worker underneath yet.
- **No fairness-monitoring store.** Gender is deliberately never collected in this
  API surface (it's excluded from scoring per PRD s8's non-scope list), so the
  disparate-impact monitoring store described in PRD s3.2 isn't built.
- **English only.** No Swahili i18n yet.
