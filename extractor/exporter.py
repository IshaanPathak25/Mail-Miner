# """
# Exporter module for saving email addresses to an Excel file.
# """

# from typing import List, Tuple
# from pathlib import Path
# from openpyxl import Workbook


# def export_to_excel(data: List[Tuple[str, str]], filename: str) -> None:
#     """
#     Export email addresses along with source URLs to an Excel file.
#     """
#     if not data:
#         return

#     # Ensure parent directory exists
#     path = Path(filename)
#     path.parent.mkdir(parents=True, exist_ok=True)

#     wb = Workbook()
#     ws = wb.active
#     ws.title = "Emails"

#     # Header
#     ws.append(["Email", "Source URL"])

#     # Data
#     for email, source in data:
#         ws.append([email, source])

#     wb.save(filename)

"""
Exporter module for saving email addresses to an Excel file
and exporting crawl reports.
"""

from typing import List, Tuple
from pathlib import Path
from openpyxl import Workbook
import json


def export_to_excel(data: List[Tuple[str, str]], filename: str) -> None:
    """
    Export email addresses along with source URLs to an Excel file.
    """
    if not data:
        return

    # Ensure parent directory exists
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()
    ws = wb.active
    ws.title = "Emails"

    # Header
    ws.append(["Email", "Source URL"])

    # Data
    for email, source in data:
        ws.append([email, source])

    wb.save(filename)


def export_crawl_report(stats: dict, filename: str) -> None:
    """
    Export crawl statistics to a JSON file.
    """
    if not stats:
        return

    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)