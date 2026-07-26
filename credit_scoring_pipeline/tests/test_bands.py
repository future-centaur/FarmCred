import config
from scoring import bands


def test_missing_source_resolves_to_neutral_not_floor():
    assert bands.cash_flow_stability(None) == config.NEUTRAL_BAND
    assert bands.cash_flow_stability({}) == config.NEUTRAL_BAND
    assert bands.repayment_history(None, None) == config.NEUTRAL_BAND
    assert bands.market_linkage(None) == config.NEUTRAL_BAND
    assert bands.social_collateral(None) == config.NEUTRAL_BAND
    assert bands.production_capacity(None) == config.NEUTRAL_BAND
    assert bands.climate_exposure(None, None) == config.NEUTRAL_BAND


def test_band_points_always_in_range():
    result = bands.cash_flow_stability({"monthly_inflows_kes": [1_000_000] * 12})
    assert config.BAND_MIN_POINTS <= result["points"] <= config.BAND_MAX_POINTS

    result = bands.cash_flow_stability({"monthly_inflows_kes": [1] * 12})
    assert config.BAND_MIN_POINTS <= result["points"] <= config.BAND_MAX_POINTS


def test_sunculture_ownership_mitigates_climate_exposure_by_one_band():
    climate = {"regional_exposure": "high", "rainfall_deficit_pct": 28}
    unmitigated = bands.climate_exposure(climate, {"sunculture_owner": False})
    mitigated = bands.climate_exposure(climate, {"sunculture_owner": True})
    assert mitigated["points"] == unmitigated["points"] + 1


def test_thin_bureau_file_falls_back_to_cooperative_proxy():
    no_file = {"has_crb_file": False}
    strong_proxy = bands.repayment_history(no_file, {"input_loan_deductions_last_12mo": 4})
    assert strong_proxy["points"] > config.NEUTRAL_BAND["points"]

    weak_proxy = bands.repayment_history(no_file, {"input_loan_deductions_last_12mo": 0})
    assert weak_proxy == config.NEUTRAL_BAND
