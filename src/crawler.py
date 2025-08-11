import requests
from bs4 import BeautifulSoup
from utils.helpers import save_page_data, extract_links, extract_words, can_fetch_url
import random
from urllib.parse import urljoin, urlparse
import time
import os
from utils.constants import LANGUAGE_CODES, FILE_EXTENSIONS, SEEDS, CRAWLER_STATE_FILE
import json

file_path = os.path.join("files", CRAWLER_STATE_FILE)

# Ensure the directory exists
os.makedirs(os.path.dirname(file_path), exist_ok=True)

def crawl_page(url: str)-> dict:
    try:
        response  = requests.get(url, timeout=5, headers={ 'User-Agent': "MyCrawler"})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Cannot fetch url: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Check for english language
    html_tag = soup.find('html')
    if html_tag and html_tag.get('lang') and not html_tag.get('lang').lower().startswith('en'):
        print(f"Skipping non-English page: {url}")
        return None

    title = soup.title.string if soup.title else ""

    description = ""
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag and 'content' in meta_tag.attrs:
        description = meta_tag['content']
        
    favicon = ""
    icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
    if icon_link and 'href' in icon_link.attrs:
        favicon = urljoin(url, icon_link['href'])
        
    links = extract_links(soup, url)
    words_freq = extract_words(soup)

    return {
        "url": url,
        "title": title,
        "favicon": favicon,
        "description": description,
        "links": links,
        "words_freq": words_freq,
    }
    

def save_crawler_state(visited, queue):
    state = {
        "visited": list(visited),
        "queue": list(queue),
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(state, f)
    
    print("Crawler state Saved successfully")

def load_crawler_state():
    """Loads the crawler state from a JSON file. If not found, initializes with seeds."""
    if not os.path.exists(file_path):
        print("No crawler state file found")
        return set(), SEEDS
    
    with open(file_path, 'r', encoding='utf-8') as f:
        state = json.load(f)
        return set(state['visited']), list(state['queue'])


def crawl_many(max_pages: int = 10, jump_every=5, domain_cooldown_s: int = 5, save_state_every=10):

    visited, queue = load_crawler_state()

    crawl_count = 0
    
    # Track the last time a domain was crawled
    domain_last_crawled = {}

    while queue and len(visited) < max_pages:

        if crawl_count > 0 and crawl_count % jump_every == 0:
            url = random.choice(queue)
        else:
            url = queue.pop(0)

        # Already done 
        if url in visited:
            continue
        
        # Check cooldown for domains
        domain = urlparse(url).netloc
        current_time = time.time()
        last_crawled_time = domain_last_crawled.get(domain, 0)

        if current_time - last_crawled_time < domain_cooldown_s:
            print(f"Cooldown for {domain}. Re-queueing {url}")
            # If on cooldown put it at the end of the queue
            queue.append(url)
            continue

        # Loggs 
        print(f"[{len(visited)+1}] Crawling: {url}")
        
        if not can_fetch_url(url, user_agent="MyCrawler"):
            print("cannot fetch url by robots.txt")
            continue
        
        # Do the actual stuff
        page = crawl_page(url)

        if not page:
            continue

        # Save the data
        save_page_data(page)
        visited.add(url)
        crawl_count += 1
        
        # Update the last crawled time for this domains
        domain_last_crawled[domain] = time.time()

        # Add new links to queue and all_seen_urls
        for link in page['links']:
            
            # skip images and pdf files etc.
            if any(link.lower().endswith(ext) for ext in  FILE_EXTENSIONS):
                continue

            # Add a check to skip domains like ar.wikipedia.org which are likely not english
            parsed_url = urlparse(link)
            if parsed_url.hostname and parsed_url.hostname.split('.')[0] in LANGUAGE_CODES:
                continue
            
            if link not in queue:
                queue.append(link)
        
        if crawl_count % save_state_every == 0:
            save_crawler_state(visited, queue)

if __name__ == "__main__":
    # The crawler will save it state every 10 urls so even if the crawler is seitched off it will start again fromt he same spot.   
    crawl_many(max_pages=100000, domain_cooldown_s=3, save_state_every=5)
