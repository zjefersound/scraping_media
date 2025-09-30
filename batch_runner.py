from scraping import Youtube, Instagram, Tiktok, X
from utils import tools


def run_batch(usernames, strategy, save_imgs=False):
    tools.make_dir("dist")

    if strategy == "y":
        key = tools.read_settings("env.json").get("yt_api_key")
        scraper = Youtube(key)
    elif strategy == "i":
        scraper = Instagram()
    elif strategy == "t":
        scraper = Tiktok()
    elif strategy == "x":
        scraper = X()
    else:
        raise ValueError(f"Invalid strategy '{strategy}', must be one of 'y', 'i', 't', 'x'")

    for username in usernames:
        if not len(username):
            continue
        try:
            print(f"Running for {username} with strategy '{strategy}'...")

            if save_imgs:
                scraper.get(username, type="bs64")
            else:
                scraper.get(username, type="clean")

            scraper.save(username)
        except Exception:
            print(f"ERROR with: {username} - Skipping...")
            continue

if __name__ == "__main__":
    usernames = []
    run_batch(usernames, "y", save_imgs=True)
