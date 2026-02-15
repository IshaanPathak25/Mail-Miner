# Web Email Extractor

A lightweight Python-based tool that automatically extracts email addresses from websites and exports them into clean Excel files.

## Overview

Web Email Extractor is a simple, reliable tool designed to solve a practical problem: converting unstructured web content into usable, structured email data with minimal effort. It takes a single website URL as input, identifies all valid email addresses on the page, cleans and deduplicates the data, and generates a professional Excel spreadsheet ready for immediate use.

## Features

- **Simple Input**: Just provide a website URL
- **Comprehensive Extraction**: Finds emails in both text content and mailto links
- **Smart Validation**: Filters out invalid or malformed email addresses
- **Automatic Deduplication**: Removes duplicate entries automatically
- **Excel Export**: Generates clean, formatted Excel files with metadata
- **Error Handling**: Clear error messages and recovery guidance
- **No Complexity**: Straightforward design with predictable behavior

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository:
   ```bash
   cd web-email-extractor
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Extract emails from a website:
```bash
python main.py https://example.com
```

This will create a file named `extracted_emails.xlsx` in the current directory.

### Specify Output File

Custom output file name:
```bash
python main.py https://example.com -o my_emails.xlsx
```

Or using the long form:
```bash
python main.py https://example.com --output company_contacts.xlsx
```

### Without URL Scheme

The tool automatically adds `https://` if you forget:
```bash
python main.py example.com
```

## Output Format

The tool generates an Excel file with two sheets:

### 1. Email Addresses Sheet
- **No.**: Sequential numbering
- **Email Address**: The extracted email address

Emails are:
- Converted to lowercase
- Sorted alphabetically
- Deduplicated
- Validated for proper format

### 2. Metadata Sheet
Contains extraction details:
- Total number of emails found
- Extraction date and time
- Source URL

## Project Structure

```
web-email-extractor/
│
├── main.py                 # CLI interface and entry point
├── requirements.txt        # Project dependencies
├── README.md              # Documentation
│
└── extractor/             # Core extraction package
    ├── __init__.py        # Package orchestration
    ├── fetcher.py         # Webpage retrieval
    ├── parser.py          # Email pattern extraction
    ├── validator.py       # Email validation
    ├── cleaner.py         # Deduplication and cleaning
    └── exporter.py        # Excel file generation
```

## How It Works

The extraction process follows a clear pipeline:

1. **Fetch**: Retrieves the webpage content using HTTP requests
2. **Parse**: Extracts email patterns using regex and BeautifulSoup
3. **Validate**: Filters out invalid email addresses
4. **Clean**: Deduplicates and normalizes the results
5. **Export**: Generates a formatted Excel file

## Error Handling

The tool provides clear error messages and guidance:

- **Connection errors**: Checks URL format and internet connectivity
- **Invalid URLs**: Suggests adding `https://` prefix
- **No emails found**: Informs when no valid emails are detected
- **File permission errors**: Checks if output file is open elsewhere

## Dependencies

- **requests** (>=2.31.0): HTTP library for fetching webpages
- **beautifulsoup4** (>=4.12.0): HTML parsing and text extraction
- **lxml** (>=4.9.0): Fast XML and HTML parser
- **openpyxl** (>=3.1.0): Excel file creation and formatting

## Limitations

- Extracts only from the initial page load (no JavaScript execution)
- Does not follow links or crawl multiple pages
- Email addresses must be in standard format
- Respects standard HTTP timeout limits

## Examples

### Example 1: Company Contact Page
```bash
python main.py https://company.com/contact
```

### Example 2: About Page
```bash
python main.py https://organization.org/about -o team_emails.xlsx
```

### Example 3: Simple Domain
```bash
python main.py example.com
```

## Requirements File

The `requirements.txt` includes:
```
requests>=2.31.0
beautifulsoup4>=4.12.0
openpyxl>=3.1.0
lxml>=4.9.0
```

## License

This project is provided as-is for educational and practical use.

## Version

Current version: **1.0.0**

## Support

If you encounter issues:
1. Verify your Python version (3.7+)
2. Ensure all dependencies are installed
3. Check your internet connection
4. Verify the target URL is accessible
5. Make sure the output file isn't open in Excel

## Contributing

This is a focused, single-purpose tool. The design prioritizes simplicity and reliability over feature expansion.

---

**Web Email Extractor** - Simple, predictable, and reliable email extraction.

