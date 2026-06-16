from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.services.project_catalog import CatalogRefreshService

router = APIRouter(prefix='/admin')
refresh_service = CatalogRefreshService()


@router.post('/refresh')
async def manual_refresh(
    session: AsyncSession = Depends(get_session),
) -> dict[str, str | int | bool]:
    return await refresh_service.refresh(session, force=True)
