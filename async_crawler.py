import aiohttp
import asyncio

from urllib.parse import urlparse

from crawl import extract_page_data, normalize_url, get_urls_from_html

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=1):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None


    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    
    # returns True if page not visited
    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if normalized_url in self.page_data:
                return False
            
            return True
        

    async def get_html_async(self, url):
        try:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
                if response.status != 200:
                    raise Exception(f"Error Code: {response.status}")
                
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    raise Exception(f"Invalid content type")
                
                return await response.text()
        except Exception as e:
            print(e)
            return None
        
    
    async def crawl_page_async(self, current_url=None):
        if current_url is None:
            current_url = self.base_url

        base_url_parsed, current_url_parsed = urlparse(self.base_url), urlparse(current_url)

        if base_url_parsed.netloc != current_url_parsed.netloc:
            return 
        
        current_url_normalized = normalize_url(current_url)

        if not await self.add_page_visit(current_url_normalized):
            return
                
        print(f"Crawling page: {current_url}")
        
        try:
            async with self.semaphore:
                html = await self.get_html_async(current_url)

                if html is None:
                    raise Exception("Error while getting HTML")
        except Exception as e:
            print(e)
            
            async with self.lock:
                self.page_data[current_url_normalized] = {}

            return 

        data = extract_page_data(html, current_url)

        async with self.lock:
                self.page_data[current_url_normalized] = data
        
        urls = get_urls_from_html(html, current_url)
        tasks = set()
        for url in urls:
            task = asyncio.create_task(self.crawl_page_async(url))

            tasks.add(task)
            task.add_done_callback(tasks.discard)

        await asyncio.gather(*tasks)

        return
    

    async def crawl(self):
        await self.crawl_page_async()

        return self.page_data

async def crawl_site_async(base_url):
    async with AsyncCrawler(base_url, max_concurrency=3) as crawler:
        return await crawler.crawl()
