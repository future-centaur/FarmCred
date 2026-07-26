"""One banding function per parameter -- the atomic unit of the model.

Every function returns a ``{"points": 1-5, "label": str, "why": str}`` dict,
never a raw number, and every function treats "no data" as
:data:`config.NEUTRAL_BAND` -- the midpoint, never the floor. That single rule
is what lets a thin-file farmer compete on the evidence that does exist
instead of being punished for evidence that was never collected (PRD s9).

Four of these feed the weighted composite score (``config.SCORE_WEIGHTS``):
``cash_flow_stability``, ``repayment_history``, ``market_linkage``,
``social_collateral``. Two are structuring-only and never touch the score:
``production_capacity``, ``climate_exposure``.
"""

from __future__ import annotations

import statistics
from datetime import date, datetime
from typing import Any, Dict, List, Optional

import config

Band = Dict[str, Any]


def _neutral() -> Band:
    return dict(config.NEUTRAL_BAND)


def _band(points: int, label: str, why: str) -> Band:
    points = max(config.BAND_MIN_POINTS, min(config.BAND_MAX_POINTS, points))
    return {"points": points, "label": label, "why": why}


def _label_for(points: int) -> str:
    return {1: "Weak", 2: "Fair", 3: "Moderate", 4: "Good", 5: "Strong"}[points]


# ---------------------------------------------------------------------------
# Scored parameters (weighted into composite_score_0_100)
# ---------------------------------------------------------------------------


def cash_flow_stability(agrovet_mpesa: Optional[Dict[str, Any]]) -> Band:
    """From mobile-money inflow level and month-to-month variance."""
    if not agrovet_mpesa:
        return _neutral()

    inflows: List[float] = agrovet_mpesa.get("monthly_inflows_kes") or []
    if not inflows:
        return _neutral()

    mean = statistics.mean(inflows)
    cv = (statistics.pstdev(inflows) / mean) if mean and len(inflows) > 1 else 0.0

    if mean >= 15_000:
        level = 5
    elif mean >= 10_000:
        level = 4
    elif mean >= 6_000:
        level = 3
    elif mean >= 3_000:
        level = 2
    else:
        level = 1

    if cv <= 0.20:
        variance_adj = 1
    elif cv <= 0.45:
        variance_adj = 0
    else:
        variance_adj = -1

    points = level + variance_adj
    if agrovet_mpesa.get("input_purchases_before_planting"):
        points += 1

    points = max(config.BAND_MIN_POINTS, min(config.BAND_MAX_POINTS, points))
    why = (
        f"Average monthly inflow of KES {mean:,.0f} with "
        f"{'low' if cv <= 0.20 else 'moderate' if cv <= 0.45 else 'high'} "
        f"month-to-month variance"
        + (
            "; buys inputs ahead of planting."
            if agrovet_mpesa.get("input_purchases_before_planting")
            else "."
        )
    )
    return _band(points, _label_for(points), why)


def repayment_history(
    crb_paygo: Optional[Dict[str, Any]], cooperative: Optional[Dict[str, Any]]
) -> Band:
    """Primarily from the bureau file; falls back to co-op loan-deduction
    servicing as a proxy for a farmer with no bureau file at all."""
    has_file = bool(crb_paygo) and crb_paygo.get("has_crb_file")

    if not has_file:
        deductions = (cooperative or {}).get("input_loan_deductions_last_12mo")
        if deductions is not None and deductions >= 2:
            return _band(
                4,
                "Good",
                f"No bureau file, but {deductions} on-time cooperative "
                "input-loan deductions in the last 12 months show a track "
                "record of servicing debt.",
            )
        return _neutral()

    negative_listings = crb_paygo.get("negative_listings") or []
    tradeline = crb_paygo.get("paygo_tradeline")
    points = 5
    why_parts: List[str] = ["Clean bureau file"]

    if negative_listings:
        most_recent = min(l["months_ago"] for l in negative_listings)
        largest = max(l["amount_kes"] for l in negative_listings)
        if most_recent <= 12:
            points -= 3
        elif most_recent <= 24:
            points -= 2
        else:
            points -= 1
        why_parts = [f"A KES {largest:,} negative listing {most_recent} months ago"]

    if tradeline in ("completed", "current_good"):
        points += 1
        why_parts.append("a PAYGo tradeline in good standing")
    elif tradeline == "delinquent":
        points -= 2
        why_parts.append("a delinquent PAYGo tradeline")

    points = max(config.BAND_MIN_POINTS, min(config.BAND_MAX_POINTS, points))
    return _band(points, _label_for(points), "; ".join(why_parts) + ".")


def market_linkage(cooperative: Optional[Dict[str, Any]]) -> Band:
    """From cooperative/off-taker delivery tier and delivery consistency."""
    if not cooperative:
        return _neutral()

    tier = cooperative.get("delivery_tier")
    seasons_with = cooperative.get("seasons_with_delivery", 0)
    seasons_total = cooperative.get("seasons_total", 0)
    ratio = (seasons_with / seasons_total) if seasons_total else 0.0

    tier_points = {"high": 5, "mid": 3, "low": 1}.get(tier, 3)
    if ratio >= 0.75:
        ratio_adj = 0
    elif ratio >= 0.5:
        ratio_adj = -1
    else:
        ratio_adj = -2

    points = max(config.BAND_MIN_POINTS, min(config.BAND_MAX_POINTS, tier_points + ratio_adj))
    why = (
        f"{tier or 'unranked'} delivery tier with {seasons_with}/{seasons_total} "
        "seasons delivered to the off-taker."
    )
    return _band(points, _label_for(points), why)


def social_collateral(cooperative: Optional[Dict[str, Any]]) -> Band:
    """From tenure inside the cooperative -- a proxy for social capital and
    peer/community standing that a bureau file cannot see."""
    if not cooperative:
        return _neutral()

    member_since = cooperative.get("member_since")
    years = _years_since(member_since)
    if years is None:
        return _neutral()

    if years >= 8:
        points = 5
    elif years >= 5:
        points = 4
    elif years >= 3:
        points = 3
    elif years >= 1:
        points = 2
    else:
        points = 1

    why = f"{years:.0f} years of continuous membership at {cooperative.get('cooperative_name', 'the cooperative')}."
    return _band(points, _label_for(points), why)


# ---------------------------------------------------------------------------
# Structuring-only parameters (never weighted into composite_score_0_100)
# ---------------------------------------------------------------------------


def production_capacity(kiamis: Optional[Dict[str, Any]]) -> Band:
    """From satellite-verified acreage and input-subsidy participation. Sizes
    the loan; never judges the farmer's creditworthiness."""
    if not kiamis:
        return _neutral()

    acres = kiamis.get("land_size_acres_satellite_verified")
    if acres is None:
        acres = kiamis.get("land_size_acres_self_reported", 0)

    if acres >= 3:
        points = 5
    elif acres >= 2:
        points = 4
    elif acres >= 1.2:
        points = 3
    elif acres >= 0.7:
        points = 2
    else:
        points = 1

    subsidy_seasons = len(kiamis.get("input_subsidy_history") or [])
    if subsidy_seasons >= 2:
        points = min(config.BAND_MAX_POINTS, points + 1)

    why = f"{acres:.1f} satellite-verified acres under {kiamis.get('crop', 'crop')}."
    return _band(points, _label_for(points), why)


def climate_exposure(
    climate: Optional[Dict[str, Any]], crb_paygo: Optional[Dict[str, Any]]
) -> Band:
    """From regional exposure classification and rainfall deficit, mitigated
    one step by owned/financed irrigation. 5 = least exposed. Sizes the loan
    (term, insurance); never judges the farmer's creditworthiness."""
    if not climate:
        return _neutral()

    exposure = climate.get("regional_exposure")
    rainfall_deficit = climate.get("rainfall_deficit_pct", 0)

    base = {"low": 5, "moderate": 4, "elevated": 3, "high": 2, "severe": 1}.get(exposure, 3)
    if rainfall_deficit >= 40:
        base = min(base, 1)
    elif rainfall_deficit >= 25:
        base = min(base, 2)

    mitigated = bool(crb_paygo) and crb_paygo.get("sunculture_owner")
    points = base
    why = f"{exposure or 'unclassified'} regional exposure, {rainfall_deficit}% rainfall deficit"
    if mitigated:
        points = min(config.BAND_MAX_POINTS, points + 1)
        why += "; irrigation ownership mitigates exposure one band."
    else:
        why += "."

    points = max(config.BAND_MIN_POINTS, min(config.BAND_MAX_POINTS, points))
    return _band(points, _label_for(points), why)


def _years_since(iso_date: Optional[str]) -> Optional[float]:
    if not iso_date:
        return None
    try:
        then = datetime.strptime(iso_date, "%Y-%m-%d").date()
    except ValueError:
        return None
    days = (date.today() - then).days
    return days / 365.25 if days > 0 else 0.0
