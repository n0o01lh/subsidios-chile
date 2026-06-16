from fastapi import APIRouter, Query

from app.schemas.call import PostulationCallResponse
from app.services.project_catalog import CallsCatalogService

router = APIRouter(prefix='/calls')
service = CallsCatalogService()


@router.get('', response_model=list[PostulationCallResponse])
async def list_calls(region: int | None = Query(default=None, ge=1, le=16)) -> list[PostulationCallResponse]:
    return service.list_calls(region)
