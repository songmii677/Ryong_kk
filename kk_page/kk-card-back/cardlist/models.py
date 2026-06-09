from django.db import models


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