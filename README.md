# Web Crawler

A command-line web crawler built in Python that asynchronously crawls a website and exports the results to a CSV report.

## What it does

Given a starting URL, the crawler visits pages within the same domain and collects data from each one. It stays within the base domain, skips already-visited pages, and stops once it hits the page limit you set.

For each page it crawls, it extracts:
- The H1 heading
- The first paragraph of text
- All outgoing links
- All image URLs

Everything is saved to a `report.csv` file when the crawl finishes.

## What I learned
- Async programming with `asyncio` and `aiohttp`
- Concurrency control with semaphores and locks
- HTML parsing with BeautifulSoup
- URL normalization and same-domain filtering
- Writing CSV files with Python's `csv` module
- Test-Driven Development with `test_crawl.py`
