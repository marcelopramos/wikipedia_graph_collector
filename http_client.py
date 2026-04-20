import requests
from config import API_URL, WIKI_USER_AGENT

if not WIKI_USER_AGENT:
    raise RuntimeError(
        "WIKI_USER_AGENT is not defined. "
        "Set the environment variable or .env file before running. "
        "Format: WikipediGraphIdeologicClusters/<version> (<email>)"
    )

HEADERS = {
    "User-Agent": WIKI_USER_AGENT
}

def get(params):
    r = requests.get(API_URL, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()