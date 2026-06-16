from datetime import UTC, datetime

scraper_state: dict[str, datetime] = {}


def mark_scraper_run(scraper_name: str) -> None:
    scraper_state[scraper_name] = datetime.now(UTC)
