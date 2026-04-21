"""
CLI argument parsing for Web Email Extractor.
"""

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="email-extractor",
        description="Async web crawler that extracts email addresses from a website.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "url",
        help="Target website URL to crawl (e.g. https://example.com)",
    )

    parser.add_argument(
        "--depth",
        type=int,
        default=2,
        metavar="N",
        help="Maximum crawl depth from the start URL",
    )

    parser.add_argument(
        "--max-pages",
        type=int,
        default=20,
        metavar="N",
        help="Maximum number of pages to crawl (0 = unlimited)",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        metavar="N",
        help="Number of async crawl workers",
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        metavar="DIR",
        help="Directory to write output files (emails.xlsx, report.json, crawl_log.json)",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each crawled URL to stdout",
    )

    return parser.parse_args()