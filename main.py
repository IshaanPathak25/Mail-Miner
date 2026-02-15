"""
Main entry point for the Web Email Extractor.
"""

from extractor.validator import validate_and_fix_url
from extractor.fetcher import fetch_page_content
from extractor.parser import extract_emails
from extractor.cleaner import clean_emails
from extractor.exporter import export_to_excel


def main():
    print("=== Web Email Extractor ===")

    try:
        url = input("Enter website URL: ").strip()

        # Step 1: Validate and normalize URL
        url = validate_and_fix_url(url)

        # Step 2: Fetch webpage content
        html_content = fetch_page_content(url)

        # Step 3: Extract raw emails
        raw_emails = extract_emails(html_content)

        # Step 4: Clean emails
        cleaned_emails = clean_emails(raw_emails)

        if not cleaned_emails:
            print("No email addresses found on the website.")
            return

        # Step 5: Export to Excel
        output_file = "emails.xlsx"
        export_to_excel(cleaned_emails, output_file)

        print(f"Success! {len(cleaned_emails)} emails saved to '{output_file}'.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
