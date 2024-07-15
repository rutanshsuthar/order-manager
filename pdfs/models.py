# pdfs/models.py
from django.db import models

from orders.models import Order


class PresignedURL(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="presigned_url")
    url = models.URLField()
    expiry_time = models.DateTimeField(default='2000-01-01 00:00:00.00000+00.00')

    def __str__(self):
        return f"Presigned URL for Order {self.order.id}"
