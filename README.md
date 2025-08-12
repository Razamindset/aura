# Aura

Aura is a search Engine written in python

<div>
<img src="./image.png" style="margin:auto">
</div>

## Setup

Follow these steps to set up your development environment.

### 1. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

**Note:** You will need to create a `requirements.txt` file first. You can generate it using:
`pip freeze > requirements.txt`

### 3. Download NLTK Data

NLTK requires specific data packages for tokenization and stemming. Run the following commands:

```bash
python3 -c "import nltk; nltk.download('punkt')"
python3 -c "import nltk; nltk.download('punkt_tab')"
```

## Usage

Use the `run.py` script to manage different aspects of the project.

### 1. Crawl and Index Data

This command starts the web crawler, which will automatically trigger the indexer periodically.

```bash
python run.py crawl
```

**Important:** If you are running this for the first time or after making changes to how data is processed (e.g., stemming), ensure you delete any old data files before crawling:

```bash
rm files/crawled_data.jsonl files/inverted_index.json files/documents.json
```

### 2. Run the Web Server

This command starts the Flask web server, allowing you to interact with the search engine via a web interface.

```bash
python run.py web
```

---

### Crawling

Seeds are used as a string point. Any url that is found is appended to a queue. With that we have random jumps after 5 seconds so the results can have some variety. We skip all files and only consider simple site data for now. We see the robots.txt to respect the sites rules. All the crawled data is saved in a jsonl file.

### Indexing

A simple reverse index for words is built along with icon, title, desc info for each url.

### Searcher

Simple TF-IDF Search

```python
idf = math.log(total_documents / (1 + num_docs_with_word))

# Go through the list of [doc_id, term_frequency] for the word
for doc_id_str, tf in inverted_index[word]:
    scores[str(doc_id_str)] += tf * idf
```

### Stemming

Stem the words while crawling and searching for better results. Like throwing, throwed -> throw

### Website

The front end is pretty much vibe coded as there isn't much right now.

### Note

The crawler indexer and everything is under heavy development. So stuff can change very rapidly

### Future Plans

I donot have a clear plan. For now i will improve the page indexing and crawling. Add some structure to the search results potenitally adding more info like images yt links etc. Machine learning seems like a nice experiment but only time will tell what we do.
