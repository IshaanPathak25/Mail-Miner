"""
Cleaner module for deduplicating and cleaning email addresses.
"""

from typing import List

JUNK_EXTENSIONS = (".png", ".jpg", ".jpeg", ".svg", ".css", ".js")


def clean_emails(emails: List[str]) -> List[str]:
    """
    Clean and deduplicate a list of email addresses.
    
    Args:
        emails: List of email addresses to clean
    
    Returns:
        List of unique, cleaned email addresses sorted alphabetically
    """
    if not emails:
        return []
    
    cleaned = set()

    for email in emails:
        if not email:
            continue

        normalized = email.lower().strip()

        # Skip junk asset references
        if normalized.endswith(JUNK_EXTENSIONS):
            continue

        cleaned.add(normalized)

    return sorted(cleaned)
