import json
import math
from collections import defaultdict
import os

# --- Configuration ---
INDEX_DIR = "output"
DOCUMENTS_PATH = os.path.join(INDEX_DIR, "documents.json")
INVERTED_INDEX_PATH = os.path.join(INDEX_DIR, "inverted_index.json")

# --- Global Variables ---
documents = None
inverted_index = None
total_documents = 0

# --- Load the index files ---
def load_index():
    """Loads the documents and inverted index from JSON files into memory."""
    global documents, inverted_index, total_documents
    
    print("Loading search index...")
    try:
        with open(DOCUMENTS_PATH, "r", encoding="utf-8") as f:
            documents = json.load(f)
        
        with open(INVERTED_INDEX_PATH, "r", encoding="utf-8") as f:
            inverted_index = json.load(f)
            
        total_documents = len(documents)
        print(f"Index loaded successfully. {total_documents} documents.")
        
    except FileNotFoundError:
        print("Error: Index files not found. Please run the indexer first.")
        documents = {}
        inverted_index = {}
    except json.JSONDecodeError:
        print("Error: Could not decode index files. They may be corrupted.")
        documents = {}
        inverted_index = {}

# TF-IDF Search
def search(query: str):
    """
    Performs a search using the TF-IDF algorithm.
    1. Calculates scores for documents based on the query.
    2. Ranks documents by score.
    3. Returns the top results with their details.
    """
    if not documents or not inverted_index:
        print("Search index is not loaded.")
        return []

    query_words = query.lower().split()
    
    scores = defaultdict(float)
    
    for word in query_words:
        if word in inverted_index:
            num_docs_with_word = len(inverted_index[word])
            idf = math.log(total_documents / (1 + num_docs_with_word))
            
            # Go through the list of [doc_id, term_frequency] for the word
            for doc_id_str, tf in inverted_index[word]:
                scores[str(doc_id_str)] += tf * idf


    ranked_doc_ids = sorted(scores.keys(), key=lambda doc_id: scores[doc_id], reverse=True)
    
    results = []
    for doc_id in ranked_doc_ids:
        doc_details = documents.get(doc_id)
        if doc_details:
            results.append({
                'title': doc_details.get('title', 'No Title'),
                'url': doc_details.get('url'),
                'description': doc_details.get('description'),
                'icon_url': doc_details.get('favicon')
            })
            
    return results

load_index()