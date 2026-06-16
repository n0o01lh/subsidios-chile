from datetime import date

from app.schemas.call import PostulationCallResponse
from app.schemas.project import ProjectResponse, RegionResponse

PROJECTS: list[ProjectResponse] = [
    ProjectResponse(id=1, name='Condominio Valle Azul', region=13, commune='Santiago', subsidy_program='DS1 Tramo 2', available_units=24, min_price_uf=1900, max_price_uf=2400, bedrooms=2, address='Av. Central 1234', source_url='https://www.observatoriohab.minvu.cl/'),
    ProjectResponse(id=2, name='Portal Rural Sur', region=10, commune='Ancud', subsidy_program='DS10', available_units=16, min_price_uf=900, max_price_uf=1500, bedrooms=3, address='Ruta Rural Km 6', source_url='https://www.serviu.cl/'),
]

CALLS: list[PostulationCallResponse] = [
    PostulationCallResponse(id=1, subsidy_program='DS1 Tramo 1', region=13, opening_date=date(2026, 4, 1), closing_date=date(2026, 4, 30), available_quotas=3000, requirements='Up to 13,484 FRS score and minimum savings requirement.', source_url='https://www.serviu.cl/'),
    PostulationCallResponse(id=2, subsidy_program='DS49', region=8, opening_date=date(2026, 3, 15), closing_date=date(2026, 4, 15), available_quotas=1800, requirements='No property ownership and social support certification.', source_url='https://www.serviu.cl/'),
]

REGIONS = [
    RegionResponse(id=1, name='Arica y Parinacota'),
    RegionResponse(id=2, name='Tarapacá'),
    RegionResponse(id=3, name='Antofagasta'),
    RegionResponse(id=4, name='Atacama'),
    RegionResponse(id=5, name='Valparaíso'),
    RegionResponse(id=6, name="O'Higgins"),
    RegionResponse(id=7, name='Maule'),
    RegionResponse(id=8, name='Biobío'),
    RegionResponse(id=9, name='La Araucanía'),
    RegionResponse(id=10, name='Los Lagos'),
    RegionResponse(id=11, name='Aysén'),
    RegionResponse(id=12, name='Magallanes'),
    RegionResponse(id=13, name='Metropolitana'),
    RegionResponse(id=14, name='Los Ríos'),
    RegionResponse(id=15, name='Arica'),
    RegionResponse(id=16, name='Ñuble'),
]


class ProjectsCatalogService:
    def list_projects(
        self,
        region: int | None = None,
        commune: str | None = None,
        subsidy_program: str | None = None,
        min_price_uf: float | None = None,
        max_price_uf: float | None = None,
        bedrooms: int | None = None,
    ) -> list[ProjectResponse]:
        projects = PROJECTS
        if region is not None:
            projects = [item for item in projects if item.region == region]
        if commune:
            projects = [item for item in projects if item.commune.lower() == commune.lower()]
        if subsidy_program:
            projects = [item for item in projects if subsidy_program.lower() in item.subsidy_program.lower()]
        if min_price_uf is not None:
            projects = [item for item in projects if item.max_price_uf >= min_price_uf]
        if max_price_uf is not None:
            projects = [item for item in projects if item.min_price_uf <= max_price_uf]
        if bedrooms is not None:
            projects = [item for item in projects if item.bedrooms >= bedrooms]
        return projects

    def list_regions(self) -> list[RegionResponse]:
        return REGIONS


class CallsCatalogService:
    def list_calls(self, region: int | None = None) -> list[PostulationCallResponse]:
        calls = CALLS
        if region is not None:
            calls = [item for item in calls if item.region == region]
        return calls
