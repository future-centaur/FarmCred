"""CLI demo entrypoint -- no HTTP layer, prints the full scorecard for every
shipped demo profile (PRD s6). Useful for a quick sanity check of the scoring
engine on its own, independent of the API/frontend.
"""

from __future__ import annotations

from data.mock_farmers import all_farmer_ids, get_farmer
from scoring import score_farmer, score_tier


def _print_farmer(farmer_id: str) -> None:
    farmer = get_farmer(farmer_id)
    result = score_farmer(farmer)

    print(f"\n{'=' * 72}")
    print(f"{farmer_id}  {farmer['name']}  ({farmer['crop']}, {farmer['county']})")
    print("=" * 72)

    if not result["eligible"]:
        print("INELIGIBLE:")
        for failure in result["gate_failures"]:
            print(f"  - [{failure['gate']}] {failure['reason']}")
        return

    print(f"Composite score: {result['composite_score_0_100']}/100  ({score_tier(result['composite_score_0_100'])})")
    print("\nParameter bands (weighted into the score):")
    for name, band in result["parameter_bands"].items():
        print(f"  {name:22s} {band['points']}/5  {band['label']:10s} {band['why']}")

    print("\nStructuring bands (size the loan, never the score):")
    print(f"  {'production_capacity':22s} {result['production_capacity']['points']}/5  {result['production_capacity']['label']}")
    print(f"  {'climate_exposure':22s} {result['climate_exposure']['points']}/5  {result['climate_exposure']['label']}")

    ls = result["loan_structuring"]
    print(f"\nLoan offer: KES {ls['max_loan_amount_kes']:,} over {ls['term_months']} months"
          f"{' (insurance mandatory)' if ls['insurance_mandatory'] else ''}")

    print(f"\nraw_sources_used: {result['raw_sources_used']}")


def main() -> None:
    for farmer_id in all_farmer_ids():
        _print_farmer(farmer_id)


if __name__ == "__main__":
    main()
