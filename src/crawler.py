import requests
from bs4 import BeautifulSoup
from utils.helpers import save_page_data, extract_links, extract_words
import random

def crawl_page(url: str)-> dict:
    try:
        response  = requests.get(url, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f"Cannot fetch url: {e}")
        return None    
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for english language
    html_tag = soup.find('html')
    if html_tag and html_tag.get('lang') and not html_tag.get('lang').lower().startswith('en'):
        print(f"Skipping non-English page: {url}")
        return None
    
    title = soup.title.string if soup.title else ""
    links = extract_links(soup, url)
    words_freq = extract_words(soup)
    
    return {
        "url": url,
        "title":title,
        "links": links,
        "words_freq": words_freq,
    }

def crawl_many(seed_urls, max_pages: int = 10, jump_every=5):
    visited = set()
    queue = list(seed_urls)
    all_seen_urls = set(queue)
    crawl_count = 0
    
    while queue and len(visited) < max_pages:

        if crawl_count > 0 and crawl_count % jump_every == 0:

            unseen = list(all_seen_urls - visited)

            if unseen:
                url = random.choice(unseen)
                print(f"🌐 Jumping randomly to: {url}")

            else:
                url = queue.pop(0)

        else:
            url = queue.pop(0)

        if url in visited:
            continue

        print(f"[{len(visited)+1}] Crawling: {url}")
        page = crawl_page(url)

        if not page:
            continue

        save_page_data(page)
        visited.add(url)
        crawl_count += 1

        # Add new links to queue and all_seen_urls
        for link in page['links']:
            if link not in visited and link not in queue:
                queue.append(link)
                all_seen_urls.add(link)

seeds = [
    "https://en.wikipedia.org/wiki/Web_crawler",
    "https://www.python.org/",
    "https://google.com",
    "https://github.com",
    "https://github.com/Razamindset",
    "https://myportfolio-mu-coral.vercel.app/",
    "https://github.com/Ali-Raza764",
]

crawl_many(seed_urls=seeds, max_pages=10)