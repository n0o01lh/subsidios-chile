from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime, timedelta
from typing import Any

from sqlalchemy import delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.call import PostulationCall
from app.models.project import Project
from app.models.scraper_run import ScraperRun
from app.schemas.call import PostulationCallResponse
from app.schemas.project import ProjectResponse, RegionResponse
from app.scrapers.inmobiliaria_scraper import InmobiliariaScraper, load_inmobiliarias
from app.scrapers.minvu_scraper import MinvuScraper
from app.scrapers.observatorio_scraper import ObservatorioScraper
from app.scrapers.serviu_scraper import ServiuScraper

FALLBACK_PROJECTS: list[dict[str, Any]] = [
    {
        'name': 'Condominio Valle Azul',
        'region': 13,
        'commune': 'Santiago',
        'subsidy_program': 'DS1 Tramo 2',
        'available_units': 24,
        'min_price_uf': 1900,
        'max_price_uf': 2400,
        'bedrooms': 2,
        'address': 'Av. Central 1234',
        'source_url': 'https://www.observatoriohab.minvu.cl/',
    },
    {
        'name': 'Portal Rural Sur',
        'region': 10,
        'commune': 'Ancud',
        'subsidy_program': 'DS10',
        'available_units': 16,
        'min_price_uf': 900,
        'max_price_uf': 1500,
        'bedrooms': 3,
        'address': 'Ruta Rural Km 6',
        'source_url': 'https://www.serviu.cl/',
    },
]

FALLBACK_CALLS: list[dict[str, Any]] = [
    {
        'subsidy_program': 'DS1 Tramo 1',
        'region': 13,
        'opening_date': date(2026, 4, 1),
        'closing_date': date(2026, 4, 30),
        'available_quotas': 3000,
        'requirements': 'Up to 13,484 FRS score and minimum savings requirement.',
        'source_url': 'https://www.serviu.cl/',
    },
    {
        'subsidy_program': 'DS49',
        'region': 8,
        'opening_date': date(2026, 3, 15),
        'closing_date': date(2026, 4, 15),
        'available_quotas': 1800,
        'requirements': 'No property ownership and social support certification.',
        'source_url': 'https://www.serviu.cl/',
    },
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


def _safe_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


class CatalogRefreshService:
    def __init__(self) -> None:
        self._observatorio = ObservatorioScraper()
        self._serviu = ServiuScraper()
        self._minvu = MinvuScraper()

    async def refresh(
        self,
        session: AsyncSession,
        *,
        force: bool = False,
        max_age_hours: int = 24,
    ) -> dict[str, Any]:
        if not force and not await self._is_cache_stale(session, max_age_hours=max_age_hours):
            return {'status': 'cache_reused', 'refreshed': False}

        now = datetime.now(UTC)
        scraped_projects, scraped_calls = await self._run_scrapers(session, now)

        projects = self._build_projects(scraped_projects)
        calls = self._build_calls(scraped_calls)

        await session.execute(delete(Project))
        session.add_all([Project(**item, scraped_at=now) for item in projects])

        await session.execute(delete(PostulationCall))
        session.add_all([PostulationCall(**item, scraped_at=now) for item in calls])
        await session.commit()

        await self._record_run(
            session,
            scraper_name='catalog_refresh',
            records_collected=len(projects) + len(calls),
            started_at=now,
            finished_at=datetime.now(UTC),
        )

        return {
            'status': 'refresh_completed',
            'refreshed': True,
            'projects': len(projects),
            'calls': len(calls),
        }

    async def _run_scrapers(
        self, session: AsyncSession, started_at: datetime
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        async def _fetch(coro: Any) -> tuple[list[dict[str, Any]], Exception | None]:
            try:
                return await coro, None
            except Exception as exc:  # pragma: no cover - network-dependent
                return [], exc

        # Run all HTTP scraping concurrently (no DB access here)
        (obs_data, obs_err), (serviu_data, serviu_err), (minvu_data, minvu_err) = (
            await asyncio.gather(
                _fetch(self._observatorio.scrape()),
                _fetch(self._serviu.scrape()),
                _fetch(self._minvu.scrape()),
            )
        )

        # Record results sequentially to avoid concurrent session access
        for scraper_name, data, err in [
            ('observatorio_scraper', obs_data, obs_err),
            ('serviu_scraper', serviu_data, serviu_err),
            ('minvu_scraper', minvu_data, minvu_err),
        ]:
            if err is not None:  # pragma: no cover - network-dependent
                await self._record_run(
                    session,
                    scraper_name=scraper_name,
                    status='failed',
                    message=str(err)[:500],
                    records_collected=0,
                    started_at=started_at,
                    finished_at=datetime.now(UTC),
                )
            else:
                await self._record_run(
                    session,
                    scraper_name=scraper_name,
                    records_collected=len(data),
                    started_at=started_at,
                    finished_at=datetime.now(UTC),
                )

        return obs_data, serviu_data

    def _build_projects(self, scraped_projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
        projects = [*FALLBACK_PROJECTS]
        seen_names = {item['name'].lower() for item in projects}

        for item in scraped_projects:
            name = (item.get('name') or '').strip() or 'Observatorio Project'
            key = name.lower()
            if key in seen_names:
                continue

            seen_names.add(key)
            projects.append(
                {
                    'name': name[:255],
                    'region': _safe_int(item.get('region'), 13),
                    'commune': (item.get('commune') or 'Sin información')[:120],
                    'subsidy_program': (item.get('program_type') or 'General')[:80],
                    'available_units': _safe_int(item.get('available_units'), 0),
                    'min_price_uf': _safe_float(item.get('min_price_uf'), 0),
                    'max_price_uf': _safe_float(item.get('max_price_uf'), 0),
                    'bedrooms': max(_safe_int(item.get('bedrooms'), 2), 1),
                    'address': (item.get('address') or 'Sin información')[:255],
                    'source_url': 'https://www.observatoriohab.minvu.cl/',
                }
            )
        return projects

    def _build_calls(self, scraped_calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
        calls = [*FALLBACK_CALLS]
        today = date.today()
        closing = today + timedelta(days=45)
        seen_programs = {(item['subsidy_program'].lower(), item['region']) for item in calls}

        for item in scraped_calls:
            subsidy_program = (item.get('subsidy_program') or '').strip() or 'SERVIU Call'
            region = _safe_int(item.get('region'), 13)
            key = (subsidy_program.lower(), region)
            if key in seen_programs:
                continue

            seen_programs.add(key)
            calls.append(
                {
                    'subsidy_program': subsidy_program[:120],
                    'region': min(max(region, 1), 16),
                    'opening_date': today,
                    'closing_date': closing,
                    'available_quotas': max(_safe_int(item.get('available_quotas'), 0), 0),
                    'requirements': (
                        item.get('requirements') or 'Consultar sitio oficial SERVIU'
                    )[:500],
                    'source_url': 'https://www.serviu.cl/',
                }
            )
        return calls

    async def _record_run(
        self,
        session: AsyncSession,
        *,
        scraper_name: str,
        records_collected: int,
        started_at: datetime,
        finished_at: datetime,
        status: str = 'success',
        message: str = '',
    ) -> None:
        session.add(
            ScraperRun(
                scraper_name=scraper_name,
                status=status,
                message=message,
                records_collected=records_collected,
                started_at=started_at,
                finished_at=finished_at,
            )
        )
        await session.flush()

    async def _is_cache_stale(self, session: AsyncSession, *, max_age_hours: int) -> bool:
        project_count = await session.scalar(select(func.count()).select_from(Project))
        call_count = await session.scalar(select(func.count()).select_from(PostulationCall))
        if not project_count and not call_count:
            return True

        latest_run = await session.scalar(
            select(ScraperRun)
            .where(ScraperRun.scraper_name == 'catalog_refresh', ScraperRun.status == 'success')
            .order_by(desc(ScraperRun.finished_at))
            .limit(1)
        )
        if latest_run is None:
            return True

        max_age = timedelta(hours=max_age_hours)
        return datetime.now(UTC) - latest_run.finished_at.replace(tzinfo=UTC) >= max_age


class ProjectsCatalogService:
    async def list_projects(
        self,
        session: AsyncSession,
        region: int | None = None,
        commune: str | None = None,
        subsidy_program: str | None = None,
        min_price_uf: float | None = None,
        max_price_uf: float | None = None,
        bedrooms: int | None = None,
    ) -> list[ProjectResponse]:
        query = select(Project)
        if region is not None:
            query = query.where(Project.region == region)
        if commune:
            query = query.where(func.lower(Project.commune) == commune.lower())
        if subsidy_program:
            query = query.where(Project.subsidy_program.ilike(f'%{subsidy_program}%'))
        if min_price_uf is not None:
            query = query.where(Project.max_price_uf >= min_price_uf)
        if max_price_uf is not None:
            query = query.where(Project.min_price_uf <= max_price_uf)
        if bedrooms is not None:
            query = query.where(Project.bedrooms >= bedrooms)

        rows = (await session.execute(query.order_by(Project.id.asc()))).scalars().all()
        return [
            ProjectResponse(
                id=item.id,
                name=item.name,
                region=item.region,
                commune=item.commune,
                subsidy_program=item.subsidy_program,
                available_units=item.available_units,
                min_price_uf=item.min_price_uf,
                max_price_uf=item.max_price_uf,
                bedrooms=item.bedrooms,
                address=item.address,
                source_url=item.source_url,
            )
            for item in rows
        ]

    def list_regions(self) -> list[RegionResponse]:
        return REGIONS


class CallsCatalogService:
    async def list_calls(
        self, session: AsyncSession, region: int | None = None
    ) -> list[PostulationCallResponse]:
        query = select(PostulationCall)
        if region is not None:
            query = query.where(PostulationCall.region == region)
        rows = (await session.execute(query.order_by(PostulationCall.id.asc()))).scalars().all()
        return [
            PostulationCallResponse(
                id=item.id,
                subsidy_program=item.subsidy_program,
                region=item.region,
                opening_date=item.opening_date,
                closing_date=item.closing_date,
                available_quotas=item.available_quotas,
                requirements=item.requirements,
                source_url=item.source_url,
            )
            for item in rows
        ]
