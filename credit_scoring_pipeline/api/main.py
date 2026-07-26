"""FastAPI app, route registration -- the thin service layer PRD s4 calls for.

Each route maps directly onto an existing pipeline function (config, scoring,
connectors); this module wires transport, not logic.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import connectors, farmers, los, prequalify, scores
from api.store.db import init_db

app = FastAPI(
    title="FarmCred Smallholder Credit Scoring API",
    version="0.1.0",
    description="Rules-based scorecard and connector pipeline for Kenyan smallholder farmers.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


app.include_router(prequalify.router)
app.include_router(farmers.router)
app.include_router(connectors.router)
app.include_router(scores.router)
app.include_router(los.router)
