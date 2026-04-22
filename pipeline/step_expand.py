from expander import expand_from_articles_batch
import os
import sys

def load_seed_titles(folder="data/raw"):
    titles = set()

    for f in os.listdir(folder):
        if f.endswith("_article.json"):
            parts = f.split("_", 1)
            if len(parts) < 2:
                continue

            title_part = parts[1].replace("_article.json", "")
            title = title_part.replace("_", " ")

            titles.add(title)

    return list(titles)

if __name__ == "__main__":
    seed_titles = load_seed_titles()

    max_processed = 100_000

    if len(sys.argv) > 1:
        max_processed = int(sys.argv[1])

    expand_from_articles_batch(seed_titles, max_processed=max_processed, batch_size=50)
