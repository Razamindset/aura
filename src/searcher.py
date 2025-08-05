import json
from collections import defaultdict

INDEX_PATH = "index.json"
index = None

def load_index():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def search(query: str):
    words = query.lower().split()
    scores = defaultdict(int)
    
    for word in words:
        if word in index:
            for url, freq in index[word].items():
                scores[url] += freq  # Higher freq = more relevant
    
    ranked = sorted(scores.items(),  key=lambda x: x[1], reverse=True)

    results = []
    for url, score in ranked:
        # In a real scenario, you'd fetch the title and description from a metadata store
        # For now, using dummy data
        results.append({
            'title': f'Search Result for {url}',
            'url': url,
            'description': f'This is a dummy description for {url} with a score of {score}.'
        })
    return results

index = load_index()