"""POST/GET /v1/farmers/{id}/score, GET .../score/history (PRD s4).

Scoring runs over whatever connector data is already cached/consented so far
-- it never reaches into a live connector itself, so a farmer who skipped
Phase 4 still scores (with those parameters at NEUTRAL_BAND) rather than
being blocked.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.store import farmer_store, score_store
from scoring import score_farmer, score_tier

router = APIRouter(tags=["scores"])


def _score_and_save(farmer_id: str) -> dict:
    farmer = farmer_store.get_farmer(farmer_id)
    if farmer is None:
        raise HTTPException(status_code=404, detail="farmer not found")

    connector_data = farmer_store.get_connector_data(farmer_id)
    result = score_farmer(farmer, connector_data)
    if result["eligible"]:
        result["tier"] = score_tier(result["composite_score_0_100"])
    meta = score_store.save_score(farmer_id, result)
    return {**result, "scored_at": meta["scored_at"]}


@router.post("/v1/farmers/{farmer_id}/score")
def score(farmer_id: str) -> dict:
    return _score_and_save(farmer_id)


@router.get("/v1/farmers/{farmer_id}/score")
def latest_score(farmer_id: str) -> dict:
    if farmer_store.get_farmer(farmer_id) is None:
        raise HTTPException(status_code=404, detail="farmer not found")
    result = score_store.get_latest_score(farmer_id)
    if result is None:
        raise HTTPException(status_code=404, detail="no score on file for this farmer yet")
    return result


@router.get("/v1/farmers/{farmer_id}/score/history")
def score_history(farmer_id: str) -> list:
    if farmer_store.get_farmer(farmer_id) is None:
        raise HTTPException(status_code=404, detail="farmer not found")
    return score_store.get_score_history(farmer_id)
