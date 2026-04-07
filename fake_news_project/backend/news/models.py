from django.db import models

# Create your models here.
from django.db import models


class DetectionHistory(models.Model):
    url = models.TextField(blank=True, null=True)
    content = models.TextField()
    prediction = models.CharField(max_length=50)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"