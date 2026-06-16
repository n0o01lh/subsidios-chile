from bs4 import BeautifulSoup

from app.scrapers.base_scraper import BaseScraper


class MinvuScraper(BaseScraper):
    def __init__(self) -> None:
        super().__init__('https://www.minvu.gob.cl')

    async def scrape(self) -> list[dict[str, str]]:
        html = await self.fetch('/')
        soup = BeautifulSoup(html, 'html.parser')
        headings = soup.select('h1, h2, h3')
        updates: list[dict[str, str]] = []
        for heading in headings[:20]:
            updates.append(
                {
                    'title': heading.get_text(strip=True)[:120],
                    'date': 'Unknown',
                    'summary': 'Extracted from MINVU public page.',
                    'affected_subsidy_program': 'General update',
                }
            )
        return updates
