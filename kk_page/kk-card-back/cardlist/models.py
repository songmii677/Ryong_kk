from django.db import models
from django.conf import settings


class Card(models.Model):
    company = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=100, default="")

    card_type = models.CharField(max_length=30, blank=True, default="")
    target = models.CharField(max_length=50, blank=True, default="")

    annual_fee = models.JSONField(default=dict, blank=True)
    benefits = models.JSONField(default=dict, blank=True)

    image_url = models.URLField(max_length=500, blank=True, default="")
    detail_url = models.URLField(max_length=500, blank=True, default="")

    class Meta:
        ordering = ["company", "name"]

    def __str__(self):
        return f"{self.company} - {self.name}"
    
class RecommendResult(models.Model):
    persona_title = models.CharField(max_length=100)
    persona_description = models.TextField(blank=True)
    card_list = models.ManyToManyField(
        Card,
        related_name="recommend_results",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recommend_results",
    )
    class Meta:
        ordering = ["-id"]
    def __str__(self):
        return f"{self.user.username} - {self.persona_title}"