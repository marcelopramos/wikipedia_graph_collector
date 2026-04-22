from http_client import get

ARTICLE_NAMESPACE_ID = 0

def random_article():
    return get({
        "action": "query",
        "list": "random",
        "rnlimit": 1,
        "rnnamespace": ARTICLE_NAMESPACE_ID,
        "format": "json"
    })

def links_by_article(title):
    return get({
        "action": "query",
        "prop": "links",
        "titles": title,
        "pllimit": "max",
        "plnamespace": ARTICLE_NAMESPACE_ID,
        "format": "json"
    })

def categories_by_article(title):
    return get({
        "action": "query",
        "prop": "categories",
        "titles": title,
        "cllimit": "max",
        "format": "json"
    })

def extract_pages(data):
    return data.get("query", {}).get("pages", {})

def get_links_from_pages(pages):
    links = []

    for page_id in pages:
        page = pages[page_id]

        source = page.get("title")
        if not source:
            continue

        for link in page.get("links", []):
            target = link.get("title")
            if target:
                links.append((source, target))

    return links

def get_categories_from_pages(pages):
    categories = {}

    for page_id in pages:
        page = pages[page_id]
        title = page.get("title")

        if not title:
            continue

        cats = page.get("categories", [])
        categories[title] = [c["title"] for c in cats if "title" in c]

    return categories

def links_and_categories_batch(titles):
        if not titles:
            return {}

        params = {
            "action": "query",
            "prop": "links|categories",
            "titles": "|".join(titles),
            "pllimit": "max",
            "cllimit": "max",
            "format": "json"
        }

        result = get(params)

        pages = result.get("query", {}).get("pages", {})

        while "continue" in result:
            result = get({**params, **result["continue"]})

            new_pages = result.get("query", {}).get("pages", {})

            for pid, page in new_pages.items():
                if pid in pages:
                    pages[pid].setdefault("links", [])
                    pages[pid].setdefault("categories", [])

                    pages[pid]["links"] += page.get("links", [])
                    pages[pid]["categories"] += page.get("categories", [])

        return {"query": {"pages": pages}}
