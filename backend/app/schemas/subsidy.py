from pydantic import BaseModel


class SubsidyResponse(BaseModel):
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
    region_availability: list[int]
    postulation_periods: list[str]
    compatible_savings_instruments: list[str]
    compatible_with: list[str]
