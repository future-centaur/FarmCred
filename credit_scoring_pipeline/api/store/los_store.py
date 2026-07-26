"""Stub loan-origination-system hand-off (PRD s4, s8). Schema mirrors Mambu's
create-application response shape; this does not implement real servicing.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .db import get_conn


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_application(
    farmer_id: str,
    composite_score_0_100: Optional[int],
    loan_structuring: Optional[Dict[str, Any]],
    gate_failures: List[Dict[str, str]],
) -> Dict[str, str]:
    application_id = f"app_{uuid.uuid4().hex[:12]}"
    status = "approved_pending_disbursement" if not gate_failures else "declined"
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO los_applications
               (application_id, farmer_id, composite_score_0_100, loan_structuring,
                gate_failures, status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                application_id,
                farmer_id,
                composite_score_0_100,
                json.dumps(loan_structuring) if loan_structuring else None,
                json.dumps(gate_failures),
                status,
                _now(),
            ),
        )
    return {"application_id": application_id, "status": status}


def get_application(application_id: str) -> Optional[Dict[str, Any]]:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM los_applications WHERE application_id = ?", (application_id,)
        ).fetchone()
    return dict(row) if row else None


def record_disbursement(application_id: str, amount_kes: float, disbursed_at: str) -> Dict[str, str]:
    disbursement_id = f"disb_{uuid.uuid4().hex[:12]}"
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO los_disbursements
               (disbursement_id, application_id, amount_kes, disbursed_at, status)
               VALUES (?, ?, ?, ?, ?)""",
            (disbursement_id, application_id, amount_kes, disbursed_at, "disbursed"),
        )
    return {"disbursement_id": disbursement_id, "status": "disbursed"}


def record_repayment(application_id: str, amount_kes: float, paid_at: str, on_time: bool) -> Dict[str, str]:
    repayment_id = f"repay_{uuid.uuid4().hex[:12]}"
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO los_repayments
               (repayment_id, application_id, amount_kes, paid_at, on_time, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (repayment_id, application_id, amount_kes, paid_at, int(on_time), "recorded"),
        )
    return {"repayment_id": repayment_id, "status": "recorded"}
