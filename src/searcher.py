import json

def load_index(filepath="index.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
    
def search(query: str, index: dict):
    words = query.lower().split()
    results = set()
    
    for word in words:
        if word in index:
            results.update(index[word])  # Union of all matches

    return list(results)


index = load_index("index.json")

while True:
    query = input("Search Aura: ").strip()
    if query.lower() in ["exit", "quit"]:
        break

    matches = search(query, index)
    if matches:
        print(f"\nFound {len(matches)} results:")
        for url in matches:
            print(f" - {url}")
    else:
        print("No results found.\n")
