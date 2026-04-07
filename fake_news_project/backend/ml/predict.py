import joblib
import os

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "saved_models", "fake_news_logisticregression_pipeline.joblib")

model = joblib.load(model_path)


def predict_text(text):
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]

    confidence = max(probabilities) * 100

    if prediction == 1:
        label = "Real News"
    else:
        label = "Fake News"

    return {
        "label": label,
        "confidence": round(confidence, 2)
    }