import re
import string
import nltk
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
from nltk.tokenize import word_tokenize

STOPWORD_FILES = [
    "../dictionaries/StopWords_Generic.txt",
    "../dictionaries/StopWords_GenericLong.txt",
    "../dictionaries/StopWords_Names.txt",
    "../dictionaries/StopWords_Auditor.txt",
    "../dictionaries/StopWords_Geographic.txt",
    "../dictionaries/StopWords_Currencies.txt",
    "../dictionaries/StopWords_DatesandNumbers.txt",
]

def _load_stopwords():
    words = set()
    for path in STOPWORD_FILES:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.split("|")[0].strip().lower()
                if word:
                    words.add(word)
    return words

def _load_word_list(path, stopwords):
    words = set()
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            word = line.strip().lower()
            if word and word not in stopwords:
                words.add(word)
    return words

STOPWORDS = _load_stopwords()
POSITIVE_WORDS = _load_word_list("../dictionaries/positive-words.txt", STOPWORDS)
NEGATIVE_WORDS = _load_word_list("../dictionaries/negative-words.txt", STOPWORDS)


def analyze_sentiment(text):
    tokens = word_tokenize(text.lower())
    cleaned = [
        t.strip(string.punctuation)
        for t in tokens
        if t not in string.punctuation
    ]
    cleaned = [t for t in cleaned if t and t not in STOPWORDS]

    positive_score = sum(1 for t in cleaned if t in POSITIVE_WORDS)
    negative_score = sum(1 for t in cleaned if t in NEGATIVE_WORDS)
    total = len(cleaned)

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (total + 0.000001)

    return {
        "positive_score": positive_score,
        "negative_score": negative_score,
        "polarity_score": polarity_score,
        "subjectivity_score": subjectivity_score,
    }
