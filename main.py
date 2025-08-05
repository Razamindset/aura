from flask import Flask, render_template, request, jsonify
from src.searcher import search as search_query

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get('query')
    results = search_query(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)