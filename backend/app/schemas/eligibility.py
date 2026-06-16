from pydantic import BaseModel, Field


class EligibilityRequest(BaseModel):
    frs_score: float = Field(ge=0, le=100000)
    monthly_household_income: float | None = Field(default=None, ge=0)
    family_members: int | None = Field(default=None, ge=1)
    current_savings_uf: float | None = Field(default=0, ge=0)
    region: int | None = Field(default=None, ge=1, le=16)
    owns_property: bool = False
    age: int | None = Field(default=None, ge=18)
    context: str = Field(default='urban', pattern='^(urban|rural)$')


class EligibilityResult(BaseModel):
    subsidy_id: str
    subsidy_name: str
    eligible: bool
    benefit_uf: float
    score: float
    requirement_gaps: list[str]
    estimated_timeline_months: int


class EligibilityResponse(BaseModel):
    best_match_subsidy_id: str | None
    ranked_subsidies: list[EligibilityResult]
