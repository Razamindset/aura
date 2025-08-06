import json
from collections import defaultdict
import hashlib
import os

INDEX_PATH = "index.json"
index = None

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    index = json.load(f)

def search(query: str):
    words = query.lower().split()
    scores = defaultdict(int)

    for word in words:
        if word in index:
            for url, freq in index[word].items():
                scores[url] += freq  # Higher freq = more relevant

    ranked = sorted(scores.items(),  key=lambda x: x[1], reverse=True)

    results = []
    # Loop over the results and add title and description for each page
    for url, score in ranked:
        filename = hashlib.md5(url.encode('utf-8')).hexdigest() + ".json"
        file_path = os.path.join("output", filename)

        with open(file_path, "r", encoding="utf-8") as f:
            file = json.load(f)

            results.append({
                'title': file['title'],
                'url': url,
                'description': file['description'],
                'icon_url': file['favicon']
            })

    return results
