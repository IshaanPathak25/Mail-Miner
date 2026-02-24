# """
# Main entry point for the Web Email Extractor.
# """

# from extractor.validator import validate_and_fix_url
# from extractor.cleaner import clean_emails
# from extractor.exporter import export_to_excel
# from extractor.crawler import crawl_site


# def main():
#     print("=== Web Email Extractor ===")

#     try:
#         url = input("Enter website URL: ").strip()

#         # Step 1: Validate and normalize URL
#         url = validate_and_fix_url(url)

#         # Step 2–4: Crawl site and collect raw emails
#         print("\nStarting crawl...\n")
#         raw_emails = crawl_site(url, max_pages=12, max_depth=2)

#         # Step 5: Clean emails
#         cleaned_emails = clean_emails(raw_emails)

#         if not cleaned_emails:
#             print("No email addresses found on the website.")
#             return

#         # Step 6: Export to Excel
#         output_file = "emails.xlsx"
#         export_to_excel(cleaned_emails, output_file)

#         print(f"\nSuccess! {len(cleaned_emails)} emails saved to '{output_file}'.")

#     except ValueError as ve:
#         print(f"Input Error: {ve}")
#     except Exception as e:
#         print(f"Unexpected Error: {e}")


# if __name__ == "__main__":
#     main()


"""
Main entry point for the Web Email Extractor.
"""

import asyncio

from extractor.validator import validate_and_fix_url
from extractor.cleaner import clean_emails
from extractor.exporter import export_to_excel
from extractor.crawler import crawl_site


async def async_main():
    print("=== Web Email Extractor ===")

    try:
        url = input("Enter website URL: ").strip()

        # Step 1: Validate and normalize URL
        url = validate_and_fix_url(url)

        # Step 2–4: Crawl site asynchronously
        print("\nStarting crawl...\n")
        raw_emails = await crawl_site(
            url,
            max_pages=20,   # slightly increased default
            max_depth=2,
        )

        # Step 5: Clean emails
        cleaned_emails = clean_emails(raw_emails)

        if not cleaned_emails:
            print("No email addresses found on the website.")
            return

        # Step 6: Export to Excel
        output_file = "emails.xlsx"
        export_to_excel(cleaned_emails, output_file)

        print(f"\nSuccess! {len(cleaned_emails)} emails saved to '{output_file}'.")

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()