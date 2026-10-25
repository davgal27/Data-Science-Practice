
import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime

NEWEST_URL = "https://news.ycombinator.com/newest"
POPULAR_URL = "https://news.ycombinator.com/"

SAMPLE_SIZE = 15
timestamp = datetime.now().astimezone()

for url, filename in [(NEWEST_URL, "newest.txt"),(POPULAR_URL, "popular.txt")]:

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    articles = soup.select("tr.athing") # tr = table row, hackernews calls rows: athing
    sampled = random.sample(articles, SAMPLE_SIZE)

    with open(filename, "a", encoding="utf-8") as file:

        file.write(f"\nTimestamp: {timestamp}\n")

        for article in sampled:
            # . before class names, no . before HTML tags 

            article_id = article.get("id")

            title = article.select_one(".titleline a").get_text(strip = True)

            details = article.find_next_sibling("tr") # next table row
            score = details.select_one(".score")
            # convert to an int for easy analysis. Split()[0] takes the first word from eg. 10 points (so takes 10)
            points = int(score.get_text().split()[0]) if score else None 

            comments = 0
            for link in details.select("a"):
                text = link.get_text(strip = True)

                if "comment" in text:
                    comments = int(text.split()[0])
                    break

            file.write(f"{article_id} | {title} | {points} | {comments}\n")

        file.write("\n===================================================================================\n")

    print(f"Saved {len(sampled)} articles to {filename}")
