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