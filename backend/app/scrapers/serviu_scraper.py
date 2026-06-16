from bs4 import BeautifulSoup

from app.scrapers.base_scraper import BaseScraper


class ServiuScraper(BaseScraper):
    def __init__(self) -> None:
        super().__init__('https://www.serviu.cl')

    async def scrape(self) -> list[dict[str, str]]:
        html = await self.fetch('/')
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select('a')
        calls: list[dict[str, str]] = []
        for link in links[:20]:
            calls.append(
                {
                    'subsidy_program': link.get_text(strip=True)[:80] or 'SERVIU Call',
                    'region': 'Unknown',
                    'opening_date': 'Unknown',
                    'closing_date': 'Unknown',
                    'available_quotas': '0',
                    'requirements': 'Check official SERVIU website',
                }
            )
        return calls
