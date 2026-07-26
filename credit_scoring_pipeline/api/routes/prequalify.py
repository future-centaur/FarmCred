"""POST /v1/prequalify -- instant, no login, no connector calls (PRD s3.1, s5.1)."""

from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

import config
from api.store import farmer_store

router = APIRouter(tags=["prequalify"])


class PrequalifyRequest(BaseModel):
    phone: str
    ward: str
    county: Optional[str] = None
    crop: str
    land_size_band: str
    loan_purpose: str


class PrequalifyResponse(BaseModel):
    prequalified: bool
    reasons: List[str]


@router.post("/v1/prequalify", response_model=PrequalifyResponse)
def prequalify(body: PrequalifyRequest) -> PrequalifyResponse:
    elig = config.ELIGIBILITY
    reasons: List[str] = []

    if body.crop not in elig["financed_value_chains"]:
        reasons.append(
            f"'{body.crop}' is not a value chain this lender currently finances here."
        )

    if body.county is not None and body.county not in elig["serviceable_counties"]:
        reasons.append(f"'{body.county}' county is outside the current service footprint.")

    if body.land_size_band not in elig["land_size_bands"]:
        reasons.append("Land size band is not recognised.")

    prequalified = not reasons
    farmer_store.save_prequalify_session(
        phone=body.phone,
        county=body.county,
        ward=body.ward,
        crop=body.crop,
        land_size_band=body.land_size_band,
        loan_purpose=body.loan_purpose,
        prequalified=prequalified,
        reasons=reasons,
    )
    return PrequalifyResponse(prequalified=prequalified, reasons=reasons)


@router.get("/v1/config/eligibility")
def eligibility_config() -> dict:
    return config.ELIGIBILITY
