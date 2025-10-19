import sys

from crawl import crawl_page

import asyncio

from async_crawler import AsyncCrawler

async def main():
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)

    if len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)

    print(f"starting crawl of: {sys.argv[1]}")

    try:
        ac = AsyncCrawler(base_url=sys.argv[1], max_concurrency=1)
        data = await ac.crawl()

        for url in data.keys():
            page_data = data[url]

            print(page_data.get("h1"))
            print(page_data.get("first_paragraph"))

    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
