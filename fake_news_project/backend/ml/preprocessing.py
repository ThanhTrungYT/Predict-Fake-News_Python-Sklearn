import re
import string
from underthesea import word_tokenize

def clean_text(text):
    text = str(text).lower().strip()
    text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
    text = re.sub(r'<.*?>+', ' ', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    text = re.sub(r'\w*\d\w*', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = word_tokenize(text, format="text")
    return text
def preprocess_series(series):
    return series.fillna('').apply(clean_text)