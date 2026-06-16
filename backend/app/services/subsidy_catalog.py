from dataclasses import dataclass


@dataclass(frozen=True)
class SubsidyRule:
    id: str
    name: str
    decree: str
    target: str
    frs_min: float
    frs_max: float
    benefit_uf: float
    required_savings_uf: float
    max_property_value_uf: float
    mortgage_allowed: bool
    mortgage_required: bool
    modality: str
    region_availability: tuple[int, ...]
    postulation_periods: tuple[str, ...]
    compatible_savings_instruments: tuple[str, ...]
    compatible_with: tuple[str, ...]
    allows_existing_home: bool
    rural_only: bool = False


SUBSIDY_RULES: tuple[SubsidyRule, ...] = (
    SubsidyRule('ds49', 'Subsidio Habitacional DS49', 'DS49', 'Vulnerable households', 0, 11734, 950, 10, 1100, False, False, 'individual', tuple(range(1, 17)), ('March', 'September'), ('MINVU Savings Book',), ('municipal_complement',), False),
    SubsidyRule('ds49_collective', 'Subsidio Habitacional DS49 Colectivo', 'DS49', 'Collective vulnerable households', 0, 11734, 1000, 8, 1100, False, False, 'collective', tuple(range(1, 17)), ('March', 'September'), ('MINVU Savings Book',), ('municipal_complement',), False),
    SubsidyRule('ds1_tramo_1', 'Subsidio DS1 Tramo 1', 'DS1', 'Emerging middle class', 0, 13484, 500, 30, 2200, True, False, 'individual', tuple(range(1, 17)), ('April', 'November'), ('MINVU Savings Book', 'Term deposit'), ('mortgage_credit',), False),
    SubsidyRule('ds1_tramo_2', 'Subsidio DS1 Tramo 2', 'DS1', 'Emerging middle class', 0, 14557, 400, 40, 2600, True, True, 'individual', tuple(range(1, 17)), ('April', 'November'), ('MINVU Savings Book', 'Term deposit'), ('mortgage_credit', 'ds116'), False),
    SubsidyRule('ds1_tramo_3', 'Subsidio DS1 Tramo 3', 'DS1', 'Emerging middle class', 0, 16352, 300, 80, 3000, True, True, 'individual', tuple(range(1, 17)), ('April', 'November'), ('MINVU Savings Book', 'Term deposit'), ('mortgage_credit', 'ds116'), False),
    SubsidyRule('ds19', 'Subsidio DS19 (PPPF)', 'DS19', 'Rental and leasing', 0, 25000, 220, 4, 0, False, False, 'entity', tuple(range(1, 17)), ('Open all year',), ('MINVU Savings Book',), ('none',), False),
    SubsidyRule('ds116', 'Subsidio de Integración Social DS116', 'DS116', 'Mixed income projects', 0, 18000, 350, 20, 2600, True, True, 'entity', tuple(range(1, 17)), ('May', 'October'), ('MINVU Savings Book',), ('ds1_tramo_2', 'ds1_tramo_3'), False),
    SubsidyRule('ds10', 'Subsidio Rural DS10', 'DS10', 'Rural housing', 0, 20000, 700, 10, 1800, False, False, 'individual', tuple(range(1, 17)), ('June',), ('MINVU Savings Book',), ('municipal_complement',), False, True),
    SubsidyRule('ds27', 'Subsidio Mejoramiento DS27', 'DS27', 'Home improvement', 0, 18000, 250, 3, 0, False, False, 'entity', tuple(range(1, 17)), ('Open all year',), ('MINVU Savings Book',), ('none',), True),
)
