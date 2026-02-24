# """
# Async concurrent crawler module for discovering pages and aggregating emails.
# """

# import asyncio
# from urllib.parse import urljoin, urlparse
# from typing import Set, List

# import aiohttp
# from bs4 import BeautifulSoup

# from extractor.fetcher import fetch_page_content
# from extractor.parser import extract_emails


# # Pages that statistically contain emails more often
# PRIORITY_KEYWORDS = (
#     "contact",
#     "about",
#     "team",
#     "support",
#     "help",
#     "careers",
#     "admissions",
# )

# # File types we should NEVER crawl
# SKIP_EXTENSIONS = (
#     ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
#     ".pdf", ".zip", ".rar", ".exe", ".css", ".js",
#     ".ico", ".mp4", ".mp3", ".avi"
# )

# # How many workers run in parallel (tune later)
# CRAWL_WORKERS = 8


# def _normalize_url(url: str) -> str:
#     """Canonicalize URL for deduplication."""
#     parsed = urlparse(url)
#     scheme = "https"
#     netloc = parsed.netloc.lower()
#     path = parsed.path.rstrip("/")
#     return f"{scheme}://{netloc}{path}"


# def _is_same_domain(base_url: str, new_url: str) -> bool:
#     return urlparse(base_url).netloc.lower() == urlparse(new_url).netloc.lower()


# def _prioritize_links(links: Set[str]) -> List[str]:
#     priority, normal = [], []
#     for link in links:
#         if any(k in link.lower() for k in PRIORITY_KEYWORDS):
#             priority.append(link)
#         else:
#             normal.append(link)
#     return priority + normal


# async def crawl_site(
#     start_url: str,
#     max_pages: int = 20,
#     max_depth: int = 2,
# ) -> List[str]:
#     """
#     Concurrent site crawler (deadlock-safe).
#     """

#     visited: Set[str] = set()
#     emails: Set[str] = set()

#     queue: asyncio.Queue = asyncio.Queue()
#     await queue.put((start_url, 0))

#     pages_crawled = 0
#     pages_lock = asyncio.Lock()
#     visited_lock = asyncio.Lock()
#     email_lock = asyncio.Lock()

#     timeout = aiohttp.ClientTimeout(total=20)

#     async with aiohttp.ClientSession(timeout=timeout) as session:

#         async def worker(worker_id: int):
#             nonlocal pages_crawled

#             while True:
#                 try:
#                     current_url, depth = await asyncio.wait_for(queue.get(), timeout=5)
#                 except asyncio.TimeoutError:
#                     return

#                 normalized_current = _normalize_url(current_url)

#                 # ---- visited check ----
#                 async with visited_lock:
#                     if normalized_current in visited or depth > max_depth:
#                         queue.task_done()
#                         continue
#                     visited.add(normalized_current)

#                 # ---- page budget check (NON-EXITING) ----
#                 should_process = False
#                 async with pages_lock:
#                     if pages_crawled < max_pages:
#                         pages_crawled += 1
#                         crawl_index = pages_crawled
#                         should_process = True

#                 if should_process:
#                     html_content = await fetch_page_content(session, current_url)

#                     if html_content:
#                         print(f"[Crawl] ({crawl_index}) {current_url}")

#                         # --- Extract emails ---
#                         page_emails = extract_emails(html_content)
#                         if page_emails:
#                             async with email_lock:
#                                 emails.update(page_emails)

#                         # --- Discover links ---
#                         if depth < max_depth:
#                             soup = BeautifulSoup(html_content, "lxml")
#                             found_links: Set[str] = set()

#                             for a in soup.find_all("a", href=True):
#                                 href = a["href"].strip()

#                                 if not href or href.startswith(("mailto:", "tel:", "javascript:")):
#                                     continue

#                                 absolute = urljoin(start_url, href)
#                                 absolute = absolute.split("#")[0]

#                                 if absolute.lower().endswith(SKIP_EXTENSIONS):
#                                     continue

#                                 if _is_same_domain(start_url, absolute):
#                                     found_links.add(absolute)

#                             ordered_links = _prioritize_links(found_links)

#                             for link in ordered_links:
#                                 normalized_link = _normalize_url(link)
#                                 async with visited_lock:
#                                     if normalized_link not in visited:
#                                         await queue.put((link, depth + 1))

#                 queue.task_done()

#         # ---- Start workers ----
#         workers = [
#             asyncio.create_task(worker(i))
#             for i in range(CRAWL_WORKERS)
#         ]

#         await queue.join()

#         for w in workers:
#             w.cancel()

#     return list(emails)


import asyncio
import random
from urllib.parse import urljoin, urlparse
from typing import Set, List, Optional

import aiohttp
from bs4 import BeautifulSoup

from extractor.fetcher import fetch_page_content
from extractor.parser import extract_emails


PRIORITY_KEYWORDS = (
    "contact",
    "about",
    "team",
    "support",
    "help",
    "careers",
    "admissions",
)

SKIP_EXTENSIONS = (
    ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
    ".pdf", ".zip", ".rar", ".exe", ".css", ".js",
    ".ico", ".mp4", ".mp3", ".avi"
)

CRAWL_WORKERS = 8

# ⭐ polite delay settings
POLITE_DELAY_MIN = 0.05
POLITE_DELAY_MAX = 0.15


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    scheme = "https"
    netloc = parsed.netloc.lower()
    path = parsed.path.rstrip("/")
    return f"{scheme}://{netloc}{path}"


def _is_same_domain(base_url: str, new_url: str) -> bool:
    return urlparse(base_url).netloc.lower() == urlparse(new_url).netloc.lower()


def _prioritize_links(links: Set[str]) -> List[str]:
    priority, normal = [], []
    for link in links:
        if any(k in link.lower() for k in PRIORITY_KEYWORDS):
            priority.append(link)
        else:
            normal.append(link)
    return priority + normal


async def crawl_site(
    start_url: str,
    max_pages: Optional[int] = None,  # ⭐ unlimited supported
    max_depth: int = 3,
) -> List[str]:

    visited: Set[str] = set()
    emails: Set[str] = set()

    queue: asyncio.Queue = asyncio.Queue()
    await queue.put((start_url, 0))

    pages_crawled = 0
    pages_lock = asyncio.Lock()
    visited_lock = asyncio.Lock()
    email_lock = asyncio.Lock()

    timeout = aiohttp.ClientTimeout(total=20)

    connector = aiohttp.TCPConnector(
        limit=CRAWL_WORKERS * 2,
        limit_per_host=CRAWL_WORKERS,  # ⭐ very important for stability
    )

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:

        async def worker(worker_id: int):
            nonlocal pages_crawled

            while True:
                try:
                    current_url, depth = await asyncio.wait_for(queue.get(), timeout=5)
                except asyncio.TimeoutError:
                    return

                normalized_current = _normalize_url(current_url)

                async with visited_lock:
                    if normalized_current in visited or depth > max_depth:
                        queue.task_done()
                        continue
                    visited.add(normalized_current)

                should_process = False
                async with pages_lock:
                    if max_pages is None or pages_crawled < max_pages:
                        pages_crawled += 1
                        crawl_index = pages_crawled
                        should_process = True

                if should_process:
                    html_content = await fetch_page_content(session, current_url)

                    if html_content:
                        print(f"[Crawl] ({crawl_index}) {current_url}")

                        page_emails = extract_emails(html_content)
                        if page_emails:
                            async with email_lock:
                                emails.update(page_emails)

                        if depth < max_depth:
                            soup = BeautifulSoup(html_content, "lxml")
                            found_links: Set[str] = set()

                            for a in soup.find_all("a", href=True):
                                href = a["href"].strip()

                                if not href or href.startswith(("mailto:", "tel:", "javascript:")):
                                    continue

                                absolute = urljoin(start_url, href)
                                absolute = absolute.split("#")[0]

                                if absolute.lower().endswith(SKIP_EXTENSIONS):
                                    continue

                                if _is_same_domain(start_url, absolute):
                                    found_links.add(absolute)

                            ordered_links = _prioritize_links(found_links)

                            for link in ordered_links:
                                normalized_link = _normalize_url(link)
                                async with visited_lock:
                                    if normalized_link not in visited:
                                        await queue.put((link, depth + 1))

                    # ⭐ polite throttling with jitter
                    await asyncio.sleep(
                        random.uniform(POLITE_DELAY_MIN, POLITE_DELAY_MAX)
                    )

                queue.task_done()

        workers = [
            asyncio.create_task(worker(i))
            for i in range(CRAWL_WORKERS)
        ]

        await queue.join()

        for w in workers:
            w.cancel()

    return list(emails)