from django.db import models


class Customer(models.Model):
    name = models.TextField()
    phone_number = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
