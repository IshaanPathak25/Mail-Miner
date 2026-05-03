"""
FastAPI app for Web Email Extractor.
Provides UI + download endpoint.
"""

import os
import tempfile
import zipfile
from urllib.parse import urlparse
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel

from extractor.crawler import crawl_site
from extractor.cleaner import clean_emails
from extractor.exporter import (
    export_to_excel,
    export_crawl_report,
    export_crawl_log,
)
from extractor.validator import validate_and_fix_url


app = FastAPI(title="Web Email Extractor")


# ---------------------------
# Request Model
# ---------------------------

class CrawlRequest(BaseModel):
    url: str
    depth: int = 2
    max_pages: int = 20
    include_report: bool = True
    include_log: bool = True


# ---------------------------
# Helper: generate filename prefix
# ---------------------------

def _make_prefix(url: str) -> str:
    netloc = urlparse(url).netloc.lower().lstrip("www.")
    return netloc.split(".")[0]


# ---------------------------
# UI Route
# ---------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    template_path = Path(__file__).parent / "templates" / "index.html"

    if not template_path.exists():
        return HTMLResponse(
            content="<h2>Error: index.html not found</h2>",
            status_code=500
        )

    return HTMLResponse(template_path.read_text(encoding="utf-8"))


# ---------------------------
# Download Endpoint
# ---------------------------

@app.post("/download")
async def download(req: CrawlRequest):
    try:
        # Step 1: Validate URL
        url = validate_and_fix_url(req.url)
        max_pages = req.max_pages if req.max_pages > 0 else None

        # Step 2: Run crawler
        raw_emails, stats, crawl_log = await crawl_site(
            url,
            max_pages=max_pages,
            max_depth=req.depth,
        )

        # Step 3: Clean emails
        cleaned = clean_emails(raw_emails)

        prefix = _make_prefix(url)

        # ✅ FIX: Use mkdtemp (persistent)
        tmpdir = tempfile.mkdtemp()

        files_to_zip = []

        # ---- Excel (always included) ----
        excel_path = os.path.join(tmpdir, f"{prefix}_emails.xlsx")

        if cleaned:
            export_to_excel(cleaned, excel_path)
        else:
            # prevent crash if no emails
            with open(excel_path, "w", encoding="utf-8") as f:
                f.write("No emails found")

        files_to_zip.append(excel_path)

        # ---- Report (optional) ----
        if req.include_report:
            report_path = os.path.join(tmpdir, f"{prefix}_report.json")
            export_crawl_report(stats, report_path)
            files_to_zip.append(report_path)

        # ---- Crawl log (optional) ----
        if req.include_log:
            log_path = os.path.join(tmpdir, f"{prefix}_crawl_log.json")
            export_crawl_log(crawl_log, log_path)
            files_to_zip.append(log_path)

        # ---- Create ZIP ----
        zip_path = os.path.join(tmpdir, f"{prefix}_result.zip")

        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file in files_to_zip:
                if os.path.exists(file):
                    zf.write(file, os.path.basename(file))

        # Step 5: Return ZIP
        return FileResponse(
            zip_path,
            media_type="application/zip",
            filename=f"{prefix}_result.zip"
        )

    except Exception as e:
        print("ERROR:", str(e))  # shows in terminal
        raise HTTPException(status_code=500, detail=str(e))