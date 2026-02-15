"""
Parser module for extracting email addresses from HTML content.
"""

import re
from typing import List
from bs4 import BeautifulSoup


def extract_emails(html_content: str) -> List[str]:
    """
    Extract all email addresses from HTML content.

    Args:
        html_content: The HTML content as a string

    Returns:
        A list of email addresses found in the content
    """
    soup = BeautifulSoup(html_content, 'lxml')

    for script in soup(['script', 'style']):
        script.decompose()

    text = soup.get_text()

    mailto_emails = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('mailto:'):
            email = href.replace('mailto:', '').split('?')[0]
            mailto_emails.append(email)

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    text_emails = re.findall(email_pattern, text)

    return text_emails + mailto_emails
