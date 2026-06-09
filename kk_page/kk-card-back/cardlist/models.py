from django.db import models


class Card(models.Model):
    company = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=30, blank=True)
    target = models.CharField(max_length=50, blank=True)

    annual_fee = models.JSONField(default=dict, blank=True)
    benefits = models.JSONField(default=dict, blank=True)

    image_url = models.URLField(max_length=500, blank=True)
    detail_url = models.URLField(max_length=500, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["company", "name"]

    def __str__(self):
        return f"{self.company} - {self.name}"