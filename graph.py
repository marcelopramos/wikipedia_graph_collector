import os
import json
import time
import pickle
import networkx as nx

SEED_DIR = "data/seed"
EXPANDED_DIR = "data/expanded"

OUTPUT_DIR = "graph"
GRAPHML_FILE = os.path.join(OUTPUT_DIR, "wikipedia.graphml")
GEXF_FILE = os.path.join(OUTPUT_DIR, "wikipedia.gexf")
PICKLE_FILE = os.path.join(OUTPUT_DIR, "wikipedia.gpickle")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_json_files(folder):
    return sorted(
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".json")
    )


def normalize_categories(categories):
    out = []
    for c in categories:
        if isinstance(c, dict):
            t = c.get("title")
            if t:
                out.append(t.replace("Category:", ""))
        elif isinstance(c, str):
            out.append(c)
    return out


def normalize_links(links):
    out = []
    for l in links:
        if isinstance(l, dict):
            t = l.get("title")
            if t:
                out.append(t)
        elif isinstance(l, str):
            out.append(l)
    return out


def fmt_time(s):
    m = int(s // 60)
    s = int(s % 60)
    return f"{m:02d}:{s:02d}"


def progress(i, total, start, label):
    elapsed = time.time() - start
    speed = i / elapsed if elapsed else 0
    eta = (total - i) / speed if speed else 0
    print(
        f"[{label}] {i}/{total} | "
        f"elapsed {fmt_time(elapsed)} | "
        f"eta {fmt_time(eta)} | "
        f"{speed:.1f} f/s"
    )


def build_graph():
    t0 = time.time()
    G = nx.DiGraph()
    G.graph["dataset"] = "Wikipedia crawl"

    files = list_json_files(SEED_DIR) + list_json_files(EXPANDED_DIR)
    total = len(files)

    print(f"Total files: {total}")

    # -------------------------
    # PASS 1: COLLECT NODES ONLY
    # -------------------------
    nodes_data = {}

    t1 = time.time()

    for i, path in enumerate(files, 1):
        try:
            page = load_json(path)
            title = page.get("title")
            if not title:
                continue

            nodes_data[title] = {
                "pageid": page.get("pageid", -1),
                "categories": "|".join(
                    normalize_categories(page.get("categories", []))
                ),
                "links": normalize_links(page.get("links", []))
            }

        except Exception as e:
            print(f"[node error] {path}: {e}")

        if i % 1000 == 0:
            progress(i, total, t1, "scan")

    # add nodes safely
    for title, data in nodes_data.items():
        G.add_node(title, pageid=data["pageid"], categories=data["categories"])

    print(f"Nodes: {G.number_of_nodes()}")

    # -------------------------
    # PASS 2: ADD EDGES ONLY BETWEEN EXISTING NODES
    # -------------------------
    t2 = time.time()

    for i, (title, data) in enumerate(nodes_data.items(), 1):

        for link in data["links"]:
            if link in nodes_data:   # IMPORTANT FIX
                G.add_edge(title, link)

        if i % 1000 == 0:
            progress(i, len(nodes_data), t2, "edges")

    print(f"Edges: {G.number_of_edges()}")

    # -------------------------
    # SAVE (GraphML required by professor)
    # -------------------------
    print("Saving GraphML...")
    t3 = time.time()
    nx.write_graphml(G, GRAPHML_FILE)
    print(f"GraphML saved in {fmt_time(time.time() - t3)}")

    print("Saving GEXF...")
    t4 = time.time()
    nx.write_gexf(G, GEXF_FILE)
    print(f"GEXF saved in {fmt_time(time.time() - t4)}")

    print("Saving Pickle (fast reload)...")
    t5 = time.time()
    with open(PICKLE_FILE, "wb") as f:
        pickle.dump(G, f)
    print(f"Pickle saved in {fmt_time(time.time() - t5)}")

    print(f"TOTAL TIME: {fmt_time(time.time() - t0)}")
    print(f"FINAL → Nodes: {G.number_of_nodes()} | Edges: {G.number_of_edges()}")

