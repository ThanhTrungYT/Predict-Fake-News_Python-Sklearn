import joblib
import os
import math
import numpy as np

from scipy.sparse import hstack

model = None
vectorizer = None
scaler = None
source_scores = None

def extract_extra_features(text):
    words = text.split()

    len_text = len(words)
    num_exclaim = text.count("!")
    num_upper = sum(1 for c in text if c.isupper())

    return [len_text, num_exclaim, num_upper]

def load_model():
    global model, vectorizer, scaler, source_scores

    if model is not None:
        return  # đã load rồi thì bỏ qua

    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "saved_models", "LinearSVM.joblib")

    print("📦 Loading model from:", model_path)

    if not os.path.exists(model_path):
        raise Exception(f"Model file not found: {model_path}")

    loaded = joblib.load(model_path)
    print("🔍 Loaded type:", type(loaded))

    if isinstance(loaded, dict):
        print("📦 Dict keys:", loaded.keys())

        if "model" not in loaded:
            raise Exception("File joblib không chứa key 'model'")

        model = loaded["model"]
        vectorizer = loaded.get("tfidf") or loaded.get("vectorizer")
        scaler = loaded.get("scaler")
        source_scores = loaded.get("source_scores", {})

    else:
        # Trường hợp load trực tiếp pipeline
        model = loaded
        vectorizer = None
        scaler = None
        source_scores = {}

    if not hasattr(model, "predict"):
        raise Exception("Object được load không có hàm predict()")

def predict_text(text, source=""):
    load_model()

    if not text or not text.strip():
        raise ValueError("Text đầu vào đang rỗng")

    text = text.strip()
    source = (source or "").strip()

    if vectorizer is None:
        raise Exception("Không tìm thấy TF-IDF/vectorizer trong file model")

    # 1. TF-IDF feature
    X_text = vectorizer.transform([text])

    # 2. Extra features
    X_extra = np.array([extract_extra_features(text)], dtype=float)

    if scaler is not None:
        X_extra = scaler.transform(X_extra)

    # 3. Source score feature
    source_score = source_scores.get(source, 0.5)
    X_source = np.array([[source_score]], dtype=float)

    # 4. Ghép toàn bộ feature giống train.py
    X_input = hstack([X_text, X_extra, X_source])

    try:
        prediction = model.predict(X_input)[0]
    except Exception as e:
        raise Exception(f"❌ Lỗi khi predict: {str(e)}")

    confidence = 0.0

    try:
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(X_input)[0]
            confidence = max(probs) * 100

        elif hasattr(model, "decision_function"):
            score = model.decision_function(X_input)
            score = score[0] if hasattr(score, "__len__") else score
            confidence = (1 / (1 + math.exp(-abs(float(score))))) * 100

    except Exception as e:
        print("⚠️ Lỗi confidence:", e)

    label = "Real News" if prediction == 1 else "Fake News"

    return {
        "label": label,
        "confidence": round(min(confidence, 100), 2)
    }