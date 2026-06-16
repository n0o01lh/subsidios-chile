from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from app.scrapers.base_scraper import BaseScraper

# Maximum property value (UF) for the most generous subsidy (DS1 Tramo 3).
# Projects priced at or below this threshold can potentially qualify for a subsidy.
_MAX_SUBSIDY_VALUE_UF = 3000.0

_SUBSIDY_KEYWORDS = re.compile(
    r'\b(DS\s*49|DS\s*1|DS\s*10|DS\s*19|DS\s*116|DS\s*27|subsidio|SERVIU|MINVU|postulaci[oó]n)\b',
    re.IGNORECASE,
)

_UF_PATTERN = re.compile(r'(\d[\d\.,]*)\s*UF', re.IGNORECASE)

_DORMITORIOS_PATTERN = re.compile(r'(\d)\s*(?:dormitorio|dorm\.?|d(?:ormi)?\.?\s*(?:piezas?)?)', re.IGNORECASE)

_DATA_FILE = Path(__file__).resolve().parent.parent / 'data' / 'inmobiliarias.json'


def load_inmobiliarias() -> list[dict[str, Any]]:
    """Return the list of inmobiliarias from the JSON catalogue."""
    with _DATA_FILE.open(encoding='utf-8') as fh:
        return json.load(fh)


def _parse_uf(text: str) -> float | None:
    """Extract the first UF value found in *text*, or return None."""
    match = _UF_PATTERN.search(text)
    if not match:
        return None
    raw = match.group(1).replace('.', '').replace(',', '.')
    try:
        return float(raw)
    except ValueError:
        return None


def _fits_any_subsidy(min_uf: float, max_uf: float) -> bool:
    """Return True when the project price range overlaps with at least one subsidy."""
    return min_uf <= _MAX_SUBSIDY_VALUE_UF


class InmobiliariaScraper(BaseScraper):
    """Generic scraper for a single inmobiliaria website."""

    def __init__(self, name: str, base_url: str) -> None:
        super().__init__(base_url.rstrip('/'))
        self.inmobiliaria_name = name

    async def scrape(self) -> list[dict[str, Any]]:
        try:
            html = await self.fetch('/')
        except Exception:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        return self._extract_projects(soup)

    def _extract_projects(self, soup: BeautifulSoup) -> list[dict[str, Any]]:
        projects: list[dict[str, Any]] = []
        seen: set[str] = set()

        # Candidate containers: cards, articles, sections, list items
        candidates = soup.select(
            'article, .card, .project, .proyecto, .propiedad, '
            '.listing, li[class*="project"], li[class*="proyecto"], '
            'section[class*="project"], section[class*="proyecto"], '
            'div[class*="project"], div[class*="proyecto"]'
        )

        for card in candidates[:50]:
            text = card.get_text(separator=' ', strip=True)

            # Only keep cards that mention a subsidy keyword or have a UF price
            has_subsidy_kw = bool(_SUBSIDY_KEYWORDS.search(text))
            uf_values = _UF_PATTERN.findall(text)
            if not has_subsidy_kw and not uf_values:
                continue

            name = self._extract_name(card) or f'{self.inmobiliaria_name} Project'
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)

            min_uf, max_uf = self._extract_price_range(text, uf_values)
            if not _fits_any_subsidy(min_uf, max_uf):
                continue

            projects.append({
                'name': name[:255],
                'region': self._extract_region(text),
                'commune': self._extract_commune(text),
                'program_type': self._extract_program(text),
                'available_units': self._extract_units(text),
                'min_price_uf': min_uf,
                'max_price_uf': max_uf,
                'bedrooms': self._extract_bedrooms(text),
                'address': self._extract_address(card, text),
                'source_url': self.base_url,
                'inmobiliaria': self.inmobiliaria_name,
            })

        return projects

    # ------------------------------------------------------------------
    # Field helpers
    # ------------------------------------------------------------------

    def _extract_name(self, card: Any) -> str:
        for selector in ('h1', 'h2', 'h3', 'h4', '.name', '.title', '.nombre'):
            tag = card.select_one(selector)
            if tag:
                text = tag.get_text(strip=True)
                if text:
                    return text[:255]
        return ''

    def _extract_price_range(self, text: str, uf_values: list[str]) -> tuple[float, float]:
        prices: list[float] = []
        for raw in uf_values:
            try:
                prices.append(float(raw.replace('.', '').replace(',', '.')))
            except ValueError:
                pass
        if not prices:
            return 0.0, 0.0
        return min(prices), max(prices)

    def _extract_region(self, text: str) -> int:
        region_map = {
            'arica': 15, 'tarapacá': 1, 'antofagasta': 2, 'atacama': 3,
            'coquimbo': 4, 'valparaíso': 5, "o'higgins": 6, 'libertador': 6,
            'maule': 7, 'biobío': 8, 'bío-bío': 8, 'araucanía': 9,
            'los lagos': 10, 'aysén': 11, 'magallanes': 12,
            'metropolitana': 13, 'santiago': 13, 'los ríos': 14, 'ñuble': 16,
        }
        lower = text.lower()
        for keyword, region_id in region_map.items():
            if keyword in lower:
                return region_id
        return 13  # default to Metropolitana

    def _extract_commune(self, text: str) -> str:
        # Look for "Comunas: X" or "en X" patterns; fall back to empty
        match = re.search(r'(?:comuna|en)\s*[:\s]\s*([A-Za-záéíóúÁÉÍÓÚñÑ\s]{3,40}?)(?:[,\.\d]|$)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()[:120]
        return 'Sin información'

    def _extract_program(self, text: str) -> str:
        for program in ('DS116', 'DS49', 'DS1', 'DS10', 'DS19', 'DS27'):
            if re.search(rf'\b{program}\b', text, re.IGNORECASE):
                return program
        if re.search(r'\bsubsidio\b', text, re.IGNORECASE):
            return 'Subsidio'
        return 'General'

    def _extract_units(self, text: str) -> int:
        match = re.search(r'(\d+)\s*(?:unidades?|departamentos?|casas?)\s*disponibles?', text, re.IGNORECASE)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                pass
        return 0

    def _extract_bedrooms(self, text: str) -> int:
        match = _DORMITORIOS_PATTERN.search(text)
        if match:
            try:
                return max(int(match.group(1)), 1)
            except ValueError:
                pass
        return 2

    def _extract_address(self, card: Any, text: str) -> str:
        for selector in ('.address', '.direccion', '.location', '.ubicacion'):
            tag = card.select_one(selector)
            if tag:
                addr = tag.get_text(strip=True)
                if addr:
                    return addr[:255]
        # Fallback: look for "Av.", "Calle", "Pasaje" etc.
        match = re.search(r'(?:Av(?:enida)?\.?|Calle|Pasaje|Ruta|Km\.?)\s+[^\.,\n]{5,80}', text)
        if match:
            return match.group(0)[:255]
        return 'Sin información'
