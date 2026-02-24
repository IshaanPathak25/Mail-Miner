"""
Async Fetcher module for retrieving webpage content.
"""

import asyncio
from typing import Optional

import aiohttp

# ---- Config ----
DEFAULT_TIMEOUT = 12
MAX_RETRIES = 2
CONCURRENT_REQUESTS = 10

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )
}

_semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)


async def _fetch_once(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int,
) -> Optional[str]:
    """Single attempt fetch."""
    try:
        async with session.get(url, headers=HEADERS, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            return await resp.text()
    except (asyncio.TimeoutError, aiohttp.ClientError):
        return None


async def fetch_page_content(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> Optional[str]:
    """
    Fetch page with HTTPS→HTTP fallback and retries.
    """

    async with _semaphore:
        # --- Build HTTPS-first URL ---
        if url.startswith("http://"):
            https_url = "https://" + url[len("http://") :]
        else:
            https_url = url

        # --- Try HTTPS first ---
        for _ in range(MAX_RETRIES + 1):
            html = await _fetch_once(session, https_url, timeout)
            if html:
                return html
            await asyncio.sleep(0.4)

        # --- Fallback to HTTP if original was HTTP ---
        if url.startswith("http://"):
            for _ in range(MAX_RETRIES + 1):
                html = await _fetch_once(session, url, timeout)
                if html:
                    return html
                await asyncio.sleep(0.4)

    return None