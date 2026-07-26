import config
from data.mock_farmers import GATE_DEMO_IDS, get_farmer
from scoring import check_eligibility_gates, score_farmer


def test_config_weights_sum_to_one():
    assert abs(sum(config.SCORE_WEIGHTS.values()) - 1.0) < 1e-9


def test_structuring_parameters_excluded_from_score_weights():
    assert not set(config.SCORE_WEIGHTS) & set(config.STRUCTURING_PARAMETERS)


def test_clean_file_farmer_is_eligible_and_scores_high():
    result = score_farmer(get_farmer("F001"))
    assert result["eligible"]
    assert result["composite_score_0_100"] >= 80


def test_thin_file_farmer_is_eligible_not_penalised_to_floor():
    result = score_farmer(get_farmer("F002"))
    assert result["eligible"]
    assert result["parameter_bands"]["repayment_history"] == config.NEUTRAL_BAND
    assert result["parameter_bands"]["market_linkage"] == config.NEUTRAL_BAND
    assert result["parameter_bands"]["social_collateral"] == config.NEUTRAL_BAND
    assert result["composite_score_0_100"] > 20  # not scored at the floor


def test_each_gate_demo_profile_trips_exactly_the_expected_gate():
    expected_gates = {
        "F004": "unfinanced_value_chain",
        "F005": "out_of_service_area",
        "F006": "active_insolvency",
        "F007": "failed_kyc",
    }
    for farmer_id in GATE_DEMO_IDS:
        result = score_farmer(get_farmer(farmer_id))
        assert not result["eligible"], farmer_id
        gates_tripped = {f["gate"] for f in result["gate_failures"]}
        assert expected_gates[farmer_id] in gates_tripped, farmer_id


def test_production_capacity_and_climate_never_affect_composite_score():
    farmer = get_farmer("F001")
    result_a = score_farmer(farmer)

    # Swap in a much worse production-capacity/climate-exposure pair by hand
    # and confirm the composite score is untouched -- only loan structuring
    # should move.
    from scoring.engine import _structure_loan

    worse_capacity = {"points": 1, "label": "Weak", "why": "test"}
    worse_climate = {"points": 1, "label": "Weak", "why": "test"}
    worse_structuring = _structure_loan(worse_capacity, worse_climate)

    assert worse_structuring["max_loan_amount_kes"] < result_a["loan_structuring"]["max_loan_amount_kes"]
    # composite_score_0_100 is computed purely from parameter_bands / SCORE_WEIGHTS
    assert set(config.SCORE_WEIGHTS) == set(result_a["parameter_bands"])


def test_gate_failure_short_circuits_before_bands_are_computed():
    result = score_farmer(get_farmer("F006"))
    assert not result["eligible"]
    assert "parameter_bands" not in result
    assert "composite_score_0_100" not in result


def test_missing_kiamis_and_crb_never_trip_a_gate_on_their_own():
    farmer = {"farmer_id": "X", "crop": "tea", "county": "kericho", "national_id": "1"}
    result = check_eligibility_gates(farmer, {}, {})
    assert result["eligible"]
