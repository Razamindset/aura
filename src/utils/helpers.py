import os
import hashlib
import json
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from collections import Counter

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

def save_page_data(page_data: dict, output_directory: str = "output"):
    os.makedirs(output_directory, exist_ok=True)
    
    url = page_data['url']
    filename = hashlib.md5(url.encode('utf-8')).hexdigest() + ".json"

    file_path = os.path.join(output_directory, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(page_data, f, indent=2, ensure_ascii=False)