import requests
from bs4 import BeautifulSoup
from utils.helpers import save_page_data, extract_links, extract_words
import random
from urllib.parse import urljoin, urlparse
import urllib.robotparser
import time
import os
from utils.constants import LANGUAGE_CODES, FILE_EXTENSIONS, SEEDS

robots_parsers = {}

def can_fetch_url(url: str, user_agent="*") -> bool:
    full_domain = urlparse(url).scheme + "://" + urlparse(url).netloc

    if full_domain not in robots_parsers:
        robots_url = full_domain + "/robots.txt"
        
        rp = urllib.robotparser.RobotFileParser()
        
        try:
            rp.set_url(robots_url)
            rp.read()
        except Exception as e: 
            rp = None
            print(e)
        
        robots_parsers[full_domain] = rp
    
    rp = robots_parsers.get(full_domain)
    
    if rp is None:
        return True
    
    return rp.can_fetch(user_agent, url)

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
    
    

def crawl_many(seed_urls, max_pages: int = 10, jump_every=5, domain_cooldown_s: int = 5):
    visited = set()
    queue = list(seed_urls)
    all_seen_urls = set(queue)
    crawl_count = 0
    
    # Track the last time a domain was crawled
    domain_last_crawled = {}

    output_file = "output/crawled_data.jsonl"
    if os.path.exists(output_file):
        os.remove(output_file)
        print(f"Removed old data file: {output_file}")

    while queue and len(visited) < max_pages:

        if crawl_count > 0 and crawl_count % jump_every == 0:
            unseen = list(all_seen_urls - visited)
            if unseen:
                url = random.choice(unseen)
                print(f"\n🌐 Jumping randomly to: {url}\n")
            else:
                url = queue.pop(0)
        else:
            url = queue.pop(0)

        if url in visited:
            continue
        
        domain = urlparse(url).netloc
        current_time = time.time()
        last_crawled_time = domain_last_crawled.get(domain, 0)

        if current_time - last_crawled_time < domain_cooldown_s:
            print(f"Cooldown for {domain}. Re-queueing {url}")
            # If on cooldown put it at the end of the queue
            queue.append(url)
            continue

        print(f"[{len(visited)+1}] Crawling: {url}")
        
        if not can_fetch_url(url, user_agent="MyCrawler"):
            print("cannot fetch url by robots.txt")
            continue
        
        page = crawl_page(url)

        if not page:
            continue

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
            
            if link not in all_seen_urls:
                queue.append(link)
                all_seen_urls.add(link)

if __name__ == "__main__":
  
    crawl_many(seed_urls=SEEDS, max_pages=1000, domain_cooldown_s=3)
