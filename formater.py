def format_page(categories_json, links_json):
    pages_cat = categories_json["query"]["pages"]
    pages_links = links_json["query"]["pages"]

    page_id = next(iter(pages_cat.keys()))

    page_cat = pages_cat[page_id]
    page_links = pages_links.get(page_id, {})

    title = page_cat.get("title")

    categories = [
        c["title"].replace("Category:", "")
        for c in page_cat.get("categories", [])
    ]

    links = [
        l["title"]
        for l in page_links.get("links", [])
    ]

    return {
        "pageid": int(page_id),
        "title": title,
        "categories": categories,
        "links": links
    }