import aiohttp
import asyncio

from urllib.parse import urlparse

from crawl import extract_page_data, normalize_url, get_urls_from_html

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency, max_page):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

        self.max_page = max_page
        self.should_stop = False
        self.all_tasks = set()


    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    
    # returns True if page not visited
    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False

            if normalized_url in self.page_data:
                return False
            
            self.page_data[normalized_url] = {}
            if len(self.page_data) >= self.max_page:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")

                for task in self.all_tasks:
                    if not task.done():
                        task.cancel()

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
        if self.should_stop:
            return

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

        if self.should_stop:
            return
        
        urls = get_urls_from_html(html, current_url)
        tasks = set()
        for url in urls:
            task = asyncio.create_task(self.crawl_page_async(url))

            tasks.add(task)
            self.all_tasks.add(task)
            task.add_done_callback(tasks.discard)

        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)

        return
    

    async def crawl(self):
        await self.crawl_page_async()

        return self.page_data

async def crawl_site_async(base_url, max_concurrency=1, max_page=10):
    async with AsyncCrawler(base_url, max_concurrency=max_concurrency, max_page=max_page) as crawler:
        return await crawler.crawl()
