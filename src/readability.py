import re
import string
import nltk
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords as nltk_stopwords

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
    words = set(nltk_stopwords.words("english"))
    for path in STOPWORD_FILES:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                word = line.split("|")[0].strip().lower()
                if word:
                    words.add(word)
    return words

STOPWORDS = _load_stopwords()


def _syllable_count(word):
    word = word.lower()
    if len(word) > 3 and (word.endswith("es") or word.endswith("ed")):
        word = word[:-2]
    count = len(re.findall(r"[aeiou]", word))
    return max(1, count)


def analyze_readability(text):
    sentences = sent_tokenize(text)
    num_sentences = max(len(sentences), 1)

    all_tokens = word_tokenize(text)
    words = [t for t in all_tokens if t not in string.punctuation and re.search(r"[a-zA-Z]", t)]
    num_words = max(len(words), 1)

    avg_sentence_length = num_words / num_sentences

    syllables = [_syllable_count(w) for w in words]
    complex_word_count = sum(1 for s in syllables if s > 2)
    percentage_complex_words = complex_word_count / num_words
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    cleaned = [w for w in words if w.lower() not in STOPWORDS]
    word_count = len(cleaned)

    syllable_per_word = sum(syllables) / num_words

    pronoun_matches = re.findall(r"\b(I|we|my|ours|us)\b", text, re.IGNORECASE)
    personal_pronouns = sum(1 for m in pronoun_matches if not (m.upper() == "US" and m.isupper()))

    avg_word_length = sum(len(w) for w in words) / num_words

    return {
        "avg_sentence_length": avg_sentence_length,
        "complex_word_count": complex_word_count,
        "percentage_complex_words": percentage_complex_words,
        "fog_index": fog_index,
        "avg_words_per_sentence": avg_sentence_length,
        "word_count": word_count,
        "syllable_per_word": syllable_per_word,
        "personal_pronouns": personal_pronouns,
        "avg_word_length": avg_word_length,
    }
