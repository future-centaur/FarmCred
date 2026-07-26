"""Score history -- every score_farmer() output, timestamped, never overwritten
in place (PRD s3.2). Feeds the eventual transition from rules-based bands to a
fitted model once repayment outcomes accumulate.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .db import get_conn


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def save_score(farmer_id: str, result: Dict[str, Any]) -> Dict[str, str]:
    score_id = f"score_{uuid.uuid4().hex[:12]}"
    scored_at = _now()
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO score_history (score_id, farmer_id, payload, scored_at) VALUES (?, ?, ?, ?)",
            (score_id, farmer_id, json.dumps(result), scored_at),
        )
    return {"score_id": score_id, "scored_at": scored_at}


def get_latest_score(farmer_id: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            """SELECT payload, scored_at FROM score_history
               WHERE farmer_id = ? ORDER BY scored_at DESC LIMIT 1""",
            (farmer_id,),
        ).fetchone()
    if row is None:
        return None
    payload = json.loads(row["payload"])
    payload["scored_at"] = row["scored_at"]
    return payload


def get_score_history(farmer_id: str) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT payload, scored_at FROM score_history
               WHERE farmer_id = ? ORDER BY scored_at DESC""",
            (farmer_id,),
        ).fetchall()
    out = []
    for row in rows:
        payload = json.loads(row["payload"])
        payload["scored_at"] = row["scored_at"]
        out.append(payload)
    return out
