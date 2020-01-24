import re
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk import stem
import unicodedata

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('portuguese'))
stemmer = stem.RSLPStemmer()


def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")

    return str(text)


def preprocess_text(text):
    text = text.lower()

    text = strip_accents(text)
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub(' ', text)
    text = re.sub(r'[\n]{2,}', " ", text)
    text = re.sub(r'[ ]{2,}', " ", text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)

    return text


def preprocess_stemming_text(text):
    text = text.lower()

    text = strip_accents(text)
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub(' ', text)
    text = re.sub(r'[\n]{2,}', " ", text)
    text = re.sub(r'[ ]{2,}', " ", text)
    text = ' '.join(stemmer.stem(word)
                    for word in text.split() if word not in STOPWORDS)

    return text
