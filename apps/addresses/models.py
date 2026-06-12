from django.db import models
from django.conf import settings


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="addresses", on_delete=models.CASCADE
    )
    complement = models.TextField(blank=True, null=True)
    number = models.IntegerField()
    street = models.CharField(max_length=255)
    neighborhood = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=8)
    is_main = models.BooleanField(default=False)
