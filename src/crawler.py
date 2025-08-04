import requests
from bs4 import BeautifulSoup
from utils.helpers import save_page_data, extract_links, extract_words

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

def crawl_many(seed_url: str, max_pages: int = 10):
    visited = set()
    queue = [seed_url]
    
    while queue and len(visited) < max_pages:
        url = queue.pop()
        
        if url in visited:
            continue
        
        print(f"[{len(visited) + 1}] Crawling: {url}")
        page = crawl_page(url)
        
        if not page:
            continue
        
        save_page_data(page)
        visited.add(url)
        
        for link in page['links']:
            if link not in visited and link not in queue:
                queue.append(link)

crawl_many("https://en.wikipedia.org/", max_pages=10)