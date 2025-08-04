import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def extract_links(soup: BeautifulSoup, base_url):
    links = []
    for a in soup.find_all("a", href=True):

        href = a["href"]

        # We wanna skip these ones
        if href.startswith("#") or href.startswith("javascript"):
            continue

        absolute_url = urljoin(base_url, href)
        
        links.append(absolute_url)
    
    return links

def extract_words(soup: BeautifulSoup) -> list[str]:
    raw_text = soup.get_text(separator=" ")
    clean_text = re.sub(r"[^a-zA-Z0-9\s]", "", raw_text)
    clean_text = clean_text.lower()
    words = clean_text.split()
    return words

def crawl_page(url: str)-> dict:
    try:
        response  = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f"Cannot fetch url: {e}")
        return None    
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.title.string if soup.title else ""
    links = extract_links(soup, url)
    words = extract_words(soup)
    
    
    return {
        "url": url,
        "title":title,
        "links": links,
        "words": words,
    }

print(crawl_page("https://www.wikipedia.org/"))