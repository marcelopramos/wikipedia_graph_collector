import time
from config import REQUEST_SLEEP
from article import random_article
from article import links_by_article
from article import categories_by_article
from article import links_and_categories_batch
from article import extract_pages
from storage import save_json
import os
import json
from collections import deque

CHECKPOINT_FILE = "data/expanded/checkpoint.json"

def collect_random_articles(n=100, start=0):
    seeds = []

    for i in range(start, start + n):
        data = random_article()
        title = data["query"]["random"][0]["title"]

        links = links_by_article(title)
        categories = categories_by_article(title)

        safe = title.replace(" ", "_").replace("/", "_")

        save_json(data, f"data/raw/{i}_{safe}_article.json")
        save_json(links, f"data/raw/{i}_{safe}_links.json")
        save_json(categories, f"data/raw/{i}_{safe}_categories.json")

        seeds.append(title)

        print(f"[{i}] {title}")

        time.sleep(REQUEST_SLEEP)

    return seeds
