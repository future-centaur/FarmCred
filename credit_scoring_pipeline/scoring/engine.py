"""Gates -> bands -> composite -> loan structuring.

This module deliberately does not call connectors itself. Callers (the CLI
demo, the API service layer) resolve each source to a ``ConnectorRecord``
first -- ``{"payload": {...}, "fetched": bool}`` -- and pass the whole map in
as ``connector_data``. That keeps consent-gating (a source a farmer hasn't
consented to yet is simply absent from the map) entirely outside the scoring
logic, which only ever asks "what did I get" and "did the fetch succeed".

The three-way split the PRD insists on preserving:

* **Eligibility gates** (:func:`check_eligibility_gates`) -- pass/fail,
  short-circuits everything else.
* **Parameter bands -> composite score** -- the four creditworthiness
  parameters in ``config.SCORE_WEIGHTS``.
* **Loan structuring** (:func:`_structure_loan`) -- production capacity +
  climate exposure only, never fed back into eligibility or the score.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, TypedDict

import config
from connectors import ConnectorUnavailableError, get_connector

from . import bands as bands_mod


class ConnectorRecord(TypedDict, total=False):
    payload: Dict[str, Any]
    fetched: bool


ConnectorDataMap = Dict[str, ConnectorRecord]


def _get(connector_data: ConnectorDataMap, source: str) -> tuple[Dict[str, Any], bool]:
    record = connector_data.get(source)
    if record is None:
        return {}, False
    return (record.get("payload") or {}), bool(record.get("fetched"))


def fetch_all_live(farmer_id: str) -> ConnectorDataMap:
    """Fetch every source directly from its configured connector.

    Used by the CLI demo and tests, which don't model a consent/cache layer.
    The API service layer instead builds its ``ConnectorDataMap`` from
    whatever has actually been refreshed (and consented to) so far.
    """
    out: ConnectorDataMap = {}
    for source in config.CONNECTOR_SOURCES:
        try:
            payload = get_connector(source).fetch(farmer_id)
            out[source] = {"payload": payload, "fetched": True}
        except ConnectorUnavailableError:
            out[source] = {"payload": {}, "fetched": False}
    return out


def check_eligibility_gates(
    farmer: Dict[str, Any],
    kiamis: Optional[Dict[str, Any]],
    crb_paygo: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Hard pass/fail checks that sit outside the score entirely.

    Absence of KIAMIS or CRB data never itself trips a gate -- gates only
    trip on evidence, never on a missing lookup. (A background lookup that
    hasn't resolved yet just means gates checked so far pass; the API layer
    is responsible for not scoring until the required phases have run.)
    """
    gate_failures = []
    kiamis = kiamis or {}
    crb_paygo = crb_paygo or {}
    elig = config.ELIGIBILITY

    crop = farmer.get("crop")
    if crop is not None and crop not in elig["financed_value_chains"]:
        gate_failures.append(
            {
                "gate": "unfinanced_value_chain",
                "reason": f"'{crop}' is not a value chain this lender currently finances.",
            }
        )

    county = farmer.get("county")
    if county is not None and county not in elig["serviceable_counties"]:
        gate_failures.append(
            {
                "gate": "out_of_service_area",
                "reason": f"'{county}' county is outside the current service footprint.",
            }
        )

    if elig["require_identity_match"] and kiamis.get("national_id"):
        typed_id = farmer.get("national_id")
        registry_id = kiamis.get("national_id")
        if typed_id and registry_id and typed_id != registry_id:
            gate_failures.append(
                {
                    "gate": "failed_kyc",
                    "reason": "Typed national ID does not match the KIAMIS registry record.",
                }
            )

    self_reported = kiamis.get("land_size_acres_self_reported")
    verified = kiamis.get("land_size_acres_satellite_verified")
    if self_reported and verified is not None:
        ratio = verified / self_reported if self_reported else 0
        if ratio < elig["min_satellite_to_self_report_ratio"]:
            gate_failures.append(
                {
                    "gate": "unverifiable_plot_location",
                    "reason": (
                        "Satellite-verified acreage is far below the self-reported "
                        "plot size, suggesting the GPS pin is not on the farmer's plot."
                    ),
                }
            )

    if crb_paygo.get("has_crb_file"):
        for listing in crb_paygo.get("negative_listings") or []:
            if (
                listing.get("amount_kes", 0) >= elig["crb_negative_listing_gate_kes"]
                and listing.get("months_ago", 9999)
                <= elig["crb_negative_listing_gate_lookback_months"]
            ):
                gate_failures.append(
                    {
                        "gate": "active_insolvency",
                        "reason": (
                            f"A KES {listing['amount_kes']:,} negative listing "
                            f"{listing['months_ago']} months ago exceeds the active-"
                            "insolvency threshold."
                        ),
                    }
                )
                break

        if crb_paygo.get("existing_loan_balance_kes", 0) >= elig["crb_existing_balance_gate_kes"]:
            gate_failures.append(
                {
                    "gate": "over_leveraged",
                    "reason": (
                        f"Existing loan balance of KES "
                        f"{crb_paygo['existing_loan_balance_kes']:,} exceeds the "
                        "over-leverage threshold."
                    ),
                }
            )

    return {"eligible": not gate_failures, "gate_failures": gate_failures}


def _round_to(amount: float, step: int) -> int:
    return int(round(amount / step) * step)


def _structure_loan(production_capacity: Dict[str, Any], climate_exposure: Dict[str, Any]) -> Dict[str, Any]:
    ls = config.LOAN_STRUCTURING
    cap_points = production_capacity["points"]
    climate_points = climate_exposure["points"]

    base = ls["capacity_base_kes"][cap_points]
    multiplier = ls["climate_multiplier"][climate_points]
    amount = base * multiplier
    amount = max(ls["min_loan_floor_kes"], min(ls["max_loan_ceiling_kes"], amount))
    amount = _round_to(amount, ls["rounding_kes"])

    term_months = ls["term_months_by_climate"][climate_points]
    insurance_mandatory = climate_points <= ls["insurance_mandatory_at_or_below_climate_points"]

    rationale = (
        f"Production-capacity band {cap_points}/5 sizes a KES {base:,} base need; "
        f"climate-exposure band {climate_points}/5 applies a "
        f"{multiplier:.0%} multiplier and a {term_months}-month term"
        + (", with mandatory index insurance." if insurance_mandatory else ".")
    )

    return {
        "max_loan_amount_kes": amount,
        "term_months": term_months,
        "insurance_mandatory": insurance_mandatory,
        "rationale": rationale,
    }


def score_farmer(
    farmer: Dict[str, Any], connector_data: Optional[ConnectorDataMap] = None
) -> Dict[str, Any]:
    """Gates -> bands -> composite -> loan structuring for one farmer.

    ``connector_data`` maps source -> ``{"payload": dict, "fetched": bool}``.
    If omitted, every source is fetched live via its registered connector
    (the CLI-demo / test-suite path); the API service layer instead passes in
    whatever has already been refreshed and consented to.
    """
    if connector_data is None:
        connector_data = fetch_all_live(farmer["farmer_id"])

    raw_sources_used = {s: _get(connector_data, s)[1] for s in config.CONNECTOR_SOURCES}

    kiamis, _ = _get(connector_data, "kiamis")
    crb_paygo, _ = _get(connector_data, "crb_paygo")

    gate_result = check_eligibility_gates(farmer, kiamis, crb_paygo)
    if not gate_result["eligible"]:
        return {
            "eligible": False,
            "gate_failures": gate_result["gate_failures"],
            "raw_sources_used": raw_sources_used,
        }

    cooperative, _ = _get(connector_data, "cooperative")
    agrovet_mpesa, _ = _get(connector_data, "agrovet_mpesa")
    climate, _ = _get(connector_data, "climate")

    parameter_bands = {
        "cash_flow_stability": bands_mod.cash_flow_stability(agrovet_mpesa),
        "repayment_history": bands_mod.repayment_history(crb_paygo, cooperative),
        "market_linkage": bands_mod.market_linkage(cooperative),
        "social_collateral": bands_mod.social_collateral(cooperative),
    }

    weighted_points = sum(
        config.SCORE_WEIGHTS[param] * band["points"] for param, band in parameter_bands.items()
    )
    composite_score_0_100 = round(weighted_points / config.BAND_MAX_POINTS * 100)

    production_capacity = bands_mod.production_capacity(kiamis)
    climate_exposure = bands_mod.climate_exposure(climate, crb_paygo)
    loan_structuring = _structure_loan(production_capacity, climate_exposure)

    return {
        "eligible": True,
        "gate_failures": [],
        "production_capacity": production_capacity,
        "climate_exposure": climate_exposure,
        "parameter_bands": parameter_bands,
        "composite_score_0_100": composite_score_0_100,
        "loan_structuring": loan_structuring,
        "raw_sources_used": raw_sources_used,
    }


def score_tier(composite_score_0_100: int) -> str:
    """Map a raw score to the farmer-facing tier label (PRD s5.3)."""
    for floor, label in config.SCORE_TIERS:
        if composite_score_0_100 >= floor:
            return label
    return config.SCORE_TIERS[-1][1]
