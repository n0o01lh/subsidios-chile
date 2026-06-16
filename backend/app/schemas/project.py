from pydantic import BaseModel


class ProjectResponse(BaseModel):
    id: int
    name: str
    region: int
    commune: str
    subsidy_program: str
    available_units: int
    min_price_uf: float
    max_price_uf: float
    bedrooms: int
    address: str
    source_url: str


class RegionResponse(BaseModel):
    id: int
    name: str
