"""POST /v1/farmers/{id}/connectors/{source}/refresh (PRD s4).

Gated on the consent category that covers each source (PRD s5.2's phased
consent flow) -- CRB additionally implies the prior-notice line has been
shown, since granting that consent is only offered after that screen renders.
Never raises: a live connector's ConnectorUnavailableError resolves to
``fetched: false``, never a 5xx.
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from connectors import ConnectorUnavailableError, get_connector
from api.store import farmer_store

router = APIRouter(tags=["connectors"])

Source = Literal["kiamis", "cooperative", "agrovet_mpesa", "crb_paygo", "climate"]


class RefreshResponse(BaseModel):
    source: str
    fetched: bool
    cached_at: str


@router.post("/v1/farmers/{farmer_id}/connectors/{source}/refresh", response_model=RefreshResponse)
def refresh_connector(farmer_id: str, source: Source) -> RefreshResponse:
    if farmer_store.get_farmer(farmer_id) is None:
        raise HTTPException(status_code=404, detail="farmer not found")

    required_category = farmer_store.CONNECTOR_CONSENT_CATEGORY[source]
    if not farmer_store.has_consent(farmer_id, required_category):
        raise HTTPException(
            status_code=403,
            detail=f"consent category '{required_category}' has not been granted",
        )

    try:
        payload = get_connector(source).fetch(farmer_id)
        fetched = True
    except ConnectorUnavailableError:
        payload = {}
        fetched = False

    cached_at = farmer_store.save_connector_result(farmer_id, source, payload, fetched)
    return RefreshResponse(source=source, fetched=fetched, cached_at=cached_at)
