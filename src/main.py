import os
import pandas as pd
from sentiment import analyze_sentiment
from readability import analyze_readability

INPUT_FILE = "../data/Input.xlsx"
ARTICLES_DIR = "../articles"
OUTPUT_FILE = "../data/Output.xlsx"

COLUMNS = [
    "URL_ID", "URL",
    "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
    "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX",
    "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT", "WORD COUNT",
    "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH",
]

df = pd.read_excel(INPUT_FILE)
total = len(df)
rows = []

for idx, row in df.iterrows():
    url_id = str(row["URL_ID"])
    url = str(row["URL"])
    filepath = os.path.join(ARTICLES_DIR, f"{url_id}.txt")

    if not os.path.exists(filepath):
        rows.append([url_id, url] + [0] * 13)
        print(f"Missing: {url_id} ({idx + 1}/{total})")
        continue

    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    s = analyze_sentiment(text)
    r = analyze_readability(text)

    rows.append([
        url_id, url,
        s["positive_score"],
        s["negative_score"],
        s["polarity_score"],
        s["subjectivity_score"],
        r["avg_sentence_length"],
        r["percentage_complex_words"],
        r["fog_index"],
        r["avg_words_per_sentence"],
        r["complex_word_count"],
        r["word_count"],
        r["syllable_per_word"],
        r["personal_pronouns"],
        r["avg_word_length"],
    ])

    print(f"Processed: {url_id} ({idx + 1}/{total})")

output_df = pd.DataFrame(rows, columns=COLUMNS)
output_df.to_excel(OUTPUT_FILE, index=False)
print(f"\nSaved to {OUTPUT_FILE}")
