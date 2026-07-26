"""Shared SQLite connection and schema for the farmer profile, consent log,
connector cache, score history, and stub-LOS tables (PRD s3.2).

One file, one connection helper -- ``farmer_store`` and ``score_store`` both
import :func:`get_conn` rather than each owning a schema fragment.
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

import config

_SCHEMA = """
CREATE TABLE IF NOT EXISTS prequalify_sessions (
    session_id TEXT PRIMARY KEY,
    phone TEXT NOT NULL,
    county TEXT,
    ward TEXT,
    crop TEXT,
    land_size_band TEXT,
    loan_purpose TEXT,
    prequalified INTEGER NOT NULL,
    reasons TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS farmers (
    farmer_id TEXT PRIMARY KEY,
    phone TEXT NOT NULL,
    national_id TEXT,
    county TEXT,
    ward TEXT,
    crop TEXT,
    secondary_crops TEXT,
    land_size_band TEXT,
    land_size_acres REAL,
    loan_purpose TEXT,
    tenure_status TEXT,
    gps_lat REAL,
    gps_lon REAL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS consents (
    consent_id TEXT PRIMARY KEY,
    farmer_id TEXT NOT NULL,
    category TEXT NOT NULL,
    granted INTEGER NOT NULL,
    locale TEXT,
    recorded_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS connector_cache (
    farmer_id TEXT NOT NULL,
    source TEXT NOT NULL,
    payload TEXT NOT NULL,
    fetched INTEGER NOT NULL,
    cached_at TEXT NOT NULL,
    PRIMARY KEY (farmer_id, source)
);

CREATE TABLE IF NOT EXISTS score_history (
    score_id TEXT PRIMARY KEY,
    farmer_id TEXT NOT NULL,
    payload TEXT NOT NULL,
    scored_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS los_applications (
    application_id TEXT PRIMARY KEY,
    farmer_id TEXT NOT NULL,
    composite_score_0_100 INTEGER,
    loan_structuring TEXT,
    gate_failures TEXT,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS los_disbursements (
    disbursement_id TEXT PRIMARY KEY,
    application_id TEXT NOT NULL,
    amount_kes REAL NOT NULL,
    disbursed_at TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS los_repayments (
    repayment_id TEXT PRIMARY KEY,
    application_id TEXT NOT NULL,
    amount_kes REAL NOT NULL,
    paid_at TEXT NOT NULL,
    on_time INTEGER NOT NULL,
    status TEXT NOT NULL
);
"""


def _db_path() -> str:
    match = re.match(r"sqlite:///(.+)", config.DATABASE_URL)
    return match.group(1) if match else "./farmcred.db"


def get_conn() -> sqlite3.Connection:
    path = _db_path()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(_SCHEMA)
