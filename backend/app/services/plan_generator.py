from app.schemas.eligibility import EligibilityRequest
from app.schemas.plan import GeneratedPlan, PlanGenerationRequest, PlanGenerationResponse
from app.services.eligibility_engine import EligibilityEngine


class PlanGenerator:
    def __init__(self) -> None:
        self.engine = EligibilityEngine()

    def generate(self, payload: PlanGenerationRequest) -> PlanGenerationResponse:
        plans: list[GeneratedPlan] = []
        scenarios = [
            ('Plan A', payload.baseline, 'Current baseline situation.'),
            *[(scenario.name, self._apply_scenario(payload.baseline, scenario.savings_delta_uf, scenario.income_override), 'Scenario with adjusted conditions.') for scenario in payload.scenarios],
        ]

        for name, input_snapshot, description in scenarios:
            result = self.engine.check_eligibility(input_snapshot)
            eligible = [item for item in result.ranked_subsidies if item.eligible]
            total_benefit = sum(item.benefit_uf for item in eligible)
            average_wait = int(sum(item.estimated_timeline_months for item in eligible) / len(eligible)) if eligible else 18
            steps = [
                description,
                'Update supporting documentation in your municipality.',
                'Verify active postulation calls in SERVIU.',
            ]
            plans.append(
                GeneratedPlan(
                    name=name,
                    input_snapshot=input_snapshot,
                    result=result,
                    total_benefit_uf=round(total_benefit, 2),
                    estimated_waiting_time_months=average_wait,
                    steps=steps,
                )
            )

        return PlanGenerationResponse(plans=plans)

    @staticmethod
    def _apply_scenario(base: EligibilityRequest, savings_delta_uf: float, income_override: float | None) -> EligibilityRequest:
        new_savings = (base.current_savings_uf or 0) + savings_delta_uf
        return EligibilityRequest(
            frs_score=base.frs_score,
            monthly_household_income=income_override if income_override is not None else base.monthly_household_income,
            family_members=base.family_members,
            current_savings_uf=new_savings,
            region=base.region,
            owns_property=base.owns_property,
            age=base.age,
            context=base.context,
        )
