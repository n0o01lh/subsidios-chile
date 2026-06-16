from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, calls, eligibility, health, plans, projects, subsidies
from app.core.config import settings
from app.services.project_catalog import CallsCatalogService, ProjectsCatalogService
from app.services.scraper_runtime import mark_scraper_run

scheduler = AsyncIOScheduler(timezone='UTC')


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    scheduler.add_job(
        lambda: mark_scraper_run('observatorio_scraper'),
        'interval',
        hours=24,
        id='observatorio_scraper',
        replace_existing=True,
    )
    scheduler.add_job(
        lambda: mark_scraper_run('serviu_scraper'),
        'interval',
        hours=12,
        id='serviu_scraper',
        replace_existing=True,
    )
    scheduler.add_job(
        lambda: mark_scraper_run('minvu_scraper'),
        'interval',
        hours=6,
        id='minvu_scraper',
        replace_existing=True,
    )
    scheduler.start()

    if not ProjectsCatalogService().list_projects() and not CallsCatalogService().list_calls():
        mark_scraper_run('startup_seed')

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
