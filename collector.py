import time
from config import REQUEST_SLEEP
from article import random_article
from article import links_by_article
from article import categories_by_article
from storage import save_json

def collect_random_articles(n=100):
    seeds = []

    for i in range(n):
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

def expand_from_articles(seed_titles, max_new=1000):
    visited = set(seed_titles)
    queue = list(seed_titles)

    i = 0

    while queue and i < max_new:
        title = queue.pop(0)

        links = links_by_article(title)
        categories = categories_by_article(title)

        safe = title.replace(" ", "_").replace("/", "_")

        save_json(links, f"data/expanded/{i}_{safe}_links.json")
        save_json(categories, f"data/expanded/{i}_{safe}_categories.json")

        pages = links.get("query", {}).get("pages", {})

        new_titles = []

        for page_id in pages:
            for link in pages[page_id].get("links", []):
                t = link.get("title")

                if t and t not in visited:
                    visited.add(t)
                    new_titles.append(t)

        queue.extend(new_titles)

        print(f"[{i}] {title} | new: {len(new_titles)}")

        i += 1
        time.sleep(REQUEST_SLEEP)