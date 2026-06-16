from app.schemas.combiner import CombinationResponse
from app.services.subsidy_catalog import SUBSIDY_RULES


class SubsidyCombiner:
    def combine(self, selected_subsidies: list[str]) -> CombinationResponse:
        subsidy_map = {item.id: item for item in SUBSIDY_RULES}
        selected = [subsidy_map[item] for item in selected_subsidies if item in subsidy_map]

        warnings: list[str] = []
        rules_applied: list[str] = []
        valid = True

        if 'ds49' in selected_subsidies or 'ds49_collective' in selected_subsidies:
            rules_applied.append('DS49 can be combined with municipal complementary subsidies.')

        if any(item.id.startswith('ds1') for item in selected):
            rules_applied.append('DS1 can be combined with mortgage credit.')

        if 'ds116' in selected_subsidies and not ({'ds1_tramo_2', 'ds1_tramo_3'} & set(selected_subsidies)):
            warnings.append('DS116 is typically combined with DS1 Tramo 2 or 3.')

        incompatible_pairs = {
            frozenset({'ds49', 'ds1_tramo_3'}): 'DS49 and DS1 Tramo 3 are not compatible in the same application.'
        }

        for pair, warning in incompatible_pairs.items():
            if pair.issubset(set(selected_subsidies)):
                valid = False
                warnings.append(warning)

        total = round(sum(item.benefit_uf for item in selected), 2)
        return CombinationResponse(valid=valid, total_package_uf=total, warnings=warnings, applied_rules=rules_applied)
