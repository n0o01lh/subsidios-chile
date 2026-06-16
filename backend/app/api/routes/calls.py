from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.call import PostulationCallResponse
from app.services.project_catalog import CallsCatalogService

router = APIRouter(prefix='/calls')
service = CallsCatalogService()


@router.get('', response_model=list[PostulationCallResponse])
async def list_calls(
    region: int | None = Query(default=None, ge=1, le=16),
    session: AsyncSession = Depends(get_session),
) -> list[PostulationCallResponse]:
    return await service.list_calls(session, region)
