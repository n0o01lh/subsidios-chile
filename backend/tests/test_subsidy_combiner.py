from app.services.subsidy_combiner import SubsidyCombiner


def test_combiner_detects_incompatible_pair() -> None:
    combiner = SubsidyCombiner()

    result = combiner.combine(['ds49', 'ds1_tramo_3'])

    assert result.valid is False
    assert result.total_package_uf > 0
    assert any('not compatible' in warning for warning in result.warnings)


def test_combiner_applies_ds1_rule() -> None:
    combiner = SubsidyCombiner()

    result = combiner.combine(['ds1_tramo_2'])

    assert result.valid is True
    assert any('mortgage credit' in rule for rule in result.applied_rules)
