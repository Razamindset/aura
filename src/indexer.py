import os
import json
from collections import defaultdict

def build_index(data_folder="output") -> dict:    
    documents = {}
    inverted_index = defaultdict(list)
    doc_id = 0
    
    file_path = os.path.join(data_folder, "crawled_data.jsonl")
    
    print(f"Reading data from {file_path}...")
        
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in f:
            try:
                page = json.loads(line)
            except Exception as e:
                print(e)
                continue
            
            # Will be used for desc etc
            documents[doc_id] = {
                "url": page.get("url", ""),
                "title": page.get("title", "No Title"),
                "description": page.get("description", ""),
                "favicon": page.get("favicon", "")
            }
            
            # Build the reversed index
            words_freq = page.get("words_freq", {})
            for word, freq in words_freq.items():
                inverted_index[word].append([doc_id, freq])
            
            doc_id += 1
    
    print(f"processed {len(documents)}")
    
    return documents, inverted_index
            

def save_index(documents, inverted_index, output_dir="output"):
    if documents is None or inverted_index is None:
        print("Index building failed. Nothing to save.")
        return
 
    # Ensure the output directory exists.
    os.makedirs(output_dir, exist_ok=True)
 
    # Define file paths
    docs_filepath = os.path.join(output_dir, "documents.json")
    index_filepath = os.path.join(output_dir, "inverted_index.json")
   
    # Save the documents dictionary
    with open(docs_filepath, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)

    print(f"-> Successfully saved {len(documents)} documents to {docs_filepath}")

    # Save the inverted index dictionary
    with open(index_filepath, "w", encoding="utf-8") as f:
        json.dump(inverted_index, f, indent=2, ensure_ascii=False)

    print(f"-> Successfully saved inverted index with {len(inverted_index)} words to {index_filepath}")
    

if __name__ == "__main__":
    docs, index = build_index("output")
    save_index(docs, index)