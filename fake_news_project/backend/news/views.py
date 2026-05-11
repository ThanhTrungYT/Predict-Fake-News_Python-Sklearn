from django.shortcuts import render
from ml.predict import predict_text

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# 🔥 DRF
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def extract_article_from_url(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")

        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        domain = urlparse(url).netloc

        return text[:5000], domain

    except Exception:
        return None, None

def home(request):
    context = {}

    if request.method == "POST":
        text = request.POST.get("text")
        url = request.POST.get("url")

        if url:
            article_text, source = extract_article_from_url(url)

            if article_text:
                text = article_text
                context["source"] = source
                context["article"] = article_text
            else:
                context["error"] = "Không thể lấy nội dung từ URL này."

        if text:
            result = predict_text(text)

            context["prediction"] = result["label"]
            context["confidence"] = result["confidence"]

    return render(request, "index.html", context)

@api_view(["POST"])
def predict_api(request):
    text = request.data.get("text")
    url = request.data.get("url")

    source = None

    if url:
        article_text, source = extract_article_from_url(url)

        if not article_text:
            return Response(
                {"error": "Không thể lấy nội dung từ URL"},
                status=status.HTTP_400_BAD_REQUEST
            )

        text = article_text

    if not text:
        return Response(
            {"error": "Vui lòng nhập text hoặc URL"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🔥 Predict
    result = predict_text(text)

    return Response({
        "prediction": result["label"],
        "confidence": result["confidence"],
        "source": source,
        "text_preview": text[:300]
    })