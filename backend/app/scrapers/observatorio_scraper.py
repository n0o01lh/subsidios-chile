from bs4 import BeautifulSoup

from app.scrapers.base_scraper import BaseScraper


class ObservatorioScraper(BaseScraper):
    def __init__(self) -> None:
        super().__init__('https://www.observatoriohab.minvu.cl')

    async def scrape(self) -> list[dict[str, str]]:
        html = await self.fetch('/')
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('article, .card, .project')
        projects: list[dict[str, str]] = []

        for card in cards[:20]:
            projects.append(
                {
                    'name': card.get_text(strip=True)[:120] or 'Observatorio Project',
                    'region': 'Unknown',
                    'commune': 'Unknown',
                    'program_type': 'Unknown',
                    'available_units': '0',
                    'price_range_uf': 'Not listed',
                    'address': 'Not listed',
                }
            )

        return projects
