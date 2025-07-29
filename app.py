from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    articles = scrape_the_verge() #defining articles variable
    return render_template("index.html", articles=articles)

def scrape_the_verge():
    url = "https://www.theverge.com/rss/index.xml"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    print("Status code:", response.status_code)
    print("Raw response snippet:\n", response.text[:500])

    soup = BeautifulSoup(response.content, "xml")
    articles = []

    for entry in soup.find_all("entry"):
        title = entry.title.text
        link = entry.link["href"]
        updated = entry.updated.text

        articles.append({
            "title": title,
            "url": link,
            "date": updated
        })

    print("Articles found:", len(articles))
    return articles

if __name__ == "__main__":
    app.run(debug=True)