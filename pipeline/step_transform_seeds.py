import os
import json
from formater import format_page

RAW_DIR = "data/raw"
SEED_DIR = "data/seed"

os.makedirs(SEED_DIR, exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def process_seeds():
    files = os.listdir(RAW_DIR)

    # Collect pageids
    page_ids = set()

    for filename in files:
        if filename.endswith("_categories.json"):
            page_ids.add(
                filename.replace("_categories.json", "")
            )

    total = len(page_ids)

    for i, page_id in enumerate(page_ids, start=1):
        cat_file = os.path.join(
            RAW_DIR,
            f"{page_id}_categories.json"
        )

        links_file = os.path.join(
            RAW_DIR,
            f"{page_id}_links.json"
        )

        if not os.path.exists(links_file):
            print(f"[skip] Missing links for {page_id}")
            continue

        try:
            categories_json = load_json(cat_file)
            links_json = load_json(links_file)

            page = format_page(
                categories_json,
                links_json
            )

            out_file = os.path.join(
                SEED_DIR,
                f"{page_id}.json"
            )

            save_json(page, out_file)

        except Exception as e:
            print(f"[error] {page_id}: {e}")

        if i % 10 == 0:
            print(f"[progress] {i}/{total}")

    print("Done.")


if __name__ == "__main__":
    process_seeds()