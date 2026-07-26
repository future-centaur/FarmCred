"""Stub LOS hand-off endpoints (PRD s4, s8). Schema mirrors Mambu's
create-application response shape; no real servicing/disbursement/collections.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from api.store import los_store

router = APIRouter(tags=["los"])


class LoanApplicationRequest(BaseModel):
    farmer_id: str
    composite_score_0_100: Optional[int] = None
    loan_structuring: Optional[Dict[str, Any]] = None
    gate_failures: List[Dict[str, str]] = []


class LoanApplicationResponse(BaseModel):
    application_id: str
    status: str


@router.post("/v1/los/loan-application", response_model=LoanApplicationResponse)
def create_loan_application(body: LoanApplicationRequest) -> LoanApplicationResponse:
    result = los_store.create_application(
        body.farmer_id, body.composite_score_0_100, body.loan_structuring, body.gate_failures
    )
    return LoanApplicationResponse(**result)


class DisbursementRequest(BaseModel):
    application_id: str
    amount_kes: float
    disbursed_at: str


class DisbursementResponse(BaseModel):
    disbursement_id: str
    status: str


@router.post("/v1/los/disbursement", response_model=DisbursementResponse)
def record_disbursement(body: DisbursementRequest) -> DisbursementResponse:
    if los_store.get_application(body.application_id) is None:
        raise HTTPException(status_code=404, detail="application not found")
    result = los_store.record_disbursement(body.application_id, body.amount_kes, body.disbursed_at)
    return DisbursementResponse(**result)


class RepaymentRequest(BaseModel):
    application_id: str
    amount_kes: float
    paid_at: str
    on_time: bool


class RepaymentResponse(BaseModel):
    repayment_id: str
    status: str


@router.post("/v1/los/repayment", response_model=RepaymentResponse)
def record_repayment(body: RepaymentRequest) -> RepaymentResponse:
    if los_store.get_application(body.application_id) is None:
        raise HTTPException(status_code=404, detail="application not found")
    result = los_store.record_repayment(body.application_id, body.amount_kes, body.paid_at, body.on_time)
    return RepaymentResponse(**result)
