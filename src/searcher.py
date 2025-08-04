import json
from collections import defaultdict

def load_index(filepath="index.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
    
def search(query: str, index: dict):
    words = query.lower().split()
    scores = defaultdict(int)
    
    for word in words:
        if word in index:
            for url, freq in index[word].items():
                scores[url] += freq  # Higher freq = more relevant
    
    ranked = sorted(scores.items(),  key=lambda x: x[1], reverse=True)

    return ranked

index = load_index("index.json")

while True:
    query = input("Search Aura: ").strip()
    if query.lower() in ["exit", "quit"]:
        break

    matches = search("python search", index)

    if matches:
        for url, score in matches:
            print(f"{url}  (score: {score})")
    else:
        print("No results.")
