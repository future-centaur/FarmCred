"""Farmer profile store, consent log, and raw connector cache (PRD s3.2).

Every consent category is logged as its own row with its own timestamp -- the
PRD is explicit that a single blanket checkbox is never acceptable.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .db import get_conn

CONSENT_CATEGORIES = ("kiamis_gps", "mpesa", "cooperative", "crb")

# Which consent category gates which connector's /refresh endpoint.
CONNECTOR_CONSENT_CATEGORY = {
    "kiamis": "kiamis_gps",
    "climate": "kiamis_gps",
    "agrovet_mpesa": "mpesa",
    "cooperative": "cooperative",
    "crb_paygo": "crb",
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def save_prequalify_session(
    phone: str,
    county: Optional[str],
    ward: str,
    crop: str,
    land_size_band: str,
    loan_purpose: str,
    prequalified: bool,
    reasons: List[str],
) -> str:
    session_id = _new_id("pq")
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO prequalify_sessions
               (session_id, phone, county, ward, crop, land_size_band,
                loan_purpose, prequalified, reasons, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session_id,
                phone,
                county,
                ward,
                crop,
                land_size_band,
                loan_purpose,
                int(prequalified),
                json.dumps(reasons),
                _now(),
            ),
        )
    return session_id


def create_farmer(
    phone: str,
    national_id: str,
    gps_lat: float,
    gps_lon: float,
    tenure_status: str,
    crop: str,
    secondary_crops: List[str],
    land_size_acres: float,
    county: Optional[str] = None,
    ward: Optional[str] = None,
    land_size_band: Optional[str] = None,
    loan_purpose: Optional[str] = None,
) -> str:
    farmer_id = _new_id("F")
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO farmers
               (farmer_id, phone, national_id, county, ward, crop,
                secondary_crops, land_size_band, land_size_acres, loan_purpose,
                tenure_status, gps_lat, gps_lon, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                farmer_id,
                phone,
                national_id,
                county,
                ward,
                crop,
                json.dumps(secondary_crops),
                land_size_band,
                land_size_acres,
                loan_purpose,
                tenure_status,
                gps_lat,
                gps_lon,
                _now(),
            ),
        )
    return farmer_id


def get_farmer(farmer_id: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM farmers WHERE farmer_id = ?", (farmer_id,)).fetchone()
    if row is None:
        return None
    farmer = dict(row)
    farmer["secondary_crops"] = json.loads(farmer["secondary_crops"] or "[]")
    return farmer


def record_consent(farmer_id: str, category: str, granted: bool, locale: Optional[str]) -> Dict[str, str]:
    consent_id = _new_id("consent")
    recorded_at = _now()
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO consents (consent_id, farmer_id, category, granted, locale, recorded_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (consent_id, farmer_id, category, int(granted), locale, recorded_at),
        )
    return {"consent_id": consent_id, "recorded_at": recorded_at}


def get_consents(farmer_id: str) -> Dict[str, bool]:
    """Latest granted/revoked state per category (last write wins)."""
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT category, granted FROM consents
               WHERE farmer_id = ? ORDER BY recorded_at ASC""",
            (farmer_id,),
        ).fetchall()
    state: Dict[str, bool] = {}
    for row in rows:
        state[row["category"]] = bool(row["granted"])
    return state


def has_consent(farmer_id: str, category: str) -> bool:
    return get_consents(farmer_id).get(category, False)


def save_connector_result(farmer_id: str, source: str, payload: Dict[str, Any], fetched: bool) -> str:
    cached_at = _now()
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO connector_cache (farmer_id, source, payload, fetched, cached_at)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(farmer_id, source) DO UPDATE SET
                 payload = excluded.payload,
                 fetched = excluded.fetched,
                 cached_at = excluded.cached_at""",
            (farmer_id, source, json.dumps(payload), int(fetched), cached_at),
        )
    return cached_at


def get_connector_data(farmer_id: str) -> Dict[str, Dict[str, Any]]:
    """``{source: {"payload": {...}, "fetched": bool}}`` for every cached source."""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT source, payload, fetched FROM connector_cache WHERE farmer_id = ?",
            (farmer_id,),
        ).fetchall()
    return {
        row["source"]: {"payload": json.loads(row["payload"]), "fetched": bool(row["fetched"])}
        for row in rows
    }


def get_raw_sources_used(farmer_id: str) -> Dict[str, bool]:
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT source, fetched FROM connector_cache WHERE farmer_id = ?",
            (farmer_id,),
        ).fetchall()
    return {row["source"]: bool(row["fetched"]) for row in rows}
