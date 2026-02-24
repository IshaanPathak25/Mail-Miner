"""
Parser module for extracting email addresses from HTML content.
"""

import re
import html
from typing import List, Set
from bs4 import BeautifulSoup


EMAIL_PATTERN = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
)

OBFUSCATION_PATTERNS = [
    (r'\s*\[at\]\s*', '@'),
    (r'\s*\(at\)\s*', '@'),
    (r'\s+at\s+', '@'),
    (r'\s*\[dot\]\s*', '.'),
    (r'\s*\(dot\)\s*', '.'),
    (r'\s+dot\s+', '.'),
]


def _deobfuscate(text: str) -> str:
    """Normalize common email obfuscations."""
    text = text.lower()
    for pattern, repl in OBFUSCATION_PATTERNS:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    return text


def _normalize_email(email: str) -> str:
    """Clean and normalize extracted email."""
    return email.strip().strip('.,;:)]>').lower()


def extract_emails(html_content: str) -> List[str]:
    """
    Extract all email addresses from HTML content.
    """
    soup = BeautifulSoup(html_content, "lxml")

    # --- Extract mailto first ---
    emails: Set[str] = set()

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("mailto:"):
            email = href.replace("mailto:", "").split("?")[0]
            emails.add(_normalize_email(email))

    # --- Collect visible text ---
    for tag in soup(["script", "style"]):
        tag.extract()

    visible_text = soup.get_text(separator=" ")

    # --- ALSO scan script contents separately ---
    script_text = " ".join(
        script.get_text(" ") for script in soup.find_all("script")
    )

    combined_text = f"{visible_text} {script_text}"

    # --- Decode HTML entities ---
    combined_text = html.unescape(combined_text)

    # --- De-obfuscate ---
    combined_text = _deobfuscate(combined_text)

    # --- Regex extraction ---
    found_emails = EMAIL_PATTERN.findall(combined_text)

    for email in found_emails:
        emails.add(_normalize_email(email))

    return sorted(emails)