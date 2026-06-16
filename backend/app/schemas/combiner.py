from pydantic import BaseModel


class CombinationRequest(BaseModel):
    selected_subsidies: list[str]


class CombinationResponse(BaseModel):
    valid: bool
    total_package_uf: float
    warnings: list[str]
    applied_rules: list[str]
