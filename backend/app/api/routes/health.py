from datetime import UTC, datetime

from fastapi import APIRouter

from app.schemas.health import HealthResponse
from app.services.scraper_runtime import scraper_state

router = APIRouter(prefix='')


@router.get('/health', response_model=HealthResponse)
async def health_check() -> HealthResponse:
    now = datetime.now(UTC)
    status = {
        scraper: f'{int((now - updated).total_seconds() / 3600)} hours ago'
        for scraper, updated in scraper_state.items()
    }
    return HealthResponse(status='ok', scraper_status=status)
