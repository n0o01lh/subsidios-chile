from datetime import UTC, datetime

from fastapi import APIRouter

from app.services.scraper_runtime import scraper_state

router = APIRouter(prefix='/admin')


@router.post('/refresh')
async def manual_refresh() -> dict[str, str]:
    now = datetime.now(UTC)
    scraper_state['manual_refresh'] = now
    return {'status': 'refresh_triggered', 'timestamp': now.isoformat()}
