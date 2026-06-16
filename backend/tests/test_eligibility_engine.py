from app.schemas.eligibility import EligibilityRequest
from app.services.eligibility_engine import EligibilityEngine


def test_eligibility_returns_best_match_for_vulnerable_profile() -> None:
    engine = EligibilityEngine()
    payload = EligibilityRequest(
        frs_score=8000,
        monthly_household_income=500000,
        family_members=3,
        current_savings_uf=15,
        region=13,
        owns_property=False,
        age=28,
        context='urban',
    )

    result = engine.check_eligibility(payload)

    assert result.best_match_subsidy_id in {'ds49_collective', 'ds49'}
    assert any(item.eligible for item in result.ranked_subsidies)


def test_eligibility_flags_missing_savings_gap() -> None:
    engine = EligibilityEngine()
    payload = EligibilityRequest(frs_score=12000, current_savings_uf=2, context='urban')

    result = engine.check_eligibility(payload)

    tramo_1 = next(item for item in result.ranked_subsidies if item.subsidy_id == 'ds1_tramo_1')
    assert not tramo_1.eligible
    assert any('Increase savings' in gap for gap in tramo_1.requirement_gaps)


def test_eligibility_accepts_boundary_frs_value() -> None:
    engine = EligibilityEngine()
    payload = EligibilityRequest(frs_score=11734, current_savings_uf=10, context='urban')

    result = engine.check_eligibility(payload)

    ds49 = next(item for item in result.ranked_subsidies if item.subsidy_id == 'ds49')
    assert ds49.eligible


def test_eligibility_requires_income_for_mortgage_programs() -> None:
    engine = EligibilityEngine()
    payload = EligibilityRequest(frs_score=14000, current_savings_uf=80, context='urban')

    result = engine.check_eligibility(payload)

    tramo_2 = next(item for item in result.ranked_subsidies if item.subsidy_id == 'ds1_tramo_2')
    assert not tramo_2.eligible
    assert any('monthly household income information' in gap for gap in tramo_2.requirement_gaps)
