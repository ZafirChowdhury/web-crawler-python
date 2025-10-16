from urllib.parse import urlparse
from bs4 import BeautifulSoup

def normalize_url(url):
    parsed_url = urlparse(url)

    path = parsed_url.path

    while path.endswith("/"):
        path = path[:-1]

    return f"{parsed_url.netloc}{path}"

def get_h1_from_html(html):
    parsed_html = BeautifulSoup(html, "html.parser")

    h1 = parsed_html.find("h1")
    if h1:
        return h1.get_text().strip()
    
    return ""

def get_first_paragraph_from_html(html):
    pass
