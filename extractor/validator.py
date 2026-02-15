"""
Validator module for validating and fixing input URLs.
"""

from urllib.parse import urlparse


def validate_and_fix_url(url: str) -> str:
    """
    Validate and normalize a website URL.

    Args:
        url: Raw URL input from the user

    Returns:
        A valid URL string with scheme

    Raises:
        ValueError: If the URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL cannot be empty.")

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.netloc:
        raise ValueError("Invalid URL provided.")

    return url
