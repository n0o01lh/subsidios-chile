from app.schemas.eligibility import EligibilityRequest, EligibilityResponse, EligibilityResult
from app.services.subsidy_catalog import SUBSIDY_RULES


class EligibilityEngine:
    def check_eligibility(self, payload: EligibilityRequest) -> EligibilityResponse:
        ranked_results: list[EligibilityResult] = []

        for rule in SUBSIDY_RULES:
            gaps: list[str] = []
            eligible = True

            if not (rule.frs_min <= payload.frs_score <= rule.frs_max):
                eligible = False
                gaps.append(f'FRS score must be between {rule.frs_min} and {rule.frs_max}.')

            if payload.current_savings_uf is not None and payload.current_savings_uf < rule.required_savings_uf:
                eligible = False
                missing_savings = round(rule.required_savings_uf - payload.current_savings_uf, 2)
                gaps.append(f'Increase savings by {missing_savings} UF.')

            if payload.owns_property and not rule.allows_existing_home:
                eligible = False
                gaps.append('Applicant must not own a property for this program.')

            if payload.region and payload.region not in rule.region_availability:
                eligible = False
                gaps.append('Region is not available for this subsidy call.')

            if rule.rural_only and payload.context != 'rural':
                eligible = False
                gaps.append('This subsidy is only available in rural context.')

            score = rule.benefit_uf - (len(gaps) * 20)
            timeline = 6 + len(gaps) * 2

            ranked_results.append(
                EligibilityResult(
                    subsidy_id=rule.id,
                    subsidy_name=rule.name,
                    eligible=eligible,
                    benefit_uf=rule.benefit_uf,
                    score=score,
                    requirement_gaps=gaps,
                    estimated_timeline_months=timeline,
                )
            )

        ranked_results.sort(key=lambda item: (item.eligible, item.benefit_uf, item.score), reverse=True)
        best_match = next((item.subsidy_id for item in ranked_results if item.eligible), None)
        return EligibilityResponse(best_match_subsidy_id=best_match, ranked_subsidies=ranked_results)
