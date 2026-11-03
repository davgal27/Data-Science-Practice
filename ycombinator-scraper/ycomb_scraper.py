
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import json

NEWEST_URL = "https://news.ycombinator.com/newest"
POPULAR_URL = "https://news.ycombinator.com/"

PAGES = 5
timestamp = datetime.now().astimezone()

Path("raw").mkdir(exist_ok=True) # create raw folder if not there 

for url, filename in [(NEWEST_URL, "newest.txt"), (POPULAR_URL, "popular.txt")]:

    # Keep raw data
    raw_path = Path("raw") / f"{Path(filename).stem}.json"
    if raw_path.exists():
        with open(raw_path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)
    else:
        raw_data = []

    with open(filename, "a", encoding="utf-8") as file:

        file.write(f"\nTimestamp: {timestamp}\n")

        for page_number in range(1, PAGES + 1):
            page = requests.get(url, timeout=20)
            page.raise_for_status()
            soup = BeautifulSoup(page.content, "html.parser")

            # Keep the original HTML so we can extract other fields later.
            raw_data.append({
                "timestamp": timestamp.isoformat(),
                "page_number": page_number,
                "url": page.url,
                "html": page.text
            })

            articles = soup.select("tr.athing") # tr = table row, hackernews calls rows: athing

            for article in articles:
                # . before class names, no . before HTML tags
                article_id = article.get("id")

                title = article.select_one(".titleline a").get_text(strip=True)

                details = article.find_next_sibling("tr") # next table row
                score = details.select_one(".score")
                # convert to an int for easy analysis. Split()[0] takes the first word from eg. 10 points (so takes 10)
                points = int(score.get_text().split()[0]) if score else None

                comments = 0
                for link in details.select("a"):
                    text = link.get_text(strip=True)
                    if "comment" in text:
                        comments = int(text.split()[0])
                        break

                file.write(f"{article_id} | {title} | {points} | {comments} | {page_number}\n")

            # go to the next page using more 
            more = soup.select_one("a.morelink")
            if more :
                url = requests.compat.urljoin(page.url, more["href"])
            else: 
                break

        file.write("\n===================================================================================\n")

    # Save raw pages, including pages from previous runs.
    with open(raw_path, "w", encoding="utf-8") as file:
        json.dump(raw_data, file, ensure_ascii=False, indent=2)
