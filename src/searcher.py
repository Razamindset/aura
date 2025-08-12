import json
import math
from collections import defaultdict
import os
from .constants import DOCS_FILE, REVERSE_INDEX_FILE, FILES_DIRECTORY
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

class Searcher:
    def __init__(self):
        self.documents = None
        self.inverted_index = None
        self.total_documents = 0
        self.stemmer = PorterStemmer()
        self._load_index()

    def _load_index(self):
        """Loads the documents and inverted index from JSON files into memory."""
        print("Loading search index...")
        try:
            with open(os.path.join(FILES_DIRECTORY, DOCS_FILE), "r", encoding="utf-8") as f:
                self.documents = json.load(f)
            
            with open(os.path.join(FILES_DIRECTORY, REVERSE_INDEX_FILE), "r", encoding="utf-8") as f:
                self.inverted_index = json.load(f)
                
            self.total_documents = len(self.documents)
            print(f"Index loaded successfully. {self.total_documents} documents.")
            
        except FileNotFoundError:
            print("Error: Index files not found. Please run the indexer first.")
            self.documents = {}
            self.inverted_index = {}
        except json.JSONDecodeError:
            print("Error: Could not decode index files. They may be corrupted.")
            self.documents = {}
            self.inverted_index = {}

    def search(self, query: str):
        """
        Performs a search using the TF-IDF algorithm.
        1. Calculates scores for documents based on the query.
        2. Ranks documents by score.
        3. Returns the top results with their details.
        """
        if not self.documents or not self.inverted_index:
            print("Search index is not loaded.")
            return []

        query_words = query.lower().split()

        query_tokens = word_tokenize(query.lower())

        query_words = [self.stemmer.stem(word) for word in query_tokens]
        
        scores = defaultdict(float)
        
        for word in query_words:
            if word in self.inverted_index:
                num_docs_with_word = len(self.inverted_index[word])
                idf = math.log(self.total_documents / (1 + num_docs_with_word))
                
                for doc_id_str, tf in self.inverted_index[word]:
                    scores[str(doc_id_str)] += tf * idf

        ranked_doc_ids = sorted(scores.keys(), key=lambda doc_id: scores[doc_id], reverse=True)
        
        results = []
        for doc_id in ranked_doc_ids:
            doc_details = self.documents.get(doc_id)
            if doc_details:
                results.append({
                    'title': doc_details.get('title', 'No Title'),
                    'url': doc_details.get('url'),
                    'description': doc_details.get('description'),
                    'icon_url': doc_details.get('favicon')
                })
                
        return results

if __name__ == "__main__":
    searcher = Searcher()
    
    while True:
        query = input("Enter search query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        
        results = searcher.search(query)
        
        if results:
            print(f"Found {len(results)} results:")
            for i, result in enumerate(results[:10], 1): # Display top 10
                print(f"{i}. {result['title']} ({result['url']})")
        else:
            print("No results found.")
