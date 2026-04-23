import time
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

TIMEOUT = 30
MAX_RETRIES = 8
INITIAL_BACKOFF = 2

logging.basicConfig(
    filename="network_errors.log",
    level=logging.WARNING,
    format="%(asctime)s %(levelname)s %(message)s"
)

session = requests.Session()

retry_strategy = Retry(
    total=MAX_RETRIES,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)
session.mount("http://", adapter)

def get(params):
    backoff = INITIAL_BACKOFF

    for attempt in range(MAX_RETRIES):
        try:
            r = session.get(
                API_URL,
                headers=HEADERS,
                params=params,
                timeout=TIMEOUT
            )

            r.raise_for_status()

            return r.json()

        except requests.exceptions.RequestException as e:
            logging.warning(
                "Request failed (attempt %d/%d): %s",
                attempt + 1,
                MAX_RETRIES,
                str(e)
            )

            if attempt == MAX_RETRIES - 1:
                logging.error(
                    "Max retries exceeded. Sleeping before retry cycle."
                )
                time.sleep(60)
                backoff = INITIAL_BACKOFF
            else:
                time.sleep(backoff)
                backoff *= 2