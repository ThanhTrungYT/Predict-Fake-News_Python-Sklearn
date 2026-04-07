import os
import joblib
import numpy as np

from pathlib import Path
from collections import Counter
from scipy.sparse import hstack

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

from data_loader import load_data_from_folder
from preprocessing import preprocess_series
from models import get_models
from evaluate import evaluate_model

BASE_DIR = Path(__file__).resolve().parent.parent.parent / "dataset_split"

TRAIN_DIR = BASE_DIR / "train"
TEST_DIR  = BASE_DIR / "test"

def extract_extra_features(text):
    words = text.split()

    len_text = len(words) 
    num_exclaim = text.count("!")
    num_upper = sum(1 for c in text if c.isupper())

    return [len_text, num_exclaim, num_upper]

def compute_source_scores(real_counts, fake_counts, alpha=5):
    source_scores = {}

    all_sources = set(real_counts.keys()).union(set(fake_counts.keys()))

    for src in all_sources:
        real = real_counts.get(src, 0)
        fake = fake_counts.get(src, 0)

        total = real + fake

        base_score = (real + alpha) / (total + 2 * alpha)

        confidence = min(1.0, total / 20) 

        score = base_score * confidence + 0.5 * (1 - confidence)

        score = max(0.2, min(0.8, score))

        source_scores[src] = score

    return source_scores
def main():
    data_train = load_data_from_folder(TRAIN_DIR, "TRAIN")
    data_test  = load_data_from_folder(TEST_DIR, "TEST")

    X_train_text = preprocess_series(data_train['text'])
    X_test_text  = preprocess_series(data_test['text'])

    y_train = data_train['label']
    y_test  = data_test['label']

    tfidf = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1, 3),
        min_df=5,
        max_df=0.95,
        sublinear_tf=True,
        norm='l2'
    )

    X_text_train = tfidf.fit_transform(X_train_text)
    X_text_test  = tfidf.transform(X_test_text)

    X_extra_train = np.array([extract_extra_features(t) for t in X_train_text])
    X_extra_test  = np.array([extract_extra_features(t) for t in X_test_text])

    scaler = StandardScaler()
    X_extra_train = scaler.fit_transform(X_extra_train)
    X_extra_test  = scaler.transform(X_extra_test)

    real_sources = data_train[data_train['label'] == 1]['source']
    fake_sources = data_train[data_train['label'] == 0]['source']

    real_counts = Counter(real_sources)
    fake_counts = Counter(fake_sources)

    source_scores_dict = compute_source_scores(real_counts, fake_counts)

    def get_source_score(src):
        return source_scores_dict.get(src, 0.5)

    X_source_train = np.array([
        get_source_score(s) for s in data_train['source']
    ]).reshape(-1, 1)

    X_source_test = np.array([
        get_source_score(s) for s in data_test['source']
    ]).reshape(-1, 1)

    X_train = hstack([X_text_train, X_extra_train, X_source_train])
    X_test  = hstack([X_text_test, X_extra_test, X_source_test])

    models = get_models(y_train)

    results = {}

    MODEL_DIR = Path(__file__).resolve().parent / "saved_models"
    MODEL_DIR.mkdir(exist_ok=True)

    for name, clf in models.items():
        print(f"\n{'='*60}")
        print(f"TRAINING: {name}")
        print(f"{'='*60}")

        try:
            clf.fit(X_train, y_train)

            y_pred = clf.predict(X_test)

            acc, f1 = evaluate_model(y_test, y_pred, name)

            results[name] = acc

            filename = MODEL_DIR / f"{name}.joblib"
            joblib.dump({
                "model": clf,
                "tfidf": tfidf,
                "scaler": scaler,
                "source_scores": source_scores_dict
            }, filename)

            print(f"✅ Saved: {filename}")

        except Exception as e:
            print(f"❌ Error with {name}: {e}")

    print("\n📊 MODEL COMPARISON")
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    for name, acc in sorted_results:
        print(f"{name}: {acc:.4f}")

    if sorted_results:
        best = sorted_results[0]
        print(f"\n🏆 Best Model: {best[0]} ({best[1]:.4f})")

if __name__ == "__main__":
    main()