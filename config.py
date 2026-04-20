import os
from dotenv import load_dotenv

load_dotenv()

WIKI_USER_AGENT = os.getenv("WIKI_USER_AGENT")

API_URL = "https://en.wikipedia.org/w/api.php"

REQUEST_SLEEP = float(os.getenv("REQUEST_SLEEP", 0.5))

MAX_LINKS = int(os.getenv("MAX_LINKS", 500))
