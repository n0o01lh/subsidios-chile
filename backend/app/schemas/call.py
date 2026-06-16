from datetime import date

from pydantic import BaseModel


class PostulationCallResponse(BaseModel):
    id: int
    subsidy_program: str
    region: int
    opening_date: date
    closing_date: date
    available_quotas: int
    requirements: str
    source_url: str
