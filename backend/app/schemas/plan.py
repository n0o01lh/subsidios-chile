from pydantic import BaseModel

from app.schemas.eligibility import EligibilityRequest, EligibilityResponse


class PlanScenario(BaseModel):
    name: str
    savings_delta_uf: float = 0
    income_override: float | None = None


class PlanGenerationRequest(BaseModel):
    baseline: EligibilityRequest
    scenarios: list[PlanScenario]


class GeneratedPlan(BaseModel):
    name: str
    input_snapshot: EligibilityRequest
    result: EligibilityResponse
    total_benefit_uf: float
    estimated_waiting_time_months: int
    steps: list[str]


class PlanGenerationResponse(BaseModel):
    plans: list[GeneratedPlan]
