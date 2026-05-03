# MailMiner — Web Email Extractor

A **production-grade, async web crawler** that extracts emails from websites using intelligent prioritization, concurrency, and structured outputs — available via both **CLI and live web app**.

🌐 **Live App**: https://mail-miner.onrender.com/  
💻 **GitHub**: https://github.com/IshaanPathak25/Mail-Miner

---

## 🚀 Overview

MailMiner is an advanced email extraction system designed to transform unstructured web content into structured, usable data.

Unlike basic scrapers, it features:
- **Async concurrent crawling**
- **Priority-based URL traversal**
- **Source-aware email tracking**
- **Analytics and crawl reporting**
- **CLI + Web interface**

---

## ⚡ Features

### 🔍 Intelligent Crawling
- Async crawling using `asyncio + aiohttp`
- Configurable worker pool for concurrency
- Domain-restricted crawling
- Depth and page-limit control

### 🧠 Priority-Based Extraction
- High-value pages prioritized:
  - `contact`, `faculty`, `directory`, `staff`
- Low-value pages deprioritized:
  - `gallery`, `events`, `news`

### 📧 Email Extraction
- Extracts from:
  - Page text (regex)
  - `mailto:` links
- Source tracking:
  email → source URL(s)


### 📊 Structured Outputs
- Excel export (`.xlsx`)
- Crawl report (`report.json`)
- Crawl log (`crawl_log.json`)

### 🖥️ Dual Interface

#### CLI Mode
```bash
python main.py https://example.com
```

#### Web App
- Clean UI
- Download Options:
  - Excel
  - Excel + report
  - Excel + report + crawl log

### 🧰 Tech Stack
- Backend: Python, FastAPI
- Concurrency: asyncio, aiohttp
- Parsing: BeautifulSoup, lmxl
- Data Processing: Regex
- Export: openpyxl
- Deployment: Render
- Frontend: HTML

### 🚀 Usage
#### CLI Usage:
- Basic
  ```bash
  python main.py https://example.com
  ```
- Full Control
  ```bash
  python main.py https://example.com \
  --depth 3 \
  --max-pages 50 \
  --workers 12 \
  --output-dir ./results \
  --verbose
  ```
- Summary Only
  ```bash
  python main.py https://example.com --only-summary
  ```

- Top Pages Insight
  ```bash
  python main.py https://example.com --top-pages 5
  ```

### 📊 Output Format
1. Excel File
   | Email | Source URL |

2. Crawl Report (report.json)
   ```json
   {
      "total_pages_crawled": 20,
      "total_emails_found": 321,
      "unique_emails": 300,
      "top_email_domains": {
        "nitt.edu": 120
      }
   }
   ```
3. Crawl Log (crawl_log.json)
   ```json
   [
     {
       "url": "...",
       "depth": 2,
       "emails_found": 12
     }
   ]
   ```

### 🧠 How It Works
Pipeline
1. Fetch — Async page retrieval
2. Parse — Extract emails via regex + HTML parsing
3. Clean — Normalize and deduplicate
4. Track — Map emails to source pages
5. Prioritize — Rank URLs dynamically
6. Export — Generate structured outputs

### 📁 Project Structure
```
web-email-extractor/
│
├── app.py                 # FastAPI web server
├── main.py                # CLI entry point
├── requirements.txt
├── Procfile
│
├── templates/             # Web UI
│   └── index.html
│
└── extractor/
    ├── crawler.py
    ├── fetcher.py
    ├── parser.py
    ├── cleaner.py
    ├── exporter.py
    ├── validator.py
    └── cli.py
```

### ⚠️ Limitations
- No JavaScript rendering (static HTML only)
- Performance depends on target website structure
- Free-tier deployment may timeout on large crawls

### 🔮 Future Improvements
- Adaptive crawling (self-learning priorities)
- JavaScript rendering (Playwright fallback)
- Email classification (personal vs institutional)
- UI-based result preview before download

### 🧪 Example Use Cases
- Academic institution email extraction
- Lead generation
- Directory scraping
- Data collection for research

### 📦 Installation
```bash
git clone https://github.com/IshaanPathak25/web-email-extractor
cd web-email-extractor
pip install -r requirements.txt
```

### ▶️ Run Locally
CLI
```bash
python main.py https://example.com
```

Web App
```bash
uvicorn app:app --reload
```

### 🧠 Key Highlights
- Async architecture for high efficiency
- Priority-based crawling for smarter extraction
- Source-aware email tracking
- Deployable web interface
- Modular, scalable design
