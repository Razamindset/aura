import os
import json
from collections import defaultdict
from .constants import REVERSE_INDEX_FILE, FILES_DIRECTORY, CRAWLED_DATA_FILE, DOCS_FILE

class Indexer():
    def __init__(self):
        pass

    def _save_index(self, index):
        if index is None:
            return
        
        index_filepath = os.path.join(FILES_DIRECTORY, REVERSE_INDEX_FILE)
        
        # Save the inverted index dictionary
        with open(index_filepath, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        print(f"-> Successfully saved inverted index with {len(index)} words to {index_filepath}")
            
    def _save_docs(self, docs):
        if docs is None:
            return
        
        docs_filepath = os.path.join(FILES_DIRECTORY, DOCS_FILE)

        with open(docs_filepath, 'w', encoding='utf-8') as f:
            json.dump(docs, f, indent=2, ensure_ascii=False)

        print(f"-> Successfully saved {len(docs)} documents to {docs_filepath}")

    def _build_index(self):
        documents = {}
        inverted_index = defaultdict(list)
        doc_id = 0
        
        file_path = os.path.join(FILES_DIRECTORY, CRAWLED_DATA_FILE)
        
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

    def run(self):
        docs, index = self._build_index()
        self._save_docs(docs)
        self._save_index(index)
        pass

if __name__ == "__main__":
    indexer = Indexer()
    indexer.run()