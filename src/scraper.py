import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup

INPUT_FILE = "../data/Input.xlsx"
OUTPUT_DIR = "../articles"
FAILED_LOG = "../failed_urls.txt"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)
try:
    session.get("https://insights.blackcoffer.com/", timeout=15)
except Exception:
    pass

df = pd.read_excel(INPUT_FILE)
total = len(df)

with open(FAILED_LOG, "w", encoding="utf-8") as failed_file:
    for idx, row in df.iterrows():
        url_id = str(row["URL_ID"])
        url = str(row["URL"])
        count = idx + 1

        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            title_tag = soup.find("h1")
            title = title_tag.get_text(strip=True) if title_tag else ""

            content_div = (
                soup.find("div", class_="td-post-content")
                or soup.find("div", class_="entry-content")
                or soup.find("div", class_="post-content")
                or soup.find("article")
            )
            body = content_div.get_text(separator="\n", strip=True) if content_div else ""

            output_path = os.path.join(OUTPUT_DIR, f"{url_id}.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"{title}\n\n{body}")

            print(f"Done: {url_id} ({count}/{total})")

        except Exception as e:
            print(f"Failed: {url_id} ({count}/{total}) — {e}")
            failed_file.write(f"{url_id}\t{url}\n")

        time.sleep(1)
