from urllib.parse import urlparse, urljoin
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
    parsed_html = BeautifulSoup(html, "html.parser")

    main = parsed_html.find("main")

    if main:
        inner_p = main.find("p")
        if inner_p:
            return inner_p.get_text().strip()

    outer_p = parsed_html.find("p")
    if outer_p:
        return outer_p.get_text().strip()
    
    return ""


def get_urls_from_html(html, base_url):
    parsed_html = BeautifulSoup(html, "html.parser")

    a_tags = parsed_html.find_all("a")

    urls = []
    for a in a_tags:
        url = a.get("href")
        if url:
            urls.append(urljoin(base_url, url))

    return urls


def get_images_from_html(html, base_url):
    parsed_html = BeautifulSoup(html, "html.parser")

    img_tags = parsed_html.find_all("img")

    imgs = []
    for img in img_tags:
        src = img.get("src")
        if src:
            imgs.append(urljoin(base_url, src))

    return imgs
