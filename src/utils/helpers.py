import os
import hashlib
import json
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
from collections import Counter
import urllib.robotparser


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

STOP_WORDS = set([
    "a", "an", "the", "and", "or", "but", "if", "while", "is", "are", "was", "were", "in", "on", "for", "to", "of",
    "at", "by", "with", "as", "it", "this", "that", "these", "those", "i", "you", "he", "she", "they", "we", "me",
    "my", "your", "our", "their", "his", "her", "its", "be", "been", "being", "do", "does", "did", "will", "would",
    "can", "could", "should", "shall", "not"
])

def extract_words(soup: BeautifulSoup) -> dict:
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

    clean_text = re.sub(r"[^a-zA-Z0-9\s]", "", raw_text)
    clean_text = clean_text.lower()
    words = clean_text.split()

    # Clean the words before returning
    filtered = [
        word for word in words
        if word not in STOP_WORDS and len(word) >= 3
    ]
    return dict(Counter(filtered))


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

def save_page_data(page_data: dict, files_directory: str = "files"):
    os.makedirs(files_directory, exist_ok=True)
        
    file_name = "crawled_data.jsonl"

    file_path = os.path.join(files_directory, file_name)

    with open(file_path, "a", encoding="utf-8") as f:
        # Convert the dictionary to a compact JSON string.
        json_string = json.dumps(page_data, ensure_ascii=False)
        # Write the string followed by a newline character.
        f.write(json_string + "\n")
