import os
import json
from collections import defaultdict

def build_index(data_folder="output") -> dict:
    index = defaultdict(set)
    
    
    for filename in os.listdir(data_folder):
        if not filename.endswith(".json"):
            continue

        file_path = os.path.join(data_folder, filename)
        
        with open(file_path, 'r', encoding="utf-8") as f:
            page = json.load(f)
        
        url = page["url"]
        words = page["words"]
        
        for word in words:
            index[word].add(url)
    
    final_index = {word: list(urls) for word, urls in index.items()}
    
    return final_index

def save_index(index: dict, filepath="index.json"):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

index = build_index("output")
save_index(index)