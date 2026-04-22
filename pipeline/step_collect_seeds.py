import sys
from collector import collect_random_articles

import os
import re

def get_last_index(folder="data/raw"):
    files = os.listdir(folder)
    indices = []

    for f in files:
        match = re.match(r"(\d+)_", f)
        if match:
            indices.append(int(match.group(1)))

    return max(indices) + 1 if indices else 0

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    start = get_last_index()
    collect_random_articles(n=n, start=start)