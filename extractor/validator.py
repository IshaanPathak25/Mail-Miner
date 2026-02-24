"""
Validator module for validating and fixing input URLs.
"""

from urllib.parse import urlparse, urlunparse


def validate_and_fix_url(url: str) -> str:
    """
    Validate and normalize a website URL.

    Args:
        url: Raw URL input from the user

    Returns:
        A valid normalized URL string

    Raises:
        ValueError: If the URL is invalid
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL cannot be empty.")

    url = url.strip()

    # Add scheme if missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    # Basic host validation
    if not parsed.netloc or "." not in parsed.netloc:
        raise ValueError("Invalid URL provided.")

    # Normalize host to lowercase
    netloc = parsed.netloc.lower()

    # Remove fragment
    normalized = parsed._replace(netloc=netloc, fragment="")

    final_url = urlunparse(normalized)

    # Remove trailing slash (except root)
    if final_url.endswith("/") and parsed.path == "":
        final_url = final_url.rstrip("/")

    return final_url