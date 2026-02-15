"""
Fetcher module for retrieving webpage content.
"""

import requests


def fetch_page_content(url: str, timeout: int = 10) -> str:
    """
    Fetch the HTML content from the given URL.

    Args:
        url: Valid website URL
        timeout: Request timeout in seconds

    Returns:
        HTML content as a string
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()

    return response.text
