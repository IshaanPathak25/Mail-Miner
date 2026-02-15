"""
Exporter module for saving email addresses to an Excel file.
"""

from typing import List
import pandas as pd


def export_to_excel(emails: List[str], filename: str) -> None:
    """
    Export email addresses to an Excel file.

    Args:
        emails: List of cleaned email addresses
        filename: Output Excel filename
    """
    if not emails:
        return

    df = pd.DataFrame(emails, columns=["Email"])
    df.to_excel(filename, index=False)
