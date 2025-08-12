from .constants import SEEDS, CRAWLER_STATE_FILE, FILES_DIRECTORY, CRAWLED_DATA_FILE, FILE_EXTENSIONS, LANGUAGE_CODES, STOP_WORDS
from collections import deque, Counter
import os
import json
from urllib.parse import urlparse, urljoin
import urllib.robotparser
import random
import time
import requests
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from .indexer import Indexer

class Crawler():
    def __init__(self, seed_urls: list = SEEDS, save_state_every = 20, domain_cooldown_s = 5 , jump_every = 20, index_every_n_crawls = 100):

        # Configration
        self.seed_urls = seed_urls
        self.state_file = CRAWLER_STATE_FILE
        self.folder_name = FILES_DIRECTORY
        self.crawled_data_file = CRAWLED_DATA_FILE
        self.save_state_every = save_state_every
        self.domain_cooldown_s = domain_cooldown_s
        self.jump_every = jump_every
        self.user_agent = "AuraCrawler"
        self.index_every_n_crawls = index_every_n_crawls

        # NLP Tools
        self.stemmer = PorterStemmer()

        # State
        self.queue = deque()
        self.visited = set()
        self.all_seen_urls = set()
        self.crawled_times = {}
        self.crawl_count = 0

        # Caches
        self.robots_parsers = {}

        # Folders and files
        self._load_state()

    def _load_seeds(self):
        self.queue.extend(self.seed_urls)
        self.all_seen_urls.update(self.seed_urls)
        print("Loaded: Starting from new seeds")
    
    def _load_state(self):
        os.makedirs(self.folder_name, exist_ok=True)

        self.path = os.path.join(self.folder_name, self.state_file)

        if os.path.exists(self.path):
            try:
                with open(self.path, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                    self.visited = set(state.get('visited', []))
                    self.all_seen_urls = set(state.get('all_seen_urls', []))
                    self.queue = deque(state.get('queue', []))
                    self.crawl_count = state.get('crawl_count', 0)
                    print("Success: Recovered Crawler State")
            except json.JSONDecodeError:
                print("Warning: State file is empty or corrupted. Starting with a fresh state.")
                self._load_seeds()
        else:
            self._load_seeds()

    def _save_state(self):
        state = {
            "visited": list(self.visited),
            "queue": list(self.queue),
            "all_seen_urls": list(self.all_seen_urls),
            "crawl_count": self.crawl_count
        }

        try:
            file_path = os.path.join(self.folder_name, self.state_file)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(state, f)
            print("Success: Crawler state Saved successfully")

        except Exception as e:
            print(f"Error: Saving Crawler State {e}")

    def _can_fetch(self, url) -> bool:
        full_domain = urlparse(url).scheme + "://" + urlparse(url).netloc

        if full_domain not in self.robots_parsers:
            robots_url = full_domain + "/robots.txt"
            
            rp = urllib.robotparser.RobotFileParser()

            try:
                rp.set_url(robots_url)
                rp.read()
            except Exception as e: 
                rp = None
                print(e)
            
            self.robots_parsers[full_domain] = rp
        
        rp = self.robots_parsers.get(full_domain)
        
        if rp is None:
            return True
        
        return rp.can_fetch(self.user_agent, url)

    def _save_data(self, page_data: dict):
        os.makedirs(self.folder_name, exist_ok=True)        

        file_path = os.path.join(self.folder_name, self.crawled_data_file)

        with open(file_path, "a", encoding="utf-8") as f:
            json_string = json.dumps(page_data, ensure_ascii=False)
            f.write(json_string + "\n")

    def _handle_cooldown(self, domain, url) -> bool:
        current_time = time.time()
        last_crawled_time = self.crawled_times.get(domain, 0)

        if current_time - last_crawled_time < self.domain_cooldown_s:
            print(f"Skipping: {domain} for cooldown: Re-queueing {url}")
            self.queue.append(url)
            return True
        
        return False

    def _extract_words(self, soup: BeautifulSoup) -> dict:
        # Remove script, style, nav, header, and footer elements
        for element in soup(["script", "style", "nav", "header", "footer"]):
            element.decompose()

        # Get text from the main content, or body, or the whole page
        main_content = soup.find("main")
        if main_content:
            raw_text = main_content.get_text(separator=" ")
        elif soup.body:
            raw_text = soup.body.get_text(separator=" ")
        else:
            raw_text = soup.get_text(separator=" ")

        words = word_tokenize(raw_text)
        stemmed_words = [self.stemmer.stem(word.lower()) for word in words]

        # Clean the words before returning
        filtered = [
            word for word in stemmed_words
            if word.isalpha() and word not in STOP_WORDS and len(word) >= 3
        ]
        return dict(Counter(filtered))

    def _extract_links(self, soup: BeautifulSoup, base_url):
        links = []
        for a in soup.find_all("a", href=True):

            href = a["href"]

            # We wanna skip these ones
            if href.startswith("#") or href.startswith("javascript"):
                continue

            absolute_url = urljoin(base_url, href)

            links.append(absolute_url)

        return links

    def _crawl_page(self, url):
        try:
            response  = requests.get(url, timeout=5, headers={ 'User-Agent': self.user_agent})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Cannot fetch url: {e}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else ""

        description = ""
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag and 'content' in meta_tag.attrs:
            description = meta_tag['content']
            
        favicon = ""
        icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        if icon_link and 'href' in icon_link.attrs:
            favicon = urljoin(url, icon_link['href'])
            
        links = self._extract_links(soup, url)
        words_freq = self._extract_words(soup)

        return {
            "url": url,
            "title": title,
            "favicon": favicon,
            "description": description,
            "links": links,
            "words_freq": words_freq,
        }

    def _get_next_url(self):
        if not self.queue:
            return None
        
        if self.crawl_count > 0 and self.crawl_count % self.jump_every == 0:
            idx = random.randrange(len(self.queue))
            url = self.queue[idx]
            del self.queue[idx]
        
        else:
            url = self.queue.popleft()
        
        return url

    def run(self):
        while self.queue:
            url = self._get_next_url()

            if url is None or url in self.visited:
                continue

            domain = urlparse(url).netloc

            if self._handle_cooldown(domain, url):
                continue
            
            if not self._can_fetch(url):
                print(f"Skipping: Cannot Fetch {url} by robots.txt")
                continue

            print(f"[{len(self.visited)+1}] Crawling: {url}")

            page_data = self._crawl_page(url)

            if not page_data:
                continue

            self._save_data(page_data)

            self.visited.add(url)

            self.crawl_count += 1

            self.crawled_times[domain] = time.time()

            # Add the newly discovered urls to the queue
            for link in page_data['links']:
            
                # skip images and pdf files etc.
                if any(link.lower().endswith(ext) for ext in  FILE_EXTENSIONS):
                    continue

                # Add a check to skip domains like ar.wikipedia.org which are likely not english
                parsed_url = urlparse(link)
                if parsed_url.hostname and parsed_url.hostname.split('.')[0] in LANGUAGE_CODES:
                    continue
            
                # This check mighst become slower as the list grows so we would need a set for this
                if link not in self.all_seen_urls:
                    self.all_seen_urls.add(link)
                    self.queue.append(link)
        
            if self.crawl_count % self.save_state_every == 0:
                self._save_state()

            if self.crawl_count % self.index_every_n_crawls == 0:
                print(f"Triggering indexer after {self.crawl_count} crawls...")
                indexer = Indexer()
                indexer.run()


            

if __name__ == "__main__":
    crawler = Crawler()
    crawler.run()
