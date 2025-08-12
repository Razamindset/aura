import argparse
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

def main():
    parser = argparse.ArgumentParser(description="Aura search Engine")
    parser.add_argument("command", choices=["crawl", "web"])

    args = parser.parse_args()

    if args.command == "crawl":
        print("Running: Crawler")
        from src.crawler import Crawler
        crawler = Crawler()
        crawler.run()
        print("Crawling Completed")

    elif args.command == "web":
        print("Running: Web Server")
        from src.server import app
        app.run(debug=True)
        print("Server stopped")

if __name__ == "__main__":
    main()