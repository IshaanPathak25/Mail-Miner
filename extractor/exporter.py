"""
Exporter module for saving email addresses to an Excel file.
"""

from typing import List
from pathlib import Path
from openpyxl import Workbook


def export_to_excel(emails: List[str], filename: str) -> None:
    """
    Export email addresses to an Excel file.
    """
    if not emails:
        return

    # Ensure parent directory exists
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Emails"

    # Header
    ws.append(["Email"])

    # Data
    for email in emails:
        ws.append([email])

    wb.save(filename)