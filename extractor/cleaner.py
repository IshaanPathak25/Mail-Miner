import re
from typing import List, Tuple

JUNK_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".svg", ".css", ".js",
    ".webp", ".gif", ".ico", ".bmp"
)

TRAILING_CHARS = ".,;:)]}>\"'"

BASIC_EMAIL_SANITY = re.compile(
    r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$"
)


def _normalize(email: str) -> str:
    """Normalize and strip common noise."""
    return email.lower().strip().strip(TRAILING_CHARS)


def clean_emails(data: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
    """
    Clean and deduplicate (email, source_url) pairs.

    - Keeps same email if found on different pages
    - Removes exact duplicate pairs
    """
    if not data:
        return []

    cleaned = set()

    for email, source in data:
        if not email:
            continue

        normalized = _normalize(email)

        # Skip junk asset references
        if normalized.endswith(JUNK_EXTENSIONS):
            continue

        # Basic sanity filter
        if not BASIC_EMAIL_SANITY.match(normalized):
            continue

        cleaned.add((normalized, source))

    # Sort by email for consistency
    return sorted(cleaned, key=lambda x: x[0])