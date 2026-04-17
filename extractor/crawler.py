# import asyncio
# import random
# from urllib.parse import urljoin, urlparse
# from typing import Set, Optional, Dict

# import aiohttp
# from bs4 import BeautifulSoup

# from extractor.fetcher import fetch_page_content
# from extractor.parser import extract_emails


# SKIP_EXTENSIONS = (
#     ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
#     ".pdf", ".zip", ".rar", ".exe", ".css", ".js",
#     ".ico", ".mp4", ".mp3", ".avi"
# )

# CRAWL_WORKERS = 8

# POLITE_DELAY_MIN = 0.05
# POLITE_DELAY_MAX = 0.15


# def _normalize_url(url: str) -> str:
#     parsed = urlparse(url)
#     scheme = "https"
#     netloc = parsed.netloc.lower()
#     path = parsed.path.rstrip("/")
#     return f"{scheme}://{netloc}{path}"


# def _is_same_domain(base_url: str, new_url: str) -> bool:
#     return urlparse(base_url).netloc.lower() == urlparse(new_url).netloc.lower()


# def _score_url(url: str, anchor_text: str = "", email_boost: int = 0) -> int:
#     url_lower = url.lower()
#     anchor_lower = anchor_text.lower()

#     score = 50

#     # High-value signals (URL)
#     if any(k in url_lower for k in ["contact", "faculty", "staff", "directory"]):
#         score -= 30

#     if any(k in url_lower for k in ["admission", "department", "people"]):
#         score -= 20

#     # Low-value signals
#     if any(k in url_lower for k in ["gallery", "event", "news", "video"]):
#         score += 20

#     # Anchor text boost
#     if any(k in anchor_lower for k in ["contact", "faculty", "staff", "directory", "team"]):
#         score -= 10

#     return score + email_boost


# async def crawl_site(
#     start_url: str,
#     max_pages: Optional[int] = None,
#     max_depth: int = 3,
# ) -> list[tuple[str, str]]:

#     visited: Set[str] = set()   # processed
#     seen: Set[str] = set()      # enqueued

#     email_map: Dict[str, Set[str]] = {}

#     queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
#     counter = 0

#     start_priority = _score_url(start_url)
#     await queue.put((start_priority, counter, start_url, 0))
#     seen.add(_normalize_url(start_url))

#     pages_crawled = 0
#     pages_lock = asyncio.Lock()
#     visited_lock = asyncio.Lock()
#     email_lock = asyncio.Lock()

#     timeout = aiohttp.ClientTimeout(total=20)

#     connector = aiohttp.TCPConnector(
#         limit=CRAWL_WORKERS * 2,
#         limit_per_host=CRAWL_WORKERS,
#     )

#     async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:

#         async def worker(worker_id: int):
#             nonlocal pages_crawled, counter

#             while True:
#                 try:
#                     priority, _, current_url, depth = await asyncio.wait_for(
#                         queue.get(), timeout=5
#                     )
#                 except asyncio.TimeoutError:
#                     return

#                 normalized_current = _normalize_url(current_url)

#                 async with visited_lock:
#                     if normalized_current in visited or depth > max_depth:
#                         queue.task_done()
#                         continue
#                     visited.add(normalized_current)

#                 should_process = False
#                 async with pages_lock:
#                     if max_pages is None or pages_crawled < max_pages:
#                         pages_crawled += 1
#                         crawl_index = pages_crawled
#                         should_process = True

#                 if should_process:
#                     html_content = await fetch_page_content(session, current_url)

#                     if html_content:
#                         print(f"[Crawl] ({crawl_index}) {current_url}")

#                         page_emails = extract_emails(html_content)

#                         # Email density boost
#                         email_boost = -10 if len(page_emails) >= 3 else 0

#                         if page_emails:
#                             async with email_lock:
#                                 for email in page_emails:
#                                     if email not in email_map:
#                                         email_map[email] = set()
#                                     email_map[email].add(current_url)

#                         if depth < max_depth:
#                             soup = BeautifulSoup(html_content, "lxml")

#                             for a in soup.find_all("a", href=True):
#                                 href = a["href"].strip()

#                                 if not href or href.startswith(("mailto:", "tel:", "javascript:")):
#                                     continue

#                                 absolute = urljoin(current_url, href)
#                                 absolute = absolute.split("#")[0]

#                                 if absolute.lower().endswith(SKIP_EXTENSIONS):
#                                     continue

#                                 if not _is_same_domain(start_url, absolute):
#                                     continue

#                                 normalized_link = _normalize_url(absolute)

#                                 async with visited_lock:
#                                     if normalized_link in seen:
#                                         continue
#                                     seen.add(normalized_link)

#                                 anchor_text = a.get_text(" ", strip=True)

#                                 counter += 1
#                                 priority = _score_url(
#                                     absolute,
#                                     anchor_text=anchor_text,
#                                     email_boost=email_boost
#                                 )

#                                 await queue.put((priority, counter, absolute, depth + 1))

#                     await asyncio.sleep(
#                         random.uniform(POLITE_DELAY_MIN, POLITE_DELAY_MAX)
#                     )

#                 queue.task_done()

#         workers = [
#             asyncio.create_task(worker(i))
#             for i in range(CRAWL_WORKERS)
#         ]

#         await queue.join()

#         for w in workers:
#             w.cancel()

#     result = []
#     for email, sources in email_map.items():
#         for src in sources:
#             result.append((email, src))

#     return result

import asyncio
import random
from urllib.parse import urljoin, urlparse
from typing import Set, Optional, Dict
from collections import Counter
from datetime import datetime

import aiohttp
from bs4 import BeautifulSoup

from extractor.fetcher import fetch_page_content
from extractor.parser import extract_emails


SKIP_EXTENSIONS = (
    ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
    ".pdf", ".zip", ".rar", ".exe", ".css", ".js",
    ".ico", ".mp4", ".mp3", ".avi"
)

CRAWL_WORKERS = 8

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


def _score_url(url: str, anchor_text: str = "", email_boost: int = 0) -> int:
    url_lower = url.lower()
    anchor_lower = anchor_text.lower()

    score = 50

    if any(k in url_lower for k in ["contact", "faculty", "staff", "directory"]):
        score -= 30

    if any(k in url_lower for k in ["admission", "department", "people"]):
        score -= 20

    if any(k in url_lower for k in ["gallery", "event", "news", "video"]):
        score += 20

    if any(k in anchor_lower for k in ["contact", "faculty", "staff", "directory", "team"]):
        score -= 10

    return score + email_boost


async def crawl_site(
    start_url: str,
    max_pages: Optional[int] = None,
    max_depth: int = 3,
) -> tuple[list[tuple[str, str]], dict]:

    visited: Set[str] = set()
    seen: Set[str] = set()

    email_map: Dict[str, Set[str]] = {}

    # ✅ Crawl stats
    crawl_stats = {
        "start_url": start_url,
        "total_pages_crawled": 0,
        "total_emails_found": 0,
        "unique_emails": 0,
        "crawl_depth": max_depth,
    }

    queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
    counter = 0

    start_priority = _score_url(start_url)
    await queue.put((start_priority, counter, start_url, 0))
    seen.add(_normalize_url(start_url))

    pages_crawled = 0
    pages_lock = asyncio.Lock()
    visited_lock = asyncio.Lock()
    email_lock = asyncio.Lock()

    timeout = aiohttp.ClientTimeout(total=20)

    connector = aiohttp.TCPConnector(
        limit=CRAWL_WORKERS * 2,
        limit_per_host=CRAWL_WORKERS,
    )

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:

        async def worker(worker_id: int):
            nonlocal pages_crawled, counter

            while True:
                try:
                    priority, _, current_url, depth = await asyncio.wait_for(
                        queue.get(), timeout=5
                    )
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
                        crawl_stats["total_pages_crawled"] = pages_crawled
                        should_process = True

                if should_process:
                    html_content = await fetch_page_content(session, current_url)

                    if html_content:
                        print(f"[Crawl] ({crawl_index}) {current_url}")

                        page_emails = extract_emails(html_content)

                        # ✅ stats: total raw emails found
                        crawl_stats["total_emails_found"] += len(page_emails)

                        email_boost = -10 if len(page_emails) >= 3 else 0

                        if page_emails:
                            async with email_lock:
                                for email in page_emails:
                                    if email not in email_map:
                                        email_map[email] = set()
                                    email_map[email].add(current_url)

                        if depth < max_depth:
                            soup = BeautifulSoup(html_content, "lxml")

                            for a in soup.find_all("a", href=True):
                                href = a["href"].strip()

                                if not href or href.startswith(("mailto:", "tel:", "javascript:")):
                                    continue

                                absolute = urljoin(current_url, href)
                                absolute = absolute.split("#")[0]

                                if absolute.lower().endswith(SKIP_EXTENSIONS):
                                    continue

                                if not _is_same_domain(start_url, absolute):
                                    continue

                                # 🔥 optional junk filter (high ROI)
                                if any(x in absolute.lower() for x in ["login", "register", "search"]):
                                    continue

                                normalized_link = _normalize_url(absolute)

                                async with visited_lock:
                                    if normalized_link in seen:
                                        continue
                                    seen.add(normalized_link)

                                anchor_text = a.get_text(" ", strip=True)

                                counter += 1
                                priority = _score_url(
                                    absolute,
                                    anchor_text=anchor_text,
                                    email_boost=email_boost
                                )

                                await queue.put((priority, counter, absolute, depth + 1))

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

    # ✅ final stats
    crawl_stats["unique_emails"] = len(email_map)

    domain_counter = Counter()
    for email in email_map:
        domain = email.split("@")[-1]
        domain_counter[domain] += 1

    crawl_stats["top_email_domains"] = dict(domain_counter.most_common(10))
    crawl_stats["timestamp"] = datetime.utcnow().isoformat()

    # flatten result
    result = []
    for email, sources in email_map.items():
        for src in sources:
            result.append((email, src))

    return result, crawl_stats