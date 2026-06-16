from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    scraper_status: dict[str, str]
