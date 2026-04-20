from collector import collect_random_articles, expand_from_articles

def main():
    seeds = collect_random_articles(n=10)
    expand_from_articles(seeds, max_new=1000)

if __name__ == "__main__":
    main()