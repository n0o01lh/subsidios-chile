from __future__ import annotations

import asyncio
import random
from abc import ABC, abstractmethod
from typing import Any

import httpx


class BaseScraper(ABC):
    user_agents = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Mozilla/5.0 (X11; Linux x86_64)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
    )

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self._cache: dict[str, str] = {}

    async def fetch(self, path: str = '/') -> str:
        if path in self._cache:
            return self._cache[path]

        retries = 3
        for attempt in range(retries):
            try:
                headers = {'User-Agent': random.choice(self.user_agents)}
                async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                    response = await client.get(f'{self.base_url}{path}', headers=headers)
                    response.raise_for_status()
                    self._cache[path] = response.text
                    return response.text
            except httpx.HTTPError:
                if attempt == retries - 1:
                    raise
                await asyncio.sleep(2**attempt)

        return ''

    @abstractmethod
    async def scrape(self) -> list[dict[str, Any]]:
        raise NotImplementedError
