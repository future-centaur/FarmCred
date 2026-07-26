"""POST /v1/farmers -- creates the Farmer record and triggers Phase-3
background KIAMIS + climate lookups the instant GPS + Phase-1 consent exist
(PRD s3.1, s5.2). The MVP runs that background step inline rather than on a
task queue; ConnectorUnavailableError resolves to a cache miss, never a 5xx
(PRD s4 error convention).
"""

from __future__ import annotations

from typing import List, Literal, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from connectors import ConnectorUnavailableError, get_connector
from api.store import farmer_store
from data.mock_farmers import register_synthetic_farmer

router = APIRouter(tags=["farmers"])

ConsentCategory = Literal["kiamis_gps", "mpesa", "cooperative", "crb"]


class GpsPin(BaseModel):
    lat: float
    lon: float


class CreateFarmerRequest(BaseModel):
    phone: str
    national_id: str
    gps_pin: GpsPin
    tenure_status: str
    crop: str
    secondary_crops: List[str] = []
    land_size_acres: float
    county: Optional[str] = None
    ward: Optional[str] = None
    land_size_band: Optional[str] = None
    loan_purpose: Optional[str] = None


class CreateFarmerResponse(BaseModel):
    farmer_id: str


def _background_refresh(farmer_id: str, source: str) -> None:
    try:
        payload = get_connector(source).fetch(farmer_id)
        farmer_store.save_connector_result(farmer_id, source, payload, fetched=True)
    except ConnectorUnavailableError:
        farmer_store.save_connector_result(farmer_id, source, {}, fetched=False)


@router.post("/v1/farmers", response_model=CreateFarmerResponse)
def create_farmer(body: CreateFarmerRequest) -> CreateFarmerResponse:
    farmer_id = farmer_store.create_farmer(
        phone=body.phone,
        national_id=body.national_id,
        gps_lat=body.gps_pin.lat,
        gps_lon=body.gps_pin.lon,
        tenure_status=body.tenure_status,
        crop=body.crop,
        secondary_crops=body.secondary_crops,
        land_size_acres=body.land_size_acres,
        county=body.county,
        ward=body.ward,
        land_size_band=body.land_size_band,
        loan_purpose=body.loan_purpose,
    )

    register_synthetic_farmer(
        farmer_id,
        {
            "farmer_id": farmer_id,
            "phone": body.phone,
            "national_id": body.national_id,
            "county": body.county,
            "ward": body.ward,
            "crop": body.crop,
            "secondary_crops": body.secondary_crops,
            "land_size_band": body.land_size_band,
            "land_size_acres": body.land_size_acres,
            "loan_purpose": body.loan_purpose,
            "tenure_status": body.tenure_status,
            "gps_lat": body.gps_pin.lat,
            "gps_lon": body.gps_pin.lon,
        },
    )

    # Submitting the GPS pin at Phase 1 *is* the kiamis_gps consent event (the
    # map-pin explainer is the plain-language purpose line) -- log it so every
    # consent category still has its own timestamped record (PRD s9).
    farmer_store.record_consent(farmer_id, "kiamis_gps", True, "en")

    # Phase 3: GPS + Phase-1 consent alone is sufficient to trigger these two
    # lookups -- no further farmer action, invisible to the farmer.
    _background_refresh(farmer_id, "kiamis")
    _background_refresh(farmer_id, "climate")

    return CreateFarmerResponse(farmer_id=farmer_id)


@router.get("/v1/farmers/{farmer_id}")
def read_farmer(farmer_id: str) -> dict:
    farmer = farmer_store.get_farmer(farmer_id)
    if farmer is None:
        raise HTTPException(status_code=404, detail="farmer not found")
    farmer["consents"] = farmer_store.get_consents(farmer_id)
    farmer["raw_sources_used"] = farmer_store.get_raw_sources_used(farmer_id)
    return farmer


class ConsentRequest(BaseModel):
    category: ConsentCategory
    granted: bool
    locale: str = "en"


class ConsentResponse(BaseModel):
    consent_id: str
    recorded_at: str


@router.post("/v1/farmers/{farmer_id}/consent", response_model=ConsentResponse)
def record_consent(farmer_id: str, body: ConsentRequest) -> ConsentResponse:
    if farmer_store.get_farmer(farmer_id) is None:
        raise HTTPException(status_code=404, detail="farmer not found")
    result = farmer_store.record_consent(farmer_id, body.category, body.granted, body.locale)
    return ConsentResponse(**result)
