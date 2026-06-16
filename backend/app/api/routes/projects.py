from fastapi import APIRouter, Query

from app.schemas.project import ProjectResponse, RegionResponse
from app.services.project_catalog import ProjectsCatalogService

router = APIRouter(prefix='/projects')
service = ProjectsCatalogService()


@router.get('', response_model=list[ProjectResponse])
async def list_projects(
    region: int | None = Query(default=None, ge=1, le=16),
    commune: str | None = None,
    subsidy_program: str | None = None,
    min_price_uf: float | None = Query(default=None, ge=0),
    max_price_uf: float | None = Query(default=None, ge=0),
    bedrooms: int | None = Query(default=None, ge=1),
) -> list[ProjectResponse]:
    return service.list_projects(region, commune, subsidy_program, min_price_uf, max_price_uf, bedrooms)


@router.get('/regions', response_model=list[RegionResponse])
async def list_regions() -> list[RegionResponse]:
    return service.list_regions()
