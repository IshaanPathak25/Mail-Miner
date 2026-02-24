"""
Cleaner module for deduplicating and cleaning email addresses.
"""

import re
from typing import List

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


def clean_emails(emails: List[str]) -> List[str]:
    """
    Clean and deduplicate a list of email addresses.
    """
    if not emails:
        return []

    cleaned = set()

    for email in emails:
        if not email:
            continue

        normalized = _normalize(email)

        # Skip junk asset references
        if normalized.endswith(JUNK_EXTENSIONS):
            continue

        # Basic sanity filter (cheap but effective)
        if not BASIC_EMAIL_SANITY.match(normalized):
            continue

        cleaned.add(normalized)

    return sorted(cleaned)