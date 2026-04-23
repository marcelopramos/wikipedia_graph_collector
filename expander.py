import random
import time
from collections import deque
from config import REQUEST_SLEEP
from storage import save_json
from article import links_and_categories_batch, extract_pages
import os
import json
from collections import deque
import re

INVALID_FILENAME_CHARS = r'[<>:"/\\|?*]'
CHECKPOINT_FILE = "data/expanded/checkpoint.json"
LINK_SAMPLE_PROB = 0.15
MAX_LINKS_PER_PAGE = 25
MAX_QUEUE_SIZE = 120_000

def save_checkpoint(i, visited, queue):
    os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)

    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {
                "i": i,
                "visited": list(visited),
                "queue": list(queue),
            },
            f
        )

def load_checkpoint():
    if not os.path.exists(CHECKPOINT_FILE):
        return None

    with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    return (
        data["i"],
        set(data["visited"]),
        deque(data["queue"])
    )

def sample_links(page):
    links = page.get("links", [])
    out = []

    for link in links:
        t = link.get("title")
        if not t:
            continue
        if ":" in t:
            continue
        if random.random() > LINK_SAMPLE_PROB:
            continue
        out.append(t)
        if len(out) >= MAX_LINKS_PER_PAGE:
            break

    return out

def enqueue(queue, visited, titles):
    for t in titles:
        if t not in visited:
            visited.add(t)
            queue.append(t)

    if len(queue) > MAX_QUEUE_SIZE:
        queue = deque(list(queue)[:MAX_QUEUE_SIZE])

    return queue

def sanitize_filename(title):
    title = title.replace(" ", "_")
    title = re.sub(INVALID_FILENAME_CHARS, "_", title)
    return title[:180]

def process_pages(pages, queue, visited, i):
    for page_id, page in pages.items():
        title = page.get("title")
        if not title:
            continue

        safe = sanitize_filename(title)

        try:
            save_json(
                page,
                f"data/expanded/{i}_{safe}_data.json"
            )
        except OSError:
            fallback = f"data/expanded/{i}_page.json"
            save_json(page, fallback)

        titles = sample_links(page)
        queue = enqueue(queue, visited, titles)

        i += 1

    return queue, i

def expand_from_articles_batch(seed_titles, max_processed=100_000, batch_size=50):
    loaded = load_checkpoint()

    if loaded:
        i, visited, queue = loaded
        visited = set(visited)
        queue = deque(queue)
    else:
        i = 0
        visited = set(seed_titles)
        queue = deque(seed_titles)

    start_global = time.time()

    while queue and i < max_processed:
        batch = []

        while queue and len(batch) < batch_size:
            batch.append(queue.popleft())

        start_batch = time.time()
        data = links_and_categories_batch(batch)
        batch_time = time.time() - start_batch

        pages = extract_pages(data)

        queue, i = process_pages(
            pages,
            queue,
            visited,
            i
        )

        if i % 50 == 0:
            save_checkpoint(i, list(visited), list(queue))

        elapsed = time.time() - start_global
        avg = elapsed / i if i > 0 else 0
        eta = (max_processed - i) * avg if avg > 0 else 0

        print(
            f"[progress] i={i} | batch={len(batch)} | "
            f"batch_time={batch_time:.2f}s | "
            f"queue={len(queue)} | "
            f"avg={avg:.3f}s/node | "
            f"ETA={eta/60:.1f} min"
        )

        time.sleep(REQUEST_SLEEP)

    save_checkpoint(i, list(visited), list(queue))
    return visited
