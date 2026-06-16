# Subsidios Chile

Subsidios Chile is a full-stack platform that helps citizens evaluate housing subsidy options in Chile, compare postulation plans, and discover compatible projects.

## Stack

- Frontend: React + Vite + TypeScript + Tailwind CSS
- Backend: FastAPI + SQLAlchemy async ORM + PostgreSQL
- Scraping: httpx + BeautifulSoup4 + Playwright-ready architecture
- Scheduling: APScheduler

## Setup (English)

1. Copy environment variables:
   ```bash
   cp .env.example .env
   ```
2. Start all services:
   ```bash
   docker compose up --build
   ```
3. Open:
   - Frontend: http://localhost:5173
   - Backend docs: http://localhost:8000/docs

## Configuración (Español)

1. Copia las variables de entorno:
   ```bash
   cp .env.example .env
   ```
2. Levanta los servicios:
   ```bash
   docker compose up --build
   ```
3. Accesos:
   - Frontend: http://localhost:5173
   - API docs: http://localhost:8000/docs

## API endpoints

- `GET /api/v1/subsidies`
- `GET /api/v1/subsidies/{id}`
- `POST /api/v1/eligibility/check`
- `POST /api/v1/eligibility/combine`
- `POST /api/v1/plans/generate`
- `GET /api/v1/projects`
- `GET /api/v1/projects/regions`
- `GET /api/v1/calls`
- `GET /api/v1/health`
- `POST /api/v1/admin/refresh`

## Notes

- UI text is in Spanish for end users.
- Code, comments, docs, and variable names are in English.
- The disclaimer appears in all pages: _"Esta herramienta es orientativa. Siempre consulte con su SERVIU regional."_
- Scraped projects/calls are persisted in PostgreSQL and refreshed by scheduler/admin endpoint, so the API serves cached data between refresh runs.

## Next iteration

- Deploy the frontend static build to GitHub Pages and point it to the production API URL.
