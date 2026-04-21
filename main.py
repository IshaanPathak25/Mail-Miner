# """
# Main entry point for the Web Email Extractor.
# """

# import asyncio
# import os

# from extractor.cli import parse_args
# from extractor.validator import validate_and_fix_url
# from extractor.cleaner import clean_emails
# from extractor.exporter import (
#     export_to_excel,
#     export_crawl_report,
#     export_crawl_log,
# )
# from extractor.crawler import crawl_site


# async def async_main():
#     args = parse_args()

#     print("=== Web Email Extractor ===")
#     print(f"  URL        : {args.url}")
#     print(f"  Depth      : {args.depth}")
#     print(f"  Max pages  : {args.max_pages or 'unlimited'}")
#     print(f"  Workers    : {args.workers}")
#     print(f"  Output dir : {args.output_dir}")
#     print()

#     try:
#         # Step 1: Validate and normalize URL
#         url = validate_and_fix_url(args.url)

#         # Resolve max_pages: 0 means unlimited (None in crawler)
#         max_pages = args.max_pages if args.max_pages > 0 else None

#         # Ensure output directory exists
#         os.makedirs(args.output_dir, exist_ok=True)

#         # Step 2–4: Crawl site asynchronously
#         print("Starting crawl...\n")
#         raw_emails, stats, crawl_log = await crawl_site(
#             url,
#             max_pages=max_pages,
#             max_depth=args.depth,
#             workers=args.workers,
#             verbose=args.verbose,
#         )

#         # Step 5: Clean emails
#         cleaned_emails = clean_emails(raw_emails)

#         if not cleaned_emails:
#             print("No email addresses found on the website.")
#         else:
#             # Step 6: Export emails to Excel
#             output_file = os.path.join(args.output_dir, "emails.xlsx")
#             export_to_excel(cleaned_emails, output_file)
#             print(f"\nSuccess! {len(cleaned_emails)} emails saved to '{output_file}'.")

#         # Step 7: Export crawl report
#         report_file = os.path.join(args.output_dir, "report.json")
#         export_crawl_report(stats, report_file)
#         print(f"Crawl report saved to '{report_file}'.")

#         # Step 8: Export detailed crawl log
#         log_file = os.path.join(args.output_dir, "crawl_log.json")
#         export_crawl_log(crawl_log, log_file)
#         print(f"Crawl log saved to '{log_file}'.")

#     except ValueError as ve:
#         print(f"Input Error: {ve}")
#     except Exception as e:
#         print(f"Unexpected Error: {e}")


# def main():
#     asyncio.run(async_main())


# if __name__ == "__main__":
#     main()

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

        if not cleaned_emails:
            print("No email addresses found on the website.")
        else:
            # Step 6: Export emails to Excel
            output_file = os.path.join(args.output_dir, filenames["emails"])
            export_to_excel(cleaned_emails, output_file)
            print(f"\nSuccess! {len(cleaned_emails)} emails saved to '{output_file}'.")

        # Step 7: Export crawl report
        report_file = os.path.join(args.output_dir, filenames["report"])
        export_crawl_report(stats, report_file)
        print(f"Crawl report saved to '{report_file}'.")

        # Step 8: Export detailed crawl log
        log_file = os.path.join(args.output_dir, filenames["crawl_log"])
        export_crawl_log(crawl_log, log_file)
        print(f"Crawl log saved to '{log_file}'.")

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()