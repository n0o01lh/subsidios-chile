from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, calls, eligibility, health, plans, projects, subsidies
from app.core.config import settings
from app.core.database import AsyncSessionLocal, Base, engine
from app.models import call, project, scraper_run, subsidy  # noqa: F401
from app.services.project_catalog import CatalogRefreshService

scheduler = AsyncIOScheduler(timezone='UTC')
refresh_service = CatalogRefreshService()


async def run_scheduled_refresh() -> None:
    async with AsyncSessionLocal() as session:
        await refresh_service.refresh(session, force=True)


async def _initial_refresh() -> None:
    async with AsyncSessionLocal() as session:
        await refresh_service.refresh(session, force=False, max_age_hours=24)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    # Run initial catalog refresh in the background so startup is not blocked
    asyncio.create_task(_initial_refresh())

    scheduler.add_job(
        run_scheduled_refresh,
        'interval',
        hours=12,
        id='catalog_refresh',
        replace_existing=True,
    )
    scheduler.start()

    yield

    scheduler.shutdown(wait=False)


app = FastAPI(title='Subsidios Chile API', version='0.1.0', lifespan=lifespan)

origins = [origin.strip() for origin in settings.backend_cors_origins if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health.router, prefix='/api/v1', tags=['health'])
app.include_router(subsidies.router, prefix='/api/v1', tags=['subsidies'])
app.include_router(eligibility.router, prefix='/api/v1', tags=['eligibility'])
app.include_router(plans.router, prefix='/api/v1', tags=['plans'])
app.include_router(projects.router, prefix='/api/v1', tags=['projects'])
app.include_router(calls.router, prefix='/api/v1', tags=['calls'])
app.include_router(admin.router, prefix='/api/v1', tags=['admin'])
