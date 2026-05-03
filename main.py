"""
Main entry point for the Web Email Extractor.
"""

import asyncio
import os
from urllib.parse import urlparse

from extractor.cli import parse_args
from extractor.validator import validate_and_fix_url
from extractor.cleaner import clean_emails
from extractor.exporter import (
    export_to_excel,
    export_crawl_report,
    export_crawl_log,
)
from extractor.crawler import crawl_site


def _make_output_filenames(url: str) -> dict:
    netloc = urlparse(url).netloc.lower()
    netloc = netloc.lstrip("www.")
    label = netloc.split(".")[0]
    return {
        "emails":    f"{label}_emails.xlsx",
        "report":    f"{label}_report.json",
        "crawl_log": f"{label}_crawl_log.json",
    }


def _short_url(url: str) -> str:
    parsed = urlparse(url)
    return parsed.path or "/"


async def async_main():
    args = parse_args()

    print("=== Web Email Extractor ===")
    print(f"  URL        : {args.url}")
    print(f"  Depth      : {args.depth}")
    print(f"  Max pages  : {args.max_pages or 'unlimited'}")
    print(f"  Workers    : {args.workers}")
    print(f"  Output dir : {args.output_dir}")
    print()

    try:
        # Step 1: Validate and normalize URL
        url = validate_and_fix_url(args.url)

        # Resolve max_pages: 0 means unlimited (None in crawler)
        max_pages = args.max_pages if args.max_pages > 0 else None

        # Ensure output directory exists
        os.makedirs(args.output_dir, exist_ok=True)

        # Build output filenames from domain
        filenames = _make_output_filenames(url)

        # Step 2–4: Crawl site asynchronously
        print("Starting crawl...\n")
        raw_emails, stats, crawl_log = await crawl_site(
            url,
            max_pages=max_pages,
            max_depth=args.depth,
            workers=args.workers,
            verbose=args.verbose,
        )

        # Step 5: Clean emails
        cleaned_emails = clean_emails(raw_emails)

        # 🔥 Top pages insight (printed always if enabled)
        if getattr(args, "top_pages", 0) > 0 and crawl_log:
            print("\n=== Top Pages by Email Yield ===")

            top_pages = sorted(
                crawl_log,
                key=lambda x: x["emails_found"],
                reverse=True
            )[:args.top_pages]

            for i, entry in enumerate(top_pages, 1):
                print(f"{i}. {_short_url(entry['url'])} → {entry['emails_found']} emails")

        # 🔥 ONLY SUMMARY MODE
        if args.only_summary:
            print("\n=== Crawl Summary ===")
            for k, v in stats.items():
                print(f"{k}: {v}")
            return

        # 📊 Export Excel
        if not args.no_excel and cleaned_emails:
            output_file = os.path.join(args.output_dir, filenames["emails"])
            export_to_excel(cleaned_emails, output_file)
            print(f"\nSaved emails → {output_file}")
        elif not cleaned_emails:
            print("No email addresses found.")

        # 📄 Export Report
        if not args.no_report:
            report_file = os.path.join(args.output_dir, filenames["report"])
            export_crawl_report(stats, report_file)
            print(f"Saved report → {report_file}")

        # 📜 Export Crawl Log
        if not args.no_log:
            log_file = os.path.join(args.output_dir, filenames["crawl_log"])
            export_crawl_log(crawl_log, log_file)
            print(f"Saved crawl log → {log_file}")

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()