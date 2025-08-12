from flask import Flask, render_template, request, jsonify
from src.searcher import Searcher

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Create a single instance of the Searcher
searcher = Searcher()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get('query')
    results = searcher.search(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)