import sys

from async_crawler import crawl_site_async

import asyncio

async def main():
    args = sys.argv
    if len(args) < 2:
        print("no website provided")
        sys.exit(1)
    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)

    base_url = args[1]

    print(f"Starting async crawl of: {base_url}")

    page_data = await crawl_site_async(base_url)

    try: # to catch key errors form empty {} that I used to track if a link is visited or not
        for page in page_data.values():
            print(f"Found {len(page['outgoing_links'])} outgoing links on {page['url']}")
    except Exception as e:
        pass

    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())